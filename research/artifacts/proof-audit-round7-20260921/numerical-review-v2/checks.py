#!/usr/bin/env python3
"""New round-7 author checks. No repository program imports or missing appendix replay.

All verification gates explicitly raise; -O preserves them. Finite computations
are labelled separately from the general derivation notes in derivations.md.
"""
import argparse
import ast
import hashlib
import json
import platform
import sys
import time
import traceback
from functools import lru_cache
from pathlib import Path

import mpmath as mp
import sympy as sp

mp.mp.dps = 90
ROOT = Path(__file__).resolve().parent
GROUPS = []


def require(Condition, Message):
	if not bool(Condition):
		raise RuntimeError(Message)


def exact_zero(Expression, Message):
	Value = sp.simplify(sp.expand(Expression))
	require(Value == 0, Message + ': ' + str(Value))


def close(Value, Expected, Tolerance, Message):
	Error = abs(Value - Expected)
	require(Error <= mp.mpf(Tolerance), Message + ': error=' + str(Error))
	return mp.nstr(Error, 65)


def decimal(Value):
	return mp.nstr(Value, 65)


def number(Value):
	return mp.mpf(str(sp.N(Value, 88)))


def group(Name, Kind):
	def register(Function):
		GROUPS.append((Name, Kind, Function))
		return Function
	return register


def trig_zero(Expression, Message):
	Value = sp.simplify(sp.expand(Expression.rewrite(sp.exp)))
	require(Value == 0, Message + ': ' + str(Value))


@group('W_product_to_sum_general', 'symbolic_identity')
def w_product_to_sum():
	n, t = sp.symbols('n t', real=True)
	Raw = 2 * ((n + 1) * sp.cos((n + 1) * t) * sp.sin(n * t) - n * sp.sin((n + 1) * t) * sp.cos(n * t))
	Correct = sp.sin((2 * n + 1) * t) - (2 * n + 1) * sp.sin(t)
	trig_zero(Raw - Correct, 'W/pi product-to-sum')
	return {'identity': 'W=pi*(sin((2n+1)*theta)-(2n+1)*sin(theta))', 'theta': 'pi*x'}


@group('W_sum_squares_general_recurrence', 'symbolic_identity')
def w_recurrence():
	n, t = sp.symbols('n t', real=True)
	Wn = sp.sin((2 * n + 1) * t) - (2 * n + 1) * sp.sin(t)
	Wprev = sp.sin((2 * n - 1) * t) - (2 * n - 1) * sp.sin(t)
	trig_zero(Wn - Wprev + 4 * sp.sin(t) * sp.sin(n * t) ** 2, 'telescoping increment')
	exact_zero(Wn.subs(n, 0), 'zero base case')
	return {'base': 0, 'increment': '-4*pi*sin(theta)*sin(n*theta)^2', 'general_note': 'Sum the checked increment over integer n>=1. Strict negativity for 0<x<1 uses the j=1 summand; see derivations.md.'}


@group('W_finite_exact_Chebyshev_certificates', 'finite_exact')
def w_chebyshev():
	z = sp.symbols('z')
	for n in (1, 2, 3, 4, 5, 8, 12):
		A, B = sp.chebyshevu(n, z), sp.chebyshevu(n - 1, z)
		Raw = 2 * (1 - z ** 2) * (A * sp.diff(B, z) - sp.diff(A, z) * B)
		Target = sp.chebyshevu(2 * n, z) - (2 * n + 1)
		Sum = sum(sp.chebyshevu(j - 1, z) ** 2 for j in range(1, n + 1))
		exact_zero(Raw - Target, 'raw W at n=' + str(n))
		exact_zero(Target + 4 * (1 - z ** 2) * Sum, 'sum squares n=' + str(n))
	return {'n': [1, 2, 3, 4, 5, 8, 12], 'identities_per_n': 2}


@group('W_n2_half_counterexample', 'exact_counterexample')
def w_counterexample():
	x = sp.symbols('x', real=True)
	Un, Up = sp.sqrt(2) * sp.sin(2 * sp.pi * x), sp.sqrt(2) * sp.sin(3 * sp.pi * x)
	Actual = sp.simplify((sp.diff(Up, x) * Un - Up * sp.diff(Un, x)).subs(x, sp.Rational(1, 2)))
	Old = -6 * sp.pi
	exact_zero(Actual + 4 * sp.pi, 'actual W at half')
	require(sp.simplify(Actual - Old) != 0, 'old W must be refuted')
	return {'n': 2, 'x': '1/2', 'actual': str(Actual), 'old': str(Old)}


