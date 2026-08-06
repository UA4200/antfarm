# OPEN EMPIRE SCHEMA V1

**Version:** 1.0.0
**Status:** Draft — Pending Validation
**Owner:** Nathan (Sovereign Operator)
**Source:** OPEN_EMPIRE_ASSET_TAXONOMY_V1.md
**Materialization Date:** 2026-08-05
**Dependencies:** OPEN_EMPIRE_ASSET_TAXONOMY_V1.md · OPEN_EMPIRE_ONTOLOGY_V1.md
**Revision History:**

| Version | Date | Author | Change |
|---|---|---|---|
| 1.0.0 | 2026-08-05 | Alusi | Initial materialization under Governance Freeze Order 2026-08-05 |

---

## PREAMBLE

The Schema implements the Taxonomy as machine-readable field definitions. Every field name, type, and constraint is derived directly from `OPEN_EMPIRE_ASSET_TAXONOMY_V1.md`. No field is invented here. Unresolved items are marked `TODO_PENDING_APPROVAL`.

**Hierarchy:** Taxonomy → Schema → Asset Registry → OEPM

---

## SECTION 1: SCHEMA CONVENTIONS

### Field Type System

| Type Token | Description |
|---|---|
| `uuid` | UUID v4 string; immutable after creation |
| `string` | UTF-8 text; max length noted where relevant |
| `enum(...)` | One of the listed values only; case-sensitive |
| `iso8601` | ISO 8601 datetime string (e.g., `2026-08-05T15:30:00Z`) |
| `usd` | Non-negative number, US Dollar denominated |
| `semver` | Semantic version string (e.g., `1.0.0`) |
| `boolean` | `true` or `false` |
| `ref:TypeName` | Foreign key reference to another asset type's `id` field |
| `array[type]` | Ordered array of the specified type |
| `object` | Nested object; structure defined inline |
| `number` | Numeric value; signed unless noted |

### Common Fields (All Asset Types)

The following fields are inherited by ALL asset types. They are not repeated in per-type schemas below.

| Field | Type | Required | Constraints |
|---|---|---|---|
| `id` | `uuid` | ✅ | Unique; immutable after creation |
| `name` | `string` | ✅ | Max 200 chars; human-readable |
| `created_at` | `iso8601` | ✅ | Set at creation; immutable |
| `updated_at` | `iso8601` | ✅ | Updated on every write |
| `status` | `enum(...)` | ✅ | Values constrained to asset-type's Lifecycle Applicability |
| `owner` | `string` | ✅ | Name or role reference; must be active |

### Governance Metadata Fields (Governance Documents Only)

| Field | Type | Required | Constraints |
|---|---|---|---|
| `governance_version` | `semver` | ✅ | Schema version that validated this record |
| `last_validated_at` | `iso8601` | ✅ | Timestamp of last validation run |
| `validation_status` | `enum(passing, failing, not_validated)` | ✅ | — |

---

## SECTION 2: ASSET TYPE SCHEMAS

### Notation
Each schema shows only fields BEYOND the common fields (id, name, created_at, updated_at, status, owner).
`✅` = required. `○` = optional. Status enum values are the Lifecycle Applicability states for that type.

---

## LAYER 1 — BUSINESS

### Portfolio
**Status Values:** `Active` · `Archived`

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `mission_alignment` | `string` | ✅ | References documented mission statement |
| `programs` | `array[ref:Program]` | ✅ | Min 1 Program OR 1 Venture required |
| `ventures` | `array[ref:Venture]` | ✅ | Min 1 Program OR 1 Venture required |
| `kpis` | `array[ref:ExecutiveKPI]` | ✅ | — |
| `capital_deployed_usd` | `usd` | ✅ | — |

**Validation:** Must have ≥1 Program or Venture. Owner must be Nathan or delegated Executive Role.

---

### Program
**Status Values:** `Planned` · `Active` · `On Hold` · `Completed` · `Archived`

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `portfolio_id` | `ref:Portfolio` | ✅ | Must belong to exactly one Portfolio |
| `objectives` | `array[string]` | ✅ | — |
| `projects` | `array[ref:Project]` | ✅ | Min 1 required |
| `capabilities` | `array[ref:BusinessCapability]` | ○ | — |
| `start_date` | `iso8601` | ✅ | — |
| `target_end_date` | `iso8601` | ✅ | — |

**Validation:** Must belong to exactly one Portfolio. Owner must be an active Executive Role. `On Hold` requires documented reason and review date.

---

### Project
**Status Values:** `Planned` · `In Progress` · `Blocked` · `Complete` · `Cancelled`

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `program_id` | `ref:Program` | ✅ | — |
| `deliverables` | `array[string]` | ✅ | Min 1 required |
| `start_date` | `iso8601` | ✅ | — |
| `end_date` | `iso8601` | ✅ | Must be defined |
| `risk_level` | `enum(P0, P1, P2, P3, P4)` | ✅ | See Risk Level schema |

**Validation:** Must have `end_date`. Min 1 deliverable. Must carry `risk_level`. Cannot be `Active` without owner. `Blocked` requires documented blocker and escalation target.

---

### Business Capability
**Status Values:** `Emerging` · `Developing` · `Established` · `Optimized` · `Retired`

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `description` | `string` | ✅ | Implementation-independent definition |
| `maturity_level` | `enum(Emerging, Developing, Established, Optimized)` | ✅ | Must be one of four values |
| `enabling_assets` | `array[uuid]` | ✅ | Min 1 required |
| `programs` | `array[ref:Program]` | ✅ | — |

**Validation:** Must be implementation-independent. Min 1 enabling asset. `Retired` must reference retirement justification.

---

### Venture
**Status Values:** `Pre-Launch` · `Active` · `Scaling` · `On Hold` · `Winding Down` · `Closed`

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `portfolio_id` | `ref:Portfolio` | ✅ | — |
| `revenue_model` | `string` | ✅ | Must be explicit |
| `capital_deployed_usd` | `usd` | ✅ | — |
| `daily_spend_cap_usd` | `usd` | ✅ | Mandatory if autonomous financial operations |
| `programs` | `array[ref:Program]` | ✅ | — |
| `p_and_l_ref` | `string` | ✅ | Path or reference to P&L record |

**Validation:** Must have `revenue_model`. Must have `capital_deployed_usd`. `daily_spend_cap_usd` is MANDATORY for any autonomous financial operations. Cannot transition to `Scaling` without ≥1 verified revenue event.

---

### Executive KPI
**Status Values:** `Active` · `Deprecated`

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `target_value` | `number` | ✅ | — |
| `current_value` | `number` | ✅ | — |
| `unit` | `string` | ✅ | e.g., USD, %, count |
| `measurement_frequency` | `string` | ✅ | e.g., daily, weekly |
| `owner_asset_id` | `uuid` | ✅ | Linked to exactly one owner asset |
| `owner_asset_type` | `string` | ✅ | Taxonomy canonical asset type name |
| `direction` | `enum(higher_is_better, lower_is_better)` | ✅ | — |
| `last_updated` | `iso8601` | ✅ | — |
| `evidence_state` | `enum(Verified, Asserted, Estimated, Unverified, Stale)` | ✅ | — |

**Validation:** Must have numeric `target_value`. Must define `measurement_frequency`. Linked to exactly one owner asset. Stale KPIs (not refreshed within 2× measurement_frequency) must be flagged and must not be used in financial decisions.

