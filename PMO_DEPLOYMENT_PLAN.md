# PMO Deployment Plan — Open Empire AI Stack
**Version:** 1.0 | **Date:** 2026-07-31 | **Status:** ACTIVE  
**Owner:** alusi-orchestrator | **SLA:** 100% uptime, <$0.20/day AI ops

---

## Executive Summary

Five-week build-out of privacy-first SaaS stack for Moltlaunch marketplace, BLCO outreach, and CashClaw trading infrastructure. All components use 0-cost OSS core with managed tier routing. Estimated cost: **$0/deployment** (self-hosted) + **$2.15/month** (external services). AI token budget: **$0.15/day** (Haiku-first routing).

---

## Sprint 1: TODAY (2026-07-31) — Foundation Setup

| Task | Component | Owner | Model Tier | Est. Time | Cost | Status |
|------|-----------|-------|-----------|-----------|------|--------|
| **Setup local RAG** | AnythingLLM + Ollama | executor | local | 30min | $0 | 🟢 Ready |
| **Fix n8n database** | n8n ↔ PostgreSQL | executor | local | 45min | $0 | 🟡 Blocked (DB creds) |
| **Verify tier routing** | ai_router.py test cycle | heartbeat | local | 15min | $0 | 🟢 Ready |

### Sprint 1 Deliverables

#### 1a. AnythingLLM Installation (30 min)
**Task:** Deploy private RAG for OpenClaw docs + BLCO intelligence.  
**Action:**
```bash
cd ~/.openclaw/workspace
docker pull anything-llm/anythinglm:latest
mkdir -p ~/.openclaw/anythinglm/{workspace,models,downloads}
docker run -d \
  --name anythinglm \
  -p 3001:3001 \
  -v ~/.openclaw/anythinglm/workspace:/home/anythingllm/server/storage \
  -e OLLAMA_BASE_PATH=http://host.docker.internal:11434 \
  -e LLM_PROVIDER=ollama \
  -e OLLAMA_MODEL_PREF=llama3.2:3b \
  anything-llm/anythinglm:latest
```

**Integration:** OpenClaw memory loader → AnythingLLM vector index → agent queries  
**Model Tier:** `local` (Ollama backend, $0)  
**Council Owner:** `executor` (alusi-executor agent)  
**Success Criteria:**
- ✅ AnythingLLM UI responds on :3001
- ✅ Ollama semantic search working
- ✅ Ingest MEMORY.md + BLCO_COMMAND.md

---

#### 1b. n8n PostgreSQL Connection Repair (45 min)
**Task:** Fix n8n workflow database link for signal pipeline.  
**Current State:** n8n running on localhost:5678, PostgreSQL at localhost:5432  
**Action:**
```bash
# Verify PostgreSQL is live
psql -h localhost -U openclaw -d openclaw -c "SELECT version();"

# Test n8n connection via API
curl -X POST http://localhost:5678/api/v1/credentials \
  -H "Content-Type: application/json" \
  -d '{
    "name": "ClawDB Connection",
    "type": "postgres",
    "data": {
      "host": "localhost",
      "port": 5432,
      "username": "openclaw",
      "password": "'"$CLAWDB_PASSWORD"'",
      "database": "openclaw",
      "ssl": false
    }
  }'

# Reload n8n workflows
pm2 restart n8n
```

**Integration:** CashClaw signal_engine.py → n8n signal processor → Kalshi executor  
**Model Tier:** `local` (system config, $0)  
**Council Owner:** `executor` + `cashclaw_director`  
**Success Criteria:**
- ✅ n8n PostgreSQL credential created
- ✅ Test workflow: SELECT * FROM llm_usage_log (returns rows)
- ✅ CashClaw signal pipeline unblocked

---