@group('Taylor_pi4_general', 'symbolic_identity')
def taylor_coefficient():
	n = sp.symbols('n', integer=True, positive=True)
	x = sp.symbols('x', real=True)
	f = 2 * sp.pi ** 2 * (n ** 2 * sp.sin(n * sp.pi * x) ** 2 - (n + 1) ** 2 * sp.sin((n + 1) * sp.pi * x) ** 2)
	C2 = sp.diff(f, x, 2).subs(x, 0) / 2
	Expected = 2 * sp.pi ** 4 * (n ** 4 - (n + 1) ** 4)
	exact_zero(C2 - Expected, 'Taylor coefficient')
	for Order in (0, 1, 3):
		exact_zero(sp.diff(f, x, Order).subs(x, 0), 'Taylor zero odd/constant')
	require(sp.simplify((C2 - 2 * sp.pi ** 2 * (n ** 4 - (n + 1) ** 4)).subs(n, 2)) != 0, 'old pi2 coefficient must fail')
	return {'x2_coefficient': str(sp.factor(C2)), 'scope': 'fixed n Taylor expansion; not a uniform-in-n remainder bound'}


def n2_data():
	t = sp.symbols('t')
	Roots = [(11 - 2 * sp.sqrt(10)) / 36, (11 + 2 * sp.sqrt(10)) / 36]
	P = -144 * t ** 2 + 88 * t - 9
	return t, Roots, P


@group('n2_exact_roots_and_reduction', 'finite_exact')
def n2_roots():
	t, Roots, P = n2_data()
	exact_zero(16 * t - 9 * (4 * t - 1) ** 2 - P, 'root polynomial from sine identity')
	for T in Roots:
		exact_zero(P.subs(t, T), 'root polynomial')
		require(T > 0 and T < 1, 'root lies in (0,1)')
		require(sp.simplify(sp.diff(P, t).subs(t, T)) != 0, 'simple t root')
	return {'t_roots': [str(T) for T in Roots], 'f_reduction': 'f=2*pi^2*(1-t)*(-144*t^2+88*t-9), t=cos(pi*x)^2'}


@group('n2_normalized_determinant_exact', 'finite_exact')
def n2_determinant():
	t, Roots, P = n2_data()
	F = sp.Rational(2, 9) * (1 - t) * P
	SquaredSlope = sp.diff(F, t) ** 2 * 4 * sp.pi ** 2 * t * (1 - t)
	Det = sp.simplify(sp.prod(SquaredSlope.subs(t, T) for T in Roots))
	Expected = sp.Rational(7030400000, 4782969) * sp.pi ** 4
	exact_zero(Det - Expected, 'normalized determinant')
	require(Det > 0, 'determinant positive')
	return {'det_DxF': str(Det), 'numeric': str(sp.N(Det, 50)), 'normalization': 'F_j=f(x_j)/(lambda_3), lambda_3=9*pi^2; four independent full-interval interfaces'}


@group('n2_four_root_order_signs_numeric', 'high_precision_finite')
def n2_root_locations():
	_, Roots, _ = n2_data()
	X1, X2 = [mp.acos(mp.sqrt(number(T))) / mp.pi for T in reversed(Roots)]
	Xs = [X1, X2, 1 - X2, 1 - X1]
	Signs = []
	Slopes = []
	for j, x in enumerate(Xs):
		f = 2 * mp.pi ** 2 * (4 * mp.sin(2 * mp.pi * x) ** 2 - 9 * mp.sin(3 * mp.pi * x) ** 2)
		close(f, 0, '1e-80', 'n2 root residual')
		Slope = 4 * mp.pi ** 3 * (8 * mp.sin(2 * mp.pi * x) * mp.cos(2 * mp.pi * x) - 27 * mp.sin(3 * mp.pi * x) * mp.cos(3 * mp.pi * x))
		Signs.append(int(mp.sign(Slope)))
		Slopes.append(Slope / (9 * mp.pi ** 2))
		if j:
			require(Xs[j - 1] < x, 'ordered roots')
	require(Signs == [1, -1, 1, -1], 'alternating signs')
	close(mp.fprod(Slopes), number(sp.Rational(7030400000, 4782969) * sp.pi ** 4), '1e-75', 'numeric determinant cross-check')
	return {'x_roots': [decimal(x) for x in Xs], 'signs': Signs}


def phase_rescale(Angle, Scale):
	Turns = mp.floor(Angle / mp.pi)
	Remainder = Angle - Turns * mp.pi
	return Turns * mp.pi + mp.atan2(Scale * mp.sin(Remainder), mp.cos(Remainder))


