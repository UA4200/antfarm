# OPEN EMPIRE — OPERATIONAL DIGITAL TWIN SPEC V1
## Foundational Enhancement #8: Operational Digital Twin

**Status:** SPEC  
**Version:** 1.0.0  
**Created:** 2026-08-06  
**Operator:** Nathan Asiegbu  
**Governed by:** Open Empire Constitution v2, Governance Baseline v1.0.0 (commit 17df0ff)

---

## 1. What Is the Digital Twin?

The Open Empire Operational Digital Twin is a **continuously-updated JSON representation of the entire live system state**. It is the single source of truth for:

- What is running right now
- What the financial positions are right now
- Whether governance is healthy right now
- Whether all agents are operating within their defined bounds

The twin is **not** a historical record (that's the trade logs and governance journals). It is the **present-moment snapshot** of the system, updated automatically.

The twin **replaces manual status checks**. Instead of running `pm2 status` or reading `.env` files, Mission Control and any monitoring agent reads `current_state.json`.

---

## 2. State Components

### 2.1 Runtime State

**Source:** `pm2 jlist` (JSON process list)  
**Update frequency:** Every 60 seconds  
**Purpose:** Know which processes are running, their health, memory/CPU, and restart counts.

```json
"runtime": {
  "updated_at": "2026-08-06T12:00:00Z",
  "pm2_process_count": 42,
  "processes": [
    {
      "pm2_id": 38,
      "name": "cashclaw_director",
      "uuid": "a1b2c3d4-0000-5001-8000-000000000038",
      "status": "online",
      "cpu_pct": 0.3,
      "memory_mb": 44.5,
      "restart_count": 0,
      "uptime_seconds": 86400,
      "last_restart": null
    }
  ],
  "summary": {
    "online": 37,
    "stopped": 5,
    "errored": 0,
    "degraded": 2
  }
}
```

### 2.2 Infrastructure State

**Source:** `lsof -i -n -P` (port bindings) + system checks  
**Update frequency:** Every 60 seconds (bundled with runtime)  
**Purpose:** Know which ports are bound, detect unexpected services, verify loopback policy.

```json
"infrastructure": {
  "updated_at": "2026-08-06T12:00:00Z",
  "ports": {
    "3333": {"service": "mission-control", "bound_to": "127.0.0.1", "status": "ok"},
    "5432": {"service": "clawdb", "bound_to": "127.0.0.1", "status": "ok"},
    "11434": {"service": "ollama", "bound_to": "127.0.0.1", "status": "ok"},
    "3001": {"service": "grafana", "bound_to": "127.0.0.1", "status": "unknown"}
  },
  "loopback_policy_violations": [],
  "tailscale": {
    "status": "connected",
    "node_count": null
  }
}
```

### 2.3 Financial State

**Source:** Trade log files (`~/.openclaw/trading/logs/trades.jsonl`)  
**Update frequency:** Every 5 minutes (aligned with trading cycles)  
**Purpose:** Know current balances, open positions, P&L, and spend cap status.

```json
"financial": {
  "updated_at": "2026-08-06T12:00:00Z",
  "platforms": {
    "kalshi": {
      "balance_usd": 1.55,
      "open_orders_usd": 80.00,
      "daily_spend_usd": 2.50,
      "daily_cap_usd": 10.00,
      "spend_pct": 25.0,
      "status": "ACTIVE",
      "last_trade_at": "2026-08-06T11:45:00Z"
    },
    "polymarket": {
      "balance_usd": 0.06,
      "open_orders_usd": 0.00,
      "daily_spend_usd": 0.00,
      "daily_cap_usd": 10.00,
      "spend_pct": 0.0,
      "status": "ACTIVE",
      "last_trade_at": null
    }
  },
  "ai_spend_today_usd": 0.12,
  "ai_spend_cap_usd": 0.20,
  "ai_spend_pct": 60.0,
  "total_pnl_7d_usd": null,
  "total_pnl_30d_usd": null
}
```

### 2.4 Governance State

**Source:** SHA256SUMS + governance validation scripts  
**Update frequency:** On change (inotify) + every 5 minutes (fallback cron)  
**Purpose:** Know if governance artifacts are intact and whether the system is in constitutional compliance.

```json
"governance": {
  "updated_at": "2026-08-06T12:00:00Z",
  "baseline_version": "1.0.0",
  "baseline_commit": "17df0ff",
  "baseline_status": "FROZEN",
  "last_validation_run": "2026-08-06T12:00:00Z",
  "validation_result": "PASS",
  "artifact_integrity": {
    "OPEN_EMPIRE_CONSTITUTION_V2.md": "verified",
    "GOVERNANCE_BASELINE_V1.md": "verified",
    "SHA256SUMS": "self-referential"
  },
  "track_b_progress": {
    "total_enhancements": 10,
    "spec_complete": 8,
    "implemented": 0,
    "in_progress": 0
  }
}
```

### 2.5 Agent State

**Source:** PM2 runtime state + agent-specific log parsing + health endpoints (when available)  
**Update frequency:** Every 60 seconds  
**Purpose:** Know each key agent's operational status, last activity, and capability health.

```json
"agents": {
  "updated_at": "2026-08-06T12:00:00Z",
  "agents": [
    {
      "uuid": "oe-agent-0002",
      "name": "cashclaw_director",
      "status": "ACTIVE",
      "last_cycle_at": "2026-08-06T11:55:00Z",
      "last_cycle_result": "no_trades",
      "health": "healthy",
      "capabilities": ["kalshi_trading", "kelly_sizing", "spend_cap_enforcement"]
    },
    {
      "uuid": "oe-agent-0005",
      "name": "trading_sentinel",
      "status": "ACTIVE",
      "last_cycle_at": "2026-08-06T11:55:00Z",
      "last_cycle_result": "all_clear",
      "health": "healthy",
      "capabilities": ["watchdog", "circuit_breaker"]
    }
  ]
}
```

---

## 3. Storage Design

### 3.1 Rolling State (current_state.json)

```
~/.openclaw/workspace/digital_twin/
├── current_state.json          ← Always the latest state (overwritten each cycle)
├── snapshots/
│   ├── 2026-08-06T12.json     ← Hourly snapshots (kept 7 days)
│   ├── 2026-08-06T13.json
│   └── ...
└── schema/
    └── digital_twin_schema_v1.json
```

**`current_state.json` root schema:**

```json
{
  "schema_version": "1.0.0",
  "generated_at": "2026-08-06T12:00:00Z",
  "generation_duration_ms": 1200,
  "operator": "Nathan Asiegbu",
  "system_health": "healthy|degraded|critical",
  "empire_health_score": 0.87,
  "runtime": {},
  "infrastructure": {},
  "financial": {},
  "governance": {},
  "agents": {},
  "alerts_active": [],
  "drift_detected": false,
  "drift_summary": null
}
```

### 3.2 Snapshot Retention Policy

| Snapshot Age | Retention |
|-------------|-----------|
| < 24 hours | All snapshots (every hour) |
| 1–7 days | 6-hour snapshots |
| 7–30 days | Daily snapshots |
| > 30 days | Weekly snapshots |

**Rotation script:** `digital_twin/rotate_snapshots.py` (to build)

---

## 4. Implementation: Digital Twin Updater

**File:** `~/.openclaw/workspace/digital_twin/update_twin.py`  
**PM2 name:** `digital-twin-updater`  
**Cron:** `*/1 * * * *` (every 60 seconds)

### 4.1 Pseudo-implementation

```python
#!/usr/bin/env python3
"""
Open Empire Digital Twin Updater
Runs every 60 seconds. Reads live state from multiple sources and writes current_state.json.
"""

import json
import subprocess
import os
import time
from datetime import datetime, timezone
from pathlib import Path

TWIN_DIR = Path(os.path.expanduser("~/.openclaw/workspace/digital_twin"))
CURRENT_STATE_PATH = TWIN_DIR / "current_state.json"
SNAPSHOTS_DIR = TWIN_DIR / "snapshots"
TRADE_LOG_PATH = Path(os.path.expanduser("~/.openclaw/trading/logs/trades.jsonl"))
GOVERNANCE_DIR = Path(os.path.expanduser("~/.openclaw/workspace/governance"))

def get_runtime_state() -> dict:
    """Pull live PM2 process list."""
    try:
        result = subprocess.run(["pm2", "jlist"], capture_output=True, text=True, timeout=10)
        processes = json.loads(result.stdout)
        
        parsed = []
        for proc in processes:
            mem = proc.get("monit", {}).get("memory", 0)
            cpu = proc.get("monit", {}).get("cpu", 0)
            parsed.append({
                "pm2_id": proc.get("pm_id"),
                "name": proc.get("name"),
                "status": proc.get("pm2_env", {}).get("status"),
                "cpu_pct": round(cpu, 2),
                "memory_mb": round(mem / 1024 / 1024, 1),
                "restart_count": proc.get("pm2_env", {}).get("restart_time", 0),
                "uptime_seconds": int(
                    (time.time() * 1000 - proc.get("pm2_env", {}).get("pm_uptime", time.time() * 1000)) / 1000
                )
            })
        
        statuses = [p["status"] for p in parsed]
        return {
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "pm2_process_count": len(parsed),
            "processes": parsed,
            "summary": {
                "online": statuses.count("online"),
                "stopped": statuses.count("stopped"),
                "errored": statuses.count("errored"),
                "degraded": sum(1 for p in parsed if p["restart_count"] > 5)
            }
        }
    except Exception as e:
        return {"error": str(e), "updated_at": datetime.now(timezone.utc).isoformat()}


def get_financial_state() -> dict:
    """Read trade logs for spend and balance estimates."""
    from datetime import timedelta
    
    now = datetime.now(timezone.utc)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    
    daily_spend = {"cashclaw_director": 0.0, "cashclaw_arb": 0.0, "polymarket-trader": 0.0}
    
    if TRADE_LOG_PATH.exists():
        with open(TRADE_LOG_PATH) as f:
            for line in f:
                try:
                    trade = json.loads(line.strip())
                    trade_time = datetime.fromisoformat(trade.get("timestamp", ""))
                    if trade_time >= today_start:
                        agent = trade.get("agent", "")
                        size = float(trade.get("size_usd", 0))
                        if agent in daily_spend:
                            daily_spend[agent] += size
                except Exception:
                    continue
    
    return {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "platforms": {
            "kalshi": {
                "daily_spend_usd": round(daily_spend["cashclaw_director"] + daily_spend["cashclaw_arb"], 2),
                "daily_cap_usd": 10.00,
                "spend_pct": round((daily_spend["cashclaw_director"] + daily_spend["cashclaw_arb"]) / 10 * 100, 1),
                "status": "ACTIVE"
            },
            "polymarket": {
                "daily_spend_usd": round(daily_spend["polymarket-trader"], 2),
                "daily_cap_usd": 10.00,
                "spend_pct": round(daily_spend["polymarket-trader"] / 10 * 100, 1),
                "status": "ACTIVE"
            }
        }
    }


def get_governance_state() -> dict:
    """Read SHA256SUMS and run quick integrity check."""
    sha256_path = GOVERNANCE_DIR / "SHA256SUMS"
    result = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "baseline_version": "1.0.0",
        "baseline_commit": "17df0ff",
        "baseline_status": "FROZEN",
        "sha256sums_exists": sha256_path.exists(),
        "validation_result": "UNKNOWN"
    }
    
    if sha256_path.exists():
        try:
            verify = subprocess.run(
                ["shasum", "-a", "256", "-c", str(sha256_path)],
                cwd=str(GOVERNANCE_DIR),
                capture_output=True, text=True, timeout=30
            )
            result["validation_result"] = "PASS" if verify.returncode == 0 else "FAIL"
            result["last_validation_run"] = datetime.now(timezone.utc).isoformat()
        except Exception as e:
            result["validation_error"] = str(e)
    
    return result


def compute_health_score(runtime: dict, financial: dict, governance: dict) -> float:
    """Compute composite empire health score 0.0 - 1.0."""
    score = 1.0
    
    summary = runtime.get("summary", {})
    total = runtime.get("pm2_process_count", 1)
    online = summary.get("online", 0)
    errored = summary.get("errored", 0)
    
    if total > 0:
        score *= (online / total)
    score -= (errored * 0.1)
    
    for platform_data in financial.get("platforms", {}).values():
        pct = platform_data.get("spend_pct", 0)
        if pct >= 100:
            score -= 0.3
        elif pct >= 80:
            score -= 0.1
    
    if governance.get("validation_result") == "FAIL":
        score -= 0.4
    
    return max(0.0, min(1.0, round(score, 2)))


def main():
    TWIN_DIR.mkdir(parents=True, exist_ok=True)
    SNAPSHOTS_DIR.mkdir(exist_ok=True)
    
    start = time.time()
    
    runtime = get_runtime_state()
    financial = get_financial_state()
    governance = get_governance_state()
    health_score = compute_health_score(runtime, financial, governance)
    
    if health_score >= 0.9:
        system_health = "healthy"
    elif health_score >= 0.6:
        system_health = "degraded"
    else:
        system_health = "critical"
    
    state = {
        "schema_version": "1.0.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "generation_duration_ms": int((time.time() - start) * 1000),
        "operator": "Nathan Asiegbu",
        "system_health": system_health,
        "empire_health_score": health_score,
        "runtime": runtime,
        "financial": financial,
        "governance": governance,
        "agents": {},
        "alerts_active": [],
        "drift_detected": False
    }
    
    # Write rolling state
    with open(CURRENT_STATE_PATH, "w") as f:
        json.dump(state, f, indent=2)
    
    # Hourly snapshot
    hour = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H")
    snapshot_path = SNAPSHOTS_DIR / f"{hour}.json"
    if not snapshot_path.exists():
        with open(snapshot_path, "w") as f:
            json.dump(state, f, indent=2)
    
    print(f"[digital-twin] Updated. Health: {system_health} ({health_score}). "
          f"Processes: {runtime.get('summary', {}).get('online', '?')}/online. "
          f"Duration: {state['generation_duration_ms']}ms")


if __name__ == "__main__":
    main()
```

---

## 5. Visualization: Mission Control Integration

Mission Control (port 3333) should render the digital twin as a **live topology map**.

### API Endpoint (to build in mission-control)

```
GET /api/twin/current
→ Returns current_state.json contents

GET /api/twin/snapshots?from=2026-08-06T00&to=2026-08-06T12
→ Returns list of snapshot timestamps

GET /api/twin/snapshots/:timestamp
→ Returns specific snapshot
```

### Required Mission Control Components

| Component | Data Source | Refresh |
|-----------|------------|---------|
| Empire Health Score gauge | `empire_health_score` | 60s |
| PM2 Process grid | `runtime.processes` | 60s |
| Financial Positions panel | `financial.platforms` | 5min |
| Spend Cap gauges (3) | `financial.platforms.*.spend_pct` | 5min |
| Governance Status badge | `governance.validation_result` | on-change |
| Active Alerts feed | `alerts_active` | 60s |
| System Health timeline | Snapshot history | hourly |

---

## 6. Empire Health Score

The composite health score (0.0 – 1.0) is the single most important metric:

| Score | Label | Color | Meaning |
|-------|-------|-------|---------|
| 0.90–1.00 | HEALTHY | Green | All systems nominal |
| 0.70–0.89 | GOOD | Yellow-Green | Minor issues, no action required |
| 0.50–0.69 | DEGRADED | Yellow | Multiple services degraded |
| 0.30–0.49 | WARNING | Orange | Significant issues, attention needed |
| 0.00–0.29 | CRITICAL | Red | Major failure, immediate action required |

**Score components:**
- Process uptime ratio: 40% weight
- No errored processes: 20% weight
- Financial caps not breached: 20% weight
- Governance validation passing: 20% weight

---

## 7. PM2 Registration for Digital Twin Updater

```json
{
  "name": "digital-twin-updater",
  "script": "~/.openclaw/workspace/digital_twin/update_twin.py",
  "interpreter": "python3",
  "cron_restart": "*/1 * * * *",
  "autorestart": false,
  "watch": false,
  "env": {
    "NODE_ENV": "production"
  }
}
```

---

## 8. Non-Goals (v1)

- No real-time streaming (WebSocket) — polling every 60s is sufficient.
- No historical analytics — snapshots provide timeline, full analytics is a future enhancement.
- No multi-machine twin — single Mac mini host only.
- No AI-assisted anomaly detection — score-based thresholds are sufficient for v1.

---

## 9. References

- Observability Spec (Enhancement #2) — health endpoints feed agent state
- Event-Driven Ops (Enhancement #7) — events feed `alerts_active`
- Drift Detection Spec (Enhancement #10) — drift status feeds `drift_detected`
- Registry-First Policy (Enhancement #6) — registered assets match twin topology
- Knowledge Graph Seed (Enhancement #1) — graph schema aligns with twin structure
