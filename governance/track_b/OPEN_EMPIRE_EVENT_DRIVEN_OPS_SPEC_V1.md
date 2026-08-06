# OPEN EMPIRE — EVENT-DRIVEN OPERATIONS SPEC V1
## Foundational Enhancement #7: Event-Driven Operations

**Status:** SPEC  
**Version:** 1.0.0  
**Created:** 2026-08-06  
**Operator:** Nathan Asiegbu  
**Governed by:** Open Empire Constitution v2, Governance Baseline v1.0.0 (commit 17df0ff)

---

## 1. Executive Summary

Open Empire currently operates on a **polling model**: PM2 cron jobs fire every 5–15 minutes regardless of whether there is work to do. This is functional but inefficient, creates detection lag, and does not support reactive operations.

This spec defines the target **event-driven operations model**: key state changes emit events, events route through n8n, and the right actions fire automatically — no polling required for event-class operations.

**Current state:** n8n is online but has 0 workflows deployed. This spec is the blueprint for those first workflows.

---

## 2. Event Taxonomy

### Event Schema (Standard)

All events MUST conform to this envelope:

```json
{
  "event_id": "uuid4",
  "event_type": "<EVENT_TYPE>",
  "source": "<service-name>",
  "timestamp": "2026-08-06T12:00:00Z",
  "priority": "P0|P1|P2|P3|INFO",
  "payload": {},
  "dedup_key": "<event_type>:<source>:<context_hash>",
  "dedup_window_seconds": 300
}
```

---

### 2.1 GOVERNANCE_CHANGE

**Description:** Any modification to the `~/.openclaw/workspace/governance/` directory.

```json
{
  "event_type": "GOVERNANCE_CHANGE",
  "priority": "P0",
  "triggers": [
    "Verify SHA256 of changed file against SHA256SUMS",
    "If SHA256 mismatch: emit GOVERNANCE_TAMPERED (P0 CRITICAL)",
    "If authorized change: update SHA256SUMS",
    "Send Telegram notification with diff summary",
    "Log to governance_change.jsonl"
  ],
  "channels": ["telegram", "n8n", "governance_change.jsonl"],
  "dedup_window_seconds": 60,
  "detection_method": "inotifywait on governance/ directory OR cron SHA256 check every 5min",
  "current_gap": "No inotify watcher deployed. SHA256 check is manual."
}
```

---

### 2.2 TRADE_PLACED

**Description:** A trade order is submitted by cashclaw_director, cashclaw_arb, or polymarket-trader.

```json
{
  "event_type": "TRADE_PLACED",
  "priority": "INFO",
  "triggers": [
    "Append to trades.jsonl",
    "Update daily spend counter",
    "Check if spend > 80% of daily cap → emit BUDGET_ALERT",
    "Check if spend = daily cap → emit BUDGET_HARD_STOP",
    "Send Telegram digest (batched, max 1/minute)"
  ],
  "channels": ["telegram", "n8n", "trades.jsonl"],
  "dedup_window_seconds": 5,
  "payload_fields": ["platform", "market_id", "side", "size_usd", "price", "order_id"],
  "source_services": ["cashclaw_director", "cashclaw_arb", "polymarket-trader"]
}
```

---

### 2.3 TRADE_SETTLED

**Description:** An open position resolves (YES/NO fills, expiry).

```json
{
  "event_type": "TRADE_SETTLED",
  "priority": "INFO",
  "triggers": [
    "Update P&L in trade ledger",
    "Update running balance",
    "Send Telegram P&L update",
    "Trigger P&L audit if daily loss > $5"
  ],
  "channels": ["telegram", "n8n", "trades.jsonl"],
  "dedup_window_seconds": 10,
  "payload_fields": ["platform", "market_id", "outcome", "profit_usd", "balance_after"],
  "source_services": ["trading_sentinel", "cashclaw_director"]
}
```

---

### 2.4 AGENT_DOWN

