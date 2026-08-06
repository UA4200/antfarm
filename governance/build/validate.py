#!/usr/bin/env python3
"""
Open Empire Governance Validation Suite
Version: 1.0.0
Validates all 12 canonical governance documents against defined rules.
"""

import os
import re
import json
import hashlib
import sys
import argparse
from datetime import datetime, timezone
from pathlib import Path

VALIDATOR_VERSION = "1.0.0"

CANONICAL_DOCS = {
    "GOV-01": "OPEN_EMPIRE_CONSTITUTION_V1.md",
    "GOV-02": "OPEN_EMPIRE_ASSET_TAXONOMY_V1.md",
    "GOV-03": "OPEN_EMPIRE_ONTOLOGY_V1.md",
    "GOV-04": "OPEN_EMPIRE_SCHEMA_V1.md",
    "GOV-05": "OPEN_EMPIRE_GLOSSARY_V1.md",
    "GOV-06": "OPEN_EMPIRE_ADR_INDEX_V1.md",
    "GOV-07": "OPEN_EMPIRE_LIFECYCLE_STATE_MACHINE_V1.md",
    "GOV-08": "OPEN_EMPIRE_POLICY_ENGINE_V1.md",
    "GOV-09": "OPEN_EMPIRE_EXECUTIVE_COMMAND_LANGUAGE_V1.md",
    "GOV-10": "OPEN_EMPIRE_OEPM_MANIFEST_STANDARD_V1.md",
    "GOV-11": "OPEN_EMPIRE_DEPENDENCY_MAP_V1.md",
    "GOV-12": "OPEN_EMPIRE_VALIDATION_SUITE_V1.md",
}

SEMVER_RE = re.compile(r'\d+\.\d+\.\d+')
DATE_RE = re.compile(r'\d{4}-\d{2}-\d{2}')

results = []
doc_contents = {}
doc_hashes = {}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()


def rule(rule_id, doc_id, doc_name, status, evidence, message=None):
    results.append({
        "rule_id": rule_id,
        "doc_id": doc_id,
        "document": doc_name,
        "document_sha256": doc_hashes.get(doc_name, ""),
        "status": status,
        "evidence": evidence,
        "message": message
    })
    return status == "PASS"


def check(cond, rule_id, doc_id, doc_name, evidence_pass, evidence_fail, severity="BLOCK"):
    if cond:
        rule(rule_id, doc_id, doc_name, "PASS", evidence_pass)
        return True
    else:
        rule(rule_id, doc_id, doc_name, "FAIL" if severity == "BLOCK" else "WARN", evidence_fail)
        return False


def validate_structure(doc_id, doc_name, content):
    """VR-ST: Structure rules applied to every document."""
    check(content.startswith("# OPEN EMPIRE"),
          "VR-ST001", doc_id, doc_name,
          "Document begins with '# OPEN EMPIRE'",
          "Document does not begin with '# OPEN EMPIRE'")

    for field, rule_id in [
        ("**Version:**", "VR-ST002"),
        ("**Status:**",  "VR-ST003"),
        ("**Owner:**",   "VR-ST004"),
        ("**Source:**",  "VR-ST005"),
        ("**Materialization Date:**", "VR-ST006"),
        ("**Dependencies:**", "VR-ST007"),
        ("**Revision History:**", "VR-ST008"),
    ]:
        check(field in content, rule_id, doc_id, doc_name,
              f"Found '{field}'", f"Missing '{field}'")

    # VR-ST009: semver
    ver_match = re.search(r'\*\*Version:\*\*\s*(\S+)', content)
    if ver_match:
        check(bool(SEMVER_RE.match(ver_match.group(1))),
              "VR-ST009", doc_id, doc_name,
              f"Version '{ver_match.group(1)}' is valid semver",
              f"Version '{ver_match.group(1)}' is not valid semver")
    else:
        rule("VR-ST009", doc_id, doc_name, "FAIL", "No version found")

    # VR-ST010: Owner contains Nathan
    check("Nathan" in content,
          "VR-ST010", doc_id, doc_name,
          "Owner field contains 'Nathan'",
          "Owner field does not contain 'Nathan'")

    # VR-ST011: Materialization Date is valid date
    mat_match = re.search(r'\*\*Materialization Date:\*\*\s*(\S+)', content)
    if mat_match:
        check(bool(DATE_RE.match(mat_match.group(1))),
              "VR-ST011", doc_id, doc_name,
              f"Materialization Date '{mat_match.group(1)}' is valid",
              f"Materialization Date '{mat_match.group(1)}' is not a valid date")
    else:
        rule("VR-ST011", doc_id, doc_name, "FAIL", "No Materialization Date found")

    # VR-ST012: Revision History has at least one row
    rev_section = content.find("**Revision History:**")
    if rev_section >= 0:
        after = content[rev_section:]
        rows = [l for l in after.split('\n') if l.startswith('| 1.') or re.match(r'\|\s*\d+\.\d+\.\d+', l)]
        check(len(rows) >= 1,
              "VR-ST012", doc_id, doc_name,
              f"Revision History has {len(rows)} row(s)",
              "Revision History has no rows")
    else:
        rule("VR-ST012", doc_id, doc_name, "FAIL", "No Revision History section found")


