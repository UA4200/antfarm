# OPEN EMPIRE MASTER REGISTRY INDEX V1

**Version:** 1.0.0  
**Generated:** 2026-08-06T11:41:00-05:00  
**Generator:** Alusi Gate A Finalization Directive  
**Purpose:** Index of all Open Empire registries — not a duplicate registry. Each entry points to the canonical source of truth for that registry.  
**Owner:** Nathan (Sovereign Operator)

---

## PREAMBLE

This Master Registry Index is an index of registries. It does not duplicate any registry's content. For each registry it specifies: owner, canonical path, schema, source of truth, update mechanism, consumers, validation method, and lifecycle status.

All registries indexed here are subordinate to the governance baseline. Any registry entry that conflicts with the governance Taxonomy, Schema, or Ontology must be resolved in favor of governance.

---

## 1. ASSET REGISTRY

| Field | Value |
|---|---|
| **Registry Name** | Open Empire Asset Registry |
| **Owner** | Nathan (Sovereign Operator) / Alusi (Chief of Staff) |
| **Canonical Path** | `~/.openclaw/workspace/governance/` (governance) + `~/.openclaw/vault/` (operational instances) |
| **Schema** | OPEN_EMPIRE_SCHEMA_V1.md |
| **Source of Truth** | Canonical governance documents define asset types; individual OEPM manifests declare instances |
| **Update Mechanism** | New assets: create OEPM manifest → submit to registry → Nathan approval. Changes: Change Control process. |
| **Consumers** | Mission Control, Alusi governance layer, OEPM build pipeline |
| **Validation Method** | `python3 build/validate.py` — Schema conformance rules VR-SC0xx |
| **Lifecycle Status** | ACTIVE — V1.0.0 baseline |

---

## 2. REPOSITORY REGISTRY

| Field | Value |
|---|---|
| **Registry Name** | Open Empire Repository Registry |
| **Owner** | Nathan (Sovereign Operator) |
| **Canonical Path** | `~/.openclaw/workspace/AGENTS.md` (operational) / `UA4200/` GitHub org |
| **Schema** | OPEN_EMPIRE_ASSET_TAXONOMY_V1.md → Repository asset class |
| **Source of Truth** | GitHub org `UA4200` + AGENTS.md |
| **Update Mechanism** | New repos: deploy via `open-empire-github-deployment` skill; update AGENTS.md |
| **Consumers** | CI/CD pipelines, Alusi orchestrator, PMO |
| **Validation Method** | `gh repo list UA4200` + AGENTS.md cross-check |
| **Lifecycle Status** | ACTIVE — 6 repos deployed (alusi-core, open-empire-core, git-github, mission-control, antfarm, blco-pipeline) |

---

## 3. PACKAGE REGISTRY

| Field | Value |
|---|---|
| **Registry Name** | Open Empire Package Registry |
| **Owner** | Nathan (Sovereign Operator) |
| **Canonical Path** | `~/.openclaw/workspace/` (npm packages) + `~/.openclaw/venv/` (Python packages) |
| **Schema** | package.json (npm), requirements.txt / pyproject.toml (Python) |
| **Source of Truth** | Per-project package manifests |
| **Update Mechanism** | `npm install` / `pip install` within approved workflows |
| **Consumers** | All Node.js and Python processes |
| **Validation Method** | `npm audit` + `pip check` per project |
| **Lifecycle Status** | ACTIVE — managed per-project |

---

## 4. RUNTIME REGISTRY

| Field | Value |
|---|---|
| **Registry Name** | Open Empire Runtime Registry |
| **Owner** | Nathan (Sovereign Operator) / Alusi (Chief of Staff) |
| **Canonical Path** | `~/.openclaw/workspace/AGENTS.md` |
| **Schema** | PM2 ecosystem files + AGENTS.md table format |
| **Source of Truth** | Live PM2 process list (`pm2 jlist`) — AGENTS.md is a documentation mirror |
| **Update Mechanism** | PM2 ecosystem files updated via operator approval; AGENTS.md updated to reflect live state |
| **Consumers** | Trading Sentinel, Alusi orchestrator, Mission Control |
| **Validation Method** | `pm2 jlist` cross-check against AGENTS.md; OPEN_EMPIRE_PM2_TOPOLOGY_V1.json |
| **Lifecycle Status** | ACTIVE — 35 processes tracked. Note: AGENTS.md PM2 IDs partially stale; canonical source is live pm2 jlist. |

