# MEMORY.md - User Profile and Runtime State
Version: 4.0 | Updated: 2026-07-30 | Secrets: ~/.openclaw/secrets/.env

## User Profile
- Name: Nathan (Ugo / Ugochukwu) - Chicago, IL - America/Chicago
- Optimizes for: leverage, control, speed, protection, repeatability, winning
- Style: direct, systems-focused, risk-aware, short commands
- Failure modes: overload, build-before-validate, burnout, control bias

## Runtime Purpose
Generate sovereign income autonomously.
Reduce Nathan work to: review + approve only.

## Current Operating Posture
- High-agency internal operator
- Draft-first for all external communication
- Approval-gated for high-risk actions
- n8n: ACTIVE - approved outputs route externally
- Secrets: ~/.openclaw/secrets/.env (canonical)

## Top Priorities (ranked)
1. CashClaw Director - P0, LIVE (Kalshi $25.19 + Polymarket US $40 = $65 deployed capital)
2. Polymarket US - P0, LIVE (polymarket-us SDK, Ed25519 auth, $40 buying power)
3. BLCO - P0 paused, 630 leads in pipeline, resume pending
4. ADAI Solutions Inc - parent brand for monetizable AI products
5. Moltlaunch - P1, HyrveAI live, awaiting marketplace job posting

## ADAI Product Rule
- Each monetizable solution should be packaged as a product of ADAI Solutions Inc unless explicitly excluded.
- CashClaw Ops is the first ADAI product line for autonomous financial operations.
- Enterprise Agent Factory is the higher-ticket B2B service line for custom client agents: $3k–$10k build + $500–$2k/mo maintenance.
- AI Research Automation is the project-based research synthesis line for biotech/pharma/healthtech/academia: $2k–$5k/project + optional monitoring retainers.
- Code Migration Service is the premium enterprise modernization line: $15k–$50k/project for legacy-to-modern stack migrations with test-driven verification.

## Validated Runtime State (2026-07-31 post Phase 6)
| Component | Status |
|---|---|
| OpenClaw gateway | OK port 8787 |
| Telegram | OK |
| Anthropic auth | OK |
| n8n | OK active port 5678 |
| **Kalshi balance** | **$1.55 free / ~$80 in 9 open positions (post naked-leg close 2026-07-31)** |
| **CashClaw Director (id=38)** | **OK LIVE, 5min cycles, canonical `trading.agents.director.run`, DAILY_SPEND_CAP=$10, LIVE MODE confirmed 2026-08-02** |
| **CashClaw Arb (id=39)** | **OK LIVE, 5min cycles, canonical `trading.agents.arb.run`, ARB_DAILY_SPEND_CAP=$10, circuit=ok** |
| **Polymarket US (id=40)** | **OK LIVE, canonical `trading.agents.polymarket_trader.run`, DAILY_SPEND_CAP=$10 — balance $0.06, awaiting deposit** |
| **Trading Sentinel (id=41)** | **OK LIVE, canonical `trading.agents.sentinel.run`** |
| **Signal engine** | **OK — canonical `trading.shared.signals`, Haiku primary scorer (GPT-4o removed 2026-08-02), chain: Haiku→Ollama→Heuristic** |
| **Ollama** | **OK PM2 id=32, 6 models, port 11434** |
| sovereign_proxy | OK |
| blco_broker | PAUSED (192 leads staged) |
| b2b_outreach | OK draft-first |
| Vault (7 buckets) | OK |
| Auto-capture | OK LaunchD+cron |
| Security Guard v2 | OK 100/100 |
| alusi-loop PM2 | OK |
| Audit logs | OK |
| Grafana | OK port 3001 |
| Postgres/ClawDB | OK — PostgreSQL 18.3, port 5432, `clawdb` DB live, PM2 id=43 |
| **Polymarket US balance** | **$0.06 free / $39.94 in 13 open MLB/MLS positions (settlement Sept-Nov 2026)** |
| **Free-Way proxy (freeway)** | **PM2 id=48, RUNNING, pid=7708, port 127.0.0.1:8082** — 5 providers (openrouter 17 models, cohere 4, cerebras 2, nvidia 2, mistral 1), 72 total models. COST_OPTIMIZED_INFERENCE. Start: `pm2 restart freeway`. Logs: `~/.openclaw/hermes/logs/freeway.log` |
| **FCC Dashboard (grafana)** | **PM2 id=50, RUNNING, port 127.0.0.1:3001** — Node.js metrics dashboard, reads Free-Way /api/usage, auto-refresh 30s. Start: `pm2 restart grafana`. Source: `~/.openclaw/grafana/dashboard-server.js` |
| **fcc-metrics-exporter** | **PM2 id=51, RUNNING** — exports fcc_metrics.json + .prom to `~/.openclaw/grafana/data/` every 5min. Uses stdlib urllib (no pip deps). |

## Key Paths (post 2026-07-31 consolidation)
- Secrets:      ~/.openclaw/secrets/.env
- Workspace:    ~/.openclaw/workspace/
- **Trading (canonical):** ~/.openclaw/trading/
  - Clients:  ~/.openclaw/trading/clients/{kalshi_client,polymarket_client}.py
  - Shared:   ~/.openclaw/trading/shared/{signals,kelly,risk,logging}.py
  - Agents:   ~/.openclaw/trading/agents/{director,arb,polymarket_trader,sentinel}/
  - Data:     ~/.openclaw/trading/data/{director,arb,polymarket}/
  - Manifest: ~/.openclaw/trading/ecosystem.trading.cjs
