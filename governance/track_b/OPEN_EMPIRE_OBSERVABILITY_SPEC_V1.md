# OPEN EMPIRE — ENTERPRISE OBSERVABILITY SPEC V1
## Foundational Enhancement #2: Unified Observability Stack

**Status:** SPEC  
**Version:** 1.0.0  
**Created:** 2026-08-06  
**Operator:** Nathan Asiegbu  
**Governed by:** Open Empire Constitution v2, Governance Baseline v1.0.0 (commit 17df0ff)

---

## 1. Executive Summary

Open Empire currently operates 42 PM2 processes across 5 portfolios with no unified log aggregation, no distributed tracing, no Prometheus metrics export, and no standard health endpoints. Grafana exists on port 3001 but health status is unknown as of 2026-08-06.

This spec defines the target observability stack in three phases: **Quick Wins** (days), **Core Stack** (weeks), and **Full Telemetry** (months).

The guiding principle: **every service must be observable without SSHing into the host.**

---

## 2. Current State Assessment

| Pillar       | Component                       | Status            | Gap                                           |
|-------------|----------------------------------|-------------------|-----------------------------------------------|
| Logs        | PM2 native logs                  | ✅ Active          | No structured JSON format. No central sink.   |
| Logs        | `~/.openclaw/logs/` directory    | ✅ Exists          | Files written, no rotation policy enforced.   |
| Metrics     | PM2 metrics API                  | ✅ Active          | No scrape endpoint exposed.                   |
| Metrics     | Grafana (port 3001)              | ⚠️ Unknown        | Health check needed.                          |
| Metrics     | Prometheus                       | ❌ Not deployed    | No exporter.                                  |
| Health      | Service health endpoints         | ❌ Missing         | No `/health` routes on any PM2 service.       |
| Alerts      | Telegram channel                 | ✅ Active          | Ad-hoc. No severity matrix.                   |
| Alerts      | n8n routing                      | ⚠️ Inactive       | n8n online but 0 workflows deployed.          |
| Traces      | OpenTelemetry                    | ❌ Not deployed    | No distributed tracing.                       |

---

## 3. Target Observability Stack

### 3.1 Logs

**Current path:** PM2 stdout/stderr → `~/.openclaw/logs/<service>.log`  
**Target path:** PM2 → structured JSON → rotated files → (future) Loki or Elasticsearch

#### Standards

All services MUST write structured JSON logs with these mandatory fields:

```json
{
  "timestamp": "2026-08-06T12:00:00.000Z",
  "level": "INFO|WARN|ERROR|DEBUG",
  "service": "<pm2-process-name>",
  "version": "<semver>",
  "message": "Human-readable message",
  "trace_id": "<optional-uuid>",
  "data": {}
}
```

#### PM2 Log Date Format Standardization (Quick Win)

Add to all `ecosystem.config.js` files:

```js
env: {
  PM2_LOG_DATE_FORMAT: "YYYY-MM-DDTHH:mm:ss.SSSZ"
}
```

Or globally via PM2 config:

```bash
pm2 set pm2:log-date-format 'YYYY-MM-DDTHH:mm:ss.SSSZ'
```

#### Log Rotation Policy

| Service Class | Max Size | Retain |
|--------------|----------|--------|
| Trading agents (cashclaw_director, cashclaw_arb, polymarket-trader) | 50 MB | 7 days |
| Core infrastructure (executor, heartbeat, gateway) | 100 MB | 30 days |
| Staging / degraded services | 20 MB | 3 days |
| All others | 50 MB | 14 days |

```bash
# Enable PM2 log rotation
pm2 install pm2-logrotate
pm2 set pm2-logrotate:max_size 50M
pm2 set pm2-logrotate:retain 7
pm2 set pm2-logrotate:compress true
pm2 set pm2-logrotate:dateFormat YYYY-MM-DD
```

#### Future: Log Forwarding

```
PM2 log files → Filebeat/Vector → Loki → Grafana LogQL
                                OR
                              → Elasticsearch → Kibana
```

Decision deferred until local storage pressure warrants it (threshold: >10 GB total log size).

---

### 3.2 Metrics

**Current state:** PM2 built-in metrics only (CPU, memory per process).  
**Target state:** Prometheus-compatible `/metrics` endpoint → Grafana dashboards.

#### PM2 Prometheus Exporter

Deploy `pm2-prom-module` or build a thin exporter:

```
Location: ~/.openclaw/workspace/observability/pm2-exporter/
Port: 9090
Endpoint: GET http://127.0.0.1:9090/metrics
```

**Metric families to expose:**

