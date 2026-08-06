# OPEN EMPIRE LIFECYCLE STATE MACHINE V1
## Valid States and Transitions for All Open Empire Asset Types

**Version:** 1.0.0
**Status:** Draft — Pending Validation
**Owner:** Nathan (Sovereign Operator)
**Source:** `~/.openclaw/workspace/governance/OPEN_EMPIRE_ASSET_TAXONOMY_V1.md`
**Materialization Date:** 2026-08-05
**Dependencies:** OPEN_EMPIRE_ASSET_TAXONOMY_V1.md (canonical state definitions); OPEN_EMPIRE_ONTOLOGY_V1.md (relationship constraints that gate transitions)
**Revision History:**
| Version | Date | Author | Change |
|---|---|---|---|
| 1.0.0 | 2026-08-05 | Alusi | Initial materialization under Governance Freeze Order 2026-08-05 |

---

## PREAMBLE

This document is the formal lifecycle state machine for all 58 Open Empire asset types. It is derived exclusively from the `Lifecycle Applicability` fields of the OPEN_EMPIRE_ASSET_TAXONOMY_V1.md, supplemented by the validation rules and notes in each entry.

**Core principles (from Taxonomy):**
- Every asset is always in exactly **one** Lifecycle State.
- State transitions are **governed events**, not silent updates.
- Every transition must be **logged with actor and timestamp**.
- **Terminal states** (Archived, Retired, Cancelled, Closed, Dissolved, Revoked, Yanked, Disbanded, Superseded) require explicit approval.
- **Undocumented transitions** are governance violations.
- States not listed in an asset type's valid state set **may not be used** without a Taxonomy minor version update.

**Reading the transition tables:**
- "Trigger" = the event or condition that initiates the transition
- "Required Conditions" = what must be true for the transition to be valid
- "Nathan Approval Required?" = YES/No (see rules below)

**Nathan Approval Rule:**
- Any transition to: Archived, Cancelled, Closed, Dissolved, Retired, Revoked, Yanked, Disbanded, Sunset → **YES**
- First Active state for any new Venture → **YES**
- Any capital deployment change → **YES**
- Tier-0 asset retirement or decommissioning → **YES (P0-level)**
- All other transitions → **No (agent-autonomous where trigger conditions are met)**

---

# SECTION 1 — UNIVERSAL STATE DEFINITIONS

All states that appear in the Taxonomy across any asset type are defined here. This is the master state vocabulary. No asset may use a state not in this list without a Taxonomy V1.x update.

---

## ACTIVE
- **Definition:** The asset is fully operational, in normal service, and producing its intended output. The primary operating state for most asset types.
- **Entry Conditions:** All validation rules for the asset type are met; owner is assigned; governing policy/council is confirmed; required relationships are in place.
- **Exit Conditions:** A monitored degradation, intentional halt, scheduled retirement, governance decision to place On Hold, or promotion to a higher-capacity state (e.g., Scaling).
- **Permitted Actions:** All normal operations for the asset type; writes to Storage; API calls; model inference; execution of Playbooks; governance reviews.
- **Restrictions:** None during normal operation. Financial agents: constrained by spend_cap_usd. All agents: constrained by tool_access[] and policy_ids[].

---

## ARCHIVED
- **Definition:** The asset has been deliberately removed from active service and preserved for historical and audit purposes. It is read-only. No operational use.
- **Entry Conditions:** Nathan's explicit approval; Retirement State completed; archive_path confirmed; data retention policy applied; Registry retirement record created.
- **Exit Conditions:** None — Archived is a **terminal state**. Archived assets cannot be re-activated.
- **Permitted Actions:** Read-only audit access; provenance chain queries; regulatory review.
- **Restrictions:** No writes, no deployments, no new relationships. Cannot be deleted without separate P0 approval with audit log entry.

---

## AVAILABLE (Model-specific)
- **Definition:** The AI Model is accessible via its provider's API, responding within normal SLAs, and cleared for use by authorized agents.
- **Entry Conditions:** Model Provider is Active; auth credentials valid; no active rate limits.
- **Exit Conditions:** Rate limit exceeded; provider degradation; provider deprecates model.
- **Permitted Actions:** Inference calls by authorized agents; routing by Router.
- **Restrictions:** Must comply with Model Dispatch Policy; real-time chain additions require Nathan approval.

---

## BETA (Package-specific)
- **Definition:** The Package is in active development or early testing phase; not yet production-stable.
- **Entry Conditions:** Package created and importable; initial testing underway.
- **Exit Conditions:** Testing complete with no active critical issues → Stable; or critical defect → Yanked (Nathan approval).
- **Permitted Actions:** Development use; testing; non-production deployment.
- **Restrictions:** Should not be consumed by Tier-0 Services without explicit exception.

---

## BLOCKED (Project-specific)
- **Definition:** The Project cannot progress because a documented external blocker or dependency is unresolved.
- **Entry Conditions:** Project was In Progress; blocker encountered and documented with escalation target.
- **Exit Conditions:** Blocker resolved → In Progress; or situation unrecoverable → Cancelled (Nathan approval).
- **Permitted Actions:** Blocker tracking; escalation; contingency planning.
- **Restrictions:** No new deliverable work should begin until blocker is resolved.

---

## BREAKING-CHANGE-PENDING (API-specific)
- **Definition:** The API is active but a breaking change has been announced and is scheduled for deployment.
- **Entry Conditions:** Breaking change decision approved; migration plan exists.
- **Exit Conditions:** All consuming assets migrated and migration complete → Active (new version); consuming assets unable to migrate → escalate.
- **Permitted Actions:** Current version continues serving; migration work proceeds; consuming assets notified.
- **Restrictions:** No new integrations against this API version.

---

## BROKEN (Integration-specific)
- **Definition:** The Integration is completely non-functional. Requests are failing. P1 alert has been or should be triggered within 60 seconds.
- **Entry Conditions:** Integration was Degraded and failures became total; or sudden total failure from Active state.
- **Exit Conditions:** Root cause resolved and re-validated → Active; or Integration decommissioned → Deprecated (Nathan approval).
- **Permitted Actions:** Incident response; circuit breaker enforcement; alert handling.
- **Restrictions:** No new transactions through this Integration. Circuit breaker must be engaged.

---

## CANCELLED (Project-specific)
- **Definition:** The Project has been deliberately stopped before completion. No further work will proceed on this Project.
- **Entry Conditions:** Nathan's explicit approval; cancellation reason documented.
- **Exit Conditions:** None — Cancelled is a **terminal state**.
- **Permitted Actions:** Read-only access; provenance audit.
- **Restrictions:** No new work. Any produced outputs (Repositories, Services) must be reassigned or archived.

---

## CLOSED (Venture-specific)
- **Definition:** The Venture has permanently ceased operations. No further revenue generation or capital deployment.
- **Entry Conditions:** Nathan's explicit approval; all outstanding obligations settled; P&L final record archived; any active Programs wound down.
- **Exit Conditions:** None — Closed is a **terminal state**.
- **Permitted Actions:** Audit and provenance review only.
- **Restrictions:** No financial operations. No new capital deployment. All subordinate Programs must be Completed or Archived.

---

## COMPLETE (Project-specific)
- **Definition:** The Project has delivered all defined deliverables and met all completion criteria. It is successfully finished.
- **Entry Conditions:** All deliverables produced and verified; completion criteria confirmed; outputs transferred to operational ownership.
- **Exit Conditions:** May proceed to Archived (Nathan approval) when historical preservation is appropriate.
- **Permitted Actions:** Documentation; handover to operational ownership of produced assets.
- **Restrictions:** No new deliverable work. The Project as a Project is done. Its outputs live on as Services/Agents.

---

## COMPLETED (Program-specific)
- **Definition:** All Projects within the Program have reached Complete status and the Program's strategic objectives have been met.
- **Entry Conditions:** All Projects in Complete or Archived state; Business Outcomes delivered or formally assessed; Program owner confirms.
- **Exit Conditions:** May proceed to Archived (Nathan approval).
- **Permitted Actions:** Documentation; handover; transition planning.
- **Restrictions:** No new Projects added to a Completed Program without explicitly re-opening it to Active.

---

## COMPRESSING (Memory Store-specific)
- **Definition:** The Memory Store is executing its scheduled compression cycle.
- **Entry Conditions:** Compression schedule triggered (every 6 hours per Taxonomy).
- **Exit Conditions:** Compression cycle finishes → Active.
- **Permitted Actions:** Read-only agent access during compression; compression write operations.
- **Restrictions:** New delta writes are queued until compression completes. Delta writes must not exceed 300 tokens per event.

---

## CORRUPTED (Memory Store-specific)
- **Definition:** The Memory Store has a data integrity failure. Its content may not be trusted.
- **Entry Conditions:** Data integrity check fails; read errors detected.
- **Exit Conditions:** Recovery from backup → Active; irrecoverable → Archived (Nathan approval).
- **Permitted Actions:** P1 alert dispatch; backup recovery procedures; forensic read access only.
- **Restrictions:** No agent reads from Corrupted Memory Store for operational decisions. No writes.

---

## CRASHED (Runtime-specific)
- **Definition:** The Runtime has failed unexpectedly. The process is not running.
- **Entry Conditions:** Unexpected process failure; PM2 detects exit code ≠ 0; heartbeat timeout.
- **Exit Conditions:** Auto-restart triggered → Restarting; manual investigation begins.
- **Permitted Actions:** Alert dispatch (within 60 seconds); restart initiation; log collection.
- **Restrictions:** No operational traffic routed to crashed Runtime. Tier-0 Runtime crash = P0 incident.

---

## DECOMMISSIONED (Environment/Infrastructure-specific)
- **Definition:** The Environment or Infrastructure has been permanently taken out of service.
- **Entry Conditions:** Nathan's explicit approval; all Services migrated; no active processes remaining.
- **Exit Conditions:** None — Decommissioned is a **terminal state** for Environments and Infrastructure.
- **Permitted Actions:** Audit access; record keeping.
- **Restrictions:** No services may run in a decommissioned Environment.

---

