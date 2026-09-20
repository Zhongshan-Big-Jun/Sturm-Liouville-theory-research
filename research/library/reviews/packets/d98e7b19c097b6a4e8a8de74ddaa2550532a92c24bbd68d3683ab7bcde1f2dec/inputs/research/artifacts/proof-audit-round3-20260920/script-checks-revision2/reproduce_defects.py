"""Minimal author regression reproducer; definitions-only avoids old import effects."""
import ast
from fractions import Fraction
import math
from pathlib import Path
import sys


import os
Repo = Path(os.environ['AUDIT_SOURCE_ROOT']).resolve()
sys.path.insert(0, str(Repo / 'scripts'))


def definitions(Name):
	PathName = Repo / 'scripts' / Name
	Tree = ast.parse(PathName.read_text(encoding='utf-8-sig'))
	Tree.body = [Node for Node in Tree.body if isinstance(Node, (ast.Import, ast.ImportFrom, ast.FunctionDef))]
	Namespace = {'__name__': Name.removesuffix('.py')}
	exec(compile(Tree, str(PathName), 'exec'), Namespace)
	return Namespace


def check_normalization():
	Module = definitions('d3_stability_verify2.py')
	Actual = Module['solve_u_log'](lambda m: 6, lambda m: 0, 3, 2)[2]
	if not math.isclose(Actual, math.log(2), abs_tol=1e-14):
		raise AssertionError(f'log u_2={Actual}; expected log(6/3)={math.log(2)}')


def check_exact_logs():
	Module = definitions('d3_stability_verify.py')
	Sequence = [Fraction(0)] + [Fraction(10 ** (400 * m)) for m in range(1, 11)]
	Rate = Module['poly_growth_rate'](Sequence, 10)
	if not math.isfinite(Rate):
		raise AssertionError(f'nonfinite growth diagnostic: {Rate}')


def check_initial_value(Name):
	Sequence = definitions(Name)['u_sequence'](lambda k: 0, 3)
	if Sequence[0] != 0:
		raise AssertionError(f'u_0={Sequence[0]}; expected 0')


def check_sparse():
	Module = definitions('op12_sparse_check.py')
	Actual = [k for k in range(1, 4001) if Module['is_sparse'](k)]
	if Actual != [4, 16, 256]:
		raise AssertionError(f'indices={Actual}; expected [4, 16, 256]')


def main():
	Checks = [
		('log solver c0 normalization', check_normalization),
		('large exact recurrence logs', check_exact_logs),
		('dichotomy u0', lambda: check_initial_value('op12_dichotomy_verify.py')),
		('threshold u0', lambda: check_initial_value('op12_threshold_verify.py')),
		('sparse indices', check_sparse),
	]
	Failures = 0
	for Name, Check in Checks:
		try:
			Check()
		except Exception as Error:
			Failures += 1
			print(f'FAIL {Name}: {type(Error).__name__}: {Error}')
		else:
			print(f'PASS {Name}')
	print(f'{len(Checks) - Failures}/{len(Checks)} checks passed')
	return 1 if Failures else 0


if __name__ == '__main__':
	raise SystemExit(main())
