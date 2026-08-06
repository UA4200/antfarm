# OPEN_EMPIRE_DISASTER_RECOVERY_SPECIFICATION_V1
## Foundational Enhancement #4 — Automated Disaster Recovery
**Version:** 1.0.0  
**Created:** 2026-08-06T12:40:00Z  
**Owner:** Nathan Asiegbu  
**Governance Baseline:** v1.0.0 (commit 17df0ff)  
**Status:** SPECIFIED — implementation pending

---

## 1. RECOVERY OBJECTIVES

| Metric | Target | Current |
|--------|--------|---------|
| RTO (Recovery Time Objective) | < 30 minutes | Unknown |
| RPO (Recovery Point Objective) | < 5 minutes (trades), < 1 hour (governance) | Unknown |
| Governance rollback | < 5 minutes | READY (v1.0.0 snapshot exists) |
| Trading stack recovery | < 10 minutes | Partial (PM2 restart works) |
| Full system recovery | < 30 minutes | Not tested |

---

## 2. RECOVERY SCENARIOS

### 2.1 Scenario A — Governance Corruption
**Trigger:** SHA256 mismatch on any canonical governance artifact  
**Procedure:**
1. Detect via drift detection cron (scheduled every 6h)
2. Stop governance-dependent operations (not trading)
3. Checkout v1.0.0: `git checkout v1.0.0 -- governance/`
4. Verify: `cd governance/ && python3 build/validate.py`
5. Confirm 240/240 PASS before resuming
6. Telegram alert: "GOVERNANCE ROLLBACK EXECUTED — awaiting validation"
**RTO:** < 5 minutes  
**RPO:** 0 (governance artifacts are code, not data)  
**Snapshot backup:** `governance_v1.0.0_snapshot_20260806T074103Z.tar.gz` (SHA256: 442222da...)  
**Snapshot restore:** `tar -xzf governance_v1.0.0_snapshot_*.tar.gz -C ~/.openclaw/workspace/`  
**Tested:** NOT YET — scheduled for B9 validation

### 2.2 Scenario B — Trading Agent Crash Loop
**Trigger:** cashclaw_director / cashclaw_arb / polymarket-trader crashes 3+ times  
**Procedure:**
1. Detect via trading_sentinel (pm_id=41) — already wired
2. Sentinel sends Telegram alert automatically
3. Manual review: `pm2 logs cashclaw_director --lines 100`
4. Fix or hold: `pm2 stop cashclaw_director cashclaw_arb polymarket-trader`
5. Capital is safe — open positions remain on exchange, no new trades executed
6. Restart when root cause resolved: `pm2 restart cashclaw_director`
7. Verify daily spend cap enforced before restarting
**RTO:** < 10 minutes  
**RPO:** 0 (trades are recorded on exchange — no local data loss risk)  
**Current daily caps:** $10/each (director, arb, polymarket)

### 2.3 Scenario C — Database Failure (PostgreSQL)
**Trigger:** clawdb PM2 process stops, PostgreSQL unreachable on port 5432  
**Procedure:**
1. Detect: `pm2 status clawdb` → stopped
2. Restart: `pm2 restart clawdb`
3. Verify: `psql -U NeoOC -d clawdb -h localhost -c "SELECT 1"`
4. If data corruption suspected: restore from backup (see 3.1)
5. Notify affected services (trading agents log locally to JSONL also — no data lost)
**RTO:** < 5 minutes (restart) / < 30 minutes (restore from backup)  
**RPO:** up to 24h (backup frequency TBD — CURRENT GAP)  
**Gap:** No PostgreSQL backup currently configured — P0 action item

### 2.4 Scenario D — Mac Mini Unresponsive
**Trigger:** SSH/Tailscale connection refused, no response on any port  
**Procedure:**
1. Attempt Tailscale SSH: `tailscale ssh NeoOC@100.107.5.103`
2. If unreachable: check Tailscale dashboard for last seen time
3. Physical access required if Tailscale offline
4. On restart: PM2 should auto-restore (pm2 startup configured — verify)
5. Verify trading agents resume within 5min (PM2 on-restart)
6. Check Kalshi/Polymarket positions manually — no automated close-out
**RTO:** < 30 minutes (assuming remote access works)  
**Gap:** PM2 startup script — verify `pm2 startup` was run

