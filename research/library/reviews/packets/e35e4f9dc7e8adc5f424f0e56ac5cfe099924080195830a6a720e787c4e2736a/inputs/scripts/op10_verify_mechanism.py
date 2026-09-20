# -*- coding: utf-8 -*-
"""Author diagnostics for the Krein scale; finite sums are not full norms.

Importing defines functions only. Run main() explicitly for the numerical checks.
No numerical outcome certifies density or an infinite-dimensional theorem.
"""
import math
from fractions import Fraction
from functools import lru_cache

import numpy as np
from scipy.integrate import quad

c = 3.0
NCOS = 40


def checked_quad(Fn, *Args, **Kwargs):
	"""Reject a failed estimator; returned floats are not interval certificates."""
	Kwargs.setdefault("epsabs", 1e-11)
	Kwargs.setdefault("epsrel", 1e-11)
	Result = quad(Fn, *Args, full_output=1, **Kwargs)
	Value, Error = Result[:2]
	if len(Result) != 3 or not math.isfinite(Value) or not math.isfinite(Error):
		raise ArithmeticError("quadrature failed; reduce truncation or use analytic coefficients")
	if Error > max(Kwargs["epsabs"], Kwargs["epsrel"] * abs(Value)):
		raise ArithmeticError("quadrature error estimate exceeds the requested tolerance")
	return Value, Error


@lru_cache(maxsize=256)
def mu_root(k):
	"""One root in (k*pi, (k+1/2)*pi), or an explicit precision failure."""
	if not isinstance(k, int) or k < 1:
		raise ValueError("k must be a positive integer")
	Pole = (k + 0.5) * math.pi
	# delta = Pole - mu removes the tangent pole. h decreases strictly.
	def h(Delta):
		return math.cos(Delta) - (Pole - Delta) * math.sin(Delta)
	Lo, Hi = 0.0, math.pi / 2
	if not (h(Lo) > 0 and h(Hi) < 0):
		raise ArithmeticError("invalid root bracket")
	for _ in range(200):
		Mid = (Lo + Hi) / 2
		if Mid == Lo or Mid == Hi:
			break
		if h(Mid) > 0:
			Lo = Mid
		else:
			Hi = Mid
	if not (h(Lo) >= 0 and h(Hi) <= 0):
		raise ArithmeticError("lost root bracket")
	Mu = Pole - (Lo + Hi) / 2
	if not k * math.pi < Mu < Pole:
		raise ArithmeticError("root and pole unresolved at float precision")
	# tan(mu)-mu is ill-conditioned near the pole; use its scaled numerator.
	if abs(math.sin(Mu) / Mu - math.cos(Mu)) > 8 * math.ulp(Mu):
		raise ArithmeticError("root residual exceeds float resolution")
	return Mu


def mu_roots(N=40):
	if not isinstance(N, int) or N < 0:
		raise ValueError("N must be a nonnegative integer")
	return np.array([mu_root(k) for k in range(1, N + 1)])


def basis(NCos=NCOS, NSin=40, Shift=c):
	"""Unnormalised modes: (eigenvalue, exact L2 norm squared, function)."""
	if Shift <= 0:
		raise ValueError("the shift must be positive")
	yield Shift, 2.0, lambda x: 1.0
	yield Shift, 2.0 / 3.0, lambda x: x
	for n in range(1, NCos + 1):
		yield (n * math.pi)**2 + Shift, 1.0, lambda x, n=n: math.cos(n * math.pi * x)
	for Mu in mu_roots(NSin):
		yield Mu**2 + Shift, Mu**2 / (1 + Mu**2), lambda x, Mu=Mu: math.sin(Mu * x)


def peval(Poly, x):
	return np.polyval(Poly[::-1], x)


def proj(Poly, Fn):
	return checked_quad(lambda x: peval(Poly, x) * Fn(x), -1, 1,
		epsabs=1e-11, epsrel=1e-11, limit=200)[0]


@lru_cache(maxsize=128)
def spectral_coefficients(Poly, N, Shift):
	return tuple((Lam, proj(Poly, Fn) / math.sqrt(NormSq))
		for Lam, NormSq, Fn in basis(N, N, Shift))


def partial_inner_t(PolyA, PolyB, t, N=40):
	"""Finite projection only; this can be finite when A or B is not in H^t."""
	A = spectral_coefficients(tuple(PolyA), N, c)
	B = spectral_coefficients(tuple(PolyB), N, c)
	return math.fsum(Lam**t * a * b for (Lam, a), (_, b) in zip(A, B))


