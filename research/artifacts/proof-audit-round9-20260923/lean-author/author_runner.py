from pathlib import Path
import datetime, hashlib, json, os, shutil, subprocess, sys, time, uuid
BASE = Path(__file__).resolve().parent
PROJECT = BASE / 'project'
LEAN = Path('/mnt/f/DevCache/elan/toolchains/leanprover--lean4---v4.31.0/bin/lean.exe')
LAKE = LEAN.with_name('lake.exe')
PLUGIN = Path('/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/lean-verify/2.0.1')
ORIGINAL = Path('/mnt/f/LaTeX/BVE research/lean-proof')
def digest(p):
	with Path(p).open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()
def write_json(p,v):
	Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def win(p):
	return subprocess.check_output(['wslpath','-w',str(Path(p).resolve())],text=True).strip()
def environment(extra=()):
	e=os.environ.copy()
	packages=json.loads((ORIGINAL/'lake-manifest.json').read_text())['packages']
	paths=[*extra]+[ORIGINAL/'.lake/packages'/p['name']/'.lake/build/lib/lean' for p in packages]
	e['LEAN_PATH']=';'.join(win(p) for p in paths if Path(p).is_dir())
	e['LEAN_SRC_PATH']=''
	e['PYTHONDONTWRITEBYTECODE']='1'
	tmp=BASE/'tmp';tmp.mkdir(exist_ok=True)
	e['TMPDIR']=str(tmp);e['TEMP']=e['TMP']=win(tmp)
	keys=('LEAN_PATH','LEAN_SRC_PATH','TEMP','TMP')
	e['WSLENV']=':'.join([v for v in e.get('WSLENV','').split(':') if v and v.split('/')[0] not in keys]+list(keys))
	return e

def run(label,args,cwd=PROJECT,inputs=(),extra=()):
	out=BASE/'commands'/label;out.mkdir(parents=True,exist_ok=False)
	snap=out/'inputs';snap.mkdir()
	paths=list(dict.fromkeys([Path(__file__),*map(Path,inputs)]))
	before={str(p):digest(p) for p in paths}
	for i,p in enumerate(paths):shutil.copyfile(p,snap/f'{i:02d}-{p.name}')
	e=environment(extra)
	rec={'command_id':str(uuid.uuid4()),'label':label,'argv':list(map(str,args)),'cwd':str(cwd),
		'author_thread_id':os.environ.get('CODEX_THREAD_ID'),'inherited_session_id':os.environ.get('CODEX_SESSION_ID'),
		'utc_start':datetime.datetime.now(datetime.timezone.utc).isoformat(),'inputs_before':before,
		'environment':{k:e.get(k) for k in ('LEAN_PATH','LEAN_SRC_PATH','WSLENV','TMPDIR','TEMP','TMP','PYTHONDONTWRITEBYTECODE')}}
	write_json(out/'command.json',rec);start=time.monotonic()
	with (out/'stdout.log').open('wb') as so,(out/'stderr.log').open('wb') as se:
		p=subprocess.Popen(rec['argv'],cwd=cwd,env=e,stdout=so,stderr=se)
		rec['pid']=p.pid;write_json(out/'command.json',rec)
		rec['exit_code']=p.wait()
	rec.update(utc_end=datetime.datetime.now(datetime.timezone.utc).isoformat(),seconds=time.monotonic()-start,
		inputs_after={str(p):digest(p) for p in paths},stdout_sha256=digest(out/'stdout.log'),stderr_sha256=digest(out/'stderr.log'))
	rec['inputs_unchanged']=rec['inputs_before']==rec['inputs_after'];write_json(out/'command.json',rec)
	print(label,rec['exit_code'],round(rec['seconds'],3),flush=True)
	print((out/'stdout.log').read_text(errors='replace')[-18000:],end='',flush=True)
	print((out/'stderr.log').read_text(errors='replace')[-5000:],end='',flush=True)
	return rec

if __name__=='__main__':
	mode,label=sys.argv[1:3]
	if mode=='compile':
		source=PROJECT/(sys.argv[3] if len(sys.argv)>3 else 'AuditRound9.lean')
		obj=BASE/'development'/label/source.with_suffix('.olean').name;obj.parent.mkdir(parents=True,exist_ok=False)
		r=run(label,[LEAN,'-R',win(PROJECT),'-o',win(obj),win(source)],inputs=[source,PROJECT/'lean-toolchain'])
	elif mode=='verify':
		contract=BASE/sys.argv[3]
		r=run(label,[sys.executable,'-B',PLUGIN/'scripts/verify_lean_project.py','--project',PROJECT,'--contract',contract,'--lean',LEAN,'--lake',LAKE,'--direct','--strict-exit','--build-timeout','1800','--output',BASE/'evidence'/label],inputs=[contract,PROJECT/'AuditRound9.lean',PROJECT/'lean-toolchain'])
	elif mode=='version':
		r=run(label,[LEAN,'--version'],inputs=[PROJECT/'lean-toolchain'])
	else: raise ValueError(mode)
	sys.exit(r['exit_code'])