---

### Business Outcome
**Status Values:** `Targeted` · `Achieved` · `Missed` · `Superseded`

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `description` | `string` | ✅ | — |
| `target_date` | `iso8601` | ✅ | — |
| `success_criteria` | `array[string]` | ✅ | Min 1 required |
| `linked_kpis` | `array[ref:ExecutiveKPI]` | ✅ | Min 1 required |
| `linked_programs` | `array[ref:Program]` | ✅ | — |

**Validation:** Must have `success_criteria[]`. Must link to ≥1 KPI. Cannot be `Achieved` without all success_criteria confirmed. `Missed` must document causal analysis.

---

## LAYER 2 — GOVERNANCE

### Council
**Status Values:** `Active` · `Suspended` · `Dissolved`

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `domain` | `string` | ✅ | — |
| `members` | `array[string]` | ✅ | — |
| `chair_role` | `string` | ✅ | Must be assigned |
| `escalation_path` | `string` | ✅ | Must be defined |
| `policies` | `array[ref:Policy]` | ✅ | — |
| `meeting_cadence` | `string` | ✅ | — |

**Validation:** Must have `chair_role`. Must define `escalation_path`. Cannot be `Dissolved` while governing Active assets. `Suspended` must document reason.

---

### Executive Role
**Status Values:** `Active` · `Vacant` · `Delegated` · `Retired`

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `title` | `string` | ✅ | — |
| `domain` | `string` | ✅ | — |
| `holder` | `enum(human, agent)` | ✅ | — |
| `council_id` | `ref:Council` | ✅ | — |
| `authority_scope` | `string` | ✅ | Must be explicit |
| `escalation_target` | `string` | ✅ | — |

**Validation:** Must have named holder. Must define `authority_scope` explicitly. `Vacant` roles must have `acting_holder` or `escalation_target`. `Delegated` must document scope and duration.

---

### Ownership Role
**Status Values:** `Active` · `Delegated` · `Vacant`

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `title` | `string` | ✅ | — |
| `asset_type` | `string` | ✅ | Taxonomy canonical type name |
| `asset_ids` | `array[uuid]` | ✅ | Min 1 asset |
| `holder` | `enum(human, agent)` | ✅ | — |
| `executive_role_id` | `ref:ExecutiveRole` | ✅ | — |

**Validation:** Must be linked to ≥1 asset. Cannot be `Vacant` for Tier-0 assets. Must have escalation path. Tier-0 agent-held roles require human Council oversight.

---

### Standard
**Status Values:** `Draft` · `Active` · `Deprecated` · `Superseded`

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `version` | `semver` | ✅ | — |
| `scope` | `string` | ✅ | Must be explicit |
| `requirements` | `array[string]` | ✅ | — |
| `issuing_council_id` | `ref:Council` | ✅ | — |
| `effective_date` | `iso8601` | ✅ | — |
| `superseded_by` | `ref:Standard` | ○ | Required if `Deprecated` |

**Validation:** Must have version. Must define scope. `Deprecated` must reference replacement. `Active` must list ≥1 Verification Method. Cannot be `Deprecated` without superseding Standard.

---

### Policy
**Status Values:** `Draft` · `Active` · `Under Review` · `Deprecated` · `Superseded`

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `version` | `semver` | ✅ | — |
| `statement` | `string` | ✅ | — |
| `scope` | `string` | ✅ | — |
| `exceptions` | `array[string]` | ✅ | Empty array = no exceptions; silence not permitted |
| `enforcement_mechanism` | `string` | ✅ | — |
| `issuing_council_id` | `ref:Council` | ✅ | — |
| `effective_date` | `iso8601` | ✅ | — |

**Validation:** Must have `statement`. Must define `scope`. Must list `enforcement_mechanism`. Cannot be `Deprecated` without superseding Policy. Exceptions must be explicit — silence implies no exceptions.

---

### Playbook
**Status Values:** `Draft` · `Active` · `Outdated` · `Deprecated`

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `version` | `semver` | ✅ | — |
| `policy_ids` | `array[ref:Policy]` | ✅ | Must implement ≥1 Policy |
| `steps` | `array[string]` | ✅ | Must be deterministic and sequentially ordered |
| `prerequisites` | `array[string]` | ✅ | — |
| `expected_outputs` | `array[string]` | ✅ | — |
| `last_validated` | `iso8601` | ✅ | — |

**Validation:** Must implement ≥1 Policy. Must have `steps[]`. Must have `expected_outputs[]`. Steps must be deterministic.

---

### Approval Type
**Status Values:** `Active` · `Deprecated`

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `authority_level` | `string` | ✅ | — |
| `mechanism` | `enum(telegram, openclaw_native, n8n, manual)` | ✅ | — |
| `timeout_seconds` | `number` | ✅ | — |
| `escalation_on_timeout` | `string` | ✅ | Timeout escalates — never auto-approves |
| `applies_to` | `array[string]` | ✅ | Asset types or action types this covers |

---

### Risk Level
**Status Values:** `Active` (canonical enumeration)

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `id` | `enum(P0, P1, P2, P3, P4)` | ✅ | Overrides common `id` field; must be one of five values |
| `description` | `string` | ✅ | — |
| `response_sla_minutes` | `number` | ✅ | — |
| `approval_required` | `boolean` | ✅ | — |
| `escalation_path` | `string` | ✅ | P0 and P1 require explicit escalation paths |

**Note:** Risk Levels are canonical enumerated values, not individually created records.

---

### Lifecycle State
**Status Values:** `Active` (this entry IS the lifecycle definition)

Applied fields (added to every asset type that has a lifecycle):

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `status` | `string` | ✅ | Constrained to asset-type's Lifecycle Applicability |
| `status_changed_at` | `iso8601` | ✅ | Must be logged on every transition |
| `status_changed_by` | `string` | ✅ | Actor who triggered the change |

**Validation:** State transitions must be logged with actor and timestamp. Terminal states (Archived, Retired, Cancelled, Closed) require explicit approval. Undocumented transitions are governance violations.

---

### Evidence State
**Status Values:** `Active` (canonical enumeration)

Applied fields (added to every reportable asset):

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `evidence_state` | `enum(Verified, Asserted, Estimated, Unverified, Stale)` | ✅ | — |
| `evidence_source` | `string` | ✅ | — |
| `evidence_timestamp` | `iso8601` | ✅ | — |

**State Definitions:** Verified = machine-confirmed with source. Asserted = human-stated. Estimated = calculated from proxy. Unverified = no confirmation. Stale = confirmed but not refreshed within SLA.

---

## LAYER 3 — ENGINEERING

### Repository
**Status Values:** `Active` · `Archived` · `Deprecated`

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `github_org` | `string` | ✅ | — |
| `github_repo` | `string` | ✅ | — |
| `visibility` | `enum(private, public)` | ✅ | — |
| `default_branch` | `string` | ✅ | — |
| `tier` | `enum(T0, T1, T2, T3)` | ✅ | — |
| `owner_role_id` | `ref:OwnershipRole` | ✅ | — |
| `ci_status` | `string` | ✅ | Tracked for T0 and T1 |
| `last_commit_at` | `iso8601` | ✅ | — |
| `git_initialized` | `boolean` | ✅ | T0 repos must be `true` |
| `remote_url` | `string` | ✅ | — |

