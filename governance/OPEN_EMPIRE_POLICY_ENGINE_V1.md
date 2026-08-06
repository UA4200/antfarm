# OPEN EMPIRE POLICY ENGINE V1

**Version:** 1.0.0
**Status:** Draft — Pending Validation
**Owner:** Nathan (Sovereign Operator)
**Source:** `~/.openclaw/workspace/CONSTITUTION.md` · `~/.openclaw/workspace/governance/OPEN_EMPIRE_ASSET_TAXONOMY_V1.md` · AGENTS.md operational context
**Materialization Date:** 2026-08-05
**Dependencies:** OPEN_EMPIRE_ASSET_TAXONOMY_V1.md · CONSTITUTION.md
**Revision History:**
| Version | Date | Author | Change |
|---|---|---|---|
| 1.0.0 | 2026-08-05 | Alusi | Initial materialization under Governance Freeze Order 2026-08-05 |

---

## PREAMBLE

The Policy Engine is the enforcement backbone of Open Empire. It formalizes all governance rules into machine-readable, auditable, enforceable policies. Every agent, service, and human operator in Open Empire is bound by these policies.

Policies are not suggestions. They are behavioral constraints that pre-empt unauthorized action, audit completed actions, and halt runaway processes. A policy violation is a governance event requiring logging, alerting, and resolution.

This document is the canonical source for all policy IDs. Downstream documents referencing policies must cite the `POL-NNN` identifiers defined here.

---

## SECTION 1 — POLICY ENGINE ARCHITECTURE

### 1.1 What Is the Policy Engine?

The Policy Engine is a registry of enforceable rules governing:
- **Agent behavior** — what agents may and may not do autonomously
- **Asset state transitions** — what lifecycle changes require approval
- **Spending** — financial caps, per-trade limits, AI cost governance
- **External communications** — draft-first, approval-gated dispatch
- **Security** — model access, secret handling, scope boundaries

The Policy Engine is not a running service. It is a canonical governance document whose rules must be implemented in code (env vars, agent logic, circuit breakers) and audited regularly.

### 1.2 Enforcement Mechanisms

Policies are enforced via three classes of mechanism:

| Mechanism | When It Fires | Effect |
|---|---|---|
| **Pre-action gate** | Before an action is executed | BLOCK or WARN before execution; prevents the action if severity = BLOCK |
| **Post-action audit** | After an action completes | Records compliance or violation; does not prevent but does escalate |
| **Circuit breaker** | On repeated failure or threshold breach | Halts the agent/process; requires human reset to resume |

### 1.3 Policy Authority

- **Creation/modification:** Nathan only, via Change Control after Governance Baseline V1.0.0
- **Interpretation disputes:** Alusi (Chief of Staff) interprets; Nathan is the final arbiter
- **Emergency overrides:** Nathan explicit directive only, documented post-hoc

---

## SECTION 2 — POLICY REGISTRY FORMAT

Each policy entry follows this canonical structure:

```
## POL-NNN: <Policy Name>
**Category:** Spending | Execution | Communication | Security | Governance
**Severity:** BLOCK | WARN | AUDIT
**Scope:** [which agents/asset types this applies to]
**Trigger:** [what action triggers this policy check]
**Rule:** [the enforceable rule in clear language]
**Implementation:** [how to implement — env var, code check, config flag]
**Override:** [can it be overridden? by whom?]
```

**Severity definitions:**
- **BLOCK** — Action must not proceed. Log violation. Telegram alert. Await reset/override.
- **WARN** — Action may proceed. Log warning. Telegram alert. No halt.
- **AUDIT** — Action proceeds. Logged for compliance review. No immediate alert.

---

## SECTION 3 — POLICY REGISTRY

---

### SPENDING POLICIES

---

## POL-001: Daily Spend Cap Enforcement

