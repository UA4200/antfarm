# Open Empire Ventures
*Last updated: 2026-08-09*

## Active Ventures

- **CashClaw** — Autonomous trading (Kalshi + Polymarket), $65 deployed
  - PM2 38: cashclaw_director (5min cycle, Kelly criterion)
  - PM2 39: cashclaw_arb (bundle + cross-arb detection)
  - PM2 40: polymarket-trader (MLB/MLS/sports-champ strategy)
  - PM2 41: trading_sentinel (watchdog)
  - Daily spend caps: $10 per agent

- **BLCO Pipeline** — Buyer qualification (paused, 192 leads)
  - Status: Lead sourcing PAUSED 2026-07-19
  - Pipeline: 192 leads (Europe 27, Asia 28, Americas 19, MENA 15, Global 11, unknown 89)
  - Output: ~/.openclaw/blco/leads.jsonl → n8n → Airtable

- **ADAI Solutions** — AI product line
  - Enterprise Agent Factory
  - Code Migration tooling

- **Moltlaunch** — HyrveAI marketplace
  - Monitor: PM2 10 (hyrvea-monitor, continuous)

- **Open Empire** — Sovereign AI ecosystem
  - Federation staging: PM2 33 (every 15min)
  - Lifecycle staging: PM2 34 (every 15min)
  - KG API: PM2 52 (port 6279)

## Navigation
← [[EMPIRE_HOME]]