**Validation:** Must define `tier`. T0 repos must have remote configured and `git_initialized=true`. Uninitialized T0 repos are a governance violation.

---

### Package
**Status Values:** `Stable` · `Beta` · `Deprecated` · `Yanked`

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `version` | `semver` | ✅ | — |
| `repository_id` | `ref:Repository` | ✅ | — |
| `runtime` | `enum(python, node, other)` | ✅ | — |
| `entry_point` | `string` | ✅ | — |
| `dependencies` | `array[string]` | ✅ | — |

**Validation:** Must have semver. Must define `runtime`. Yanked packages must be replaced in all consuming services within 24h. Deprecated packages trigger P1 if still consumed by Active services.

---

### Library
**Status Values:** `Active` · `Deprecated` · `Superseded`

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `version` | `semver` | ✅ | — |
| `package_id` | `ref:Package` | ✅ | — |
| `module_path` | `string` | ✅ | Must be reachable when `Active` |
| `public_api` | `array[string]` | ✅ | — |

**Validation:** Cannot be `Active` if `module_path` is unreachable. `Deprecated` must list consuming assets with migration timelines.

---

### Framework
**Status Values:** `Active` · `Deprecated` · `Upgrading`

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `version` | `semver` | ✅ | — |
| `runtime` | `string` | ✅ | — |
| `purpose` | `string` | ✅ | — |
| `consuming_assets` | `array[uuid]` | ✅ | — |
| `upgrade_policy` | `string` | ✅ | Must be defined |

**Validation:** Must define `upgrade_policy`. Must list `consuming_assets[]`. Major version upgrades require Change Control. `Upgrading` state must have rollback plan.

---

### Model
**Status Values:** `Available` · `Deprecated` · `Unavailable` · `Rate-Limited`

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `provider_id` | `ref:ModelProvider` | ✅ | — |
| `version` | `string` | ✅ | — |
| `context_window` | `number` | ✅ | Token count |
| `cost_per_1k_input_usd` | `usd` | ✅ | — |
| `cost_per_1k_output_usd` | `usd` | ✅ | — |
| `latency_class` | `enum(real-time, batch)` | ✅ | — |
| `use_cases` | `array[string]` | ✅ | — |

**Validation:** Must reference a Model Provider. Must define cost fields. Models may not be added to real-time chains without explicit approval (ADR-004).

---

### Model Provider
**Status Values:** `Active` · `Degraded` · `Unavailable`

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `api_endpoint` | `string` | ✅ | — |
| `auth_type` | `string` | ✅ | — |
| `models` | `array[ref:Model]` | ✅ | — |
| `billing_account` | `string` | ✅ | — |
| `daily_cost_cap_usd` | `usd` | ✅ | Mandatory |

**Validation:** Must define `auth_type`. Must define `daily_cost_cap_usd`. API credentials stored in Secret Metadata — never hardcoded. Degradation triggers fallback routing.

---

### API
**Status Values:** `Active` · `Deprecated` · `Breaking-Change-Pending` · `Retired`

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `version` | `semver` | ✅ | Consuming assets must pin to specific version |
| `base_url` | `string` | ✅ | — |
| `auth_type` | `string` | ✅ | — |
| `endpoints` | `array[string]` | ✅ | — |
| `rate_limits` | `object` | ✅ | — |
| `breaking_change_policy` | `string` | ✅ | — |

**Validation:** Must define `version`. Must list `endpoints[]`. Must define `rate_limits`. `Deprecated` must list migration target. Breaking changes require Change Control and migration plan before deployment.

---

### Router
**Status Values:** `Active` · `Degraded` · `Misconfigured`

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `type` | `enum(model_router, message_router, request_router, approval_router)` | ✅ | — |
| `rules` | `array[object]` | ✅ | Min 1; must be deterministic and ordered |
| `fallback_target` | `string` | ✅ | Must be defined |

**Validation:** Must define ≥1 routing rule. Must have `fallback_target`. Rules must be ordered and deterministic. `Misconfigured` must be flagged immediately.

---

### Integration
**Status Values:** `Active` · `Degraded` · `Broken` · `Deprecated`

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `external_system` | `string` | ✅ | — |
| `api_id` | `ref:API` | ✅ | — |
| `auth_type` | `string` | ✅ | — |
| `secret_metadata_id` | `ref:SecretMetadata` | ✅ | Never store credentials inline |
| `data_flow_direction` | `enum(inbound, outbound, bidirectional)` | ✅ | — |
| `error_handling` | `string` | ✅ | — |
| `circuit_breaker` | `boolean` | ✅ | T0 integrations must be `true` |

**Validation:** Must reference Secret Metadata. Must define `error_handling`. Must define `data_flow_direction`. `Broken` triggers P1 alert within 60s. All T0 integrations must have `circuit_breaker=true`.

---

### Environment
**Status Values:** `Active` · `Decommissioned`

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `type` | `enum(development, staging, production, local)` | ✅ | One of four canonical values only |
| `host` | `string` | ✅ | — |
| `services` | `array[ref:Service]` | ✅ | — |
| `secrets_scope` | `string` | ✅ | Production must have explicit scope; staging must NOT use production secrets |

---

### Infrastructure
**Status Values:** `Active` · `Degraded` · `Maintenance` · `Decommissioned`

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `type` | `enum(mac_mini, cloud_vps, container, managed_service)` | ✅ | — |
| `host_identifier` | `string` | ✅ | — |
| `os` | `string` | ✅ | — |
| `cpu` | `string` | ✅ | — |
| `ram_gb` | `number` | ✅ | — |
| `network_posture` | `string` | ✅ | Must be documented; production must be loopback-bound unless explicitly opened with Nathan approval |

---

### Database
**Status Values:** `Active` · `Migrating` · `Degraded` · `Retired`

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `engine` | `string` | ✅ | — |
| `version` | `string` | ✅ | — |
| `host` | `string` | ✅ | — |
| `port` | `number` | ✅ | — |
| `database_name` | `string` | ✅ | — |
| `schemas` | `array[string]` | ✅ | — |
| `owner_role_id` | `ref:OwnershipRole` | ✅ | — |
| `backup_policy` | `string` | ✅ | T0 databases must have automated backup |

**Validation:** Must define `engine` and `version`. Must have `backup_policy`. Schema changes require Change Control. `Degraded` triggers P0 alert.

---

### Storage
**Status Values:** `Active` · `Archiving` · `Full` · `Retired`

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `type` | `enum(filesystem, s3, object_store)` | ✅ | — |
| `root_path` | `string` | ✅ | — |
| `retention_policy` | `string` | ✅ | — |
| `owner_role_id` | `ref:OwnershipRole` | ✅ | — |
| `access_permissions` | `string` | ✅ | — |
| `immutable` | `boolean` | ✅ | — |

---

### Secret Metadata
**Status Values:** `Active` · `Rotating` · `Expired` · `Revoked`

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `type` | `enum(api_key, private_key, oauth_token, webhook_secret)` | ✅ | — |
| `associated_system` | `string` | ✅ | — |
| `environment` | `string` | ✅ | — |
| `rotation_policy` | `string` | ✅ | — |
| `last_rotated_at` | `iso8601` | ✅ | — |
| `expiry_at` | `iso8601` | ○ | Required if applicable |

