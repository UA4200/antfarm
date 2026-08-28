# Open Empire Capability Factory Spec
**Version:** 1.0 | **Date:** 2026-08-09

---

## Concept
Repositories are implementation units. Capabilities are operational/business units.
A capability is what the Empire *can do*, not what code exists on disk.

## Capability Activation Model

```
ENABLE CAPABILITY <name>
  ↓
Resolve: required repos + services + agents + workflows + models + dashboards
  ↓
Health check each dependency
  ↓
Start missing services (via PM2)
  ↓
Register in KG
  ↓
Return: CAPABILITY_ACTIVE | CAPABILITY_DEGRADED | CAPABILITY_BLOCKED
```

## Current Capability Catalog (16 total)

| Capability | Status | Key Repos/Services |
|---|---|---|
| COST_OPTIMIZED_INFERENCE | ✅ OPERATIONAL | Free-Way, adaptive_router.py |
| GOVERNED_ROUTING | ✅ OPERATIONAL | native-router |
| LOCAL_INFERENCE | ✅ OPERATIONAL | Ollama (6 models) |
| ADAPTIVE_ROUTING | ✅ OPERATIONAL | oe-proxy v2 |
| PREMIUM_ESCALATION_CONTROL | ✅ OPERATIONAL | oe-proxy audit log |
| KNOWLEDGE_GRAPH | ✅ OPERATIONAL | ClawDB + kg-api |
| COST_TELEMETRY | ✅ OPERATIONAL | grafana + fcc-metrics-exporter |
| MEMORY_PIPELINE | ✅ OPERATIONAL | memory/ + OpenClaw wiki |
| TASK_OBSERVER | ✅ OPERATIONAL_GUARDED | task_observer_collector.py |
| ECONOMIC_GOVERNOR | ✅ OPERATIONAL | economic_guard.py |
| OBSIDIAN_HUMAN_VIEW | ✅ OPERATIONAL | workspace vault (5 MOCs) |
| AUTONOMOUS_TRADING | ✅ PROTECTED | CashClaw (PM2 38-41) |
| WORKFLOW_AUTOMATION | ✅ OPERATIONAL | n8n (14 workflows) |
| CICD_FACTORY | 🔲 DESIGNED | GitHub Actions (UA4200) |
| CAPABILITY_FACTORY | 🔲 DESIGNED | This spec |
| REPOSITORY_FACTORY | 🔲 DESIGNED | kg_seed.py + registry |

## Capability Domains

| Domain | Capabilities |
|---|---|
| Inference | COST_OPTIMIZED_INFERENCE, GOVERNED_ROUTING, LOCAL_INFERENCE, ADAPTIVE_ROUTING, PREMIUM_ESCALATION_CONTROL |
| Intelligence | KNOWLEDGE_GRAPH, MEMORY_PIPELINE, TASK_OBSERVER, OBSIDIAN_HUMAN_VIEW |
| Operations | ECONOMIC_GOVERNOR, WORKFLOW_AUTOMATION, COST_TELEMETRY |
| Trading | AUTONOMOUS_TRADING |
| Development | CICD_FACTORY, CAPABILITY_FACTORY, REPOSITORY_FACTORY |

## Extending: Adding a New Capability
1. Define capability in `OPEN_EMPIRE_CAPABILITY_REGISTRY_V2.json`
2. Seed entity in ClawDB KG (`kg_seed.py`)
3. Map to required repos/services
4. Add activation logic
5. Register relationships (`PROVIDES`, `DEPENDS_ON`, `INTEGRATES_WITH`)
6. Add MOC entry in Obsidian