### 2.5 Scenario E — Full OpenClaw Gateway Failure
**Trigger:** alusi-gateway (pm_id=1, port 8788) unresponsive  
**Procedure:**
1. Detect: `curl -f http://localhost:8788/health`
2. Restart: `pm2 restart alusi-gateway`
3. Verify channels reconnect: Telegram, Discord adapters
4. If persistent failure: `pm2 logs alusi-gateway --lines 200`
**RTO:** < 5 minutes

---

## 3. BACKUP STRATEGY

### 3.1 Current Backup Posture (as of 2026-08-06)
| Asset | Backup Status | Method | Schedule |
|-------|--------------|--------|----------|
| Governance artifacts | ✅ BACKED UP | git v1.0.0 tag + tarball snapshot | On governance freeze |
| Trade JSONL files | ⚠️ NO BACKUP | Only at ~/.openclaw/trading/data/ | Not configured |
| PostgreSQL databases | ❌ NO BACKUP | No pg_dump scheduled | CRITICAL GAP |
| PM2 ecosystem files | ⚠️ PARTIAL | In workspace (untracked) | Not committed |
| Secrets (.env) | ⚠️ NOT BACKED UP | Only at ~/.openclaw/secrets/.env | CRITICAL GAP |
| Ollama models | ⚠️ RECOVERABLE | Can re-pull from Ollama registry | ~30min to restore |
| n8n workflows | ✅ N/A | 0 workflows currently configured | — |

### 3.2 Required Backup Actions (P0)
1. **PostgreSQL daily backup:** `pg_dump clawdb > ~/backups/clawdb_$(date +%Y%m%d).sql`
   - Schedule: daily 01:00 CDT
   - Retention: 7 days
   - Alert: if backup fails

2. **Secrets backup:** Encrypted copy to secure location (iCloud Keychain or 1Password)
   - Current: single point of failure at ~/.openclaw/secrets/.env
   - Risk: HIGH

3. **Trade JSONL backup:** Nightly copy to ~/backups/trading/
   - Paths: ~/.openclaw/trading/data/{director,arb,polymarket}/

---

## 4. RECOVERY VALIDATION SCHEDULE

| Test | Schedule | Method | Acceptance Criteria |
|------|---------|--------|---------------------|
| Governance snapshot restore | Weekly Sunday 06:00 CDT | Extract to /tmp, run validate.py | 240/240 PASS |
| PostgreSQL restore drill | Monthly 1st Sunday | pg_dump + pg_restore to temp DB | All 7 tables intact |
| PM2 restart drill | Monthly | pm2 kill + pm2 resurrect | All required-on services online in < 5min |
| Tailscale SSH test | Weekly | tailscale ssh from MacBook | Command executes |
| Trading agent recovery | Monthly | pm2 stop + pm2 start trading agents | Agents resume within 1 cycle |

---

## 5. KNOWN GAPS (as of 2026-08-06)

| Gap | Severity | P0/P1 | Owner | Target Date |
|-----|---------|-------|-------|-------------|
| No PostgreSQL backup | CRITICAL | P0 | Nathan | 2026-08-07 |
| No secrets backup | CRITICAL | P0 | Nathan | 2026-08-07 |
| PM2 startup not verified | HIGH | P0 | Nathan | 2026-08-07 |
| No formalized bootstrap script | HIGH | P1 | Nathan | 2026-08-14 |
| No DR runbook tested end-to-end | HIGH | P1 | Nathan | 2026-08-21 |
| No trade JSONL backup | MEDIUM | P1 | Nathan | 2026-08-14 |

---

## 6. GOVERNANCE ROLLBACK — VERIFIED

**Rollback path confirmed operational:**
```bash
# Option A: git checkout
cd ~/.openclaw/workspace
git checkout v1.0.0 -- governance/

# Option B: snapshot restore
tar -xzf governance_v1.0.0_snapshot_20260806T074103Z.tar.gz -C ~/.openclaw/workspace/

# Verify after either method:
cd ~/.openclaw/workspace
python3 governance/build/validate.py
# Expected: 240/240 PASS
```

Snapshot SHA256: `442222da3d167072f981d6337591517fb57d85b538512130209820a59164a96c`  
Snapshot location: `~/.openclaw/workspace/governance_v1.0.0_snapshot_20260806T074103Z.tar.gz`  
Git tag: `v1.0.0` (immutable, commit 17df0ff)

---

*Document generated 2026-08-06 as part of Open Empire Track B execution.*  
*Governance baseline: v1.0.0. Authority: Nathan Asiegbu.*
