from pathlib import Path
import datetime
import hashlib
import json
import os
import subprocess
import sys
import time

Root = Path('/mnt/f/LaTeX/BVE research')
Out = Path('/mnt/f/tools/math-audit-round12-20260926')
Name = sys.argv[1]
Cases = {**{'half-' + Mode: ['_gapn2_half_problem_probe.py', '4', Mode, '80'] for Mode in ['sup', 'inf']}, **{'raw-' + Mode: ['_gapn2_rawko_closed.py', '4', Mode, '80'] for Mode in ['sup','inf']}, 'green-inertia': ['_gapn2_green_inertia_probe.py']}
Args = Cases[Name.removesuffix('-final')]
Target = Out / 'repaired-runs' / Name
Target.mkdir(parents=True, exist_ok=False)
Sources = ['_sl_prufer.py', '_gapn2_half_problem_probe.py', '_gapn2_jacobian_probe.py', '_gapn2_symmetry_recon.py', '_gapn2_jacobian_analytic.py', '_gapn2_sector_decomposition.py', '_gapn2_rawko_closed.py', '_gapn2_green_inertia_probe.py', 'reflection_seeds.py', 'op03_gap_table.json']
Before = {Name: hashlib.sha256((Root / 'scripts' / Name).read_bytes()).hexdigest() for Name in Sources}
Command = [sys.executable, '-B', 'scripts/' + Args[0], *Args[1:]]
Record = dict(command=Command, cwd=str(Root), started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), source_before=Before, status='RUNNING', scope='Actual coordinator finite CLI execution; not independent review or interval certification')
def save():
	(Target / 'execution.json').write_text(json.dumps(Record, indent=2) + '\n')
save()
Timer = time.monotonic()
with (Target / 'stdout.log').open('wb') as Output, (Target / 'stderr.log').open('wb') as Error:
	Process = subprocess.Popen(Command, cwd=Root, env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1', OPENBLAS_NUM_THREADS='1'), stdout=Output, stderr=Error)
	Record['pid'] = Process.pid
	save()
	Code = Process.wait()
After = {Name: hashlib.sha256((Root / 'scripts' / Name).read_bytes()).hexdigest() for Name in Sources}
Record.update(exit_code=Code, source_after=After, unchanged=Before == After, seconds=time.monotonic()-Timer, status='COMPLETED' if Code == 0 and Before == After else 'FAILED')
save()
print(json.dumps(dict(name=Name, exit_code=Code, unchanged=Before == After, seconds=Record['seconds'])), flush=True)
raise SystemExit(Code or (0 if Before == After else 1))
