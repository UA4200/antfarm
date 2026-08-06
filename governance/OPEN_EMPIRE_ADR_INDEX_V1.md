# OPEN EMPIRE ARCHITECTURAL DECISION RECORD INDEX V1

**Version:** 1.0.0
**Status:** Draft — Pending Validation
**Owner:** Nathan (Sovereign Operator)
**Source:** `~/.openclaw/workspace/AGENTS.md` (V5.0), `~/.openclaw/workspace/CONSTITUTION.md` (V1.2), `~/.openclaw/workspace/governance/OPEN_EMPIRE_ASSET_TAXONOMY_V1.md` (V1.0.0), project history 2026-07-30 through 2026-08-05
**Materialization Date:** 2026-08-05
**Dependencies:** OPEN_EMPIRE_ASSET_TAXONOMY_V1.md, OPEN_EMPIRE_CONSTITUTION_V1.md
**Revision History:**
| Version | Date | Author | Change |
|---|---|---|---|
| 1.0.0 | 2026-08-05 | Alusi | Initial materialization under Governance Freeze Order 2026-08-05 |

---

## ABOUT THIS DOCUMENT

An Architectural Decision Record (ADR) documents a significant architectural decision: the context that required it, the decision made, and the consequences that followed. ADRs are immutable records — they are never deleted, only superseded.

This index contains the 10 foundational ADRs for Open Empire, covering decisions made between 2026-07-30 and 2026-08-05. After Governance Baseline V1.0.0 is declared, all new ADRs must follow the **ADR Template** at the end of this document and be added via Change Control.

---

## ADR-001: Kalshi API Migration to V2 with RSA-PSS Signing

**Date:** 2026-07-30
**Status:** Accepted
**Supersedes:** N/A

### Context

The Kalshi V1 API was deprecated by Kalshi and began returning HTTP 410 (Gone) errors on all trading endpoints. Simultaneously, the existing signing implementation used PKCS1v15, which Kalshi's V2 API rejects. These two failures together completely blocked all Kalshi trading operations. The system had no canonical Kalshi client — signing logic was embedded in scattered agent scripts.

### Decision

Migrate all Kalshi interactions to the V2 API endpoint (`/portfolio/events/orders`) with RSA-PSS signing. Create a canonical client at `trading.clients.kalshi_client.KalshiClient`. All Kalshi operations — market scanning, order placement, balance check — must use this canonical client. No agent may call Kalshi APIs directly without routing through `KalshiClient`.

### Consequences

**Positive:**
- Eliminates 410 errors; all Kalshi operations functional.
- RSA-PSS signing is centralized in one module — reduces signing drift risk.
- Canonical client pattern establishes a reusable model for all future exchange integrations.

**Negative:**
- All existing Kalshi code in legacy `cashclaw/` paths must be updated or deprecated — creates a migration burden.
- RSA-PSS key management adds operational complexity (key storage, rotation policy).
- V2 API contract must be monitored for future breaking changes; no V3 migration plan exists yet.

**Active constraint:** All Kalshi operations must use `trading.clients.kalshi_client.KalshiClient`. Legacy paths (`~/.openclaw/cashclaw/`) are deprecated.

---

## ADR-002: Trading Code Consolidation under `~/.openclaw/trading/`

**Date:** 2026-07-31
**Status:** Accepted
**Supersedes:** N/A

### Context

Trading code was fragmented across three separate directory trees:
- `~/.openclaw/cashclaw/` — original Kalshi trading stack
- `~/.openclaw/moltlaunch/agents/cashclaw_director/` — director agent variant
- `~/.openclaw/polymarket/` — Polymarket integration

This fragmentation caused: duplicate logic across three codebases, confusion about which path was canonical, maintenance burden requiring triple-updates for any shared change, and multiple crash loops on 2026-07-30 due to module path drift between PM2 configs and actual code locations.

### Decision

