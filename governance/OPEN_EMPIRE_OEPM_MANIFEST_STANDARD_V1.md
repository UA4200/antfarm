# OPEN EMPIRE OEPM MANIFEST STANDARD V1

**Version:** 1.0.0
**Status:** Draft — Pending Validation
**Owner:** Nathan (Sovereign Operator)
**Source:** `~/.openclaw/workspace/governance/OPEN_EMPIRE_ASSET_TAXONOMY_V1.md` · AGENTS.MD operational context · `OPEN_EMPIRE_POLICY_ENGINE_V1.md`
**Materialization Date:** 2026-08-05
**Dependencies:** OPEN_EMPIRE_ASSET_TAXONOMY_V1.md · OPEN_EMPIRE_POLICY_ENGINE_V1.md · OPEN_EMPIRE_LIFECYCLE_STATE_MACHINE_V1.md (TODO_PENDING_APPROVAL — not yet materialized)
**Revision History:**
| Version | Date | Author | Change |
|---|---|---|---|
| 1.0.0 | 2026-08-05 | Alusi | Initial materialization under Governance Freeze Order 2026-08-05 |

---

## PREAMBLE

The OEPM (Open Empire Portfolio Management) Manifest Standard defines the format for declaring any repository, agent, service, or other governed asset as a registered member of the Open Empire portfolio.

A manifest is a machine-readable contract. It is not documentation — it is governance data. Every asset in Open Empire must have one. Every system consuming Open Empire data (Mission Control, PMO, OEPM governance layer) reads manifests, not documentation.

This Standard defines the manifest schema, validation rules, lifecycle, and registry format. It is the single source of truth for how assets are declared, registered, and governed in Open Empire.

---

## SECTION 1 — WHAT IS AN OEPM MANIFEST?

An OEPM manifest is a machine-readable declaration file placed at the root of any repository, agent directory, or service configuration that participates in Open Empire. It:

1. **Identifies** the asset with a canonical name, type, and unique ID
2. **Classifies** the asset according to the Taxonomy (layer, type, lifecycle state)
3. **Places** the asset in the portfolio hierarchy (Portfolio → Program → Project → Asset)
4. **Declares** the asset's runtime configuration (PM2 ID, port, cycle, environment)
5. **Binds** the asset to its governance obligations (applicable policies, spend caps, approval requirements)
6. **Describes** the asset's dependencies and health characteristics
7. **Registers** the asset in the central OEPM registry

An asset without an OEPM manifest is an unregistered asset. Unregistered assets are governance violations under POL-031 (No Scope Expansion) because they cannot be governed, audited, or policy-enforced.

### 1.1 Manifest File Naming

**Primary format:** `oepm.json`
**Alternative format:** `oepm.yaml` (acceptable when JSON tooling is unavailable; must be semantically equivalent)
**Location:** Root of the asset's canonical directory

### 1.2 Scope of Coverage

Every asset of the following Taxonomy types must have an OEPM manifest:
- Agent
- Service
- Repository (Tier-0 and Tier-1)
- Database
- Workflow (when deployed as a standalone governed asset)
- Automation (when deployed as a standalone governed asset)

