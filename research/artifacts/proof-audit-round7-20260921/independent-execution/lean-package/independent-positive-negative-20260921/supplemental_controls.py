#!/usr/bin/env python3
"""Execute unmodified negative inputs after the supplied replay's retained failure."""
from pathlib import Path
import json, os, subprocess, time
from executor import BASE,RUN,digest,pointer,save,stamp,run
config=json.loads((BASE/'lean-package/runtime-config.json').read_text())
pre=json.loads((RUN/'preflight.json').read_text())
for row in pre['checks']:
    if digest(row['path'])!=row['expected_sha256']:
        raise RuntimeError('frozen input changed; do not continue: '+row['path'])
positive=json.loads((RUN/'replay/positive/run-manifest.json').read_text())
library=Path(positive['evidence']['run_directory'])/'lib'
win=lambda p:subprocess.check_output(['wslpath','-w',str(p)],cwd=BASE,text=True).strip()
temp=RUN/'tmp';temp.mkdir(exist_ok=True)
os.environ.update(PYTHONDONTWRITEBYTECODE='1',LEAN_PATH=config['LEAN_PATH'],LEAN_SRC_PATH='',TMPDIR=str(temp),TEMP=win(temp),TMP=win(temp))
os.environ['WSLENV']=':'.join([x for x in os.environ.get('WSLENV','').split(':') if x and x.split('/')[0] not in ('LEAN_PATH','LEAN_SRC_PATH','TEMP','TMP')]+['LEAN_PATH','LEAN_SRC_PATH','TEMP','TMP'])
output=RUN/'supplemental-negative'
if output.exists(): raise RuntimeError('supplemental negative destination already exists')
settings={'driver':pointer(__file__),'collector':pointer(RUN/'executor.py'),'runtime_config':pointer(BASE/'lean-package/runtime-config.json'),'environment':{k:os.environ[k] for k in ('LEAN_PATH','LEAN_SRC_PATH','WSLENV','PYTHONDONTWRITEBYTECODE','TMPDIR','TEMP','TMP')},'negative_destination_existed':False,'purpose':'Original replay failed at its generated inspection; preserve that failure and separately execute original negative contracts/control.'}
save(RUN/'supplemental-configuration.json',settings)
os.environ['LEAN_PATH']=win(library)+';'+config['LEAN_PATH']
code=run('supplemental-wrong-mirror-factor',[config['lean'],win(BASE/'lean-package/controls/WrongMirrorFactor.lean')])
print('mirror-factor expected rejection exit',code,flush=True)
contract=json.loads((BASE/'lean-package/wrong-target-contract.json').read_text())
wrong=RUN/'WrongTargetExact.lean'
wrong.write_text('import SL.AuditRound7\nexample : '+contract['expected_type']+' := '+contract['declaration']+'\n')
code=run('supplemental-wrong-target-native',[config['lean'],win(wrong)])
print('wrong-target native expected rejection exit',code,flush=True)
os.environ['LEAN_PATH']=config['LEAN_PATH']
argv=['python3','-B',config['verifier'],'--project',str(BASE/'lean-package/snapshot'),'--direct','--lean',config['lean'],'--lake',config['lake'],'--strict-exit','--build-timeout','1800','--contract',str(BASE/'lean-package/wrong-target-contract.json'),'--output',str(output)]
logs=RUN/'executor-logs';label='supplemental-wrong-target-verifier';receipt=logs/(label+'.json')
rec={'argv':argv,'cwd':str(BASE),'started_at_utc':stamp(),'driver':pointer(__file__),'verifier':pointer(config['verifier']),'contract':pointer(BASE/'lean-package/wrong-target-contract.json'),'output_previously_absent':True,'configuration':pointer(RUN/'supplemental-configuration.json')}
save(receipt,rec);seen=set();artifacts={};start=time.monotonic()
with (logs/(label+'.stdout.log')).open('xb') as out,(logs/(label+'.stderr.log')).open('xb') as err,(logs/(label+'.observations.jsonl')).open('x') as events:
    p=subprocess.Popen(argv,cwd=BASE,env=os.environ.copy(),stdout=out,stderr=err)
    rec['pid']=p.pid;save(receipt,rec);print('started wrong-target verifier pid',p.pid,flush=True)
    def event(obj):
        events.write(json.dumps({'utc':stamp(),'seconds':time.monotonic()-start,**obj})+'\n');events.flush()
    while True:
        pending=[p.pid];visited=set()
        while pending:
            pid=pending.pop()
            if pid in visited: continue
            visited.add(pid);proc=Path('/proc')/str(pid)
            try:
                args=[s.decode(errors='replace') for s in (proc/'cmdline').read_bytes().split(b'\0') if s]
                key=(pid,tuple(args))
                if key not in seen: seen.add(key);event({'kind':'process','pid':pid,'argv':args})
                pending.extend(int(x) for x in (proc/'task'/str(pid)/'children').read_text().split())
            except OSError: pass
        for f in output.glob('lean-verification-runs/*/lib/SL/AuditRound7.olean*'):
            st=f.stat();key=(st.st_size,st.st_mtime_ns)
            if artifacts.get(str(f))!=key:
                artifacts[str(f)]=key;event({'kind':'candidate_artifact_observed','path':str(f),'bytes':st.st_size,'mtime_ns':st.st_mtime_ns})
        code=p.poll()
        if code is not None: break
        time.sleep(.2)
rec.update(returncode=code,ended_at_utc=stamp(),seconds=time.monotonic()-start,process_observation_count=len(seen))
for stream in ('stdout','stderr'):
    rec[stream]=pointer(logs/(label+'.'+stream+'.log'))
rec['observations_file']=pointer(logs/(label+'.observations.jsonl'))
save(receipt,rec)
print('finished wrong-target verifier exit',code,'seconds',round(rec['seconds'],2),flush=True)
raise SystemExit(code)