Consolidate all trading code under a single canonical path: `~/.openclaw/trading/`. Canonical sub-structure:
- `trading/clients/` — exchange API clients (kalshi_client, polymarket_client)
- `trading/shared/` — shared libraries (signals, kelly, risk, logging)
- `trading/agents/` — trading agents (director, arb, polymarket_trader, sentinel)
- `trading/data/` — trade logs and state files

All PM2 ecosystem configs updated to reference canonical paths. Legacy directories moved to `~/.openclaw/_deprecated/` after Phase 6 approval (not deleted — retirement, not deletion).

### Consequences

**Positive:**
- Single canonical path eliminates module path drift.
- Shared libraries (`trading.shared.*`) are now genuinely shared — no duplication.
- PM2 configs map cleanly to canonical module paths.
- Crash loops caused by path mismatch resolved.

**Negative:**
- Migration requires updating all PM2 ecosystem configs and agent references.
- `_deprecated/` directories persist until Phase 6 approval — creates a transitional state that must be tracked.
- Any agent or script that hardcoded old paths will break if not updated.

**Active constraint:** `~/.openclaw/trading/` is the canonical and only authorized trading code path. References to legacy paths are governance violations.

---

## ADR-003: Rolling 24h Daily Spend Caps on All Trading Ventures

**Date:** 2026-07-31
**Status:** Accepted
**Supersedes:** N/A

### Context

An overnight trading drain event depleted approximately $63 in autonomous trading operations without human awareness or intervention. No spend limits were enforced at the code level. The trading agents had standing authorization but no upper bound on cumulative spend within a time window. This was identified as a critical governance gap — the absence of a hard ceiling on autonomous financial operations.

### Decision

Implement rolling 24-hour spend caps enforced at the agent code level for all trading Ventures:
- `CASHCLAW_DAILY_SPEND_CAP_USD=10` — CashClaw Director (cashclaw_director, PM2 id=38)
- `ARB_DAILY_SPEND_CAP_USD=10` — Arb executor (cashclaw_arb, PM2 id=39)
- `POLY_DAILY_SPEND_CAP_USD=10` — Polymarket Trader (polymarket_trader, PM2 id=40)

Enforcement mechanism: before placing any trade, each agent sums the `size_usd` values in `trades.jsonl` for the rolling 24-hour window. If the sum of placed trades meets or exceeds the cap, the trade is blocked, logged, and a Telegram alert is sent. The cap resets on a rolling basis (not midnight-based).

### Consequences

**Positive:**
- Maximum possible autonomous loss capped at $30/day across all three trading agents ($10 each).
- Provides a predictable financial boundary for Nathan's oversight.
- Eliminates the overnight drain scenario — worst case is now $10 per agent before halt.

**Negative:**
- Caps are agent-level, not platform-level — if an agent bypasses its cap check (bug), the platform will not independently enforce the cap. Requires trading_sentinel as a backup watchdog.
- A $10/day cap may constrain profitable arb windows where more capital deployment would be advantageous. Requires explicit Nathan directive to raise.
- Cap enforcement depends on `trades.jsonl` integrity — if the file is tampered with, caps could be bypassed.

**Active constraint:** Every trading agent must check its spend cap before placing any trade. This constraint is mandatory for all future trading agents added to the system.

---

## ADR-004: Signal Chain Lock — Haiku→Ollama→Heuristic, No GPT-4o

**Date:** 2026-08-02
**Status:** Accepted
**Supersedes:** N/A

### Context

GPT-4o was included in the signal scoring chain as a fallback or alternative model for trade signal evaluation. A cost governance review identified this as inconsistent with the $0.12/day signal scoring cost target. GPT-4o's token pricing is 10-50× higher than Claude Haiku for equivalent inference tasks. Its presence in the real-time chain created unpredictable cost exposure on every scoring cycle.

### Decision

