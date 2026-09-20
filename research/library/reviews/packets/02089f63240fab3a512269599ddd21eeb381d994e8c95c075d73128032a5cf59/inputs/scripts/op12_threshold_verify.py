# -*- coding: utf-8 -*-
"""Finite partial sums for B=0 examples, not convergence tests.

The analytic series boundaries use u_m ~ const*(log m)^C for C/(k log k)
(C>0), or u_m ~ m^C/Gamma(2+C) for C/k (C>=0). These are not upper
bounds for a general second-order recurrence with the same eps.
"""
import mpmath as mp

from op12_dichotomy_verify import power_product, u_sequence


def diag_partial(u, beta, Ns):
	"""Selected finite partial sums; preserve the existing (N, string) interface."""
	if not 0 <= Ns < len(u):
		raise ValueError('require 0 <= Ns < len(u)')
	Beta = mp.mpf(beta)
	Total = mp.mpf(0)
	Output = []
	Checkpoints = {Ns // 8, Ns // 4, Ns // 2, Ns}
	for N in range(1, Ns + 1):
		Total += u[N]**2 * mp.power(2 * N + 1, -2 * Beta)
		if N in Checkpoints:
			Output.append((N, mp.nstr(Total, 10)))
	return Output


def main():
	with mp.workdps(60):
		print('B=0 product examples only; each displayed number is a finite partial sum.')
		print('Series labels come from analytic asymptotics, not convergence of these samples.')
		for N in (10000, 20000):
			u = u_sequence(lambda k: 1 / (k * mp.log(k)), N)
			print(f'eps=1/(k log(k)), N={N}:')
			for Beta in (mp.mpf('0.5'), mp.mpf('0.6')):
				Behavior = 'converges' if Beta > mp.mpf('0.5') else 'diverges'
				print(f'  beta={Beta}: {diag_partial(u, Beta, N)}; analytic B=0 series: {Behavior}.')

		N = 20000
		u = u_sequence(lambda k: mp.mpf(2) / k, N)
		if not mp.almosteq(u[N], power_product(2, N), rel_eps=mp.mpf('1e-50')):
			raise AssertionError('Gamma(2+C) product normalization regression')
		print(f'eps=2/k: u_{N}/N^2={mp.nstr(u[N] / N**2, 12)}; limit=1/Gamma(4)=1/6.')
		for Beta in (mp.mpf('2.4'), mp.mpf('2.5'), mp.mpf('2.6')):
			Behavior = 'converges' if Beta > mp.mpf('2.5') else 'diverges'
			print(f'  beta={Beta}: {diag_partial(u, Beta, N)}; analytic B=0 series: {Behavior}.')
	return 0


if __name__ == '__main__':
	raise SystemExit(main())
