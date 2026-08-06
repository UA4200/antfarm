# OPEN EMPIRE ONTOLOGY V1
## Valid Relationships Between All Open Empire Asset Types

**Version:** 1.0.0
**Status:** Draft — Pending Validation
**Owner:** Nathan (Sovereign Operator)
**Source:** `~/.openclaw/workspace/governance/OPEN_EMPIRE_ASSET_TAXONOMY_V1.md`
**Materialization Date:** 2026-08-05
**Dependencies:** OPEN_EMPIRE_ASSET_TAXONOMY_V1.md (must remain the authoritative source for all asset type definitions and relationship declarations)
**Revision History:**
| Version | Date | Author | Change |
|---|---|---|---|
| 1.0.0 | 2026-08-05 | Alusi | Initial materialization under Governance Freeze Order 2026-08-05 |

---

## PREAMBLE

This Ontology is a formal directed graph of all valid relationships between Open Empire asset types. It is derived exclusively from the `Allowed Relationships` fields of the OPEN_EMPIRE_ASSET_TAXONOMY_V1.md.

**Authority hierarchy:**
- The Taxonomy is the source of truth. This Ontology implements it.
- No relationship may exist in the Registry that is not defined here.
- No relationship verb may be used that is not defined in Section 1.
- Any proposed relationship not in this Ontology requires a Taxonomy minor version update before use.

**Reading this document:**
- Relationships are directed: `Source → VERB → Target`
- Where an inverse exists, it is noted; the inverse is also a valid relationship in its own right.
- "Multiplicity" describes how many targets one source may have: `1:1`, `1:N`, `M:N`.

---

# SECTION 1 — RELATIONSHIP VOCABULARY

All verbs used in the Open Empire asset graph, derived from Taxonomy `Allowed Relationships` fields.

---

## ACCESSED_BY
- **Direction:** Source (Database/Storage/Memory Store) → ACCESSED_BY → Target (Service/Agent)
- **Meaning:** The source asset is read or written by the target asset during normal operation.
- **Inverse:** USES / READS (implicit; no canonical inverse verb)
- **Multiplicity:** One-to-many (one Database accessed by many Services/Agents)

---

## ACHIEVED_BY
- **Direction:** Source (Target State) → ACHIEVED_BY → Target (Migration State)
- **Meaning:** The Target State's success criteria are confirmed complete by the execution of the referenced Migration State.
- **Inverse:** PROGRESSES_TOWARD
- **Multiplicity:** One-to-one

---

## ALERTS_TO
- **Direction:** Source (Drift Detection) → ALERTS_TO → Target (Dashboard)
- **Meaning:** A drift event surfaces an alert on the target Dashboard.
- **Inverse:** None
- **Multiplicity:** One-to-one

---

## APPLIED_TO
- **Direction:** Source (Standard/Risk Level/Lifecycle State/Operational Status/Business Criticality/Recovery Priority/Versioning/Schema Evolution) → APPLIED_TO → Target (various asset types)
- **Meaning:** A classification, standard, or versioning scheme is assigned to the target asset. Read as "Standard X applies to Repository Y."
- **Inverse:** None (classification is unidirectional)
- **Multiplicity:** One-to-many (one Standard applied to many Repositories/APIs/Databases)

---

## APPROVED_BY
- **Direction:** Source (Target State/Retirement State/Supersession/Change Control) → APPROVED_BY → Target (Council/Executive Role/Approval Type)
- **Meaning:** The source artifact requires explicit authorization from the target authority before it may proceed or take effect.
- **Inverse:** None
- **Multiplicity:** One-to-one (exactly one approver per governed event)

---

## ARCHIVED_IN
- **Direction:** Source (Retirement State) → ARCHIVED_IN → Target (Storage)
- **Meaning:** Retired assets are preserved in the target Storage path for audit continuity.
- **Inverse:** None
- **Multiplicity:** One-to-one

---

## ASSESSED_FOR
- **Direction:** Source (Integration Readiness) → ASSESSED_FOR → Target (Integration)
- **Meaning:** An Integration Readiness record evaluates the production-readiness of a specific Integration.
- **Inverse:** None
- **Multiplicity:** One-to-one

---

## ASSIGNED_TO
- **Direction:** Source (Executive Role) → ASSIGNED_TO → Target (Council)
- **Meaning:** An Executive Role is formally placed under the authority of a Council.
- **Inverse:** ASSIGNS
- **Multiplicity:** One-to-one (each Executive Role belongs to exactly one Council)

---

## ASSIGNS
- **Direction:** Source (Council) → ASSIGNS → Target (Executive Role)
- **Meaning:** A Council formally designates an Executive Role to a holder within its domain.
- **Inverse:** ASSIGNED_TO
- **Multiplicity:** One-to-many (one Council may assign multiple Executive Roles)

---

## AUTHENTICATED_VIA
- **Direction:** Source (Model Provider/Integration) → AUTHENTICATED_VIA → Target (Secret Metadata)
- **Meaning:** The source asset uses credentials described by the target Secret Metadata record for authentication.
- **Inverse:** DESCRIBES
- **Multiplicity:** One-to-one (each authentication relationship references exactly one Secret Metadata record)

---

## BACKED_UP_BY / BACKED_UP_TO
- **Direction:** Source (Database) → BACKED_UP_BY → Target (Automation); Source (Memory Store) → BACKED_UP_TO → Target (Storage)
- **Meaning:** The source asset's data is preserved by the target Automation or copied to the target Storage for disaster recovery.
- **Inverse:** None
- **Multiplicity:** One-to-one or One-to-many

---

## BELONGS_TO
- **Direction:** Source (Program/Project/Venture) → BELONGS_TO → Target (Portfolio/Program)
- **Meaning:** The source asset is owned and governed by the target asset in the hierarchy.
- **Inverse:** CONTAINS
- **Multiplicity:** Many-to-one (many Programs belong to one Portfolio; many Projects belong to one Program)

---

## BILLED_TO
- **Direction:** Source (Model Provider) → BILLED_TO → Target (Venture)
- **Meaning:** AI inference costs from the Model Provider are charged against the target Venture's capital allocation.
- **Inverse:** None
- **Multiplicity:** One-to-one (each Model Provider is billed to one Venture cost center)

---

## CAPTURED_BY
- **Direction:** Source (Current State) → CAPTURED_BY → Target (Automation)
- **Meaning:** The point-in-time state snapshot is produced by the target Automation.
- **Inverse:** None
- **Multiplicity:** One-to-one

---

## CARRIES
- **Direction:** Source (Project/Venture/Executive KPI) → CARRIES → Target (Risk Level/Evidence State)
- **Meaning:** The source asset is tagged with the target classification value.
- **Inverse:** APPLIED_TO (partial inverse — APPLIED_TO is broader)
- **Multiplicity:** One-to-one (one risk_level per asset; one evidence_state per KPI)

---

## CATALOGS
- **Direction:** Source (Registry) → CATALOGS → Target (all asset types)
- **Meaning:** The Registry maintains an authoritative record of all instances of the target asset type.
- **Inverse:** None
- **Multiplicity:** One-to-many

---

## CHAIRS
- **Direction:** Source (Executive Role) → CHAIRS → Target (Council)
- **Meaning:** The Executive Role holder presides over the Council and is its accountable authority.
- **Inverse:** None
- **Multiplicity:** One-to-one (each Council has exactly one Chair)

---

## COMPARES
- **Direction:** Source (Drift Detection) → COMPARES → Target (Registry state vs Current State)
- **Meaning:** The Drift Detection mechanism evaluates the divergence between the expected state (Registry) and the actual state (Current State).
- **Inverse:** None
- **Multiplicity:** One-to-many (one Drift Detection process may compare many assets)

---

## CONSUMED_BY
- **Direction:** Source (API/Knowledge Base) → CONSUMED_BY → Target (Integration/Agent/Playbook)
- **Meaning:** The source asset is actively used as input by the target asset.
- **Inverse:** CONSUMES
- **Multiplicity:** One-to-many

---

## CONSUMES
- **Direction:** Source (Router/Integration/Automation/Agent) → CONSUMES → Target (API/Integration)
- **Meaning:** The source asset makes active use of the target asset's interface or data.
- **Inverse:** CONSUMED_BY
- **Multiplicity:** Many-to-many (many agents/automations consume many APIs)

---

## CONTAINED_IN
- **Direction:** Source (Package/Library) → CONTAINED_IN → Target (Repository/Package)
- **Meaning:** The source module is physically housed within the target Repository or Package.
- **Inverse:** CONTAINS
- **Multiplicity:** Many-to-one

---

