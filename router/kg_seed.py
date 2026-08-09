#!/usr/bin/env python3
"""
Open Empire Knowledge Graph Seed — P0.5
Seeds ClawDB kg_entities + kg_relationships from authoritative sources:
 - PM2 process list (live)
 - AGENTS.md (agent registry)
 - MEMORY.md (validated runtime state)
 - Free-Way catalog (providers + models)
 - Trading agents (hardcoded protected)
Version: 1.0 | 2026-08-09
"""
import subprocess, json, re, datetime, urllib.request, os, sys

# ── DB connection via psql ────────────────────────────────────────────
DB = "postgresql://NeoOC@127.0.0.1:5432/clawdb"

def sql(query, params=None):
    """Execute SQL via psql, return stdout."""
    if params:
        for k, v in params.items():
            v_escaped = str(v).replace("'", "''")
            query = query.replace(f":{k}", f"'{v_escaped}'")
    result = subprocess.run(
        ["psql", "-h", "127.0.0.1", "-p", "5432", "-U", "NeoOC", "-d", "clawdb",
         "-t", "-A", "-c", query],
        capture_output=True, text=True, timeout=15
    )
    if result.returncode != 0:
        print(f"SQL ERROR: {result.stderr[:200]}", file=sys.stderr)
        return None
    return result.stdout.strip()

def upsert_entity(canonical_name, entity_type, description="", metadata=None,
                  source_system="alusi-seed", source_record_id=None,
                  owner="Nathan", status="active", evidence_status="VERIFIED"):
    """Insert entity if not exists; return id."""
    meta_json = json.dumps(metadata or {}).replace("'", "''")
    desc = description.replace("'", "''")
    src_id = (source_record_id or "").replace("'", "''")

    # Check existing
    existing = sql(f"SELECT id FROM kg_entities WHERE canonical_name='{canonical_name}' AND entity_type='{entity_type}' LIMIT 1;")
    if existing:
        eid = existing.strip()
        # Update last_seen
        sql(f"UPDATE kg_entities SET last_seen_at=NOW(), updated_at=NOW() WHERE id={eid};")
        return int(eid)

    result = sql(f"""
INSERT INTO kg_entities (canonical_name, entity_type, description, metadata,
    source_system, source_record_id, owner, status, evidence_status)
VALUES ('{canonical_name}','{entity_type}','{desc}','{meta_json}'::jsonb,
    '{source_system}','{src_id}','{owner}','{status}','{evidence_status}')
RETURNING id;
""")
    if result:
        # result may contain extra lines; grab the first integer line
        eid = int([l for l in result.strip().splitlines() if l.strip().isdigit()][0])
        # Log event
        sql(f"INSERT INTO kg_graph_events (event_type,actor,entity_id,details) VALUES ('entity_created','alusi-seed',{eid},'{{\"name\":\"{canonical_name}\",\"type\":\"{entity_type}\"}}');")
        return eid
    return None

def upsert_relationship(source_id, target_id, rel_type, dep_class="hard",
                        strength=1.0, source_system="alusi-seed", metadata=None):
    """Insert relationship if not exists."""
    if not source_id or not target_id:
        return None
    meta_json = json.dumps(metadata or {}).replace("'", "''")
    existing = sql(f"SELECT id FROM kg_relationships WHERE source_entity_id={source_id} AND target_entity_id={target_id} AND relationship_type='{rel_type}' LIMIT 1;")
    if existing:
        return int(existing.strip())
    result = sql(f"""
INSERT INTO kg_relationships (source_entity_id,target_entity_id,relationship_type,
    dependency_class,strength,source_system,metadata)
VALUES ({source_id},{target_id},'{rel_type}','{dep_class}',{strength},'{source_system}','{meta_json}'::jsonb)
RETURNING id;
""")
    if result:
        rid_lines = [l for l in result.strip().splitlines() if l.strip().isdigit()]
        if not rid_lines: return None
        rid = int(rid_lines[0])
        sql(f"INSERT INTO kg_graph_events (event_type,actor,rel_id,details) VALUES ('relationship_created','alusi-seed',{rid},'{{\"type\":\"{rel_type}\",\"src\":{source_id},\"tgt\":{target_id}}}');")
        return rid
    return None

