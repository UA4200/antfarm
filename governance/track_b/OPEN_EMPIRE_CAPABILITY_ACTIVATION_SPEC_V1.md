# OPEN EMPIRE — CAPABILITY ACTIVATION SPEC V1
## B6 Capability Activation Specification

**Status:** ACTIVE  
**Version:** 1.0.0  
**Created:** 2026-08-06  
**Operator:** Nathan Asiegbu  
**Governed by:** Open Empire Constitution v2, Governance Baseline v1.0.0 (commit 17df0ff)

---

## 1. Purpose

This spec defines the activation runbooks for each major Open Empire capability. Each runbook includes prerequisites, services to start, validation steps, kill switch procedures, and current status.

The runbooks are designed to be **executed by Alusi** on Nathan's instruction or by Nathan directly.

---

## 2. Capability Inventory

| Capability | Status | Key Services |
|-----------|--------|-------------|
| TRADING | ACTIVE | cashclaw_director, cashclaw_arb, polymarket-trader, trading_sentinel |
| BLCO | PAUSED | blco_broker (b2b_outreach) |
| ADAI | PRE_LAUNCH | None built yet |
| CONTENT | ACTIVE | hyrvea-monitor |
| INFRASTRUCTURE | ACTIVE (always-on) | executor, alusi-gateway, heartbeat, n8n, clawdb |
| APPROVALS | ACTIVE | exec-gateway, telegram-approvals, alusi-controlled-worker |
| COMMUNICATIONS | ACTIVE | alusi-telegram-adapter, alusi-discord-adapter |
| LOCAL_AI | ACTIVE | ollama |
| EMAIL | ON_DEMAND | email-dispatcher |
| GOVERNANCE | ACTIVE | executor (validation tasks) |

---

## 3. ENABLE TRADING

### 3.1 Overview

Automated prediction-market trading on Kalshi and Polymarket US. Three active agents + one watchdog sentinel.

**Current status:** ✅ ACTIVE  
**Capital deployed:** Kalshi $1.55 free + $80 open positions, Polymarket US $0.06  
**Daily spend caps:** $10 per platform per agent

### 3.2 Prerequisites Checklist

```
[ ] Kalshi API key valid: curl -s https://trading-api.kalshi.com/trade-api/v2/portfolio/balance (expect 200)
[ ] Kalshi private key file exists: ls -la $(cat ~/.openclaw/secrets/.env | grep KALSHI_PRIVATE_KEY_PATH | cut -d= -f2)
[ ] Kalshi private key permissions: stat -f '%Lp' <key_path> → 600
[ ] Polymarket API key valid: check polymarket-trader logs for auth success
[ ] Kalshi balance > $5: verify via Kalshi portfolio API
[ ] Polymarket balance > $1: verify via Polymarket API
[ ] Trading hours: Mon–Fri 9am–5pm ET (agents self-guard, but confirm)
[ ] Daily spend caps set: CASHCLAW_DAILY_SPEND_CAP_USD=10, ARB_DAILY_SPEND_CAP_USD=10, POLY_DAILY_SPEND_CAP_USD=10
[ ] trading_sentinel online: pm2 status trading_sentinel → online
[ ] trades.jsonl writable: touch ~/.openclaw/trading/logs/trades.jsonl
```

### 3.3 Activation Steps

```bash
# Step 1: Start all trading agents
pm2 start cashclaw_director cashclaw_arb polymarket-trader trading_sentinel

# Step 2: Verify status
pm2 status | grep -E "cashclaw|polymarket|sentinel"

# Step 3: Tail logs for first cycle (wait 5 minutes)
pm2 logs cashclaw_director --lines 20 --nostream
pm2 logs cashclaw_arb --lines 20 --nostream
pm2 logs polymarket-trader --lines 20 --nostream
pm2 logs trading_sentinel --lines 20 --nostream

# Step 4: Verify no immediate errors
# Expected log pattern: "cycle complete", "no trades", or a specific trade logged
```