def endpoint_phase(s, Edges, Densities):
	Angle = mp.mpf(0)
	for a, b, r in zip(Edges[:-1], Edges[1:], Densities):
		Scale = mp.sqrt(r)
		Angle = phase_rescale(Angle, Scale) + s * Scale * (b - a)
		Angle = phase_rescale(Angle, 1 / Scale)
	return Angle


def propagate(Lambda, Edges, Densities):
	y, dy = mp.mpf(0), mp.mpf(1)
	Segments, Mass = [], mp.mpf(0)
	for a, b, r in zip(Edges[:-1], Edges[1:], Densities):
		k, L = mp.sqrt(Lambda * r), b - a
		A, B = y, dy / k
		Integral = (A * A * (L / 2 + mp.sin(2 * k * L) / (4 * k)) + B * B * (L / 2 - mp.sin(2 * k * L) / (4 * k)) + A * B * mp.sin(k * L) ** 2 / k)
		Segments.append((a, b, r, k, A, B, r * Integral))
		Mass += r * Integral
		y, dy = A * mp.cos(k * L) + B * mp.sin(k * L), k * (-A * mp.sin(k * L) + B * mp.cos(k * L))
	return {'lambda': Lambda, 'end_y': y, 'end_dy': dy, 'mass': Mass, 'segments': Segments}


@lru_cache(maxsize=None)
def eigenpair(Edges, Densities, Index):
	Lo, Hi = Index * mp.pi / mp.sqrt(max(Densities)), Index * mp.pi / mp.sqrt(min(Densities))
	for _ in range(110):
		Mid = (Lo + Hi) / 2
		if endpoint_phase(Mid, Edges, Densities) < Index * mp.pi:
			Lo = Mid
		else:
			Hi = Mid
	s = mp.findroot(lambda q: propagate(q * q, Edges, Densities)['end_y'], (Lo, Hi), solver='secant', tol=mp.mpf('1e-85'), maxsteps=40)
	Pair = propagate(s * s, Edges, Densities)
	close(endpoint_phase(s, Edges, Densities), Index * mp.pi, '1e-75', 'eigenvalue index from unwrapped phase')
	close(Pair['end_y'], 0, '1e-75', 'Dirichlet shooting residual')
	require(Pair['mass'] > 0, 'positive exact-integral norm')
	return Pair


def value(Pair, x, Normalized=True):
	for a, b, r, k, A, B, _ in Pair['segments']:
		if a <= x <= b:
			y = A * mp.cos(k * (x - a)) + B * mp.sin(k * (x - a))
			return y / mp.sqrt(Pair['mass']) if Normalized else y
	raise ValueError('point outside [0,1]')


def symmetric_pairs(a):
	Edges = (mp.mpf(0), a, 1 - a, mp.mpf(1))
	Densities = (mp.mpf(1), mp.mpf(4), mp.mpf(1))
	return eigenpair(Edges, Densities, 1), eigenpair(Edges, Densities, 2)


def gap(a):
	P1, P2 = symmetric_pairs(a)
	return P2['lambda'] - P1['lambda']


def fh_data():
	a = mp.mpf(1) / 4
	P1, P2 = symmetric_pairs(a)
	f = P1['lambda'] * value(P1, a) ** 2 - P2['lambda'] * value(P2, a) ** 2
	return a, P1, P2, f, 2 * (1 - 4) * f


@group('piecewise_L2rho_antiderivative_identity', 'symbolic_identity')
def integral_identity():
	A, B, k, L = sp.symbols('A B k L', real=True, nonzero=True)
	I = A ** 2 * (L / 2 + sp.sin(2 * k * L) / (4 * k)) + B ** 2 * (L / 2 - sp.sin(2 * k * L) / (4 * k)) + A * B * sp.sin(k * L) ** 2 / k
	trig_zero(sp.diff(I, L) - (A * sp.cos(k * L) + B * sp.sin(k * L)) ** 2, 'squared-wave primitive')
	exact_zero(I.subs(L, 0), 'primitive initial value')
	return {'method': 'closed-form exact segment integration evaluated at 90 decimal digits; not a mesh/trapezoid norm'}