---

## 5. PM2 REGISTRY

| Field | Value |
|---|---|
| **Registry Name** | PM2 Process Registry |
| **Owner** | Nathan (Sovereign Operator) |
| **Canonical Path** | `~/.openclaw/workspace/OPEN_EMPIRE_PM2_TOPOLOGY_V1.json` (Gate A snapshot) |
| **Schema** | OPEN_EMPIRE_PM2_TOPOLOGY_V1.json schema |
| **Source of Truth** | `pm2 jlist` (live state); OPEN_EMPIRE_PM2_TOPOLOGY_V1.json (Gate A snapshot) |
| **Update Mechanism** | Refresh via Gate A or manual `pm2 jlist` capture; requires AGENTS.md sync |
| **Consumers** | Trading Sentinel, Alusi loop, mission-control |
| **Validation Method** | `pm2 list` vs registered processes; class assignments per OPEN_EMPIRE_PM2_CLASSIFICATION_REPORT.md |
| **Lifecycle Status** | ACTIVE — snapshot 2026-08-06 |

---

## 6. AGENT REGISTRY

| Field | Value |
|---|---|
| **Registry Name** | Open Empire Agent Registry |
| **Owner** | Nathan (Sovereign Operator) |
| **Canonical Path** | `~/.openclaw/workspace/AGENTS.md` + `~/.openclaw/workspace/agents/council_templates/` |
| **Schema** | AGENTS.md table format + OPEN_EMPIRE_ASSET_TAXONOMY_V1.md Agent asset class |
| **Source of Truth** | AGENTS.md (council templates + PM2 agents) |
| **Update Mechanism** | New agents: proof-of-concept before activation; approval required; AGENTS.md updated |
| **Consumers** | Alusi orchestrator, Mission Control, n8n |
| **Validation Method** | Cross-reference PM2 live list + AGENTS.md; verify script paths |
| **Lifecycle Status** | ACTIVE — 178 VoltAgent subagents + 59 council templates |

---

## 7. WORKFLOW REGISTRY

| Field | Value |
|---|---|
| **Registry Name** | Antfarm Workflow Registry |
| **Owner** | Nathan (Sovereign Operator) |
| **Canonical Path** | `~/.openclaw/workspace/antfarm/` |
| **Schema** | Antfarm workflow manifest (SQLite-backed) |
| **Source of Truth** | `node ~/.openclaw/workspace/antfarm/dist/cli/cli.js workflow status` |
| **Update Mechanism** | `node antfarm/dist/cli/cli.js workflow install <name>` |
| **Consumers** | Alusi orchestrator, session agents |
| **Validation Method** | `node antfarm/dist/cli/cli.js logs` |
| **Lifecycle Status** | ACTIVE — feature-dev, security-audit, bug-fix workflows installed |

---

## 8. DASHBOARD REGISTRY

| Field | Value |
|---|---|
| **Registry Name** | Open Empire Dashboard Registry |
| **Owner** | Nathan (Sovereign Operator) |
| **Canonical Path** | `~/.openclaw/workspace/AGENTS.md` (ports section) |
| **Schema** | Port assignment table |
| **Source of Truth** | Live port assignments confirmed by `lsof -i -P -n` |
| **Update Mechanism** | Port conflict prevention check before any new service |
| **Consumers** | Nathan direct access |
| **Validation Method** | `lsof -i -P -n | grep LISTEN` cross-check |
| **Lifecycle Status** | ACTIVE |
| **Current Assignments** | Mission Control: 3333 · OpenClaw Dashboard: 8080 · Open Empire Nexus: 4444 · Grafana: 3001 · n8n: 5678 · Ollama: 11434 · PostgreSQL: 5432 · Alusi Gateway: 8788 · OpenClaw Gateway: 8787 |

