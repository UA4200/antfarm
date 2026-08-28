#!/usr/bin/env python3
"""
Open Empire Adaptive Inference Router — v1.0
Replaces hardcoded Groq-first chains with dynamic provider scoring.

Architecture:
  REQUEST → TASK_CLASSIFIER → CAPABILITY_FILTER → HEALTH_FILTER
  → DYNAMIC_SCORER → EXECUTOR → TELEMETRY → LEARNING

No provider is hardcoded as primary. Groq competes equally with all others.
Free providers earn economic advantage through scoring, not hard position.

2026-08-09 | Authority: Nathan Asiegbu
"""
import os, json, time, pathlib, hashlib, datetime, urllib.request, urllib.error, logging

log = logging.getLogger("adaptive_router")
HOME = pathlib.Path.home()
ROUTER_STATE_FILE = HOME / ".openclaw/router/router_state.json"
ROUTER_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
TELEMETRY_FILE = HOME / ".openclaw/logs/adaptive_router_telemetry.jsonl"
TELEMETRY_FILE.parent.mkdir(parents=True, exist_ok=True)

FW_BASE = "http://127.0.0.1:8082"

# ── Capability matrix ────────────────────────────────────────────────
# task_type → set of required capabilities
TASK_CAPS = {
    "heartbeat":       {"text"},
    "classify":        {"text"},
    "summarize":       {"text"},
    "extract":         {"text"},
    "json_gen":        {"text", "json"},
    "general":         {"text"},
    "analysis":        {"text", "reasoning"},
    "coding":          {"text", "code"},
    "complex_coding":  {"text", "code", "reasoning"},
    "long_context":    {"text", "long_context"},
    "tool_use":        {"text", "tools"},
    "critical":        {"text", "reasoning"},
}

# ── Provider capability declarations ─────────────────────────────────
PROVIDER_CAPS = {
    "groq/llama-3.1-8b":        {"text", "json", "code"},
    "groq/llama-3.3-70b":       {"text", "json", "code", "reasoning"},
    "cohere/command-r7b":       {"text", "json"},
    "cohere/command-r":         {"text", "json"},
    "cohere/command-r-plus":    {"text", "json", "reasoning"},
    "openrouter/north-mini-code":       {"text", "code"},
    "openrouter/nemotron-3-nano-30b-a3b": {"text", "json", "reasoning"},
    "openrouter/nemotron-3-super-120b-a12b": {"text","json","code","reasoning","long_context"},
    "openrouter/gpt-oss-20b":   {"text", "json", "code"},
    "openrouter/command-r-plus": {"text","json","reasoning"},
    "cerebras/zai-glm-4.7":     {"text"},
    "nvidia/llama-3.1-nemotron-ultra": {"text","json","reasoning"},
    "mistral/mistral-medium-3": {"text","json","code","reasoning"},
    "ollama/qwen2.5:3b":        {"text", "json", "code"},
    "ollama/qwen2.5:1.5b":      {"text", "json"},
    "ollama/llama3.2:3b":       {"text"},
    "ollama/tinyllama":         {"text"},
    # ── OpenAI — TIER 3 (low-cost paid) / TIER 4 (premium) ──────────────────
    # Placed after free/local tiers. Scored via policy; never default over free.
    "openai/gpt-4o-mini":       {"text","json","code","reasoning","tools"},
    "openai/gpt-4.1-mini":      {"text","json","code","tools"},
    "openai/gpt-4o":            {"text","json","code","reasoning","tools","long_context"},
    "openai/gpt-4.1":           {"text","json","code","reasoning","tools","long_context"},
    "openai/o3-mini":           {"text","json","code","reasoning","tools"},
    # o1-mini: owner-gated — not in ALL_CANDIDATES auto-routing
    # ── Anthropic — paid escalation ────────────────────────────────────────
    "anthropic/claude-haiku-4-5":  {"text","json","code","reasoning","tools"},
    "anthropic/claude-sonnet-4-5": {"text","json","code","reasoning","tools","long_context"},
    "anthropic/claude-opus-4-5":   {"text","json","code","reasoning","tools","long_context","critical"},
}

