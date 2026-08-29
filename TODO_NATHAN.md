# TODO_NATHAN.md — Items Nathan Needs to Provide
Version: 4.0 | Updated: 2026-08-27 | Scrubbed against ~/.openclaw/secrets/.env

---

## ✅ CLEARED — Previously Listed, Now Confirmed in Secrets

| # | Key | Status | Notes |
|---|-----|--------|-------|
| — | `OPENCLAW_API_KEY` | ✅ PRESENT | `befb196d...` wired |
| — | `TELEGRAM_ALERTS_GROUP_ID` | ✅ TESTED LIVE | `-5121923677` — message delivered |
| — | `TELEGRAM_BRIEFING_GROUP_ID` | ✅ TESTED LIVE | `-1003920031365` — message delivered |
| — | `TELEGRAM_LOGS_GROUP_ID` | ✅ TESTED LIVE | `-1003933658318` — message delivered |
| — | `GEMINI_API_KEY` | ✅ PRESENT | `AIzaSyC...` |
| — | `SUPABASE_URL` | ✅ PRESENT | `https://ibofkvptfmklsqdcvezj.supabase.com` |
| — | `SUPABASE_SERVICE_ROLE_KEY` | ✅ PRESENT | wired |
| — | `GF_SECURITY_ADMIN_PASSWORD` | ✅ PRESENT | `GRAFANA_ADMIN_PASSWORD` set |
| — | `DEBOUNCE_API_KEY` | ✅ N/A | Replaced by Hunter.io |

---

## 🔴 BLOCKING — Empty Keys (no value in secrets)

| # | Key | Service | Where to Get |
|---|-----|---------|--------------|
| 1 | `ENHANCOR_API_KEY` | Seedance-2.0 UGC ads | https://app.enhancor.ai/api-dashboard |
| 2 | `TWITTER_API_KEY` + `TWITTER_API_SECRET` + `TWITTER_ACCESS_TOKEN` + `TWITTER_ACCESS_SECRET` | Twitter auto-post | Twitter Dev Portal |

---

## ✅ CONFIRMED — PollyReach

Activated 2026-05-09. Alusi phone: **+1 (571) 725-2743** | Inbound prompt set | 10-min poller active | Test call delivered successfully.

---

## 🟡 CONFIG — Decisions / Paths Still Needed

| # | Item | Why | Notes |
|---|------|-----|-------|
| ~~5~~ | ~~Obsidian vault path~~ | ✅ DONE — vault at `~/Documents/Obsidian Vault`, cron active, syncing daily | — |
| 6 | YouTube Channel ID + Handle | content-skill-pack ideation + yt-titles lookup | — |
| 7 | Content output path | Where content-skill-pack saves files | — |
| 8 | Product image for Seedance | First A/B test ad | Needs `ENHANCOR_API_KEY` first |
| 9 | Target audience for Seedance | Ad copy generation | — |
| 10 | resumex.dev username / token | auto-job-applier profile fetch | — |
| 11 | Discord #channel ID for agent logs | Wire agent status updates | `DISCORD_GUILD_ID` present, need channel |

---

## ✅ CLEARED — Previously Reported Configuration Issues

| # | Item | Issue | Fix |
|---|------|-------|-----|
| 12 | `DATABASE_URL` | Old default password was reported | ✅ Fixed and confirmed against the rotated ClawDB password |

---

## ✅ All Confirmed Wired (no action needed)

