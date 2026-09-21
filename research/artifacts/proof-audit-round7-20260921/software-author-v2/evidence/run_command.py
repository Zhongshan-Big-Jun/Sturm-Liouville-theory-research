"""Append-only author process receipts; no expected status is rewritten."""
import argparse, datetime, hashlib, json, os
from pathlib import Path
import subprocess, sys, time

base = Path(__file__).resolve().parents[1]
p = argparse.ArgumentParser()
p.add_argument('--cwd', required=True)
p.add_argument('--name', required=True)
p.add_argument('argv', nargs=argparse.REMAINDER)
a = p.parse_args()
cwd = (base / a.cwd).resolve()
out = base / 'evidence' / 'executions' / a.name
if not cwd.is_relative_to(base) or not out.resolve().is_relative_to(base):
    raise RuntimeError('outside author directory')
out.mkdir(parents=True, exist_ok=False)
argv = a.argv[1:] if a.argv[:1] == ['--'] else a.argv
manifest = json.loads((cwd / 'manifest.json').read_text())
paths = [cwd / rel for rel in manifest['package_files']]
paths += [cwd / 'manifest.json', cwd / 'manifest.sha256']
def hashes():
    return {str(path.relative_to(cwd)): hashlib.sha256(path.read_bytes()).hexdigest() for path in paths}
before = hashes()
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
start = time.monotonic()
env = os.environ.copy()
env.update(PYTHONDONTWRITEBYTECODE='1', OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1')
with (out / 'stdout.txt').open('wb') as stdout, (out / 'stderr.txt').open('wb') as stderr:
    proc = subprocess.Popen(argv, cwd=cwd, env=env, stdout=stdout, stderr=stderr)
    timed_out = False
    try:
        status = proc.wait(timeout=400)
    except subprocess.TimeoutExpired:
        proc.kill(); status = proc.wait(); timed_out = True
receipt = dict(argv=argv, cwd=str(cwd), pid=proc.pid, started_utc=started,
    finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    seconds=time.monotonic()-start, exit_code=status, timed_out=timed_out,
    input_sha256_before=before, input_sha256_after=hashes(),
    streams={name:hashlib.sha256((out/name).read_bytes()).hexdigest() for name in ('stdout.txt','stderr.txt')})
receipt['inputs_unchanged'] = receipt['input_sha256_before'] == receipt['input_sha256_after']
(out / 'receipt.json').write_text(json.dumps(receipt, indent=2)+'\n')
print(json.dumps({k:receipt[k] for k in ('argv','cwd','pid','seconds','exit_code','inputs_unchanged')}), flush=True)
print((out / 'stdout.txt').read_text()[-3000:])
print((out / 'stderr.txt').read_text()[-3000:], file=sys.stderr)
sys.exit(status)
