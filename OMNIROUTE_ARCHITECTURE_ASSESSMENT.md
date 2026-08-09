# OmniRoute Architecture Assessment
**C0.4 | Generated:** 2026-08-09 | **Agent:** Research Agent A  
**Repo:** `diegosouzapw/OmniRoute` | **Last verified:** 2026-08-09 (actively maintained; re-audits every 2 weeks)

---

## OmniRoute At a Glance

| Attribute | Value |
|---|---|
| License | MIT |
| Contributors | 500+ |
| Providers | 290+ total, 90+ free tiers |
| Models | 500+ (516 documented) |
| Free tokens/month | ~1.53B (documented free tiers, pool-deduped) |
| Default port | localhost:20128 |
| Routing strategies | 19 (priority, fill-first, weighted, round-robin, cost-optimized, headroom, auto, fusion, pipeline…) |
| Compression | RTK+Caveman stacked: 15–95% tokens saved (~89% avg on tool-heavy sessions) |
| Packaging | npm global (`npm i -g omniroute`), Docker, Electron Desktop/PWA |
| MCP | 104 tools, A2A, memory, guardrails, evals |
| Tests | 25,000+ |
| Circuit breakers | ✅ |
| TLS stealth | ✅ (3-level proxy) |

### Architecture

```
IDE / Agent (Claude Code, Cursor, Cline…)
        │
        ▼
OmniRoute Smart Router (localhost:20128/v1)
   ├── RTK + Caveman compression
   ├── 19 routing strategies
   ├── Circuit breakers + key cooldown + model lockout
   ├── TLS stealth proxy (3 levels)
   ├── MCP (104 tools) + A2A
   └── 4-tier cascade:
        Tier 1: Subscription (Claude Code, Codex, Copilot)  →quota out→
        Tier 2: API Key (DeepSeek, Groq, xAI)              →budget hit→
        Tier 3: Cheap (GLM $0.5, MiniMax $0.2)             →budget hit→
        Tier 4: Free (Kiro, Qoder, Pollinations)            always-on
```

### Zero-Config Start

```bash
npm i -g omniroute
# Server auto-starts on localhost:20128
# model=auto works out of the box with no API keys
```

---

## What We Already Have (Open Empire Stack)

| Component | Capability |
|---|---|
| Free-Way (FCC) port 8082 | 5 providers, 72 models, OpenAI+Anthropic bridge, PM2-managed |
| fcc_router.py | Governed auto-selector, task→model chain routing, fallback logic, cost tracking |
| native-router (PM2 id=26) | Running, port unknown |
| Governance layer | Kelly controls, spend caps ($10/day), approval gates, financial safety |

**Free-Way already handles:** multi-provider gateway, free-tier routing, provider fallback, cost-optimized routing, usage tracking, provider health, rate-limit handling.

**Free-Way does NOT have:** RTK+Caveman compression, 19 routing strategies, MCP gateway, live dashboard, TLS stealth, circuit breakers at 290-provider scale, 4-tier cascade, desktop GUI.

---

## The 10 Promotion Questions

### Q1: What problem does OmniRoute solve?

OmniRoute solves three distinct problems:
1. **Provider fragmentation** — aggregates 290+ providers behind one OpenAI-compatible endpoint with quota-aware fallback, so developer tools never hit a rate limit mid-session
2. **Token waste** — RTK+Caveman stacked compression saves 15–95% tokens on tool-heavy sessions, reducing cost and latency
3. **Setup friction** — zero-config start (no API keys required), works with all major coding agents out of the box

### Q2: Do we already solve that problem?

**Partially.** Free-Way (FCC) solves problem #1 at smaller scale (5 providers vs 290). Problem #2 is **not solved** — we have zero token compression. Problem #3 is solved differently (fcc_router.py is governance-first, not zero-config).

Critical gap: **we have no token compression whatsoever.** OmniRoute's RTK+Caveman is the standout unmatched capability.

### Q3: Is the existing solution better?

**Depends on dimension:**

| Dimension | Winner |
|---|---|
| Governance/sovereignty | **Free-Way + fcc_router.py** — baked-in Kelly controls, spend caps, approval gates |
| Provider breadth | **OmniRoute** — 290 vs 5 (58× more) |
| Token compression | **OmniRoute** — 15–95% vs 0% |
| Operational stability | **Free-Way** — PM2-managed, known state, integrated with Open Empire |
| Dashboard/observability | **OmniRoute** — live analytics, quota tracking, savings reporting |
| Custom routing logic | **Free-Way** — fcc_router.py has domain-specific task chains |
| Free token capacity | **OmniRoute** — ~1.53B/month vs ~72 models (capacity not published) |

