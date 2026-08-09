# Knowledge Graph
*Last updated: 2026-08-09*

Database: ClawDB (PostgreSQL 18.3, port 5432)
API: http://127.0.0.1:6279 (PM2 id=52)

## Stats
- 61+ entities | 23+ relationships | 0 orphans
- Entity types: AGENT, VENTURE, PROJECT, CAPABILITY, PROVIDER, MODEL, ROUTER, SERVICE, RUNTIME, DASHBOARD, REPOSITORY

## Query Examples
```bash
KG_KEY=$(grep OPENEMPIRE_ROUTER_KEY ~/.openclaw/secrets/.env | cut -d= -f2-)
curl -s "http://127.0.0.1:6279/entities?type=VENTURE" -H "x-api-key: $KG_KEY"
curl -s "http://127.0.0.1:6279/validate" -H "x-api-key: $KG_KEY"
```

## Available Endpoints (12 total)
- `GET /entities` — List entities (filter by type)
- `GET /entities/:id` — Get entity by ID
- `GET /relationships` — List relationships
- `GET /validate` — Validate graph integrity
- See kg-api PM2 52 for full endpoint list

## Navigation
← [[EMPIRE_HOME]]
