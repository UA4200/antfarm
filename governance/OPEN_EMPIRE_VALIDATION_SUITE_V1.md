# OPEN EMPIRE VALIDATION SUITE V1

**Version:** 1.0.0
**Status:** Draft — Pending Validation
**Owner:** Nathan (Sovereign Operator)
**Source:** All 12 canonical governance documents
**Materialization Date:** 2026-08-05
**Dependencies:** All 11 other governance documents + OPEN_EMPIRE_DEPENDENCY_MAP_V1.md
**Revision History:**

| Version | Date | Author | Change |
|---|---|---|---|
| 1.0.0 | 2026-08-05 | Alusi | Initial materialization under Governance Freeze Order 2026-08-05 |

---

## PREAMBLE

The Validation Suite defines the rules, procedures, and evidence artifacts required to validate all 12 canonical governance documents and declare Governance Baseline V1.0.0. Validation executes only against canonical files on the filesystem. Conversation history is never used as runtime validation input. All validation runs must persist reproducible evidence.

**Canonical validation script:** `~/.openclaw/workspace/governance/build/validate.py`

---

## SECTION 1: VALIDATION PRINCIPLES

1. **Filesystem-only:** Validation reads files from `~/.openclaw/workspace/governance/`. No other source is authoritative.
2. **Reproducibility:** Any validation run on the same files must produce identical results. Non-deterministic validation = BLOCKED status.
3. **Evidence Persistence:** Every run persists all artifacts to `~/.openclaw/workspace/governance/build/runs/<timestamp>/`.
4. **No Partial Credit:** A document either PASSES or FAILS. No partial pass states.
5. **Blocking Rules:** Any single FAIL across any RULE blocks the overall PASS verdict. All rules must pass.
6. **SHA-256 Binding:** Validation results are bound to the exact SHA-256 of each input file. Re-validation against different content requires a new run.

---

## SECTION 2: VALIDATION RULE CATALOG

### VR-SUITE: Suite-Level Rules (applied to the set of all 12 documents)

| Rule ID | Description | Severity | Check Method |
|---|---|---|---|
| VR-S001 | All 12 canonical documents must exist at their canonical paths | BLOCK | `os.path.exists()` |
| VR-S002 | No document may be zero bytes | BLOCK | `os.path.getsize() > 0` |
| VR-S003 | All 12 documents must have unique SHA-256 hashes | BLOCK | `hashlib.sha256()` |
| VR-S004 | Dependency Map must list all 12 documents in its Document Registry | BLOCK | Text search |
| VR-S005 | Build pipeline must complete without errors | BLOCK | Exit code check |

---

### VR-STRUCT: Structure Rules (applied to every document)

| Rule ID | Description | Severity | Check Method |
|---|---|---|---|
| VR-ST001 | Document must begin with `# OPEN EMPIRE` heading | BLOCK | Line 1 regex |
| VR-ST002 | Document must contain `**Version:**` field | BLOCK | Regex search |
| VR-ST003 | Document must contain `**Status:**` field | BLOCK | Regex search |
| VR-ST004 | Document must contain `**Owner:**` field | BLOCK | Regex search |
| VR-ST005 | Document must contain `**Source:**` field | BLOCK | Regex search |
| VR-ST006 | Document must contain `**Materialization Date:**` field | BLOCK | Regex search |
| VR-ST007 | Document must contain `**Dependencies:**` field | BLOCK | Regex search |
| VR-ST008 | Document must contain `**Revision History:**` table | BLOCK | Regex search |
| VR-ST009 | Version value must be valid semver (e.g., `1.0.0`) | BLOCK | Regex: `\d+\.\d+\.\d+` |
| VR-ST010 | Owner field must contain "Nathan" | BLOCK | String contains |
| VR-ST011 | Materialization Date must be valid date (YYYY-MM-DD) | BLOCK | Regex |
| VR-ST012 | Revision History must contain at least one row (initial entry) | BLOCK | Table row count |

---

### VR-CONTENT: Content Rules (document-specific)

#### Constitution (GOV-01)

| Rule ID | Description | Severity |
|---|---|---|
| VR-C001 | Must contain "Sovereignty Clause" or "Sovereign Operator" | BLOCK |
| VR-C002 | Must contain "Nathan" as sovereign | BLOCK |
| VR-C003 | Must contain at least 5 of the 10 Standing Rules | BLOCK |
| VR-C004 | Must contain "Amendment Procedure" or "Change Control" | BLOCK |
| VR-C005 | Must contain budget cap values ($2, $5, $10) | WARN |

#### Asset Taxonomy (GOV-02)

| Rule ID | Description | Severity |
|---|---|---|
| VR-T001 | Must contain at least 50 `### ` section headings (asset types) | BLOCK |
| VR-T002 | Must contain "Canonical Name" and "Canonical Definition" columns | BLOCK |
| VR-T003 | Must contain "Required Schema Fields" column | BLOCK |
| VR-T004 | Must contain "Lifecycle Applicability" column | BLOCK |
| VR-T005 | Must contain "Allowed Relationships" column | BLOCK |
| VR-T006 | Must contain all 6 layer headings (LAYER 1 through LAYER 6) | BLOCK |

