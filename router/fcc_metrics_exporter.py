#!/usr/bin/env python3
"""
FCC Metrics Exporter — Open Empire Cost Telemetry
Version: 1.1 | 2026-08-09
Uses only stdlib (urllib) — no pip deps needed.
"""
import os, json, time, datetime, pathlib
from urllib.request import urlopen, Request
from urllib.error import URLError

FREEWAY_BASE = "http://127.0.0.1:8082"
FREEWAY_KEY  = os.environ.get("FREEWAY_API_KEY", "open-empire-local")
OUT_DIR      = pathlib.Path.home() / ".openclaw/grafana/data"
OUT_DIR.mkdir(parents=True, exist_ok=True)

COST_TABLE = {
    "openrouter": (0.00, 0.00),
    "cohere":     (0.00, 0.00),
    "cerebras":   (0.00, 0.00),
    "nvidia":     (0.00, 0.00),
    "mistral":    (0.27, 0.27),
    "groq":       (0.00, 0.00),
    "anthropic":  (3.00, 15.00),
}

def fetch(path):
    req = Request(f"{FREEWAY_BASE}{path}", headers={"x-api-key": FREEWAY_KEY})
    try:
        with urlopen(req, timeout=10) as r:
            return json.loads(r.read())
    except URLError as e:
        print(f"[exporter] WARN fetch {path}: {e}")
        return {}

def cost(provider, in_tok, out_tok):
    inp, out = COST_TABLE.get(provider, (0,0))
    return (in_tok * inp + out_tok * out) / 1_000_000

def run():
    ts      = datetime.datetime.utcnow().isoformat() + "Z"
    ts_ms   = int(time.time() * 1000)
    usage   = fetch("/api/usage")
    catalog = fetch("/api/catalog")

    records = usage.get("records", [])
    active  = [p for p in catalog.get("providers", []) if p.get("available")]

    enriched = []
    for r in records:
        p    = r.get("providerName", "unknown")
        est  = cost(p, r.get("promptTokens", 0), r.get("completionTokens", 0))
        enriched.append({**r, "estimatedCostUsd": round(est, 6)})

    total_calls  = sum(r.get("callCount", 0) for r in records)
    total_tokens = sum(r.get("totalTokens", 0) for r in records)
    total_cost   = sum(r["estimatedCostUsd"] for r in enriched)

    metrics = {
        "timestamp": ts, "epoch": ts_ms,
        "summary": {
            "totalCalls": total_calls,
            "totalTokens": total_tokens,
            "totalCostUsd": round(total_cost, 6),
            "activeProviders": len(active),
        },
        "byModel": enriched,
        "activeProviders": [{"name": p["name"], "modelCount": p.get("modelCount",0)} for p in active],
    }

    (OUT_DIR / "fcc_metrics.json").write_text(json.dumps(metrics, indent=2))

    prom = [
        f"fcc_total_calls {total_calls} {ts_ms}",
        f"fcc_total_tokens {total_tokens} {ts_ms}",
        f"fcc_total_cost_usd {total_cost:.6f} {ts_ms}",
        f"fcc_active_providers {len(active)} {ts_ms}",
    ]
    for r in enriched:
        lbl = f'model="{r["modelId"]}",provider="{r["providerName"]}"'
        prom += [
            f'fcc_model_calls{{{lbl}}} {r["callCount"]} {ts_ms}',
            f'fcc_model_tokens{{{lbl}}} {r["totalTokens"]} {ts_ms}',
            f'fcc_model_cost_usd{{{lbl}}} {r["estimatedCostUsd"]:.6f} {ts_ms}',
        ]
    (OUT_DIR / "fcc_metrics.prom").write_text("\n".join(prom) + "\n")

    print(f"[fcc_exporter] {ts} calls={total_calls} tokens={total_tokens} cost=${total_cost:.4f} providers={len(active)}")

if __name__ == "__main__":
    run()
