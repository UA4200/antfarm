#!/usr/bin/env python3
"""
Task Observer Collector — Open Empire
Reads skill-observations/*.jsonl, groups patterns, generates skill_workshop proposals.
Runs weekly (via cron). Never auto-modifies protected domains.
"""
import json, pathlib, datetime, collections

OBS_DIR = pathlib.Path.home() / '.openclaw/workspace/skill-observations'
PROPOSALS_DIR = pathlib.Path.home() / '.openclaw/workspace/skill-proposals'
OBS_DIR.mkdir(exist_ok=True)
PROPOSALS_DIR.mkdir(exist_ok=True)

PROTECTED_DOMAINS = {'constitution','kelly','capital','financial','security','approval','governance','trading','cashclaw'}

def is_governance_domain(text):
    return any(d in text.lower() for d in PROTECTED_DOMAINS)

def collect():
    now = datetime.datetime.now(datetime.timezone.utc)
    cutoff = now - datetime.timedelta(days=7)
    observations = []
    for f in OBS_DIR.glob('*.jsonl'):
        for line in f.read_text().splitlines():
            try:
                obs = json.loads(line)
                ts = datetime.datetime.fromisoformat(obs.get('ts','2000-01-01'))
                if ts > cutoff:
                    observations.append(obs)
            except: pass
    
    # Group by (task_type, pattern)
    groups = collections.defaultdict(list)
    for obs in observations:
        key = (obs.get('task_type','?'), obs.get('pattern','?'))
        groups[key].append(obs)
    
    proposals = []
    for (task_type, pattern), obs_list in groups.items():
        if len(obs_list) < 3: continue  # Need 3+ occurrences
        if is_governance_domain(pattern): 
            # Write to governance observations, not proposals
            gov_path = pathlib.Path.home() / '.openclaw/vault/governance_observations.jsonl'
            gov_path.parent.mkdir(exist_ok=True)
            with open(gov_path,'a') as f:
                f.write(json.dumps({'ts':now.isoformat(),'pattern':pattern,'count':len(obs_list),'domain':'GOVERNANCE_HUMAN_ONLY'})+'\n')
            continue
        
        outcomes = [o.get('outcome','?') for o in obs_list]
        fail_count = outcomes.count('fail') + outcomes.count('friction')
        
        proposals.append({
            'ts': now.isoformat(),
            'task_type': task_type,
            'pattern': pattern,
            'occurrence_count': len(obs_list),
            'failure_count': fail_count,
            'proposal_type': 'update_skill' if fail_count > 0 else 'codify_success',
            'status': 'PENDING_REVIEW',
            'governance_domain': False
        })
    
    if proposals:
        ts_str = now.strftime('%Y%m%d_%H%M%S')
        out = PROPOSALS_DIR / f'proposals_{ts_str}.json'
        out.write_text(json.dumps(proposals, indent=2))
        print(f'[task_observer] Generated {len(proposals)} proposals → {out}')
    else:
        print(f'[task_observer] No patterns with 3+ occurrences in last 7 days ({len(observations)} observations)')
    
    return proposals

if __name__ == '__main__':
    collect()
