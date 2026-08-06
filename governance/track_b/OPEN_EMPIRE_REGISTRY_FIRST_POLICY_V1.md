# OPEN EMPIRE — REGISTRY-FIRST ARCHITECTURE POLICY V1
## Foundational Enhancement #6: Registry-First Architecture

**Status:** ACTIVE — ENFORCED AS OF 2026-08-06  
**Version:** 1.0.0  
**Created:** 2026-08-06  
**Operator:** Nathan Asiegbu  
**Governed by:** Open Empire Constitution v2, Governance Baseline v1.0.0 (commit 17df0ff)

---

## 1. Principle

> **Nothing enters Open Empire production without registration.**

All assets — services, agents, capabilities, repositories, databases, governance documents — must exist in the Open Empire Master Registry with a valid UUID before they are deployed, started, or activated.

This is not bureaucracy. It is the foundation of observability, drift detection, spend governance, and autonomous operations. An unregistered asset is an unmonitored asset. An unmonitored asset is a liability.

---

## 2. What Requires Registration

| Asset Class | Examples | Registry Target |
|-------------|----------|-----------------|
| PM2 Services | Any `pm2 start` | RUNTIME_REGISTRY_V1.json |
| Agents | Any autonomous agent | AGENTS.md + Master Registry |
| Capabilities | New skill/capability | Knowledge Graph + Master Registry |
| Repositories | New code directory | ASSET_UUID_REGISTRY_V1.json |
| Databases | New DB/SQLite file used by a service | ASSET_UUID_REGISTRY_V1.json |
| Governance Documents | Any new canonical policy doc | SHA256SUMS + Master Registry |
| External API Keys | Any new secret | SECRETS_GOVERNANCE_V1.json |
| Cron Jobs | Any new PM2 cron entry | RUNTIME_REGISTRY_V1.json |
| n8n Workflows | Any new automation workflow | Master Registry |

---

## 3. Pre-Production Registration Checklist

Before any asset goes to production, ALL of the following must be true:

```
[ ] UUID assigned (uuid5 from Open Empire namespace)
[ ] Registered in Master Registry (OPEN_EMPIRE_MASTER_REGISTRY.json)
[ ] Human ID assigned (OE-<TYPE>-<NNNN> format)
[ ] Capability defined (what problem does this asset solve?)
[ ] Owner assigned (Nathan Asiegbu or delegated)
[ ] Parent portfolio/program identified
[ ] Daily spend cap declared (if financial operations involved)
[ ] Governance review completed (Nathan explicit approval for new agents/financial services)
[ ] Health endpoint defined (HTTP services) or health check method documented
[ ] Secrets declared in SECRETS_GOVERNANCE_V1.json (if new API keys required)
[ ] Draft registered in ASSET_UUID_REGISTRY_V1.json
```

**Checklist template file:** `REGISTRY_ENTRY_TEMPLATE.json` (see Section 7)

---

## 4. Enforcement Mechanism

### 4.1 exec-gateway Pre-Deployment Check

The `exec-gateway` service (PM2 id 13) MUST check the runtime registry before approving any `pm2 start` command.

**Enforcement logic (target implementation):**

```python
# exec_gateway/registry_check.py

import json
import os

RUNTIME_REGISTRY_PATH = os.path.expanduser(
    "~/.openclaw/workspace/governance/RUNTIME_REGISTRY_V1.json"
)

def check_registry_before_start(service_name: str) -> dict:
    """
    Returns: {"approved": bool, "reason": str, "uuid": str | None}
    """
    with open(RUNTIME_REGISTRY_PATH) as f:
        registry = json.load(f)
    
    registered = {s["name"]: s for s in registry.get("services", [])}
    
    if service_name not in registered:
        return {
            "approved": False,
            "reason": f"Service '{service_name}' not found in Runtime Registry. "
                      "Register it first or request emergency bypass.",
            "uuid": None
        }
    
    entry = registered[service_name]
    if entry.get("status") == "DEPRECATED":
        return {
            "approved": False,
            "reason": f"Service '{service_name}' is DEPRECATED in registry. "
                      "Cannot start deprecated services without governance review.",
            "uuid": entry["uuid"]
        }
    
    return {
        "approved": True,
        "reason": "Registry check passed",
        "uuid": entry["uuid"]
    }
```