@group('nonstationary_shooting_index_and_residual', 'high_precision_finite')
def shooting_check():
	a, P1, P2, f, FH = fh_data()
	require(abs(f) > 1, 'must use a genuinely nonstationary configuration')
	require(P1['lambda'] < P2['lambda'], 'spectral ordering')
	return {'densities': [1, 4, 1], 'interfaces': ['1/4', '3/4'], 'n': 1, 'lambda_1': decimal(P1['lambda']), 'lambda_2': decimal(P2['lambda']), 'shooting_residuals': [decimal(P['end_y']) for P in (P1, P2)], 'f_a': decimal(f), 'derivative_FH': decimal(FH), 'root_selection': 'monotone unwrapped phase bracketing; independent endpoint-y secant refinement'}


@group('exact_segment_normalization_vs_quadrature', 'high_precision_finite')
def normalization_check():
	a, P1, P2, _, _ = fh_data()
	Data = []
	for P in (P1, P2):
		Quadrature = mp.mpf(0)
		for Left, Right, r, k, A, B, _ in P['segments']:
			Quadrature += r * mp.quad(lambda t: (A * mp.cos(k * t) + B * mp.sin(k * t)) ** 2, [0, Right - Left])
		Error = close(Quadrature, P['mass'], '1e-80', 'quadrature vs segment integral')
		close(Quadrature / P['mass'], 1, '1e-80', 'weighted norm equals one')
		close(value(P, a) ** 2, value(P, 1 - a) ** 2, '1e-75', 'mirror squared eigenfunction')
		Data.append({'shooting_mass': decimal(P['mass']), 'segment_masses': [decimal(S[-1]) for S in P['segments']], 'quadrature_error': Error, 'normalized_u_a': decimal(value(P, a))})
	return Data


@group('symmetric_FH_vs_independent_central_difference', 'high_precision_finite')
def symmetric_fh_check():
	a, P1, P2, _, FH = fh_data()
	Results, Previous = [], None
	for Step in ('1e-5', '1e-8', '1e-11'):
		h = mp.mpf(Step)
		FD = (gap(a + h) - gap(a - h)) / (2 * h)
		Error = abs(FD - FH)
		if Previous is not None:
			require(Error < Previous * mp.mpf('2e-6'), 'central difference O(h^2) convergence')
		Previous = Error
		Results.append({'h': Step, 'central_difference': decimal(FD), 'error': decimal(Error)})
	close(FD, FH, '1e-18', 'full mirrored gap derivative')
	close(FH, mp.mpf('53.8809721602405715236952429875'), '5e-29', 'reported rounded numerical target')
	for P, Slot in ((P1, 0), (P2, 1)):
		Plus, Minus = symmetric_pairs(a + h)[Slot], symmetric_pairs(a - h)[Slot]
		Deriv = (Plus['lambda'] - Minus['lambda']) / (2 * h)
		Prediction = -2 * P['lambda'] * (1 - 4) * value(P, a) ** 2
		close(Deriv, Prediction, '1e-18', 'individual mirrored eigenvalue derivative')
	return {'FH': decimal(FH), 'differences': Results, 'h_changes': 'left a+h and right 1-a-h; both lengths move; new shooting roots for each perturbation'}


@group('legacy_symmetric_formula_is_half', 'high_precision_counterexample')
def half_formula_check():
	a, _, _, f, FH = fh_data()
	h = mp.mpf('1e-11')
	FD = (gap(a + h) - gap(a - h)) / (2 * h)
	Old = (1 - 4) * f
	close(FD / Old, 2, '1e-19', 'old formula must be half')
	require(abs(FD - Old) > 20, 'nonstationary negative control gap')
	return {'old': decimal(Old), 'correct': decimal(FH), 'FD_over_old': decimal(FD / Old)}


@group('one_interface_parameter_has_no_mirror_factor', 'high_precision_finite')
def one_interface_check():
	a, _, _, f, _ = fh_data()
	h = mp.mpf('1e-11')
	Densities = tuple(mp.mpf(r) for r in (1, 4, 1))
	def single_gap(Left):
		Edges = (mp.mpf(0), Left, mp.mpf(3) / 4, mp.mpf(1))
		return eigenpair(Edges, Densities, 2)['lambda'] - eigenpair(Edges, Densities, 1)['lambda']
	FD = (single_gap(a + h) - single_gap(a - h)) / (2 * h)
	close(FD, (1 - 4) * f, '1e-18', 'one independent full-interval interface')
	return {'central_difference': decimal(FD), 'FH': decimal((1 - 4) * f), 'parameter': 'x_left changes; x_right fixed at 3/4. Do not double this convention.'}