**Note:** This record stores metadata only. The actual secret is at `~/.openclaw/secrets/.env`. Credentials are NEVER stored in this schema record.

---

## LAYER 4 — OPERATIONS

### Runtime
**Status Values:** `Running` · `Starting` · `Stopped` · `Crashed` · `Restarting`

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `environment_id` | `ref:Environment` | ✅ | — |
| `package_id` | `ref:Package` | ✅ | — |
| `interpreter` | `enum(python3.13, node24, other)` | ✅ | — |
| `pid` | `number` | ✅ | — |
| `uptime_seconds` | `number` | ✅ | — |
| `memory_mb` | `number` | ✅ | — |

---

### Service
**Status Values:** `Planned` · `Staging` · `Active` · `Degraded` · `Stopped` · `Retired`

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `pm2_id` | `number` | ✅ | PM2 process numeric id |
| `port` | `number` | ○ | If applicable |
| `tier` | `string` | ✅ | — |
| `owner_role_id` | `ref:OwnershipRole` | ✅ | — |
| `health_check_url` | `string` | ○ | — |
| `restart_policy` | `string` | ✅ | — |
| `last_restart_at` | `iso8601` | ✅ | — |

---

### PM2 Process
**Status Values:** `Online` · `Stopped` · `Errored` · `Restarting`

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `id` | `number` | ✅ | PM2 numeric id; overrides common uuid id |
| `script` | `string` | ✅ | — |
| `args` | `array[string]` | ✅ | — |
| `cwd` | `string` | ✅ | — |
| `interpreter` | `string` | ✅ | — |
| `env` | `object` | ✅ | Key-value environment vars |
| `restart_policy` | `string` | ✅ | — |
| `cron_restart` | `string` | ○ | cron expression if applicable |

---

### Workflow
**Status Values:** `Active` · `Paused` · `Deprecated` · `Failed`

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `trigger_type` | `enum(cron, event, manual)` | ✅ | — |
| `steps` | `array[string]` | ✅ | — |
| `success_criteria` | `string` | ✅ | — |
| `owner_role_id` | `ref:OwnershipRole` | ✅ | — |
| `framework` | `enum(n8n, antfarm, openclaw_cron)` | ✅ | — |

---

### Automation
**Status Values:** `Active` · `Paused` · `Failed` · `Deprecated`

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `trigger` | `string` | ✅ | cron expression, event name, or api_call |
| `script` | `string` | ✅ | — |
| `cwd` | `string` | ✅ | — |
| `environment_id` | `ref:Environment` | ✅ | — |
| `logging_target` | `string` | ✅ | — |
| `retry_policy` | `string` | ✅ | — |

---

### Agent
**Status Values:** `Draft` · `Testing` · `Active` · `Suspended` · `Retired`

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `agent_type` | `enum(director, arb, trader, monitor, orchestrator, specialist, chief_of_staff)` | ✅ | — |
| `model_id` | `ref:Model` | ✅ | — |
| `tool_access` | `array[string]` | ✅ | — |
| `policy_ids` | `array[ref:Policy]` | ✅ | — |
| `owner_role_id` | `ref:OwnershipRole` | ✅ | — |
| `memory_scope` | `string` | ✅ | — |
| `spend_cap_usd` | `usd` | ○ | **Required if agent has financial operations** |

**Validation:** Financial agents MUST have `spend_cap_usd`. All agents must have `policy_ids[]`.

---

### Agent Team
**Status Values:** `Active` · `Reorganizing` · `Disbanded`

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `purpose` | `string` | ✅ | — |
| `agents` | `array[ref:Agent]` | ✅ | — |
| `lead_agent_id` | `ref:Agent` | ✅ | — |
| `council_id` | `ref:Council` | ✅ | — |
| `coordination_protocol` | `string` | ✅ | — |
| `collective_spend_cap_usd` | `usd` | ✅ | — |

---

### Dashboard
**Status Values:** `Active` · `Degraded` · `Stopped`

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `port` | `number` | ✅ | — |
| `service_id` | `ref:Service` | ✅ | — |
| `data_sources` | `array[string]` | ✅ | — |
| `refresh_interval_seconds` | `number` | ✅ | — |
| `access_control` | `string` | ✅ | — |

---

### Knowledge Base
**Status Values:** `Active` · `Outdated` · `Archived`

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `domain` | `string` | ✅ | — |
| `format` | `enum(markdown, json, jsonl, vector_db)` | ✅ | — |
| `root_path` | `string` | ✅ | — |
| `curation_policy` | `string` | ✅ | — |
| `last_updated` | `iso8601` | ✅ | — |
| `owner_role_id` | `ref:OwnershipRole` | ✅ | — |

---

### Memory Store
**Status Values:** `Active` · `Compressing` · `Corrupted` · `Archived`

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `type` | `enum(active, compressed, archive, vector)` | ✅ | — |
| `root_path` | `string` | ✅ | — |
| `retention_days` | `number` | ✅ | — |
| `compression_schedule` | `string` | ✅ | cron expression |
| `owner_agent_id` | `ref:Agent` | ✅ | — |

---

### Registry
**Status Values:** `Active` · `Stale` · `Rebuilding`

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `scope` | `enum(global, domain-specific)` | ✅ | — |
| `asset_types` | `array[string]` | ✅ | Taxonomy canonical type names |
| `storage_format` | `enum(json, jsonl, postgresql, markdown)` | ✅ | — |
| `root_path_or_table` | `string` | ✅ | — |
| `last_sync_at` | `iso8601` | ✅ | — |
| `owner_role_id` | `ref:OwnershipRole` | ✅ | — |

---

## LAYER 5 — STATUS

### Execution Role
**Status Values:** `Active` · `Delegated` · `Vacant`

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `title` | `string` | ✅ | — |
| `scope` | `string` | ✅ | — |
| `holder` | `string` | ✅ | agent_id or human_name |
| `ownership_role_id` | `ref:OwnershipRole` | ✅ | — |
| `task_types` | `array[string]` | ✅ | — |

---

### Operational Status
**Status Values:** `Active` (real-time classification)

Applied fields (attached to monitored assets):

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `status` | `enum(OK, DEGRADED, STOPPED, ERRORED, RESTARTING, UNKNOWN)` | ✅ | — |
| `last_checked_at` | `iso8601` | ✅ | — |
| `check_method` | `enum(pm2, health_check, heartbeat, manual)` | ✅ | — |
| `incident_open` | `boolean` | ✅ | — |
| `notes` | `string` | ○ | — |

---

### Integration Readiness
**Status Values:** `Not Ready` · `Partially Ready` · `Ready` · `Validated` · `Degraded`

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `integration_id` | `ref:Integration` | ✅ | — |
| `auth_verified` | `boolean` | ✅ | — |
| `endpoint_reachable` | `boolean` | ✅ | — |
| `error_handling_tested` | `boolean` | ✅ | — |
| `end_to_end_validated` | `boolean` | ✅ | — |
| `last_validated_at` | `iso8601` | ✅ | — |
| `readiness_state` | `enum(Not Ready, Partially Ready, Ready, Validated, Degraded)` | ✅ | — |
| `notes` | `string` | ○ | — |

---

### Business Criticality
**Status Values:** `Active` (canonical enumeration)