### 4.2 Current Enforcement State (2026-08-06)

As of Governance Baseline v1.0.0, enforcement is **advisory** (log + Telegram alert on violation).  
**Target Phase 2:** Hard block — exec-gateway rejects unapproved `pm2 start` commands.

| Phase | State | Date |
|-------|-------|------|
| Phase 1 (current) | Advisory — log violations, Telegram alert | 2026-08-06 |
| Phase 2 (target) | Soft block — Nathan approval required for unregistered | TBD |
| Phase 3 (target) | Hard block — automated rejection, no bypass without override | TBD |

---

## 5. Exception Process

### 5.1 Emergency Bypass

If a service must start immediately (production emergency, time-critical trading fix) before registration can be completed:

1. **Nathan explicit approval required** — via Telegram or direct `openclaw approve` command.
2. **Bypass token generated** — logged to `~/.openclaw/vault/approvals/approvals.jsonl` with reason.
3. **Retroactive registration required within 24 hours** — checklist completed, UUID assigned.
4. **Sentinel alert remains active** — `trading_sentinel` flags unregistered services until registration completes.

**Emergency bypass log format:**

```json
{
  "bypass_id": "EMR-2026-08-06-001",
  "service_name": "example-service",
  "approved_by": "Nathan Asiegbu",
  "approved_at": "2026-08-06T12:00:00Z",
  "reason": "Critical fix for Kalshi API timeout",
  "retroactive_deadline": "2026-08-07T12:00:00Z",
  "registration_completed": false
}
```

### 5.2 Retroactive Registration

All 42 PM2 processes active as of 2026-08-06 are registered retroactively under this policy. Their registration date is `2026-08-06` regardless of when they were originally deployed.

**Known retroactive gaps:**
- PM IDs 33, 34, 35 (open-empire-federation-staging, open-empire-lifecycle-staging, dynamics51) — STOPPED with high restarts — registered with status DEGRADED/STOPPED.
- AGENTS.md stale PM2 IDs — documented in Gate A, to be reconciled in next registry sweep.

---

## 6. Registry Entry Lifecycle

```
DRAFT → ACTIVE → DEPRECATED → DECOMMISSIONED
  ↑          ↓
SPEC      DEGRADED
```

| Status | Meaning |
|--------|---------|
| SPEC | Asset defined in spec, not yet deployed |
| DRAFT | Registration in progress, asset not yet live |
| ACTIVE | Deployed and operational |
| DEGRADED | Operational but unhealthy (e.g., high restarts) |
| PAUSED | Intentionally stopped, expected to resume |
| STOPPED | Stopped, on-demand only |
| DEPRECATED | Superseded, should not be started |
| DECOMMISSIONED | Permanently retired, UUID retained for history |

---

## 7. Registry Entry Template

**File: `REGISTRY_ENTRY_TEMPLATE.json`**