def validate_content(doc_id, doc_name, content):
    """VR-CONTENT: Document-specific content rules."""

    if doc_id == "GOV-01":  # Constitution
        check("Sovereign Operator" in content or "Sovereignty" in content,
              "VR-C001", doc_id, doc_name, "Contains Sovereignty reference", "Missing Sovereignty reference")
        check("Nathan" in content,
              "VR-C002", doc_id, doc_name, "Contains 'Nathan' as sovereign", "Missing Nathan reference")
        standing_rules = ["DRAFT-ONLY", "3-STRIKE", "SECURITY FIRST", "LOG EVERYTHING",
                          "CIRCUIT BREAKER", "COUNCIL GATE", "N8N RELAY", "BUDGET RESPECT",
                          "10-MINUTE", "MEMORY FIRST"]
        found = sum(1 for r in standing_rules if r in content.upper() or r.replace("-", " ") in content.upper())
        check(found >= 5, "VR-C003", doc_id, doc_name,
              f"Found {found}/10 Standing Rules", f"Only found {found}/10 Standing Rules (need ≥5)")
        check("Amendment" in content or "Change Control" in content,
              "VR-C004", doc_id, doc_name, "Contains Amendment/Change Control procedure", "Missing amendment procedure")
        cap_found = any(cap in content for cap in ["$2", "$5", "$10"])
        check(cap_found, "VR-C005", doc_id, doc_name,
              "Contains budget cap values", "Missing budget cap values", severity="WARN")

    elif doc_id == "GOV-02":  # Taxonomy
        headings = len(re.findall(r'^### ', content, re.MULTILINE))
        check(headings >= 50, "VR-T001", doc_id, doc_name,
              f"Found {headings} asset type headings", f"Only {headings} headings (need ≥50)")
        check("Canonical Name" in content and "Canonical Definition" in content,
              "VR-T002", doc_id, doc_name, "Contains Canonical Name/Definition columns", "Missing columns")
        check("Required Schema Fields" in content,
              "VR-T003", doc_id, doc_name, "Contains Required Schema Fields", "Missing Required Schema Fields")
        check("Lifecycle Applicability" in content,
              "VR-T004", doc_id, doc_name, "Contains Lifecycle Applicability", "Missing Lifecycle Applicability")
        check("Allowed Relationships" in content,
              "VR-T005", doc_id, doc_name, "Contains Allowed Relationships", "Missing Allowed Relationships")
        layers_found = sum(1 for i in range(1, 7) if f"LAYER {i}" in content)
        check(layers_found == 6, "VR-T006", doc_id, doc_name,
              f"Found all 6 layer headings", f"Only found {layers_found}/6 layer headings")

    elif doc_id == "GOV-03":  # Ontology
        uc = content.upper()
        check("RELATIONSHIP VOCABULARY" in uc or "RELATIONSHIP" in uc,
              "VR-O001", doc_id, doc_name, "Contains Relationship Vocabulary", "Missing Relationship Vocabulary")
        verbs = ["CONTAINS", "BELONGS_TO", "GOVERNED_BY", "MEASURED_BY", "PRODUCES"]
        found = sum(1 for v in verbs if v in content)
        check(found >= 5, "VR-O002", doc_id, doc_name,
              f"Found {found} relationship verbs", f"Only {found} verbs (need ≥5)")
        check("OPEN_EMPIRE_ASSET_TAXONOMY" in content,
              "VR-O003", doc_id, doc_name, "References Taxonomy", "Missing Taxonomy reference", severity="WARN")

    elif doc_id == "GOV-04":  # Schema
        uc = content.upper()
        check("SCHEMA CONVENTION" in uc or "Schema Convention" in content,
              "VR-SC001", doc_id, doc_name, "Contains Schema Conventions", "Missing Schema Conventions")
        check("Common Fields" in content and "created_at" in content,
              "VR-SC002", doc_id, doc_name, "Contains Common Fields definition", "Missing Common Fields")
        # Count ### headings in SECTION 2 (asset type schemas) — each type is a ### heading
        sec2_match = re.search(r'SECTION 2.*?(?=## SECTION 3|\Z)', content, re.DOTALL)
        if sec2_match:
            schemas = len(re.findall(r'^### ', sec2_match.group(0), re.MULTILINE))
        else:
            schemas = len(re.findall(r'^### (?!Field Type|Common Fields|Governance Meta|Notation)', content, re.MULTILINE))
        check(schemas >= 50, "VR-SC003", doc_id, doc_name,
              f"Found {schemas} asset type schema sections", f"Only {schemas} schemas (need ≥50)")
        check("VALIDATION RULE" in uc or "Validation Rule" in content,
              "VR-SC004", doc_id, doc_name, "Contains Validation Rule Index", "Missing Validation Rule Index")
        json_count = content.count('"$schema"')
        check(json_count >= 3, "VR-SC005", doc_id, doc_name,
              f"Found {json_count} JSON Schema examples", f"Only {json_count} JSON schemas (need ≥3)")
        check('"$schema"' in content,
              "VR-SC006", doc_id, doc_name, "JSON Schema blocks contain $schema key", "Missing $schema key", severity="WARN")

    elif doc_id == "GOV-05":  # Glossary
        terms = len(re.findall(r'^### ', content, re.MULTILINE))
        check(terms >= 50, "VR-G001", doc_id, doc_name,
              f"Found {terms} term definitions", f"Only {terms} terms (need ≥50)")
        check("Runtime Terms" in content,
              "VR-G002", doc_id, doc_name, "Contains Runtime Terms section", "Missing Runtime Terms")
        check("TRACK_B_AUTHORIZED" in content,
              "VR-G003", doc_id, doc_name, "Defines TRACK_B_AUTHORIZED", "Missing TRACK_B_AUTHORIZED definition")
        check("Governance Baseline" in content,
              "VR-G004", doc_id, doc_name, "Defines Governance Baseline", "Missing Governance Baseline definition")
        check("TODO_PENDING_APPROVAL" in content,
              "VR-G005", doc_id, doc_name, "Defines TODO_PENDING_APPROVAL", "Missing TODO_PENDING_APPROVAL")

    elif doc_id == "GOV-06":  # ADR Index
        adrs = len(re.findall(r'^## ADR-\d+', content, re.MULTILINE))
        check(adrs >= 5, "VR-A001", doc_id, doc_name,
              f"Found {adrs} ADR entries", f"Only {adrs} ADRs (need ≥5)")
        check("**Status:**" in content or "Status:" in content,
              "VR-A002", doc_id, doc_name, "ADR entries have Status field", "Missing Status field in ADRs")
        for i in range(1, 11):
            check(f"ADR-{i:03d}" in content or f"ADR-{i}" in content,
                  "VR-A003", doc_id, doc_name,
                  f"ADR-{i:03d} present", f"ADR-{i:03d} missing")
        check("ADR Template" in content,
              "VR-A004", doc_id, doc_name, "Contains ADR Template", "Missing ADR Template", severity="WARN")

    elif doc_id == "GOV-07":  # Lifecycle State Machine
        uc = content.upper()
        check("STATE DEFINITION" in uc or "UNIVERSAL STATE" in uc,
              "VR-L001", doc_id, doc_name, "Contains Universal State Definitions", "Missing State Definitions")
        machines = len(re.findall(r'^## ', content, re.MULTILINE))
        check(machines >= 20, "VR-L002", doc_id, doc_name,
              f"Found {machines} sections", f"Only {machines} sections (need ≥20 for state machines)")
        check("Transition" in content or "TRANSITION" in uc,
              "VR-L003", doc_id, doc_name, "Contains Transition table", "Missing Transition table")
        check("Nathan" in content and "Approval" in content,
              "VR-L004", doc_id, doc_name, "Contains Nathan Approval column", "Missing Nathan Approval column")

    elif doc_id == "GOV-08":  # Policy Engine
        pol_count = len(re.findall(r'POL-\d+', content))
        check(pol_count >= 10, "VR-P001", doc_id, doc_name,
              f"Found {pol_count} POL references", f"Only {pol_count} POL refs (need ≥10)")
        check("POL-001" in content,
              "VR-P002", doc_id, doc_name, "POL-001 present", "POL-001 missing")
        check("POL-020" in content,
              "VR-P003", doc_id, doc_name, "POL-020 present", "POL-020 missing")
        check("POL-030" in content,
              "VR-P004", doc_id, doc_name, "POL-030 present", "POL-030 missing")
        check("matrix" in content.lower() or "Matrix" in content,
              "VR-P005", doc_id, doc_name, "Contains enforcement matrix", "Missing enforcement matrix", severity="WARN")

    elif doc_id == "GOV-09":  # ECL
        uc = content.upper()
        check("COMMAND VOCABULARY" in uc or "CORE COMMAND" in uc,
              "VR-E001", doc_id, doc_name, "Contains Command Vocabulary section", "Missing Command Vocabulary")
        for cmd in ["Continue", "Yes", "Go ahead", "Do it"]:
            check(cmd in content, "VR-E002", doc_id, doc_name,
                  f"Defines '{cmd}' command", f"Missing '{cmd}' command definition")
        check("TRACK_B_AUTHORIZED" in content,
              "VR-E003", doc_id, doc_name, "Defines TRACK_B_AUTHORIZED command", "Missing TRACK_B_AUTHORIZED")
        check("Authorization" in content or "AUTHORIZATION" in uc or "matrix" in content.lower(),
              "VR-E004", doc_id, doc_name, "Contains Authorization section", "Missing Authorization section", severity="WARN")

    elif doc_id == "GOV-10":  # OEPM Manifest Standard
        check('"oepm_version"' in content or 'oepm_version' in content,
              "VR-M002", doc_id, doc_name, "Contains oepm_version definition", "Missing oepm_version")
        check('"asset"' in content or '**asset**' in content or '`asset`' in content,
              "VR-M003", doc_id, doc_name, "Contains asset object definition", "Missing asset definition")
        check("portfolio_placement" in content,
              "VR-M004", doc_id, doc_name, "Contains portfolio_placement definition", "Missing portfolio_placement")
        check("governance" in content,
              "VR-M005", doc_id, doc_name, "Contains governance section", "Missing governance section")
        examples = len(re.findall(r'cashclaw|clawdb|TAXONOMY', content))
        check(examples >= 2, "VR-M006", doc_id, doc_name,
              f"Found {examples} example references", f"Only {examples} examples (need ≥2)", severity="WARN")
        check("{" in content and '"' in content,
              "VR-M001", doc_id, doc_name, "Contains JSON manifest schema", "Missing JSON manifest schema")

    elif doc_id == "GOV-11":  # Dependency Map
        uc = content.upper()
        check("DOCUMENT REGISTRY" in uc or "Document Registry" in content,
              "VR-D001", doc_id, doc_name, "Contains Document Registry", "Missing Document Registry")
        # Check all 12 docs are listed
        missing = [fn for fn in CANONICAL_DOCS.values() if fn not in content]
        check(len(missing) == 0, "VR-D001b", doc_id, doc_name,
              "All 12 documents in registry", f"Missing from registry: {missing}")
        check("DEPENDENCY MATRIX" in uc or "Dependency Matrix" in content,
              "VR-D002", doc_id, doc_name, "Contains Dependency Matrix", "Missing Dependency Matrix")
        check("TOPOLOGICAL" in uc or "Build Order" in content or "BUILD ORDER" in uc,
              "VR-D003", doc_id, doc_name, "Contains Build Order", "Missing Topological Build Order")
        check("circular" in content.lower() or "CIRCULAR" in uc,
              "VR-D004", doc_id, doc_name, "Contains circular dependency check", "Missing circular dep check")
        check("CHANGE PROPAGATION" in uc or "Change Propagation" in content or "propagation" in content.lower(),
              "VR-D005", doc_id, doc_name, "Contains Change Propagation Rules", "Missing Change Propagation Rules")

    elif doc_id == "GOV-12":  # Validation Suite (self)
        check("Validation Rule Catalog" in content or "VALIDATION RULE CATALOG" in content.upper(),
              "VR-VS001", doc_id, doc_name, "Contains Validation Rule Catalog", "Missing rule catalog")
        vr_count = len(re.findall(r'VR-[A-Z]+\d+', content))
        check(vr_count >= 30, "VR-VS002", doc_id, doc_name,
              f"Found {vr_count} VR-NNN rules", f"Only {vr_count} rules (need ≥30)")
        check("Definition of Done" in content,
              "VR-VS003", doc_id, doc_name, "Contains Definition of Done", "Missing Definition of Done")
        check("validate.py" in content or "build_pipeline" in content,
              "VR-VS004", doc_id, doc_name, "References build pipeline script", "Missing pipeline reference")


