#!/bin/bash
# OPEN EMPIRE — Governance Drift Detection (B9)
# Wired to n8n OEPM - Governance Change Alert
GOVERNANCE_DIR="$HOME/.openclaw/workspace/governance"
N8N_WEBHOOK="http://127.0.0.1:5678/webhook/governance-change"
LOG="$HOME/.openclaw/logs/governance_drift_$(date +%Y%m%d).log"
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)

echo "[$TIMESTAMP] GOVERNANCE DRIFT CHECK START" >> "$LOG"
cd "$HOME/.openclaw/workspace" 2>/dev/null || exit 1

BASELINE_HASH=$(git rev-parse "v1.0.0^{commit}" 2>/dev/null)
if [ -z "$BASELINE_HASH" ]; then
  echo "[$TIMESTAMP] ERROR: baseline tag v1.0.0 not found" >> "$LOG"
  curl -s -X POST "$N8N_WEBHOOK" -H "Content-Type: application/json" \
    -d "{\"event\":\"TAG_MISSING\",\"file\":\"v1.0.0\",\"details\":\"Governance baseline tag not found — possible repo corruption\",\"severity\":\"CRITICAL\"}" > /dev/null 2>&1
  exit 1
fi

DIRTY=$(git diff --name-only HEAD -- governance/ 2>/dev/null | wc -l | tr -d ' ')
if [ "$DIRTY" != "0" ]; then
  CHANGED=$(git diff --name-only HEAD -- governance/ 2>/dev/null | head -5 | tr '\n' ',')
  echo "[$TIMESTAMP] DRIFT_DETECTED: $DIRTY governance files have uncommitted changes: $CHANGED" >> "$LOG"
  curl -s -X POST "$N8N_WEBHOOK" -H "Content-Type: application/json" \
    -d "{\"event\":\"UNCOMMITTED_CHANGES\",\"file\":\"$CHANGED\",\"details\":\"$DIRTY governance files modified outside change control\",\"severity\":\"CRITICAL\"}" > /dev/null 2>&1
  exit 2
fi

echo "[$TIMESTAMP] GOVERNANCE_CLEAN: OK | HEAD: $(git rev-parse HEAD 2>/dev/null)" >> "$LOG"
exit 0
