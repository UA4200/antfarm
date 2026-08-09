# PROJECTS.md - Project Registry and Council Queue
Version: 2.1

## Council Queue Rules
1. Evaluate READY items every cycle
2. PASS all criteria -> submit to council with task_id
3. sovereign_proxy approval required - no exceptions
4. All outputs DRAFT-ONLY
5. Approved outputs -> n8n -> external delivery

## VENTURE 1: Moltlaunch (P0 - INSTALLING)
CashClaw Director is first agent - finds + executes Kalshi jobs.

| ID | Use Case | Status |
|---|---|---|
| ML-01 | Install Moltlaunch | ACTIVE |
| ML-02 | CashClaw Director running | ACTIVE |
| ML-03 | Fix signal engine CC-01 | READY |
| ML-04 | First live trade | BLOCKED |
| ML-05 | n8n trade alert | READY |

## VENTURE 2: CashClaw (P0 - DEGRADED)
$25 capital | 70%+ win rate target | Q4 Polymarket

| ID | Use Case | Status |
|---|---|---|
| CC-01 | Fix signal engine | READY - P0 |
| CC-02 | Market scanning | BLOCKED CC-01 |
| CC-03 | Kelly execution | BLOCKED CC-01 |
| CC-04 | Win/loss logging | BLOCKED CC-01 |

## VENTURE 3: BLCO (P1 - ACTIVE)
Output: leads.jsonl -> n8n (active) -> Airtable

| ID | Use Case | Status |
|---|---|---|
| BL-01 | Signal scan 6hr | READY |
| BL-02 | Contact finder | READY |
| BL-03 | Draft outreach | READY |
| BL-04 | n8n -> Airtable | READY |
| BL-05 | Telegram summary 9am | READY |

## VENTURE 4: ADAI INC (P1 - ACTIVE)
Services: Discovery/Single Agent/Council/Retainer

| ID | Use Case | Status |
|---|---|---|
| AD-01 | B2B lead list 100 SMBs | READY |
| AD-02 | LinkedIn templates x3 | READY |
| AD-03 | Email nurture 5-touch | READY |
| AD-04 | n8n -> Airtable CRM | READY |
