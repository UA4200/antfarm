# Revenue Strategy Backlog
**Source:** Absorbed from intake repos + Empire intelligence | **Updated:** 2026-05-07

---

## Active Revenue Streams (Empire)

### 1. BLCO (B2B Lead + Client Ops)
- **Status:** Active — blco-enricher installed (monitoring crash loop)
- **Mechanism:** Lead sourcing → enrichment → outreach → proposal → close
- **Agents:** Revenue_Operator, b2b_outreach, blco_broker
- **Target:** $5k–$12k/month from ADAI client work

### 2. ADAI Inc (AI Agency Services)
- **Status:** Active — outreach not yet started (P0 blocker)
- **Mechanism:** AI automation, Claude Code implementation for SMBs
- **Target:** $3k–$8k/month recurring

### 3. CashClaw (Algorithmic Trading)
- **Status:** Signal broken (CC-01) — Trading Sentinel monitoring
- **Mechanism:** Polymarket, Kalshi prediction markets + Hyperliquid (sandboxed)
- **Target:** $2k–$5k/month passive when signal restored
- **Warning:** hyperliquid-trading-agent — NEVER install without full security audit

---

## Identified Opportunities (from repo absorption)

### ClawRouter / Franklin Integration
**Source:** awesome-claude-code-toolkit (ClawRouter v0.12.161)
- Routes prompts across 41+ LLMs via x402 USDC micropayments
- 15-dimension routing, 4 profiles (speed/quality/cost/balanced)
- **Revenue angle:** Offer multi-LLM routing as an ADAI service feature
- **Cost savings:** Use cost profile during ADAI Night Ops (12am–4am CDT) to reduce token spend by 40–60%
- **Action:** Evaluate ClawRouter as backbone for ADAI automation pipeline — reduces Claude API spend

### Skill Marketplace Play
**Source:** ECC + awesome-claude-skills analysis
- 471 unique skill URLs indexed in master_skills_index.json
- OpenClaw skill ecosystem growing — early skill publishers get attention
- **Revenue angle:** Publish 3–5 high-quality OpenClaw skills under ADAI brand
- **Action:** Package 2 existing Empire automations as public skills; measure star growth

### Agency-as-a-Service
**Source:** agency-agents (59 templates across 6 domains)
- Templates cover: engineering, finance, PM, sales, strategy, product
- **Revenue angle:** White-label agent team for SMB clients — "Your AI department in a box"
- **Pricing:** $1,500–$3,000/month per client for managed agent stack
- **Action:** Package agency-agents + VoltAgent into ADAI offering; pitch to 5 leads

### Antfarm Workflow Productization
**Source:** Antfarm (feature-dev, security-audit, bug-fix workflows)
- Deterministic, repeatable, no-hallucination multi-agent workflows
- **Revenue angle:** "AI code review + security audit" as a service
- **Pricing:** $500–$1,500 per repo security audit
- **Action:** Run antfarm security-audit on 3 client codebases as proof of concept

### GitNexus Intelligence Layer
**Source:** GitNexus v1.6.3 — MCP + workspace analysis
- Indexes codebase structure, provides semantic search, generates context
- **Revenue angle:** Include GitNexus as "codebase onboarding" in ADAI client engagement
- **Differentiator:** Day 1 context vs. 2-week ramp for human developers

---

## Priority Matrix

| Strategy | Monthly Revenue Potential | Effort | Priority |
|----------|--------------------------|--------|----------|
| ADAI outreach (first batch) | $3k–$8k | Low (already built) | **P0** |
| BLCO lead revival | $2k–$5k | Low (fix crash loop) | **P0** |
| CashClaw CC-01 fix | $2k–$5k passive | Medium | **P1** |
| Agency-as-a-Service pitch | $1.5k–$3k/client | Medium | **P1** |
| Antfarm audit productization | $0.5k–$1.5k/audit | Low | **P2** |
| ClawRouter cost optimization | -40% API spend | Low | **P1** |
| Skill marketplace | Reputation/brand | Low | **P3** |

---

## Next Actions

1. **TODAY:** Start ADAI first outreach batch (requires DISCORD_OWNER_ID + Telegram bot)
2. **THIS WEEK:** Fix blco-enricher crash loop (1357 restarts) → Revenue_Operator unblocked
3. **THIS WEEK:** Investigate CashClaw CC-01 signal failure root cause
4. **NEXT WEEK:** Package ADAI "AI Department" offering using agency-agents templates
5. **NEXT WEEK:** Run antfarm security-audit on 1 client repo as pilot