Applied fields:

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `criticality_tier` | `enum(Tier-0, Tier-1, Tier-2, Tier-3)` | ✅ | — |
| `revenue_impact` | `enum(direct, indirect, none)` | ✅ | — |
| `mttr_target_minutes` | `number` | ✅ | Mean Time To Recover |
| `rpo_target_minutes` | `number` | ✅ | Recovery Point Objective |
| `notes` | `string` | ○ | — |

---

### Recovery Priority
**Status Values:** `Active` (canonical ordered list)

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `priority_rank` | `number` | ✅ | 1 = highest priority |
| `asset_id` | `uuid` | ✅ | — |
| `asset_type` | `string` | ✅ | Taxonomy canonical type name |
| `rto_minutes` | `number` | ✅ | Recovery Time Objective |
| `rpo_minutes` | `number` | ✅ | Recovery Point Objective |
| `dependencies` | `array[uuid]` | ✅ | — |
| `recovery_steps_ref` | `string` | ✅ | Path to recovery runbook |

---

### Relationship Type
**Status Values:** `Active` (canonical enumeration)

Applied fields (relationship record between two assets):

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `source_asset_id` | `uuid` | ✅ | — |
| `source_asset_type` | `string` | ✅ | — |
| `relationship_type` | `string` | ✅ | Must be a verb from Ontology vocabulary |
| `target_asset_id` | `uuid` | ✅ | — |
| `target_asset_type` | `string` | ✅ | — |
| `direction` | `enum(directed, bidirectional)` | ✅ | — |
| `strength` | `enum(required, optional, deprecated)` | ✅ | — |

---

### Verification Method
**Status Values:** `Active` (canonical enumeration)

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `type` | `enum(api_call, log_check, ui_check, unit_test, end_to_end_test, manual_review, heartbeat, balance_check, schema_diff)` | ✅ | — |
| `automation_eligible` | `boolean` | ✅ | — |
| `cadence` | `string` | ✅ | — |
| `evidence_produced` | `string` | ✅ | What artifact this method generates |

---

## LAYER 6 — LIFECYCLE

### Current State
**Status Values:** `Active` (point-in-time snapshot)

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `asset_id` | `uuid` | ✅ | — |
| `snapshot_timestamp` | `iso8601` | ✅ | — |
| `captured_by` | `string` | ✅ | — |
| `evidence_state` | `enum(Verified, Asserted, Estimated, Unverified, Stale)` | ✅ | — |
| `configuration` | `object` | ✅ | Key-value snapshot of asset configuration |
| `operational_status` | `string` | ✅ | — |
| `known_issues` | `array[string]` | ✅ | Empty array if none |
| `notes` | `string` | ○ | — |

---

### Target State
**Status Values:** `Proposed` · `Approved` · `In Progress` · `Achieved` · `Superseded`

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `asset_id` | `uuid` | ✅ | — |
| `target_id` | `uuid` | ✅ | — |
| `approved_by` | `string` | ✅ | Nathan for all non-trivial targets |
| `approved_at` | `iso8601` | ✅ | — |
| `target_configuration` | `object` | ✅ | — |
| `success_criteria` | `array[string]` | ✅ | — |
| `target_date` | `iso8601` | ✅ | — |

---

### Migration State
**Status Values:** `Not Started` · `In Progress` · `Blocked` · `Rolled Back` · `Complete`

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `asset_id` | `uuid` | ✅ | — |
| `migration_id` | `uuid` | ✅ | — |
| `current_state_id` | `ref:CurrentState` | ✅ | — |
| `target_state_id` | `ref:TargetState` | ✅ | — |
| `steps_completed` | `array[string]` | ✅ | — |
| `steps_remaining` | `array[string]` | ✅ | — |
| `blockers` | `array[string]` | ✅ | Empty array if none |
| `risk_level` | `enum(P0, P1, P2, P3, P4)` | ✅ | — |
| `rollback_plan` | `string` | ✅ | — |

---

### Retirement State
**Status Values:** `Planned Retirement` · `Retiring` · `Retired` · `Archived`

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `asset_id` | `uuid` | ✅ | — |
| `retirement_date` | `iso8601` | ✅ | — |
| `approved_by` | `string` | ✅ | — |
| `superseded_by_id` | `uuid` | ○ | Required if replaced by another asset |
| `archive_path` | `string` | ✅ | — |
| `data_retention_policy` | `string` | ✅ | — |

---

### Supersession
**Status Values:** `Active` (permanent record — never deleted)

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `predecessor_asset_id` | `uuid` | ✅ | — |
| `predecessor_asset_type` | `string` | ✅ | — |
| `successor_asset_id` | `uuid` | ✅ | — |
| `successor_asset_type` | `string` | ✅ | — |
| `effective_date` | `iso8601` | ✅ | — |
| `approved_by` | `string` | ✅ | — |
| `reason` | `string` | ✅ | — |
| `migration_state_id` | `ref:MigrationState` | ○ | If applicable |
| `notes` | `string` | ○ | — |

---

