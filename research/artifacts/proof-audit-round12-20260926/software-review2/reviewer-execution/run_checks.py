"""Execute bounded frozen commands and preserve every result."""
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import time

audit = Path(__file__).resolve().parent
root = audit / 'payload'
cases = [
    ('candidate-normal', ['-B', 'check_repair.py', str(root)]),
    ('candidate-optimized', ['-B', '-O', 'check_repair.py', str(root)]),
    ('half-sup', ['-B', 'scripts/_gapn2_half_problem_probe.py', '4', 'sup', '80']),
    ('half-inf', ['-B', 'scripts/_gapn2_half_problem_probe.py', '4', 'inf', '80']),
    ('rawko-sup', ['-B', 'scripts/_gapn2_rawko_closed.py', '4', 'sup', '80']),
    ('rawko-inf', ['-B', 'scripts/_gapn2_rawko_closed.py', '4', 'inf', '80']),
    ('green-inertia', ['-B', 'scripts/_gapn2_green_inertia_probe.py']),
]
if len(sys.argv) > 1:
    cases = [(Path(sys.argv[1]).stem, ['-B', str(Path(sys.argv[1]).resolve())])]
for name, args in cases:
    env = os.environ.copy()
    env.update(PYTHONPATH=str(audit / 'hooks'), PYTHONDONTWRITEBYTECODE='1',
               REVIEW_EVIDENCE_ROOT=str(audit),
               REVIEW_ORIGINS_OUTPUT=str(audit / 'logs' / (name + '-origins.json')),
               OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1')
    command = [sys.executable, *args]
    record = {'name': name, 'argv': command, 'cwd': str(root),
              'started_utc': datetime.now(timezone.utc).isoformat()}
    start = time.monotonic()
    with (audit / 'logs' / (name + '.stdout')).open('w') as out, (audit / 'logs' / (name + '.stderr')).open('w') as err:
        try:
            result = subprocess.run(command, cwd=root, env=env, stdout=out, stderr=err, timeout=180)
            record['returncode'] = result.returncode
        except subprocess.TimeoutExpired:
            record['returncode'] = None
            record['timeout_seconds'] = 180
    record['elapsed_seconds'] = time.monotonic() - start
    record['ended_utc'] = datetime.now(timezone.utc).isoformat()
    origins = audit / 'logs' / (name + '-origins.json')
    record['project_isolation_pass'] = json.loads(origins.read_text())['project_isolation_pass'] if origins.exists() else False
    (audit / 'logs' / (name + '-run.json')).write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps(record), flush=True)