# ── Seed: Core Ventures ───────────────────────────────────────────────
def seed_ventures():
    ventures = [
        ("CashClaw",       "Autonomous Kalshi + Polymarket trading system",  {"capital_deployed_usd": 65.19}),
        ("BLCO Pipeline",  "BLCO buyer qualification and outreach system",   {"leads": 192}),
        ("ADAI Solutions", "Monetizable AI products parent brand",           {"products": ["CashClaw Ops", "Enterprise Agent Factory", "AI Research Automation", "Code Migration"]}),
        ("Moltlaunch",     "HyrveAI marketplace venture",                    {"status": "live"}),
        ("Open Empire",    "Sovereign AI-native execution ecosystem",        {"version": "V1"}),
    ]
    ids = {}
    for name, desc, meta in ventures:
        eid = upsert_entity(name, "VENTURE", desc, meta, owner="Nathan")
        ids[name] = eid
        print(f"  VENTURE: {name} → id={eid}")
    return ids

# ── Seed: Portfolios / Programs ───────────────────────────────────────
def seed_portfolios():
    portfolios = [
        ("Sovereign Income", "Autonomous revenue generation portfolio", {}),
        ("Infrastructure",   "Open Empire runtime infrastructure",      {}),
        ("Intelligence",     "AI cost, memory, routing optimization",   {}),
    ]
    ids = {}
    for name, desc, meta in portfolios:
        eid = upsert_entity(name, "PORTFOLIO", desc, meta)
        ids[name] = eid
        print(f"  PORTFOLIO: {name} → id={eid}")
    return ids

# ── Seed: Providers + Models ──────────────────────────────────────────
def seed_providers():
    providers = [
        ("Anthropic",   "Primary LLM provider — Haiku/Sonnet/Opus", {"tier": "premium", "port": None}),
        ("OpenRouter",  "Free-tier multi-model gateway (17 models)", {"tier": "free",    "models": 17}),
        ("Cohere",      "Free-tier command-r models",               {"tier": "free",    "models": 4}),
        ("Cerebras",    "Free-tier fast inference",                  {"tier": "free",    "models": 2}),
        ("NVIDIA NIM",  "Free-tier Nemotron models",                {"tier": "free",    "models": 2}),
        ("Mistral",     "Low-cost mistral-medium-3",                {"tier": "low_cost","models": 1}),
        ("Ollama",      "Local inference — 6 models",               {"tier": "local",   "port": 11434, "models": 6}),
    ]
    ids = {}
    for name, desc, meta in providers:
        eid = upsert_entity(name, "PROVIDER", desc, meta, source_system="freeway-catalog")
        ids[name] = eid
        print(f"  PROVIDER: {name} → id={eid}")

    # Key models
    models = [
        ("claude-haiku-4-5",        "Anthropic",  "Signal scoring, Haiku-tier",        {"cost_per_1m_input": 0.80}),
        ("claude-sonnet-4-6",       "Anthropic",  "Strategy, complex synthesis",        {"cost_per_1m_input": 3.00}),
        ("command-r7b",             "Cohere",     "Free primary — chat/classify",       {"cost": 0.00}),
        ("north-mini-code",         "OpenRouter", "Free primary — code generation",     {"cost": 0.00}),
        ("nemotron-3-nano-30b-a3b", "OpenRouter", "Free — summarization",              {"cost": 0.00}),
        ("qwen2.5:3b",              "Ollama",     "Local — batch/overnight tasks",      {"cost": 0.00}),
        ("tinyllama",               "Ollama",     "Local — heartbeat/monitoring",       {"cost": 0.00}),
    ]
    model_ids = {}
    for mname, provider_name, desc, meta in models:
        mid = upsert_entity(mname, "MODEL", desc, meta, source_system="fcc-validated")
        model_ids[mname] = mid
        if provider_name in ids:
            upsert_relationship(ids[provider_name], mid, "PROVIDES", "hard", 1.0)
        print(f"  MODEL: {mname} → id={mid}")

    return ids, model_ids

# ── Seed: Routers ─────────────────────────────────────────────────────
def seed_routers():
    routers = [
        ("Free-Way",      "Free-tier multi-provider gateway, port 8082, PM2 id=48", {"pm2_id": 48, "port": 8082, "status": "running"}),
        ("native-router", "Open Empire governed premium router, port 6251, PM2 id=26", {"pm2_id": 26, "port": 6251, "status": "running"}),
        ("fcc_router",    "Governed task dispatch layer — wraps Free-Way", {"path": "workspace/router/fcc_router.py"}),
        ("claude-proxy",  "Unknown proxy, port 4099, PM2 id=28", {"pm2_id": 28, "port": 4099, "status": "audit_pending"}),
    ]
    ids = {}
    for name, desc, meta in routers:
        eid = upsert_entity(name, "ROUTER", desc, meta, source_system="pm2-topology")
        ids[name] = eid
        print(f"  ROUTER: {name} → id={eid}")
    return ids