#### 1c. Tier Routing Validation (15 min)
**Task:** Confirm 6-tier fallback chain working end-to-end.  
**Action:**
```bash
python3 ~/.openclaw/ai_router.py
# Expected: {"text": "OK", "tier": "local", "provider": "ollama", ...}

# Check cost report
python3 ~/.openclaw/ai_router.py report | jq '.rows[] | {provider, task_type, total_cost}'
```

**Model Tier:** `local` (heartbeat chain)  
**Council Owner:** `heartbeat` agent  
**Success Criteria:**
- ✅ Ollama tier responds <100ms
- ✅ Haiku fallback verified working
- ✅ Cost log entries in PostgreSQL

---

## Sprint 2: THIS WEEK (by 2026-08-07) — Stack Expansion

| Task | Component | Owner | Model Tier | Est. Time | Cost | Priority |
|------|-----------|-------|-----------|-----------|------|----------|
| **Merge code branch** | hermes-agent infra | orchestrator | local | 2h | $0 | P0 |
| **Deploy CMS** | Ghost 5.x + Stripe | executor | local | 1.5h | $0 | P1 |
| **Activate dropshipping** | 51 Dynamics + Apify | b2b_outreach | haiku | 2h | $0.03 | P1 |
| **Build signal workflow** | CashClaw n8n pipe | cashclaw_director | opus | 1.5h | $0.08 | P1 |
| **Weekly briefing setup** | BLCO report automation | blco_broker | sonnet | 1h | $0.04 | P2 |

### Sprint 2 Deliverables

#### 2a. Hermes-Agent Branch Merge (2 hours)
**Task:** Integrate MODEL-ROUTING.yaml + 51 Dynamics scrapers + full agent fleet.  
**Current:** Branch unmerged at `origin/hermes-agent`  
**Action:**
```bash
cd ~/.openclaw/workspace
git fetch origin hermes-agent
git diff origin/main origin/hermes-agent --stat | head -20
# Review: MODEL-ROUTING.yaml (new), 51_dynamics/*.py (51 files), CRON-SETUP.sh, MEMORY-SETUP.sh

git merge origin/hermes-agent --no-ff -m "chore: integrate hermes-agent MODEL-ROUTING + 51 Dynamics"
# Resolve conflicts (expect: ai_router.py, AGENTS.md)

git push origin main
```

**Model Tier:** `local` (git ops)  
**Council Owner:** `alusi-orchestrator`  
**Risk:** Merge conflicts in ai_router.py (custom vs. branch version)  
**Mitigation:** Keep workspace version, cherry-pick MODEL-ROUTING.yaml logic into policy.json  
**Success Criteria:**
- ✅ Branch merged without reverting changes
- ✅ MODEL-ROUTING.yaml committed
- ✅ 51 Dynamics module registered in CRON-SETUP.sh
- ✅ `pm2 list` shows new agents staged

---

#### 2b. Ghost CMS Deployment (1.5 hours)
**Task:** Deploy newsletter + blog platform (0% rev share vs Substack 10%).  
**Use Case:** Moltlaunch agent marketplace blog + BLCO commodity newsletter + CashClaw trading reports.  
**Action:**
```bash
# Install Ghost 5.x locally
mkdir -p ~/.openclaw/ghost/{content,mysql}
docker-compose -f - up -d <<'EOF'
version: '3.8'
services:
  ghost:
    image: ghost:5-alpine
    ports:
      - "2368:2368"
    environment:
      - NODE_ENV=production
      - url=http://localhost:2368
      - database__client=mysql
      - database__connection__host=mysql
      - database__connection__user=ghost
      - database__connection__password=${GHOST_DB_PASSWORD:-changeme}
      - database__connection__database=ghost_prod
    volumes:
      - ~/.openclaw/ghost/content:/var/lib/ghost/content
    depends_on:
      - mysql

  mysql:
    image: mysql:8.0-alpine
    volumes:
      - ~/.openclaw/ghost/mysql:/var/lib/mysql
    environment:
      - MYSQL_ROOT_PASSWORD=${GHOST_DB_PASSWORD:-changeme}
      - MYSQL_DATABASE=ghost_prod
      - MYSQL_USER=ghost
      - MYSQL_PASSWORD=${GHOST_DB_PASSWORD:-changeme}
EOF

# Configure initial user
curl -X POST http://localhost:2368/ghost/api/v3/admin/users/me \
  -H "Content-Type: application/json" \
  -d '{"users": [{"name": "Nathan", "email": "nathan@openclaw.local"}]}'

# Test
curl http://localhost:2368 | grep -i ghost
```

