# OPEN EMPIRE GLOSSARY V1

**Version:** 1.0.0
**Status:** Draft — Pending Validation
**Owner:** Nathan (Sovereign Operator)
**Source:** `~/.openclaw/workspace/governance/OPEN_EMPIRE_ASSET_TAXONOMY_V1.md` (V1.0.0)
**Materialization Date:** 2026-08-05
**Dependencies:** OPEN_EMPIRE_ASSET_TAXONOMY_V1.md (all 58 canonical definitions extracted from this source), OPEN_EMPIRE_CONSTITUTION_V1.md
**Revision History:**
| Version | Date | Author | Change |
|---|---|---|---|
| 1.0.0 | 2026-08-05 | Alusi | Initial materialization under Governance Freeze Order 2026-08-05 |

---

## ABOUT THIS GLOSSARY

This Glossary is the human-readable reference for all canonical terms used across Open Empire governance documents. Every entry in the **Taxonomy Terms** section is extracted verbatim from `OPEN_EMPIRE_ASSET_TAXONOMY_V1.md`. No definition here may contradict the Taxonomy. If a conflict is detected, the Taxonomy prevails.

The **Runtime Terms** section defines additional governance-process terms used in the Governance Freeze and Build Pipeline that are not themselves Taxonomy asset types.

Entries are sorted alphabetically. Total canonical terms: **58 Taxonomy + 11 Runtime = 69 entries**.

---

## TAXONOMY TERMS

*(All definitions extracted verbatim from OPEN_EMPIRE_ASSET_TAXONOMY_V1.md V1.0.0)*

---

### Agent
**Definition:** An AI-driven autonomous execution entity — with defined capabilities, policies, memory scope, and tool access — that carries out tasks on behalf of Open Empire with or without human intervention.
**Layer:** Layer 4 — Operations
**See Also:** L3: Model · L4: Agent Team, Service · L2: Policy, Approval Types

---

### Agent Team
**Definition:** A named, organized group of Agents with complementary roles that collaborate under a shared governance structure to accomplish a complex, ongoing objective.
**Layer:** Layer 4 — Operations
**See Also:** L4: Agent · L2: Council · L5: Execution Roles

---

### API
**Definition:** A versioned programmatic interface — exposed by a service or external system — that Open Empire consumes or publishes, defining the data contract and behavioral guarantees between systems.
**Layer:** Layer 3 — Engineering
**See Also:** L3: Integration, Router · L4: Service, Agent · L6: Schema Evolution

---

### Approval Type
**Definition:** A categorized class of approval action required before a governed operation may proceed — defining the required authority level, delivery mechanism, and time constraints.
**Layer:** Layer 2 — Governance
**See Also:** L2: Policies, Council · L4: Automation, Agent · sovereign_proxy Service

---

### Automation
**Definition:** A single-purpose, repeatable automated action or bounded sequence of actions executed by a system without human intervention — a discrete step within a Workflow or a standalone background task.
**Layer:** Layer 4 — Operations
**See Also:** L4: Workflow, Service · L2: Policy · L3: Integration

---

### Business Capability
**Definition:** A stable, reusable ability that Open Empire possesses and applies across multiple Programs or Projects — independent of any specific technology or implementation.
**Layer:** Layer 1 — Business
**See Also:** L3: Model, API, Integration · L4: Agent, Service · L5: Business Criticality

---

### Business Criticality
**Definition:** A standardized four-tier classification of how critical an asset is to Open Empire's revenue generation, operational continuity, and mission delivery.
**Layer:** Layer 5 — Execution
**See Also:** L2: Risk Levels · L5: Recovery Priority · L4: Service, Agent

---

### Business Outcome
**Definition:** A qualitative or quantitative result that Open Empire intends to achieve through the execution of one or more Programs or Ventures — expressed in terms of value delivered, not tasks completed.
**Layer:** Layer 1 — Business
**See Also:** L1: Executive KPI · L2: Council · L5: Business Criticality

---

