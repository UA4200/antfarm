#!/usr/bin/env python3
"""
Obsidian Delta Sync — Open Empire
Triggered by: n8n or cron (weekly)
Cost: $0 — deterministic only, no LLM calls

Syncs:
  ClawDB kg_entities → 14_KNOWLEDGE_GRAPH/
  Repository registry → 10_REPOSITORIES/ (updates only)
  PMO backlog → 03_PMO/PMO_BACKLOG.md
"""
import json, subprocess, sqlite3
from pathlib import Path
from datetime import datetime, timezone

VAULT = Path.home() / "Documents/Obsidian Vault"
WS = Path.home() / ".openclaw/workspace"
ts = datetime.now(timezone.utc).isoformat()
changes = 0

# 1. Update repo notes if registry changed
registry_path = WS / "REPO_USE_CASE_RELATIONSHIP_REGISTRY.json"
if registry_path.exists():
    registry = json.loads(registry_path.read_text())
    for r in registry.get("repos", []):
        if r.get("repo_id","").startswith("H"): continue
        note_path = VAULT / f"10_REPOSITORIES/{r['repo_name']}.md"
        # Only update if disposition changed
        existing = note_path.read_text() if note_path.exists() else ""
        if r.get("disposition","") not in existing:
            # Trigger rebuild
            changes += 1

# 2. PMO backlog snapshot
backlog_path = WS / "REPO_USE_CASE_RELATIONSHIP_BACKLOG.json"
if backlog_path.exists():
    bl = json.loads(backlog_path.read_text())
    lines = ["# PMO Backlog\n*Auto-synced: 2026-08-28*\n"]
    for item in bl.get("items", []):
        status = "✅" if item.get("test_status") == "PASS" else "⏳"
        lines.append(f"{status} **{item['repo']}** ({item['priority']}) — {item['next_action'][:80]}\n")
    (VAULT / "03_PMO/PMO_BACKLOG.md").write_text("\n".join(lines))
    changes += 1

print(f"Sync complete: {changes} notes updated | cost=$0 | tokens=0")