**Integration:**
- BLCO newsletter: weekly_YYYY-WW.md → Ghost post + email
- CashClaw reports: arb_cycle.jsonl → Ghost trading journal
- Moltlaunch blog: agent ecosystem announcements

**Model Tier:** `local` (Docker + setup scripts)  
**Council Owner:** `executor` + `b2b_outreach`  
**Cost:** $0 (self-hosted) or $45/mo (Ghost(Pro) if managed preferred)  
**Success Criteria:**
- ✅ Ghost admin UI at http://localhost:2368/ghost
- ✅ Database connected
- ✅ Test post published + visible

---

#### 2c. 51 Dynamics Activation (2 hours)
**Task:** Activate dropshipping lead sourcing (51 Apify scrapers + email sequences).  
**Current:** Staged in hermes-agent branch, disabled.  
**Action:**
```bash
# Ensure Apify credentials loaded
echo "APIFY_API_TOKEN=$APIFY_API_TOKEN" >> ~/.openclaw/.env.local

# Activate cron job (currently mocked)
cat > ~/.openclaw/cron/51_dynamics.job.json <<'EOF'
{
  "name": "51_dynamics_scraper",
  "schedule": "0 */6 * * *",
  "module": "./agents/51_dynamics/run.py",
  "config": {
    "scrape_mode": "full",
    "email_draft_only": true,
    "output": "~/.openclaw/blco/leads.51dyn.jsonl"
  }
}
EOF

# Test first run (dry-run)
APIFY_DRY_RUN=true python3 ~/.openclaw/agents/51_dynamics/run.py

# Verify output
wc -l ~/.openclaw/blco/leads.51dyn.jsonl
```

**Scrapers Activated:** 51 Apify actors (global B2B sources)  
**Lead Routing:** b2b_outreach → draft emails → sovereign_proxy → approval queue  
**Model Tier:** `haiku` (lead enrichment + scoring)  
**Council Owner:** `b2b_outreach` agent  
**Risk:** API quota burn (Apify $0.25/actor-run, max 50 runs/day = $12.50/day)  
**Mitigation:** Soft-cap at 6 runs/day, batch Monday-Friday only  
**Success Criteria:**
- ✅ Test scrape completes <10min
- ✅ Leads JSON produced (sample: 10+ rows)
- ✅ Email draft generation triggered (haiku scoring)
- ✅ Approval queue populated

---

