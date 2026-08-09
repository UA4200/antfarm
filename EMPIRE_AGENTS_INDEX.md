# Open Empire — Agent Registry
*Last updated: 2026-08-09 | Source: AGENTS.md v5.0*

## Core Infrastructure Agents
| PM2 ID | Agent | Status | Cycle | Role |
|---|---|---|---|---|
| 0 | executor | ✅ OK | continuous | Core task executor |
| 1 | heartbeat | ✅ OK | continuous | Alusi-loop heartbeat |
| 2 | alusi-gateway | ✅ OK | continuous | OpenClaw gateway |
| 3 | alusi-telegram-adapter | ✅ OK | continuous | Telegram channel |
| 4 | alusi-discord-adapter | ✅ OK | continuous | Discord channel |
| 5 | alusi-controlled-worker | ✅ OK | continuous | Approval worker |
| 6 | alusi-orchestrator | ✅ OK | continuous | Multi-agent orchestration |
| 13 | exec-gateway | ✅ OK | continuous | Exec approval gateway |
| 14 | telegram-approvals | ✅ OK | continuous | Telegram approval handler |
| 15 | ecosystem.email-dispatcher | ✅ OK | continuous | Ecosystem email layer |
| 17 | mission-control | ✅ OK | continuous | Command Center UI port 3333 |

## Trading Agents — PROTECTED
| PM2 ID | Agent | Status | Cycle | Role |
|---|---|---|---|---|
| 38 | cashclaw_director | ✅ OK | every 5min | Kalshi director, Kelly, V2 API, $10 cap |
| 39 | cashclaw_arb | ✅ OK | every 5min | Kalshi bundle arb + cross-arb alert |
| 40 | polymarket-trader | ✅ OK | 15min cycle | MLB/MLS/sports-champ, GPT-4o signals |
| 41 | trading_sentinel | ✅ OK | every 5min | CashClaw watchdog |

## AI / Inference Agents
| PM2 ID | Agent | Status | Cycle | Role |
|---|---|---|---|---|
| 24 | ollama | ✅ OK | continuous | Local LLM server, port 11434, 6 models |
| 48 | freeway | ✅ OK | continuous | FCC proxy, port 8082, 72 models |
| 50 | grafana | ✅ OK | continuous | FCC Cost Dashboard, port 3001 |
| 51 | fcc-metrics-exporter | ✅ OK | continuous | Free-Way usage scraper every 5min |
| 54 | oe-proxy | ✅ OK | continuous | Governed inference proxy port 4100 |

## Open Empire Agents
| PM2 ID | Agent | Status | Cycle | Role |
|---|---|---|---|---|
| 10 | hyrvea-monitor | ✅ OK | continuous | Hyrvea pipeline monitor |
| 33 | open-empire-federation-staging | ✅ OK | every 15min | Federation state, Python 3.14.6 |
| 34 | open-empire-lifecycle-staging | ✅ OK | every 15min | Lifecycle state, Python 3.14.6 |
| 43 | clawdb | ✅ OK | continuous | PostgreSQL 18.3, port 5432 |
| 52 | kg-api | ✅ OK | continuous | Knowledge Graph API, port 6279 |

## On-Demand / Stopped Agents
| PM2 ID | Agent | Status | Cycle | Role |
|---|---|---|---|---|
| 11 | email-dispatcher | ⏹ STOPPED | on-demand | Approved email dispatch |
| 12 | openclaw-dashboard | ⏹ STOPPED | on-demand | Legacy dashboard |
| 16 | pnl-audit | ⏹ STOPPED | on-demand | P&L audit runner |

## Sovereign / Unnamed Agents
| Agent | Status | Cycle | Role |
|---|---|---|---|
| sovereign_proxy | ✅ OK | continuous | Approval gating, all council items |
| blco_broker | ✅ OK | every 5min | BLCO buyer qualification (sourcing paused) |
| b2b_outreach | ✅ OK | every 5min | Lead gen draft-only |

## Navigation
← [[EMPIRE_HOME]]
