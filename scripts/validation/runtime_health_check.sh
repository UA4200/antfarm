#!/bin/bash
# OPEN EMPIRE — Runtime Health Check
# B9 Continuous Validation — Runtime Layer
# Required-always-on PM2 processes (pm_ids that must be ONLINE)
REQUIRED=(0 1 3 4 5 8 9 10 14 15 23 24 36 38 39 40 41 42)
LOG="$HOME/.openclaw/logs/runtime_health_$(date +%Y%m%d).log"
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
FAILED=0

echo "[$TIMESTAMP] RUNTIME HEALTH CHECK START" >> "$LOG"

PM2_JSON=$(pm2 jlist 2>/dev/null)

for pmid in "${REQUIRED[@]}"; do
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
    echo "[$TIMESTAMP] ALERT: pm_id=$pmid STATUS=$STATUS — REQUIRED service is not online" >> "$LOG"
    FAILED=$((FAILED+1))
  fi
done

TOTAL=${#REQUIRED[@]}
if [ "$FAILED" -eq 0 ]; then
  echo "[$TIMESTAMP] RUNTIME_HEALTH: ALL $TOTAL required services ONLINE" >> "$LOG"
  exit 0
else
  echo "[$TIMESTAMP] RUNTIME_HEALTH: $FAILED of $TOTAL required services NOT ONLINE" >> "$LOG"
  exit 2
fi
