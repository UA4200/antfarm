# OPEN EMPIRE DEPENDENCY MAP V1

**Version:** 1.0.0
**Status:** Draft — Pending Validation
**Owner:** Nathan (Sovereign Operator)
**Source:** All 12 canonical governance documents in `~/.openclaw/workspace/governance/`
**Materialization Date:** 2026-08-05
**Dependencies:** All other 11 governance documents (this document is derived from them)
**Revision History:**

| Version | Date | Author | Change |
|---|---|---|---|
| 1.0.0 | 2026-08-05 | Alusi | Initial materialization under Governance Freeze Order 2026-08-05 |

---

## PREAMBLE

This Dependency Map defines the directed dependency graph for all 12 canonical governance documents of Governance Baseline V1.0.0. It governs the order in which documents must be read, validated, and updated. It identifies which documents are upstream (must exist before dependents) and which are downstream (may only be updated after upstream documents are stable).

**Rule:** A document cannot be considered valid if any of its upstream dependencies have a `Status` of `failing` or `not_validated`.

---

## SECTION 1: DOCUMENT REGISTRY

| ID | Document | Filename | Size | Materialization Date |
|---|---|---|---|---|
| GOV-01 | Constitution | OPEN_EMPIRE_CONSTITUTION_V1.md | ~14KB | 2026-08-05 |
| GOV-02 | Asset Taxonomy | OPEN_EMPIRE_ASSET_TAXONOMY_V1.md | ~115KB | 2026-08-04 |
| GOV-03 | Ontology | OPEN_EMPIRE_ONTOLOGY_V1.md | ~60KB | 2026-08-05 |
| GOV-04 | Schema | OPEN_EMPIRE_SCHEMA_V1.md | ~56KB | 2026-08-05 |
| GOV-05 | Glossary | OPEN_EMPIRE_GLOSSARY_V1.md | ~25KB | 2026-08-05 |
| GOV-06 | ADR Index | OPEN_EMPIRE_ADR_INDEX_V1.md | ~23KB | 2026-08-05 |
| GOV-07 | Lifecycle State Machine | OPEN_EMPIRE_LIFECYCLE_STATE_MACHINE_V1.md | ~87KB | 2026-08-05 |
| GOV-08 | Policy Engine | OPEN_EMPIRE_POLICY_ENGINE_V1.md | ~20KB | 2026-08-05 |
| GOV-09 | Executive Command Language | OPEN_EMPIRE_EXECUTIVE_COMMAND_LANGUAGE_V1.md | ~16KB | 2026-08-05 |
| GOV-10 | OEPM Manifest Standard | OPEN_EMPIRE_OEPM_MANIFEST_STANDARD_V1.md | ~24KB | 2026-08-05 |
| GOV-11 | Dependency Map | OPEN_EMPIRE_DEPENDENCY_MAP_V1.md | this | 2026-08-05 |
| GOV-12 | Validation Suite | OPEN_EMPIRE_VALIDATION_SUITE_V1.md | ~TBD | 2026-08-05 |

---

## SECTION 2: DEPENDENCY MATRIX

A `✅` indicates GOV-Row DEPENDS ON GOV-Col. Read row → depends on column.

| | GOV-01 | GOV-02 | GOV-03 | GOV-04 | GOV-05 | GOV-06 | GOV-07 | GOV-08 | GOV-09 | GOV-10 | GOV-11 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **GOV-01 Constitution** | — | — | — | — | — | — | — | — | — | — | — |
| **GOV-02 Taxonomy** | ✅ | — | — | — | — | — | — | — | — | — | — |
| **GOV-03 Ontology** | — | ✅ | — | — | — | — | — | — | — | — | — |
| **GOV-04 Schema** | — | ✅ | ✅ | — | — | — | — | — | — | — | — |
| **GOV-05 Glossary** | — | ✅ | — | — | — | — | — | — | — | — | — |
| **GOV-06 ADR Index** | ✅ | — | — | — | — | — | — | — | — | — | — |
| **GOV-07 Lifecycle SM** | — | ✅ | — | — | — | — | — | — | — | — | — |
| **GOV-08 Policy Engine** | ✅ | ✅ | — | ✅ | — | — | ✅ | — | — | — | — |
| **GOV-09 ECL** | ✅ | — | — | — | — | — | — | ✅ | — | — | — |
| **GOV-10 OEPM Manifest** | — | ✅ | — | ✅ | — | — | ✅ | ✅ | — | — | — |
| **GOV-11 Dep Map** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | — |
| **GOV-12 Val Suite** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## SECTION 3: DIRECTED DEPENDENCY GRAPH

