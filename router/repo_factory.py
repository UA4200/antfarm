#!/usr/bin/env python3
"""
Open Empire Repository Factory — v1.0
Runs the governed lifecycle pipeline against a repository.
Usage: python3 repo_factory.py <repo_path_or_url> [--stage <stage>] [--all]

Stages: discover, hash, secret_scan, license, dependency, capability_fit, register, install, test, integrate
2026-08-09 | Authority: Nathan Asiegbu
"""
import os, sys, json, subprocess, pathlib, hashlib, datetime, re

HOME = pathlib.Path.home()
REGISTRY_PATH = HOME / ".openclaw/workspace/OPEN_EMPIRE_REPOSITORY_REGISTRY_V2.json"
KG_API = "http://127.0.0.1:6279"
LOG_DIR = HOME / ".openclaw/logs/repo_factory"
LOG_DIR.mkdir(parents=True, exist_ok=True)

KNOWN_SECRET_PATTERNS = [
    r'sk-[a-zA-Z0-9]{20,}',           # OpenAI
    r'gsk_[a-zA-Z0-9]{20,}',          # Groq
    r'ghp_[a-zA-Z0-9]{36}',           # GitHub PAT
    r'AIza[0-9A-Za-z\-_]{35}',        # Google
    r'AKIA[0-9A-Z]{16}',              # AWS
    r'xai-[a-zA-Z0-9]{30,}',          # xAI
]

APPROVED_LICENSES = {"MIT","Apache-2.0","BSD-2-Clause","BSD-3-Clause","ISC","Unlicense","CC0-1.0","WTFPL"}

def run(cmd, cwd=None, capture=True):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=capture, text=True, timeout=30, cwd=cwd)
        return r.returncode, (r.stdout or "").strip(), (r.stderr or "").strip()
    except subprocess.TimeoutExpired:
        return -1, "", "TIMEOUT"
    except Exception as e:
        return -1, "", str(e)

def log_event(repo_path, stage, result, details=""):
    entry = {"ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
             "repo": str(repo_path), "stage": stage, "result": result, "details": details[:200]}
    log_file = LOG_DIR / f"factory_{datetime.datetime.now().strftime('%Y%m%d')}.jsonl"
    with open(log_file, "a") as f:
        f.write(json.dumps(entry) + "\n")

# ── Stage 1: DISCOVER ─────────────────────────────────────────────────────────
def stage_discover(path):
    path = pathlib.Path(path).expanduser().resolve()
    if not path.exists():
        return {"stage": "discover", "status": "FAIL", "error": f"Path not found: {path}"}
    rc, remote, _ = run("git remote get-url origin", cwd=path)
    rc2, branch, _ = run("git rev-parse --abbrev-ref HEAD", cwd=path)
    rc3, commit, _ = run("git rev-parse --short HEAD", cwd=path)
    rc4, dirty_out, _ = run("git status --porcelain", cwd=path)
    dirty_count = len([l for l in dirty_out.splitlines() if l.strip()])
    name = path.name
    result = {
        "stage": "discover", "status": "PASS",
        "path": str(path), "name": name,
        "remote": remote or "NO_REMOTE",
        "branch": branch or "unknown",
        "commit": commit or "unknown",
        "dirty_files": dirty_count,
        "has_remote": bool(remote)
    }
    log_event(path, "discover", "PASS", f"remote={remote} branch={branch} dirty={dirty_count}")
    return result

# ── Stage 2: HASH ─────────────────────────────────────────────────────────────
def stage_hash(path):
    path = pathlib.Path(path).expanduser().resolve()
    rc, commit, _ = run("git rev-parse HEAD", cwd=path)
    config_files = list(path.glob("*.json")) + list(path.glob("*.toml")) + list(path.glob("*.yaml"))
    config_hash = hashlib.md5("".join(str(f) for f in config_files[:5]).encode()).hexdigest()[:8]
    result = {"stage": "hash", "status": "PASS", "commit_hash": commit, "config_hash": config_hash}
    log_event(path, "hash", "PASS")
    return result

