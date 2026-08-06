# OPEN_EMPIRE_PROGRESSIVE_DEPLOYMENT_SPECIFICATION_V1
## Foundational Enhancement #9 — Progressive Deployment Strategy
**Version:** 1.0.0  
**Created:** 2026-08-06T12:40:00Z  
**Owner:** Nathan Asiegbu  
**Governance Baseline:** v1.0.0  
**Status:** SPECIFIED — staging environments pending

---

## 1. ENVIRONMENT TOPOLOGY

### Current State (2026-08-06)
Only one environment exists: **Production** (Ugo's Mac Mini, NeoOC user).  
No formal dev/staging separation. All services run in production.

### Target State
```
Development (local branch)
    ↓ [PR + governance check]
Staging (separate PM2 namespace or environment vars)
    ↓ [health gates + validation]
Production (main branch, live PM2)
```

### Environment Definitions

#### Development
- **Host:** Same Mac Mini, separate PM2 namespace `--env development`
- **Purpose:** Feature development, experimentation
- **Data:** Mock/synthetic data only — NEVER live Kalshi/Polymarket APIs
- **Spend cap:** $0 (no real API calls)
- **Governance:** governance validation must PASS before PR

#### Staging
- **Host:** Same Mac Mini, PM2 namespace `--env staging`  
  OR: use `ugos-mac-mini-2` (Tailscale 100.114.191.57) as dedicated staging node when active
- **Purpose:** Integration testing, validation gates, pre-production smoke test
- **Data:** Staging API keys (Kalshi demo if available), clawdb_staging database
- **Spend cap:** $1/day (paper trading only)
- **Governance:** governance validation must PASS + integration tests pass

#### Production
- **Host:** Mac Mini NeoOC (current)
- **Data:** Live — Kalshi $25.19 capital, Polymarket $0.06
- **Spend caps:** $10/day/agent (enforced)
- **Governance:** FROZEN at v1.0.0; changes require change control

---

## 2. DEPLOYMENT PIPELINE

```
Code Change
    ↓
git branch feature/xxx
    ↓
Development testing
    ↓
governance/build/validate.py (must 240/240 PASS)
    ↓
PR to main → GitHub Actions
    ↓
CI: lint + validate + test
    ↓
Staging deploy (pm2 reload --env staging)
    ↓
Staging health gates (5min soak)
    ↓
Canary deploy (10% traffic if applicable)
    ↓
Full production promote
    ↓
Post-deploy validation
    ↓
Registry update
```

---

## 3. HEALTH GATES

### Gate 1 — Pre-Commit
- Governance validation: `python3 governance/build/validate.py` must PASS
- No secrets committed to git (git pre-commit hook)
- AGENTS.md + MEMORY.md consistency check

### Gate 2 — Staging Deploy
- All required PM2 services online in < 60 seconds
- Health endpoints return 200 (where implemented)
- No ERROR-level log entries in first 2 minutes
- Database connectivity confirmed

### Gate 3 — Production Promote
- Staging soak time: minimum 5 minutes
- Trading agents: paper trade must execute at least 1 successful cycle
- Sentinel: confirms monitoring active
- Daily spend cap: verified enforced

### Gate 4 — Post-Deploy Validation
- Full governance validation pass
- Runtime topology matches registry
- Telegram notification: "DEPLOY COMPLETE — [service] v[version] at [timestamp]"

---

## 4. CANARY DEPLOYMENT (Trading Agents)

Trading agents require special canary procedure due to live capital risk:

1. **Deploy to single agent first:** e.g., only restart `cashclaw_director`
2. **Monitor 1 complete cycle (5 min)**
3. **Verify:** no unexpected trades, spend cap respected, logs clean
4. **Then deploy:** remaining agents one at a time
5. **Never restart all 4 trading agents simultaneously**

---

## 5. ROLLBACK PROCEDURE

### Automatic Rollback Triggers
- Health gate failure after deploy
- 3 consecutive PM2 crashes post-deploy
- Governance validation failure post-deploy

### Rollback Steps
```bash
# 1. Stop affected service
pm2 stop [service_name]

# 2. Git checkout previous version
git checkout HEAD~1 -- [service_path]

# 3. Reinstall if package changes
npm install --production

# 4. Restart
pm2 restart [service_name]

# 5. Validate
pm2 status [service_name]
```

### Governance Rollback (if governance was changed)
```bash
git checkout v1.0.0 -- governance/
python3 governance/build/validate.py
# Must see: 240/240 PASS
```

---

## 6. CURRENT GAPS

| Gap | Severity | Action |
|-----|---------|--------|
| No staging environment | HIGH | Create PM2 staging namespace |
| No GitHub Actions workflows | HIGH | Create .github/workflows/ per B5 plan |
| No pre-commit hooks | MEDIUM | Add governance validation hook |
| No automated health endpoints | MEDIUM | Add /health to each service |
| Single environment for trading | HIGH | Requires staging API keys from Kalshi/Polymarket |

---

## 7. IMPLEMENTATION PHASES

### Phase 1 (Immediate — this session)
- ✅ Governance frozen at v1.0.0
- ✅ Git repo initialized with v1.0.0 tag
- Document this spec

### Phase 2 (Week 1 — B5)
- Create GitHub Actions workflows for all UA4200 repos
- Add pre-commit governance validation hook
- Define staging environment variables

### Phase 3 (Week 2)
- Stand up staging PM2 namespace
- Deploy non-trading agents to staging first
- Health endpoint template deployed

### Phase 4 (Week 3-4)
- Paper trading in staging (if Kalshi provides staging API)
- Full canary deploy procedure tested
- Rollback drill completed

---

*Document generated 2026-08-06 as part of Open Empire Track B execution.*  
*Governance baseline: v1.0.0. Authority: Nathan Asiegbu.*
