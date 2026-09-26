from pathlib import Path
import datetime, hashlib,json,os,subprocess,sys,time
base=Path(__file__).resolve().parent.parent
root=base/'inputs'
name=sys.argv[1]
cmd=[sys.executable,'-B']+sys.argv[2:]
env=os.environ.copy()
env['PYTHONPATH']=str(base/'evidence/hook')
env['PYTHONDONTWRITEBYTECODE']='1'
env['OPENBLAS_NUM_THREADS']='1'
env['OMP_NUM_THREADS']='1'
env['R12_ORIGIN_FILE']=str(base/'evidence'/f'{name}.origins.json')
def hashes(): return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()}
pre=hashes(); started=datetime.datetime.now(datetime.timezone.utc).isoformat(); t=time.monotonic()
r=subprocess.run(cmd,cwd=root,env=env,capture_output=True,text=True)
meta=dict(argv=cmd,cwd=str(root),start_utc=started,seconds=time.monotonic()-t,returncode=r.returncode,source_sha256_before=pre,source_sha256_after=hashes())
(base/'evidence'/f'{name}.stdout.txt').write_text(r.stdout)
(base/'evidence'/f'{name}.stderr.txt').write_text(r.stderr)
(base/'evidence'/f'{name}.run.json').write_text(json.dumps(meta,indent=2))
print(json.dumps({k:v for k,v in meta.items() if not k.startswith('source_')}))
if name.startswith('candidate') and r.returncode==0:
    v=json.loads(r.stdout)
    print(json.dumps({k:v[k] for k in ['status','optimized','count']}))
    print(json.dumps([x for x in v['checks'] if x['name'].startswith('full-J')]))
else: print(r.stdout)
if r.stderr: print('STDERR:',r.stderr)
