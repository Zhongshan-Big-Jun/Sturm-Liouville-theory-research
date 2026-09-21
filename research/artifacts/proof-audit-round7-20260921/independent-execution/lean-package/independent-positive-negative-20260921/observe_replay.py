#!/usr/bin/env python3
"""Launch the unmodified replay with independent process/artifact observations."""
from pathlib import Path
import json, os, subprocess, time
from executor import BASE, RUN, digest, pointer, save, stamp

argv=['python3','-B','lean-package/replay.py',str(RUN/'replay')]
logs=RUN/'executor-logs';logs.mkdir(exist_ok=True)
receipt=logs/'lean-replay.json'
if receipt.exists() or (RUN/'replay').exists():
    raise RuntimeError('must use a previously nonexistent replay destination')
preflight=json.loads((RUN/'preflight.json').read_text())
baseline=json.loads((RUN/'runtime-before.json').read_text())
if not (preflight['all_declared_hashes_match'] and preflight['runtime_leanpath_matches_config'] and preflight['python']['matches_frozen_python'] and preflight['mathlib_head']['match'] and all(x['stable_during_hash'] for x in baseline['artifacts'])):
    raise RuntimeError('preflight failed; do not execute replacement inputs')
for row in preflight['checks']:
    if digest(row['path'])!=row['expected_sha256']:
        raise RuntimeError('input changed since preflight: '+row['path'])
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(RUN/'tmp'))
(RUN/'tmp').mkdir(exist_ok=True)
rec={'argv':argv,'cwd':str(BASE),'started_at_utc':stamp(),'observer':pointer(__file__),'collector_library':pointer(RUN/'executor.py'),'python':pointer(Path('/usr/bin/python3').resolve()),'replay_directory_existed_before':False,'observations':'Linux child-process cmdline and stat observations; not a Windows syscall/open-file trace.'}
save(receipt,rec)
seen=set();artifacts={};started=time.monotonic()
with (logs/'lean-replay.stdout.log').open('xb') as out,(logs/'lean-replay.stderr.log').open('xb') as err,(logs/'lean-replay.observations.jsonl').open('x') as events:
    proc=subprocess.Popen(argv,cwd=BASE,env=env,stdout=out,stderr=err)
    rec['pid']=proc.pid;save(receipt,rec)
    print('started lean replay pid',proc.pid,flush=True)
    def event(obj):
        events.write(json.dumps({'utc':stamp(),'elapsed_seconds':time.monotonic()-started,**obj},ensure_ascii=False)+'\n');events.flush()
    while True:
        pending=[proc.pid];visit=set()
        while pending:
            pid=pending.pop()
            if pid in visit: continue
            visit.add(pid)
            p=Path('/proc')/str(pid)
            try:
                args=[s.decode(errors='replace') for s in (p/'cmdline').read_bytes().split(b'\0') if s]
                identity=(pid,tuple(args))
                if identity not in seen:
                    seen.add(identity);event({'kind':'process','pid':pid,'argv':args})
                pending += [int(s) for s in (p/'task'/str(pid)/'children').read_text().split()]
            except OSError: pass
        for branch in ('positive','negative'):
            for obj in (RUN/'replay'/branch/'lean-verification-runs').glob('*/lib/SL/AuditRound7.olean*'):
                st=obj.stat();identity=(st.st_size,st.st_mtime_ns)
                if artifacts.get(str(obj)) != identity:
                    artifacts[str(obj)]=identity
                    event({'kind':'candidate_artifact_observed','path':str(obj),'bytes':st.st_size,'mtime_ns':st.st_mtime_ns})
        code=proc.poll()
        if code is not None: break
        time.sleep(0.2)
rec.update(returncode=code,ended_at_utc=stamp(),elapsed_seconds=time.monotonic()-started,distinct_process_observations=len(seen),candidate_artifacts={p:pointer(p) for p in artifacts})
for s in ('stdout','stderr'):
    rec[s]=pointer(logs/('lean-replay.'+s+'.log'))
rec['observations_file']=pointer(logs/'lean-replay.observations.jsonl')
save(receipt,rec)
print('finished lean replay exit',code,'seconds',round(rec['elapsed_seconds'],2),'observed process identities',len(seen),flush=True)
raise SystemExit(code)