def partial_norm_t(Poly, t, N=40):
	return math.sqrt(partial_inner_t(Poly, Poly, t, N))


def known_normsq_bounds(Kind, t, N=40):
	"""Analytic tail bounds for x2/p4; inf means out of domain.

	Floating evaluation of these bounds is not an outward-rounded certificate.
	"""
	if not isinstance(N, int) or N < 1 or not math.isfinite(t) or c <= 0:
		raise ValueError("need N >= 1, finite order, and positive shift")
	Constant, Factor, Power = {"x2": (2 / 9, 16, 4), "p4": (98 / 225, 2304, 8)}[Kind]
	if t >= (Power - 1) / 2:
		return math.inf, math.inf
	Partial = Constant * c**t + Factor * math.fsum(
		((n * math.pi)**2 + c)**t / (n * math.pi)**Power for n in range(1, N + 1))
	Tail = Factor * math.pi**(2 * t - Power) * (1 + c / (math.pi * (N + 1))**2)**max(t, 0)
	Tail *= N**(2 * t - Power + 1) / (Power - 2 * t - 1)
	return Partial, Partial + Tail


def kc(Poly):
	"""Formal differential expression; operator action requires domain membership."""
	Out = [c * a for a in Poly]
	for j in range(len(Poly) - 2):
		Out[j] -= (j + 1) * (j + 2) * Poly[j + 2]
	return Out


def p_n(n):
	if not isinstance(n, int) or n < 0 or n in (2, 3):
		raise ValueError("sparse-family index must be 0, 1, or >= 4")
	Poly = [0.0] * (n + 1)
	Poly[n] = 1.0
	m = n // 2
	if m >= 2:
		Poly[n - 2] = -m / (m - 1)
	return Poly


def xk(k):
	return [0.0] * k + [1.0]


def A_m(m):
	return 2 * m * (2 * m - 1) + c * m / (m - 1)


def B_m(m):
	return 2 * m * (2 * m - 3)


def pinned_solution(c0, Coefficients):
	"""Exact rational recurrence, rejecting hypotheses insufficient for monotonicity."""
	c0 = Fraction(c0)
	if c0 <= 0:
		raise ValueError("c0 must be positive")
	Values = [Fraction(0), Fraction(1)]
	for a, b in Coefficients:
		a, b = Fraction(a), Fraction(b)
		if b < 0 or a - b < c0:
			raise ValueError("need B_j >= 0 and A_j - B_j >= c0")
		Values.append((a * Values[-1] - b * Values[-2]) / c0)
	return Values


def self_check():
	"""Positive and negative author checks, not an independent acceptance test."""
	if not __debug__:
		raise RuntimeError("run self checks without Python -O")
	References = (4.493409457909064, 7.725251836937707, 10.9041216594289, 14.06619391283147)
	for k, Expected in enumerate(References, 1):
		assert math.isclose(mu_root(k), Expected, abs_tol=2e-13, rel_tol=0)
	for k in (40, 1000, 1000000):
		mu_root(k)  # checks bracket, branch, and scaled residual internally
	try:
		mu_root(10**12)
	except ArithmeticError:
		pass
	else:
		raise AssertionError("unresolved high root must not be returned as a pole")
	for Bad in (0, -1):
		try:
			mu_root(Bad)
		except ValueError:
			pass
		else:
			raise AssertionError("invalid root index accepted")
	Modes = list(basis(2, 2))
	for i, (_, NormSq, Fn) in enumerate(Modes):
		for j, (_, OtherNorm, Other) in enumerate(Modes):
			Gram = quad(lambda x: Fn(x) * Other(x), -1, 1)[0] / math.sqrt(NormSq * OtherNorm)
			assert abs(Gram - (i == j)) < 2e-11
	for t in (-2.0, 0.0, 1.0, 3.0):
		for Poly, NormSq in (([1.0], 2.0), ([0.0, 1.0], 2.0 / 3.0)):
			assert math.isclose(partial_inner_t(Poly, Poly, t, 6), c**t * NormSq, rel_tol=1e-10)
	for Kind, Poly, Power, Factor in (("x2", xk(2), 2, 4), ("p4", p_n(4), 4, -48)):
		for n in (1, 2, 3, 8):
			Exact = Factor * (-1)**n / (n * math.pi)**Power
			assert math.isclose(proj(Poly, lambda x: math.cos(n * math.pi * x)), Exact,
				rel_tol=1e-9, abs_tol=2e-12)
		Threshold = (2 * Power - 1) / 2
		assert all(math.isfinite(v) for v in known_normsq_bounds(Kind, Threshold - 0.01))
		for t in (Threshold, Threshold + 0.25):
			assert known_normsq_bounds(Kind, t) == (math.inf, math.inf)
		# Exact L2 polynomial norms must be enclosed by the analytic tail bound.
		Lo, Hi = known_normsq_bounds(Kind, 0)
		ExactL2 = 2 / 5 if Kind == "x2" else 214 / 315
		assert Lo <= ExactL2 <= Hi
	assert pinned_solution(1, [(1, 0)] * 4) == [0, 1, 1, 1, 1, 1]
	# A high-frequency unsupported quadrature must either be accurate or refuse.
	try:
		High = proj(xk(2), lambda x: math.cos(1000 * math.pi * x))
	except ArithmeticError:
		pass
	else:
		assert math.isclose(High, 4 / (1000 * math.pi)**2, rel_tol=1e-8, abs_tol=1e-12)
	# Unlike a constant/odd probe, x^2 detects deletion of the differential term.
	assert abs(partial_inner_t(xk(2), kc(p_n(4)), 0)
		- c * partial_inner_t(xk(2), p_n(4), 0)) > 1
	for Coefficients in ([(0, 0)], [(1, -1)]):
		try:
			pinned_solution(1, Coefficients)
		except ValueError:
			pass
		else:
			raise AssertionError("missing growth hypothesis accepted")