# ── Stage 3: SECRET SCAN ──────────────────────────────────────────────────────
def stage_secret_scan(path):
    path = pathlib.Path(path).expanduser().resolve()
    findings = []
    scan_exts = [".py",".js",".ts",".json",".sh",".env",".yaml",".yml",".md"]
    for ext in scan_exts:
        for f in list(path.rglob(f"*{ext}"))[:50]:  # limit
            if ".git" in str(f): continue
            try:
                content = f.read_text(errors="ignore")
                for pattern in KNOWN_SECRET_PATTERNS:
                    if re.search(pattern, content):
                        findings.append({"file": str(f.relative_to(path)), "pattern": pattern[:20]})
            except: pass
    if findings:
        log_event(path, "secret_scan", "FAIL", f"{len(findings)} potential secrets")
        return {"stage":"secret_scan","status":"FAIL","findings":findings[:10],"error":"Potential secrets found — review before proceeding"}
    log_event(path, "secret_scan", "PASS")
    return {"stage":"secret_scan","status":"PASS","findings":[]}

# ── Stage 4: LICENSE CHECK ────────────────────────────────────────────────────
def stage_license(path):
    path = pathlib.Path(path).expanduser().resolve()
    license_file = None
    for name in ["LICENSE","LICENSE.md","LICENSE.txt","license"]:
        candidate = path / name
        if candidate.exists():
            license_file = candidate
            break
    if not license_file:
        return {"stage":"license","status":"WARNING","license":"UNKNOWN","approved":False,"note":"No LICENSE file found"}
    content = license_file.read_text(errors="ignore")[:500]
    detected = "UNKNOWN"
    for lic in APPROVED_LICENSES:
        if lic.lower().replace("-"," ") in content.lower() or lic in content:
            detected = lic; break
    if "mit" in content.lower(): detected = "MIT"
    elif "apache" in content.lower(): detected = "Apache-2.0"
    elif "bsd" in content.lower(): detected = "BSD"
    approved = detected in APPROVED_LICENSES or detected.startswith("BSD")
    log_event(path, "license", "PASS" if approved else "WARNING", f"license={detected}")
    return {"stage":"license","status":"PASS" if approved else "WARNING","license":detected,"approved":approved}

# ── Stage 5: DEPENDENCY ANALYSIS ─────────────────────────────────────────────
def stage_dependency(path):
    path = pathlib.Path(path).expanduser().resolve()
    deps = {}
    if (path/"package.json").exists():
        try:
            pj = json.loads((path/"package.json").read_text())
            deps["npm"] = list(pj.get("dependencies",{}).keys())[:10]
            deps["npm_dev"] = list(pj.get("devDependencies",{}).keys())[:5]
        except: pass
    if (path/"requirements.txt").exists():
        lines = (path/"requirements.txt").read_text().splitlines()
        deps["pip"] = [l.split("==")[0].split(">=")[0] for l in lines if l and not l.startswith("#")][:10]
    if (path/"pyproject.toml").exists():
        deps["pyproject"] = "present"
    manager = "npm" if "npm" in deps else ("pip" if "pip" in deps else "none")
    log_event(path, "dependency", "PASS", f"manager={manager}")
    return {"stage":"dependency","status":"PASS","package_manager":manager,"deps_sample":deps}

# ── Stage 6: CAPABILITY FIT ───────────────────────────────────────────────────
def stage_capability_fit(path):
    path = pathlib.Path(path).expanduser().resolve()
    name = path.name.lower()
    # Heuristic capability mapping
    cap_map = {
        "trading": "AUTONOMOUS_TRADING", "cashclaw": "AUTONOMOUS_TRADING",
        "polymarket": "AUTONOMOUS_TRADING", "kalshi": "AUTONOMOUS_TRADING",
        "router": "ADAPTIVE_ROUTING", "proxy": "ADAPTIVE_ROUTING", "freeway": "COST_OPTIMIZED_INFERENCE",
        "memory": "MEMORY_PIPELINE", "obsidian": "OBSIDIAN_HUMAN_VIEW",
        "kg": "KNOWLEDGE_GRAPH", "knowledge": "KNOWLEDGE_GRAPH",
        "n8n": "WORKFLOW_AUTOMATION", "workflow": "WORKFLOW_AUTOMATION",
        "mission": "WORKFLOW_AUTOMATION", "blco": "WORKFLOW_AUTOMATION",
        "skill": "TASK_OBSERVER", "observer": "TASK_OBSERVER",
        "antfarm": "WORKFLOW_AUTOMATION", "hermes": "MEMORY_PIPELINE",
    }
    capability = "UNKNOWN"
    for keyword, cap in cap_map.items():
        if keyword in name: capability = cap; break
    log_event(path, "capability_fit", "PASS", f"capability={capability}")
    return {"stage":"capability_fit","status":"PASS","mapped_capability":capability,"note":"heuristic — verify manually for non-obvious repos"}

