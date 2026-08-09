# PMO Research Directive — N8N Automation Integration
Issued: 2026-05-16 | Authority: Nathan (Alusi PMO Office)
Return: Morning Brief (daily 7am Telegram + briefing group)

---

## Mission
Research, document, and propose N8N automation flows for all tested and approved workflows in the Open Empire stack. Priority: workflows already running as cron/shell scripts that can be made observable, retryable, and alertable via N8N.

## Scope

### Tier 1 — Immediate Candidates (already running, move to N8N)
| Workflow | Current Impl | N8N Opportunity |
|---|---|---|
| CI/CD health check | cron → bash | N8N schedule → multi-step → Telegram result |
| BLCO weekly scan | cron → python | N8N schedule → scraper → Airtable → Telegram |
| Morning brief | cron → bash | N8N schedule → AI summary → Telegram/Discord |
| Obsidian sync | cron → bash | N8N schedule → file ops → validation |
| CashClaw signal engine | pm2 → python | N8N trigger → signal → executor → alert |
| Hyrve monitor | cron → node.js | N8N schedule → API poll → accept → alert |
| Lead enrichment | cron → node.js | N8N schedule → enrichment → Airtable push |
| Dream engine | cron → python | N8N schedule → memory compress → write |

### Tier 2 — New Opportunities
- BLCO outreach drip sequence (Day 0, 7, 14) → N8N email drip with approval gate
- Trade outcome tracking (Kalshi results → Airtable → P&L dashboard)
- Error alert aggregator (all logs → N8N → one daily error digest)
- Agent health watchdog (PM2 status → N8N → Telegram if degraded)
- Weekly P&L report (trades.jsonl → N8N → formatted Telegram/Discord report)

## Research Questions
1. Which existing N8N webhooks are already wired? (check n8n at localhost:5678)
2. What N8N nodes/integrations are available for: Kalshi, Airtable, Telegram, ClawDB?
3. Can N8N replace PM2 for any agents (retry, scheduling, error handling)?
4. Cost/complexity estimate per workflow migration
5. Best pattern for approval-gated workflows in N8N (human-in-the-loop node)

## Deliverable Format (Morning Brief Section)
```
## N8N Automation Pipeline
[Date]

### Workflows Proposed This Cycle
- [Workflow Name]: [Current impl] → [N8N proposal] | Effort: [S/M/L] | Revenue impact: [High/Med/Low]

### N8N Health
- Active workflows: X
- New proposals: X
- Approved for migration: X

### This Week's Migration Target
- [One workflow to migrate]
```

## Output Location
- Research: ~/.openclaw/workspace/directives/n8n_automation_research.md
- Morning brief section: appended to ~/.openclaw/logs/morning_brief_YYYY-MM-DD.md
- Telegram: included in 7am briefing summary

## Governance
- All N8N workflow builds: Nathan approval before activation
- Live external sends (email, Telegram to external): approval gate required
- Financial operations: always approval-gated
- Propose one migration per week, validate before next

## Status
- [ ] Initial research complete
- [ ] Tier 1 candidates documented with N8N node maps
- [ ] First workflow migrated to N8N (propose week of 2026-05-19)
- [ ] Morning brief section live
