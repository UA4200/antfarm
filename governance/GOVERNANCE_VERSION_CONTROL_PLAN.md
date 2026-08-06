# GOVERNANCE VERSION CONTROL PLAN

**Generated:** 2026-08-06T11:40:00-05:00  
**Artifact:** Open Empire Governance Baseline  
**Phase:** Gate A Phase 8

---

## Current State

The governance directory (`~/.openclaw/workspace/governance/`) is **not in any Git repository**. The workspace directory (`~/.openclaw/workspace/`) is also not a Git repository.

**Decision per Gate A directive:** Do not run `git init` autonomously. Identify the correct canonical repository and request Nathan approval.

---

## Recommended Integration Plan

### Option A (Recommended): Governance as subdirectory of `open-empire-core`

**Repo:** `UA4200/open-empire-core` (deployed v0.1.0-deploy-20260730)

**Rationale:**
- `open-empire-core` is the logical home for foundational empire governance artifacts
- Avoids creating a new repo (governance scope is not standalone infrastructure)
- Enables history tracking alongside core architecture decisions
- ADR-NNN records belong alongside core repo history

**Implementation steps (requires Nathan approval):**
1. Clone or locate `open-empire-core` working directory on NeoOC
2. Create `governance/` subdirectory within repo
3. Copy all 12 canonical governance files + build/ directory
4. Perform secret scan before any commit (governance files confirmed clean)
5. Initial commit: `"feat: add Governance Baseline V1.0.0-RC1"`
6. Push to `main` branch (no force push)
7. Tag: `governance-v1.0.0-rc1`

### Option B: Dedicated governance repository

**Repo:** `UA4200/open-empire-governance` (new, requires creation)

**Rationale:** Complete separation of governance from implementation. Harder to accidentally modify.

**Drawback:** Requires new repo creation, additional approval, more maintenance overhead.

### Option C: Subdirectory of `alusi-core`

**Repo:** `UA4200/alusi-core` (deployed v0.1.0-deploy-20260730)

**Rationale:** Alusi is the governance enforcer — co-location makes sense operationally.

**Drawback:** Governance is empire-wide; scoping it under alusi-core may imply incorrect ownership.

---

## Files to Version Control

All canonical governance files and generated build artifacts. **Exclude:**

| Category | Examples | Reason |
|---|---|---|
| Secrets | ~/.openclaw/secrets/.env | Credential exposure risk |
| Private keys | RSA/Ed25519 key files | Credential exposure risk |
| Trading records | trades.jsonl, arb_cycle.jsonl | Live financial data |
| Runtime databases | PostgreSQL data files | Live data |
| Logs | ~/.openclaw/logs/* | Potentially sensitive |
| API credentials | Any .env files | Security |

**Safe to commit (governance dir only):**
- All 12 OPEN_EMPIRE_*.md files
- SHA256SUMS.txt
- build/build_pipeline.py
- build/validate.py
- build/dist/*.json, *.yaml, *.dot, *.md
- build/runs/ (validation evidence — exclude if large)
- All Gate A output files generated 2026-08-06

---

## Pre-Commit Security Checklist

Before any commit to governance artifacts:
- [ ] No `*.env` files staged
- [ ] No private key files (`*.pem`, `*.key`, `id_rsa`, `id_ed25519`)
- [ ] No API token patterns in files (`sk-`, `Bearer `, API key literals)
- [ ] No IP addresses or port-specific values hardcoded as governance standards
- [ ] No PM2 process IDs embedded as canonical definitions
- [ ] No trading account IDs or balances
- [ ] No PII (Nathan's personal information beyond public operator identity)

---

## `.gitignore` Additions (recommended)

```
# Open Empire governance — exclude from governance commits
secrets/
*.env
*.key
*.pem
logs/
trades.jsonl
arb_cycle.jsonl
build/runs/*/rule_results.json  # large; keep VALIDATION_REPORT.md only
```

---

## Authorization Required

This plan requires Nathan (Sovereign Operator) approval before execution.

**Approval scope:**
1. Which repository (Option A, B, or C)?
2. First commit content scope
3. Branch strategy (main only vs governance-specific branch)
4. Tag naming convention

No git operations will be executed until approval is granted.
