from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys, time
PROJECT = Path('/mnt/f/LaTeX/BVE research/lean-proof')
OUT = Path('/mnt/f/tools/math-audit-round2-20260920/lean-author')
BIN = Path('/mnt/f/DevCache/elan/toolchains/leanprover--lean4---v4.31.0/bin')

def win_path(p):
	return subprocess.check_output(['wslpath', '-w', str(p)], text=True).strip()

def digest(p):
	return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def run(name, args, sources=(), env_extra=None):
	log = OUT / 'logs' / name
	if log.with_suffix('.json').exists():
		raise SystemExit('Refusing to overwrite a recorded run: ' + name)
	env = os.environ.copy()
	paths = [OUT / 'build', PROJECT / '.lake/build/lib/lean']
	packages = json.loads((PROJECT / 'lake-manifest.json').read_text())['packages']
	paths += [PROJECT / '.lake/packages' / p['name'] / '.lake/build/lib/lean' for p in packages]
	env['LEAN_PATH'] = ';'.join(win_path(p) for p in paths)
	env['WSLENV'] = ':'.join([e for e in env.get('WSLENV', '').split(':') if e and e.split('/')[0] != 'LEAN_PATH'] + ['LEAN_PATH'])
	if env_extra:
		env.update(env_extra)
	before = {str(p): digest(p) for p in sources}
	snap = OUT / 'attempts' / name
	snap.mkdir(parents=True, exist_ok=False)
	for p in sources:
		(snap / Path(p).name).write_bytes(Path(p).read_bytes())
	record = {'argv': args, 'cwd': str(PROJECT), 'utc_start': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'LEAN_PATH': env['LEAN_PATH'], 'WSLENV': env['WSLENV'], 'source_sha256_before': before}
	log.with_suffix('.json').write_text(json.dumps(record, ensure_ascii=False, indent=2))
	t = time.monotonic()
	with log.with_suffix('.stdout.txt').open('wb') as stdout, log.with_suffix('.stderr.txt').open('wb') as stderr:
		result = subprocess.run(args, cwd=PROJECT, env=env, stdout=stdout, stderr=stderr)
	record.update(exit_code=result.returncode, duration_seconds=time.monotonic()-t, utc_end=datetime.datetime.now(datetime.timezone.utc).isoformat(), source_sha256_after={str(p):digest(p) for p in sources})
	record['source_unchanged_during_run'] = record['source_sha256_before'] == record['source_sha256_after']
	record['stdout_sha256'] = digest(log.with_suffix('.stdout.txt'))
	record['stderr_sha256'] = digest(log.with_suffix('.stderr.txt'))
	if '-o' in args:
		path = subprocess.check_output(['wslpath', '-u', args[args.index('-o')+1]], text=True).strip()
		if Path(path).exists(): record['output_artifact'] = {'path': path, 'sha256': digest(path)}
	log.with_suffix('.json').write_text(json.dumps(record, ensure_ascii=False, indent=2))
	print(name, 'exit', result.returncode, 'seconds', round(record['duration_seconds'], 2), flush=True)
	print(log.with_suffix('.stdout.txt').read_text(errors='replace'), end='', flush=True)
	print(log.with_suffix('.stderr.txt').read_text(errors='replace'), end='', flush=True)
	return result.returncode

if __name__ == '__main__':
	name, relative = sys.argv[1:3]
	source = PROJECT / relative
	output = OUT / 'build' / Path(relative).with_suffix('.olean')
	output.parent.mkdir(parents=True, exist_ok=True)
	sys.exit(run(name, [str(BIN / 'lean.exe'), '-o', win_path(output), relative], [source]))