**Description:** A PM2 process stops unexpectedly (status changes from online to stopped/errored without an explicit `pm2 stop` command).

```json
{
  "event_type": "AGENT_DOWN",
  "priority": "P0",
  "triggers": [
    "Immediate Telegram alert with process name, exit code, last 10 log lines",
    "If trading agent: pause companion trading agents (safety net)",
    "Attempt auto-restart after 30 seconds if not a CRITICAL trading agent",
    "If trading agent: require Nathan approval for restart",
    "Log to agent_down.jsonl"
  ],
  "channels": ["telegram", "n8n"],
  "dedup_window_seconds": 60,
  "payload_fields": ["pm2_name", "pm2_id", "exit_code", "restart_count", "last_log_lines"],
  "source_services": ["trading_sentinel", "pm2-prometheus-exporter"],
  "trading_agents": ["cashclaw_director", "cashclaw_arb", "polymarket-trader", "trading_sentinel"]
}
```

---

### 2.5 VALIDATION_FAILED

**Description:** The governance validation suite runs and finds a FAIL result (SHA256 mismatch, missing artifact, constitutional breach).

```json
{
  "event_type": "VALIDATION_FAILED",
  "priority": "P0",
  "triggers": [
    "Immediate Telegram alert with failing check name and details",
    "Block any new deployments until resolved",
    "Log to validation_failures.jsonl",
    "Notify Nathan for manual review"
  ],
  "channels": ["telegram", "n8n"],
  "dedup_window_seconds": 300,
  "payload_fields": ["check_name", "expected_hash", "actual_hash", "artifact_path", "severity"],
  "source_services": ["executor", "governance-validator (to-build)"]
}
```

---

### 2.6 BUDGET_ALERT

**Description:** Daily spend on any trading platform exceeds threshold relative to daily cap.

```json
{
  "event_type": "BUDGET_ALERT",
  "priority": "P1",
  "thresholds": [
    {"level": "WARN", "pct_of_cap": 80, "priority": "P1"},
    {"level": "CRITICAL", "pct_of_cap": 100, "priority": "P0", "action": "HARD_STOP"}
  ],
  "triggers": {
    "WARN": [
      "Telegram warning with spend/cap breakdown",
      "Log to budget_alerts.jsonl"
    ],
    "CRITICAL": [
      "Telegram CRITICAL alert",
      "pm2 stop cashclaw_director cashclaw_arb polymarket-trader",
      "sentinel stays running for monitoring",
      "Require Nathan approval to resume"
    ]
  },
  "channels": ["telegram", "n8n"],
  "dedup_window_seconds": 900,
  "payload_fields": ["platform", "spent_usd", "cap_usd", "pct_used", "remaining_usd"],
  "caps": {
    "cashclaw_director": 10,
    "cashclaw_arb": 10,
    "polymarket-trader": 10,
    "ai_ops_daily": 0.20
  }
}
```

---

### 2.7 REPO_PUSH

**Description:** A push to the `main` branch of any UA4200 GitHub repository.

```json
{
  "event_type": "REPO_PUSH",
  "priority": "P2",
  "triggers": [
    "Run governance validation on changed files",
    "Update SHA256SUMS for changed artifacts",
    "Trigger deployment pipeline if applicable (future CI/CD)",
    "Send Telegram notification with commit summary",
    "Check for unregistered new services in code"
  ],
  "channels": ["telegram", "n8n"],
  "dedup_window_seconds": 30,
  "payload_fields": ["repo", "branch", "commit_sha", "commit_message", "author", "changed_files"],
  "implementation": {
    "source": "GitHub webhook → POST to OpenClaw gateway",
    "webhook_url": "http://127.0.0.1:<gateway-port>/webhook/github",
    "github_repos": [
      "UA4200/open-empire",
      "UA4200/trading",
      "UA4200/mission-control",
      "UA4200/alusi",
      "UA4200/blco",
      "UA4200/hyrvea"
    ],
    "current_gap": "No GitHub webhook configured. Repos exist but webhook endpoint not deployed."
  }
}
```

