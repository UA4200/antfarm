# OPEN EMPIRE ASSET TAXONOMY V1
**Version:** 1.0.0
**Status:** Active — Versioned Standard
**Owner:** Nathan (Sovereign Operator)
**Source:** Open Empire sovereign doctrine (~/.openempire/), operational history, SOUL.md, MEMORY.md
**Materialization Date:** 2026-08-04
**Dependencies:** OPEN_EMPIRE_CONSTITUTION_V1.md (this Taxonomy is the primary implementing standard of the Constitution)
**Issued By:** Alusi (Chief of Staff) | Approved By: Nathan (Sovereign Operator)
**Effective Date:** 2026-08-04
**Revision History:**

| Version | Date | Author | Change |
|---|---|---|---|
| 1.0.0 | 2026-08-04 | Alusi | Initial materialization — root governance artifact |
**Next Review:** 2026-11-04 (Quarterly)
**Location:** `~/.openclaw/workspace/governance/OPEN_EMPIRE_ASSET_TAXONOMY_V1.md`

---

## PREAMBLE

This Taxonomy is not merely a list of definitions.
It is the language of Open Empire.

Every future document must reuse these definitions.
No future deliverable may redefine a term that already exists in this Taxonomy.

**Hierarchy of artifacts:**
1. **This Taxonomy** — root governance artifact. Defines all canonical terms.
2. **The Schema** — implements the Taxonomy as machine-readable field definitions.
3. **The Ontology** — defines valid relationships between Taxonomy elements.
4. **The Asset Registry** — instantiates the Schema with real Open Empire assets.
5. **Mission Control** — visualizes the Registry.
6. **OEPM** — consumes the Registry to govern execution.
7. **PMO** — governs execution from the Registry.
8. **The Build Book** — explains how to implement assets.
9. **The Operations Playbook** — explains how to operate assets.

Every future artifact inherits upward from these governance documents rather than redefining concepts independently.

**Evolution Policy:** This Taxonomy is a versioned standard. It is not frozen. Additions and non-breaking clarifications increment the minor version (V1.x). Breaking redefinitions of existing terms require a major version (V2) with full Change Control approval. No term defined here may be silently redefined in downstream documents.

---

## ENTRY FORMAT

Each entry contains the following 13 fields:

| Field | Description |
|---|---|
| **Canonical Name** | The single, authoritative name for this asset type |
| **Canonical Definition** | The precise definition — binding across all Open Empire documents |
| **Purpose within Open Empire** | Why this asset type exists and what problem it solves |
| **Parent Layer** | The layer this asset type belongs to |
| **Parent Asset** | The asset type that contains or governs this one (if applicable) |
| **Child Asset Types** | Asset types that are contained within or governed by this one |
| **Allowed Relationships** | Valid directed relationships to/from other asset types |
| **Lifecycle Applicability** | Valid states for this asset type |
| **Required Schema Fields** | Minimum fields every instance must carry |
| **Validation Rules** | Rules that must be true for the asset to be considered valid |
| **Examples from Open Empire** | Real instances from the current Open Empire deployment |
| **Cross References** | Related Taxonomy entries and governance documents |
| **Notes** | Implementation guidance, decisions, and constraints |

---

# LAYER 1 — BUSINESS

> The strategic and financial layer. Defines what Open Empire is building, for what purpose, and with what expected return.

---

### Portfolio

| Field | Value |
|---|---|
| **Canonical Name** | Portfolio |
| **Canonical Definition** | A governed collection of Programs and Ventures aligned to a single sovereign mission, managed as a unified capital and strategic asset. |
| **Purpose within Open Empire** | Top-level strategic container for all revenue-generating and capability-building initiatives under Open Empire. The Portfolio is the unit at which Nathan exercises sovereign financial authority. |
| **Parent Layer** | Layer 1 — Business |
| **Parent Asset** | None (root node — no parent) |
| **Child Asset Types** | Program, Venture |
| **Allowed Relationships** | CONTAINS Program · CONTAINS Venture · MEASURED_BY Executive KPI · PRODUCES Business Outcome · GOVERNED_BY Council |
| **Lifecycle Applicability** | Active · Archived |
| **Required Schema Fields** | `id` · `name` · `owner` · `mission_alignment` · `programs[]` · `ventures[]` · `kpis[]` · `capital_deployed_usd` · `created_at` · `status` |
| **Validation Rules** | Must have at least one Program or Venture. Must have an assigned owner. Must align to a documented mission statement. Owner must be Nathan or an explicitly delegated Executive Role. |
| **Examples from Open Empire** | Open Empire Sovereign Portfolio (master) · ADAI Products Portfolio · CashClaw Ops Portfolio |
| **Cross References** | L2: Council · L1: Program, Venture, Executive KPI, Business Outcome |
| **Notes** | There is one sovereign Portfolio at the top of Open Empire. All sub-portfolios derive authority from it. No Portfolio may operate with autonomous capital deployment without a daily_spend_cap and Nathan's explicit approval. |

---

### Program

| Field | Value |
|---|---|
| **Canonical Name** | Program |
| **Canonical Definition** | A coordinated grouping of Projects and Business Capabilities that together deliver a strategic Business Outcome within a Portfolio. |
| **Purpose within Open Empire** | Bridges strategic Portfolio intent with tactical Project execution. Manages cross-Project dependencies and shared capability development over multi-quarter horizons. |
| **Parent Layer** | Layer 1 — Business |
| **Parent Asset** | Portfolio |
| **Child Asset Types** | Project · Business Capability |
| **Allowed Relationships** | BELONGS_TO Portfolio · CONTAINS Project · REQUIRES Business Capability · MEASURED_BY Executive KPI · DELIVERS Business Outcome · GOVERNED_BY Council |
| **Lifecycle Applicability** | Planned · Active · On Hold · Completed · Archived |
| **Required Schema Fields** | `id` · `name` · `portfolio_id` · `owner` · `objectives[]` · `projects[]` · `capabilities[]` · `status` · `start_date` · `target_end_date` |
| **Validation Rules** | Must belong to exactly one Portfolio. Must have at least one Project. Owner must be an active Executive Role. On Hold state requires a documented reason and review date. |
| **Examples from Open Empire** | CashClaw Trading Program · BLCO Commodity Sales Program · Moltlaunch Marketplace Program · ADAI Products Program |
| **Cross References** | L2: Council · L5: Execution Roles · L6: Current State |
| **Notes** | Programs are not time-boxed the way Projects are — they may span multiple quarters. When a Program's Projects are complete but the capability must persist, the Program converts to an ongoing Venture or Business Capability. |

---

### Project

| Field | Value |
|---|---|
| **Canonical Name** | Project |
| **Canonical Definition** | A time-boxed, scope-defined unit of work within a Program that produces one or more deliverables with measurable completion criteria. |
| **Purpose within Open Empire** | The primary unit of planned execution within Open Empire. Governed by PMO lifecycle rules. Every discrete piece of time-bounded work is a Project. |
| **Parent Layer** | Layer 1 — Business |
| **Parent Asset** | Program |
| **Child Asset Types** | None (leaf node in Business layer — links to Engineering and Operations assets as outputs) |
| **Allowed Relationships** | BELONGS_TO Program · PRODUCES Repository · PRODUCES Service · PRODUCES Agent · GOVERNED_BY Policy · MEASURED_BY Executive KPI · CARRIES Risk Level |
| **Lifecycle Applicability** | Planned · In Progress · Blocked · Complete · Cancelled |
| **Required Schema Fields** | `id` · `name` · `program_id` · `owner` · `deliverables[]` · `start_date` · `end_date` · `status` · `risk_level` |
| **Validation Rules** | Must have a defined `end_date`. Must list at least one deliverable. Must carry an assigned `risk_level`. Cannot be Active without an owner. Blocked state requires documented blocker and escalation target. |
| **Examples from Open Empire** | CashClaw Phase 5 Consolidation (Complete 2026-07-31) · Open Empire GitHub Deployment v0.1.0 (Complete 2026-07-30) · Polymarket US Integration (Complete 2026-07-31) · Trading Repository Git Init (Pending) |
| **Cross References** | L2: Lifecycle States · L5: Operational Status · L6: Change Control |
| **Notes** | A Project is not permanently active. When a Project's output must keep running beyond completion, it graduates to a Service, Automation, or Agent. The completion of a Project does not destroy its outputs — it transfers ownership to an Operational asset. |

---

### Business Capability

| Field | Value |
|---|---|
| **Canonical Name** | Business Capability |
| **Canonical Definition** | A stable, reusable ability that Open Empire possesses and applies across multiple Programs or Projects — independent of any specific technology or implementation. |
| **Purpose within Open Empire** | Separates WHAT Open Empire can do from HOW it currently does it. Enables capability gap analysis and strategic investment prioritization independent of individual system lifecycles. |
| **Parent Layer** | Layer 1 — Business |
| **Parent Asset** | Program (associated with) · Portfolio (owned by) |
| **Child Asset Types** | None |
| **Allowed Relationships** | REQUIRED_BY Program · ENABLED_BY Service · ENABLED_BY Agent · ENABLED_BY Integration · GOVERNED_BY Policy |
| **Lifecycle Applicability** | Emerging · Developing · Established · Optimized · Retired |
| **Required Schema Fields** | `id` · `name` · `description` · `maturity_level` · `enabling_assets[]` · `owner` · `programs[]` |
| **Validation Rules** | Must be defined independently of any specific implementation. Must list at least one enabling asset. `maturity_level` must be one of: Emerging, Developing, Established, Optimized. Retired capabilities must reference their retirement justification. |
| **Examples from Open Empire** | Autonomous Trading · Lead Sourcing · AI Signal Scoring · Multi-channel Messaging · Approval Gating · Contract Arbitrage Detection |
| **Cross References** | L3: Model, API, Integration · L4: Agent, Service · L5: Business Criticality |
| **Notes** | Business Capabilities survive the retirement of individual systems that enable them. When trading/ superseded cashclaw/, the Autonomous Trading capability did not retire — only its implementation changed. This distinction is critical for roadmap planning. |

---

### Venture

| Field | Value |
|---|---|
| **Canonical Name** | Venture |
| **Canonical Definition** | A revenue-generating or revenue-targeting operational unit within Open Empire — a distinct line of business with its own capital allocation, P&L accountability, and go-to-market strategy. |
| **Purpose within Open Empire** | Tracks each monetizable initiative as a business unit with its own economics. The Venture is the unit at which Open Empire measures financial performance. |
| **Parent Layer** | Layer 1 — Business |
| **Parent Asset** | Portfolio |
| **Child Asset Types** | Program · Project (via Program) |
| **Allowed Relationships** | BELONGS_TO Portfolio · CONTAINS Program · MEASURED_BY Executive KPI · PRODUCES Business Outcome · GOVERNED_BY Council · CARRIES Risk Level |
| **Lifecycle Applicability** | Pre-Launch · Active · Scaling · On Hold · Winding Down · Closed |
| **Required Schema Fields** | `id` · `name` · `portfolio_id` · `owner` · `revenue_model` · `capital_deployed_usd` · `daily_spend_cap_usd` · `status` · `programs[]` · `p_and_l_ref` |
| **Validation Rules** | Must have an explicit `revenue_model`. Must have a defined `capital_deployed_usd`. Must have a `daily_spend_cap_usd` if it involves any autonomous financial operations. Cannot transition to Scaling without at least one verified revenue event. |
| **Examples from Open Empire** | CashClaw Ops — Kalshi + Polymarket US trading ($65.19 capital, $10/day spend cap) · BLCO Commodity Sales (paused, 630 leads) · Moltlaunch HyrveAI (P1, marketplace live) · ADAI Enterprise Agent Factory ($3k–$10k build + $500–$2k/mo maintenance) |
| **Cross References** | L2: Council, Risk Levels · L5: Business Criticality, Recovery Priority |
| **Notes** | A Venture is not a Project. It is ongoing. It has its own P&L. It can contain multiple Programs. The daily_spend_cap is mandatory and enforced at the agent level — CASHCLAW_DAILY_SPEND_CAP_USD, ARB_DAILY_SPEND_CAP_USD, POLY_DAILY_SPEND_CAP_USD are all Venture-level controls. |

---

### Executive KPI

| Field | Value |
|---|---|
| **Canonical Name** | Executive KPI |
| **Canonical Definition** | A quantifiable, time-bound performance indicator tracked at the Portfolio, Program, or Venture level to assess progress against strategic objectives. |
| **Purpose within Open Empire** | Provides Nathan with a single pane of governance metrics across all active initiatives without requiring direct system access. |
| **Parent Layer** | Layer 1 — Business |
| **Parent Asset** | Portfolio · Program · Venture (one owner per KPI) |
| **Child Asset Types** | None |
| **Allowed Relationships** | MEASURES Portfolio · MEASURES Program · MEASURES Venture · DISPLAYED_BY Dashboard · EVALUATED_BY Council · CARRIES Evidence State |
| **Lifecycle Applicability** | Active · Deprecated |
| **Required Schema Fields** | `id` · `name` · `target_value` · `current_value` · `unit` · `measurement_frequency` · `owner_asset_id` · `owner_asset_type` · `direction` (higher_is_better \| lower_is_better) · `last_updated` · `evidence_state` |
| **Validation Rules** | Must have a numeric `target_value`. Must have a defined `measurement_frequency`. Must be linked to exactly one owner asset. `evidence_state` must be populated. Stale KPIs (not refreshed within 2× measurement_frequency) must be flagged. |
| **Examples from Open Empire** | Daily P&L USD (CashClaw) · Win Rate % (Director) · Lead Pipeline Count (BLCO) · Daily AI Spend USD · Active Ventures · Monthly Passive Revenue USD · Free Kalshi Balance USD |
| **Cross References** | L4: Dashboard · L5: Operational Status · L2: Evidence States |
| **Notes** | KPIs are the primary language of governance reviews. Every active Venture must have at least one revenue-related KPI. KPIs backed by live API data carry Evidence State = Verified. Manually reported KPIs carry Asserted. |

---

### Business Outcome

