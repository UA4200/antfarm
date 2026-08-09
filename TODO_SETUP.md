# TODO — Repo & Skill Setup
Generated: Tue May 5, 2026 · 06:37 CDT
Reminder set: 11:00 AM CDT

---

## 🔑 BLOCKING — API Keys Needed
These tools are installed but CANNOT run without their key.

| # | Tool | Key Needed | Where to Get |
|---|------|-----------|--------------|
| 1 | claude-thumbnails | `GEMINI_API_KEY` | https://aistudio.google.com/apikey |
| 2 | Seedance-2.0-AI-UGC | `ENHANCOR_API_KEY` | https://app.enhancor.ai/api-dashboard |
| 3 | pollyreach | `POLLYREACH_API_KEY` | https://pollyreach.io/dashboard |
| 4 | content-skill-pack (full) | `APIFY_API_TOKEN` | https://apify.com |
| 5 | content-skill-pack (auto-post) | `TWITTER_API_KEY` + `TWITTER_API_SECRET` + `TWITTER_ACCESS_TOKEN` + `TWITTER_ACCESS_SECRET` | Twitter Dev Portal |
| 6 | content-skill-pack (blog DB) | `SUPABASE_URL` + `SUPABASE_SERVICE_ROLE_KEY` | https://supabase.com |
| 7 | openai-whisper (API mode) | `OPENAI_API_KEY` ✅ (likely already set) | Already in .env |
| 8 | auto-job-applier | resumex.dev account + API token | https://resumex.dev |

**Action:** Add each key to `~/.openclaw/secrets/.env` then tell Alusi "keys added."

---

## ✅ CONFIRM — Obsidian Setup
- [ ] Obsidian DMG downloading to /tmp/Obsidian.dmg
- [ ] After install: set your vault path
- [ ] Run: `openclaw skills enable obsidian-openclaw-memory`
- [ ] Tell Alusi your Obsidian vault path → she will wire the skill

---

## 🖥️ APPROVE — App Installs (need your click/approval)

| # | App | Action |
|---|-----|--------|
| 1 | Samin Command Center | Review `/tmp/install-samin-cc.sh`, then approve |
| 2 | Obsidian | Currently downloading — open DMG and drag to /Applications |

---

## 📋 REVIEW — Plans Alusi Will Execute After Approval

- [ ] CI/CD plan (see `CICD_PLAN.md`) — review and say "go"
- [ ] Obsidian memory skill config — need vault path from you
- [ ] Discord channel for agent status updates — confirm which channel

---

## 📊 DATA Alusi Needs From You

| # | What | Why |
|---|------|-----|
| 1 | Obsidian vault path | To wire `obsidian-openclaw-memory` |
| 2 | Your YouTube Channel ID | For `content-skill-pack` ideation/titles/cascade |
| 3 | Your YouTube Channel Handle | For `yt-titles` performance lookup |
| 4 | Content vault save path | Where content-skill-pack saves outputs |
| 5 | Product image for Seedance | To run first A/B test ad |
| 6 | Target audience for Seedance | To write ad copy |
| 7 | resumex.dev username | For auto-job-applier profile fetch |

---

## 🚦 STATUS — What's Already Done
- ✅ 15 ClawHub skills already installed
- ✅ nano-pdf installed
- ✅ blogwatcher installed
- ✅ openai-whisper installed
- ✅ 7 Samin repos cloned to ~/repos/samin/
- ✅ content-skill-pack skills installed to ~/.claude/skills/
- ✅ ai-storyboard-video-starter set up
- ✅ 11am reminder set
- ⏳ Obsidian downloading
- ⏳ GitHub repos batch (subagent running)
- ⏳ CI/CD plan being drafted

---

## 🔧 AFTER KEYS ARE PROVIDED
Tell Alusi which keys you added and she will:
1. Activate claude-thumbnails → generate first thumbnail
2. Activate Seedance → run first A/B test
3. Activate PollyReach → test first call
4. Wire Twitter auto-post for content-cascade