## CONTAINS
- **Direction:** Source (Portfolio/Program/Venture/Repository/Package/Agent Team) → CONTAINS → Target (Program/Venture/Project/Package/Library/Agent)
- **Meaning:** The source asset is the direct parent container of the target asset.
- **Inverse:** BELONGS_TO / CONTAINED_IN
- **Multiplicity:** One-to-many

---

## CONTRASTED_WITH
- **Direction:** Source (Current State/Target State) → CONTRASTED_WITH → Target (Target State/Current State)
- **Meaning:** The source state document is compared against the target state document to identify gaps.
- **Inverse:** CONTRASTED_WITH (symmetric)
- **Multiplicity:** One-to-one

---

## CURATED_BY
- **Direction:** Source (Knowledge Base) → CURATED_BY → Target (Ownership Role)
- **Meaning:** The Ownership Role is responsible for maintaining the accuracy and currency of the Knowledge Base.
- **Inverse:** OWNS (partial)
- **Multiplicity:** Many-to-one

---

## DEFINED_BY / DEFINED_IN
- **Direction:** Source (Framework/Recovery Priority) → DEFINED_BY → Target (Standard/Playbook); Source (PM2 Process) → DEFINED_IN → Target (ecosystem config)
- **Meaning:** The source asset's specification or configuration is authoritatively established by the target document.
- **Inverse:** None
- **Multiplicity:** One-to-one

---

## DELIVERS / DELIVERED_BY
- **Direction:** Source (Program) → DELIVERS → Target (Business Outcome); Source (Business Outcome) → DELIVERED_BY → Target (Program/Venture)
- **Meaning:** The Program or Venture is the mechanism through which the Business Outcome is achieved.
- **Inverse:** DELIVERS ↔ DELIVERED_BY
- **Multiplicity:** Many-to-many (one Program may deliver multiple Outcomes; one Outcome may be delivered by multiple Programs)

---

## DEPLOYS_TO
- **Direction:** Source (Repository) → DEPLOYS_TO → Target (Service)
- **Meaning:** The code in the Repository is deployed and runs as the target Service.
- **Inverse:** None (Service does not formally reference Repository in its Allowed Relationships)
- **Multiplicity:** One-to-many (one Repository may deploy to multiple Services)

---

## DESCRIBES
- **Direction:** Source (Secret Metadata) → DESCRIBES → Target (Integration/Service/Agent)
- **Meaning:** The Secret Metadata record governs the credential lifecycle for the target asset's authentication requirements.
- **Inverse:** AUTHENTICATED_VIA (partial)
- **Multiplicity:** One-to-many (one Secret Metadata record may describe credentials used by multiple consuming assets)

---

## DETERMINES
- **Direction:** Source (Risk Level/Business Criticality) → DETERMINES → Target (Approval Type/Recovery Priority)
- **Meaning:** The source classification directly dictates which Approval Type gates a change and what Recovery Priority is assigned.
- **Inverse:** None
- **Multiplicity:** Many-to-one (many P0 assets share the same Recovery Priority class)

---

## DISPLAYED_BY / DISPLAYS
- **Direction:** Source (Executive KPI/Lifecycle State) → DISPLAYED_BY → Target (Dashboard); Source (Dashboard) → DISPLAYS → Target (Operational Status/Executive KPI)
- **Meaning:** The source metric or state is rendered visible in the target Dashboard.
- **Inverse:** DISPLAYED_BY ↔ DISPLAYS
- **Multiplicity:** One-to-many (Dashboard displays many KPIs/statuses)

---

## DOCUMENTED_BY
- **Direction:** Source (API/Retirement State/Supersession) → DOCUMENTED_BY → Target (Standard/Registry)
- **Meaning:** The source asset's specification, retirement record, or provenance chain is formally captured by the target artifact.
- **Inverse:** None
- **Multiplicity:** One-to-one or One-to-many

---

## ENABLED_BY
- **Direction:** Source (Business Capability) → ENABLED_BY → Target (Service/Agent/Integration)
- **Meaning:** The abstract capability is made operationally possible by the target technical asset.
- **Inverse:** None (Services/Agents do not formally declare ENABLES in their Allowed Relationships)
- **Multiplicity:** One-to-many (one capability enabled by many technical assets)

---

## ENFORCED_BY / ENFORCES
- **Direction:** Source (Standard) → ENFORCED_BY → Target (Council); Source (Council) → ENFORCES → Target (Policy); Source (Policy) → ENFORCED_BY → Target (Execution Role)
- **Meaning:** The source artifact's compliance is actively verified and maintained by the target authority.
- **Inverse:** ENFORCED_BY ↔ ENFORCES
- **Multiplicity:** Many-to-one (many Standards enforced by one Council)

---

## ESCALATES_TO
- **Direction:** Source (Council/Executive Role) → ESCALATES_TO → Target (Council/Executive Role)
- **Meaning:** When a decision or issue exceeds the source's authority scope, it is formally elevated to the target.
- **Inverse:** None
- **Multiplicity:** One-to-one (each authority has exactly one escalation path; exception: Nathan has none)

---

## EVALUATED_BY
- **Direction:** Source (Executive KPI) → EVALUATED_BY → Target (Council)
- **Meaning:** The Council formally reviews and assesses the KPI as part of its governance function.
- **Inverse:** None
- **Multiplicity:** Many-to-one

---

## EVIDENCE_PROVIDED_BY
- **Direction:** Source (Current State) → EVIDENCE_PROVIDED_BY → Target (Evidence State)
- **Meaning:** The Current State snapshot carries a classification of how well its data is verified.
- **Inverse:** None
- **Multiplicity:** One-to-one

---

## EXECUTES / EXECUTED_BY
- **Direction:** Source (Playbook/Automation) → EXECUTED_BY → Target (Agent/Execution Role/Service/Automation); Source (Agent/Execution Role) → EXECUTES → Target (Playbook/Automation/Agent Task)
- **Meaning:** The source procedure or task is carried out by the target actor.
- **Inverse:** EXECUTES ↔ EXECUTED_BY
- **Multiplicity:** Many-to-many

---

## EXPOSES / EXPOSED_BY
- **Direction:** Source (Service) → EXPOSES → Target (API); Source (API) → EXPOSED_BY → Target (Service)
- **Meaning:** The Service makes its interface available through the target API specification.
- **Inverse:** EXPOSES ↔ EXPOSED_BY
- **Multiplicity:** One-to-many (one Service may expose multiple APIs)

---

## GATES
- **Direction:** Source (Integration Readiness) → GATES → Target (Lifecycle State transition)
- **Meaning:** The Integration Readiness assessment must be in a qualifying state before the target lifecycle transition (e.g., Staging→Active) may proceed.
- **Inverse:** None
- **Multiplicity:** One-to-one

---

## GOVERNED_BY / GOVERNS
- **Direction:** Source (many) → GOVERNED_BY → Target (Council/Policy/Standard/Playbook/Change Control); Source (Council/Executive Role) → GOVERNS → Target (Portfolio/Program/Venture/Policy)
- **Meaning:** The source asset is subject to the authority, rules, and oversight of the target governance artifact.
- **Inverse:** GOVERNED_BY ↔ GOVERNS
- **Multiplicity:** Many-to-one (many assets may be governed by one Council/Policy)

---

## GOVERNS_CONTRACT_FOR
- **Direction:** Source (API) → GOVERNS_CONTRACT_FOR → Target (Integration)
- **Meaning:** The API specification defines the data contract and behavioral guarantees that the Integration must honor.
- **Inverse:** None
- **Multiplicity:** One-to-many

---

## GOVERNS_SCOPE_OF
- **Direction:** Source (Environment) → GOVERNS_SCOPE_OF → Target (Database/Storage)
- **Meaning:** The Environment determines which Database and Storage instances are in scope — preventing production data from being accessed in non-production contexts.
- **Inverse:** None
- **Multiplicity:** One-to-many

---

## GRANTED_BY
- **Direction:** Source (Approval Type) → GRANTED_BY → Target (Executive Role)
- **Meaning:** The authority to issue a specific class of approval belongs exclusively to the target Executive Role.
- **Inverse:** None
- **Multiplicity:** One-to-one (each Approval Type has one granting authority)

---

## HOSTED_ON / HOSTS
- **Direction:** Source (Framework/Repository/Database/Storage/Runtime/PM2 Process) → HOSTED_ON → Target (Infrastructure); Source (Infrastructure) → HOSTS → Target (Environment); Source (Environment) → HOSTS → Target (Service/Agent)
- **Meaning:** The source asset runs on or is physically located within the target hosting asset.
- **Inverse:** HOSTED_ON ↔ HOSTS
- **Multiplicity:** Many-to-one (many services hosted on one Infrastructure)

---

