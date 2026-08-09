# Obsidian ↔ Open Empire Integration Report
**Date:** 2026-08-09 | **Author:** Agent C (C0 Sprint) | **Status:** Strategic Design

---

## Executive Summary

Obsidian serves as the **human knowledge interface** for Open Empire — the layer where Nathan navigates, understands, and governs the sovereign AI ecosystem. Currently the workspace vault is operational but **not wired as a knowledge interface**: files exist but aren't connected, indexed, or surfaced as live intelligence.

This report defines: what Obsidian should do, what MOCs/indexes to create, how automated views work, and how it connects to Mission Control.

---

## 1. Role in the Open Empire Stack

```
┌─────────────────────────────────────────────────────────┐
│                     NATHAN (Human)                       │
│                          │                               │
│              Obsidian Knowledge Interface                │
│         (Navigate · Understand · Govern)                 │
│                          │                               │
├──────────────────────────┼──────────────────────────────┤
│         Mission Control (port 3333)                      │
│         (Live status · Metrics · Alerts)                 │
│                          │                               │
├──────────────────────────┼──────────────────────────────┤
│     Agents · Services · Databases · APIs                 │
│  (OpenClaw · PM2 · PostgreSQL · Kalshi · Polymarket)    │
└─────────────────────────────────────────────────────────┘
```

