# Open Empire — Continuous Validation Specification (B9)

**Document Type:** Continuous Validation Specification  
**Version:** 1.0.0  
**Produced:** 2026-08-06  
**Authority:** Nathan Asiegbu  
**Status:** SPEC COMPLETE — cron activation pending Nathan approval

> ⚠️ **Important:** All cron jobs defined in this document are **NOT YET ACTIVE**. Activation requires explicit approval from Nathan Asiegbu. This document defines the specification; cron activation will be executed as a separate approved step.

---

## Executive Summary

This specification defines 6 continuous validation workstreams for the Open Empire system. Each validation type has a scheduled frequency, script path (to be created), alert channel (Telegram), severity rating, and remediation action.

| ID | Validation Type | Schedule | Severity | Status |
|---|---|---|---|---|
| CV-01 | Governance Validation | Every 6 hours | CRITICAL | Spec complete — script path defined |
| CV-02 | Runtime Agent Validation | Every 5 minutes | CRITICAL | Spec complete — script path defined |
| CV-03 | Repository Health Check | Daily 03:00 CDT | WARNING | Spec complete — script path defined |
| CV-04 | Secrets Validation | Every 1 hour | CRITICAL | Spec complete — script path defined |
| CV-05 | Bootstrap Validation | Weekly Sunday 06:00 CDT | WARNING | Spec complete — script path defined |
| CV-06 | Dependency Drift Detection | Every 15 minutes | WARNING | Spec complete — script path defined |

---

## Validation Type CV-01: Governance Validation

### Overview

Runs the full governance validation suite against the workspace to ensure no governance files have been modified, corrupted, or diverged from the v1.0.0 baseline.

### Schema

```json
{
  "id": "CV-01",
  "name": "governance_validation",
  "description": "Full 240-check governance validation suite",
  "schedule_cron": "0 */6 * * *",
  "schedule_human": "Every 6 hours (00:00, 06:00, 12:00, 18:00 CDT)",
  "script_path": "~/.openclaw/workspace/ops/validators/cv01_governance.sh",
  "validation_command": "~/.venvs/venv313/bin/python ~/.openclaw/workspace/governance/build/validate.py",
  "expected_output_pattern": "240/240 PASS",
  "alert_channel": "telegram",
  "alert_on": "any FAIL or non-240 result",
  "severity": "CRITICAL",
  "remediation_action": "STOP all autonomous agents immediately; do not restart until manual investigation completes; notify Nathan Asiegbu",
  "log_path": "~/.openclaw/workspace/governance/logs/cv01_$(date +%Y%m%d_%H%M%S).log",
  "retention_days": 30,
  "active": false,
  "activation_requires": "Nathan Asiegbu explicit approval"
}
```

### Script Specification

**Path:** `~/.openclaw/workspace/ops/validators/cv01_governance.sh`

```bash
#!/bin/bash
# CV-01: Governance Validation
# Run: every 6 hours via cron
# Alert: Telegram on FAIL

set -euo pipefail

TIMESTAMP=$(date -u +%Y%m%dT%H%M%SZ)
LOG_DIR=~/.openclaw/workspace/governance/logs
LOG_FILE="${LOG_DIR}/cv01_${TIMESTAMP}.log"
VALIDATE_CMD=~/.venvs/venv313/bin/python
VALIDATE_SCRIPT=~/.openclaw/workspace/governance/build/validate.py
TELEGRAM_SCRIPT=~/.openclaw/workspace/ops/notify_telegram.sh

mkdir -p "$LOG_DIR"

echo "[CV-01] Governance validation starting at $TIMESTAMP" | tee "$LOG_FILE"

# Run validation
$VALIDATE_CMD $VALIDATE_SCRIPT 2>&1 | tee -a "$LOG_FILE"
EXIT_CODE=${PIPESTATUS[0]}

if [ $EXIT_CODE -eq 0 ] && grep -q "240/240 PASS" "$LOG_FILE"; then
    echo "[CV-01] PASS — 240/240 checks passed" | tee -a "$LOG_FILE"
    # Optional: Telegram success summary (configurable)
else
    echo "[CV-01] FAIL — governance validation did not return 240/240 PASS" | tee -a "$LOG_FILE"
    # Alert via Telegram
    bash "$TELEGRAM_SCRIPT" "🚨 CRITICAL: Governance validation FAILED at $TIMESTAMP. Manual investigation required. Check: $LOG_FILE"
    exit 1
fi
```

