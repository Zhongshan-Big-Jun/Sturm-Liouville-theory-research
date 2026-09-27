"""Persist exact commands, stdout/stderr, exit codes and hashes outside the repo."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

parser = argparse.ArgumentParser()
parser.add_argument('mode', choices=('normal', 'optimized'))
args = parser.parse_args()
here = Path(__file__).resolve().parent
results = []
for script in ('reproduce_before.py', 'test_rigid1d.py'):
    command = [sys.executable, '-B']
    if args.mode == 'optimized':
        command.append('-O')
    command.append(str(here/script))
    log = here/f'{Path(script).stem}.{args.mode}.log'
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    timer = time.monotonic()
    print(f'RUN {command}', flush=True)
    with log.open('w') as stream:
        result = subprocess.run(command, cwd=here, stdout=stream, stderr=subprocess.STDOUT)
    record = {'command': command, 'cwd': str(here), 'started_utc': started,
              'elapsed_seconds': time.monotonic()-timer, 'exit_code': result.returncode,
              'log': str(log), 'sha256': hashlib.sha256(log.read_bytes()).hexdigest()}
    results.append(record)
    (here/f'run_results.{args.mode}.json').write_text(json.dumps(results, indent=2)+'\n')
    print(json.dumps(record), flush=True)
    print('\n'.join(log.read_text().splitlines()[-12:]), flush=True)
sys.exit(0 if all(item['exit_code'] == 0 for item in results) else 1)
