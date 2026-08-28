#!/usr/bin/env python3
"""
Open Empire Economic Guard — P0.6
Tracks inference spend, enforces daily/monthly budgets, fires alerts.
Reads kg_cost_records from ClawDB + Free-Way usage.
Version: 1.0 | 2026-08-09
"""
import os, json, datetime, subprocess, pathlib, urllib.request

SECRETS_FILE   = pathlib.Path.home() / ".openclaw/secrets/.env"
LOG_FILE       = pathlib.Path.home() / ".openclaw/logs/economic_guard.jsonl"
METRICS_FILE   = pathlib.Path.home() / ".openclaw/grafana/data/economic_guard.json"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
METRICS_FILE.parent.mkdir(parents=True, exist_ok=True)

# ── Budget limits ──────────────────────────────────────────────────────
DAILY_SOFT_USD    = 0.10   # Soft alert — Telegram
DAILY_HARD_USD    = 0.20   # Hard alert — block Sonnet+
DAILY_EMERGENCY   = 0.50   # Emergency — block all non-free model calls
MONTHLY_WARN_USD  = 3.00   # Monthly warning threshold

# ── Cost table (per 1M tokens in/out) ─────────────────────────────────
COST_TABLE = {
    "groq":       (0.00, 0.00),
    "openrouter": (0.00, 0.00),
    "cohere":     (0.00, 0.00),
    "cerebras":   (0.00, 0.00),
    "nvidia":     (0.00, 0.00),
    "mistral":    (0.27, 0.27),
    "anthropic":  (3.00, 15.00),   # Sonnet baseline
    "haiku":      (0.80, 4.00),
    "sonnet":     (3.00, 15.00),
    "opus":       (15.00, 75.00),
    # OpenAI — USD per 1M tokens (input, output)
    "openai_4omini":    (0.15, 0.60),
    "openai_4dot1mini": (0.40, 1.60),
    "openai_4o":        (2.50, 10.00),
    "openai_4dot1":     (2.00, 8.00),
    "openai_o3mini":    (1.10, 4.40),
    "openai_o1mini":    (3.00, 12.00),
}

FREE_PROVIDERS = {"groq","openrouter","cohere","cerebras","nvidia"}

def _db(query):
    r = subprocess.run(["psql","-h","127.0.0.1","-p","5432","-U","NeoOC","-d","clawdb",
                        "-t","-A","-c",query], capture_output=True, text=True, timeout=10)
    return r.stdout.strip() if r.returncode == 0 else ""

def _secrets():
    s = {}
    for l in SECRETS_FILE.read_text(errors="ignore").splitlines():
        l = l.strip()
        if l.startswith("#") or "=" not in l: continue
        k,v = l.split("=",1); s[k.strip()] = v.strip()
    return s

def _fw_usage():
    try:
        sec = _secrets()
        fw_key = _secrets().get("FREEWAY_API_KEY","open-empire-local")
        req = urllib.request.Request("http://127.0.0.1:8082/api/usage",
              headers={"x-api-key": fw_key})
        d = json.loads(urllib.request.urlopen(req, timeout=8).read())
        return d.get("records",[])
    except: return []

def compute_stats():
    """Compute today's + month's spend from KG cost_records + Free-Way usage."""
    now   = datetime.datetime.now(datetime.timezone.utc)
    today = now.date().isoformat()
    month = now.strftime("%Y-%m")

    # From ClawDB kg_cost_records
    day_cost   = _db(f"SELECT COALESCE(SUM(estimated_cost_usd),0) FROM kg_cost_records WHERE DATE(recorded_at)='{today}';")
    month_cost = _db(f"SELECT COALESCE(SUM(estimated_cost_usd),0) FROM kg_cost_records WHERE TO_CHAR(recorded_at,'YYYY-MM')='{month}';")
    day_calls  = _db(f"SELECT COALESCE(COUNT(*),0) FROM kg_cost_records WHERE DATE(recorded_at)='{today}';")
    prem_today = _db(f"SELECT COALESCE(COUNT(*),0) FROM kg_cost_records WHERE DATE(recorded_at)='{today}' AND estimated_cost_usd>0;")
    free_today = _db(f"SELECT COALESCE(COUNT(*),0) FROM kg_cost_records WHERE DATE(recorded_at)='{today}' AND estimated_cost_usd=0;")

    try: day_usd   = float(day_cost or 0)
    except: day_usd = 0.0
    try: month_usd = float(month_cost or 0)
    except: month_usd = 0.0
    try: calls_today = int(day_calls or 0)
    except: calls_today = 0

    # Supplement with Free-Way session usage
    fw_records = _fw_usage()
    fw_calls   = sum(r.get("callCount",0) for r in fw_records)
    fw_tokens  = sum(r.get("totalTokens",0) for r in fw_records)

    # Route analysis
    free_pct = 100.0
    premium_pct = 0.0
    if calls_today > 0:
        try:
            fp = int(free_today or 0); pp = int(prem_today or 0)
            free_pct    = round(fp / calls_today * 100, 1)
            premium_pct = round(pp / calls_today * 100, 1)
        except: pass

    status = "OK"
    alerts = []
    if day_usd >= DAILY_EMERGENCY:
        status = "EMERGENCY"; alerts.append(f"EMERGENCY: Daily AI spend ${day_usd:.3f} >= ${DAILY_EMERGENCY}")
    elif day_usd >= DAILY_HARD_USD:
        status = "HARD_LIMIT"; alerts.append(f"HARD: Daily AI spend ${day_usd:.3f} >= ${DAILY_HARD_USD} — block Sonnet+")
    elif day_usd >= DAILY_SOFT_USD:
        status = "SOFT_ALERT"; alerts.append(f"SOFT: Daily AI spend ${day_usd:.3f} >= ${DAILY_SOFT_USD}")
    if month_usd >= MONTHLY_WARN_USD:
        alerts.append(f"Monthly spend ${month_usd:.2f} >= ${MONTHLY_WARN_USD}")

    result = {
        "ts":                 now.isoformat(),
        "status":             status,
        "alerts":             alerts,
        "today": {
            "date":           today,
            "cost_usd":       round(day_usd, 6),
            "calls":          calls_today,
            "free_pct":       free_pct,
            "premium_pct":    premium_pct,
        },
        "month": {
            "month":          month,
            "cost_usd":       round(month_usd, 4),
        },
        "freeway_session": {
            "calls":          fw_calls,
            "tokens":         fw_tokens,
            "cost_usd":       0.00,
        },
        "limits": {
            "daily_soft":     DAILY_SOFT_USD,
            "daily_hard":     DAILY_HARD_USD,
            "daily_emergency":DAILY_EMERGENCY,
            "monthly_warn":   MONTHLY_WARN_USD,
        }
    }
    return result

def run():
    stats = compute_stats()
    # Write to metrics file (read by Grafana dashboard)
    METRICS_FILE.write_text(json.dumps(stats, indent=2))
    # Append to log
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(stats) + "\n")

    if stats["alerts"]:
        for a in stats["alerts"]:
            print(f"[economic_guard] ALERT: {a}")
    else:
        print(f"[economic_guard] OK | today=${stats['today']['cost_usd']:.4f} | month=${stats['month']['cost_usd']:.4f} | free={stats['today']['free_pct']}%")

    return stats

if __name__ == "__main__":
    import sys
    if "--json" in sys.argv:
        print(json.dumps(run(), indent=2))
    else:
        run()
