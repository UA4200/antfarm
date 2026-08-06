# Open Empire — GitHub Control Plane Specification
**Version:** 1.0.0 | **Date:** 2026-08-06 | **Ref:** B5  
**Governed by:** OPEN_EMPIRE_GOVERNANCE_BASELINE_V1.0.0

---

## Overview

This spec defines the GitHub configuration, CI/CD workflows, branch protection, and governance integration for all UA4200 repositories in the Open Empire. The goal is to wire GitHub as the authoritative source of truth for code deployments, with all merges gated by governance validation.

---

## Current State

| Repository | Remote Configured | CI/CD | Branch Protection | Governance Check |
|------------|-------------------|-------|-------------------|-----------------|
| git-github.git | ✅ Yes | ❌ None | ❌ None | ❌ None |
| open-empire-governance | ❌ No remote | ❌ None | ❌ None | ❌ None |
| open-empire-trading | ❌ No remote | ❌ None | ❌ None | ❌ None |
| open-empire-infrastructure | ❌ No remote | ❌ None | ❌ None | ❌ None |
| open-empire-adai | ❌ No remote | ❌ None | ❌ None | ❌ None |
| open-empire-blco | ❌ No remote | ❌ None | ❌ None | ❌ None |

**Critical Gap:** Only 1 of 6 repos has a GitHub remote. None have CI/CD or branch protection.

---

## UA4200 Repositories — Full Definition

| Repo ID | Repository Name | Workspace Path | Portfolio | Purpose |
|---------|----------------|----------------|-----------|---------|
| UA4200-R01 | open-empire-governance | `~/.openclaw/workspace/governance/` | P002 | Governance docs, registry, validation scripts |
| UA4200-R02 | open-empire-trading | `~/.openclaw/trading/` | P001 | Trading agents, clients, shared modules |
| UA4200-R03 | open-empire-infrastructure | `~/.openclaw/workspace/` | P002 | Alusi core, mission-control, services |
| UA4200-R04 | open-empire-adai | `~/.openclaw/workspace/adai/` | P003 | ADAI Solutions products |
| UA4200-R05 | open-empire-blco | `~/.openclaw/blco/` | P004 | BLCO pipeline, leads, outreach |
| UA4200-R06 | git-github | `~/.openclaw/workspace/git-github/` | P002 | Git/GitHub integration utilities |

---

## Required GitHub Actions Workflows

### 1. `validate.yml` — Governance Validation
**Trigger:** On every push to any branch, on every PR  
**Purpose:** Run governance validation to ensure registry integrity

```yaml
# .github/workflows/validate.yml
name: Governance Validation

on:
  push:
    branches: ["**"]
  pull_request:
    branches: [main]

jobs:
  governance-validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.13"
      
      - name: Install dependencies
        run: pip install jsonschema pyyaml
      
      - name: Run governance validation
        run: python governance/build/validate.py --strict
        
      - name: Post validation summary
        if: always()
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            // Post validation results as PR comment
```

### 2. `deploy.yml` — Deployment to OpenClaw Host
**Trigger:** On push to `main` branch, manual dispatch  
**Purpose:** Deploy updated code to the OpenClaw Mac mini via Tailscale

```yaml
# .github/workflows/deploy.yml
name: Deploy to OpenClaw

on:
  push:
    branches: [main]
  workflow_dispatch:
    inputs:
      service:
        description: "Service to restart after deploy"
        required: false
        type: string

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4
      
      - name: Validate governance before deploy
        run: python governance/build/validate.py --strict
      
      - name: Deploy via SSH over Tailscale
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.DEPLOY_TARGET }}
          username: NeoOC
          key: ${{ secrets.DEPLOY_SSH_KEY }}
          script: |
            cd ~/.openclaw/workspace
            git pull origin main
            if [ -n "${{ github.event.inputs.service }}" ]; then
              pm2 restart ${{ github.event.inputs.service }}
            fi
      
      - name: Notify via OpenClaw gateway
        run: |
          curl -X POST ${{ secrets.OPENCLAW_API_KEY }} \
            -d '{"event": "deploy", "repo": "${{ github.repository }}", "sha": "${{ github.sha }}"}'
```