def main():
    parser = argparse.ArgumentParser(description="Open Empire Governance Validator")
    parser.add_argument("--governance-dir", default=os.path.expanduser("~/.openclaw/workspace/governance"))
    parser.add_argument("--output-dir", default=None)
    args = parser.parse_args()

    gov_dir = Path(args.governance_dir)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = Path(args.output_dir) if args.output_dir else Path(gov_dir) / "build" / "runs" / ts
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Open Empire Governance Validator v{VALIDATOR_VERSION}")
    print(f"Governance dir: {gov_dir}")
    print(f"Output dir: {out_dir}")
    print(f"Timestamp: {ts}")
    print()

    # === SUITE RULES ===
    all_present = True
    for doc_id, fname in CANONICAL_DOCS.items():
        fpath = gov_dir / fname
        exists = fpath.exists()
        check(exists, "VR-S001", doc_id, fname,
              f"File exists: {fpath}", f"MISSING: {fpath}")
        if exists:
            size = fpath.stat().st_size
            check(size > 0, "VR-S002", doc_id, fname,
                  f"File size: {size} bytes", f"File is empty")
            doc_hashes[fname] = sha256_file(fpath)
            with open(fpath, 'r', encoding='utf-8') as f:
                doc_contents[doc_id] = f.read()
        else:
            all_present = False

    if not all_present:
        print("FATAL: One or more documents are missing. Cannot continue.")
        _write_outputs(out_dir, ts, "FAIL")
        sys.exit(1)

    # Check unique hashes
    hashes = list(doc_hashes.values())
    check(len(set(hashes)) == len(hashes), "VR-S003", "SUITE", "ALL",
          "All 12 documents have unique SHA-256 hashes",
          f"Duplicate hashes detected among {len(hashes)} documents")

    # Check Dependency Map lists all 12
    dep_map = doc_contents.get("GOV-11", "")
    missing_in_depmap = [fn for fn in CANONICAL_DOCS.values() if fn not in dep_map]
    check(len(missing_in_depmap) == 0, "VR-S004", "SUITE", "ALL",
          "Dependency Map lists all 12 documents",
          f"Missing from Dependency Map: {missing_in_depmap}")

    # === STRUCTURE + CONTENT RULES ===
    for doc_id, content in doc_contents.items():
        fname = CANONICAL_DOCS[doc_id]
        print(f"Validating {fname}...")
        validate_structure(doc_id, fname, content)
        validate_content(doc_id, fname, content)

    # === RESULTS ===
    passed = [r for r in results if r["status"] == "PASS"]
    failed = [r for r in results if r["status"] == "FAIL"]
    warned = [r for r in results if r["status"] == "WARN"]
    overall = "PASS" if len(failed) == 0 else "FAIL"

    print()
    print(f"Rules run:    {len(results)}")
    print(f"Passed:       {len(passed)}")
    print(f"Failed:       {len(failed)}")
    print(f"Warnings:     {len(warned)}")
    print(f"Overall:      {overall}")

    if failed:
        print("\nFailed rules:")
        for r in failed:
            print(f"  {r['rule_id']} [{r['doc_id']}] {r['document']}: {r['evidence']}")

    _write_outputs(out_dir, ts, overall)

    if overall == "FAIL":
        sys.exit(1)
    sys.exit(0)


