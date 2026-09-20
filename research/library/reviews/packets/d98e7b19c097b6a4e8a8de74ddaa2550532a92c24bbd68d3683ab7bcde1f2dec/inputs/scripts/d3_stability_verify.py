# -*- coding: utf-8 -*-
"""Finite author checks for the moment-jump recurrence, not completeness proofs.

For c0 > 0, B >= 0 and eps = (A-B-c0)/c0 >= 0, the product is a
lower bound. It is the exact solution only in the B=0 examples below.
The diagonal series uses the actual recurrence solution; its finite partial
sums cannot establish convergence. Both parity recurrences matter for density.
"""
from fractions import Fraction as F
import math


def solve_u(c0, A, B, N, u0=0, u1=1):
	"""Exact rational recurrence c0*u_m=A_m*u_(m-1)-B_m*u_(m-2)."""
	if c0 <= 0 or N < 0:
		raise ValueError('require c0 > 0 and N >= 0')
	u = [F(0)] * (N + 1)
	u[0] = F(u0)
	if N >= 1:
		u[1] = F(u1)
	for m in range(2, N + 1):
		u[m] = (F(A(m)) * u[m - 1] - F(B(m)) * u[m - 2]) / F(c0)
	return u


def log_positive(Value):
	"""Log a positive rational without converting its magnitude to float."""
	Value = F(Value)
	if Value <= 0:
		raise ValueError('log requires a positive value')
	return math.log(Value.numerator) - math.log(Value.denominator)


def poly_growth_rate(u, N):
	"""Finite tail average of log(u_m)/log(m), not an asymptotic bound."""
	Rates = [log_positive(u[m]) / math.log(m)
		for m in range(max(2, N // 2), N) if u[m] > 0]
	return math.fsum(Rates) / len(Rates) if Rates else math.nan


def perturbed_coefficients(c, m, delta=0):
	"""Coefficients of (c-D^2)(x^(2m)-(m/(m-1)+delta)*x^(2m-2)).

	This is a formal polynomial expression. Nonzero delta generally violates
	the even Krein boundary condition p'(1)=0.
	"""
	if m < 2:
		raise ValueError('basis coefficients require m >= 2')
	Alpha = F(m, m - 1) + F(delta)
	return F(2 * m * (2 * m - 1)) + F(c) * Alpha, Alpha * (2 * m - 2) * (2 * m - 3)


def check_growth_lemma(c0, eps, N=200, B=None):
	"""Check the product lower bound on 2..N under its actual hypotheses."""
	if B is None:
		B = lambda m: F(0)
	if c0 <= 0 or any(F(eps(m)) < 0 or F(B(m)) < 0 for m in range(2, N + 1)):
		raise ValueError('growth bound requires c0 > 0, eps >= 0 and B >= 0')
	A = lambda m: F(c0) * (1 + F(eps(m))) + F(B(m))
	u = solve_u(c0, A, B, N)
	Product = F(1)
	Worst = F(0)
	for m in range(2, N + 1):
		Product *= 1 + F(eps(m))
		if u[m] < Product:
			Worst = max(Worst, (Product - u[m]) / Product)
	return Worst == 0, float(Worst)


def main():
	print('Finite author diagnostics; no completeness proof from scans or partial sums.')
	for b in (0, 2):
		Ok, Worst = check_growth_lemma(3, lambda m: F(2, m), B=lambda m: b)
		if not Ok:
			raise AssertionError(f'product lower-bound regression: B={b}, error={Worst}')
		print(f'Product lower bound: c0=3, B={b}, eps=2/k, m<=200: PASS')

	Actual = solve_u(1, lambda m: 3, lambda m: 2, 100)
	if any(Actual[m] != 2**m - 1 for m in range(101)):
		raise AssertionError('A=3, B=2 exact recurrence regression')
	Sharp = solve_u(1, lambda m: 3 + F(2, m), lambda m: 2, 100)
	if Sharp[2] != 4 or any(Sharp[m] < 2**m - 1 for m in range(101)):
		raise AssertionError('R3-F1 nonzero-B regression')
	print('General B=2: eps=0 gives u_m=2^m-1; eps=2/m gives u_2=4, product=2.')

	N = 5000
	u = solve_u(1, lambda m: 1 + F(2, m), lambda m: 0, N)
	if any(u[m] != F((m + 1) * (m + 2), 6) for m in range(1, N + 1)):
		raise AssertionError('B=0 product normalization regression')
	print(f'B=0, eps=2/k: u_{N}/N^2={float(u[N] / N**2):.8f}; limit=1/Gamma(4)=1/6.')
	for Beta in (2.4, 2.5, 2.6):
		Partial = math.fsum(float(u[m])**2 / (2 * m + 1)**(2 * Beta) for m in range(1, N + 1))
		Behavior = 'converges' if Beta > 2.5 else 'diverges'
		print(f'  beta={Beta}: finite partial sum (N={N})={Partial:.8f}; analytic B=0 series: {Behavior}.')

	for c in (F(3), F(5), F(1), F(1, 2)):
		A = lambda m: perturbed_coefficients(c, m)[0]
		B = lambda m: perturbed_coefficients(c, m)[1]
		u = solve_u(c, A, B, 200)
		LogU = log_positive(u[200])
		print(f'Unperturbed c={c}: log u_200={LogU:.3f}, tail diagnostic={poly_growth_rate(u, 200):.3f}.')

	if perturbed_coefficients(3, 4, 1) != (F(63), F(70)):
		raise AssertionError('R3-F2 actual perturbed coefficients regression')
	print('Basis perturbation c=3, delta_4=1: A_4=63, B_4=70, A_4-B_4=-7.')
	for D in (0, 1, 5):
		Pairs = [perturbed_coefficients(3, m, F(D, math.isqrt(m))) for m in range(2, 301)]
		Margin = min(A - B - 3 for A, B in Pairs)
		Status = 'hold on sampled indices' if Margin >= 0 and all(B >= 0 for _, B in Pairs) else 'FAIL'
		print(f'  delta_m={D}/floor(sqrt(m)), m<=300: min(A-B-c)={float(Margin):.3f}; growth hypotheses {Status}.')
	print('Perturbed polynomial expressions are not automatically in the Krein operator domain.')
	return 0


if __name__ == '__main__':
	raise SystemExit(main())