**Category:** Spending
**Severity:** BLOCK
**Scope:** All trading agents (cashclaw_director, cashclaw_arb, polymarket_trader)
**Trigger:** Before any trade placement — at the start of each agent cycle
**Rule:** Sum of placed `size_usd` in `trades.jsonl` over the last 24 rolling hours must be strictly less than the `daily_spend_cap_usd` environment variable for that agent. If the sum equals or exceeds the cap, the trade is BLOCKED. A Telegram alert is fired and the violation is logged.
**Implementation:**
- `cashclaw_director`: `CASHCLAW_DAILY_SPEND_CAP_USD=10`
- `cashclaw_arb`: `ARB_DAILY_SPEND_CAP_USD=10`
- `polymarket_trader`: `POLY_DAILY_SPEND_CAP_USD=10`
- Check implemented at cycle start in each agent's `run.py`. Sum trades.jsonl entries with `timestamp > now - 86400s` and `status = placed`.
**Override:** Nathan directive via Telegram approval only. Override must be logged with directive text and timestamp.

---

## POL-002: Per-Trade Hard Cap

**Category:** Spending
**Severity:** BLOCK
**Scope:** All trading agents (cashclaw_director, cashclaw_arb, polymarket_trader)
**Trigger:** Before any single trade placement
**Rule:** A single trade's `size_usd` must not exceed $5.00. Kelly-calculated position size is the normal limit and will be lower in typical operation. $5.00 is the absolute hard ceiling regardless of Kelly output. Trades above $5.00 are BLOCKED before submission.
**Implementation:** Hard cap check in `executor.py` / trade submission code. `if size_usd > 5.00: BLOCK`. Kelly NO-fix (see POL-014) means Kelly output is used as-is up to the $5 ceiling.
**Override:** Nathan directive only. Must specify the approved size and the specific trade context.

---

## POL-003: Per-Action AI Cost Soft Cap

**Category:** Spending
**Severity:** WARN (above $2) / BLOCK (above $5)
**Scope:** All agents making AI model calls
**Trigger:** After any AI model API call completes (post-action audit of estimated cost)
**Rule:**
- Any single AI action with estimated cost > $2.00 → WARN + log. Continue.
- Any single AI action with estimated cost > $5.00 → BLOCK + log + Telegram escalation. Halt that action chain.
**Implementation:** Cost estimation based on token counts × per-model rate. Log in cost tracker. Alert via Telegram at $5 threshold.
**Override:** Alusi may authorize continuation above $2 up to $5 per action. Above $5 requires Nathan only.

---

## POL-004: Daily AI Spend Tiers

**Category:** Spending
**Severity:** WARN at $10 / BLOCK at $20 / EMERGENCY BLOCK at $50
**Scope:** All agents and all AI model invocations
**Trigger:** Each AI model call; checked against rolling 24h spend accumulator
**Rule:**
- Cumulative daily AI spend > $10 → Telegram alert. Continue all models.
- Cumulative daily AI spend > $20 → BLOCK claude-sonnet-4-6 and above. Route to Haiku only.
- Cumulative daily AI spend > $50 → BLOCK all model calls system-wide. Manual Nathan reset required.
**Implementation:** Daily AI cost tracker in OpenClaw budget tracking. Environment-level cap enforcement. Daily target for autonomous ops: <$0.20.
**Override:**
- $10–$20 tier: Alusi may continue at Haiku-only routing.
- $20–$50 tier: Nathan directive required to unlock Sonnet+.
- >$50: Nathan manual reset only.

---

### EXECUTION POLICIES

---

## POL-010: Three-Strike Halt

**Category:** Execution
**Severity:** BLOCK
**Scope:** All agents and automated tasks
**Trigger:** Third consecutive failure of the same task or action
**Rule:** Any agent task or action that fails 3 consecutive times must halt entirely. The agent logs the failure sequence, fires a Telegram alert with the task name and error details, and awaits a Nathan reset command. Retrying without reset is a policy violation.
**Implementation:** Strike counter per task in agent state. On third failure: set `circuit_open=true`, log, alert, exit cycle. Counter resets on Nathan's explicit reset command.
**Override:** Nathan reset command. Command must specify the agent/task being reset.

---

## POL-011: Ten-Minute Execution Limit

