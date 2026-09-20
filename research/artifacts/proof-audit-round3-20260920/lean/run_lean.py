from pathlib import Path
import datetime
import hashlib
import json
import os
import subprocess
import sys
import time

PROJECT = Path('/mnt/f/LaTeX/BVE research/lean-proof')
OUT = Path('/mnt/f/tools/math-audit-round3-20260920/lean-author')
BIN = Path('/mnt/f/DevCache/elan/toolchains/leanprover--lean4---v4.31.0/bin')


def win_path(PathValue):
	return subprocess.check_output(['wslpath', '-w', str(PathValue)], text=True).strip()


def digest(PathValue):
	with Path(PathValue).open('rb') as Handle:
		return hashlib.file_digest(Handle, 'sha256').hexdigest()


def run(Name, Args, Sources):
	Log = OUT / 'logs' / Name
	if Log.with_suffix('.json').exists():
		raise SystemExit('Refusing to overwrite recorded run: ' + Name)
	Env = os.environ.copy()
	Paths = [OUT / 'final/build', OUT / 'build', PROJECT / '.lake/build/lib/lean']
	Packages = json.loads((PROJECT / 'lake-manifest.json').read_text())['packages']
	Paths += [PROJECT / '.lake/packages' / P['name'] / '.lake/build/lib/lean' for P in Packages]
	Env['LEAN_PATH'] = ';'.join(win_path(P) for P in Paths)
	Env['WSLENV'] = ':'.join([P for P in Env.get('WSLENV', '').split(':') if P and P.split('/')[0] != 'LEAN_PATH'] + ['LEAN_PATH'])
	Before = {str(P): digest(P) for P in Sources}
	Snapshot = OUT / 'attempts' / Name
	Snapshot.mkdir(parents=True, exist_ok=False)
	for Index, P in enumerate(Sources):
		(Snapshot / (str(Index) + '-' + P.name)).write_bytes(P.read_bytes())
	Record = {
		'argv': Args, 'cwd_wsl': str(PROJECT), 'cwd_windows': win_path(PROJECT),
		'utc_start': datetime.datetime.now(datetime.timezone.utc).isoformat(),
		'environment_overrides': {K: Env[K] for K in ['LEAN_PATH', 'WSLENV']},
		'other_lean_environment': {K: Env[K] for K in ['LEAN_SYSROOT', 'LEAN_SRC_PATH', 'ELAN_TOOLCHAIN'] if K in Env},
		'executable_sha256': digest(Args[0]), 'runner_sha256': digest(__file__),
		'source_sha256_before': Before,
	}
	Log.with_suffix('.json').write_text(json.dumps(Record, ensure_ascii=False, indent=2) + '\n')
	Start = time.monotonic()
	with Log.with_suffix('.stdout.txt').open('xb') as Stdout, Log.with_suffix('.stderr.txt').open('xb') as Stderr:
		Result = subprocess.run(Args, cwd=PROJECT, env=Env, stdout=Stdout, stderr=Stderr)
	Record.update(exit_code=Result.returncode, duration_seconds=time.monotonic() - Start,
		utc_end=datetime.datetime.now(datetime.timezone.utc).isoformat(),
		source_sha256_after={str(P): digest(P) for P in Sources})
	Record['source_unchanged_during_run'] = Record['source_sha256_before'] == Record['source_sha256_after']
	Record['stdout_sha256'] = digest(Log.with_suffix('.stdout.txt'))
	Record['stderr_sha256'] = digest(Log.with_suffix('.stderr.txt'))
	if '-o' in Args:
		Artifact = Path(subprocess.check_output(['wslpath', '-u', Args[Args.index('-o') + 1]], text=True).strip())
		if Artifact.exists():
			Record['output_artifact'] = {'path': str(Artifact), 'sha256': digest(Artifact)}
	Log.with_suffix('.json').write_text(json.dumps(Record, ensure_ascii=False, indent=2) + '\n')
	print(Name, 'exit', Result.returncode, 'seconds', round(Record['duration_seconds'], 2), flush=True)
	if Result.returncode or '--version' in Args:
		print(Log.with_suffix('.stdout.txt').read_text(errors='replace'), end='', flush=True)
		print(Log.with_suffix('.stderr.txt').read_text(errors='replace'), end='', flush=True)
	return Result.returncode


if __name__ == '__main__':
	Name, Mode = sys.argv[1:3]
	Source = PROJECT / 'SL/AuditRound3.lean'
	Configs = [PROJECT / N for N in ['lean-toolchain', 'lakefile.lean', 'lake-manifest.json']]
	if Mode in ['build', 'final-build']:
		Artifact = OUT / ('final/build' if Mode == 'final-build' else 'build') / 'SL/AuditRound3.olean'
		Artifact.parent.mkdir(parents=True, exist_ok=True)
		Args = [str(BIN / 'lean.exe'), '-o', win_path(Artifact), 'SL/AuditRound3.lean']
		Sources = [Source] + Configs
	elif Mode == 'probe':
		Probe = OUT / sys.argv[3]
		Args = [str(BIN / 'lean.exe'), win_path(Probe)]
		Sources = [Probe, Source] + Configs
	elif Mode == 'deps':
		Args = [str(BIN / 'lean.exe'), '--deps', 'SL/AuditRound3.lean']
		Sources = [Source] + Configs
	elif Mode == 'version':
		Args = [str(BIN / 'lean.exe'), '--version']
		Sources = Configs
	else:
		raise SystemExit('Unknown mode: ' + Mode)
	sys.exit(run(Name, Args, Sources))
