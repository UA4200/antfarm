#!/bin/bash
# OPEN EMPIRE — Remote Bootstrap Script (Sprint 5)
# Run this after any machine reboot or full system recovery
# Can be executed via: tailscale ssh NeoOC@100.107.5.103 "bash ~/.openclaw/workspace/scripts/validation/remote_bootstrap.sh"
# ════════════════════════════════════════════════════════════════
set -e
LOG="$HOME/.openclaw/logs/bootstrap_$(date +%Y%m%d_%H%M%S).log"
TS() { date -u +%Y-%m-%dT%H:%M:%SZ; }

echo "[$(TS)] OPEN EMPIRE BOOTSTRAP START" | tee -a "$LOG"
echo "[$(TS)] Host: $(hostname) | User: $(whoami)" | tee -a "$LOG"

# STEP 1: Verify secrets file
if [ ! -f "$HOME/.openclaw/secrets/.env" ]; then
  echo "[$(TS)] CRITICAL: secrets/.env not found — bootstrap cannot continue" | tee -a "$LOG"
  exit 1
fi
echo "[$(TS)] ✅ Secrets file present" | tee -a "$LOG"

# STEP 2: Load secrets
while IFS= read -r line; do
  [[ "$line" =~ ^[A-Z_][A-Z_0-9]*= ]] && export "$line" 2>/dev/null || true
done < "$HOME/.openclaw/secrets/.env"
echo "[$(TS)] ✅ Secrets loaded" | tee -a "$LOG"

# STEP 3: Start PM2 from saved state
if command -v pm2 &>/dev/null; then
  pm2 resurrect 2>&1 | tail -3 | tee -a "$LOG"
  sleep 5
  ONLINE=$(pm2 jlist 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print(sum(1 for p in d if p.get('pm2_env',{}).get('status')=='online'))" 2>/dev/null || echo "?")
  echo "[$(TS)] ✅ PM2 resurrected — $ONLINE processes online" | tee -a "$LOG"
else
  echo "[$(TS)] WARNING: pm2 not found" | tee -a "$LOG"
fi

# STEP 4: Verify critical services
echo "[$(TS)] Verifying critical services..." | tee -a "$LOG"
declare -A PORTS=(["alusi-gateway"]=8788 ["n8n"]=5678 ["postgresql"]=5432 ["ollama"]=11434 ["mission-control"]=3333)
for SERVICE in "${!PORTS[@]}"; do
  PORT="${PORTS[$SERVICE]}"
  if nc -z 127.0.0.1 "$PORT" 2>/dev/null; then
    echo "[$(TS)] ✅ $SERVICE (port $PORT): UP" | tee -a "$LOG"
  else
    echo "[$(TS)] ⚠️  $SERVICE (port $PORT): DOWN — may need pm2 start" | tee -a "$LOG"
  fi
done

# STEP 5: Verify governance baseline
echo "[$(TS)] Verifying governance baseline..." | tee -a "$LOG"
cd "$HOME/.openclaw/workspace"
TAG_EXISTS=$(git tag -l v1.0.0 2>/dev/null)
if [ "$TAG_EXISTS" = "v1.0.0" ]; then
  echo "[$(TS)] ✅ Governance baseline v1.0.0 tag present" | tee -a "$LOG"
else
  echo "[$(TS)] ⚠️  Governance tag v1.0.0 not found — check git state" | tee -a "$LOG"
fi

# STEP 6: Verify trading agents
echo "[$(TS)] Verifying trading agents..." | tee -a "$LOG"
for AGENT in cashclaw_director cashclaw_arb polymarket-trader trading_sentinel; do
  STATUS=$(pm2 jlist 2>/dev/null | python3 -c "
import json,sys
d=json.load(sys.stdin)
for p in d:
    if p.get('name')=='$AGENT':
        print(p.get('pm2_env',{}).get('status','?'))
        break
else:
    print('not_found')
" 2>/dev/null)
  echo "[$(TS)] Trading: $AGENT = $STATUS" | tee -a "$LOG"
done

# STEP 7: Run B9 health check
bash "$HOME/.openclaw/workspace/scripts/validation/runtime_health_check.sh" 2>&1 | tail -2 | tee -a "$LOG"

echo "[$(TS)] ════════════════════════════════════" | tee -a "$LOG"
echo "[$(TS)] BOOTSTRAP COMPLETE — review log: $LOG" | tee -a "$LOG"
echo "[$(TS)] PM2 startup requires sudo (one-time): sudo env PATH=\$PATH:/usr/local/bin /usr/local/lib/node_modules/pm2/bin/pm2 startup launchd -u NeoOC --hp /Users/NeoOC" | tee -a "$LOG"