## DEGRADED
- **Definition:** The asset is running but experiencing partial failures, reduced performance, or intermittent errors. Normal operations are impaired.
- **Entry Conditions:** Health check fails but asset has not fully stopped; some requests succeeding; monitoring detects anomaly.
- **Exit Conditions:** Issue resolved → Active; degradation worsens → Broken/Crashed/Stopped as applicable.
- **Permitted Actions:** Alert dispatch; incident response; diagnostic procedures.
- **Restrictions:** For Tier-0 assets: alert within 60 seconds; escalate to Nathan within 15 minutes if P0.

---

## DELEGATED (Executive Role/Ownership Role/Execution Role-specific)
- **Definition:** The Role's responsibilities have been temporarily transferred to an acting holder with documented scope and expiry.
- **Entry Conditions:** Delegation formally documented with delegating party, acting holder, scope, and expiry date.
- **Exit Conditions:** Delegation expiry reached → Active (original holder resumes); or delegation renewed.
- **Permitted Actions:** Acting holder performs within delegated scope only.
- **Restrictions:** Acting holder cannot exceed the delegated scope. Cannot re-delegate without original holder's approval.

---

## DEPRECATED
- **Definition:** The asset is no longer recommended for use and is scheduled for eventual retirement. A replacement may exist.
- **Entry Conditions:** Nathan's approval; superseding asset identified (mandatory for Standards — no deprecation without replacement).
- **Exit Conditions:** All consumers migrated → Retired or Archived (Nathan approval); superseding asset confirmed.
- **Permitted Actions:** Continued operation for existing consumers during migration window; no new consumers.
- **Restrictions:** No new Services, Agents, or systems should depend on a Deprecated asset. Deprecated packages still consumed by Active services trigger a P1 alert.

---

## DISSOLVED (Council-specific)
- **Definition:** The Council has been permanently disbanded. Its authority is transferred or relinquished.
- **Entry Conditions:** Nathan's explicit approval; no Active assets remain under Council governance; all authority transferred.
- **Exit Conditions:** None — Dissolved is a **terminal state** for Councils.
- **Permitted Actions:** Audit access; provenance.
- **Restrictions:** Cannot be Dissolved while governing any Active asset.

---

## DRAFT
- **Definition:** The asset is under development and has not yet been formally approved for active use.
- **Entry Conditions:** Asset creation initiated; no formal approval yet.
- **Exit Conditions:** Review and approval → Active; abandonment → (no formal terminal state, remains Draft or is deleted — deletion requires approval).
- **Permitted Actions:** Author/creator modifications; review process.
- **Restrictions:** Draft assets must not be deployed to production or enforced as binding rules.

---

## EMERGING (Business Capability-specific)
- **Definition:** The capability has been identified but not yet consistently delivered. It is in its earliest recognizable form.
- **Entry Conditions:** Capability concept documented; at least one enabling asset identified or proposed.
- **Exit Conditions:** Enabling assets identified and developing → Developing.
- **Permitted Actions:** Capability documentation; enabling asset identification; investment planning.
- **Restrictions:** Must not be cited as an established capability in customer or partner communications.

---

## ERRORED (PM2 Process-specific)
- **Definition:** The PM2 Process has encountered an unexpected error state. The managed Service may be non-functional.
- **Entry Conditions:** PM2 detects non-zero exit code; process failed to start or crashed.
- **Exit Conditions:** Auto-restart → Restarting; manual intervention and fix → Online.
- **Permitted Actions:** Alert dispatch; log collection; restart attempts.
- **Restrictions:** No operational traffic.

---

## ESTABLISHED (Business Capability-specific)
- **Definition:** The capability is consistently available, reliable, and in active production use across multiple Programs or Ventures.
- **Entry Conditions:** Capability has been Developing and is now consistently delivered; enabling assets are Tier-1 or better.
- **Exit Conditions:** Continuous improvement investment → Optimized; or capability investment withdrawn → Developing.
- **Permitted Actions:** All normal business operations relying on this capability.
- **Restrictions:** None.

---

## EVOLVED / STABLE (Schema Evolution-specific — post-migration)
- **Definition:** The schema has completed a migration cycle and is in a stable, consistent state again.
- **Entry Conditions:** Migration complete; all consumers updated; verification methods passed.
- **Exit Conditions:** New evolution proposed → Evolving or Breaking-Change-Pending.
- **Permitted Actions:** All normal data operations.
- **Restrictions:** None.

---

## EXPIRED (Secret Metadata-specific)
- **Definition:** The credential has reached its expiry date and is no longer valid.
- **Entry Conditions:** `expiry_at` timestamp reached; P0 alert dispatched.
- **Exit Conditions:** Renewed and rotated → Active; or decommissioned → Revoked.
- **Permitted Actions:** Emergency rotation procedures only; P0 escalation.
- **Restrictions:** No system may use an Expired credential for authentication. Any asset using Expired credentials must halt its relevant operations immediately.

---

## EXPERIMENTAL (mentioned in Taxonomy notes — valid state supplement)
- **Definition:** TODO_PENDING_APPROVAL — Not explicitly listed in any Taxonomy Lifecycle Applicability field. Reserved for future Taxonomy minor version definition if needed.

---

## FAILED
- **Definition:** The asset has encountered an error during execution that prevented normal completion. May be recoverable.
- **Entry Conditions:** Automation or Workflow step encountered unhandled exception or timeout; error logged.
- **Exit Conditions:** Error resolved and restart authorized → Active; error unresolvable → Deprecated (Nathan approval).
- **Permitted Actions:** Error diagnosis; log review; recovery attempt.
- **Restrictions:** Failed Automations must log full stack trace.

---

## FULL (Storage-specific)
- **Definition:** The Storage has reached its capacity threshold. New writes may fail.
- **Entry Conditions:** Disk or allocation threshold exceeded; P1 alert dispatched.
- **Exit Conditions:** Space freed or storage expanded → Active.
- **Permitted Actions:** Emergency cleanup; alert dispatch; storage expansion.
- **Restrictions:** No new writes until capacity is resolved. Immutable trade logs must never be deleted to free space.

---

## IN PROGRESS (Project/Migration State/Change Control-specific)
- **Definition:** Active execution work is underway.
- **Entry Conditions:** Approved work order; assigned owner; dependencies met.
- **Exit Conditions:** Work completed → Complete; unresolvable blocker → Blocked/Rolled Back; cancelled → Cancelled/Rejected (Nathan approval).
- **Permitted Actions:** All execution work; progress logging; status reporting.
- **Restrictions:** None, within approved scope.

---

## MIGRATING (Database/Schema Evolution-specific)
- **Definition:** The Database or Schema is undergoing a structural change. Operations may be partially affected.
- **Entry Conditions:** Migration script approved via Change Control; backup confirmed before start.
- **Exit Conditions:** Migration completes successfully → Active/Stable; migration fails → rollback to Active.
- **Permitted Actions:** Migration execution; monitoring; rollback preparation.
- **Restrictions:** No schema changes to the migrating object outside the approved migration script.

---

## MISCONFIGURED (Router-specific)
- **Definition:** The Router has an invalid or erroneous configuration that may cause incorrect routing.
- **Entry Conditions:** Configuration error detected; routing rules ambiguous or broken.
- **Exit Conditions:** Configuration corrected and validated → Active.
- **Permitted Actions:** Emergency configuration fix; alert dispatch.
- **Restrictions:** Misconfigured Router must not remain in production for Tier-0 routing chains.

---

## MISSED (Business Outcome-specific)
- **Definition:** The target date has passed without all success criteria being met.
- **Entry Conditions:** `target_date` reached; success criteria not confirmed; causal analysis completed.
- **Exit Conditions:** None — Missed is a **terminal state**. The Outcome is documented as Missed with causal analysis. A new Outcome may be created to replace it.
- **Permitted Actions:** Causal analysis; lessons learned; creation of replacement Outcome.
- **Restrictions:** Cannot be converted to Achieved retroactively.

---

## NOT READY (Integration Readiness-specific)
- **Definition:** The Integration has not passed any readiness checks.
- **Entry Conditions:** Initial state for any Integration before validation.
- **Exit Conditions:** Some checks pass → Partially Ready.
- **Permitted Actions:** Authentication configuration; endpoint testing.
- **Restrictions:** Must not be promoted to Active Service state.

---

## ON HOLD (Program/Venture-specific)
- **Definition:** The asset is temporarily paused. A documented reason and review date must exist.
- **Entry Conditions:** Documented reason; review date set; governing Council notified.
- **Exit Conditions:** Condition resolved → Active; or On Hold becomes permanent → Winding Down/Archived (Nathan approval).
- **Permitted Actions:** Maintenance of minimal operational state; periodic review; planning for resumption.
- **Restrictions:** No new capital deployment while On Hold (Venture). No new Projects added to an On Hold Program.

---

## ONLINE (PM2 Process-specific)
- **Definition:** The PM2 Process and its managed Service are running normally.
- **Entry Conditions:** Process started successfully; health check passing.
- **Exit Conditions:** `pm2 stop` → Stopped; unexpected failure → Errored.
- **Permitted Actions:** All normal Service operations.
- **Restrictions:** None.

---

## OPTIMIZED (Business Capability-specific)
- **Definition:** The capability is operating at peak efficiency with continuous improvement applied. The highest maturity state.
- **Entry Conditions:** Capability was Established; continuous improvement investment confirmed; performance metrics at target.
- **Exit Conditions:** Investment or enabling asset support withdrawn → Established.
- **Permitted Actions:** All capability operations at full capacity.
- **Restrictions:** None.

---

## OUTDATED (Knowledge Base/Playbook-specific)
- **Definition:** The asset's content has not been updated within its defined SLA and may no longer reflect current reality.
- **Entry Conditions:** `last_updated` or `last_validated` exceeds the defined SLA (2× measurement_frequency for KPIs; defined review cadence for Playbooks).
- **Exit Conditions:** Updated/re-validated → Active.
- **Permitted Actions:** Read access; update procedures.
- **Restrictions:** Outdated Knowledge Bases must not be used for live financial or operational decisions without explicit acknowledgment. Outdated Playbooks must not be executed for Tier-0 operations.

---