### 3. `governance-check.yml` — PR Governance Gate
**Trigger:** On every PR to `main`  
**Purpose:** Required check — PR cannot merge unless governance validation passes

```yaml
# .github/workflows/governance-check.yml
name: Governance Check (Required)

on:
  pull_request:
    branches: [main]
    types: [opened, synchronize, reopened]

jobs:
  governance-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.13"
      
      - name: Install validation dependencies
        run: pip install jsonschema pyyaml
      
      - name: Run strict governance validation
        run: python governance/build/validate.py --strict --output=json > governance_result.json
      
      - name: Check governance pass/fail
        run: |
          PASS=$(cat governance_result.json | python -c "import sys,json; d=json.load(sys.stdin); print(d.get('passed', False))")
          if [ "$PASS" != "True" ]; then
            echo "❌ Governance validation FAILED. PR cannot merge."
            cat governance_result.json
            exit 1
          fi
          echo "✅ Governance validation passed."
      
      - name: Post governance result as PR status
        uses: actions/github-script@v7
        with:
          script: |
            const result = require('./governance_result.json');
            await github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `## Governance Check Result\n\n${result.passed ? '✅ PASSED' : '❌ FAILED'}\n\nVersion: ${result.version || 'unknown'}\nTimestamp: ${new Date().toISOString()}`
            });
```

---

## Branch Protection Rules

Apply to **all 6 repositories**, branch: `main`

```
Branch protection: main
├── Require a pull request before merging: YES
│   ├── Required approvals: 1 (Nathan Asiegbu)
│   └── Dismiss stale reviews when new commits pushed: YES
├── Require status checks to pass before merging: YES
│   ├── Required checks:
│   │   ├── governance-check (REQUIRED — must pass)
│   │   └── governance-validate (REQUIRED — must pass)
│   └── Require branches to be up to date before merging: YES
├── Require conversation resolution before merging: YES
├── Restrict pushes that create matching branches: NO
├── Allow force pushes: NO (never)
├── Allow deletions: NO
└── Require linear history: YES (prefer)
```

**Implementation via GitHub API or UI:**
- Settings → Branches → Branch protection rules → Add rule
- Pattern: `main`
- Check all boxes above

---

## Repository Secrets Required

Each repository needs these secrets (Settings → Secrets and variables → Actions):

| Secret Name | Value Source | Required By |
|-------------|-------------|-------------|
| `OPENCLAW_API_KEY` | From `~/.openclaw/secrets/.env` (OPENCLAW key) | deploy.yml — gateway notification |
| `DEPLOY_TARGET` | Tailscale IP of Mac mini | deploy.yml — SSH deploy |
| `DEPLOY_SSH_KEY` | SSH private key for NeoOC@mac-mini | deploy.yml — SSH auth |
| `ANTHROPIC_API_KEY` | From `~/.openclaw/secrets/.env` | Any workflow needing Claude |
| `GITHUB_TOKEN` | Auto-provided by GitHub Actions | PR comments, status checks |

**Note:** `GITHUB_TOKEN` is automatically available. Only the first 4 need manual configuration.

---

## Webhooks — OpenClaw Gateway Integration

Configure webhooks in each repository (Settings → Webhooks → Add webhook):

```
Payload URL: http://<TAILSCALE_IP>:8788/webhooks/github
Content type: application/json
Secret: <webhook_secret_from_secrets_env>