## IMPLEMENTS / IMPLEMENTED_BY
- **Direction:** Source (Playbook/Router/Memory Store/Library) → IMPLEMENTS → Target (Policy/Standard/Knowledge Base); Source (Policy) → IMPLEMENTED_BY → Target (Playbook); Source (Approval Type) → IMPLEMENTED_BY → Target (Service)
- **Meaning:** The source artifact is the operational expression of the target abstract specification.
- **Inverse:** IMPLEMENTS ↔ IMPLEMENTED_BY
- **Multiplicity:** Many-to-many (one Playbook may implement multiple Policies; one Policy may be implemented by multiple Playbooks)

---

## IMPORTED_BY / IMPORTS
- **Direction:** Source (Library) → IMPORTED_BY → Target (Service/Agent/Automation); Source (Package) → IMPORTS → Target (Library)
- **Meaning:** The source module's code is included and used by the target asset at runtime.
- **Inverse:** IMPORTED_BY ↔ IMPORTS
- **Multiplicity:** Many-to-many

---

## INDEXED_BY
- **Direction:** Source (Knowledge Base) → INDEXED_BY → Target (Memory Store)
- **Meaning:** The Memory Store maintains a structured index over the Knowledge Base for rapid agent retrieval.
- **Inverse:** IMPLEMENTS (partial — Memory Store IMPLEMENTS Knowledge Base for long-form synthesis)
- **Multiplicity:** One-to-one

---

## INFORMED_BY / INFORMS
- **Direction:** Source (Operational Status) → INFORMED_BY → Target (Lifecycle State); Source (Business Criticality) → INFORMS → Target (Risk Level assignment)
- **Meaning:** The source classification is derived from or influenced by the target classification.
- **Inverse:** INFORMED_BY ↔ INFORMS
- **Multiplicity:** One-to-one

---

## INSTANTIATES
- **Direction:** Source (Runtime) → INSTANTIATES → Target (Package)
- **Meaning:** The Runtime is the live execution of the static code Package in a specific Environment.
- **Inverse:** None
- **Multiplicity:** Many-to-one (many Runtimes may instantiate the same Package in different Environments)

---

## ISSUED_BY
- **Direction:** Source (Policy) → ISSUED_BY → Target (Council)
- **Meaning:** The Council is the originating authority that created and owns the Policy.
- **Inverse:** None (different from ENFORCES — ISSUES is about authorship; ENFORCES is about compliance)
- **Multiplicity:** Many-to-one

---

## LOGGED_BY / LOGGED_TO
- **Direction:** Source (Migration State/Change Control) → LOGGED_BY → Target (Automation); Source (Automation) → LOGGED_TO → Target (Storage)
- **Meaning:** Events from the source are recorded by the target Automation, or the Automation writes its output to the target Storage.
- **Inverse:** None
- **Multiplicity:** One-to-one or One-to-many

---

## MANAGED_BY / MANAGES
- **Direction:** Source (Runtime/Service/Storage) → MANAGED_BY → Target (PM2 Process/Automation); Source (PM2 Process) → MANAGES → Target (Service)
- **Meaning:** The source asset's operational lifecycle (start/stop/restart/cleanup) is controlled by the target manager.
- **Inverse:** MANAGED_BY ↔ MANAGES
- **Multiplicity:** One-to-one (each Service is managed by exactly one PM2 Process)

---

## MEASURED_BY / MEASURES
- **Direction:** Source (Portfolio/Program/Venture/Project) → MEASURED_BY → Target (Executive KPI); Source (Executive KPI) → MEASURES → Target (Portfolio/Program/Venture)
- **Meaning:** The source asset's performance is quantified by the target KPI.
- **Inverse:** MEASURED_BY ↔ MEASURES
- **Multiplicity:** One-to-many (one Portfolio may be measured by many KPIs)

---

## MEMBER_OF
- **Direction:** Source (Agent/Execution Role) → MEMBER_OF → Target (Agent Team)
- **Meaning:** The source agent or role is a formal participant in the target Agent Team.
- **Inverse:** CONTAINS (Agent Team CONTAINS Agent)
- **Multiplicity:** Many-to-one (many Agents are members of one Team)

---

## MONITORED_BY / MONITORS
- **Direction:** Source (Model Provider/PM2 Process) → MONITORED_BY → Target (Service/Dashboard); Source (Dashboard) → MONITORS → Target (Service/Agent)
- **Meaning:** The source asset's health and status are observed and tracked by the target monitoring asset.
- **Inverse:** MONITORED_BY ↔ MONITORS
- **Multiplicity:** One-to-many (one Dashboard monitors many Services)

---

## ORCHESTRATED_BY / ORCHESTRATES
- **Direction:** Source (Agent Team) → ORCHESTRATED_BY → Target (Agent/lead agent); Source (Workflow) → ORCHESTRATES → Target (Automation/Agent)
- **Meaning:** The source multi-asset group operates under the direction of the target lead agent or Workflow.
- **Inverse:** ORCHESTRATED_BY ↔ ORCHESTRATES
- **Multiplicity:** Many-to-one (Agent Team directed by one lead Agent)

---

## OWNED_BY / OWNS
- **Direction:** Source (Repository/Integration) → OWNED_BY → Target (Ownership Role); Source (Ownership Role) → OWNS → Target (Repository/Service/Agent/Workflow/Database/Knowledge Base); Source (Executive Role) → OWNS → Target (Portfolio/Venture)
- **Meaning:** The target Role is the accountable steward of the source asset.
- **Inverse:** OWNED_BY ↔ OWNS
- **Multiplicity:** Many-to-one (each asset has exactly one owner; one Owner may own many assets)

---

## PART_OF
- **Direction:** Source (Automation) → PART_OF → Target (Workflow)
- **Meaning:** The Automation is a constituent step within the broader Workflow.
- **Inverse:** ORCHESTRATES (partial)
- **Multiplicity:** Many-to-one

---

## PRODUCES
- **Direction:** Source (Portfolio/Venture/Project/Workflow/Agent/Agent Team) → PRODUCES → Target (Business Outcome/Repository/Service/Agent)
- **Meaning:** The source asset's execution results in the creation of the target asset or the achievement of the target outcome.
- **Inverse:** None
- **Multiplicity:** One-to-many

---

## PROGRESSES_FROM / PROGRESSES_TOWARD
- **Direction:** Source (Migration State) → PROGRESSES_FROM → Target (Current State); Source (Migration State) → PROGRESSES_TOWARD → Target (Target State)
- **Meaning:** The Migration State tracks the live transition from the actual Current State to the intended Target State.
- **Inverse:** PROGRESSES_TOWARD ↔ ACHIEVED_BY
- **Multiplicity:** One-to-one

---

## PROVIDED_BY / PROVIDES / PROVIDES_STRUCTURE_FOR
- **Direction:** Source (Model) → PROVIDED_BY → Target (Model Provider); Source (Infrastructure) → PROVIDES → Target (Database/Storage); Source (Framework) → PROVIDES_STRUCTURE_FOR → Target (Service/Agent)
- **Meaning:** The source asset exists within or is supplied by the target, or the target Framework defines the structural conventions the source must follow.
- **Inverse:** PROVIDED_BY ↔ HOSTS (partial); PROVIDES ↔ HOSTED_ON (partial)
- **Multiplicity:** Many-to-one (many Models from one Provider; many Services structured by one Framework)

---

## PUBLISHED_TO
- **Direction:** Source (Package) → PUBLISHED_TO → Target (Registry)
- **Meaning:** The Package's distributable artifact is registered in the target Registry for discovery and consumption.
- **Inverse:** CATALOGS (partial)
- **Multiplicity:** One-to-one

---

## QUERIED_BY
- **Direction:** Source (Registry) → QUERIED_BY → Target (Dashboard/Agent)
- **Meaning:** The Registry is read by the target Dashboard or Agent to surface asset information.
- **Inverse:** None
- **Multiplicity:** One-to-many

---

## READ_BY
- **Direction:** Source (Storage) → READ_BY → Target (Service)
- **Meaning:** The Service reads data from the Storage.
- **Inverse:** None (different from ACCESSED_BY — READ_BY is read-only; ACCESSED_BY includes writes)
- **Multiplicity:** One-to-many

---

## REFERENCED_BY
- **Direction:** Source (Business Outcome) → REFERENCED_BY → Target (Council); Source (Verification Method) → REFERENCED_BY → Target (Standard)
- **Meaning:** The source artifact is cited or included by the target governance body or document.
- **Inverse:** None
- **Multiplicity:** One-to-many

---