# ── Seed: Agents from AGENTS.md ───────────────────────────────────────
def seed_agents():
    agents_data = [
        ("executor",                  0,  "Core task executor",                          "AGENT"),
        ("heartbeat",                 1,  "Alusi-loop heartbeat",                        "AGENT"),
        ("alusi-gateway",             2,  "OpenClaw gateway, port 8787",                 "AGENT"),
        ("alusi-telegram-adapter",    3,  "Telegram channel adapter",                    "AGENT"),
        ("alusi-discord-adapter",     4,  "Discord channel adapter",                     "AGENT"),
        ("alusi-controlled-worker",   5,  "Approval worker",                             "AGENT"),
        ("alusi-orchestrator",        6,  "Multi-agent orchestration",                   "AGENT"),
        ("cashclaw_director",         38, "LIVE — Kalshi trading director",              "AGENT"),
        ("cashclaw_arb",              39, "LIVE — Bundle + cross-arb executor",          "AGENT"),
        ("polymarket-trader",         40, "LIVE — Polymarket MLB/MLS sports trader",     "AGENT"),
        ("trading_sentinel",          41, "LIVE — CashClaw watchdog",                    "AGENT"),
        ("ollama",                    24, "Local LLM server, port 11434, 6 models",      "RUNTIME"),
        ("freeway",                   48, "Free-Way proxy, port 8082, 5 providers",      "ROUTER"),
        ("grafana",                   50, "FCC Cost Dashboard, port 3001",               "DASHBOARD"),
        ("fcc-metrics-exporter",      51, "FCC metrics scraper every 5min",              "SERVICE"),
        ("mission-control",           17, "Command Center UI, port 3333",                "DASHBOARD"),
        ("clawdb",                    36, "PostgreSQL 18.3, port 5432",                  "RUNTIME"),
        ("n8n",                       45, "Workflow automation, port 5678",              "SERVICE"),
    ]
    ids = {}
    for name, pm2_id, desc, etype in agents_data:
        meta = {"pm2_id": pm2_id, "source": "AGENTS.md"}
        protected = pm2_id in [38, 39, 40, 41]
        if protected:
            meta["protected"] = True
            meta["governance"] = "CASHCLAW_PROTECTED"
        eid = upsert_entity(name, etype, desc, meta, source_system="pm2-topology",
                            source_record_id=str(pm2_id))
        ids[name] = eid
        print(f"  {etype}: {name}(pm2={pm2_id}) → id={eid}")
    return ids

# ── Seed: Capabilities ────────────────────────────────────────────────
def seed_capabilities():
    caps = [
        ("COST_OPTIMIZED_INFERENCE", "Free/low-cost LLM routing via Free-Way"),
        ("GOVERNED_ROUTING",         "Approval-gated model dispatch via native-router"),
        ("LOCAL_INFERENCE",          "Zero-cost Ollama inference"),
        ("COST_TELEMETRY",           "FCC usage tracking and dashboard"),
        ("AUTONOMOUS_TRADING",       "Live Kalshi + Polymarket trading"),
        ("MEMORY_PIPELINE",          "Active→compressed→archive memory management"),
        ("KNOWLEDGE_GRAPH",          "ClawDB entity+relationship store (P0)"),
        ("TASK_DISPATCH",            "fcc_router.py task-type→model routing"),
    ]
    ids = {}
    for name, desc in caps:
        eid = upsert_entity(name, "CAPABILITY", desc, {}, source_system="capability-registry")
        ids[name] = eid
        print(f"  CAPABILITY: {name} → id={eid}")
    return ids

# ── Seed: Repositories ────────────────────────────────────────────────
def seed_repositories():
    repos = [
        ("alusi-core",            "https://github.com/UA4200/alusi-core",          "Core Alusi agent"),
        ("open-empire-core",      "https://github.com/UA4200/open-empire-core",    "Empire foundation"),
        ("Free-Way",              "https://github.com/GoDiao/Free-Way",            "FCC proxy"),
        ("trading",               "~/.openclaw/trading/ (local)",                  "Canonical trading codebase"),
        ("antfarm",               "https://github.com/UA4200/antfarm",             "Workflow automation"),
        ("blco-pipeline",         "https://github.com/UA4200/blco-pipeline",       "BLCO lead pipeline"),
    ]
    ids = {}
    for name, remote, desc in repos:
        eid = upsert_entity(name, "REPOSITORY", desc, {"remote": remote}, source_system="repo-registry")
        ids[name] = eid
        print(f"  REPO: {name} → id={eid}")
    return ids