### 3.4 Validation

| Check | Command | Expected Result |
|-------|---------|----------------|
| Director running | `pm2 status cashclaw_director` | online |
| ARB running | `pm2 status cashclaw_arb` | online |
| Polymarket running | `pm2 status polymarket-trader` | online |
| Sentinel watching | `pm2 status trading_sentinel` | online |
| Director log clean | `pm2 logs cashclaw_director --lines 5 --nostream` | No ERROR lines |
| Trade file exists | `ls -la ~/.openclaw/trading/logs/trades.jsonl` | File present |
| Spend cap respected | Check trades.jsonl for today's sum < $10 | Sum < cap |

### 3.5 Kill Switch

**Immediate pause (trading stop, sentinel stays):**

```bash
# Stop all trading agents — sentinel remains for monitoring
pm2 stop cashclaw_director cashclaw_arb polymarket-trader

# Verify stop
pm2 status | grep -E "cashclaw|polymarket"
# Expected: stopped status

# Sentinel continues monitoring open positions
pm2 status trading_sentinel  # should remain: online
```

**Full trading shutdown (including sentinel):**

```bash
pm2 stop cashclaw_director cashclaw_arb polymarket-trader trading_sentinel
```

**Emergency spend cap override:**

```bash
# If agents still running despite cap breach, force stop immediately
pm2 stop cashclaw_director cashclaw_arb polymarket-trader
# Then notify Nathan via Telegram with balance snapshot
```

### 3.6 Restart After Kill

```bash
# Verify balance before restart
# Verify no open positions at risk
# Confirm cap not already reached today

pm2 start cashclaw_director
pm2 start cashclaw_arb
pm2 start polymarket-trader
# Sentinel restarts automatically or:
pm2 start trading_sentinel
```

---

## 4. ENABLE BLCO

### 4.1 Overview

Bonny Light Crude Oil wholesale brokerage. 192 leads staged in leads.jsonl. All outreach is draft-first — no emails sent without Nathan approval.

**Current status:** ⏸️ PAUSED — awaiting Nathan resume signal  
**Lead pipeline:** 192 leads staged (Europe 27, Asia 28, Americas 19, MENA 15, Global traders 11, unknown 89)  
**Outreach gate:** DRAFT-FIRST enforced. All emails go to approval queue before send.

### 4.2 Prerequisites Checklist

```
[ ] Nathan provides explicit resume signal: "Resume BLCO"
[ ] Lead list exists: ls ~/.openclaw/blco/leads.jsonl (192 leads expected)
[ ] Outreach template reviewed and approved by Nathan
[ ] BLCO_COMMAND.md updated with current strategy
[ ] Hunter.io / Apollo API keys valid (for enrichment)
[ ] Email dispatch configured: GMAIL_APP_PASSWORD or AgentMail
[ ] Draft-first gate confirmed active in b2b_outreach agent config
[ ] sovereign_proxy operational: approvals.jsonl writable
```

### 4.3 Activation Steps

```bash
# Step 1: Verify lead file
wc -l ~/.openclaw/blco/leads.jsonl
head -3 ~/.openclaw/blco/leads.jsonl | python3 -m json.tool

# Step 2: Review BLCO command
cat ~/.openclaw/blco/BLCO_COMMAND.md

# Step 3: Start enricher (if exists, else Alusi builds it)
pm2 start blco-enricher --name blco-enricher
# OR for b2b_outreach existing agent:
# Confirm it is in draft-only mode
pm2 start b2b_outreach

# Step 4: Monitor first 10 leads processed
pm2 logs blco-enricher --lines 20 --nostream
```

### 4.4 Validation

| Check | Expected |
|-------|---------|
| Enricher running | pm2 status blco-enricher → online |
| No emails sent without approval | Check approval queue: ~/.openclaw/vault/approvals/ |
| Draft gate active | First draft goes to approval queue, not inbox |
| Leads being processed | blco-enricher logs show lead processing |

