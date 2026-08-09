# Obsidian Knowledge Architecture V1
**Date:** 2026-08-09 | **Vault:** `~/.openclaw/workspace/` | **Status:** Mapping existing → target

---

## Architecture Philosophy

The workspace vault is **dual-purpose**: it's both the Open Empire operating surface (code, configs, scripts) AND the knowledge layer (governance, memory, decisions). The architecture must serve both roles without destructive reorganization.

**Principles:**
1. **Additive only** — no destructive moves. Add structure around what exists.
2. **MOC-first** — Map of Content files as navigation anchors, not folders
3. **Workspace = Source of Truth** — Documents vault is archived, not active
4. **Automated** — Agents write; Obsidian surfaces. Not manual documentation.

---

## Current State → Target Structure Mapping

### Layer 0: Entry Points (MOC Layer)

| Target File | Maps To | Status | Action |
|---|---|---|---|
| `HOME.md` | Vault entry point | ❌ Missing | **Create** |
| `EMPIRE_INDEX.md` | Open Empire ventures + status | ❌ Missing | **Create** |
| `INFRASTRUCTURE_INDEX.md` | All agents, services, ports | ❌ Missing | **Create** |
| `TRADING_INDEX.md` | CashClaw + Polymarket + Arb | ❌ Missing | **Create** |
| `BLCO_INDEX.md` | BLCO pipeline + leads | ❌ Missing | **Create** |
| `KNOWLEDGE_INDEX.md` | Research + learning | ❌ Missing | **Create** |

---

### Layer 1: Governance Core

**Exists (keep as-is):**

| File | Category | Notes |
|---|---|---|
| `AGENTS.md` | Governance | ✅ Authoritative agent registry |
| `CONSTITUTION.md` | Governance | ✅ Core charter |
| `COUNCIL.md` | Governance | ✅ Decision authority |
| `MEMORY.md` | Runtime state | ✅ Live — auto-updated |
| `HEARTBEAT.md` | Loop mechanics | ✅ Live — circuit breakers |
| `SOUL.md` | Identity | ✅ Operating bias |
| `IDENTITY.md` | Identity | ✅ Alusi COS definition |
| `GOALS.md` | Planning | ✅ Current goal set |
| `PROJECTS.md` | Planning | ✅ Active project registry |
| `STATUS.md` | Runtime | ✅ Auto-generated |
| `TOOLS.md` | Local setup | ✅ Environment notes |

**Target additions (tags + frontmatter):**
```yaml
---
category: governance
status: active
last_updated: 2026-08-09
tags: [governance, core]
---
```

---

### Layer 2: Ventures / Domains

**Exists (scattered at root):**

| Current File | Domain | Target Grouping |
|---|---|---|
| `CASHCLAW.md` | Trading | → `TRADING_INDEX.md` links |
| `MOLTLAUNCH.md` | Trading platform | → `TRADING_INDEX.md` links |
| `BLCO.md` | BLCO venture | → `BLCO_INDEX.md` links |
| `DEPLOY_LOG.md` | Infrastructure | → `INFRASTRUCTURE_INDEX.md` links |
| `DOCKER_STATUS.md` | Infrastructure | → `INFRASTRUCTURE_INDEX.md` links |

**Subdirectory mapping:**

| Existing Dir | Domain | In Target Structure |
|---|---|---|
| `projects/` | All ventures | Project MOCs — keep, add YAML frontmatter |
| `directives/` | Deployment records | `INFRASTRUCTURE_INDEX.md` → directives |
| `governance/` | Governance artifacts | `EMPIRE_INDEX.md` → governance |
| `moltlaunch/` | CashClaw trading agent | Operational — not primary Obsidian content |
| `blco/` | BLCO pipeline | `BLCO_INDEX.md` links |
| `vault/` | Approvals/secrets | Operational — not in Obsidian graph |

---

### Layer 3: Memory & Daily Notes

**Exists:**

| Existing | Target |
|---|---|
| `memory/` (91 daily notes, 2026-05-04 →) | ✅ Keep — add daily template |
| `memory-index.md` | Enhance → weekly summary links |
| `brain.md` | Keep — personal thinking space |

**Target template for daily notes:**
```markdown
---
date: {{date}}
tags: [daily-note]
week: {{date:GGGG-[W]WW}}
---
# {{date:YYYY-MM-DD}}

## Focus
- 

## Decisions Made
- 

## Active Projects
[[PROJECT_NAME]]

## Notes
```

---

### Layer 4: Research & Intelligence

**Exists:**

