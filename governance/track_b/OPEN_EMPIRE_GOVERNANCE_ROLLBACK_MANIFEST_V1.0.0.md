# Open Empire Governance Rollback Procedure — v1.0.0

**Document Type:** Rollback Manifest  
**Target Version:** v1.0.0  
**Baseline Commit:** `17df0ff218708440edb74214ff5576a30af221a5`  
**Tag:** `v1.0.0` (tag SHA: `29cccb19612114c755471f86e14d0a06f70b2830`)  
**Snapshot:** `governance_v1.0.0_snapshot_20260806T074103Z.tar.gz`  
**Snapshot SHA256:** `442222da3d167072f981d6337591517fb57d85b538512130209820a59164a96c`  
**Snapshot Size:** 213,882 bytes  
**Authorized By:** Nathan Asiegbu  
**Document Status:** FROZEN — change control required  
**Last Updated:** 2026-08-06

---

## 1. Purpose

This document provides the complete, authoritative step-by-step rollback procedure to restore the Open Empire system to the governance baseline at **v1.0.0**. This procedure is to be followed:

- After a failed governance upgrade that destabilizes the system
- When validation results drop below the 240/240 baseline
- On explicit instruction from Nathan Asiegbu
- In response to a security incident requiring state reversion

---

## 2. Prerequisites

Before initiating rollback, confirm all of the following:

| # | Prerequisite | Verification Command |
|---|---|---|
| 1 | You have shell access to `ugos-mac-mini-3` (primary host) | `tailscale ssh NeoOC@100.107.5.103` or direct terminal |
| 2 | Git is installed and working | `git --version` |
| 3 | Python 3.13 is available (venv313) | `~/.venvs/venv313/bin/python --version` |
| 4 | PM2 is running | `pm2 list` |
| 5 | Snapshot file exists and is accessible | `ls -lh ~/.openclaw/workspace/governance/snapshots/governance_v1.0.0_snapshot_20260806T074103Z.tar.gz` |
| 6 | You have confirmed with Nathan Asiegbu that rollback is authorized | Telegram confirmation or verbal |
| 7 | All active trading agents are paused | `pm2 stop cashclaw_director cashclaw_arb polymarket-trader` (run BEFORE rollback) |

> **WARNING:** Do NOT proceed without completing all 7 prerequisites. Rolling back while trading agents are live may cause in-flight trades to reference stale state.

---

## 3. Pre-Rollback Snapshot (Current State)

Before rolling back, capture the current state so it can be compared or restored if rollback itself fails.

```bash
# Create a pre-rollback snapshot of current state
cd ~/.openclaw/workspace
TIMESTAMP=$(date -u +%Y%m%dT%H%M%SZ)
tar czf ~/rollback_rescue_${TIMESTAMP}.tar.gz \
  governance/ \
  AGENTS.md \
  TOOLS.md \
  trading/

# Record the current git state
git log --oneline -5 > ~/pre_rollback_git_state_${TIMESTAMP}.txt
git status >> ~/pre_rollback_git_state_${TIMESTAMP}.txt

echo "Pre-rollback snapshot saved: ~/rollback_rescue_${TIMESTAMP}.tar.gz"
```

---

## 4. Pause All Autonomous Agents

```bash
# Stop all trading and autonomous agents before rollback
pm2 stop cashclaw_director cashclaw_arb polymarket-trader trading_sentinel

# Verify they are stopped
pm2 list | grep -E "cashclaw|polymarket|sentinel"
# Expected: all show status=stopped
```

---

## 5. Verify Snapshot Integrity

```bash
# Navigate to snapshots directory
cd ~/.openclaw/workspace/governance/snapshots/

# Verify SHA256 of snapshot
sha256sum governance_v1.0.0_snapshot_20260806T074103Z.tar.gz
# Expected output must match EXACTLY:
# 442222da3d167072f981d6337591517fb57d85b538512130209820a59164a96c  governance_v1.0.0_snapshot_20260806T074103Z.tar.gz

# If SHA256 does NOT match, DO NOT PROCEED — escalate immediately (see Section 9)
```

---

## 6. Git Rollback to v1.0.0

```bash
cd ~/.openclaw/workspace

# Save any uncommitted local changes to a stash
git stash save "pre-rollback-stash-$(date -u +%Y%m%dT%H%M%SZ)"

# Verify the tag exists
git tag -l v1.0.0
# Expected: v1.0.0

# Verify the tag SHA
git rev-list -n 1 v1.0.0
# Expected: 17df0ff218708440edb74214ff5576a30af221a5

# Check out the v1.0.0 tag as a detached HEAD (safe, non-destructive)
git checkout v1.0.0

# Alternatively, to reset master branch to v1.0.0 (destructive — requires authorization):
# git checkout master
# git reset --hard v1.0.0
# git push --force-with-lease origin master   # Only if GitHub push is authorized

echo "Git rollback to v1.0.0 complete. HEAD is now: $(git rev-parse HEAD)"
```

---

## 7. Snapshot Restore Procedure

This restores the governance directory to the exact state captured in the v1.0.0 snapshot.

