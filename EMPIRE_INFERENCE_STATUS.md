# Inference Routing Status
*Last updated: 2026-08-09*

Gateway: http://127.0.0.1:4100 (oe-proxy v2, adaptive)
ANTHROPIC_BASE_URL=http://127.0.0.1:4100

## Active Providers (6 free + 1 paid)
- **Groq**: llama-3.1-8b, llama-3.3-70b (4-key pool)
- **OpenRouter**: 17 free models
- **Cohere**: command-r7b, command-r, command-r-plus, command-a
- **Cerebras**: zai-glm-4.7
- **NVIDIA NIM**: llama-3.1-nemotron-ultra
- **Mistral**: mistral-medium-3 (low-cost)
- **Anthropic**: Haiku/Sonnet/Opus (premium, governed)

## Economic Guard
| Threshold | Limit |
|---|---|
| Daily soft | $0.10 |
| Daily hard | $0.20 |
| Daily emergency | $0.50 |

## Routing Logic (oe-proxy)
| Request Model | Routes To |
|---|---|
| claude-haiku-* | Groq free (llama-3.1-8b) |
| claude-sonnet-* | Groq 70B / free |
| claude-opus-* | Anthropic premium |

## Free-Way (FCC)
- Port: 8082 (127.0.0.1 only)
- 72 models across 5 providers
- Cost-optimized inference routing
- Grafana dashboard: http://127.0.0.1:3001 (auto-refresh 30s)
- Metrics exporter: PM2 51 (fcc-metrics-exporter, every 5min)

## Navigation
← [[EMPIRE_HOME]]
