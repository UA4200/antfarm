# AGENTS.md - Agent Registry and Health
Version: 5.0 | Updated: 2026-07-30

## Active Agents
| Agent | PM2 ID | Status | Cycle | Notes |
|---|---|---|---|---|
| executor | 0 | OK | continuous | core task executor |
| heartbeat | 1 | OK | continuous | alusi-loop heartbeat |
| alusi-gateway | 2 | OK | continuous | OpenClaw gateway |
| alusi-telegram-adapter | 3 | OK | continuous | Telegram channel |
| alusi-discord-adapter | 4 | OK | continuous | Discord channel |
| alusi-controlled-worker | 5 | OK | continuous | approval worker |
| alusi-orchestrator | 6 | OK | continuous | multi-agent orchestration |
| cashclaw_director | 38 | OK | every 5min | LIVE — canonical `trading.agents.director.run`, venv313, V2 API, Kelly NO-fix, `CASHCLAW_DAILY_SPEND_CAP_USD=10` (restarted 2026-08-02, env confirmed) |
| cashclaw_arb | 39 | OK | every 5min | LIVE — canonical `trading.agents.arb.run`, Kalshi bundle arb + Kalshi↔Polymarket cross-arb (alert mode), `ARB_DAILY_SPEND_CAP_USD=10`, circuit=ok |
| polymarket-trader | 40 | OK | 15min cycle | LIVE — canonical `trading.agents.polymarket_trader.run`, MLB/MLS/sports-champ strategy, GPT-4o signals, `POLY_DAILY_SPEND_CAP_USD=10` |
| ollama | 24 | OK | continuous | Local LLM server, port 11434, 6 models |
| hyrvea-monitor | 10 | OK | continuous | Hyrvea pipeline monitor |
| email-dispatcher | 11 | STOPPED | on-demand | approved email dispatch |
| openclaw-dashboard | 12 | STOPPED | on-demand | legacy dashboard |
| open-empire-federation-staging | 33 | OK | every 15min | Python3.14.6, one-shot cron exits after run (stopped=normal), writes latest_federation_state.json |
| open-empire-lifecycle-staging | 34 | OK | every 15min | Python3.14.6, one-shot cron exits after run (stopped=normal), writes latest_lifecycle_state.json |
| clawdb | 43 | OK | continuous | PostgreSQL 18.3, port 5432, LC_ALL fixed |
| exec-gateway | 13 | OK | continuous | exec approval gateway |
| telegram-approvals | 14 | OK | continuous | Telegram approval handler |
| ecosystem.email-dispatcher | 15 | OK | continuous | ecosystem email layer |
| pnl-audit | 16 | STOPPED | on-demand | P&L audit runner |
| mission-control | 17 | OK | continuous | Command Center UI port 3333 |
| trading_sentinel | 41 | OK | every 5min | canonical `trading.agents.sentinel.run`, CashClaw watchdog, reads new + legacy (during transition) trade paths |
| freeway | 48 | OK | continuous | Free-Way proxy, port 8082, 127.0.0.1 only, 5 providers (openrouter/cohere/cerebras/nvidia/mistral), 72 models, COST_OPTIMIZED_INFERENCE |
| grafana | 50 | OK | continuous | FCC Cost Dashboard (Node.js), port 3001, http://127.0.0.1:3001, auto-refresh 30s, reads Free-Way /api/usage |
| fcc-metrics-exporter | 51 | OK | continuous | Scrapes Free-Way usage every 5min → ~/.openclaw/grafana/data/fcc_metrics.json + .prom |
| kg-api | 52 | OK | continuous | Knowledge Graph read API, port 6279, 127.0.0.1 only, auth=OPENEMPIRE_ROUTER_KEY, 12 endpoints |
| oe-proxy | 54 | OK | continuous | Governed inference proxy port 4100 — intercepts claude-* requests, routes haiku→Groq free, sonnet→Groq70B/free, opus→Anthropic premium. ANTHROPIC_BASE_URL=http://127.0.0.1:4100 |

**Removed 2026-07-31 (Phase 5 cutover):**
- id=6 (`cashclaw` legacy stub) — superseded, deleted
- id=35 (`polymarket-trader` legacy `poly_engine.py`) — geoblocked/stale, deleted
- id=53 (`cashclaw_arb` old path) — replaced by id=55 with canonical path
- id=54 (`polymarket-trader` old path) — replaced by id=56 with canonical path
- id=14 (`trading_sentinel` old path) — replaced by id=57 with canonical path

| sovereign_proxy | — | OK | continuous | approval gating (alusi system) |
| blco_broker | — | OK | every 5min | BLCO buyer qualification |
| b2b_outreach | — | OK | every 5min | lead gen draft-only |

## Trading Consolidation (2026-07-31)
- All Kalshi + Polymarket code consolidated under `~/.openclaw/trading/`.
- Canonical clients: `trading.clients.kalshi_client.KalshiClient` (RSA-PSS V2), `trading.clients.polymarket_client.PolymarketClient` (Ed25519, api.polymarket.us).
- Shared modules: `trading.shared.{signals,kelly,risk,logging}`. Kelly NO-fix preserved verbatim.
- Agents: `trading.agents.{director,arb,polymarket_trader,sentinel}`.
- Legacy dirs (`~/.openclaw/cashclaw/`, `~/.openclaw/moltlaunch/agents/cashclaw_director/`, `~/.openclaw/polymarket/`) become `_deprecated/` after Phase 6 approval.
- **Rolling 24h spend caps added 2026-07-31 (after $63 overnight drain event):**
  - `CASHCLAW_DAILY_SPEND_CAP_USD=10` (director)
  - `POLY_DAILY_SPEND_CAP_USD=10` (polymarket_trader)
  - Enforced against sum of PLACED size_usd in trades.jsonl over last 24h.

