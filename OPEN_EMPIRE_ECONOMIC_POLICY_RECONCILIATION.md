# Open Empire Economic Policy Reconciliation
**Generated:** 2026-08-09T20:30:00Z

## Critical Separation

| Policy Domain | Scope | Thresholds | Controlled By |
|---|---|---|---|
| Inference Telemetry | Non-CashClaw AI inference | $0.10/$0.20/$0.50/day | economic_guard.py |
| Empire Operations | Paid services, subscriptions | Nathan explicit approval | Nathan |
| CashClaw Capital | Kalshi+Polymarket trading | Kelly + $10/day cap | trading agents |
| CashClaw Risk | Signal thresholds, edge requirements | 60% confidence, 5pt edge | hardcoded in agents |

## Key Rule

Inference alert thresholds ($0.10/$0.20/$0.50) **cannot** be interpreted as authorization for financial transactions, capital deployment, or trading decisions.

```json
{
  "generated_at": "2026-08-09T20:30:00Z",
  "purpose": "Explicitly separate inference telemetry thresholds from Empire spending authority",
  "policies": {
    "INFERENCE_TELEMETRY_ALERT_THRESHOLDS": {
      "scope": "Non-CashClaw AI inference only (oe-proxy, fcc_router, economic_guard)",
      "daily_soft_usd": 0.1,
      "daily_hard_usd": 0.2,
      "daily_emergency_usd": 0.5,
      "monthly_warn_usd": 3.0,
      "action_on_soft": "Telegram alert, continue",
      "action_on_hard": "Block Sonnet+, Haiku only",
      "action_on_emergency": "Block all non-free model calls, manual reset",
      "note": "These thresholds apply ONLY to inference spend. They are NOT general financial authorization limits."
    },
    "EMPIRE_OPERATIONAL_BUDGET": {
      "scope": "All non-trading operational expenditure",
      "approval_required": "Nathan explicit for any paid service subscription",
      "current_approved_paid": [
        "Anthropic API (governed escalation)",
        "Mistral (low-cost, in Free-Way pool)"
      ],
      "note": "Small inference alert thresholds do NOT authorize broad financial spending."
    },
    "VENTURE_BUDGETS": {
      "CashClaw": {
        "deployed_capital_usd": 65.19,
        "daily_spend_cap_usd": 10,
        "controlled_by": "CASHCLAW_DAILY_SPEND_CAP_USD env var"
      },
      "BLCO": {
        "budget": "draft-first, zero spend without approval"
      },
      "ADAI": {
        "budget": "zero until revenue",
        "approval": "Nathan per engagement"
      }
    },
    "CASHCLAW_CAPITAL_CONTROLS": {
      "scope": "Kalshi + Polymarket capital ONLY",
      "kelly_criterion": "PROTECTED \u2014 no modification",
      "daily_loss_limit": "enforced in trading agents",
      "per_trade_max": "5% of balance",
      "approval_required": "Nathan explicit for any Kelly or capital limit change",
      "inference_thresholds_do_NOT_override": true
    },
    "CASHCLAW_RISK_CONTROLS": {
      "signal_confidence_threshold": "60%",
      "edge_threshold": "5pts",
      "provider": "Anthropic Haiku ONLY for signal scoring",
      "approval_required": "Nathan explicit for any change"
    }
  },
  "key_rule": "Inference alert thresholds ($0.10/$0.20/$0.50) CANNOT be interpreted as authorization for any financial transaction, capital deployment, or trading decision.",
  "verdict": "ECONOMIC_POLICIES_RECONCILED"
}
```