## REPLACES
- **Direction:** Source (Supersession record) → REPLACES (predecessor) → REPLACED_BY (successor)
- **Meaning:** The Supersession record formalizes that one asset has taken over the responsibilities of another.
- **Inverse:** SUPERSEDED_BY
- **Multiplicity:** One-to-one per Supersession event (but a successor may replace multiple predecessors)

---

## REPORTS / REPORTS_TO
- **Direction:** Source (Runtime) → REPORTS → Target (Operational Status); Source (Ownership Role) → REPORTS_TO → Target (Executive Role); Source (Execution Role) → REPORTS_TO → Target (Ownership Role); Source (Agent) → REPORTS_TO → Target (Execution Role)
- **Meaning:** The source emits status information to the target (REPORTS), or the source Role is accountable to the target Role (REPORTS_TO).
- **Inverse:** None
- **Multiplicity:** One-to-one

---

## REQUIRED_BY / REQUIRES
- **Direction:** Source (Business Capability) → REQUIRED_BY → Target (Program); Source (Program) → REQUIRES → Target (Business Capability); Source (Approval Type) → REQUIRED_BY → Target (Policy); Source (Change Control) → REQUIRED_BY → Target (Standard)
- **Meaning:** The source cannot fulfill its purpose without the target.
- **Inverse:** REQUIRED_BY ↔ REQUIRES
- **Multiplicity:** Many-to-many

---

## ROTATED_BY
- **Direction:** Source (Secret Metadata) → ROTATED_BY → Target (Playbook)
- **Meaning:** The credential described by the Secret Metadata record is renewed and replaced according to the target Playbook's procedure.
- **Inverse:** None
- **Multiplicity:** One-to-one

---

## ROUTED_BY / ROUTES_TO
- **Direction:** Source (Model) → ROUTED_BY → Target (Router); Source (Router) → ROUTES_TO → Target (Model/Service/Agent)
- **Meaning:** The Router determines which Model, Service, or Agent receives a given request or signal.
- **Inverse:** ROUTED_BY ↔ ROUTES_TO
- **Multiplicity:** One Router → many targets (fallback chain)

---

## RUNS_IN / RUNS_ON
- **Direction:** Source (Runtime) → RUNS_IN → Target (Environment); Source (PM2 Process) → RUNS_ON → Target (Infrastructure)
- **Meaning:** The source Runtime operates within the scoped target Environment; the PM2 Process runs on the physical Infrastructure.
- **Inverse:** HOSTS (partial)
- **Multiplicity:** Many-to-one

---

## SERVED_BY
- **Direction:** Source (Dashboard) → SERVED_BY → Target (Service)
- **Meaning:** The Dashboard's content is provided by the backing Service.
- **Inverse:** EXPOSES (partial)
- **Multiplicity:** One-to-one

---

## STORED_IN
- **Direction:** Source (Secret Metadata/Knowledge Base) → STORED_IN → Target (`~/.openclaw/secrets/.env`/Storage)
- **Meaning:** The source asset's physical data resides in the target file or Storage path.
- **Inverse:** None
- **Multiplicity:** One-to-one

---

## SUPERSEDED_BY
- **Direction:** Source (Retirement State/asset) → SUPERSEDED_BY → Target (active asset)
- **Meaning:** The source asset has been formally replaced by the target. The Supersession record is permanent.
- **Inverse:** REPLACES
- **Multiplicity:** One-to-one per supersession event

---

## TRANSITIONS
- **Direction:** Source (Lifecycle State) → TRANSITIONS → Target (governed by Policy and Approval Type)
- **Meaning:** State changes between lifecycle states are governed events, not silent updates. Every transition is logged with actor and timestamp.
- **Inverse:** None (meta-relationship — applies to all asset types)
- **Multiplicity:** N/A — meta-relationship

---

## TRIGGERED_BY / TRIGGERS
- **Direction:** Source (Workflow) → TRIGGERED_BY → Target (Event); Source (Operational Status degradation) → TRIGGERS → Target (Alert); Source (Drift Detection) → TRIGGERS → Target (Change Control); Source (Supersession) → TRIGGERS → Target (Retirement State)
- **Meaning:** The source event or condition causes the target process to initiate.
- **Inverse:** TRIGGERED_BY ↔ TRIGGERS
- **Multiplicity:** One-to-many

---

## USED_BY / USES
- **Direction:** Source (Package/Model/API/Integration) → USED_BY → Target (Service/Agent/Automation/Playbook); Source (Agent/Service/Playbook/Automation/Environment) → USES → Target (Model/API/Integration/Database/Service/Secret Metadata)
- **Meaning:** The source asset is actively consumed as a dependency by the target, or the target asset actively consumes the source.
- **Inverse:** USED_BY ↔ USES
- **Multiplicity:** Many-to-many

---

## VALIDATED_BY / VALIDATES
- **Direction:** Source (Business Outcome/Standard/Playbook/Integration Readiness/Evidence State/Schema Evolution) → VALIDATED_BY → Target (Executive KPI/Verification Method); Source (Verification Method) → VALIDATES → Target (Integration Readiness/Operational Status/Evidence State)
- **Meaning:** The source claim or artifact is confirmed by the target measurement or method.
- **Inverse:** VALIDATED_BY ↔ VALIDATES
- **Multiplicity:** One-to-many (one Business Outcome validated by many KPIs)

---

## VERIFIED_BY
- **Direction:** Source (Evidence State) → VERIFIED_BY → Target (Verification Method)
- **Meaning:** The evidence classification is supported by the output of a named Verification Method.
- **Inverse:** None
- **Multiplicity:** One-to-one

---

## VISUALIZED_BY
- **Direction:** Source (Lifecycle State) → VISUALIZED_BY → Target (Dashboard)
- **Meaning:** The state of assets is rendered in the Dashboard for human situational awareness.
- **Inverse:** None
- **Multiplicity:** One-to-many

---

## WRITTEN_BY
- **Direction:** Source (Storage/Registry) → WRITTEN_BY → Target (Service/Agent/Automation)
- **Meaning:** The source Storage or Registry receives writes from the target actor.
- **Inverse:** None (directional — write access is a specific permission)
- **Multiplicity:** One-to-many

---

# SECTION 2 — ASSET TYPE RELATIONSHIP MATRIX

Complete table of all valid directed relationships extracted from the Taxonomy's `Allowed Relationships` fields. Every row represents one valid edge in the Open Empire asset graph.

