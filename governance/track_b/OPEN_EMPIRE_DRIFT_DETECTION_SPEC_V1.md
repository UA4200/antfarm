# OPEN EMPIRE — AUTONOMOUS DRIFT DETECTION SPEC V1
## Foundational Enhancement #10: Drift Detection

**Status:** SPEC  
**Version:** 1.0.0  
**Created:** 2026-08-06  
**Operator:** Nathan Asiegbu  
**Governed by:** Open Empire Constitution v2, Governance Baseline v1.0.0 (commit 17df0ff)

---

## 1. What Is Drift?

**Drift** is any divergence between the expected state of Open Empire (as defined in governance artifacts, registries, and last-known-good baselines) and the actual live state of the system.

Drift is not always malicious — it happens naturally through:
- Manual operations that bypass governance (emergency fixes)
- Failed deployments that leave partial state
- Dependency updates that change behavior
- Bugs that cause processes to stop or behave unexpectedly

**The goal of drift detection is not to prevent drift — it is to make drift instantly visible.**

---

## 2. Drift Detection Architecture

```
[Detection Script]  →  [Drift Report]  →  [Alert Router]  →  [Telegram]
   (per layer)            (JSON)           (n8n WF-005)       (Nathan)
```

**Drift detector:** `~/.openclaw/workspace/governance/scripts/drift_detector.py`  
**Schedule:** Every 5 minutes (cron via PM2)  
**Output:** `~/.openclaw/workspace/governance/drift_report.json`  
**Alert channel:** Telegram (primary)

---

## 3. Six-Layer Drift Detection

### Layer 1 — Governance Drift

**What it detects:** Unauthorized modifications to canonical governance artifacts.

**Detection method:**
```bash
# Compare live SHA256 against baseline SHA256SUMS
shasum -a 256 -c ~/.openclaw/workspace/governance/SHA256SUMS 2>&1
```

**Files monitored:**
- `OPEN_EMPIRE_CONSTITUTION_V2.md`
- `GOVERNANCE_BASELINE_V1.md`
- `SHA256SUMS` itself
- All Track B spec files
- `AGENTS.md`
- `RUNTIME_REGISTRY_V1.json`

**Drift threshold:** Any mismatch = DRIFT DETECTED (zero tolerance)

**Alert channel:** Telegram — P0 CRITICAL

**Remediation action:**
1. Alert Nathan immediately.
2. Show diff of changed file (if detectable).
3. Prompt: restore from last known-good commit, or acknowledge as authorized change.
4. If unauthorized change confirmed: treat as security incident.

**Current known drift (2026-08-06):**
- None in governance artifacts. SHA256SUMS baseline is being established in this Track B pass.

---

### Layer 2 — Registry Drift

**What it detects:** Assets present in the live runtime that are not registered, or registered assets that are no longer present.

**Detection method:**
```python
import json
import subprocess

# Live PM2 processes
pm2_result = subprocess.run(["pm2", "jlist"], capture_output=True, text=True)
live_procs = {p["name"] for p in json.loads(pm2_result.stdout)}

# Registry
with open("RUNTIME_REGISTRY_V1.json") as f:
    registry = json.load(f)
registered_procs = {s["name"] for s in registry["services"]}

unregistered = live_procs - registered_procs      # Running but not registered
missing = registered_procs - live_procs            # Registered but not running
```

**Drift threshold:**
- Unregistered running process: DRIFT (P1 HIGH)
- Registered ACTIVE process not running: DRIFT (P1 HIGH)
- Registered STOPPED/PAUSED process not running: EXPECTED (no alert)

**Alert channel:** Telegram — P1 HIGH

**Remediation action:**
1. For unregistered: prompt Nathan to register via checklist or mark as emergency bypass.
2. For missing ACTIVE: check logs, attempt restart if appropriate, alert Nathan.

**Current known drift (2026-08-06):**
- PM IDs 33, 34, 35: `open-empire-federation-staging`, `open-empire-lifecycle-staging`, `dynamics51` — STOPPED with high restart counts. These processes are in a state not matching expected HEALTHY registry status.
- AGENTS.md documents stale PM2 IDs (noted in Gate A) — some PM2 IDs in AGENTS.md differ from live pm2 ID assignments. Registry reconciliation required.
- **Action:** Register all with status DEGRADED/STOPPED as part of Track B Phase 1.