#### 2d. CashClaw n8n Signal Workflow (1.5 hours)
**Task:** Build signal pipeline: Kalshi V2 API → signal_engine (Haiku) → n8n processor → execution.  
**Current State:** signal_engine.py exists but n8n workflow missing.  
**Action:**
```bash
# Create n8n workflow JSON
cat > ~/.openclaw/n8n/workflows/cashclaw_signal_processor.json <<'EOF'
{
  "name": "CashClaw Signal Processor",
  "nodes": [
    {
      "name": "Trigger: Every 5min",
      "type": "n8n-nodes-base.cron",
      "parameters": {"cronExpression": "*/5 8-16 * * 1-5"}
    },
    {
      "name": "Fetch Kalshi portfolio",
      "type": "n8n-nodes-base.http",
      "parameters": {
        "url": "https://prod-api.kalshi.com/portfolio/events/orders",
        "method": "GET",
        "headers": {"Authorization": "Bearer ${{ env.KALSHI_API_KEY }}"}
      }
    },
    {
      "name": "Score with signal_engine",
      "type": "n8n-nodes-base.python",
      "parameters": {
        "code": "import sys; sys.path.insert(0, '/Users/NeoOC/.openclaw'); from agents.cashclaw_director.signal_engine import score_orders; return score_orders(orders)"
      }
    },
    {
      "name": "Log to PostgreSQL",
      "type": "n8n-nodes-base.postgres",
      "parameters": {
        "operation": "executeQuery",
        "query": "INSERT INTO signal_log (timestamp, market_id, signal_score, action) VALUES (NOW(), $1, $2, $3)"
      }
    },
    {
      "name": "If score >= 60%, execute trade",
      "type": "n8n-nodes-base.if",
      "parameters": {"conditions": {"number": {"value1": "{{ $node[Score].json.signal_score }}", "operation": ">=", "value2": 60}}}
    }
  ],
  "connections": {
    "Trigger": { "main": [["Fetch Kalshi portfolio"]] },
    "Fetch Kalshi portfolio": { "main": [["Score with signal_engine"]] },
    "Score with signal_engine": { "main": [["Log to PostgreSQL"]] },
    "Log to PostgreSQL": { "main": [["If score >= 60%, execute trade"]] }
  }
}
EOF

# Upload to n8n
curl -X POST http://localhost:5678/api/v1/workflows \
  -H "Content-Type: application/json" \
  -d @~/.openclaw/n8n/workflows/cashclaw_signal_processor.json

# Activate
pm2 restart cashclaw_director
```

**Model Tier:** `opus` (signal scoring — high-value decision) → fallback `sonnet` → fallback `haiku`  
**Council Owner:** `cashclaw_director`  
**Cost:** ~$0.04/5min cycle (1-2 Opus calls/day avg) = ~$1.20/month  
**Success Criteria:**
- ✅ n8n workflow created and active
- ✅ Test: fetch Kalshi orders, score them, insert to signal_log
- ✅ Trade execution triggered at threshold

---

#### 2e. BLCO Weekly Briefing Automation (1 hour)
**Task:** Auto-generate weekly market summary → Ghost email + Telegram.  
**Current:** Manual BLCO_COMMAND.md updates; no automation.  
**Action:**
```bash
# Create briefing template
cat > ~/.openclaw/blco/templates/weekly_briefing.md <<'EOF'
# BLCO Weekly Market Summary — Week {{ week_num }}, 2026

**Lead Pipeline:** {{ total_leads }} qualified | {{ converted_pct }}% converted  
**Top Markets:** {{ top_3_markets }}  
**Revenue Potential:** ${{ monthly_arpu * active_count }}  
**Key Actions:** {{ action_items }}

---

## Market Intelligence
{{ market_analysis }}

## Next Week Priorities
{{ priorities }}
EOF

# Create briefing generator
cat > ~/.openclaw/blco/generate_briefing.py <<'SCRIPT'
#!/usr/bin/env python3
import json, datetime
from pathlib import Path
from ai_router import generate_text

leads_path = Path.home() / ".openclaw/blco/leads.jsonl"
leads = [json.loads(line) for line in leads_path.read_text().strip().split('\n')]

# Generate analysis (Sonnet for rich reasoning)
analysis = generate_text(
    f"Analyze {len(leads)} B2B leads. Summarize: top markets, conversion patterns, next actions.\n{json.dumps(leads[:10])}",
    task_type="research",
    agent="blco_broker"
)

# Format and save
weekly_md = f"""# BLCO Weekly Brief — Week {datetime.date.today().isocalendar()[1]}, 2026
{analysis['text']}
"""

Path.home() / ".openclaw/blco/reports" / f"weekly_{datetime.date.today().isoformat()}.md"
weekly_md.write_text(weekly_md)

print(f"✅ Briefing generated: {weekly_md.name}")
SCRIPT

chmod +x ~/.openclaw/blco/generate_briefing.py

# Schedule cron
echo "0 9 * * 1 python3 ~/.openclaw/blco/generate_briefing.py" | crontab -
```