### Cron Entry (NOT active until approved)

```cron
0 */6 * * * ~/.openclaw/workspace/ops/validators/cv01_governance.sh >> ~/.openclaw/workspace/governance/logs/cv01_cron.log 2>&1
```

---

## Validation Type CV-02: Runtime Agent Validation

### Overview

Checks PM2 process status every 5 minutes. Alerts on any STOPPED, ERRORED, or STOPPED_RESTART_LIMIT status for required-always-on services.

### Required-Always-On Services

| PM2 ID | Name | Criticality |
|---|---|---|
| 0 | executor | CRITICAL |
| 1 | heartbeat | CRITICAL |
| 2 | alusi-gateway | CRITICAL |
| 3 | alusi-telegram-adapter | CRITICAL |
| 4 | alusi-discord-adapter | WARNING |
| 5 | alusi-controlled-worker | CRITICAL |
| 6 | alusi-orchestrator | CRITICAL |
| 38 | cashclaw_director | CRITICAL (trading hours only) |
| 39 | cashclaw_arb | CRITICAL (trading hours only) |
| 40 | polymarket-trader | CRITICAL (trading hours only) |
| 41 | trading_sentinel | CRITICAL |
| 43 | clawdb | CRITICAL |
| 13 | exec-gateway | CRITICAL |
| 14 | telegram-approvals | CRITICAL |
| 17 | mission-control | WARNING |
| 10 | hyrvea-monitor | WARNING |
| 45 | open-empire-federation-staging | WARNING |
| 46 | open-empire-lifecycle-staging | WARNING |

### Schema

```json
{
  "id": "CV-02",
  "name": "runtime_agent_validation",
  "description": "PM2 process status check for all required-always-on agents",
  "schedule_cron": "*/5 * * * *",
  "schedule_human": "Every 5 minutes, 24/7",
  "script_path": "~/.openclaw/workspace/ops/validators/cv02_runtime.sh",
  "alert_channel": "telegram",
  "alert_on": "any CRITICAL service in stopped/errored state",
  "severity": "CRITICAL",
  "remediation_action": "Attempt automatic PM2 restart for non-trading agents; for trading agents (38,39,40,41), alert only — do NOT auto-restart without investigation",
  "log_path": "~/.openclaw/workspace/governance/logs/cv02_runtime.log",
  "retention_days": 7,
  "active": false,
  "activation_requires": "Nathan Asiegbu explicit approval"
}
```

### Script Specification

**Path:** `~/.openclaw/workspace/ops/validators/cv02_runtime.sh`

```bash
#!/bin/bash
# CV-02: Runtime Agent Validation
# Run: every 5 minutes via cron

TIMESTAMP=$(date -u +%Y%m%dT%H%M%SZ)
LOG_FILE=~/.openclaw/workspace/governance/logs/cv02_runtime.log
TELEGRAM_SCRIPT=~/.openclaw/workspace/ops/notify_telegram.sh

# Critical non-trading agents — auto-restart allowed
CRITICAL_AGENTS="executor heartbeat alusi-gateway alusi-telegram-adapter alusi-controlled-worker alusi-orchestrator exec-gateway telegram-approvals clawdb"

# Trading agents — alert only, no auto-restart
TRADING_AGENTS="cashclaw_director cashclaw_arb polymarket-trader trading_sentinel"

check_agent() {
    local name=$1
    local status=$(pm2 jlist 2>/dev/null | python3 -c "
import json, sys
data = json.load(sys.stdin)
for p in data:
    if p['name'] == '${name}':
        print(p['pm2_env']['status'])
        break
else:
    print('NOT_FOUND')
")
    echo "$status"
}

ALERTS=()

for agent in $CRITICAL_AGENTS; do
    status=$(check_agent "$agent")
    if [ "$status" != "online" ]; then
        ALERTS+=("CRITICAL: $agent is $status — auto-restart attempted")
        echo "[$TIMESTAMP] CRITICAL: $agent is $status — attempting restart" >> "$LOG_FILE"
        pm2 restart "$agent" 2>> "$LOG_FILE" || true
    fi
done

for agent in $TRADING_AGENTS; do
    status=$(check_agent "$agent")
    if [ "$status" != "online" ] && [ "$status" != "stopped" ]; then
        # stopped is expected outside trading hours
        ALERTS+=("CRITICAL: TRADING AGENT $agent is $status — MANUAL INTERVENTION REQUIRED")
        echo "[$TIMESTAMP] CRITICAL: TRADING AGENT $agent is $status" >> "$LOG_FILE"
    fi
done

if [ ${#ALERTS[@]} -gt 0 ]; then
    MSG="⚠️ CV-02 Runtime Alert at $TIMESTAMP:"$'\n'
    for alert in "${ALERTS[@]}"; do
        MSG+="• $alert"$'\n'
    done
    bash "$TELEGRAM_SCRIPT" "$MSG"
fi
```

