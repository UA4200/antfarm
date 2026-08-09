# Phase 5 Deployment Receipt — 2026-07-30

## Deployment Host
Ugos-Mac-mini.lan | macOS 12.7.6 | x86_64 | NeoOC

## Component SHA Map
| Component | GitHub Repo | Head SHA | Live Path | PM2 IDs | Status |
|---|---|---|---|---|---|
| Alusi Core | UA4200/alusi-core | 87c56b9e47f0 | ~/.openclaw/ | 0,1,2,3,4,5 | RUNNING |
| Open Empire Core | UA4200/open-empire-core | 8807a1d377e3 | ~/.openclaw/empire/ | 25,26 | RUNNING |
| Git/GitHub Workspace | UA4200/git-github | 75d2d2386d4a | ~/.openclaw/workspace/ | all | RUNNING |
| Mission Control | UA4200/mission-control | 62b7a9b612cd | ~/.openclaw/workspace/mission-control/ | 18 | RUNNING |
| Antfarm | UA4200/antfarm | 268e24837b03 | ~/.openclaw/workspace/antfarm/ | (workflows) | RUNNING |
| BLCO Pipeline | UA4200/blco-pipeline | ec07264280511 | ~/.openclaw/blco/ | 16 | STOPPED |

## Postgres
- Status: RUNNING (pg_ctl, PM2 id=43, name=clawdb)
- Socket: /tmp/.s.PGSQL.5432
- TCP: 127.0.0.1:5432
- Database: clawdb (exists)
- Version: PostgreSQL 18.3

## CashClaw Director
- Status: NOT INCLUDED — CONFLICT
- PM2 ID 7 — preserved, not wired to GitHub
- Path: ~/.openclaw/moltlaunch/agents/cashclaw_director/
- Capital: $25.19 (Kalshi, live)

## Git Remote Wiring Summary
| Live Path | GitHub Repo | Git Status | Remote Action |
|---|---|---|---|
| ~/.openclaw/workspace/ | UA4200/git-github | Had .git, no remote | Added origin |
| ~/.openclaw/workspace/mission-control/ | UA4200/mission-control | Not git | init + remote add origin |
| ~/.openclaw/workspace/antfarm/ | UA4200/antfarm | Had .git, origin=snarktank/antfarm | Added ua4200 remote |
| ~/.openclaw/blco/ | UA4200/blco-pipeline | Not git | init + remote add origin |

## Deployment Method
Code committed to GitHub from live paths. No service restarts performed.
GitHub governance layer established. Exact SHAs documented for rollback reference.
No `git add` or `git commit` performed on live paths — remote wire only.

## Constraints Applied
- cashclaw_director (PM2 ID 7) untouched
- No secrets committed
- No leads.jsonl committed
- No PM2 restarts performed
- No git add/commit in live paths

## Timestamp
Generated: 2026-07-30 11:17 CDT
Phase: 5 of 5