---

### 2.8 REGISTRY_MUTATION

**Description:** A new asset is registered in any registry file (Master Registry, Runtime Registry, UUID Registry).

```json
{
  "event_type": "REGISTRY_MUTATION",
  "priority": "P2",
  "triggers": [
    "Update SHA256SUMS for modified registry file",
    "Send Telegram notification with asset name and type",
    "Log to registry_mutations.jsonl",
    "Trigger knowledge graph rebuild (future)"
  ],
  "channels": ["telegram", "n8n"],
  "dedup_window_seconds": 30,
  "payload_fields": ["registry_name", "asset_name", "asset_type", "uuid", "mutation_type"],
  "mutation_types": ["CREATED", "UPDATED", "DEPRECATED", "DECOMMISSIONED"]
}
```

---

### 2.9 HEALTH_DEGRADED

**Description:** A service health check returns `status: degraded` or `status: unhealthy`.

```json
{
  "event_type": "HEALTH_DEGRADED",
  "priority": "P1",
  "triggers": [
    "Telegram notification with service name and failing checks",
    "Log to health_events.jsonl",
    "If 3 consecutive degraded results: escalate to P0 and page Nathan"
  ],
  "channels": ["telegram", "n8n"],
  "dedup_window_seconds": 300,
  "payload_fields": ["service_name", "health_url", "status", "failing_checks", "consecutive_count"],
  "source_services": ["pm2-health-poller (to-build)"],
  "current_gap": "No /health endpoints exist yet. Blocked on Observability Spec Phase 2."
}
```

---

## 3. Event Routing Architecture

```
[Event Source]              [Router]           [Sink]
─────────────              ─────────          ──────
PM2 process exit     →
GitHub webhook       →
Trade log append     →    n8n Workflow    →  Telegram alert
Cron validator       →    Engine          →  PM2 action
Health endpoint      →    (port TBD)      →  trades.jsonl
inotify watch        →                   →  governance log
```

### n8n Workflow Routing Table (Target)

| Workflow ID | Trigger Event | n8n Flow Name |
|-------------|---------------|---------------|
| WF-001 | AGENT_DOWN (trading) | Trading Agent Down - Emergency |
| WF-002 | AGENT_DOWN (non-trading) | Service Down - Auto Restart |
| WF-003 | BUDGET_ALERT (WARN) | Spend Cap Warning |
| WF-004 | BUDGET_ALERT (CRITICAL) | Spend Cap Hard Stop |
| WF-005 | GOVERNANCE_CHANGE | Governance Change Validator |
| WF-006 | VALIDATION_FAILED | Validation Failure Alert |
| WF-007 | TRADE_PLACED | Trade Notification (batched) |
| WF-008 | TRADE_SETTLED | P&L Update |
| WF-009 | REPO_PUSH | GitHub Push Handler |
| WF-010 | HEALTH_DEGRADED | Health Degraded Alert |
| WF-011 | REGISTRY_MUTATION | Registry Update Notifier |

**Current state:** n8n online, 0 of 11 workflows deployed.

---

## 4. Implementation Plan

### Phase 1 — Foundation (Days 1–7)
*Prerequisites: n8n is online (already true).*

| Task | Owner | Acceptance Criteria |
|------|-------|---------------------|
| Deploy WF-003: Spend Cap Warning | Alusi | Simulated 80% spend triggers Telegram |
| Deploy WF-004: Spend Cap Hard Stop | Alusi | Simulated 100% spend stops trading agents |
| Deploy WF-001: Trading Agent Down | Alusi | `pm2 stop cashclaw_director` triggers Telegram in <30s |
| Build `pm2-event-watcher.py` script | Alusi | Polls pm2 jlist, emits AGENT_DOWN events |
| Wire AGENT_DOWN → n8n webhook | Alusi | Full path: pm2 stop → script → n8n → Telegram |

**Acceptance Gate:** P0 events (agent down, spend cap breach) trigger Telegram within 60 seconds.

