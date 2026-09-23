"""Software-author regression checks. No mathematical/independent verdict."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import time
import traceback
import numpy as np
import mpmath as mp

BASE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location('candidate', BASE / '_gapn2_second_variation_probe.py')
C = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(C)
ROWS = []


def require(Condition, Message):
	if not Condition:
		raise AssertionError(Message)


def rejects(Callback):
	try:
		Callback()
	except ValueError:
		return
	raise AssertionError('invalid input was not rejected with ValueError')


def group(Name, Callback):
	Start = time.monotonic()
	try:
		Evidence = Callback()
		Row = {'name': Name, 'passed': True, 'evidence': Evidence}
	except Exception:
		Row = {'name': Name, 'passed': False, 'traceback': traceback.format_exc()}
	Row['elapsed_seconds'] = time.monotonic() - Start
	ROWS.append(Row)
	print(json.dumps(Row, indent=2), flush=True)


def projections():
	A = np.array([2., -3., 5.])
	b = np.array([1.7, -.6, .2])
	Widths = np.array([.1, .3, .6])
	B0, A0, W0 = b.copy(), A.copy(), Widths.copy()
	Euclidean = C.project_tangent(b, A)
	Weighted = C.project_tangent(b, A, Widths, 'width-weighted')
	Expected = b - (b @ A) / (A @ A) * A
	ExpectedWeighted = b - (b @ A) / (A @ (A / Widths)) * A / Widths
	require(np.max(abs(Euclidean - Expected)) < 5e-16, 'incorrect Euclidean coefficients')
	require(np.max(abs(Weighted - ExpectedWeighted)) < 5e-16, 'incorrect weighted coefficients')
	require(abs(Euclidean @ A) < 1e-14 and abs(Weighted @ A) < 1e-14, 'not tangent')
	require(np.max(abs(Euclidean - Weighted)) > .01, 'metrics unexpectedly conflated')
	require(np.array_equal(b, B0) and np.array_equal(A, A0) and np.array_equal(Widths, W0), 'input mutated')
	for Scale in (1e-250, 1e250):
		require(np.max(abs(C.project_tangent(b, Scale * A) - Euclidean)) < 5e-16, 'normal scale dependence')
	Zero = C.project_tangent(b, np.zeros(3))
	require(np.array_equal(Zero, b) and not np.shares_memory(Zero, b), 'zero normal not identity copy')
	require(np.array_equal(C.project_tangent(b, np.zeros(3), Widths, 'width-weighted'), b), 'weighted zero normal')
	Parallel = C.project_tangent(A, A)
	require(np.max(abs(Parallel)) < 5e-16, 'parallel direction not annihilated')
	return {'euclidean': Euclidean.tolist(), 'weighted': Weighted.tolist(), 'euclidean_residual': float(Euclidean @ A), 'weighted_residual': float(Weighted @ A)}


def invalid_inputs():
	Cases = [
		lambda: C.project_tangent([1, 2], [1]),
		lambda: C.project_tangent([[1, 2]], [1, 2]),
		lambda: C.project_tangent([], []),
		lambda: C.project_tangent([1, np.nan], [1, 2]),
		lambda: C.project_tangent([1, 2], [1, np.inf]),
		lambda: C.project_tangent([1, 2], [1, -np.inf]),
		lambda: C.project_tangent([1j, 2], [1, 2]),
		lambda: C.project_tangent([1, 2], [0, 0], [1, 0]),
		lambda: C.project_tangent([1, 2], [1, 2], [1]),
		lambda: C.project_tangent([1, 2], [1, 2], [1, np.nan]),
		lambda: C.project_tangent([1, 2], [1, 2], [1, -1], 'width-weighted'),
		lambda: C.project_tangent([1, 2], [1, 2], metric='width-weighted'),
		lambda: C.project_tangent([1, 2], [1, 2], metric='unknown'),
		lambda: C.validate_blocks([]),
		lambda: C.validate_blocks([(0, 1), (1, 1)]),
		lambda: C.validate_blocks([(1, -1)]),
		lambda: C.validate_blocks([(1, np.inf)]),
		lambda: C.validate_blocks([(np.nan, 1)]),
		lambda: C.validate_blocks([(1, 2, 3)]),
		lambda: C.quadrature_rule([(1, 1)], 0),
		lambda: C.quadrature_rule([(1, 1)], 8.5),
		lambda: C.quadrature_rule([(1, 1)], 8, [.5, np.nan]),
		lambda: C.quadrature_rule([(1, 1)], 8, [0]),
		lambda: C.fd_second([(1, 1)], [], 0),
		lambda: C.fd_second([(1, 1)], [1, 2], 0),
		lambda: C.fd_second([(1, 1)], [1], -1),
		lambda: C.fd_second([(1, 1)], [1], 0, h=np.nan),
		lambda: C.fd_second([(1, 1)], [1], 0, h=0),
		lambda: C.fd_second([(1, 1)], [1], 0, h=2),
		lambda: C.fd_second([(1, 1)], [1], 0, dps=12),
		lambda: C.fd_second([(1, 1)], [1], 0, refine=0),
		lambda: C.build_case(0, 4, 'sup'),
		lambda: C.build_case(2, np.inf, 'sup'),
		lambda: C.build_case(2, np.nan, 'sup'),
		lambda: C.build_case(2, .5, 'sup'),
		lambda: C.build_case(2, 4, 'other'),
		lambda: C.q_formula([1, 1], np.eye(2), np.eye(2), 1, [1, 1]),
		lambda: C.q_formula([1, 2], np.eye(3), np.eye(2), 1, [1, 1]),
		lambda: C.q_formula([1, 2], np.eye(2), np.eye(2), 2, [1, 1]),
		lambda: C.q_formula([1, 2], np.eye(2), np.eye(2), 1, [1]),
		lambda: C.q_formula([1, 2], [[1, np.nan], [0, 1]], np.eye(2), 1, [1, 1]),
	]
	for Callback in Cases:
		rejects(Callback)
	return {'rejected_cases': len(Cases)}


def constant_counterexample():
	T = C.HighPrecisionTangent([(.25, 1), (.75, 1)], 1, 70)
	with mp.workdps(70):
		Expected = [-3 * mp.pi ** 2 / 4 - mp.pi / 2, -9 * mp.pi ** 2 / 4 + mp.pi / 2]
		AnalyticError = max(abs(a - b) for a, b in zip(T.integrals, Expected))
		require(AnalyticError < mp.mpf('1e-55'), 'mp block integrals disagree with exact SL formula')
		OldDirection = np.array([float(-(9 * mp.pi - 2) / (3 * (3 * mp.pi + 2))), 1.])
		DirectOld = T.direct_residual(OldDirection)
		FormulaOld = -3 * mp.pi ** 2 / 2 + mp.pi / 3
		require(abs(DirectOld - FormulaOld) < mp.mpf('3e-15'), 'direct quadrature misses exact bad direction')
		NewDirection = C.project_tangent(OldDirection, T.A)
		DirectNew = T.direct_residual(NewDirection)
		require(abs(DirectNew) < mp.mpf('2e-15'), 'correct projection is not tangent')
		return {'analytic_error': mp.nstr(AnalyticError, 20), 'exact_bad_derivative': mp.nstr(FormulaOld, 35),
			'old_direct_fh': mp.nstr(DirectOld, 35), 'new_direct_fh': mp.nstr(DirectNew, 35)}


def endpoint_and_source_case():
	Rc, Z, Blocks, _ = C.build_case(2, 4, 'sup')
	Probe = C.SpectralProbe(Blocks, 61, 64)
	T = C.HighPrecisionTangent(Blocks, 2, 70)
	Points, Weights, Values, Knots = Probe.quadrature()
	F = Probe.lam[1] * Values[1] ** 2 - Probe.lam[2] * Values[2] ** 2
	Actual = np.array([np.sum(Weights[(Points > L) & (Points < R)] * F[(Points > L) & (Points < R)]) for L, R in zip(Probe.edges[:-1], Probe.edges[1:])])
	Error = float(np.max(abs(Actual - T.A)))
	require(Error < 2e-12, 'endpoint-aligned Gauss vs mp antiderivative mismatch')
	Coeff = C.project_tangent([1, 0, 0, 0, 0], T.A)
	Direct = T.direct_residual(Coeff)
	require(abs(Direct) < 1e-14, 'actual source case fh residual')
	Widths = np.array([L for L, _ in Blocks])
	Legacy = C.project_tangent([1, 0, 0, 0, 0], T.A / Widths)
	OldDirect = T.direct_residual(Legacy)
	require(abs(OldDirect) > 1, 'real source negative control did not expose the old mapping')
	Direction = C.block_direction(Coeff, Probe.edges)
	Lam, Cu, Cw, Diag = Probe.pairings(Direction)
	Independent = []
	from scipy.integrate import quad
	for k, l in ((1, 1), (1, 2), (1, 7), (2, 13)):
		Parts = []
		for i, (Left, Right) in enumerate(zip(Probe.edges[:-1], Probe.edges[1:])):
			Parts.append(quad(lambda x: Coeff[i] * C.eigfun(Blocks, Probe.roots[k], [x])[0] * C.eigfun(Blocks, Probe.roots[l], [x])[0], Left, Right, epsabs=2e-13, epsrel=2e-13)[0])
		Difference = abs(sum(Parts) - Cu[k, l])
		require(Difference < 2e-13, 'independent adaptive pairings mismatch')
		Independent.append({'k': k + 1, 'l': l + 1, 'difference': Difference})
	return {'max_integral_error': Error, 'old_direct_fh': mp.nstr(OldDirect, 30), 'new_direct_fh': mp.nstr(Direct, 30), 'pairing_crosschecks': Independent, 'actual_knots': Knots.tolist()}


def narrow_breakpoints():
	Blocks = [(.29343444668879154, 1), (.7065655533112085, 4)]
	Center, HalfWidth = .29343444668879154, 1e-7
	Breaks = (Center - HalfWidth, Center + HalfWidth)
	Points, Weights, Knots = C.quadrature_rule(Blocks, 8, Breaks)
	Mass = np.sum(Weights * (abs(Points - Center) < HalfWidth) / (2 * HalfWidth))
	# Actual represented endpoint width, rather than a rounded decimal assumption.
	Expected = (Breaks[1] - Breaks[0]) / (2 * HalfWidth)
	require(abs(Mass - Expected) < 1e-14, 'narrow discontinuity lost to grid masks')
	Grid = np.linspace(0., 1., 4001)
	OldMass = np.trapezoid((abs(Grid - Center) < HalfWidth).astype(float) / (2 * HalfWidth), Grid)
	require(OldMass == 0, 'negative control unexpectedly resolves narrow bump')
	return {'actual_mass': float(Mass), 'represented_endpoint_mass': Expected, 'old_grid_mass': float(OldMass), 'knots': Knots.tolist()}


def scale_direction_identity_and_fd():
	Blocks = [(.25, 1), (.75, 1)]
	Probe = C.SpectralProbe(Blocks, 21, 64)
	Lam, Cu, Cw, Diag = Probe.pairings(lambda x: np.ones_like(x))
	Q = C.q_formula(Lam, Cu, Cw, 1, Diag)
	Exact = 3 * np.pi ** 2
	require(abs(Q - Exact) < 2e-12, 'constant scaling Q identity')
	Errors = []
	with mp.workdps(70):
		for Step in (1e-2, 1e-3, 1e-4):
			FD = C.fd_second(Blocks, [1, 1], 0, h=Step, dps=70)[0]
			ExactFinite = 2 * mp.pi ** 2 / (1 - mp.mpf(Step) ** 2)
			Error = abs(FD - ExactFinite)
			require(Error < mp.mpf('1e-45'), 'mp FD does not match exact finite-step answer')
			Errors.append({'h': Step, 'absolute_error_vs_exact_finite_step': mp.nstr(Error, 20)})
	return {'Q': Q, 'exact_Q': Exact, 'Q_error': abs(Q - Exact), 'FD': Errors}


def main():
	Parser = argparse.ArgumentParser()
	Parser.add_argument('--output', type=Path, default=BASE / 'tests.json')
	Args = Parser.parse_args()
	for Name, Callback in [('projection_metric_zero_scale', projections), ('invalid_inputs', invalid_inputs),
		('constant_density_unequal_width_counterexample', constant_counterexample), ('real_endpoint_source_crosscheck', endpoint_and_source_case),
		('subgrid_bump_endpoints', narrow_breakpoints), ('scaling_identity_and_exact_finite_step_FD', scale_direction_identity_and_fd)]:
		group(Name, Callback)
	Result = {'role': 'software-author checks only', 'optimized': not __debug__, 'candidate_sha256': hashlib.sha256((BASE / '_gapn2_second_variation_probe.py').read_bytes()).hexdigest(),
		'checks': ROWS, 'failed': sum(not Row['passed'] for Row in ROWS)}
	Args.output.write_text(json.dumps(Result, indent=2, allow_nan=False) + '\n')
	return int(Result['failed'] != 0)


if __name__ == '__main__':
	sys.exit(main())
