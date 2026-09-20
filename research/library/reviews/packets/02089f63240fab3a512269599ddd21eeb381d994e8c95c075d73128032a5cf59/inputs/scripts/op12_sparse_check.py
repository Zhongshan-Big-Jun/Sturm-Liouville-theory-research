# -*- coding: utf-8 -*-
"""B=0 product with eps_k=exp(k) at k=2^(2^j), j>=1, computed in log-space.

For m>=4, the last jump K satisfies K<=m<K^2, hence S(m)>=K>sqrt(m).
The count is floor(log_2(log_2(m))). These analytic observations are distinct
from the finite diagnostics below; no completeness proof is asserted here.
"""
import mpmath as mp


def is_sparse(k):
	"""Exactly 4, 16, 256, 65536, ...; the exponent must be a power of two."""
	if k < 4 or k & (k - 1):
		return False
	Exponent = k.bit_length() - 1
	return Exponent & (Exponent - 1) == 0


def log_sparse_factor(k):
	"""log(1+eps_k) without forming exp(k)."""
	if not is_sparse(k):
		return mp.mpf(0)
	return mp.mpf(k) + mp.log1p(mp.exp(-k))


def lu(N):
	"""Return log(u_0..u_N), jump count; u0=0, u1=1."""
	if N < 0:
		raise ValueError('require N >= 0')
	LogU = [mp.mpf(0)] * (N + 1)
	LogU[0] = -mp.inf
	Count = 0
	for m in range(2, N + 1):
		LogU[m] = LogU[m - 1]
		if is_sparse(m):
			Count += 1
			LogU[m] += log_sparse_factor(m)
	return LogU, Count


def main():
	with mp.workdps(60):
		N = 65536
		LogU, Count = lu(N)
		Jumps = [k for k in range(2, N + 1) if is_sparse(k)]
		if Jumps != [4, 16, 256, 65536] or Count != 4:
			raise AssertionError(f'sparse-index regression: {Jumps}, count={Count}')
		print(f'B=0 sparse product: jumps through {N} = {Jumps}.')
		for m in (4000, N):
			if not mp.isfinite(LogU[m]):
				raise AssertionError(f'nonfinite sparse log at m={m}')
			print(f'  m={m}: log u_m={mp.nstr(LogU[m], 12)}, log u_m/log m={mp.nstr(LogU[m] / mp.log(m), 10)} (finite values).')
		print('Analytic bound: S(m)>=K>sqrt(m) for last jump K; finite values alone do not prove completeness.')
	return 0


if __name__ == '__main__':
	raise SystemExit(main())