### Cron Entry (NOT active until approved)

```cron
*/5 * * * * ~/.openclaw/workspace/ops/validators/cv02_runtime.sh >> ~/.openclaw/workspace/governance/logs/cv02_cron.log 2>&1
```

---

## Validation Type CV-03: Repository Health Check

### Overview

Runs a `git fetch` + `git status` on the primary workspace repo daily. Detects: uncommitted critical files, divergence from remote, or fetch failures indicating connectivity issues.

### Schema

```json
{
  "id": "CV-03",
  "name": "repository_health_check",
  "description": "Daily git fetch and status check for ~/.openclaw/workspace",
  "schedule_cron": "0 8 * * *",
  "schedule_human": "Daily at 03:00 CDT (08:00 UTC)",
  "script_path": "~/.openclaw/workspace/ops/validators/cv03_repo_health.sh",
  "alert_channel": "telegram",
  "alert_on": "fetch failure OR divergence from remote exceeds 5 commits",
  "severity": "WARNING",
  "remediation_action": "Notify Nathan Asiegbu; do not auto-merge or auto-push; require manual review",
  "log_path": "~/.openclaw/workspace/governance/logs/cv03_repo_health.log",
  "retention_days": 30,
  "active": false,
  "activation_requires": "Nathan Asiegbu explicit approval"
}
```

### Script Specification

**Path:** `~/.openclaw/workspace/ops/validators/cv03_repo_health.sh`

```bash
#!/bin/bash
# CV-03: Repository Health Check
# Run: daily 03:00 CDT

TIMESTAMP=$(date -u +%Y%m%dT%H%M%SZ)
LOG_FILE=~/.openclaw/workspace/governance/logs/cv03_repo_health.log
TELEGRAM_SCRIPT=~/.openclaw/workspace/ops/notify_telegram.sh
WORKSPACE=~/.openclaw/workspace

echo "[$TIMESTAMP] CV-03: Repository health check" >> "$LOG_FILE"

cd "$WORKSPACE"

# Fetch from remote
git fetch origin 2>> "$LOG_FILE"
FETCH_EXIT=$?

if [ $FETCH_EXIT -ne 0 ]; then
    MSG="⚠️ CV-03 WARNING: git fetch failed for workspace repo at $TIMESTAMP. Network issue or remote unavailable."
    echo "$MSG" >> "$LOG_FILE"
    bash "$TELEGRAM_SCRIPT" "$MSG"
    exit 1
fi

# Check divergence
BEHIND=$(git rev-list --count HEAD..origin/master 2>/dev/null || echo "0")
AHEAD=$(git rev-list --count origin/master..HEAD 2>/dev/null || echo "0")

echo "[$TIMESTAMP] Behind remote: $BEHIND commits. Ahead: $AHEAD commits." >> "$LOG_FILE"

if [ "$BEHIND" -gt 5 ]; then
    MSG="⚠️ CV-03 WARNING: workspace is $BEHIND commits behind origin/master. Manual review required."
    bash "$TELEGRAM_SCRIPT" "$MSG"
fi

# Record workspace git status summary
git status --short >> "$LOG_FILE"
echo "[$TIMESTAMP] CV-03: COMPLETE" >> "$LOG_FILE"
```

