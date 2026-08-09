# Postgres Recovery Diagnosis
**Generated:** 2026-07-30 10:45 CDT  
**Host:** Ugos-Mac-mini.lan (macOS 12.7.6 x86_64, user: NeoOC)  
**Scope:** READ-ONLY investigation — no changes made

---

## Current State

| Item | Finding |
|---|---|
| Binary installed | ✅ `/usr/local/Cellar/postgresql@18/18.3/` — healthy |
| Data directory | ❌ `/usr/local/var/postgresql@18` — **DOES NOT EXIST** |
| Postgres process | ❌ Not running |
| Socket `/tmp/.s.PGSQL.5432` | ❌ Missing (service never started successfully) |
| LaunchD plist | ⚠️ Present at `~/Library/LaunchAgents/homebrew.mxcl.postgresql@18.plist` — points to missing dir |
| Log file | ⚠️ `/usr/local/var/log/postgresql@18.log` — **152 MB / 1.6M lines** of crash-loop errors |
| Alternate data dir | ⚠️ `/usr/local/var/postgres/` — partially initialized (see below) |
| ClawDB schema | ℹ️ No dedicated ClawDB schema found; `supabase_adai_schema.sql` exists (ADAI only) |
| Existing data at risk | ✅ **None** — cluster was never initialized, zero data to lose |

### Log Tail (last entries — repeated 800,000+ times)
```
postgres: could not access directory "/usr/local/var/postgresql@18": No such file or directory
Run initdb or pg_basebackup to initialize a PostgreSQL data directory.
```

The LaunchD plist has `KeepAlive: true`. Because the data directory is missing, postgres crashes on every restart attempt, which launchd re-tries immediately — creating a crash loop that has been filling the log file continuously.

### Partial `/usr/local/var/postgres/` Directory
- Created today (2026-07-30 08:25–08:26)
- Contains: `base/`, `global/`, `pg_dynshmem/` only
- **Missing:** `PG_VERSION`, `postgresql.conf`, `pg_hba.conf`, `pg_wal/`, `pg_xact/`, `pg_tblspc/`, and all other required cluster files
- **Verdict:** Incomplete/aborted `initdb` run — NOT a valid or usable data cluster
- This directory should be left in place (do not delete without Nathan's explicit approval)

---

## Root Cause

**`initdb` was never successfully executed for the postgresql@18 formula**, so the required data cluster at `/usr/local/var/postgresql@18` was never created; the LaunchD `KeepAlive: true` plist has been crash-looping postgres continuously since installation, generating a 152 MB log file.

---

## Recovery Options

### Option A — Fresh `initdb` (Recommended)
**Risk: LOW** | **Effort: Low** | **Data loss: None (nothing to lose)**

Initialize a new empty cluster at the correct path, then start the service.

```bash
# Step 1: Initialize the cluster
/usr/local/opt/postgresql@18/bin/initdb \
  --locale=en_US.UTF-8 \
  --encoding=UTF8 \
  -D /usr/local/var/postgresql@18

# Step 2: Start the service via brew (so launchd registers it cleanly)
brew services start postgresql@18

# Step 3: Verify
psql -U NeoOC -l

# Step 4 (optional but recommended): Rotate the bloated log
> /usr/local/var/log/postgresql@18.log
```

**Why safe:** No data has ever been stored in this cluster. `initdb` creates a fresh, empty cluster — equivalent to a brand-new install.

---

### Option B — `brew reinstall postgresql@18`
**Risk: LOW-MEDIUM** | **Effort: Low** | **Data loss: None**

Reinstalling the formula triggers a post-install hook that may run `initdb` automatically if no data directory is found.

```bash
brew reinstall postgresql@18
brew services start postgresql@18
```

**Risk note:** Reinstall may alter the Cellar version or reset any custom plist settings. Less predictable than Option A.

---

### Option C — Point LaunchD at Existing `/usr/local/var/postgres/`
**Risk: HIGH** | **Effort: Medium** | **Data loss: Possible**

Edit the plist to use `-D /usr/local/var/postgres` instead. 

**Rejected — do not pursue.** The `/usr/local/var/postgres/` directory is an incomplete, aborted initdb from today. It lacks `PG_VERSION` and all configuration files. Pointing postgres at it would either fail or produce undefined behavior. If a previous version's data was present it could also cause version mismatch corruption.

---

## Recommended Recovery Path

**→ Option A: Fresh `initdb` + `brew services start`**

The data directory was never initialized. There is zero data at risk. A fresh `initdb` is the cleanest, fastest, and most predictable fix. The 5-command sequence above is the entire recovery.

### Additional Recommended Action
The log file at `/usr/local/var/log/postgresql@18.log` is **152 MB**. After postgres is running, truncate it:
```bash
> /usr/local/var/log/postgresql@18.log
```

---

## Nathan Approval Required?

**YES** — Approval required before executing Option A.

Rationale:
- `initdb` is a database cluster creation command (even on empty dirs, irreversible in the sense that it commits the data directory path)
- AGENTS.md activation rule: "New agents: proof-of-concept before activation" — database service startup falls under this
- The partial `/usr/local/var/postgres/` directory may be intentional (e.g., another agent may have started an initdb for a reason) — Nathan should confirm it can be ignored
- AGENTS.md rule: "Financial = explicit approval" — postgres backs revenue-critical agents (cashclaw_director, n8n)

**Approval ask:** "Approve `initdb` at `/usr/local/var/postgresql@18` + `brew services start postgresql@18` — no existing data at risk, log confirms cluster was never initialized."

---

## Post-Recovery Checklist (for after approval + execution)

- [ ] `psql -U NeoOC -l` — confirm postgres is up
- [ ] Create `clawdb` database if required: `createdb clawdb`
- [ ] Apply any schemas from `~/.openclaw/workspace/schemas/` or `supabase_adai_schema.sql`
- [ ] Check n8n and other agents that may have Postgres connection strings
- [ ] Truncate `/usr/local/var/log/postgresql@18.log`
- [ ] Confirm cashclaw_director (PM2 ID 7) status unaffected

---

*Diagnosis written by diagnostic subagent — read-only investigation, no changes made.*
