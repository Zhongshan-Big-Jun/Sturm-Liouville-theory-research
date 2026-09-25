from pathlib import Path
import datetime, hashlib, json, os, shutil, subprocess, sys, time, uuid

BASE = Path(__file__).resolve().parent
PROJECT = BASE / 'project'
LEAN = Path('/mnt/f/DevCache/elan/toolchains/leanprover--lean4---v4.31.0/bin/lean.exe')
LAKE = LEAN.with_name('lake.exe')
PLUGIN = Path('/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/lean-verify/2.0.1')
ORIGINAL = Path('/mnt/f/LaTeX/BVE research/lean-proof')

def digest(PathArg):
	with Path(PathArg).open('rb') as File:
		return hashlib.file_digest(File, 'sha256').hexdigest()

def write_json(PathArg, Value):
	Path(PathArg).write_text(json.dumps(Value, ensure_ascii=False, indent=2) + '\n')

def win(PathArg):
	return subprocess.check_output(['wslpath', '-w', str(Path(PathArg).resolve())], text=True).strip()

def environment(Extra=()):
	Env = os.environ.copy()
	Packages = json.loads((BASE / 'lake-manifest.json').read_text())['packages']
	Paths = [*Extra] + [ORIGINAL / '.lake/packages' / P['name'] / '.lake/build/lib/lean' for P in Packages]
	Env['LEAN_PATH'] = ';'.join(win(P) for P in Paths if Path(P).is_dir())
	Env['LEAN_SRC_PATH'] = ''
	Env['PYTHONDONTWRITEBYTECODE'] = '1'
	Temp = BASE / 'tmp'
	Temp.mkdir(exist_ok=True)
	Env['TMPDIR'] = str(Temp)
	Env['TEMP'] = Env['TMP'] = win(Temp)
	Keys = ('LEAN_PATH', 'LEAN_SRC_PATH', 'TEMP', 'TMP')
	Env['WSLENV'] = ':'.join([V for V in Env.get('WSLENV', '').split(':') if V and V.split('/')[0] not in Keys] + list(Keys))
	return Env

def run(Label, Args, Cwd=PROJECT, Inputs=(), Extra=()):
	if not Label.replace('-', '').replace('_', '').isalnum():
		raise ValueError('invalid immutable command label')
	Out = BASE / 'commands' / Label
	Out.mkdir(parents=True, exist_ok=False)
	Snap = Out / 'inputs'
	Snap.mkdir()
	Paths = list(dict.fromkeys([Path(__file__), *map(Path, Inputs)]))
	Before = {str(P): digest(P) for P in Paths}
	for I, P in enumerate(Paths):
		shutil.copyfile(P, Snap / f'{I:02d}-{P.name}')
	Env = environment(Extra)
	Record = {'command_id': str(uuid.uuid4()), 'label': Label, 'argv': list(map(str, Args)), 'cwd': str(Cwd),
		'role': 'independent_reviewer', 'packet_sha256': '96a6a726749351139af2db393e13a9fb267866eec0139df1cd556a3c97904423',
		'utc_start': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'inputs_before': Before,
		'environment': {K: Env.get(K) for K in ('LEAN_PATH', 'LEAN_SRC_PATH', 'WSLENV', 'TMPDIR', 'TEMP', 'TMP', 'PYTHONDONTWRITEBYTECODE')}}
	write_json(Out / 'command.json', Record)
	Start = time.monotonic()
	with (Out / 'stdout.log').open('wb') as Stdout, (Out / 'stderr.log').open('wb') as Stderr:
		Process = subprocess.Popen(Record['argv'], cwd=Cwd, env=Env, stdout=Stdout, stderr=Stderr)
		Record['pid'] = Process.pid
		write_json(Out / 'command.json', Record)
		Record['exit_code'] = Process.wait()
	Record.update(utc_end=datetime.datetime.now(datetime.timezone.utc).isoformat(), seconds=time.monotonic()-Start,
		inputs_after={str(P): digest(P) for P in Paths}, stdout_sha256=digest(Out / 'stdout.log'), stderr_sha256=digest(Out / 'stderr.log'))
	Record['inputs_unchanged'] = Record['inputs_before'] == Record['inputs_after']
	write_json(Out / 'command.json', Record)
	print(Label, Record['exit_code'], round(Record['seconds'], 3), flush=True)
	print((Out / 'stdout.log').read_text(errors='replace')[-4000:], end='', flush=True)
	print((Out / 'stderr.log').read_text(errors='replace')[-5000:], end='', flush=True)
	return Record

if __name__ == '__main__':
	Mode, Label = sys.argv[1:3]
	if Mode == 'version':
		Result = run(Label, [LEAN, '--version'], Inputs=[PROJECT / 'lean-toolchain'])
	elif Mode == 'compile':
		Source = PROJECT / (sys.argv[3] if len(sys.argv) > 3 else 'AuditRound11.lean')
		if not Source.resolve().is_relative_to(BASE):
			raise ValueError('source outside reviewer workspace')
		Object = BASE / 'objects' / Label / Source.with_suffix('.olean').name
		Object.parent.mkdir(parents=True, exist_ok=False)
		Extra = [BASE / 'objects' / V for V in sys.argv[4:]]
		Result = run(Label, [LEAN, '-R', win(PROJECT), '-o', win(Object), win(Source)], Inputs=[Source, PROJECT / 'lean-toolchain'], Extra=Extra)
	elif Mode == 'verify':
		Contract = BASE / sys.argv[3]
		Result = run(Label, [sys.executable, '-B', PLUGIN / 'scripts/verify_lean_project.py', '--project', PROJECT,
			'--contract', Contract, '--lean', LEAN, '--lake', LAKE, '--direct', '--strict-exit', '--build-timeout', '1800',
			'--output', BASE / 'evidence' / Label], Inputs=[Contract, PROJECT / 'AuditRound11.lean', PROJECT / 'lean-toolchain'])
	else:
		raise ValueError(Mode)
	sys.exit(Result['exit_code'])