The following Taxonomy types may use a manifest but are not required to:
- Library (typically covered by their parent Package's manifest)
- Package (covered if independently deployed)
- Knowledge Base
- Memory Store

Governance documents (Policies, Playbooks, Standards, Taxonomy) carry their own header format per the Materialization Standard and do not use `oepm.json` files. However, they ARE registered in the central asset registry as governance assets.

---

## SECTION 2 — MANIFEST FILE FORMAT

### 2.1 Full Manifest Schema (JSON)

```json
{
  "$schema": "https://openempire.local/schemas/oepm/v1.0.0",
  "oepm_version": "1.0.0",

  "asset": {
    "id": "<uuid-v4>",
    "name": "<canonical name — matches AGENTS.md entry or governance document title>",
    "type": "<Taxonomy Canonical Name — must be exact match from OPEN_EMPIRE_ASSET_TAXONOMY_V1.md>",
    "version": "<semver — e.g. 1.0.0>",
    "status": "<valid Lifecycle State for this asset type>",
    "layer": "<L1|L2|L3|L4|L5|L6 — taxonomy layer of this asset type>",
    "owner": "Nathan",
    "created_at": "<iso8601>",
    "updated_at": "<iso8601>",
    "canonical_path": "<absolute filesystem path on production host>"
  },

  "portfolio_placement": {
    "portfolio_id": "<uuid of the containing Portfolio manifest, or null if top-level>",
    "program_id": "<uuid of the containing Program manifest, or null>",
    "venture_id": "<uuid of the containing Venture manifest, or null>",
    "project_id": "<uuid of the producing Project manifest, or null>"
  },

  "runtime": {
    "pm2_id": "<integer PM2 process ID, or null if not PM2-managed>",
    "pm2_name": "<PM2 process name string, or null>",
    "port": "<integer port number, or null if no port>",
    "cycle_seconds": "<integer cycle duration in seconds, or null if continuous>",
    "environment": "<production|staging|development>"
  },

  "governance": {
    "policies": ["<POL-NNN>", "..."],
    "daily_spend_cap_usd": "<number or null — mandatory for financial agents>",
    "requires_approval_for": ["<approval_category>", "..."],
    "circuit_breaker": "<boolean — true if this asset has a circuit breaker per policy>"
  },

  "dependencies": [
    {
      "asset_name": "<canonical name of dependency>",
      "asset_type": "<Taxonomy Canonical Name>",
      "canonical_path": "<absolute path or null for external services>",
      "relationship": "<DEPENDS_ON|CONSUMES|PRODUCES>"
    }
  ],

  "health": {
    "status_file": "<absolute path to status output file, or null>",
    "log_path": "<absolute path to primary log file or directory>",
    "heartbeat_url": "<url for health check endpoint, or null>",
    "recovery_procedure": "<absolute path to runbook file, or null>"
  },

  "registry": {
    "registered_at": "<iso8601 — when this manifest was first added to the registry>",
    "last_synced_at": "<iso8601 — when the registry last confirmed this manifest is current>",
    "registry_path": "~/.openclaw/workspace/governance/registry/"
  }
}
```

### 2.2 Field Definitions

#### `asset` block

| Field | Type | Required | Notes |
|---|---|---|---|
| `id` | UUID v4 string | Required | Stable across the asset's lifetime. Never reused. |
| `name` | string | Required | Canonical name. Must match AGENTS.md or governance document title exactly. |
| `type` | string | Required | Must be an exact Canonical Name from OPEN_EMPIRE_ASSET_TAXONOMY_V1.md. |
| `version` | semver string | Required | Asset code/config version. Not the manifest schema version. |
| `status` | string | Required | Must be a valid Lifecycle State for this asset type per Taxonomy. |
| `layer` | string | Required | L1–L6, corresponding to Taxonomy layer of the asset type. |
| `owner` | string | Required | Must be "Nathan" for all assets (Sovereign Operator). Delegated stewards are in `governance` layer. |
| `created_at` | ISO 8601 | Required | When the asset was first created/deployed. |
| `updated_at` | ISO 8601 | Required | When the manifest was last updated. |
| `canonical_path` | string | Required | Absolute filesystem path on the production host (Ugos-Mac-mini). |

#### `portfolio_placement` block

| Field | Type | Required | Notes |
|---|---|---|---|
| `portfolio_id` | UUID string or null | Required | References the Portfolio this asset ultimately belongs to. |
| `program_id` | UUID string or null | Optional | References the Program if applicable. |
| `venture_id` | UUID string or null | Optional | References the Venture if this asset is Venture-level (e.g., trading agents). |
| `project_id` | UUID string or null | Optional | References the producing Project if the asset was delivered by a defined Project. |

#### `runtime` block

| Field | Type | Required | Notes |
|---|---|---|---|
| `pm2_id` | integer or null | Required | Official PM2 process ID from current ecosystem. null if not PM2-managed. |
| `pm2_name` | string or null | Required | PM2 process name. Must match actual PM2 name exactly. |
| `port` | integer or null | Optional | Listening port. null if process has no listening port. |
| `cycle_seconds` | integer or null | Optional | Cycle duration for cron/interval processes. null for continuous processes. |
| `environment` | string | Required | One of: `production`, `staging`, `development`. |

#### `governance` block

| Field | Type | Required | Notes |
|---|---|---|---|
| `policies` | array of strings | Required | List of POL-NNN IDs from OPEN_EMPIRE_POLICY_ENGINE_V1.md. Must match Enforcement Matrix. |
| `daily_spend_cap_usd` | number or null | Required for financial agents | Matches the env var value. null for non-financial assets. |
| `requires_approval_for` | array of strings | Required | Categories requiring approval: `external_communication`, `financial_operations`, `deployment`. |
| `circuit_breaker` | boolean | Required | true if the asset implements a circuit breaker per POL-010 or POL-012. |

#### `dependencies` array

Each dependency entry:

| Field | Type | Required | Notes |
|---|---|---|---|
| `asset_name` | string | Required | Canonical name of the dependency. |
| `asset_type` | string | Required | Taxonomy Canonical Name of the dependency. |
| `canonical_path` | string or null | Required | Absolute path, or null for external services (Kalshi API, Telegram API, etc.). |
| `relationship` | string | Required | One of: `DEPENDS_ON`, `CONSUMES`, `PRODUCES`. |

#### `health` block

| Field | Type | Required | Notes |
|---|---|---|---|
| `status_file` | string or null | Optional | Path to a file the process writes with its current status. |
| `log_path` | string | Required | Where this asset's logs are written. |
| `heartbeat_url` | string or null | Optional | HTTP endpoint for liveness check, if any. |
| `recovery_procedure` | string or null | Optional | Path to a runbook describing recovery steps. |

#### `registry` block

| Field | Type | Required | Notes |
|---|---|---|---|
| `registered_at` | ISO 8601 | Required | Set once at initial registration. Never updated. |
| `last_synced_at` | ISO 8601 | Required | Updated each time the registry sync process confirms this manifest. |
| `registry_path` | string | Required | Always: `~/.openclaw/workspace/governance/registry/`. |

---

## SECTION 3 — MANIFEST VALIDATION RULES

All OEPM manifests must pass the following validation checks before being accepted into the registry:

### 3.1 Schema Validation
- `$schema` must reference `https://openempire.local/schemas/oepm/v1.0.0`
- All required fields must be present and non-null (unless explicitly nullable)
- Field types must match the schema definitions

### 3.2 Taxonomy Compliance
- `asset.type` must be an exact Canonical Name from OPEN_EMPIRE_ASSET_TAXONOMY_V1.md
- `asset.status` must be a valid Lifecycle State for the given `asset.type` per the Taxonomy's Lifecycle Applicability field
- `asset.layer` must match the Parent Layer of the asset type in the Taxonomy

### 3.3 Portfolio Integrity
- `portfolio_placement.portfolio_id` must reference an existing Portfolio manifest in the registry
- If `venture_id` is set, the referenced Venture manifest must exist in the registry
- If `program_id` is set, the referenced Program manifest must exist in the registry

### 3.4 Policy Compliance
- Every `governance.policies` entry must reference a valid POL-NNN from OPEN_EMPIRE_POLICY_ENGINE_V1.md
- Policies listed must include at minimum all policies in the agent's row of the Policy Enforcement Matrix
- Financial agents (`asset.type = Agent` with non-null `daily_spend_cap_usd`) must include POL-001 and POL-002

### 3.5 Semver Compliance
- `asset.version` must be valid semantic versioning (major.minor.patch)

### 3.6 Path Validity
- `asset.canonical_path` must be an absolute filesystem path (begins with `/` or `~`)
- `health.log_path` must be an absolute filesystem path

### 3.7 Runtime Integrity
- If `runtime.pm2_id` is set, it must match the known PM2 process registry (cross-referenced against AGENTS.md)
- `runtime.environment` must be one of the four canonical Environment types from the Taxonomy

### 3.8 Validation Failure Behavior
A manifest failing any validation rule must not be added to the registry. The validation failure is logged. A Telegram alert is sent with the failing manifest name and failed rule. The asset is flagged as `unregistered_governance_violation` until the manifest is corrected and re-submitted.

---

## SECTION 4 — MANIFEST REGISTRY

### 4.1 Registry Location

All OEPM manifests register into the central registry at:

```
~/.openclaw/workspace/governance/registry/
```

### 4.2 Registry Index File

The registry maintains a flat JSON index file:

**Path:** `~/.openclaw/workspace/governance/registry/asset_registry.json`

**Format:**
```json
{
  "registry_version": "1.0.0",
  "last_updated": "<iso8601>",
  "total_assets": "<integer>",
  "assets": [
    {
      "id": "<uuid>",
      "name": "<canonical name>",
      "type": "<Taxonomy Canonical Name>",
      "status": "<Lifecycle State>",
      "canonical_path": "<absolute path>",
      "manifest_path": "<absolute path to oepm.json>",
      "registered_at": "<iso8601>",
      "last_synced_at": "<iso8601>",
      "validation_status": "valid | invalid | pending",
      "pm2_id": "<integer or null>"
    }
  ]
}
```

### 4.3 Individual Manifest Storage

In addition to the index, the registry stores a copy of each validated manifest:

```
~/.openclaw/workspace/governance/registry/manifests/<asset-id>.json
```

This ensures the registry has a canonical copy independent of whether the source directory is accessible.

### 4.4 Registry Integrity

- The registry index is append-only for new registrations
- Status updates to existing entries are versioned (old entry preserved, new entry with updated timestamp)
- Registry files are immutable records — deletion requires P0 Nathan approval
- TODO_PENDING_APPROVAL: Automated registry sync process schedule

---

## SECTION 5 — MANIFEST LIFECYCLE

### 5.1 Creation

When a new asset is created:
1. Generate a UUID v4 for `asset.id`
2. Populate all required fields from the asset's definition in AGENTS.md and Taxonomy
3. Set `asset.status` to the appropriate initial Lifecycle State for the asset type
4. Set `registry.registered_at` to the current timestamp
5. Place `oepm.json` at the root of the asset's canonical directory

### 5.2 Registration

After manifest creation:
1. Run manifest validation (Section 3)
2. If validation passes: add entry to `asset_registry.json`, store copy in `registry/manifests/`
3. If validation fails: log failure, alert Nathan, do not register until corrected
4. Set `registry.last_synced_at` to registration timestamp

### 5.3 Validation in Build Pipeline

TODO_PENDING_APPROVAL — Build pipeline not yet formalized. When formalized:
- All manifests in the governance registry are validated on each pipeline run
- Manifests that fail re-validation after a code change → alert, halt deployment
- Kelly.py hash verification is part of manifest validation for cashclaw_director

### 5.4 Update (After Baseline)

After Governance Baseline V1.0.0:
- Manifest updates require Change Control (per POL-030)
- Exception: `asset.status` changes from lifecycle transitions are allowed with PM2 restart evidence
- Exception: `runtime.pm2_id` updates from authorized redeployments are allowed
- All other field changes require Change Control proposal, Nathan approval, and version increment

### 5.5 Retirement

When an asset is retired:
1. Set `asset.status` to `Retired`, `Archived`, `Deprecated`, or `Closed` (per asset type's valid states)
2. Update `asset.updated_at`
3. Keep `oepm.json` in place — retirement does not delete the manifest
4. Update registry entry status to `retired`
5. Registry copy preserved permanently as immutable record

---

## SECTION 6 — EXAMPLE MANIFESTS

### Example 1: cashclaw_director (PM2 id=38, Trading Agent)

```json
{
  "$schema": "https://openempire.local/schemas/oepm/v1.0.0",
  "oepm_version": "1.0.0",

  "asset": {
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "name": "cashclaw_director",
    "type": "Agent",
    "version": "2.0.0",
    "status": "Active",
    "layer": "L4",
    "owner": "Nathan",
    "created_at": "2026-07-30T00:00:00-05:00",
    "updated_at": "2026-08-02T00:00:00-05:00",
    "canonical_path": "/Users/NeoOC/.openclaw/trading"
  },

  "portfolio_placement": {
    "portfolio_id": "TODO_PENDING_APPROVAL",
    "program_id": "TODO_PENDING_APPROVAL",
    "venture_id": "TODO_PENDING_APPROVAL",
    "project_id": "TODO_PENDING_APPROVAL"
  },

  "runtime": {
    "pm2_id": 38,
    "pm2_name": "cashclaw_director",
    "port": null,
    "cycle_seconds": 300,
    "environment": "production"
  },

  "governance": {
    "policies": [
      "POL-001",
      "POL-002",
      "POL-010",
      "POL-011",
      "POL-012",
      "POL-013",
      "POL-014",
      "POL-015",
      "POL-031",
      "POL-032"
    ],
    "daily_spend_cap_usd": 10,
    "requires_approval_for": ["financial_operations"],
    "circuit_breaker": true
  },

  "dependencies": [
    {
      "asset_name": "trading.shared.kelly",
      "asset_type": "Library",
      "canonical_path": "/Users/NeoOC/.openclaw/trading/trading/shared/kelly.py",
      "relationship": "DEPENDS_ON"
    },
    {
      "asset_name": "trading.shared.signals",
      "asset_type": "Library",
      "canonical_path": "/Users/NeoOC/.openclaw/trading/trading/shared/signals.py",
      "relationship": "DEPENDS_ON"
    },
    {
      "asset_name": "Kalshi V2 API",
      "asset_type": "API",
      "canonical_path": null,
      "relationship": "CONSUMES"
    },
    {
      "asset_name": "claude-haiku-4-5",
      "asset_type": "Model",
      "canonical_path": null,
      "relationship": "CONSUMES"
    },
    {
      "asset_name": "clawdb",
      "asset_type": "Database",
      "canonical_path": "/Users/NeoOC/.openclaw/trading/data",
      "relationship": "PRODUCES"
    },
    {
      "asset_name": "Telegram Integration",
      "asset_type": "Integration",
      "canonical_path": null,
      "relationship": "CONSUMES"
    }
  ],

  "health": {
    "status_file": null,
    "log_path": "/Users/NeoOC/.openclaw/trading/data/trades.jsonl",
    "heartbeat_url": null,
    "recovery_procedure": null
  },

  "registry": {
    "registered_at": "2026-08-05T00:00:00-05:00",
    "last_synced_at": "2026-08-05T00:00:00-05:00",
    "registry_path": "~/.openclaw/workspace/governance/registry/"
  }
}
```

---

### Example 2: OPEN_EMPIRE_ASSET_TAXONOMY_V1.md (Governance Document)

```json
{
  "$schema": "https://openempire.local/schemas/oepm/v1.0.0",
  "oepm_version": "1.0.0",

  "asset": {
    "id": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
    "name": "OPEN_EMPIRE_ASSET_TAXONOMY_V1",
    "type": "Standard",
    "version": "1.0.0",
    "status": "Active",
    "layer": "L2",
    "owner": "Nathan",
    "created_at": "2026-08-04T00:00:00-05:00",
    "updated_at": "2026-08-04T00:00:00-05:00",
    "canonical_path": "/Users/NeoOC/.openclaw/workspace/governance/OPEN_EMPIRE_ASSET_TAXONOMY_V1.md"
  },

  "portfolio_placement": {
    "portfolio_id": "TODO_PENDING_APPROVAL",
    "program_id": "TODO_PENDING_APPROVAL",
    "venture_id": null,
    "project_id": "TODO_PENDING_APPROVAL"
  },

  "runtime": {
    "pm2_id": null,
    "pm2_name": null,
    "port": null,
    "cycle_seconds": null,
    "environment": "production"
  },

  "governance": {
    "policies": ["POL-030"],
    "daily_spend_cap_usd": null,
    "requires_approval_for": ["deployment"],
    "circuit_breaker": false
  },

  "dependencies": [],

  "health": {
    "status_file": null,
    "log_path": "/Users/NeoOC/.openclaw/workspace/governance/",
    "heartbeat_url": null,
    "recovery_procedure": null
  },

  "registry": {
    "registered_at": "2026-08-05T00:00:00-05:00",
    "last_synced_at": "2026-08-05T00:00:00-05:00",
    "registry_path": "~/.openclaw/workspace/governance/registry/"
  }
}
```

---

### Example 3: clawdb (PostgreSQL Service, PM2 id=43)

```json
{
  "$schema": "https://openempire.local/schemas/oepm/v1.0.0",
  "oepm_version": "1.0.0",

  "asset": {
    "id": "c3d4e5f6-a7b8-9012-cdef-123456789012",
    "name": "clawdb",
    "type": "Database",
    "version": "18.3.0",
    "status": "Active",
    "layer": "L3",
    "owner": "Nathan",
    "created_at": "2026-07-30T00:00:00-05:00",
    "updated_at": "2026-07-30T00:00:00-05:00",
    "canonical_path": "/Users/NeoOC/.openclaw/clawdb"
  },

  "portfolio_placement": {
    "portfolio_id": "TODO_PENDING_APPROVAL",
    "program_id": null,
    "venture_id": null,
    "project_id": "TODO_PENDING_APPROVAL"
  },

  "runtime": {
    "pm2_id": 43,
    "pm2_name": "clawdb",
    "port": 5432,
    "cycle_seconds": null,
    "environment": "production"
  },

  "governance": {
    "policies": ["POL-010", "POL-011", "POL-031"],
    "daily_spend_cap_usd": null,
    "requires_approval_for": ["deployment"],
    "circuit_breaker": false
  },

  "dependencies": [
    {
      "asset_name": "Ugos-Mac-mini",
      "asset_type": "Infrastructure",
      "canonical_path": "/Users/NeoOC",
      "relationship": "DEPENDS_ON"
    }
  ],

  "health": {
    "status_file": null,
    "log_path": "/Users/NeoOC/.openclaw/logs/clawdb/",
    "heartbeat_url": null,
    "recovery_procedure": null
  },

  "registry": {
    "registered_at": "2026-08-05T00:00:00-05:00",
    "last_synced_at": "2026-08-05T00:00:00-05:00",
    "registry_path": "~/.openclaw/workspace/governance/registry/"
  }
}
```

---

## APPENDIX A — ASSET TYPE TO LAYER MAPPING

Quick reference for `asset.layer` values (derived from Taxonomy):

| Taxonomy Layer | Layer Code | Asset Types |
|---|---|---|
| Business | L1 | Portfolio · Program · Project · Business Capability · Venture · Executive KPI · Business Outcome |
| Governance | L2 | Council · Executive Role · Ownership Role · Standard · Policy · Playbook · Approval Type · Risk Level · Lifecycle State · Evidence State |
| Engineering | L3 | Repository · Package · Library · Framework · Model · Model Provider · API · Router · Integration · Environment · Infrastructure · Database · Storage · Secret Metadata |
| Operations | L4 | Runtime · Service · PM2 Process · Workflow · Automation · Agent · Agent Team · Dashboard · Knowledge Base · Memory Store · Registry |
| Execution | L5 | Execution Role · Operational Status · Integration Readiness · Business Criticality · Recovery Priority · Relationship Type · Verification Method |
| Evolution | L6 | Current State · Target State · Migration State · Retirement State · Supersession · Versioning · Change Control · Drift Detection · Schema Evolution |

---

## APPENDIX B — INITIAL LIFECYCLE STATE BY ASSET TYPE

| Asset Type | Initial State on First Deployment |
|---|---|
| Agent | `Active` (if deployed and running) or `Draft` (if in development) |
| Service | `Active` (if deployed) or `Planned` (if not yet deployed) |
| Database | `Active` (if running) |
| Repository | `Active` |
| Standard / Policy / Playbook | `Draft` (until validated and approved) |
| Venture | `Active` (if live) or `Pre-Launch` (if not yet revenue-generating) |

---

## APPENDIX C — MANIFEST CREATION CHECKLIST

Before submitting an OEPM manifest for registration:

- [ ] `asset.id` is a freshly generated UUID v4 (not reused from another asset)
- [ ] `asset.type` is an exact match to a Canonical Name in the Taxonomy
- [ ] `asset.status` is valid for this asset type
- [ ] `asset.canonical_path` is an absolute path verified to exist on Ugos-Mac-mini
- [ ] `portfolio_placement.portfolio_id` references an existing Portfolio (or is marked TODO_PENDING_APPROVAL if Portfolio UUIDs not yet assigned)
- [ ] `runtime.pm2_id` matches actual PM2 process list (or is null if not PM2-managed)
- [ ] `governance.policies` matches the Policy Enforcement Matrix in OPEN_EMPIRE_POLICY_ENGINE_V1.md
- [ ] `governance.daily_spend_cap_usd` is populated for all financial agents
- [ ] `health.log_path` is a valid, existing log path
- [ ] `registry.registered_at` is set to current timestamp
- [ ] Manifest passes all Section 3 validation rules

---

*OPEN EMPIRE OEPM MANIFEST STANDARD V1.0.0 — Materialized 2026-08-05 — Alusi, Chief of Staff*
*Under Governance Freeze Order 2026-08-05. No modifications without Change Control after Baseline.*