- `ANTHROPIC_API_KEY` ✅
- `VERCEL_USER_ID` + `VERCEL_TOKEN_ID` ✅ (added 2026-05-09)
- `APIFY_API_KEY` + `APIFY_API_TOKEN` + `APIFY_USER_ID` ✅ (added 2026-05-09)
- `FIRECRAWL_API_KEY` ✅ (added 2026-05-09, CLI live, scrape tested)
- `POLLYREACH_API_KEY` ✅ (Alusi — +15717252743, activated + tested 2026-05-09)
- `TWILIO_ACCOUNT_SID` + `TWILIO_AUTH_TOKEN` + `TWILIO_PHONE_NUMBER` ✅ (active, balance $15.34, SMS tested 2026-05-09)
- `FIRECRAWL_API_KEY` ✅ (CLI v1.16.2, scrape tested 2026-05-09)
- `APIFY_API_KEY` + `APIFY_USER_ID` ✅ (added 2026-05-09)
- `VERCEL_USER_ID` + `VERCEL_TOKEN_ID` ✅ (added 2026-05-09)
- `.env` bare-key errors ✅ fixed (7 empty keys properly formatted)
- `OPENAI_API_KEY` ✅
- `KALSHI_API_KEY_ID` + `KALSHI_PRIVATE_KEY_PATH` ✅
- `TELEGRAM_BOT_TOKEN` + all 3 group IDs ✅ (tested live 2026-05-08)
- `DISCORD_BOT_TOKEN` + `DISCORD_GUILD_ID` ✅
- `N8N_API_KEY` + all webhook URLs ✅
- `AIRTABLE_TOKEN` ✅
- `HUNTER_API_KEY` ✅
- `HYRVEA_API_KEY` ✅
- `PHANTOMBUSTER_API_KEY` ✅
- `OPENCLAW_API_KEY` + `OPENCLAW_GATEWAY_TOKEN` ✅
- `SUPABASE_URL` + `SUPABASE_SERVICE_ROLE_KEY` + `SUPABASE_ANON_KEY` ✅
- `GEMINI_API_KEY` ✅
- `ELEVENLABS_API_KEY` ✅
- `HEYGEN_API_KEY` ✅
- `INSTANTLY_API_KEY` ✅
- `STRIPE_PUBLISHABLE_KEY` + `STRIPE_SECRET_KEY` ✅ (live keys)
- `ALPACA_API_KEY` + `ALPACA_SECRET_KEY` ✅ (paper trading)
- `TAVILY_API_KEY` ✅
- `APOLO_API_KEY` ✅
- `BRAVE_API_KEY` ✅
- `AGENTMAIL_*` ✅
- `SMTP/GMAIL` credentials ✅
- `TWILIO_*` ✅
- `GRAFANA_ADMIN_PASSWORD` ✅
- `CLAWDB_*` ✅
- `SHOPIFY_API_KEY` + `SHOPIFY_API_SECRET` ✅
- `EIA_API_KEY` ✅
- `COMTRADE_API_KEY` ✅

---

## ✅ CONFIRMED COMPLETE — Current Records

| Item | Status | Notes |
|---|---|---|
| Obsidian vault indexing | ✅ FIXED | obsidian_sync.sh now points to correct vault |
| CI/CD implementation | ✅ LIVE | `~/.openclaw/bin/cicd_health.sh` — cron 1am daily |
| Empire injection script | ✅ CONFIRMED RAN | 20+ repos in ~/.openclaw/repos/installed/ |
| CashClaw stack | ✅ LIVE | Canonical agents under `~/.openclaw/trading/`; director, arb, Polymarket trader, and sentinel are recorded as live |
| ClawDB password | ✅ ROTATED | New password stored in secrets; database role change confirmed |
| DATABASE_URL | ✅ FIXED | Updated with current ClawDB password |
| Discord #agent-logs | ✅ CREATED | Channel ID: `1505383212443242666` |
| DISCORD_AGENT_LOGS_CHANNEL_ID | ✅ WIRED | In secrets/.env |
| HeyGen API | ✅ CONFIRMED | 1,500 credits, avatars live |
| AgentMail | ✅ CONFIRMED | neooc@agentmail.to live, SMTP/IMAP wired |
| Launch prep doc | ✅ WRITTEN | ~/.openclaw/workspace/projects/BLCO/LAUNCH_PREP.md |
| PMO N8N research directive | ✅ ISSUED | ~/.openclaw/workspace/directives/PMO_N8N_RESEARCH.md |

## 🔴 STILL BLOCKING / NEEDS NATHAN

| Item | Blocker |
|---|---|
| Instantly cold email | 402 — needs paid plan upgrade (app.instantly.ai) |
| Grafana password rotation | API returned empty (port 3001 — may need manual) |
| BLCO domain warming | BLCO_EMAIL + BLCO_EMAIL_PASS still missing |
| TELEGRAM_BOT_TOKEN_BLCO | Still missing |
| Twitter API keys | Still missing (auto-post blocked) |
| ENHANCOR_API_KEY | Still missing (Seedance blocked) |

## 📌 NEXT DECISIONS

1. Provide or confirm the missing BLCO, Twitter, and Enhancor credentials when those launches are authorized.
2. Decide the YouTube channel, content output path, and Seedance target audience/product image.
3. Provide resumex.dev username/token if job-search automation is still wanted.
4. Provide the Discord channel ID for agent logs only if it differs from the confirmed `#agent-logs` channel above.
