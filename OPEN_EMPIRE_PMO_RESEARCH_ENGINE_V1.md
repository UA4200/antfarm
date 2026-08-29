# Open Empire PMO Research Engine V1
**Date:** 2026-08-09 | **Authority:** Nathan Asiegbu | **Status:** OPERATIONAL
**First template run:** Ruflo Evaluation 2026-08-09

---

## Doctrine

Research does NOT equal adoption.
Documented capabilities are NOT benchmarked capabilities.
README claims are NOT evidence.
Installation is NOT justified by power; it is justified by measurable advantage over what the Empire already has.

---

## Canonical Technology Evaluation Lifecycle

```
DISCOVER
  ↓
SOURCE_VALIDATE
  ↓
REPOSITORY_INTAKE          ← deterministic tools first (curl/API/git)
  ↓
SECURITY_REVIEW            ← parallel with LICENSE
  ↓
LICENSE_REVIEW             ← parallel with SECURITY
  ↓
OVERLAP_ANALYSIS           ← compare against current stack
  ↓
CAPABILITY_GAP_ANALYSIS    ← does it fill a real gap?
  ↓
SANDBOX_INSTALL            ← isolated path only (e.g. ~/.openclaw/sandbox/<name>/)
  ↓
BENCHMARK                  ← real workloads, not toy tasks
  ↓
COMPARE                    ← vs existing engines on same workloads
  ↓
ADOPT / PILOT / DEFER / REJECT
  ↓
REGISTER                   ← update all relevant registries
  ↓
RE-EVALUATE (if DEFER)     ← set cron reminder with specific trigger conditions
```

---

## Research Lanes

| Lane | Focus |
|---|---|
| GitHub | Stars, forks, issues, commit cadence, releases, security advisories |
| Official docs | Architecture, APIs, integration docs |
| Academic / papers | Any research backing capability claims |
| MCP ecosystem | MCP tool availability, integration patterns |
| Agent frameworks | Comparison with ruv, langchain, crewai, autogen, etc. |
| Model/provider | Provider support, model routing, cost implications |
| Security advisories | CVEs, GHSA, published audits |
| Industry | Adoption, case studies, real-world validation |
| Competitors | What alternatives exist |
| Regulation | Any compliance implications |

---

## Execution Pattern (Preferred)

```
DETERMINISTIC_TOOLS        → repo facts, hashes, license text, dependency lists
  +
PARALLEL_SPECIALISTS       → intake / security / overlap in parallel
  +
SINGLE_AGENT               → synthesis, sandbox install, benchmark orchestration
  +
PMO_JUDGE                  → comparison and task-class recommendation
  +
ALUSI                      → final adoption decision under governance
```

Do NOT let the candidate evaluate itself.

---

## Required Artifacts (per evaluation)

| Artifact | Contents |
|---|---|
| `<CANDIDATE>_REPOSITORY_INTAKE.json` | Canonical owner, repo URL, branch, latest commit, license, stars, issues, language, release cadence, runtime deps, documented capabilities |
| `<CANDIDATE>_SECURITY_REVIEW.json` | Findings by severity (CRITICAL/HIGH/MEDIUM/LOW), install script review, network/credential/telemetry analysis, overall risk, production clearance |
| `<CANDIDATE>_LICENSE_REVIEW.json` | SPDX identifier, internal/commercial/modification/redistribution/ADAI use analysis, attribution requirements, patent implications |
| `<CANDIDATE>_DEPENDENCY_ANALYSIS.json` | Runtime deps, dev deps, postinstall scripts, known CVEs in deps, version constraints |
| `<CANDIDATE>_CAPABILITY_OVERLAP_MATRIX.json` | Dimension scores vs existing stack, pairwise classifications, unique vs duplicated capabilities |
| `<CANDIDATE>_SANDBOX_INSTALL_REPORT.json` | Install command, version confirmed, files/processes/ports/hooks created, rollback instructions, functional test results |
| `<CANDIDATE>_BENCHMARK_RESULTS.json` | W1-W8 workload results, metrics per workload class, status per class |
| `<CANDIDATE>_COMPETITOR_COMPARISON.json` | Same workloads across competing engines, comparative metrics |
| `<CANDIDATE>_SPEED_QUALITY_COST_ANALYSIS.json` | Speed/quality/cost tradeoffs, crossover analysis, token overhead |
| `<CANDIDATE>_CAPABILITY_IMPROVEMENT_PROPOSAL.json` | Gap addressed, current baseline, proposed improvement, adoption phases, permanent exclusions |
| `<CANDIDATE>_PMO_SELECTION_POLICY.md` | When PMO should route to this engine, criteria thresholds, permanent exclusions, re-evaluation trigger |
| `<CANDIDATE>_FINAL_DECISION.md` | ADOPT/PILOT/DEFER/REJECT with full decision statements |

Plus update registries:
- `OPEN_EMPIRE_EXECUTION_ENGINE_REGISTRY_V1.json`
- `OPEN_EMPIRE_EXECUTION_STRATEGY_REGISTRY_V1.json`

---

## Decision Thresholds

| Decision | Criteria |
|---|---|
| ADOPT | Security CLEARED, license CLEARED, benchmark demonstrates measurable advantage (speed OR quality OR both), overlap acceptable, stable release |
| PILOT | Some criteria met; limited scope trial with measurement |
| DEFER | Real capabilities but blockers (unstable, overlapping, not needed yet); set re-evaluation trigger |
| REJECT | Security unresolvable, license incompatible, net capability duplication, no measurable advantage |

---

## Capability Improvement Proposal Gate

Before any sandbox install ask:

> **Does this create a measurable advantage for an approved Open Empire capability?**

- YES → create `CAPABILITY_IMPROVEMENT_PROPOSAL`, continue evaluation
- NO → archive as intelligence only; do not proceed to sandbox

---

## Research Template Files

Reusable templates at: `~/.openclaw/workspace/research/ruflo/artifacts/` (Ruflo = reference implementation)

Copy and adapt for each new candidate.

---

## Completed Evaluations

| Candidate | Date | Decision | Reason |
|---|---|---|---|
| Ruflo (claude-flow v3.34.0) | 2026-08-09 | DEFER | CLI broken (alpha deps), 4 CRITICAL security findings, substantial overlap with existing stack |

---

## Re-evaluation Queue

| Candidate | Trigger | Date |
|---|---|---|
| Ruflo | @claude-flow/cli-core exits alpha AND CRITICAL security patched | 2026-11-09 |

---

## Governance

- Research may NOT directly authorize installation
- Sandbox install requires security + license clearance
- Production adoption requires full benchmark + Nathan acceptance
- PMO owns planning; Alusi owns final acceptance
- Task Observer learns from outcomes; may propose improvements; may NOT autonomously adopt
