#!/usr/bin/env python3
"""Record actual process receipts for the newly authored checker."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent


def sha256(Data):
	return hashlib.sha256(Data).hexdigest()


def require(Condition, Message):
	if not Condition:
		raise RuntimeError(Message)


def run_case(Name, Options, ExpectedExit, Output=None):
	Args = [sys.executable, '-B'] + Options + [str(ROOT / 'checks.py')]
	if Output is not None:
		Args += ['--output', Output]
	else:
		Args += ['--negative-control', 'old-fh']
	Start = datetime.datetime.now(datetime.timezone.utc).isoformat()
	Begin = time.monotonic()
	Result = subprocess.run(Args, cwd=ROOT, capture_output=True, env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'), timeout=240)
	for Channel in ('stdout', 'stderr'):
		(ROOT / 'receipts' / (Name + '.' + Channel + '.log')).write_bytes(getattr(Result, Channel))
	Receipt = {'name': Name, 'argv': Args, 'cwd': str(ROOT), 'started_at_utc': Start, 'ended_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'elapsed_seconds': round(time.monotonic() - Begin, 6), 'returncode': Result.returncode, 'expected_exitcode': ExpectedExit, 'checks_sha256': sha256((ROOT / 'checks.py').read_bytes()), 'runner_sha256': sha256(Path(__file__).read_bytes()), 'stdout_path': 'receipts/' + Name + '.stdout.log', 'stderr_path': 'receipts/' + Name + '.stderr.log', 'stdout_sha256': sha256(Result.stdout), 'stderr_sha256': sha256(Result.stderr), 'output_path': Output, 'output_sha256': sha256((ROOT / Output).read_bytes()) if Output and (ROOT / Output).exists() else None}
	(ROOT / 'receipts' / (Name + '.execution.json')).write_text(json.dumps(Receipt, indent=2) + '\n')
	print(Name + ': exit=' + str(Result.returncode) + ', seconds=' + str(Receipt['elapsed_seconds']), flush=True)
	require(Result.returncode == ExpectedExit, Name + ' unexpected exit status')
	return Receipt


def main():
	Receipts = []
	Receipts.append(run_case('normal', [], 0, 'outputs.json'))
	Receipts.append(run_case('optimized', ['-O'], 0, 'outputs.optimized.json'))
	Receipts.append(run_case('negative-normal-old-fh', [], 1))
	Receipts.append(run_case('negative-optimized-old-fh', ['-O'], 1))
	Normal = json.loads((ROOT / 'outputs.json').read_text())
	Optimized = json.loads((ROOT / 'outputs.optimized.json').read_text())
	for Label, Payload, Flag in (('normal', Normal, 0), ('optimized', Optimized, 1)):
		require(Payload['optimize'] == Flag, Label + ' optimize flag')
		require(Payload['failed_groups'] == 0, Label + ' contains failed group')
		require(Payload['passed_groups'] == Payload['total_groups'] == 25, Label + ' complete group count')
	A = [(G['name'], G['kind'], G['status'], G['details']) for G in Normal['groups']]
	B = [(G['name'], G['kind'], G['status'], G['details']) for G in Optimized['groups']]
	require(A == B, 'normal and optimized mathematical results differ')
	Summary = {'normal': {'passed': Normal['passed_groups'], 'total': Normal['total_groups'], 'optimize': Normal['optimize']}, 'optimized': {'passed': Optimized['passed_groups'], 'total': Optimized['total_groups'], 'optimize': Optimized['optimize']}, 'mathematical_results_identical': True, 'intentional_old_fh_negative_controls': {'normal_exit': Receipts[2]['returncode'], 'optimized_exit': Receipts[3]['returncode'], 'expected_exit': 1}, 'receipts': [R['name'] + '.execution.json' for R in Receipts], 'role': 'author execution evidence, not independent final review'}
	(ROOT / 'receipts/execution-summary.json').write_text(json.dumps(Summary, indent=2) + '\n')
	print('25/25 in both modes; details identical; both wrong-formula processes rejected.', flush=True)


if __name__ == '__main__':
	main()