#### Ontology (GOV-03)

| Rule ID | Description | Severity |
|---|---|---|
| VR-O001 | Must contain "Relationship Vocabulary" section | BLOCK |
| VR-O002 | Must contain at least 5 relationship verbs (CONTAINS, BELONGS_TO, etc.) | BLOCK |
| VR-O003 | Must reference OPEN_EMPIRE_ASSET_TAXONOMY_V1.md | WARN |

#### Schema (GOV-04)

| Rule ID | Description | Severity |
|---|---|---|
| VR-SC001 | Must contain "Schema Conventions" section | BLOCK |
| VR-SC002 | Must contain "Common Fields" definition (id, name, created_at, etc.) | BLOCK |
| VR-SC003 | Must contain at least 50 asset type schema sections | BLOCK |
| VR-SC004 | Must contain "Validation Rule Index" section | BLOCK |
| VR-SC005 | Must contain at least 3 JSON Schema examples | BLOCK |
| VR-SC006 | JSON Schema blocks must contain `"$schema"` key | WARN |

#### Glossary (GOV-05)

| Rule ID | Description | Severity |
|---|---|---|
| VR-G001 | Must contain at least 50 term definitions | BLOCK |
| VR-G002 | Must contain "Runtime Terms" section | BLOCK |
| VR-G003 | Must define "TRACK_B_AUTHORIZED" | BLOCK |
| VR-G004 | Must define "Governance Baseline" | BLOCK |
| VR-G005 | Must define "TODO_PENDING_APPROVAL" | BLOCK |

#### ADR Index (GOV-06)

| Rule ID | Description | Severity |
|---|---|---|
| VR-A001 | Must contain at least 5 ADR entries | BLOCK |
| VR-A002 | All ADR entries must have Status field | BLOCK |
| VR-A003 | ADR-001 through ADR-010 must be present | BLOCK |
| VR-A004 | Must contain ADR Template section | WARN |

#### Lifecycle State Machine (GOV-07)

| Rule ID | Description | Severity |
|---|---|---|
| VR-L001 | Must contain "Universal State Definitions" section | BLOCK |
| VR-L002 | Must contain at least 20 asset type state machine definitions | BLOCK |
| VR-L003 | Must contain Transition Table headers | BLOCK |
| VR-L004 | Must contain "Nathan Approval Required" column in transitions | BLOCK |

#### Policy Engine (GOV-08)

| Rule ID | Description | Severity |
|---|---|---|
| VR-P001 | Must contain at least 10 POL-NNN entries | BLOCK |
| VR-P002 | POL-001 (Daily Spend Cap) must be present | BLOCK |
| VR-P003 | POL-020 (Draft-Only Communication) must be present | BLOCK |
| VR-P004 | POL-030 (Change Control) must be present | BLOCK |
| VR-P005 | Must contain enforcement matrix | WARN |

#### Executive Command Language (GOV-09)

| Rule ID | Description | Severity |
|---|---|---|
| VR-E001 | Must contain "Core Command Vocabulary" section | BLOCK |
| VR-E002 | Must define "Continue", "Yes", "Go ahead", "Do it" commands | BLOCK |
| VR-E003 | Must define "TRACK_B_AUTHORIZED" as a governance command | BLOCK |
| VR-E004 | Must contain "Authorization Matrix" section | WARN |

#### OEPM Manifest Standard (GOV-10)

| Rule ID | Description | Severity |
|---|---|---|
| VR-M001 | Must contain manifest JSON schema | BLOCK |
| VR-M002 | Must contain `"oepm_version"` field definition | BLOCK |
| VR-M003 | Must contain `"asset"` object definition | BLOCK |
| VR-M004 | Must contain `"portfolio_placement"` definition | BLOCK |
| VR-M005 | Must contain `"governance"` section | BLOCK |
| VR-M006 | Must contain at least 2 example manifests | WARN |

#### Dependency Map (GOV-11)

| Rule ID | Description | Severity |
|---|---|---|
| VR-D001 | Must contain "Document Registry" table with all 12 documents | BLOCK |
| VR-D002 | Must contain "Dependency Matrix" section | BLOCK |
| VR-D003 | Must contain "Topological Build Order" section | BLOCK |
| VR-D004 | Must confirm no circular dependencies | BLOCK |
| VR-D005 | Must contain "Change Propagation Rules" section | BLOCK |

#### Validation Suite (GOV-12 — self-referential check)

| Rule ID | Description | Severity |
|---|---|---|
| VR-VS001 | Must contain "Validation Rule Catalog" section | BLOCK |
| VR-VS002 | Must contain at least 30 VR-NNN rules | BLOCK |
| VR-VS003 | Must define "Definition of Done" criteria | BLOCK |
| VR-VS004 | Must reference the build pipeline script path | BLOCK |

