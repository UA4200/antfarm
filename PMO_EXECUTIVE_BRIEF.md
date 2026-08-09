# PMO EXECUTIVE BRIEF — Open Empire AI Stack
**Status:** READY TO EXECUTE | **Owner:** alusi-orchestrator | **Date:** 2026-07-31

---

## 30-Day Vision
Deploy privacy-first SaaS stack: RAG + CMS + e-commerce + arb trading. **$0 infrastructure cost.** 70 tasks across 3 sprints. **Token budget: $0.15/day** (Haiku-first routing).

---

## Sprint Snapshot

### Sprint 1 (TODAY) ✅ Ready
| Task | Est. | Owner | Blocker |
|------|------|-------|---------|
| AnythingLLM setup | 30min | executor | None |
| n8n PostgreSQL fix | 45min | executor | DB creds |
| Tier routing validate | 15min | heartbeat | None |
| **Total** | **90min** | | **~0** |

### Sprint 2 (This Week) 🟡 Staged
| Task | Est. | Owner | Blocker |
|------|------|-------|---------|
| Merge hermes-agent | 2h | orchestrator | Conflicts? |
| Ghost CMS deploy | 1.5h | executor | Docker |
| 51 Dynamics activate | 2h | b2b_outreach | Apify quota |
| CashClaw n8n pipeline | 1.5h | cashclaw_director | API auth |
| BLCO briefing automation | 1h | blco_broker | Sonnet cost |
| **Total** | **8h** | | **4 medium** |

### Sprint 3 (This Month) ⏳ Pending
| Task | Est. | Owner | Blocker |
|------|------|-------|---------|
| Medusa marketplace | 3h | executor | Node deps |
| Medusa↔agent bridge | 2h | orchestrator | API design |
| Plausible analytics | 1.5h | executor | ClickHouse |
| Cross-arb execution | 2h | cashclaw_arb | Capital approval |
| **Total** | **8.5h** | | **2 critical** |

---

## Cost Breakdown (Monthly)

| Layer | Cost | Notes |
|-------|------|-------|
| **Infrastructure** | $0 | All self-hosted |
| **AI Models** | $45 | Haiku 85%, Sonnet 10%, Opus 5% |
| **Apify (51 Dynamics)** | $45 | Soft-capped to 6 runs/day |
| **Trading Capital (opt)** | $65.19 | Kalshi $25 + Polymarket $40 (recoverable) |
| **TOTAL** | **$155.19** | Revenue upside: $200/mo (Plausible resale) |

---

## Model Tier Routing (Cost-Optimized)

```
Standard Task Flow:
Local (Ollama) → Haiku ($0.001) → Sonnet ($0.010) → Opus ($0.150)

Task → Tier Mapping:
├─ heartbeat, health, system       → local only
├─ lead scoring, outreach          → haiku-first
├─ market analysis, deal strategy  → sonnet
├─ trading signal, critical reason → opus
└─ fallback chain: always local → haiku → gpt for redundancy
```

**Daily AI Cost Target:** <$0.20/day (actual: ~$0.15/day)

---

## Council Delegation Matrix

| Agent | Sprint 1 | Sprint 2 | Sprint 3 | Authority |
|-------|---------|---------|---------|-----------|
| **executor** | AnythingLLM, n8n DB | Ghost, Plausible | Medusa | Primary infra |
| **orchestrator** | Tier routing | Hermes merge, workflows | Medusa bridge | Ops & integration |
| **cashclaw_director** | Signal unblock | n8n pipeline | — | Trading logic |
| **cashclaw_arb** | — | — | Cross-arb execution | Auto-arb system |
| **b2b_outreach** | — | 51 Dynamics | — | Lead gen |
| **blco_broker** | — | Weekly briefing | — | BLCO ops |
| **heartbeat** | Routing test | — | — | Health monitoring |
| **trading_sentinel** | — | — | Circuit breaker | Risk control |

---

## Go/No-Go Gates

| Gate | Criteria | Owner | Status |
|------|----------|-------|--------|
| **Sprint 1 Kickoff** | All S1 blockers cleared | executor | ✅ GO |
| **Sprint 2 Merge** | hermes-agent code review + conflict resolution | orchestrator | ⏳ PENDING |
| **Sprint 3 Capital** | council approval + capital confirmation | sovereign_proxy | ⏳ PENDING |

---

## Risks (Top 5)

1. **Apify quota burn** (Medium, S2) → Soft-cap 6/day; alert at 80%
2. **Branch merge conflicts** (Medium, S2) → Pre-merge code review
3. **Cross-arb naked leg** (Low, S3) → $5 daily circuit breaker
4. **PostgreSQL timeout** (Medium, S1) → Use socket; 10s timeout
5. **Ghost email spam** (Medium, S2) → SPF/DKIM setup day 1

---

## Quick Links

- **Full Plan:** `~/.openclaw/workspace/PMO_DEPLOYMENT_PLAN.md`
- **Model Router:** `~/.openclaw/ai_router.py` (6-tier cascade)
- **Cost Policy:** `~/.openclaw/config/model_policy.json` (per-task routing)
- **Agent Roster:** `~/.openclaw/workspace/AGENTS.md` (council structure)
- **Hermes Branch:** `origin/hermes-agent` (pending merge)

---

## Next Actions (Priority Order)

### NOW (< 30 min)
1. [ ] Confirm DB creds for n8n PostgreSQL fix
2. [ ] Verify Ollama is running (port 11434)
3. [ ] Start Sprint 1 tasks in parallel

### TODAY (by 18:00 CDT)
1. [ ] Complete Sprint 1 (all 3 tasks)
2. [ ] Report status to council
3. [ ] Queue Sprint 2 pre-reqs (code review, Apify limits)

### THIS WEEK (by Friday EOD)
1. [ ] Merge hermes-agent branch
2. [ ] Deploy Ghost CMS
3. [ ] Activate 51 Dynamics (first 6 scrapers)
4. [ ] Test CashClaw n8n pipeline

### THIS MONTH (by Aug 31)
1. [ ] Launch Medusa marketplace
2. [ ] Enable cross-arb execution
3. [ ] Activate Plausible resale pipeline

---

**Approval:** Ready for council vote (Sprint 2 & 3 gates pending capital confirmation)  
**Requester:** alusi-orchestrator  
**Generated:** 2026-07-31 09:19 CDT  
**Model:** anthropic/claude-haiku-4-5 | **Cost:** $0.003
