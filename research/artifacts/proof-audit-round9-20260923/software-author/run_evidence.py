"""Author execution ledger with explicit cwd, command, exit and output hashes."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

BASE = Path(__file__).resolve().parent
REPO = Path('/mnt/f/LaTeX/BVE research')
ENV = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1', 'OPENBLAS_NUM_THREADS': '1', 'OMP_NUM_THREADS': '1'}
CANDIDATE = BASE / '_gapn2_second_variation_probe.py'


def run(Job):
	Name, Arguments, Expected = Job
	Command = [sys.executable, '-B'] + Arguments
	Log = BASE / (Name + '.log')
	Start = time.monotonic()
	with Log.open('w') as Handle:
		Completed = subprocess.run(Command, cwd=REPO, env=ENV, stdout=Handle, stderr=subprocess.STDOUT)
	Row = {'name': Name, 'command': Command, 'cwd': str(REPO), 'exit_code': Completed.returncode,
		'expected_exit_code': Expected, 'elapsed_seconds': time.monotonic() - Start,
		'log': str(Log), 'log_sha256': hashlib.sha256(Log.read_bytes()).hexdigest()}
	print(json.dumps(Row), flush=True)
	return Row


def main():
	Jobs = []
	for n, R, Mode in ((2, 4, 'sup'), (3, 4, 'sup'), (2, 10, 'sup'), (2, 4, 'inf')):
		Name = 'n%dR%d%s' % (n, R, Mode.upper())
		Jobs.append((Name, [str(CANDIDATE), str(n), str(R), Mode, '--output', str(BASE / (Name + '.json'))], 0))
	Jobs.extend([
		('R1_compatibility', [str(CANDIDATE), '2', '1', 'sup', '--output', str(BASE / 'R1_compatibility.json')], 0),
		('tests', [str(BASE / 'test_candidate.py'), '--output', str(BASE / 'tests.json')], 0),
		('sensitivity', [str(BASE / 'sensitivity.py')], 0),
		('tests_optimized', ['-O', str(BASE / 'test_candidate.py'), '--output', str(BASE / 'tests_optimized.json')], 0),
		('legacy_original_n2R4SUP', [str(REPO / 'scripts/_gapn2_second_variation_probe.py'), '2', '4', 'sup'], 0),
		('cli_invalid_R', [str(CANDIDATE), '2', 'nan', 'sup'], 2),
		('cli_invalid_mode', [str(CANDIDATE), '2', '4', 'invalid'], 2),
		('cli_invalid_modes', [str(CANDIDATE), '2', '4', 'sup', '--modes', '2'], 2),
		('cli_help', [str(CANDIDATE), '--help'], 0),
		('new_projection_green_final', [str(BASE / 'regression_projection.py'), str(CANDIDATE)], 0),
	])
	CandidateHash = hashlib.sha256(CANDIDATE.read_bytes()).hexdigest()
	with ThreadPoolExecutor(max_workers=2) as Pool:
		Rows = list(Pool.map(run, Jobs))
	Result = {'role': 'software author', 'candidate_sha256_before': CandidateHash,
		'candidate_sha256_after': hashlib.sha256(CANDIDATE.read_bytes()).hexdigest(), 'runs': Rows}
	(BASE / 'execution_manifest.json').write_text(json.dumps(Result, indent=2) + '\n')
	return int(any(Row['exit_code'] != Row['expected_exit_code'] for Row in Rows))


if __name__ == '__main__':
	sys.exit(main())