---

## 9. SERVICE REGISTRY

| Field | Value |
|---|---|
| **Registry Name** | Open Empire Service Registry |
| **Owner** | Nathan (Sovereign Operator) |
| **Canonical Path** | `~/.openclaw/workspace/AGENTS.md` (agents table) + `OPEN_EMPIRE_PM2_TOPOLOGY_V1.json` |
| **Schema** | PM2 process entries; OPEN_EMPIRE_ASSET_TAXONOMY_V1.md Service asset class |
| **Source of Truth** | PM2 live list |
| **Update Mechanism** | New service: proof-of-concept + approval; PM2 ecosystem file update |
| **Consumers** | Alusi, Mission Control, Trading Sentinel |
| **Validation Method** | `pm2 list` + health checks |
| **Lifecycle Status** | ACTIVE — 29 services online |

---

## 10. POLICY REGISTRY

| Field | Value |
|---|---|
| **Registry Name** | Open Empire Policy Registry |
| **Owner** | Nathan (Sovereign Operator) |
| **Canonical Path** | `~/.openclaw/workspace/governance/OPEN_EMPIRE_POLICY_ENGINE_V1.md` |
| **Schema** | POL-NNN ID format; Policy Engine structure |
| **Source of Truth** | OPEN_EMPIRE_POLICY_ENGINE_V1.md |
| **Update Mechanism** | Change Control via Governance Baseline versioning; Nathan approval required for new policies |
| **Consumers** | Alusi (all enforcement), ECL interpreter, all agents |
| **Validation Method** | `python3 build/validate.py` — VR-P0xx rules |
| **Lifecycle Status** | ACTIVE — 17 policies (POL-001 through POL-033) |

---

## 11. VALIDATION REGISTRY

| Field | Value |
|---|---|
| **Registry Name** | Open Empire Validation Registry |
| **Owner** | Nathan (Sovereign Operator) / Alusi |
| **Canonical Path** | `~/.openclaw/workspace/governance/OPEN_EMPIRE_VALIDATION_SUITE_V1.md` + `build/runs/` |
| **Schema** | VR-NNN rule format; validation_summary.json schema |
| **Source of Truth** | OPEN_EMPIRE_VALIDATION_SUITE_V1.md (rules); `build/runs/<timestamp>/` (evidence) |
| **Update Mechanism** | New rules added via Governance Baseline versioning |
| **Consumers** | Build pipeline, Gate A finalization, CI/CD |
| **Validation Method** | `python3 build/validate.py` — self-validating |
| **Lifecycle Status** | ACTIVE — 76 VR-NNN rules, 240 rule instances |

---

## 12. ADR REGISTRY

| Field | Value |
|---|---|
| **Registry Name** | Architectural Decision Record Registry |
| **Owner** | Nathan (Sovereign Operator) |
| **Canonical Path** | `~/.openclaw/workspace/governance/OPEN_EMPIRE_ADR_INDEX_V1.md` |
| **Schema** | ADR-NNN format; ADR template in document |
| **Source of Truth** | OPEN_EMPIRE_ADR_INDEX_V1.md |
| **Update Mechanism** | New ADRs: follow ADR template; add via Change Control; immutable once committed |
| **Consumers** | Nathan, Alusi, all governance processes |
| **Validation Method** | `python3 build/validate.py` — VR-A0xx rules |
| **Lifecycle Status** | ACTIVE — 10 ADRs (ADR-001 through ADR-010) |

---

## 13. SECRET METADATA REGISTRY

