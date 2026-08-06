# Open Empire — Mission Control Integration Plan
**Version:** 1.0.0 | **Date:** 2026-08-06 | **Ref:** B4  
**Governed by:** OPEN_EMPIRE_GOVERNANCE_BASELINE_V1.0.0

---

## Overview

Mission Control (port 3333, pm_id=14) is the designated command center for the Open Empire. Currently it runs as a standalone UI with no live data feeds from the governance registry, runtime services, or trading systems. This plan wires all critical data streams into Mission Control to create a true single pane of glass.

---

## Current State

| Component | Status |
|-----------|--------|
| Mission Control service | ✅ Running (pm_id=14, port=3333) |
| Source code location | `~/.openclaw/workspace/mission-control/` |
| Governance registry data | ❌ Not connected |
| Runtime PM2 status | ❌ Not connected |
| Portfolio/program data | ❌ Not connected |
| Trading P&L feed | ❌ Not connected |
| Alert streams | ❌ Not connected |
| n8n workflow status | ❌ Not connected |
| Telemetry (nexus-telemetry) | ⚠️ Exists but not wired to MC |

**Gap Summary:** Mission Control is running but is a blank canvas — none of the 20 registered capabilities feed data into it.

---

## Integration Requirements

### R1 — Governance Validation Results Display
- **What:** Show current governance status, last validation run, registry versions, open issues
- **Source:** `~/.openclaw/workspace/governance/build/validate.py` output + track_b registry files
- **Endpoint to add:** `GET /api/governance/status`
- **Display:** Governance panel showing: schema version, last run timestamp, pass/fail counts, flagged issues

### R2 — Runtime Registry Live Topology View
- **What:** Visual service topology derived from OPEN_EMPIRE_RUNTIME_DEPENDENCY_GRAPH_V1.json
- **Source:** Runtime registry + dependency graph JSON files
- **Endpoint to add:** `GET /api/runtime/topology`
- **Display:** Interactive graph: nodes (services) + edges (dependencies). Highlight DEGRADED/STOPPED nodes in red.

### R3 — PM2 Process Monitor
- **What:** Live PM2 process status table (name, pm_id, status, pid, restarts, uptime)
- **Source:** `pm2 jlist` via exec-gateway (approved) or pm2 API if available
- **Endpoint to add:** `GET /api/processes` — proxies PM2 status
- **Display:** Sortable table, color-coded: online=green, stopped=grey, degraded(high restarts)=red
- **Refresh:** Every 30 seconds

### R4 — Portfolio Status Executive Dashboard
- **What:** Portfolio health overview from OPEN_EMPIRE_PORTFOLIO_REGISTRY_V1.json
- **Source:** Portfolio + Program + Venture registry JSONs
- **Endpoint to add:** `GET /api/portfolio/summary`
- **Display:** Card grid per portfolio with status badge, capital, active programs count, risk level

### R5 — Trading P&L Financial Panel
- **What:** Live trading P&L from clawdb.daily_pnl and clawdb.trades
- **Source:** PostgreSQL `clawdb` database, `daily_pnl` and `trades` tables
- **Endpoint to add:** `GET /api/trading/pnl?days=7`
- **Display:** P&L chart (7-day rolling), total deployed capital ($65.19), today's trades, daily spend vs cap

### R6 — Alert Streams Notification Center
- **What:** Consolidated alert stream from trading_sentinel, exec-gateway, telegram-approvals
- **Source:** `clawdb.agent_events` + `clawdb.health_log` + exec-gateway queue
- **Endpoint to add:** `GET /api/alerts/recent?limit=50`, WebSocket `ws://127.0.0.1:3333/ws/alerts`
- **Display:** Notification feed with severity (INFO/WARN/CRITICAL), source agent, timestamp, dismiss action

### R7 — n8n Workflow Status Panel
- **What:** n8n workflow registry status (currently 0 workflows)
- **Source:** n8n REST API at `http://127.0.0.1:5678/api/v1/workflows`
- **Endpoint to add:** `GET /api/automation/workflows`
- **Display:** Workflow list with last execution, success/failure, next scheduled run. Show "0 workflows" warning prominently.