### Versioning
**Status Values:** `Active` (continuous — applies throughout an asset's lifecycle)

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `asset_id` | `uuid` | ✅ | — |
| `version_scheme` | `enum(semver, calver, git_sha, sequential)` | ✅ | — |
| `current_version` | `string` | ✅ | — |
| `previous_version` | `string` | ✅ | — |
| `changelog_ref` | `string` | ✅ | Path or URL to changelog |
| `version_history` | `array[object]` | ✅ | — |

---

### Change Control
**Status Values:** `Proposed` · `Approved` · `In Progress` · `Complete` · `Rejected` · `Rolled Back`

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `change_title` | `string` | ✅ | — |
| `asset_ids` | `array[uuid]` | ✅ | — |
| `change_type` | `enum(config, code, schema, infrastructure, policy)` | ✅ | — |
| `risk_level` | `enum(P0, P1, P2, P3, P4)` | ✅ | — |
| `approver_id` | `string` | ✅ | Nathan for all P0/P1 changes |
| `rollback_plan` | `string` | ✅ | — |
| `scheduled_at` | `iso8601` | ✅ | — |
| `completion_evidence` | `string` | ✅ | Required to mark `Complete` |

---

### Drift Detection
**Status Values:** `Active` · `Alert-Open` · `Resolved` · `Suppressed`

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `asset_id` | `uuid` | ✅ | — |
| `detection_method` | `enum(config_hash, process_check, api_probe, schema_diff)` | ✅ | — |
| `expected_state_ref` | `string` | ✅ | Reference to baseline/target state |
| `detected_at` | `iso8601` | ✅ | — |
| `drift_description` | `string` | ✅ | — |
| `severity` | `enum(P0, P1, P2, P3, P4)` | ✅ | — |
| `resolution_ref` | `string` | ○ | Required to mark `Resolved` |

---

### Schema Evolution
**Status Values:** `Proposed` · `Approved` · `In Progress` · `Complete` · `Rejected`

| Field | Type | Req | Notes / Constraints |
|---|---|---|---|
| `schema_id` | `uuid` | ✅ | — |
| `current_version` | `semver` | ✅ | — |
| `proposed_change` | `string` | ✅ | — |
| `backward_compatible` | `boolean` | ✅ | — |
| `migration_script_ref` | `string` | ○ | **Required if `backward_compatible=false`** |
| `approved_by` | `string` | ✅ | — |
| `effective_date` | `iso8601` | ✅ | — |

---

## SECTION 3: VALIDATION RULE INDEX

| RULE-ID | Asset Type | Rule Text | Severity |
|---|---|---|---|
| RULE-001 | Portfolio | Must have ≥1 Program or Venture | ERROR |
| RULE-002 | Portfolio | Owner must be Nathan or delegated Executive Role | ERROR |
| RULE-003 | Portfolio | Must align to documented mission statement | ERROR |
| RULE-004 | Program | Must belong to exactly one Portfolio | ERROR |
| RULE-005 | Program | Must have ≥1 Project | ERROR |
| RULE-006 | Program | Owner must be active Executive Role | ERROR |
| RULE-007 | Program | `On Hold` requires documented reason and review date | ERROR |
| RULE-008 | Project | Must have defined `end_date` | ERROR |
| RULE-009 | Project | Must list ≥1 deliverable | ERROR |
| RULE-010 | Project | Must carry assigned `risk_level` | ERROR |
| RULE-011 | Project | Cannot be `Active` without owner | ERROR |
| RULE-012 | Project | `Blocked` requires documented blocker and escalation target | ERROR |
| RULE-013 | Business Capability | Must be implementation-independent | WARNING |
| RULE-014 | Business Capability | Must list ≥1 enabling asset | ERROR |
| RULE-015 | Business Capability | `maturity_level` must be one of four canonical values | ERROR |
| RULE-016 | Business Capability | `Retired` must reference retirement justification | ERROR |
| RULE-017 | Venture | Must have explicit `revenue_model` | ERROR |
| RULE-018 | Venture | Must have defined `capital_deployed_usd` | ERROR |
| RULE-019 | Venture | Must have `daily_spend_cap_usd` if autonomous financial operations | ERROR |
| RULE-020 | Venture | Cannot transition to `Scaling` without ≥1 verified revenue event | ERROR |
| RULE-021 | Executive KPI | Must have numeric `target_value` | ERROR |
| RULE-022 | Executive KPI | Must define `measurement_frequency` | ERROR |
| RULE-023 | Executive KPI | Must be linked to exactly one owner asset | ERROR |
| RULE-024 | Executive KPI | `evidence_state` must be populated | ERROR |
| RULE-025 | Executive KPI | Stale KPIs must be flagged; must not be used in financial decisions | ERROR |
| RULE-026 | Business Outcome | Must have `success_criteria[]` | ERROR |
| RULE-027 | Business Outcome | Must link to ≥1 KPI | ERROR |
| RULE-028 | Business Outcome | Cannot be `Achieved` without all success_criteria confirmed | ERROR |
| RULE-029 | Business Outcome | `Missed` must document causal analysis | WARNING |
| RULE-030 | Council | Must have `chair_role` assigned | ERROR |
| RULE-031 | Council | Must define `escalation_path` | ERROR |
| RULE-032 | Council | Cannot be `Dissolved` while governing Active assets | ERROR |
| RULE-033 | Council | `Suspended` must document reason | ERROR |
| RULE-034 | Executive Role | Must have named holder | ERROR |
| RULE-035 | Executive Role | Must define `authority_scope` explicitly | ERROR |
| RULE-036 | Executive Role | `Vacant` must have `acting_holder` or `escalation_target` | ERROR |
| RULE-037 | Ownership Role | Must be linked to ≥1 asset | ERROR |
| RULE-038 | Ownership Role | Cannot be `Vacant` for Tier-0 assets | ERROR |
| RULE-039 | Standard | Must have version number | ERROR |
| RULE-040 | Standard | `Deprecated` must reference replacement | ERROR |
| RULE-041 | Standard | `Active` must list ≥1 Verification Method | ERROR |
| RULE-042 | Standard | Cannot be `Deprecated` without superseding Standard | ERROR |
| RULE-043 | Policy | Must have `statement` | ERROR |
| RULE-044 | Policy | Must define `scope` | ERROR |
| RULE-045 | Policy | Must list `enforcement_mechanism` | ERROR |
| RULE-046 | Policy | Exceptions must be explicit — empty array = no exceptions | ERROR |
| RULE-047 | Playbook | Must implement ≥1 Policy | ERROR |
| RULE-048 | Playbook | Steps must be deterministic and sequentially ordered | ERROR |
| RULE-049 | Approval Type | Timeout must escalate — never auto-approve | ERROR |
| RULE-050 | Repository | Must define `tier` | ERROR |
| RULE-051 | Repository | T0 repos must have remote and `git_initialized=true` | ERROR |
| RULE-052 | Package | `Yanked` packages must be replaced within 24h | ERROR |
| RULE-053 | Package | `Deprecated` package still consumed by Active service → P1 alert | ERROR |
| RULE-054 | Library | Cannot be `Active` if `module_path` unreachable | ERROR |
| RULE-055 | Model | Models may not be added to real-time chains without explicit approval | ERROR |
| RULE-056 | Model Provider | API credentials must be in Secret Metadata — never hardcoded | ERROR |
| RULE-057 | Model Provider | Must define `daily_cost_cap_usd` | ERROR |
| RULE-058 | API | Consuming assets must pin to specific version | WARNING |
| RULE-059 | API | Breaking changes require Change Control before deployment | ERROR |
| RULE-060 | Integration | Must reference Secret Metadata (never inline credentials) | ERROR |
| RULE-061 | Integration | T0 integrations must have `circuit_breaker=true` | ERROR |
| RULE-062 | Integration | `Broken` triggers P1 alert within 60s | ERROR |
| RULE-063 | Environment | `staging` must not use production secrets | ERROR |
| RULE-064 | Infrastructure | Production must be loopback-bound unless Nathan-approved | ERROR |
| RULE-065 | Database | Must have `backup_policy` | ERROR |
| RULE-066 | Database | T0 databases must have automated backup | ERROR |
| RULE-067 | Database | Schema changes require Change Control | ERROR |
| RULE-068 | Database | `Degraded` triggers P0 alert | ERROR |
| RULE-069 | Secret Metadata | Actual secrets never stored in this record | ERROR |
| RULE-070 | Agent | Financial agents must have `spend_cap_usd` | ERROR |
| RULE-071 | Agent | All agents must have `policy_ids[]` | ERROR |
| RULE-072 | Lifecycle State | Terminal states require explicit approval | ERROR |
| RULE-073 | Lifecycle State | State transitions must log actor and timestamp | ERROR |
| RULE-074 | Lifecycle State | Undocumented transitions are governance violations | ERROR |
| RULE-075 | Change Control | `Complete` requires `completion_evidence` | ERROR |
| RULE-076 | Schema Evolution | `backward_compatible=false` requires `migration_script_ref` | ERROR |
| RULE-077 | Migration State | `Blocked` state requires documented blockers | ERROR |

---

## SECTION 4: JSON SCHEMA — CRITICAL TYPES

### Portfolio (JSON Schema draft-07)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://openempire.local/schemas/v1/Portfolio",
  "title": "Portfolio",
  "type": "object",
  "required": ["id", "name", "owner", "status", "created_at", "updated_at",
               "mission_alignment", "programs", "ventures", "kpis", "capital_deployed_usd"],
  "properties": {
    "id":                    { "type": "string", "format": "uuid" },
    "name":                  { "type": "string", "maxLength": 200 },
    "owner":                 { "type": "string" },
    "status":                { "type": "string", "enum": ["Active", "Archived"] },
    "created_at":            { "type": "string", "format": "date-time" },
    "updated_at":            { "type": "string", "format": "date-time" },
    "mission_alignment":     { "type": "string", "minLength": 1 },
    "programs":              { "type": "array", "items": { "type": "string", "format": "uuid" } },
    "ventures":              { "type": "array", "items": { "type": "string", "format": "uuid" } },
    "kpis":                  { "type": "array", "items": { "type": "string", "format": "uuid" } },
    "capital_deployed_usd":  { "type": "number", "minimum": 0 }
  },
  "anyOf": [
    { "properties": { "programs": { "minItems": 1 } } },
    { "properties": { "ventures": { "minItems": 1 } } }
  ]
}
```

### Venture (JSON Schema draft-07)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://openempire.local/schemas/v1/Venture",
  "title": "Venture",
  "type": "object",
  "required": ["id", "name", "owner", "status", "created_at", "updated_at",
               "portfolio_id", "revenue_model", "capital_deployed_usd",
               "daily_spend_cap_usd", "programs", "p_and_l_ref"],
  "properties": {
    "id":                   { "type": "string", "format": "uuid" },
    "name":                 { "type": "string", "maxLength": 200 },
    "owner":                { "type": "string" },
    "status":               { "type": "string", "enum": ["Pre-Launch","Active","Scaling","On Hold","Winding Down","Closed"] },
    "created_at":           { "type": "string", "format": "date-time" },
    "updated_at":           { "type": "string", "format": "date-time" },
    "portfolio_id":         { "type": "string", "format": "uuid" },
    "revenue_model":        { "type": "string", "minLength": 1 },
    "capital_deployed_usd": { "type": "number", "minimum": 0 },
    "daily_spend_cap_usd":  { "type": "number", "minimum": 0 },
    "programs":             { "type": "array", "items": { "type": "string", "format": "uuid" } },
    "p_and_l_ref":          { "type": "string", "minLength": 1 }
  }
}
```