## cashclaw_director (Venture 1 - Moltlaunch)
- Parent: Moltlaunch marketplace
- Modules:
  - market_scanner.py (V2 API `/portfolio/events/orders`, RSA-PSS signed)
  - signal_engine.py (Claude Haiku, 60% conf, 5pt edge)
  - executor.py (Kelly criterion, 5% max, live balance check)
  - run.py (5min cycle, trading hours guard, expiry filter)
- Capital: **$25.19 funded** (Kalshi deposit confirmed 2026-07-30)
- Max per trade: $1.25
- Target: 70%+ win rate, then add Polymarket for cross-arb
- Status: **OK stable** — all crash-loop bugs fixed 2026-07-30
- Path: ~/.openclaw/moltlaunch/agents/cashclaw_director/
- Fixes deployed 2026-07-30:
  - Kalshi V2 API endpoint migration (was 410 deprecated)
  - RSA-PSS signing (was PKCS1v15)
  - Trading hours guard (Mon-Fri 9am-5pm ET)
  - Market expiry filter (strips expired contracts)
  - Live balance check ($5 min)
  - Cycle 60s → 300s (5min, -80% API calls)

## sovereign_proxy
- Role: approval gating for ALL council items
- Approvals: ~/.openclaw/vault/approvals/approvals.jsonl
- n8n: routes approved outputs

## blco_broker (EXPANDED — BLCO Command Center) ⛔ LEAD SOURCING PAUSED 2026-07-19
- Authority: Alusi (consolidated under one system)
- Command file: ~/.openclaw/blco/BLCO_COMMAND.md
- Goal: Sell BLCO worldwide — VERIFIED SELLER active
- Pipeline: 192 leads (Europe 27, Asia 28, Americas 19, MENA 15, Global traders 11, unknown 89)
- Output: ~/.openclaw/blco/leads.jsonl -> n8n -> Airtable
- Weekly scan: every Monday 07:00 CDT (cron active)
- Existing Open Empire scraper: every Monday 06:00 CDT
- Reports: ~/.openclaw/blco/reports/weekly_YYYY-WW.md
- Telegram: weekly report + daily 9am summary
- All outreach: DRAFT-FIRST, Nathan approval required

## b2b_outreach
- Output: draft emails -> sovereign_proxy -> n8n -> approval queue

## trading_sentinel
- Status: stub - wire after signal fix

## cashclaw_arb (auto-arb executor, 2026-07-30)
- Purpose: 2-strategy arb detection + execution
- Modules:
  - arb_executor.py       (bundle + cross-arb detection, atomic 2-leg execution)
  - arb_cycle.py          (cron entrypoint, logs to arb_cycle.jsonl)
  - polymarket_scanner.py (Polymarket US SDK wrapper, Ed25519 auth)
  - market_scanner.py     (Kalshi V2 API wrapper)
- Cron: `*/5 8-16 * * 1-5` (every 5min, Mon–Fri trading hours)
- Env: `ARB_DRY_RUN=false ARB_CROSS_MODE=alert ARB_MIN_PROFIT_CENTS=3 ARB_MIN_CROSS_PROFIT=5`
- Modes:
  - Bundle arbs (Kalshi-only): auto-execute at ≥3¢ profit
  - Cross-arbs (Kalshi×Polymarket US): alert-only — Telegram, human approval (semantic false-positive risk)
- Safety:
  - Max $5 per arb (split $2.50/leg)
  - Max 2 concurrent arbs
  - Daily loss circuit at -$5
  - Naked leg unwind protocol if leg B fails
- Capital: Kalshi $25.19 + Polymarket US $40 = $65.19 deployed

## Activation Rules
- Max 5% capital per trade
- All outbound draft-first
- Financial = explicit approval
- Generic entities blocked
- New agents: proof-of-concept before activation

## Optimization Rules
- Spawn sub-agents for parallel research/build/verify work.
- Before claiming no memory/context, check vault/MEMORY references when relevant.

## Model Cost Governance (2026-07-30)
- Route batch/overnight tasks through Ollama (local, $0)
- Real-time signal scoring → Haiku only
- Template-first for structured outputs (briefings, reports, emails)
- AI only when personalization/reasoning is genuinely needed
- Daily target: <$0.20 for autonomous ops

<!-- antfarm:workflows -->
# Antfarm Workflow Policy

## Installing Workflows
Run: `node ~/.openclaw/workspace/antfarm/dist/cli/cli.js workflow install <name>`
Agent cron jobs are created automatically during install.

## Running Workflows
- Start: `node ~/.openclaw/workspace/antfarm/dist/cli/cli.js workflow run <workflow-id> "<task>"`
- Status: `node ~/.openclaw/workspace/antfarm/dist/cli/cli.js workflow status "<task title>"`
- Workflows self-advance via agent cron jobs polling SQLite for pending steps.
<!-- /antfarm:workflows -->