def _write_outputs(out_dir, ts, overall):
    # rule_results.json
    with open(out_dir / "rule_results.json", 'w') as f:
        json.dump(results, f, indent=2)

    # failed_rules.json
    failed = [r for r in results if r["status"] == "FAIL"]
    with open(out_dir / "failed_rules.json", 'w') as f:
        json.dump(failed, f, indent=2)

    # SHA256SUMS
    with open(out_dir / "SHA256SUMS", 'w') as f:
        for fname, h in sorted(doc_hashes.items()):
            f.write(f"{h}  {fname}\n")

    # validation_summary.json
    summary = {
        "validator_version": VALIDATOR_VERSION,
        "run_timestamp": ts,
        "governance_dir": str(Path(out_dir).parent.parent.parent),
        "overall_status": overall,
        "documents_checked": len(CANONICAL_DOCS),
        "rules_run": len(results),
        "rules_passed": len([r for r in results if r["status"] == "PASS"]),
        "rules_failed": len(failed),
        "rules_warned": len([r for r in results if r["status"] == "WARN"]),
        "input_artifacts": doc_hashes,
    }
    with open(out_dir / "validation_summary.json", 'w') as f:
        json.dump(summary, f, indent=2)

    # VALIDATION_REPORT.md
    with open(out_dir / "VALIDATION_REPORT.md", 'w') as f:
        f.write(f"# Open Empire Governance Validation Report\n\n")
        f.write(f"**Run Timestamp:** {ts}\n")
        f.write(f"**Validator Version:** {VALIDATOR_VERSION}\n")
        f.write(f"**Overall Status:** {overall}\n")
        f.write(f"**Rules Run:** {len(results)} | Passed: {len([r for r in results if r['status']=='PASS'])} | Failed: {len(failed)} | Warned: {len([r for r in results if r['status']=='WARN'])}\n\n")
        f.write("## Document Hashes\n\n")
        for fname, h in sorted(doc_hashes.items()):
            f.write(f"- `{fname}`: `sha256:{h[:16]}...`\n")
        if failed:
            f.write("\n## Failed Rules\n\n")
            for r in failed:
                f.write(f"- **{r['rule_id']}** `{r['document']}`: {r['evidence']}\n")
        f.write(f"\n---\n*Generated by Open Empire Governance Validator v{VALIDATOR_VERSION}*\n")

    print(f"\nOutputs written to: {out_dir}")


if __name__ == "__main__":
    main()