**Obsidian is NOT:**
- A real-time dashboard (that's Mission Control)
- An agent execution surface (that's Claude Code / OpenClaw)
- A database (that's ClawDB / PostgreSQL)

**Obsidian IS:**
- The knowledge layer where decisions are documented
- The human-readable view of system state
- The governance and constitution repository
- The strategic planning surface (goals, dreams, ventures)
- The memory archive (daily notes, learnings, retrospectives)

---

## 2. Key MOCs to Create

### 2.1 `HOME.md` — Vault Entry Point
**Purpose:** Single entry point for Nathan. Not an index — a contextual home base.

**Sections:**
- Today's focus (manual or Dataview from daily note)
- Live system links (Mission Control, PM2 dashboard)
- Quick navigation to all domains
- Governance quick-links
- Weekly review link

---

### 2.2 `EMPIRE_INDEX.md` — Venture Map
**Purpose:** Bird's eye view of all Open Empire business ventures.

**Content:**
```
Ventures:
- CashClaw (Kalshi prediction markets) → [[TRADING_INDEX]]
- BLCO Commodity Pipeline → [[BLCO_INDEX]]
- Open Empire Services (AI automation consulting, B2B outreach)
- Infrastructure Ventures (OpenClaw platform, Freeway proxy)

Revenue Status (manual/Dataview):
- CashClaw: $25.19 deployed | Target: $100+ monthly
- BLCO: 192 leads | Next: resume outreach
- Services: draft mode

Goals → [[GOALS]]
Governance → [[COUNCIL]] [[CONSTITUTION]]
```

---

### 2.3 `TRADING_INDEX.md` — Trading Operations Knowledge
**Purpose:** Understand the trading system, not monitor it (Mission Control does monitoring).

**Content:**
- CashClaw Director description + links to AGENTS.md entry
- Spend caps, Kelly criterion rules, risk parameters
- Arb strategy documentation
- Polymarket integration status
- Links to CASHCLAW.md, MOLTLAUNCH.md, directives/PHASE*.md
- Trade performance retrospectives (manually updated weekly)

---

### 2.4 `BLCO_INDEX.md` — BLCO Pipeline Knowledge
**Purpose:** BLCO venture documentation and outreach governance.

**Content:**
- Verified Seller status documentation
- Pipeline stage map (192 leads by region)
- Outreach approval workflow (draft-first rule)
- Email template library links
- Weekly report archive links (blco/reports/)
- BLCO_COMMAND.md executive summary

---

### 2.5 `INFRASTRUCTURE_INDEX.md` — System Architecture Knowledge
**Purpose:** Nathan can understand the full infrastructure without touching it.

**Content:**
- All PM2 agents with descriptions (from AGENTS.md)
- Port map (OpenClaw: 8787, Mission Control: 3333, PostgreSQL: 5432, Ollama: 11434, Freeway: 8082)
- Deployment history (links to directives/)
- Recovery runbooks (links to RESCUE_GATEWAY_RUNBOOK.md)
- GitHub repos (UA4200 org) and their purposes
- CI/CD status

---

### 2.6 `KNOWLEDGE_INDEX.md` — Research & Learning
**Purpose:** All knowledge resources — repos, research, benchmarks, guides.

**Content:**
- Installed repos index (awesome-claude-code-*, GSD, learn-claude-code, etc.)
- Research outputs (research_outputs/, CONSOLIDATED_REPO_LEARNINGS.md)
- Benchmarks (FREE_CLAUDE_CODE_COST_BENCHMARK.json, C0_TOKEN_COMPRESSION_BENCHMARK.json)
- PDF reference library (OC 1 vault: training guides, security guides)
- Learning notes / book notes (second-brain/ folder)

---

## 3. Automated Views (Agent-Driven)

These are views where **agents write the content, Obsidian surfaces it** — no manual maintenance.

### 3.1 Daily Briefing Note
**Source:** Morning Brief agent (projects/Morning_Brief/)
**Target:** `memory/YYYY-MM-DD.md` — auto-generated by agent each morning
**Format:**
```markdown
---
date: 2026-08-09
tags: [daily-briefing, auto-generated]
generated_by: morning-brief-agent
---
## System Status
- CashClaw: OK | Balance: $XX.XX | Last trade: ...
- BLCO: XX leads | ...
- Services: all green

## Today's Priority
...

## Overnight Events
...
```

### 3.2 Weekly Trade Report
**Source:** trading_sentinel agent (auto)
**Target:** `memory/weeks/YYYY-WW.md`
**Content:** P&L summary, win rate, notable trades, cap status

### 3.3 BLCO Weekly Report
**Source:** blco_broker agent (Monday 07:00 CDT)
**Target:** Existing `blco/reports/weekly_YYYY-WW.md` → symlink or embed in `BLCO_INDEX.md`

### 3.4 Agent Health Snapshot
**Source:** OpenClaw (write to workspace on heartbeat)
**Target:** `STATUS.md` — already auto-generated
**Enhancement:** Add YAML frontmatter so Dataview can query it

### 3.5 Spend Cap Dashboard (Dataview)
```dataview
TABLE spend_24h, cap, status
FROM "."
WHERE category = "spend-tracker"
```
Agents write frontmatter to small status notes; Dataview aggregates.

---

## 4. Mission Control ↔ Obsidian Connection

**Mission Control** (port 3333, Next.js) provides real-time operational data.
**Obsidian** provides knowledge context and governance.

### Integration Points

| Mission Control | Obsidian Link |
|---|---|
| Agent status panel | `AGENTS.md` — canonical definition |
| Trading P&L widget | `TRADING_INDEX.md` — context + rules |
| BLCO pipeline widget | `BLCO_INDEX.md` — governance |
| Alert history | `memory/YYYY-MM-DD.md` — incident notes |
| Deployment log | `INFRASTRUCTURE_INDEX.md` → `directives/` |

### Recommended: Mission Control → Obsidian Deep Link
Add a "Knowledge Base" link in Mission Control for each agent panel:
```
Agent: cashclaw_director
→ [View in Obsidian](obsidian://open?vault=workspace&file=TRADING_INDEX)
```

### Recommended: Obsidian Canvas Dashboard
Create `COMMAND_CANVAS.canvas` in workspace root using the Obsidian canvas plugin (already enabled):
- Node: EMPIRE_INDEX → linked to all venture MOCs
- Node: STATUS.md → live agent status
- Node: GOALS.md → current objectives
- Node: HEARTBEAT.md → circuit breakers
- Visual layout matching Mission Control structure

---

## 5. Open Empire File Tagging Schema

For Dataview queries to work, key files need YAML frontmatter. Proposed schema:

```yaml
---
# Core fields (all files)
category: governance | agent | project | venture | knowledge | daily
status: active | paused | archived | draft
last_updated: YYYY-MM-DD

# For agents
pm2_id: 0
port: 3333
auto_restart: true

# For ventures
revenue_stage: seed | growing | profitable
spend_cap_usd: 10

# For projects
priority: critical | high | medium | low
owner: alusi | nathan
---
```

---

## 6. Plugin Recommendations for Integration

| Plugin | Purpose | Priority |
|---|---|---|
| `dataview` | ✅ INSTALLED | Dynamic tables from frontmatter |
| `templater-obsidian` | ✅ INSTALLED | Auto-populate templates |
| `obsidian-tasks` | Task management with due dates | HIGH |
| `obsidian-kanban` | Visual project board | MEDIUM |
| `calendar` | Daily note calendar view | MEDIUM |
| `excalidraw` | Architecture diagrams | LOW |
| `obsidian-git` | Auto-commit vault to git | HIGH |
| `table-editor-obsidian` | Better table editing | LOW |

**Priority install:** `obsidian-git` — auto-commits the workspace vault changes, creating a history of Nathan's knowledge edits alongside code changes.

**Priority install:** `obsidian-tasks` — surfaces TODO items from across all vault files in one view, enabling Nathan to manage Open Empire actions without a separate task app.

---

## 7. Implementation Roadmap

### Phase 1 — Foundation (1-2 hours, non-destructive)
- [ ] Create `.obsidianignore`
- [ ] Create `HOME.md`
- [ ] Create `EMPIRE_INDEX.md`, `TRADING_INDEX.md`, `BLCO_INDEX.md`, `INFRASTRUCTURE_INDEX.md`, `KNOWLEDGE_INDEX.md`
- [ ] Add frontmatter to 10 core governance files

### Phase 2 — Intelligence Layer (1 day)
- [ ] Create daily note template in `templates/`
- [ ] Deploy 3 Dataview queries
- [ ] Set up COMMAND_CANVAS.canvas
- [ ] Install obsidian-tasks and obsidian-git plugins

### Phase 3 — Automation Wiring (ongoing)
- [ ] Morning Brief agent writes to daily note template
- [ ] trading_sentinel writes weekly trade report
- [ ] STATUS.md gains YAML frontmatter
- [ ] Mission Control gains Obsidian deep links

### Phase 4 — Knowledge Enrichment (ongoing)
- [ ] Add frontmatter to all project files
- [ ] Archive Documents vault (snapshot + mark read-only)
- [ ] Create REFERENCE_LIBRARY.md for OC 1 PDFs
- [ ] Weekly review template with agent retrospective

---

## 8. Security Note

The workspace vault contains sensitive operational data. Obsidian's `sync` plugin is disabled (confirmed). Ensure:
- `trades.jsonl`, `leads.jsonl`, `*.env` files are in `.obsidianignore`
- `obsidian-git` plugin is configured to use the existing workspace git remote (not a new cloud sync)
- Vault is NOT shared via Obsidian Publish or any cloud sync service

---

*Report V1 — Agent C — C0 Sprint — 2026-08-09*
