# PHASE 2 — COMPONENT LEDGER
**Date:** 2026-07-30  
**Authority:** Nathan Asiegbu — PR14-264d22c  
**Status:** INITIAL DRAFT — evidence-based, non-mutating collection

## Evidence State Key
- `GITHUB_VERIFIED` — committed code on UA4200 with exact SHA
- `LOCAL_VERIFIED` — confirmed on disk, untracked
- `RUNTIME_VERIFIED` — confirmed running in PM2/launchd/cron
- `DOCUMENTED_ONLY` — referenced in docs but not confirmed on disk
- `MISSING` — expected but not found
- `CASHCLAW_CONFLICT` — overlaps with CashClaw operational zone
- `SUPERSEDED` — older variant replaced by a newer one

---

## COMPONENT LEDGER

### C-01: Open Empire ROS (Repository Operating System)
| Field | Value |
|---|---|
| Evidence | `GITHUB_VERIFIED` |
| Repo | UA4200/open-empire-ros |
| Branch | main |
| SHA | e785769c2b5a19371831cb433562d5fe6c01e808 |
| Local path | ~/.openclaw/empire/ros/ (knowledge_graph, mission_control, pmo, registry) |
| Purpose | Repo intelligence — discovery, fingerprinting, manifest, PMO scoring, knowledge-graph |
| Version | 0.1.0 |
| CLI | empire-ros |
| Tests | GitHub Actions workflow present |
| Deployment | Not deployed as a running service yet |
| Port | None |
| Database | None |
| Secrets | None required |
| Deployment status | GITHUB_VERIFIED, not running locally |
| Remaining blocker | v0.2–v0.5 roadmap not implemented |

---