**Category:** Execution
**Severity:** BLOCK
**Scope:** All agent tasks and automated operations
**Trigger:** Any task running longer than 600 seconds (10 minutes)
**Rule:** No single task may execute longer than 10 minutes. At the 10-minute mark, the task is hard-killed. The kill is logged. A Telegram alert fires with the task name, duration, and last known state.
**Implementation:** Timeout wrapper in task execution. `signal.alarm(600)` or equivalent process timeout. PM2 watch does not replace this — it must be implemented at the task level.
**Override:** Nathan directive for a specific long-running task must include an explicit timeout value greater than 10 minutes. This override is per-task, not standing.

---

## POL-012: Circuit Breaker — Zero Confidence

**Category:** Execution
**Severity:** BLOCK
**Scope:** cashclaw_director, signal engine (trading/shared/signals.py)
**Trigger:** Third consecutive cycle where signal scoring returns `p_yes=0.00`
**Rule:** If the signal engine returns `p_yes=0.00` for 3 consecutive scoring cycles, the cashclaw_director must halt. Zero confidence three times in a row indicates a broken signal chain, stale market data, or API failure — not a valid "no trade" signal. Halt, log, Telegram alert, await Nathan reset.
**Implementation:** Zero-confidence counter in director's `run.py`. Increment on each `p_yes=0.00`. Reset on any non-zero result. At 3: `circuit_open=true`, alert, exit.
**Override:** Nathan reset command. Before resetting, Nathan should verify signal chain integrity (Haiku connectivity, Ollama availability, market data freshness).

---

## POL-013: Live Balance Minimum

**Category:** Execution
**Severity:** BLOCK
**Scope:** cashclaw_director
**Trigger:** Before any trade placement
**Rule:** The live Kalshi free balance must be ≥ $5.00 before any trade is placed. If the balance is below $5.00, the trade is BLOCKED. Log the balance check result. Alert Nathan if balance has declined below this threshold.
**Implementation:** Live balance check via Kalshi V2 API at cycle start, before executor.py runs. `if free_balance < 5.00: BLOCK, log, alert`.
**Override:** Nathan directive with explicit acknowledgment of the current balance and authorization to proceed. Must document the specific balance at time of override.

---

## POL-014: Kelly NO-fix

**Category:** Execution
**Severity:** BLOCK
**Scope:** `trading/shared/kelly.py` (canonical path: `~/.openclaw/trading/trading/shared/kelly.py`)
**Trigger:** Any proposed modification to `kelly.py` — code edit, refactor, optimization, parameter change
**Rule:** `kelly.py` must not be modified by any agent, automation, or process without Nathan's explicit directive. The file is preserved verbatim as a deliberate Change Control decision (established 2026-07-31). Any modification attempt by an agent is a BLOCK-level policy violation, immediately logged and Nathan-alerted.
**Implementation:** File integrity check (hash comparison) in pre-deployment validation. If hash of `kelly.py` differs from baseline, BLOCK deployment and alert.
**Override:** Nathan explicit directive AND ADR (Architecture Decision Record) amendment documenting the change rationale. Both required before any modification proceeds.

---

## POL-015: Signal Chain Lock

**Category:** Execution
**Severity:** BLOCK
**Scope:** Signal engine (`trading/shared/signals.py`), cashclaw_director, polymarket_trader
**Trigger:** Any attempt to add, reorder, or replace models in the signal scoring chain
**Rule:** The canonical signal scoring chain is: **Haiku → Ollama → Heuristic**. This chain is locked as of 2026-08-02 (GPT-4o removal directive). GPT-4o must not be reinserted. No additional model may be added to the real-time scoring chain without Nathan's explicit directive. Chain order must not be reordered.
**Implementation:** Configuration check in signals.py at startup — validate chain matches canonical sequence. Alert if mismatch detected.
**Override:** Nathan explicit directive. Must specify the new chain configuration. Alusi must document rationale before applying.

---

### COMMUNICATION POLICIES

---

## POL-020: Draft-Only External Communication