## PAUSED (Workflow/Automation-specific)
- **Definition:** The asset has been temporarily stopped. A documented reason and resume condition must exist.
- **Entry Conditions:** Manual pause or trigger condition met; reason documented; resume condition defined.
- **Exit Conditions:** Resume condition met → Active.
- **Permitted Actions:** State preservation; monitoring.
- **Restrictions:** No trigger events processed while Paused.

---

## PARTIALLY READY (Integration Readiness-specific)
- **Definition:** The Integration has passed some but not all readiness checks.
- **Entry Conditions:** At least one of the four boolean checks (auth_verified, endpoint_reachable, error_handling_tested, end_to_end_validated) is true, but not all.
- **Exit Conditions:** All checks pass → Ready.
- **Permitted Actions:** Continued validation work; non-production testing.
- **Restrictions:** Must not be promoted to Active Service state.

---

## PLANNED (Project/Service-specific)
- **Definition:** The asset has been defined and approved but work has not yet begun.
- **Entry Conditions:** Asset definition complete; owner assigned; dependencies identified; approved for execution.
- **Exit Conditions:** Work begins → In Progress (Project) / Staging (Service); cancelled before start → Cancelled (Nathan approval).
- **Permitted Actions:** Planning; dependency resolution; resource allocation.
- **Restrictions:** No active production operations.

---

## PLANNED RETIREMENT (Retirement State-specific)
- **Definition:** The retirement of an asset has been formally scheduled but not yet initiated.
- **Entry Conditions:** Nathan's approval; retirement date set; successor identified (if applicable); data retention policy decided.
- **Exit Conditions:** Decommission work begins → Retiring.
- **Permitted Actions:** Retirement planning; successor asset preparation; dependency update planning.
- **Restrictions:** No new dependencies on the asset being planned for retirement.

---

## PRE-LAUNCH (Venture-specific)
- **Definition:** The Venture has been defined and is being prepared for its first active operation. No revenue yet; no capital deployed.
- **Entry Conditions:** Venture definition complete; revenue model documented; capital allocation planned.
- **Exit Conditions:** Capital deployed, operations begun → Active (Nathan approval required).
- **Permitted Actions:** Preparation; team assembly; initial tool and system setup.
- **Restrictions:** No capital deployment without Nathan approval.

---

## RATE-LIMITED (Model-specific)
- **Definition:** The Model is accessible but call frequency has exceeded the provider's rate limits. Requests are being throttled.
- **Entry Conditions:** API returns 429; rate limit window active.
- **Exit Conditions:** Rate limit window clears → Available; or fallback to alternate model in chain.
- **Permitted Actions:** Fallback routing per Model Dispatch Policy; wait for rate limit reset.
- **Restrictions:** No additional calls to rate-limited Model until window clears.

---

## READY (Integration Readiness-specific)
- **Definition:** All four readiness boolean checks have passed. The Integration is eligible for production.
- **Entry Conditions:** auth_verified=true, endpoint_reachable=true, error_handling_tested=true, end_to_end_validated=false (one live transaction still needed for Validated).
- **Exit Conditions:** Live transaction confirmed → Validated; check regression → Partially Ready.
- **Permitted Actions:** Final production preparation.
- **Restrictions:** Not yet cleared for sustained production use — must reach Validated first.

---

## REORGANIZING (Agent Team-specific)
- **Definition:** The Agent Team is undergoing a change in membership, roles, or lead agent assignment.
- **Entry Conditions:** Member added/removed; lead agent change; coordination protocol update.
- **Exit Conditions:** Reorganization complete → Active.
- **Permitted Actions:** Team structure changes; member onboarding/offboarding.
- **Restrictions:** Collective spend cap must remain enforced during reorganization.

---

## RESTARTING (Runtime/PM2 Process-specific)
- **Definition:** The Runtime or PM2 Process is in the process of restarting after a failure or manual stop command.
- **Entry Conditions:** Crash followed by auto-restart trigger; or manual `pm2 restart`.
- **Exit Conditions:** Restart successful → Running/Online; restart fails again → Crashed/Errored.
- **Permitted Actions:** Restart monitoring; log collection.
- **Restrictions:** No operational traffic during restart.

---

## RETIRED (Business Capability/Executive Role/API/Library/Database/Storage/Agent/Service-specific)
- **Definition:** The asset has completed its operational life. It is no longer active. Archived for provenance. Not the same as Deleted.
- **Entry Conditions:** Nathan's explicit approval; Retirement State process completed; archive_path confirmed; all consuming assets migrated.
- **Exit Conditions:** None — Retired is a **terminal state**.
- **Permitted Actions:** Audit and provenance review only.
- **Restrictions:** No operational use. Retired ≠ Deleted. Deletion requires separate P0 approval with audit log.

---

## RETIRING (Retirement State-specific)
- **Definition:** Active decommissioning work is in progress. The asset is being wound down.
- **Entry Conditions:** Nathan's approval; Planned Retirement preceded this; decommission work initiated.
- **Exit Conditions:** All processes stopped and data archived → Retired.
- **Permitted Actions:** Shutdown procedures; data archival; dependency cleanup.
- **Restrictions:** No new dependencies. No new traffic or data writes.

---

## REVOKED (Secret Metadata-specific)
- **Definition:** The credential has been permanently invalidated due to a security incident or deliberate decommissioning.
- **Entry Conditions:** Nathan's explicit approval; security incident confirmed; or deliberate retirement; credential invalidated at provider.
- **Exit Conditions:** None — Revoked is a **terminal state**.
- **Permitted Actions:** Incident forensics; audit review.
- **Restrictions:** All consuming assets must remove the Revoked credential within 1 hour. Any service still using a Revoked credential is a P0 security incident.

---

## ROLLING BACK / ROLLED BACK (Migration State/Change Control-specific)
- **Definition:** An in-progress change has been reversed to restore the prior state.
- **Entry Conditions:** Nathan's approval; change failure confirmed; rollback plan exists (pre-approved).
- **Exit Conditions:** Rollback complete → Change Control Rejected; asset returns to pre-change state.
- **Permitted Actions:** Rollback execution per documented plan; validation of restored state.
- **Restrictions:** Only the pre-approved rollback plan may be executed. No improvised rollback procedures.

---

## RUNNING (Runtime-specific)
- **Definition:** The Runtime process is active, healthy, and executing normally.
- **Entry Conditions:** Process started; health check passing; PID confirmed active.
- **Exit Conditions:** `pm2 stop` → Stopped; unexpected failure → Crashed.
- **Permitted Actions:** All normal Runtime operations.
- **Restrictions:** None during normal operation.

---

## SCALING (Venture-specific)
- **Definition:** The Venture has proven its revenue model and is in active growth mode with increasing capital deployment and operational scale.
- **Entry Conditions:** At least one verified revenue event confirmed; capital allocation approved for expansion; Nathan aware.
- **Exit Conditions:** Growth targets met or new plateau → Active (mature, steady state); growth reversed → On Hold (Nathan notification); or winding down → Winding Down (Nathan approval).
- **Permitted Actions:** Increased capital deployment within approved caps; team expansion; new Program initiation.
- **Restrictions:** Daily spend caps still enforced absolutely. No cap removal without Nathan explicit approval.

---

## STABLE (Package-specific and Schema Evolution-specific)
- **Definition:** (Package): The Package is production-ready, tested, and reliable for use by Active services. (Schema Evolution): The schema is in a consistent state with no active evolution in progress.
- **Entry Conditions:** (Package): Testing complete; no critical open issues; semantic version confirmed. (Schema Evolution): Last migration completed successfully.
- **Exit Conditions:** New major version needed → Breaking-Change-Pending; additive change → Evolving.
- **Permitted Actions:** All normal operations.
- **Restrictions:** None.

---

## STAGING (Service-specific)
- **Definition:** The Service has been deployed to a pre-production environment and is undergoing validation before promotion to Active.
- **Entry Conditions:** Deployment complete in staging environment; Integration Readiness assessment underway.
- **Exit Conditions:** Integration Readiness = Validated → Active; validation failure → Planned (re-work needed).
- **Permitted Actions:** Testing; integration validation; performance profiling.
- **Restrictions:** No production traffic. Staging must not use production secrets.

---

## STARTING (Runtime-specific)
- **Definition:** The Runtime is in the process of initializing.
- **Entry Conditions:** `pm2 start` command or restart triggered.
- **Exit Conditions:** Initialization complete → Running; initialization failure → Crashed.
- **Permitted Actions:** Initialization procedures.
- **Restrictions:** No operational traffic until Running.

---

## STALE (Registry-specific)
- **Definition:** The Registry has not been updated within its defined SLA (>24h for live assets) and may not reflect the current state of governed assets.
- **Entry Conditions:** `last_sync_at` timestamp exceeds the stale threshold.
- **Exit Conditions:** Sync triggered and completed → Active.
- **Permitted Actions:** Stale data display with explicit staleness warning; sync trigger.
- **Restrictions:** Stale Registry must not be used as the authoritative source for financial decisions.

---

## STOPPED (Runtime/Service/PM2 Process/Dashboard-specific)
- **Definition:** The asset has been intentionally halted. STOPPED ≠ ERRORED. STOPPED = deliberate operational decision.
- **Entry Conditions:** Intentional shutdown command; maintenance window; or deliberate operational decision.
- **Exit Conditions:** Manual restart → Running/Online/Active.
- **Permitted Actions:** Data review; maintenance; restart preparation.
- **Restrictions:** No operational traffic. For intentionally STOPPED services (e.g., email-dispatcher), no automatic restart without explicit operator instruction.

---

## SUPERSEDED (Business Outcome/Standard/Policy/Library/Target State/Retirement State-specific)
- **Definition:** The asset has been formally replaced by a newer version or successor. The supersession record is permanent.
- **Entry Conditions:** Nathan's approval; successor identified; Supersession record created in Registry.
- **Exit Conditions:** None — Superseded is a **terminal state**.
- **Permitted Actions:** Audit and provenance review. The supersession record itself is immutable and permanent.
- **Restrictions:** No operational use. All references must be updated to the successor within 30 days.

---

