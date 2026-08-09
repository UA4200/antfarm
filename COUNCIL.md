# COUNCIL.md - Multi-Council Architecture
Version: 1.0 | 2026-05-06

## Design Principle
Empire runs like a corporation, not a group chat.
Alusi = CEO + COS + routing layer + memory governor + escalation authority.
All councils operate independently, report upward through compressed intelligence only.

## Agent Roster

### ACTIVE ALWAYS (continuous, never sleep)
| Agent | Role | Model |
|---|---|---|
| Alusi | CEO, memory governor, escalation authority | sonnet (default) |
| PMO_Commander | task routing, project state | haiku |
| Revenue_Operator | BLCO + ADAI revenue ops | haiku |
| Trading_Sentinel | CashClaw watchdog, Kalshi monitor | haiku |
| LifeOS_Orchestrator | schedule, health, daily brief | haiku/local |

### SLEEP MODE (dormant until triggered)
| Agent | Trigger |
|---|---|
| cashclaw | CC-01 signal fix confirmed |
| cashclaw_director | new market cycle |
| blco_broker | new lead signal or 5min cron |
| b2b_outreach | new ADAI outreach task |
| email-dispatcher | approval granted |
| pnl-audit | on-demand |
| skill-sync | skill install event |
| openclaw-dashboard | on-demand |

### Trigger Conditions
- new task created
- new lead qualified
- scheduled cron fires
- escalation from subordinate
- approval request received

## Council Channels (5 permanent)
| Channel | Scope |
|---|---|
| #life-os | health, schedule, personal ops |
| #video-studio | content production, publishing |
| #stock-trading | CashClaw, Kalshi, Polymarket |
| #adai-hq | ADAI Inc product + client ops |
| #empire-command | cross-council, escalations, strategy |

No new channels without ROI justification.

## Communication Protocol
```
Agent
  → structured summary (≤300 tokens)
  → Alusi
  → routed selectively to council or action
```

### Forbidden
- agent-to-agent chatter
- duplicated reporting
- recursive analysis loops
- broad memory injection

## Context Retrieval
Agents retrieve ONLY:
- task-relevant memory
- recent summaries (last 24h)
- required KPIs

Deeper retrieval → escalate to Alusi → Alusi performs selective recall.

## Escalation Path
```
Local agent (haiku/local)
  → PMO_Commander (haiku)
    → Alusi (sonnet)
      → Opus [only for: security review, major architecture, high-stakes decisions]
```

## ADAI Execution Window
Night ops: 12:00 AM – 4:00 AM CDT
Tasks: lead sourcing, proposal drafting, automation research, CRM cleanup, content batching
Model: haiku primary, sonnet for complex drafts

## Cost Targets
| Mode | Daily Cap |
|---|---|
| Normal ops | < $10 |
| Heavy ops | < $20 |
| Local execution | 80% |
| Lightweight cloud | 15% |
| Premium reasoning | 5% |

## Success Metrics
1. Full operational continuity
2. Minimal token drift
3. No context pollution
4. Fast retrieval (<2s)
5. Sustainable long-term cost
6. High signal-to-noise ratio
