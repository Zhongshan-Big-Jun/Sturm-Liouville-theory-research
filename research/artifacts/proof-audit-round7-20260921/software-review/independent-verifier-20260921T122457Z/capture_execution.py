"""Reviewer-owned execution capture; no candidate/harness changes."""
from pathlib import Path
import datetime,hashlib,json,os,shlex,subprocess,sys,time
ROOT=Path(__file__).resolve().parent.parent
OWN=Path(__file__).resolve().parent
label=sys.argv[1]; argv=sys.argv[2:]
if argv[:1]==['--']:argv=argv[1:]
folder=OWN/label;folder.mkdir()
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def inputs():
    pkt=json.loads((ROOT/'PACKET.json').read_text())
    return {'PACKET.json':digest(ROOT/'PACKET.json'),**{rel:digest(ROOT/rel) for rel in pkt['files']}}
before=inputs()
env=os.environ.copy()
removed=[]
for key in ('PYTHONPATH','PYTHONHOME','PYTHONSTARTUP','PYTHONUSERBASE'):
    if key in env:removed.append(key);env.pop(key)
(OWN/'runtime-tmp').mkdir(exist_ok=True)
overrides=dict(PYTHONDONTWRITEBYTECODE='1',PYTHONNOUSERSITE='1',PYTHONUTF8='1',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',TMPDIR=str(OWN/'runtime-tmp'),MPLCONFIGDIR=str(OWN/'runtime-tmp'))
env.update(overrides)
record={'role':'independent verifier actual execution','argv':argv,'command':shlex.join(argv),'cwd':str(ROOT),'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'input_sha256_before':before,'environment_overrides':overrides,'removed_environment_names':removed,'python_executable_sha256':digest(Path('/usr/bin/python3')),'stdout':str(folder/'stdout.txt'),'stderr':str(folder/'stderr.txt')}
(folder/'receipt.json').write_text(json.dumps({**record,'status':'running'},indent=2)+'\n')
print('RUNNING '+record['command'],flush=True)
start=time.monotonic()
with (folder/'stdout.txt').open('wb') as so,(folder/'stderr.txt').open('wb') as se:
    try:
        proc=subprocess.run(argv,cwd=ROOT,env=env,stdout=so,stderr=se,timeout=900)
        code=proc.returncode;timed_out=False
    except subprocess.TimeoutExpired:
        code=124;timed_out=True
record.update(seconds=time.monotonic()-start,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='completed',exit_code=code,timed_out=timed_out,input_sha256_after=inputs(),stdout_sha256=digest(folder/'stdout.txt'),stderr_sha256=digest(folder/'stderr.txt'),capture_script_sha256=digest(Path(__file__)))
record['inputs_unchanged']=record['input_sha256_before']==record['input_sha256_after']
for line in (folder/'stdout.txt').read_text(errors='replace').splitlines():
    if line.startswith('Replay directory: '):record['replay_directory']=line.split(': ',1)[1]
(folder/'receipt.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({k:record[k] for k in ['argv','cwd','exit_code','seconds','inputs_unchanged','stdout','stderr']},indent=2),flush=True)
print((folder/'stdout.txt').read_text(errors='replace'),flush=True)
print((folder/'stderr.txt').read_text(errors='replace'),file=sys.stderr,flush=True)
sys.exit(code)
