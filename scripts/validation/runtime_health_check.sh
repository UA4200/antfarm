#!/bin/bash
# OPEN EMPIRE — Runtime Health Check (B9) — updated 2026-08-06
# Uses name-based PM2 lookup (pm_ids can change on restart)
N8N_WEBHOOK="http://127.0.0.1:5678/webhook/runtime-health-alert"
LOG="$HOME/.openclaw/logs/runtime_health_$(date +%Y%m%d).log"
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)

REQUIRED_NAMES=(executor alusi-gateway alusi-discord-adapter alusi-controlled-worker alusi-orchestrator exec-gateway telegram-approvals ecosystem.email-dispatcher mission-control heartbeat ollama clawdb cashclaw_director cashclaw_arb polymarket-trader trading_sentinel alusi-telegram-adapter)

PM2_JSON=$(pm2 jlist 2>/dev/null)
FAILED=0; FAILED_NAMES=""

for name in "${REQUIRED_NAMES[@]}"; do
  STATUS=$(echo "$PM2_JSON" | python3 -c "
import json,sys
d=json.load(sys.stdin)
for p in d:
    if p.get('name')=='$name':
        print(p.get('pm2_env',{}).get('status','unknown'))
        break
else:
    print('not_found')
" 2>/dev/null)
  if [ "$STATUS" != "online" ]; then
    echo "[$TIMESTAMP] ALERT: $name STATUS=$STATUS" >> "$LOG"
    FAILED=$((FAILED+1)); FAILED_NAMES="$FAILED_NAMES $name"
    curl -s -X POST "$N8N_WEBHOOK" -H "Content-Type: application/json" \
      -d "{\"service\":\"$name\",\"status\":\"$STATUS\",\"severity\":\"CRITICAL\",\"details\":\"Required service down. Action: pm2 restart $name\"}" > /dev/null 2>&1 || true
  fi
done

# n8n is monitored separately as KNOWN_ISSUE (restart bug)
N8N_STATUS=$(echo "$PM2_JSON" | python3 -c "
import json,sys; d=json.load(sys.stdin)
for p in d:
    if p.get('name')=='n8n': print(p.get('pm2_env',{}).get('status','?')); break
else: print('not_found')
" 2>/dev/null)
echo "[$TIMESTAMP] n8n_status=$N8N_STATUS (KNOWN_ISSUE: restart_bug_v2.8.4)" >> "$LOG"

TOTAL=${#REQUIRED_NAMES[@]}
if [ "$FAILED" -eq 0 ]; then
  echo "[$TIMESTAMP] RUNTIME_HEALTH: ALL $TOTAL required services ONLINE" >> "$LOG"
  exit 0
else
  echo "[$TIMESTAMP] RUNTIME_HEALTH: $FAILED/$TOTAL DOWN:$FAILED_NAMES" >> "$LOG"
  exit 2
fi
