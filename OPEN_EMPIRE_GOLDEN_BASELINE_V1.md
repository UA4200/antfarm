# OPEN EMPIRE GOLDEN BASELINE V1
**Generated:** 2026-08-28 | **Status:** CERTIFIED (reconstruction proven)
**Authority:** Nathan Asiegbu | **Maintained by:** Alusi / PMO

---

## HOST & RUNTIME ENVIRONMENT

| Item | Value |
|---|---|
| Host | Ugos-Mac-mini (NeoOC) — macOS 12.7.6 x86_64 |
| Node | v24.14.0 |
| Python | 3.14.6 |
| PostgreSQL | 18.3 (launchd-managed, port 5432) |
| PM2 | 7.0.1 |
| Ollama | PM2 id=22, port 11434, 6 models |
| Git | 2.53.0 |
| n8n | PM2 id=34, port 5678, 14 workflows (7 active) |

---

## CANONICAL REPOSITORIES

| Repo | Path | Remote | Commit | Priority |
|---|---|---|---|---|
| workspace | ~/.openclaw/workspace | UA4200/git-github.git | 62e6bd1 | P0 |
| blco | ~/.openclaw/blco | UA4200/blco-pipeline.git | 49f83f9 | P0 |
| trading | ~/.openclaw/trading | **NONE (Nathan action)** | c97d732 | P0 |
| free_llm_router | ~/.openclaw/repos/free_llm_router | upstream | HEAD | P0 |
| antfarm | ~/.openclaw/workspace/antfarm | upstream | HEAD | P0 |
| mission-control | ~/.openclaw/workspace/mission-control | UA4200/mission-control.git | HEAD | P0 |
| iFixAi | ~/.openclaw/repos/iFixAi | upstream | HEAD | P1 |
| openhuman | ~/.openclaw/repos/openhuman | upstream | HEAD | P1 |
| Personal_AI_Infrastructure | ~/.openclaw/repos/Personal_AI_Infrastructure | upstream | HEAD | P1 |
| agency-agents | ~/.openclaw/repos/installed/agency-agents | upstream | HEAD | P1 |
| claude-code-ultimate-guide | ~/.openclaw/repos/installed/claude-code-ultimate-guide | upstream | HEAD | P1 |
| GitNexus | ~/.openclaw/repos/installed/GitNexus | upstream | HEAD | P1 |
| hermes-agent | ~/.openclaw/repos/installed/hermes-agent | upstream | HEAD | P2 |
| ai-hedge-fund | ~/.openclaw/repos/installed/ai-hedge-fund | upstream | HEAD | P2-SANDBOX |
| hyperliquid-trading-agent | ~/.openclaw/repos/installed/hyperliquid-trading-agent | upstream | HEAD | P2-SANDBOX |
| ruflo | ~/.openclaw/repos/ruflo | upstream | HEAD | DEFERRED |

**Strategic missing (not found locally):** open-empire-core, alusi-core, AI-Trader

---

## ACTIVE SERVICES & PORTS

| Service | Port | PM2 ID | Status | Health Check |
|---|---|---|---|---|
| clawdb (PostgreSQL) | 5432 | launchd | online | `psql -h 127.0.0.1 -d clawdb -c 'SELECT 1'` |
| n8n | 5678 | 34 | online | `curl http://localhost:5678/healthz` |
| ollama | 11434 | 22 | online | `curl http://127.0.0.1:11434/api/tags` |
| freeway (Free-Way) | 8082 | 35 | online | `curl http://127.0.0.1:8082/health` |
| fcc-8083 | 8083 | 46 | online | `curl http://127.0.0.1:8083/v1/models` |
| oe-proxy | 4100 | 38 | online | `curl http://127.0.0.1:4100/health` |
| kg-api | 6279 | 39 | online | `curl -H "Authorization: Bearer $KG_KEY" http://127.0.0.1:6279/health` |
| mission-control | 3333 | 13 | online | — |
| grafana / FCC dashboard | 3001 | 36 | online | — |
| CashClaw director | — | 29 | online | PM2 status |
| CashClaw arb | — | 30 | online | PM2 status |
| Polymarket trader | — | 31 | online | PM2 status |
| Trading sentinel | — | 32 | online | PM2 status |

**PM2 totals:** 40 processes, 34 online, 6 stopped

---

## DATABASE STATE

| DB | Tables | KG Entities | KG Relationships | Latest Backup |
|---|---|---|---|---|
| clawdb | 10 | 58 | 20 | clawdb_20260828_0600.sql (60KB, 0.6h) |

**Backup schedule:** Every 6h via `/usr/local/bin/pg_dump` (fixed 2026-08-28 — was 0-byte since Aug 9)
**Backup count:** 27 files in `~/.openclaw/backups/clawdb/`
**Restore:** `psql -h 127.0.0.1 -U NeoOC -d clawdb < latest.sql`

---

## INFERENCE ROUTING STACK