---

### Layer 3 — Repository Drift

**What it detects:** Local repository divergence from the UA4200 GitHub `main` branch.

**Detection method:**
```bash
# For each tracked repo
cd ~/.openclaw/workspace
git fetch origin main 2>/dev/null
BEHIND=$(git rev-list HEAD..origin/main --count)
AHEAD=$(git rev-list origin/main..HEAD --count)

echo "Behind: $BEHIND, Ahead: $AHEAD"
```

**Repos to monitor:**

| Repo Path | Remote | Branch |
|-----------|--------|--------|
| `~/.openclaw/workspace` | UA4200/open-empire | main |
| `~/.openclaw/trading` | UA4200/trading | main |
| `~/.openclaw/workspace/mission-control` | UA4200/mission-control | main |
| `~/.openclaw/alusi` | UA4200/alusi | main |
| `~/.openclaw/blco` | UA4200/blco | main |
| `~/.openclaw/hyrvea` | UA4200/hyrvea | main |

**Drift threshold:**
- Local is BEHIND remote: DRIFT (P2 MEDIUM) — undeployed changes exist
- Local is AHEAD of remote: DRIFT (P2 MEDIUM) — uncommitted local changes
- Diverged (both ahead and behind): DRIFT (P1 HIGH) — merge conflict risk

**Alert channel:** Telegram — P2 MEDIUM

**Remediation action:**
1. If behind: pull latest, run validation, deploy.
2. If ahead: commit and push or discard local changes.
3. If diverged: Nathan manual review required.

**Current known drift (2026-08-06):**
- Repository sync status not yet measured. Baseline measurement required in first drift detector run.

---

### Layer 4 — Runtime Drift

**What it detects:** Discrepancy between the expected PM2 process list and what `pm2 jlist` reports.

**Detection method:**
```python
# Expected: all processes in registry with status ACTIVE|ONLINE
expected_online = {
    s["name"] for s in registry["services"]
    if s["status"] in ("ACTIVE", "ONLINE")
}

# Actual online
actual_online = {
    p["name"] for p in pm2_processes
    if p["status"] == "online"
}

# Process that should be online but isn't
not_running = expected_online - actual_online

# Process that is online but registry says it shouldn't be
unexpected_online = {
    p["name"] for p in pm2_processes
    if p["status"] == "online"
    and registry.get(p["name"], {}).get("status") in ("STOPPED", "PAUSED", "DEPRECATED")
}
```

**Drift threshold:**
- Expected ACTIVE process not online: DRIFT (P1 HIGH)
- DEPRECATED/STOPPED process running: DRIFT (P2 MEDIUM)
- Restart count > 5 in last hour: WARNING (P2)

**Alert channel:** Telegram — P1 HIGH / P2 MEDIUM

**Remediation action:**
1. For not-running ACTIVE: check logs for crash reason, restart if safe.
2. For unexpected online DEPRECATED: investigate, stop if confirmed stale.
3. For high restarts: examine error logs, report to Nathan.

**Current known drift (2026-08-06):**
- PM2 processes 45 and 46 (open-empire-federation-staging, open-empire-lifecycle-staging) are ONLINE per PM2 but have high restart counts — classified as DEGRADED rather than healthy ONLINE. Drift from expected healthy state.

---

### Layer 5 — Infrastructure Drift

**What it detects:** Unexpected changes to port bindings, loopback policy violations, or missing expected ports.

**Detection method:**
```bash
# Get all listening ports
lsof -iTCP -sTCP:LISTEN -n -P | awk '{print $9}' | sort -u

# Check for non-loopback bindings (policy violation)
lsof -iTCP -sTCP:LISTEN -n -P | grep -v '127.0.0.1' | grep -v '::1' | grep -v '*'
```

**Expected port bindings:**

| Port | Service | Expected Binding |
|------|---------|-----------------|
| 3333 | mission-control | 127.0.0.1 |
| 5432 | clawdb (PostgreSQL) | 127.0.0.1 |
| 11434 | ollama | 127.0.0.1 |
| 3001 | grafana | 127.0.0.1 |
| 8038 | cashclaw_director /health | 127.0.0.1 (target) |
| 8039 | cashclaw_arb /health | 127.0.0.1 (target) |
| 8040 | polymarket-trader /health | 127.0.0.1 (target) |
| 8041 | trading_sentinel /health | 127.0.0.1 (target) |