### Project (JSON Schema draft-07)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://openempire.local/schemas/v1/Project",
  "title": "Project",
  "type": "object",
  "required": ["id", "name", "owner", "status", "created_at", "updated_at",
               "program_id", "deliverables", "start_date", "end_date", "risk_level"],
  "properties": {
    "id":           { "type": "string", "format": "uuid" },
    "name":         { "type": "string", "maxLength": 200 },
    "owner":        { "type": "string" },
    "status":       { "type": "string", "enum": ["Planned","In Progress","Blocked","Complete","Cancelled"] },
    "created_at":   { "type": "string", "format": "date-time" },
    "updated_at":   { "type": "string", "format": "date-time" },
    "program_id":   { "type": "string", "format": "uuid" },
    "deliverables": { "type": "array", "items": { "type": "string" }, "minItems": 1 },
    "start_date":   { "type": "string", "format": "date-time" },
    "end_date":     { "type": "string", "format": "date-time" },
    "risk_level":   { "type": "string", "enum": ["P0","P1","P2","P3","P4"] }
  }
}
```

### Agent (JSON Schema draft-07)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://openempire.local/schemas/v1/Agent",
  "title": "Agent",
  "type": "object",
  "required": ["id", "name", "owner", "status", "created_at", "updated_at",
               "agent_type", "model_id", "tool_access", "policy_ids",
               "owner_role_id", "memory_scope"],
  "properties": {
    "id":             { "type": "string", "format": "uuid" },
    "name":           { "type": "string", "maxLength": 200 },
    "owner":          { "type": "string" },
    "status":         { "type": "string", "enum": ["Draft","Testing","Active","Suspended","Retired"] },
    "created_at":     { "type": "string", "format": "date-time" },
    "updated_at":     { "type": "string", "format": "date-time" },
    "agent_type":     { "type": "string", "enum": ["director","arb","trader","monitor","orchestrator","specialist","chief_of_staff"] },
    "model_id":       { "type": "string", "format": "uuid" },
    "tool_access":    { "type": "array", "items": { "type": "string" } },
    "policy_ids":     { "type": "array", "items": { "type": "string", "format": "uuid" }, "minItems": 1 },
    "owner_role_id":  { "type": "string", "format": "uuid" },
    "memory_scope":   { "type": "string" },
    "spend_cap_usd":  { "type": "number", "minimum": 0 }
  }
}
```