---

## SECTION 3: VALIDATION PROCESS

### Run Procedure

```bash
# Standard validation run
cd ~/.openclaw/workspace/governance/build
python3 validate.py --governance-dir ~/.openclaw/workspace/governance \
                    --output-dir ~/.openclaw/workspace/governance/build/runs/$(date +%Y%m%dT%H%M%S)
```

### Input Artifacts
- All 12 `*.md` files in `~/.openclaw/workspace/governance/`

### Output Artifacts (persisted per run)

Every validation run produces the following in `build/runs/<timestamp>/`:

| Artifact | Filename | Description |
|---|---|---|
| Rule Results | `rule_results.json` | Array of {rule_id, document, status, evidence, message} |
| Summary | `validation_summary.json` | Overall pass/fail, counts, timestamp, document hashes |
| SHA256SUMS | `SHA256SUMS` | Hash of every input file |
| Failed Rules | `failed_rules.json` | Subset of rule_results where status=FAIL |
| Validator Log | `validate.log` | Full execution log |
| Pass/Fail Report | `VALIDATION_REPORT.md` | Human-readable summary |

### Result Schema (`rule_results.json`)

```json
[
  {
    "rule_id": "VR-ST001",
    "document": "OPEN_EMPIRE_CONSTITUTION_V1.md",
    "document_sha256": "abc123...",
    "status": "PASS",
    "evidence": "Line 1: '# OPEN EMPIRE CONSTITUTION V1'",
    "message": null
  }
]
```

### Summary Schema (`validation_summary.json`)

```json
{
  "validator_version": "1.0.0",
  "run_timestamp": "2026-08-05T16:00:00Z",
  "governance_dir": "~/.openclaw/workspace/governance",
  "overall_status": "PASS",
  "documents_checked": 12,
  "rules_run": 74,
  "rules_passed": 74,
  "rules_failed": 0,
  "rules_warned": 0,
  "input_artifacts": {
    "OPEN_EMPIRE_CONSTITUTION_V1.md": "sha256:...",
    "OPEN_EMPIRE_ASSET_TAXONOMY_V1.md": "sha256:..."
  }
}
```

---

## SECTION 4: GOVERNANCE BASELINE V1.0.0 DEFINITION OF DONE

Governance Baseline V1.0.0 is declared complete when ALL of the following are true:

### Document Completeness
- [ ] All 12 canonical Markdown documents exist in `~/.openclaw/workspace/governance/`
- [ ] All 12 documents contain the required materialization header (Version, Status, Owner, Source, Materialization Date, Dependencies, Revision History)
- [ ] No document contains fabricated content — all content is derived from source documents or marked `TODO_PENDING_APPROVAL`

### Validation
- [ ] `validate.py` executes without Python errors
- [ ] All BLOCK-severity rules pass (zero failures)
- [ ] `VALIDATION_REPORT.md` generated with `overall_status: PASS`
- [ ] `failed_rules.json` is empty

### Build Pipeline
- [ ] `build_pipeline.py` (or `build.sh`) executes without errors
- [ ] JSON representation of governance generated
- [ ] YAML representation of governance generated
- [ ] Dependency graph file generated
- [ ] `SHA256SUMS` file generated and verified
- [ ] `RELEASE_MANIFEST.md` generated
- [ ] `ROLLBACK_MANIFEST.md` generated
- [ ] All outputs are reproducible (running build twice on same inputs = identical hashes)

### Release
- [ ] `RELEASE_MANIFEST.md` lists all 12 documents with SHA-256 hashes
- [ ] `ROLLBACK_MANIFEST.md` documents the prior state and rollback procedure
- [ ] `Governance Baseline V1.0.0` tag or marker created

### Declaration
- [ ] Alusi formally declares: `TRACK_B_AUTHORIZED`
- [ ] Nathan acknowledges

---

## SECTION 5: VALIDATION FAILURE HANDLING

| Failure Type | Response |
|---|---|
| Missing document (VR-S001) | Stop validation. Cannot proceed. Agent must materialize missing document. |
| Structure failure (VR-ST*) | Document must be revised to include required header field. |
| Content failure (VR-C*, etc.) | Document must be revised. Re-run full validation after fix. |
| Build pipeline error | Pipeline bug must be fixed. Re-run. Status = BLOCKED until resolved. |
| Non-deterministic output | Root cause must be identified. Status = BLOCKED. |

**Rule:** After any failure fix, the full validation suite re-runs from the beginning. No partial re-runs.

---

## SECTION 6: VALIDATOR VERSION HISTORY

| Version | Date | Changes |
|---|---|---|
| 1.0.0 | 2026-08-05 | Initial Governance Baseline V1.0.0 validator |

Future versions of the validator are released only through Change Control.
