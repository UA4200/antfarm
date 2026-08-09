# Phase 6 — Alusi Stability Gate

**Opened:** 2026-07-30 ~11:26 CDT
**Gate closes:** 2026-07-31 ~11:26 CDT (24-hour soak)
**Authorized by:** PR14-264d22c (OPEN_EMPIRE_FULL_RECONSTRUCTION_AND_DEPLOYMENT.md)

## Gate Criteria (ALL must pass to proceed to Phase 7)

| # | Criterion | Pass Condition | Current |
|---|---|---|---|
| G1 | alusi-gateway uptime | 24h continuous, 0 unstable restarts | MONITORING |
| G2 | CashClaw Director | ONLINE throughout, 0 unstable | ✅ PASSING (check #6: 2h) |
| G3 | n8n | Healthy at port 5678 throughout | MONITORING |
| G4 | Postgres | Accepting connections throughout | ✅ PASSING (just started) |
| G5 | No CI failures | All 6 repos CI green at gate close | ✅ PASSING |
| G6 | No P0 crashes | No PM2 unstable_restart events | MONITORING |
| G7 | Mission Control | Accessible at port 3333 | MONITORING |
| G8 | Telegram adapter | Online throughout | MONITORING |

## Checkpoints
| Time (CDT) | Who | Actions |
|---|---|---|
| 11:26 (T+0) | Alusi | Gate opened, baseline captured |
| 17:00 (T+5.5h) | Alusi | Midday check — PM2 state, postgres, CashClaw |
| 23:00 (T+11.5h) | Alusi | Night check |
| 2026-07-31 05:00 (T+17.5h) | Alusi | Pre-dawn check |
| 2026-07-31 11:26 (T+24h) | Alusi | Gate evaluation — pass/fail |

## Failure Actions
- G2 (CashClaw unstable): HALT immediately, escalate to Nathan
- G1 (alusi-gateway down): Restart, log, continue monitoring
- G4 (Postgres down): Attempt restart via pg_ctl, log
- Any P0 crash: 3 consecutive failures → halt gate, await Nathan instruction

## Baseline (T+0)
- PM2: 32 processes (27 online + 5 stopped at baseline)
- CashClaw: 116 restarts, 2h uptime, 0 unstable
- Postgres: PostgreSQL 18.3, clawdb exists
- n8n: OK port 5678
- All 6 repos: CI green

## Phase 7 Trigger
Nathan command: `APPROVE PHASE7 MERGE <sha>` OR Alusi auto-advance if all G1-G8 pass at T+24h.