@group('u_second_derivative_true_nonzero_jump', 'high_precision_counterexample')
def second_derivative_jump():
	a, P, _, _, _ = fh_data()
	LeftSegment, RightSegment = P['segments'][0:2]
	def local_expression(Segment, x):
		Left, _, _, k, A, B, _ = Segment
		return (A * mp.cos(k * (x - Left)) + B * mp.sin(k * (x - Left))) / mp.sqrt(P['mass'])
	Left = mp.diff(lambda x: local_expression(LeftSegment, x), a, 2)
	Right = mp.diff(lambda x: local_expression(RightSegment, x), a, 2)
	Actual = Right - Left
	Expected = -P['lambda'] * 3 * value(P, a)
	close(Actual, Expected, '1e-75', 'one-sided analytic second derivatives')
	require(abs(Actual) > 1, 'actual jump nonzero')
	close(local_expression(LeftSegment, a), local_expression(RightSegment, a), '1e-80', 'u continuity')
	close(mp.diff(lambda x: local_expression(LeftSegment, x), a), mp.diff(lambda x: local_expression(RightSegment, x), a), '1e-75', 'u prime continuity')
	return {'index': 1, 'u_a': decimal(value(P, a)), 'u_second_left': decimal(Left), 'u_second_right': decimal(Right), 'jump_right_minus_left': decimal(Actual), 'expected': decimal(Expected), 'conclusion': 'This eigenfunction is C1 but not C2, hence not globally C3.'}


@group('trial_plateau_Gram_integrals_general', 'symbolic_identity')
def plateau_integrals():
	h, d, R, x = sp.symbols('h d R x', positive=True)
	Ramp = (h / 2 - x) / (h / 2 - d)
	Mass = 2 * R * d + 2 * sp.integrate(Ramp ** 2, (x, d, h / 2))
	Energy = 2 * sp.integrate(sp.diff(Ramp, x) ** 2, (x, d, h / 2))
	exact_zero(Mass - (2 * R * d + (h - 2 * d) / 3), 'plateau exact mass')
	exact_zero(Energy - 4 / (h - 2 * d), 'plateau exact energy')
	return {'basis': 'phi_j=1 on |x-jh|<=delta; linear to zero at |x-jh|=h/2; disjoint supports', 'diagonal_mass': str(sp.simplify(Mass)), 'diagonal_energy': str(sp.simplify(Energy)), 'conditions': 'h=1/(n+1), 0<delta<=h/12, R>=1', 'scope': 'integral identities; dimension/min-max argument is in derivations.md'}


@group('trial_plateau_bound_finite_exact_instances', 'finite_exact')
def plateau_bound():
	Rows = []
	for n in (1, 2, 3, 5, 8):
		for R in (8, 1000, 1000000, 1000000000):
			h = sp.Rational(1, n + 1)
			d = min(h / 12, sp.Rational(R) ** sp.Rational(-2, 3))
			E, M = 4 / (h - 2 * d), 2 * R * d + (h - 2 * d) / 3
			Bound = 6 / (h * R * d)
			require(E / M <= Bound, 'plateau upper Rayleigh bound')
			for j in range(1, n + 1):
				require(0 < j * h - h / 2 < j * h - d < j * h + d < j * h + h / 2 < 1, 'plateau support and high-density interval geometry')
			Rows.append({'n': n, 'R': R, 'delta': str(d), 'rayleigh': str(E / M), 'upper_bound': str(Bound)})
	return {'instances': Rows, 'scope': 'finite exact tests, not an infinite-dimensional spectral proof'}