| # | Source Asset Type | Relationship | Target Asset Type | Multiplicity |
|---|---|---|---|---|
| 1 | Portfolio | CONTAINS | Program | 1:N |
| 2 | Portfolio | CONTAINS | Venture | 1:N |
| 3 | Portfolio | MEASURED_BY | Executive KPI | 1:N |
| 4 | Portfolio | PRODUCES | Business Outcome | 1:N |
| 5 | Portfolio | GOVERNED_BY | Council | N:1 |
| 6 | Program | BELONGS_TO | Portfolio | N:1 |
| 7 | Program | CONTAINS | Project | 1:N |
| 8 | Program | REQUIRES | Business Capability | N:M |
| 9 | Program | MEASURED_BY | Executive KPI | 1:N |
| 10 | Program | DELIVERS | Business Outcome | N:M |
| 11 | Program | GOVERNED_BY | Council | N:1 |
| 12 | Project | BELONGS_TO | Program | N:1 |
| 13 | Project | PRODUCES | Repository | 1:N |
| 14 | Project | PRODUCES | Service | 1:N |
| 15 | Project | PRODUCES | Agent | 1:N |
| 16 | Project | GOVERNED_BY | Policy | N:M |
| 17 | Project | MEASURED_BY | Executive KPI | 1:N |
| 18 | Project | CARRIES | Risk Level | N:1 |
| 19 | Business Capability | REQUIRED_BY | Program | N:M |
| 20 | Business Capability | ENABLED_BY | Service | N:M |
| 21 | Business Capability | ENABLED_BY | Agent | N:M |
| 22 | Business Capability | ENABLED_BY | Integration | N:M |
| 23 | Business Capability | GOVERNED_BY | Policy | N:M |
| 24 | Venture | BELONGS_TO | Portfolio | N:1 |
| 25 | Venture | CONTAINS | Program | 1:N |
| 26 | Venture | MEASURED_BY | Executive KPI | 1:N |
| 27 | Venture | PRODUCES | Business Outcome | 1:N |
| 28 | Venture | GOVERNED_BY | Council | N:1 |
| 29 | Venture | CARRIES | Risk Level | N:1 |
| 30 | Executive KPI | MEASURES | Portfolio | N:M |
| 31 | Executive KPI | MEASURES | Program | N:M |
| 32 | Executive KPI | MEASURES | Venture | N:M |
| 33 | Executive KPI | DISPLAYED_BY | Dashboard | N:M |
| 34 | Executive KPI | EVALUATED_BY | Council | N:1 |
| 35 | Executive KPI | CARRIES | Evidence State | N:1 |
| 36 | Business Outcome | DELIVERED_BY | Program | N:M |
| 37 | Business Outcome | DELIVERED_BY | Venture | N:M |
| 38 | Business Outcome | VALIDATED_BY | Executive KPI | N:M |
| 39 | Business Outcome | REFERENCED_BY | Council | N:M |
| 40 | Council | GOVERNS | Portfolio | 1:N |
| 41 | Council | GOVERNS | Program | 1:N |
| 42 | Council | GOVERNS | Venture | 1:N |
| 43 | Council | ASSIGNS | Executive Role | 1:N |
| 44 | Council | ENFORCES | Policy | 1:N |
| 45 | Council | ESCALATES_TO | Council | N:1 |
| 46 | Council | REVIEWS | Business Outcome | N:M |
| 47 | Executive Role | ASSIGNED_TO | Council | N:1 |
| 48 | Executive Role | OWNS | Portfolio | 1:N |
| 49 | Executive Role | OWNS | Venture | 1:N |
| 50 | Executive Role | GOVERNS | Policy | 1:N |
| 51 | Executive Role | ESCALATES_TO | Executive Role | N:1 |
| 52 | Executive Role | CHAIRS | Council | 1:1 |
| 53 | Ownership Role | REPORTS_TO | Executive Role | N:1 |
| 54 | Ownership Role | OWNS | Repository | 1:N |
| 55 | Ownership Role | OWNS | Service | 1:N |
| 56 | Ownership Role | OWNS | Agent | 1:N |
| 57 | Ownership Role | OWNS | Workflow | 1:N |
| 58 | Ownership Role | OWNS | Database | 1:N |
| 59 | Ownership Role | OWNS | Knowledge Base | 1:N |
| 60 | Standard | ENFORCED_BY | Council | N:1 |
| 61 | Standard | APPLIED_TO | Repository | 1:N |
| 62 | Standard | APPLIED_TO | API | 1:N |
| 63 | Standard | APPLIED_TO | Database | 1:N |
| 64 | Standard | VALIDATED_BY | Verification Method | 1:N |
| 65 | Policy | ISSUED_BY | Council | N:1 |
| 66 | Policy | IMPLEMENTED_BY | Playbook | 1:N |
| 67 | Policy | APPLIES_TO | Agent | 1:N |
| 68 | Policy | APPLIES_TO | Service | 1:N |
| 69 | Policy | APPLIES_TO | Automation | 1:N |
| 70 | Policy | ENFORCED_BY | Execution Role | 1:N |
| 71 | Playbook | IMPLEMENTS | Policy | N:M |
| 72 | Playbook | EXECUTED_BY | Agent | N:M |
| 73 | Playbook | EXECUTED_BY | Execution Role | N:M |
| 74 | Playbook | USES | API | N:M |
| 75 | Playbook | USES | Service | N:M |
| 76 | Playbook | VALIDATED_BY | Verification Method | N:M |
| 77 | Approval Type | REQUIRED_BY | Policy | N:M |
| 78 | Approval Type | GRANTED_BY | Executive Role | N:1 |
| 79 | Approval Type | IMPLEMENTED_BY | Service | 1:1 |
| 80 | Approval Type | APPLIES_TO | Agent | 1:N |
| 81 | Approval Type | APPLIES_TO | Automation | 1:N |
| 82 | Risk Level | APPLIED_TO | Project | 1:N |
| 83 | Risk Level | APPLIED_TO | Agent | 1:N |
| 84 | Risk Level | APPLIED_TO | Service | 1:N |
| 85 | Risk Level | APPLIED_TO | Automation | 1:N |
| 86 | Risk Level | DETERMINES | Approval Type | N:1 |
| 87 | Risk Level | DETERMINES | Recovery Priority | N:1 |
| 88 | Lifecycle State | APPLIED_TO | (all asset types) | 1:N |
| 89 | Lifecycle State | VISUALIZED_BY | Dashboard | 1:N |
| 90 | Evidence State | APPLIED_TO | Executive KPI | 1:N |
| 91 | Evidence State | APPLIED_TO | Business Outcome | 1:N |
| 92 | Evidence State | APPLIED_TO | Operational Status | 1:N |
| 93 | Evidence State | VERIFIED_BY | Verification Method | N:1 |
| 94 | Repository | CONTAINS | Package | 1:N |
| 95 | Repository | CONTAINS | Library | 1:N |
| 96 | Repository | DEPLOYS_TO | Service | 1:N |
| 97 | Repository | OWNED_BY | Ownership Role | N:1 |
| 98 | Repository | GOVERNED_BY | Standard | N:M |
| 99 | Repository | HOSTED_ON | Infrastructure | N:1 |
| 100 | Package | CONTAINED_IN | Repository | N:1 |
| 101 | Package | IMPORTS | Library | N:M |
| 102 | Package | USED_BY | Service | N:M |
| 103 | Package | USED_BY | Agent | N:M |
| 104 | Package | PUBLISHED_TO | Registry | N:1 |
| 105 | Library | CONTAINED_IN | Package | N:1 |
| 106 | Library | IMPORTED_BY | Service | N:M |
| 107 | Library | IMPORTED_BY | Agent | N:M |
| 108 | Library | IMPORTED_BY | Automation | N:M |
| 109 | Library | IMPLEMENTS | Standard | N:M |
| 110 | Framework | PROVIDES_STRUCTURE_FOR | Service | 1:N |
| 111 | Framework | PROVIDES_STRUCTURE_FOR | Agent | 1:N |
| 112 | Framework | DEFINED_BY | Standard | N:1 |
| 113 | Framework | HOSTED_ON | Infrastructure | N:1 |
| 114 | Model | PROVIDED_BY | Model Provider | N:1 |
| 115 | Model | USED_BY | Agent | N:M |
| 116 | Model | USED_BY | Service | N:M |
| 117 | Model | GOVERNED_BY | Policy | N:M |
| 118 | Model | ROUTED_BY | Router | N:1 |
| 119 | Model Provider | HOSTS | Model | 1:N |
| 120 | Model Provider | AUTHENTICATED_VIA | Secret Metadata | N:1 |
| 121 | Model Provider | BILLED_TO | Venture | N:1 |
| 122 | Model Provider | MONITORED_BY | Service | N:1 |
| 123 | API | EXPOSED_BY | Service | N:1 |
| 124 | API | CONSUMED_BY | Integration | N:M |
| 125 | API | CONSUMED_BY | Agent | N:M |
| 126 | API | GOVERNS_CONTRACT_FOR | Integration | 1:N |
| 127 | API | DOCUMENTED_BY | Standard | N:M |
| 128 | Router | ROUTES_TO | Model | 1:N |
| 129 | Router | ROUTES_TO | Service | 1:N |
| 130 | Router | ROUTES_TO | Agent | 1:N |
| 131 | Router | IMPLEMENTS | Policy | N:M |
| 132 | Router | CONSUMES | API | N:M |
| 133 | Integration | CONSUMES | API | N:1 |
| 134 | Integration | OWNED_BY | Service | N:1 |
| 135 | Integration | AUTHENTICATED_VIA | Secret Metadata | N:1 |
| 136 | Integration | GOVERNED_BY | Policy | N:M |
| 137 | Integration | PRODUCES | (data_for) Service | N:1 |
| 138 | Environment | HOSTS | Service | 1:N |
| 139 | Environment | HOSTS | Agent | 1:N |
| 140 | Environment | USES | Secret Metadata | N:M |
| 141 | Environment | GOVERNS_SCOPE_OF | Database | 1:N |
| 142 | Environment | GOVERNS_SCOPE_OF | Storage | 1:N |
| 143 | Infrastructure | HOSTS | Environment | 1:N |
| 144 | Infrastructure | PROVIDES | Database | 1:N |
| 145 | Infrastructure | PROVIDES | Storage | 1:N |
| 146 | Infrastructure | GOVERNED_BY | Policy | N:M |
| 147 | Database | HOSTED_ON | Infrastructure | N:1 |
| 148 | Database | ACCESSED_BY | Service | N:M |
| 149 | Database | ACCESSED_BY | Agent | N:M |
| 150 | Database | GOVERNED_BY | Standard | N:M |
| 151 | Database | BACKED_UP_BY | Automation | N:1 |
| 152 | Storage | HOSTED_ON | Infrastructure | N:1 |
| 153 | Storage | WRITTEN_BY | Service | N:M |
| 154 | Storage | WRITTEN_BY | Agent | N:M |
| 155 | Storage | READ_BY | Service | N:M |
| 156 | Storage | MANAGED_BY | Automation | N:1 |
| 157 | Secret Metadata | DESCRIBES | Integration | 1:N |
| 158 | Secret Metadata | DESCRIBES | Service | 1:N |
| 159 | Secret Metadata | DESCRIBES | Agent | 1:N |
| 160 | Secret Metadata | STORED_IN | (canonical .env file) | 1:1 |
| 161 | Secret Metadata | GOVERNED_BY | Policy | N:1 |
| 162 | Secret Metadata | ROTATED_BY | Playbook | N:1 |
| 163 | Runtime | INSTANTIATES | Package | N:1 |
| 164 | Runtime | MANAGED_BY | PM2 Process | N:1 |
| 165 | Runtime | RUNS_IN | Environment | N:1 |
| 166 | Runtime | REPORTS | Operational Status | 1:1 |
| 167 | Service | MANAGED_BY | PM2 Process | 1:1 |
| 168 | Service | EXPOSES | API | 1:N |
| 169 | Service | CONSUMES | Integration | 1:N |
| 170 | Service | USES | Database | N:M |
| 171 | Service | USES | Model | N:M |
| 172 | Service | OWNED_BY | Ownership Role | N:1 |
| 173 | Service | GOVERNED_BY | Policy | N:M |
| 174 | PM2 Process | MANAGES | Service | 1:1 |
| 175 | PM2 Process | DEFINED_IN | (ecosystem config .cjs) | N:1 |
| 176 | PM2 Process | RUNS_ON | Infrastructure | N:1 |
| 177 | PM2 Process | MONITORED_BY | Dashboard | N:M |
| 178 | Workflow | ORCHESTRATES | Automation | 1:N |
| 179 | Workflow | ORCHESTRATES | Agent | N:M |
| 180 | Workflow | TRIGGERED_BY | (Event) | N:M |
| 181 | Workflow | GOVERNED_BY | Playbook | N:M |
| 182 | Workflow | PRODUCES | Business Outcome | N:M |
| 183 | Automation | PART_OF | Workflow | N:1 |
| 184 | Automation | EXECUTED_BY | Service | N:M |
| 185 | Automation | USES | API | N:M |
| 186 | Automation | USES | Integration | N:M |
| 187 | Automation | GOVERNED_BY | Policy | N:M |
| 188 | Automation | LOGGED_TO | Storage | N:1 |
| 189 | Agent | MEMBER_OF | Agent Team | N:M |
| 190 | Agent | USES | Model | N:M |
| 191 | Agent | USES | API | N:M |
| 192 | Agent | USES | Service | N:M |
| 193 | Agent | GOVERNED_BY | Policy | N:M |
| 194 | Agent | EXECUTES | Playbook | N:M |
| 195 | Agent | REPORTS_TO | Execution Role | N:1 |
| 196 | Agent | PRODUCES | Business Outcome | N:M |
| 197 | Agent Team | CONTAINS | Agent | 1:N |
| 198 | Agent Team | GOVERNED_BY | Council | N:1 |
| 199 | Agent Team | ORCHESTRATED_BY | Agent | N:1 |
| 200 | Agent Team | PRODUCES | Business Outcome | N:M |
| 201 | Dashboard | DISPLAYS | Operational Status | 1:N |
| 202 | Dashboard | DISPLAYS | Executive KPI | 1:N |
| 203 | Dashboard | MONITORS | Service | 1:N |
| 204 | Dashboard | MONITORS | Agent | 1:N |
| 205 | Dashboard | SERVED_BY | Service | N:1 |
| 206 | Knowledge Base | CONSUMED_BY | Agent | N:M |
| 207 | Knowledge Base | CONSUMED_BY | Playbook | N:M |
| 208 | Knowledge Base | CURATED_BY | Ownership Role | N:1 |
| 209 | Knowledge Base | STORED_IN | Storage | N:1 |
| 210 | Knowledge Base | INDEXED_BY | Memory Store | N:1 |
| 211 | Memory Store | ACCESSED_BY | Agent | N:M |
| 212 | Memory Store | MANAGED_BY | Automation | N:1 |
| 213 | Memory Store | BACKED_UP_TO | Storage | N:1 |
| 214 | Memory Store | IMPLEMENTS | Knowledge Base | N:1 |
| 215 | Registry | CATALOGS | (all asset types) | 1:N |
| 216 | Registry | GOVERNED_BY | Council | N:1 |
| 217 | Registry | QUERIED_BY | Dashboard | N:M |
| 218 | Registry | QUERIED_BY | Agent | N:M |
| 219 | Registry | WRITTEN_BY | Automation | N:M |
| 220 | Execution Role | REPORTS_TO | Ownership Role | N:1 |
| 221 | Execution Role | EXECUTES | Automation | N:M |
| 222 | Execution Role | EXECUTES | Playbook | N:M |
| 223 | Execution Role | EXECUTES | (Agent Task) | N:M |
| 224 | Execution Role | MEMBER_OF | Agent Team | N:M |
| 225 | Operational Status | APPLIED_TO | Service | 1:N |
| 226 | Operational Status | APPLIED_TO | Agent | 1:N |
| 227 | Operational Status | APPLIED_TO | Automation | 1:N |
| 228 | Operational Status | DISPLAYED_BY | Dashboard | 1:N |
| 229 | Operational Status | TRIGGERS | (Alert) | 1:1 |
| 230 | Operational Status | INFORMED_BY | Lifecycle State | N:1 |
| 231 | Integration Readiness | ASSESSED_FOR | Integration | 1:1 |
| 232 | Integration Readiness | GATES | (Lifecycle State transition) | 1:1 |
| 233 | Integration Readiness | VERIFIED_BY | Verification Method | N:M |
| 234 | Business Criticality | APPLIED_TO | (any asset) | 1:N |
| 235 | Business Criticality | DETERMINES | Recovery Priority | N:1 |
| 236 | Business Criticality | DETERMINES | (Approval Type requirements) | N:1 |
| 237 | Business Criticality | INFORMS | Risk Level | N:1 |
| 238 | Recovery Priority | APPLIED_TO | Service | 1:N |
| 239 | Recovery Priority | APPLIED_TO | Database | 1:N |
| 240 | Recovery Priority | APPLIED_TO | Integration | 1:N |
| 241 | Recovery Priority | INFORMED_BY | Business Criticality | N:1 |
| 242 | Recovery Priority | INFORMED_BY | Risk Level | N:1 |
| 243 | Recovery Priority | DEFINED_BY | Playbook | N:1 |
| 244 | Verification Method | VALIDATES | Integration Readiness | 1:N |
| 245 | Verification Method | VALIDATES | Operational Status | 1:N |
| 246 | Verification Method | VALIDATES | Evidence State | 1:N |
| 247 | Verification Method | EXECUTED_BY | Automation | N:M |
| 248 | Verification Method | REFERENCED_BY | Standard | N:M |
| 249 | Current State | CONTRASTED_WITH | Target State | 1:1 |
| 250 | Current State | EVIDENCE_PROVIDED_BY | Evidence State | 1:1 |
| 251 | Current State | CAPTURED_BY | Automation | N:1 |
| 252 | Current State | REVIEWED_BY | Council | N:M |
| 253 | Target State | CONTRASTED_WITH | Current State | 1:1 |
| 254 | Target State | ACHIEVED_BY | Migration State | 1:1 |
| 255 | Target State | APPROVED_BY | Council | N:1 |
| 256 | Target State | GOVERNS | Change Control | 1:N |
| 257 | Migration State | PROGRESSES_FROM | Current State | N:1 |
| 258 | Migration State | PROGRESSES_TOWARD | Target State | N:1 |
| 259 | Migration State | GOVERNED_BY | Change Control | N:1 |
| 260 | Migration State | LOGGED_BY | Automation | N:1 |
| 261 | Migration State | REVIEWED_BY | Council | N:M |
| 262 | Retirement State | SUPERSEDED_BY | (active asset) | 1:1 |
| 263 | Retirement State | ARCHIVED_IN | Storage | N:1 |
| 264 | Retirement State | APPROVED_BY | Approval Type | N:1 |
| 265 | Retirement State | DOCUMENTED_BY | Registry | N:1 |
| 266 | Supersession | REPLACES | (predecessor → successor) | 1:1 |
| 267 | Supersession | DOCUMENTED_BY | Registry | N:1 |
| 268 | Supersession | APPROVED_BY | Approval Type | N:1 |
| 269 | Supersession | TRIGGERS | Retirement State | 1:1 |
| 270 | Versioning | APPLIED_TO | Repository | 1:N |
| 271 | Versioning | APPLIED_TO | Package | 1:N |
| 272 | Versioning | APPLIED_TO | API | 1:N |
| 273 | Versioning | APPLIED_TO | Standard | 1:N |
| 274 | Versioning | APPLIED_TO | Policy | 1:N |
| 275 | Versioning | GOVERNS | Change Control | 1:N |
| 276 | Change Control | GOVERNS | Migration State | 1:N |
| 277 | Change Control | GOVERNS | Versioning | 1:N |
| 278 | Change Control | REQUIRED_BY | Standard | N:M |
| 279 | Change Control | APPROVED_BY | Council | N:1 |
| 280 | Change Control | LOGGED_BY | Registry | N:1 |
| 281 | Drift Detection | COMPARES | Registry vs Current State | 1:N |
| 282 | Drift Detection | ALERTS_TO | Dashboard | N:1 |
| 283 | Drift Detection | TRIGGERS | Change Control | N:1 |
| 284 | Drift Detection | GOVERNED_BY | Policy | N:1 |
| 285 | Schema Evolution | APPLIED_TO | Database | N:M |
| 286 | Schema Evolution | APPLIED_TO | API | N:M |
| 287 | Schema Evolution | APPLIED_TO | Registry | N:M |
| 288 | Schema Evolution | GOVERNS | Versioning | N:1 |
| 289 | Schema Evolution | REQUIRES | Change Control | N:1 |
| 290 | Schema Evolution | VALIDATED_BY | Verification Method | N:M |