---

## Implementation Phases

### Phase 1 — API Endpoints in Mission Control (Week 1)
**Goal:** Add REST API endpoints to Mission Control server to accept registry data pushes and expose data to frontend.

Tasks:
1. [ ] Inspect `~/.openclaw/workspace/mission-control/` source to understand tech stack
2. [ ] Add `GET /api/health` endpoint (sanity check)
3. [ ] Add `POST /api/registry/push` endpoint to accept JSON registry payloads
4. [ ] Add `GET /api/governance/status` from governance validate.py output
5. [ ] Add `GET /api/processes` reading from PM2 API or pm2 jlist
6. [ ] Test all Phase 1 endpoints with curl

**Blocker:** Source code inspection required first. Tech stack unknown until `~/.openclaw/workspace/mission-control/` is read.

### Phase 2 — Registry Sync (Week 1-2)
**Goal:** Pipe Track B registry files into Mission Control API on a schedule.

Tasks:
1. [ ] Write `registry_sync.py` script that reads all Track B JSON files and POSTs to MC `/api/registry/push`
2. [ ] Register registry_sync as a cron job (every 5 minutes)
3. [ ] Add `GET /api/portfolio/summary` from portfolio/program/venture registries
4. [ ] Add `GET /api/runtime/topology` from dependency graph
5. [ ] Verify MC frontend can consume new endpoints

### Phase 3 — Live Dashboards (Week 2-3)
**Goal:** Frontend dashboards consuming all live data.

Tasks:
1. [ ] Portfolio status card grid (R4)
2. [ ] Runtime topology graph (R2) — recommend using vis.js or D3
3. [ ] PM2 process table with 30s refresh (R3)
4. [ ] Trading P&L chart connecting to clawdb (R5)
5. [ ] n8n workflow panel (R7)

### Phase 4 — Alerting (Week 3-4)
**Goal:** Real-time alert streams into MC notification center.

Tasks:
1. [ ] WebSocket endpoint for live alerts (R6)
2. [ ] Connect trading_sentinel alert log to MC
3. [ ] Connect exec-gateway approval queue to MC
4. [ ] Governance validation failure alerts
5. [ ] DEGRADED service alerts (staging services, high restart counts)
6. [ ] Daily spend cap approach warnings (80% threshold)

---

## Required: MC REST API for Registry Pushes

Mission Control **must** expose a REST API accepting `POST /api/registry/push` with payload:
```json
{
  "registry_type": "portfolio|capability|runtime|agent",
  "version": "1.0.0",
  "timestamp": "2026-08-06T12:40:00Z",
  "data": { ... }
}
```
Authentication: internal token only (127.0.0.1 loopback, not externally exposed).

---

## Blockers

| Blocker | Owner | Action Required |
|---------|-------|-----------------|
| MC source code not yet inspected | Nathan | Run `read ~/.openclaw/workspace/mission-control/` to audit tech stack |
| PM2 API vs jlist approach unclear | Agent | Inspect if pm2 module exposed via API or jlist required via exec |
| clawdb schema needs verification | Agent | Confirm `daily_pnl` and `trades` column names before writing queries |
| n8n API auth credentials | Nathan | Confirm n8n username/password for API calls |

---

## Success Criteria

| Criteria | Target |
|----------|--------|
| All 7 data streams wired | Phase 4 complete |
| PM2 table refreshes live | Phase 3 |
| Portfolio dashboard visible | Phase 3 |
| Trading P&L panel visible | Phase 3 |
| Alert notification center live | Phase 4 |
| Topology graph renders | Phase 3 |
| Registry sync running every 5min | Phase 2 |

---

*Plan created: 2026-08-06 | Owner: Nathan Asiegbu | Governed by OPEN_EMPIRE_GOVERNANCE_BASELINE_V1.0.0*
