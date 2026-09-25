from pathlib import Path
import subprocess,json,datetime,hashlib
O=Path('/mnt/f/tools/math-audit-round10-20260925');R=Path('/mnt/f/LaTeX/BVE research')
Native=['/mnt/c/Users/HuangZY/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe','F:/tools/math-audit-round10-20260925/run_native_posix.py']
for Name in ['math-review','renewal-review']:
    D=json.loads((O/(Name+'-verified.json')).read_text())
    P=json.loads((O/(Name+'-packet.json')).read_text())
    if D['verdict']!='APPROVED' or D['packet_sha256']!=P['packet_sha256']:
        raise RuntimeError('Current exact review is not approved: '+Name)
for Name,Script in [('release-current-final','release_current_final.py'),('annotate-index','annotate_index.py'),('query-library','query_library.py')]:
    Log=O/(Name+'.log')
    if Log.exists():raise RuntimeError('Stage log already exists; inspect saved result and resume only missing work: '+str(Log))
    Args=Native+[str(O/Script)];Start=datetime.datetime.now(datetime.timezone.utc).isoformat()
    with Log.open('wb') as F:Result=subprocess.run(Args,cwd=R,stdout=F,stderr=subprocess.STDOUT)
    Row=dict(name=Name,argv=Args,started_utc=Start,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),exit_code=Result.returncode,log=str(Log),log_sha256=hashlib.sha256(Log.read_bytes()).hexdigest())
    with (O/'final-library-pipeline.jsonl').open('a') as F:F.write(json.dumps(Row)+'\n')
    print(Name,Result.returncode,flush=True)
    if Result.returncode:raise RuntimeError('Stage failed; inspect durable outputs before resuming: '+str(Log))
print('Current releases, annotations, index and actual retrieval complete.',flush=True)