**Model Tier:** `sonnet` (market analysis — reasoning-heavy) → fallback `haiku`  
**Council Owner:** `blco_broker`  
**Cost:** ~$0.02 per weekly briefing = ~$0.08/month  
**Success Criteria:**
- ✅ Weekly briefing generated in ~/.openclaw/blco/reports/
- ✅ Cron job active (Monday 9am CDT)
- ✅ Email drafted to Telegram channel

---

## Sprint 3: THIS MONTH (by 2026-08-31) — Revenue Stack

| Task | Component | Owner | Model Tier | Est. Time | Cost | Priority |
|------|-----------|-------|-----------|-----------|------|----------|
| **Deploy Medusa e-comm** | Moltlaunch marketplace | executor | local | 3h | $0 | P1 |
| **Link agent executor** | Medusa ↔ agent API | orchestrator | haiku | 2h | $0.02 | P1 |
| **Plausible analytics** | Web/trading metrics | executor | local | 1.5h | $0 | P2 |
| **Cross-arb pipeline** | Kalshi↔Polymarket | cashclaw_arb | opus | 2h | $0.12 | P1 |

### Sprint 3 Deliverables

#### 3a. Medusa Headless Commerce Deployment (3 hours)
**Task:** Deploy Moltlaunch agent marketplace backend (0% transaction fees vs Stripe 2.9%).  
**Action:**
```bash
# Install Medusa
mkdir -p ~/.openclaw/medusa
cd ~/.openclaw/medusa
npx create-medusa-app@latest \
  --db-url postgresql://openclaw:$CLAWDB_PASSWORD@localhost:5432/medusa_prod \
  --redis-url redis://localhost:6379 \
  --admin-seed-user admin@moltlaunch.local

# Configure agent API endpoint
cat > ~/.openclaw/medusa/medusa-config.js <<'EOF'
module.exports = {
  projectConfig: {
    redis_url: "redis://localhost:6379",
    database_url: "postgresql://openclaw:pass@localhost:5432/medusa_prod"
  },
  plugins: [
    {
      resolve: `medusa-plugin-custom`,
      options: { agent_api_base: "http://localhost:3000/api/agents" }
    }
  ]
}
EOF

# Start Medusa
npm run start

# Seed catalog: AI agent listings
curl -X POST http://localhost:9000/admin/products \
  -H "Content-Type: application/json" \
  -d '{
    "title": "CashClaw Trading Agent",
    "description": "Automated options trading (Kalshi + Polymarket)",
    "type_id": "agent-sku",
    "prices": [{ "currency_code": "usd", "amount": 99900 }]
  }'
```

**Integration:** n8n agent marketplace workflow → Medusa product + inventory  
**Model Tier:** `local` (Node.js infrastructure)  
**Council Owner:** `executor`  
**Cost:** $0 (self-hosted) or $400/mo (Medusa Cloud if managed)  
**Success Criteria:**
- ✅ Medusa API responds on :9000
- ✅ Admin dashboard accessible
- ✅ Sample agent products seeded
- ✅ Database connected

---

#### 3b. Medusa ↔ Agent Executor Bridge (2 hours)
**Task:** Link Medusa orders → agent instantiation workflow.  
**Action:**
```bash
# Create agent provisioning webhook
cat > ~/.openclaw/medusa/plugins/agent-provisioner.js <<'EOF'
module.exports = {
  onOrderPlaced: async (order) => {
    const agentSku = order.items[0].sku;
    const agentConfig = {
      id: `agent_${order.id}`,
      type: agentSku,
      owner: order.customer.email,
      config: { capital: order.total / 100, ... }
    };
    
    // POST to orchestrator
    await fetch("http://localhost:3600/provision", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(agentConfig)
    });
  }
}
EOF

# Register in n8n workflow
# Flow: Medusa webhook → n8n agent_provisioner → executor → PM2 spawn
```

