# Open Empire Migration Runbook
**Version:** 1.0 | **Date:** 2026-08-28 | **Authority:** Nathan Asiegbu
**Status:** DRAFT — DO NOT EXECUTE until Nathan authorizes cutover

---

## Prerequisites (must ALL be TRUE before cutover)

### Source Machine (Mac Mini / NeoOC)
- [ ] `pm2 save --force` — ensure dump.pm2 is current
- [ ] `pg_dump -Fc --no-privileges --no-owner clawdb > /tmp/clawdb_final.pgdump` — final DB snapshot
- [ ] All trading agents stopped: `pm2 stop cashclaw_director cashclaw_arb polymarket-trader trading_sentinel`
- [ ] Verify no open orders: check Kalshi + Polymarket positions manually
- [ ] n8n workflows paused or exports saved
- [ ] Final git push for workspace + blco repos confirmed

### Target Machine (new machine)
- [ ] macOS up to date
- [ ] Homebrew installed
- [ ] Node.js ≥24.15.0 via nvm
- [ ] Python 3.14.x installed
- [ ] PostgreSQL 18.x installed (Homebrew, launchd-managed)
- [ ] PM2 installed globally: `npm install -g pm2`
- [ ] Git + SSH keys configured (same UA4200 SSH key as source)
- [ ] Ollama installed (https://ollama.ai)
- [ ] Free disk: ≥50GB available

---

## Transfer Order

### Phase 1 — Secrets (manual, encrypted)
1. Copy `~/.openclaw/secrets/.env` via AirDrop or encrypted USB — **never email or cloud**
2. Verify perms: `chmod 600 ~/.openclaw/secrets/.env`
3. Spot-check: `wc -l ~/.openclaw/secrets/.env` → expect 258 lines
4. **Do NOT sync via iCloud, Dropbox, or any cloud service**

### Phase 2 — Databases
```bash
# Source: create final snapshot
/usr/local/bin/pg_dump -h 127.0.0.1 -p 5432 -U NeoOC -Fc --no-privileges --no-owner clawdb \
  > ~/transfer/clawdb_migration.pgdump
shasum -a 256 ~/transfer/clawdb_migration.pgdump > ~/transfer/clawdb_migration.sha256

# Target: create DB and restore
createdb clawdb
pg_restore -h 127.0.0.1 -U <target_user> --no-privileges --no-owner -d clawdb \
  ~/transfer/clawdb_migration.pgdump
psql -h 127.0.0.1 -d clawdb -c "SELECT COUNT(*) FROM kg_entities;"  # expect: 58+
```

### Phase 3 — n8n
```bash
# Source: export all workflows
# Via n8n UI: Settings → Export → Download all
cp -r ~/.n8n ~/transfer/n8n_backup/

# Target:
# Install n8n: npm install -g n8n
# Copy backup: cp -r ~/transfer/n8n_backup/.n8n ~/
# Import workflows via UI or n8n CLI
```

### Phase 4 — Repositories (git clone from GitHub)
```bash
# All canonical repos — clone fresh on target
mkdir -p ~/.openclaw/{repos,workspace}
git clone git@github.com:UA4200/git-github.git ~/.openclaw/workspace
git clone git@github.com:UA4200/blco-pipeline.git ~/.openclaw/blco
git clone git@github.com:UA4200/trading.git ~/.openclaw/trading
git clone git@github.com:UA4200/alusi-core.git ~/.openclaw/repos/installed/alusi-core
git clone git@github.com:UA4200/open-empire-core.git ~/.openclaw/repos/installed/open-empire-core
git clone git@github.com:UA4200/mission-control.git ~/.openclaw/workspace/mission-control
git clone git@github.com:UA4200/hermes-agent.git ~/.openclaw/repos/installed/hermes-agent
git clone git@github.com:UA4200/OpenClaw-Agent-Command-Center.git ~/.openclaw/repos/installed/OpenClaw-Agent-Command-Center
git clone git@github.com:UA4200/awesome-openclaw-usecases.git ~/.openclaw/repos/installed/awesome-openclaw-usecases
# antfarm is a workspace subdir — included in workspace clone above
```

### Phase 5 — Python Environments
```bash
# Trading agents
cd ~/.openclaw/trading && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt

# BLCO monitor (stdlib only — no venv needed)
python3 -c "import imaplib,smtplib,hashlib; print('stdlib OK')"

# Router (stdlib only)
cd ~/.openclaw/workspace/router && python3 -c "import adaptive_router; print('OK')"
```

### Phase 6 — Ollama Models
```bash
# Install models (do on target, not transfer — large files)
ollama pull qwen2.5:3b
ollama pull llama3.2:3b
ollama pull phi3:mini
ollama pull qwen2.5:1.5b
ollama pull gemma2:2b
ollama pull tinyllama
```

### Phase 7 — OpenClaw
```bash
# Install OpenClaw on target
npm install -g openclaw

# Configure
cp ~/.openclaw/config.json ~/.openclaw/  # or reconfigure
openclaw memory index --force  # rebuild memory index with new machine's key
```

### Phase 8 — PM2 Processes
```bash
# Copy PM2 ecosystem files
cp ~/.pm2/dump.pm2 ~/transfer/
# On target: pm2 resurrect (after adjusting paths if needed)
# Start services in dependency order:
# 1. PostgreSQL (launchd)
# 2. ollama
# 3. freeway, fcc-8083
# 4. oe-proxy, kg-api
# 5. n8n, mission-control, grafana
# 6. alusi-gateway, telegram, discord adapters
# 7. cashclaw agents (LAST — only after all above verified)
```

### Phase 9 — Free-Way / FCC
```bash
# Clone and install
git clone <free_llm_router_upstream> ~/.openclaw/repos/free_llm_router
cd ~/.openclaw/repos/free_llm_router/installed/Free-Way
npm install
cp .env.8083 .env.8083  # already in repo (no secrets in file)
# Secrets loaded from ~/.openclaw/secrets/.env at startup
```

---

## Validation Sequence (run on target after setup)

```bash
#!/bin/bash
# health_check.sh — post-migration validation

echo "=== PostgreSQL ===" && psql -h 127.0.0.1 -d clawdb -c 'SELECT COUNT(*) FROM kg_entities;'
echo "=== OE-Proxy ===" && curl -s http://127.0.0.1:4100/health
echo "=== n8n ===" && curl -s http://localhost:5678/healthz
echo "=== Ollama ===" && curl -s http://127.0.0.1:11434/api/tags | python3 -c "import sys,json;d=json.load(sys.stdin);print(f'{len(d[\"models\"])} models')"
echo "=== Free-Way ===" && curl -s http://127.0.0.1:8082/health
echo "=== BLCO Monitor ===" && python3 ~/.openclaw/blco/blco_email_monitor.py --once --quiet | grep MONITOR_RESULT
echo "=== Router ===" && cd ~/.openclaw/workspace/router && python3 -c "import adaptive_router; print(f'{len(adaptive_router.ALL_CANDIDATES)} candidates')"
echo "=== Memory ===" && python3 -c "
import sqlite3,pathlib
db=pathlib.Path.home()/'.openclaw/agents/main/agent/openclaw-agent.sqlite'
c=sqlite3.connect(str(db))
vec=c.execute('SELECT COUNT(*) FROM memory_index_chunks_vec_rowids').fetchone()[0]
print(f'Vector index: {vec} entries')
"
echo "=== PM2 ===" && pm2 status | grep -c "online" | xargs echo "online processes:"
echo "=== Calendar tests ===" && python3 ~/.openclaw/blco/test_compute_next_run.py
```

---

## Rollback Plan

If migration fails at any phase:

| Phase | Rollback Action |
|---|---|
| 1-3 (secrets/DB) | Stop target, revert to source, no data lost |
| 4 (repos) | Re-clone from GitHub (all canonical source is remote) |
| 5-6 (envs/models) | Delete venv/models, re-install |
| 7 (OpenClaw) | npm uninstall -g openclaw, reinstall from scratch |
| 8 (PM2) | pm2 delete all on target; restore source machine from dump |
| 9 (Free-Way) | pm2 stop freeway fcc-8083; source machine unaffected |

**Trading rollback**: Source machine trading agents should remain STOPPED on source during migration. If migration fails, restart them on source: `pm2 start cashclaw_director cashclaw_arb polymarket-trader trading_sentinel`

---

## Duplicate Job Protection

**CRITICAL:** After migration, the source machine PM2 processes must be stopped before starting trading on target:

```bash
# Source machine — run BEFORE starting trading agents on target:
pm2 stop cashclaw_director cashclaw_arb polymarket-trader trading_sentinel
pm2 stop blco-email-monitor  # avoid duplicate IMAP sessions
```

**Scheduled cron jobs** must be reviewed on source and disabled after migration:
```bash
crontab -l > ~/crontab_source_backup.txt
crontab -r  # remove all cron on source after migration verified
```

---

## Deferred Items (do not block migration)

| Item | Reason | Next Action |
|---|---|---|
| Groq billing verification | API returned 403 | Check Groq console, re-add to free pool if verified |
| Ollama embedding model | Not installed | Consider nomic-embed-text on 32GB target (3GB, fast) |
| openhuman entry-point | TypeScript monorepo, no main | Low priority — reference only |
| Obsidian Copilot plugin | Makes external API calls | Disable or configure to use local provider on target |

---

## Unresolved Decisions (require Nathan)

1. **Target machine user account name** — affects all path references
2. **n8n database migration strategy** — SQLite copy vs fresh credentials
3. **Obsidian vault sync** — iCloud? Manual copy? (caution: .obsidianignore must transfer)
4. **Kalshi/Polymarket session cookies** — may need re-auth on new machine

---

## Authorization Gate

This runbook is ready. **DO NOT EXECUTE until Nathan explicitly says: "Begin migration."**

Migration readiness certificate: `~/.openclaw/workspace/OPEN_EMPIRE_FINAL_PRE_MIGRATION_FREEZE_MANIFEST.json`
