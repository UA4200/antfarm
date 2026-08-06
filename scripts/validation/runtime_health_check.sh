#!/bin/bash
# OPEN EMPIRE — Runtime Health Check (B9)
# Wired to n8n OEPM - Runtime Health Alert
N8N_WEBHOOK="http://127.0.0.1:5678/webhook/runtime-health-alert"
LOG="$HOME/.openclaw/logs/runtime_health_$(date +%Y%m%d).log"
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
REQUIRED=(0 1 3 4 5 8 9 10 14 15 23 24 36 38 39 40 41 42)
REQUIRED_NAMES=("executor" "alusi-gateway" "alusi-discord-adapter" "alusi-controlled-worker" "alusi-orchestrator" "exec-gateway" "telegram-approvals" "ecosystem.email-dispatcher" "mission-control" "heartbeat" "n8n" "ollama" "clawdb" "cashclaw_director" "cashclaw_arb" "polymarket-trader" "trading_sentinel" "alusi-telegram-adapter")

PM2_JSON=$(pm2 jlist 2>/dev/null)
FAILED=0
FAILED_NAMES=""

for i in "${!REQUIRED[@]}"; do
  pmid="${REQUIRED[$i]}"
  name="${REQUIRED_NAMES[$i]}"
  STATUS=$(echo "$PM2_JSON" | python3 -c "
import json,sys
d=json.load(sys.stdin)
for p in d:
    if p.get('pm_id')==$pmid:
        print(p.get('pm2_env',{}).get('status','unknown'))
        break
else:
    print('not_found')
" 2>/dev/null)
  if [ "$STATUS" != "online" ]; then
    echo "[$TIMESTAMP] ALERT: $name (pm_id=$pmid) STATUS=$STATUS" >> "$LOG"
    FAILED=$((FAILED+1))
    FAILED_NAMES="$FAILED_NAMES $name"
    # Alert via n8n
    curl -s -X POST "$N8N_WEBHOOK" -H "Content-Type: application/json" \
      -d "{\"service\":\"$name\",\"pm_id\":$pmid,\"status\":\"$STATUS\",\"severity\":\"CRITICAL\",\"details\":\"Required service is not online. Action: pm2 restart $name\"}" > /dev/null 2>&1
  fi
done

TOTAL=${#REQUIRED[@]}
if [ "$FAILED" -eq 0 ]; then
  echo "[$TIMESTAMP] RUNTIME_HEALTH: ALL $TOTAL required services ONLINE" >> "$LOG"
  exit 0
else
  echo "[$TIMESTAMP] RUNTIME_HEALTH: $FAILED/$TOTAL DOWN:$FAILED_NAMES" >> "$LOG"
  exit 2
fi
