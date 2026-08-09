#!/bin/bash
# KG API launcher — sources secrets before starting
set -a
source /Users/NeoOC/.openclaw/secrets/.env 2>/dev/null || true
KG_PORT=6279
set +a
exec python3 /Users/NeoOC/.openclaw/workspace/router/kg_api.py