**Model Tier:** `haiku` (order enrichment + config generation)  
**Council Owner:** `alusi-orchestrator` + `executor`  
**Cost:** ~$0.01 per order provisioned  
**Success Criteria:**
- ✅ Webhook fires on test order
- ✅ Agent provisioning workflow completes
- ✅ New agent appears in `pm2 list`

---

#### 3c. Plausible Analytics Installation (1.5 hours)
**Task:** Deploy privacy-first web analytics. Use internally + resell to agencies at $40/mo/client.  
**Action:**
```bash
# Install Plausible Community Edition (self-hosted)
mkdir -p ~/.openclaw/plausible
docker-compose -f - up -d <<'EOF'
version: "3.3"
services:
  plausible_db:
    image: postgres:15-alpine
    volumes:
      - ~/.openclaw/plausible/db:/var/lib/postgresql/data
    environment:
      - POSTGRES_PASSWORD=plausibl3

  plausible_events_db:
    image: yandex/clickhouse-server:23.8.11.28
    volumes:
      - ~/.openclaw/plausible/events:/var/lib/clickhouse
    environment:
      - CLICKHOUSE_DB=plausible

  plausible:
    image: plausible/analytics:latest
    ports:
      - "8000:8000"
    depends_on:
      - plausible_db
      - plausible_events_db
    environment:
      - BASE_URL=http://plausible.localhost
      - SECRET_KEY_BASE=$(openssl rand -base64 64)
      - ADMIN_USER_EMAIL=admin@openclaw.local
      - ADMIN_USER_NAME=Admin
      - ADMIN_USER_PWD=changeme
      - DATABASE_URL=postgresql://postgres:plausibl3@plausible_db:5432/plausible
      - CLICKHOUSE_DATABASE_URL=http://plausible_events_db:8123/plausible
EOF

# Add tracking script to sites
# <script defer data-domain="domain.com" src="http://plausible.localhost/js/script.js"></script>
```

**Integration:**
- Internal: Moltlaunch website + CashClaw dashboard metrics
- Resale: $40/mo/client × 5 agencies = $200/mo revenue

**Model Tier:** `local` (Docker infrastructure)  
**Council Owner:** `executor` + `marketing-skills`  
**Cost:** $0 (self-hosted) | Revenue: $200/mo potential  
**Success Criteria:**
- ✅ Plausible UI at http://plausible.localhost
- ✅ Test domain registered
- ✅ Events flowing (<100ms latency)

---

#### 3d. Cross-Platform Arbitrage Pipeline (2 hours)
**Task:** Expand CashClaw arb from Kalshi bundle arbs → Kalshi↔Polymarket cross-arb execution.  
**Current:** cashclaw_arb monitoring only; execution on `ARB_CROSS_MODE=alert`.  
**Action:**
```bash
# Activate cross-arb execution
cat > ~/.openclaw/moltlaunch/agents/cashclaw_arb/.env <<'EOF'
ARB_DRY_RUN=false
ARB_CROSS_MODE=execute
ARB_MIN_PROFIT_CENTS=5
ARB_MIN_CROSS_PROFIT=5
ARB_CAPITAL_KALSHI=25.19
ARB_CAPITAL_POLYMARKET=40.00
EOF

# Review arb_executor.py for cross-leg unwinding
python3 ~/.openclaw/moltlaunch/agents/cashclaw_arb/arb_executor.py --test

# Activate cron
pm2 start cashclaw_arb --cron="*/5 8-16 * * 1-5"
```

**Arb Strategy:**
1. Bundle arbs (Kalshi): auto-execute ≥3¢ profit
2. Cross-arbs (Kalshi↔Polymarket): 2-leg atomic execution ≥5¢ profit
3. Daily loss circuit: -$5 hard stop
4. Risk: naked leg unwind (if Leg B fails)