### Repository (JSON Schema draft-07)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://openempire.local/schemas/v1/Repository",
  "title": "Repository",
  "type": "object",
  "required": ["id", "name", "owner", "status", "created_at", "updated_at",
               "github_org", "github_repo", "visibility", "default_branch",
               "tier", "owner_role_id", "ci_status", "last_commit_at",
               "git_initialized", "remote_url"],
  "properties": {
    "id":              { "type": "string", "format": "uuid" },
    "name":            { "type": "string", "maxLength": 200 },
    "owner":           { "type": "string" },
    "status":          { "type": "string", "enum": ["Active","Archived","Deprecated"] },
    "created_at":      { "type": "string", "format": "date-time" },
    "updated_at":      { "type": "string", "format": "date-time" },
    "github_org":      { "type": "string" },
    "github_repo":     { "type": "string" },
    "visibility":      { "type": "string", "enum": ["private","public"] },
    "default_branch":  { "type": "string" },
    "tier":            { "type": "string", "enum": ["T0","T1","T2","T3"] },
    "owner_role_id":   { "type": "string", "format": "uuid" },
    "ci_status":       { "type": "string" },
    "last_commit_at":  { "type": "string", "format": "date-time" },
    "git_initialized": { "type": "boolean" },
    "remote_url":      { "type": "string" }
  },
  "if": { "properties": { "tier": { "enum": ["T0"] } } },
  "then": {
    "properties": { "git_initialized": { "const": true } },
    "required": ["remote_url"]
  }
}
```

---

## SECTION 5: SCHEMA REGISTRY INDEX

| Asset Type | Layer | Additional Fields | Key Enums |
|---|---|---|---|
| Portfolio | L1 | mission_alignment, programs[], ventures[], kpis[], capital_deployed_usd | status: Active, Archived |
| Program | L1 | portfolio_id, objectives[], projects[], capabilities[], start_date, target_end_date | status: Planned, Active, On Hold, Completed, Archived |
| Project | L1 | program_id, deliverables[], start_date, end_date, risk_level | status: Planned, In Progress, Blocked, Complete, Cancelled |
| Business Capability | L1 | description, maturity_level, enabling_assets[], programs[] | maturity: Emerging→Optimized |
| Venture | L1 | portfolio_id, revenue_model, capital_deployed_usd, daily_spend_cap_usd, programs[], p_and_l_ref | status: Pre-Launch→Closed |
| Executive KPI | L1 | target_value, current_value, unit, measurement_frequency, owner_asset_id, direction, evidence_state | direction: higher/lower_is_better |
| Business Outcome | L1 | description, target_date, success_criteria[], linked_kpis[], linked_programs[] | status: Targeted, Achieved, Missed, Superseded |
| Council | L2 | domain, members[], chair_role, escalation_path, policies[], meeting_cadence | status: Active, Suspended, Dissolved |
| Executive Role | L2 | title, domain, holder, council_id, authority_scope, escalation_target | holder: human, agent |
| Ownership Role | L2 | title, asset_type, asset_ids[], holder, executive_role_id | status: Active, Delegated, Vacant |
| Standard | L2 | version, scope, requirements[], issuing_council_id, effective_date, superseded_by | status: Draft→Superseded |
| Policy | L2 | version, statement, scope, exceptions[], enforcement_mechanism, issuing_council_id, effective_date | status: Draft→Superseded |
| Playbook | L2 | version, policy_ids[], steps[], prerequisites[], expected_outputs[], last_validated | status: Draft→Deprecated |
| Approval Type | L2 | authority_level, mechanism, timeout_seconds, escalation_on_timeout, applies_to[] | mechanism: telegram, openclaw_native, n8n, manual |
| Risk Level | L2 | id (P0–P4), description, response_sla_minutes, approval_required, escalation_path | id: P0–P4 |
| Lifecycle State | L2 | status, status_changed_at, status_changed_by | applied fields |
| Evidence State | L2 | evidence_state, evidence_source, evidence_timestamp | state: Verified, Asserted, Estimated, Unverified, Stale |
| Repository | L3 | github_org, github_repo, visibility, default_branch, tier, owner_role_id, ci_status, last_commit_at, git_initialized, remote_url | tier: T0–T3 |
| Package | L3 | version, repository_id, runtime, entry_point, dependencies[] | runtime: python, node, other |
| Library | L3 | version, package_id, module_path, public_api[] | status: Active, Deprecated, Superseded |
| Framework | L3 | version, runtime, purpose, consuming_assets[], upgrade_policy | status: Active, Deprecated, Upgrading |
| Model | L3 | provider_id, version, context_window, cost_per_1k_input_usd, cost_per_1k_output_usd, latency_class, use_cases[] | latency: real-time, batch |
| Model Provider | L3 | api_endpoint, auth_type, models[], billing_account, daily_cost_cap_usd | status: Active, Degraded, Unavailable |
| API | L3 | version, base_url, auth_type, endpoints[], rate_limits, breaking_change_policy | status: Active, Deprecated, Breaking-Change-Pending, Retired |
| Router | L3 | type, rules[], fallback_target | type: model/message/request/approval_router |
| Integration | L3 | external_system, api_id, auth_type, secret_metadata_id, data_flow_direction, error_handling, circuit_breaker | direction: inbound, outbound, bidirectional |
| Environment | L3 | type, host, services[], secrets_scope | type: development, staging, production, local |
| Infrastructure | L3 | type, host_identifier, os, cpu, ram_gb, network_posture | type: mac_mini, cloud_vps, container, managed_service |
| Database | L3 | engine, version, host, port, database_name, schemas[], owner_role_id, backup_policy | status: Active, Migrating, Degraded, Retired |
| Storage | L3 | type, root_path, retention_policy, owner_role_id, access_permissions, immutable | type: filesystem, s3, object_store |
| Secret Metadata | L3 | type, associated_system, environment, rotation_policy, last_rotated_at, expiry_at | type: api_key, private_key, oauth_token, webhook_secret |
| Runtime | L4 | environment_id, package_id, interpreter, pid, uptime_seconds, memory_mb | status: Running, Starting, Stopped, Crashed, Restarting |
| Service | L4 | pm2_id, port, tier, owner_role_id, health_check_url, restart_policy, last_restart_at | status: Planned→Retired |
| PM2 Process | L4 | id (numeric), script, args[], cwd, interpreter, env{}, restart_policy, cron_restart | status: Online, Stopped, Errored, Restarting |
| Workflow | L4 | trigger_type, steps[], success_criteria, owner_role_id, framework | framework: n8n, antfarm, openclaw_cron |
| Automation | L4 | trigger, script, cwd, environment_id, logging_target, retry_policy | status: Active, Paused, Failed, Deprecated |
| Agent | L4 | agent_type, model_id, tool_access[], policy_ids[], owner_role_id, memory_scope, spend_cap_usd | type: director, arb, trader, etc. |
| Agent Team | L4 | purpose, agents[], lead_agent_id, council_id, coordination_protocol, collective_spend_cap_usd | status: Active, Reorganizing, Disbanded |
| Dashboard | L4 | port, service_id, data_sources[], refresh_interval_seconds, access_control | status: Active, Degraded, Stopped |
| Knowledge Base | L4 | domain, format, root_path, curation_policy, last_updated, owner_role_id | format: markdown, json, jsonl, vector_db |
| Memory Store | L4 | type, root_path, retention_days, compression_schedule, owner_agent_id | type: active, compressed, archive, vector |
| Registry | L4 | scope, asset_types[], storage_format, root_path_or_table, last_sync_at, owner_role_id | format: json, jsonl, postgresql, markdown |
| Execution Role | L5 | title, scope, holder, ownership_role_id, task_types[] | status: Active, Delegated, Vacant |
| Operational Status | L5 | status, last_checked_at, check_method, incident_open, notes | status: OK, DEGRADED, STOPPED, ERRORED, RESTARTING, UNKNOWN |
| Integration Readiness | L5 | integration_id, auth_verified, endpoint_reachable, error_handling_tested, end_to_end_validated, last_validated_at, readiness_state, notes | state: Not Ready→Degraded |
| Business Criticality | L5 | criticality_tier, revenue_impact, mttr_target_minutes, rpo_target_minutes, notes | tier: Tier-0 to Tier-3 |
| Recovery Priority | L5 | priority_rank, asset_id, asset_type, rto_minutes, rpo_minutes, dependencies[], recovery_steps_ref | — |
| Relationship Type | L5 | source/target asset_id, asset_type, relationship_type, direction, strength | strength: required, optional, deprecated |
| Verification Method | L5 | type, automation_eligible, cadence, evidence_produced | type: api_call, log_check, etc. |
| Current State | L6 | asset_id, snapshot_timestamp, captured_by, evidence_state, configuration{}, operational_status, known_issues[], notes | evidence: Verified→Stale |
| Target State | L6 | asset_id, target_id, approved_by, approved_at, target_configuration{}, success_criteria[], target_date | status: Proposed→Superseded |
| Migration State | L6 | asset_id, migration_id, current_state_id, target_state_id, steps_completed[], steps_remaining[], blockers[], risk_level, rollback_plan | status: Not Started→Complete |
| Retirement State | L6 | asset_id, retirement_date, approved_by, superseded_by_id, archive_path, data_retention_policy | status: Planned Retirement→Archived |
| Supersession | L6 | predecessor/successor asset_id+type, effective_date, approved_by, reason, migration_state_id, notes | permanent record |
| Versioning | L6 | asset_id, version_scheme, current_version, previous_version, changelog_ref, version_history[] | scheme: semver, calver, git_sha, sequential |
| Change Control | L6 | change_title, asset_ids[], change_type, risk_level, approver_id, rollback_plan, scheduled_at, completion_evidence | type: config, code, schema, infrastructure, policy |
| Drift Detection | L6 | asset_id, detection_method, expected_state_ref, detected_at, drift_description, severity, resolution_ref | method: config_hash, process_check, api_probe, schema_diff |
| Schema Evolution | L6 | schema_id, current_version, proposed_change, backward_compatible, migration_script_ref, approved_by, effective_date | status: Proposed→Rejected |