### Change Control
**Definition:** The governance process governing when, why, and how Open Empire assets may be modified — requiring pre-approval, documentation, rollback planning, and completion evidence for all significant changes.
**Layer:** Layer 6 — Evolution
**See Also:** L6: Migration State, Versioning · L2: Approval Types, Council · L5: Risk Levels

---

### Council
**Definition:** A named governance body within Open Empire responsible for decision-making, oversight, and accountability within a defined domain.
**Layer:** Layer 2 — Governance
**See Also:** L1: Portfolio, Venture · L2: Executive Roles, Policies · L5: Execution Roles

---

### Current State
**Definition:** A point-in-time, evidence-backed snapshot of an asset's actual operational configuration, status, and characteristics — as-is, without projection or aspiration.
**Layer:** Layer 6 — Evolution
**See Also:** L6: Target State, Migration State · L2: Evidence States · L5: Operational Status

---

### Dashboard
**Definition:** A real-time or near-real-time visualization interface that displays Operational Status, Executive KPIs, and system health across Open Empire assets.
**Layer:** Layer 4 — Operations
**See Also:** L4: Service · L1: Executive KPI · L5: Operational Status

---

### Database
**Definition:** A managed persistent data store used by Open Empire services — identified by engine, version, host, and logical schema — for structured, queryable data persistence.
**Layer:** Layer 3 — Engineering
**See Also:** L3: Infrastructure, Storage · L4: Service · L6: Schema Evolution

---

### Drift Detection
**Definition:** An automated or scheduled comparison between the registered/expected state of an asset and its actual current state — identifying unauthorized, unintended, or silent deviations from the governed baseline.
**Layer:** Layer 6 — Evolution
**See Also:** L6: Current State, Change Control · L4: Registry · L5: Verification Methods

---

### Environment
**Definition:** A named, isolated runtime context in which Open Empire services operate — distinguishing between local development, staging, and production deployments with scoped configurations and secrets.
**Layer:** Layer 3 — Engineering
**See Also:** L3: Infrastructure, Secret Metadata · L4: Service, Runtime

---

### Evidence State
**Definition:** A standardized classification of the verification status of a fact, claim, metric, or operational condition within Open Empire — indicating how well-supported the information is.
**Layer:** Layer 2 — Governance
**See Also:** L2: Verification Methods · L5: Operational Status

---

### Execution Role
**Definition:** A named operational role at the task execution level — assigned to an agent or human responsible for carrying out specific recurring operational duties within a defined scope.
**Layer:** Layer 5 — Execution
**See Also:** L2: Executive Roles, Ownership Roles · L4: Agent, Automation

---

### Executive KPI
**Definition:** A quantifiable, time-bound performance indicator tracked at the Portfolio, Program, or Venture level to assess progress against strategic objectives.
**Layer:** Layer 1 — Business
**See Also:** L4: Dashboard · L5: Operational Status · L2: Evidence States

---

### Executive Role
**Definition:** A named, accountable authority role at the strategic level of Open Empire — assigned to an individual or agent with full decision-making authority within a defined domain.
**Layer:** Layer 2 — Governance
**See Also:** L2: Council, Ownership Roles · L5: Execution Roles

---

### Framework
**Definition:** A foundational software system that provides structure, conventions, and core capabilities upon which Open Empire services and agents are built.
**Layer:** Layer 3 — Engineering
**See Also:** L3: Infrastructure, Environment · L4: Runtime, Service

---

### Infrastructure
**Definition:** The physical or virtual compute, network, and storage resources that host Open Empire environments and services — the foundational physical layer.
**Layer:** Layer 3 — Engineering
**See Also:** L3: Environment, Database · L2: Security Policy

---

### Integration
**Definition:** A configured connection between Open Empire and an external system — encapsulating authentication, data mapping, error handling, and circuit-breaking for a specific external API or data source.
**Layer:** Layer 3 — Engineering
**See Also:** L3: API, Secret Metadata · L4: Service, Automation

---

### Integration Readiness
**Definition:** A standardized assessment of whether an Integration is ready for production use — covering authentication verification, endpoint reachability, error handling validation, and end-to-end transaction confirmation.
**Layer:** Layer 5 — Execution
**See Also:** L3: Integration, API · L5: Verification Methods · L2: Evidence States

