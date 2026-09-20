"""Independent calculations for author regression checks, not independent review."""
import contextlib
from fractions import Fraction as F
import importlib
import io
import json
import math
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

import mpmath as mp


import os
Repo = Path(os.environ['AUDIT_SOURCE_ROOT']).resolve()
Output = Path(__file__).resolve().parent
sys.path.insert(0, str(Repo / 'scripts'))
Exact = importlib.import_module('d3_stability_verify')
Logs = importlib.import_module('d3_stability_verify2')
Product = importlib.import_module('op12_dichotomy_verify')
Threshold = importlib.import_module('op12_threshold_verify')
Sparse = importlib.import_module('op12_sparse_check')


def to_mp(Value):
	Value = F(Value)
	return mp.mpf(Value.numerator) / Value.denominator


def apply_expression(Polynomial, c):
	"""Apply c-D^2 by differentiating coefficient dictionaries."""
	Result = {}
	for Degree, Coefficient in Polynomial.items():
		Result[Degree] = Result.get(Degree, F(0)) + c * Coefficient
		if Degree >= 2:
			Result[Degree - 2] = Result.get(Degree - 2, F(0)) - Degree * (Degree - 1) * Coefficient
	return Result


def legendre_pairing(Polynomial):
	"""Exact integral against (3*x^2-1)/2 on [-1,1]."""
	Total = F(0)
	for Degree, Coefficient in Polynomial.items():
		for Offset, Weight in ((0, F(-1, 2)), (2, F(3, 2))):
			if (Degree + Offset) % 2 == 0:
				Total += Coefficient * Weight * F(2, Degree + Offset + 1)
	return Total


