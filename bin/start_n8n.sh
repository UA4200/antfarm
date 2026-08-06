#!/bin/bash
# n8n startup wrapper — loads secrets before starting
set -a
while IFS= read -r line; do
  [[ "$line" =~ ^[A-Z_][A-Z_0-9]*= ]] && export "$line" 2>/dev/null || true
done < "$HOME/.openclaw/secrets/.env"
set +a
exec /Users/NeoOC/.npm-global/bin/n8n start