Events to trigger:
- Push (on every push)
- Pull requests (PR opened, closed, merged, reviewed)
- Releases (new release published)
- Workflow runs (CI pass/fail)
```

**Webhook handler in Alusi gateway** should:
1. On push to `main`: trigger registry sync, notify Telegram
2. On PR merge: log to governance audit trail (clawdb.agent_events)
3. On release: trigger deployment notification
4. On CI failure: alert Telegram immediately

---

## Governance Check: PR Merge Gate

Every PR to `main` **must** pass governance validation before merge is allowed.

**Validation runs:**
1. Schema validation of all registry JSON files
2. Cross-reference integrity (capability_ids in agents exist in capability registry, etc.)
3. Governance version consistency across all files
4. No broken dependency graph references

**Validation is defined in:** `~/.openclaw/workspace/governance/build/validate.py`

---

## Status Badges

Every repository's `README.md` must include:

```markdown
## Status

![Governance](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/NeoOC/<repo>/main/.github/badges/governance.json)
![CI](https://github.com/NeoOC/<repo>/actions/workflows/validate.yml/badge.svg)
![Deploy](https://github.com/NeoOC/<repo>/actions/workflows/deploy.yml/badge.svg)

**Governed by:** OPEN_EMPIRE_GOVERNANCE_BASELINE_V1.0.0
```

**Dynamic governance badge:** Generate `.github/badges/governance.json` during CI validation run.

---

## Implementation Order

### Step 1 — Add Git Remotes (All 5 missing repos)
```bash
# For each missing repo, create on GitHub then:
cd ~/.openclaw/workspace/governance/
git remote add origin https://github.com/NeoOC/open-empire-governance.git

cd ~/.openclaw/trading/
git remote add origin https://github.com/NeoOC/open-empire-trading.git

# ... etc for infrastructure, adai, blco
```

**Required:** Nathan must create repos on GitHub first (or use GitHub CLI: `gh repo create`).

### Step 2 — Push Governance Registry
```bash
cd ~/.openclaw/workspace/governance/
git add .
git commit -m "chore: initial governance registry push [UA4200]"
git push -u origin main
```

### Step 3 — Set Branch Protection
For each repo, via GitHub UI or GitHub CLI:
```bash
gh api repos/NeoOC/open-empire-governance/branches/main/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"contexts":["governance-check","governance-validate"]}' \
  --field enforce_admins=true \
  --field required_pull_request_reviews='{"required_approving_review_count":1}' \
  --field restrictions=null
```

### Step 4 — Add Workflows
Copy workflow files to `.github/workflows/` in each repo and push:
```bash
mkdir -p .github/workflows/
cp ~/.openclaw/workspace/governance/track_b/.github/workflows/*.yml .github/workflows/
git add .github/workflows/
git commit -m "ci: add governance validation and deploy workflows [UA4200]"
git push
```

### Step 5 — Configure Secrets
For each repo, set secrets via GitHub CLI or UI:
```bash
gh secret set OPENCLAW_API_KEY --body "$OPENCLAW_KEY" --repo NeoOC/open-empire-governance
gh secret set DEPLOY_TARGET --body "$TAILSCALE_IP" --repo NeoOC/open-empire-governance
gh secret set DEPLOY_SSH_KEY --body "$(cat ~/.ssh/id_rsa)" --repo NeoOC/open-empire-governance
```

### Step 6 — Configure Webhooks
Via GitHub UI (Settings → Webhooks) for each repo, add the Alusi gateway webhook.

---

## Timeline

| Step | Duration | Dependencies |
|------|----------|-------------|
| Step 1: Add remotes | 30 min | Nathan creates repos on GitHub |
| Step 2: Push governance | 15 min | Step 1 complete |
| Step 3: Branch protection | 30 min | Step 2 complete (need at least 1 commit on main) |
| Step 4: Add workflows | 1 hour | validate.py must exist; workflows written |
| Step 5: Configure secrets | 30 min | Tailscale IP confirmed; SSH key ready |
| Step 6: Webhooks | 30 min | Alusi gateway webhook handler must be implemented |

**Total estimated time:** 3-4 hours once Nathan creates the GitHub repos.

---

*Spec created: 2026-08-06 | Owner: Nathan Asiegbu | Governed by OPEN_EMPIRE_GOVERNANCE_BASELINE_V1.0.0*