@group('center_vanishing_subspace_finite_Gram_bounds', 'finite_exact')
def vanishing_gram():
	t = sp.symbols('t')
	Basis = [t * (1 - t), t * (1 - t) * (2 * t - 1)]
	K = sp.Matrix([[sp.integrate(sp.diff(p, t) * sp.diff(q, t), (t, 0, 1)) for q in Basis] for p in Basis])
	M = sp.Matrix([[sp.integrate(p * q, (t, 0, 1)) for q in Basis] for p in Basis])
	for p in Basis:
		exact_zero(p.subs(t, 0), 'vanishing at cell left')
		exact_zero(p.subs(t, 1), 'vanishing at cell right')
	def positive_definite(A, Label):
		for j in range(1, A.rows + 1):
			require(A[:j, :j].det() > 0, Label + ' leading principal minor')
	Rows = []
	for n in (1, 2, 3, 5):
		for R in (8, 1000, 1000000):
			h = sp.Rational(1, n + 1)
			d = min(h / 12, sp.Rational(R) ** sp.Rational(-2, 3))
			Energy, Mass = K / h, h * M
			# pi<22/7 gives a strictly stronger rational finite-space check.
			positive_definite(sp.Rational(49, 484) * h ** 2 * Energy - Mass, 'finite cell Poincare')
			for Cell in range(n + 1):
				Intervals = []
				if Cell > 0:
					Intervals.append((0, d / h))
				if Cell < n:
					Intervals.append((1 - d / h, 1))
				HighMass = sp.Matrix([[h * sum(sp.integrate(p * q, (t, a, b)) for a, b in Intervals) for q in Basis] for p in Basis])
				positive_definite(d ** 2 * Energy / 2 - HighMass, 'center neighborhood mass')
				positive_definite((sp.Rational(49, 484) * h ** 2 + (R - 1) * d ** 2 / 2) * Energy - (Mass + (R - 1) * HighMass), 'finite weighted bound')
			Rows.append({'n': n, 'R': R, 'delta': str(d), 'tested_subspace_dimension': 2 * (n + 1), 'cells_checked': n + 1})
	return {'cases': Rows, 'scope': 'All vectors in these finite polynomial subspaces only. Full H0^1 center-vanishing bound needs the analytic argument, not this test.'}


def thin_density(n, R):
	h = mp.mpf(1) / (n + 1)
	d = min(h / 12, mp.power(R, -mp.mpf(2) / 3))
	Edges, Densities = [mp.mpf(0)], []
	for j in range(1, n + 1):
		Edges.extend([j * h - d, j * h + d])
		Densities.extend([mp.mpf(1), mp.mpf(R)])
	Edges.append(mp.mpf(1))
	Densities.append(mp.mpf(1))
	return h, d, tuple(Edges), tuple(Densities)


@group('thin_density_spectral_bound_samples', 'high_precision_finite')
def thin_spectra():
	Rows = []
	for n, R in ((1, 1000), (2, 1000), (3, 1000), (2, 1000000)):
		h, d, Edges, Densities = thin_density(n, R)
		Ln = eigenpair(Edges, Densities, n)['lambda']
		Lp = eigenpair(Edges, Densities, n + 1)['lambda']
		Upper = 6 / (h * R * d)
		Lower = 1 / (h ** 2 / mp.pi ** 2 + (R - 1) * d ** 2 / 2)
		Cap = (n + 1) ** 2 * mp.pi ** 2
		require(0 < Ln <= Upper, 'lambda_n trial bound sample')
		require(Lower <= Lp <= Cap, 'lambda_n+1 center-vanishing and rho>=1 bounds sample')
		Rows.append({'n': n, 'R': R, 'lambda_n': decimal(Ln), 'lambda_n_plus_1': decimal(Lp), 'upper_lambda_n': decimal(Upper), 'lower_lambda_n_plus_1': decimal(Lower), 'upper_cap': decimal(Cap)})
	return {'samples': Rows, 'scope': 'finite spectral samples; no infinite-dimensional theorem certification'}


@group('thin_density_scalar_limits_general_n', 'symbolic_identity')
def scalar_limits():
	n = sp.symbols('n', integer=True, positive=True)
	q = sp.symbols('q', positive=True)
	h, R, d = 1 / (n + 1), q ** 3, q ** -2
	Upper = 6 / (h * R * d)
	Lower = 1 / (h ** 2 / sp.pi ** 2 + (R - 1) * d ** 2 / 2)
	exact_zero(sp.limit(Upper, q, sp.oo), 'upper lambda_n tends to zero')
	exact_zero(sp.limit(Lower, q, sp.oo) - (n + 1) ** 2 * sp.pi ** 2, 'lower lambda_n+1 scalar limit')
	return {'R': 'q^3', 'delta': 'q^-2 once q^2>=12(n+1)', 'limits': ['0', '(n+1)^2*pi^2'], 'scope': 'scalar asymptotics of bounds, conditional on the full variational argument in derivations.md'}


@group('constant_density_refutes_general_4pi2', 'symbolic_counterexample')
def constant_density_gap():
	n = sp.symbols('n', integer=True, positive=True)
	Gap = ((n + 1) ** 2 - n ** 2) * sp.pi ** 2
	exact_zero(Gap - (2 * n + 1) * sp.pi ** 2, 'constant-density gap')
	require(Gap.subs(n, 2) > 4 * sp.pi ** 2, 'S2(R)>=5*pi2 excludes a 4*pi2 limit')
	exact_zero(((n + 1) ** 2 * sp.pi ** 2).subs(n, 1) - 4 * sp.pi ** 2, 'n1 special case retained')
	return {'S_n_lower_bound': '(2n+1)*pi^2 for every R>=1 since rho=1 is admissible', 'n2_lower': '5*pi^2', 'n1_limit_candidate': '4*pi^2', 'scope': 'supremum over the whole box class, not arbitrary stationary branches'}