| Field | Value |
|---|---|
| **Registry Name** | Secret Metadata Registry |
| **Owner** | Nathan (Sovereign Operator) |
| **Canonical Path** | `~/.openclaw/secrets/.env` (secrets) — METADATA ONLY, never values |
| **Schema** | Key names and purpose documentation (no values stored in registry) |
| **Source of Truth** | `~/.openclaw/secrets/.env` (access controlled, not version controlled) |
| **Update Mechanism** | Manual update; Nathan-only access |
| **Consumers** | All PM2 processes via environment injection |
| **Validation Method** | `~/.openclaw/scripts/secrets_health.sh` — checks key presence without exposing values |
| **Lifecycle Status** | ACTIVE — Anthropic, Kalshi, Polymarket, Telegram, Discord credentials stored |
| **CRITICAL NOTE** | Secret values are NEVER stored in any registry, governance file, or version-controlled path |

---

## 14. BACKUP REGISTRY

| Field | Value |
|---|---|
| **Registry Name** | Backup Registry |
| **Owner** | Nathan (Sovereign Operator) |
| **Canonical Path** | `~/.openclaw/vault/` (primary) + external destination TBD |
| **Schema** | Backup manifest with file lists and checksums |
| **Source of Truth** | LaunchD + cron auto-capture (per AGENTS.md: "Auto-capture OK LaunchD+cron") |
| **Update Mechanism** | Automatic via LaunchD cron; manual on critical changes |
| **Consumers** | Disaster recovery procedures |
| **Validation Method** | Periodic backup restoration test (not yet scheduled — BLOCKER noted) |
| **Lifecycle Status** | ACTIVE (auto-capture) — formal backup validation schedule PENDING |

---

## 15. RECOVERY REGISTRY

| Field | Value |
|---|---|
| **Registry Name** | Recovery Registry |
| **Owner** | Nathan (Sovereign Operator) |
| **Canonical Path** | `~/.openclaw/workspace/governance/ROLLBACK_MANIFEST.json` (governance) + `OPEN_EMPIRE_BOOTSTRAP_SPECIFICATION_V1.md` (system recovery) |
| **Schema** | ROLLBACK_MANIFEST.json schema; Bootstrap Specification structure |
| **Source of Truth** | OPEN_EMPIRE_BOOTSTRAP_SPECIFICATION_V1.md for system recovery; ROLLBACK_MANIFEST.json for governance rollback |
| **Update Mechanism** | Update Bootstrap Spec on architecture changes; update Rollback Manifest on governance version changes |
| **Consumers** | Nathan, qualified engineers for disaster recovery |
| **Validation Method** | OPEN_EMPIRE_BOOTSTRAP_VALIDATION_V1.json (dry-run checks) |
| **Lifecycle Status** | ACTIVE — V1.0.0-RC1 |

---

## INDEX SUMMARY

| # | Registry | Status | Canonical Path |
|---|---|---|---|
| 1 | Asset Registry | ACTIVE | governance/ + vault/ |
| 2 | Repository Registry | ACTIVE | AGENTS.md + UA4200 GitHub |
| 3 | Package Registry | ACTIVE | per-project manifests |
| 4 | Runtime Registry | ACTIVE | AGENTS.md + pm2 jlist |
| 5 | PM2 Registry | ACTIVE | PM2_TOPOLOGY_V1.json |
| 6 | Agent Registry | ACTIVE | AGENTS.md + agents/ |
| 7 | Workflow Registry | ACTIVE | antfarm/ |
| 8 | Dashboard Registry | ACTIVE | AGENTS.md ports |
| 9 | Service Registry | ACTIVE | PM2 live list |
| 10 | Policy Registry | ACTIVE | POLICY_ENGINE_V1.md |
| 11 | Validation Registry | ACTIVE | VALIDATION_SUITE_V1.md + build/runs/ |
| 12 | ADR Registry | ACTIVE | ADR_INDEX_V1.md |
| 13 | Secret Metadata Registry | ACTIVE | secrets/.env (metadata only) |
| 14 | Backup Registry | ACTIVE | vault/ (auto-capture) |
| 15 | Recovery Registry | ACTIVE | ROLLBACK_MANIFEST.json + BOOTSTRAP_SPEC_V1.md |
