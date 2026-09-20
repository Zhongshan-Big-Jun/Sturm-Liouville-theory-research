# -*- coding: utf-8 -*-
"""Positive-step log recurrence diagnostics, not a stability certification.

The growth lemma needs the actual B>=0 and A-B>=c0 at every step.
The solver can also handle decreasing positive solutions, but cannot certify
sign-changing recurrences or infer completeness from a finite run.
"""
import math

from d3_stability_verify import perturbed_coefficients


def solve_u_log(A, B, c0, N):
	"""Return log(u_m), u0=0, u1=1; reject unsupported/nonpositive steps.

	Domain: finite c0>0, A_m>0, B_m>=0, and positive computed u_m (m>=1).
	The subtractive term is evaluated by log differences and expm1; no ratio
	u_(m-1)/u_(m-2) is exponentiated. Near cancellation is conservatively
	rejected at floating-point resolution. This is not interval arithmetic.
	"""
	if not math.isfinite(c0) or c0 <= 0 or N < 0:
		raise ValueError('require finite c0 > 0 and N >= 0')
	LogU = [-math.inf] * (N + 1)
	if N >= 1:
		LogU[1] = 0.0
	LogC = math.log(c0)
	for m in range(2, N + 1):
		Am, Bm = A(m), B(m)
		if not math.isfinite(Am) or not math.isfinite(Bm) or Am <= 0 or Bm < 0:
			raise ValueError(f'unsupported coefficients at m={m}: require finite A>0, B>=0')
		LogA = math.log(Am)
		Correction = 0.0
		if Bm > 0 and m > 2:
			Terms = (math.log(Bm), -LogA, LogU[m - 2], -LogU[m - 1])
			LogRatio = math.fsum(Terms)
			Resolution = 16 * math.ulp(max(1.0, *(abs(Term) for Term in Terms)))
			if LogRatio >= -Resolution:
				raise ValueError(f'nonpositive or numerically unresolved recurrence step at m={m}')
			Correction = math.log(-math.expm1(LogRatio))
		LogU[m] = LogA + LogU[m - 1] + Correction - LogC
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
