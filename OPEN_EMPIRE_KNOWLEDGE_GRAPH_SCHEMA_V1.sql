-- ============================================================
-- OPEN EMPIRE KNOWLEDGE GRAPH — ClawDB Schema V1
-- Authority: Nathan Asiegbu | Generated: 2026-08-09
-- DB: clawdb @ 127.0.0.1:5432
-- Governance: Open Empire V1 | Ontology: OPEN_EMPIRE_ONTOLOGY_V1
-- ============================================================

-- Extensions
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- ============================================================
-- ONTOLOGY CONSTANTS (enforced via CHECK constraints)
-- ============================================================

-- Entity types (governance-controlled enum via check)
-- AGENT, VENTURE, PROJECT, PROGRAM, PORTFOLIO, REPOSITORY,
-- CAPABILITY, PROVIDER, MODEL, ROUTER, SERVICE, RUNTIME,
-- WORKFLOW, DASHBOARD, GOVERNANCE_ARTIFACT, DECISION,
-- COST_RECORD, OUTCOME, SKILL, EXCEPTION, TASK, DATASET

-- Relationship types (OPEN_EMPIRE_ONTOLOGY_V1)
-- DEPENDS_ON, USES, IMPLEMENTS, RUNS_ON, HOSTS, OWNS,
-- GOVERNS, REPORTS_TO, BELONGS_TO, PROVIDES, MONITORS,
-- MANAGES, TRIGGERS, SUPERSEDES, BACKS_UP, INTEGRATES_WITH,
-- EXECUTED_BY, ROUTED_TO, PROVIDED_BY, PRODUCES, INCURS,
-- CONSUMES, OBSERVES, PROPOSES_CHANGE_TO

-- Evidence states
-- VERIFIED, DERIVED, UNVERIFIED, DEPRECATED

-- ============================================================
-- TABLE: entities
-- ============================================================

CREATE TABLE IF NOT EXISTS kg_entities (
    id                  BIGSERIAL PRIMARY KEY,
    asset_uuid          UUID NOT NULL DEFAULT gen_random_uuid(),
    canonical_name      TEXT NOT NULL,
    entity_type         TEXT NOT NULL CHECK (entity_type IN (
                            'AGENT','VENTURE','PROJECT','PROGRAM','PORTFOLIO',
                            'REPOSITORY','CAPABILITY','PROVIDER','MODEL','ROUTER',
                            'SERVICE','RUNTIME','WORKFLOW','DASHBOARD',
                            'GOVERNANCE_ARTIFACT','DECISION','COST_RECORD',
                            'OUTCOME','SKILL','EXCEPTION','TASK','DATASET'
                        )),
    layer               TEXT,
    status              TEXT NOT NULL DEFAULT 'active' CHECK (status IN (
                            'active','inactive','deprecated','draft','blocked'
                        )),
    description         TEXT,
    -- Provenance hierarchy
    portfolio_id        BIGINT REFERENCES kg_entities(id) ON DELETE SET NULL,
    program_id          BIGINT REFERENCES kg_entities(id) ON DELETE SET NULL,
    project_id          BIGINT REFERENCES kg_entities(id) ON DELETE SET NULL,
    venture_id          BIGINT REFERENCES kg_entities(id) ON DELETE SET NULL,
    capability_id       BIGINT REFERENCES kg_entities(id) ON DELETE SET NULL,
    repository_id       BIGINT REFERENCES kg_entities(id) ON DELETE SET NULL,
    runtime_id          BIGINT REFERENCES kg_entities(id) ON DELETE SET NULL,
    -- Ownership
    owner               TEXT,
    -- Provenance
    source_system       TEXT NOT NULL DEFAULT 'alusi-seed',
    source_record_id    TEXT,
    source_version      TEXT,
    source_hash         TEXT,
    evidence_status     TEXT NOT NULL DEFAULT 'VERIFIED' CHECK (evidence_status IN (
                            'VERIFIED','DERIVED','UNVERIFIED','DEPRECATED'
                        )),
    confidence          NUMERIC(3,2) CHECK (confidence BETWEEN 0 AND 1),
    -- Flexible metadata (no secrets/PII)
    metadata            JSONB NOT NULL DEFAULT '{}',
    -- Timestamps
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    first_seen_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_seen_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    is_active           BOOLEAN NOT NULL DEFAULT TRUE,

    CONSTRAINT kg_entities_uuid_unique UNIQUE (asset_uuid)
);

