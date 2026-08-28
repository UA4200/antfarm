# Task Observer — Open Empire Fit Report
**Author:** C0 Research Agent B  
**Date:** 2026-08-09  
**Source:** `rebelytics/one-skill-to-rule-them-all` (GitHub), CC BY 4.0  
**Component evaluated:** `task-observer` (SKILL.md + references/)  
**Classification:** Architecture Review — Skill Evolution Layer

---

## 1. What Task Observer Is

Task Observer is a **meta-skill** that runs alongside active work sessions, watches what the AI does, and produces structured recommendations for improving skills. It does not modify skills directly — it observes, logs, and proposes.

### Core Behavior

```
Session Starts
  → Observer reads observation log + cross-cutting principles
  → Observer watches session silently
  → Signals captured:
      • User corrections and adjustments
      • Workflow gaps no existing skill covers
      • Patterns repeating across sessions
      • Improvements to the observer's own methodology
  → Observations appended to log.md (silently, never interrupting work)
  → Review cycle (weekly or on-demand): cross-check observations → generate proposals
  → Proposals staged for human review and approval
  → Skills updated only after human approval
```

### What It Stores

| File | Location | Content |
|---|---|---|
| Observation log | `[workspace]/skill-observations/log.md` | Numbered entries: title, date, affected skill, type, issue, suggestion, principle |
| Cross-cutting principles | `[workspace]/cross-cutting-principles.md` | Generalizable rules that apply across all skills |
| Review date tracker | `[workspace]/skill-observations/last-review-date.txt` | When last review ran |
| Staged skill updates | `[workspace]/skill-updates/` | Proposed skill changes awaiting approval |
| Archive | `[workspace]/skill-observations/archive/` | Resolved observations |

### What It Does NOT Do
- Does NOT modify skill files directly
- Does NOT deploy changes automatically
- Does NOT rewrite governance, financial policy, or security controls
- Does NOT replace the human review step

---

## 2. Open Empire Existing Coverage

### What Open Empire Already Has

| Component | Location | Function |
|---|---|---|
| Skills system | `~/.openclaw/skills/` + `workspace/skills/` | Reusable skill definitions |
| `skill_workshop` tool | OpenClaw built-in | Create/update/propose/apply skill changes |
| ActionLogger | Implied in agent context | Logs agent actions taken |
| OutcomeCollector | Implied in agent context | Collects outcome data |
| PatternAnalyzer | `~/.openclaw/memory/pattern_analysis/latest.json` | Behavioral pattern extraction |
| PMO governance | Constitution, AGENTS.md | Venture governance, agent controls |

### Critical Status Questions (Unconfirmed)
- ActionLogger: mentioned in context but operational status unknown
- OutcomeCollector: mentioned but operational status unknown
- PatternAnalyzer: exists (`latest.json` present) but whether it feeds skill improvement unknown

---

## 3. Does Task Observer Duplicate PatternAnalyzer?

**No — they operate at different layers.**

| Dimension | PatternAnalyzer | Task Observer |
|---|---|---|
| **Target** | Operational behavior patterns (trading, lead gen, agent cycles) | Skill methodology patterns (how skills are written and used) |
| **Input** | Agent outputs, trade data, action logs | Session workflow, AI corrections, skill usage during tasks |
| **Output** | `latest.json` — behavioral pattern summary | `log.md` — structured skill improvement observations |
| **Layer** | Layer 3 (Normalization) in memory architecture | Meta-layer above skills |
| **Scope** | "What is the system doing" | "How should skills describe what to do" |
| **Consumer** | Signals engine, risk management | Skills system, skill_workshop |

**Verdict:** PatternAnalyzer analyzes agent *outcomes*. Task Observer analyzes skill *quality and completeness*. They are genuinely complementary, not duplicative.

---

## 4. Is Task Observer Additive?

**Yes — it fills a genuine gap.**

Open Empire has a sophisticated skills system and a `skill_workshop` tool for proposing skill changes. What it does NOT have is a systematic mechanism that:

1. **Watches active sessions for skill-improvement signals in real time** — currently, skill improvement happens when Nathan explicitly requests it, not from systematic observation
2. **Maintains a cross-cutting principles library** — generalizable rules that apply across all skills, not just one
3. **Flags when a correction in session X should update skill Y** — the connection between "agent did something wrong" and "skill needs updating" is currently manual
4. **Self-improves its own observation methodology** — the skill captures improvements to its own process over time

This is a **meta-skill feedback loop** that the existing system lacks. PatternAnalyzer catches operational patterns; `skill_workshop` handles proposals. Task Observer is the bridge that watches sessions and identifies when `skill_workshop` proposals should be created.

**Compounding value over time:** At scale (50+ skills, parallel sessions, multiple ventures), manually auditing each skill for quality becomes unmanageable. Task Observer's value compounds: more sessions → more observations → higher quality floor across all skills.

---

## 5. Governance Guardrails Required

This is the critical section. Task Observer must operate within strict boundaries in Open Empire.

### HARD BLOCKS — Task Observer MUST NOT Propose Changes To:

| Protected Domain | Rationale |
|---|---|
| **AGENTS.md** | Agent registry / PM2 config — changes affect live production |
| **MEMORY.md** | Canonical runtime state — changes affect all agent decisions |
| **Constitution / governance docs** | Core legal and operating framework |
| **Financial controls** | Daily spend caps, Kelly criterion, risk limits |
| **Approval gates** | sovereign_proxy logic, approval workflows |
| **Security policy** | Auth methods, secrets management |
| **Kelly criterion implementation** | Trading risk model — Kelly NO-fix preserved verbatim by policy |
| **Production deployment policy** | PM2 ecosystem configs, trading agent entrypoints |
| **Secrets / credentials** | Any path under `~/.openclaw/secrets/` |
| **Trading agent logic** | `trading.agents.*` — live capital at risk |

**These domains are read-only to Task Observer.** It may observe, but any observation touching these domains must be flagged as "GOVERNANCE DOMAIN — HUMAN ONLY" and route to Nathan directly, not to skill_workshop.

### PROPOSE-ONLY RULE (Enforced, Not Just Requested)

Task Observer's design already enforces propose-only for skill changes. For Open Empire, this extends further:
- All observations → `skill-observations/log.md` (read-only log)
- All proposals → `skill_workshop` tool (creates pending proposal, not live change)
- Proposals must be explicitly `skill_workshop apply`'d by a human
- No autonomous skill deployment

### Additional Guardrails

| Rule | Implementation |
|---|---|
| Observation log must not contain secrets | Observer must strip/exclude any observation that references credentials, API keys, or financial account data |
| Review cycle: human-triggered only | Weekly review may be suggested but never auto-deployed |
| Cross-cutting principles: Nathan approval before propagation | Before a new principle propagates to protected skills, Nathan must review |
| Scope declaration required | Each observation must declare its scope: `[SKILL]` or `[GOVERNANCE — BLOCKED]` |
| Observation log in workspace/ | Log lives in `~/.openclaw/workspace/skill-observations/log.md` — already in Obsidian vault, human-visible |

---

## 6. Integration Design for Open Empire

### Where It Lives

```
~/.openclaw/workspace/
  skills/
    task-observer/
      SKILL.md              ← task-observer skill
      references/
        weekly-review.md
        skill-authoring.md
        environments.md
  skill-observations/
    log.md                  ← observation log (human-visible in Obsidian)
    last-review-date.txt
    archive/
  skill-updates/            ← staged proposals (routed to skill_workshop)
  cross-cutting-principles.md
```

### Integration with skill_workshop

Task Observer's review cycle output → `skill_workshop create/update` (pending proposals only).

Flow:
```
Task Observer observation (log.md)
  → Weekly review: cross-check against skills
    → Skill update candidates identified
      → skill_workshop create proposal (status: pending)
        → Nathan reviews via skill_workshop list/inspect
          → Nathan runs skill_workshop apply (or reject)
            → Skill updated or discarded
```

This integrates cleanly. No new tools needed. `skill_workshop` is the approval gateway.

### Activation

Per task-observer design, activate via CLAUDE.md / system prompt instruction to ensure consistent loading. Suggested addition to OpenClaw session config:

```
At the start of every task-oriented session where tools will be used, load the task-observer skill.
```

---

## 7. Fit Assessment Summary

| Dimension | Score | Notes |
|---|---|---|
| Genuine gap | ✅ YES | No existing systematic skill observation loop |
| Duplicates PatternAnalyzer | ❌ NO | Different layer, different target |
| Creates new silo | ✅ NO | Uses workspace/, skill_workshop — existing infrastructure |
| Governance safe | ✅ YES (with guardrails) | Propose-only by design; add hard domain blocks |
| Integration complexity | LOW | Drop SKILL.md in workspace/skills/, add CLAUDE.md instruction |
| Value for Open Empire | MEDIUM-HIGH | Compounds with skill library growth |
| Immediate ROI | LOW-MEDIUM | Pays off at scale, not immediately |

**Verdict: INTEGRATE WITH GUARDRAILS.**

Task Observer is additive, non-duplicative, and fits cleanly into the existing skill_workshop flow. It is low-risk to add (no new daemons, no new databases, no new APIs). The only implementation work required is:
1. Place SKILL.md + references/ in `workspace/skills/task-observer/`
2. Add activation instruction to session config
3. Document the HARD BLOCKS list in the skill or in a governance wrapper

---

## 8. What Task Observer Does NOT Replace

To be explicit:

| Component | Relationship to Task Observer |
|---|---|
| ActionLogger | Still needed — captures raw actions (different layer) |
| OutcomeCollector | Still needed — captures outcomes (different layer) |
| PatternAnalyzer | Still needed — analyzes operational patterns (different layer) |
| PMO governance | Untouched — governance docs are read-only to Observer |
| skill_workshop | Used BY Task Observer as the proposal output channel |
| Nathan review | Non-negotiable — all proposals require human approval |

---

## 9. Recommended Implementation Checklist

```
□ Place task-observer SKILL.md + references/ in ~/.openclaw/workspace/skills/task-observer/
□ Add session activation instruction (CLAUDE.md or OpenClaw session config)
□ Create governance wrapper file: workspace/skill-observations/OBSERVER_GOVERNANCE.md
    • List all HARD BLOCK domains
    • Confirm propose-only rule
    • Confirm skill_workshop as the only output channel
□ Establish weekly review cadence (Monday, human-triggered)
□ Wire review output to skill_workshop create (not direct file write)
□ First review after 2 weeks of session accumulation
□ Nathan final authority on cross-cutting principle propagation
```

---

*Full credit: task-observer created by Eoghan Henn / rebelytics.com, CC BY 4.0. Canonical: https://github.com/rebelytics/one-skill-to-rule-them-all*
