#!/usr/bin/env python3
"""
FCC Governed Auto-Selector — Open Empire Cost Router
Version: 1.0 | 2026-08-09
Role: Select cheapest passing provider for any given task type

Usage:
  from fcc_router import route_inference
  result = route_inference(task_type="summarize", prompt="...")

Architecture:
  task_type → model_chain → try in order → first success returned
  Fallback: FCC free → FCC low-cost → Haiku → block (no Sonnet/Opus without explicit escalation)
"""

import os, json, time, requests, logging
from typing import Optional

log = logging.getLogger("fcc_router")

# ── Config ──────────────────────────────────────────────────────────────────
FREEWAY_BASE   = "http://127.0.0.1:8082"
FREEWAY_KEY    = os.environ.get("FREEWAY_API_KEY", "open-empire-local")
ANTHROPIC_KEY  = os.environ.get("ANTHROPIC_API_KEY", "")
ANTHROPIC_BASE = "https://api.anthropic.com"

# Cost tiers per 1M tokens (input / output) — approximate 2026-08
PROVIDER_COST = {
    "freeway_free":  (0.00, 0.00),   # openrouter free, cohere, cerebras, nvidia
    "freeway_paid":  (0.27, 0.27),   # mistral-medium-3
    "haiku":         (0.80, 4.00),   # claude-haiku-4-5
    "sonnet":        (3.00, 15.00),  # claude-sonnet-4-6 — REQUIRES explicit escalation
}

# ── Task → Model chain map ────────────────────────────────────────────────
# Each task type maps to an ordered list of (provider, model, max_tokens)
# Router tries each in order; returns first success.
# NOTE: Groq uses /v1/chat/completions (not /v1/messages). Use model IDs: llama-3.1-8b, llama-3.3-70b
# All other freeway models use /v1/messages (Anthropic bridge)
TASK_CHAINS = {
    "summarize": [
        ("freeway", "command-r7b",             512),
        ("groq",    "llama-3.1-8b",            512),   # fast free fallback
        ("freeway", "nemotron-3-nano-30b-a3b", 512),
    ],
    "classify": [
        ("groq",    "llama-3.1-8b",            128),   # fastest for classification
        ("freeway", "command-r7b",             128),
        ("freeway", "gpt-oss-20b",             128),
    ],
    "codegen": [
        ("freeway", "north-mini-code",         1024),
        ("groq",    "llama-3.3-70b",           1024),  # 70B for complex code
        ("freeway", "nemotron-3-super-120b-a12b", 1024),
    ],
    "code_review": [
        ("freeway", "command-r",               512),
        ("groq",    "llama-3.3-70b",           512),
        ("freeway", "north-mini-code",         512),
    ],
    "draft_email": [
        ("freeway", "command-r-plus",          1024),
        ("groq",    "llama-3.3-70b",           1024),
        ("freeway", "command-r7b",             1024),
    ],
    "heartbeat": [
        ("groq",    "llama-3.1-8b",            64),    # fastest + free
        ("freeway", "command-r7b",             64),
    ],
    "signal_score": [
        # CashClaw — confidence-critical, Haiku primary
        ("haiku",   "claude-haiku-4-5",       256),
        ("freeway", "command-r-plus",          256),   # fallback if Haiku down
    ],
    "analysis": [
        ("groq",    "llama-3.3-70b",           2048),
        ("freeway", "nemotron-3-super-120b-a12b", 2048),
        ("haiku",   "claude-haiku-4-5",       2048),
    ],
    "general": [
        ("groq",    "llama-3.1-8b",            512),
        ("freeway", "command-r7b",             512),
        ("freeway", "gpt-oss-20b",             512),
        ("haiku",   "claude-haiku-4-5",       512),
    ],
}

# ── Core router ──────────────────────────────────────────────────────────────
def route_inference(
    task_type: str,
    prompt: str,
    system: str = "",
    max_tokens: Optional[int] = None,
    escalate_to_sonnet: bool = False,   # must be explicit
) -> dict:
    """
    Route a prompt to the cheapest available provider for the task.
    Returns: { success, provider, model, text, tokens, cost_usd, latency_ms, error }
    """
    chain = TASK_CHAINS.get(task_type, TASK_CHAINS["general"])

    for provider, model, default_max in chain:
        tokens = max_tokens or default_max
        t0 = time.time()
        try:
            if provider == "freeway":
                result = _call_freeway(model, prompt, system, tokens)
            elif provider == "groq":
                result = _call_groq(model, prompt, system, tokens)
            elif provider == "haiku":
                result = _call_anthropic("claude-haiku-4-5", prompt, system, tokens)
            else:
                result = {"success": False, "error": f"Unknown provider: {provider}"}

            latency = int((time.time() - t0) * 1000)
            if result.get("success"):
                cost = _estimate_cost(provider, result.get("input_tokens",0), result.get("output_tokens",0))
                log.info(f"[fcc_router] {task_type} → {provider}/{model} ✓ {latency}ms ${cost:.5f}")
                return {**result, "provider": provider, "model": model,
                        "latency_ms": latency, "cost_usd": cost, "task_type": task_type}
            else:
                log.warning(f"[fcc_router] {task_type} → {provider}/{model} FAIL: {result.get('error','?')}")
        except Exception as e:
            log.error(f"[fcc_router] {task_type} → {provider}/{model} EXCEPTION: {e}")

    # All chain options exhausted
    if escalate_to_sonnet and ANTHROPIC_KEY:
        log.warning(f"[fcc_router] ESCALATING {task_type} to Sonnet — all chain options failed")
        t0 = time.time()
        result = _call_anthropic("claude-sonnet-4-6", prompt, system, max_tokens or 1024)
        latency = int((time.time() - t0) * 1000)
        if result.get("success"):
            cost = _estimate_cost("sonnet", result.get("input_tokens",0), result.get("output_tokens",0))
            return {**result, "provider": "sonnet", "model": "claude-sonnet-4-6",
                    "latency_ms": latency, "cost_usd": cost, "task_type": task_type}

    return {"success": False, "error": "All providers failed", "task_type": task_type,
            "provider": None, "model": None, "text": None, "cost_usd": 0.0}