The canonical signal chain is locked to: **Haiku → Ollama → Heuristic** in that exact sequence. GPT-4o is removed from all signal scoring paths. No reinsertion of GPT-4o or any other external paid model into the real-time signal chain is permitted without an explicit Nathan directive.

Operational meaning of the chain:
1. **Haiku** — Claude Haiku (Anthropic) is the primary real-time scorer. Low cost, fast latency.
2. **Ollama** — Local inference (Ollama, port 11434) is the fallback when Haiku is rate-limited or unavailable. Zero marginal cost.
3. **Heuristic** — Rule-based heuristic scoring is the final fallback when both AI models are unavailable. Zero cost, deterministic.

### Consequences

**Positive:**
- Signal scoring cost target ~$0.12/day achieved and maintainable.
- Deterministic fallback chain — the system never fails silently due to model unavailability.
- Heuristic fallback ensures trading can continue even during full AI provider outages.

**Negative:**
- GPT-4o's superior reasoning on complex market signals is unavailable for routine scoring. This may reduce signal quality in edge cases.
- Signal quality degradation must be monitored — if win rate drops after lock, the chain design must be revisited via Change Control.
- Ollama inference on Intel Mac Mini is 2-8 tokens/second — may introduce latency in the fallback path.

**Active constraint:** The Haiku→Ollama→Heuristic chain is locked. Any deviation is a governance violation triggering a P0 Drift Detection alert. See also: ADR-008 (Haiku-Only Scoring).

---

## ADR-005: Kelly NO-fix — kelly.py is Immutable

**Date:** 2026-07-31
**Status:** Accepted
**Supersedes:** N/A

### Context

The Kelly criterion implementation in `trading/shared/kelly.py` was tuned and validated as part of the Phase 5 trading consolidation. The Kelly formula governs position sizing — the calculation of how much capital to stake on each trade as a fraction of the available bankroll. Ad-hoc modifications to Kelly parameters or formula implementation had caused inconsistent position sizing in earlier iterations, with risk of both under-sizing (foregone profit) and over-sizing (excess capital exposure).

### Decision

`trading.shared.kelly` (kelly.py) is frozen. The Kelly criterion implementation **must not be modified** by any agent for any reason without an explicit Nathan directive. This constraint is:
- Permanent until superseded by a Nathan directive
- Enforced at the Library level (see Taxonomy entry for Library)
- Recorded in this ADR as an immutable governance constraint

No refactoring, "optimization," parameter tuning, or formula adjustment is permitted under this constraint.

### Consequences

**Positive:**
- Position sizing is stable and predictable across all trading cycles.
- Eliminates risk of drift from well-intentioned but unreviewed Kelly modifications.
- Creates a stable baseline for P&L attribution — Kelly behavior is a known constant.

**Negative:**
- If market conditions change significantly, the Kelly parameters may become suboptimal. Adjustment requires a formal Change Proposal and Nathan directive.
- Any bug discovered in kelly.py requires the same formal process — cannot be hotfixed unilaterally.
- Future trading agents that need different Kelly parameters must implement their own fork with explicit approval, not modify the shared library.

**Active constraint:** kelly.py is immutable. This is the Kelly NO-fix governance constraint referenced throughout Open Empire documentation.

---

## ADR-006: Polymarket US — Ed25519 Auth via api.polymarket.us

**Date:** 2026-07-31
**Status:** Accepted
**Supersedes:** N/A

### Context

Polymarket launched Polymarket US as a separate platform from the legacy Polymarket, targeting US-based participants with a distinct API surface and authentication method. Polymarket US requires Ed25519 cryptographic signing (distinct from PKCS1v15 or RSA-PSS used on other platforms). The legacy `polymarket/` codebase did not support Ed25519 signing and targeted the wrong API endpoint. $40 of capital was allocated to Polymarket US as part of the cross-arb strategy between Kalshi and Polymarket.

### Decision

