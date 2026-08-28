# Open Empire Repository Factory Spec
**Version:** 1.0 | **Date:** 2026-08-09

---

## Purpose
Every repository entering Open Empire must pass a governed lifecycle, not just be cloned.

## Pipeline

```
DISCOVER → SECURITY SCAN → LICENSE CHECK → DEPENDENCY ANALYSIS
→ DUPLICATE CHECK → CAPABILITY FIT → REGISTER → INSTALL/BUILD
→ TEST → INTEGRATE → CI/CD → OBSERVE → MAINTAIN → UPGRADE → RETIRE
```

## Stage Definitions

| Stage | Gate | Tool | Output |
|---|---|---|---|
| DISCOVER | path + remote found | find + git | candidate list |
| SECURITY SCAN | no critical CVEs | gitleaks + npm audit | scan report |
| LICENSE CHECK | compatible license | license-checker | license.json |
| DEPENDENCY ANALYSIS | deps pinned, no critical | pip/npm audit | deps report |
| DUPLICATE CHECK | no existing canonical | registry query | dedup decision |
| CAPABILITY FIT | maps to ≥1 capability | manual/KG | capability tag |
| REGISTER | entity in KG + registry | kg_seed.py | UUID assigned |
| INSTALL/BUILD | builds cleanly | npm/pip/make | build log |
| TEST | tests pass or waived | pytest/jest | test report |
| INTEGRATE | service wired if needed | PM2/config | integration doc |
| CI/CD | pipeline active (UA4200) | GitHub Actions | CI status |
| OBSERVE | health check passes | PM2/healthz | uptime log |

## Classification Rules
- **CANONICAL**: In active production, PM2-managed or direct dependency of PM2 process
- **INSTALLED**: Built + available, supporting role, not PM2-primary
- **INTAKE_COPY**: Cloned for evaluation — must exit within 30 days or be promoted/archived
- **EXTERNAL_DEPENDENCY**: Upstream we don't own — track version, don't modify
- **ARCHIVE_CANDIDATE**: No active use for 60+ days, no planned use

## No Repo Goes to Production Simply Because It Was Cloned

## Current Estate (2026-08-09)
- 37 repositories catalogued
- 3 canonical, 22 installed, 4 intake, 2 external, 5 archive candidates
- 2 critical actions pending Nathan: workspace uncommitted files + open-empire-nexus remote
