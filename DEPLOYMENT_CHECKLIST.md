# CashClaw_Director HYRVE Monitor - Deployment Checklist

**Date:** 2026-05-10  
**Agent ID:** 0cfbc512  
**Status:** Ready for Deployment ✅

---

## Pre-Deployment (Before First Run)

- [ ] **Get API Key**
  - [ ] Log in to HYRVE dashboard
  - [ ] Navigate to API settings / Agent keys
  - [ ] Copy your `HYRVE_AGENT_API_KEY`
  - [ ] Save it securely

- [ ] **Store API Key**
  - [ ] Choose storage method:
    - [ ] Environment variable (`export HYRVE_AGENT_API_KEY=...`)
    - [ ] Secrets file (`~/.openclaw/secrets/HYRVE_AGENT_API_KEY`)
    - [ ] .env file (`~/.openclaw/.env`)
  - [ ] Verify file permissions (if using file storage)
  - [ ] Test: Run `echo $HYRVE_AGENT_API_KEY` (should show key)

- [ ] **Verify Files**
  - [ ] `hyrve_monitor_v2.js` exists
  - [ ] `setup_hyrve_cron.sh` exists
  - [ ] Both files are executable: `ls -la *.js *.sh`

- [ ] **Create Log Directory**
  - [ ] Run: `mkdir -p ~/.openclaw/memory/logs`
  - [ ] Check: `ls -la ~/.openclaw/memory/logs`

---

## Testing Phase (Validation)

- [ ] **Test 1: Manual Execution**
  ```bash
  cd ~/.openclaw/workspace
  node hyrve_monitor_v2.js
  ```
  - [ ] No errors about missing API key
  - [ ] API response received (or error about connection)
  - [ ] Log file created: `~/.openclaw/memory/logs/hyrve_bid_log.jsonl`

- [ ] **Test 2: Check Logs**
  ```bash
  cat ~/.openclaw/memory/logs/hyrve_bid_log.jsonl
  ```
  - [ ] JSONL format is valid
  - [ ] Contains agent_id: `0cfbc512`
  - [ ] Shows status (ACCEPTED/REJECTED/ERROR)

- [ ] **Test 3: Review Filters**
  - [ ] Confidence filter: >95%
  - [ ] Job types: seo_audit, lead_generation, email_outreach, content_writing
  - [ ] Budget caps enforced correctly
  - [ ] Max mission: $100

---

## Deployment Phase (Go Live)

- [ ] **Option A: Manual Scheduling**
  - [ ] Run setup script: `./setup_hyrve_cron.sh`
  - [ ] Choose frequency (every 15/30 min, hourly, etc.)
  - [ ] Confirm crontab entry: `crontab -l | grep hyrve`

- [ ] **Option B: Manual Cron Entry**
  - [ ] Edit crontab: `crontab -e`
  - [ ] Add cron line (choose frequency):
    ```
    # Every 30 minutes
    */30 * * * * cd /Users/NeoOC/.openclaw/workspace && HYRVE_AGENT_API_KEY="your_key" node hyrve_monitor_v2.js >> ~/.openclaw/memory/logs/hyrve_cron.log 2>&1
    ```
  - [ ] Save and exit editor
  - [ ] Verify: `crontab -l`

- [ ] **Option C: OpenClaw Task**
  - [ ] Create OpenClaw task (if available):
    ```bash
    openclaw task create \
      --name "HYRVE Monitor" \
      --schedule "*/30 * * * *" \
      --command "cd /Users/NeoOC/.openclaw/workspace && node hyrve_monitor_v2.js"
    ```

- [ ] **Verification**
  - [ ] First scheduled run completed
  - [ ] Check logs: `tail ~/.openclaw/memory/logs/hyrve_bid_log.jsonl`
  - [ ] Verify entries from scheduled time
  - [ ] Check cron execution log: `tail ~/.openclaw/memory/logs/hyrve_cron.log`

---

## Post-Deployment (Monitoring)