class BehaviorChecks(unittest.TestCase):
	def test_general_solution_is_not_product(self):
		Actual = Exact.solve_u(1, lambda m: 3, lambda m: 2, 200)
		self.assertEqual(Actual, [F(2**m - 1) for m in range(201)])
		Sharp = Exact.solve_u(1, lambda m: 3 + F(2, m), lambda m: 2, 100)
		self.assertEqual(Sharp[2], 4)
		self.assertTrue(all(Sharp[m] >= 2**m - 1 for m in range(101)))
		self.assertEqual(Exact.check_growth_lemma(3, lambda m: F(2, m), B=lambda m: 2), (True, 0.0))

	def test_exact_polynomial_coefficients(self):
		for c in (F(1, 2), F(3), F(5)):
			for Delta in (F(-36, 7), F(-1, 3), F(0), F(1), F(7, 9)):
				for m in range(2, 20):
					Alpha = F(m, m - 1) + Delta
					Polynomial = {2 * m: F(1), 2 * m - 2: -Alpha}
					Applied = apply_expression(Polynomial, c)
					A, B = Exact.perturbed_coefficients(c, m, Delta)
					self.assertEqual(Applied, {2 * m: c, 2 * m - 2: -A, 2 * m - 4: B})
					self.assertEqual(sum(Degree * Coefficient for Degree, Coefficient in Polynomial.items()), -(2 * m - 2) * Delta)
		self.assertEqual(Exact.perturbed_coefficients(3, 4, 1), (63, 70))

	def test_bounded_perturbation_counterexample(self):
		# Finite exact cross-checks of the audit's algebraic construction, not a proof by scan.
		Nu = [legendre_pairing(apply_expression({2 * m: F(1)}, F(3))) for m in range(31)]
		Deltas = {}
		for m in range(2, 31):
			Alpha = Nu[m] / Nu[m - 1]
			Deltas[m] = Alpha - F(m, m - 1)
			Claimed = F(6 * m * (2 * m + 5), (m - 1) * (2 * m + 3) * (4 * m * m - 6 * m - 7))
			self.assertEqual(Deltas[m], Claimed)
			self.assertEqual(legendre_pairing(apply_expression({2 * m: F(1), 2 * m - 2: -Alpha}, F(3))), 0)
		self.assertEqual(Deltas[2], F(-36, 7))
		self.assertEqual(Deltas[3], 1)
		A = lambda m: Exact.perturbed_coefficients(3, m, Deltas[m])[0]
		B = lambda m: Exact.perturbed_coefficients(3, m, Deltas[m])[1]
		Actual = Exact.solve_u(3, A, B, 30)
		Mu1 = legendre_pairing({2: F(1)})
		self.assertEqual(Actual, [legendre_pairing({2 * m: F(1)}) / Mu1 for m in range(31)])
		with self.assertRaises(ValueError):
			Logs.solve_u_log(A, B, 3, 30)

	def test_log_solver_against_exact_recurrence(self):
		with mp.workdps(90):
			for c in (F(1, 2), F(1), F(3), F(5), F(5, 2)):
				for Perturbed in (False, True):
					Pairs = {}
					for m in range(2, 301):
						Delta = F(1, 100 * m**2) if Perturbed else F(0)
						Applied = apply_expression({2 * m: F(1), 2 * m - 2: -F(m, m - 1) - Delta}, c)
						Pairs[m] = (-Applied[2 * m - 2], Applied[2 * m - 4])
					A, B = lambda m: Pairs[m][0], lambda m: Pairs[m][1]
					Actual = Exact.solve_u(c, A, B, 300)
					LogU = Logs.solve_u_log(A, B, c, 300)
					self.assertEqual(LogU[0], -math.inf)
					for m in range(1, 301):
						self.assertAlmostEqual(LogU[m], float(mp.log(to_mp(Actual[m]))), delta=5e-10)

	def test_log_solver_c0_and_large_ratios(self):
		for c in (0.5, 3, 5):
			Actual = Logs.solve_u_log(lambda m: 2 * c, lambda m: 0, c, 30)
			for m in range(1, 31):
				self.assertAlmostEqual(Actual[m], (m - 1) * math.log(2), delta=1e-12)
		Actual = Logs.solve_u_log(lambda m: 1e300, lambda m: 1, 1, 3)
		self.assertAlmostEqual(Actual[3], 600 * math.log(10), delta=1e-10)
		Actual = Logs.solve_u_log(lambda m: 1e-300, lambda m: 0, 1e300, 3)
		self.assertAlmostEqual(Actual[3], -1200 * math.log(10), delta=1e-10)

	def test_log_solver_cancellation_and_nonpositive_steps(self):
		b = 1 - 1e-12
		Actual = Logs.solve_u_log(lambda m: 1, lambda m: b, 1, 3)
		self.assertAlmostEqual(Actual[3], math.log(1 - b), delta=1e-12)
		for b in (1, 2):
			with self.assertRaisesRegex(ValueError, 'm=3'):
				Logs.solve_u_log(lambda m: 1, lambda m: b, 1, 3)
		for a in (0, -1, math.nan, math.inf):
			with self.assertRaises(ValueError):
				Logs.solve_u_log(lambda m: a, lambda m: 0, 1, 2)
		for b in (-1, math.nan, math.inf):
			with self.assertRaises(ValueError):
				Logs.solve_u_log(lambda m: 1, lambda m: b, 1, 2)
		for c in (0, -1, math.nan, math.inf):
			with self.assertRaises(ValueError):
				Logs.solve_u_log(lambda m: 1, lambda m: 0, c, 2)

	def test_exact_zero_and_unresolved_cancellation_rejected(self):
		for c in range(1, 11):
			for a in range(1, 11):
				for d in range(1, 11):
					A = lambda m: a if m == 2 else d
					B = lambda m: F(a * d, c)
					self.assertEqual(Exact.solve_u(c, A, B, 3)[3], 0)
					with self.assertRaises(ValueError, msg=f'zero step: c={c}, A2={a}, A3={d}'):
						Logs.solve_u_log(A, B, c, 3)
		with self.assertRaisesRegex(ValueError, 'unresolved'):
			Logs.solve_u_log(lambda m: 1, lambda m: math.nextafter(1, 0), 1, 3)

	def test_exact_logs_beyond_float_range(self):
		for Value in (F(10**10000), F(1, 10**10000), F(10**10000 + 1, 10**300)):
			with mp.workdps(90):
				self.assertAlmostEqual(Exact.log_positive(Value), float(mp.log(to_mp(Value))), delta=1e-10)
		u = Exact.solve_u(F(1, 2), lambda m: Exact.perturbed_coefficients(F(1, 2), m)[0], lambda m: Exact.perturbed_coefficients(F(1, 2), m)[1], 200)
		with self.assertRaises(OverflowError):
			float(u[200])
		self.assertTrue(math.isfinite(Exact.poly_growth_rate(u, 200)))
		for Value in (0, -1):
			with self.assertRaises(ValueError):
				Exact.log_positive(Value)

	def test_initial_values_and_empty_prefix(self):
		for N in (0, 1, 2):
			for Module in (Product, Threshold):
				u = Module.u_sequence(lambda k: 0, N)
				self.assertEqual(u, [mp.mpf(0)] + [mp.mpf(1)] * N)
			self.assertEqual(Exact.solve_u(1, lambda m: 1, lambda m: 0, N), [F(0)] + [F(1)] * N)
			LogU, Count = Sparse.lu(N)
			self.assertEqual(LogU[0], -mp.inf)
			self.assertEqual(Count, 0)
		self.assertEqual(Product.power_product(2, 0), 0)

	def test_gamma_normalization_against_exact_product(self):
		with mp.workdps(90):
			for C in (F(0), F(1), F(2), F(3), F(1, 2)):
				Expected = F(1)
				u = Product.u_sequence(lambda k: to_mp(C) / k, 200)
				for m in range(1, 201):
					if m >= 2:
						Expected *= 1 + C / m
					self.assertLess(abs(u[m] / to_mp(Expected) - 1), mp.mpf('1e-80'))
					self.assertLess(abs(Product.power_product(to_mp(C), m) / to_mp(Expected) - 1), mp.mpf('1e-80'))
			self.assertLess(abs(Product.power_product(2, 5000) / to_mp(F(5001 * 5002, 6)) - 1), mp.mpf('1e-80'))

	def test_finite_diagonal_sums_against_rationals(self):
		with mp.workdps(90):
			u = Product.u_sequence(lambda k: mp.mpf(2) / k, 80)
			Expected = sum((F((m + 1) * (m + 2), 6)**2 / (2 * m + 1)**4 for m in range(1, 81)), F(0))
			self.assertLess(abs(Product.diag_series(u, 80, 2) - to_mp(Expected)), mp.mpf('1e-80'))
			for N, Value in Threshold.diag_partial(u, 2, 80):
				Expected = sum((F((m + 1) * (m + 2), 6)**2 / (2 * m + 1)**4 for m in range(1, N + 1)), F(0))
				self.assertLess(abs(mp.mpf(Value) / to_mp(Expected) - 1), mp.mpf('1e-9'))
			self.assertEqual(Product.diag_series(u, 0, 2), 0)

	def test_main_uses_exact_log_k(self):
		class Captured(Exception):
			pass

		for Module in (Product, Threshold):
			Original = Module.u_sequence
			Observed = []

			def capture(eps, N):
				if N == 4000:
					return Original(eps, N)
				Observed.append(eps(2))
				raise Captured()

			with mp.workdps(60), patch.object(Module, 'u_sequence', capture), contextlib.redirect_stdout(io.StringIO()):
				with self.assertRaises(Captured):
					Module.main()
				self.assertLess(abs(Observed[0] - 1 / (2 * mp.log(2))), mp.mpf('1e-55'))

	def test_sparse_indices_and_plateaus(self):
		Expected = [2**(2**j) for j in range(1, 7)]
		for k in range(0, 70001):
			self.assertEqual(Sparse.is_sparse(k), k in Expected)
		for k in Expected:
			self.assertTrue(Sparse.is_sparse(k))
			self.assertFalse(Sparse.is_sparse(k - 1))
			self.assertFalse(Sparse.is_sparse(k + 1))
		with mp.workdps(90):
			LogU, Count = Sparse.lu(65536)
			self.assertEqual(Count, 4)
			ExpectedLog = mp.fsum(mp.log(1 + mp.exp(k)) for k in Expected[:4])
			self.assertLess(abs(LogU[65536] - ExpectedLog), mp.mpf('1e-80'))
			self.assertEqual(LogU[256], LogU[65535])
			self.assertEqual(LogU[16], LogU[255])
			self.assertTrue(mp.isfinite(Sparse.log_sparse_factor(2**32)))
			self.assertTrue(mp.isfinite(Product.eps_sparse(65536)))
			self.assertTrue(callable(Sparse.lu))
			self.assertEqual(Sparse.lu(4)[1], 1)

	def test_imports_are_quiet_and_preserve_precision(self):
		Code = (
			'import sys, mpmath as mp; '
			f'sys.path.insert(0, {str(Repo / "scripts")!r}); '
			'mp.mp.dps=37; '
			'import d3_stability_verify, d3_stability_verify2, op12_dichotomy_verify, op12_threshold_verify, op12_sparse_check; '
			'assert mp.mp.dps == 37'
		)
		Result = subprocess.run([sys.executable, '-B', '-c', Code], capture_output=True, text=True, timeout=20)
		self.assertEqual(Result.returncode, 0, Result.stderr)
		self.assertEqual(Result.stdout, '')
		self.assertEqual(Result.stderr, '')

	def test_asserted_regressions_exit_nonzero(self):
		Injections = {
			'd3_stability_verify': 'M.check_growth_lemma=lambda *a, **kw: (False, 1)',
			'd3_stability_verify2': 'M.solve_u_log=lambda *a, **kw: [0, 0, 0]',
			'op12_dichotomy_verify': 'M.u_sequence=lambda eps, N: [mp.mpf(0)]+[mp.mpf(1)]*N; M.diag_series=lambda *a: 0; M.power_product=lambda *a: 0',
			'op12_threshold_verify': 'M.u_sequence=lambda eps, N: [mp.mpf(0)]+[mp.mpf(1)]*N; M.diag_partial=lambda *a: []; M.power_product=lambda *a: 0',
			'op12_sparse_check': 'M.is_sparse=lambda k: False',
		}
		Records = []
		for Name, Injection in Injections.items():
			for Options in ([], ['-O']):
				Code = f'import sys, mpmath as mp; sys.path.insert(0, {str(Repo / "scripts")!r}); import {Name} as M; {Injection}; raise SystemExit(M.main())'
				Command = [sys.executable, '-B', *Options, '-c', Code]
				Result = subprocess.run(Command, capture_output=True, text=True, timeout=20)
				Records.append({'command': Command, 'exit_code': Result.returncode, 'stdout': Result.stdout, 'stderr': Result.stderr})
				self.assertNotEqual(Result.returncode, 0, Name)
				self.assertIn('AssertionError', Result.stderr, Name)
		(Output / 'assertion-failure-probes.json').write_text(json.dumps(Records, indent=2) + '\n')


if __name__ == '__main__':
	unittest.main(verbosity=2)
