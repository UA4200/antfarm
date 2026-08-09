# 🦞 PMO Council Report — ADAI Energy Video / Namecheap / Leads

**Date:** 2026-05-18
**Mission:** Launch readiness for ADAI Energy (`adaienergy.com`) — BLCO supplier site, promo video, and Instantly outreach campaign.

---

## 1. Promo Video — ⚠️ BLOCKED ON API KEY

**Status:** Video **not generated**. No `MUAPI_API_KEY` exists in `~/.openclaw/secrets/.env`, `~/.openclaw/secrets.env`, or any other scanned env file. The 80+ API keys in `~/.openclaw/secrets/.env` cover OpenAI, Anthropic, ElevenLabs, HeyGen, Apify, Instantly, Hunter, Stripe, etc. — but **no Muapi**.

### Muapi API mechanics (verified from Open-Lovart + AI-Youtube-Shorts-Generator source)

- **Base URL:** `https://api.muapi.ai/api/v1`
- **Auth header:** `x-api-key: <YOUR_KEY>`
- **Submit job:** `POST /api/v1/{model-endpoint}` → returns `{"request_id": "..."}`
- **Poll result:** `GET /api/v1/predictions/{request_id}/result` → status flips to `completed` and the response includes the video URL.
- **Video models exposed in Open-Lovart:** Kling v3, Sora 2, Veo 3, Wan 2.6, Seedance 2.0, Runway Gen-3, Luma Ray2 (text-to-video) and Kling v2.1 I2V, Veo3 I2V, Runway I2V, Luma Ray2 I2V, Seedance 2.0 I2V (image-to-video).

### Exact action Nathan needs to take (≤ 2 sentences)

> Sign up at **`https://muapi.ai`** → Dashboard → **API Keys** → Create key → add `MUAPI_API_KEY=<key>` to `~/.openclaw/secrets/.env`. Once the key exists I will execute a direct `POST https://api.muapi.ai/api/v1/kling-v2-1` (or Wan 2.6) with the cinematic 16:9 prompt and save the result to `~/.openclaw/workspace/adaienergy-site/assets/promo-video.mp4`.

### Prompt locked and ready to fire

```
Cinematic 16:9 corporate energy promo. Aerial ocean shot at golden hour.
Offshore oil platform at sunset. Executive reviewing trade documents. Oil
tanker on open ocean. Global trade route map. Refinery towers at dusk.
Professional grade. Dark navy and gold palette. ADAI Energy — Precision.
Volume. Trust.
```

### Reference call (drop-in once `MUAPI_API_KEY` is set)

```bash
curl -X POST "https://api.muapi.ai/api/v1/kling-v2-1" \
  -H "x-api-key: $MUAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Cinematic 16:9 corporate energy promo. Aerial ocean shot at golden hour. Offshore oil platform at sunset. Executive reviewing trade documents. Oil tanker on open ocean. Global trade route map. Refinery towers at dusk. Professional grade. Dark navy and gold palette. ADAI Energy — Precision. Volume. Trust.",
    "aspect_ratio": "16:9",
    "duration": 10
  }'
# Then poll: curl "https://api.muapi.ai/api/v1/predictions/<request_id>/result" -H "x-api-key: $MUAPI_API_KEY"
```

> Exact endpoint slug (`kling-v2-1`, `wan-2-6`, `veo-3`, etc.) should be confirmed against `https://muapi.ai/playground` — each model has its own playground page that shows the canonical endpoint name and required payload schema.

---

## 2. Namecheap Deployment — ✅ READY

Full step-by-step brief written to **`~/.openclaw/workspace/adaienergy-site/DEPLOY.md`** (188 lines). Covers:

1. **cPanel File Manager upload** — zip site, upload, extract into `public_html/` (or `public_html/adaienergy.com/` if addon domain).
2. **DNS** — Advanced DNS in Namecheap dashboard: `A @ → SHARED_IP`, `CNAME www → adaienergy.com.` (or switch to Namecheap Web Hosting nameservers for auto-management).
3. **Redirect `adaiblco.com` + `adaioil.com` → `adaienergy.com`** — two options documented:
   - **Option A (recommended):** Park as cPanel aliases sharing root + `.htaccess` 301 block. Preserves HTTPS on redirect domains.
   - **Option B:** Namecheap free URL Redirect (301 Unmasked). Cheaper but no HTTPS on source — cert warning before redirect.
4. **SSL** — cPanel → SSL/TLS Status → Run AutoSSL across all three domains (+ www variants). Expect 5–15 min issuance.
5. **Formspree contact form** — sign up free tier (50 submissions/mo), get Form ID, replace `REPLACE_WITH_FORM_ID` in `js/main.js` **line 68**, re-upload. Lock allowed domains to `adaienergy.com` in Formspree dashboard.

The brief also includes an EasyWP escape hatch in case Namecheap product was bought wrong, and a post-deploy verification checklist.

---

## 3. Instantly Campaign — ✅ CSV READY (caveat: 4 verified, 76 guessed)

**Source file:** `~/.openclaw/blco/outreach/enriched_for_instantly.jsonl` — **80 leads** scored by the BLCO pipeline.

**Generated files:**
- `~/.openclaw/blco/outreach/instantly_upload.csv` — **all 80 leads**, sorted verified-first then by score desc.
- `~/.openclaw/blco/outreach/instantly_upload_verified_only.csv` — **4 verified leads** (Apify-crawled, real emails from site contact pages).

**Verified leads (real emails, safe to send first):**

| Email | Company | Score |
|-------|---------|-------|
| `david@premieroilbrokers.com` | Premier Oil Brokerage Services for Energy Solutions | 80 |
| `info@ametheus.com` | Due Diligence on BLCO seller | 80 |
| `support@globaltradeplaza.com` | Buy Wholesale Bonny Light Crude Oil (Blco) Online from Suppliers & Exporters | 75 |
| `info@nnrvtradepartners.com` | How to Pass Refinery Compliance in 2025 | 63 |

**Domain-guessed (76 leads):** All in the `trade@<domain>.com` pattern from `enriched_via: "domain_guess"`. Bounce rate will be high. **Recommendation:** before bulk-loading into Instantly, run them through a verification step (Hunter `HUNTER_API_KEY` is already in secrets, or Debounce via `DEBOUNCE_API_KEY`) and drop anything with `score < 80` from the verifier. Sending unverified bulk will burn the `adaienergy.com` sender reputation before it has a chance to warm up.

### CSV columns
```
Email, First Name, Last Name, Company, Domain, Lead Score
```

Matches Instantly's default import schema — drop in directly via Instantly → Leads → Import CSV.

---

## 4. Critical Path — What unblocks the launch

| Blocker | Owner | Action |
|---------|-------|--------|
| `MUAPI_API_KEY` missing | Nathan | Sign up `muapi.ai`, paste key into `~/.openclaw/secrets/.env`. Then re-run video generation. |
| Namecheap product type (Stellar vs EasyWP) | Nathan | Confirm hosting plan in Namecheap dashboard — DEPLOY.md assumes Stellar/cPanel. |
| Intake email (`trade@adaienergy.com`) | Nathan | Provision in cPanel → Email Accounts after DNS resolves. Required before Formspree is useful. |
| 76 unverified leads | PMO | Run Hunter/Debounce verify pass before bulk import. |

---

## Files written this session

```
~/.openclaw/workspace/adaienergy-site/DEPLOY.md
~/.openclaw/workspace/PMO_VIDEO_DEPLOY_REPORT.md
~/.openclaw/blco/outreach/instantly_upload.csv
~/.openclaw/blco/outreach/instantly_upload_verified_only.csv
```

— PMO Council 🦞