---

### Phase 2 — Governance Events (Days 8–14)
*Prerequisites: Phase 1 complete, health endpoints from Observability Spec Phase 2.*

| Task | Owner | Acceptance Criteria |
|------|-------|---------------------|
| Deploy WF-005: Governance Change | Alusi | Edit a governance file → Telegram notification |
| Deploy WF-006: Validation Failure | Alusi | Corrupt a SHA256 → Telegram P0 alert |
| Deploy WF-011: Registry Mutation | Alusi | Add registry entry → Telegram notification |
| Deploy WF-007: Trade Placed (batched) | Alusi | Trades batch to Telegram max 1/minute |
| Build governance inotify watcher OR cron | Alusi | SHA256 checked every 5 minutes |

---

### Phase 3 — Full Event Grid (Days 15–30)
*Prerequisites: Phase 2 complete, GitHub repos accessible.*

| Task | Owner | Acceptance Criteria |
|------|-------|---------------------|
| Deploy WF-009: GitHub Push Handler | Nathan + Alusi | GitHub push → n8n webhook → Telegram |
| Configure GitHub webhooks (all 6 repos) | Nathan | Webhooks active, events firing |
| Deploy WF-010: Health Degraded | Alusi | Health endpoint fail → Telegram |
| Deploy WF-008: Trade Settled | Alusi | Settlement → P&L Telegram update |
| Deploy WF-002: Non-trading auto-restart | Alusi | Non-trading service down → auto restart |

---

## 5. Event Dedup Policy

Events with the same `dedup_key` will be suppressed within `dedup_window_seconds`.

**Dedup key format:** `<event_type>:<source>:<context_hash>`

**Example:**
- AGENT_DOWN:cashclaw_director:exit-1 → suppress second alert for 60 seconds.
- BUDGET_ALERT:cashclaw_director:warn-80pct → suppress repeat for 900 seconds.
- GOVERNANCE_CHANGE:SHA256SUMS:modified → suppress within 60 seconds.
- CRITICAL events: **never dedup** — always send.

**Implementation:** n8n has built-in dedup via the "Deduplicate" or "Wait" nodes. Redis not required.

---

## 6. Telegram Alert Format Standards

### P0 Critical
```
🚨🚨🚨 [P0-CRITICAL] Open Empire
Event: AGENT_DOWN
Service: cashclaw_director (pm2:38)
Time: 2026-08-06 12:00:00 CDT
Exit Code: 1
Restart Count: 3
Last Log: [2026-08-06T12:00:00Z] ERROR: Kalshi API timeout

⚠️ TRADING PAUSED — approval required to resume
Dashboard: http://127.0.0.1:3333
```

### P1 High
```
⚠️ [P1-HIGH] Open Empire
Event: BUDGET_ALERT
Platform: kalshi (cashclaw_director)
Spent: $8.12 / $10.00 (81%)
Remaining: $1.88
Time: 2026-08-06 12:00:00 CDT
```

### INFO
```
✅ [TRADE] Kalshi
Market: Will-BTC-100k-Aug
Side: YES | Size: $1.25
Price: 0.62 | Expected: $2.02
Time: 2026-08-06 12:00:00 CDT
```

---

## 7. Non-Goals (v1)

- No pub/sub message broker (RabbitMQ, Kafka) — n8n webhook-based routing is sufficient.
- No event replay or event sourcing architecture.
- No external webhooks to third-party services without Nathan approval.
- No real-time streaming — polling at appropriate cadence is acceptable for non-critical events.

---

## 8. References

- Open Empire Constitution v2
- Governance Baseline v1.0.0 — commit 17df0ff
- AGENTS.md — PM2 process registry
- Observability Spec (Enhancement #2) — health endpoints required for HEALTH_DEGRADED
- Drift Detection Spec (Enhancement #10) — governance drift feeds GOVERNANCE_CHANGE
- Digital Twin Spec (Enhancement #8) — event log feeds digital twin state
