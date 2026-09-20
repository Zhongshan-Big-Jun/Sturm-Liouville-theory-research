# -*- coding: utf-8 -*-
"""Positive-step log recurrence diagnostics, not a stability certification.

The growth lemma needs the actual B>=0 and A-B>=c0 at every step.
The solver can also handle decreasing positive solutions, but cannot certify
sign-changing recurrences or infer completeness from a finite run.
"""
import math
from fractions import Fraction

from d3_stability_verify import perturbed_coefficients


def exact_coefficient(Value):
	"""Preserve the supplied rational value, including a float's exact bits."""
	try:
		return Fraction(Value)
	except (TypeError, ValueError, OverflowError) as Error:
		raise ValueError('coefficients must have a finite exact Fraction conversion') from Error


def log_fraction(Value):
	"""Approximate the log of a positive fraction without range overflow."""
	Numerator, Denominator = Value.numerator, Value.denominator
	if Numerator <= 0:
		raise ValueError('require a positive fraction')
	if Denominator <= 2 * Numerator and Numerator <= 2 * Denominator:
		return math.log1p(float(Value - 1))
	NumeratorShift = max(0, Numerator.bit_length() - 54)
	DenominatorShift = max(0, Denominator.bit_length() - 54)
	Mantissa = (Numerator >> NumeratorShift) / (Denominator >> DenominatorShift)
	return (NumeratorShift - DenominatorShift) * math.log(2) + math.log(Mantissa)


def solve_u_log(A, B, c0, N):
	"""Return diagnostic logs; reject every nonpositive exact recurrence step.

	Domain: Fraction-convertible finite coefficients, c0>0, A_m>0, B_m>=0.
	Track r_m=u_m/u_(m-1) exactly, with r_2=A_2/c0 and
	r_m=(A_m-B_m/r_(m-1))/c0 thereafter. Thus propagated floating error
	cannot decide positivity. Floats mean their represented rational values,
	not unknown exact coefficients before input rounding. Log values remain
	approximate; this is not an interval or stability certificate. Exact ratio
	denominators can grow with N, trading speed for reliable sign decisions.
	"""
	C = exact_coefficient(c0)
	if C <= 0 or N < 0:
		raise ValueError('require finite c0 > 0 and N >= 0')
	LogU = [-math.inf] * (N + 1)
	if N >= 1:
		LogU[1] = 0.0
	Ratio = Fraction(1)
	for m in range(2, N + 1):
		Am, Bm = exact_coefficient(A(m)), exact_coefficient(B(m))
		if Am <= 0 or Bm < 0:
			raise ValueError(f'unsupported coefficients at m={m}: require finite A>0, B>=0')
		Ratio = (Am if m == 2 else Am - Bm / Ratio) / C
		if Ratio <= 0:
			raise ValueError(f'nonpositive exact recurrence step at m={m}')
		LogU[m] = math.fsum((LogU[m - 1], log_fraction(Ratio)))
		if not math.isfinite(LogU[m]):
			raise ValueError(f'nonfinite log recurrence step at m={m}')
	return LogU


def lfact(n):
	return math.lgamma(n + 1)


def main():
	print('Finite author diagnostics; positive log solver is not a stability certificate.')
	Probe = solve_u_log(lambda m: 6, lambda m: 0, 3, 2)[2]
	if not math.isclose(Probe, math.log(2), abs_tol=1e-14):
		raise AssertionError('missing c0 normalization in log recurrence')
	try:
		solve_u_log(lambda m: 1, lambda m: 1, 1, 3)
	except ValueError:
		pass
	else:
		raise AssertionError('nonpositive recurrence step was accepted')
	N = 300
	for c in (3.0, 5.0, 1.0, 0.5, 1.5):
		A = lambda m: perturbed_coefficients(c, m)[0]
		B = lambda m: perturbed_coefficients(c, m)[1]
		LogU = solve_u_log(A, B, c, N)
		Lower = (N - 1) * math.log(4 / c) + lfact(N)
		if LogU[N] < Lower - 1e-9:
			raise AssertionError(f'unperturbed growth lower bound failed for c={c}')
		print(f'Unperturbed c={c}: log u_{N}={LogU[N]:.3f}, log lower bound={Lower:.3f}, margin={LogU[N] - Lower:.3f}.')

	for D in (0.0, 1.0, 5.0, 20.0):
		A = lambda m: perturbed_coefficients(3, m, D / math.sqrt(m))[0]
		B = lambda m: perturbed_coefficients(3, m, D / math.sqrt(m))[1]
		Margin = min(A(m) - B(m) - 3 for m in range(2, N + 1))
		Status = 'hold on sampled indices' if Margin >= 0 else 'FAIL'
		print(f'Basis delta_m={D}/sqrt(m): min(A-B-c)={float(Margin):.3f}; growth hypotheses {Status}.')
		try:
			LogU = solve_u_log(A, B, 3, N)
		except ValueError as Error:
			print(f'  Positive log solver rejected: {Error}')
		else:
			print(f'  log u_{N}={LogU[N]:.3f}; finite positive solution only, no stability conclusion.')

	LogU = solve_u_log(lambda m: 1 + 1 / math.log(m), lambda m: 0, 1, 2000)
	print(f'B=0, eps=1/log(k): log u_2000 - 8 log(2000)={LogU[2000] - 8 * math.log(2000):.3f} (finite comparison).')
	return 0


if __name__ == '__main__':
	raise SystemExit(main())
