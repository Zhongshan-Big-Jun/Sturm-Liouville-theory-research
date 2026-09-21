"""Local author compile helper. All writes stay below this directory."""
from pathlib import Path
import datetime, hashlib, json, os, shutil, subprocess, sys, time

BASE = Path(__file__).resolve().parent
ROOT = Path('/mnt/f/LaTeX/BVE research/lean-proof')
LEAN = Path('/mnt/f/DevCache/elan/toolchains/leanprover--lean4---v4.31.0/bin/lean.exe')

def digest(path):
	with Path(path).open('rb') as File:
		return hashlib.file_digest(File, 'sha256').hexdigest()

def write_json(path, value):
	Path(path).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')

def win(path):
	return subprocess.check_output(['wslpath', '-w', str(path)], text=True).strip()

def environment(extra=()):
	Packages = json.loads((ROOT / 'lake-manifest.json').read_text())['packages']
	Paths = list(map(Path, extra)) + [ROOT / '.lake/packages' / P['name'] / '.lake/build/lib/lean' for P in Packages]
	Paths = [P for P in Paths if P.is_dir()]
	Env = os.environ.copy()
	Env['LEAN_PATH'] = ';'.join(map(win, Paths))
	Env['LEAN_SRC_PATH'] = ''
	Env['WSLENV'] = ':'.join([V for V in Env.get('WSLENV', '').split(':') if V and V.split('/')[0] not in ('LEAN_PATH', 'LEAN_SRC_PATH', 'TEMP', 'TMP')] + ['LEAN_PATH', 'LEAN_SRC_PATH', 'TEMP', 'TMP'])
	Env['PYTHONDONTWRITEBYTECODE'] = '1'
	Temp = BASE / 'tmp'
	Temp.mkdir(exist_ok=True)
	Env['TMPDIR'] = str(Temp)
	Env['TEMP'] = Env['TMP'] = win(Temp)
	return Env

def run(output, label, args, env, cwd, sources=()):
	Output = Path(output).resolve()
	if not Output.is_relative_to(BASE):
		raise ValueError('Output must stay within the authorized lean-author directory')
	Logs = Output / 'logs'
	Logs.mkdir(parents=True, exist_ok=True)
	Prefix = Logs / label
	if Prefix.with_suffix('.json').exists():
		raise FileExistsError(Prefix)
	Snapshot = Output / 'attempts' / label
	Snapshot.mkdir(parents=True)
	Sources = list(dict.fromkeys(map(Path, sources)))
	Before = {str(P): digest(P) for P in Sources}
	for I, P in enumerate(Sources):
		shutil.copyfile(P, Snapshot / f'{I:02d}-{P.name}')
	Record = dict(argv=list(map(str, args)), cwd=str(cwd), utc_start=datetime.datetime.now(datetime.timezone.utc).isoformat(), environment={K:env.get(K) for K in ('LEAN_PATH', 'LEAN_SRC_PATH', 'WSLENV', 'PYTHONDONTWRITEBYTECODE', 'TMPDIR', 'TEMP', 'TMP')}, source_sha256_before=Before, helper_sha256=digest(__file__), executable_sha256=digest(args[0]))
	write_json(Prefix.with_suffix('.json'), Record)
	Start = time.monotonic()
	with Prefix.with_suffix('.stdout.txt').open('xb') as Stdout, Prefix.with_suffix('.stderr.txt').open('xb') as Stderr:
		Process = subprocess.Popen(list(map(str, args)), cwd=cwd, env=env, stdout=Stdout, stderr=Stderr)
		Record['pid'] = Process.pid
		write_json(Prefix.with_suffix('.json'), Record)
		Record['exit_code'] = Process.wait()
	Record.update(duration_seconds=time.monotonic()-Start, utc_end=datetime.datetime.now(datetime.timezone.utc).isoformat(), source_sha256_after={str(P):digest(P) for P in Sources})
	Record['inputs_unchanged'] = Before == Record['source_sha256_after']
	for Stream in ('stdout', 'stderr'):
		Record[Stream + '_sha256'] = digest(Prefix.with_suffix('.' + Stream + '.txt'))
	if '-o' in args:
		Object = Path(subprocess.check_output(['wslpath', '-u', str(args[args.index('-o')+1])], text=True).strip())
		if Object.exists():
			Record['output_artifact'] = dict(path=str(Object), sha256=digest(Object))
	write_json(Prefix.with_suffix('.json'), Record)
	print(label, 'exit', Record['exit_code'], 'seconds', round(Record['duration_seconds'], 2), flush=True)
	if Record['exit_code'] or '--version' in args:
		print(Prefix.with_suffix('.stdout.txt').read_text(errors='replace'), end='', flush=True)
		print(Prefix.with_suffix('.stderr.txt').read_text(errors='replace'), end='', flush=True)
	return Record

if __name__ == '__main__':
	Label = sys.argv[1]
	Source = BASE / 'snapshot/SL/AuditRound7.lean'
	Object = BASE / 'development' / Label / 'SL/AuditRound7.olean'
	Object.parent.mkdir(parents=True, exist_ok=False)
	Args = [str(LEAN), '--root=' + win(BASE / 'snapshot'), '-o', win(Object), win(Source)]
	Sources = [Source, BASE / 'run_lean.py'] + [ROOT / N for N in ('lean-toolchain', 'lakefile.lean', 'lake-manifest.json')]
	sys.exit(run(BASE / 'development', Label, Args, environment(), BASE / 'snapshot', Sources)['exit_code'])
