# Headroom Fit Assessment
**C0.8 | Generated:** 2026-08-09 | **Agent:** Research Agent A  
**Repo:** `headroomlabs-ai/headroom` | **Last verified:** 2026-08-09

---

## Headroom At a Glance

| Attribute | Value |
|---|---|
| License | Apache 2.0 |
| PyPI package | `headroom-ai` |
| npm package | `headroom-ai` (TypeScript SDK only, no CLI) |
| Python requirement | 3.10+ (we have 3.14 ✓) |
| Maintenance state | **Actively maintained** — CI badges live, changelogs current, TrendShift trending |
| OpenClaw support | **Native** — `headroom wrap openclaw` installs as ContextEngine plugin |
| CI | GitHub Actions passing |

---

## What Headroom Does

Headroom is a **context compression layer for AI agents**. It compresses everything an AI agent reads — tool outputs, logs, RAG chunks, files, conversation history — before it reaches the LLM. Same answers, fraction of the tokens.

### Architecture

```
Your agent (Claude Code, OpenClaw, Cursor…)
        │   prompts · tool outputs · logs · RAG results · files
        ▼
┌────────────────────────────────────────────────────┐
│  Headroom   (runs locally — your data stays here)  │
│  ────────────────────────────────────────────────  │
│  CacheAligner  →  ContentRouter  →  CCR            │
│                    ├─ SmartCrusher   (JSON)        │
│                    ├─ CodeCompressor (AST)         │
│                    └─ Kompress-v2-base (text, HF)  │
│                                                    │
│  Cross-agent memory  ·  headroom learn  ·  MCP     │
└────────────────────────────────────────────────────┘
        │   compressed prompt  +  retrieval tool
        ▼
LLM provider  (via Free-Way port 8082 / Anthropic / OpenAI)
```

### Five Deployment Modes

1. **Library** — `compress(messages)` inline in Python or TypeScript app
2. **Proxy** — `headroom proxy --port 8787`, zero code changes, any language
3. **Agent wrap** — `headroom wrap openclaw` (native support!) installs as ContextEngine plugin
4. **MCP server** — `headroom_compress`, `headroom_retrieve`, `headroom_stats`
5. **Inline** — `withHeadroom(new Anthropic())` / `withHeadroom(new OpenAI())`

### Compression Components

| Component | Target | Real-World Savings |
|---|---|---|
| SmartCrusher | JSON (tool outputs, API responses) | 60–95% |
| CodeCompressor | Source code (AST-based) | 47% |
| Kompress-v2-base | Natural language text (HuggingFace model) | 73–92% |
| CacheAligner | Detects KV-cache-busting volatile content | Preserves cache hits |

### Proven Benchmarks

| Workload | Before | After | Savings |
|---|---|---|---|
| Code search (100 results) | 17,765 tokens | 1,408 tokens | **92%** |
| SRE incident debugging | 65,694 tokens | 5,118 tokens | **92%** |
| GitHub issue triage | 54,174 tokens | 14,761 tokens | **73%** |
| Codebase exploration | 78,502 tokens | 41,254 tokens | **47%** |
| Accuracy (GSM8K) | 0.870 | 0.870 | **±0 loss** |
| Accuracy (TruthfulQA) | 0.530 | 0.560 | **+0.030 gain** |
| Tool calling (BFCL) | — | 97% at 32% compression | Preserved |

### Additional Features

- **Reversible (CCR)** — originals cached locally; LLM can retrieve on demand
- **Cross-agent memory** — shared store across Claude, Codex, Gemini, Grok, auto-dedup
- **`headroom learn`** — mines failed sessions, writes corrections to `AGENTS.md` / `CLAUDE.md`
- **Output token reduction** — trims model responses (verbosity steering + effort routing)
- **`headroom output-savings`** — reports measured/estimated output token savings
- **CacheAligner** — warns about volatile content that busts provider KV cache prefixes

---

## What We Already Have vs What Headroom Adds

| Capability | Open Empire Current | Headroom Adds |
|---|---|---|
| Multi-provider routing | ✅ Free-Way FCC (5 providers) | No change to routing |
| Token compression | ❌ None | ✅ 15-95% on compressible types |
| JSON data compression | ❌ None | ✅ SmartCrusher 60-95% |
| Code compression | ❌ None | ✅ CodeCompressor 47% |
| Context reversal | ❌ None | ✅ CCR reversible cache |
| Cross-agent memory | ❌ Siloed per agent | ✅ Shared store (Claude, Codex, Gemini, Grok) |
| KV cache preservation | ❌ No awareness | ✅ CacheAligner |
| Output token trimming | ❌ None | ✅ Verbosity steering + effort routing |
| AGENTS.md learning | ❌ Manual | ✅ `headroom learn` auto-mines sessions |
| OpenClaw ContextEngine | ❌ Empty | ✅ `headroom wrap openclaw` installs natively |

---

## Open Empire-Specific Fit Analysis

### Where Headroom Delivers Real Value

**1. Market Scanner Outputs (Kalshi/Polymarket)**  
JSON API responses from market_scanner.py are prime SmartCrusher targets. A 65K-token incident log → 5K tokens (92%) pattern maps directly to Kalshi event list + orderbook snapshots passed to signal_engine.py.