## SUSPENDED (Council/Agent-specific)
- **Definition:** The Council or Agent has been temporarily halted from its normal operations. The suspension reason and conditions for resumption must be documented.
- **Entry Conditions:** Policy violation; security investigation; or deliberate governance decision; suspension reason documented.
- **Exit Conditions:** Suspension condition resolved → Active; or permanent → Dissolved/Retired (Nathan approval).
- **Permitted Actions:** Investigation; documentation of suspension reason and resume conditions.
- **Restrictions:** Suspended Council cannot issue new governance decisions. Suspended Agent cannot execute operations or make financial transactions.

---

## TARGETED (Business Outcome-specific)
- **Definition:** The Business Outcome has been defined and approved as a goal but not yet achieved or assessed.
- **Entry Conditions:** Success criteria documented; linked KPIs identified; target date set.
- **Exit Conditions:** All success criteria confirmed → Achieved; target date passed without criteria met → Missed; objective replaced → Superseded.
- **Permitted Actions:** Work toward achievement; KPI tracking; progress reporting.
- **Restrictions:** None.

---

## TESTING (Agent-specific)
- **Definition:** The Agent has been developed and is undergoing validation in a test environment before production activation.
- **Entry Conditions:** Agent development complete; policy_ids defined; test environment ready.
- **Exit Conditions:** All tests passed → Active (Nathan approval required if financial agent); testing fails → Draft (rework).
- **Permitted Actions:** Test execution; policy validation; tool access verification.
- **Restrictions:** No production data. No real financial transactions.

---

## UNAVAILABLE (Model/Model Provider-specific)
- **Definition:** The Model or Model Provider is completely inaccessible.
- **Entry Conditions:** API returns 5xx; connection timeout; provider outage confirmed.
- **Exit Conditions:** Service restored → Available/Active.
- **Permitted Actions:** Fallback routing per Model Dispatch Policy; incident tracking.
- **Restrictions:** No calls to Unavailable Model/Provider. Routing chain must activate fallback.

---

## UNDER REVIEW (Policy-specific)
- **Definition:** The Policy is in a formal review cycle. It remains in effect until the review concludes.
- **Entry Conditions:** Scheduled review cadence reached; or triggered by an incident or request.
- **Exit Conditions:** Review confirms policy is correct → Active; review recommends changes → Under Review continues until Deprecated/Superseded.
- **Permitted Actions:** Policy continues to be enforced during review. Review documentation produced.
- **Restrictions:** Policy may not be silently amended during review without formal versioning.

---

## VACANT (Executive Role/Ownership Role/Execution Role-specific)
- **Definition:** The Role exists but has no holder. It is ungoverned.
- **Entry Conditions:** Previous holder departed or was removed; no replacement assigned yet.
- **Exit Conditions:** New holder assigned → Active.
- **Permitted Actions:** Escalation to parent role; emergency coverage by higher authority.
- **Restrictions:** Tier-0 assets with Vacant Ownership Roles are governance violations requiring immediate remediation. P0-critical recurring Execution Roles cannot remain Vacant.

---

## VALIDATED (Integration Readiness-specific)
- **Definition:** The Integration has completed at least one successful live transaction and is cleared for sustained production use.
- **Entry Conditions:** All four readiness checks passed (Ready state) AND at least one live transaction confirmed.
- **Exit Conditions:** Integration failure → Degraded; full failure → Not Ready (requires re-validation).
- **Permitted Actions:** Full production operations.
- **Restrictions:** Must be re-validated after every API version change.

---

## WINDING DOWN (Venture-specific)
- **Definition:** The Venture is in an active, deliberate shut-down process. Capital deployment is decreasing. Operations are being concluded.
- **Entry Conditions:** Nathan's explicit approval; wind-down plan documented; timeline established.
- **Exit Conditions:** All operations concluded → Closed (Nathan approval).
- **Permitted Actions:** Concluding operations; P&L finalization; asset disposal.
- **Restrictions:** No new capital deployment. No new Programs or Projects initiated.

---

## YANKED (Package-specific)
- **Definition:** The Package version has been removed from availability due to a critical defect or security issue.
- **Entry Conditions:** Nathan's explicit approval; critical defect or security vulnerability confirmed.
- **Exit Conditions:** None — Yanked is a **terminal state** for that Package version.
- **Permitted Actions:** Emergency replacement procedures.
- **Restrictions:** All consuming Services must remove the Yanked Package within 24 hours. Any Service still consuming a Yanked Package after 24 hours is a P1 incident.

---

# SECTION 2 — PER-ASSET STATE MACHINES

---

## LAYER 1 — BUSINESS

---

## Portfolio

**Valid States:** Active · Archived
**Initial State:** Active (Portfolios are created Active)
**Terminal States:** Archived

### Transition Table
| From State | To State | Trigger | Required Conditions | Nathan Approval Required? |
|---|---|---|---|---|
| Active | Archived | All Programs/Ventures Completed or Closed; Portfolio purpose fulfilled | No active Programs or Ventures; owner confirms; Registry updated | **YES** |

---

## Program

**Valid States:** Planned · Active · On Hold · Completed · Archived
**Initial State:** Planned
**Terminal States:** Archived

### Transition Table
| From State | To State | Trigger | Required Conditions | Nathan Approval Required? |
|---|---|---|---|---|
| Planned | Active | Program execution begins | At least one Project assigned; owner confirmed as active Executive Role; governing Council confirmed | No |
| Active | On Hold | Blocker, resource constraint, or strategic pause | Documented reason; review date set; Council notified | No |
| Active | Completed | All Projects complete; objectives met | All child Projects in Complete or Archived state; Business Outcomes assessed | No |
| On Hold | Active | Blocker resolved; review date reached | Documented resolution of hold condition | No |
| On Hold | Archived | Program not resuming | Nathan approval; all Projects concluded | **YES** |
| Completed | Archived | Program fully archived | Nathan approval; all outputs transferred to operational ownership | **YES** |
| Active | Archived | Program cancelled mid-execution | Nathan approval; Projects disposed of | **YES** |

---

## Project

**Valid States:** Planned · In Progress · Blocked · Complete · Cancelled
**Initial State:** Planned
**Terminal States:** Complete · Cancelled

### Transition Table
| From State | To State | Trigger | Required Conditions | Nathan Approval Required? |
|---|---|---|---|---|
| Planned | In Progress | Work begins | Owner assigned; deliverables defined; start_date reached; risk_level assigned | No |
| In Progress | Blocked | Blocker encountered | Blocker documented; escalation target identified | No |
| Blocked | In Progress | Blocker resolved | Documented resolution | No |
| In Progress | Complete | All deliverables produced | All deliverables produced and verified; completion criteria met; outputs transferred to operational ownership | No |
| In Progress | Cancelled | Project abandoned | Nathan approval; cancellation reason documented | **YES** |
| Blocked | Cancelled | Unresolvable blocker | Nathan approval; cancellation reason documented | **YES** |
| Planned | Cancelled | Project cancelled before start | Nathan approval | **YES** |
| Complete | (Archived via Program) | Program archives | See Program → Archived | **YES** |

---

## Business Capability

**Valid States:** Emerging · Developing · Established · Optimized · Retired
**Initial State:** Emerging
**Terminal States:** Retired

### Transition Table
| From State | To State | Trigger | Required Conditions | Nathan Approval Required? |
|---|---|---|---|---|
| Emerging | Developing | Enabling assets identified and being built | At least one enabling asset (Service/Agent/Integration) identified or under development | No |
| Developing | Established | Capability consistently delivered | Enabling assets Active; capability reliably available across Programs | No |
| Established | Optimized | Continuous improvement investment confirmed | Performance metrics at target; active improvement program | No |
| Optimized | Established | Investment or improvement withdrawn | Formal decision to deprioritize optimization | No |
| Establishing | Developing | Enabling asset fails or is retired | Primary enabling asset lost; backup not available | No |
| Any Active State | Retired | Capability no longer needed; enabling assets retiring | Nathan approval; all Programs using capability migrated or closed | **YES** |

---

## Venture

**Valid States:** Pre-Launch · Active · Scaling · On Hold · Winding Down · Closed
**Initial State:** Pre-Launch
**Terminal States:** Closed

### Transition Table
| From State | To State | Trigger | Required Conditions | Nathan Approval Required? |
|---|---|---|---|---|
| Pre-Launch | Active | Capital deployed; first operations begin | Capital deployed; revenue model confirmed; daily_spend_cap_usd set; Council confirmed | **YES (first Active state)** |
| Active | Scaling | Revenue model validated | At least one verified revenue event confirmed; scaling plan approved | No (but Nathan notified) |
| Active | On Hold | Strategic pause | Documented reason; review date; Council notified; capital deployment suspended | No |
| Scaling | On Hold | Growth reversed or paused | Documented reason; review date | No |
| On Hold | Active | Hold condition resolved | Documented resolution | No |
| Active | Winding Down | Decision to close Venture | Nathan approval; wind-down plan documented | **YES** |
| Scaling | Winding Down | Decision to close Venture | Nathan approval; wind-down plan documented | **YES** |
| On Hold | Winding Down | Decision to not resume | Nathan approval | **YES** |
| Winding Down | Closed | All operations concluded | Nathan approval; P&L finalized; all assets transferred or retired | **YES** |

---

## Executive KPI

**Valid States:** Active · Deprecated
**Initial State:** Active
**Terminal States:** Deprecated

### Transition Table
| From State | To State | Trigger | Required Conditions | Nathan Approval Required? |
|---|---|---|---|---|
| Active | Deprecated | KPI no longer relevant; replaced by better metric | Nathan approval; replacement KPI identified (if applicable); all dashboards updated | **YES** |

---

## Business Outcome

**Valid States:** Targeted · Achieved · Missed · Superseded
**Initial State:** Targeted
**Terminal States:** Achieved · Missed · Superseded

### Transition Table
| From State | To State | Trigger | Required Conditions | Nathan Approval Required? |
|---|---|---|---|---|
| Targeted | Achieved | All success criteria confirmed | All `success_criteria[]` verified with Verified evidence_state; Council confirms | No |
| Targeted | Missed | Target date passes without criteria met | `target_date` reached; causal analysis documented | No |
| Targeted | Superseded | Objective replaced by updated outcome | Nathan approval; superseding Outcome created | **YES** |

---

## LAYER 2 — GOVERNANCE

---

## Council

