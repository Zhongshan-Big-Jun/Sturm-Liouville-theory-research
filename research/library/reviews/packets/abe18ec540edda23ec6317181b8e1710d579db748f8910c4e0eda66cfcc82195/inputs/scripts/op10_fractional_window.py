# -*- coding: utf-8 -*-
"""Author diagnostics for the fractional window, with explicit domain status.

The sparse-family density proof uses H^3 density and spectral truncation.
Monomials of degree >= 2 are not in H^s when s >= 3/2. Their finite
spectral sums must not be reported as full norms or interpolation evidence.
Importing this module does not solve roots, integrate, print, or run tests.
"""
import math
from functools import lru_cache

from scipy.integrate import quad

c = 3.0


@lru_cache(maxsize=256)
def mu_root(k):
	"""Bracket in the pole-distance coordinate, with explicit precision failure."""
	if not isinstance(k, int) or k < 1:
		raise ValueError("k must be a positive integer")
	Pole = (k + 0.5) * math.pi
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
	if abs(math.sin(Mu) / Mu - math.cos(Mu)) > 8 * math.ulp(Mu):
		raise ArithmeticError("root residual exceeds float resolution")
	return Mu


def mu_roots(N=30):
	if not isinstance(N, int) or N < 0:
		raise ValueError("N must be a nonnegative integer")
	return [mu_root(k) for k in range(1, N + 1)]


def cos_normsq(k, n):
	"""Return <x^k,cos(n*pi*x)> and the exact cosine norm squared."""
	if n == 0:
		return (2 / (k + 1) if k % 2 == 0 else 0.0), 2.0
	if k % 2 or k == 0:
		return 0.0, 1.0
	Val = quad(lambda x: x**k * math.cos(n * math.pi * x), -1, 1,
		epsabs=1e-11, epsrel=1e-11, limit=200)[0]
	return Val, 1.0


def sin_normsq(k, Mu):
	"""Sine mode data; Mu must be a root returned by mu_root."""
	NormSq = Mu**2 / (1 + Mu**2)
	if k % 2 == 0 or k == 1:
		return 0.0, NormSq
	Val = quad(lambda x: x**k * math.sin(Mu * x), -1, 1,
		epsabs=1e-11, epsrel=1e-11, limit=200)[0]
	return Val, NormSq


def monomial_domain(k, t):
	"""Analytic membership, independent of truncation size.

	For even k>=2 the cosine coefficient is 2*k*(-1)^n/(n*pi)^2+O(n^-4).
	For odd k>=3 the sine coefficient is 2*(k-1)*sin(mu)/mu^2+O(mu^-4).
	Their nonzero leading terms give the same strict threshold t < 3/2.
	"""
	if not isinstance(k, int) or k < 0 or not math.isfinite(t):
		raise ValueError("need a nonnegative integer degree and finite order")
	return "IN_DOMAIN" if k <= 1 or t < 1.5 else "DIVERGENT"


def monomial_partial_normsq(k, t, N=30):
	"""Squared norm of the finite projection, even outside the full domain."""
	monomial_domain(k, t)  # validate arguments without changing the partial-sum meaning
	if not isinstance(N, int) or N < 0 or c <= 0:
		raise ValueError("need N >= 0 and a positive shift")
	Constant = 2 / (k + 1) if k % 2 == 0 else 0.0
	Linear = 2 / (k + 2) if k % 2 else 0.0
	Terms = [c**t * (Constant**2 / 2 + Linear**2 / (2 / 3))]
	if k % 2 == 0:
		for n in range(1, N + 1):
			Val, NormSq = cos_normsq(k, n)
			Terms.append(((n * math.pi)**2 + c)**t * Val**2 / NormSq)
	else:
		for Mu in mu_roots(N):
			Val, NormSq = sin_normsq(k, Mu)
			Terms.append((Mu**2 + c)**t * Val**2 / NormSq)
	return math.fsum(Terms)


def x2_partial_normsq(t, N):
	"""Exact coefficient formula, evaluated in floating point; not the full norm."""
	if not isinstance(N, int) or N < 0 or not math.isfinite(t) or c <= 0:
		raise ValueError("need N >= 0, finite order, and positive shift")
	return 2 * c**t / 9 + 16 * math.fsum(
		((n * math.pi)**2 + c)**t / (n * math.pi)**4 for n in range(1, N + 1))


def self_check():
	if not __debug__:
		raise RuntimeError("run self checks without Python -O")
	References = (4.493409457909064, 7.725251836937707, 10.9041216594289, 14.06619391283147)
	for k, Expected in enumerate(References, 1):
		assert math.isclose(mu_root(k), Expected, abs_tol=2e-13, rel_tol=0)
	for k in (40, 1000, 1000000):
		mu_root(k)
	try:
		mu_root(10**12)
	except ArithmeticError:
		pass
	else:
		raise AssertionError("unresolved high root must not be returned as a pole")
	for k in (1, 3, 40):
		Mu = mu_root(k)
		_, NormSq = sin_normsq(3, Mu)
		Integral = quad(lambda x: math.sin(Mu * x)**2, -1, 1, limit=200)[0]
		assert math.isclose(Integral, NormSq, rel_tol=1e-10)
		assert abs(quad(lambda x: x * math.sin(Mu * x), -1, 1, limit=200)[0]) < 1e-10
	for t in (-2.0, 0.0, 1.0, 3.0):
		assert math.isclose(monomial_partial_normsq(0, t), 2 * c**t, rel_tol=1e-12)
		assert math.isclose(monomial_partial_normsq(1, t), (2 / 3) * c**t, rel_tol=1e-12)
	for t in (0.75, 1.75):
		# The latter equality checks partial sums only; the full norm diverges.
		assert math.isclose(monomial_partial_normsq(2, t), x2_partial_normsq(t, 30), rel_tol=1e-10)
	assert monomial_domain(2, 1.49) == "IN_DOMAIN"
	assert monomial_domain(1, 100.0) == "IN_DOMAIN"
	for k, t in ((2, 1.5), (3, 1.5), (4, 1.75)):
		assert monomial_domain(k, t) == "DIVERGENT"
	try:
		monomial_domain(-1, 0)
	except ValueError:
		pass
	else:
		raise AssertionError("negative degree accepted")


def main():
	self_check()
	print("AUTHOR_SELF_CHECKS: low/high roots, precision rejection, sine norm, linear mode, domain boundaries")
	print("(a) PARTIAL_SUM: negative-order projections, including odd modes")
	print("Analytically, the full squared norm is <= c^t * ||x^k||_0^2 for t < 0.")
	for t in (-0.5, -0.25, -0.1):
		for k in (0, 1, 2, 3, 4, 8):
			Partial = monomial_partial_normsq(k, t)
			Bound = c**t * 2 / (2 * k + 1)
			assert Partial <= Bound + 1e-10
			print(f"  t={t:+.2f}, k={k}: partial squared norm={Partial:.10g}, analytic full upper bound={Bound:.10g}")
	print("(b) ANALYTIC_DOMAIN: old monomial interpolation claim withdrawn")
	for t in (1.5, 1.75):
		for k in (2, 4, 8, 16):
			print(f"  t={t}, k={k}: {monomial_domain(k, t)}; no finite full norm")
	print("Divergent x^2 squared-norm partial sums (illustration, not the divergence proof):")
	for t in (1.5, 1.75):
		for N in (40, 160, 640, 2560):
			print(f"  t={t}, N={N}: {x2_partial_normsq(t, N):.10f}")
	print("UNCOVERED: infinite-dimensional density; outward-rounded numerical certificates; independent acceptance")


if __name__ == "__main__":
	main()