-- Indexes for kg_entities
CREATE INDEX IF NOT EXISTS idx_kg_entities_uuid        ON kg_entities(asset_uuid);
CREATE INDEX IF NOT EXISTS idx_kg_entities_type        ON kg_entities(entity_type);
CREATE INDEX IF NOT EXISTS idx_kg_entities_name        ON kg_entities(canonical_name);
CREATE INDEX IF NOT EXISTS idx_kg_entities_status      ON kg_entities(status);
CREATE INDEX IF NOT EXISTS idx_kg_entities_is_active   ON kg_entities(is_active);
CREATE INDEX IF NOT EXISTS idx_kg_entities_capability  ON kg_entities(capability_id);
CREATE INDEX IF NOT EXISTS idx_kg_entities_repository  ON kg_entities(repository_id);
CREATE INDEX IF NOT EXISTS idx_kg_entities_venture     ON kg_entities(venture_id);
CREATE INDEX IF NOT EXISTS idx_kg_entities_metadata    ON kg_entities USING GIN(metadata);
CREATE INDEX IF NOT EXISTS idx_kg_entities_name_trgm   ON kg_entities USING GIN(canonical_name gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_kg_entities_updated     ON kg_entities(updated_at DESC);

-- Auto-update updated_at
CREATE OR REPLACE FUNCTION kg_update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER kg_entities_updated_at
    BEFORE UPDATE ON kg_entities
    FOR EACH ROW EXECUTE FUNCTION kg_update_timestamp();

-- ============================================================
-- TABLE: entity_aliases
-- ============================================================

CREATE TABLE IF NOT EXISTS kg_entity_aliases (
    id          BIGSERIAL PRIMARY KEY,
    entity_id   BIGINT NOT NULL REFERENCES kg_entities(id) ON DELETE CASCADE,
    alias       TEXT NOT NULL,
    alias_type  TEXT DEFAULT 'name' CHECK (alias_type IN ('name','pm2_name','slug','legacy')),
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(entity_id, alias)
);

CREATE INDEX IF NOT EXISTS idx_kg_aliases_entity ON kg_entity_aliases(entity_id);
CREATE INDEX IF NOT EXISTS idx_kg_aliases_alias  ON kg_entity_aliases USING GIN(alias gin_trgm_ops);

-- ============================================================
-- TABLE: relationships
-- ============================================================

CREATE TABLE IF NOT EXISTS kg_relationships (
    id                  BIGSERIAL PRIMARY KEY,
    source_entity_id    BIGINT NOT NULL REFERENCES kg_entities(id) ON DELETE CASCADE,
    target_entity_id    BIGINT NOT NULL REFERENCES kg_entities(id) ON DELETE CASCADE,
    relationship_type   TEXT NOT NULL CHECK (relationship_type IN (
                            'DEPENDS_ON','USES','IMPLEMENTS','RUNS_ON','HOSTS',
                            'OWNS','GOVERNS','REPORTS_TO','BELONGS_TO','PROVIDES',
                            'MONITORS','MANAGES','TRIGGERS','SUPERSEDES',
                            'BACKS_UP','INTEGRATES_WITH','EXECUTED_BY',
                            'ROUTED_TO','PROVIDED_BY','PRODUCES','INCURS',
                            'CONSUMES','OBSERVES','PROPOSES_CHANGE_TO'
                        )),
    dependency_class    TEXT CHECK (dependency_class IN (
                            'hard','soft','optional','governance','observational'
                        )),
    status              TEXT NOT NULL DEFAULT 'active' CHECK (status IN (
                            'active','inactive','deprecated','proposed','blocked'
                        )),
    strength            NUMERIC(3,2) DEFAULT 1.0 CHECK (strength BETWEEN 0 AND 1),
    -- Provenance
    evidence_status     TEXT NOT NULL DEFAULT 'VERIFIED' CHECK (evidence_status IN (
                            'VERIFIED','DERIVED','UNVERIFIED','DEPRECATED'
                        )),
    source_system       TEXT NOT NULL DEFAULT 'alusi-seed',
    source_record_id    TEXT,
    -- Metadata
    metadata            JSONB NOT NULL DEFAULT '{}',
    -- Validity window
    valid_from          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    valid_to            TIMESTAMPTZ,
    -- Timestamps
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    is_active           BOOLEAN NOT NULL DEFAULT TRUE,

    -- No duplicate active edges for same semantic relationship
    CONSTRAINT kg_rel_no_dup UNIQUE (source_entity_id, target_entity_id, relationship_type),
    -- No self-loops (except SUPERSEDES which is self-referential by design)
    CONSTRAINT kg_rel_no_selfloop CHECK (
        source_entity_id != target_entity_id
        OR relationship_type = 'SUPERSEDES'
    )
);

CREATE INDEX IF NOT EXISTS idx_kg_rel_source       ON kg_relationships(source_entity_id);
CREATE INDEX IF NOT EXISTS idx_kg_rel_target       ON kg_relationships(target_entity_id);
CREATE INDEX IF NOT EXISTS idx_kg_rel_type         ON kg_relationships(relationship_type);
CREATE INDEX IF NOT EXISTS idx_kg_rel_status       ON kg_relationships(status);
CREATE INDEX IF NOT EXISTS idx_kg_rel_is_active    ON kg_relationships(is_active);
CREATE INDEX IF NOT EXISTS idx_kg_rel_metadata     ON kg_relationships USING GIN(metadata);
CREATE INDEX IF NOT EXISTS idx_kg_rel_updated      ON kg_relationships(updated_at DESC);

CREATE TRIGGER kg_relationships_updated_at
    BEFORE UPDATE ON kg_relationships
    FOR EACH ROW EXECUTE FUNCTION kg_update_timestamp();

-- ============================================================
-- TABLE: relationship_evidence
-- ============================================================

CREATE TABLE IF NOT EXISTS kg_relationship_evidence (
    id              BIGSERIAL PRIMARY KEY,
    relationship_id BIGINT NOT NULL REFERENCES kg_relationships(id) ON DELETE CASCADE,
    evidence_type   TEXT NOT NULL CHECK (evidence_type IN (
                        'pm2_state','config_file','registry','manual','derived','cost_record'
                    )),
    evidence_path   TEXT,
    evidence_hash   TEXT,
    evidence_data   JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_kg_evidence_rel ON kg_relationship_evidence(relationship_id);

-- ============================================================
-- TABLE: graph_events (audit trail)
-- ============================================================

CREATE TABLE IF NOT EXISTS kg_graph_events (
    id          BIGSERIAL PRIMARY KEY,
    event_type  TEXT NOT NULL CHECK (event_type IN (
                    'entity_created','entity_updated','entity_deprecated',
                    'relationship_created','relationship_deprecated',
                    'seed_run','validation_run','api_query'
                )),
    entity_id   BIGINT REFERENCES kg_entities(id) ON DELETE SET NULL,
    rel_id      BIGINT REFERENCES kg_relationships(id) ON DELETE SET NULL,
    actor       TEXT NOT NULL DEFAULT 'alusi',
    details     JSONB DEFAULT '{}',
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_kg_events_type      ON kg_graph_events(event_type);
CREATE INDEX IF NOT EXISTS idx_kg_events_entity    ON kg_graph_events(entity_id);
CREATE INDEX IF NOT EXISTS idx_kg_events_created   ON kg_graph_events(created_at DESC);

-- ============================================================
-- TABLE: cost_records (cost/outcome linkage — P0.7)
-- ============================================================

CREATE TABLE IF NOT EXISTS kg_cost_records (
    id              BIGSERIAL PRIMARY KEY,
    asset_uuid      UUID NOT NULL DEFAULT gen_random_uuid(),
    agent_entity_id BIGINT REFERENCES kg_entities(id) ON DELETE SET NULL,
    task_entity_id  BIGINT REFERENCES kg_entities(id) ON DELETE SET NULL,
    venture_entity_id BIGINT REFERENCES kg_entities(id) ON DELETE SET NULL,
    provider        TEXT NOT NULL,
    model           TEXT NOT NULL,
    route           TEXT,
    prompt_tokens   INTEGER DEFAULT 0,
    completion_tokens INTEGER DEFAULT 0,
    total_tokens    INTEGER DEFAULT 0,
    compression_ratio NUMERIC(4,3) DEFAULT 1.0,
    cache_hit       BOOLEAN DEFAULT FALSE,
    latency_ms      INTEGER,
    retries         INTEGER DEFAULT 0,
    fallbacks       INTEGER DEFAULT 0,
    estimated_cost_usd NUMERIC(12,8) DEFAULT 0,
    success         BOOLEAN NOT NULL DEFAULT TRUE,
    quality_score   NUMERIC(3,2),
    task_type       TEXT,
    metadata        JSONB DEFAULT '{}',
    recorded_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT kg_cost_uuid_unique UNIQUE (asset_uuid)
);

CREATE INDEX IF NOT EXISTS idx_kg_cost_agent    ON kg_cost_records(agent_entity_id);
CREATE INDEX IF NOT EXISTS idx_kg_cost_venture  ON kg_cost_records(venture_entity_id);
CREATE INDEX IF NOT EXISTS idx_kg_cost_provider ON kg_cost_records(provider);
CREATE INDEX IF NOT EXISTS idx_kg_cost_model    ON kg_cost_records(model);
CREATE INDEX IF NOT EXISTS idx_kg_cost_date     ON kg_cost_records(recorded_at DESC);
CREATE INDEX IF NOT EXISTS idx_kg_cost_success  ON kg_cost_records(success);

-- ============================================================
-- HELPER VIEWS
-- ============================================================

CREATE OR REPLACE VIEW kg_active_entities AS
    SELECT * FROM kg_entities WHERE is_active = TRUE AND status = 'active';

CREATE OR REPLACE VIEW kg_active_relationships AS
    SELECT r.*, 
           s.canonical_name AS source_name, s.entity_type AS source_type,
           t.canonical_name AS target_name, t.entity_type AS target_type
    FROM kg_relationships r
    JOIN kg_entities s ON r.source_entity_id = s.id
    JOIN kg_entities t ON r.target_entity_id = t.id
    WHERE r.is_active = TRUE AND r.status = 'active';

CREATE OR REPLACE VIEW kg_cost_by_provider AS
    SELECT provider, model,
           COUNT(*) as call_count,
           SUM(total_tokens) as total_tokens,
           SUM(estimated_cost_usd) as total_cost_usd,
           AVG(latency_ms) as avg_latency_ms,
           SUM(CASE WHEN success THEN 1 ELSE 0 END)::float / COUNT(*) as success_rate
    FROM kg_cost_records
    GROUP BY provider, model
    ORDER BY total_cost_usd DESC;

CREATE OR REPLACE VIEW kg_cost_by_venture AS
    SELECT v.canonical_name as venture, v.asset_uuid as venture_uuid,
           COUNT(cr.*) as call_count,
           SUM(cr.total_tokens) as total_tokens,
           SUM(cr.estimated_cost_usd) as total_cost_usd
    FROM kg_cost_records cr
    LEFT JOIN kg_entities v ON cr.venture_entity_id = v.id
    GROUP BY v.canonical_name, v.asset_uuid
    ORDER BY total_cost_usd DESC;

-- ============================================================
-- SEED EVENT (marks schema creation)
-- ============================================================

INSERT INTO kg_graph_events (event_type, actor, details)
VALUES ('seed_run', 'alusi', '{"phase":"schema_creation","version":"V1","schema_tables":["kg_entities","kg_entity_aliases","kg_relationships","kg_relationship_evidence","kg_graph_events","kg_cost_records"]}');