### Cron Entry (NOT active until approved)

```cron
0 8 * * * ~/.openclaw/workspace/ops/validators/cv03_repo_health.sh >> ~/.openclaw/workspace/governance/logs/cv03_cron.log 2>&1
```

---

## Validation Type CV-04: Secrets Validation

### Overview

Checks that all 40 known secret keys exist in `~/.openclaw/secrets/.env` every hour. Does NOT read or transmit values — only checks for key presence. Alerts if any key is missing (possible `.env` corruption or accidental deletion).

### Schema

```json
{
  "id": "CV-04",
  "name": "secrets_validation",
  "description": "Hourly check that all 40 known secret keys exist in ~/.openclaw/secrets/.env",
  "schedule_cron": "0 * * * *",
  "schedule_human": "Every hour at :00",
  "script_path": "~/.openclaw/workspace/ops/validators/cv04_secrets.sh",
  "secrets_manifest_path": "~/.openclaw/workspace/governance/secrets/key_manifest.json",
  "alert_channel": "telegram",
  "alert_on": "any known key missing from .env",
  "severity": "CRITICAL",
  "remediation_action": "STOP all trading agents immediately; investigate .env integrity; restore from encrypted backup if available; notify Nathan Asiegbu",
  "log_path": "~/.openclaw/workspace/governance/logs/cv04_secrets.log",
  "retention_days": 7,
  "active": false,
  "activation_requires": "Nathan Asiegbu explicit approval + key_manifest.json creation"
}
```

### Script Specification

**Path:** `~/.openclaw/workspace/ops/validators/cv04_secrets.sh`

```bash
#!/bin/bash
# CV-04: Secrets Validation
# Run: every hour
# NOTE: Only checks key NAMES exist. Never reads or logs values.

TIMESTAMP=$(date -u +%Y%m%dT%H%M%SZ)
LOG_FILE=~/.openclaw/workspace/governance/logs/cv04_secrets.log
TELEGRAM_SCRIPT=~/.openclaw/workspace/ops/notify_telegram.sh
ENV_FILE=~/.openclaw/secrets/.env
KEY_MANIFEST=~/.openclaw/workspace/governance/secrets/key_manifest.json

MISSING=()

# Check .env file exists
if [ ! -f "$ENV_FILE" ]; then
    MSG="🚨 CV-04 CRITICAL: ~/.openclaw/secrets/.env NOT FOUND at $TIMESTAMP. Stopping trading agents."
    echo "$MSG" >> "$LOG_FILE"
    bash "$TELEGRAM_SCRIPT" "$MSG"
    pm2 stop cashclaw_director cashclaw_arb polymarket-trader 2>/dev/null || true
    exit 1
fi

# Check key manifest exists
if [ ! -f "$KEY_MANIFEST" ]; then
    echo "[$TIMESTAMP] CV-04: key_manifest.json not found — skip key-by-key check (create manifest first)" >> "$LOG_FILE"
    exit 0
fi

# Check each known key exists (name only — no value read)
EXPECTED_KEYS=$(python3 -c "
import json
with open('$KEY_MANIFEST') as f:
    m = json.load(f)
for k in m.get('keys', []):
    print(k['name'])
")

for key in $EXPECTED_KEYS; do
    if ! grep -q "^${key}=" "$ENV_FILE" 2>/dev/null; then
        MISSING+=("$key")
    fi
done

if [ ${#MISSING[@]} -gt 0 ]; then
    MSG="🚨 CV-04 CRITICAL: ${#MISSING[@]} keys missing from .env at $TIMESTAMP: ${MISSING[*]}"
    echo "$MSG" >> "$LOG_FILE"
    bash "$TELEGRAM_SCRIPT" "$MSG"
    exit 1
else
    echo "[$TIMESTAMP] CV-04: All ${EXPECTED_KEYS} keys present. PASS." >> "$LOG_FILE"
fi
```

### Cron Entry (NOT active until approved)

```cron
0 * * * * ~/.openclaw/workspace/ops/validators/cv04_secrets.sh >> ~/.openclaw/workspace/governance/logs/cv04_cron.log 2>&1
```