---

# SECTION 3 — RELATIONSHIP CONSTRAINTS

## 3.1 Mandatory Relationships (Asset is Invalid Without These)

| Asset Type | Mandatory Relationship | Constraint |
|---|---|---|
| Portfolio | GOVERNED_BY Council | Must have at least one governing Council |
| Portfolio | CONTAINS Program or Venture | Must have at least one Program or Venture |
| Program | BELONGS_TO Portfolio | Exactly one Portfolio; no orphan Programs |
| Program | CONTAINS Project | Must have at least one Project |
| Project | BELONGS_TO Program | Exactly one Program parent |
| Project | CARRIES Risk Level | Risk level is never blank |
| Venture | BELONGS_TO Portfolio | Exactly one Portfolio parent |
| Venture | CARRIES Risk Level | Risk level is never blank |
| Executive KPI | CARRIES Evidence State | Every KPI must have an evidence_state |
| Business Outcome | VALIDATED_BY Executive KPI | Must be linked to at least one KPI |
| Council | ASSIGNS Executive Role (Chair) | Must have a chair role |
| Executive Role | ASSIGNED_TO Council | Must belong to a Council (exception: Nathan/Sovereign Operator) |
| Standard | VALIDATED_BY Verification Method | Active Standards must list at least one verification method |
| Policy | ISSUED_BY Council | Must have a council authority |
| Playbook | IMPLEMENTS Policy | Must implement at least one Policy |
| Approval Type | GRANTED_BY Executive Role | Must have a defined granting authority |
| Repository | OWNED_BY Ownership Role | Every Repository must have an owner |
| Package | CONTAINED_IN Repository | Must reside in exactly one Repository |
| Integration | AUTHENTICATED_VIA Secret Metadata | Must reference a Secret Metadata record — no inline credentials |
| Integration | CONSUMES API | Must reference the API it connects to |
| Secret Metadata | GOVERNED_BY Policy | Must be governed by Secret Management Policy |
| Runtime | MANAGED_BY PM2 Process | All production Runtimes managed by PM2 |
| Service | MANAGED_BY PM2 Process | Must have a PM2 id |
| Service | OWNED_BY Ownership Role | Every Service must have an owner |
| Agent | GOVERNED_BY Policy | Must have at least one governing policy |
| Agent Team | ORCHESTRATED_BY Agent | Must have a lead agent |
| Migration State | GOVERNED_BY Change Control | No migration without an approved Change Control |
| Change Control | APPROVED_BY Council | Must have an approver before In Progress |
| Retirement State | APPROVED_BY Approval Type | Retirement always requires explicit approval |
| Supersession | DOCUMENTED_BY Registry | Supersession records are permanent and never deleted |