**2. AGENTS.md Auto-Learning**  
`headroom learn` mines failed sessions and writes corrections to `AGENTS.md`. This is directly applicable — failed cashclaw_director cycles, arb false positives, failed Polymarket signals could auto-feed institutional memory.

**3. OpenClaw Native Integration**  
Headroom explicitly lists OpenClaw in its agent compatibility matrix with `headroom wrap openclaw` installing as a ContextEngine plugin. This is the cleanest deployment path — no proxy rewiring, no port changes.

**4. KV Cache Alignment**  
CacheAligner detects volatile content (timestamps, live prices, session IDs) that would bust provider KV cache prefixes. Our governance prompts (reused across every trading cycle) benefit most from this.

**5. Cross-Agent Memory**  
Shared memory across cashclaw_director, arb, polymarket_trader, and sentinel agents would allow institutional state (e.g., "Kalshi weather markets unreliable Tuesdays") to propagate without manual AGENTS.md edits.

### Risks and Constraints

| Risk | Severity | Mitigation |
|---|---|---|
| Additional proxy layer (headroom:8787 → FCC:8082 → provider) | Medium | Use `headroom wrap openclaw` (ContextEngine plugin) instead of proxy mode — avoids double-proxy |
| Kompress-v2-base model needs local compute | Low | macOS 12 Intel: CPU inference acceptable; MPS not available on macOS 12 (Headroom has `pytorch_mps` extra for macOS 13+) |
| ML dependencies (torch, transformers) for Kompress | Medium | Install with `[all]` but skip `[pytorch-mps]` on macOS 12; fallback to SmartCrusher/CodeCompressor works fine |
| Governance prompt must not be compressed | Low | Explicitly block governance, Kelly, financial schemas from compression via config |
| `headroom learn` writes to AGENTS.md | Medium | Run `--dry-run` mode first; review suggestions before `--apply`; never auto-apply to financial controls section |
| Apache 2.0 license compatibility | None | Compatible with Open Empire's operating model |

---

## macOS 12 Compatibility Check

| Component | macOS 12 Status |
|---|---|
| Python 3.10+ | ✅ (we have 3.14) |
| SmartCrusher (JSON) | ✅ Pure Python |
| CodeCompressor (AST) | ✅ Pure Python |
| Kompress-v2-base (HuggingFace) | ✅ CPU inference, no MPS needed |
| `pytorch_mps` extra | ❌ macOS 13+ only — skip this extra |
| headroom proxy | ✅ |
| `headroom wrap openclaw` | ✅ Explicitly supported |
| `headroom learn` | ✅ |

Install command for macOS 12:
```bash
pip install "headroom-ai[proxy,mcp,ml,code,memory]"
# Omit: pytorch-mps, vector (requires C++ toolchain)
```

---

## Recommended Pilot Plan

### Phase 1: ContextEngine Plugin (Week 1, Zero Risk)
```bash
pip install "headroom-ai[proxy,mcp,ml,code,memory]"
headroom wrap openclaw  # installs as ContextEngine plugin
headroom doctor         # verify routing
```
No proxy change, no port conflict. Compression applies to OpenClaw sessions natively.

### Phase 2: Validate Compression on Market Data (Week 2)
```python
from headroom import compress
# Test on cashclaw_director market scanner outputs
compressed = compress(kalshi_event_list_messages)
# Measure: token count before/after, latency before/after
```
Target: >40% reduction on JSON market data payloads.

### Phase 3: headroom learn on AGENTS.md (Week 3, Manual Review Only)
```bash
headroom learn          # dry-run — preview corrections
# Human reviews suggestions
headroom learn --apply  # only after review, never for financial controls section
```

### Phase 4: Cross-Agent Memory (Week 4, Optional)
Enable shared memory store across director, arb, polymarket_trader. Evaluate whether shared institutional state improves signal quality.

---

## Verdict

```
PILOT
```

**Rationale:**

1. **Native OpenClaw integration** (`headroom wrap openclaw`) makes the install path trivial and non-breaking. No port changes, no gateway rewiring.

2. **Real compression on Open Empire's heaviest data type** — JSON market data from Kalshi/Polymarket APIs is exactly what SmartCrusher is optimized for (60-92% documented savings). On free providers this saves $0 but reduces per-call latency and frees token quota for more complex signal prompts.

3. **`headroom learn` + AGENTS.md** is uniquely valuable for an autonomous multi-agent system — failed trading cycles automatically improve the agent's institutional memory without manual intervention.

4. **Zero dollar cost** on free tier, zero irreversible changes (CCR reversible, wrap is undoable with `headroom unwrap openclaw`).

5. **macOS 12 compatible** with minor install flag changes (skip `pytorch-mps`).

**Blocked if:** Headroom attempts to compress or rewrite governance prompts containing Kelly controls, spend caps, or approval gates. Mitigation: configure compression block-list for these prompt types before enabling.

**Success criteria for promoting to INSTALL:**
- SmartCrusher achieves >30% compression on Kalshi/Polymarket API payloads in 2-week pilot
- No accuracy degradation on signal scoring (measured: same GPT-4o/Haiku confidence outputs)
- `headroom learn` suggestions reviewed and found useful (at least 1 actionable AGENTS.md correction)
- No proxy-related failures in cashclaw_director or arb cycles during pilot period