**Valid States:** Active · Suspended · Dissolved
**Initial State:** Active
**Terminal States:** Dissolved

### Transition Table
| From State | To State | Trigger | Required Conditions | Nathan Approval Required? |
|---|---|---|---|---|
| Active | Suspended | Governance issue; investigation | Documented suspension reason; authority temporarily transferred | No (Nathan informed) |
| Suspended | Active | Suspension condition resolved | Documented resolution | No |
| Active | Dissolved | Council no longer needed | Nathan approval; no Active assets governed; all authority transferred | **YES** |
| Suspended | Dissolved | Council permanently closed | Nathan approval; all governed assets re-assigned | **YES** |

---

## Executive Role

**Valid States:** Active · Vacant · Delegated · Retired
**Initial State:** Active
**Terminal States:** Retired

### Transition Table
| From State | To State | Trigger | Required Conditions | Nathan Approval Required? |
|---|---|---|---|---|
| Active | Vacant | Holder departs or is unavailable | Escalation path activated; acting holder assigned if possible | No |
| Vacant | Active | New holder assigned | Named holder confirmed; authority_scope defined | No |
| Active | Delegated | Temporary delegation | Delegation documented: scope, acting_holder, expiry_date | No |
| Delegated | Active | Delegation expires or is revoked | Delegation expiry reached or original holder resumes | No |
| Active | Retired | Role abolished | Nathan approval; no assets remain under this role's authority | **YES** |

---

## Ownership Role

**Valid States:** Active · Delegated · Vacant
**Initial State:** Active
**Terminal States:** None (Roles persist; an Ownership Role for a retired asset becomes Vacant pending reassignment)

### Transition Table
| From State | To State | Trigger | Required Conditions | Nathan Approval Required? |
|---|---|---|---|---|
| Active | Delegated | Temporary delegation | Documented scope, holder, and expiry | No |
| Delegated | Active | Delegation expires | Expiry date reached | No |
| Active | Vacant | Holder unavailable | Escalation to Executive Role; acting holder sought | No |
| Vacant | Active | New holder assigned | Named holder confirmed | No |

---

## Standard

**Valid States:** Draft · Active · Deprecated · Superseded
**Initial State:** Draft
**Terminal States:** Superseded

### Transition Table
| From State | To State | Trigger | Required Conditions | Nathan Approval Required? |
|---|---|---|---|---|
| Draft | Active | Formal Council approval | Issuing Council approval; version number assigned; at least one Verification Method defined | No |
| Active | Deprecated | Superseding Standard in development | Superseding Standard identified; deprecation notice issued | No (Council decision) |
| Active | Superseded | Superseding Standard goes Active | Superseding Standard is now Active; all references updated | No (Council decision) |
| Deprecated | Superseded | Superseding Standard confirmed | Formal Supersession record created | No |

---

## Policy

**Valid States:** Draft · Active · Under Review · Deprecated · Superseded
**Initial State:** Draft
**Terminal States:** Superseded

### Transition Table
| From State | To State | Trigger | Required Conditions | Nathan Approval Required? |
|---|---|---|---|---|
| Draft | Active | Council approval | Issuing Council approval; enforcement_mechanism defined; scope defined | No |
| Active | Under Review | Scheduled review or incident triggers | Review initiated; Policy continues to be enforced during review | No |
| Under Review | Active | Review concludes; Policy confirmed valid | Review documentation completed | No |
| Under Review | Deprecated | Review recommends retirement | Nathan approval; replacement Policy identified | **YES** |
| Active | Deprecated | Policy replaced | Nathan approval; superseding Policy identified | **YES** |
| Active | Superseded | New version issued | Superseding Policy version activated; Supersession record created | No (Council) |
| Deprecated | Superseded | Replacement confirmed active | Formal Supersession record | No |

---

## Playbook

**Valid States:** Draft · Active · Outdated · Deprecated
**Initial State:** Draft
**Terminal States:** Deprecated

### Transition Table
| From State | To State | Trigger | Required Conditions | Nathan Approval Required? |
|---|---|---|---|---|
| Draft | Active | Validation complete | At least one Policy implemented; steps defined; expected_outputs defined; last_validated set | No |
| Active | Outdated | last_validated exceeds SLA | Validation SLA exceeded | No (automatic) |
| Outdated | Active | Re-validated | Steps verified against current state; last_validated updated | No |
| Active | Deprecated | Playbook replaced or obsolete | Nathan approval; replacement Playbook or automation gap noted | **YES** |
| Outdated | Deprecated | Not worth re-validating | Nathan approval | **YES** |

---

## Approval Type

**Valid States:** Active · Deprecated
**Initial State:** Active
**Terminal States:** Deprecated

### Transition Table
| From State | To State | Trigger | Required Conditions | Nathan Approval Required? |
|---|---|---|---|---|
| Active | Deprecated | Approval Type replaced or obsolete | Nathan approval; no active Policy references remaining | **YES** |

---

## Risk Level

**Lifecycle Note:** Risk Level is a canonical enumeration (P0–P4). It is not subject to individual lifecycle management. All five levels (P0, P1, P2, P3, P4) remain Active as defined constants. Risk Level entries in the Registry are assigned values, not individual assets with their own lifecycles.

---

## Lifecycle State

**Lifecycle Note:** This asset type IS the lifecycle definition. It does not have its own lifecycle. It is permanently Active as the master state taxonomy.

---

## Evidence State

**Lifecycle Note:** Evidence State is a canonical enumeration (Verified, Asserted, Estimated, Unverified, Stale). It is not subject to individual lifecycle management. All five values remain Active as defined constants.

---

## LAYER 3 — ENGINEERING

---

## Repository

**Valid States:** Active · Archived · Deprecated
**Initial State:** Active
**Terminal States:** Archived

### Transition Table
| From State | To State | Trigger | Required Conditions | Nathan Approval Required? |
|---|---|---|---|---|
| Active | Deprecated | Repository no longer maintained; no active consumers | All consuming Services migrated; git_initialized confirmed | No |
| Active | Archived | Project complete; code preserved | Nathan approval; all outputs migrated; archive_path confirmed | **YES** |
| Deprecated | Archived | All consumers migrated | Nathan approval; no remaining dependents | **YES** |

---

## Package

**Valid States:** Stable · Beta · Deprecated · Yanked
**Initial State:** Beta
**Terminal States:** Yanked

### Transition Table
| From State | To State | Trigger | Required Conditions | Nathan Approval Required? |
|---|---|---|---|---|
| Beta | Stable | Testing complete | No critical issues; semantic version confirmed; dependency list verified | No |
| Stable | Deprecated | Newer version available | Replacement Package identified; deprecation notice issued | No |
| Deprecated | Yanked | Critical security issue discovered | Nathan approval; all consuming Services notified | **YES** |
| Beta | Yanked | Critical defect discovered | Nathan approval | **YES** |
| Yanked | (no transition) | Terminal state | — | — |

---

## Library

**Valid States:** Active · Deprecated · Superseded
**Initial State:** Active
**Terminal States:** Superseded

### Transition Table
| From State | To State | Trigger | Required Conditions | Nathan Approval Required? |
|---|---|---|---|---|
| Active | Deprecated | Newer version or replacement available | Replacement Library identified; consuming assets notified | No |
| Deprecated | Superseded | Replacement confirmed active and all consumers migrated | Supersession record created; all consumers migrated | No |
| Active | Superseded | Immediate replacement with direct cutover | Supersession record created | No |

**Note:** `trading.shared.kelly` carries the KELLY NO-FIX constraint. Its Library entry may not transition to Deprecated or Superseded without Nathan's explicit directive. This constraint is permanent until explicitly overridden.

---

## Framework

**Valid States:** Active · Deprecated · Upgrading
**Initial State:** Active
**Terminal States:** Deprecated

### Transition Table
| From State | To State | Trigger | Required Conditions | Nathan Approval Required? |
|---|---|---|---|---|
| Active | Upgrading | Version upgrade initiated | Change Control approved; rollback plan defined; impact analysis of consuming_assets[] complete | No (Change Control governs) |
| Upgrading | Active | Upgrade complete and validated | All consuming assets verified; health checks passing | No |
| Upgrading | Active (rollback) | Upgrade failure | Rollback plan executed; prior version restored | No (but Nathan informed) |
| Active | Deprecated | Framework replaced | Nathan approval; all consuming assets migrated; replacement identified | **YES** |

---

## Model

**Valid States:** Available · Deprecated · Unavailable · Rate-Limited
**Initial State:** Available
**Terminal States:** Deprecated

### Transition Table
| From State | To State | Trigger | Required Conditions | Nathan Approval Required? |
|---|---|---|---|---|
| Available | Rate-Limited | API returns 429 | Rate limit window active | No (automatic) |
| Rate-Limited | Available | Rate limit window clears | Rate limit reset confirmed | No (automatic) |
| Available | Unavailable | Provider outage | API unreachable; fallback routing activates | No (automatic) |
| Unavailable | Available | Provider restored | API responding; fallback routing deactivates | No (automatic) |
| Available | Deprecated | Provider deprecates model | Nathan approval; consuming agents updated to use replacement | **YES** |

---

## Model Provider

**Valid States:** Active · Degraded · Unavailable
**Initial State:** Active
**Terminal States:** None (providers are external; their states are observed, not governed)

### Transition Table
| From State | To State | Trigger | Required Conditions | Nathan Approval Required? |
|---|---|---|---|---|
| Active | Degraded | Partial service disruption | API errors; increased latency; fallback routing engaged | No (automatic) |
| Degraded | Active | Service restored | API responding normally; fallback routing deactivated | No (automatic) |
| Active | Unavailable | Full outage | Total API inaccessibility | No (automatic) |
| Unavailable | Active | Service restored | Full API access restored | No (automatic) |
| Degraded | Unavailable | Degradation worsens to total failure | Total inaccessibility detected | No (automatic) |

---

## API

**Valid States:** Active · Deprecated · Breaking-Change-Pending · Retired
**Initial State:** Active
**Terminal States:** Retired