---

### Knowledge Base
**Definition:** A curated, structured collection of domain knowledge, operational procedures, market intelligence, and reference data — accessible to agents and humans for decision support.
**Layer:** Layer 4 — Operations
**See Also:** L4: Memory Store · L2: Playbook · L3: Storage

---

### Library
**Definition:** A reusable module of shared code providing discrete, composable functionality — imported by other packages or services but not independently deployable.
**Layer:** Layer 3 — Engineering
**See Also:** L3: Package, Framework · L4: Agent, Service

---

### Lifecycle State
**Definition:** A standardized enumeration of states that an Open Empire asset may occupy, from inception through retirement — providing the universal state machine for all asset types.
**Layer:** Layer 2 — Governance
**See Also:** L6: Current State, Target State, Retirement State · L2: Approval Types

---

### Memory Store
**Definition:** A persistent or semi-persistent storage layer that enables agents and the system to retain context, state, and accumulated knowledge across session boundaries.
**Layer:** Layer 4 — Operations
**See Also:** L4: Knowledge Base · L3: Storage · L4: Agent

---

### Migration State
**Definition:** The active transitional state of an asset or system moving from its Current State toward a defined Target State — tracking progress, intermediate steps, risks, and blockers.
**Layer:** Layer 6 — Evolution
**See Also:** L6: Current State, Target State, Change Control · L2: Risk Levels

---

### Model
**Definition:** An AI/ML model — identified by provider, name, and version — used by Open Empire agents and services for inference, classification, generation, or scoring.
**Layer:** Layer 3 — Engineering
**See Also:** L3: Model Provider, Router · L2: Model Dispatch Policy · L4: Agent

---

### Model Provider
**Definition:** An organization or local system that hosts and serves one or more AI Models accessible to Open Empire via API or local inference endpoint.
**Layer:** Layer 3 — Engineering
**See Also:** L3: Model · L3: Secret Metadata · L2: Model Dispatch Policy

---

### Operational Status
**Definition:** A standardized real-time state indicator for a running Service, Agent, or Automation — reflecting its current health and availability as observed by monitoring systems.
**Layer:** Layer 5 — Execution
**See Also:** L4: Dashboard · L2: Evidence States, Lifecycle States · L1: Executive KPI

---

### Ownership Role
**Definition:** A named, accountable operational role responsible for day-to-day stewardship of one or more specific assets — beneath Executive authority but above execution-level task completion.
**Layer:** Layer 2 — Governance
**See Also:** L2: Executive Roles, Council · L4: Service, Agent, Registry

---

### Package
**Definition:** A distributable, versioned module within a Repository that can be imported or installed as a discrete unit of functionality.
**Layer:** Layer 3 — Engineering
**See Also:** L3: Repository, Library · L4: Service, Agent

---

### Playbook
**Definition:** A versioned, step-by-step operational procedure that implements one or more Policies — executable by an agent, human, or automated system.
**Layer:** Layer 2 — Governance
**See Also:** L2: Policies, Council · L4: Agent, Automation · L5: Verification Methods

---

### PM2 Process
**Definition:** A specific process instance managed by the PM2 process manager — identified by PM2 numeric id, name, and ecosystem config — responsible for starting, monitoring, and restarting a Service.
**Layer:** Layer 4 — Operations
**See Also:** L4: Service, Runtime · L3: Infrastructure, Environment

---

### Policy
**Definition:** A mandatory, enforceable rule governing behavior, decision-making, or operations within Open Empire — defining WHAT must happen, issued by a Council or Executive Role.
**Layer:** Layer 2 — Governance
**See Also:** L2: Council, Standards, Playbooks · L5: Approval Types, Risk Levels

---

### Portfolio
**Definition:** A governed collection of Programs and Ventures aligned to a single sovereign mission, managed as a unified capital and strategic asset.
**Layer:** Layer 1 — Business
**See Also:** L2: Council · L1: Program, Venture, Executive KPI, Business Outcome

