#!/usr/bin/env bash
# Phase 7 — PR Merge + Release Tagging
# ⚠️  GATED — run ONLY after Nathan issues: APPROVE PHASE7 MERGE <sha>
# Directive: PR14-264d22c | Host: Ugos-Mac-mini.lan
set -euo pipefail

GH_TOKEN=$(grep -A5 'github.com:' ~/.config/gh/hosts.yml | grep 'oauth_token' | awk '{print $2}')

echo "=== PHASE 7: Merge + Tag ==="
echo "Timestamp: $(date)"
echo "Gate: Phase 6 must have passed (all G1-G8 green at T+24h)"
echo ""

# Merge order: governance first, then products
# Format: "repo:pr_number:branch"
MERGE_PRS=(
  "alusi-core:1:feature/wp-001-governance-and-control-stack"
  "open-empire-core:1:feature/wp-002-mega-blocks-and-empire-audits"
  "git-github:15:feature/wp-003-phase-reports-and-component-ledger"
)

# open-empire-core WP-007 branch
MERGE_BRANCHES=(
  "open-empire-core:feature/wp-007-empire-directory"
)

echo "--- Step 1: Merge draft PRs to main ---"
for entry in "${MERGE_PRS[@]}"; do
  repo=$(echo $entry | cut -d: -f1)
  pr=$(echo $entry | cut -d: -f2)
  echo "Merging UA4200/$repo PR #$pr..."
  RESULT=$(curl -s -X PUT \
    -H "Authorization: token $GH_TOKEN" \
    -H "Content-Type: application/json" \
    "https://api.github.com/repos/UA4200/$repo/pulls/$pr/merge" \
    -d "{\"merge_method\":\"squash\",\"commit_title\":\"${repo}: deploy 2026-07-30 (Phase 7 merge)\"}" \
    | python3 -c "import sys,json; d=json.load(sys.stdin); print('merged='+str(d.get('merged','?')),'sha='+d.get('sha','?')[:12])")
  echo "  $RESULT"
  sleep 2
done

echo ""
echo "--- Step 2: Tag all repos v0.1.0-deploy-20260730 ---"
for repo in alusi-core open-empire-core git-github mission-control antfarm blco-pipeline; do
  SHA=$(curl -s -H "Authorization: token $GH_TOKEN" \
    "https://api.github.com/repos/UA4200/$repo/git/ref/heads/main" \
    | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('object',{}).get('sha','?')[:12])" 2>/dev/null)

  RESULT=$(curl -s -X POST \
    -H "Authorization: token $GH_TOKEN" \
    "https://api.github.com/repos/UA4200/$repo/releases" \
    -d "{\"tag_name\":\"v0.1.0-deploy-20260730\",\"name\":\"Open Empire Deploy 2026-07-30\",\"body\":\"Initial GitHub governance deployment. Directive: PR14-264d22c\\nSHA: ${SHA}\\nHost: Ugos-Mac-mini.lan\",\"draft\":false,\"prerelease\":false}" \
    | python3 -c "import sys,json; d=json.load(sys.stdin); print('tag='+d.get('tag_name','err'), 'url='+d.get('html_url','?')[:70])")
  echo "  $repo: $RESULT"
  sleep 1
done

echo ""
echo "=== Phase 7 complete ==="
echo "All repos merged to main and tagged v0.1.0-deploy-20260730"
echo "Update PHASE7_RELEASE_MANIFEST with merge SHAs and mark status DEPLOYED"
