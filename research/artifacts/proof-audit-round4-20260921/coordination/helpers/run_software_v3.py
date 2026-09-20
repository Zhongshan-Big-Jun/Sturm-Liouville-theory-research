from pathlib import Path
import sys,subprocess,os,hashlib,json,datetime
Root=Path('/mnt/f/LaTeX/BVE research');Out=Path('/mnt/f/tools/math-audit-round4-20260921/scripts-revision3');Out.mkdir(exist_ok=True)
Source=Root/'scripts/d4_third_order_theory.py'; Before=hashlib.sha256(Source.read_bytes()).hexdigest()
Env=os.environ.copy();Env['PYTHONDONTWRITEBYTECODE']='1';Env['AUDIT_SOURCE_ROOT']=str(Root)
for Mode in ['normal','optimized']:
	for Kind,PathValue in [('program',Source),('behavior',Out/'behavior_checks.py')]:
		Name=Mode+'-'+Kind;Args=[sys.executable]+(['-O'] if Mode=='optimized' else [])+[str(PathValue)];Env['AUDIT_CHECK_OUTPUT']=str(Out/(Mode+'-behavior-results.json'))
		Record={'argv':Args,'source_sha256_before':Before,'utc_start':datetime.datetime.now(datetime.timezone.utc).isoformat()}
		with (Out/(Name+'.stdout.txt')).open('xb') as O,(Out/(Name+'.stderr.txt')).open('xb') as E:
			R=subprocess.run(Args,env=Env,cwd=Root,stdout=O,stderr=E,timeout=150)
		Record.update(exit_code=R.returncode,source_sha256_after=hashlib.sha256(Source.read_bytes()).hexdigest())
		(Out/(Name+'.json')).write_text(json.dumps(Record,indent=2)+'\n')
		assert R.returncode==0 and Record['source_sha256_after']==Before,Name
		print(Name,'PASS',flush=True)
print('Source',Before)
