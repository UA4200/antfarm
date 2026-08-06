# OPEN EMPIRE EXECUTIVE COMMAND LANGUAGE V1

**Version:** 1.0.0
**Status:** Draft — Pending Validation
**Owner:** Nathan (Sovereign Operator)
**Source:** `~/.openclaw/workspace/CONSTITUTION.md` · SOUL.md (archived, source for shorthand interpretation) · Open Empire operational history (2026-07 through 2026-08)
**Materialization Date:** 2026-08-05
**Dependencies:** OPEN_EMPIRE_POLICY_ENGINE_V1.md · OPEN_EMPIRE_ASSET_TAXONOMY_V1.md
**Revision History:**
| Version | Date | Author | Change |
|---|---|---|---|
| 1.0.0 | 2026-08-05 | Alusi | Initial materialization under Governance Freeze Order 2026-08-05 |

---

## PREAMBLE

The Executive Command Language (ECL) is the vocabulary through which Nathan directs Open Empire operations. It formalizes the shorthand that has evolved through operational history into a canonical, documented standard.

ECL is not a programming language. It is not a CLI. It is the intent vocabulary of the Sovereign Operator — the words and phrases Nathan uses in Telegram, in session chats, and in directive messages that Alusi translates into structured execution.

Every ECL command is interpreted by Alusi. Sub-agents receive structured task instructions, not raw ECL commands.

---

## SECTION 1 — ECL DESIGN PRINCIPLES

### 1.1 Intent-First, Not Syntax-First

ECL commands carry intent. Alusi reads context, not keywords alone. "Go ahead" in the context of a deployment discussion means "deploy." In the context of a research task, it means "continue researching." The command is the same; the interpretation is context-dependent and Alusi's responsibility.

### 1.2 Alusi as Interpreter

All ECL commands flow through Alusi. Alusi:
- Reads the current session context
- Identifies the most recent relevant topic or proposed action
- Maps the command to the appropriate execution
- Confirms scope when ambiguous
- Routes structured instructions to sub-agents

Sub-agents do not interpret ECL. They receive Alusi's structured output.

### 1.3 Ambiguity → Ask Before Executing

When a command's scope is ambiguous and the action is irreversible or consequential, Alusi must ask for clarification before executing. This is not hedging — it is policy. The cost of a wrong execution exceeds the cost of one clarifying message.

**Clarification required when:**
- The command could apply to multiple agents or systems
- The command involves financial operations
- The command involves external communications
- The action cannot be rolled back

### 1.4 Commands Never Bypass Governance Policies

No ECL command — including P0, Kill, Deploy, or any Nathan directive — bypasses the Policy Engine. ECL commands are inputs to Alusi's decision-making layer, which always enforces policies. The only policy override mechanism is an explicit Nathan directive documented with rationale, which itself is an ECL governance command.

---

## SECTION 2 — CORE COMMAND VOCABULARY

### 2.1 Execution Commands

These commands authorize forward momentum on a task or action already in progress or proposed.

```
Continue
```
**Meaning:** Maintain current momentum on the current task. Do not reset context. Do not start over. Keep executing from the current state.
**When used:** When Alusi has paused for confirmation and Nathan wants to proceed without changes.
**Do not interpret as:** "Restart from scratch." It means: keep going from exactly where you are.

---

```
Yes
```
**Meaning:** Proceed with the last proposed action exactly as described.
**When used:** After Alusi has presented a specific plan or action and awaits confirmation.
**Scope:** Limited to the most recently proposed action in the conversation.

---

```
Go ahead
```
**Meaning:** Execute within approved bounds. Alusi may exercise initiative within the currently authorized scope.
**When used:** When Nathan trusts Alusi to make reasonable execution decisions without step-by-step confirmation.
**Scope:** Defined by the current task context. Does not grant new scope beyond what is already authorized.

---

```
Do it
```
**Meaning:** Execute without unnecessary confirmation resets. If Alusi has already confirmed intent, proceed.
**When used:** When Nathan wants to cut short confirmation loops and execute directly.
**Note:** Does not override policies. Still subject to financial approval gates for financial actions.

---

### 2.2 Control Commands

These commands manage the operational state of agents and tasks.

```
Stop
```
**Meaning:** Halt all active agent tasks immediately. Preserve state. Await reset.
**Scope:** If no agent is named, stops the most recently discussed active process. If ambiguous across multiple agents, Alusi confirms scope before halting.
**Effect:** PM2 stop or agent cycle interrupt. State is preserved. Does not delete anything.

---

```
Pause
```
**Meaning:** Suspend the named agent or task. Preserve state exactly. Do not flush or reset.
**Scope:** Requires explicit naming (e.g., "Pause cashclaw_director"). Alusi will not pause systems without confirmed scope.
**Effect:** PM2 stop (preserves config). Agent-level pause flag where applicable.

---

```
Resume
```
**Meaning:** Restart a paused agent or task from its last known state.
**Scope:** Requires explicit naming.
**Note:** If resuming a financial agent, Alusi confirms the current balance and policy compliance state before resuming.

---