---

### Program
**Definition:** A coordinated grouping of Projects and Business Capabilities that together deliver a strategic Business Outcome within a Portfolio.
**Layer:** Layer 1 — Business
**See Also:** L2: Council · L5: Execution Roles · L6: Current State

---

### Project
**Definition:** A time-boxed, scope-defined unit of work within a Program that produces one or more deliverables with measurable completion criteria.
**Layer:** Layer 1 — Business
**See Also:** L2: Lifecycle States · L5: Operational Status · L6: Change Control

---

### Recovery Priority
**Definition:** A ranked ordering of asset restoration priority during a system outage — defining the pre-approved sequence in which services are recovered to minimize business impact.
**Layer:** Layer 5 — Execution
**See Also:** L5: Business Criticality · L2: Risk Levels · L4: Service

---

### Registry
**Definition:** A governed, queryable catalog of all Open Empire assets of a specific type — providing a single source of truth for discovery, governance, and audit.
**Layer:** Layer 4 — Operations
**See Also:** L4: Dashboard, Knowledge Base · L2: Council · L1: Portfolio

---

### Relationship Type
**Definition:** A standardized, directed connection type between two Open Empire assets — defining how they interact, depend on, or govern each other within the asset graph.
**Layer:** Layer 5 — Execution
**See Also:** All asset types (Allowed Relationships field)

---

### Repository
**Definition:** A version-controlled code storage unit (Git repository) containing the source of one or more Open Empire services, libraries, agents, or configurations.
**Layer:** Layer 3 — Engineering
**See Also:** L3: Package, Library · L4: Service · L6: Versioning, Change Control

---

### Retirement State
**Definition:** The final operational state of an asset that has been intentionally decommissioned — no longer active, archived for audit continuity, and excluded from operational registries.
**Layer:** Layer 6 — Evolution
**See Also:** L6: Supersession, Versioning · L2: Lifecycle States, Approval Types

---

### Risk Level
**Definition:** A standardized severity classification applied to assets, operations, and decisions — quantifying potential business impact if a failure, breach, or adverse event occurs.
**Layer:** Layer 2 — Governance
**See Also:** L2: Approval Types, Policy · L5: Recovery Priority, Business Criticality

---

### Router
**Definition:** A system component that inspects incoming requests or signals and routes them to the appropriate handler, model, or service based on defined, ordered rules.
**Layer:** Layer 3 — Engineering
**See Also:** L3: Model, API · L4: Service, Automation

---

### Runtime
**Definition:** The active execution environment in which a Service or Agent operates at a given moment — including process, interpreter, memory state, and loaded configuration.
**Layer:** Layer 4 — Operations
**See Also:** L3: Package, Environment · L4: PM2 Process, Service

---

### Schema Evolution
**Definition:** The governed process by which the data structures, field definitions, and format specifications of Open Empire assets, databases, and registries change over time — maintaining backward compatibility and audit continuity.
**Layer:** Layer 6 — Evolution
**See Also:** L6: Versioning, Change Control · L3: Database, API · L4: Registry

---

### Secret Metadata
**Definition:** A governance record describing a secret (API key, private key, credential) — containing everything EXCEPT the secret value itself — used for lifecycle tracking, rotation management, and audit.
**Layer:** Layer 3 — Engineering
**See Also:** L3: Integration, API · L2: Secret Management Policy · L5: Verification Methods

---

### Service
**Definition:** A long-running, named operational process that provides continuous capability to Open Empire — independently deployable, monitored, and owned.
**Layer:** Layer 4 — Operations
**See Also:** L3: Repository, API · L4: PM2 Process, Runtime · L5: Operational Status, Recovery Priority

---

### Standard
**Definition:** A mandatory, versioned technical or operational specification that all Open Empire assets must comply with — defining HOW something must be done.
**Layer:** Layer 2 — Governance
**See Also:** L2: Council, Policies · L3: Repository, API · L5: Verification Methods

---