@group('R7_P01_rho2_Schrodinger_counterexample', 'exact_counterexample')
def schrodinger_counterexample():
	x, tau = sp.symbols('x tau', real=True)
	u = sp.sin(sp.pi * x)
	OrdinaryMass = sp.integrate(u ** 2, (x, 0, 1))
	WeightedMass = sp.integrate(2 * u ** 2, (x, 0, 1))
	Lambda = sp.pi ** 2 + 2 * tau
	Old = WeightedMass
	Actual = sp.diff(Lambda, tau)
	exact_zero(-sp.diff(u, x, 2) + 2 * tau * u - Lambda * u, 'rho2 exact eigen-equation')
	exact_zero(WeightedMass - 1, 'weighted normalization')
	exact_zero(OrdinaryMass - sp.Rational(1, 2), 'fixed L2 norm')
	exact_zero(Old - 1, 'old formula prediction')
	exact_zero(Actual - 2, 'true derivative')
	require(Actual != Old, 'normalization error negative control')
	return {'rho': 2, 'H': '-d2/dx2+2*tau on fixed L2(0,1)', 'u': 'sin(pi*x)', 'weighted_norm_squared': str(WeightedMass), 'ordinary_norm_squared': str(OrdinaryMass), 'old_prediction': str(Old), 'true_derivative': str(Actual)}


@group('R7_P01_generalized_FH_two_exact_models', 'finite_exact')
def generalized_fh_check():
	x, tau = sp.symbols('x tau', real=True)
	u = sp.sin(sp.pi * x)
	Mass = sp.integrate(u ** 2, (x, 0, 1))
	Potential = sp.integrate(2 * u ** 2, (x, 0, 1)) / Mass
	exact_zero(Potential - 2, 'A prime=2I, B=I')
	Lambda = sp.pi ** 2 / (2 + tau)
	Weighted = -Lambda * Mass / ((2 + tau) * Mass)
	exact_zero(Weighted - sp.diff(Lambda, tau), 'A prime=0, B prime=I')
	return {'formula': "lambda'=(<u,A' u>-lambda*<u,B' u>)/<u,Bu>", 'potential_model_derivative': str(Potential), 'weighted_string_derivative': str(Weighted), 'scope': 'two exact model instantiations; not a general operator differentiability proof'}


@group('R7_P02_direct_matrix_and_switch_scaling', 'finite_exact_counterexamples')
def direct_matrix_and_switch_scaling():
	K = sp.diag(1, 1, -1, -1)
	H = -81 * K
	exact_zero(K.det() - 1, 'positive determinant counterexample')
	require(H[0, 0] < 0 < H[2, 2], 'Hessian has both signs despite detK>0')
	# Pointwise switch data: lambda_n=4, lambda_np1=9, u=3, v=2,
	# u_prime=1, v_prime=0, s=3, c=2/3, epsilon=1, W=-2.
	W, Fprime, s, Lp = sp.Integer(-2), sp.Integer(24), sp.Integer(3), sp.Integer(9)
	RawScaled = Fprime / s
	NormalizedScaled = Fprime / (s * Lp)
	OldScaled = 2 * sp.Rational(2, 3) * abs(W) / 3
	exact_zero(Fprime + 2 * Lp * sp.Rational(2, 3) * W, 'fprime carries lambda_np1')
	exact_zero(NormalizedScaled - OldScaled, 'K diagonal uses fprime/(s*lambda_np1)')
	require(RawScaled != OldScaled, 'fprime/s cannot drop lambda_np1')
	S = sp.diag(3, -3, 3, -3, 3, -3)
	exact_zero(S.det() + 3 ** 6, 'n3 sign from det diag(s)')
	# Independent array-semantics counterexample, not execution of repo code.
	S2 = sp.diag(3, -3)
	J = sp.Matrix([[1, 2], [-2, -1]])
	Correct = -9 * S2 * J
	Elementwise = -9 * S2.multiply_elementwise(J)
	require(Correct == Correct.T, 'chosen true Hessian symmetric')
	require(Correct != Elementwise and Correct[0, 1] != 0 and Elementwise[0, 1] == 0, 'ndarray multiplication by diagonal erases off-diagonals')
	return {'K': str(K), 'det_K': str(K.det()), 'Hessian_diagonal': list(map(str, H.diagonal())), 'fprime_over_s': str(RawScaled), 'fprime_over_s_lambda': str(NormalizedScaled), 'old_missing_lambda_expression': str(OldScaled), 'n3_detJ_sign_when_K_identity': -1, 'matrix_product_H': str(Correct), 'elementwise_product_H': str(Elementwise), 'scope': 'Finite algebra refutes a general matrix implication and distinguishes normalization/array semantics. Does not refute a particular spectral branch or certify G2.'}


