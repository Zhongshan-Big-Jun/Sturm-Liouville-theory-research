"""Round8 command receipts. Logging/environment pattern adapted from round7; see attribution.json."""
from pathlib import Path
import datetime, hashlib, json, os, shutil, subprocess, sys, time, uuid

BASE = Path(__file__).resolve().parent

def digest(path):
	with Path(path).open('rb') as f:
		return hashlib.file_digest(f, 'sha256').hexdigest()

def write_json(path, value):
	Path(path).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')

def win(path):
	p = Path(path).resolve()
	return str(p).replace('/mnt/' + str(p).split('/')[2] + '/', str(p).split('/')[2].upper() + ':\\', 1).replace('/', '\\') if str(p).startswith('/mnt/') else subprocess.check_output(['wslpath','-w',str(p)],text=True).strip()

def environment(output, extra=()):
	c = json.loads((BASE / 'runtime-config.json').read_text())
	e = os.environ.copy()
	e['LEAN_PATH'] = ';'.join([win(p) for p in extra] + [c['LEAN_PATH']])
	e['LEAN_SRC_PATH'] = ''
	e['WSLENV'] = ':'.join([v for v in e.get('WSLENV','').split(':') if v and v.split('/')[0] not in ('LEAN_PATH','LEAN_SRC_PATH','TEMP','TMP')] + ['LEAN_PATH','LEAN_SRC_PATH','TEMP','TMP'])
	tmp = Path(output).resolve()/'tmp'
	tmp.mkdir(parents=True,exist_ok=True)
	e['TMPDIR'] = str(tmp)
	e['TEMP'] = e['TMP'] = win(tmp)
	e['PYTHONDONTWRITEBYTECODE'] = '1'
	return e

def run(output, label, args, env, cwd, sources=(), artifacts=()):
	out=Path(output).resolve()
	logs=out/'logs'
	logs.mkdir(parents=True,exist_ok=True)
	prefix=logs/label
	if prefix.with_suffix('.json').exists():
		raise FileExistsError(prefix)
	snap=out/'attempts'/label
	snap.mkdir(parents=True)
	inputs=list(dict.fromkeys(Path(p).resolve() for p in sources))
	before={str(p):digest(p) for p in inputs}
	for i,p in enumerate(inputs): shutil.copyfile(p,snap/f'{i:02d}-{p.name}')
	rec={'run_id':str(uuid.uuid4()),'label':label,'argv':list(map(str,args)), 'cwd':str(cwd),
		'utc_start':datetime.datetime.now(datetime.timezone.utc).isoformat(),
		'environment':{k:env.get(k) for k in ('LEAN_PATH','LEAN_SRC_PATH','WSLENV','TMPDIR','TEMP','TMP','PYTHONDONTWRITEBYTECODE')},
		'inputs_before':before, 'runner_sha256':digest(__file__), 'executable_sha256':digest(args[0])}
	write_json(prefix.with_suffix('.json'),rec)
	start=time.monotonic()
	with prefix.with_suffix('.stdout.txt').open('xb') as so, prefix.with_suffix('.stderr.txt').open('xb') as se:
		p=subprocess.Popen(list(map(str,args)),cwd=cwd,env=env,stdout=so,stderr=se)
		rec['pid']=p.pid
		write_json(prefix.with_suffix('.json'),rec)
		rec['exit_code']=p.wait()
	rec.update(duration_seconds=time.monotonic()-start,utc_end=datetime.datetime.now(datetime.timezone.utc).isoformat(),inputs_after={str(p):digest(p) for p in inputs})
	rec['inputs_unchanged']=rec['inputs_before']==rec['inputs_after']
	for stream in ('stdout','stderr'): rec[stream+'_sha256']=digest(prefix.with_suffix('.'+stream+'.txt'))
	rec['artifacts']={str(p):digest(p) for p in map(Path,artifacts) if p.is_file()}
	write_json(prefix.with_suffix('.json'),rec)
	print(label,'exit',rec['exit_code'],'seconds',round(rec['duration_seconds'],2),flush=True)
	if rec['exit_code'] or '--version' in args:
		print(prefix.with_suffix('.stdout.txt').read_text(errors='replace'),end='',flush=True)
		print(prefix.with_suffix('.stderr.txt').read_text(errors='replace'),end='',flush=True)
	return rec

if __name__=='__main__':
	label=sys.argv[1]
	source=BASE/'AuditRound8.lean'
	out=BASE/'development'
	obj=out/label/'AuditRound8.olean'
	obj.parent.mkdir(parents=True,exist_ok=False)
	c=json.loads((BASE/'runtime-config.json').read_text())
	r=run(out,label,[c['lean'],'--root='+win(BASE),'-o',win(obj),win(source)],environment(out),BASE,[source,BASE/'run_lean.py',BASE/'runtime-config.json'],[obj])
	sys.exit(r['exit_code'])