| Field | Value |
|---|---|
| **Canonical Name** | Business Outcome |
| **Canonical Definition** | A qualitative or quantitative result that Open Empire intends to achieve through the execution of one or more Programs or Ventures — expressed in terms of value delivered, not tasks completed. |
| **Purpose within Open Empire** | Connects execution activity to strategic intent. Prevents activity-tracking from substituting for impact measurement. Every Project and Program must trace to at least one Business Outcome. |
| **Parent Layer** | Layer 1 — Business |
| **Parent Asset** | Portfolio · Program |
| **Child Asset Types** | None |
| **Allowed Relationships** | DELIVERED_BY Program · DELIVERED_BY Venture · VALIDATED_BY Executive KPI · REFERENCED_BY Council |
| **Lifecycle Applicability** | Targeted · Achieved · Missed · Superseded |
| **Required Schema Fields** | `id` · `name` · `description` · `target_date` · `success_criteria[]` · `linked_kpis[]` · `linked_programs[]` · `status` |
| **Validation Rules** | Must have defined `success_criteria[]`. Must be linked to at least one KPI. `status` must be one of four canonical values. Cannot be marked Achieved without all success_criteria confirmed. Missed outcomes must document causal analysis. |
| **Examples from Open Empire** | "$12k–$30k/month passive income within 30 days" (Targeted) · "BLCO first verified sale" (Targeted) · "CashClaw 70%+ win rate" (Targeted) · "Open Empire GitHub repos live and CI green" (Achieved 2026-07-30) |
| **Cross References** | L1: Executive KPI · L2: Council · L5: Business Criticality |
| **Notes** | Business Outcomes are the WHY behind every Project and Program. They must be stated before work begins. The mission "$12k–$30k/month passive within 30 days" is the governing Business Outcome for all current Ventures. |

---

# LAYER 2 — GOVERNANCE

> The authority and accountability layer. Defines who governs what, what rules apply, and how decisions are made and enforced.

---

### Council

| Field | Value |
|---|---|
| **Canonical Name** | Council |
| **Canonical Definition** | A named governance body within Open Empire responsible for decision-making, oversight, and accountability within a defined domain. |
| **Purpose within Open Empire** | Structures multi-agent and human-AI collaborative governance. Each Council owns a specific domain and escalation path. Councils are the institutional memory of governance decisions. |
| **Parent Layer** | Layer 2 — Governance |
| **Parent Asset** | None (governance root — Nathan is the sovereign authority above all Councils) |
| **Child Asset Types** | Executive Roles (assigned to) · Policies (enforced by) · Playbooks (issued through) |
| **Allowed Relationships** | GOVERNS Portfolio · GOVERNS Program · GOVERNS Venture · ASSIGNS Executive Role · ENFORCES Policy · ESCALATES_TO Council (parent council) · REVIEWS Business Outcome |
| **Lifecycle Applicability** | Active · Suspended · Dissolved |
| **Required Schema Fields** | `id` · `name` · `domain` · `members[]` · `chair_role` · `escalation_path` · `policies[]` · `meeting_cadence` · `status` |
| **Validation Rules** | Must have a defined domain. Must have a `chair_role` assigned. Must define an `escalation_path`. Cannot be Dissolved while governing Active assets. Suspended Councils must document the suspension reason. |
| **Examples from Open Empire** | PMO Council · Trading Council · BLCO Council · Security Council · Engineering Council · Portfolio Council |
| **Cross References** | L1: Portfolio, Venture · L2: Executive Roles, Policies · L5: Execution Roles |
| **Notes** | Nathan is the sovereign authority above all Councils. No Council decision may override Nathan's explicit directive. Nathan's approval constitutes an override of any Council decision. |

---

### Executive Role

| Field | Value |
|---|---|
| **Canonical Name** | Executive Role |
| **Canonical Definition** | A named, accountable authority role at the strategic level of Open Empire — assigned to an individual or agent with full decision-making authority within a defined domain. |
| **Purpose within Open Empire** | Ensures clear ownership and accountability at the top of each governance domain. Every domain must have a single accountable Executive Role. |
| **Parent Layer** | Layer 2 — Governance |
| **Parent Asset** | Council |
| **Child Asset Types** | Ownership Roles (report to Executive Role) |
| **Allowed Relationships** | ASSIGNED_TO Council · OWNS Portfolio · OWNS Venture · GOVERNS Policy · ESCALATES_TO Executive Role (higher authority) · CHAIRS Council |
| **Lifecycle Applicability** | Active · Vacant · Delegated · Retired |
| **Required Schema Fields** | `id` · `title` · `domain` · `holder` (human \| agent) · `council_id` · `authority_scope` · `escalation_target` · `status` |
| **Validation Rules** | Must have a named holder. Must define `authority_scope` explicitly. Vacant roles must have an `acting_holder` or `escalation_target`. Delegated roles must document delegation scope and duration. |
| **Examples from Open Empire** | Sovereign Operator (Nathan — no escalation) · Chief of Staff (Alusi) · PMO Director · Trading Director · BLCO Director · Engineering Lead |
| **Cross References** | L2: Council, Ownership Roles · L5: Execution Roles |
| **Notes** | Alusi holds the Chief of Staff Executive Role by design. Nathan holds Sovereign Operator as the ultimate authority with no escalation path. No agent may invoke Opus-level decisions except Alusi. No agent may override Nathan. |

---

### Ownership Role

| Field | Value |
|---|---|
| **Canonical Name** | Ownership Role |
| **Canonical Definition** | A named, accountable operational role responsible for day-to-day stewardship of one or more specific assets — beneath Executive authority but above execution-level task completion. |
| **Purpose within Open Empire** | Bridges Executive direction and Execution-layer task completion. Ensures every governed asset has an identifiable, accountable owner at all times. |
| **Parent Layer** | Layer 2 — Governance |
| **Parent Asset** | Executive Role |
| **Child Asset Types** | None |
| **Allowed Relationships** | REPORTS_TO Executive Role · OWNS Repository · OWNS Service · OWNS Agent · OWNS Workflow · OWNS Database · OWNS Knowledge Base |
| **Lifecycle Applicability** | Active · Delegated · Vacant |
| **Required Schema Fields** | `id` · `title` · `asset_type` · `asset_ids[]` · `holder` (human \| agent) · `executive_role_id` · `status` |
| **Validation Rules** | Must be linked to at least one asset. Cannot be Vacant for Tier-0 assets. Must have an escalation path. Tier-0 asset Ownership Roles may be held by AI agents only when there is human oversight within the Council. |
| **Examples from Open Empire** | Trading System Owner · BLCO Pipeline Owner · Engineering Lead · Operations Manager · Memory Curator · Registry Maintainer |
| **Cross References** | L2: Executive Roles, Council · L4: Service, Agent, Registry |
| **Notes** | Ownership Roles may be held by agents or humans. Where held by agents, Nathan retains override authority in all cases. An unowned Tier-0 asset is a governance violation requiring immediate remediation. |

---

### Standard

| Field | Value |
|---|---|
| **Canonical Name** | Standard |
| **Canonical Definition** | A mandatory, versioned technical or operational specification that all Open Empire assets must comply with — defining HOW something must be done. |
| **Purpose within Open Empire** | Enforces consistency and interoperability across all layers of Open Empire. Standards are not aspirational — they are enforced requirements. |
| **Parent Layer** | Layer 2 — Governance |
| **Parent Asset** | Council (issuing authority) |
| **Child Asset Types** | None |
| **Allowed Relationships** | ENFORCED_BY Council · APPLIED_TO Repository · APPLIED_TO API · APPLIED_TO Database · VALIDATED_BY Verification Method |
| **Lifecycle Applicability** | Draft · Active · Deprecated · Superseded |
| **Required Schema Fields** | `id` · `name` · `version` · `scope` · `requirements[]` · `issuing_council_id` · `effective_date` · `status` · `superseded_by` (if applicable) |
| **Validation Rules** | Must have a version number. Must define scope explicitly. Deprecated Standards must reference their replacement. Active Standards must list at least one Verification Method. Cannot be Deprecated without a superseding Standard. |
| **Examples from Open Empire** | API Naming Standard · Secret Management Standard · PM2 Process Naming Standard · Git Branching Standard · Model Dispatch Standard · Trade Log Integrity Standard |
| **Cross References** | L2: Council, Policies · L3: Repository, API · L5: Verification Methods |
| **Notes** | Standards specify HOW. Policies specify WHAT must happen. This distinction is maintained strictly — a Standard is a technical specification; a Policy is a behavioral rule. Both are mandatory. |

---

### Policy

| Field | Value |
|---|---|
| **Canonical Name** | Policy |
| **Canonical Definition** | A mandatory, enforceable rule governing behavior, decision-making, or operations within Open Empire — defining WHAT must happen, issued by a Council or Executive Role. |
| **Purpose within Open Empire** | Defines the behavioral boundaries within which all agents, humans, and systems must operate. Policies are the rules; Playbooks are the procedures that implement them. |
| **Parent Layer** | Layer 2 — Governance |
| **Parent Asset** | Council |
| **Child Asset Types** | Playbooks (implement Policies) |
| **Allowed Relationships** | ISSUED_BY Council · IMPLEMENTED_BY Playbook · APPLIES_TO Agent · APPLIES_TO Service · APPLIES_TO Automation · ENFORCED_BY Execution Role |
| **Lifecycle Applicability** | Draft · Active · Under Review · Deprecated · Superseded |
| **Required Schema Fields** | `id` · `name` · `version` · `statement` · `scope` · `exceptions[]` · `enforcement_mechanism` · `issuing_council_id` · `effective_date` · `status` |
| **Validation Rules** | Must have a policy statement. Must define scope. Must list enforcement_mechanism. Cannot be Deprecated without a superseding Policy. Exceptions must be explicitly listed — silence implies no exceptions. |
| **Examples from Open Empire** | Draft-First Policy (all external comms require approval before send) · Daily Spend Cap Policy ($10/day per trading Venture) · Approval Gating Policy (sovereign_proxy) · Model Dispatch Policy (Haiku→Ollama→Heuristic) · Geoblocking Compliance Policy |
| **Cross References** | L2: Council, Standards, Playbooks · L5: Approval Types, Risk Levels |
| **Notes** | Policies bind all agents, not just humans. An agent that violates a Policy triggers an audit event. The Draft-First and Spend Cap policies are the two highest-consequence policies currently active — violations have direct financial and reputational risk. |

---

### Playbook

| Field | Value |
|---|---|
| **Canonical Name** | Playbook |
| **Canonical Definition** | A versioned, step-by-step operational procedure that implements one or more Policies — executable by an agent, human, or automated system. |
| **Purpose within Open Empire** | Converts Policy intent into reproducible execution steps. The operational intelligence layer. Playbooks prevent improvisation in high-stakes scenarios. |
| **Parent Layer** | Layer 2 — Governance |
| **Parent Asset** | Policy |
| **Child Asset Types** | None |
| **Allowed Relationships** | IMPLEMENTS Policy · EXECUTED_BY Agent · EXECUTED_BY Execution Role · USES API · USES Service · VALIDATED_BY Verification Method |
| **Lifecycle Applicability** | Draft · Active · Outdated · Deprecated |
| **Required Schema Fields** | `id` · `name` · `version` · `policy_ids[]` · `steps[]` · `prerequisites[]` · `expected_outputs[]` · `owner` · `status` · `last_validated` |
| **Validation Rules** | Must implement at least one Policy. Must have defined `steps[]`. Must have `expected_outputs[]`. Must have a `last_validated` date. Steps must be deterministic and sequentially ordered. |
| **Examples from Open Empire** | Trade Approval Playbook · BLCO Lead Qualification Playbook · Incident Response Playbook · Secret Rotation Playbook · Repository Recovery Playbook (D21) · Agent Onboarding Playbook |
| **Cross References** | L2: Policies, Council · L4: Agent, Automation · L5: Verification Methods |
| **Notes** | OpenClaw Skills are the technical implementation of Playbooks. Every OpenClaw Skill should reference the Playbook it implements. A Playbook without a corresponding Skill is an automation gap to be addressed. |

---

### Approval Type

| Field | Value |
|---|---|
| **Canonical Name** | Approval Type |
| **Canonical Definition** | A categorized class of approval action required before a governed operation may proceed — defining the required authority level, delivery mechanism, and time constraints. |
| **Purpose within Open Empire** | Provides a taxonomy of authorization gates that all agents and systems must respect. Every external action, financial operation, and high-risk change must pass through a defined Approval Type. |
| **Parent Layer** | Layer 2 — Governance |
| **Parent Asset** | Policy |
| **Child Asset Types** | None |
| **Allowed Relationships** | REQUIRED_BY Policy · GRANTED_BY Executive Role · IMPLEMENTED_BY Service (sovereign_proxy) · APPLIES_TO Agent · APPLIES_TO Automation |
| **Lifecycle Applicability** | Active · Deprecated |
| **Required Schema Fields** | `id` · `name` · `authority_level` · `mechanism` (telegram \| openclaw_native \| n8n \| manual) · `timeout_seconds` · `escalation_on_timeout` · `applies_to[]` |
| **Validation Rules** | Must define `authority_level`. Must specify `mechanism`. Must define `timeout_seconds`. Must define `escalation_on_timeout` behavior. Timeout without response escalates — it does not auto-approve. |
| **Examples from Open Empire** | Financial Approval (Nathan only, Telegram, 300s timeout) · External Send Approval (Nathan only) · Agent Deploy Approval (PMO Council) · Config Change Approval (Engineering Council) · Emergency Spend Override (Nathan only, immediate) |
| **Cross References** | L2: Policies, Council · L4: Automation, Agent · sovereign_proxy Service |
| **Notes** | Financial Approvals are absolute: no autonomous spend above the daily_spend_cap without explicit Nathan approval. Timeout does not equal approval — a timed-out approval request is automatically rejected and logged. |

---

### Risk Level

