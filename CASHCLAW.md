# CASHCLAW.md - Agent Spec
Version: 2.0

## Identity
- Standalone: cashclaw (PM2 direct Kalshi)
- Via Moltlaunch: cashclaw_director
- Status: DEGRADED - p_yes=0.00
- Secrets: ~/.openclaw/secrets/.env

## Capital
- $25 starting, max 5% Kelly (~$1.25/trade)
- Q4 2026: Polymarket

## Modules
1. market_scanner.py - 200 markets/cycle
2. signal_engine.py - Claude Haiku, 70% conf, 5pt edge
3. executor.py - Kelly sizing, RSA-PSS Kalshi orders
4. cashclaw_engine.py - 15-min cycles
5. run.py - PM2, Telegram alerts

## CC-01 Fix
set -a && source ~/.openclaw/secrets/.env && set +a
python3 ~/.openclaw/cashclaw/cashclaw_engine.py

## Paths
- Engine: ~/.openclaw/cashclaw/cashclaw_engine.py
- Trades: ~/.openclaw/cashclaw/trades.jsonl
- Director: ~/.openclaw/moltlaunch/agents/cashclaw_director/