```
                     ┌─────────────────────────────────┐
                     │     GOV-02: ASSET TAXONOMY       │
                     │     (ROOT — no dependencies)     │
                     └──────────────┬──────────────────┘
                                    │ DEFINES ALL TERMS
          ┌─────────────────────────┼──────────────────────────────┐
          │                         │                              │
          ▼                         ▼                              ▼
┌──────────────────┐    ┌──────────────────────┐    ┌──────────────────────────┐
│  GOV-03: ONTOLOGY│    │ GOV-05: GLOSSARY      │    │  GOV-07: LIFECYCLE SM    │
│  (relationships) │    │ (term extraction)     │    │  (state transitions)     │
└────────┬─────────┘    └──────────────────────┘    └──────────┬───────────────┘
         │                                                       │
         ▼                                                       │
┌──────────────────┐                                            │
│  GOV-04: SCHEMA  │◄───────────────────────────────────────────┘
│  (field defs)    │    (uses lifecycle states as enum values)
└────────┬─────────┘
         │
         │         ┌──────────────────────────────────┐
         │         │       GOV-01: CONSTITUTION        │
         │         │       (sovereign law — no deps)   │
         │         └──────────────┬───────────────────┘
         │                        │
         │              ┌─────────┤
         │              │         │
         │              ▼         ▼
         │    ┌──────────────┐  ┌──────────────────────┐
         │    │ GOV-06: ADR  │  │  GOV-08: POLICY ENGINE│
         │◄───┤    INDEX     │  │  (depends: 01,02,04,07)│
         │    └──────────────┘  └──────────┬────────────┘
         │                                  │
         │                        ┌─────────┤
         │                        │         │
         │                        ▼         ▼
         │              ┌──────────────┐  ┌──────────────────────┐
         │              │  GOV-09: ECL │  │ GOV-10: OEPM MANIFEST│
         │              │  (01 + 08)   │  │ (02, 04, 07, 08)     │
         │              └──────────────┘  └──────────────────────┘
         │
         └──────────────────────────────────────────────┐
                                                         ▼
                                              ┌────────────────────────┐
                                              │  GOV-11: DEPENDENCY MAP │
                                              │  (depends on ALL above) │
                                              └──────────┬─────────────┘
                                                         │
                                                         ▼
                                              ┌────────────────────────┐
                                              │ GOV-12: VALIDATION SUITE│
                                              │  (validates ALL above)  │
                                              └────────────────────────┘
```

---

## SECTION 4: TOPOLOGICAL BUILD ORDER

The canonical order in which governance documents must be validated and released:

| Order | Document ID | Document Name | Can Start After |
|---|---|---|---|
| 1 | GOV-02 | Asset Taxonomy | — (root, no deps) |
| 2 | GOV-01 | Constitution | — (root, no deps; parallel with GOV-02) |
| 3 | GOV-03 | Ontology | GOV-02 complete |
| 4 | GOV-05 | Glossary | GOV-02 complete (parallel with GOV-03) |
| 5 | GOV-07 | Lifecycle State Machine | GOV-02 complete (parallel with GOV-03, GOV-05) |
| 6 | GOV-06 | ADR Index | GOV-01 complete (parallel with GOV-03, GOV-05, GOV-07) |
| 7 | GOV-04 | Schema | GOV-02 ✅ + GOV-03 ✅ |
| 8 | GOV-08 | Policy Engine | GOV-01 ✅ + GOV-02 ✅ + GOV-04 ✅ + GOV-07 ✅ |
| 9 | GOV-09 | Executive Command Language | GOV-01 ✅ + GOV-08 ✅ |
| 10 | GOV-10 | OEPM Manifest Standard | GOV-02 ✅ + GOV-04 ✅ + GOV-07 ✅ + GOV-08 ✅ |
| 11 | GOV-11 | Dependency Map | All GOV-01 through GOV-10 ✅ |
| 12 | GOV-12 | Validation Suite | All GOV-01 through GOV-11 ✅ |