# ── Stage 7: REGISTER ─────────────────────────────────────────────────────────
def stage_register(path, discovery_data):
    """Register repo in the registry file — idempotent."""
    path = pathlib.Path(path).expanduser().resolve()
    if not REGISTRY_PATH.exists():
        return {"stage":"register","status":"WARNING","note":"Registry file not found"}
    try:
        registry = json.loads(REGISTRY_PATH.read_text())
        repos = registry.get("repositories", [])
        existing = [r for r in repos if r.get("path") == str(path)]
        if existing:
            log_event(path, "register", "PASS", "already_registered")
            return {"stage":"register","status":"PASS","note":"Already registered","action":"none"}
        new_entry = {
            "id": len(repos)+1,
            "path": str(path),
            "name": path.name,
            "remote": discovery_data.get("remote","unknown"),
            "branch": discovery_data.get("branch","unknown"),
            "commit": discovery_data.get("commit","unknown"),
            "dirty_files": discovery_data.get("dirty_files",0),
            "classification": "INTAKE_COPY",
            "status": "active",
            "registered_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
        repos.append(new_entry)
        registry["repositories"] = repos
        registry["summary"]["total"] = len(repos)
        REGISTRY_PATH.write_text(json.dumps(registry, indent=2))
        log_event(path, "register", "PASS", "new_entry")
        return {"stage":"register","status":"PASS","note":"Registered as INTAKE_COPY"}
    except Exception as e:
        return {"stage":"register","status":"FAIL","error":str(e)}

# ── Main pipeline runner ──────────────────────────────────────────────────────
def run_pipeline(path, stages=None):
    all_stages = ["discover","hash","secret_scan","license","dependency","capability_fit","register"]
    selected = stages or all_stages
    results = {"repo": str(path), "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(), "stages": []}
    discovery_data = {}

    for stage in selected:
        if stage == "discover":      r = stage_discover(path)
        elif stage == "hash":        r = stage_hash(path)
        elif stage == "secret_scan": r = stage_secret_scan(path)
        elif stage == "license":     r = stage_license(path)
        elif stage == "dependency":  r = stage_dependency(path)
        elif stage == "capability_fit": r = stage_capability_fit(path)
        elif stage == "register":    r = stage_register(path, discovery_data)
        else: r = {"stage": stage, "status": "SKIP", "note": "stage not implemented"}

        results["stages"].append(r)
        if stage == "discover": discovery_data = r
        if r.get("status") == "FAIL": break  # Stop on failure

    failed = [s for s in results["stages"] if s.get("status") == "FAIL"]
    warned = [s for s in results["stages"] if s.get("status") == "WARNING"]
    results["overall_status"] = "FAIL" if failed else ("WARNING" if warned else "PASS")
    results["failed_stages"] = [s["stage"] for s in failed]
    return results


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Open Empire Repository Factory")
    parser.add_argument("path", nargs="?", default=".", help="Repository path")
    parser.add_argument("--stage", nargs="*", help="Run specific stages only")
    parser.add_argument("--all-repos", action="store_true", help="Run against all known repos in registry")
    args = parser.parse_args()

    if args.all_repos and REGISTRY_PATH.exists():
        registry = json.loads(REGISTRY_PATH.read_text())
        repos = registry.get("repositories", [])
        print(f"Running factory on {len(repos)} repos...")
        summary = {"total": len(repos), "pass": 0, "fail": 0, "warn": 0}
        for repo in repos:
            rpath = repo.get("path","")
            if pathlib.Path(rpath).exists():
                result = run_pipeline(rpath, args.stage)
                status = result["overall_status"]
                summary[status.lower() if status in ("PASS","FAIL") else "warn"] += 1
                print(f"  [{status}] {repo['name']}")
            else:
                print(f"  [SKIP] {repo.get('name','?')} — path not found")
        print(f"\nSummary: {summary}")
    else:
        result = run_pipeline(args.path, args.stage)
        print(json.dumps(result, indent=2))