Adopt the polymarket-us SDK with Ed25519 signing for all Polymarket operations. Create a canonical client at `trading.clients.polymarket_client.PolymarketClient` targeting `api.polymarket.us`. All Polymarket operations must use this canonical client. The legacy `polymarket/` path is deprecated and moved to `_deprecated/`.

### Consequences

**Positive:**
- $40 capital deployed on Polymarket US with correct authentication.
- Ed25519 signing is centralized in the canonical client — consistent with the pattern established in ADR-001 for Kalshi.
- Enables the Kalshi↔Polymarket US cross-arb strategy (alert mode, pending validation per ADR-003 constraints).

**Negative:**
- Ed25519 key management adds another credential to the Secret Metadata registry.
- Geoblocking risk: Polymarket US is US-only. Geographic access must be verified on any infrastructure change.
- The cross-arb strategy uses alert-only mode due to semantic false-positive risk — full automation pending further validation.

**Active constraint:** `trading.clients.polymarket_client.PolymarketClient` is the canonical Polymarket client. Legacy `polymarket/` is deprecated.

---

## ADR-007: CashClaw Director Cycle Extended from 60s to 300s

**Date:** 2026-07-30
**Status:** Accepted
**Supersedes:** N/A

### Context

The CashClaw Director was initially configured with a 60-second polling cycle — scanning for market opportunities and evaluating signals every 60 seconds. This created approximately 1,440 API calls per day to the Kalshi API during trading hours, which represented 80% more calls than operationally necessary. The 60-second cycle was a default development setting that was never reviewed for production suitability. Kalshi's API has rate limits that, at 60-second cycles, created unnecessary risk of rate-limiting and excess API cost.

### Decision

Change the CashClaw Director cycle from 60 seconds to 300 seconds (5 minutes). The PM2 `cron_restart` and internal loop timer are both updated to reflect the 5-minute cadence. This applies to all trading agents that follow the Director's polling pattern: director, arb, sentinel (15-minute cycle for polymarket_trader is separate).

### Consequences

**Positive:**
- -80% reduction in Kalshi API calls (from ~1,440 to ~288 per trading day).
- Reduced rate-limiting risk.
- Lower Anthropic API costs per day (fewer Haiku scoring calls).
- Consistent with the $0.12/day signal cost target.

**Negative:**
- Maximum signal latency increases from ~1 minute to ~4 minutes. A market opportunity that opens and closes within 4 minutes will be missed.
- For highly time-sensitive arbitrage windows, the 5-minute cycle may be too slow. This trade-off was reviewed and accepted for the current market conditions.

**Active constraint:** Director cycle is 5 minutes. Changes to cycle time require Change Control due to cost and API impact.

---

## ADR-008: Haiku-Only Signal Scoring — No Sonnet for Routine Scoring

**Date:** 2026-08-02
**Status:** Accepted
**Supersedes:** N/A

### Context

A cost governance review identified that Claude Sonnet was being used as a fallback for signal scoring in some agent configurations. Sonnet's pricing is approximately 5× higher than Haiku for equivalent short-context scoring tasks. The signal scoring task — classifying a market opportunity as buy/hold/pass — does not require Sonnet-class reasoning; it requires fast, consistent classification on structured inputs. Sonnet was being used out of convenience, not necessity.

### Decision

Claude Haiku is the primary and only permitted model for routine real-time signal scoring. Claude Sonnet is explicitly **not permitted** for routine scoring. Sonnet remains available for:
- Drafting complex documents (BLCO outreach, governance documents)
- Complex analysis requiring multi-step reasoning
- Session-level Chief of Staff functions (Alusi)

This ADR supplements ADR-004 (Signal Chain Lock): the chain is Haiku→Ollama→Heuristic, and Sonnet is not in that chain at any position.

### Consequences

**Positive:**
- Signal scoring cost target ~$0.12/day achievable and maintained.
- Clear model dispatch policy: Haiku for real-time scoring, Sonnet for drafting and analysis.
- Prevents cost creep from ad-hoc model selection in new agents.

