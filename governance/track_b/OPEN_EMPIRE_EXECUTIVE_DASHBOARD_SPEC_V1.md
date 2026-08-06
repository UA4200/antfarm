# OPEN EMPIRE — EXECUTIVE DASHBOARDS SPEC V1
## B7 Executive Dashboards Specification

**Status:** SPEC  
**Version:** 1.0.0  
**Created:** 2026-08-06  
**Operator:** Nathan Asiegbu  
**Governed by:** Open Empire Constitution v2, Governance Baseline v1.0.0 (commit 17df0ff)

---

## 1. Overview

Mission Control (port 3333) currently serves as the primary operational interface. This spec defines **7 role-based dashboards** to be built within Mission Control, each providing a focused view for a different operational role.

All dashboards are for Nathan's personal use. Role labels (CEO, COO, etc.) represent **operational perspectives**, not separate users.

**Implementation target:** Mission Control React app (`~/.openclaw/workspace/mission-control`)  
**Data refresh model:** Polling via REST API endpoints  
**Primary data source:** Digital Twin `current_state.json` (Enhancement #8)

---

## 2. Mission Control Data Architecture

### 2.1 API Layer (to build in mission-control backend)

```
GET /api/twin/current             → Full current_state.json
GET /api/twin/runtime             → Runtime state only
GET /api/twin/financial           → Financial state only
GET /api/twin/governance          → Governance state only
GET /api/pm2/status               → Live pm2 jlist
GET /api/trading/pnl?days=7       → P&L summary
GET /api/trading/trades?limit=20  → Recent trades
GET /api/governance/validation    → Last validation result
GET /api/github/repos             → Repo sync status
GET /api/alerts/active            → Active alert queue
GET /api/registry/completeness    → Registry stats
```

### 2.2 Data Sources Matrix

| Data Type | Source | Refresh Rate |
|-----------|--------|-------------|
| PM2 process status | `pm2 jlist` via API | 30s |
| Trading balances | Trade log JSONL | 5min |
| Daily spend | Trade log JSONL (today's sum) | 5min |
| Governance validation | SHA256SUMS check | 5min |
| GitHub repo status | `git fetch` result | 15min |
| Alert queue | n8n webhook / log | 30s |
| Registry completeness | Registry JSON count | 5min |
| AI spend | API provider billing endpoints | 1h |
| Empire health score | Digital twin computed | 60s |

---

## 3. Dashboard Specifications

---

### 3.1 CEO DASHBOARD — Strategic Command

**Purpose:** Nathan's top-level situational awareness. Answer in 10 seconds: Is the Empire healthy? Am I making money?  
**Default route:** `/` (home)  
**Refresh rate:** 60 seconds

#### Panels

**Panel 1: Empire Health Score (Hero)**
- Type: Large circular gauge (0–100%)
- Data: `current_state.empire_health_score * 100`
- Color: Green (≥90), Yellow-Green (≥70), Yellow (≥50), Orange (≥30), Red (<30)
- Label: "EMPIRE HEALTH"
- Refresh: 60s

**Panel 2: Revenue Status**
- Type: KPI cards (3 in row)
- Card A: "Trading P&L (7d)" — source: trades.jsonl rolling sum
- Card B: "Pipeline Value" — source: manual entry or BLCO lead count × estimated deal size
- Card C: "Monthly Projection" — source: (7d P&L / 7) × 30
- Refresh: 5min

**Panel 3: Portfolio Health Grid**
- Type: Status cards (5 portfolios)
- Each card shows: name, status badge, active capabilities count, last activity
- Data: Capability Activation Spec status map

| Portfolio | Status | Capabilities | Revenue |
|-----------|--------|-------------|---------|
| Moltlaunch | 🟢 ACTIVE | Trading x2 | $XX/day |
| BLCO | 🟡 PAUSED | 0 active | $0 |
| ADAI | 🔵 PRE_LAUNCH | 0 active | $0 |
| Content | 🟢 ACTIVE | Content x1 | TBD |
| Infrastructure | 🟢 ACTIVE | Core | N/A |

**Panel 4: Top 3 Risks**
- Type: Ordered list
- Source: Manually maintained + auto-detected from drift/alerts
- Default risks (as of 2026-08-06):
  1. Trading cap breach risk ($10/day hard limit)
  2. Kalshi/Polymarket API auth expiry
  3. Registry drift (staging services degraded)

**Panel 5: Top 3 Opportunities**
- Type: Ordered list
- Source: Manually maintained
- Default opportunities (as of 2026-08-06):
  1. n8n workflows deployment (event-driven ops not yet active)
  2. BLCO resumption (192 leads staged, ready to activate)
  3. Digital twin deployment (replaces manual status checks)

**Panel 6: Monthly Income Goal Tracker**
- Type: Progress bar
- Target: $12,000–$30,000/month
- Current: Sum of all P&L sources
- Refresh: Daily

---

### 3.2 COO DASHBOARD — Operational Command

**Purpose:** Is everything running? What needs attention right now?  
**Route:** `/ops` or `/coo`  
**Refresh rate:** 30 seconds

#### Panels

**Panel 1: PM2 Process Health Grid**
- Type: Grid of process status badges
- Data: `pm2 jlist` mapped to status colors
- Show: All 42 processes, sorted by criticality (trading first)
- Color: Green=online, Yellow=degraded, Red=stopped/errored

**Process Priority Groups:**

| Group | Processes |
|-------|-----------|
| CRITICAL | executor, alusi-gateway, clawdb, exec-gateway |
| TRADING | cashclaw_director, cashclaw_arb, polymarket-trader, trading_sentinel |
| COMMUNICATIONS | alusi-telegram-adapter, alusi-discord-adapter, telegram-approvals |
| CONTENT | hyrvea-monitor |
| STAGING | open-empire-federation-staging, open-empire-lifecycle-staging |
| ON_DEMAND | email-dispatcher, pnl-audit, openclaw-dashboard |

**Panel 2: Service Uptime Percentages**
- Type: Table with sparklines
- Data: PM2 `pm_uptime` vs current time
- Columns: Service, Uptime %, Restarts (24h), Last Restart

**Panel 3: Daily Task Completion**
- Type: Checklist / progress tracker
- Items: Trading cycles completed today, governance validation last run, drift check last run
- Data: Log parsing

**Panel 4: Pending Approvals Queue**
- Type: List
- Data: `~/.openclaw/vault/approvals/` — unprocessed items
- Action buttons: Approve / Reject (links to approval flow)

**Panel 5: Alert Count by Severity**
- Type: Bar chart or counter badges
- Data: Today's alerts from n8n/Telegram
- Breakdown: P0 (red), P1 (orange), P2 (yellow), P3 (green), INFO (blue)

**Panel 6: Degraded Services Detail**
- Type: Expandable list
- Auto-populates when any service has restart_count > 3 in last hour
- Shows: service name, restart count, last log lines

---

### 3.3 CFO DASHBOARD — Financial Command

**Purpose:** How much money do I have? Am I within caps? What's the trend?  
**Route:** `/finance` or `/cfo`  
**Refresh rate:** 5 minutes

#### Panels

**Panel 1: Kalshi Position Summary**
- Type: Card with metrics
- Data: Trade log JSONL + Kalshi API (when health endpoint built)
- Fields:
  - Balance: $1.55 free
  - Open Orders: $80.00
  - Total Deployed: $81.55
  - Daily Spend Today: $X.XX / $10.00
  - Spend % Bar (green/yellow/red)
  - Last Trade: timestamp + market name

**Panel 2: Polymarket Position Summary**
- Type: Card with metrics
- Fields:
  - Balance: $0.06
  - Open Orders: $0.00
  - Daily Spend Today: $X.XX / $10.00
  - Spend % Bar
  - Last Trade: timestamp + market name

**Panel 3: Daily AI Spend Tracker**
- Type: Gauge with target line
- Current spend: $X.XX
- Daily target: $0.20
- Overage: highlighted in red
- Breakdown: Anthropic, OpenAI, Other

**Panel 4: Daily Spend Cap Status (All Agents)**
- Type: 3-row table
- Rows: cashclaw_director, cashclaw_arb, polymarket-trader
- Columns: Agent, Spent Today, Cap, %, Status
- Alert threshold: Yellow at 80%, Red at 100%

**Panel 5: P&L Trend (7-day)**
- Type: Line chart
- Data: trades.jsonl — daily realized P&L
- X: last 7 days, Y: USD profit/loss
- Show: cumulative line + per-day bars

**Panel 6: Trade Activity Feed**
- Type: Scrolling list (last 20 trades)
- Columns: Time, Platform, Market, Side, Size, Outcome (if settled)
- Color: Green for wins, Red for losses, Grey for pending

---

### 3.4 CTO DASHBOARD — Technical Command

**Purpose:** Is the code healthy? Are repos in sync? Is the build pipeline working?  
**Route:** `/tech` or `/cto`  
**Refresh rate:** 15 minutes (repos), 60s (services)

#### Panels

**Panel 1: GitHub Repository Status**
- Type: Table
- Repos: 6 UA4200 repositories
- Columns: Repo, Branch, Local vs Remote (ahead/behind), Last Push, Status
- Color: Green=in sync, Yellow=behind, Orange=ahead, Red=diverged

**Panel 2: CI/CD Pipeline Status**
- Type: Status cards
- Note: No CI/CD deployed yet — panel shows "NOT YET CONFIGURED"
- Placeholder shows planned: GitHub Actions → deploy on push to main

**Panel 3: Governance Validation Suite**
- Type: Status widget
- Last run: timestamp
- Result: PASS / FAIL badge
- Artifacts checked: count of files verified
- Next scheduled run: next 5-minute cron

**Panel 4: Drift Detection Status**
- Type: 6-row grid (one per layer)
- Each row: Layer name, Status (CLEAN/DRIFT/UNKNOWN), Last checked, Drift items count
- Layers: Governance, Registry, Repository, Runtime, Infrastructure, Configuration

**Panel 5: Ollama Model Inventory**
- Type: Table
- Data: `ollama list` output via API
- Columns: Model Name, Size, Last Used
- Note: 6 models installed as of 2026-08-06

**Panel 6: Service Health Endpoints**
- Type: Grid
- Shows health endpoint status for all services that have `/health` (Phase 2)
- Until implemented: shows "HEALTH ENDPOINTS PENDING (Observability Phase 2)"

---

### 3.5 PMO DASHBOARD — Governance & Program Management

**Purpose:** Is governance healthy? What is Track B progress? What's open?  
**Route:** `/pmo` or `/governance`  
**Refresh rate:** 5 minutes

#### Panels

**Panel 1: Governance Baseline Status**
- Type: Status card
- Baseline: FROZEN v1.0.0
- Commit: 17df0ff
- SHA256 integrity: VERIFIED / TAMPERED
- Last verified: timestamp

**Panel 2: Track B Progress**
- Type: Progress table
- Enhancement list with status per enhancement

| # | Enhancement | Status |
|---|-------------|--------|
| 1 | Enterprise Knowledge Graph | SEED — file-based v1 |
| 2 | Observability Stack | SPEC — not implemented |
| 3 | Secrets Governance | METADATA_COMPLETE |
| 4 | Governance Automation | SPEC (not in Track B file set) |
| 5 | Asset UUID Registry | REGISTERED |
| 6 | Registry-First Policy | ACTIVE |
| 7 | Event-Driven Ops | SPEC — n8n workflows pending |
| 8 | Digital Twin | SPEC — update_twin.py pending |
| 9 | API Gateway | SPEC (not in Track B file set) |
| 10 | Drift Detection | SPEC — detector.py pending |

**Panel 3: Open Defects / Known Issues**
- Type: Issue list
- Source: Manually maintained or parsed from governance notes

Current known issues (2026-08-06):
1. PM2 IDs 45, 46 degraded (high restarts) — needs investigation
2. AGENTS.md stale PM2 IDs — registry reconciliation needed
3. Grafana port 3001 — status unknown, needs health check
4. n8n 0 workflows — event routing not active
5. No `/health` endpoints on any service

**Panel 4: Registry Completeness**
- Type: Gauge percentage
- Data: (registered assets / total known assets) × 100
- Components:
  - PM2 services: X/42
  - Capabilities: X/20
  - Repositories: X/22
  - Documents: X/12

**Panel 5: Open Approvals (PMO View)**
- Type: List
- Data: approvals.jsonl pending items
- Different from COO view — focuses on governance approvals vs operational

**Panel 6: Governance Change Log (last 10)**
- Type: Feed
- Source: governance_change.jsonl (Enhancement #7 event log)
- Shows: timestamp, changed file, authorized/unauthorized, actor

---

### 3.6 TRADING DASHBOARD — Dedicated Trading Operations

**Purpose:** Full-screen trading view. Single pane for all trading activity.  
**Route:** `/trading`  
**Refresh rate:** 30 seconds

#### Panels

**Row 1: Spend Caps (Large)**
- Three gauges: CashClaw Director | CashClaw ARB | Polymarket
- Each: spent/cap with color coding

**Row 2: Active Positions**
- Table: open orders on Kalshi and Polymarket
- Columns: Platform, Market, Side, Size, Current Price, P&L Est.

**Row 3: Trade Feed (Today)**
- All trades from trades.jsonl today
- Live-updating

**Row 4: Agent Status**
- 4 process status badges: director, arb, polymarket-trader, sentinel
- Restart counts, last cycle time

**Row 5: Circuit Breaker Status**
- Sentinel circuit status (ok/tripped)
- Kill switch button (requires approval)

---

### 3.7 SYSTEM OVERVIEW (Full Topology)

**Purpose:** Visual map of entire Open Empire topology.  
**Route:** `/overview`  
**Refresh rate:** 60 seconds

#### Visualization

Render the Knowledge Graph Seed as a live network topology:
- Nodes: processes, databases, services (colored by status)
- Edges: dependency relationships
- Clickable nodes expand to service detail panel
- Zoom/pan enabled

**Tech:** D3.js or React Force Graph library

---

## 4. Implementation Plan

### Phase 1 — Foundation (Days 1–7)

| Task | Acceptance Criteria |
|------|---------------------|
| Create digital twin updater (Enhancement #8) | `current_state.json` written every 60s |
| Build `GET /api/twin/current` endpoint in mission-control | Returns JSON, 200 OK |
| Build `GET /api/pm2/status` endpoint | Returns pm2 jlist |
| Implement CEO Dashboard panels 1–3 | Health score, portfolio status live |
| Implement COO Dashboard panel 1 | PM2 process grid live |

### Phase 2 — Financial + Alerts (Days 8–14)

| Task | Acceptance Criteria |
|------|---------------------|
| Build trade log parser API endpoint | Returns daily spend per agent |
| Implement CFO Dashboard | All 6 panels live with real data |
| Implement COO alerts panel | Alert count from n8n feeds in |
| Implement Trading Dashboard | Spend gauges live |

### Phase 3 — Governance + Full Suite (Days 15–30)

| Task | Acceptance Criteria |
|------|---------------------|
| Implement PMO Dashboard | Track B progress, validation status |
| Implement CTO Dashboard | Repo status, drift detection |
| Implement System Overview topology | Interactive graph renders |
| Connect all dashboards to digital twin | Single data source for all |

---

## 5. Technology Stack

| Layer | Technology | Notes |
|-------|-----------|-------|
| Frontend | React + Tailwind CSS | Already in mission-control |
| Charts | Recharts or Chart.js | Lightweight, React-native |
| Graph viz | React Force Graph | For system topology view |
| State | React Query (auto-refresh) | Poll-based with stale-while-revalidate |
| Backend | Express.js (already in mission-control) | Add API routes |
| Data | Digital twin JSON + pm2 CLI + JSONL parsing | No new DB required |

---

## 6. Non-Goals (v1)

- No mobile app — desktop browser only.
- No user authentication — loopback-bound, Nathan-only access.
- No historical drill-down charts beyond 7 days (snapshots provide raw data).
- No real-time WebSocket streaming — polling is sufficient.
- No multi-tenant or multi-operator views.

---

## 7. References

- Digital Twin Spec (Enhancement #8) — primary data source
- Observability Spec (Enhancement #2) — health endpoint data feeds
- Event-Driven Ops (Enhancement #7) — alert queue data
- Drift Detection Spec (Enhancement #10) — drift status panels
- Registry-First Policy (Enhancement #6) — registry completeness panel
- Knowledge Graph Seed (Enhancement #1) — topology visualization data
- AGENTS.md — PM2 process list