**Category:** Communication
**Severity:** BLOCK
**Scope:** All agents — b2b_outreach, blco_broker, email-dispatcher, all external API integrations
**Trigger:** Any action that would send content to an external party (email, API POST, webhook, chat message to non-system recipients)
**Rule:** No outbound communication to external parties may execute without: (1) sovereign_proxy approval, AND (2) Nathan confirmation. All agent outputs destined for external parties are routed to the approval queue first. n8n routes only approved outputs. Unapproved direct sends are a BLOCK-level violation.
**Implementation:** All external dispatch calls must pass through the approval queue interface. Bypass of sovereign_proxy is not permitted under any circumstances. Implement as a wrapper that routes output to approval queue and blocks until approval is received.
**Override:** Nathan standing authorization for specific, named workflows only (e.g., a pre-approved weekly report template). Standing authorizations must be documented by workflow name and scope.

---

## POL-021: BLCO Lead Sourcing Pause

**Category:** Communication
**Severity:** BLOCK
**Scope:** blco_broker agent
**Trigger:** Any new BLCO lead sourcing action — scraping, list building, outreach generation
**Rule:** BLCO lead sourcing is paused as of 2026-07-19. No new outreach may be generated, queued, or sent until Nathan explicitly lifts the pause. Existing pipeline data (192 leads as of pause date) must not be acted upon without explicit Nathan reauthorization.
**Implementation:** Hard block in blco_broker cycle. Check for `BLCO_SOURCING_PAUSED=true` env var. If set, log and exit without action.
**Override:** Nathan directive: explicit statement that BLCO lead sourcing is resumed. Must include scope (full resume or limited scope) and any updated outreach constraints.

---

### GOVERNANCE POLICIES

---

## POL-030: Change Control After Baseline

**Category:** Governance
**Severity:** BLOCK
**Scope:** All governance documents in `~/.openclaw/workspace/governance/`
**Trigger:** Any direct edit to a governance document after Governance Baseline V1.0.0 is declared
**Rule:** After the Governance Baseline V1.0.0 release, no governance document may be directly edited. All changes must proceed via the Change Control process: propose change, document rationale, Nathan approves, Alusi applies, version increment. Emergency amendments require Nathan directive AND post-hoc ratification via formal Change Control.
**Implementation:** Governance documents are version-controlled (git). Unauthorized direct edits detected via diff from baseline hash. Alert Nathan.
**Override:** None for the process requirement. Emergency amendments must be post-hoc ratified within 48 hours of Nathan's directive.

---

## POL-031: No Scope Expansion

**Category:** Governance
**Severity:** BLOCK
**Scope:** All agents
**Trigger:** Any agent action that extends beyond its documented scope (as defined in AGENTS.md or its OEPM manifest)
**Rule:** No agent may expand its scope of operation beyond its authorized task definition without Nathan's explicit directive. Scope expansion includes: accessing systems not in its manifest dependencies, initiating new outreach channels, creating new PM2 processes, spawning new agents, or taking financial actions not in its authorized strategy.
**Implementation:** OEPM manifest defines authorized scope for each agent. Agents must validate actions against manifest before executing. Out-of-scope action → BLOCK + log + alert.
**Override:** Nathan directive. Must specify the new scope being authorized and the duration (permanent or time-limited).

---

## POL-032: No Opus Except Alusi

**Category:** Governance
**Severity:** BLOCK
**Scope:** All agents except Alusi (main agent)
**Trigger:** Any agent invoking `claude-opus`, `claude-opus-4`, or equivalent high-cost flagship model
**Rule:** No agent may invoke Opus-class or equivalent flagship models directly. Only Alusi (the main OpenClaw agent) may invoke Opus-class models — and only when the task genuinely requires it and cost justification is documented. All other agents are restricted to Haiku, local Ollama models, and Heuristic fallback.
**Implementation:** Model dispatch validation in each sub-agent's initialization. Reject model calls to Opus-class models from non-Alusi sessions. Log attempt and alert Nathan.
**Override:** Nathan directive via Alusi escalation only. Nathan must authorize the specific use case.

---

## POL-033: Validation Before External Deployment

**Category:** Governance
**Severity:** BLOCK
**Scope:** All code deployments to production (PM2 processes, cron jobs, configuration changes)
**Trigger:** Any deployment action — `pm2 start`, `pm2 restart` with new config, crontab changes, config file changes to production paths
**Rule:** Any code deployed to production must pass a validation check before activation. Validation minimally includes: syntax check, import check, env var presence check, and baseline hash verification for locked files (kelly.py). Failed validation → BLOCK deployment, log, alert Nathan.
**Implementation:** Pre-deployment validation script invoked before any pm2 ecosystem change. Validation results logged. Only after pass: deploy proceeds.
**Override:** Nathan explicit approval with documented risk acceptance. Must specify what validation step was bypassed and why.