**Negative:**
- Sonnet's richer context window and superior reasoning are unavailable for signal evaluation. Complex market signals may be under-analyzed at Haiku's level.
- As the signal scoring task grows in complexity (more market types, more signal dimensions), Haiku may become insufficient. A re-evaluation trigger should be defined.

**Active constraint:** Haiku is the only permitted model for routine signal scoring. Sonnet is reserved for drafting and complex analysis. See also ADR-004.

---

## ADR-009: Asset Taxonomy as Root Governance Artifact

**Date:** 2026-08-04
**Status:** Accepted
**Supersedes:** N/A

### Context

Multiple governance documents and operational files defined overlapping concepts inconsistently. "Agent" was defined differently in AGENTS.md, CONSTITUTION.md, and various Playbooks. "Venture" had no formal definition but was used in multiple contexts. "Service" was conflated with "Process" and "Agent" interchangeably. This semantic drift made governance documents harder to read, created hidden conflicts, and made automated governance tooling impossible to build without a controlled vocabulary.

### Decision

`OPEN_EMPIRE_ASSET_TAXONOMY_V1.md` is the **root governance artifact**. It contains the single, authoritative definition for all 58 canonical asset types used in Open Empire. Every downstream document — Constitution, Playbooks, ADRs, Registry, Schema — inherits its definitions from the Taxonomy. No term defined in the Taxonomy may be silently redefined in any downstream document.

The Taxonomy hierarchy:
1. Taxonomy → root definitions
2. Schema → machine-readable field definitions (inherits Taxonomy)
3. Ontology → valid relationships (inherits Taxonomy)
4. Asset Registry → real instances (implements Schema)
5. All other documents → reference the above

### Consequences

**Positive:**
- Semantic consistency enforced across all governance documents.
- New documents can be written using Taxonomy terms without fear of definition conflict.
- Machine-readable governance tooling (Build Pipeline, Validation Suite) becomes possible.
- ADR and Glossary generation can be automated from the Taxonomy.

**Negative:**
- Any change to a Taxonomy definition now requires a version bump and Change Control — previously, changing a word in a document was trivial.
- Approximately 15 existing documents contain terms that do not match their Taxonomy definitions. These require a reconciliation pass (scheduled for Track B).
- The Taxonomy is 58 entries across 6 layers — a significant investment to maintain accurately.

**Active constraint:** No term defined in the Taxonomy may be silently redefined in any document. Clarifications are permitted; redefinitions require a V2 Taxonomy with P0 Change Control.

---

## ADR-010: Governance Freeze Order — Controlled Freeze to Baseline V1.0.0

**Date:** 2026-08-05
**Status:** Accepted
**Supersedes:** N/A

### Context

The governance architecture phase was at risk of indefinite expansion. New document proposals continued to emerge without clear criteria for when the governance foundation was "complete." The risk: spending indefinite time on governance documents while Track B (actual implementation — trading improvements, BLCO activation, ADAI product delivery) was deferred. Additionally, governance documents written under open-ended scope tend to be over-engineered, include aspirational content, and require revision cycles that consume more capacity than they save.

### Decision

Freeze the governance architecture at exactly 12 authorized deliverables. No new governance artifacts may be created after the Governance Freeze Order (2026-08-05) without going through Change Control. The 12 authorized deliverables define the complete Governance Baseline V1.0.0:

