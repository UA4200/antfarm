# Open Empire Workspace — Claude Code Context
# Workspace: ~/.openclaw/workspace/ | Host: Ugos-Mac-mini.lan

## This workspace is the Open Empire operating surface.
## Always read ~/.claude/CLAUDE.md first for global rules and CashClaw protection.

## Workspace Structure
```
AGENTS.md          — agent registry and activation rules (authoritative)
MEMORY.md          — user profile, runtime state, top priorities
HEARTBEAT.md       — loop mechanics, model dispatch, circuit breakers
SOUL.md            — operating bias, response shape
IDENTITY.md        — Alusi Chief of Staff identity
GOALS.md           — current goal set
PROJECTS.md        — active project registry
STATUS.md          — auto-generated system status
TOOLS.md           — local tool notes (cameras, SSH, TTS)

antfarm/           — multi-agent workflow engine (UA4200/antfarm)
mission-control/   — Next.js command center (UA4200/mission-control)
skills/            — OpenClaw domain skills
agents/            — agent definitions (council_templates/ etc.)
directives/        — deployment records, phase reports, ops docs
scripts/           — utility scripts
```

## Deployment Records (2026-07-30)
```
directives/PHASE0_REPORT_20260730.md         — host verification
directives/PHASE2_COMPONENT_LEDGER_20260730.md — 25-component ledger
directives/PHASE5_DEPLOYMENT_RECEIPT_20260730.md — SHA map
directives/PHASE6_STABILITY_GATE_20260730.md — stability gate (bypassed)
directives/PHASE7_RELEASE_MANIFEST_20260730.md — release manifest
directives/OPS_SUMMARY_20260730.txt          — ops summary
```

## Git Wiring
- This workspace is git-tracked: git remote = UA4200/git-github
- Staging clones at: ~/.openclaw/staging/<repo>/
- Never `git add` secrets, leads.jsonl, trades.jsonl, *.env files

## OpenClaw Skills in Workspace
The following OpenClaw skills are available and can be loaded:
```
skills/ai-automation-consulting/
skills/auto-job-applier/
skills/blco-commodity-outreach/
skills/humanizer/
skills/marketing-skills/
skills/ml-ops-skill-pack/
skills/multi-search-engine/
skills/obsidian-openclaw-memory/
skills/self-improving-agent/
skills/skill-vetter/
skills/word-docx/
```

## Antfarm Workflows
```bash
# Install a workflow
node ~/workspace/antfarm/dist/cli/cli.js workflow install <name>
# Run a workflow
node ~/workspace/antfarm/dist/cli/cli.js workflow run <id> "<task>"
# Status
node ~/workspace/antfarm/dist/cli/cli.js workflow status "<task>"
```

## Notification Route (for coding-agent completion messages)
- channel: telegram
- target: 6588652716
- Send: openclaw message send --channel telegram --target '6588652716' --message '<result>'