```prometheus
# HELP oe_pm2_process_status PM2 process status (1=online, 0=stopped, -1=errored)
oe_pm2_process_status{name="cashclaw_director", id="38"} 1

# HELP oe_pm2_process_restarts Total PM2 restarts since epoch
oe_pm2_process_restarts{name="cashclaw_director", id="38"} 0

# HELP oe_pm2_process_cpu_percent CPU utilization
oe_pm2_process_cpu_percent{name="cashclaw_director", id="38"} 0.3

# HELP oe_pm2_process_memory_bytes Memory usage in bytes
oe_pm2_process_memory_bytes{name="cashclaw_director", id="38"} 45678592

# HELP oe_trading_daily_spend_usd Daily spend against cap
oe_trading_daily_spend_usd{agent="cashclaw_director", cap="10"} 1.25

# HELP oe_trading_balance_usd Current trading account balance
oe_trading_balance_usd{platform="kalshi"} 25.19
oe_trading_balance_usd{platform="polymarket"} 0.06

# HELP oe_governance_validation_pass Governance validation last result
oe_governance_validation_pass{suite="baseline"} 1
```

#### Grafana Configuration

- **Existing:** Grafana on port 3001 (status unknown — health check required).
- **Action:** Run `curl -f http://127.0.0.1:3001/api/health` on first implementation sprint.
- **Target dashboards:** See Section 5.

---

### 3.3 Health Endpoints

Every PM2 service that exposes an HTTP server MUST implement:

```
GET /health
```

**Standard Response Schema:**

```json
{
  "status": "healthy|degraded|unhealthy",
  "version": "1.0.0",
  "service": "cashclaw_director",
  "uptime_seconds": 3600,
  "timestamp": "2026-08-06T12:00:00Z",
  "checks": {
    "database": "ok|fail|skip",
    "external_api": "ok|fail|skip",
    "spend_cap": "ok|warn|fail",
    "last_cycle_elapsed_seconds": 42
  }
}
```

**HTTP Status Codes:**

| Status   | Code |
|----------|------|
| healthy  | 200  |
| degraded | 200  |
| unhealthy | 503 |

**Health Endpoint Template (`health_endpoint_template.py`):**

```python
import time
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

SERVICE_NAME = "your-service-name"
SERVICE_VERSION = "1.0.0"
START_TIME = time.time()

def check_health() -> dict:
    return {
        "status": "healthy",
        "version": SERVICE_VERSION,
        "service": SERVICE_NAME,
        "uptime_seconds": int(time.time() - START_TIME),
        "timestamp": __import__("datetime").datetime.utcnow().isoformat() + "Z",
        "checks": {}
    }

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            result = check_health()
            status_code = 200 if result["status"] != "unhealthy" else 503
            body = json.dumps(result).encode()
            self.send_response(status_code)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, fmt, *args):
        pass  # Suppress default access logs

def start_health_server(port: int = 8080):
    server = HTTPServer(("127.0.0.1", port), HealthHandler)
    server.serve_forever()
```

**Health Port Allocation (reserved):**

| Service | Health Port |
|---------|-------------|
| cashclaw_director | 8038 |
| cashclaw_arb | 8039 |
| polymarket-trader | 8040 |
| trading_sentinel | 8041 |
| alusi-gateway | 8002 |
| alusi-orchestrator | 8006 |
| hyrvea-monitor | 8010 |
| executive-dashboard (future) | 8080 |

---

### 3.4 Alerts

**Primary channel:** Telegram (already wired via `alusi-telegram-adapter` + `telegram-approvals`).  
**Secondary channel:** n8n webhooks (once workflows are deployed).

#### Alert Severity Matrix

| Severity | Trigger Examples | SLA | Action |
|----------|-----------------|-----|--------|
| **P0 - CRITICAL** | Trading agent down unexpectedly, daily spend cap breached, database offline, governance artifact tampered | Immediate | Telegram direct message + PM2 alert + auto-stop trading |
| **P1 - HIGH** | Service restart > 3x in 1h, balance < $2 on any trading platform, Kalshi/Polymarket API auth failure | < 5 min | Telegram notification |
| **P2 - MEDIUM** | Spend cap > 80% of daily limit, staging service degraded, Grafana unreachable | < 15 min | Telegram notification |
| **P3 - LOW** | Log rotation triggered, PM2 restart count incremented, n8n workflow failed | < 1 hour | Logged, Telegram daily digest |
| **INFO** | Successful trade placed, governance validation passed, agent cycle completed | None | Logged only |

#### Alert Template (Telegram)

```
🚨 [P0-CRITICAL] Open Empire Alert
Service: cashclaw_director
Event: AGENT_DOWN
Time: 2026-08-06T12:00:00Z
Details: Process exited unexpectedly (exit code 1)
Action Required: pm2 restart cashclaw_director
Dashboard: http://127.0.0.1:3333
```

#### Alert Dedup Policy

- Same alert from same service: suppress repeat within 5 minutes.
- Same alert class (e.g. AGENT_DOWN): suppress within 1 minute if already notified.
- CRITICAL: no dedup — always send.

---

### 3.5 Distributed Tracing (Future)

**Target:** OpenTelemetry for cross-service request tracing.

**Scope:**
- Trading cycle: director → signal_engine → executor → trade log
- Approval flow: exec-gateway → telegram-approvals → sovereign-proxy → executor
- BLCO outreach: lead → enricher → draft → approval queue

**Implementation deferred until:**
1. Health endpoints are live on all major services.
2. Prometheus exporter is deployed.
3. n8n has at least 3 active workflows.