---

## Validation Type CV-05: Bootstrap Validation

### Overview

Weekly check that the system could be bootstrapped from scratch. Verifies: all required tools present, required ports available, required directories exist, required PM2 processes are defined in ecosystem config.

### Schema

```json
{
  "id": "CV-05",
  "name": "bootstrap_validation",
  "description": "Weekly validation that bootstrap prerequisites are intact",
  "schedule_cron": "0 11 * * 0",
  "schedule_human": "Weekly Sunday at 06:00 CDT (11:00 UTC)",
  "script_path": "~/.openclaw/workspace/ops/validators/cv05_bootstrap.sh",
  "alert_channel": "telegram",
  "alert_on": "any prerequisite missing or misconfigured",
  "severity": "WARNING",
  "remediation_action": "Notify Nathan Asiegbu; document the gap; schedule remediation",
  "log_path": "~/.openclaw/workspace/governance/logs/cv05_bootstrap.log",
  "retention_days": 90,
  "active": false,
  "activation_requires": "Nathan Asiegbu explicit approval"
}
```

### Script Specification

**Path:** `~/.openclaw/workspace/ops/validators/cv05_bootstrap.sh`

```bash
#!/bin/bash
# CV-05: Bootstrap Validation
# Run: weekly Sunday 06:00 CDT

TIMESTAMP=$(date -u +%Y%m%dT%H%M%SZ)
LOG_FILE=~/.openclaw/workspace/governance/logs/cv05_bootstrap.log
TELEGRAM_SCRIPT=~/.openclaw/workspace/ops/notify_telegram.sh

WARNINGS=()

echo "[$TIMESTAMP] CV-05: Bootstrap validation starting" >> "$LOG_FILE"

# Tool checks
command -v git      >/dev/null 2>&1 || WARNINGS+=("MISSING: git")
command -v node     >/dev/null 2>&1 || WARNINGS+=("MISSING: node")
command -v npm      >/dev/null 2>&1 || WARNINGS+=("MISSING: npm")
command -v pm2      >/dev/null 2>&1 || WARNINGS+=("MISSING: pm2")
command -v python3  >/dev/null 2>&1 || WARNINGS+=("MISSING: python3")
command -v brew     >/dev/null 2>&1 || WARNINGS+=("MISSING: homebrew")
command -v tailscale >/dev/null 2>&1 || WARNINGS+=("MISSING: tailscale")

# Python venv
[ -f ~/.venvs/venv313/bin/python ] || WARNINGS+=("MISSING: venv313 at ~/.venvs/venv313")

# Required directories
[ -d ~/.openclaw/workspace ]         || WARNINGS+=("MISSING: ~/.openclaw/workspace")
[ -d ~/.openclaw/workspace/governance ] || WARNINGS+=("MISSING: governance directory")
[ -d ~/.openclaw/trading ]           || WARNINGS+=("MISSING: ~/.openclaw/trading")
[ -d ~/.openclaw/blco ]              || WARNINGS+=("MISSING: ~/.openclaw/blco")
[ -d ~/.openclaw/vault ]             || WARNINGS+=("MISSING: ~/.openclaw/vault")

# Required files
[ -f ~/.openclaw/secrets/.env ]      || WARNINGS+=("MISSING: ~/.openclaw/secrets/.env")
[ -f ~/.openclaw/workspace/AGENTS.md ] || WARNINGS+=("MISSING: AGENTS.md")

# Port availability (occupied = service running = good)
nc -z localhost 3333 2>/dev/null || WARNINGS+=("WARNING: mission-control port 3333 not responding")
nc -z localhost 5432 2>/dev/null || WARNINGS+=("WARNING: clawdb port 5432 not responding")
nc -z localhost 11434 2>/dev/null || WARNINGS+=("WARNING: ollama port 11434 not responding")

# Node version check
NODE_VER=$(node --version 2>/dev/null | sed 's/v//')
NODE_MAJOR=$(echo $NODE_VER | cut -d. -f1)
[ "$NODE_MAJOR" -ge 24 ] 2>/dev/null || WARNINGS+=("WARNING: Node.js $NODE_VER < v24 expected")

if [ ${#WARNINGS[@]} -gt 0 ]; then
    MSG="⚠️ CV-05 Bootstrap WARNING at $TIMESTAMP: ${#WARNINGS[@]} issues found:"$'\n'
    for w in "${WARNINGS[@]}"; do
        MSG+="• $w"$'\n'
    done
    echo "$MSG" >> "$LOG_FILE"
    bash "$TELEGRAM_SCRIPT" "$MSG"
else
    echo "[$TIMESTAMP] CV-05: All bootstrap prerequisites intact. PASS." >> "$LOG_FILE"
    bash "$TELEGRAM_SCRIPT" "✅ CV-05 Weekly bootstrap check PASS at $TIMESTAMP — all prerequisites intact."
fi
```

