# FREE_CLAUDE_CODE_CONFIGURATION_REPORT
**Date:** 2026-08-09  
**Authority:** Nathan Asiegbu — C0.2 Directive  
**Status:** COMPLETE

---

## 1. Canonical Installation

**Project:** Free-Way  
**Path:** `~/.openclaw/repos/free_llm_router/installed/Free-Way`  
**Git Remote:** `https://github.com/GoDiao/Free-Way.git`  
**Commit:** `80af6bd` (main branch, clean)  
**Node.js:** v24.14.0  
**Port:** `127.0.0.1:8082` (loopback only)

Free-Way is an OpenAI-compatible + Anthropic-bridge local proxy that routes `/v1/messages` and `/v1/chat/completions` calls to free/low-cost cloud providers. It was previously installed (2026-07-31) but had fallen offline and was not under PM2.

---

## 2. Issues Found and Fixed

| Issue | Status |
|---|---|
| Free-Way not running (process dead) | ✅ Fixed — PM2 id=48 active |
| PID file malformed (`freeway_pid=37977`) | ✅ Fixed — PID file now contains `7708` |
| No PM2 registration | ✅ Fixed — registered as `freeway` (id=48) |
| PM2 ecosystem CJS parsed-as-script bug | ✅ Fixed — wrapper script `start-freeway.sh` sources .env |
| Provider keys not reaching PM2 daemon | ✅ Fixed — wrapper script handles env sourcing |

---

## 3. Files Created

| File | Purpose |
|---|---|
| `start-freeway.sh` | Launch wrapper — sources `.env`, then `exec node dist/index.js` |
| `ecosystem.freeway.cjs` | Reference config + documentation for restart procedure |

---

## 4. Provider Configuration

No changes to `.env` or provider keys were made. All 5 active providers were already configured:

| Provider | Models | Cost |
|---|---|---|
| OpenRouter | 17 free models | $0 |
| Cohere | 4 models (command-r family) | $0 free tier |
| Cerebras | 2 models (zai-glm-4.7) | $0 free tier |
| NVIDIA NIM | 2 models (nemotron) | $0 free tier |
| Mistral | 1 model (mistral-medium-3) | Low-cost |

**Total available models:** 72 (via /v1/models with auth)  
**Models from active providers:** 24

---

## 5. Auth Configuration

- **Endpoint auth:** `x-api-key: <FREEWAY_API_KEY>` or `Authorization: Bearer <FREEWAY_API_KEY>`
- **Key location:** `~/.openclaw/repos/free_llm_router/installed/Free-Way/.env`
- **Management API:** Requires same key for `/api/models/refresh`, `/api/config/keys`

---

## 6. Recommended Model Routing

| Task | Model | Provider |
|---|---|---|
| Basic prompt/classification | `command-r7b` | cohere |
| Code generation | `north-mini-code` | openrouter |
| Summarization | `nemotron-3-nano-30b-a3b` | openrouter |
| Code review | `command-r` | cohere |
| Long context | `nemotron-3-super-120b-a12b` | openrouter |
| Fast inference | `zai-glm-4.7` | cerebras (quirk: avoid short prompts) |

---

## 7. Known Limitations (from FREE_CLAUDE_CODE.md)

1. Claude Code CLI requires `--model <freeway-model-id>` — cannot use claude-* model names
2. PM2 daemon does not inherit shell env → must use `start-freeway.sh` wrapper
3. `zai-glm-4.7` (cerebras) and `mistral-medium-3` return empty content on very short prompts
4. No streaming mode tested — all tests used non-streaming requests
5. `/api/models/refresh` requires auth header to work

---

## 8. Start/Restart Procedure

```bash
# Preferred: PM2 restart (already registered)
pm2 restart freeway

# From scratch:
cd ~/.openclaw/repos/free_llm_router/installed/Free-Way
pm2 start start-freeway.sh --name freeway --interpreter bash \
  --log ~/.openclaw/hermes/logs/freeway.log \
  --output ~/.openclaw/hermes/logs/freeway.log \
  --error ~/.openclaw/hermes/logs/freeway.err.log \
  --time --max-restarts 5 --restart-delay 3000
pm2 save

# Verify:
curl http://127.0.0.1:8082/health
# → {"status":"ok"}
```

---

## 9. CashClaw Preservation

CashClaw (PM2 ids 38, 39, 40, 41) was not modified. All trading agents remain online.  
Free-Way runs on port 8082 — no conflict with any existing service.  
Anthropic API key remains in main secrets, used directly by OpenClaw — not routed through Free-Way.