```bash
cd ~/.openclaw/workspace/governance/snapshots/

# Inspect snapshot contents before restoring
tar tzf governance_v1.0.0_snapshot_20260806T074103Z.tar.gz | head -30

# Create a staging restore directory
mkdir -p ~/rollback_staging/
cd ~/rollback_staging/

# Extract snapshot to staging
tar xzf ~/.openclaw/workspace/governance/snapshots/governance_v1.0.0_snapshot_20260806T074103Z.tar.gz

# Compare staging with current governance directory
diff -rq ~/rollback_staging/governance/ ~/.openclaw/workspace/governance/ \
  --exclude="*.pyc" \
  --exclude="__pycache__" 2>&1 | head -50

# Review diff output. If acceptable, proceed with restore:
rsync -av --delete ~/rollback_staging/governance/ ~/.openclaw/workspace/governance/

echo "Snapshot restore complete."

# Clean up staging
rm -rf ~/rollback_staging/
```

---

## 8. Post-Rollback Validation

Run the full validation suite to confirm v1.0.0 baseline is intact.

```bash
cd ~/.openclaw/workspace

# Run governance validation
~/.venvs/venv313/bin/python governance/build/validate.py 2>&1 | tee ~/rollback_validation_$(date -u +%Y%m%dT%H%M%SZ).log

# Expected last line: VALIDATION COMPLETE: 240/240 PASS
# If result is NOT 240/240 PASS, DO NOT restart agents — escalate (see Section 9)
```

### Additional Spot Checks

```bash
# Verify git state
git log --oneline -3
# Expected first line: 17df0ff (HEAD, tag: v1.0.0) <commit message>

# Verify snapshot SHA in manifest
cat governance/track_b/OPEN_EMPIRE_GOVERNANCE_RELEASE_MANIFEST_V1.0.0.json | \
  python3 -c "import json,sys; m=json.load(sys.stdin); print(m['snapshot']['snapshot_sha256'])"
# Expected: 442222da3d167072f981d6337591517fb57d85b538512130209820a59164a96c

# Verify PM2 agents (should still be stopped)
pm2 list | grep -E "cashclaw|polymarket|sentinel"
```

---

## 9. Restart Agents After Successful Validation

Only restart agents after validation confirms 240/240 PASS.

```bash
# Restart trading agents
pm2 restart cashclaw_director cashclaw_arb polymarket-trader trading_sentinel

# Wait 30 seconds and check status
sleep 30
pm2 list

# Verify no crash loops (online status expected)
pm2 logs cashclaw_director --lines 20
pm2 logs polymarket-trader --lines 20
```

---

## 10. Escalation — If Rollback Fails

If any step fails or validation does not return 240/240 PASS:

### Immediate Actions

1. **DO NOT restart trading agents.**
2. **Keep all autonomous systems stopped.**
3. **Capture the error output:**
   ```bash
   pm2 logs --lines 100 > ~/escalation_pm2_logs_$(date -u +%Y%m%dT%H%M%SZ).txt
   git status > ~/escalation_git_status.txt
   ```

### Contact

| Method | Details |
|---|---|
| **Primary:** Telegram | Message Nathan Asiegbu on the trading/ops Telegram channel |
| **Secondary:** Direct message | Include error log files as attachment |
| **Subject line:** `[URGENT] Open Empire Rollback Failure — Manual Intervention Required` |

### Information to Include in Escalation

- Step number where failure occurred (Sections 5–9)
- Exact error message or unexpected output
- Current `git status` and `git log --oneline -3` output
- Current `pm2 list` output
- SHA256 of snapshot file (Section 5)
- Timestamp of failure

### Escalation Levels

| Level | Trigger | Response |
|---|---|---|
| L1 | Snapshot SHA mismatch | Locate backup snapshot, verify chain of custody |
| L2 | Validation < 240/240 | Manual file-by-file comparison with snapshot |
| L3 | Git repo corrupted | `git fsck`, restore from GitHub remote |
| L4 | All recovery paths exhausted | Full system restore from macOS Time Machine + re-bootstrap |

---

## 11. Rollback Decision Log Template

Complete this log entry after any rollback event and save to `~/.openclaw/workspace/governance/rollback_log.md`:

```markdown
## Rollback Event — [DATE]

- **Triggered by:** [Nathan Asiegbu / automated / incident]
- **Reason:** [Brief description]
- **From version:** [e.g., v1.2.0]
- **To version:** v1.0.0
- **Initiated at:** [ISO timestamp]
- **Completed at:** [ISO timestamp]
- **Validation result:** [240/240 PASS / FAIL + detail]
- **Agents restarted:** [yes/no]
- **Notes:** [Any anomalies or deviations from this procedure]
- **Authorized by:** [Nathan Asiegbu]
```

---

## 12. Document Maintenance

This document is **FROZEN** at v1.0.0. Changes require:
1. A new governance review (Gate A equivalent)
2. Version increment to v1.0.1 or higher
3. New snapshot capture
4. Authorization by Nathan Asiegbu

**Do not modify this document without authorization.**