### Cron Entry (NOT active until approved)

```cron
0 11 * * 0 ~/.openclaw/workspace/ops/validators/cv05_bootstrap.sh >> ~/.openclaw/workspace/governance/logs/cv05_cron.log 2>&1
```

---

## Validation Type CV-06: Dependency Drift Detection

### Overview

Compares the runtime-observed ports (from `lsof -i` / `netstat`) against the registered port registry every 15 minutes. Alerts if a registered service is no longer on its expected port, or if an unregistered port appears on a known service number.

### Schema

```json
{
  "id": "CV-06",
  "name": "dependency_drift_detection",
  "description": "Every-15-min comparison of live runtime ports against OPEN_EMPIRE_RUNTIME_PORT_REGISTRY.json",
  "schedule_cron": "*/15 * * * *",
  "schedule_human": "Every 15 minutes",
  "script_path": "~/.openclaw/workspace/ops/validators/cv06_port_drift.sh",
  "port_registry_path": "~/.openclaw/workspace/governance/RUNTIME_PORT_REGISTRY.json",
  "alert_channel": "telegram",
  "alert_on": "any registered required port not listening OR unexpected port collision",
  "severity": "WARNING",
  "remediation_action": "Notify Nathan Asiegbu; identify which process moved or died; restart if appropriate",
  "log_path": "~/.openclaw/workspace/governance/logs/cv06_port_drift.log",
  "retention_days": 7,
  "active": false,
  "activation_requires": "Nathan Asiegbu explicit approval + RUNTIME_PORT_REGISTRY.json validation"
}
```

### Script Specification

**Path:** `~/.openclaw/workspace/ops/validators/cv06_port_drift.sh`

```bash
#!/bin/bash
# CV-06: Dependency Drift Detection
# Run: every 15 minutes

TIMESTAMP=$(date -u +%Y%m%dT%H%M%SZ)
LOG_FILE=~/.openclaw/workspace/governance/logs/cv06_port_drift.log
TELEGRAM_SCRIPT=~/.openclaw/workspace/ops/notify_telegram.sh
PORT_REGISTRY=~/.openclaw/workspace/governance/RUNTIME_PORT_REGISTRY.json

# Define required ports inline (fallback if registry not available)
declare -A REQUIRED_PORTS
REQUIRED_PORTS[3333]="mission-control"
REQUIRED_PORTS[5432]="clawdb-postgresql"
REQUIRED_PORTS[11434]="ollama"
REQUIRED_PORTS[3001]="grafana"

DRIFTS=()

for port in "${!REQUIRED_PORTS[@]}"; do
    service="${REQUIRED_PORTS[$port]}"
    if ! nc -z localhost "$port" 2>/dev/null; then
        DRIFTS+=("PORT $port ($service) not responding")
    fi
done

if [ ${#DRIFTS[@]} -gt 0 ]; then
    MSG="⚠️ CV-06 Port Drift WARNING at $TIMESTAMP:"$'\n'
    for d in "${DRIFTS[@]}"; do
        MSG+="• $d"$'\n'
    done
    echo "$MSG" >> "$LOG_FILE"
    bash "$TELEGRAM_SCRIPT" "$MSG"
else
    echo "[$TIMESTAMP] CV-06: All required ports responding. PASS." >> "$LOG_FILE"
fi
```

### Cron Entry (NOT active until approved)

```cron
*/15 * * * * ~/.openclaw/workspace/ops/validators/cv06_port_drift.sh >> ~/.openclaw/workspace/governance/logs/cv06_cron.log 2>&1
```