**Overall:** Our stack is better for governed, policy-constrained autonomous ops. OmniRoute is better for raw provider breadth, compression, and developer-tool integration.

### Q4: What measurable improvement does it provide?

| Metric | Current | With OmniRoute |
|---|---|---|
| Active providers | 5 | 290 (58× more fallback options) |
| Free tier token pool | ~72 models (capacity unknown) | ~1.53B tokens/month documented |
| Token compression | 0% | 15–95% (avg ~89% on tool-heavy sessions) |
| Cost savings on free tier | $0.00 (already free) | $0.00 (still free, but lower latency) |
| Routing strategies | ~4 (fcc_router chains) | 19 |
| MCP tools available | 0 via gateway | 104 |

**Key finding:** On our current **fully-free** usage (15 calls, 3790 tokens, $0.00 cost), OmniRoute provides **zero dollar savings** but meaningful latency reduction via compression and dramatically expanded fallback capacity.

### Q5: What new dependencies does it create?

- Node.js npm global install (single binary, we have Node v24 ✓)
- New port 20128 (no known conflict)
- External maintainer risk (single-maintainer community project despite 500+ contributors)
- If replacing FCC: all agents must be re-pointed from port 8082 → 20128
- No governance layer — Kelly controls, approval gates, spend caps are not built into OmniRoute; must be layered above it
- Desktop app / Electron optional (no requirement)

### Q6: What does failure affect?

**If OmniRoute is used alongside FCC (additive):**
- OmniRoute failure = lose compression + expanded provider access; FCC still serves all requests
- Blast radius: low

**If OmniRoute replaces FCC (substitutive):**
- OmniRoute failure = all 72 model routes go dark
- Trading agents (cashclaw_director, arb, polymarket_trader) lose signal generation
- Blast radius: critical

### Q7: Can it be rolled back?

**Yes, cleanly.**
- `pm2 stop omniroute` or `npm uninstall -g omniroute`
- Revert `ANTHROPIC_BASE_URL`/`OPENAI_BASE_URL`/`OPENAI_API_BASE` env vars back to `http://localhost:8082/v1`
- FCC (Free-Way) remains intact throughout
- Rollback time: ~2 minutes

### Q8: Does it reduce or increase total operating complexity?

**Increases complexity if additive (two gateways, two configs, two ports).**  
**Reduces complexity if substitutive** (one gateway instead of FCC + native-router + fcc_router.py).  

However, the governance layer (fcc_router.py) must be preserved regardless — OmniRoute does not replicate financial controls. A hybrid architecture (OmniRoute upstream of fcc_router.py) would be 3 layers, which is worse.

Net assessment: **increases complexity** unless we also retire native-router (PM2 id=26) and simplify fcc_router.py to a thin governance wrapper over OmniRoute.

### Q9: Does it reduce cost per successful task?

**On free tier: no** — cost is already $0.00.  
**Latency per successful task:** yes, compression reduces token count → faster responses from providers.  
**Tasks per dollar:** undefined (free), but compression means more complex tasks fit within free-tier context limits.  
**Reliability per task:** yes — 290 fallback providers vs 5 dramatically reduces failure probability.

### Q10: Should it be production, pilot, deferred, or rejected?

**SELECTIVE CAPABILITY PILOT for compression only.**

OmniRoute's RTK+Caveman compression is the single feature we genuinely lack. However, deploying the full OmniRoute stack as a gateway replacement introduces:
- Governance gap (no Kelly controls, no spend caps)
- Maintainer dependency (community project)
- Migration cost (all agents re-pointed)

Better approach: evaluate OmniRoute's compression as a **standalone module** or implement equivalent compression in fcc_router.py directly.

---

## Verdict

```
OMNIROUTE_SELECTIVE_CAPABILITY_ONLY
```

**Rationale:** OmniRoute solves real problems (provider breadth, token compression) but is not a justified full replacement for the governed Free-Way stack. The RTK+Caveman compression is the one genuinely absent capability; the remaining features either duplicate FCC or add complexity without commensurate governed-autonomy benefit. Token compression on free tier saves $0 in cost but reduces latency and increases effective context capacity. 

**Recommended action:** 
1. Do not install OmniRoute as a gateway replacement
2. Evaluate headroom (C0.8) for the compression gap — it directly wraps OpenClaw
3. If provider breadth becomes a bottleneck, pilot OmniRoute's provider catalog behind the existing fcc_router.py governance layer (OmniRoute → fcc_router.py → Open Empire) with a 30-day trial and explicit rollback checkpoint

**Blocked by:** Governance gap — OmniRoute has no analog for Kelly controls, daily spend caps, or approval gates. These are non-negotiable for autonomous financial agents.