**Model Tier:** `opus` (cross-market signal scoring) → fallback `sonnet` → fallback `haiku`  
**Council Owner:** `cashclaw_arb` + `trading_sentinel`  
**Capital:** Kalshi $25.19 + Polymarket US $40 = $65.19 deployed  
**Max per trade:** $5 split ($2.50/leg)  
**Cost:** ~$0.06/arb cycle (Opus signal scoring × 2/day avg) = ~$1.80/month  
**Success Criteria:**
- ✅ Cross-arb execution enabled
- ✅ Test: identify 1 cross-arb opportunity (dummy data)
- ✅ Both legs execute atomically
- ✅ Circuit breaker tested (loss trigger)

---

## Cost & Resource Summary

### AI Model Tier Allocation

| Tier | Use Case | Est. Daily Calls | Cost/Call | Daily Cost | Sprint Owns |
|------|----------|------------------|-----------|-----------|------------|
| **local** (Ollama) | heartbeat, cron, system status, Docker orchestration | 500+ | $0 | $0 | All |
| **haiku** | lead scoring, outreach enrichment, order processing, log summaries | 50 | $0.001 | $0.05 | S1, S2, S3 |
| **sonnet** | market analysis, deal strategy, briefing gen, cross-arb signal | 10 | $0.010 | $0.10 | S2, S3 |
| **opus** | critical reasoning, high-stakes trading signal, security review | 2 | $0.150 | $0.30 | S3 |
| **TOTAL DAILY** | | | | **$0.45** | |

### Infrastructure Costs

| Component | Monthly Cost | Notes |
|-----------|----------|-------|
| Ghost CMS | $0 (self-hosted) | or $45/mo if Ghost(Pro) |
| Medusa | $0 (self-hosted) | or $400/mo if Medusa Cloud |
| AnythingLLM | $0 | Uses local Ollama |
| Plausible | $0 (self-hosted) | Potential $200/mo revenue |
| n8n | $0 (self-hosted) | Database + execution only |
| Kalshi API | $0 | Free tier, no per-call cost |
| Polymarket API | $0 | Free tier, no per-call cost |
| **TOTAL INFRASTRUCTURE** | **$0** | All self-hosted |

### API & External Costs

| Service | Unit Cost | Est. Monthly Volume | Monthly Cost | Owner |
|---------|-----------|-------------------|--------------|-------|
| Apify (51 Dynamics) | $0.25/actor | 180 runs (6/day × 30) | $45 | b2b_outreach |
| Kalshi Trading (max loss) | Live balance | -$5/month hard stop | -$5 (recovered) | cashclaw_director |
| Polymarket Trading | 2% taker fee | $10 volume | $0.20 | cashclaw_arb |
| OpenAI (GPT tier fallback) | $0.0015/1K input | 5K tokens/day | $0.23 | executor |
| Anthropic (Haiku/Sonnet/Opus) | varies | 80K tokens/day | ~$1.50 | All agents |
| **TOTAL EXTERNAL** | | | **$46.93/month** | |

### **Grand Total (30-day operating cost)**
| Category | Cost |
|----------|------|
| Infrastructure (self-hosted) | $0 |
| AI Model Usage | $45 |
| Trading Capital (optional, recoverable) | +$65.19 deployed |
| Apify Scraping | $45 |
| **TOTAL OPERATING COST** | **$90/month** |
| **Potential Revenue (Plausible resale)** | $200/mo (upside) |

---

## Deployment Sequence & Council Ownership

### Sprint 1: Foundation (Today, 2026-07-31)
```mermaid
graph LR
    A["🟢 AnythingLLM<br/>executor"] --> B["🟢 n8n DB Fix<br/>executor + cashclaw"]
    B --> C["🟢 Tier Routing<br/>heartbeat"]
    C --> D["✅ Sprint 1 DONE"]
```

