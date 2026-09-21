"""Reviewer-owned bounded subprocess capture; never edits frozen inputs."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

OWN = Path(__file__).resolve().parent
ROOT = OWN.parent
PACKET = json.loads((ROOT / 'PACKET.json').read_text())
INITIAL = json.loads((OWN / 'initial-hashes.json').read_text())

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def frozen_hashes():
    return {p: sha(ROOT / p) for p in INITIAL['files']}

def package_hashes(base):
    return {p: sha(base / p) for p in PACKET['files']}

def create_copy(name):
    dest = OWN / name
    dest.mkdir(exist_ok=False)
    for rel in PACKET['files']:
        src = ROOT / rel
        if not src.resolve().is_relative_to(ROOT) or src.is_symlink():
            raise RuntimeError('unsafe packet path: ' + rel)
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, target)
    if package_hashes(dest) != PACKET['files']:
        raise RuntimeError('copy mismatch')
    return dest

def capture(name, cwd, argv, expected, package=None, extra_env=None):
    out = OWN / 'executions' / name
    out.mkdir(parents=True, exist_ok=False)
    before = frozen_hashes()
    if before != {p: v['actual_sha256'] for p, v in INITIAL['files'].items()}:
        raise RuntimeError('frozen input changed before execution')
    env = os.environ.copy()
    env.update(PYTHONDONTWRITEBYTECODE='1', OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', PYTHONUTF8='1')
    if extra_env:
        env.update(extra_env)
    receipt = dict(argv=argv, cwd=str(cwd), expected_exit=expected,
                   started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                   frozen_input_sha256_before=before, runner_sha256=sha(Path(__file__)),
                   environment_selected={k:env.get(k) for k in ('PYTHONPATH','PYTHONNOUSERSITE','PYTHONOPTIMIZE','PYTHONDONTWRITEBYTECODE','OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','PYTHONUTF8')})
    if package:
        receipt['package_input_sha256_before'] = package_hashes(package)
    t = time.monotonic()
    with (out/'stdout.txt').open('wb') as stdout, (out/'stderr.txt').open('wb') as stderr:
        proc = subprocess.Popen(argv, cwd=cwd, env=env, stdout=stdout, stderr=stderr)
        receipt['pid'] = proc.pid
        receipt['exit_code'] = proc.wait()
    receipt.update(seconds=time.monotonic()-t, frozen_input_sha256_after=frozen_hashes(),
                   stdout_sha256=sha(out/'stdout.txt'), stderr_sha256=sha(out/'stderr.txt'))
    if package:
        receipt['package_input_sha256_after'] = package_hashes(package)
        receipt['package_unchanged'] = receipt['package_input_sha256_before'] == receipt['package_input_sha256_after']
        receipt['generated_output_sha256'] = {p.relative_to(package).as_posix():sha(p) for p in sorted(package.rglob('*')) if p.is_file() and p.relative_to(package).as_posix() not in PACKET['files']}
    receipt['frozen_unchanged'] = receipt['frozen_input_sha256_before'] == receipt['frozen_input_sha256_after']
    receipt['matches_expected_exit'] = receipt['exit_code'] == expected
    (out/'receipt.json').write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps({k:receipt[k] for k in ('argv','pid','exit_code','expected_exit','seconds','frozen_unchanged','matches_expected_exit')}), flush=True)
    return receipt

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['normal','optimized'])
    args = parser.parse_args()
    package = create_copy('package-' + args.mode)
    flags = ['-B'] + (['-O'] if args.mode == 'optimized' else [])
    capture('verify-' + args.mode, package,
            [sys.executable, *flags, str(package/'regression/verify_package.py')], 0, package)
    capture('replay-' + args.mode, package,
            [sys.executable, *flags, str(package/'regression/replay.py'), '--label', 'independent-review-'+args.mode], 0, package)

if __name__ == '__main__':
    main()