def main():
	self_check()
	print("AUTHOR_SELF_CHECKS: roots, complete low-mode Gram matrix, coefficients, thresholds, growth hypotheses")
	print("(A) FINITE_IDENTITY: transport on p_n in the proved range t <= 3; no full-norm certificate")
	for t in (0.5, 1.5, 1.75, 2.5, 3.0):
		for n in (0, 1, 4, 5, 6, 7):
			Lhs = partial_norm_t(kc(p_n(n)), t - 2)
			Rhs = partial_norm_t(p_n(n), t)
			assert math.isclose(Lhs, Rhs, rel_tol=1e-7, abs_tol=1e-6), (t, n, Lhs, Rhs)
	print("(B) FINITE_IDENTITY: jump relation only where all test polynomials are known to belong (t <= 1)")
	w = [0.5, 0.75, 1, -2, 0, 0, 0, 1]
	for t in (0.0, 0.75, 1.0):
		for m in (2, 3, 5, 8):
			Lhs = partial_inner_t(w, kc(p_n(2 * m)), t)
			Rhs = c * partial_inner_t(w, xk(2 * m), t) - A_m(m) * partial_inner_t(w, xk(2 * m - 2), t)
			Rhs += B_m(m) * partial_inner_t(w, xk(2 * m - 4), t)
			assert math.isclose(Lhs, Rhs, rel_tol=1e-8, abs_tol=1e-7), (t, m)
	print("OUT_OF_DOMAIN: old jump tests at t=1.5,1.75 require x^2 in H^t and are withdrawn")
	print("(C) ANALYTIC_DOMAIN / TAIL_BOUND (floating evaluation)")
	for Kind, Orders in (("x2", (0.75, 1.49, 1.5, 1.75, 2.5)), ("p4", (3.0, 3.49, 3.5, 4.0))):
		for t in Orders:
			Lo, Hi = known_normsq_bounds(Kind, t)
			print(f"  {Kind}, t={t}: " + ("DIVERGENT, not in H^t" if math.isinf(Lo) else f"norm squared between {Lo:.10g} and {Hi:.10g}"))
	print("(D) EXACT_FINITE_CHECK: pinned growth lower bound, both parities, j <= 30")
	for Shift in (1, 3, 10, 50):
		for Parity in (0, 1):
			Pairs = [(2 * j * (2 * j - 1 + 2 * Parity) + Fraction(Shift * j, j - 1),
				2 * j * (2 * j - 3 + 2 * Parity)) for j in range(2, 31)]
			Values = pinned_solution(Shift, Pairs)
			assert all(Values[j] >= Fraction(4, Shift)**(j - 1) * math.factorial(j) for j in range(2, 31))
	print("UNSUPPORTED_QUADRATURE: failed or inaccurate estimators raise ArithmeticError; no finite norm is returned")
	print("UNCOVERED: density for 3 < s < 7/2; certified quadrature; independent acceptance")


if __name__ == "__main__":
	main()