**Drift threshold:**
- Non-loopback binding detected: CRITICAL DRIFT (P0) — security violation
- Expected port not bound: DRIFT (P1 HIGH) — service may be down
- Unexpected new port: DRIFT (P2 MEDIUM) — investigate

**Alert channel:** Telegram — P0 CRITICAL for non-loopback violations

**Remediation action:**
1. Non-loopback: Immediate alert, identify service, kill if unauthorized.
2. Missing expected port: Check if service is stopped, restart if appropriate.
3. Unexpected port: Identify owning process (`lsof -i :<port>`), register or stop.

**Current known drift (2026-08-06):**
- Port 3001 (Grafana): Status unknown. May or may not be bound. Baseline measurement needed.
- Health endpoint ports (8038–8041): Not yet bound (health endpoints not yet built — Observability Spec Phase 2 prereq).

---

### Layer 6 — Configuration Drift

**What it detects:** Changes to PM2 ecosystem config files or critical environment variable values relative to last-known-good baseline.

**Detection method:**
```bash
# Hash ecosystem config files
sha256sum ~/.openclaw/workspace/ecosystem*.config.js \
          ~/.openclaw/trading/ecosystem*.config.js \
          ~/.openclaw/moltlaunch/ecosystem*.config.js 2>/dev/null
```

**Config files to monitor:**

| Config File | Service Class |
|------------|---------------|
| `~/.openclaw/workspace/ecosystem.config.js` | Core infrastructure |
| `~/.openclaw/trading/ecosystem.config.js` | Trading agents |
| `~/.openclaw/moltlaunch/ecosystem.config.js` | Legacy moltlaunch |

**Critical env vars to spot-check (not log values):**

| Variable | Check |
|----------|-------|
| `CASHCLAW_DAILY_SPEND_CAP_USD` | Must equal "10" |
| `ARB_DAILY_SPEND_CAP_USD` | Must equal "10" |
| `POLY_DAILY_SPEND_CAP_USD` | Must equal "10" |
| `ARB_DRY_RUN` | Must equal "false" in production |
| `OPENCLAW_MODE` | Must equal "production" |

**Drift threshold:**
- Ecosystem config SHA256 changed: DRIFT (P1 HIGH)
- Spend cap env var changed from expected: DRIFT (P0 CRITICAL) — safety violation
- OPENCLAW_MODE not "production": DRIFT (P1 HIGH)

**Alert channel:** Telegram — P0 CRITICAL for spend cap changes

**Remediation action:**
1. Config hash changed: Show diff, prompt Nathan to confirm or restore.
2. Spend cap changed: IMMEDIATE alert, restore correct value, restart affected service.
3. Mode mismatch: Alert Nathan, investigate.

**Current known drift (2026-08-06):**
- Ecosystem config SHA256 baselines not yet established. First drift run will create baselines.
- All spend caps confirmed correct per AGENTS.md: CASHCLAW_DAILY_SPEND_CAP_USD=10, ARB_DAILY_SPEND_CAP_USD=10, POLY_DAILY_SPEND_CAP_USD=10.

---

## 4. Drift Report Schema