### Storage
**Definition:** A file-based or object-based data persistence layer used for non-relational data — logs, documents, media, exports, and raw data files.
**Layer:** Layer 3 — Engineering
**See Also:** L3: Database, Infrastructure · L4: Memory Store · L6: Drift Detection

---

### Supersession
**Definition:** A formal replacement relationship record where one asset explicitly replaces another — documenting the transition of authority, capability, and reference from the predecessor to the successor.
**Layer:** Layer 6 — Evolution
**See Also:** L6: Retirement State, Migration State, Change Control · L3: Repository

---

### Target State
**Definition:** A defined, approved future configuration of an asset or system — specifying what it should look like, how it should behave, and what measurable criteria confirm it has been achieved.
**Layer:** Layer 6 — Evolution
**See Also:** L6: Current State, Migration State, Change Control · L2: Council

---

### Venture
**Definition:** A revenue-generating or revenue-targeting operational unit within Open Empire — a distinct line of business with its own capital allocation, P&L accountability, and go-to-market strategy.
**Layer:** Layer 1 — Business
**See Also:** L2: Council, Risk Levels · L5: Business Criticality, Recovery Priority

---

### Verification Method
**Definition:** A standardized technique used to confirm that an asset, integration, or operational condition is functioning as expected and meets its defined requirements.
**Layer:** Layer 5 — Execution
**See Also:** L2: Evidence States, Standards · L5: Integration Readiness, Operational Status

---

### Versioning
**Definition:** A standardized system for assigning, tracking, and communicating the version identity of Open Empire assets — enabling change tracking, rollback, and compatibility management across the entire stack.
**Layer:** Layer 6 — Evolution
**See Also:** L6: Change Control, Supersession · L3: Repository, API · L2: Standards

---

### Workflow
**Definition:** A defined, multi-step automated process — with explicit triggers, sequenced steps, branching logic, and completion criteria — that orchestrates multiple services or agents toward a business outcome.
**Layer:** Layer 4 — Operations
**See Also:** L4: Automation, Agent · L2: Playbook · L3: Integration

---

## RUNTIME TERMS

*These terms are not Taxonomy asset types but are used in governance operations, the Governance Freeze, and the Build Pipeline. They are defined here as supplementary governance vocabulary.*

---

### Build Pipeline
**Definition:** The automated toolchain that reads canonical Markdown governance documents and produces JSON, YAML, dependency graph, glossary, validation results, release manifest, SHA256SUMS, and rollback manifest.
**See Also:** Governance Baseline, Change Control, Versioning

---

### Canonical Path
**Definition:** The single authoritative filesystem location for a governance document, code module, or data file. No duplicates permitted. Any reference to a canonical asset must use its canonical path — never an alias, symlink target, or legacy path.
**See Also:** Repository, Storage, Package

---

### Change Control *(Runtime usage)*
**Definition:** In runtime governance context, Change Control refers to the mandatory process for modifying any governance document after Baseline V1.0.0: Change Proposal → Review → Validation → Approval → Versioned Release. Operationally distinct from informal edits or agent-initiated changes. See also the Taxonomy entry for **Change Control** (Layer 6 — Evolution).
**See Also:** Governance Baseline, OPEN_EMPIRE_CONSTITUTION_V1.md Section 8

---

### Daily Spend Cap
**Definition:** A per-Venture hard limit on autonomous financial operations within a rolling 24-hour window. Mandatory for all Ventures with trading or payment agents. Enforced at agent code level against the sum of placed `size_usd` in `trades.jsonl` over the last 24 hours. Current active caps: `CASHCLAW_DAILY_SPEND_CAP_USD=10`, `ARB_DAILY_SPEND_CAP_USD=10`, `POLY_DAILY_SPEND_CAP_USD=10`.
**See Also:** Venture, Agent, ADR-003

---

### Governance Baseline
**Definition:** The published V1.0.0 set of all 12 canonical governance documents, validated by the Validation Suite and released via the Build Pipeline. Governance Baseline completion is the prerequisite for `TRACK_B_AUTHORIZED`.
**See Also:** Build Pipeline, TRACK_B_AUTHORIZED, Change Control