### 4.5 Kill Switch

```bash
pm2 stop blco-enricher b2b_outreach
# Verify no pending outreach in queue
```

### 4.6 Resume Signal Template

Nathan should send one of:
- Telegram: "Resume BLCO outreach"
- OpenClaw chat: "Enable BLCO"
- This triggers: Alusi runs the activation checklist, confirms prerequisites, starts enricher.

---

## 5. ENABLE ADAI

### 5.1 Overview

AI-native digital products and SaaS. ADAI Inc is in development phase. No agents built yet.

**Current status:** 🔴 PRE_LAUNCH — product specs being developed

### 5.2 Prerequisites Checklist (for future activation)

```
[ ] Product specs approved by Nathan
[ ] ADAI INC registered as legal entity
[ ] Payment processor configured (Stripe, etc.)
[ ] Product landing page deployed
[ ] Initial product built and tested
[ ] Customer acquisition pipeline designed
[ ] Pricing model approved
[ ] Nathan explicit "Launch ADAI" signal
```

### 5.3 Current Development Tasks

1. Define product MVP (what AI-native product does ADAI sell?)
2. Create product specification document
3. Build prototype
4. Configure payment processing
5. Create landing page
6. Define agent architecture for ADAI operations

### 5.4 Services to Build

| Service | Purpose | Status |
|---------|---------|--------|
| adai-product-server | Serves ADAI product | NOT BUILT |
| adai-payment-handler | Processes payments | NOT BUILT |
| adai-customer-agent | Customer onboarding | NOT BUILT |

### 5.5 Activation Command (Future)

```bash
# Once built:
pm2 start adai-product-server adai-payment-handler adai-customer-agent
```

---

## 6. ENABLE CONTENT

### 6.1 Overview

Hyrvea-powered content pipeline. Currently active with hyrvea-monitor running.

**Current status:** ✅ ACTIVE  
**Active services:** hyrvea-monitor (PM2 ID 10)

### 6.2 Prerequisites Checklist

```
[ ] HYRVEA_API_KEY valid: check hyrvea-monitor logs for auth success
[ ] Content pipeline configured in Hyrvea dashboard
[ ] Output directories exist
[ ] hyrvea-monitor online: pm2 status hyrvea-monitor → online
```

### 6.3 Activation Steps (if monitor goes down)

```bash
# Restart Hyrvea monitor
pm2 restart hyrvea-monitor

# Verify
pm2 status hyrvea-monitor
pm2 logs hyrvea-monitor --lines 10 --nostream
```

### 6.4 Validation

| Check | Expected |
|-------|---------|
| Monitor running | pm2 status hyrvea-monitor → online |
| API authenticated | Logs show no auth errors |
| Content processing | Logs show pipeline activity |

### 6.5 Kill Switch

```bash
pm2 stop hyrvea-monitor
```

### 6.6 Content Expansion (Future)

To activate additional content capabilities:

| Capability | Prerequisite | Service |
|-----------|-------------|---------|
| HeyGen video | HEYGEN_API_KEY valid | heygen-generator (to build) |
| ElevenLabs TTS | ELEVENLABS_API_KEY valid | elevenlabs-tts (to build) |
| Social publishing | Social API keys | content-publisher (to build) |

---

## 7. ENABLE INFRASTRUCTURE (Core — Always-On)

### 7.1 Overview

Core infrastructure that supports all other capabilities. Always-on. Never intentionally stopped.

**Current status:** ✅ ACTIVE (all core services running)

### 7.2 Core Services (Always-On)