# ── Cost table (USD per 1M tokens in/out) ─────────────────────────────
COST_TABLE = {
    "groq":       (0.00, 0.00),
    "cohere":     (0.00, 0.00),
    "openrouter": (0.00, 0.00),
    "cerebras":   (0.00, 0.00),
    "nvidia":     (0.00, 0.00),
    "mistral":    (0.27, 0.27),
    "ollama":     (0.00, 0.00),
    # OpenAI tiers — USD per 1M tokens (input, output)
    "openai_4omini":   (0.15, 0.60),    # TIER 3 — gpt-4o-mini
    "openai_4dot1mini":(0.40, 1.60),    # TIER 3 — gpt-4.1-mini
    "openai_4o":       (2.50, 10.00),   # TIER 4 — gpt-4o
    "openai_4dot1":    (2.00,  8.00),   # TIER 4 — gpt-4.1
    "openai_o3mini":   (1.10,  4.40),   # TIER 4 — o3-mini (medium reasoning)
    "openai_o1mini":   (3.00, 12.00),   # TIER 5 — owner-gated
    # Anthropic tiers
    "anthropic_haiku":  (0.80, 4.00),
    "anthropic_sonnet": (3.00, 15.00),
    "anthropic_opus":   (15.00, 75.00),
}

FREE_PROVIDERS = {"cohere","openrouter","cerebras","nvidia","ollama"}
# Groq: API returned 403 on 2026-08-28 test — cost UNVERIFIED, removed from free pool.
# Circuit breaker handles Groq failures. Re-add after billing status confirmed.
UNVERIFIED_COST_PROVIDERS = {"groq"}   # claimed free, not confirmed — scored 0.4 (below confirmed-free 1.0)
# OpenAI is NOT in FREE_PROVIDERS — always scored with cost penalty
OPENAI_TIER3_MODELS = {"gpt-4o-mini", "gpt-4.1-mini", "gpt-4.1-nano"}  # low-cost paid
OPENAI_TIER4_MODELS = {"gpt-4o", "gpt-4.1", "o3-mini"}                  # premium paid

# ── Scoring weights (tunable) ─────────────────────────────────────────
SCORE_WEIGHTS = {
    "task_fit":    0.30,   # Can the model handle this task?
    "quality":     0.20,   # Historical quality score
    "cost":        0.20,   # 1.0 for free, 0.0 for expensive
    "reliability": 0.15,   # Recent success rate
    "latency":     0.10,   # Normalized (lower=better)
    "quota":       0.05,   # Headroom remaining
}

# ── Default provider candidates (ordered by economic preference) ──────
ALL_CANDIDATES = [
    # Free-tier fast
    ("groq",     "llama-3.1-8b",             "/v1/messages"),
    ("groq",     "llama-3.3-70b",            "/v1/messages"),
    ("cohere",   "command-r7b",              "/v1/messages"),
    ("cohere",   "command-r",               "/v1/messages"),
    ("cohere",   "command-r-plus",          "/v1/messages"),
    ("openrouter","north-mini-code",         "/v1/messages"),
    ("openrouter","nemotron-3-nano-30b-a3b", "/v1/messages"),
    ("openrouter","nemotron-3-super-120b-a12b","/v1/messages"),
    ("openrouter","gpt-oss-20b",            "/v1/messages"),
    ("cerebras", "zai-glm-4.7",             "/v1/messages"),
    ("nvidia",   "llama-3.1-nemotron-ultra", "/v1/messages"),
    # TIER 3 — Low-cost paid
    ("mistral",  "mistral-medium-3",        "/v1/messages"),
    ("openai",   "gpt-4o-mini",             "openai"),    # $0.15/$0.60 per 1M
    ("openai",   "gpt-4.1-mini",            "openai"),    # $0.40/$1.60 per 1M
    # Local (free, slow — fallback)
    ("ollama",   "qwen2.5:3b",              "ollama"),
    ("ollama",   "qwen2.5:1.5b",           "ollama"),
    # TIER 4 — Premium paid (OpenAI + Anthropic compete via scoring)
    ("openai",   "gpt-4o",                  "openai"),    # $2.50/$10 per 1M
    ("openai",   "gpt-4.1",                 "openai"),    # $2.00/$8 per 1M
    ("openai",   "o3-mini",                 "openai"),    # $1.10/$4.40 reasoning
    ("anthropic","claude-haiku-4-5",        "anthropic"),
    ("anthropic","claude-sonnet-4-5",       "anthropic"),
    # o1-mini excluded from auto-routing — owner-gated TIER 5
]