1. OPEN_EMPIRE_ASSET_TAXONOMY_V1.md ✓ (complete)
2. OPEN_EMPIRE_CONSTITUTION_V1.md (Wave A)
3. OPEN_EMPIRE_GLOSSARY_V1.md (Wave A)
4. OPEN_EMPIRE_ADR_INDEX_V1.md (Wave A)
5. OPEN_EMPIRE_SCHEMA_V1.json (Wave B)
6. OPEN_EMPIRE_ONTOLOGY_V1.md (Wave B)
7. OPEN_EMPIRE_ASSET_REGISTRY_V1.json (Wave C)
8. OPEN_EMPIRE_VALIDATION_SUITE_V1.md (Wave C)
9. OPEN_EMPIRE_BUILD_PIPELINE_V1.md (Wave D)
10. OPEN_EMPIRE_PLAYBOOK_V1.md (Wave D)
11. OPEN_EMPIRE_RELEASE_MANIFEST_V1.md (Wave E)
12. OPEN_EMPIRE_ROLLBACK_MANIFEST_V1.md (Wave E)

Track B (implementation) begins immediately after Governance Baseline V1.0.0 is declared (`TRACK_B_AUTHORIZED`).

### Consequences

**Positive:**
- Creates a clear completion criterion for the governance architecture phase.
- Prevents scope creep — every proposed addition requires a formal Change Control.
- Frees capacity for Track B implementation work.
- Forces governance documents to be minimal and functional rather than aspirational and comprehensive.

**Negative:**
- Some governance gaps will exist at V1.0.0 — they are marked `TODO_PENDING_APPROVAL` and scheduled for V1.1.0.
- The 12-document count was determined by judgment, not formal completeness analysis. Some needed governance artifacts may have been omitted.
- The freeze creates pressure to complete all 12 deliverables quickly, which may reduce document quality if not managed.

**Active constraint:** The authorized deliverables are frozen at 12. The Governance Freeze Order is in effect. Success is measured by operational capability, not document count.

---

## ADR Template

Use this template for all future ADRs after Governance Baseline V1.0.0. Submit new ADRs via Change Control.

---

## ADR-NNN: \<Title\>
**Date:** YYYY-MM-DD
**Status:** Proposed | Accepted | Superseded | Deprecated
**Proposed By:** \<name or agent\>
**Supersedes:** ADR-NNN (if applicable)

### Context
[Why is this decision needed? What problem does it solve? What was the situation that forced a decision?]

### Decision
[What was decided? Be specific. Name the canonical paths, models, caps, or constraints that were adopted.]

### Consequences
[Positive and negative consequences. What becomes easier? What becomes harder? What constraints does this create? What risks does this introduce?]

### Review Date
[When should this ADR be reviewed? Under what conditions should this decision be revisited?]

---

## Summary Index

| ADR | Title | Status | Date |
|---|---|---|---|
| ADR-001 | Kalshi API Migration to V2 with RSA-PSS Signing | Accepted | 2026-07-30 |
| ADR-002 | Trading Code Consolidation under `~/.openclaw/trading/` | Accepted | 2026-07-31 |
| ADR-003 | Rolling 24h Daily Spend Caps on All Trading Ventures | Accepted | 2026-07-31 |
| ADR-004 | Signal Chain Lock — Haiku→Ollama→Heuristic, No GPT-4o | Accepted | 2026-08-02 |
| ADR-005 | Kelly NO-fix — kelly.py is Immutable | Accepted | 2026-07-31 |
| ADR-006 | Polymarket US — Ed25519 Auth via api.polymarket.us | Accepted | 2026-07-31 |
| ADR-007 | CashClaw Director Cycle Extended from 60s to 300s | Accepted | 2026-07-30 |
| ADR-008 | Haiku-Only Signal Scoring — No Sonnet for Routine Scoring | Accepted | 2026-08-02 |
| ADR-009 | Asset Taxonomy as Root Governance Artifact | Accepted | 2026-08-04 |
| ADR-010 | Governance Freeze Order — Controlled Freeze to Baseline V1.0.0 | Accepted | 2026-08-05 |

---

*OPEN EMPIRE ADR INDEX V1.0.0 — Materialized 2026-08-05 — Alusi, Chief of Staff*
*10 foundational ADRs covering 2026-07-30 through 2026-08-05*
*ADR records are immutable — they are never deleted, only superseded*
*Governed by: Governance Freeze Order 2026-08-05*
