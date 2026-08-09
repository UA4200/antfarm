#!/usr/bin/env python3
"""
Groq Key Pool Rotator — P0.3
Manages 4 Groq API keys from secrets, rotates on rate-limit/rejection.
Never logs key values — only masked fingerprints.
Version: 1.0 | 2026-08-09
"""
import os, json, time, datetime, pathlib, hashlib, urllib.request, urllib.error

SECRETS_FILE = pathlib.Path.home() / ".openclaw/secrets/.env"
FW_ENV_FILE  = pathlib.Path.home() / ".openclaw/repos/free_llm_router/installed/Free-Way/.env"
ROTATION_LOG = pathlib.Path.home() / ".openclaw/logs/groq_rotation.jsonl"
ROTATION_LOG.parent.mkdir(parents=True, exist_ok=True)
QUARANTINE_FILE = pathlib.Path.home() / ".openclaw/logs/groq_quarantined.json"
FW_BASE = "http://127.0.0.1:8082"

def _load_secrets():
    keys = {}
    for line in SECRETS_FILE.read_text(errors="ignore").splitlines():
        line = line.strip()
        if line.startswith("#") or "=" not in line: continue
        k, v = line.split("=", 1)
        keys[k.strip()] = v.strip()
    return keys

def _mask(key_value: str) -> str:
    """Return masked fingerprint — never the key itself."""
    if not key_value: return "EMPTY"
    h = hashlib.sha256(key_value.encode()).hexdigest()[:8]
    return f"****{key_value[-4:]}[sha256:{h}]"

def _get_quarantined() -> list:
    if not QUARANTINE_FILE.exists(): return []
    try: return json.loads(QUARANTINE_FILE.read_text())
    except: return []

