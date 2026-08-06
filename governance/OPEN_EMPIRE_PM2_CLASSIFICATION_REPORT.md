# OPEN EMPIRE PM2 TOPOLOGY CLASSIFICATION REPORT

**Generated:** 2026-08-06T11:40:00-05:00  
**Generator:** Alusi Gate A Finalization Directive  
**Host:** Ugos-Mac-mini (macOS 12.7.6 x64)  
**PM2 Snapshot:** 2026-08-06T11:38:00-05:00  
**Total Processes:** 35 (29 online, 6 stopped)

---

## ⚠️ CRITICAL NON-NEGOTIABLES

- **CashClaw and all trading processes (PM2 IDs 38, 39, 40, 41) are UNTOUCHED.**
- No stopped processes were restarted during this classification.
- Classification is observation-only; all recommendations require Nathan approval before action.

---

## Classification Legend

| Class | Code | Meaning |
|---|---|---|
| REQUIRED_ALWAYS_ON | A | Core infrastructure; failure degrades or breaks system |
| REQUIRED_ON_DEMAND | B | Needed periodically; intentionally stopped between runs |
| OPTIONAL | C | Provides value but non-critical; recoverable if down |
| DEGRADED_REQUIRES_REPAIR | D | Was crash-looping; stopped to prevent damage; needs investigation |
| DEPRECATED | E | No longer needed; candidate for removal |
| UNKNOWN_REQUIRES_REVIEW | F | Insufficient information; Nathan review required |

---

## TIER 0 — CRITICAL ALWAYS-ON (A)

These processes are the heartbeat, data layer, approval chain, and live trading stack. They must never be stopped without explicit Nathan approval and controlled shutdown procedure.

| PM2 ID | Name | Status | Memory | Notes |
|---|---|---|---|---|
| 0 | executor | ✅ online | 31 MB | Core execution layer |
| 1 | alusi-gateway | ✅ online | 27 MB | Port 8788 |
| 4 | alusi-controlled-worker | ✅ online | 5 MB | Approval worker |
| 8 | exec-gateway | ✅ online | 1.8 MB | Exec approval gating |
| 15 | heartbeat | ✅ online | 10 MB | 5min alusi loop |
| 36 | clawdb | ✅ online | 2.6 MB | PostgreSQL 18.3 port 5432 |
| **38** | **cashclaw_director** | **✅ online** | **15 MB** | **🔴 P0 LIVE KALSHI TRADING** |
| **39** | **cashclaw_arb** | **✅ online** | **32 MB** | **🔴 P0 LIVE ARB TRADING** |
| **40** | **polymarket-trader** | **✅ online** | **19 MB** | **🔴 P0 LIVE POLYMARKET** |
| **41** | **trading_sentinel** | **✅ online** | **28 MB** | **🔴 P0 TRADING WATCHDOG** |

---

## TIER 1 — REQUIRED ALWAYS-ON (A)

These processes enable communication, routing, and automation delivery. Failure does not immediately stop trading but degrades operator visibility and automation.

| PM2 ID | Name | Status | Memory | Notes |
|---|---|---|---|---|
| 3 | alusi-discord-adapter | ✅ online | 23 MB | Discord channel |
| 5 | alusi-orchestrator | ✅ online | 4 MB | 15min cron orchestration |
| 9 | telegram-approvals | ✅ online | 6 MB | Nathan approval channel |
| 10 | ecosystem.email-dispatcher | ✅ online | 28 MB | Email via n8n |
| 14 | mission-control | ✅ online | 36 MB | Command Center port 3333 |
| 23 | n8n | ✅ online | 221 MB | Automation delivery (large but normal) |
| 24 | ollama | ✅ online | 140 MB | Local LLM port 11434 |
| 26 | native-router | ✅ online | 3.5 MB | Channel routing |
| 42 | alusi-telegram-adapter | ✅ online | 15 MB | Primary Telegram channel |

---

## TIER 2 — REQUIRED ON DEMAND (B)

Intentionally stopped; restart only when their specific use case activates.

| PM2 ID | Name | Status | Restart Count | Reason Stopped | Expected Next Start |
|---|---|---|---|---|---|
| 11 | pnl-audit | ⛔ stopped | 0 | Intentional (AGENTS.md) | On Nathan request for P&L audit |
| 12 | blco-enricher | ⛔ stopped | 0 | BLCO paused since 2026-07-19 | When BLCO lead sourcing resumes |

---

## TIER 2 — OPTIONAL (C)