```json
{
  "report_id": "drift-2026-08-06T12:00:00Z",
  "generated_at": "2026-08-06T12:00:00Z",
  "operator": "Nathan Asiegbu",
  "overall_drift_detected": true,
  "drift_count": 3,
  "layers": {
    "governance": {
      "status": "CLEAN",
      "checked_at": "2026-08-06T12:00:00Z",
      "drift_items": []
    },
    "registry": {
      "status": "DRIFT",
      "checked_at": "2026-08-06T12:00:00Z",
      "drift_items": [
        {
          "type": "UNREGISTERED_PROCESS",
          "name": "new-mystery-service",
          "pm2_id": 99,
          "severity": "P1",
          "action": "Register or stop"
        }
      ]
    },
    "repository": {
      "status": "UNKNOWN",
      "checked_at": "2026-08-06T12:00:00Z",
      "drift_items": [],
      "note": "Baseline not yet established"
    },
    "runtime": {
      "status": "DRIFT",
      "checked_at": "2026-08-06T12:00:00Z",
      "drift_items": [
        {
          "type": "DEGRADED_PROCESS",
          "name": "open-empire-federation-staging",
          "pm2_id": 45,
          "restart_count": 47,
          "severity": "P2"
        }
      ]
    },
    "infrastructure": {
      "status": "UNKNOWN",
      "checked_at": "2026-08-06T12:00:00Z",
      "note": "Baseline not yet established. Run lsof to create."
    },
    "configuration": {
      "status": "UNKNOWN",
      "checked_at": "2026-08-06T12:00:00Z",
      "note": "Ecosystem config SHA256 baselines not yet created."
    }
  }
}
```

---

## 5. Drift Detector Implementation Schedule

### Phase 1 — Layers 1 + 4 (Registry + Runtime) — Days 1–3
*Lowest complexity, highest value for trading safety.*

| Task | Acceptance Criteria |
|------|---------------------|
| Build `drift_detector.py` with Layer 1 (governance SHA256) | Corrupt a file → detect drift |
| Add Layer 4 (runtime vs registry) | Stop a process → detect as missing ACTIVE |
| Wire to Telegram via n8n WF-005 | Alert fires within 5 min of drift |
| PM2 cron: `*/5 * * * *` | Runs every 5 min, logs output |

### Phase 2 — Layers 2 + 6 (Registry + Config) — Days 4–7

| Task | Acceptance Criteria |
|------|---------------------|
| Add Layer 2 (unregistered processes) | Start test service → detect unregistered |
| Add Layer 6 (ecosystem config hash) | Edit ecosystem config → detect change |
| Create baseline SHA256 for ecosystem configs | Hash stored in governance/ |

### Phase 3 — Layers 3 + 5 (Repo + Infrastructure) — Days 8–14

| Task | Acceptance Criteria |
|------|---------------------|
| Add Layer 3 (git repo divergence) | Diverge local branch → detect |
| Add Layer 5 (port bindings) | Start service on non-loopback → P0 alert |
| Establish infrastructure baseline | Expected ports documented + hashed |

---

## 6. Drift Baseline Establishment Checklist

Before drift detection goes live, these baselines must be created:

```
[ ] SHA256SUMS for all governance artifacts (Layer 1 baseline)
[ ] Runtime Registry accurately reflects all 42 PM2 processes (Layer 2+4 baseline)
[ ] SHA256 of each ecosystem.config.js captured (Layer 6 baseline)
[ ] lsof port map snapshot taken and saved as infrastructure_baseline.json (Layer 5 baseline)
[ ] git fetch run on all 6 repos, behind/ahead counts logged (Layer 3 baseline)
```

---

## 7. Known Drift Summary (2026-08-06)

| Layer | Status | Details |
|-------|--------|---------|
| Governance | UNKNOWN | SHA256 baselines being established |
| Registry | DRIFT | PM IDs 33,34,35 STOPPED with high restarts; AGENTS.md stale IDs |
| Repository | UNKNOWN | Baseline measurement not yet run |
| Runtime | DRIFT | PM2 45,46 degraded (high restarts); pm2 ID list in AGENTS.md partially stale |
| Infrastructure | UNKNOWN | Grafana port 3001 status unknown |
| Configuration | UNKNOWN | Ecosystem config baselines not yet captured |

---

## 8. Integration Points

- **Digital Twin (Enhancement #8):** `drift_report.json` feeds `current_state.drift_detected`
- **Event-Driven Ops (Enhancement #7):** `GOVERNANCE_CHANGE` event fires on Layer 1 drift
- **Observability Spec (Enhancement #2):** Health endpoints enable Layer 4 enrichment
- **Registry-First Policy (Enhancement #6):** Layer 2 enforces registration requirement

---

## 9. References

- Open Empire Constitution v2
- Governance Baseline v1.0.0 — commit 17df0ff
- SHA256SUMS — `~/.openclaw/workspace/governance/SHA256SUMS`
- RUNTIME_REGISTRY_V1.json
- AGENTS.md
