from pathlib import Path
import datetime,hashlib,json,os,shutil,subprocess,sys,time
ROOT=Path('/mnt/f/LaTeX/BVE research/lean-proof')
OUT=Path('/mnt/f/tools/math-audit-round5-20260921/lean-author')
LEAN=Path('/mnt/f/DevCache/elan/toolchains/leanprover--lean4---v4.31.0/bin/lean.exe')
SOURCE=ROOT/'SL/AuditRound5.lean'
CONFIGS=[ROOT/n for n in ['lean-toolchain','lakefile.lean','lake-manifest.json']]
def digest(p):
	with Path(p).open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()
def win(p): return subprocess.check_output(['wslpath','-w',str(p)],text=True).strip()
def environment():
	e=os.environ.copy()
	packages=json.loads((ROOT/'lake-manifest.json').read_text())['packages']
	paths=[OUT/'build']+[ROOT/'.lake/packages'/p['name']/'.lake/build/lib/lean' for p in packages]
	e['LEAN_PATH']=';'.join(map(win,paths))
	e['WSLENV']=':'.join([x for x in e.get('WSLENV','').split(':') if x and x.split('/')[0]!='LEAN_PATH']+['LEAN_PATH'])
	return e
def run(name,args,sources=()):
	log=OUT/'logs'/name
	assert not log.with_suffix('.json').exists(),name
	snap=OUT/'attempts'/name; snap.mkdir()
	sources=list(dict.fromkeys([*sources,*CONFIGS]))
	for i,p in enumerate(sources): shutil.copyfile(p,snap/f'{i:02d}-{p.name}')
	e=environment(); before={str(p):digest(p) for p in sources}
	r={'argv':args,'cwd':str(OUT),'cwd_windows':win(OUT),'utc_start':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_sha256_before':before,'runner_sha256':digest(__file__),'executable_sha256':digest(args[0]),'LEAN_PATH':e['LEAN_PATH'],'WSLENV':e['WSLENV']}
	log.with_suffix('.json').write_text(json.dumps(r,indent=2)+'\n')
	start=time.monotonic()
	with log.with_suffix('.stdout.txt').open('xb') as a,log.with_suffix('.stderr.txt').open('xb') as b:
		p=subprocess.Popen(args,cwd=OUT,env=e,stdout=a,stderr=b)
		r['pid']=p.pid;log.with_suffix('.json').write_text(json.dumps(r,indent=2)+'\n'); code=p.wait()
	r.update(exit_code=code,duration_seconds=time.monotonic()-start,utc_end=datetime.datetime.now(datetime.timezone.utc).isoformat(),source_sha256_after={str(p):digest(p) for p in sources})
	r['source_unchanged_during_run']=r['source_sha256_after']==before
	for s in ['stdout','stderr']:r[s+'_sha256']=digest(log.with_suffix('.'+s+'.txt'))
	if '-o' in args:
		obj=Path(subprocess.check_output(['wslpath','-u',args[args.index('-o')+1]],text=True).strip())
		if obj.exists():r['output_artifact']={'path':str(obj),'sha256':digest(obj)}
	log.with_suffix('.json').write_text(json.dumps(r,indent=2)+'\n')
	print(name,'exit',code,'seconds',round(r['duration_seconds'],2),flush=True)
	if code or '--version' in args:
		print(log.with_suffix('.stdout.txt').read_text(errors='replace'),end='')
		print(log.with_suffix('.stderr.txt').read_text(errors='replace'),end='')
	return code
if __name__=='__main__':
	name,mode=sys.argv[1:3]
	if mode=='build':
		obj=OUT/'build/SL/AuditRound5.olean'
		if obj.exists():
			p=OUT/'attempts'/(name+'-previous-artifact');p.mkdir();shutil.copyfile(obj,p/obj.name)
		args=[str(LEAN),'--root='+win(ROOT),'-o',win(obj),win(SOURCE)];src=[SOURCE]
	elif mode in ['probe','deps']:
		p=OUT/sys.argv[3];args=[str(LEAN)]+(['--deps'] if mode=='deps' else [])+[win(p)];src=[p,SOURCE,OUT/'build/SL/AuditRound5.olean']
	elif mode=='version': args=[str(LEAN),'--version'];src=[]
	else: raise SystemExit(mode)
	sys.exit(run(name,args,src))
