#!/usr/bin/env python3
"""
Open Empire Knowledge Graph API — P0.8
Read-focused HTTP API for ClawDB KG queries.
Port: 6279 (loopback only)
Auth: OPENEMPIRE_ROUTER_KEY
Uses stdlib only (http.server + subprocess/psql).
"""
import os, json, subprocess, re, urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT   = int(os.environ.get("KG_PORT", 6279))
HOST   = "127.0.0.1"
DB_DSN = "postgresql://NeoOC@127.0.0.1:5432/clawdb"
MASTER_KEY = os.environ.get("OPENEMPIRE_ROUTER_KEY", "sk-ope-local")

def db(query):
    """Execute read-only SQL, return list of dicts."""
    r = subprocess.run(
        ["psql", "-h","127.0.0.1","-p","5432","-U","NeoOC","-d","clawdb",
         "--csv","-c", query],
        capture_output=True, text=True, timeout=10
    )
    if r.returncode != 0:
        raise RuntimeError(r.stderr[:200])
    lines = r.stdout.strip().splitlines()
    if not lines: return []
    headers = lines[0].split(",")
    rows = []
    for line in lines[1:]:
        vals = line.split(",")
        rows.append(dict(zip(headers, vals)))
    return rows

def safe_str(s): return re.sub(r"[';\"\\]", "", str(s or ""))[:200]

class KGHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args): pass  # suppress default logging

    def auth_ok(self):
        key = self.headers.get("x-api-key","")
        return key == MASTER_KEY

    def send_json(self, data, code=200):
        body = json.dumps(data, default=str).encode()
        self.send_response(code)
        self.send_header("Content-Type","application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if not self.auth_ok():
            return self.send_json({"error":"Unauthorized"}, 401)

        parsed = urllib.parse.urlparse(self.path)
        path   = parsed.path.rstrip("/")
        params = dict(urllib.parse.parse_qsl(parsed.query))

        try:
            if path == "/health":
                count = db("SELECT COUNT(*) as n FROM kg_entities;")
                return self.send_json({"status":"ok","entities":count[0]["n"]})

            elif path == "/entities":
                etype = safe_str(params.get("type",""))
                limit = min(int(params.get("limit",100)), 500)
                where = f"AND entity_type='{etype}'" if etype else ""
                rows  = db(f"SELECT id,asset_uuid,canonical_name,entity_type,status,description,owner,metadata FROM kg_entities WHERE is_active=TRUE {where} ORDER BY canonical_name LIMIT {limit};")
                return self.send_json({"entities": rows, "count": len(rows)})

            elif path.startswith("/entities/"):
                uid = safe_str(path.split("/")[-1])
                rows = db(f"SELECT * FROM kg_entities WHERE asset_uuid='{uid}' OR id='{uid}' LIMIT 1;")
                if not rows: return self.send_json({"error":"Not found"},404)
                return self.send_json(rows[0])

            elif path == "/relationships":
                entity_id = safe_str(params.get("entity_id",""))
                rtype     = safe_str(params.get("type",""))
                limit     = min(int(params.get("limit",100)), 500)
                where_parts = ["r.is_active=TRUE","r.status='active'"]
                if entity_id:
                    where_parts.append(f"(r.source_entity_id='{entity_id}' OR r.target_entity_id='{entity_id}')")
                if rtype:
                    where_parts.append(f"r.relationship_type='{rtype}'")
                where = " AND ".join(where_parts)
                rows  = db(f"SELECT r.id,r.relationship_type,r.dependency_class,r.strength,s.canonical_name as source,s.entity_type as source_type,t.canonical_name as target,t.entity_type as target_type FROM kg_relationships r JOIN kg_entities s ON r.source_entity_id=s.id JOIN kg_entities t ON r.target_entity_id=t.id WHERE {where} ORDER BY r.relationship_type LIMIT {limit};")
                return self.send_json({"relationships": rows, "count": len(rows)})

            elif path == "/search":
                q    = safe_str(params.get("q","")).replace("'","")
                limit= min(int(params.get("limit",20)), 100)
                rows = db(f"SELECT id,asset_uuid,canonical_name,entity_type,status,description FROM kg_entities WHERE canonical_name ILIKE '%{q}%' AND is_active=TRUE ORDER BY canonical_name LIMIT {limit};")
                return self.send_json({"results": rows, "query": q, "count": len(rows)})

            elif path == "/graph/agents":
                rows = db("SELECT e.id,e.asset_uuid,e.canonical_name,e.status,e.metadata FROM kg_entities e WHERE e.entity_type='AGENT' AND e.is_active=TRUE ORDER BY e.canonical_name;")
                return self.send_json({"agents": rows, "count": len(rows)})

            elif path == "/graph/ventures":
                rows = db("SELECT e.*,rel.canonical_name as related FROM kg_entities e LEFT JOIN kg_relationships r ON r.source_entity_id=e.id OR r.target_entity_id=e.id LEFT JOIN kg_entities rel ON rel.id=CASE WHEN r.source_entity_id=e.id THEN r.target_entity_id ELSE r.source_entity_id END WHERE e.entity_type='VENTURE' AND e.is_active=TRUE GROUP BY e.id,rel.canonical_name ORDER BY e.canonical_name LIMIT 50;")
                return self.send_json({"ventures": rows})

            elif path == "/graph/capabilities":
                rows = db("SELECT e.canonical_name,e.description,e.status,COUNT(r.id) as providers FROM kg_entities e LEFT JOIN kg_relationships r ON r.target_entity_id=e.id AND r.relationship_type='PROVIDES' WHERE e.entity_type='CAPABILITY' AND e.is_active=TRUE GROUP BY e.canonical_name,e.description,e.status;")
                return self.send_json({"capabilities": rows})

            elif path == "/graph/dependencies":
                entity_id = safe_str(params.get("entity_id",""))
                depth     = min(int(params.get("depth",2)), 5)
                if not entity_id: return self.send_json({"error":"entity_id required"},400)
                rows = db(f"SELECT r.relationship_type,s.canonical_name as from_entity,s.entity_type as from_type,t.canonical_name as to_entity,t.entity_type as to_type FROM kg_relationships r JOIN kg_entities s ON r.source_entity_id=s.id JOIN kg_entities t ON r.target_entity_id=t.id WHERE (r.source_entity_id='{entity_id}' OR r.target_entity_id='{entity_id}') AND r.is_active=TRUE;")
                return self.send_json({"dependencies": rows, "entity_id": entity_id})

            elif path == "/cost/summary":
                rows = db("SELECT * FROM kg_cost_by_provider LIMIT 50;")
                total = db("SELECT SUM(estimated_cost_usd) as total, COUNT(*) as calls, SUM(total_tokens) as tokens FROM kg_cost_records;")
                return self.send_json({"by_provider": rows, "totals": total[0] if total else {}})

            elif path == "/cost/by-venture":
                rows = db("SELECT * FROM kg_cost_by_venture LIMIT 20;")
                return self.send_json({"by_venture": rows})

            elif path == "/validate":
                orphans = db("SELECT COUNT(*) as n FROM kg_relationships r LEFT JOIN kg_entities s ON r.source_entity_id=s.id LEFT JOIN kg_entities t ON r.target_entity_id=t.id WHERE s.id IS NULL OR t.id IS NULL;")
                dups    = db("SELECT COUNT(*) as n FROM (SELECT source_entity_id,target_entity_id,relationship_type,COUNT(*) as c FROM kg_relationships GROUP BY 1,2,3 HAVING COUNT(*)>1) x;")
                entities= db("SELECT COUNT(*) as n FROM kg_entities WHERE is_active=TRUE;")
                rels    = db("SELECT COUNT(*) as n FROM kg_relationships WHERE is_active=TRUE;")
                return self.send_json({
                    "valid": orphans[0]["n"]=="0" and dups[0]["n"]=="0",
                    "entities": entities[0]["n"], "relationships": rels[0]["n"],
                    "orphan_edges": orphans[0]["n"], "duplicate_edges": dups[0]["n"]
                })

            else:
                return self.send_json({"error":"Not found","endpoints":[
                    "GET /health","GET /entities?type=&limit=","GET /entities/{id_or_uuid}",
                    "GET /relationships?entity_id=&type=","GET /search?q=",
                    "GET /graph/agents","GET /graph/ventures","GET /graph/capabilities",
                    "GET /graph/dependencies?entity_id=",
                    "GET /cost/summary","GET /cost/by-venture","GET /validate"
                ]}, 404)

        except Exception as e:
            return self.send_json({"error": str(e)}, 500)

if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), KGHandler)
    print(f"[kg_api] Knowledge Graph API listening on http://{HOST}:{PORT}")
    print(f"[kg_api] Endpoints: /health /entities /relationships /search /graph/* /cost/* /validate")
    server.serve_forever()