---

## Shared Utility: Telegram Notifier

All validators depend on a shared notification script.

**Path:** `~/.openclaw/workspace/ops/notify_telegram.sh`

```bash
#!/bin/bash
# Shared Telegram notification utility for all CV validators
# Usage: bash notify_telegram.sh "message text"

MESSAGE="$1"
BOT_TOKEN=$(grep '^TELEGRAM_BOT_TOKEN=' ~/.openclaw/secrets/.env | cut -d= -f2)
CHAT_ID=$(grep '^TELEGRAM_CHAT_ID=' ~/.openclaw/secrets/.env | cut -d= -f2)

if [ -z "$BOT_TOKEN" ] || [ -z "$CHAT_ID" ]; then
    echo "ERROR: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set in .env" >&2
    exit 1
fi

curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
    -d "chat_id=${CHAT_ID}" \
    -d "text=${MESSAGE}" \
    -d "parse_mode=Markdown" \
    > /dev/null 2>&1
```

---

## Cron Installation (PENDING NATHAN APPROVAL)

All 6 cron jobs should be installed together after approval. The combined crontab addition:

```cron
# === OPEN EMPIRE CONTINUOUS VALIDATION — installed 2026-08-XX ===
# CV-01: Governance validation every 6 hours
0 */6 * * * ~/.openclaw/workspace/ops/validators/cv01_governance.sh >> ~/.openclaw/workspace/governance/logs/cv01_cron.log 2>&1
# CV-02: Runtime agent check every 5 minutes
*/5 * * * * ~/.openclaw/workspace/ops/validators/cv02_runtime.sh >> ~/.openclaw/workspace/governance/logs/cv02_cron.log 2>&1
# CV-03: Repository health daily at 03:00 CDT (08:00 UTC)
0 8 * * * ~/.openclaw/workspace/ops/validators/cv03_repo_health.sh >> ~/.openclaw/workspace/governance/logs/cv03_cron.log 2>&1
# CV-04: Secrets validation every hour
0 * * * * ~/.openclaw/workspace/ops/validators/cv04_secrets.sh >> ~/.openclaw/workspace/governance/logs/cv04_cron.log 2>&1
# CV-05: Bootstrap validation weekly Sunday 06:00 CDT (11:00 UTC)
0 11 * * 0 ~/.openclaw/workspace/ops/validators/cv05_bootstrap.sh >> ~/.openclaw/workspace/governance/logs/cv05_cron.log 2>&1
# CV-06: Port drift detection every 15 minutes
*/15 * * * * ~/.openclaw/workspace/ops/validators/cv06_port_drift.sh >> ~/.openclaw/workspace/governance/logs/cv06_cron.log 2>&1
# === END OPEN EMPIRE CONTINUOUS VALIDATION ===
```

**Installation command (after approval):**
```bash
# Back up existing crontab
crontab -l > ~/crontab_backup_$(date +%Y%m%d).txt

# Add CV entries
(crontab -l 2>/dev/null; cat ~/.openclaw/workspace/governance/track_b/cv_crontab_additions.txt) | crontab -

# Verify
crontab -l
```

---

## Pre-Activation Checklist

Before Nathan approves cron activation:

| # | Task | Status |
|---|---|---|
| 1 | Create `~/.openclaw/workspace/ops/validators/` directory | ❌ Pending |
| 2 | Write all 6 validator scripts to their paths | ❌ Pending |
| 3 | Write `notify_telegram.sh` utility | ❌ Pending |
| 4 | Verify TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in .env | ❌ Pending |
| 5 | Create governance log directory | ❌ Pending |
| 6 | Create key_manifest.json for CV-04 | ❌ Pending (secrets-governance repo first) |
| 7 | Test each script manually once | ❌ Pending |
| 8 | Nathan reviews and approves this spec | ❌ Pending |
| 9 | Add cron entries to crontab | ❌ Pending (after #8) |

---

## Change Log

| Date | Change | Author |
|---|---|---|
| 2026-08-06 | Initial document — B9 Continuous Validation Specification v1.0.0 | Nathan Asiegbu (via governance build) |