# ── Main Seed Runner ──────────────────────────────────────────────────
def main():
    print("\n=== OPEN EMPIRE KG SEED — P0.5 ===")
    print(f"Started: {datetime.datetime.utcnow().isoformat()}Z\n")

    print("→ Seeding ventures...")
    venture_ids = seed_ventures()

    print("\n→ Seeding portfolios...")
    portfolio_ids = seed_portfolios()

    print("\n→ Seeding providers + models...")
    provider_ids, model_ids = seed_providers()

    print("\n→ Seeding routers...")
    router_ids = seed_routers()

    print("\n→ Seeding agents...")
    agent_ids = seed_agents()

    print("\n→ Seeding capabilities...")
    cap_ids = seed_capabilities()

    print("\n→ Seeding repositories...")
    repo_ids = seed_repositories()

    print("\n→ Building relationships...")

    # Infrastructure relationships
    fw_id = agent_ids.get("freeway")
    cdb_id = agent_ids.get("clawdb")
    ollama_id = agent_ids.get("ollama")
    n8n_id = agent_ids.get("n8n")
    nr_id = router_ids.get("native-router")
    fcc_r_id = router_ids.get("fcc_router")
    mc_id = agent_ids.get("mission-control")
    grafana_id = agent_ids.get("grafana")
    exporter_id = agent_ids.get("fcc-metrics-exporter")

    if fw_id and fcc_r_id:
        upsert_relationship(fcc_r_id, fw_id, "USES", "hard", 1.0)
    if fw_id and ollama_id:
        upsert_relationship(fw_id, ollama_id, "INTEGRATES_WITH", "soft", 0.5)
    if exporter_id and fw_id:
        upsert_relationship(exporter_id, fw_id, "MONITORS", "hard", 1.0)
    if grafana_id and exporter_id:
        upsert_relationship(grafana_id, exporter_id, "DEPENDS_ON", "hard", 1.0)

    # Provider capabilities
    fw_cap = cap_ids.get("COST_OPTIMIZED_INFERENCE")
    nr_cap = cap_ids.get("GOVERNED_ROUTING")
    ol_cap = cap_ids.get("LOCAL_INFERENCE")
    kg_cap = cap_ids.get("KNOWLEDGE_GRAPH")

    if fw_id and fw_cap:
        upsert_relationship(fw_id, fw_cap, "PROVIDES", "hard", 1.0)
    if nr_id and nr_cap:
        upsert_relationship(nr_id, nr_cap, "PROVIDES", "hard", 1.0)
    if ollama_id and ol_cap:
        upsert_relationship(ollama_id, ol_cap, "PROVIDES", "hard", 1.0)
    if cdb_id and kg_cap:
        upsert_relationship(cdb_id, kg_cap, "PROVIDES", "hard", 1.0)

    # Trading agent protection relationships
    cc_dir = agent_ids.get("cashclaw_director")
    cc_arb = agent_ids.get("cashclaw_arb")
    pm_tr  = agent_ids.get("polymarket-trader")
    cc_ven = venture_ids.get("CashClaw")
    sentinel = agent_ids.get("trading_sentinel")

    for agent_id in [cc_dir, cc_arb, pm_tr]:
        if agent_id and cc_ven:
            upsert_relationship(agent_id, cc_ven, "BELONGS_TO", "hard", 1.0)
    if sentinel and cc_ven:
        upsert_relationship(sentinel, cc_ven, "MONITORS", "hard", 1.0)

    # Haiku model → CashClaw relationship
    haiku_id = model_ids.get("claude-haiku-4-5")
    if haiku_id and cc_dir:
        upsert_relationship(cc_dir, haiku_id, "USES", "hard", 1.0,
                            metadata={"purpose": "signal_scoring", "protected": True})

    # Report final counts
    print("\n=== SEED COMPLETE ===")
    counts = sql("""
SELECT entity_type, COUNT(*) as cnt FROM kg_entities GROUP BY entity_type ORDER BY cnt DESC;
""")
    print("Entity counts:\n", counts)
    rel_count = sql("SELECT COUNT(*) FROM kg_relationships;")
    print(f"Relationships: {rel_count}")
    print(f"\nFinished: {datetime.datetime.utcnow().isoformat()}Z")

if __name__ == "__main__":
    main()
