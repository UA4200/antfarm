#!/bin/bash
# OPEN EMPIRE — Secrets Presence Check
# B9 Continuous Validation — Secrets Layer
# Verifies all critical keys exist in .env (does NOT validate values)

ENV_FILE="$HOME/.openclaw/secrets/.env"
LOG="$HOME/.openclaw/logs/secrets_health_$(date +%Y%m%d).log"
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)

# Critical keys that MUST be present
CRITICAL_KEYS=(
  ANTHROPIC_API_KEY
  OPENCLAW_API_KEY
  OPENCLAW_GATEWAY_TOKEN
  KALSHI_API_KEY_ID
  KALSHI_PRIVATE_KEY_PATH
  DISCORD_BOT_TOKEN
  TELEGRAM_BOT_TOKEN
)

echo "[$TIMESTAMP] SECRETS PRESENCE CHECK START" >> "$LOG"
MISSING=0

for key in "${CRITICAL_KEYS[@]}"; do
  if ! grep -q "^${key}=" "$ENV_FILE" 2>/dev/null; then
    echo "[$TIMESTAMP] MISSING_SECRET: $key not found in .env" >> "$LOG"
    MISSING=$((MISSING+1))
  fi
done

TOTAL=${#CRITICAL_KEYS[@]}
if [ "$MISSING" -eq 0 ]; then
  echo "[$TIMESTAMP] SECRETS_HEALTH: ALL $TOTAL critical keys present" >> "$LOG"
  exit 0
else
  echo "[$TIMESTAMP] SECRETS_HEALTH: $MISSING of $TOTAL critical keys MISSING" >> "$LOG"
  exit 2
fi