Non-critical processes providing supplementary capability. Acceptable if down temporarily.

| PM2 ID | Name | Status | Memory | Notes |
|---|---|---|---|---|
| 7 | openclaw-dashboard | ✅ online | 20 MB | Port 8080; AGENTS.md ID discrepancy |
| 13 | blco-email-monitor | ✅ online | 9 MB | Inbound BLCO emails |
| 16 | nexus-telemetry | ✅ online | 26 MB | Nexus telemetry |
| 17 | open-empire-nexus | ✅ online | 26 MB | Next.js dev UI port 4444 |
| 18 | hyrve-monitor-v2 | ✅ online | 39 MB | Hyrvea/Moltlaunch monitor |
| 19 | nexus-dashboard | ✅ online | 5.5 MB | Empire nexus dashboard |
| 20 | cost-dashboard | ✅ online | 1.4 MB | AI cost tracking |
| 21 | open-empire-control-plane | ✅ online | 1.4 MB | Empire control plane |
| 22 | open-empire-mission-ui | ✅ online | 1.4 MB | Mission UI |
| 28 | claude-proxy | ✅ online | 1.8 MB | Claude API proxy |
| 25 | alpaca-demo | ✅ online | 16 MB | ⚠️ 4 restarts — review logs |

---

## DEGRADED — REQUIRES REPAIR BEFORE RESTART (D)

These processes were stopped after repeated crash restarts. **Do not restart until root cause is identified.**

| PM2 ID | Name | Status | Restart Count | Crash Pattern |
|---|---|---|---|---|
| 33 | open-empire-federation-staging | ⛔ stopped | **11** | Crash-looped before PM2 stopped it |
| 34 | open-empire-lifecycle-staging | ⛔ stopped | **9** | Crash-looped before PM2 stopped it |
| 35 | dynamics51 | ⛔ stopped | **12** | Highest crash count; unclear purpose |

### Required Actions (Nathan Approval Needed)

1. **id=33 (federation):** `pm2 logs open-empire-federation-staging --lines 50` → diagnose → fix → controlled restart
2. **id=34 (lifecycle):** `pm2 logs open-empire-lifecycle-staging --lines 50` → diagnose → fix → controlled restart
3. **id=35 (dynamics51):** Determine if 51dynamics is still a live venture; if abandoned, `pm2 delete 35`

---

## UNKNOWN — REQUIRES REVIEW (F)

| PM2 ID | Name | Status | Concern |
|---|---|---|---|
| 6 | skill-sync | ⛔ stopped | CWD is `/Downloads/OC 1` (stale path); 1 restart; purpose unclear |

### Action Required: Determine if skill-sync is still needed and whether it should be migrated to canonical path.

---

## AGENTS.MD DISCREPANCIES

AGENTS.md PM2 IDs are stale for several processes. Recommend AGENTS.md update after Gate A:

| Process | AGENTS.md ID | Live PM2 ID | AGENTS.md Status | Live Status |
|---|---|---|---|---|
| heartbeat | 1 | 15 | OK | ✅ online |
| alusi-gateway | 2 | 1 | OK | ✅ online |
| alusi-telegram-adapter | 3 | 42 | OK | ✅ online |
| exec-gateway | 13 | 8 | OK | ✅ online |
| telegram-approvals | 14 | 9 | OK | ✅ online |
| mission-control | 17 | 14 | OK | ✅ online |
| clawdb | 43 | 36 | OK | ✅ online |
| open-empire-federation-staging | 45 | 33 | **OK (WRONG)** | **⛔ stopped (11 restarts)** |
| open-empire-lifecycle-staging | 46 | 34 | **OK (WRONG)** | **⛔ stopped (9 restarts)** |

> **⚠️ AGENTS.md incorrectly shows federation-staging and lifecycle-staging as OK. These are STOPPED and crash-degraded.**

---

## Summary

| Class | Count | Healthy |
|---|---|---|
| REQUIRED_ALWAYS_ON (Tier 0+1) | 19 | 19/19 |
| REQUIRED_ON_DEMAND | 2 | 2/2 (correctly stopped) |
| OPTIONAL | 11 | 10/11 (alpaca-demo: review) |
| DEGRADED_REQUIRES_REPAIR | 3 | 0/3 (stopped, need fix) |
| UNKNOWN_REQUIRES_REVIEW | 1 | — (needs assessment) |

**Critical stack (trading + core) health: 100% online.**  
**AGENTS.md accuracy: requires update for 9 ID discrepancies and 2 status corrections.**