# ── Provider calls ───────────────────────────────────────────────────────────
def _call_freeway(model: str, prompt: str, system: str, max_tokens: int) -> dict:
    messages = [{"role": "user", "content": prompt}]
    body = {"model": model, "max_tokens": max_tokens, "messages": messages}
    if system:
        body["system"] = system

    r = requests.post(
        f"{FREEWAY_BASE}/v1/messages",
        headers={"x-api-key": FREEWAY_KEY, "anthropic-version": "2023-06-01",
                 "Content-Type": "application/json"},
        json=body,
        timeout=30,
    )
    d = r.json()
    if "error" in d:
        return {"success": False, "error": d["error"].get("message", str(d["error"]))}
    content = d.get("content", [])
    if not content:
        return {"success": False, "error": "Empty content array"}
    text = content[0].get("text", "")
    if not text.strip():
        return {"success": False, "error": "Empty text in response"}
    usage = d.get("usage", {})
    return {"success": True, "text": text,
            "input_tokens": usage.get("input_tokens", 0),
            "output_tokens": usage.get("output_tokens", 0)}


def _call_groq(model: str, prompt: str, system: str, max_tokens: int) -> dict:
    """Call Groq via Free-Way /v1/messages (Anthropic-compat — /v1/chat/completions returns 500)."""
    messages = [{"role": "user", "content": prompt}]
    body = {"model": model, "max_tokens": max_tokens, "messages": messages}
    if system:
        body["system"] = system

    r = requests.post(
        f"{FREEWAY_BASE}/v1/messages",
        headers={"x-api-key": FREEWAY_KEY,
                 "anthropic-version": "2023-06-01",
                 "Content-Type": "application/json"},
        json=body,
        timeout=30,
    )
    d = r.json()
    if "error" in d:
        return {"success": False, "error": d["error"].get("message", str(d["error"]))[:120]}
    content = d.get("content", [])
    if not content:
        return {"success": False, "error": "Empty content array"}
    text = content[0].get("text", "")
    if not text.strip():
        return {"success": False, "error": "Empty text"}
    usage = d.get("usage", {})
    return {"success": True, "text": text,
            "input_tokens": usage.get("input_tokens", 0),
            "output_tokens": usage.get("output_tokens", 0)}


def _call_anthropic(model: str, prompt: str, system: str, max_tokens: int) -> dict:
    if not ANTHROPIC_KEY:
        return {"success": False, "error": "ANTHROPIC_API_KEY not set"}
    messages = [{"role": "user", "content": prompt}]
    body = {"model": model, "max_tokens": max_tokens, "messages": messages}
    if system:
        body["system"] = system

    r = requests.post(
        f"{ANTHROPIC_BASE}/v1/messages",
        headers={"x-api-key": ANTHROPIC_KEY, "anthropic-version": "2023-06-01",
                 "Content-Type": "application/json"},
        json=body,
        timeout=30,
    )
    d = r.json()
    if "error" in d:
        return {"success": False, "error": d["error"].get("message", str(d["error"]))}
    content = d.get("content", [])
    if not content:
        return {"success": False, "error": "Empty content"}
    usage = d.get("usage", {})
    return {"success": True, "text": content[0].get("text",""),
            "input_tokens": usage.get("input_tokens",0),
            "output_tokens": usage.get("output_tokens",0)}


# ── Cost estimate ─────────────────────────────────────────────────────────────
def _estimate_cost(provider: str, in_tok: int, out_tok: int) -> float:
    tier = "freeway_free"
    if provider == "mistral": tier = "freeway_paid"
    elif provider == "haiku":  tier = "haiku"
    elif provider == "sonnet": tier = "sonnet"
    inp, outp = PROVIDER_COST[tier]
    return (in_tok * inp + out_tok * outp) / 1_000_000


# ── CLI test harness ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    task = sys.argv[1] if len(sys.argv) > 1 else "summarize"
    prompt = sys.argv[2] if len(sys.argv) > 2 else "Summarize: Revenue is sales income before expenses."
    result = route_inference(task, prompt)
    print(json.dumps(result, indent=2))
