#!/bin/bash
# OE Proxy v2 (Adaptive) launcher — sources secrets before starting
set -a
source /Users/NeoOC/.openclaw/secrets/.env 2>/dev/null || true
source /Users/NeoOC/.openclaw/repos/free_llm_router/installed/Free-Way/.env 2>/dev/null || true
OE_PROXY_PORT=4100
set +a
exec python3 /Users/NeoOC/.openclaw/workspace/router/oe_proxy.py
