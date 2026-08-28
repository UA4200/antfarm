# 🏛️ OPEN EMPIRE — GOLDEN BASELINE V2
**POST REPO ESTATE BUILD**
Version: V2 | Status: ✅ CERTIFIED | Generated: 2026-08-28 07:42 CDT
Supersedes: `OPEN_EMPIRE_GOLDEN_BASELINE_V1.json`

---

## 📋 WHAT CHANGED FROM V1

| # | Change |
|---|--------|
| 1 | `open-empire-core` cloned from UA4200 (commit 123eb75) |
| 2 | `alusi-core` cloned from UA4200 (commit 15b122a) |
| 3 | `OpenClaw-Agent-Command-Center` cloned from UA4200 (commit a454808) |
| 4 | `awesome-openclaw-usecases` cloned from UA4200 (commit 659895e) |
| 5 | `blco-pipeline` pushed to UA4200 (commit 2906b1c) |
| 6 | `trading` git init + first commit c97d732 — **LOCAL_ONLY, Nathan action pending** |
| 7 | npm installs completed: `openhuman`, `hermes-agent`, `OC-Agent-CC` |
| 8 | pip installs completed: `iFixAi` (venv), `ai-hedge-fund` (venv), `hyperliquid` (venv) |
| 9 | 43 repos classified in repository registry |
| 10 | Backup system repaired — pg_dump PATH fixed, 6h cron active |
| 11 | OpenAI registered as TIER3/4 provider in oe-proxy |
| 12 | Backup count: 28 (↑1 since V1); latest: `clawdb_20260828_0647_autotest.sql` (60KB) |

---

## 🖥️ HOST

| Property | Value |
|----------|-------|
| OS | macOS 12.7.6 x86_64 |
| Hostname | Ugos-Mac-mini |
| User | NeoOC |
| launchd services | postgresql@18 |

---

## ⚙️ RUNTIMES (live-verified 2026-08-28)

| Runtime | Version | Notes |
|---------|---------|-------|
| Node.js | v24.14.0 | ⚠️ v24.15+ needed to fix embedding |
| Python3 | 3.14.6 | |
| PostgreSQL | 18.3 | launchd-managed, port 5432 |
| PM2 | 7.0.1 | |
| Git | 2.53.0 | |
| n8n | — | via PM2, port 5678 |
| Ollama | — | PM2 id 22, port 11434, 6 models |

---

## 📦 REPOSITORY ESTATE (43 total)

| Category | Count |
|----------|-------|
| DEPLOYED & CERTIFIED | 3 |
| INSTALLED & CERTIFIED | 17 |
| SYNCED REFERENCE ONLY | 11 |
| DEFERRED (with reason) | 9 |
| REJECTED (with reason) | 2 |
| SUPERSEDED | 1 |
| **Total** | **43** |

### ⚠️ Local-Only Critical
- `trading` — commit c97d732 — **Nathan must create UA4200/trading (private) and push**

---

## 🐙 UA4200 GITHUB REPOS (10 tracked)

| Repo | Remote | Commit | Status |
|------|--------|--------|--------|
| workspace (git-github) | UA4200/git-github | 548e46b | ✅ SYNCED |
| blco-pipeline | UA4200/blco-pipeline | 2906b1c | ✅ SYNCED |
| **trading** | **PENDING** | **c97d732** | **🔴 LOCAL_ONLY_CRITICAL** |
| alusi-core | UA4200/alusi-core | 15b122a | ✅ SYNCED |
| open-empire-core | UA4200/open-empire-core | 123eb75 | ✅ SYNCED |
| antfarm | UA4200/antfarm | HEAD | ✅ SYNCED |
| mission-control | UA4200/mission-control | HEAD | ✅ SYNCED |
| hermes-agent | UA4200/hermes-agent | 44cdf55 | ✅ SYNCED |
| OpenClaw-Agent-Command-Center | UA4200/OpenClaw-Agent-Command-Center | a454808 | ✅ SYNCED |
| awesome-openclaw-usecases | UA4200/awesome-openclaw-usecases | 659895e | ✅ SYNCED |

---

## 🔧 SERVICES (PM2)

**Live verified: 34 online / 40 total** — 6 intentionally stopped

| ID | Name | Status | Port/Cycle |
|----|------|--------|-----------|
| 0 | executor | 🟢 online | continuous |
| 1 | heartbeat | 🟢 online | continuous |
| 2 | alusi-gateway | 🟢 online | continuous |
| 3 | alusi-telegram-adapter | 🟢 online | continuous |
| 4 | alusi-discord-adapter | 🟢 online | continuous |
| 5 | alusi-controlled-worker | 🟢 online | continuous |
| 6 | alusi-orchestrator | 🟢 online | continuous |
| 10 | hyrvea-monitor | 🟢 online | continuous |
| 11 | email-dispatcher | ⬛ stopped | on-demand |
| 12 | openclaw-dashboard | ⬛ stopped | legacy |
| 13 | exec-gateway | 🟢 online | continuous |
| 14 | telegram-approvals | 🟢 online | continuous |
| 15 | ecosystem.email-dispatcher | 🟢 online | continuous |
| 16 | pnl-audit | ⬛ stopped | on-demand |
| 17 | mission-control | 🟢 online | :3333 |
| 22 | ollama | 🟢 online | :11434 |
| 30 | cashclaw_director | 🟢 online | every 5min |
| 31 | cashclaw_arb | 🟢 online | every 5min |
| 32 | polymarket-trader | 🟢 online | 15min cycle |
| 33 | trading_sentinel | 🟢 online | every 5min |
| 33 | open-empire-federation-staging | 🟢 online | every 15min |
| 34 | open-empire-lifecycle-staging | 🟢 online | every 15min |
| 36 | freeway | 🟢 online | :8082 |
| 37 | grafana | 🟢 online | :3001 |
| 38 | fcc-metrics-exporter | 🟢 online | every 5min |
| 40 | oe-proxy | 🟢 online | :4100 |
| 42 | kg-api | 🟢 online | :6279 |
| 46 | fcc-8083 | 🟢 online | :8083 |

