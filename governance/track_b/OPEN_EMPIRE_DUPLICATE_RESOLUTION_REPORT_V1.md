# Open Empire — Duplicate Repository Resolution Report v1.0

**Document Type:** Duplicate Resolution Report  
**Version:** 1.0.0  
**Produced:** 2026-08-06  
**Authority:** Nathan Asiegbu  
**Status:** ACTIVE — resolution strategy defined; migration pending approval

---

## Executive Summary

The repository discovery scan identified **3 confirmed duplicate conflicts** across the Open Empire system. These are cases where the same project or closely-related project exists in multiple locations simultaneously, creating ambiguity about which copy is canonical, which copy is current, and where development should occur.

This report documents each duplicate, establishes the canonical source, defines migration strategy, and sets deprecation timeline.

---

## Duplicate 1: `antfarm`

### Conflict Overview

| Instance | Location | Type | Status |
|---|---|---|---|
| **UA4200/antfarm** (canonical) | `https://github.com/UA4200/antfarm` | Remote GitHub | ACTIVE |
| **workspace/antfarm** (deployment) | `~/.openclaw/workspace/antfarm/` | Local build | ACTIVE |
| **snarktank/antfarm** (external) | `https://github.com/snarktank/antfarm` | External/Third-party | ARCHIVED |

### Analysis

**snarktank/antfarm** is a **completely different project** that happens to share the same name. It is a third-party repo in the `repo_lab` (research/external) directory. It has **zero production dependencies** and **does not interact** with UA4200/antfarm. Name collision only.

**UA4200/antfarm** and **workspace/antfarm** are the same project in two states:
- `UA4200/antfarm` is the **upstream source** hosted on GitHub
- `~/.openclaw/workspace/antfarm/` is the **local compiled deployment** — a build artifact from UA4200/antfarm

This is the expected git clone → local build pattern. It is **not a problematic duplicate** as long as:
1. Development always originates in UA4200/antfarm
2. workspace/antfarm is never manually edited outside of a git workflow
3. workspace/antfarm is always updated via `git pull` + rebuild, not manual copy

### Canonical Designation

| Role | Canonical Source |
|---|---|
| **Source of truth** | `UA4200/antfarm` (GitHub) |
| **Runtime deployment** | `~/.openclaw/workspace/antfarm/` |
| **External reference (unrelated)** | `snarktank/antfarm` (ignore, no action needed) |

### Migration Strategy

1. **Verify** that `~/.openclaw/workspace/antfarm/` is a proper git clone of UA4200/antfarm:
   ```bash
   cd ~/.openclaw/workspace/antfarm && git remote -v
   ```
2. **If not a git clone:** treat workspace copy as build output and establish proper clone:
   ```bash
   # Backup current workspace antfarm
   mv ~/.openclaw/workspace/antfarm ~/.openclaw/workspace/antfarm_backup_$(date +%Y%m%d)
   # Fresh clone
   git clone https://github.com/UA4200/antfarm.git ~/.openclaw/workspace/antfarm
   cd ~/.openclaw/workspace/antfarm && npm install && npm run build
   ```
3. **If already a git clone:** `git pull origin main` to sync.
4. **snarktank/antfarm:** Move to `repo_lab/external/snarktank-antfarm/` or remove. No action required for operations.

### Resolution Status

- [ ] Verify workspace/antfarm git remote — **Target: 2026-08-13**
- [ ] Document in AGENTS.md after resolution — **Target: 2026-08-13**
- [ ] Archive snarktank/antfarm reference in registry — **Already done in V1 registry**

---

## Duplicate 2: `mission-control`

### Conflict Overview

| Instance | Location | Type | Status |
|---|---|---|---|
| **UA4200/mission-control** (canonical) | `https://github.com/UA4200/mission-control` | Remote GitHub | ACTIVE |
| **workspace/mission-control** (deployment) | `~/.openclaw/workspace/mission-control/` | Local deployment | ACTIVE (PM2 ID 17) |

### Analysis

This is the same project in two states — identical pattern to antfarm:
- `UA4200/mission-control` is the **upstream source**
- `~/.openclaw/workspace/mission-control/` is the **live deployment** running as PM2 process ID 17 on port 3333

The workspace copy is **actively serving production traffic** (the Command Center UI). This means any migration must preserve uptime.

### Canonical Designation

| Role | Canonical Source |
|---|---|
| **Source of truth** | `UA4200/mission-control` (GitHub) |
| **Runtime deployment** | `~/.openclaw/workspace/mission-control/` (PM2 ID 17) |

### Migration Strategy

1. **Verify** git remote of local copy:
   ```bash
   cd ~/.openclaw/workspace/mission-control && git remote -v
   # Expected: origin https://github.com/UA4200/mission-control.git
   ```
2. **Update procedure** (zero-downtime):
   ```bash
   cd ~/.openclaw/workspace/mission-control
   git pull origin main
   pm2 restart mission-control
   # Verify: curl -s http://localhost:3333/health
   ```