### Transition Table
| From State | To State | Trigger | Required Conditions | Nathan Approval Required? |
|---|---|---|---|---|
| Active | Breaking-Change-Pending | Breaking change announced | Change Control approved; migration plan exists; consuming assets notified | No |
| Breaking-Change-Pending | Active | Migration complete | All consuming assets migrated and validated on new version | No |
| Active | Deprecated | Newer version available | No new integrations; migration timeline set | No |
| Deprecated | Retired | All consumers migrated | Nathan approval; no remaining consuming assets | **YES** |

---

## Router

**Valid States:** Active · Degraded · Misconfigured
**Initial State:** Active
**Terminal States:** None (Routers are persistent infrastructure components)

### Transition Table
| From State | To State | Trigger | Required Conditions | Nathan Approval Required? |
|---|---|---|---|---|
| Active | Degraded | One or more route targets failing | Fallback routing engaged; alert dispatched | No (automatic) |
| Degraded | Active | Route targets restored | All routing rules functioning | No |
| Active | Misconfigured | Configuration error detected | Alert dispatched immediately | No (automatic) |
| Misconfigured | Active | Configuration corrected and validated | Routing rules tested; deterministic routing confirmed | No |

---

## Integration

**Valid States:** Active · Degraded · Broken · Deprecated
**Initial State:** Active (after Integration Readiness = Validated)
**Terminal States:** Deprecated

### Transition Table
| From State | To State | Trigger | Required Conditions | Nathan Approval Required? |
|---|---|---|---|---|
| Active | Degraded | Intermittent failures detected | Alert dispatched; monitoring increased | No (automatic) |
| Degraded | Active | Issues resolved | All checks passing; circuit breaker reset | No |
| Degraded | Broken | Failures become total | P1 alert within 60 seconds; circuit breaker engaged | No (automatic) |
| Broken | Active | Root cause resolved; re-validated | Integration Readiness re-validated; at least one successful live transaction | No |
| Active | Deprecated | Integration to be decommissioned | Nathan approval; consuming assets migrated | **YES** |

---

## Environment

**Valid States:** Active · Decommissioned
**Initial State:** Active
**Terminal States:** Decommissioned

### Transition Table
| From State | To State | Trigger | Required Conditions | Nathan Approval Required? |
|---|---|---|---|---|
| Active | Decommissioned | All services migrated; environment no longer needed | Nathan approval; all Services migrated out; no running processes; secrets scope removed | **YES** |

---

## Infrastructure

**Valid States:** Active · Degraded · Maintenance · Decommissioned
**Initial State:** Active
**Terminal States:** Decommissioned

### Transition Table
| From State | To State | Trigger | Required Conditions | Nathan Approval Required? |
|---|---|---|---|---|
| Active | Maintenance | Scheduled maintenance window | Maintenance schedule approved; services migrated or stopped | No |
| Maintenance | Active | Maintenance complete | All services restored; health checks passing | No |
| Active | Degraded | Performance or availability issue | Alert dispatched; incident response initiated | No (automatic) |
| Degraded | Active | Issue resolved | Performance restored; health checks passing | No |
| Any | Decommissioned | Infrastructure end-of-life | Nathan approval; all services migrated; data archived | **YES** |

---

## Database

**Valid States:** Active · Migrating · Degraded · Retired
**Initial State:** Active
**Terminal States:** Retired

### Transition Table
| From State | To State | Trigger | Required Conditions | Nathan Approval Required? |
|---|---|---|---|---|
| Active | Migrating | Schema migration initiated | Change Control approved; backup confirmed; rollback plan documented | No |
| Migrating | Active | Migration complete | Migration script succeeded; all queries tested; data integrity verified | No |
| Active | Degraded | Connection/performance issue | P0 alert dispatched; incident response initiated | No (automatic) |
| Degraded | Active | Issue resolved | All connections restored; performance normalized | No |
| Active | Retired | Database end-of-life | Nathan approval (P0-level); all consuming services migrated; data archived | **YES (P0)** |

---

## Storage

**Valid States:** Active · Archiving · Full · Retired
**Initial State:** Active
**Terminal States:** Retired

### Transition Table
| From State | To State | Trigger | Required Conditions | Nathan Approval Required? |
|---|---|---|---|---|
| Active | Archiving | Archival job triggered | Archival automation running; read-only mode for archiving path | No |
| Archiving | Active | Archival complete | Job succeeded; space reclaimed or archive confirmed | No |
| Active | Full | Capacity threshold reached | P1 alert dispatched; emergency cleanup initiated | No (automatic) |
| Full | Active | Space freed or expanded | Capacity below threshold | No |
| Active | Retired | Storage end-of-life | Nathan approval; all data migrated or disposed of per retention policy | **YES** |

---

## Secret Metadata

**Valid States:** Active · Rotating · Expired · Revoked
**Initial State:** Active
**Terminal States:** Revoked

### Transition Table
| From State | To State | Trigger | Required Conditions | Nathan Approval Required? |
|---|---|---|---|---|
| Active | Rotating | Rotation schedule reached or manual trigger | Rotation Playbook initiated; new credential ready | No |
| Rotating | Active | Rotation complete | New credential validated; all consuming assets updated; old credential invalidated | No |
| Active | Expired | `expiry_at` timestamp reached | P0 alert dispatched immediately | No (automatic — alert is immediate) |
| Expired | Active | Renewed and rotated | New credential obtained; rotation complete | No |
| Any State | Revoked | Security incident or deliberate decommission | Nathan approval; credential immediately invalidated at provider; all consumers notified within 1 hour | **YES** |

---

## LAYER 4 — OPERATIONS

---

## Runtime

**Valid States:** Running · Starting · Stopped · Crashed · Restarting
**Initial State:** Starting (transitions to Running on success)
**Terminal States:** Stopped (intentional — can restart)

### Transition Table
| From State | To State | Trigger | Required Conditions | Nathan Approval Required? |
|---|---|---|---|---|
| Starting | Running | Process initialized | PID active; health check passing; dependencies confirmed | No |
| Starting | Crashed | Startup failure | Non-zero exit code; error logged | No (automatic — alert dispatched) |
| Running | Stopped | `pm2 stop` command | Intentional shutdown | No |
| Running | Crashed | Unexpected failure | Non-zero exit; process exited unexpectedly; P0/P1 alert | No (automatic) |
| Crashed | Restarting | Auto-restart trigger | PM2 restart_policy activated | No (automatic) |
| Restarting | Running | Restart successful | Process running; health check passing | No |
| Restarting | Crashed | Restart failed | Non-zero exit again; max_restarts exceeded | No (automatic — escalate if Tier-0) |
| Stopped | Starting | Manual start / `pm2 start` | Explicit operator command | No |

---

## Service

**Valid States:** Planned · Staging · Active · Degraded · Stopped · Retired
**Initial State:** Planned
**Terminal States:** Retired

### Transition Table
| From State | To State | Trigger | Required Conditions | Nathan Approval Required? |
|---|---|---|---|---|
| Planned | Staging | Deployment to staging environment | PM2 id assigned; tier defined; owner_role_id set | No |
| Staging | Active | Integration Readiness validated | Integration Readiness = Validated; health_check_url responding; restart_policy set | No |
| Active | Degraded | Health check failing | Alert dispatched within 60 seconds for Tier-0 | No (automatic) |
| Degraded | Active | Issue resolved | Health checks passing; all dependencies restored | No |
| Active | Stopped | Intentional shutdown | `pm2 stop` command; operational decision | No |
| Stopped | Active | Restart | `pm2 restart` or `pm2 start` | No |
| Active | Retired | Service end-of-life | Nathan approval; all consumers migrated; PM2 process removed | **YES** |
| Stopped | Retired | Service permanently halted | Nathan approval | **YES** |

---

## PM2 Process

**Valid States:** Online · Stopped · Errored · Restarting
**Initial State:** Online (after successful start)
**Terminal States:** Stopped (intentional) — Note: PM2 IDs are never reused after deletion.

### Transition Table
| From State | To State | Trigger | Required Conditions | Nathan Approval Required? |
|---|---|---|---|---|
| Online | Stopped | `pm2 stop <id>` | Intentional halt | No |
| Online | Errored | Unexpected process failure | Non-zero exit; error logged | No (automatic — alert) |
| Errored | Restarting | Auto-restart policy triggers | Restart attempt initiated | No (automatic) |
| Restarting | Online | Restart successful | Process running; status=online in pm2 list | No |
| Restarting | Errored | Restart fails | Non-zero exit again | No (automatic) |
| Stopped | Online | `pm2 start` or `pm2 restart` | Explicit command | No |

---

## Workflow

**Valid States:** Active · Paused · Deprecated · Failed
**Initial State:** Active
**Terminal States:** Deprecated

### Transition Table
| From State | To State | Trigger | Required Conditions | Nathan Approval Required? |
|---|---|---|---|---|
| Active | Paused | Manual pause or trigger condition met | Reason documented; resume condition defined | No |
| Paused | Active | Resume condition met | Condition documented and confirmed | No |
| Active | Failed | Step failure during execution | Failed step and error logged; retry policy exhausted | No (automatic) |
| Failed | Active | Error resolved; Workflow restarted | Root cause fixed; restart authorized | No |
| Active | Deprecated | Workflow replaced or obsolete | Nathan approval; replacement workflow or procedure identified | **YES** |

---

## Automation

**Valid States:** Active · Paused · Failed · Deprecated
**Initial State:** Active
**Terminal States:** Deprecated

### Transition Table
| From State | To State | Trigger | Required Conditions | Nathan Approval Required? |
|---|---|---|---|---|
| Active | Paused | Manual pause | Documented reason; resume condition defined | No |
| Paused | Active | Resume condition met | Condition confirmed; Automation restarted | No |
| Active | Failed | Execution error | Error logged with full stack trace; retry policy exhausted | No (automatic) |
| Failed | Active | Error resolved | Fix deployed; Automation restarted and validated | No |
| Active | Deprecated | Automation replaced or obsolete | Nathan approval | **YES** |

---

## Agent

**Valid States:** Draft · Testing · Active · Suspended · Retired
**Initial State:** Draft
**Terminal States:** Retired