---

### Kelly NO-fix
**Definition:** The locked status of `~/.openclaw/trading/shared/kelly.py`. The Kelly criterion implementation must not be modified without an explicit Nathan directive. This constraint is permanent until superseded by an explicit Nathan directive. Recorded in ADR-005.
**See Also:** Library, Change Control, ADR-005, Signal Chain Lock

---

### Materialization Date
**Definition:** The date a governance document was first committed to its canonical filesystem path. Distinct from the effective date of the policy it encodes. Used in the document header of every governance artifact produced under the Governance Freeze Order.
**See Also:** Canonical Path, Governance Baseline, Versioning

---

### Signal Chain Lock
**Definition:** The locked canonical signal chain for all Open Empire trading operations: Haiku → Ollama → Heuristic. GPT-4o is not permitted in any real-time scoring chain without an explicit Nathan directive. Recorded in ADR-004.
**See Also:** Model, Router, Agent, Kelly NO-fix, ADR-004

---

### Sovereign Operator
**Definition:** Nathan. Final and supreme authority on all Open Empire decisions. Cannot be overridden by any agent, council, policy, or system. Holds the Sovereign Operator Executive Role with no escalation path. All autonomous operations require explicit or standing authorization from the Sovereign Operator.
**See Also:** Executive Role, Council, OPEN_EMPIRE_CONSTITUTION_V1.md Section 2

---

### TODO_PENDING_APPROVAL
**Definition:** A governance placeholder for any item that requires an explicit Nathan directive to resolve. Documents may be materialized with this placeholder; it does not block V1.0.0 release but must be resolved before V1.1.0. When this placeholder appears in a governance document, it marks a gap that Nathan must explicitly decide.
**See Also:** Change Control, Governance Baseline, Sovereign Operator

---

### TRACK_B_AUTHORIZED
**Definition:** The formal declaration that Governance Baseline V1.0.0 is complete and Open Empire is authorized to transition to full implementation (Track B). Track B begins immediately after this declaration. Track A (governance architecture) is frozen at the point of this declaration. No new governance artifacts may be created after `TRACK_B_AUTHORIZED` without a formal Change Control.
**See Also:** Governance Baseline, Build Pipeline, Change Control

---

## LAYER SUMMARY

| Layer | Count | Asset Types |
|---|---|---|
| Layer 1 — Business | 7 | Portfolio · Program · Project · Business Capability · Venture · Executive KPI · Business Outcome |
| Layer 2 — Governance | 10 | Council · Executive Role · Ownership Role · Standard · Policy · Playbook · Approval Type · Risk Level · Lifecycle State · Evidence State |
| Layer 3 — Engineering | 14 | Repository · Package · Library · Framework · Model · Model Provider · API · Router · Integration · Environment · Infrastructure · Database · Storage · Secret Metadata |
| Layer 4 — Operations | 11 | Runtime · Service · PM2 Process · Workflow · Automation · Agent · Agent Team · Dashboard · Knowledge Base · Memory Store · Registry |
| Layer 5 — Execution | 7 | Execution Role · Operational Status · Integration Readiness · Business Criticality · Recovery Priority · Relationship Type · Verification Method |
| Layer 6 — Evolution | 9 | Current State · Target State · Migration State · Retirement State · Supersession · Versioning · Change Control · Drift Detection · Schema Evolution |
| Runtime Terms | 11 | Build Pipeline · Canonical Path · Change Control (runtime) · Daily Spend Cap · Governance Baseline · Kelly NO-fix · Materialization Date · Signal Chain Lock · Sovereign Operator · TODO_PENDING_APPROVAL · TRACK_B_AUTHORIZED |
| **TOTAL** | **69** | |

---

*OPEN EMPIRE GLOSSARY V1.0.0 — Materialized 2026-08-05 — Alusi, Chief of Staff*
*Source: OPEN_EMPIRE_ASSET_TAXONOMY_V1.0.0 (58 terms) + Governance Freeze Runtime Terms (11 terms)*
*Governed by: Governance Freeze Order 2026-08-05*
