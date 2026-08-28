# Task Observer Integration Report — P0.15
**Date:** 2026-08-09 | **Verdict:** INTEGRATE WITH GUARDRAILS

---

## Integration Design

Task Observer slots into the existing skill_workshop workflow as an observation feeder — it does NOT bypass or replace it.

```
TASK EXECUTION
     ↓
OUTCOME (success/fail/friction/pattern)
     ↓
~/.openclaw/workspace/skill-observations/
     [YYYY-MM-DD-{task_type}.jsonl]
     ↓
task_observer_collector.py
     ↓
PATTERN DETECTED?
     ↓
skill_workshop proposal (PROPOSAL status — never auto-applied)
     ↓
PMO / Nathan review
     ↓
APPROVED → skill_workshop apply
```

---

## What It Captures (auto-allowed)

- Agent task failures and error patterns
- Repeated friction points (same error >2 times in 7 days)
- Successful patterns worth encoding as skills
- Missing skill gaps (agent attempted undefined task type)
- Instruction quality signals (vague instruction → poor output)

## What It CANNOT Touch (hard blocks)

| Domain | Block Type |
|---|---|
| CONSTITUTION.md | READ-ONLY — no proposals |
| AGENTS.md governance rows | READ-ONLY |
| Kelly criterion logic | READ-ONLY |
| Approval gate logic | READ-ONLY |
| CashClaw trading logic | READ-ONLY + flagged CASHCLAW_PROTECTED |
| Security policy | READ-ONLY |
| Production deployment policy | READ-ONLY |
| Secret management | READ-ONLY |

Any observation touching these domains is tagged `GOVERNANCE_DOMAIN — HUMAN_ONLY` and routed to the exception register, never to skill_workshop automatically.

---

## Implementation

### 1. Observation directory
```bash
mkdir -p ~/.openclaw/workspace/skill-observations
```

### 2. Observer schema (one line per observation)
```json
{
  "ts": "ISO8601",
  "task_type": "codegen|summarize|classify|...",
  "agent": "agent_name",
  "outcome": "success|fail|friction",
  "pattern": "description of what happened",
  "proposal_type": "new_skill|update_skill|governance_HUMAN_ONLY",
  "governance_domain": false,
  "evidence_path": "optional log path",
  "proposed_skill_name": "optional"
}
```

### 3. Weekly collector cron (reviews observations → creates proposals)
```bash
# Add to OpenClaw cron: every Monday 08:00 CDT
python3 ~/.openclaw/workspace/router/task_observer_collector.py
```

### 4. Collector logic
- Reads skill-observations/*.jsonl from last 7 days
- Groups by (task_type, pattern)
- If pattern occurs ≥3 times → create skill_workshop proposal
- GOVERNANCE_DOMAIN observations → write to ~/.openclaw/vault/governance_observations.jsonl only
- Never auto-apply proposals

---

## Status: DESIGNED — implementation pending

Creates zero new infrastructure:
- Output dir: `~/.openclaw/workspace/skill-observations/` (flat JSONL)
- Collector: `~/.openclaw/workspace/router/task_observer_collector.py`
- Proposals: via existing `skill_workshop` tool
- Governance: existing PMO + Nathan approval

No new daemon. No new database. No new port.
