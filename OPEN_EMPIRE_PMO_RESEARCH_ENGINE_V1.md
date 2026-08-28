# Open Empire PMO Research Engine V1
**Date:** 2026-08-09 | **Authority:** Nathan Asiegbu

---

## Purpose
External research informs PMO planning. Research does NOT equal adoption.

## Research Flow

```
RESEARCH → CREDIBILITY → FRESHNESS → FINDING
→ COMPARE TO EMPIRE → CAPABILITY GAP → VALUE
→ CANDIDATE → SANDBOX → BENCHMARK
→ ADOPT / PILOT / DEFER / REJECT
```

**Key gate:** Does this create a measurable advantage for an approved capability?
- YES → create CAPABILITY_IMPROVEMENT_PROPOSAL
- NO → archive as intelligence only

## Source Handling

| Source | Protocol |
|---|---|
| GitHub | inspect → security scan → license → capability fit → sandbox → benchmark → register |
| Document | extract → classify → compare with SSOT → identify implementation actions |
| Web | credibility + freshness check + cross-source verification |
| Internal data | classify → extract commitments → associate with venture/project |

**Never treat README claims as proven performance.**

## Research Lanes (priority order)

1. **Model/provider developments** — new free providers, quota changes, cost changes
2. **MCP ecosystem** — new tool integrations that could replace manual work
3. **Agent frameworks** — runtime improvements (Antfarm, n8n, new frameworks)
4. **Security advisories** — CVEs affecting installed components
5. **Pricing/free quotas** — provider policy changes affecting economic routing
6. **GitHub** — repos entering intake queue
7. **Industry best practices** — methodology improvements
8. **Venture intelligence** — CashClaw market data, BLCO buyer landscape

## Current Research Backlog

| Item | Priority | Status |
|---|---|---|
| Groq new model releases (llama3.1 family updates) | HIGH | Monitor |
| OpenRouter free tier quota limits | HIGH | Check monthly |
| Headroom install + ContextEngine benchmark | P1 | PILOT authorized |
| Hermes venv setup + benchmark vs Claude Code | P2 | Pending |
| Codex benchmark on repository audit task | P2 | Pending |
| MCP server for Kalshi/Polymarket (if exists) | P2 | Research |
| PostgreSQL backup automation (pg_dump cron) | P0 | IMPLEMENT — DB lost today |

## PostgreSQL Backup — IMMEDIATE ACTION REQUIRED

ClawDB lost `clawdb` database today on restart. Add cron backup:

```bash
# Add to crontab: every 6 hours
0 */6 * * * pg_dump -h 127.0.0.1 -p 5432 -U NeoOC clawdb > ~/.openclaw/backups/clawdb/clawdb_$(date +\%Y\%m\%d_\%H\%M).sql 2>/dev/null
```

## Promotion Criteria

A researched capability advances to ADOPT only when:
1. Benchmarked on actual Empire workloads
2. Quality meets required threshold
3. Cost per successful task ≤ current solution
4. Dependencies met without new paid services (unless Nathan approves)
5. Rollback plan exists
