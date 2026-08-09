#!/usr/bin/env python3
"""
Open Empire Governed Inference Proxy — v2.0 (Adaptive)
Port: 4100 | Loopback only | ANTHROPIC_BASE_URL=http://127.0.0.1:4100

v2: Replaced hardcoded Groq-first chains with adaptive_router.
    Groq competes equally with all providers via dynamic scoring.
    Provider selected by: task_fit × quality × cost × reliability × latency.

2026-08-09 | Authority: Nathan Asiegbu
"""
import os, json, time, datetime, http.server, logging, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import adaptive_router as AR

PORT  = int(os.environ.get("OE_PROXY_PORT", "4100"))
HOST  = "127.0.0.1"
LOG_FILE = pathlib.Path.home() / ".openclaw/logs/oe_proxy_calls.jsonl"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(level=logging.INFO, format="[oe_proxy] %(message)s")
log = logging.getLogger("oe_proxy")

# Map requested claude-* model → task_type for the adaptive router
def _model_to_task(model_name, prompt_text=""):
    """Classify the task from model tier + prompt heuristics."""
    m = model_name.lower()
    # Tool-use: handled by caller checking tools parameter
    # Model tier hints
    if "opus" in m:   return "critical"
    if "haiku" in m:  return "general"
    if "sonnet" in m: return "analysis"
    return "general"

def _detect_task_from_prompt(messages):
    """Light heuristic to refine task classification from prompt content."""
    if not messages: return None
    last = messages[-1].get("content","")
    if isinstance(last, list):
        last = " ".join(c.get("text","") for c in last if c.get("type")=="text")
    last_lower = last.lower()[:300]
    if any(w in last_lower for w in ["def ","class ","import ","function","bug","syntax","code","python","script"]):
        return "coding"
    if any(w in last_lower for w in ["summarize","summarization","summary","tldr"]):
        return "summarize"
    if any(w in last_lower for w in ["spam or not","classify","is this","true or false","yes or no","label"]):
        return "classify"
    if any(w in last_lower for w in ["{","json","output json","return json","valid json"]):
        return "json_gen"
    if any(w in last_lower for w in ["analyze","analysis","explain","why","how does","compare"]):
        return "analysis"
    return None

def audit_log(entry):
    entry.pop("api_key", None)
    try:
        with open(LOG_FILE, "a") as f:
            f.write(json.dumps(entry, default=str) + "\n")
    except: pass

class ProxyHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, fmt, *args): pass

    def _send(self, body_dict, code=200):
        body = json.dumps(body_dict, default=str).encode()
        self.send_response(code)
        self.send_header("Content-Type","application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            return self._send({"status":"ok","service":"oe-proxy-v2-adaptive","port":PORT})
        if self.path == "/v1/models":
            # Reflect Claude models — CC compatibility
            return self._send({"object":"list","data":[
                {"id":"claude-sonnet-4-5","object":"model"},
                {"id":"claude-haiku-4-5","object":"model"},
                {"id":"claude-opus-4-5","object":"model"},
            ]})
        if self.path == "/provider-status":
            return self._send({"providers": AR.get_provider_summary()})
        self._send({"error":"not found"},404)

    def do_POST(self):
        length   = int(self.headers.get("Content-Length",0))
        raw_body = self.rfile.read(length)
        try:
            req_body = json.loads(raw_body)
        except Exception:
            return self._send({"error":{"type":"parse_error","message":"invalid JSON"}},400)

        original_model = req_body.get("model","claude-sonnet-4-5")
        messages    = req_body.get("messages",[])
        system      = req_body.get("system","") or ""
        max_tokens  = req_body.get("max_tokens",1024)
        tools       = req_body.get("tools")
        is_stream   = req_body.get("stream", False)

        # Task classification: model tier + prompt heuristics
        task_type = _model_to_task(original_model)
        refined   = _detect_task_from_prompt(messages)
        if refined: task_type = refined

        # tool-use: always Anthropic (LLaMA doesn't reliably emit tool_use schema)
        if tools:
            task_type = "tool_use"
            log.info(f"Tool-call detected → routing to Anthropic for schema safety")

        # Opus tier → critical, always paid
        force_paid = "opus" in original_model.lower()

        try:
            result = AR.route(task_type, messages, system, max_tokens,
                              tools=tools, force_paid=force_paid,
                              context_label=f"cc:{original_model}")

            if not result.get("success"):
                raise RuntimeError(result.get("error","all_routes_failed"))

            # Build Anthropic-format response (CC compatibility)
            content_out = result.get("full_content") or [{"type":"text","text":result.get("text","")}]
            resp = {
                "id":   f"oe2-{int(time.time())}",
                "type": "message",
                "role": "assistant",
                "model":  original_model,   # Echo original — CC expects this
                "content": content_out,
                "stop_reason": result.get("stop_reason","end_turn"),
                "usage": {"input_tokens": result.get("in_tok",0),
                          "output_tokens": result.get("out_tok",0)},
                "_oe_route": {
                    "provider":    result.get("provider"),
                    "model":       result.get("model"),
                    "cost_usd":    result.get("cost_usd",0),
                    "latency_ms":  result.get("latency_ms",0),
                    "task_type":   task_type,
                    "is_premium":  result.get("is_premium",False),
                    "attempt_count": len(result.get("attempts",[])),
                },
            }

            audit_log({
                "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "original_model": original_model,
                "task_type":      task_type,
                "routed_provider":result.get("provider"),
                "routed_model":   result.get("model"),
                "is_premium":     result.get("is_premium",False),
                "cost_usd":       result.get("cost_usd",0),
                "latency_ms":     result.get("latency_ms",0),
                "attempt_count":  len(result.get("attempts",[])),
                "has_tools":      bool(tools),
            })

            return self._send(resp)

        except Exception as e:
            log.error(f"Route failed: {e}")
            return self._send({"error":{"type":"proxy_error","message":str(e)[:200]}},500)

if __name__ == "__main__":
    server = http.server.HTTPServer((HOST, PORT), ProxyHandler)
    log.info(f"OE Proxy v2 (Adaptive) listening on http://{HOST}:{PORT}")
    log.info(f"export ANTHROPIC_BASE_URL=http://{HOST}:{PORT}")
    log.info(f"Dynamic routing: all providers compete via scoring (no hardcoded Groq-first)")
    server.serve_forever()