### C-02: git-github Control Plane
| Field | Value |
|---|---|
| Evidence | `GITHUB_VERIFIED` |
| Repo | UA4200/git-github |
| Branch | main + 3 agent branches |
| SHA (main) | 75d2d2386d4a |
| SHA (active) | 264d22c18d059f33384ec5c7425cddcd5ca91f30 (PR #14 head) |
| Purpose | GitHub-controlled deployment governance and directive repository |
| Open PRs | #14 (this deployment), #3 (ADAI website) |
| Closed PRs | #1 (control plane), #2 (OpenClaw runtime) |
| Files | directives/OPEN_EMPIRE_FULL_RECONSTRUCTION_AND_DEPLOYMENT.md |
| Deployment status | ACTIVE — this is the control plane |

---

### C-03: OpenClaw Agent Command Center
| Field | Value |
|---|---|
| Evidence | `GITHUB_VERIFIED` |
| Repo | UA4200/OpenClaw-Agent-Command-Center |
| Branch | main |
| SHA | a454808c0d79 |
| Purpose | Single-pane-of-glass dashboard for managing OpenClaw AI |
| Local path | Not confirmed locally |
| Deployment status | On GitHub; not confirmed deployed locally |
| Remaining blocker | No local deployment confirmed |

---

### C-04: hermes-agent
| Field | Value |
|---|---|
| Evidence | `GITHUB_VERIFIED` |
| Repo | UA4200/hermes-agent |
| Branch | main + claude/summarize-weekly-calendar-b6rlm |
| SHA (main) | d472d697cd08 |
| Purpose | Self-improving AI agent with learning loop, skill creation, Telegram interface |
| Open PRs | #1 — ADAI Empire automation playbook + 51-Dynamics series |
| Deployment status | On GitHub; local deployment not confirmed |

---

### C-05: Alusi Control Stack (bin/ scripts)
| Field | Value |
|---|---|
| Evidence | `LOCAL_VERIFIED` + `RUNTIME_VERIFIED` |
| Local path | ~/.openclaw/bin/ |
| Purpose | Core Alusi decision, execution, dispatch, autonomy, approval, policy, memory loops |
| Key files | alusi-loop.py, alusi-executor.py, alusi-decide.py, alusi-dispatch.py, alusi-control.py, alusi-autonomy.py, alusi-alert.py, alusi-learn.py, alusi-improve.py, alusi-policy.py, alusi-approval-watch.py |
| Supporting | gen_status.py, compress_memory.sh, night_ops.sh, morning_brief.sh, secrets_health.sh |
| Runtime | alusi-gateway (PM2 id=1), alusi-controlled-worker (id=4), alusi-orchestrator (id=5) |
| Repo | None — untracked |
| Target repo | UA4200/git-github or new UA4200/alusi-core |
| Deployment status | RUNNING — no git provenance |
| Remaining blocker | Must be committed before Phase 3 |

---

### C-06: CashClaw Director
| Field | Value |
|---|---|
| Evidence | `LOCAL_VERIFIED` + `RUNTIME_VERIFIED` |
| **STATUS** | **⛔ CASHCLAW_CONFLICT — DO NOT MODIFY** |
| Local path | ~/.openclaw/moltlaunch/agents/cashclaw_director/ |
| Purpose | Live Kalshi prediction market trading — V2 API, RSA-PSS, Kelly criterion |
| Key files | run.py, executor.py, market_scanner.py, signal_engine.py, cashclaw_engine.py |
| State files | state.json, trades.jsonl (live production data) |
| PM2 | cashclaw_director (id=7), PID 75769, ONLINE |
| Capital | $25.19 Kalshi, max $1.25/trade |
| Repo | None — untracked |
| **Action** | **ZERO CHANGES — commit to read-only snapshot branch only** |
| Remaining blocker | CashClaw continuity — no deployment permitted |

---

### C-07: OpenClaw Workspace Governance Files
| Field | Value |
|---|---|
| Evidence | `LOCAL_VERIFIED` |
| Local path | ~/.openclaw/workspace/*.md |
| Purpose | Runtime identity, memory, task, heartbeat, governance for the Alusi agent |
| Key files | AGENTS.md, MEMORY.md, HEARTBEAT.md, SOUL.md, STATUS.md, PROJECTS.md, CONSTITUTION.md, TASK.md, GOALS.md |
| Repo | None — untracked |
| Target repo | UA4200/git-github or UA4200/alusi-core |
| Deployment status | ACTIVE governance layer — no git provenance |
| Note | These are operational SSOT files. Committing adds history; not deployment |

---

### C-08: Open Empire Directory (~/.openclaw/empire/)
| Field | Value |
|---|---|
| Evidence | `LOCAL_VERIFIED` |
| Local path | ~/.openclaw/empire/ |
| Purpose | Full Empire capability structure — 280 subdirectories covering governance, trading, client systems, routing, observability, memory, and every documented component |
| Size | 280 dirs, last modified 2026-07-18 |
| Audit trail | 29 audit JSON files in empire/audits/ including Mega Block 1, Ultra Blocks A–J |
| All ultra blocks | production_modified=false, rollback_available=true |
| Mega Block 1 | Validated 2026-05-16 |
| Ultra Block A–J | Validated 2026-05-19 |
| Repo | None — untracked |
| Target repo | UA4200/open-empire-core (new) |
| Deployment status | LOCAL_VERIFIED — structured but not GitHub-governed |
| Remaining blocker | 280 dirs to inventory, commit, and provision |

---

### C-09: Mission Control (UI)
| Field | Value |
|---|---|
| Evidence | `LOCAL_VERIFIED` + `RUNTIME_VERIFIED` |
| Local path | ~/.openclaw/workspace/mission-control/ |
| Purpose | Command center UI — Next.js app serving system status, PM2, trades, alerts |
| Port | 3333 (127.0.0.1) |
| PM2 | mission-control (id=18), 5D uptime |
| Stack | Next.js, postcss |
| Repo | None — untracked |
| Target repo | UA4200/OpenClaw-Agent-Command-Center or new |
| Deployment status | RUNNING — no git provenance |

---

### C-10: Antfarm Workflow Engine
| Field | Value |
|---|---|
| Evidence | `LOCAL_VERIFIED` |
| Local path | ~/.openclaw/workspace/antfarm/ |
| Purpose | Multi-agent workflow orchestration — TypeScript CLI, compiled dist/, SQLite polling |
| Structure | src/ (TypeScript), dist/ (compiled), cli/, server/, installer/, lib/, medic/ |
| PM2 | Not running as dedicated process |
| Repo | None — untracked |
| Target repo | UA4200/antfarm or UA4200/git-github sub-package |
| Deployment status | LOCAL_VERIFIED, compiled, not GitHub-governed |

---

### C-11: BLCO Pipeline
| Field | Value |
|---|---|
| Evidence | `LOCAL_VERIFIED` + `RUNTIME_VERIFIED` |
| Local path | ~/.openclaw/blco/ |
| Purpose | BLCO commodity buyer qualification and outreach — 630 leads in pipeline |
| Key files | blco_daily_sourcer.py, blco_email_monitor.py, blco_weekly_worldwide.py, leads.jsonl (630 leads), enriched_leads.jsonl |
| PM2 | blco-enricher (id=15), blco-email-monitor (id=16) ONLINE; blco-daily-sourcer (id=17) STOPPED (paused 2026-07-19) |
| Status | PAUSED — no sourcing, monitor active |
| Repo | None — untracked |
| Target repo | UA4200/blco-pipeline (new) |
| Deployment status | PARTIAL RUNNING — no git provenance |

---

### C-12: n8n Workflow Layer
| Field | Value |
|---|---|
| Evidence | `RUNTIME_VERIFIED` |
| Port | 5678 (all interfaces — ⚠️ not localhost-bound) |
| PM2 | n8n (id=29), 5h uptime |
| Health | {"status":"ok"} |
| Known workflows | CASHCLAW_TEST_001 |
| Export path | ~/.openclaw/workspace/jobs/ |
| Purpose | Delivery layer for all approved outputs |
| Repo | None — workflow export not committed |
| Target | Export all workflows to UA4200/git-github/n8n/ |
| Note | n8n is bound to * (all interfaces) — should be reviewed for security |

---

### C-13: Alusi Adapters (Telegram + Discord)
| Field | Value |
|---|---|
| Evidence | `RUNTIME_VERIFIED` |
| PM2 | alusi-telegram-adapter (id=2), alusi-discord-adapter (id=3) — 5D uptime |
| Local path | ~/.openclaw/workspace/ (alusi_telegram_operator.py, alusi_discord_operator.py, etc.) |
| Purpose | Channel ingestion — Telegram and Discord to Alusi |
| Repo | None — untracked |
| Target repo | UA4200/alusi-core |

---

### C-14: Hyrve Monitor
| Field | Value |
|---|---|
| Evidence | `LOCAL_VERIFIED` + `RUNTIME_VERIFIED` |
| Local path | ~/.openclaw/workspace/ (multiple variants: hyrve_monitor.py, hyrve-monitor.js, hyrve_monitor_v2.js, etc.) |
| PM2 | hyrve-monitor-v2 (id=22), 5D uptime, 46.9 MB |
| LaunchD | com.cashclaw.hyrve-monitor.plist, com.cashclaw.hyrveai_market_monitor.plist |
| Purpose | Monitors HyrveAI marketplace pipeline |
| Note | Multiple overlapping implementations — consolidation needed |
| Repo | None — untracked |
| Remaining blocker | De-duplicate implementations before committing |

---

### C-15: Trading Sentinel
| Field | Value |
|---|---|
| Evidence | `RUNTIME_VERIFIED` |
| PM2 | trading_sentinel (id=14), 5D uptime |
| Local path | ~/.openclaw/bin/ |
| Purpose | CashClaw watchdog + circuit breaker |
| Status | RUNNING (referenced as "stub" in AGENTS.md) |
| **CashClaw adjacency** | Monitors CashClaw — read-only. No deployment action. |
| Repo | None — untracked |

---

### C-16: Sovereign Proxy
| Field | Value |
|---|---|
| Evidence | `RUNTIME_VERIFIED` |
| Local path | ~/.openclaw/moltlaunch/sovereign_proxy/ (empty dir confirmed) |
| Purpose | Approval gating for all council items |
| Approvals | ~/.openclaw/vault/approvals/approvals.jsonl |
| n8n | Routes approved outputs |
| PM2 | Not in PM2 list (separate process or stub) |
| Repo | None |
| Remaining blocker | Confirm actual process and script |

---

### C-17: Polymarket Trader
| Field | Value |
|---|---|
| Evidence | `RUNTIME_VERIFIED` |
| PM2 | polymarket-trader (id=35), 12m uptime at capture |
| Purpose | Polymarket prediction market trading |
| Status | RUNNING — secrets PENDING (private key + wallet not yet provided) |
| **CashClaw adjacency** | Separate trader — different exchange. Watch for credential overlap. |
| Repo | None — untracked |

---

### C-18: Executor + Heartbeat Core
| Field | Value |
|---|---|
| Evidence | `RUNTIME_VERIFIED` |
| PM2 | executor (id=0), heartbeat (id=19) — 5D uptime each |
| Purpose | Core task executor and alusi-loop heartbeat |
| Local path | ~/.openclaw/workspace/ (executor scripts) |
| Repo | None — untracked |

---

### C-19: Nexus Stack
| Field | Value |
|---|---|
| Evidence | `RUNTIME_VERIFIED` |
| PM2 | nexus-telemetry (id=20), nexus-dashboard (id=23) — 5D uptime |
| Also | open-empire-nexus (id=21), open-empire-control-plane (id=25), open-empire-mission-ui (id=26) |
| Port | nexus on 18789 |
| Purpose | Intelligence, telemetry, knowledge graph UI |
| Repo | None — untracked |

---

### C-20: OpenClaw Security Tools
| Field | Value |
|---|---|
| Evidence | `LOCAL_VERIFIED` |
| Local path | ~/.openclaw/workspace/security_tools/ , ~/.openclaw/bin/clawsec, security-guard.js |
| Purpose | Security guard v2, injection filter, skill auditor, secrets health |
| Score | 100/100 (from MEMORY.md) |
| Repo | None — untracked |

---

### C-21: Open Empire Mega Block Script
| Field | Value |
|---|---|
| Evidence | `LOCAL_VERIFIED` |
| Path | ~/open_empire_mega_block_1.sh |
| SHA-256 | 2ec94390a8a72ce9c92d762b6b7228aef56c72cf898baf6a3f6251b167ceb9b1 |
| mtime | 2026-05-16T12:03:45 |
| Purpose | Original bootstrap script for empire directory creation |
| Target | Commit to UA4200/git-github/scripts/bootstrap/ |
| Deployment status | LOCAL_VERIFIED — not committed |

---

### C-22: Ultra Blocks A–J (Empire Validation Set)
| Field | Value |
|---|---|
| Evidence | `LOCAL_VERIFIED` |
| Path | ~/.openclaw/empire/audits/ultra_block_*.json |
| Count | 10 ultra blocks (A through J) |
| All | production_modified=false, rollback_available=true |
| Purpose | Staged empire capability validation records |
| Target | Commit to UA4200/git-github/audits/ |
| Deployment status | LOCAL_VERIFIED — not committed |

---

### C-23: Postgres / ClawDB
| Field | Value |
|---|---|
| Evidence | `DOCUMENTED_ONLY` |
| Status | ❌ DOWN — port 5432 not responding |
| LaunchD | homebrew.mxcl.postgresql@18.plist (present) |
| Purpose | Persistent database for empire state, trades, leads |
| Remaining blocker | **BLOCKER** — must start and verify schema before Phase 5 |

---

### C-24: Alpaca Trader
| Field | Value |
|---|---|
| Evidence | `RUNTIME_VERIFIED` |
| PM2 | alpaca-demo (id=34), 111m uptime |
| Local path | ~/.openclaw/bin/alpaca_trader.py, alpaca_strategy.py |
| Purpose | Alpaca stock/ETF trading demo |
| Status | RUNNING as demo |
| Repo | None |

---

### C-25: Email Dispatcher / Outreach
| Field | Value |
|---|---|
| Evidence | `RUNTIME_VERIFIED` |
| PM2 | ecosystem.email-dispatcher (id=12), 5D uptime |
| Purpose | Draft-first email delivery via n8n → approval queue |
| Repo | None |

---

## SUMMARY TABLE

| ID | Component | Evidence | GitHub | Running | Blocker |
|---|---|---|---|---|---|
| C-01 | Open Empire ROS | GITHUB_VERIFIED | ✅ | ❌ | Deploy locally |
| C-02 | git-github Control Plane | GITHUB_VERIFIED | ✅ | — | — |
| C-03 | OpenClaw Agent Command Center | GITHUB_VERIFIED | ✅ | ✅(3333) | Verify |
| C-04 | hermes-agent | GITHUB_VERIFIED | ✅ | ❌ | Deploy locally |
| C-05 | Alusi Control Stack | LOCAL+RUNTIME | ❌ | ✅ | Commit to GitHub |
| C-06 | CashClaw Director | LOCAL+RUNTIME | ❌ | ✅⛔ | CASHCLAW_CONFLICT |
| C-07 | Workspace Governance | LOCAL | ❌ | ✅ | Commit to GitHub |
| C-08 | Empire Directory (280 dirs) | LOCAL | ❌ | — | Inventory + commit |
| C-09 | Mission Control UI | LOCAL+RUNTIME | ❌ | ✅(3333) | Commit to GitHub |
| C-10 | Antfarm Engine | LOCAL | ❌ | ❌ | Commit to GitHub |
| C-11 | BLCO Pipeline | LOCAL+RUNTIME | ❌ | ⚠️ | Commit; lead sourcing paused |
| C-12 | n8n Workflows | RUNTIME | ❌ | ✅(5678) | Export + commit |
| C-13 | Alusi Adapters | RUNTIME | ❌ | ✅ | Commit to GitHub |
| C-14 | Hyrve Monitor | LOCAL+RUNTIME | ❌ | ✅ | De-dup then commit |
| C-15 | Trading Sentinel | RUNTIME | ❌ | ✅ | CASHCLAW_CONFLICT (read-only ok) |
| C-16 | Sovereign Proxy | RUNTIME | ❌ | ⚠️ | Confirm process |
| C-17 | Polymarket Trader | RUNTIME | ❌ | ✅ | Secrets pending |
| C-18 | Executor + Heartbeat | RUNTIME | ❌ | ✅ | Commit to GitHub |
| C-19 | Nexus Stack | RUNTIME | ❌ | ✅ | Commit to GitHub |
| C-20 | Security Tools | LOCAL | ❌ | — | Commit to GitHub |
| C-21 | Mega Block Script | LOCAL | ❌ | — | Commit to GitHub |
| C-22 | Ultra Blocks A–J | LOCAL | ❌ | — | Commit to GitHub |
| C-23 | Postgres/ClawDB | DOCUMENTED_ONLY | ❌ | ❌ | **BLOCKER** — start + verify |
| C-24 | Alpaca Trader | RUNTIME | ❌ | ✅ | Commit to GitHub |
| C-25 | Email Dispatcher | RUNTIME | ❌ | ✅ | Commit to GitHub |

---

## GITHUB GAPS (Components with no UA4200 repo)

Every component except C-01 through C-04 needs a canonical GitHub home.

**Proposed canonical repos:**

| Repo (new) | Components |
|---|---|
| UA4200/alusi-core | C-05, C-07, C-13, C-18 |
| UA4200/open-empire-core | C-08, C-21, C-22 |
| UA4200/cashclaw-ops | C-06 (**read-only snapshot only**) |
| UA4200/mission-control-ui | C-09 (or merge into OpenClaw-Agent-Command-Center) |
| UA4200/antfarm | C-10 |
| UA4200/blco-pipeline | C-11 |
| UA4200/hyrve-monitor | C-14 (consolidated) |
| UA4200/nexus | C-19 |
| UA4200/empire-security | C-20 |

---

## CASHCLAW CONFLICTS

| Component | Conflict | Resolution |
|---|---|---|
| C-06 cashclaw_director | Live production system | Read-only snapshot branch only. No deploy action. |
| C-15 trading_sentinel | Monitors CashClaw process | Read-only commit acceptable. No PM2 changes. |
| C-17 polymarket-trader | Same executable zone | Independent — different exchange. Commit scripts but no credential changes. |

---

## BLOCKERS

| # | Blocker | Component | Severity |
|---|---|---|---|
| B1 | Postgres/ClawDB DOWN | C-23 | HIGH — required for Phase 5 full deployment |
| B2 | All first-party code untracked | C-05 to C-25 | HIGH — core Phase 3 work |
| B3 | n8n bound to all interfaces | C-12 | MEDIUM — security review needed |
| B4 | Hyrve monitor duplicates | C-14 | MEDIUM — 10+ variant files |
| B5 | Sovereign proxy — process unclear | C-16 | MEDIUM — confirm before commit |
| B6 | CashClaw commit — read-only scope | C-06 | LOCKED — awaiting separate auth |

---
*Generated by: Alusi — Phase 2 component ledger, evidence-based*

---

## PHASE 3 UPDATE — 2026-07-30

### Repos Created and Committed

| WP | Repo | SHA | PR | Status |
|---|---|---|---|---|
| WP-001 | UA4200/alusi-core | f35f22e439b6 | #1 (draft) | Governance + alusi bin/ |
| WP-002 | UA4200/open-empire-core | da8a379d30e9 | #1 (draft) | Mega Block 1 + ultra blocks A-J |
| WP-003 | UA4200/git-github | 14d4f088735a | #15 (draft) | Phase 0-2 reports + deployment index |
| WP-004 | UA4200/mission-control | 186893e | main | Next.js UI, port 3333 |
| WP-005 | UA4200/antfarm | a442ad7 (prior) | main | Workflow engine (had 3 local commits) |
| WP-006 | UA4200/blco-pipeline | 3b9a61e | main | BLCO scripts (leads.jsonl excluded) |

### CashClaw Continuity Log
| Check | Time (CDT) | Status | Restarts | Unstable |
|---|---|---|---|---|
| #1 | ~09:16 | ONLINE | 115 | 0 |
| #2 | ~09:37 | ONLINE | 116 | 0 |
| #3 | ~09:45 | ONLINE | 116 | 0 |

### Remaining GitHub Gaps (Phase 3 continued)
- C-08 Empire Directory (280 dirs) — too large for single commit; inventory pass needed
- C-16 Sovereign Proxy — process unclear, needs investigation
- C-19 Nexus Stack — scripts not yet committed

### Blockers Updated
- B1 Postgres: PERSISTENT — brew services SIGKILL'd, launchctl I/O error; data directory may need reinit
- B3 n8n external bind: still on * — security review deferred to Phase 4
