#!/bin/bash
# Open Empire Health Check — post-migration validation
# Run: bash ~/.openclaw/workspace/health_check.sh
# Safe: read-only, no writes, no restarts

PASS=0; FAIL=0
check() {
  local label="$1"; local cmd="$2"; local expect="$3"
  result=$(eval "$cmd" 2>/dev/null | head -1)
  if echo "$result" | grep -q "$expect"; then
    echo "  PASS  $label"
    ((PASS++))
  else
    echo "  FAIL  $label (got: ${result:0:60})"
    ((FAIL++))
  fi
}

echo "=== Open Empire Health Check $(date '+%Y-%m-%d %H:%M CDT') ==="
check "PostgreSQL"     "psql -h 127.0.0.1 -p 5432 -U NeoOC -d clawdb -t -A -c 'SELECT 1'"  "1"
check "KG entities"    "psql -h 127.0.0.1 -p 5432 -U NeoOC -d clawdb -t -A -c 'SELECT COUNT(*) FROM kg_entities;'" "5"
check "OE-Proxy"       "curl -sm 3 http://127.0.0.1:4100/health"         "ok"
check "n8n"            "curl -sm 3 http://localhost:5678/healthz"         "ok"
check "Ollama"         "curl -sm 3 http://127.0.0.1:11434/api/tags"      "models"
check "Free-Way 8082"  "curl -sm 3 http://127.0.0.1:8082/health"         "ok"
check "FCC-8083"       "curl -sm 3 -H 'Authorization: Bearer open-empire-local' http://127.0.0.1:8083/v1/models" "data"
check "KG-API"         "curl -sm 3 http://127.0.0.1:6279/health"          "ok\|error"
check "Mission Control" "curl -sm 3 http://127.0.0.1:3333"               "html\|200\|Mission"
check "Grafana"        "curl -sm 3 http://127.0.0.1:3001"                 "200\|html\|FCC"
check "Router import"  "cd ~/.openclaw/workspace/router && python3 -c 'import adaptive_router; print(len(adaptive_router.ALL_CANDIDATES))'" "2"
check "BLCO monitor"   "python3 ~/.openclaw/blco/blco_email_monitor.py --once --quiet 2>/dev/null" "MONITOR_RESULT"
check "Calendar tests" "python3 ~/.openclaw/blco/test_compute_next_run.py 2>/dev/null | tail -1" "run\[5\]"
check "Memory index"   "python3 -c \"import sqlite3,pathlib; db=pathlib.Path.home()/'.openclaw/agents/main/agent/openclaw-agent.sqlite'; c=sqlite3.connect(str(db)); print(c.execute('SELECT COUNT(*) FROM memory_index_chunks_vec_rowids').fetchone()[0])\"" "[0-9]"
check "PM2 online"     "pm2 jlist 2>/dev/null | python3 -c \"import sys,json; procs=json.load(sys.stdin); print(sum(1 for p in procs if p.get('pm2_env',{}).get('status')=='online'))\"" "3"

echo ""
echo "Result: $PASS PASS / $FAIL FAIL"
[ $FAIL -eq 0 ] && echo "STATUS: HEALTHY" || echo "STATUS: DEGRADED ($FAIL checks failed)"