### Transition Table
| From State | To State | Trigger | Required Conditions | Nathan Approval Required? |
|---|---|---|---|---|
| Draft | Testing | Development complete | policy_ids defined; model_id confirmed; tool_access[] defined; test environment ready | No |
| Testing | Active | All tests passed | All policy tests passed; spend_cap_usd set (if financial); owner_role_id set | **YES (if financial agent)** / No (non-financial) |
| Active | Suspended | Policy violation; security concern; or deliberate governance decision | Suspension reason documented; Suspension logged | No (but Nathan informed immediately for P0/P1) |
| Suspended | Active | Suspension condition resolved | Nathan approval (if triggered by policy violation); documented resolution | **YES (if policy violation)** / No (if manual) |
| Active | Retired | Agent end-of-life | Nathan approval; all tasks reassigned; PM2 process removed if applicable | **YES** |
| Suspended | Retired | Agent permanently closed | Nathan approval | **YES** |

---

## Agent Team

**Valid States:** Active · Reorganizing · Disbanded
**Initial State:** Active
**Terminal States:** Disbanded

### Transition Table
| From State | To State | Trigger | Required Conditions | Nathan Approval Required? |
|---|---|---|---|---|
| Active | Reorganizing | Member addition/removal or lead agent change | Reorganization plan documented; collective_spend_cap_usd confirmed | No |
| Reorganizing | Active | Reorganization complete | New composition confirmed; Council approval | No |
| Active | Disbanded | Team no longer needed | Nathan approval; all member Agents reassigned or retired | **YES** |

---

## Dashboard

**Valid States:** Active · Degraded · Stopped
**Initial State:** Active
**Terminal States:** None (Dashboards can be restarted; permanent decommission = backing Service Retired)

### Transition Table
| From State | To State | Trigger | Required Conditions | Nathan Approval Required? |
|---|---|---|---|---|
| Active | Degraded | Data source unavailable or backing service degraded | Alert dispatched within 5 minutes | No (automatic) |
| Degraded | Active | Data sources restored | All data sources responding; display verified | No |
| Active | Stopped | Backing service stopped | PM2 process for backing service stopped | No |
| Stopped | Active | Backing service restarted | PM2 process online; dashboard accessible | No |

---

## Knowledge Base

**Valid States:** Active · Outdated · Archived
**Initial State:** Active
**Terminal States:** Archived

### Transition Table
| From State | To State | Trigger | Required Conditions | Nathan Approval Required? |
|---|---|---|---|---|
| Active | Outdated | `last_updated` exceeds SLA per curation_policy | Automatic flag | No (automatic) |
| Outdated | Active | Updated and re-curated | Content reviewed; last_updated timestamp refreshed | No |
| Active | Archived | Knowledge Base retired | Nathan approval; content preserved in Storage | **YES** |
| Outdated | Archived | Knowledge Base retired without updating | Nathan approval | **YES** |

---

## Memory Store

**Valid States:** Active · Compressing · Corrupted · Archived
**Initial State:** Active
**Terminal States:** Archived

### Transition Table
| From State | To State | Trigger | Required Conditions | Nathan Approval Required? |
|---|---|---|---|---|
| Active | Compressing | Compression schedule triggered (every 6h) | Compression job initiated | No (automatic) |
| Compressing | Active | Compression complete | Job succeeded; memory verified | No |
| Active | Corrupted | Data integrity failure detected | P1 alert dispatched; reads suspended for operational decisions | No (automatic — immediate alert) |
| Corrupted | Active | Recovery from backup | Backup restored; integrity check passed | No |
| Active | Archived | Memory Store end-of-life | Nathan approval; content archived per retention policy | **YES** |

---

## Registry

**Valid States:** Active · Stale · Rebuilding
**Initial State:** Active
**Terminal States:** None (Registry is permanent infrastructure)

### Transition Table
| From State | To State | Trigger | Required Conditions | Nathan Approval Required? |
|---|---|---|---|---|
| Active | Stale | `last_sync_at` > 24h for live assets | Alert dispatched | No (automatic) |
| Stale | Active | Sync triggered and completed | Sync job succeeded; last_sync_at updated | No |
| Active | Rebuilding | Full rebuild required | Rebuild authorized; source of truth identified | No |
| Rebuilding | Active | Rebuild complete | All assets re-catalogued; sync_at updated | No |

---

## LAYER 5 — EXECUTION

---

## Execution Role

**Valid States:** Active · Delegated · Vacant
**Initial State:** Active
**Terminal States:** None (Roles persist)

### Transition Table
| From State | To State | Trigger | Required Conditions | Nathan Approval Required? |
|---|---|---|---|---|
| Active | Delegated | Holder delegates temporarily | Delegation scope, acting holder, and expiry documented | No |
| Delegated | Active | Delegation expires | Expiry date reached | No |
| Active | Vacant | Holder unavailable | Escalation to Ownership Role; acting coverage sought | No |
| Vacant | Active | New holder assigned | Named holder confirmed | No |

---

## Operational Status

**Lifecycle Note:** Operational Status is a real-time classification (OK, DEGRADED, STOPPED, ERRORED, RESTARTING, UNKNOWN). It is not subject to an individual lifecycle — it is a continuously refreshed attribute of Services, Agents, and Automations. Status must be refreshed within ≤5 minutes for T0 assets.

---

## Integration Readiness

**Valid States:** Not Ready · Partially Ready · Ready · Validated · Degraded
**Initial State:** Not Ready
**Terminal States:** None (continuously re-assessed)

### Transition Table
| From State | To State | Trigger | Required Conditions | Nathan Approval Required? |
|---|---|---|---|---|
| Not Ready | Partially Ready | Some readiness checks pass | At least one of the four booleans = true | No |
| Partially Ready | Ready | All four checks pass | auth_verified=true, endpoint_reachable=true, error_handling_tested=true, end_to_end_validated=true | No |
| Ready | Validated | Live transaction confirmed | At least one real production transaction succeeded | No |
| Validated | Degraded | Integration failure detected | Alert dispatched; circuit breaker may engage | No (automatic) |
| Degraded | Not Ready | Complete re-validation required | Full re-validation triggered | No |
| Degraded | Validated | Issue resolved; re-validated | Live transaction confirmed after fix | No |

---

## Business Criticality

**Lifecycle Note:** Business Criticality is a canonical four-tier enumeration (Tier-0, Tier-1, Tier-2, Tier-3). Individual asset criticality is assigned, not a lifecycle. The classification itself is always Active. No asset may designate itself Tier-0 without Nathan's explicit designation.

---

## Recovery Priority

**Lifecycle Note:** Recovery Priority is a pre-approved ordered list. It is a permanent governance artifact, not an asset with individual lifecycle. Modifications to the recovery sequence require an Incident Response Playbook update via Change Control.

---

## Relationship Type

**Lifecycle Note:** Relationship Type is a canonical enumeration. All defined relationship types are permanently Active. New types require a Taxonomy V1.x update.

---

## Verification Method

**Lifecycle Note:** Verification Method is a canonical enumeration. All defined method types are permanently Active. New types require a Taxonomy V1.x update.

---

## LAYER 6 — EVOLUTION

---

## Current State

**Lifecycle Note:** Current State is a point-in-time snapshot. Once superseded by a newer snapshot, it becomes historical (no formal state transition — the new snapshot replaces it as the current reference). A Current State older than 7 days requires refresh before use in planning.

---

## Target State

**Valid States:** Proposed · Approved · In Progress · Achieved · Superseded
**Initial State:** Proposed
**Terminal States:** Achieved · Superseded

### Transition Table
| From State | To State | Trigger | Required Conditions | Nathan Approval Required? |
|---|---|---|---|---|
| Proposed | Approved | Council or Nathan approval | success_criteria[] defined; target_date set; rollback plan exists | No (Council decision) |
| Approved | In Progress | Migration work begins | Change Control approved; Current State documented | No |
| In Progress | Achieved | All success_criteria[] verified | All criteria confirmed with Verified evidence_state | No |
| In Progress | Superseded | Target replaced by updated objective | Nathan approval; new Target State created | **YES** |
| Approved | Superseded | Superseded before execution began | Nathan approval | **YES** |

---

## Migration State

**Valid States:** Not Started · In Progress · Blocked · Rolled Back · Complete
**Initial State:** Not Started
**Terminal States:** Complete · Rolled Back

### Transition Table
| From State | To State | Trigger | Required Conditions | Nathan Approval Required? |
|---|---|---|---|---|
| Not Started | In Progress | Migration execution begins | Change Control approved; rollback plan confirmed; Current State documented | No |
| In Progress | Blocked | Blocker encountered | Blocker documented; escalation initiated | No |
| Blocked | In Progress | Blocker resolved | Documented resolution | No |
| In Progress | Complete | All steps done | All steps in steps_completed[]; Target State success criteria met | No |
| In Progress | Rolled Back | Migration failure requires reversal | Nathan approval; rollback plan executed | **YES** |
| Blocked | Rolled Back | Unresolvable blocker | Nathan approval | **YES** |

---

## Retirement State

**Valid States:** Planned Retirement · Retiring · Retired · Archived
**Initial State:** Planned Retirement
**Terminal States:** Archived

### Transition Table
| From State | To State | Trigger | Required Conditions | Nathan Approval Required? |
|---|---|---|---|---|
| Planned Retirement | Retiring | Decommission work begins | Nathan approval; retirement_date set; archive_path confirmed; data_retention_policy set | **YES** |
| Retiring | Retired | All processes stopped; data archived | Shutdown procedures complete; archive confirmed; all dependencies removed | No |
| Retired | Archived | Registry updated; provenance record complete | archive_path confirmed in Registry | No |

---

## Supersession

**Lifecycle Note:** Supersession records are permanently Active. They are never deleted. This is an absolute governance rule. The permanent provenance chain depends on immutable Supersession records.

---

## Versioning

**Lifecycle Note:** Versioning is an ongoing, continuous discipline applied throughout an asset's lifecycle. It is not subject to individual state management. Major version bumps require Change Control approval.

---

## Change Control

**Valid States:** Proposed · Approved · In Progress · Complete · Rejected · Rolled Back
**Initial State:** Proposed
**Terminal States:** Complete · Rejected · Rolled Back

