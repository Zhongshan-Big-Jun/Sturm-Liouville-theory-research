from pathlib import Path
import datetime
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time

Root = Path('/mnt/f/LaTeX/BVE research')
Out = Path('/mnt/f/tools/math-audit-round12-20260926')
Artifact = Root / 'research/artifacts/proof-audit-round12-20260926'
Environment = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', OPENBLAS_NUM_THREADS='1')
Replay = Out / 'submitted-replay'
Records = []
for Optimized in [False, True]:
	Name = 'optimized' if Optimized else 'normal'
	Command = [sys.executable, '-B', *(['-O'] if Optimized else []), str(Replay / 'checks.py')]
	Started = datetime.datetime.now(datetime.timezone.utc).isoformat()
	Timer = time.monotonic()
	with (Replay / (Name + '.actual.log')).open('wb') as Log:
		Result = subprocess.run(Command, cwd=Replay, env=Environment, stdout=Log, stderr=subprocess.STDOUT)
	Records.append(dict(kind='supplied_excerpt_replay', command=Command, cwd=str(Replay), started_utc=Started, seconds=time.monotonic()-Timer, exit_code=Result.returncode))
	if Result.returncode:
		raise RuntimeError('Supplied replay failed: ' + Name)
Full = Out / 'whole-old-source'
(Full / 'scripts').mkdir(parents=True, exist_ok=True)
Names = ['_gapn2_half_problem_probe.py', '_gapn2_symmetry_recon.py', '_gapn2_jacobian_probe.py', '_gapn2_jacobian_analytic.py', '_gapn2_sector_decomposition.py', '_sl_prufer.py', 'reflection_seeds.py']
Sources = {}
for Name in Names:
	Source = Artifact / 'before/scripts' / Name
	if not Source.exists():
		Source = Root / 'scripts' / Name
	Data = Source.read_bytes()
	(Full / 'scripts' / Name).write_bytes(Data)
	Sources[Name] = hashlib.sha256(Data).hexdigest()
Code = '''import sys, json, warnings
import numpy as np
sys.path.insert(0, 'scripts')
import _gapn2_half_problem_probe as H
hb = [(0.5, 100.0)]
cases = {bc + str(n): H.half_spectrum(hb, bc, N=n) for bc in ('D','N') for n in (4,80,160)}
mu = cases['N160'][1]
with warnings.catch_warnings(record=True) as ws:
 warnings.simplefilter('always')
 value = H._spectral_green(hb, mu, 1, 'N', 0.1, 0.1, N=80)
if not (np.isposinf(value) and np.where(cases['N80'] == mu)[0].tolist() == [3]):
 raise RuntimeError('Whole source counterexample did not reproduce')
result = dict(source_module=H.__file__, roots={k:v[:6].tolist() for k,v in cases.items()}, target=float(mu), actual_index=np.where(cases['N80'] == mu)[0].tolist(), removed_index=1, result=str(value), warnings=[str(w.message) for w in ws], scope='Whole original module execution; finite counterexample')
print(json.dumps(result, indent=2))
'''
(Full / 'reproduce.py').write_text(Code)
with (Full / 'stdout.json').open('wb') as Stdout, (Full / 'stderr.log').open('wb') as Stderr:
	Result = subprocess.run([sys.executable, '-B', 'reproduce.py'], cwd=Full, env=Environment, stdout=Stdout, stderr=Stderr)
Records.append(dict(kind='whole_old_module_replay', exit_code=Result.returncode, sources=Sources, root=str(Full)))
if Result.returncode:
	raise RuntimeError('Whole source counterexample failed')
Target = Artifact / 'intake-replay'
Target.mkdir(exist_ok=True)
for Name in ['normal.actual.log', 'optimized.actual.log', 'evidence/checks_normal.json', 'evidence/checks_optimized.json', 'evidence/green_sector.json']:
	Path = Target / Name
	Path.parent.mkdir(parents=True, exist_ok=True)
	shutil.copyfile(Replay / Name, Path)
shutil.copytree(Full, Target / 'whole-old-source')
(Target / 'execution.json').write_text(json.dumps(Records, indent=2) + '\n')
print(json.dumps(dict(status='PASS', excerpt_checks=[json.loads((Replay / 'evidence' / ('checks_' + N + '.json')).read_text())['count'] for N in ['normal','optimized']], whole_source_bug_reproduced=True)), flush=True)