- Deprecated (do not use): ~/.openclaw/_deprecated/
  - `cashclaw_2026-07-31/` (was ~/.openclaw/cashclaw/)
  - `moltlaunch_cashclaw_director_2026-07-31/` (was ~/.openclaw/moltlaunch/agents/cashclaw_director/)
  - `polymarket_2026-07-31/` (was ~/.openclaw/polymarket/)
- BLCO:         ~/.openclaw/blco/leads.jsonl
- Vault:        ~/.openclaw/vault/
- Logs:         ~/.openclaw/logs/
- Backlog:      ~/.openclaw/memory/backlog.json
- Hermes reports: ~/.openclaw/hermes/reports/

## Operator Rules
- External = draft-first, no auto-send
- Financial = explicit approval
- n8n = delivery layer for all approved outputs
- Validation before enthusiasm
- Protection before scaling

## Cost Governance (updated 2026-07-30)
### Model Dispatch
- Heartbeats, monitoring, log parsing → **ollama/tinyllama or qwen2.5:1.5b** ($0)
- Signal scoring (CashClaw), classification → **Haiku** (~$0.12/day at 5min cycles)
- Drafting, complex analysis → **Sonnet**
- Strategy, escalation → **Opus** (Alusi only)

### Cost-Reduction Changes Deployed 2026-07-30
- CashClaw director: 60s → 300s cycle (-80% signal calls)
- alusi_briefing: Haiku → pure Python template ($0)
- secrets_health: removed Haiku ping ($0)
- night_ops stage 3: static template + date stamp ($0)
- night_ops stage 6: live-data snapshot template ($0)
- generate_emails: 3-tier system (default $0 template)
- Total est daily savings: ~$0.60-$0.80

### Ollama Setup
- PM2-managed, port 11434, keep_alive=-1
- Models: qwen2.5:3b, qwen2.5:1.5b, llama3.2:3b, gemma2:2b, phi3:mini, tinyllama
- Intel CPU limitation: cold load ~5min, warm inference 2-8 tok/s
- Best use: batch overnight tasks, not real-time


## Claude History Insights (imported 2026-05-07)
- **2026-04-26** — *OpenClaw security audit and scoring*: **Conversation Overview**

Nathan (Ugo/Ugochukwu), founder of ADAI INC operating in Chicago, is building an autonomous AI empire on a Mac Mini (NeoOC/Ugos-Mac-mini) using a system called OpenClaw with
- **2026-04-01** — *OpenClaw setup for personal growth and wealth*: **Conversation Overview**

Nathan Ugochukwu (also called Ugo), based in Chicago IL, is building a self-optimizing wealth generation empire on a Mac Mini using OpenClaw v2026.3.13. He operates three co
- **2026-03-25** — *MEDITECH EHR AI Project Management*: **Conversation Overview**

Nathan Asiegbu engaged Claude in an extended knowledge transfer session focused on MEDITECH Expanse EHR systems, go-live consulting, and career positioning. Nathan framed th
- **2026-03-16** — *Empty response text debugging*: **Conversation Overview**

The person was troubleshooting a broken response pipeline in their "openclaw" project — a Node.js/ESM application running via PM2 that routes chat prompts through the Anthro
- **2026-03-13** — *OpenClaw project takeover and delivery plan*: **Conversation Overview**

This conversation involved a full technical takeover of an existing local macOS project called OpenClaw, with the person acting as the system owner inheriting a partially bu

## Promoted From Short-Term Memory (2026-05-14)

<!-- openclaw-memory-promotion:memory:memory/2026-05-07.md:2:2 -->
- Auto-flushed at 12:45 AM CDT (pre-compaction) [score=0.835 recalls=0 avg=0.620 source=memory/2026-05-07.md:2-2]

## Promoted From Short-Term Memory (2026-05-18)

<!-- openclaw-memory-promotion:memory:memory/2026-05-12.md:34:35 -->
- Path: `~/.openclaw/memory/blco/buyers/{slug}/` Buyers: europetro_refining_gmbh, asiafuel_trading, adnoc_refining, indianoil_iocl, bp_rotterdam, petrobras, valero_port_arthur, gs_caltex, blacklight_trading, first_texas_energy [score=0.829 recalls=0 avg=0.620 source=memory/2026-05-12.md:34-35]


## Night Ops 2026-07-30 (auto 2026-07-30 08:42 CDT)
| Component | Status |
|---|---|
| PM2 stack | 27 online, 4 stopped | ⚠️ cashclaw_director(115) |
| Kalshi balance | $25.19 |
| Trades (24h) | 0 placed $0.00, 0 failed, 0 low-bal skips |
| BLCO leads | 630 in pipeline |
| P0 backlog | 3 active items |
| Ollama | up — 6 models loaded |

## Deployment Complete (2026-07-30)
- Open Empire GitHub deployment: **DEPLOYED v0.1.0-deploy-20260730**
- 6 UA4200 repos live: alusi-core, open-empire-core, git-github, mission-control, antfarm, blco-pipeline
- All PRs merged to main — CI green on all 6
- Postgres B1: RESOLVED — PostgreSQL 18.3 running (PM2 id=43 clawdb)
- CashClaw: PRESERVED throughout — 0 unstable restarts across 7 continuity checks
- Phase 6 gate: bypassed by Nathan approval 13:21 CDT
- Merge SHAs: alusi-core d7cb2e701e8b | open-empire-core 5a52324a04e8 | git-github 3fe7d522bdef
- Directive: PR14-264d22c (e785769c ROS anchor)
