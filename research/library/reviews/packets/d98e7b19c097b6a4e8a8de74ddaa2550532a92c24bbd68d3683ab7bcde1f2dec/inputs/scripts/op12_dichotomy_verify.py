# -*- coding: utf-8 -*-
"""Finite diagnostics for B=0 product examples, not a general dichotomy.

u0=0, u1=1 and u_m=prod_{k=2}^m(1+eps_k). For eps_k=C/k (C>=0),
u_m=Gamma(m+1+C)/(Gamma(2+C)*Gamma(m+1)) ~ m^C/Gamma(2+C).
For eps_k=C/(k*log(k)) with C>0, u_m is asymptotic to a positive
constant times (log m)^C. The respective diagonal-series boundaries are
beta=C+1/2 and beta=1/2. Finite partial sums do not decide convergence.
For c0>0, B>=0 and eps>=0 the product is only a lower bound on the actual
solution; S=O(log m) does not bound that solution from above.
"""
import mpmath as mp

from op12_sparse_check import is_sparse, lu


def u_sequence(eps, N):
	"""B=0 product sequence with nonnegative eps; u0=0 and u1=1."""
	if N < 0:
		raise ValueError('require N >= 0')
	u = [mp.mpf(1)] * (N + 1)
	u[0] = mp.mpf(0)
	for m in range(2, N + 1):
		Eps = mp.mpf(eps(m))
		if not mp.isfinite(Eps) or Eps < 0:
			raise ValueError(f'require finite eps >= 0 at m={m}')
		u[m] = u[m - 1] * (1 + Eps)
	return u


def power_product(C, m):
	"""Gamma formula for eps_k=C/k, starting at k=2, with u0=0."""
	C = mp.mpf(C)
	if not mp.isfinite(C) or C < 0 or m < 0:
		raise ValueError('require finite C >= 0 and m >= 0')
	if m == 0:
		return mp.mpf(0)
	return mp.exp(mp.loggamma(m + 1 + C) - mp.loggamma(2 + C) - mp.loggamma(m + 1))


def diag_series(u, N, beta):
	"""Finite sum over m=1..N, never a convergence test."""
	if not 0 <= N < len(u):
		raise ValueError('require 0 <= N < len(u)')
	Beta = mp.mpf(beta)
	return mp.fsum(u[m]**2 * mp.power(2 * m + 1, -2 * Beta) for m in range(1, N + 1))


def eps_sparse(k):
	"""Legacy value helper uses arbitrary precision; diagnostics use lu instead."""
	return mp.exp(k) if is_sparse(k) else mp.mpf(0)


def main():
	with mp.workdps(60):
		print('B=0 product diagnostics only; finite sums do not establish convergence or completeness.')
		u = u_sequence(lambda k: 1 / mp.sqrt(k), 4000)
		print(f'eps=k^(-1/2): log u_4000/log(4000)={mp.nstr(mp.log(u[4000]) / mp.log(4000), 10)} (finite growth diagnostic).')

		N = 20000
		for C in (1, 2):
			u = u_sequence(lambda k: C / (k * mp.log(k)), N)
			print(f'eps={C}/(k log(k)), N={N}: log u_N/loglog(N)={mp.nstr(mp.log(u[N]) / mp.log(mp.log(N)), 10)}.')
			if C == 1:
				for Beta in (mp.mpf('0.5'), mp.mpf('0.6'), mp.mpf(1)):
					Behavior = 'converges' if Beta > mp.mpf('0.5') else 'diverges'
					print(f'  beta={Beta}: finite partial sum={mp.nstr(diag_series(u, N, Beta), 10)}; analytic B=0 series: {Behavior}.')

		LogU, Count = lu(4000)
		Jumps = [k for k in range(2, 4001) if is_sparse(k)]
		if Jumps != [4, 16, 256] or Count != 3:
			raise AssertionError(f'sparse-index regression: {Jumps}')
		print(f'Sparse B=0 example: jumps={Jumps}; log u_4000={mp.nstr(LogU[4000], 12)} (finite value).')

		N = 5000
		u = u_sequence(lambda k: mp.mpf(2) / k, N)
		if not mp.almosteq(u[N], power_product(2, N), rel_eps=mp.mpf('1e-50')):
			raise AssertionError('Gamma(2+C) product normalization regression')
		print(f'eps=2/k: u_{N}/N^2={mp.nstr(u[N] / N**2, 12)}; limit=1/Gamma(4)=1/6.')
		for Beta in (mp.mpf('2.4'), mp.mpf('2.5'), mp.mpf('2.6')):
			Behavior = 'converges' if Beta > mp.mpf('2.5') else 'diverges'
			print(f'  beta={Beta}: finite partial sum (N={N})={mp.nstr(diag_series(u, N, Beta), 10)}; analytic B=0 series: {Behavior}.')
	return 0


if __name__ == '__main__':
	raise SystemExit(main())