# ── State management ──────────────────────────────────────────────────
class RouterState:
    """Persists provider health, success rates, and circuit breaker state."""
    def __init__(self):
        self._state = self._load()

    def _load(self):
        try:
            if ROUTER_STATE_FILE.exists():
                return json.loads(ROUTER_STATE_FILE.read_text())
        except: pass
        return {"providers":{}, "version":1}

    def _save(self):
        try: ROUTER_STATE_FILE.write_text(json.dumps(self._state, indent=2))
        except: pass

    def get_provider(self, key):
        return self._state["providers"].setdefault(key, {
            "success_count":0, "failure_count":0, "total_calls":0,
            "avg_latency_ms":1000, "circuit_state":"HEALTHY",
            "consecutive_failures":0, "quarantine_until":None,
            "last_success":None, "last_failure":None,
            "quality_scores":[], "avg_quality":0.7,
        })

    def record_success(self, key, latency_ms, quality=0.8):
        p = self.get_provider(key)
        p["success_count"] += 1; p["total_calls"] += 1
        p["consecutive_failures"] = 0
        # EMA latency
        p["avg_latency_ms"] = int(0.7 * p["avg_latency_ms"] + 0.3 * latency_ms)
        p["quality_scores"] = (p["quality_scores"] + [quality])[-20:]
        p["avg_quality"] = sum(p["quality_scores"]) / len(p["quality_scores"])
        p["last_success"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        if p["circuit_state"] != "HEALTHY":
            p["circuit_state"] = "HEALTHY"
            log.info(f"[circuit] {key}: RETEST→HEALTHY")
        self._save()

    def record_failure(self, key, reason=""):
        p = self.get_provider(key)
        p["failure_count"] += 1; p["total_calls"] += 1
        p["consecutive_failures"] += 1
        p["last_failure"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        if p["circuit_state"] == "HEALTHY" and p["consecutive_failures"] >= 2:
            p["circuit_state"] = "DEGRADED"
            log.warning(f"[circuit] {key}: HEALTHY→DEGRADED")
        elif p["circuit_state"] == "DEGRADED" and p["consecutive_failures"] >= 4:
            p["circuit_state"] = "QUARANTINED"
            p["quarantine_until"] = (datetime.datetime.now(datetime.timezone.utc) +
                                     datetime.timedelta(minutes=5)).isoformat()
            log.warning(f"[circuit] {key}: DEGRADED→QUARANTINED (5min)")
        self._save()

    def is_healthy(self, key):
        p = self.get_provider(key)
        if p["circuit_state"] == "QUARANTINED":
            q_until = p.get("quarantine_until")
            if q_until:
                now = datetime.datetime.now(datetime.timezone.utc)
                q_dt = datetime.datetime.fromisoformat(q_until)
                if now >= q_dt:
                    p["circuit_state"] = "RETEST"
                    p["consecutive_failures"] = 0
                    log.info(f"[circuit] {key}: QUARANTINED→RETEST (cooldown expired)")
                    self._save()
                    return True  # Allow one retest attempt
            return False
        return True

    def success_rate(self, key):
        p = self.get_provider(key)
        total = p["total_calls"]
        if total == 0: return 0.75  # Prior: assume decent
        return p["success_count"] / total

# Global state instance
_state = RouterState()

# ── Scoring engine ────────────────────────────────────────────────────
def score_candidate(provider, model, task_type, has_tools=False):
    """Score a provider/model for a given task. Higher = better."""
    key = f"{provider}/{model}"
    prov_caps = PROVIDER_CAPS.get(key, {"text"})
    req_caps  = TASK_CAPS.get(task_type, {"text"})
    if has_tools: req_caps = req_caps | {"tools"}

    # Task fit: does provider have all required capabilities?
    if not req_caps.issubset(prov_caps):
        return -1.0  # Cannot do this task

    p = _state.get_provider(key)

    # Circuit breaker
    if not _state.is_healthy(key):
        return -1.0

    # Cost score: 1.0 for confirmed-free, 0.4 for unverified-cost, scaled for paid
    if provider in FREE_PROVIDERS:
        cost_score = 1.0
    elif provider in UNVERIFIED_COST_PROVIDERS:
        cost_score = 0.4   # below confirmed-free (1.0), above paid tiers
    elif provider == "openai":
        # OpenAI cost scores calibrated against actual $/1M pricing
        # gpt-4o-mini $0.15/$0.60 < haiku $0.80/$4.00 < gpt-4o $2.50/$10
        if "4o-mini" in model:
            cost_score = 0.38   # cheapest paid tier — below Haiku price
        elif "4.1-mini" in model or "4.1-nano" in model:
            cost_score = 0.30   # slightly more than gpt-4o-mini, similar to haiku
        elif "o3-mini" in model:
            cost_score = 0.18   # reasoning: $1.10 input
        elif "4.1" in model:
            cost_score = 0.12   # $2.00 input
        else:
            cost_score = 0.10   # gpt-4o: $2.50 input
    elif "haiku" in model:
        cost_score = 0.28  # haiku $0.80/$4.00 — more expensive than gpt-4o-mini
    elif "sonnet" in model:
        cost_score = 0.12
    else:
        cost_score = 0.05  # opus/expensive

    # Quality score from history
    quality_score = p.get("avg_quality", 0.7)

    # Reliability score
    reliability_score = _state.success_rate(key)

    # Latency score: normalize against 2000ms baseline (lower=better)
    lat = p.get("avg_latency_ms", 1000)
    latency_score = max(0, 1.0 - lat / 5000)

    # Quota score (simplified — assume 1.0 unless circuit degraded)
    quota_score = 0.5 if p.get("circuit_state") == "DEGRADED" else 1.0

    # Task fit score: 1.0 if all caps present, bonus for extra caps
    extra_caps = len(prov_caps - req_caps)
    task_fit_score = min(1.0, 0.8 + extra_caps * 0.05)

    total = (SCORE_WEIGHTS["task_fit"]    * task_fit_score +
             SCORE_WEIGHTS["quality"]     * quality_score +
             SCORE_WEIGHTS["cost"]        * cost_score +
             SCORE_WEIGHTS["reliability"] * reliability_score +
             SCORE_WEIGHTS["latency"]     * latency_score +
             SCORE_WEIGHTS["quota"]       * quota_score)

    return round(total, 4)

def rank_candidates(task_type, has_tools=False, exclude_paid=False):
    """Return candidates sorted by score descending."""
    scored = []
    for provider, model, endpoint in ALL_CANDIDATES:
        if exclude_paid and provider == "anthropic": continue
        s = score_candidate(provider, model, task_type, has_tools)
        if s >= 0:
            scored.append((s, provider, model, endpoint))
    scored.sort(key=lambda x: -x[0])
    return [(p, m, e) for _, p, m, e in scored]

# ── Execution layer ───────────────────────────────────────────────────
def _fw_key():
    env = HOME / ".openclaw/repos/free_llm_router/installed/Free-Way/.env"
    for l in env.read_text(errors="ignore").splitlines():
        if l.startswith("FREEWAY_API_KEY="):
            return l.split("=",1)[1].strip()
    return os.environ.get("FREEWAY_API_KEY","open-empire-local")

def _anthropic_key():
    env = HOME / ".openclaw/secrets/.env"
    for l in env.read_text(errors="ignore").splitlines():
        if l.startswith("ANTHROPIC_API_KEY="):
            return l.split("=",1)[1].strip()
    return os.environ.get("ANTHROPIC_API_KEY","")

def call_freeway(model, messages, system, max_tokens, tools=None):
    """Call any provider via Free-Way /v1/messages bridge."""
    key = _fw_key()
    body = {"model":model,"max_tokens":max_tokens,"messages":messages}
    if system: body["system"] = system
    if tools:  body["tools"] = tools
    data = json.dumps(body).encode()
    req = urllib.request.Request(f"{FW_BASE}/v1/messages", data=data, method="POST",
          headers={"x-api-key":key,"anthropic-version":"2023-06-01","Content-Type":"application/json"})
    t0 = time.time()
    r = urllib.request.urlopen(req, timeout=30)
    d = json.loads(r.read())
    lat = int((time.time()-t0)*1000)
    if "error" in d:
        raise RuntimeError(d["error"].get("message",str(d["error"]))[:120])
    content_arr = d.get("content",[])
    text = next((c.get("text","") for c in content_arr if c.get("type")=="text"),"")
    if not text and not any(c.get("type")=="tool_use" for c in content_arr):
        raise RuntimeError("Empty response content")
    usage = d.get("usage",{})
    return {"text":text,"full_content":content_arr,"stop_reason":d.get("stop_reason","end_turn"),
            "in_tok":usage.get("input_tokens",0),"out_tok":usage.get("output_tokens",0),"lat":lat}

def call_ollama(model, messages, system, max_tokens):
    """Call local Ollama instance."""
    prompt_parts = []
    if system: prompt_parts.append(f"System: {system}")
    for m in messages:
        role = m.get("role","user")
        content = m.get("content","")
        if isinstance(content, list):
            content = " ".join(c.get("text","") for c in content if c.get("type")=="text")
        prompt_parts.append(f"{role.capitalize()}: {content}")
    prompt = "\n".join(prompt_parts)
    body = json.dumps({"model":model,"prompt":prompt,"stream":False,"options":{"num_predict":max_tokens}}).encode()
    req = urllib.request.Request("http://127.0.0.1:11434/api/generate", data=body, method="POST",
          headers={"Content-Type":"application/json"})
    t0 = time.time()
    r = urllib.request.urlopen(req, timeout=30)
    d = json.loads(r.read()); lat = int((time.time()-t0)*1000)
    text = d.get("response","")
    if not text.strip(): raise RuntimeError("Empty Ollama response")
    return {"text":text,"full_content":[{"type":"text","text":text}],"stop_reason":"end_turn",
            "in_tok":d.get("prompt_eval_count",0),"out_tok":d.get("eval_count",0),"lat":lat}

def call_anthropic_direct(model, messages, system, max_tokens, tools=None):
    """Call Anthropic API directly. Logged as premium."""
    key = _anthropic_key()
    if not key: raise RuntimeError("ANTHROPIC_API_KEY not configured")
    body = {"model":model,"max_tokens":max_tokens,"messages":messages}
    if system: body["system"] = system
    if tools:  body["tools"] = tools
    data = json.dumps(body).encode()
    req = urllib.request.Request("https://api.anthropic.com/v1/messages", data=data, method="POST",
          headers={"x-api-key":key,"anthropic-version":"2023-06-01","Content-Type":"application/json"})
    t0 = time.time()
    r = urllib.request.urlopen(req, timeout=60)
    d = json.loads(r.read()); lat = int((time.time()-t0)*1000)
    content_arr = d.get("content",[])
    text = next((c.get("text","") for c in content_arr if c.get("type")=="text"),"")
    usage = d.get("usage",{})
    return {"text":text,"full_content":content_arr,"stop_reason":d.get("stop_reason","end_turn"),
            "in_tok":usage.get("input_tokens",0),"out_tok":usage.get("output_tokens",0),"lat":lat}

def _openai_key():
    """Read OpenAI key from canonical secrets. Never logged or printed."""
    env_file = HOME / ".openclaw/secrets/.env"
    for l in env_file.read_text(errors="ignore").splitlines():
        l = l.strip()
        if l.startswith("OPENAI_API_KEY="):
            return l.split("=",1)[1].strip().strip('"').strip("'")
    return os.environ.get("OPENAI_API_KEY","")


def call_openai_direct(model, messages, system, max_tokens, tools=None):
    """
    Call OpenAI API directly. TIER 3/4 placement — never called over free/zero paths.
    Supports Anthropic-to-OpenAI message format conversion.
    Key loaded from ~/.openclaw/secrets/.env — never logged.
    """
    key = _openai_key()
    if not key:
        raise RuntimeError("OPENAI_API_KEY not configured in ~/.openclaw/secrets/.env")

    # Convert Anthropic-style messages to OpenAI format
    oai_messages = []
    if system:
        oai_messages.append({"role": "system", "content": system})
    for m in messages:
        content = m.get("content", "")
        if isinstance(content, list):
            content = " ".join(c.get("text","") for c in content if c.get("type")=="text")
        oai_messages.append({"role": m.get("role","user"), "content": content})

    body = {"model": model, "messages": oai_messages, "max_tokens": max_tokens}

    if tools:
        oai_tools = []
        for t in tools:
            oai_tools.append({
                "type": "function",
                "function": {
                    "name":        t.get("name",""),
                    "description": t.get("description",""),
                    "parameters":  t.get("input_schema", {}),
                }
            })
        body["tools"] = oai_tools
        body["tool_choice"] = "auto"

    data = json.dumps(body).encode()
    # Authorization header is not logged anywhere
    req  = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=data, method="POST",
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type":  "application/json",
        }
    )
    t0 = time.time()
    r  = urllib.request.urlopen(req, timeout=60)
    d  = json.loads(r.read())
    lat = int((time.time()-t0)*1000)

    if "error" in d:
        raise RuntimeError(d["error"].get("message", str(d["error"]))[:120])

    choice = d.get("choices",[{}])[0]
    text   = choice.get("message",{}).get("content","") or ""
    stop_r = choice.get("finish_reason","stop")
    usage  = d.get("usage",{})

    # Normalize stop_reason to Anthropic convention
    stop_map = {"stop":"end_turn","length":"max_tokens","tool_calls":"tool_use"}
    stop_r   = stop_map.get(stop_r, stop_r)

    # Handle tool calls (convert OAI → Anthropic content format)
    tool_calls  = choice.get("message",{}).get("tool_calls",[])
    full_content = ([{"type":"text","text":text}] if text else [])
    for tc in tool_calls:
        try:
            full_content.append({
                "type":  "tool_use",
                "id":    tc.get("id",""),
                "name":  tc.get("function",{}).get("name",""),
                "input": json.loads(tc.get("function",{}).get("arguments","{}") or "{}"),
            })
        except Exception:
            pass

    if not text and not tool_calls:
        raise RuntimeError("Empty OpenAI response")

    return {
        "text":         text,
        "full_content": full_content,
        "stop_reason":  stop_r,
        "in_tok":       usage.get("prompt_tokens",0),
        "out_tok":      usage.get("completion_tokens",0),
        "lat":          lat,
    }


