# Headroom Pilot Plan — P1
**Approved:** 2026-08-09 | **Duration:** 4 weeks | **Verdict:** PILOT

---

## Pilot Scope (what gets compressed)

✅ **IN SCOPE:**
- Kalshi API JSON responses (market data, order books)
- Polymarket API JSON responses (positions, settlements)
- Free-Way /api/usage responses
- Large log payloads before analysis
- Repetitive structured data (trade records, signal batches)

❌ **EXPLICITLY EXCLUDED:**
- Kelly criterion calculations
- Approval gate logic
- Financial control prompts
- CONSTITUTION.md content
- Security policy instructions
- CashClaw trading agent system prompts
- Any prompt containing spend caps, risk limits, or capital deployment rules

---

## 4-Week Schedule

| Week | Action | Success Gate |
|---|---|---|
| 1 | Install ContextEngine plugin only (`headroom wrap openclaw`) | Plugin loads, no errors |
| 2 | Enable LITE compression (10%) on Kalshi JSON responses | Token reduction ≥8%, quality preserved |
| 3 | Enable STANDARD (25%) on all non-governance data | Token reduction ≥20%, 0 instruction loss |
| 4 | Benchmark: LITE vs STANDARD vs OFF | Cost/latency/quality comparison |

---

## Baseline Metrics (pre-pilot)

| Metric | Value |
|---|---|
| Free-Way calls (session) | 15 calls |
| Total tokens | 3,790 |
| Estimated cost | $0.00 (free tier) |
| Dollar savings from compression | $0 (already free) |
| Latency reduction (expected) | 10–30% |
| Quota headroom (expected) | +33% more requests before rate limits |

---

## Compression-Off Rules (non-negotiable)

Add to Headroom config:
```yaml
compression:
  exclude_patterns:
    - "kelly"
    - "spend_cap"
    - "approval_required"
    - "ANTHROPIC_API_KEY"
    - "private_key"
    - "cashclaw"
    - "trading"
  governance_passthrough: true
  financial_passthrough: true
```

---

## Promotion Criteria

After 4 weeks, Headroom advances to production only if:
1. Zero instruction loss verified in any controlled task
2. Token reduction ≥15% across non-governance prompts
3. 0 financial/governance prompts touched
4. Quality score ≥ baseline on 20 random benchmark tasks
5. No impact on CashClaw trade outcomes

Otherwise: **DEFER** — maintain FCC-only architecture.

---

## Status: PLAN APPROVED — not yet started. Install begins after KG is stable.