@group('execution_contract_explicit_raise_and_input_identity', 'execution_integrity')
def execution_contract():
	Source = Path(__file__).read_bytes()
	Tree = ast.parse(Source)
	require(not any(isinstance(Node, ast.Assert) for Node in ast.walk(Tree)), 'checks source must not contain assert statements')
	Caught = False
	try:
		require(False, 'intentional always-active negative control')
	except RuntimeError:
		Caught = True
	require(Caught, 'explicit raise must stay active under -O')
	Manifest = json.loads((ROOT / 'inputs/manifest.json').read_text())
	for Item in Manifest['inputs']:
		Digest = hashlib.sha256((ROOT / Item['snapshot']).read_bytes()).hexdigest()
		require(Digest == Item['sha256'], 'input snapshot hash mismatch: ' + Item['snapshot'])
	return {'assert_nodes': 0, 'explicit_raise_negative_control_caught': Caught, 'input_snapshots_verified': len(Manifest['inputs'])}


def main():
	Parser = argparse.ArgumentParser()
	Parser.add_argument('--output', default='outputs.json')
	Parser.add_argument('--negative-control', choices=['old-fh', 'old-schrodinger'])
	Args = Parser.parse_args()
	if Args.negative_control == 'old-fh':
		a, _, _, f, _ = fh_data()
		h = mp.mpf('1e-11')
		close((gap(a + h) - gap(a - h)) / (2 * h), (1 - 4) * f, '1e-18', 'intentional old FH formula rejection')
		raise RuntimeError('negative control unexpectedly survived')
	if Args.negative_control == 'old-schrodinger':
		require(sp.Integer(1) == sp.Integer(2), 'intentional old Schrodinger normalization rejection')
		raise RuntimeError('negative control unexpectedly survived')
	OutputPath = (ROOT / Args.output).resolve()
	require(OutputPath.is_relative_to(ROOT), 'outputs must stay within author directory')
	Results, Start = [], time.monotonic()
	for Name, Kind, Function in GROUPS:
		Begin = time.monotonic()
		try:
			Details = Function()
			Results.append({'name': Name, 'kind': Kind, 'status': 'PASS', 'details': Details, 'elapsed_seconds': round(time.monotonic() - Begin, 6)})
			print('PASS ' + Name, flush=True)
		except Exception as Error:
			Results.append({'name': Name, 'kind': Kind, 'status': 'FAIL', 'error': str(Error), 'traceback': traceback.format_exc(), 'elapsed_seconds': round(time.monotonic() - Begin, 6)})
			print('FAIL ' + Name + ': ' + str(Error), flush=True)
	Passed = sum(R['status'] == 'PASS' for R in Results)
	Payload = {'role': 'independent executable-check author, not final reviewer', 'provenance': 'new implementation; missing appendix and external checks.py were not supplied or replayed', 'python': sys.version, 'executable': sys.executable, 'platform': platform.platform(), 'optimize': sys.flags.optimize, '__debug__': __debug__, 'mpmath': mp.__version__, 'sympy': sp.__version__, 'decimal_precision': mp.mp.dps, 'checks_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), 'input_manifest_sha256': hashlib.sha256((ROOT / 'inputs/manifest.json').read_bytes()).hexdigest(), 'total_groups': len(Results), 'passed_groups': Passed, 'failed_groups': len(Results) - Passed, 'elapsed_seconds': round(time.monotonic() - Start, 6), 'groups': Results, 'limits': ['Finite exact and high-precision tests are not infinite-dimensional proofs.', 'General derivation notes are authored support, not independent final approval.', 'No repository programs, old Blueprint tools, Lean, or historical certificate suites executed.']}
	OutputPath.write_text(json.dumps(Payload, ensure_ascii=False, indent=2) + '\n')
	print(str(Passed) + '/' + str(len(Results)) + ' groups passed; optimize=' + str(sys.flags.optimize), flush=True)
	if Passed != len(Results):
		raise SystemExit(1)


if __name__ == '__main__':
	main()