### Transition Table
| From State | To State | Trigger | Required Conditions | Nathan Approval Required? |
|---|---|---|---|---|
| Proposed | Approved | Council or Nathan approval | rollback_plan defined; risk_level assessed; approver_id set | No (Council can approve; Nathan for P0) |
| Proposed | Rejected | Council or Nathan rejects | Rejection reason documented | No |
| Approved | In Progress | Change execution begins | scheduled_at reached; executor confirmed | No |
| In Progress | Complete | Change successfully implemented | completion_evidence logged; all affected assets validated | No |
| In Progress | Rolled Back | Change fails; rollback required | Nathan approval; rollback_plan executed | **YES** |

---

## Drift Detection

**Valid States:** Active · Alert-Open · Resolved · Suppressed
**Initial State:** Active
**Terminal States:** None (ongoing detection process)

### Transition Table
| From State | To State | Trigger | Required Conditions | Nathan Approval Required? |
|---|---|---|---|---|
| Active | Alert-Open | Drift detected | drift_description logged; severity classified per Risk Level scale; alerting initiated | No (automatic) |
| Alert-Open | Resolved | Drift corrected | Change Control executed; Registry updated; re-comparison confirms alignment | No |
| Alert-Open | Suppressed | Suppression justified | Documented suppression justification; expiry_date set | No (but Nathan informed for P0 suppressions) |
| Suppressed | Active | Suppression expired | Expiry date reached | No (automatic) |
| Resolved | Active | Alert closed | Drift confirmed resolved; monitoring resumes | No |

---

## Schema Evolution

**Valid States:** Stable · Evolving · Breaking-Change-Pending · Migrating · Stable (post-migration)
**Initial State:** Stable
**Terminal States:** None (ongoing lifecycle)

### Transition Table
| From State | To State | Trigger | Required Conditions | Nathan Approval Required? |
|---|---|---|---|---|
| Stable | Evolving | Additive, backward-compatible change proposed | Proposed change documented; backward_compatible=true | No |
| Evolving | Stable | Additive change approved and applied | backward_compatible change applied; consumers unaffected | No |
| Stable | Breaking-Change-Pending | Breaking change proposed | Change documented; migration plan drafted | No |
| Breaking-Change-Pending | Migrating | Breaking change approved | Nathan approval (P0-level for Tier-0 schemas); migration_script_ref provided; rollback plan confirmed | **YES (Tier-0)** / No (Tier-1+) |
| Migrating | Stable (post-migration) | Migration complete | All consumers updated; verification methods passed | No |

---

# SECTION 3 — CROSS-ASSET STATE DEPENDENCIES

Asset state transitions that trigger or are gated by other assets' states.

| Asset / State Change | Dependencies / Gating Rules |
|---|---|
| **Service: Staging → Active** | Requires Integration Readiness = Validated for all Integrations the Service consumes. |
| **Agent: Testing → Active (financial)** | Requires Nathan's explicit approval. Requires spend_cap_usd to be set and enforced by Policy. |
| **Venture: Pre-Launch → Active** | Requires Nathan's explicit approval. Requires daily_spend_cap_usd set. Requires governing Council to be Active. |
| **Venture: Active → Scaling** | Requires at least one verified revenue event (Business Outcome = Achieved or KPI threshold confirmed). |
| **Project: Planned → In Progress** | Cannot begin if parent Program is On Hold. Program must be Active. |
| **Project: In Progress → Complete** | All deliverables (Repository/Service/Agent) produced must have owner_role_id assigned before Project can be Complete. |
| **Program: Active → Completed** | All child Projects must be Complete or Archived. No Project in Planned, In Progress, or Blocked state. |
| **Repository: Deprecated → Archived** | All Services that DEPLOYS_TO this Repository must be migrated or Retired first. |
| **API: Active → Retired** | All Integrations that CONSUME this API must be Deprecated or migrated to a new API version first. |
| **Library (trading.shared.kelly): Any → Deprecated** | Blocked by KELLY NO-FIX constraint. Requires Nathan's explicit directive before any state change. |
| **Council: Active → Dissolved** | All assets GOVERNED_BY this Council must be re-assigned to another Council first. |
| **Database (clawdb): Active → any degraded state** | All trading agents (cashclaw_director, cashclaw_arb, polymarket_trader) must halt financial operations. P0 alert dispatched. |
| **Integration: Active → Broken** | Parent Service that OWNS this Integration enters Degraded state. Circuit breaker engages. Trading halts if this is a trading Integration. |
| **Secret Metadata: Active → Expired** | All assets DESCRIBED_BY this Secret Metadata record must halt operations requiring this credential. P0 alert dispatched. |
| **Agent (trading): Active → Suspended** | The trading_sentinel (PM2 id=41) triggers a P0 alert. All financial operations by the suspended agent halt immediately. |
| **Model (real-time chain): Available → Unavailable** | Router activates next model in the Haiku→Ollama→Heuristic fallback chain. |
| **Memory Store: Active → Corrupted** | All Agents cease using this Memory Store for operational decisions. P1 alert dispatched. |
| **Framework: Active → Upgrading** | All Services and Agents that PROVIDES_STRUCTURE_FOR this Framework must be impact-analyzed. No new deployments of consuming assets during upgrade. |
| **Change Control: Proposed → Approved** | Requires `rollback_plan` to be defined — no approval is valid without a rollback plan. |
| **Migration State: Not Started → In Progress** | Requires Change Control = Approved. Requires Current State snapshot dated within 7 days. |
| **Drift Detection: Active → Alert-Open (P0)** | Nathan must be notified within 15 minutes for P0-severity drift (e.g., spend cap removed, signal chain unauthorized change). |

---

# SECTION 4 — STATE MACHINE GOVERNANCE RULES

## 4.1 Authorization Matrix

Who may authorize which class of state transition:

| Transition Class | Authorized By | Mechanism |
|---|---|---|
| Venture first Active state (capital deployment) | Nathan only | Telegram approval, 300s timeout |
| Asset to terminal state (Archived, Retired, Closed, Cancelled, Dissolved, Disbanded, Revoked, Yanked, Deprecated) | Nathan only | Telegram approval |
| Tier-0 asset retirement or decommission | Nathan only (P0-level) | Immediate Telegram + audit log |
| Change Control for Tier-0 schema change | Nathan only | Telegram approval |
| Agent suspension (policy violation) | PMO Council / Trading Council | Council decision; Nathan informed |
| Agent resumption after policy violation suspension | Nathan approval | Telegram approval |
| Agent Testing → Active (non-financial) | PMO Council or Engineering Council | Council approval |
| Framework major version upgrade | Engineering Council | Change Control |
| Council suspension | Nathan only | Direct directive |
| Standard/Policy deprecation | Nathan or issuing Council | Council decision |
| On Hold / Pause / Staging transitions | Agent-autonomous where trigger conditions met | Logged automatically |
| Auto-recovery transitions (Crashed→Restarting, Degraded→Active after fix) | Agent-autonomous | PM2 auto-restart; logged |

## 4.2 Audit Logging Requirements

Every state transition must produce an audit log entry containing:

| Field | Required? | Notes |
|---|---|---|
| `asset_id` | Mandatory | The unique ID of the transitioning asset |
| `asset_type` | Mandatory | Canonical asset type name from Taxonomy |
| `from_state` | Mandatory | Prior state |
| `to_state` | Mandatory | New state |
| `transition_timestamp` | Mandatory | ISO 8601 UTC |
| `triggered_by` | Mandatory | Agent ID, human name, or automation name |
| `trigger_reason` | Mandatory | Human-readable description of why the transition occurred |
| `approval_id` | Conditional | Required for Nathan-approved transitions |
| `evidence_state` | Conditional | Required for transitions involving financial assets |
| `notes` | Optional | Additional context |

**Storage Target:** Audit log entries are written to `~/.openclaw/vault/` (governance vault Storage) as an immutable append-only record.

**Stale Transition Detection:** Any asset that has not had its state verified within 2× its monitoring cadence must be flagged with Operational Status = UNKNOWN. UNKNOWN must never persist beyond one monitoring cycle.

## 4.3 Rollback Rules

| Condition | Rollback Rule |
|---|---|
| Any Change Control transition fails in Tier-0 asset | Rollback plan must exist before approval. Rollback requires Nathan approval. |
| Framework upgrade failure | Pre-approved rollback to prior version. Nathan informed. |
| Migration State: In Progress → Rolled Back | Nathan approval. Rollback plan executed exactly as documented. No improvised recovery. |
| Agent activated then found to violate policy | Agent Suspended immediately. Nathan notified. Rollback = all transactions from the activation period reviewed and logged. |
| Trade log manipulation attempt | P0 incident. All trading halted. Nathan immediate notification. Trade logs are immutable — no rollback of trade records is possible or permitted. |
| Secret Metadata Revoked | All consuming assets halt operations within 1 hour. No rollback — revocation is permanent. |

## 4.4 Terminal State Finality

| Terminal State | Finality Rule |
|---|---|
| Archived | Cannot be re-activated. Can only be read for audit purposes. Deletion requires separate P0 approval. |
| Cancelled | Cannot be re-opened as the same Project. A new Project must be created if work is to resume. |
| Closed | Venture is permanently closed. New Venture must be created if the business model is to be revived. |
| Dissolved | Council is permanently disbanded. New Council must be created if governance domain needs coverage. |
| Retired | Asset is permanently decommissioned. Deletion requires separate P0 approval with audit log entry. Retired ≠ Deleted. |
| Revoked | Secret credential permanently invalidated. New credential must be created; this Secret Metadata record is permanently Revoked. |
| Superseded | Predecessor is permanently replaced. Supersession record is immutable and permanent. |
| Yanked | Package version permanently unavailable. A new Package version must be released. |
| Disbanded | Agent Team is permanently closed. New Agent Team must be formed if needed. |
| Missed | Business Outcome permanently marked as not achieved on time. A new Outcome must be created if the goal is to be re-attempted. |

---

*OPEN EMPIRE LIFECYCLE STATE MACHINE V1.0.0 — Materialized 2026-08-05 — Alusi, Chief of Staff*
*Source: OPEN_EMPIRE_ASSET_TAXONOMY_V1.md*
*Next scheduled review: When Taxonomy advances to V1.1.0 or V2.0.0*
*This document governs the legal state transitions of all 58 Open Empire asset types.*