- [ ] **Daily Review**
  - [ ] Check for accepted jobs: `grep ACCEPTED ~/.openclaw/memory/logs/hyrve_bid_log.jsonl`
  - [ ] Review log size: `wc -l ~/.openclaw/memory/logs/hyrve_bid_log.jsonl`
  - [ ] Check for errors: `grep ERROR ~/.openclaw/memory/logs/hyrve_bid_log.jsonl`

- [ ] **Weekly Review**
  - [ ] Total jobs processed: `wc -l ~/.openclaw/memory/logs/hyrve_bid_log.jsonl`
  - [ ] Acceptance rate: Calculate from logs
  - [ ] Total revenue: Sum from accepted job amounts
  - [ ] Any filter issues: Review rejected jobs

- [ ] **Monthly Review**
  - [ ] Archive old logs if too large
  - [ ] Review performance metrics
  - [ ] Update filters if needed
  - [ ] Check for API changes

---

## Troubleshooting Guide

| Issue | Solution |
|-------|----------|
| API Key not found | Set using one of three methods (env var, secrets file, .env) |
| 404 Error | Verify API endpoint: `https://api.hyrveai.com/v1/jobs` |
| 401 Error | Check API key is valid, regenerate if needed |
| Cron not running | Check: `crontab -l`, verify API key is in cron environment |
| No jobs accepted | Check filters, review log for rejections, verify budget caps |
| Script errors | Run manually to see full error output |
| Log file missing | Create log dir: `mkdir -p ~/.openclaw/memory/logs` |

---

## Configuration Adjustments

### Change Job Type Filters
Edit `hyrve_monitor_v2.js`, find `allowedTypes`:
```javascript
allowedTypes: ['seo_audit', 'lead_generation', 'email_outreach', 'content_writing']
```

### Change Budget Caps
Edit `hyrve_monitor_v2.js`, find `budgetCaps`:
```javascript
budgetCaps: {
  'seo_audit': { min: 9, max: 59 },
  'lead_generation': { min: 9, max: 25 },
  'email_outreach': { min: 9, max: 29 },
  'content_writing': { min: 5, max: 12 }
}
```

### Change Confidence Threshold
Edit `hyrve_monitor_v2.js`, find `minConfidence`:
```javascript
minConfidence: 95  // Change this number
```

### Change Max Single Mission
Edit `hyrve_monitor_v2.js`, find `maxSingleMission`:
```javascript
maxSingleMission: 100  // Change this number
```

---

## Rollback Plan

If issues occur:

1. **Stop Cron Job**
   ```bash
   crontab -e
   # Delete or comment out the HYRVE monitor line
   ```

2. **Keep Logs**
   ```bash
   cp ~/.openclaw/memory/logs/hyrve_bid_log.jsonl \
      ~/.openclaw/memory/logs/hyrve_bid_log_backup_$(date +%s).jsonl
   ```

3. **Investigate**
   - Review last log entries
   - Run manual test to see errors
   - Check API status

4. **Fix & Redeploy**
   - Make configuration changes
   - Re-test with manual run
   - Restore cron job

---

## Performance Targets

| Metric | Target | Notes |
|--------|--------|-------|
| API Response | <5s | Should be quick |
| Processing Time | <30s | Depends on job count |
| Error Rate | <5% | Monitor for issues |
| Uptime | >99% | Should rarely fail |
| Log Rotation | Monthly | Keep logs manageable |

---

## Documentation References

- **README:** `HYRVE_README.md`
- **Setup Guide:** `HYRVE_SETUP.md`
- **This Checklist:** `DEPLOYMENT_CHECKLIST.md`
- **Script:** `hyrve_monitor_v2.js`
- **Setup Tool:** `setup_hyrve_cron.sh`

---

## Sign-Off

- [ ] **Deployer Name:** _________________
- [ ] **Date:** _________________
- [ ] **Deployment Environment:** Development / Staging / Production
- [ ] **API Key Stored Securely:** ☑️
- [ ] **Cron Job Active:** ☑️
- [ ] **Logs Monitoring Set Up:** ☑️
- [ ] **Team Notified:** ☑️

---

**Next Review Date:** _________________

**Emergency Contact:** 

**Notes:**

---

**Ready to deploy! ✅**

For questions, refer to `HYRVE_README.md` or `HYRVE_SETUP.md`