---

## SECTION 4 — POLICY ENFORCEMENT MATRIX

| Agent | Applied Policies |
|---|---|
| cashclaw_director | POL-001, POL-002, POL-010, POL-011, POL-012, POL-013, POL-014, POL-015, POL-031, POL-032 |
| cashclaw_arb | POL-001, POL-002, POL-010, POL-011, POL-031 |
| polymarket_trader | POL-001, POL-002, POL-010, POL-011, POL-015, POL-031 |
| trading_sentinel | POL-010, POL-011, POL-031 |
| blco_broker | POL-020, POL-021, POL-031 |
| b2b_outreach | POL-020, POL-031 |
| email-dispatcher | POL-020, POL-031 |
| executor (PM2 id=0) | POL-010, POL-011, POL-031, POL-033 |
| open-empire-federation-staging | POL-010, POL-011, POL-031 |
| open-empire-lifecycle-staging | POL-010, POL-011, POL-031 |
| alusi (main agent) | ALL POLICIES (enforcer role — Alusi is the policy enforcement layer for all other agents) |

---

## SECTION 5 — POLICY AUDIT LOG REQUIREMENTS

Every policy trigger — BLOCK, WARN, or AUDIT — must produce a log entry with the following mandatory fields:

```json
{
  "timestamp": "<iso8601>",
  "agent": "<agent_name>",
  "pm2_id": "<number or null>",
  "policy_id": "<POL-NNN>",
  "action_attempted": "<description of the action that triggered the policy>",
  "outcome": "BLOCK | WARN | PASS | OVERRIDE",
  "details": "<additional context — values, thresholds, balances>",
  "override_authority": "<null | 'Alusi' | 'Nathan'>",
  "override_directive": "<null | directive text if overridden>"
}
```

**Log destination:** `~/.openclaw/logs/policy_audit.jsonl` (append-only, immutable per POL on trade logs)
**Alert threshold:** BLOCK outcomes → Telegram alert within 60 seconds
**Retention:** Policy audit logs are immutable records. No deletion without P0 Nathan approval.
**Review cadence:** TODO_PENDING_APPROVAL (governance review cadence to be defined by Nathan)

---

## APPENDIX — POLICY INDEX

| Policy ID | Name | Category | Severity |
|---|---|---|---|
| POL-001 | Daily Spend Cap Enforcement | Spending | BLOCK |
| POL-002 | Per-Trade Hard Cap | Spending | BLOCK |
| POL-003 | Per-Action AI Cost Soft Cap | Spending | WARN / BLOCK |
| POL-004 | Daily AI Spend Tiers | Spending | WARN / BLOCK / EMERGENCY |
| POL-010 | Three-Strike Halt | Execution | BLOCK |
| POL-011 | Ten-Minute Execution Limit | Execution | BLOCK |
| POL-012 | Circuit Breaker — Zero Confidence | Execution | BLOCK |
| POL-013 | Live Balance Minimum | Execution | BLOCK |
| POL-014 | Kelly NO-fix | Execution | BLOCK |
| POL-015 | Signal Chain Lock | Execution | BLOCK |
| POL-020 | Draft-Only External Communication | Communication | BLOCK |
| POL-021 | BLCO Lead Sourcing Pause | Communication | BLOCK |
| POL-030 | Change Control After Baseline | Governance | BLOCK |
| POL-031 | No Scope Expansion | Governance | BLOCK |
| POL-032 | No Opus Except Alusi | Governance | BLOCK |
| POL-033 | Validation Before External Deployment | Governance | BLOCK |

---

*OPEN EMPIRE POLICY ENGINE V1.0.0 — Materialized 2026-08-05 — Alusi, Chief of Staff*
*Under Governance Freeze Order 2026-08-05. No modifications without Change Control after Baseline.*