## 3.2 Mutually Exclusive Relationships

| Constraint | Description |
|---|---|
| Secret value ≠ ANY relationship target | Secret Metadata describes secrets but NEVER contains their values. Credentials may only reside in `~/.openclaw/secrets/.env`. |
| Staging Environment ≠ GOVERNS_SCOPE_OF production Database | Staging environments must never access production secrets or databases. Absolute rule. |
| Nathan ESCALATES_TO = None | The Sovereign Operator has no escalation path. No relationship of type ESCALATES_TO may have Nathan as a source. |
| Retired asset ≠ GOVERNED_BY or BELONGS_TO active governance | A retired/archived asset is excluded from all active governance relationships. |
| Agent USES Model (non-Haiku/Ollama in real-time chain) | No Agent in the real-time signal scoring chain may USE a Model other than those in the approved chain (Haiku → Ollama → Heuristic) without explicit Nathan directive. |

## 3.3 Relationships Governed by Lifecycle State Changes

| Lifecycle Transition | Relationship Impact |
|---|---|
| Project: In Progress → Complete | PRODUCES relationships are transferred to operational asset ownership; Project OWNS relationship for outputs ceases |
| Service: Staging → Active | REQUIRES Integration Readiness GATES this transition — must be Validated |
| Venture: Pre-Launch → Active | Requires Nathan approval; GOVERNED_BY Council must be active |
| Venture: Active → Scaling | Requires at least one verified revenue event (Business Outcome ACHIEVED or KPI threshold met) |
| Agent: Testing → Active (financial) | Requires Nathan approval; GOVERNED_BY must include spend cap enforcement |
| Framework: Active → Upgrading | PROVIDES_STRUCTURE_FOR relationships trigger impact analysis across all consuming Services/Agents |
| Repository: Active → Deprecated | DEPLOYS_TO relationships must be reassigned or terminated |
| Integration: Active → Broken | CONSUMES API relationship becomes blocked; Circuit breaker activates; P1 alert within 60 seconds |
| API: Active → Breaking-Change-Pending | All CONSUMED_BY relationships must be migrated before transition to Retired |
| Council: Active → Dissolved | GOVERNS relationships must all be reassigned; Dissolution blocked while governing Active assets |
| Retirement State: Planned Retirement → Retiring | SUPERSEDED_BY relationship must be established before retirement begins |

## 3.4 Relationship Strength Tiers

| Strength | Meaning | Example |
|---|---|---|
| **Required** | Asset cannot be valid without this relationship | Project BELONGS_TO Program |
| **Optional** | Asset may exist without this relationship | Service USES Model |
| **Deprecated** | Relationship was valid in a prior Taxonomy version and must be removed within 30 days | Any relationship using retired asset types |

---

# SECTION 4 — ONTOLOGY GRAPH DESCRIPTION

## 4.1 Root Nodes

**Portfolio** is the root of the Business layer. It has no parent asset. All strategic and operational assets ultimately trace back to a Portfolio in the hierarchy.

**Infrastructure** is the physical root of the Engineering layer. It has no parent in the Open Empire architecture.

**Nathan (Sovereign Operator)** is the governance root. No Council, Policy, or Executive Role supersedes Nathan's explicit directive. Nathan's ESCALATES_TO relationship is null — there is no higher authority.

## 4.2 Key Structural Patterns

**The Hierarchy Pattern:**
```
Portfolio
  ├── CONTAINS → Venture
  │     └── CONTAINS → Program
  └── CONTAINS → Program
        └── CONTAINS → Project
              └── PRODUCES → Service / Agent / Repository
```
No asset in the Business layer may exist outside this hierarchy without explicit exception noted in the Registry.

**The Governance Stack:**
```
Nathan (Sovereign Override)
  └── Council
        ├── ASSIGNS → Executive Role
        │     └── (supervises) → Ownership Role
        │                          └── (supervises) → Execution Role
        ├── ENFORCES → Policy
        │     └── IMPLEMENTED_BY → Playbook
        └── GOVERNS → Portfolio / Program / Venture
```

**The Technical Stack:**
```
Infrastructure
  └── HOSTS → Environment
        └── HOSTS → Service / Agent (runtime)
              └── Service: MANAGED_BY → PM2 Process
              └── Service: USES → Database / Model / Integration
              └── Integration: CONSUMES → API
              └── Integration: AUTHENTICATED_VIA → Secret Metadata
```

**The AI Intelligence Stack:**
```
Model Provider
  └── HOSTS → Model
        └── Model: ROUTED_BY → Router
              └── Router: ROUTES_TO → Model (chain: Haiku → Ollama → Heuristic)
        └── Model: USED_BY → Agent
```