```
TIER 0: deterministic/scripts/zero-token
TIER 1: ollama (local, $0) — 6 models, keep_alive=-1
TIER 2: groq · cohere · openrouter · cerebras · nvidia (free cloud, $0)
         → via oe-proxy port 4100 (adaptive scoring, circuit-breaker)
         → fcc-8083 port 8083 (71 free models, FREEWAY_API_KEY)
TIER 3: mistral · openai/gpt-4o-mini · openai/gpt-4.1-mini (low-cost paid)
TIER 4: openai/gpt-4o · openai/gpt-4.1 · openai/o3-mini · anthropic (premium)
TIER 5: openai/o1-mini — owner-gated, excluded from auto-routing
```

**Providers registered in oe-proxy:** 21 total (13 free, 8 paid)
**OpenAI:** OPERATIONAL (validated 2026-08-28, auth via OPENAI_API_KEY)
**Free-first verified:** 6/6 task classes served free at 100% in benchmark

---

## MEMORY & KNOWLEDGE LAYER

| Layer | Status | Count |
|---|---|---|
| ClawDB KG entities | OPERATIONAL | 58 |
| ClawDB KG relationships | OPERATIONAL | 20 |
| Memory .md files | OPERATIONAL | 106 files |
| KG API (port 6279) | OPERATIONAL (auth required) | — |
| memory_search embedding | **DEGRADED** (15s timeout) | Data intact |
| Canonical outreach ledger | OPERATIONAL | 13 entries |

**Embedding fix needed:** OpenClaw memory.backend config — Nathan decision required.
All underlying data is intact; degradation is in the semantic search layer only.

---

## BACKUP & RECOVERY

| System | Location | Schedule | Latest | Status |
|---|---|---|---|---|
| clawdb | ~/.openclaw/backups/clawdb/ | Every 6h (fixed) | 0.6h ago, 60KB | ✅ VALID |
| n8n | ~/.openclaw/backups/ | cron tar | Present | ✅ |
| PM2 | ~/.pm2/dump.pm2 | Every 30min (added 2026-08-28) | 8.1h ago | ✅ |
| Secrets | ~/.openclaw/secrets/.env | Manual | Current | ✅ perms 600 |

**Reconstruction proven:** Isolated DB restore — 58 entities, 20 relations, MATCH=YES

---

## STARTUP SEQUENCE

```
0. launchd auto-starts PostgreSQL 18.3 (pid~568)
1. pm2 resurrect  →  restores all 34 online processes
2. Verify: ollama :11434, freeway :8082, fcc-8083 :8083, n8n :5678
3. Verify: oe-proxy :4100, kg-api :6279, mission-control :3333
4. Verify: CashClaw agents (director, arb, polymarket-trader, sentinel)
```

## SHUTDOWN SEQUENCE

```
1. pm2 save --force
2. /usr/local/bin/pg_dump -h 127.0.0.1 -U NeoOC clawdb > ~/.openclaw/backups/clawdb/shutdown_$(date +%Y%m%d_%H%M).sql
3. pm2 stop all
4. PostgreSQL stops with system (launchd-managed)
```

---

## HEALTH CHECK SUITE

```bash
curl -s http://127.0.0.1:4100/health        # oe-proxy
curl -s http://localhost:5678/healthz        # n8n
psql -h 127.0.0.1 -d clawdb -c 'SELECT 1'  # postgres
pm2 status                                   # all processes
python3 ~/.openclaw/blco/blco_email_monitor.py --once --quiet | grep MONITOR_RESULT
cd ~/.openclaw/workspace/router && python3 -c 'import adaptive_router; print(len(adaptive_router.ALL_CANDIDATES))'
python3 ~/.openclaw/blco/test_compute_next_run.py  # calendar tests
```

---

## KNOWN EXCEPTIONS & OPEN ITEMS

| ID | Severity | Item | Owner |
|---|---|---|---|
| EX-001 | HIGH | trading repo has no GitHub remote | Nathan (create repo, set remote) |
| EX-002 | HIGH | blco not yet pushed to remote | Nathan (approve push) |
| EX-003 | MEDIUM | memory_search embedding degraded | Nathan (config decision) |
| EX-004 | LOW | workspace 1500+ untracked files | Alusi (most covered by new .gitignore) |
| EX-005 | RESOLVED | All pre-Aug-28 clawdb backups were 0-byte | Fixed 2026-08-28 |

---

## ROLLBACK POINTS

| Tag | workspace | blco | trading | Backup |
|---|---|---|---|---|
| 2026-08-28-pre-migration | 62e6bd1 | 49f83f9 | c97d732 | clawdb_20260828_0600.sql |

---

## SECRETS INVENTORY (metadata only — 195 keys)

Key categories: AGENTMAIL(9), ANTHROPIC(3), CEREBRAS(4), COHERE(4), DEEPSEEK(4), DISCORD(4), GEMINI(6), GMAIL(4), GROQ(4), HUGGINFACE(4), KALSHI(3), MISTRAL(7), N8N(9), NVIDIA(10), OPENCLAW(5), OPENAI(1), OPENROUTER(6), POLYMARKET(6), SMTP(4), TELEGRAM(6), TWITTER(5), + 74 more categories. Location: `~/.openclaw/secrets/.env` (perms 600, git-ignored).