def _estimate_cost(provider, model, in_tok, out_tok):
    if provider in FREE_PROVIDERS: return 0.0
    if provider == "openai":
        if "o1-mini" in model:          tier = "openai_o1mini"
        elif "o3-mini" in model:        tier = "openai_o3mini"
        elif "4o-mini" in model:        tier = "openai_4omini"
        elif "4.1-mini" in model or "4.1-nano" in model: tier = "openai_4dot1mini"
        elif "4.1" in model:            tier = "openai_4dot1"
        else:                           tier = "openai_4o"
    elif "haiku"  in model:            tier = "anthropic_haiku"
    elif "opus"   in model:            tier = "anthropic_opus"
    else:                               tier = "anthropic_sonnet"
    inp, out = COST_TABLE.get(tier, (3.00, 15.00))
    return (in_tok * inp + out_tok * out) / 1_000_000

def _telemetry(entry):
    try:
        with open(TELEMETRY_FILE, "a") as f:
            f.write(json.dumps(entry, default=str) + "\n")
    except: pass

# ── Main adaptive routing function ────────────────────────────────────
def route(task_type, messages, system, max_tokens, tools=None,
          force_paid=False, context_label=""):
    """
    Route a request to the best available provider for the task.
    Returns: {"text","provider","model","cost_usd","latency_ms","attempts","is_premium","success"}
    """
    has_tools = bool(tools)
    is_premium = False
    attempts = []
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()

    # Tool-use: only providers with "tools" capability (Anthropic)
    if has_tools:
        candidates = [("anthropic","claude-sonnet-4-5","anthropic")]
        log.info(f"[adaptive] tool-use → Anthropic (schema-safe)")
    elif force_paid:
        candidates = [("anthropic","claude-sonnet-4-5","anthropic")]
    else:
        candidates = rank_candidates(task_type, has_tools=False)

    for provider, model, endpoint in candidates:
        key = f"{provider}/{model}"
        t0  = time.time()
        try:
            if endpoint == "anthropic" or provider == "anthropic":
                res = call_anthropic_direct(model, messages, system, max_tokens, tools)
                is_premium = True
            elif provider == "openai":
                res = call_openai_direct(model, messages, system, max_tokens, tools)
                is_premium = True   # tracked separately from Anthropic in telemetry
            elif endpoint == "ollama" or provider == "ollama":
                res = call_ollama(model, messages, system, max_tokens)
            else:
                res = call_freeway(model, messages, system, max_tokens, tools)

            lat  = int((time.time()-t0)*1000)
            cost = _estimate_cost(provider, model, res["in_tok"], res["out_tok"])
            _state.record_success(key, lat)
            attempts.append({"provider":provider,"model":model,"success":True,"lat":lat,"cost":cost})
            log.info(f"[adaptive] {task_type} → {provider}/{model} {lat}ms ${cost:.5f}")

            _telemetry({"ts":ts,"task_type":task_type,"provider":provider,"model":model,
                        "is_premium":is_premium,"latency_ms":lat,"cost_usd":cost,
                        "success":True,"prior_attempts":len(attempts)-1,"context":context_label})

            return {"text":res["text"],"full_content":res.get("full_content",[]),
                    "stop_reason":res.get("stop_reason","end_turn"),
                    "provider":provider,"model":model,"cost_usd":cost,
                    "latency_ms":lat,"attempts":attempts,"is_premium":is_premium,
                    "in_tok":res["in_tok"],"out_tok":res["out_tok"],"success":True}

        except Exception as e:
            lat = int((time.time()-t0)*1000)
            _state.record_failure(key, str(e)[:80])
            attempts.append({"provider":provider,"model":model,"success":False,
                             "error":str(e)[:80],"lat":lat})
            log.warning(f"[adaptive] {provider}/{model} FAIL: {e}")

    # All candidates failed
    _telemetry({"ts":ts,"task_type":task_type,"provider":None,"model":None,
                "is_premium":False,"success":False,"prior_attempts":len(attempts),
                "error":"all_candidates_failed","context":context_label})
    return {"text":"","success":False,"error":"all_candidates_failed",
            "attempts":attempts,"is_premium":False,"cost_usd":0.0}

def get_provider_summary():
    """Return provider health summary (no key values)."""
    summary = []
    for provider, model, _ in ALL_CANDIDATES:
        key = f"{provider}/{model}"
        p   = _state.get_provider(key)
        summary.append({
            "key":    key,
            "provider": provider,
            "model":  model,
            "circuit_state": p.get("circuit_state","HEALTHY"),
            "success_rate": round(_state.success_rate(key), 3),
            "avg_latency_ms": p.get("avg_latency_ms",1000),
            "total_calls": p.get("total_calls",0),
            "is_free": provider in FREE_PROVIDERS,
        })
    return summary

if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    task = sys.argv[1] if len(sys.argv) > 1 else "general"
    prompt = sys.argv[2] if len(sys.argv) > 2 else "Say: ADAPTIVE_OK"
    result = route(task, [{"role":"user","content":prompt}], "", 60)
    print(json.dumps({k:v for k,v in result.items() if k not in ("full_content","attempts")}, indent=2))
    print("Attempts:", result.get("attempts",[]))