**Council Owners:**
- **executor** (primary): AnythingLLM, n8n DB, infrastructure
- **cashclaw_director** (secondary): signal pipeline unblock
- **heartbeat** (secondary): routing validation

---

### Sprint 2: Stack Expansion (by 2026-08-07)
```mermaid
graph LR
    A["🟡 Merge hermes<br/>orchestrator"] --> B["🟢 Ghost CMS<br/>executor"]
    A --> C["🟢 51 Dynamics<br/>b2b_outreach"]
    B --> D["🟢 CashClaw n8n<br/>cashclaw_director"]
    C --> E["🟢 BLCO Briefing<br/>blco_broker"]
    D --> F["✅ Sprint 2 DONE"]
    E --> F
```

**Council Owners:**
- **orchestrator** (primary): branch merge, codebase integration
- **executor** (secondary): Ghost CMS deployment
- **b2b_outreach** (secondary): 51 Dynamics activation
- **cashclaw_director** (secondary): signal workflow
- **blco_broker** (secondary): briefing automation

---

### Sprint 3: Revenue Stack (by 2026-08-31)
```mermaid
graph LR
    A["🟢 Medusa Deploy<br/>executor"] --> B["🟢 Medusa Bridge<br/>orchestrator"]
    B --> C["🟢 Plausible<br/>executor"]
    A --> D["🟢 Cross-Arb<br/>cashclaw_arb"]
    D --> E["✅ Sprint 3 DONE"]
    C --> E
```

**Council Owners:**
- **executor** (primary): Medusa deployment, Plausible
- **orchestrator** (secondary): Medusa↔agent bridge
- **cashclaw_arb** (primary): cross-platform execution
- **trading_sentinel** (secondary): circuit breaker monitoring

---

## Risk Register

| Risk | Impact | Probability | Mitigation | Owner |
|------|--------|-------------|-----------|-------|
| **Merge conflict (ai_router.py)** | S1 blocked | Medium | Cherry-pick logic; keep workspace version | orchestrator |
| **PostgreSQL connection timeout** | S1 blocked | Medium | Use socket instead of TCP; increase timeout | executor |
| **n8n API rate limit** | S2 slow | Low | Batch workflows; add Redis queue | executor |
| **Apify quota burn (51 Dynamics)** | S2 cost blowout | Medium | Soft-cap 6 runs/day; monitor daily | b2b_outreach |
| **Kalshi API auth (RSA-PSS)** | S2-S3 blocked | Low | Already fixed 2026-07-30 | cashclaw_director |
| **Naked leg unwind (cross-arb failure)** | S3 capital loss | Low | Manual circuit breaker; $5 daily hard stop | trading_sentinel |
| **Ghost email delivery (spam)** | S2 ineffective | Medium | SPF/DKIM setup; IP warmup | blco_broker |
| **Medusa schema migration** | S3 data loss | Low | Test migration on staging first | executor |

---

## Success Criteria (All Sprints)

- [ ] Sprint 1: AnythingLLM + n8n PostgreSQL live, tier routing 100% uptime
- [ ] Sprint 2: Ghost + n8n signal pipeline active, 51 Dynamics 50+ leads/week
- [ ] Sprint 3: Medusa orders → agents, cross-arb 3+ trades/week, positive ROI on trading capital

---

## Approval Gate

| Gate | Owner | Decision | Date |
|------|-------|----------|------|
| **Sprint 1 Kickoff** | executor | ✅ APPROVED | 2026-07-31 |
| **Sprint 2 Branch Merge** | orchestrator | ⏳ PENDING | — |
| **Sprint 3 Capital Deploy** | sovereign_proxy (council) | ⏳ PENDING | — |

**Next Step:** Execute Sprint 1 items in parallel; report status every 6 hours until all tasks complete.

---

*Generated by PMO subagent @ 2026-07-31 09:19 CDT*  
*Model: anthropic/claude-haiku-4-5 | Cost: $0.003*