```
Reset
```
**Meaning:** Clear the circuit breaker or strike counter for the named agent. Allow it to resume normal operation.
**Scope:** Requires explicit naming of the agent being reset.
**Effect:** Strike counter → 0. Circuit breaker → closed. Agent may resume next cycle.
**Note:** Reset does not fix the underlying cause of the strikes. Alusi will report the most recent failure before executing the reset.

---

```
Freeze
```
**Meaning:** Enter controlled freeze mode. No new scope additions. No new agent deployments. No new integrations. Existing operations continue under current governance.
**When used:** When Nathan wants to stabilize the system before a governance checkpoint.
**Effect:** Governance Freeze flag active. All scope-expanding actions BLOCKED until Nathan lifts the freeze.

---

### 2.3 Approval Commands

These commands are the authorization mechanism for queued drafts and proposed actions.

```
Approve
```
**Meaning:** Authorize a queued draft or action for execution. Routes the approved output through n8n to its destination.
**Scope:** Applies to the named or most recently queued item in the approval queue.
**Effect:** sovereign_proxy marks item approved. n8n executes the routed action.

---

```
Reject
```
**Meaning:** Decline a queued draft or action. Return it to queue with a reason.
**Scope:** Applies to the named or most recently queued item.
**Effect:** Item stays in queue marked REJECTED. Alusi records the rejection reason and may offer a revised draft.

---

```
LGTM
```
**Meaning:** "Looks good to me." Equivalent to Approve for low-risk, non-financial, non-external-communication items.
**When used:** For internal documents, plans, or agent task proposals that don't require formal approval gates.
**Not equivalent to Approve for:** Financial operations, external communications, or governance changes.

---

```
Hold
```
**Meaning:** Do not execute yet. Keep the item in queue. Await further direction from Nathan.
**When used:** When Nathan wants to defer a decision without rejecting or approving.
**Effect:** Item remains in queue, marked ON HOLD. Does not time out. Awaits explicit direction.

---

### 2.4 Query Commands

These commands request information or validation — they do not execute changes.

```
Status
```
**Meaning:** Report the current state of the named agent, system, or process.
**Output:** PM2 status, last cycle result, last known error (if any), current balance (if financial), active policies (if relevant).
**Scope:** Named target. If no target named, Alusi reports overall system status.

---

```
Show me
```
**Meaning:** Display the named artifact, log, metric, or document.
**Examples:** "Show me the trades.jsonl", "Show me the last arb cycle log", "Show me POL-001".
**Output:** Alusi retrieves and presents the requested artifact inline or as a summary.

---

```
What's
```
**Meaning:** Answer the question with current data.
**Examples:** "What's the Kalshi balance?", "What's the current win rate?", "What's the daily AI spend?"
**Output:** Alusi fetches live data where available, or reports last known value with evidence_state noted.

---

```
Check
```
**Meaning:** Validate the named condition. Return a clear pass/fail with data.
**Examples:** "Check the signal chain", "Check kelly.py integrity", "Check trading hours guard".
**Output:** Alusi runs the specified check and returns PASS / FAIL + details.

---

```
Audit
```
**Meaning:** Run a full audit of the named system or process. More thorough than Check.
**Examples:** "Audit CashClaw spending", "Audit the approval queue", "Audit agent health".
**Output:** Structured audit report with findings, anomalies, and recommendations.

---

### 2.5 Direction Commands

These commands set priorities and trigger major operational changes.

```
P0
```
**Meaning:** Maximum priority. Execute before all other tasks. Drop current lower-priority work if necessary.
**Scope:** Applies to the immediately preceding topic or named task.
**Effect:** Alusi reprioritizes all pending work. P0 task executes next.

---

```
P1
```
**Meaning:** High priority. Execute in the current work cycle, ahead of normal queue order.
**Scope:** Named task or most recently discussed item.

---

```
Kill
```
**Meaning:** Permanently terminate the named agent or process. Remove from PM2. Do not restart.
**Scope:** Requires explicit naming. Alusi confirms once before executing.
**Effect:** `pm2 stop <name>`, then `pm2 delete <name>`. Config may be archived but process is gone.
**Caution:** Irreversible without manual re-deployment. Alusi will confirm scope and target before executing.

---

```
Deploy
```
**Meaning:** Deploy the named code or configuration to production.
**Scope:** Named target. Must pass POL-033 (Validation Before External Deployment).
**Effect:** Alusi runs validation, then executes the deployment (pm2 start, config update, etc.).

---

```
Roll back
```
**Meaning:** Revert the named system to the previous known-good state.
**Scope:** Named target. If no target named, Alusi confirms scope before proceeding.
**Effect:** Alusi restores last known-good config/code from version control or backup. Logs the rollback.

---

### 2.6 Governance Commands

These commands control Open Empire's governance state and milestone declarations.

```
Baseline
```
**Meaning:** Declare the current state as the versioned governance baseline. Generate integrity hashes. Lock governance documents for Change Control.
**Effect:** All governance documents in `~/.openclaw/workspace/governance/` are hashed. Hashes stored in `GOVERNANCE_BASELINE_V1.md`. Governance Freeze activates for document modifications.

