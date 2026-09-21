from pathlib import Path
import datetime, hashlib, json, os, shutil, subprocess, sys, time

ROOT = Path('/mnt/f/LaTeX/BVE research/lean-proof')
OUT = Path(__file__).resolve().parent
LEAN = Path('/mnt/f/DevCache/elan/toolchains/leanprover--lean4---v4.31.0/bin/lean.exe')
CONFIGS = [ROOT / n for n in ('lean-toolchain', 'lakefile.lean', 'lake-manifest.json')]

def digest(path):
	with Path(path).open('rb') as f:
		return hashlib.file_digest(f, 'sha256').hexdigest()

def win(path):
	return subprocess.check_output(['wslpath', '-w', str(path)], text=True).strip()

def environment(extra=()):
	Env = os.environ.copy()
	Packages = json.loads((ROOT / 'lake-manifest.json').read_text())['packages']
	Paths = list(extra) + [ROOT / '.lake/packages' / p['name'] / '.lake/build/lib/lean' for p in Packages]
	assert all(p.is_dir() for p in extra)
	Paths = [p for p in Paths if p.is_dir()]
	Env['LEAN_PATH'] = ';'.join(map(win, Paths))
	Env['LEAN_SRC_PATH'] = ''
	Env['WSLENV'] = ':'.join([v for v in Env.get('WSLENV', '').split(':') if v and v.split('/')[0] not in ('LEAN_PATH', 'LEAN_SRC_PATH')] + ['LEAN_PATH', 'LEAN_SRC_PATH'])
	Env['PYTHONDONTWRITEBYTECODE'] = '1'
	return Env

def run(name, args, sources=(), extra=(), cwd=None):
	Logs = OUT / 'logs'
	Logs.mkdir(exist_ok=True)
	Log = Logs / name
	assert not Log.with_suffix('.json').exists(), name
	Snap = OUT / 'attempts' / name
	Snap.mkdir(parents=True)
	Sources = list(dict.fromkeys([*map(Path, sources), *CONFIGS]))
	for i, p in enumerate(Sources):
		shutil.copyfile(p, Snap / f'{i:02d}-{p.name}')
	Env = environment(extra)
	Before = {str(p): digest(p) for p in Sources}
	Record = dict(argv=args, cwd=str(cwd or OUT), cwd_windows=win(cwd or OUT), utc_start=datetime.datetime.now(datetime.timezone.utc).isoformat(), source_sha256_before=Before, runner_sha256=digest(__file__), executable_sha256=digest(args[0]), LEAN_PATH=Env['LEAN_PATH'], WSLENV=Env['WSLENV'])
	Log.with_suffix('.json').write_text(json.dumps(Record, indent=2) + '\n')
	Start = time.monotonic()
	with Log.with_suffix('.stdout.txt').open('xb') as a, Log.with_suffix('.stderr.txt').open('xb') as b:
		Process = subprocess.Popen(args, cwd=cwd or OUT, env=Env, stdout=a, stderr=b)
		Record['pid'] = Process.pid
		Log.with_suffix('.json').write_text(json.dumps(Record, indent=2) + '\n')
		Code = Process.wait()
	Record.update(exit_code=Code, duration_seconds=time.monotonic()-Start, utc_end=datetime.datetime.now(datetime.timezone.utc).isoformat(), source_sha256_after={str(p): digest(p) for p in Sources})
	Record['source_unchanged_during_run'] = Before == Record['source_sha256_after']
	for s in ('stdout', 'stderr'):
		Record[s + '_sha256'] = digest(Log.with_suffix('.' + s + '.txt'))
	if '-o' in args:
		Artifact = Path(subprocess.check_output(['wslpath', '-u', args[args.index('-o')+1]], text=True).strip())
		if Artifact.exists():
			Record['output_artifact'] = dict(path=str(Artifact), sha256=digest(Artifact))
	Log.with_suffix('.json').write_text(json.dumps(Record, indent=2) + '\n')
	print(name, 'exit', Code, 'seconds', round(Record['duration_seconds'], 2), flush=True)
	if Code or '--version' in args:
		print(Log.with_suffix('.stdout.txt').read_text(errors='replace'), end='')
		print(Log.with_suffix('.stderr.txt').read_text(errors='replace'), end='')
	return Code

if __name__ == '__main__':
	Name, Mode = sys.argv[1:3]
	if Mode == 'version':
		sys.exit(run(Name, [str(LEAN), '--version']))
	elif Mode == 'build':
		Module = sys.argv[3]
		Source = ROOT / ('SL/' + Module + '.lean')
		Library = OUT / 'builds' / Name
		(Library / 'SL').mkdir(parents=True)
		Extra = [Library]
		if Module != 'AuditRound5':
			Dependency = OUT / 'builds/04-dependency/SL/AuditRound5.olean'
			assert Dependency.is_file(), 'dependency compile has not completed'
			for Part in Dependency.parent.glob('AuditRound5.olean*'):
				shutil.copyfile(Part, Library / 'SL' / Part.name)
		Args = [str(LEAN), '--root=' + win(ROOT), '-o', win(Library / ('SL/' + Module + '.olean')), win(Source)]
		sys.exit(run(Name, Args, [Source, ROOT / 'SL/AuditRound5.lean'], extra=Extra))
	elif Mode in ('probe', 'deps'):
		Source = OUT / sys.argv[3]
		Extra = [OUT / 'builds' / n for n in sys.argv[4:]]
		Args = [str(LEAN)] + (['--deps'] if Mode == 'deps' else []) + [win(Source)]
		sys.exit(run(Name, Args, [Source], extra=Extra))
	else:
		raise SystemExit(Mode)