| Existing | Target |
|---|---|
| `research/` | → `KNOWLEDGE_INDEX.md` links |
| `research_outputs/` | → `KNOWLEDGE_INDEX.md` links |
| `SKILLS_REPOS_MASTER_INDEX.md` | → `KNOWLEDGE_INDEX.md` links |
| `CONSOLIDATED_REPO_LEARNINGS.md` | → `KNOWLEDGE_INDEX.md` links |
| `OPEN_EMPIRE_MEMORY_ARCHITECTURE_V2.md` | → `EMPIRE_INDEX.md` links |

---

### Layer 5: Operational Artifacts (Low Obsidian Priority)

These exist in the workspace but are primarily operational, not knowledge artifacts. Obsidian can index them but they don't need MOC links:

| Dir/File | Note |
|---|---|
| `skills/` | Agent skills — operational |
| `agents/` | Agent definitions — operational |
| `scripts/` | Utility scripts |
| `cron/` | Cron definitions |
| `logs/` | Runtime logs |
| `tmp/` | Scratch space |
| `antfarm/` | Workflow engine (node_modules inside) |
| `mission-control/` | Next.js app (node_modules inside) |

**Action:** Add `.obsidianignore` to exclude build artifacts:
```
node_modules/
dist/
.git/
*.jsonl
*.env
*.profraw
```

---

## Target MOC Structure (Additive)

### `HOME.md` (Create)
```markdown
# Open Empire — Knowledge Hub
> Vault: ~/.openclaw/workspace/ | Last updated: auto

## Navigation
- [[EMPIRE_INDEX]] — Ventures, revenue, strategy
- [[INFRASTRUCTURE_INDEX]] — Agents, services, infrastructure
- [[TRADING_INDEX]] — CashClaw, Polymarket, Arbitrage
- [[BLCO_INDEX]] — BLCO commodity pipeline
- [[KNOWLEDGE_INDEX]] — Research, repos, learning

## Governance
- [[AGENTS]] · [[CONSTITUTION]] · [[COUNCIL]] · [[GOALS]] · [[MEMORY]]

## Live Status
- [[STATUS]] · [[HEARTBEAT]] · [[DEPLOY_LOG]]

## Daily Practice
- [[memory-index]] · [[brain]]
```

---

### `EMPIRE_INDEX.md` (Create)
Links: GOALS, PROJECTS, DREAMS, governance/, OPEN_EMPIRE_MEMORY_ARCHITECTURE_V2, research_outputs/

### `INFRASTRUCTURE_INDEX.md` (Create)
Links: AGENTS, DEPLOY_LOG, DOCKER_STATUS, DEPLOYMENT_CHECKLIST, RESCUE_GATEWAY_RUNBOOK, CICD_PLAN, directives/

### `TRADING_INDEX.md` (Create)
Links: CASHCLAW, MOLTLAUNCH, projects/cashclaw_ops/, projects/Trading_Bot/, projects/Trading_Sentinel/

### `BLCO_INDEX.md` (Create)
Links: BLCO, projects/BLCO/, projects/BLCO_Broker/, blco/

### `KNOWLEDGE_INDEX.md` (Create)
Links: SKILLS_REPOS_MASTER_INDEX, CONSOLIDATED_REPO_LEARNINGS, research/, research_outputs/, CLAUDE.md, FREE_CLAUDE_CODE_*.md

---

## Dataview Queries to Deploy

### Agent Status Dashboard
```dataview
TABLE status, pm2_id, notes
FROM "."
WHERE category = "agent"
SORT pm2_id ASC
```

### Active Projects
```dataview
TABLE status, last_updated
FROM "projects"
WHERE status = "active"
SORT last_updated DESC
```

### Recent Daily Notes
```dataview
LIST
FROM "memory"
SORT file.name DESC
LIMIT 7
```

---

## Graph Configuration Targets

Add group colors in `.obsidian/graph.json`:
- **Red**: CashClaw / Trading files
- **Blue**: Governance (AGENTS, CONSTITUTION, COUNCIL)
- **Green**: Memory / Daily notes
- **Yellow**: BLCO venture
- **Purple**: Infrastructure / Deployment
- **Orange**: Skills / Repos

---

## Implementation Sequence (Non-destructive)

1. **Step 1** (5 min): Create `.obsidianignore`
2. **Step 2** (10 min): Add YAML frontmatter to 10 key files
3. **Step 3** (15 min): Create `HOME.md` and 5 index MOCs
4. **Step 4** (20 min): Set up daily note template in `templates/`
5. **Step 5** (30 min): Deploy 3 Dataview queries
6. **Step 6** (ongoing): Add frontmatter as files are edited naturally

---

*Architecture V1 — non-destructive mapping — Agent C — C0 Sprint — 2026-08-09*