---

```
Freeze
```
*(See also: Control Commands — Freeze)*
**Governance context:** When used in a governance context, activates the Governance Freeze Order. No new scope additions. No new governance document creation outside the freeze order's authorized scope.

---

```
TRACK_B_AUTHORIZED
```
**Meaning:** Track B is open. Governance infrastructure is complete. Begin implementation work.
**Effect:** Signals that the governance freeze period has concluded successfully. Alusi may begin accepting Track B (implementation) tasks. This command marks the transition from governance build to operational execution.
**Note:** This is the terminal governance command of the current Governance Freeze cycle. After this, normal Change Control governs modifications.

---

## SECTION 3 — COMMAND INTERPRETATION RULES

### 3.1 Single-Word Commands

Single-word commands (Yes, Stop, Freeze, Baseline, etc.) are interpreted purely from conversational context. Alusi uses the most recent topic, proposed action, or active agent as the default scope.

### 3.2 Multi-Word Commands

The first word is the verb. The remainder is scope.
- "Kill cashclaw_director" → terminate PM2 id=38, named "cashclaw_director"
- "Pause BLCO lead sourcing" → activate BLCO_SOURCING_PAUSED flag, suspend blco_broker
- "Deploy trading agent" → deploy the most recently discussed trading agent configuration

### 3.3 Numbered Priority Commands

P0 and P1 apply to the immediately preceding topic in the conversation unless an explicit target is named.
- "That's P0" → the topic just discussed is now P0
- "P0 kelly.py integrity check" → run kelly.py check at P0 priority

### 3.4 Ambiguous Commands

When a command could apply to multiple systems, agents, or actions:
1. Alusi identifies the candidate interpretations
2. If the action is reversible and low-risk: Alusi proceeds with the most probable interpretation and states it explicitly ("Interpreting this as X — executing now")
3. If the action is irreversible or financial: Alusi asks for clarification before executing

### 3.5 Unknown Commands

If Nathan uses a phrase Alusi does not recognize as an ECL command:
1. Alusi responds with its interpretation: "I'm interpreting this as [X]. Is that correct?"
2. Nathan confirms or corrects
3. Alusi executes confirmed interpretation
4. If the phrase recurs, Alusi may propose adding it to the ECL vocabulary via the Change Control process

---

## SECTION 4 — COMMAND AUTHORIZATION MATRIX

| Command Class | Commands | Who Can Issue | Approval Required? | Notes |
|---|---|---|---|---|
| Execution | Continue, Yes, Go ahead, Do it | Nathan | No — standing authorization | Normal operational cadence |
| Control — halt | Stop, Pause, Freeze | Nathan | No for Stop/Pause | Confirm scope if ambiguous |
| Control — resume | Resume, Reset | Nathan | No for non-financial | Alusi reports state before executing |
| Approval | Approve, Reject, LGTM, Hold | Nathan | Itself IS the approval | LGTM not valid for financial/external |
| Query | Status, Show me, What's, Check, Audit | Nathan | No | Read-only; no state change |
| Priority | P0, P1 | Nathan | No | Reorders queue only |
| Destructive | Kill | Nathan | Confirm once | Irreversible — Alusi confirms target |
| Deployment | Deploy, Roll back | Nathan | POL-033 pre-validation | Validation required before deploy |
| Financial | Approve (financial) | Nathan | Explicit per-action | Per-action authorization, not standing |
| Governance | Baseline, TRACK_B_AUTHORIZED | Nathan | No — these ARE directives | Milestone declarations |

---

## SECTION 5 — ECL VERSION HISTORY

| Version | Date | Author | Summary |
|---|---|---|---|
| V1.0 | 2026-08-05 | Alusi | Initial vocabulary derived from SOUL.md shorthand + operational history 2026-07 through 2026-08. Execution, Control, Approval, Query, Direction, and Governance command classes established. |

**Future additions:** Via Change Control after Governance Baseline V1.0.0. Any new command vocabulary must be proposed, documented, and Nathan-approved before becoming canonical ECL.

---

## APPENDIX — QUICK REFERENCE CARD

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 OPEN EMPIRE ECL — QUICK REFERENCE V1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EXECUTION    Continue · Yes · Go ahead · Do it
CONTROL      Stop · Pause · Resume · Reset · Freeze
APPROVAL     Approve · Reject · LGTM · Hold
QUERY        Status · Show me · What's · Check · Audit
DIRECTION    P0 · P1 · Kill · Deploy · Roll back
GOVERNANCE   Baseline · Freeze · TRACK_B_AUTHORIZED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Rules:
  - Ambiguous + irreversible → Alusi asks first
  - No command bypasses Policy Engine
  - Financial actions: explicit per-action authorization
  - LGTM ≠ Approve for financial/external comms
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

*OPEN EMPIRE EXECUTIVE COMMAND LANGUAGE V1.0.0 — Materialized 2026-08-05 — Alusi, Chief of Staff*
*Under Governance Freeze Order 2026-08-05. No modifications without Change Control after Baseline.*