3. **No path changes needed** — workspace/mission-control IS the correct deployment location.
4. **Document** in AGENTS.md that all updates to mission-control must come through `git pull` from UA4200/mission-control.

### Risk Factors

- PM2 ID 17 is actively running — any file-system operations on this directory risk downtime
- PM2 `cwd` must remain at `~/.openclaw/workspace/mission-control/`
- Do NOT rename or move this directory while PM2 is running

### Resolution Status

- [ ] Verify git remote of workspace/mission-control — **Target: 2026-08-13**
- [ ] Establish update runbook in Remote Operations doc — **Target: 2026-08-13**
- [ ] Add PM2 update procedure to AGENTS.md — **Target: 2026-08-20**

---

## Duplicate 3: `open-empire-nexus`

### Conflict Overview

| Instance | Location | Type | Status |
|---|---|---|---|
| **open-empire-workspace** (canonical) | `~/.openclaw/workspace/` | Active workspace | ACTIVE |
| **open-empire-nexus** | `~/projects/open-empire-nexus/` | Unknown — likely superseded | LEGACY |
| **open-empire-nexus/server** | `~/projects/open-empire-nexus/server/` | Sub-project | LEGACY |

### Analysis

`open-empire-nexus` was discovered as a local git repository at `~/projects/open-empire-nexus/`. Based on its location outside the active workspace and the existence of the fully-developed `~/.openclaw/workspace/`, it is **highly likely superseded**.

Evidence for LEGACY status:
1. Located at `~/projects/` — the conventional "old projects" area vs. `~/.openclaw/workspace/` for active work
2. No PM2 process references `~/projects/open-empire-nexus`
3. Has a sub-project at `/server/` suggesting it predates the current monorepo-style workspace structure
4. No CI/CD references found for this path

Evidence requiring audit before full deprecation:
- The repository contents have not been fully inspected
- It may contain agent logic, configurations, or scripts not yet migrated to workspace
- The nexus name suggests it may have been a hub/connector layer

### Canonical Designation

| Role | Canonical Source |
|---|---|
| **Active workspace** | `~/.openclaw/workspace/` |
| **Legacy reference** | `~/projects/open-empire-nexus/` (LEGACY, pending deprecation) |

### Migration Strategy

**Phase 1 — Audit (Priority: P1)**
```bash
# Inventory the legacy repo
ls -la ~/projects/open-empire-nexus/
git -C ~/projects/open-empire-nexus log --oneline -20
git -C ~/projects/open-empire-nexus remote -v

# Compare with workspace
diff -rq ~/projects/open-empire-nexus/ ~/.openclaw/workspace/ \
  --exclude=".git" \
  --exclude="node_modules" \
  --exclude="*.pyc" 2>&1 | head -50
```

**Phase 2 — Rescue unique assets**
- If any files in nexus are NOT present in workspace, migrate them before deprecation
- Document any migrated assets in AGENTS.md

**Phase 3 — Deprecation**
- Rename: `mv ~/projects/open-empire-nexus ~/projects/open-empire-nexus-DEPRECATED-$(date +%Y%m%d)`
- Or archive as tarball and remove

**Phase 4 — Cleanup**
```bash
# After confirmed migration, archive
tar czf ~/archived_repos/open-empire-nexus-archive-$(date +%Y%m%d).tar.gz \
  ~/projects/open-empire-nexus-DEPRECATED-*/
# Remove original after verifying archive
```

### Risk Factors

- Unknown content — must audit before deletion
- May contain environment-specific configuration not in workspace
- Git history may contain useful commit archaeology

### Resolution Status

- [ ] Audit ~/projects/open-empire-nexus contents — **Target: 2026-08-13** (P1)
- [ ] Migrate any unique assets to workspace — **Target: 2026-08-20**
- [ ] Deprecate and archive — **Target: 2026-08-27**
- [ ] Confirm no PM2 references to old path — **Target: before deprecation**

---

## Summary Table

| Duplicate | Canonical | LEGACY/External | Resolution | Priority | Target Date |
|---|---|---|---|---|---|
| antfarm (3-way) | UA4200/antfarm + workspace/antfarm (deployment) | snarktank/antfarm (external, unrelated) | Verify git remotes; no structural change needed | P2 | 2026-08-13 |
| mission-control (2-way) | UA4200/mission-control + workspace/mission-control (deployment) | — | Verify git remote; document update runbook | P2 | 2026-08-13 |
| open-empire-nexus (2-way) | ~/.openclaw/workspace/ | ~/projects/open-empire-nexus (LEGACY) | Audit, migrate unique assets, deprecate | P1 | 2026-08-27 |

---

## Change Log

| Date | Change | Author |
|---|---|---|
| 2026-08-06 | Initial document created — v1.0.0 governance baseline | Nathan Asiegbu (via governance build) |