| Service | PM2 ID | Purpose | If Down |
|---------|--------|---------|---------|
| executor | 0 | Core task executor | CRITICAL — restart immediately |
| alusi-gateway | 2 | OpenClaw gateway | CRITICAL — restart immediately |
| heartbeat | 1 | Alusi loop heartbeat | HIGH — restart immediately |
| clawdb | 43 | PostgreSQL database | CRITICAL — restart immediately |
| exec-gateway | 13 | Exec approval gateway | HIGH — restart immediately |
| telegram-approvals | 14 | Telegram approval handler | HIGH — restart immediately |
| alusi-controlled-worker | 5 | Approval worker | HIGH |
| alusi-orchestrator | 6 | Multi-agent orchestration | MEDIUM |
| alusi-telegram-adapter | 3 | Telegram channel | HIGH |
| alusi-discord-adapter | 4 | Discord channel | MEDIUM |
| ecosystem.email-dispatcher | 15 | Ecosystem email layer | MEDIUM |
| ollama | 24 | Local LLM | MEDIUM |
| mission-control | 17 | Dashboard (port 3333) | LOW |

### 7.3 Core Restart Procedure

```bash
# Emergency restart — restore all core services
pm2 restart executor heartbeat alusi-gateway alusi-telegram-adapter \
    alusi-discord-adapter alusi-controlled-worker alusi-orchestrator \
    exec-gateway telegram-approvals ecosystem.email-dispatcher clawdb \
    ollama mission-control

# Verify
pm2 status
```

### 7.4 Full System Bootstrap (from scratch)

```bash
# Load environment
source ~/.openclaw/secrets/.env

# Start in dependency order
pm2 start clawdb                    # Database first
sleep 3
pm2 start executor heartbeat        # Core processes
pm2 start alusi-gateway             # Gateway
pm2 start alusi-telegram-adapter alusi-discord-adapter  # Channels
pm2 start alusi-controlled-worker alusi-orchestrator    # Workers
pm2 start exec-gateway telegram-approvals               # Approval chain
pm2 start ecosystem.email-dispatcher ollama             # Supporting
pm2 start mission-control                               # UI last

# Verify all online
pm2 status
```

### 7.5 Kill Switch (Full System Shutdown)

```bash
# CAUTION: This stops all operations
pm2 stop all
# Or:
pm2 kill  # Also removes PM2 daemon (requires full bootstrap to restart)
```

---

## 8. ENABLE EMAIL (On-Demand)

### 8.1 Overview

Email dispatch is on-demand only. Requires Nathan approval before any email is sent.

**Current status:** ⏸️ ON_DEMAND — email-dispatcher PM2 stopped

### 8.2 Activation (Nathan-triggered)

```bash
# Start dispatcher for a specific dispatch run
pm2 start email-dispatcher

# Monitor dispatch
pm2 logs email-dispatcher --lines 20

# Stop after dispatch complete
pm2 stop email-dispatcher
```

### 8.3 Prerequisites

```
[ ] Nathan has approved specific emails to send
[ ] Approval logged in approvals.jsonl
[ ] GMAIL_APP_PASSWORD or AgentMail credentials valid
[ ] Email content reviewed and approved
```

---

## 9. Capability Status Dashboard

| Capability | Status | Last Activated | Kill Switch |
|-----------|--------|----------------|------------|
| TRADING | ✅ ACTIVE | 2026-08-02 (restarted) | `pm2 stop cashclaw_director cashclaw_arb polymarket-trader` |
| BLCO | ⏸️ PAUSED | 2026-07-19 (paused) | Already stopped |
| ADAI | 🔴 PRE_LAUNCH | Never | N/A |
| CONTENT | ✅ ACTIVE | Active | `pm2 stop hyrvea-monitor` |
| INFRASTRUCTURE | ✅ ACTIVE | Always-on | `pm2 stop all` (nuclear) |
| EMAIL | ⏸️ ON_DEMAND | On-demand | `pm2 stop email-dispatcher` |

---

## 10. References

- AGENTS.md — PM2 process registry
- Open Empire Constitution v2
- Governance Baseline v1.0.0 — commit 17df0ff
- BLCO_COMMAND.md — BLCO strategy
- Observability Spec (Enhancement #2) — health checks for each capability
- Spend Governance — daily cap enforcement
