# Premium Escalation Policy — Open Empire
**Date:** 2026-08-09 | **Authority:** Nathan Asiegbu | **Governance:** V1

---

## When Premium Is Allowed

Premium inference (Anthropic Haiku/Sonnet/Opus, OpenAI) may only be used when **at least one** of the following is true:

| Condition | Allowed Premium Tier |
|---|---|
| All free/local tiers failed (≥2 attempts) | Haiku minimum |
| Task class = `SIGNAL_SCORE` (CashClaw confidence-critical) | Haiku (always) |
| Task class = `HIGH_STAKES` and governance flag set | Sonnet |
| Task class = `ARCHITECTURE` and lower tiers produced poor quality | Sonnet |
| Nathan explicitly selects model via `--model` or direct escalation flag | Any |
| Daily emergency mode — all escalation blocked | BLOCKED |

## OE Proxy Model Mapping

| Requested Model | First Route | Second Route | Premium Fallback |
|---|---|---|---|
| claude-haiku-* | Groq llama-3.1-8b | Cohere command-r7b | Anthropic Haiku |
| claude-sonnet-* | Groq llama-3.3-70b | command-r-plus / nemotron | Anthropic Sonnet |
| claude-opus-* | Anthropic Opus DIRECT | — | — |

## Every Premium Escalation Records

```json
{
  "ts": "ISO8601",
  "original_model": "claude-sonnet-4-5",
  "routed_provider": "anthropic",
  "routed_model": "claude-sonnet-4-5",
  "is_premium": true,
  "prior_failures": 2,
  "escalation_reason": "prior_failures",
  "in_tokens": N,
  "out_tokens": N,
  "cost_usd": 0.00450,
  "agent": "optional",
  "task_type": "optional",
  "venture": "optional"
}
```

Log file: `~/.openclaw/logs/oe_proxy_calls.jsonl`

## Budget Gates

| Threshold | Action |
|---|---|
| Daily spend ≥ $0.10 | Soft alert → Telegram |
| Daily spend ≥ $0.20 | Hard block Sonnet+ → Haiku only |
| Daily spend ≥ $0.50 | Emergency → block ALL non-free inference |
| Monthly spend ≥ $3.00 | Warning alert |

## What Cannot Escalate

- CashClaw trading logic calls → governed separately, always Haiku → never Sonnet without explicit override
- Heartbeat / monitoring → Groq/Ollama only, never premium
- Bulk summarization → free tier always, no escalation
- Routine PMO / agent coordination → free tier

## Audit

- All calls logged to `~/.openclaw/logs/oe_proxy_calls.jsonl`
- Economic guard runs every 5 min → `~/.openclaw/grafana/data/economic_guard.json`
- KG cost_records table tracks per-model spend
- Dashboard: http://127.0.0.1:3001 (FCC Cost Dashboard)