| Field | Value |
|---|---|
| **Canonical Name** | Risk Level |
| **Canonical Definition** | A standardized severity classification applied to assets, operations, and decisions — quantifying potential business impact if a failure, breach, or adverse event occurs. |
| **Purpose within Open Empire** | Enables consistent, risk-based decision-making and prioritization. Every asset and every change carries an explicit risk level — no implicit or assumed risk assessment. |
| **Parent Layer** | Layer 2 — Governance |
| **Parent Asset** | Council (defines) · Policy (references) |
| **Child Asset Types** | None |
| **Allowed Relationships** | APPLIED_TO Project · APPLIED_TO Agent · APPLIED_TO Service · APPLIED_TO Automation · DETERMINES Approval Type · DETERMINES Recovery Priority |
| **Lifecycle Applicability** | Active (canonical enumeration — not subject to individual lifecycle) |
| **Required Schema Fields** | `id` (P0–P4) · `name` · `description` · `response_sla_minutes` · `approval_required` · `escalation_path` |
| **Validation Rules** | Must be one of five canonical levels only. Must map to a `response_sla_minutes`. P0 and P1 levels require explicit escalation paths. Risk levels are assigned — never defaulted or left blank. |
| **Examples from Open Empire** | P0 (Critical): CashClaw live trading failure, ClawDB down, OpenClaw gateway down · P1 (High): BLCO pipeline failure, Telegram adapter down · P2 (Medium): Dashboard unavailable, Grafana down · P3 (Low): Report formatting error · P4 (Negligible): Log verbosity excess |
| **Cross References** | L2: Approval Types, Policy · L5: Recovery Priority, Business Criticality |
| **Notes** | Risk Levels are enumerated constants — P0 through P4 only. No free-text risk descriptions. Every asset in the Registry must carry an explicit `risk_level` field. |

---

### Lifecycle State

| Field | Value |
|---|---|
| **Canonical Name** | Lifecycle State |
| **Canonical Definition** | A standardized enumeration of states that an Open Empire asset may occupy, from inception through retirement — providing the universal state machine for all asset types. |
| **Purpose within Open Empire** | Enables consistent status tracking and transition governance across all asset types. Every asset is always in exactly one Lifecycle State. Transitions are governed events, not silent updates. |
| **Parent Layer** | Layer 2 — Governance |
| **Parent Asset** | Council (governance authority for transitions) |
| **Child Asset Types** | None |
| **Allowed Relationships** | APPLIED_TO all asset types · TRANSITIONS governed by Policy and Approval Type · VISUALIZED_BY Dashboard |
| **Lifecycle Applicability** | Active (this entry IS the lifecycle definition — it does not itself have a lifecycle) |
| **Required Schema Fields** | Each asset must carry: `status` (string, constrained to asset-type allowed states) · `status_changed_at` · `status_changed_by` |
| **Validation Rules** | Each asset type defines its own allowed state set (documented in its Lifecycle Applicability field). State transitions must be logged with actor and timestamp. Terminal states (Archived, Retired, Cancelled, Closed) require explicit approval. Undocumented transitions are governance violations. |
| **Examples from Open Empire** | Project: Planned→In Progress→Blocked→Complete→Archived · Service: Planned→Staging→Active→Degraded→Retired · Agent: Draft→Testing→Active→Suspended→Retired · Venture: Pre-Launch→Active→Scaling→On Hold→Winding Down→Closed |
| **Cross References** | L6: Current State, Target State, Retirement State · L2: Approval Types |
| **Notes** | The Lifecycle State taxonomy is master-governed here. Every asset type's Lifecycle Applicability field draws its valid states from this definition. No asset may invent states outside this master set without a Taxonomy minor version update. |

---

### Evidence State

| Field | Value |
|---|---|
| **Canonical Name** | Evidence State |
| **Canonical Definition** | A standardized classification of the verification status of a fact, claim, metric, or operational condition within Open Empire — indicating how well-supported the information is. |
| **Purpose within Open Empire** | Prevents unverified data from being treated as ground truth. Enforces epistemic discipline across all reports, KPIs, and operational decisions. |
| **Parent Layer** | Layer 2 — Governance |
| **Parent Asset** | Policy (evidence requirements) · Council (verification authority) |
| **Child Asset Types** | None |
| **Allowed Relationships** | APPLIED_TO Executive KPI · APPLIED_TO Business Outcome · APPLIED_TO Operational Status · VERIFIED_BY Verification Method |
| **Lifecycle Applicability** | Active (canonical enumeration — not subject to individual lifecycle) |
| **Required Schema Fields** | Each reportable asset must carry: `evidence_state` (Verified \| Asserted \| Estimated \| Unverified \| Stale) · `evidence_source` · `evidence_timestamp` |
| **Validation Rules** | **Verified** = machine-confirmed with timestamped source. **Asserted** = human-stated without independent confirmation. **Estimated** = calculated from proxy data. **Unverified** = no confirmation attempted. **Stale** = confirmed at time T but not refreshed within SLA. Stale KPIs must not be used in financial decisions. |
| **Examples from Open Empire** | Kalshi balance $1.55 → Verified (API query 2026-07-31) · BLCO leads 630 → Asserted (not re-scraped since last count) · CashClaw win rate 0% → Verified (zero trades placed, confirmed via trades.jsonl) · Polymarket balance $0.06 → Verified (API query 2026-08-02) |
| **Cross References** | L2: Verification Methods · L5: Operational Status |
| **Notes** | This is especially critical for financial balances. A balance that hasn't been queried within 15 minutes is Stale for live trading decisions. Evidence State propagates upward — a Dashboard metric is only as good as the evidence_state of its source KPI. |

---

# LAYER 3 — ENGINEERING

> The technical foundation layer. Defines the code, infrastructure, integrations, and AI models that implement Open Empire's capabilities.

---

### Repository

| Field | Value |
|---|---|
| **Canonical Name** | Repository |
| **Canonical Definition** | A version-controlled code storage unit (Git repository) containing the source of one or more Open Empire services, libraries, agents, or configurations. |
| **Purpose within Open Empire** | The fundamental unit of code ownership and version management. Every piece of code that matters to Open Empire lives in a tracked Repository. |
| **Parent Layer** | Layer 3 — Engineering |
| **Parent Asset** | Project (producing project) or Program (long-term codebase) |
| **Child Asset Types** | Package · Library |
| **Allowed Relationships** | CONTAINS Package · CONTAINS Library · DEPLOYS_TO Service · OWNED_BY Ownership Role · GOVERNED_BY Standard · HOSTED_ON Infrastructure |
| **Lifecycle Applicability** | Active · Archived · Deprecated |
| **Required Schema Fields** | `id` · `name` · `github_org` · `github_repo` · `visibility` (private \| public) · `default_branch` · `tier` (T0 \| T1 \| T2 \| T3) · `owner_role_id` · `ci_status` · `last_commit_at` · `git_initialized` (bool) · `remote_url` · `status` |
| **Validation Rules** | Must define `tier`. Tier-0 Repos must have a remote configured and `git_initialized=true`. Must have an `owner_role_id`. CI status must be tracked for T0 and T1 repos. Uninitialized T0 repos are a governance violation. |
| **Examples from Open Empire** | UA4200/trading (T0, ⚠️ no git init — pending D21 remediation) · UA4200/alusi-core (T0, CI green) · UA4200/antfarm (T1, CI green) · UA4200/mission-control (T1, CI green) · UA4200/blco-pipeline (T1) |
| **Cross References** | L3: Package, Library · L4: Service · L6: Versioning, Change Control |
| **Notes** | Repository tier determines backup priority, CI requirements, and recovery SLAs. The trading/ directory is T0-critical but currently has no git initialization (D21). This is the highest-priority engineering debt in the current backlog. |

---

### Package

| Field | Value |
|---|---|
| **Canonical Name** | Package |
| **Canonical Definition** | A distributable, versioned module within a Repository that can be imported or installed as a discrete unit of functionality. |
| **Purpose within Open Empire** | The distributable unit of code. Packages define importable boundaries — the contract between code modules. |
| **Parent Layer** | Layer 3 — Engineering |
| **Parent Asset** | Repository |
| **Child Asset Types** | Library (contained within Package) |
| **Allowed Relationships** | CONTAINED_IN Repository · IMPORTS Library · USED_BY Service · USED_BY Agent · PUBLISHED_TO Registry |
| **Lifecycle Applicability** | Stable · Beta · Deprecated · Yanked |
| **Required Schema Fields** | `id` · `name` · `version` · `repository_id` · `runtime` (python \| node \| other) · `entry_point` · `dependencies[]` · `status` |
| **Validation Rules** | Must have a semantic version. Must define `runtime`. Must list `dependencies[]`. Yanked packages must be replaced in all consuming services within 24 hours. Deprecated packages trigger a P1 alert if still consumed by Active services. |
| **Examples from Open Empire** | `trading` (Python 3.13 package, canonical entry: `trading.agents.director.run`) · `antfarm` (Node 24 package) · `alusi-core` (Node 24 package) |
| **Cross References** | L3: Repository, Library · L4: Service, Agent |
| **Notes** | Python packages in Open Empire must be importable via their canonical path (e.g., `trading.agents.director.run`). Path drift between the PM2 ecosystem config and the actual module path causes startup failures — this was the root cause of multiple 2026-07-30 crash loops. |

---

### Library

