# PM2 33/34 Root Cause & Remediation Report
**Generated:** 2026-08-09T18:35:01Z  
**Agent:** subagent:pm2-33-34-root-cause  
**Host:** Ugo's Mac mini (macOS 12.7.6)

---

## Executive Summary

**Both id=33 and id=34 are OPERATIONAL.** The `stopped` status in PM2 is a **false alarm** — these are short-lived cron scripts by design, not long-running daemons. PM2 reports `stopped` between scheduled runs. Both scripts ran successfully at **13:30:07 CDT today** and their output files are current.

**No restart was performed. No intervention was needed.**

---

## Service Profiles

### id=33 — open-empire-federation-staging

| Field | Value |
|---|---|
| Script | `/Users/NeoOC/.openclaw/empire/federation/federation_coordinator.py` |
| Interpreter | `python3` (Python 3.14.6) |
| Cron | `*/15 * * * *` (every 15 minutes) |
| Output | `~/.openclaw/empire/federation/latest_federation_state.json` |
| Last run | 2026-08-09 13:30:07 CDT ✅ |
| Next run | 2026-08-09 13:45:xx CDT |
| Restarts | 14 (majority during Python upgrade window) |

**What the script does:** Generates a federation status JSON (`status: "coordinated"`, `approval_required: true`) and exits. Takes < 1 second.

### id=34 — open-empire-lifecycle-staging

| Field | Value |
|---|---|
| Script | `/Users/NeoOC/.openclaw/empire/lifecycle/lifecycle_manager.py` |
| Interpreter | `python3` (Python 3.14.6) |
| Cron | `*/15 * * * *` (every 15 minutes) |
| Output | `~/.openclaw/empire/lifecycle/latest_lifecycle_state.json` |
| Last run | 2026-08-09 13:30:07 CDT ✅ |
| Next run | 2026-08-09 13:45:xx CDT |
| Restarts | 12 (majority during Python upgrade window) |

**What the script does:** Generates lifecycle state JSON (`phase: "final_consolidated"`, `health: "green"`, `autonomous_spending_enabled: false`) and exits. Takes < 1 second.

---

## Root Cause Analysis

### Root Cause Class: STALE_SERVICE (Misclassified as Broken)

The `stopped` status seen in `pm2 list` is **by design** for cron-triggered scripts in PM2:

1. Cron trigger fires → PM2 starts the process → script runs (~0.5s) → writes JSON → exits with code 0 → PM2 marks as `stopped`
2. At next cron trigger → cycle repeats

This is the **correct behavior** for a periodic status-writer. The scripts are NOT crashed; they are idle between cron runs.

### Historical Error Log Noise (168/149 Fatal Python errors)

The error logs contain **4,522 lines (id=33)** and **4,229 lines (id=34)** of errors from a historical Python 3.14.3_1 → 3.14.6 Homebrew upgrade. Specifically:

```
Fatal Python error: init_import_site: Failed to import the site module
...
File "/usr/local/Cellar/python@3.14/3.14.3_1/Frameworks/Python.framework/Versions/3.14/lib/python3.14/sitecustomize.py"
```

This was a **VERSION_INCOMPATIBILITY** during Brew's in-place upgrade of python@3.14 from patch version `3.14.3_1` to `3.14.6`. During the upgrade window, the Python binary existed but the standard library was in an inconsistent state, causing `site` module failures on every startup. These crashes are **fully resolved** — current `python3 --version` returns `Python 3.14.6` and passes functional tests.

---

## AGENTS.md Discrepancies Found

AGENTS.md contains stale/incorrect entries for both services:

| Field | AGENTS.md Claims | Actual |
|---|---|---|
| id=33 PM2 ID | 45 | **33** |
| id=34 PM2 ID | 46 | **34** |
| Cron interval | `*/5` (every 5 min) | **`*/15`** (every 15 min) |
| Python version | Python3.13 | **Python 3.14.6** |

The entries in AGENTS.md for PM2 IDs 45 and 46 are mismatched — ID 45 is actually **n8n**, and ID 46 does not exist in the current PM2 registry.

---

## Dependency Check Results

No downstream consumers of the output JSON files were found:

- `latest_federation_state.json` — No active reader found in workspace, trading stack, mission-control, or kg-api
- `latest_lifecycle_state.json` — No active reader found

These files appear to be **observability artifacts** for the Open Empire staging plane — useful for manual inspection, not required by any live service.

**CashClaw (ids 38, 39, 40, 41):** Confirmed online and untouched throughout this diagnosis.

---

## Action Taken

**NO_ACTION** — Services are operational. No restarts, no file changes, no PM2 commands issued.

---

## Recommendations

1. **Update AGENTS.md** — Correct PM2 IDs (33/34 not 45/46), cron interval (*/15 not */5), Python version (3.14 not 3.13)
2. **Flush error logs** — Remove historical Python upgrade noise:
   ```bash
   pm2 flush 33
   pm2 flush 34
   ```
3. **Optional: add monitoring awareness** — If any automated monitor alerts on `stopped` status for cron scripts, add `open-empire-federation-staging` and `open-empire-lifecycle-staging` to the allow-list for transient-stopped states
4. **Optional: consider `--no-autorestart`** — Since these are fire-and-exit scripts, setting `autorestart: false` + `cron_restart: */15 * * * *` more cleanly models the intent in PM2
5. **No restart needed** — Next cron trigger at 13:45 CDT will run both scripts automatically

---

## Final Verdict

**PM2_33_34_OPERATIONAL_WITH_EXCEPTION**

Both services are healthy and producing output. Exceptions:
- AGENTS.md has wrong IDs and parameters (needs update)
- Historical error logs contain noise from Python upgrade (recommend flush)
- "Stopped" status is a PM2 display artifact for cron scripts, not an error condition
