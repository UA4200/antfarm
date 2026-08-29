# Open Empire Workspace — Claude Code Context
# Path: ~/.openclaw/workspace/ | Updated: 2026-08-27

## Read ~/.claude/CLAUDE.md first for global rules, hard stops, and proxy config.

## Workspace Layout
```
AGENTS.md          — agent registry, PM2 IDs (authoritative)
MEMORY.md          — runtime state, priorities, cost rules
HEARTBEAT.md       — loop mechanics, model dispatch, circuit breakers
SOUL.md            — operating bias, response shape
IDENTITY.md        — Alusi identity

antfarm/           — multi-agent workflow engine
mission-control/   — Next.js command center (port 3333)
skills/            — OpenClaw domain skills
agents/            — council_templates/ + agent definitions
reports/           — generated status reports
scripts/           — utility scripts
directives/        — deployment records, phase reports
```

## Antfarm Workflows
```bash
node ~/.openclaw/workspace/antfarm/dist/cli/cli.js workflow install <name>
node ~/.openclaw/workspace/antfarm/dist/cli/cli.js workflow run <id> "<task>"
node ~/.openclaw/workspace/antfarm/dist/cli/cli.js workflow status "<task>"
```

## Git Rules
- Workspace tracked: git remote = UA4200/git-github
- Staging clones: ~/.openclaw/staging/<repo>/
- Never git add: secrets, leads.jsonl, trades.jsonl, *.env, *.log