| Field | Value |
|---|---|
| **Canonical Name** | Library |
| **Canonical Definition** | A reusable module of shared code providing discrete, composable functionality — imported by other packages or services but not independently deployable. |
| **Purpose within Open Empire** | Encapsulates shared logic to prevent duplication across the codebase. The DRY (Don't Repeat Yourself) enforcement unit in the Engineering layer. |
| **Parent Layer** | Layer 3 — Engineering |
| **Parent Asset** | Package or Repository |
| **Child Asset Types** | None |
| **Allowed Relationships** | CONTAINED_IN Package · IMPORTED_BY Service · IMPORTED_BY Agent · IMPORTED_BY Automation · IMPLEMENTS Standard |
| **Lifecycle Applicability** | Active · Deprecated · Superseded |
| **Required Schema Fields** | `id` · `name` · `version` · `package_id` · `module_path` · `public_api[]` · `status` |
| **Validation Rules** | Must define `module_path`. Must list `public_api[]`. Cannot be marked Active if `module_path` is unreachable. Deprecated libraries must list all consuming assets with migration timelines. |
| **Examples from Open Empire** | `trading.shared.signals` · `trading.shared.kelly` · `trading.shared.risk` · `trading.shared.logging` |
| **Cross References** | L3: Package, Framework · L4: Agent, Service |
| **Notes** | **KELLY NO-FIX**: `trading.shared.kelly` (kelly.py) is preserved verbatim as an explicit Change Control decision. Do not refactor. This constraint is enforced at the Library level and must not be overridden by any agent without Nathan's explicit directive. |

---

### Framework

| Field | Value |
|---|---|
| **Canonical Name** | Framework |
| **Canonical Definition** | A foundational software system that provides structure, conventions, and core capabilities upon which Open Empire services and agents are built. |
| **Purpose within Open Empire** | Defines the platform contracts that all services must respect. Abstracts infrastructure concerns from application logic. Framework upgrades are high-risk events requiring Change Control. |
| **Parent Layer** | Layer 3 — Engineering |
| **Parent Asset** | None (infrastructure-level — no parent in Open Empire architecture) |
| **Child Asset Types** | Library · Package (built on Framework) |
| **Allowed Relationships** | PROVIDES_STRUCTURE_FOR Service · PROVIDES_STRUCTURE_FOR Agent · DEFINED_BY Standard · HOSTED_ON Infrastructure |
| **Lifecycle Applicability** | Active · Deprecated · Upgrading |
| **Required Schema Fields** | `id` · `name` · `version` · `runtime` · `purpose` · `consuming_assets[]` · `upgrade_policy` · `status` |
| **Validation Rules** | Must define `upgrade_policy`. Must list `consuming_assets[]`. Major version upgrades require Change Control approval. A Framework in Upgrading state must have a rollback plan. |
| **Examples from Open Empire** | PM2 (process management framework) · n8n (workflow automation framework) · OpenClaw (agent runtime framework) · PostgreSQL (data persistence framework) · FastAPI / Express (API frameworks) |
| **Cross References** | L3: Infrastructure, Environment · L4: Runtime, Service |
| **Notes** | Framework upgrades cascade across all consuming assets. Before any Framework version change, a full impact analysis across `consuming_assets[]` is required. This applies especially to OpenClaw and PM2 version upgrades. |

---

### Model

| Field | Value |
|---|---|
| **Canonical Name** | Model |
| **Canonical Definition** | An AI/ML model — identified by provider, name, and version — used by Open Empire agents and services for inference, classification, generation, or scoring. |
| **Purpose within Open Empire** | The intelligence substrate of Open Empire. Governs which AI capabilities are available at what cost, latency, and quality. Model selection is a governed decision, not an ad-hoc choice. |
| **Parent Layer** | Layer 3 — Engineering |
| **Parent Asset** | Model Provider |
| **Child Asset Types** | None |
| **Allowed Relationships** | PROVIDED_BY Model Provider · USED_BY Agent · USED_BY Service · GOVERNED_BY Policy (Model Dispatch Policy) · ROUTED_BY Router |
| **Lifecycle Applicability** | Available · Deprecated · Unavailable · Rate-Limited |
| **Required Schema Fields** | `id` · `name` · `provider_id` · `version` · `context_window` · `cost_per_1k_input_usd` · `cost_per_1k_output_usd` · `latency_class` (real-time \| batch) · `use_cases[]` · `status` |
| **Validation Rules** | Must reference a Model Provider. Must define cost fields. Must define `latency_class`. Use must comply with the Model Dispatch Policy. Models may not be added to real-time chains without explicit approval. |
| **Examples from Open Empire** | `anthropic/claude-sonnet-4-6` (primary, Alusi) · `anthropic/claude-haiku-4-5` (signal scoring, real-time) · `ollama/qwen2.5:3b` (local batch) · `ollama/tinyllama` (monitoring, $0) · `ollama/llama3.2:3b` (local analysis) |
| **Cross References** | L3: Model Provider, Router · L2: Model Dispatch Policy · L4: Agent |
| **Notes** | GPT-4o was removed from the signal scoring chain on 2026-08-02. The canonical scoring chain is: **Haiku → Ollama → Heuristic**. This chain is locked. Do not reinsert external models into real-time scoring without Nathan's explicit directive. |

---

### Model Provider

| Field | Value |
|---|---|
| **Canonical Name** | Model Provider |
| **Canonical Definition** | An organization or local system that hosts and serves one or more AI Models accessible to Open Empire via API or local inference endpoint. |
| **Purpose within Open Empire** | Governs the authentication, billing, and availability contracts for all AI inference in Open Empire. Every model is traceable to exactly one Model Provider. |
| **Parent Layer** | Layer 3 — Engineering |
| **Parent Asset** | None |
| **Child Asset Types** | Model |
| **Allowed Relationships** | HOSTS Model · AUTHENTICATED_VIA Secret Metadata · BILLED_TO Venture (cost center) · MONITORED_BY Service (cost sentinel) |
| **Lifecycle Applicability** | Active · Degraded · Unavailable |
| **Required Schema Fields** | `id` · `name` · `api_endpoint` · `auth_type` · `models[]` · `billing_account` · `daily_cost_cap_usd` · `status` |
| **Validation Rules** | Must define `auth_type`. Must define `daily_cost_cap_usd`. API credentials must be stored in Secret Metadata — never hardcoded in any asset. Provider degradation triggers fallback routing per Model Dispatch Policy. |
| **Examples from Open Empire** | Anthropic (Claude family, primary paid provider) · Ollama (local, port 11434, 6 models, $0 cost) · OpenAI (GPT family, limited use — requires approval and cost justification) |
| **Cross References** | L3: Model · L3: Secret Metadata · L2: Model Dispatch Policy |
| **Notes** | Ollama is cost-free (local CPU inference). Anthropic is the primary paid provider. OpenAI use is restricted — requires explicit approval and documented cost justification before activation. Daily AI spend target for autonomous ops: <$0.20. |

---

### API

| Field | Value |
|---|---|
| **Canonical Name** | API |
| **Canonical Definition** | A versioned programmatic interface — exposed by a service or external system — that Open Empire consumes or publishes, defining the data contract and behavioral guarantees between systems. |
| **Purpose within Open Empire** | The integration contract. Every cross-system communication channel is formalized as an API. APIs are versioned, monitored, and governed. Version drift is a critical failure mode. |
| **Parent Layer** | Layer 3 — Engineering |
| **Parent Asset** | Service (exposing) or Integration (consuming external API) |
| **Child Asset Types** | None |
| **Allowed Relationships** | EXPOSED_BY Service · CONSUMED_BY Integration · CONSUMED_BY Agent · GOVERNS_CONTRACT_FOR Integration · DOCUMENTED_BY Standard |
| **Lifecycle Applicability** | Active · Deprecated · Breaking-Change-Pending · Retired |
| **Required Schema Fields** | `id` · `name` · `version` · `base_url` · `auth_type` · `endpoints[]` · `rate_limits` · `status` · `breaking_change_policy` |
| **Validation Rules** | Must define `version`. Must list `endpoints[]`. Must define `rate_limits`. Deprecated APIs must list migration target. Breaking changes require Change Control and a migration plan before deployment. Consuming assets must be pinned to a specific version. |
| **Examples from Open Empire** | Kalshi V2 API (RSA-PSS signed, /portfolio/events/orders) · Polymarket US API (Ed25519 signed, api.polymarket.us) · Anthropic API (Claude) · Telegram Bot API · n8n Webhook API · OpenClaw Gateway API (port 8787) |
| **Cross References** | L3: Integration, Router · L4: Service, Agent · L6: Schema Evolution |
| **Notes** | The Kalshi V1→V2 migration (2026-07-30) demonstrates the consequences of API version drift — the deprecated V1 returned 410 errors and blocked all trading. All APIs must be pinned, monitored, and have an explicit deprecation watch. |

---

### Router

| Field | Value |
|---|---|
| **Canonical Name** | Router |
| **Canonical Definition** | A system component that inspects incoming requests or signals and routes them to the appropriate handler, model, or service based on defined, ordered rules. |
| **Purpose within Open Empire** | Decouples routing logic from processing logic. Enables policy-based dispatch, deterministic fallback chains, and load distribution without changing application code. |
| **Parent Layer** | Layer 3 — Engineering |
| **Parent Asset** | Framework or Service |
| **Child Asset Types** | None |
| **Allowed Relationships** | ROUTES_TO Model · ROUTES_TO Service · ROUTES_TO Agent · IMPLEMENTS Policy (routing policy) · CONSUMES API |
| **Lifecycle Applicability** | Active · Degraded · Misconfigured |
| **Required Schema Fields** | `id` · `name` · `type` (model_router \| message_router \| request_router \| approval_router) · `rules[]` · `fallback_target` · `status` |
| **Validation Rules** | Must define at least one routing rule. Must define a `fallback_target`. Routing rules must be ordered and deterministic — no ambiguous routing. Misconfigured routers must be flagged immediately. |
| **Examples from Open Empire** | OpenClaw model router (Haiku→Ollama→Heuristic fallback chain) · Telegram message router · n8n workflow router · sovereign_proxy approval router |
| **Cross References** | L3: Model, API · L4: Service, Automation |
| **Notes** | The signal scoring router chain (Haiku→Ollama→Heuristic) must remain in this exact sequence per the 2026-08-02 directive. This is an active governance constraint, not a preference. |

---

### Integration

| Field | Value |
|---|---|
| **Canonical Name** | Integration |
| **Canonical Definition** | A configured connection between Open Empire and an external system — encapsulating authentication, data mapping, error handling, and circuit-breaking for a specific external API or data source. |
| **Purpose within Open Empire** | Makes every external dependency a governed asset. Each Integration is a single point of failure risk that must be monitored, documented, and protected. |
| **Parent Layer** | Layer 3 — Engineering |
| **Parent Asset** | Service (owner) or Program (consuming) |
| **Child Asset Types** | None |
| **Allowed Relationships** | CONSUMES API · OWNED_BY Service · AUTHENTICATED_VIA Secret Metadata · GOVERNED_BY Policy · PRODUCES data_for Service |
| **Lifecycle Applicability** | Active · Degraded · Broken · Deprecated |
| **Required Schema Fields** | `id` · `name` · `external_system` · `api_id` · `auth_type` · `secret_metadata_id` · `data_flow_direction` (inbound \| outbound \| bidirectional) · `error_handling` · `circuit_breaker` (bool) · `status` |
| **Validation Rules** | Must reference a Secret Metadata entry (never store credentials inline). Must define `error_handling`. Must define `data_flow_direction`. Broken integrations trigger a P1 alert within 60 seconds. All Tier-0 integrations must have `circuit_breaker=true`. |
| **Examples from Open Empire** | Kalshi Integration (RSA-PSS trading, T0) · Polymarket US Integration (Ed25519 trading, T0) · Telegram Integration (messaging, T0) · n8n Webhook Integration (approvals, T0) · GitHub Integration (CI/CD, T1) |
| **Cross References** | L3: API, Secret Metadata · L4: Service, Automation |
| **Notes** | Each Integration is a governed dependency. Every trading integration carries its own circuit breaker. When the Kalshi circuit opens, the director halts and alerts — it does not retry indefinitely. |

---

### Environment

| Field | Value |
|---|---|
| **Canonical Name** | Environment |
| **Canonical Definition** | A named, isolated runtime context in which Open Empire services operate — distinguishing between local development, staging, and production deployments with scoped configurations and secrets. |
| **Purpose within Open Empire** | Prevents contamination between test and live systems. Ensures secrets, configs, and data are always environment-scoped and never bleed between contexts. |
| **Parent Layer** | Layer 3 — Engineering |
| **Parent Asset** | Infrastructure |
| **Child Asset Types** | Service (deployed within) · Agent (running within) |
| **Allowed Relationships** | HOSTS Service · HOSTS Agent · USES Secret Metadata (environment-scoped) · GOVERNS_SCOPE_OF Database · GOVERNS_SCOPE_OF Storage |
| **Lifecycle Applicability** | Active · Decommissioned |
| **Required Schema Fields** | `id` · `name` · `type` (development \| staging \| production \| local) · `host` · `services[]` · `secrets_scope` · `status` |
| **Validation Rules** | Must define `type` — one of four canonical values only. Production environments must have an explicit `secrets_scope`. Staging environments must not use production secrets — this is an absolute rule. |
| **Examples from Open Empire** | Production (Ugos-Mac-mini, ~/.openclaw/) · Staging (open-empire-federation-staging PM2 id=45, open-empire-lifecycle-staging PM2 id=46) · Local (developer overrides) |
| **Cross References** | L3: Infrastructure, Secret Metadata · L4: Service, Runtime |
| **Notes** | The canonical production environment is Ugos-Mac-mini (NeoOC). All PM2-managed production services run here. Staging environments write to staging-scoped state files (latest_federation_state.json, latest_lifecycle_state.json). |

---

### Infrastructure

| Field | Value |
|---|---|
| **Canonical Name** | Infrastructure |
| **Canonical Definition** | The physical or virtual compute, network, and storage resources that host Open Empire environments and services — the foundational physical layer. |
| **Purpose within Open Empire** | Defines hardware constraints, availability characteristics, and hosting decisions. Infrastructure limits bound all service capacity planning. |
| **Parent Layer** | Layer 3 — Engineering |
| **Parent Asset** | None (physical root) |
| **Child Asset Types** | Environment · Database · Storage |
| **Allowed Relationships** | HOSTS Environment · PROVIDES Database · PROVIDES Storage · GOVERNED_BY Policy (Security Policy) |
| **Lifecycle Applicability** | Active · Degraded · Maintenance · Decommissioned |
| **Required Schema Fields** | `id` · `name` · `type` (mac_mini \| cloud_vps \| container \| managed_service) · `host_identifier` · `os` · `cpu` · `ram_gb` · `network_posture` · `status` |
| **Validation Rules** | Must define `type`. Production infrastructure must be loopback-bound unless explicitly opened with Nathan approval. Security posture must be documented and current. |
| **Examples from Open Empire** | Ugos-Mac-mini (Intel Mac Mini, macOS 12.7.6, x64, primary production host, all services loopback-bound) · GitHub Actions (CI/CD, cloud) |
| **Cross References** | L3: Environment, Database · L2: Security Policy |
| **Notes** | All services are loopback-bound (127.0.0.1) per Security Posture policy. CVE-2026-25253 mitigation is active. No public internet exposure without explicit Nathan approval. The Intel CPU limitation means Ollama inference is 2-8 tok/s warm — plan accordingly. |

---

### Database

| Field | Value |
|---|---|
| **Canonical Name** | Database |
| **Canonical Definition** | A managed persistent data store used by Open Empire services — identified by engine, version, host, and logical schema — for structured, queryable data persistence. |
| **Purpose within Open Empire** | The persistent structured state layer. Governs all data that must survive process restarts and be queryable across services. |
| **Parent Layer** | Layer 3 — Engineering |
| **Parent Asset** | Infrastructure |
| **Child Asset Types** | None |
| **Allowed Relationships** | HOSTED_ON Infrastructure · ACCESSED_BY Service · ACCESSED_BY Agent · GOVERNED_BY Standard (schema standard) · BACKED_UP_BY Automation |
| **Lifecycle Applicability** | Active · Migrating · Degraded · Retired |
| **Required Schema Fields** | `id` · `name` · `engine` · `version` · `host` · `port` · `database_name` · `schemas[]` · `owner_role_id` · `backup_policy` · `status` |
| **Validation Rules** | Must define `engine` and `version`. Must have a `backup_policy`. Schema changes require Change Control. Tier-0 databases must have automated backup. Degraded state triggers P0 alert. |
| **Examples from Open Empire** | clawdb (PostgreSQL 18.3, port 5432, PM2 id=43, `clawdb` database — operational 2026-07-30 post LC_ALL fix) |
| **Cross References** | L3: Infrastructure, Storage · L4: Service · L6: Schema Evolution |
| **Notes** | PostgreSQL (clawdb) is Tier-0. Recovery priority: P1 (first database, second gateway). Trading agents cannot log without it. The LC_ALL fix was critical — locale mismatch caused startup failure. Monitor locale settings on any Infrastructure update. |

---

### Storage

| Field | Value |
|---|---|
| **Canonical Name** | Storage |
| **Canonical Definition** | A file-based or object-based data persistence layer used for non-relational data — logs, documents, media, exports, and raw data files. |
| **Purpose within Open Empire** | Governs all unstructured and semi-structured data storage. Complements Database for structured data. Critical for audit trails and P&L verification. |
| **Parent Layer** | Layer 3 — Engineering |
| **Parent Asset** | Infrastructure |
| **Child Asset Types** | None |
| **Allowed Relationships** | HOSTED_ON Infrastructure · WRITTEN_BY Service · WRITTEN_BY Agent · READ_BY Service · MANAGED_BY Automation (backup / cleanup) |
| **Lifecycle Applicability** | Active · Archiving · Full · Retired |
| **Required Schema Fields** | `id` · `name` · `type` (filesystem \| s3 \| object_store) · `root_path` · `retention_policy` · `owner_role_id` · `access_permissions` · `immutable` (bool) · `status` |
| **Validation Rules** | Must define `root_path`. Must define `retention_policy`. Sensitive storage must define `access_permissions`. Trade log storage must have `immutable=true`. Storage marked Full triggers P1 alert. |
| **Examples from Open Empire** | `~/.openclaw/trading/data/` (trade logs, immutable append-only) · `~/.openclaw/logs/` (system logs) · `~/.openclaw/vault/` (governance vault) · `~/.openclaw/memory/` (memory stores) · `~/.openclaw/blco/` (BLCO pipeline data) |
| **Cross References** | L3: Database, Infrastructure · L4: Memory Store · L6: Drift Detection |
| **Notes** | Trade log files (trades.jsonl, arb_cycle.jsonl) are the source of truth for P&L auditing. They must not be deleted, modified, or truncated without P0 approval. These are immutable records. |

---

### Secret Metadata

| Field | Value |
|---|---|
| **Canonical Name** | Secret Metadata |
| **Canonical Definition** | A governance record describing a secret (API key, private key, credential) — containing everything EXCEPT the secret value itself — used for lifecycle tracking, rotation management, and audit. |
| **Purpose within Open Empire** | Enables secret lifecycle management without exposing secret values. Governs every credential Open Empire relies on. Every Integration's auth lives here — as a reference, not a value. |
| **Parent Layer** | Layer 3 — Engineering |
| **Parent Asset** | None (cross-layer governance primitive) |
| **Child Asset Types** | None |
| **Allowed Relationships** | DESCRIBES secret_in (Integration · Service · Agent) · STORED_IN `~/.openclaw/secrets/.env` · GOVERNED_BY Policy (Secret Management Policy) · ROTATED_BY Playbook |
| **Lifecycle Applicability** | Active · Rotating · Expired · Revoked |
| **Required Schema Fields** | `id` · `name` · `type` (api_key \| private_key \| oauth_token \| webhook_secret) · `associated_system` · `environment` · `rotation_policy` · `last_rotated_at` · `expiry_at` (if applicable) · `status` |
| **Validation Rules** | Must NOT contain the actual secret value — governance record only. Must define `rotation_policy`. Must link to at least one consuming asset. Expired secrets trigger immediate P0 alert. Revoked secrets must be removed from all consuming assets within 1 hour. |
| **Examples from Open Empire** | KALSHI_API_KEY metadata · ANTHROPIC_API_KEY metadata · POLY_PRIVATE_KEY metadata (Ed25519) · TELEGRAM_BOT_TOKEN metadata · KALSHI_RSA_PRIVATE_KEY metadata |
| **Cross References** | L3: Integration, API · L2: Secret Management Policy · L5: Verification Methods |
| **Notes** | Canonical secrets file: `~/.openclaw/secrets/.env`. No secrets may be hardcoded in any Repository, Playbook, or governance document. Secret values are never written into Taxonomy, Registry, Schema, or any document other than the canonical .env file. |

---

# LAYER 4 — OPERATIONS

> The live execution layer. Defines what is running, how it is managed, and what operational intelligence and assets support Open Empire's daily operation.

---

### Runtime

| Field | Value |
|---|---|
| **Canonical Name** | Runtime |
| **Canonical Definition** | The active execution environment in which a Service or Agent operates at a given moment — including process, interpreter, memory state, and loaded configuration. |
| **Purpose within Open Empire** | Bridges static code (Engineering layer) with live operation. A Runtime is an instantiation of a Package in a specific Environment. |
| **Parent Layer** | Layer 4 — Operations |
| **Parent Asset** | Environment |
| **Child Asset Types** | Service (running within) · PM2 Process (managing) |
| **Allowed Relationships** | INSTANTIATES Package · MANAGED_BY PM2 Process · RUNS_IN Environment · REPORTS Operational Status |
| **Lifecycle Applicability** | Running · Starting · Stopped · Crashed · Restarting |
| **Required Schema Fields** | `id` · `name` · `environment_id` · `package_id` · `interpreter` (python3.13 \| node24 \| other) · `pid` · `uptime_seconds` · `memory_mb` · `status` |
| **Validation Rules** | Must reference an Environment. Must have an active `pid` when `status=Running`. Crashed runtimes must trigger alert within 60 seconds. `pid` must be verified — stale PIDs are a drift condition. |
| **Examples from Open Empire** | trading/director runtime (Python 3.13, venv313) · antfarm CLI runtime (Node 24) · OpenClaw gateway runtime (Node 24, port 8787) · Ollama runtime (port 11434) |
| **Cross References** | L3: Package, Environment · L4: PM2 Process, Service |
| **Notes** | Python `venv313` is the canonical virtual environment for all trading agents. Do not run trading agents outside `venv313`. Environment mismatch was a root cause of multiple crash loops on 2026-07-30. |

---

### Service

| Field | Value |
|---|---|
| **Canonical Name** | Service |
| **Canonical Definition** | A long-running, named operational process that provides continuous capability to Open Empire — independently deployable, monitored, and owned. |
| **Purpose within Open Empire** | The primary operational unit. A Service is what runs, what fails, and what gets monitored. Everything that must stay alive is a Service. |
| **Parent Layer** | Layer 4 — Operations |
| **Parent Asset** | Program (logical) · PM2 Process (physical management) |
| **Child Asset Types** | None (consumes Engineering layer assets) |
| **Allowed Relationships** | MANAGED_BY PM2 Process · EXPOSES API · CONSUMES Integration · USES Database · USES Model · OWNED_BY Ownership Role · GOVERNED_BY Policy |
| **Lifecycle Applicability** | Planned · Staging · Active · Degraded · Stopped · Retired |
| **Required Schema Fields** | `id` · `name` · `pm2_id` · `port` (if applicable) · `tier` · `owner_role_id` · `health_check_url` · `restart_policy` · `status` · `last_restart_at` |
| **Validation Rules** | Must have a `pm2_id`. Must define `tier`. Tier-0 Services must have a `health_check_url`. Must define `restart_policy`. Degraded state triggers alert within 60 seconds for Tier-0. |
| **Examples from Open Empire** | alusi-gateway (pm2 id=2, port 8787, T0) · clawdb (pm2 id=43, port 5432, T0) · mission-control (pm2 id=17, port 3333, T1) · Ollama (pm2 id=24, port 11434, T1) · sovereign_proxy (T0) |
| **Cross References** | L3: Repository, API · L4: PM2 Process, Runtime · L5: Operational Status, Recovery Priority |
| **Notes** | A Service is the long-lived operational form of a Project deliverable. When a Project completes and its output must keep running, it becomes a Service. A Service that cannot auto-restart requires a manual recovery procedure per the Incident Response Playbook. |

---

### PM2 Process

| Field | Value |
|---|---|
| **Canonical Name** | PM2 Process |
| **Canonical Definition** | A specific process instance managed by the PM2 process manager — identified by PM2 numeric id, name, and ecosystem config — responsible for starting, monitoring, and restarting a Service. |
| **Purpose within Open Empire** | The operational lifecycle manager for all Node.js and Python services on Open Empire's primary host. PM2 is the deployment substrate for all production services. |
| **Parent Layer** | Layer 4 — Operations |
| **Parent Asset** | Service |
| **Child Asset Types** | None |
| **Allowed Relationships** | MANAGES Service · DEFINED_IN ecosystem config (`.cjs`) · RUNS_ON Infrastructure · MONITORED_BY Dashboard (Grafana, Mission Control) |
| **Lifecycle Applicability** | Online · Stopped · Errored · Restarting |
| **Required Schema Fields** | `id` (PM2 numeric id) · `name` · `script` · `args[]` · `cwd` · `interpreter` · `env{}` · `restart_policy` · `cron_restart` (if applicable) · `status` |
| **Validation Rules** | Must have a unique PM2 numeric id. Must define `script`. Must define `restart_policy`. `cron_restart` must be valid cron syntax if used. `env{}` must not contain raw secret values — must reference `.env` file. PM2 IDs are never reused after deletion. |
| **Examples from Open Empire** | cashclaw_director (id=38, 5min cycle) · cashclaw_arb (id=39, 5min cycle) · polymarket-trader (id=40, 15min cycle) · trading_sentinel (id=41, 5min cycle) · clawdb (id=43) · alusi-gateway (id=2) |
| **Cross References** | L4: Service, Runtime · L3: Infrastructure, Environment |
| **Notes** | The AGENTS.md registry is the canonical reference for PM2 IDs and their associated services. PM2 IDs are not reused — when a process is removed and a new one created, it receives the next available sequential ID. |

---

### Workflow

| Field | Value |
|---|---|
| **Canonical Name** | Workflow |
| **Canonical Definition** | A defined, multi-step automated process — with explicit triggers, sequenced steps, branching logic, and completion criteria — that orchestrates multiple services or agents toward a business outcome. |
| **Purpose within Open Empire** | Coordinates complex multi-step operations that span multiple services or agents. Higher-order than a single Automation. Workflows are the operational expression of Playbooks. |
| **Parent Layer** | Layer 4 — Operations |
| **Parent Asset** | Program or Automation Framework (n8n, antfarm) |
| **Child Asset Types** | Automation (individual steps) |
| **Allowed Relationships** | ORCHESTRATES Automation · ORCHESTRATES Agent · TRIGGERED_BY Event · GOVERNED_BY Playbook · PRODUCES Business Outcome |
| **Lifecycle Applicability** | Active · Paused · Deprecated · Failed |
| **Required Schema Fields** | `id` · `name` · `trigger_type` (cron \| event \| manual) · `steps[]` · `success_criteria` · `owner_role_id` · `framework` (n8n \| antfarm \| openclaw_cron) · `status` |
| **Validation Rules** | Must have defined `steps[]`. Must have a `trigger_type`. Must have `success_criteria`. Steps must be ordered. Idempotency must be documented for each step. Failed workflows must log the failed step and reason. |
| **Examples from Open Empire** | BLCO weekly sourcing workflow (n8n, Monday 07:00 CDT) · antfarm feature-dev workflow · Night Ops daily workflow (23:00 CDT) · Trade signal → approve → execute workflow |
| **Cross References** | L4: Automation, Agent · L2: Playbook · L3: Integration |
| **Notes** | n8n handles external-facing, approval-gated workflows. antfarm handles multi-agent internal workflows. OpenClaw cron handles lightweight recurring tasks. Do not mix frameworks within a single Workflow — each Workflow must name exactly one `framework`. |

---

### Automation

| Field | Value |
|---|---|
| **Canonical Name** | Automation |
| **Canonical Definition** | A single-purpose, repeatable automated action or bounded sequence of actions executed by a system without human intervention — a discrete step within a Workflow or a standalone background task. |
| **Purpose within Open Empire** | The atomic unit of autonomous operation. Every scheduled task, cron job, and background script is an Automation. |
| **Parent Layer** | Layer 4 — Operations |
| **Parent Asset** | Workflow (if part of one) · Service (if standalone) |
| **Child Asset Types** | None |
| **Allowed Relationships** | PART_OF Workflow · EXECUTED_BY Service · USES API · USES Integration · GOVERNED_BY Policy · LOGGED_TO Storage |
| **Lifecycle Applicability** | Active · Paused · Failed · Deprecated |
| **Required Schema Fields** | `id` · `name` · `trigger` (cron_expr \| event \| api_call) · `script` · `cwd` · `environment_id` · `logging_target` · `retry_policy` · `status` |
| **Validation Rules** | Must define `trigger`. Must define `logging_target`. Must define `retry_policy`. Failed automations must log error details with full stack trace. Paused automations must document reason and resume condition. |
| **Examples from Open Empire** | 5-min CashClaw director cycle · 5-min arb scan cycle · Monday 07:00 CDT BLCO weekly scan · Nightly compression at 23:00 CDT · Morning brief at 07:00 CDT · Secrets health check |
| **Cross References** | L4: Workflow, Service · L2: Policy · L3: Integration |
| **Notes** | Automations are scheduled via OpenClaw cron tool or PM2 `cron_restart`. The cron tool is preferred for event-driven scheduling. Do not emulate scheduling with `exec sleep` loops — this is a governance violation. |

---

### Agent

| Field | Value |
|---|---|
| **Canonical Name** | Agent |
| **Canonical Definition** | An AI-driven autonomous execution entity — with defined capabilities, policies, memory scope, and tool access — that carries out tasks on behalf of Open Empire with or without human intervention. |
| **Purpose within Open Empire** | The primary autonomous actor in Open Empire. Agents are the intelligence layer that transforms governance rules into executed action. |
| **Parent Layer** | Layer 4 — Operations |
| **Parent Asset** | Agent Team or Program |
| **Child Asset Types** | None |
| **Allowed Relationships** | MEMBER_OF Agent Team · USES Model · USES API · USES Service · GOVERNED_BY Policy · EXECUTES Playbook · REPORTS_TO Execution Role · PRODUCES Business Outcome |
| **Lifecycle Applicability** | Draft · Testing · Active · Suspended · Retired |
| **Required Schema Fields** | `id` · `name` · `agent_type` (director \| arb \| trader \| monitor \| orchestrator \| specialist \| chief_of_staff) · `model_id` · `tool_access[]` · `policy_ids[]` · `owner_role_id` · `memory_scope` · `spend_cap_usd` (if financial) · `status` |
| **Validation Rules** | Must define `model_id`. Must define `policy_ids[]`. Must not access tools outside `tool_access[]`. Suspended agents must log suspension reason and resume condition. Financial agents must carry a `spend_cap_usd`. Agents may not invoke Opus except Alusi. |
| **Examples from Open Empire** | cashclaw_director (PM2 id=38, director type, $10/day cap) · cashclaw_arb (PM2 id=39, arb type, $10/day cap) · polymarket_trader (PM2 id=40, trader type, $10/day cap) · trading_sentinel (PM2 id=41, monitor type) · Alusi (chief_of_staff, Sonnet primary) |
| **Cross References** | L3: Model · L4: Agent Team, Service · L2: Policy, Approval Types |
| **Notes** | Not all Agents are PM2 processes — Alusi is a session-bound Agent. The trading agents are both Agents (AI decision-making) AND PM2 Processes (lifecycle management). Agents are governed by policies — violation triggers audit, not silent correction. |

---

### Agent Team

| Field | Value |
|---|---|
| **Canonical Name** | Agent Team |
| **Canonical Definition** | A named, organized group of Agents with complementary roles that collaborate under a shared governance structure to accomplish a complex, ongoing objective. |
| **Purpose within Open Empire** | Enables structured multi-agent coordination. Defines interaction patterns, reporting chains, and shared resource constraints between cooperating agents. |
| **Parent Layer** | Layer 4 — Operations |
| **Parent Asset** | Program or Venture |
| **Child Asset Types** | Agent |
| **Allowed Relationships** | CONTAINS Agent · GOVERNED_BY Council · ORCHESTRATED_BY Agent (lead agent) · PRODUCES Business Outcome |
| **Lifecycle Applicability** | Active · Reorganizing · Disbanded |
| **Required Schema Fields** | `id` · `name` · `purpose` · `agents[]` · `lead_agent_id` · `council_id` · `coordination_protocol` · `collective_spend_cap_usd` · `status` |
| **Validation Rules** | Must contain at least two agents. Must define a `lead_agent_id`. Must define `coordination_protocol`. Cannot be Active without a governing Council. Must define `collective_spend_cap_usd` if any member agent has financial authority. |
| **Examples from Open Empire** | CashClaw Trading Team (director + arb + polymarket_trader + sentinel) · BLCO Outreach Team (sourcer + qualifier + emailer) · Open Empire Governance Team (Alusi + council agents) |
| **Cross References** | L4: Agent · L2: Council · L5: Execution Roles |
| **Notes** | The CashClaw Trading Team is the most critical Agent Team in current operation. trading_sentinel monitors the entire team. A sentinel anomaly triggers a P0 alert — all team agents halt pending investigation. |

---

### Dashboard

| Field | Value |
|---|---|
| **Canonical Name** | Dashboard |
| **Canonical Definition** | A real-time or near-real-time visualization interface that displays Operational Status, Executive KPIs, and system health across Open Empire assets. |
| **Purpose within Open Empire** | Nathan's primary situational awareness tool. The single pane of glass for governance oversight — providing complete visibility without requiring direct system access. |
| **Parent Layer** | Layer 4 — Operations |
| **Parent Asset** | Service (backing the dashboard) · Program (served by dashboard) |
| **Child Asset Types** | None |
| **Allowed Relationships** | DISPLAYS Operational Status · DISPLAYS Executive KPI · MONITORS Service · MONITORS Agent · SERVED_BY Service |
| **Lifecycle Applicability** | Active · Degraded · Stopped |
| **Required Schema Fields** | `id` · `name` · `port` · `service_id` · `data_sources[]` · `refresh_interval_seconds` · `access_control` · `status` |
| **Validation Rules** | Must define `port`. Must list `data_sources[]`. Must define `access_control`. All dashboards must be loopback-bound per Security Policy. Degraded dashboards must alert within 5 minutes. |
| **Examples from Open Empire** | Grafana (port 3001 — metrics and time-series) · Mission Control (port 3333, PM2 id=17 — command center, primary governance dashboard) |
| **Cross References** | L4: Service · L1: Executive KPI · L5: Operational Status |
| **Notes** | Mission Control is the primary governance dashboard. Grafana handles metrics. Both are loopback-bound. A stopped Mission Control is a T1 incident — Nathan loses primary situational awareness. |

---

### Knowledge Base

| Field | Value |
|---|---|
| **Canonical Name** | Knowledge Base |
| **Canonical Definition** | A curated, structured collection of domain knowledge, operational procedures, market intelligence, and reference data — accessible to agents and humans for decision support. |
| **Purpose within Open Empire** | The organizational intelligence layer. Prevents knowledge loss across agent handoffs and session boundaries. Everything that must be remembered between sessions lives here. |
| **Parent Layer** | Layer 4 — Operations |
| **Parent Asset** | Program (domain-specific) or Portfolio (cross-cutting) |
| **Child Asset Types** | None |
| **Allowed Relationships** | CONSUMED_BY Agent · CONSUMED_BY Playbook · CURATED_BY Ownership Role · STORED_IN Storage · INDEXED_BY Memory Store |
| **Lifecycle Applicability** | Active · Outdated · Archived |
| **Required Schema Fields** | `id` · `name` · `domain` · `format` (markdown \| json \| jsonl \| vector_db) · `root_path` · `curation_policy` · `last_updated` · `owner_role_id` · `status` |
| **Validation Rules** | Must define `domain`. Must define `curation_policy`. Must have a `last_updated` timestamp. Outdated Knowledge Bases must not be used for live financial or operational decisions without explicit acknowledgment. |
| **Examples from Open Empire** | BLCO market intelligence (`~/.openclaw/blco/knowledge/`) · Open Empire doctrine (`~/.openempire/` — 20 files, highest authority) · OpenClaw workspace docs (`/usr/local/lib/node_modules/openclaw/docs/`) |
| **Cross References** | L4: Memory Store · L2: Playbook · L3: Storage |
| **Notes** | Open Empire doctrine (`~/.openempire/`) is the highest-authority Knowledge Base. It takes precedence over all other knowledge sources except explicit Nathan directives issued in session. |

---

### Memory Store

| Field | Value |
|---|---|
| **Canonical Name** | Memory Store |
| **Canonical Definition** | A persistent or semi-persistent storage layer that enables agents and the system to retain context, state, and accumulated knowledge across session boundaries. |
| **Purpose within Open Empire** | Prevents context loss between agent sessions. Enables continuous operation without re-explaining state. The bridge between session-scoped intelligence and durable institutional knowledge. |
| **Parent Layer** | Layer 4 — Operations |
| **Parent Asset** | Agent or Service (OpenClaw gateway) |
| **Child Asset Types** | None |
| **Allowed Relationships** | ACCESSED_BY Agent · MANAGED_BY Automation (compression) · BACKED_UP_TO Storage · IMPLEMENTS Knowledge Base (long-form synthesis) |
| **Lifecycle Applicability** | Active · Compressing · Corrupted · Archived |
| **Required Schema Fields** | `id` · `name` · `type` (active \| compressed \| archive \| vector) · `root_path` · `retention_days` · `compression_schedule` · `owner_agent_id` · `status` |
| **Validation Rules** | Must define `type`. Must define `retention_days`. Active memory must compress on schedule. Corrupted memory triggers P1 alert. Active memory writes must not exceed 300 tokens per delta. |
| **Examples from Open Empire** | `~/.openclaw/memory/active/` (24h retention, ultra-short summaries) · `~/.openclaw/memory/compressed/` (daily summaries, KPIs, decisions) · `~/.openclaw/memory/archive/` (raw logs — never auto-injected) · `MEMORY.md` (Alusi session-persistent memory) |
| **Cross References** | L4: Knowledge Base · L3: Storage · L4: Agent |
| **Notes** | Canonical compression cycle: every 6 hours. Only Alusi may trigger deep retrieval from archive. Active memory delta writes must not exceed 300 tokens. Full history replay is prohibited — a governance violation defined in HEARTBEAT.md Token Governance Rule 1. |

---

### Registry

| Field | Value |
|---|---|
| **Canonical Name** | Registry |
| **Canonical Definition** | A governed, queryable catalog of all Open Empire assets of a specific type — providing a single source of truth for discovery, governance, and audit. |
| **Purpose within Open Empire** | The instantiation layer of the Taxonomy. The Registry is where abstract asset definitions become tracked, real-world entities. Every asset that exists must be registered. |
| **Parent Layer** | Layer 4 — Operations |
| **Parent Asset** | Portfolio (scope) · Council (governance) |
| **Child Asset Types** | None (contains records of all other asset types) |
| **Allowed Relationships** | CATALOGS all asset types · GOVERNED_BY Council · QUERIED_BY Dashboard · QUERIED_BY Agent · WRITTEN_BY Automation (state sync) |
| **Lifecycle Applicability** | Active · Stale · Rebuilding |
| **Required Schema Fields** | `id` · `name` · `scope` (global \| domain-specific) · `asset_types[]` · `storage_format` (json \| jsonl \| postgresql \| markdown) · `root_path_or_table` · `last_sync_at` · `owner_role_id` · `status` |
| **Validation Rules** | Must define `asset_types[]`. Must have `last_sync_at`. Stale Registries (not updated in >24h for live assets) trigger alert. Must be the authoritative source of truth for its scope — no shadow registries. |
| **Examples from Open Empire** | AGENTS.md (PM2 process registry) · `master_skills_index.json` (skills registry) · `leads.jsonl` (BLCO lead registry) · `vault/approvals/approvals.jsonl` (approval registry) · Asset Registry (full Open Empire — being instantiated from this Taxonomy) |
| **Cross References** | L4: Dashboard, Knowledge Base · L2: Council · L1: Portfolio |
| **Notes** | The full Open Empire Asset Registry is the primary Registry. It instantiates every entry in this Taxonomy as a tracked, real-world entity. Mission Control visualizes it. OEPM governs from it. PMO executes against it. |

---

# LAYER 5 — EXECUTION

> The operational classification layer. Defines the roles, statuses, priorities, relationship types, and verification methods that govern how assets are operated and validated.

---

### Execution Role

| Field | Value |
|---|---|
| **Canonical Name** | Execution Role |
| **Canonical Definition** | A named operational role at the task execution level — assigned to an agent or human responsible for carrying out specific recurring operational duties within a defined scope. |
| **Purpose within Open Empire** | Defines WHO executes what. Below Ownership Roles in authority, but critical for day-to-day operational clarity and accountability. |
| **Parent Layer** | Layer 5 — Execution |
| **Parent Asset** | Ownership Role (reports to) |
| **Child Asset Types** | None |
| **Allowed Relationships** | REPORTS_TO Ownership Role · EXECUTES Automation · EXECUTES Playbook · EXECUTES Agent Task · MEMBER_OF Agent Team |
| **Lifecycle Applicability** | Active · Delegated · Vacant |
| **Required Schema Fields** | `id` · `title` · `scope` · `holder` (agent_id \| human_name) · `ownership_role_id` · `task_types[]` · `status` |
| **Validation Rules** | Must define `scope`. Must list `task_types[]`. Cannot be Vacant for P0-critical recurring operations. Delegated roles must document delegation scope, delegating party, and expiry date. |
| **Examples from Open Empire** | Signal Scorer (CashClaw Haiku scorer) · Trade Executor (cashclaw_director) · Arb Scanner (cashclaw_arb) · Lead Qualifier (blco_broker) · Approval Processor (sovereign_proxy) · Memory Compressor (Automation) |
| **Cross References** | L2: Executive Roles, Ownership Roles · L4: Agent, Automation |
| **Notes** | Most Execution Roles in Open Empire are held by AI agents, not humans. Nathan holds Sovereign Operator — never an Execution Role. Alusi holds Chief of Staff (Executive Role) and routes Execution Roles to specialized agents. |

---

### Operational Status

| Field | Value |
|---|---|
| **Canonical Name** | Operational Status |
| **Canonical Definition** | A standardized real-time state indicator for a running Service, Agent, or Automation — reflecting its current health and availability as observed by monitoring systems. |
| **Purpose within Open Empire** | Enables rapid situational awareness without querying individual systems. The unified health language. Every AGENTS.md entry carries an Operational Status. |
| **Parent Layer** | Layer 5 — Execution |
| **Parent Asset** | Service · Agent · Automation |
| **Child Asset Types** | None |
| **Allowed Relationships** | APPLIED_TO Service · APPLIED_TO Agent · APPLIED_TO Automation · DISPLAYED_BY Dashboard · TRIGGERS Alert (on degradation) · INFORMED_BY Lifecycle State |
| **Lifecycle Applicability** | Active (real-time classification — not itself subject to lifecycle) |
| **Required Schema Fields** | `status` (OK \| DEGRADED \| STOPPED \| ERRORED \| RESTARTING \| UNKNOWN) · `last_checked_at` · `check_method` (pm2 \| health_check \| heartbeat \| manual) · `incident_open` (bool) · `notes` |
| **Validation Rules** | Must be one of six canonical values — no free-text. Must have `last_checked_at` timestamp. UNKNOWN status triggers immediate investigation. Status must be refreshed within SLA: ≤5 minutes for T0 assets. UNKNOWN must never persist beyond one monitoring cycle. |
| **Examples from Open Empire** | cashclaw_director: OK · clawdb: OK · polymarket-trader: OK (⚠️ $0.06 balance — needs deposit) · email-dispatcher: STOPPED (intentional) · pnl-audit: STOPPED (intentional) · heartbeat: multiple ERRORED events 2026-08-03 |
| **Cross References** | L4: Dashboard · L2: Evidence States, Lifecycle States · L1: Executive KPI |
| **Notes** | STOPPED ≠ ERRORED. STOPPED = intentionally halted (operational decision). ERRORED = unexpected failure (incident). Both require different response playbooks. The heartbeat failures on 2026-08-03 (08:38 CDT) require root cause analysis. |

---

### Integration Readiness

| Field | Value |
|---|---|
| **Canonical Name** | Integration Readiness |
| **Canonical Definition** | A standardized assessment of whether an Integration is ready for production use — covering authentication verification, endpoint reachability, error handling validation, and end-to-end transaction confirmation. |
| **Purpose within Open Empire** | Gates Integration promotion from staging to production. Prevents untested or partially-configured integrations from entering live systems. |
| **Parent Layer** | Layer 5 — Execution |
| **Parent Asset** | Integration |
| **Child Asset Types** | None |
| **Allowed Relationships** | ASSESSED_FOR Integration · GATES Lifecycle State transition (Staging→Active) · VERIFIED_BY Verification Method |
| **Lifecycle Applicability** | Not Ready · Partially Ready · Ready · Validated · Degraded |
| **Required Schema Fields** | `id` · `integration_id` · `auth_verified` (bool) · `endpoint_reachable` (bool) · `error_handling_tested` (bool) · `end_to_end_validated` (bool) · `last_validated_at` · `readiness_state` · `notes` |
| **Validation Rules** | All four boolean fields must be `true` for `readiness_state=Ready`. Validated requires at least one successful live transaction. Degraded triggers immediate investigation and blocks new trading activity. |
| **Examples from Open Empire** | Kalshi V2 (Validated — RSA-PSS auth confirmed + live orders placed) · Polymarket US (Validated — Ed25519 auth confirmed + 13 positions open) · n8n Webhook (Validated — approvals routing confirmed) · Telegram (Validated — messages delivered) |
| **Cross References** | L3: Integration, API · L5: Verification Methods · L2: Evidence States |
| **Notes** | Integration Readiness must be re-evaluated after every API version change. The Kalshi V1→V2 migration required full re-validation. V1 was marked Broken (returning 410) before the migration was approved. |

---

### Business Criticality

| Field | Value |
|---|---|
| **Canonical Name** | Business Criticality |
| **Canonical Definition** | A standardized four-tier classification of how critical an asset is to Open Empire's revenue generation, operational continuity, and mission delivery. |
| **Purpose within Open Empire** | Drives prioritization for resource allocation, incident response, and recovery planning. Every asset in the Registry carries a criticality tier. |
| **Parent Layer** | Layer 5 — Execution |
| **Parent Asset** | Any asset type |
| **Child Asset Types** | None |
| **Allowed Relationships** | APPLIED_TO any asset · DETERMINES Recovery Priority · DETERMINES Approval Type requirements · INFORMS Risk Level assignment |
| **Lifecycle Applicability** | Active (canonical enumeration — not subject to individual lifecycle) |
| **Required Schema Fields** | `criticality_tier` (Tier-0 \| Tier-1 \| Tier-2 \| Tier-3) · `revenue_impact` (direct \| indirect \| none) · `mttr_target_minutes` · `rpo_target_minutes` · `notes` |
| **Validation Rules** | Must be one of four tiers only. Tier-0 assets must have MTTR < 60 minutes. Tier-0 assets must have automated monitoring with ≤5-minute check cadence. `revenue_impact` must be defined. No asset may be Tier-0 without Nathan's explicit designation. |
| **Examples from Open Empire** | **Tier-0** (direct revenue, MTTR <60min): CashClaw trading stack · Kalshi/Polymarket integrations · OpenClaw gateway · ClawDB · sovereign_proxy · **Tier-1** (operational continuity): Mission Control · Grafana · antfarm · Telegram adapter · **Tier-2** (business support): BLCO pipeline · n8n · **Tier-3** (non-critical): email-dispatcher (stopped) · pnl-audit (on-demand) |
| **Cross References** | L2: Risk Levels · L5: Recovery Priority · L4: Service, Agent |
| **Notes** | Business Criticality drives AGENTS.md registry tiers and determines recovery sequencing. The assignment of Tier-0 to an asset is a governance decision requiring Council review. It cannot be self-declared by an agent. |

---

### Recovery Priority

| Field | Value |
|---|---|
| **Canonical Name** | Recovery Priority |
| **Canonical Definition** | A ranked ordering of asset restoration priority during a system outage — defining the pre-approved sequence in which services are recovered to minimize business impact. |
| **Purpose within Open Empire** | Prevents ad-hoc recovery decisions during high-stress incidents. Establishes the restoration order before an incident occurs. Recovery Priority is decided in advance — never during the incident. |
| **Parent Layer** | Layer 5 — Execution |
| **Parent Asset** | Any asset (Service · Database · Integration · Agent) |
| **Child Asset Types** | None |
| **Allowed Relationships** | APPLIED_TO Service · APPLIED_TO Database · APPLIED_TO Integration · INFORMED_BY Business Criticality · INFORMED_BY Risk Level · DEFINED_BY Playbook (Incident Response) |
| **Lifecycle Applicability** | Active (pre-approved ordered list — not subject to individual lifecycle) |
| **Required Schema Fields** | `priority_rank` (1 = highest priority) · `asset_id` · `asset_type` · `rto_minutes` (Recovery Time Objective) · `rpo_minutes` (Recovery Point Objective) · `dependencies[]` · `recovery_steps_ref` |
| **Validation Rules** | Priority ranks must be unique and sequential. RTO and RPO must be defined. Dependencies must be recovered before dependents. Recovery steps must reference an active Playbook. Assets may not be recovered out of sequence without explicit Nathan authorization. |
| **Examples from Open Empire** | P1: clawdb (PostgreSQL — all agents log here) · P2: alusi-gateway (all agent communication) · P3: cashclaw_director (primary revenue) · P4: cashclaw_arb (secondary revenue) · P5: polymarket_trader (tertiary revenue) · P6: trading_sentinel (watchdog) · P7: Telegram adapter (comms) |
| **Cross References** | L5: Business Criticality · L2: Risk Levels · L4: Service |
| **Notes** | Database (clawdb) is recovery priority 1 — trading agents cannot log without it. Gateway is priority 2 — no agent communication without it. The recovery sequence is based on dependency graph analysis, not perceived importance. |

---

### Relationship Type

| Field | Value |
|---|---|
| **Canonical Name** | Relationship Type |
| **Canonical Definition** | A standardized, directed connection type between two Open Empire assets — defining how they interact, depend on, or govern each other within the asset graph. |
| **Purpose within Open Empire** | Makes the asset graph traversable and machine-readable. Enables impact analysis, dependency resolution, and automated governance checks. |
| **Parent Layer** | Layer 5 — Execution |
| **Parent Asset** | None (cross-layer primitive — applies to any pair of asset types) |
| **Child Asset Types** | None |
| **Allowed Relationships** | APPLIED_TO any pair of asset types (as specified in each asset type's Allowed Relationships field) |
| **Lifecycle Applicability** | Active (canonical enumeration — not subject to individual lifecycle) |
| **Required Schema Fields** | `source_asset_id` · `source_asset_type` · `relationship_type` · `target_asset_id` · `target_asset_type` · `direction` (directed \| bidirectional) · `strength` (required \| optional \| deprecated) |
| **Validation Rules** | Must use canonical relationship type names only — no free-text relationship descriptions. Must be directed unless explicitly bidirectional. Deprecated relationships must be removed within 30 days. Only relationship types defined in this Taxonomy may be used in the Asset Registry. |
| **Examples from Open Empire** | CONTAINS · BELONGS_TO · MANAGED_BY · GOVERNED_BY · EXPOSES · CONSUMES · USES · OWNED_BY · REPORTS_TO · IMPLEMENTS · DEPLOYS_TO · PRODUCES · DELIVERS · TRIGGERS · MONITORS · ROUTES_TO · AUTHENTICATED_VIA · BACKED_UP_BY · MEASURED_BY · VALIDATED_BY · SUPERSEDED_BY |
| **Cross References** | All asset types (Allowed Relationships field) |
| **Notes** | The Ontology document will formally specify all valid relationship type pairs and their directionality constraints. No Relationship Type may be used that is not listed in this Taxonomy. The Ontology is the governing specification; this Taxonomy is the source of canonical relationship names. |

---

### Verification Method

| Field | Value |
|---|---|
| **Canonical Name** | Verification Method |
| **Canonical Definition** | A standardized technique used to confirm that an asset, integration, or operational condition is functioning as expected and meets its defined requirements. |
| **Purpose within Open Empire** | Makes claims verifiable. Every Evidence State of Verified must be backed by a named, documented Verification Method. Unverified claims are not acceptable for governance decisions. |
| **Parent Layer** | Layer 5 — Execution |
| **Parent Asset** | Policy (requiring verification) · Playbook (executing verification) |
| **Child Asset Types** | None |
| **Allowed Relationships** | VALIDATES Integration Readiness · VALIDATES Operational Status · VALIDATES Evidence State · EXECUTED_BY Automation · REFERENCED_BY Standard |
| **Lifecycle Applicability** | Active (canonical enumeration — not subject to individual lifecycle) |
| **Required Schema Fields** | `id` · `name` · `type` (api_call \| log_check \| ui_check \| unit_test \| end_to_end_test \| manual_review \| heartbeat \| balance_check \| schema_diff) · `automation_eligible` (bool) · `cadence` · `evidence_produced` |
| **Validation Rules** | Must define `type`. Must define `automation_eligible`. Must define `cadence`. Automated verifications must log timestamped results. Every Tier-0 asset must have at least one automated Verification Method with cadence ≤ 15 minutes. |
| **Examples from Open Empire** | Kalshi balance API call (balance_check, automated, 5min) · PM2 status check (log_check, automated, 5min) · Trade log integrity check (log_check, automated, daily) · Telegram delivery test (api_call, automated, hourly) · Manual P&L audit (manual_review, human, weekly) |
| **Cross References** | L2: Evidence States, Standards · L5: Integration Readiness, Operational Status |
| **Notes** | Every Tier-0 asset must have at least one automated Verification Method with cadence ≤ 15 minutes. Manual verification is insufficient for Tier-0 — it must be supplemented by automated checks. |

---

# LAYER 6 — EVOLUTION

> The change and continuity layer. Defines how Open Empire assets evolve over time — from current state through migration, retirement, and beyond — with full audit continuity.

---

### Current State

| Field | Value |
|---|---|
| **Canonical Name** | Current State |
| **Canonical Definition** | A point-in-time, evidence-backed snapshot of an asset's actual operational configuration, status, and characteristics — as-is, without projection or aspiration. |
| **Purpose within Open Empire** | Establishes ground truth for planning, gap analysis, and migration. Prevents decisions from being made on assumed rather than actual state. |
| **Parent Layer** | Layer 6 — Evolution |
| **Parent Asset** | Any asset type |
| **Child Asset Types** | None |
| **Allowed Relationships** | CONTRASTED_WITH Target State · EVIDENCE_PROVIDED_BY Evidence State · CAPTURED_BY Automation (state snapshot) · REVIEWED_BY Council |
| **Lifecycle Applicability** | Active (point-in-time snapshot — becomes historical when superseded) |
| **Required Schema Fields** | `asset_id` · `snapshot_timestamp` · `captured_by` · `evidence_state` · `configuration{}` · `operational_status` · `known_issues[]` · `notes` |
| **Validation Rules** | Must be timestamped. Must carry `evidence_state`. Configuration must reflect actual deployed state — not intended state. Known issues must be listed, not omitted. A Current State older than 7 days requires refresh before use in planning. |
| **Examples from Open Empire** | CashClaw Director Current State (2026-08-02): canonical path trading.agents.director.run, Python 3.13 venv313, Haiku signal chain, $10 spend cap, 5min cycle, 0 trades placed, Kalshi balance $1.55 free. |
| **Cross References** | L6: Target State, Migration State · L2: Evidence States · L5: Operational Status |
| **Notes** | Current State documents are the inputs to gap analysis. They must be refreshed before any migration planning begins. The D21 Repository Recovery audit (2026-08-03) produced Current State snapshots for all 6 Tier-0 repositories. |

---

### Target State

| Field | Value |
|---|---|
| **Canonical Name** | Target State |
| **Canonical Definition** | A defined, approved future configuration of an asset or system — specifying what it should look like, how it should behave, and what measurable criteria confirm it has been achieved. |
| **Purpose within Open Empire** | The approved destination for all change and migration work. Prevents drift by defining success criteria before work begins. No migration begins without an approved Target State. |
| **Parent Layer** | Layer 6 — Evolution |
| **Parent Asset** | Any asset type (defined for) |
| **Child Asset Types** | None |
| **Allowed Relationships** | CONTRASTED_WITH Current State · ACHIEVED_BY Migration State (successful completion) · APPROVED_BY Council · GOVERNS Change Control |
| **Lifecycle Applicability** | Proposed · Approved · In Progress · Achieved · Superseded |
| **Required Schema Fields** | `asset_id` · `target_id` · `approved_by` · `approved_at` · `target_configuration{}` · `success_criteria[]` · `target_date` · `status` |
| **Validation Rules** | Must have `approved_by`. Must define `success_criteria[]`. Must have `target_date`. Cannot be marked Achieved without all `success_criteria[]` verified. Must be Approved before migration begins. Superseded Target States must be closed with documented reason. |
| **Examples from Open Empire** | Target: trading/ has git initialized, remote configured, CI green, .gitignore excluding trade data. Target: Polymarket balance funded to $40+. Target: BLCO first verified sale. Target: CashClaw win rate 70%+. |
| **Cross References** | L6: Current State, Migration State, Change Control · L2: Council |
| **Notes** | Target States are the governance anchor for all roadmap items. Every OEPM initiative requires an explicit, approved Target State. "We'll know it when we see it" is not a Target State — it is an unacceptable governance gap. |

---

### Migration State

| Field | Value |
|---|---|
| **Canonical Name** | Migration State |
| **Canonical Definition** | The active transitional state of an asset or system moving from its Current State toward a defined Target State — tracking progress, intermediate steps, risks, and blockers. |
| **Purpose within Open Empire** | Makes change visible and governable. A Migration State is the live record of an in-progress transformation. It prevents migrations from disappearing into undocumented "work in progress." |
| **Parent Layer** | Layer 6 — Evolution |
| **Parent Asset** | Any asset in transition |
| **Child Asset Types** | None |
| **Allowed Relationships** | PROGRESSES_FROM Current State · PROGRESSES_TOWARD Target State · GOVERNED_BY Change Control · LOGGED_BY Automation · REVIEWED_BY Council |
| **Lifecycle Applicability** | Not Started · In Progress · Blocked · Rolled Back · Complete |
| **Required Schema Fields** | `asset_id` · `migration_id` · `current_state_id` · `target_state_id` · `steps_completed[]` · `steps_remaining[]` · `blockers[]` · `risk_level` · `rollback_plan` · `status` |
| **Validation Rules** | Must reference `current_state_id` and `target_state_id`. Must define `rollback_plan` before migration begins — migrations without rollback plans are blocked. Blocked migrations must trigger escalation within SLA for the assigned risk_level. |
| **Examples from Open Empire** | cashclaw_legacy → trading/ canonical migration (Phase 5/6, 2026-07-31, Complete) · Kalshi V1 → V2 API migration (2026-07-30, Complete) · trading/ git initialization (Not Started — D21 pending approval) |
| **Cross References** | L6: Current State, Target State, Change Control · L2: Risk Levels |
| **Notes** | Completed migrations must be documented as closed. Deprecated assets must be moved to `_deprecated/` per Phase 6 protocol. The `_deprecated/` directory is the archive, not the trash — do not delete without explicit approval. |

---

### Retirement State

| Field | Value |
|---|---|
| **Canonical Name** | Retirement State |
| **Canonical Definition** | The final operational state of an asset that has been intentionally decommissioned — no longer active, archived for audit continuity, and excluded from operational registries. |
| **Purpose within Open Empire** | Provides a clean, governed endpoint for asset lifecycles. Prevents zombie assets — believed retired but partially still active — from creating hidden risks and audit gaps. |
| **Parent Layer** | Layer 6 — Evolution |
| **Parent Asset** | Any asset reaching end of life |
| **Child Asset Types** | None |
| **Allowed Relationships** | SUPERSEDED_BY active asset · ARCHIVED_IN Storage · APPROVED_BY Approval Type (retirement requires explicit approval) · DOCUMENTED_BY Registry (retirement record kept permanently) |
| **Lifecycle Applicability** | Planned Retirement · Retiring · Retired · Archived |
| **Required Schema Fields** | `asset_id` · `retirement_date` · `approved_by` · `superseded_by_id` (if applicable) · `archive_path` · `data_retention_policy` · `status` |
| **Validation Rules** | Must have `approved_by`. Must have `archive_path`. Must define `data_retention_policy`. Tier-0 assets require P0-level approval to retire. Retirement ≠ Deletion — retired assets are archived with full provenance, not destroyed. |
| **Examples from Open Empire** | cashclaw/ legacy (Retired 2026-07-31, archived to `_deprecated/cashclaw_2026-07-31/`) · polymarket/ legacy (Retired 2026-07-31) · Kalshi V1 API integration (Retired 2026-07-30) · PM2 id=6 cashclaw stub (Retired 2026-07-31) |
| **Cross References** | L6: Supersession, Versioning · L2: Lifecycle States, Approval Types |
| **Notes** | Retired ≠ Deleted. Retired assets are archived with full provenance in `_deprecated/`. Deletion requires a separate, explicit approval with an audit log entry. This distinction is absolute. |

---

### Supersession

| Field | Value |
|---|---|
| **Canonical Name** | Supersession |
| **Canonical Definition** | A formal replacement relationship record where one asset explicitly replaces another — documenting the transition of authority, capability, and reference from the predecessor to the successor. |
| **Purpose within Open Empire** | Maintains audit continuity through asset replacement. Prevents institutional knowledge loss when systems are replaced. Every replacement creates a traceable provenance chain. |
| **Parent Layer** | Layer 6 — Evolution |
| **Parent Asset** | None (cross-asset relationship record — not owned by a specific asset) |
| **Child Asset Types** | None |
| **Allowed Relationships** | REPLACES (predecessor → successor) · DOCUMENTED_BY Registry · APPROVED_BY Approval Type (Change Control) · TRIGGERS Retirement State (for predecessor) |
| **Lifecycle Applicability** | Active (permanent relationship record — Supersession records are never deleted) |
| **Required Schema Fields** | `id` · `predecessor_asset_id` · `predecessor_asset_type` · `successor_asset_id` · `successor_asset_type` · `effective_date` · `approved_by` · `reason` · `migration_state_id` (if applicable) · `notes` |
| **Validation Rules** | Must reference both predecessor and successor. Must have `effective_date`. Must have `approved_by`. All references to predecessor must be updated to successor within 30 days of effective_date. Supersession records are permanent — never delete. |
| **Examples from Open Empire** | trading/ supersedes cashclaw/ + polymarket/ (effective 2026-07-31, approved Nathan) · Kalshi V2 API supersedes Kalshi V1 (effective 2026-07-30) · PM2 id=38 supersedes PM2 id=6 (cashclaw director) · canonical `trading.agents.*` supersedes all legacy agent paths |
| **Cross References** | L6: Retirement State, Migration State, Change Control · L3: Repository |
| **Notes** | Supersession records are permanent. They must never be deleted. They form the provenance chain for understanding how Open Empire evolved. Future audits depend on them. An unrecorded supersession is a governance gap. |

---

### Versioning

| Field | Value |
|---|---|
| **Canonical Name** | Versioning |
| **Canonical Definition** | A standardized system for assigning, tracking, and communicating the version identity of Open Empire assets — enabling change tracking, rollback, and compatibility management across the entire stack. |
| **Purpose within Open Empire** | Ensures every asset change is identifiable, traceable, and reversible. Prevents version confusion across distributed components. The foundation of change control. |
| **Parent Layer** | Layer 6 — Evolution |
| **Parent Asset** | Any versioned asset (Repository · Package · Library · API · Standard · Policy · Playbook · Taxonomy) |
| **Child Asset Types** | None |
| **Allowed Relationships** | APPLIED_TO Repository · APPLIED_TO Package · APPLIED_TO API · APPLIED_TO Standard · APPLIED_TO Policy · GOVERNS Change Control (version bump requirements) |
| **Lifecycle Applicability** | Active (continuous — versioning applies throughout an asset's lifecycle) |
| **Required Schema Fields** | `asset_id` · `version_scheme` (semver \| calver \| git_sha \| sequential) · `current_version` · `previous_version` · `changelog_ref` · `version_history[]` |
| **Validation Rules** | Must use canonical version scheme for the asset type. Major version bumps require Change Control approval. All version changes must be logged with timestamp and actor. Git SHAs are the canonical version identifier for code assets. No asset may silently change version without a logged event. |
| **Examples from Open Empire** | OPEN_EMPIRE_ASSET_TAXONOMY_V1.0.0 (sequential/calver) · trading package (semver) · alusi-core SHA d7cb2e701e8b (git_sha) · OpenClaw v2026.3.13 (calver) · open-empire-core SHA 5a52324a04e8 (git_sha) |
| **Cross References** | L6: Change Control, Supersession · L3: Repository, API · L2: Standards |
| **Notes** | This document is OPEN_EMPIRE_ASSET_TAXONOMY_V1.0.0. Minor additions increment to V1.1.0. Breaking revisions of existing definitions require V2.0.0 with full Change Control. No agent may unilaterally bump the Taxonomy version. |

---

### Change Control

| Field | Value |
|---|---|
| **Canonical Name** | Change Control |
| **Canonical Definition** | The governance process governing when, why, and how Open Empire assets may be modified — requiring pre-approval, documentation, rollback planning, and completion evidence for all significant changes. |
| **Purpose within Open Empire** | Prevents unauthorized or unplanned changes from destabilizing production systems. Every significant modification is a governed event with a before-state, an approver, a plan, and an after-state. |
| **Parent Layer** | Layer 6 — Evolution |
| **Parent Asset** | Policy (enforcing) · Council (approving) |
| **Child Asset Types** | None |
| **Allowed Relationships** | GOVERNS Migration State · GOVERNS Versioning (major bumps) · REQUIRED_BY Standard (changes to Standards) · APPROVED_BY Council (or Executive Role for urgent changes) · LOGGED_BY Registry |
| **Lifecycle Applicability** | Proposed · Approved · In Progress · Complete · Rejected · Rolled Back |
| **Required Schema Fields** | `id` · `change_title` · `asset_ids[]` · `change_type` (config \| code \| schema \| infrastructure \| policy) · `risk_level` · `approver_id` · `rollback_plan` · `scheduled_at` · `status` · `completion_evidence` |
| **Validation Rules** | Must define `rollback_plan` before approval — no Change Control is approved without a rollback plan. Must have `approver_id`. Tier-0 asset changes require P0-level approval. All completed changes must log `completion_evidence`. Rejected changes must document the rejection reason. |
| **Examples from Open Empire** | Phase 5/6 trading consolidation (approved Nathan 2026-07-31) · Kelly NO-fix exemption (do not modify kelly.py — permanent) · Kalshi V2 API migration (approved 2026-07-30) · GPT-4o removal from signal chain (approved 2026-08-02) · trading/ git init (pending Nathan approval) |
| **Cross References** | L6: Migration State, Versioning · L2: Approval Types, Council · L5: Risk Levels |
| **Notes** | **KELLY NO-FIX is an active Change Control decision.** `trading.shared.kelly` (kelly.py) is preserved verbatim. This constraint is permanent until Nathan issues an explicit superseding directive. It is recorded here at the Taxonomy level as an immutable constraint. |

---

### Drift Detection

| Field | Value |
|---|---|
| **Canonical Name** | Drift Detection |
| **Canonical Definition** | An automated or scheduled comparison between the registered/expected state of an asset and its actual current state — identifying unauthorized, unintended, or silent deviations from the governed baseline. |
| **Purpose within Open Empire** | Maintains integrity between the Registry (what we think is deployed) and reality (what is actually running). Prevents silent divergence from becoming invisible technical debt. |
| **Parent Layer** | Layer 6 — Evolution |
| **Parent Asset** | Registry (source of expected state) · Automation (executing detection) |
| **Child Asset Types** | None |
| **Allowed Relationships** | COMPARES Registry state vs Current State · ALERTS_TO Dashboard · TRIGGERS Change Control (if drift confirmed and requires remediation) · GOVERNED_BY Policy (drift tolerance policy) |
| **Lifecycle Applicability** | Active · Alert-Open · Resolved · Suppressed |
| **Required Schema Fields** | `id` · `asset_id` · `detection_method` (config_hash \| process_check \| api_probe \| schema_diff) · `expected_state_ref` · `detected_at` · `drift_description` · `severity` · `status` · `resolution_ref` |
| **Validation Rules** | Must define `detection_method`. Must reference `expected_state_ref`. Severity must map to canonical Risk Level scale. Unresolved P0 drifts escalate to Nathan within 15 minutes. Suppressed detections must document suppression justification and expiry. |
| **Examples from Open Empire** | PM2 process count drift (expected 27 online vs detected fewer → alert) · API version drift (Kalshi V1 calls post-migration → alert) · Config drift (spend cap removed from env → P0) · Signal chain drift (GPT-4o reinserted without approval → P0) |
| **Cross References** | L6: Current State, Change Control · L4: Registry · L5: Verification Methods |
| **Notes** | trading_sentinel (PM2 id=41) is the primary Drift Detection agent for the trading stack. A signal chain that doesn't match the approved Haiku→Ollama→Heuristic sequence triggers an immediate P0 alert. |

---

### Schema Evolution

| Field | Value |
|---|---|
| **Canonical Name** | Schema Evolution |
| **Canonical Definition** | The governed process by which the data structures, field definitions, and format specifications of Open Empire assets, databases, and registries change over time — maintaining backward compatibility and audit continuity. |
| **Purpose within Open Empire** | Enables the Taxonomy, Schema, Registry, and databases to grow without breaking existing data or downstream consumers. Manages the evolution of the language of Open Empire itself. |
| **Parent Layer** | Layer 6 — Evolution |
| **Parent Asset** | Database · API · Registry · Taxonomy (this document) |
| **Child Asset Types** | None |
| **Allowed Relationships** | APPLIED_TO Database · APPLIED_TO API · APPLIED_TO Registry · GOVERNS Versioning · REQUIRES Change Control · VALIDATED_BY Verification Method |
| **Lifecycle Applicability** | Stable · Evolving · Breaking-Change-Pending · Migrating · Stable (post-migration) |
| **Required Schema Fields** | `id` · `schema_id` · `current_version` · `proposed_change` · `backward_compatible` (bool) · `migration_script_ref` (required if `backward_compatible=false`) · `approved_by` · `effective_date` · `status` |
| **Validation Rules** | Must define `backward_compatible`. If `backward_compatible=false`, must provide `migration_script_ref`. Must have `approved_by`. Breaking schema changes require P0-level approval from Nathan. All schema evolution events must be logged with full before/after documentation. |
| **Examples from Open Empire** | Taxonomy V1.0.0 → V1.1.0 (additive field addition, backward compatible) · Taxonomy V1.x → V2 (breaking redefinition, requires P0 approval) · clawdb PostgreSQL schema addition (new table, backward compatible) · Kalshi API V1 → V2 (breaking, full migration required) |
| **Cross References** | L6: Versioning, Change Control · L3: Database, API · L4: Registry |
| **Notes** | This Taxonomy is itself subject to Schema Evolution. New asset types may be proposed and added as controlled additions. Existing definitions may be clarified. Existing definitions may NOT be silently redefined — that requires a V2 and Change Control. The evolution of this document is governed by this very entry. |

---

# APPENDIX A — DESIGN PRINCIPLES

1. **The Taxonomy is the language.** Every future document must reuse these definitions without alteration.
2. **No silent redefinition.** Clarifications are permitted. Redefinitions require a new version and Change Control.
3. **Every asset has an owner.** Unowned assets are governance violations.
4. **Evidence, not assertion.** Financial and operational decisions require Verified evidence_state.
5. **Rollback before approval.** No change proceeds without a documented rollback plan.
6. **Retirement is not deletion.** Retired assets are archived, not destroyed.
7. **Supersession is permanent record.** All supersession records are immutable.
8. **Spend caps are non-negotiable.** No autonomous financial operation exceeds its cap without explicit Nathan approval.
9. **Nathan is the sovereign override.** No Council, agent, or policy supersedes Nathan's explicit directive.
10. **The Registry instantiates the Taxonomy.** Abstract → concrete through the Registry. The Taxonomy defines the language; the Registry speaks it.

---

# APPENDIX B — LAYER SUMMARY

| Layer | Name | Primary Question Answered |
|---|---|---|
| Layer 1 | Business | What are we building and why? |
| Layer 2 | Governance | Who decides, what rules apply, and how are they enforced? |
| Layer 3 | Engineering | What is the technical foundation? |
| Layer 4 | Operations | What is running right now and how is it managed? |
| Layer 5 | Execution | How do we classify, prioritize, and validate operations? |
| Layer 6 | Evolution | How do assets change over time with continuity and audit? |

---

# APPENDIX C — ASSET COUNT

| Layer | Asset Types | Count |
|---|---|---|
| Layer 1 — Business | Portfolio · Program · Project · Business Capability · Venture · Executive KPI · Business Outcome | 7 |
| Layer 2 — Governance | Council · Executive Role · Ownership Role · Standard · Policy · Playbook · Approval Type · Risk Level · Lifecycle State · Evidence State | 10 |
| Layer 3 — Engineering | Repository · Package · Library · Framework · Model · Model Provider · API · Router · Integration · Environment · Infrastructure · Database · Storage · Secret Metadata | 14 |
| Layer 4 — Operations | Runtime · Service · PM2 Process · Workflow · Automation · Agent · Agent Team · Dashboard · Knowledge Base · Memory Store · Registry | 11 |
| Layer 5 — Execution | Execution Role · Operational Status · Integration Readiness · Business Criticality · Recovery Priority · Relationship Type · Verification Method | 7 |
| Layer 6 — Evolution | Current State · Target State · Migration State · Retirement State · Supersession · Versioning · Change Control · Drift Detection · Schema Evolution | 9 |
| **TOTAL** | | **58** |

---

# APPENDIX D — VERSION HISTORY

| Version | Date | Author | Type | Summary |
|---|---|---|---|---|
| V1.0.0 | 2026-08-04 | Alusi (approved Nathan) | Initial release | All 58 asset types defined across 6 layers. Versioned standard established. |

---

*OPEN EMPIRE ASSET TAXONOMY V1.0.0 — Issued 2026-08-04 — Alusi, Chief of Staff*
*Next scheduled review: 2026-11-04 (Quarterly)*
*Controlled evolution: minor additions via V1.x, breaking changes via V2 with P0 Change Control*