### launchd (not PM2)
| Service | Status | Port |
|---------|--------|------|
| postgresql@18 | 🟢 active | 5432 |

---

## 🗄️ DATABASE

| Property | Value |
|----------|-------|
| Engine | PostgreSQL 18.3 |
| Port | 5432 |
| Managed by | launchd (pid ~568) |
| Entities | **58** (live-verified) |
| Relationships | 20 |
| Backup count | **28** |
| Latest backup | `clawdb_20260828_0647_autotest.sql` (60KB) |
| Backup location | `~/.openclaw/backups/clawdb/` |
| Backup schedule | Every 6h (cron fixed — PATH includes /usr/local/bin) |
| Restore method | `pg_restore -Fc` (avoids `\restrict` issue) |

---

## 🧠 INFERENCE STACK

### oe-proxy (port 4100)
- **21 providers** — 13 free, 8 paid
- Routing: `haiku → Groq free` | `sonnet → Groq70B/free` | `opus → Anthropic premium`

### freeway (port 8082)
- 5 providers, 72 models, COST_OPTIMIZED_INFERENCE
- Providers: openrouter / cohere / cerebras / nvidia / mistral

### fcc-8083 (port 8083)
- 7 providers, 71 models
- OpenAI-shaped: `/v1/models` ✅ | `/v1/chat/completions` ✅ | `/v1/responses` ❌ (Codex incompatible)

### Ollama (port 11434)
- 6 local models, $0 cost

### OpenAI
- Status: OPERATIONAL, TIER3/TIER4

---

## 💾 MEMORY / EMBEDDING

| Property | Value |
|----------|-------|
| Embedding status | ⚠️ **DEGRADED** |
| Root cause | stale providerKey after Node version mismatch |
| Fix | Update Node 24.14 → 24.15+ then: `openclaw memory index --force` |
| Data integrity | ✅ Intact |
| KG entities | 58 |
| Wiki | ✅ OK |

---

## 💰 TRADING CAPITAL

| Platform | Balance | Daily Spend Cap |
|----------|---------|----------------|
| Kalshi | $25.19 | $10 (cashclaw_director) |
| Polymarket US | $40.00 | $10 (polymarket_trader) |
| Arb (combined) | shared | $10 (cashclaw_arb) |
| **Total deployed** | **$65.19** | |

---

## 📦 PACKAGE INSTALLS

### npm (completed)
- ✅ `openhuman`
- ✅ `hermes-agent`
- ✅ `OC-Agent-CC`

### pip / venv (completed)
- ✅ `iFixAi` (dedicated venv)
- ✅ `ai-hedge-fund` (dedicated venv)
- ✅ `hyperliquid-trading-agent` (dedicated venv)

---

## ⚠️ KNOWN EXCEPTIONS

### 🔴 EX-001 — HIGH: trading GitHub remote missing
- **Item:** Local repo `trading` has no GitHub remote
- **Commit:** c97d732
- **Action required (Nathan):** `gh repo create UA4200/trading --private` then `git push -u origin main`

### 🟡 EX-002 — MEDIUM: Embedding DEGRADED
- **Item:** `openclaw memory index` fails — stale providerKey
- **Action:** Update Node v24.14.0 → v24.15+ then run `openclaw memory index --force`

### 🟢 EX-003 — LOW: 6 PM2 processes stopped
- **Item:** email-dispatcher (11), openclaw-dashboard (12), pnl-audit (16) are stopped
- **Action:** None — intentionally stopped (on-demand/legacy)

---

## 🔄 ROLLBACK POINT

**Tag:** `2026-08-28-post-repo-estate`

| Artifact | Reference |
|----------|-----------|
| workspace commit | 548e46b |
| blco commit | 2906b1c |
| trading commit | c97d732 |
| alusi-core commit | 15b122a |
| open-empire-core commit | 123eb75 |
| DB backup | `clawdb_20260828_0647_autotest.sql` |

**Restore DB:**
```bash
pg_restore -h 127.0.0.1 -U NeoOC -d clawdb -Fc \
  ~/.openclaw/backups/clawdb/clawdb_20260828_0647_autotest.sql
```

---

## 🚀 STARTUP SEQUENCE

```
0. launchd auto-starts PostgreSQL 18.3 (port 5432)
1. pm2 resurrect          # restore all PM2 processes
2. pm2 status             # verify 34+ online
3. curl http://127.0.0.1:4100/health       # oe-proxy
4. curl http://127.0.0.1:8082/v1/models    # freeway
5. curl http://localhost:5678/healthz      # n8n
6. psql -h 127.0.0.1 -d clawdb -c 'SELECT COUNT(*) FROM kg_entities;'
```

---

## 🩺 HEALTH SUITE

```bash
pm2 status
curl http://127.0.0.1:4100/health
curl http://127.0.0.1:8082/v1/models
curl http://127.0.0.1:8083/v1/models
curl http://127.0.0.1:3001/
curl http://localhost:5678/healthz
psql -h 127.0.0.1 -d clawdb -c 'SELECT COUNT(*) FROM kg_entities;'
curl http://127.0.0.1:6279/health
curl http://localhost:11434/api/tags
```

---

*Generated by OpenClaw subagent | 2026-08-28 07:42 CDT*
*Certified against live system readings. Next review: next major infra change.*