**Parallel execution opportunities:**
- Wave 1 (no deps): GOV-01 (Constitution) + GOV-02 (Taxonomy) — note: Taxonomy already existed
- Wave 2 (after GOV-02): GOV-03 + GOV-05 + GOV-07 + GOV-06 all parallel
- Wave 3 (after GOV-03): GOV-04
- Wave 4 (after GOV-04): GOV-08
- Wave 5 (after GOV-08): GOV-09 + GOV-10 parallel
- Wave 6 (after all): GOV-11
- Wave 7 (after GOV-11): GOV-12

---

## SECTION 5: CHANGE PROPAGATION RULES

When a document is updated after Baseline V1.0.0, ALL downstream documents must be reviewed for impact:

| Document Updated | Must Review Downstream |
|---|---|
| GOV-01 Constitution | GOV-06, GOV-08, GOV-09, GOV-11, GOV-12 |
| GOV-02 Taxonomy | ALL other 11 documents |
| GOV-03 Ontology | GOV-04, GOV-11, GOV-12 |
| GOV-04 Schema | GOV-08, GOV-10, GOV-11, GOV-12 |
| GOV-05 Glossary | GOV-11, GOV-12 |
| GOV-06 ADR Index | GOV-11, GOV-12 |
| GOV-07 Lifecycle SM | GOV-04, GOV-08, GOV-10, GOV-11, GOV-12 |
| GOV-08 Policy Engine | GOV-09, GOV-10, GOV-11, GOV-12 |
| GOV-09 ECL | GOV-11, GOV-12 |
| GOV-10 OEPM Manifest | GOV-11, GOV-12 |
| GOV-11 Dependency Map | GOV-12 |

**Critical Rule:** Any change to GOV-02 (Taxonomy) triggers a full review of all 11 other documents. The Taxonomy is the root of the dependency graph. Changes to it require a major Change Control event.

---

## SECTION 6: CIRCULAR DEPENDENCY CHECK

No circular dependencies exist in the current graph. Verification:

- GOV-02 (Taxonomy) has no dependencies → confirmed root
- GOV-01 (Constitution) has no dependencies → confirmed root
- GOV-11 (Dependency Map) depends on all others but nothing depends on GOV-11 except GOV-12
- GOV-12 (Validation Suite) is a pure leaf — nothing depends on it in V1.0.0

**Status: PASS — No circular dependencies detected.**

---

## SECTION 7: EXTERNAL DEPENDENCIES

The governance documents have the following external dependencies (outside the governance directory):

| Governance Document | External Dependency | Path | Nature |
|---|---|---|---|
| Constitution | SOUL.md | ~/.openclaw/workspace/SOUL.md | Source for founding principles |
| Constitution | HEARTBEAT.md | ~/.openclaw/workspace/HEARTBEAT.md | Source for budget caps |
| ADR Index | AGENTS.md | ~/.openclaw/workspace/AGENTS.md | Source for PM2/operational facts |
| ADR Index | MEMORY.md | ~/.openclaw/workspace/MEMORY.md | Source for trading decisions |
| Policy Engine | HEARTBEAT.md | ~/.openclaw/workspace/HEARTBEAT.md | Source for circuit breaker rules |
| OEPM Manifest Standard | AGENTS.md | ~/.openclaw/workspace/AGENTS.md | Source for PM2 IDs / service inventory |
| All documents | Taxonomy | ~/.openclaw/workspace/governance/OPEN_EMPIRE_ASSET_TAXONOMY_V1.md | Root governance artifact |

**Note:** External source documents (SOUL.md, HEARTBEAT.md, AGENTS.md, MEMORY.md) are operational configuration files, not governance artifacts. Changes to these files do NOT require Change Control but should be reflected in governance documents via normal review cycles.

---

## SECTION 8: VERSION COMPATIBILITY MATRIX

All documents in Governance Baseline V1.0.0 are mutually compatible at version 1.0.0.

| Document | Version | Compatible With |
|---|---|---|
| All 12 documents | 1.0.0 | Each other at 1.0.0 |

After Baseline, breaking changes to any document require incrementing its major version. All dependent documents must declare compatibility with the new major version before the Baseline can be incremented to V1.1.0 or V2.0.0.