**Chosen SDK:** `opentelemetry-sdk` (Python), `@opentelemetry/api` (Node.js)  
**Collector:** Jaeger or Grafana Tempo (local, 127.0.0.1 only)

---

## 4. Implementation Phases

### Phase 1 — Quick Wins (Days 1–3)
*Prerequisites: None. Zero infra changes.*

| Task | Owner | Acceptance Criteria |
|------|-------|---------------------|
| Set PM2 log date format globally | Nathan / Alusi | All PM2 logs show ISO timestamps |
| Check Grafana health at port 3001 | Nathan / Alusi | HTTP 200 or documented as offline |
| Deploy `pm2-logrotate` module | Alusi | `pm2 logs` shows rotation active |
| Document health port allocation | Alusi | Port table committed to governance/ |
| Add Telegram alert severity matrix to n8n (even as manual trigger) | Nathan | Alert format validated |

**Acceptance Gate:** PM2 logs are timestamped, Grafana status known, log rotation active.

---

### Phase 2 — Core Stack (Days 4–14)
*Prerequisites: Phase 1 complete.*

| Task | Owner | Acceptance Criteria |
|------|-------|---------------------|
| Build PM2 Prometheus exporter | Alusi | `curl 127.0.0.1:9090/metrics` returns valid Prometheus output |
| Add `/health` endpoint to cashclaw_director | Alusi | `curl 127.0.0.1:8038/health` returns JSON with status/uptime/checks |
| Add `/health` endpoint to cashclaw_arb | Alusi | Same as above, port 8039 |
| Add `/health` endpoint to polymarket-trader | Alusi | Same as above, port 8040 |
| Add `/health` endpoint to trading_sentinel | Alusi | Same as above, port 8041 |
| Configure Grafana datasource (Prometheus) | Nathan | Grafana shows PM2 metrics |
| Create Grafana PM2 dashboard | Alusi | All 42 processes visible with CPU/mem |
| Wire P0 Telegram alert: AGENT_DOWN | Alusi | Killing a test process triggers Telegram message |
| Wire P1 Telegram alert: spend cap 80% | Alusi | Simulated spend triggers warning |

**Acceptance Gate:** All 4 trading services have `/health` endpoints. Grafana shows live PM2 metrics. Two alert rules active.

---

### Phase 3 — Full Telemetry (Days 15–45)
*Prerequisites: Phase 2 complete.*

| Task | Owner | Acceptance Criteria |
|------|-------|---------------------|
| Add `/health` endpoints to all remaining 33 services | Alusi | Full health sweep passes |
| Build n8n alert routing workflows | Alusi | All P0/P1 alerts auto-route through n8n |
| Implement governance drift detection alert | Alusi | SHA256 change triggers P0 alert |
| Structured JSON logs for all trading agents | Alusi | Logs are parseable JSON |
| Log forwarding to Loki (optional) | Nathan | Decision gate: only if log volume > 10 GB |
| OpenTelemetry traces on trading cycle | Alusi | Trade request spans visible in Jaeger |
| Mission Control health map widget | Alusi | Dashboard shows live health status per service |

**Acceptance Gate:** All services observable. Alerts routing through n8n. Governance drift detected automatically.

---

## 5. Grafana Dashboard Specifications

### 5.1 Open Empire PM2 Overview
- Panel: Process status grid (green/red per service)
- Panel: CPU usage top 10 processes
- Panel: Memory usage top 10 processes
- Panel: Restart count per process (last 24h)
- Panel: Total uptime percentage

### 5.2 Trading Operations
- Panel: Kalshi balance over time
- Panel: Polymarket balance over time
- Panel: Daily spend vs cap (gauge)
- Panel: Trade count per hour
- Panel: P&L trend (7 days)

### 5.3 Governance Health
- Panel: Last validation run timestamp
- Panel: SHA256 integrity status (pass/fail)
- Panel: Drift detection status (6 layers)
- Panel: Registry completeness %

---

## 6. Tooling Decisions

| Tool | Decision | Rationale |
|------|----------|-----------|
| Prometheus | Deploy (Phase 2) | Industry standard, Grafana native |
| Grafana | Verify + configure (Phase 1) | Already installed |
| pm2-logrotate | Deploy (Phase 1) | Official PM2 module, trivial setup |
| pm2-prom-module | Evaluate vs custom | Custom gives more control |
| OpenTelemetry | Defer (Phase 3) | Complexity not worth it yet |
| ELK/Loki | Defer until log volume warrants | 10 GB threshold |
| Jaeger | Defer (Phase 3) | Coupled to OTel decision |

---

## 7. Non-Goals (v1)

- No cloud logging (all loopback-bound, air-gap required).
- No APM products (Datadog, New Relic, etc.).
- No container-based log collection (no Docker in this runtime).
- No log ingestion to external services without explicit Nathan approval.

---

## 8. References

- Open Empire Constitution v2 — Section 4 (Operational Standards)
- Governance Baseline v1.0.0 — commit 17df0ff
- AGENTS.md — PM2 process registry
- Track B Enhancement #10 (Drift Detection Spec) — complements this document
- Track B Enhancement #7 (Event-Driven Ops) — alert routing via n8n