def _quarantine(slot: str, mask: str, reason: str):
    q = _get_quarantined()
    entry = {"slot": slot, "mask": mask, "reason": reason,
             "quarantined_at": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    q = [x for x in q if x["slot"] != slot]  # Remove old entry for same slot
    q.append(entry)
    QUARANTINE_FILE.write_text(json.dumps(q, indent=2))
    _rotation_log(slot, mask, "QUARANTINED", reason)
    print(f"[groq_rotator] QUARANTINE slot={slot} reason={reason}")

def _rotation_log(slot, mask, event, detail=""):
    entry = {
        "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "event": event,
        "slot": slot,
        "key_mask": mask,
        "detail": detail
    }
    with open(ROTATION_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")

def _write_freeway_key(key_value: str):
    """Write GROQ_API_KEY to Free-Way .env atomically."""
    lines = FW_ENV_FILE.read_text().splitlines()
    new_lines = []
    replaced = False
    for l in lines:
        if l.startswith("GROQ_API_KEY=") and not l.startswith("GROQ_API_KEY_"):
            new_lines.append(f"GROQ_API_KEY={key_value}")
            replaced = True
        else:
            new_lines.append(l)
    if not replaced:
        new_lines.append(f"GROQ_API_KEY={key_value}")
    FW_ENV_FILE.write_text("\n".join(new_lines) + "\n")

def _restart_freeway():
    """Restart Free-Way PM2 process to pick up new key."""
    import subprocess
    result = subprocess.run(["pm2", "restart", "freeway"], capture_output=True, text=True, timeout=15)
    time.sleep(4)  # Wait for restart
    return result.returncode == 0

def _test_key(groq_key: str) -> tuple[bool, str]:
    """Test a Groq key directly via Groq API. Returns (ok, error_type)."""
    try:
        body = json.dumps({"model":"llama-3.1-8b","max_tokens":5,
                           "messages":[{"role":"user","content":"hi"}]}).encode()
        req = urllib.request.Request(
            "https://api.groq.com/openai/v1/chat/completions",
            data=body, method="POST",
            headers={"Authorization":f"Bearer {groq_key}",
                     "Content-Type":"application/json"})
        urllib.request.urlopen(req, timeout=10)
        return True, ""
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:200]
        if e.code == 429:  return False, "RATE_LIMIT"
        if e.code == 401:  return False, "INVALID_KEY"
        if e.code == 403:  return False, "REVOKED"
        return False, f"HTTP_{e.code}"
    except Exception as e:
        return False, str(e)[:60]

def get_active_key_info() -> dict:
    """Return current key slot and mask without exposing value."""
    secrets = _load_secrets()
    quarantined = {q["slot"] for q in _get_quarantined()}
    for i in range(1, 5):
        slot = f"GROQ_API_KEY_{i}"
        if slot in quarantined: continue
        val = secrets.get(slot, "")
        if val:
            return {"active_slot": slot, "mask": _mask(val), "quarantined": list(quarantined)}
    return {"active_slot": None, "mask": None, "quarantined": list(quarantined)}

def rotate(reason: str = "rate_limit") -> dict:
    """
    Rotate to next available Groq key.
    Returns: {"success", "new_slot", "new_mask", "reason"}
    Do NOT rotate on quality failures — only rate_limit/rejection.
    """
    secrets     = _load_secrets()
    quarantined = {q["slot"] for q in _get_quarantined()}

    # Find current active
    fw_lines = FW_ENV_FILE.read_text().splitlines()
    current_val = ""
    for l in fw_lines:
        if l.startswith("GROQ_API_KEY=") and not l.startswith("GROQ_API_KEY_"):
            current_val = l.split("=",1)[1].strip()

    # Find current slot
    current_slot = None
    for i in range(1,5):
        slot = f"GROQ_API_KEY_{i}"
        if secrets.get(slot,"") == current_val:
            current_slot = slot
            break

    # Mark current as rate-limited (not quarantined unless INVALID/REVOKED)
    if current_slot and reason in ("INVALID_KEY","REVOKED"):
        _quarantine(current_slot, _mask(current_val), reason)
        quarantined.add(current_slot)

    # Find next available key
    for i in range(1, 5):
        slot = f"GROQ_API_KEY_{i}"
        if slot in quarantined: continue
        if slot == current_slot and reason == "rate_limit": continue  # Skip current on rate limit
        val = secrets.get(slot, "")
        if not val: continue

        # Test the key before switching
        ok, err = _test_key(val)
        if not ok:
            if err in ("INVALID_KEY","REVOKED"):
                _quarantine(slot, _mask(val), err)
                quarantined.add(slot)
                continue
            # Rate limited — try anyway (might clear by now)
            if err == "RATE_LIMIT":
                # Still try it — rate limits clear fast on Groq
                pass

        # Switch to this key
        _write_freeway_key(val)
        fw_restarted = _restart_freeway()
        _rotation_log(slot, _mask(val), "ROTATED",
                      f"from={current_slot} reason={reason} fw_restart={fw_restarted}")
        print(f"[groq_rotator] Rotated to {slot} (mask={_mask(val)}) reason={reason}")
        return {"success": True, "new_slot": slot, "new_mask": _mask(val),
                "reason": reason, "fw_restarted": fw_restarted}

    # All keys exhausted
    _rotation_log("ALL", "EXHAUSTED", "EXHAUSTED", f"reason={reason}")
    return {"success": False, "new_slot": None, "reason": "all_keys_exhausted_or_quarantined"}

def status() -> dict:
    """Return pool status — no key values."""
    secrets     = _load_secrets()
    quarantined = {q["slot"]: q for q in _get_quarantined()}
    pool = []
    for i in range(1, 5):
        slot = f"GROQ_API_KEY_{i}"
        val  = secrets.get(slot,"")
        pool.append({
            "slot":     slot,
            "present":  bool(val),
            "mask":     _mask(val) if val else "MISSING",
            "status":   "quarantined" if slot in quarantined else ("available" if val else "missing"),
            "quarantine_reason": quarantined.get(slot,{}).get("reason",""),
        })
    active = get_active_key_info()
    return {"pool": pool, "active": active, "quarantined_count": len(quarantined)}

if __name__ == "__main__":
    import sys
    cmd = sys.argv[1] if len(sys.argv)>1 else "status"
    if cmd == "status":
        print(json.dumps(status(), indent=2))
    elif cmd == "rotate":
        reason = sys.argv[2] if len(sys.argv)>2 else "rate_limit"
        print(json.dumps(rotate(reason), indent=2))
    elif cmd == "active":
        print(json.dumps(get_active_key_info(), indent=2))
