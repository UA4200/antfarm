#!/bin/bash
# OPEN EMPIRE — Governance Drift Detection
# Schedule: every 6 hours via cron
# B9 Continuous Validation — Governance Layer

GOVERNANCE_DIR="$HOME/.openclaw/workspace/governance"
BASELINE_TAG="v1.0.0"
LOG="$HOME/.openclaw/logs/governance_drift_$(date +%Y%m%d).log"
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)

echo "[$TIMESTAMP] GOVERNANCE DRIFT CHECK START" >> "$LOG"

# Check git tag integrity
cd "$HOME/.openclaw/workspace"
LIVE_HASH=$(git rev-parse HEAD 2>/dev/null)
BASELINE_HASH=$(git rev-parse "$BASELINE_TAG^{commit}" 2>/dev/null)

if [ -z "$BASELINE_HASH" ]; then
  echo "[$TIMESTAMP] ERROR: baseline tag $BASELINE_TAG not found" >> "$LOG"
  exit 1
fi

# Check if governance/ has uncommitted changes
DIRTY=$(git diff --name-only HEAD -- governance/ 2>/dev/null | wc -l | tr -d ' ')
if [ "$DIRTY" != "0" ]; then
  echo "[$TIMESTAMP] DRIFT_DETECTED: $DIRTY governance files have uncommitted changes" >> "$LOG"
  # TODO: send Telegram alert when n8n workflows are configured
  exit 2
fi

echo "[$TIMESTAMP] GOVERNANCE_CLEAN: no uncommitted changes in governance/" >> "$LOG"
echo "[$TIMESTAMP] CURRENT_HEAD: $LIVE_HASH" >> "$LOG"
echo "[$TIMESTAMP] BASELINE: $BASELINE_HASH" >> "$LOG"
echo "[$TIMESTAMP] GOVERNANCE DRIFT CHECK COMPLETE: OK" >> "$LOG"
exit 0
