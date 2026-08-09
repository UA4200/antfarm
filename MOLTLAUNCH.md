# MOLTLAUNCH.md - Venture 1 Spec
Version: 1.0

## Identity
- Name: Moltlaunch - Prediction Market Agent Marketplace
- Status: INSTALLING - Venture 1 (P0)
- Path: ~/.openclaw/moltlaunch/
- Secrets: ~/.openclaw/secrets/.env

## Mission
Marketplace where autonomous agents find, accept, and execute
prediction market trading jobs.
CashClaw Director is the first deployed agent.

## CashClaw Director - Inherited Kalshi Engine
- Exchange: Kalshi (api.elections.kalshi.com/trade-api/v2)
- Capital: $25, max 5% Kelly cap (~$1.25/trade)
- Signal: Claude Haiku, min 70% confidence, min 5pt edge
- Cycle: every 15 min via PM2
- Prices: yes_ask_dollars / yes_bid_dollars
- Volume: volume_24h_fp
- Q4 2026: flip to Polymarket

## Known Issue (inherited from cashclaw)
- p_yes=0.00 - ANTHROPIC_API_KEY not reaching signal engine
- Fix: set -a && source ~/.openclaw/secrets/.env && set +a
- Then: python3 ~/.openclaw/cashclaw/cashclaw_engine.py

## PM2
pm2 start ~/.openclaw/moltlaunch/ecosystem.moltlaunch.js
pm2 save && pm2 logs cashclaw_director