**The Governance Closure Pattern:**
Every executable asset (Agent, Service, Automation) is governed by Policy, and every Policy is ISSUED_BY a Council, and every Council is ultimately accountable to Nathan. This creates a closed governance loop.

## 4.3 Critical Structural Constraints

1. **No orphan assets.** Every asset must have at least one BELONGS_TO, CONTAINED_IN, OWNED_BY, or GOVERNED_BY relationship.
2. **No unowned Tier-0 assets.** Every Tier-0 asset must have an OWNED_BY Ownership Role.
3. **No ungoverned financial agents.** Every Agent with financial authority must CARRY a spend_cap and GOVERNED_BY a spend cap Policy.
4. **No credentials in the graph.** Secret values are never relationship targets. Only Secret Metadata records (by ID) appear in the graph.
5. **No unrecorded supersessions.** Every asset replacement triggers a Supersession record and a Retirement State. Undocumented replacements are governance violations.

## 4.4 Anti-Patterns (Invalid Graph States)

| Anti-Pattern | Why It's Invalid |
|---|---|
| Project with no end_date | Violates Project Validation Rules; Projects must be time-boxed |
| Venture without daily_spend_cap_usd if financial | Violates Venture Validation Rules; spend caps are mandatory |
| Integration with inline credentials | Violates Secret Management Policy; must use Secret Metadata |
| Agent using Model not in approved routing chain (real-time) | Violates Model Dispatch Policy and Router governance constraint |
| Tier-0 Repository without git_initialized=true | Active governance violation (D21 pattern) |
| Council dissolved while governing Active assets | Violates Council Validation Rules |
| Change Control approved without rollback_plan | Violates Change Control Validation Rules |
| Stale KPI (>2× measurement_frequency) used in financial decision | Violates Evidence State governance rules |

---

# SECTION 5 — CROSS-LAYER RELATIONSHIPS

How assets in different layers (L1-L6) relate to each other, derived from cross-references in the Taxonomy.

## L1 (Business) ↔ L2 (Governance)

| L1 Asset | Relationship | L2 Asset | Notes |
|---|---|---|---|
| Portfolio | GOVERNED_BY | Council | Top-level governance binding |
| Program | GOVERNED_BY | Council | Program governance |
| Venture | GOVERNED_BY | Council | Venture governance, Nathan approval for new Ventures |
| Project | GOVERNED_BY | Policy | Project-level policy compliance |
| Business Capability | GOVERNED_BY | Policy | Capability policies |
| Portfolio | (owned by) | Executive Role | Executive Role OWNS Portfolio |
| Venture | (owned by) | Executive Role | Executive Role OWNS Venture |
| Executive KPI | EVALUATED_BY | Council | KPIs reviewed in governance meetings |
| Business Outcome | REFERENCED_BY | Council | Outcomes validated at governance level |
| Project | CARRIES | Risk Level | Risk Level (L2) applied to Project (L1) |
| Venture | CARRIES | Risk Level | Risk Level (L2) applied to Venture (L1) |

## L1 (Business) ↔ L3 (Engineering)

| L1 Asset | Relationship | L3 Asset | Notes |
|---|---|---|---|
| Project | PRODUCES | Repository | Projects create Engineering artifacts |
| Project | PRODUCES | Service | Projects produce Services |
| Project | PRODUCES | Agent | Projects produce Agents |
| Program | (associated with) | Repository | Long-term Program codebases |
| Business Capability | ENABLED_BY | Service | Capabilities realized through Services |
| Business Capability | ENABLED_BY | Integration | Capabilities realized through Integrations |

## L1 (Business) ↔ L4 (Operations)

| L1 Asset | Relationship | L4 Asset | Notes |
|---|---|---|---|
| Business Capability | ENABLED_BY | Agent | Capabilities realized by Agents |
| Venture | (measured through) | Dashboard | KPIs displayed on Dashboards |
| Portfolio | MEASURED_BY | Executive KPI (displayed by Dashboard) | Governance visibility chain |

## L2 (Governance) ↔ L3 (Engineering)

| L2 Asset | Relationship | L3 Asset | Notes |
|---|---|---|---|
| Standard | APPLIED_TO | Repository | Engineering must meet Standards |
| Standard | APPLIED_TO | API | API Standards govern contract design |
| Standard | APPLIED_TO | Database | Schema Standards |
| Policy | APPLIES_TO | Service | Services are policy-bound |
| Policy | APPLIES_TO | Agent | Agents are policy-bound (including spend cap) |
| Approval Type | IMPLEMENTED_BY | Service (sovereign_proxy) | sovereign_proxy is the approval gateway service |
| Secret Metadata | GOVERNED_BY | Policy | Secret lifecycle governance |

## L2 (Governance) ↔ L4 (Operations)

| L2 Asset | Relationship | L4 Asset | Notes |
|---|---|---|---|
| Policy | IMPLEMENTED_BY | Playbook → EXECUTED_BY Agent | Policy → Playbook → Agent execution chain |
| Council | GOVERNED_BY → | Agent Team | Agent Teams governed by Councils |
| Lifecycle State | VISUALIZED_BY | Dashboard | State visibility in Mission Control |
| Evidence State | APPLIED_TO | Operational Status | Every operational status carries evidence |

## L2 (Governance) ↔ L5 (Execution)

| L2 Asset | Relationship | L5 Asset | Notes |
|---|---|---|---|
| Risk Level | DETERMINES | Approval Type (requirements) | Risk drives approval gate selection |
| Risk Level | DETERMINES | Recovery Priority | Risk drives recovery sequencing |
| Evidence State | VERIFIED_BY | Verification Method | Evidence must be backed by method |
| Policy | ENFORCED_BY | Execution Role | Roles enforce policies at execution level |

## L3 (Engineering) ↔ L4 (Operations)

| L3 Asset | Relationship | L4 Asset | Notes |
|---|---|---|---|
| Repository | DEPLOYS_TO | Service | Code becomes running Service |
| Package | USED_BY | Service/Agent | Packages imported by operations layer |
| Library | IMPORTED_BY | Service/Agent/Automation | Shared logic consumed by operational assets |
| Framework | PROVIDES_STRUCTURE_FOR | Service/Agent | Framework governs operational structure |
| Model | USED_BY | Agent/Service | AI models consumed by agents |
| API | CONSUMED_BY | Agent | Agents call external APIs |
| Integration | PRODUCES (data_for) | Service | Integration feeds operational Services |
| Environment | HOSTS | Service/Agent | Environment scopes operational assets |
| Database | ACCESSED_BY | Service/Agent | Operational assets use Database |
| Secret Metadata | DESCRIBES | Service/Agent | Credentials described for operational use |

## L4 (Operations) ↔ L5 (Execution)

| L4 Asset | Relationship | L5 Asset | Notes |
|---|---|---|---|
| Service | APPLIED_TO by | Operational Status | Runtime health classification |
| Agent | APPLIED_TO by | Operational Status | Agent health classification |
| Agent | REPORTS_TO | Execution Role | Agent accountability chain |
| Execution Role | MEMBER_OF | Agent Team | Roles in teams |
| Dashboard | DISPLAYS | Operational Status | Health visible in Dashboard |
| Integration | ASSESSED_FOR by | Integration Readiness | Readiness gates Service transitions |
| Service/Database/Integration | APPLIED_TO by | Recovery Priority | Recovery sequencing |
| Service/Agent | APPLIED_TO by | Business Criticality | Tier assignments |

## L4 (Operations) ↔ L6 (Evolution)

| L4 Asset | Relationship | L6 Asset | Notes |
|---|---|---|---|
| Registry | QUERIED_BY | (by Dashboard/Agent) — COMPARES by | Drift Detection | Registry is the expected state anchor |
| Service/Agent/any | (subject of) | Current State | Point-in-time snapshots of operational assets |
| Registry | WRITTEN_BY | Automation (state sync) | Automation writes migrations to Registry |

## L5 (Execution) ↔ L6 (Evolution)

| L5 Asset | Relationship | L6 Asset | Notes |
|---|---|---|---|
| Verification Method | VALIDATES | (Schema Evolution outputs) | Methods validate evolution results |
| Integration Readiness | GATES | Lifecycle State transitions | Readiness gates state machine |
| Recovery Priority | DEFINED_BY | Playbook | Recovery Playbooks define Priority sequence |
| Business Criticality | DETERMINES | (Change Control approval level) | Tier-0 changes require P0 approval |

---

*OPEN EMPIRE ONTOLOGY V1.0.0 — Materialized 2026-08-05 — Alusi, Chief of Staff*
*Source: OPEN_EMPIRE_ASSET_TAXONOMY_V1.md*
*Next scheduled review: When Taxonomy advances to V1.1.0 or V2.0.0*
