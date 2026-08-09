# P0.14 — GitHub MCP Configuration Report

**Date:** 2026-08-09  
**Task:** P0.14 — GitHub MCP Server  
**Status:** ✅ COMPLETE

---

## Summary

Added `github-ua4200` as an MCP server in `~/.claude.json`. A wrapper script pattern is used to inject the GitHub token from `~/.openclaw/secrets/.env` without embedding the raw token value in `~/.claude.json`.

---

## Token Discovery

| Check | Result |
|-------|--------|
| Secrets file | `~/.openclaw/secrets/.env` ✅ Found |
| Token variable | `GITHUB_API_TOKEN` ✅ Present |
| Token format | Redacted from this report |

**Token variable name:** `GITHUB_API_TOKEN`  
**MCP server expected variable:** `GITHUB_PERSONAL_ACCESS_TOKEN`

---

## Security Pattern: Wrapper Script

Rather than embedding the token directly in `~/.claude.json` (which is plaintext and not suitable for secrets), a wrapper script is used:

**Wrapper:** `~/.openclaw/hooks/github_mcp_wrapper.sh`

```bash
#!/bin/bash
# Wrapper sources ~/.openclaw/secrets/.env and maps:
#   GITHUB_API_TOKEN → GITHUB_PERSONAL_ACCESS_TOKEN
# Then runs: npx -y @modelcontextprotocol/server-github
```

The wrapper:
1. Sources `~/.openclaw/secrets/.env` with `set -a` (exports all)
2. Maps `GITHUB_API_TOKEN` → `GITHUB_PERSONAL_ACCESS_TOKEN`
3. Validates token is non-empty (exits 1 with error if missing)
4. Execs `npx -y @modelcontextprotocol/server-github`

---

## MCP Server Configuration Added

```json
"github-ua4200": {
  "command": "bash",
  "args": ["/Users/NeoOC/.openclaw/hooks/github_mcp_wrapper.sh"],
  "env": {}
}
```

**Config file:** `~/.claude.json` → `mcpServers.github-ua4200`

---

## Implementation Details

### Package
- **NPM Package:** `@modelcontextprotocol/server-github`
- **Installation:** Via `npx -y` (on-demand download — no global install required)
- **Protocol:** MCP stdio
- **Auth:** Personal Access Token (PAT) via `GITHUB_PERSONAL_ACCESS_TOKEN`

### What This Enables
With the GitHub MCP server, Claude Code can:
- Read repository metadata, files, and commits
- Search code, issues, and PRs
- Create/update issues and pull requests
- Review PR diffs
- List branches, tags, and releases
- Manage GitHub Actions workflows (if token has appropriate scopes)

---

## Token Scope Requirements

The `GITHUB_API_TOKEN` found in secrets must have the following scopes for full functionality:

| Scope | Purpose |
|-------|---------|
| `repo` | Full repository access (private repos) |
| `read:org` | Read org membership |
| `workflow` | GitHub Actions (optional) |

**Note:** If the token was created as a Fine-Grained PAT, ensure the appropriate repository permissions are granted.

---

## Current mcpServers State

After P0.13 + P0.14, `~/.claude.json` contains 5 MCP servers:
1. `gitnexus` — GitNexus code intelligence
2. `claude-code-guide` — Claude Code ultimate guide
3. `codebase-memory` — Codebase memory (local MCP)
4. `clawdb-readonly` — ClawDB PostgreSQL read access (P0.13)
5. **`github-ua4200`** — GitHub API ← NEW

---

## Files Created

| File | Purpose |
|------|---------|
| `~/.openclaw/hooks/github_mcp_wrapper.sh` | Token injection wrapper (executable) |
| `~/.claude.json` (patched) | MCP server registration |

---

## Rollback

```python
import json, os
path = os.path.expanduser('~/.claude.json')
with open(path) as f:
    d = json.load(f)
d.get('mcpServers', {}).pop('github-ua4200', None)
with open(path, 'w') as f:
    json.dump(d, f, indent=2)
# Also: rm ~/.openclaw/hooks/github_mcp_wrapper.sh
```

---

## Troubleshooting

If the GitHub MCP server fails to start:

1. **Check wrapper script:**
   ```bash
   bash ~/.openclaw/hooks/github_mcp_wrapper.sh
   ```

2. **Check token is present:**
   ```bash
   grep GITHUB_API_TOKEN ~/.openclaw/secrets/.env | wc -c
   ```

3. **Test npx manually:**
   ```bash
   GITHUB_PERSONAL_ACCESS_TOKEN=<your_token> npx -y @modelcontextprotocol/server-github
   ```

4. **Token expired or invalid:** Re-generate at https://github.com/settings/tokens and update `~/.openclaw/secrets/.env`