```json
{
  "_template_version": "1.0.0",
  "_instructions": "Copy this template. Fill all fields. Submit to Alusi for UUID assignment before pm2 start.",

  "uuid": "PENDING — assigned by governance agent",
  "human_id": "OE-SVC-XXXX",
  "name": "<pm2-process-name>",
  "type": "PM2_SERVICE | AGENT | CAPABILITY | REPOSITORY | DATABASE | DOCUMENT",
  "status": "DRAFT",
  "created_at": "YYYY-MM-DD",
  "registered_by": "Nathan Asiegbu",
  "immutable": true,

  "ownership": {
    "owner": "Nathan Asiegbu",
    "parent_portfolio": "OE-PORT-XXXX",
    "parent_program": "OE-PROG-XXXX"
  },

  "deployment": {
    "pm2_name": "<name>",
    "pm2_id": "TBD — assigned at first start",
    "script": "path/to/entry.py or dist/index.js",
    "cwd": "~/.openclaw/<path>",
    "interpreter": "python3 | node",
    "cron": "*/5 * * * * | null",
    "env_source": "~/.openclaw/secrets/.env"
  },

  "health": {
    "health_endpoint": "http://127.0.0.1:<port>/health | null",
    "health_check_method": "http | pm2_status | log_parse",
    "expected_cycle_seconds": 300
  },

  "governance": {
    "spend_cap_usd_daily": null,
    "requires_nathan_approval": false,
    "draft_first_gate": false,
    "secrets_required": []
  },

  "capability_id": "OE-CAP-XXXX",
  "aliases": [],
  "notes": ""
}
```

---

## 8. Registry Sweep Protocol

A **registry sweep** reconciles the live `pm2 jlist` output against the Runtime Registry. It must be run:

- **On demand:** When drift is suspected.
- **Weekly:** Every Monday as part of governance maintenance.
- **Post-deploy:** After any `pm2 start` or `pm2 delete`.

**Sweep command:**

```bash
# Full registry sweep
python3 ~/.openclaw/workspace/governance/scripts/registry_sweep.py \
  --registry ~/.openclaw/workspace/governance/RUNTIME_REGISTRY_V1.json \
  --output ~/.openclaw/workspace/governance/sweep_results_$(date +%Y%m%d).json
```

**Sweep output format:**

```json
{
  "sweep_date": "2026-08-06T12:00:00Z",
  "registered_not_running": ["service-a"],
  "running_not_registered": ["new-mystery-service"],
  "degraded": ["open-empire-federation-staging"],
  "drift_detected": true,
  "drift_count": 2,
  "action_required": true
}
```

---

## 9. Governance Integration

This policy integrates with:

- **Drift Detection Spec (Enhancement #10):** Registry drift is Layer 2 of the 6-layer drift detection system.
- **Observability Spec (Enhancement #2):** All registered services must expose `/health` endpoints (Phase 2).
- **Asset UUID Registry (Enhancement #5):** UUIDs assigned here are immutable and cross-referenced.
- **Secrets Governance (Enhancement #3):** New secrets require parallel registration.
- **Event-Driven Ops (Enhancement #7):** `REGISTRY_MUTATION` event fires on every new registration.

---

## 10. Compliance Verification

**Validation check (run weekly):**

```bash
# Verify registry completeness
python3 -c "
import json, subprocess, sys

registry_path = '/Users/NeoOC/.openclaw/workspace/governance/RUNTIME_REGISTRY_V1.json'
pm2_output = subprocess.run(['pm2', 'jlist'], capture_output=True, text=True)
pm2_procs = {p['name'] for p in json.loads(pm2_output.stdout)}

with open(registry_path) as f:
    registry = {s['name'] for s in json.load(f).get('services', [])}

unregistered = pm2_procs - registry
if unregistered:
    print(f'FAIL: {len(unregistered)} unregistered processes: {unregistered}', file=sys.stderr)
    sys.exit(1)
else:
    print(f'PASS: All {len(pm2_procs)} processes registered.')
"
```

**Expected result after retroactive registration:** `PASS: All 42 processes registered.`

---

## 11. Policy Exceptions Log

| Date | Exception | Reason | Retroactive By |
|------|-----------|--------|----------------|
| 2026-08-06 | All 42 PM2 processes | Retroactive registration at policy creation | 2026-08-06 |

---

## 12. References

- Open Empire Constitution v2
- Governance Baseline v1.0.0 — commit 17df0ff
- RUNTIME_REGISTRY_V1.json
- OPEN_EMPIRE_ASSET_UUID_REGISTRY_V1.json
- OPEN_EMPIRE_DRIFT_DETECTION_SPEC_V1.md (Enhancement #10)
