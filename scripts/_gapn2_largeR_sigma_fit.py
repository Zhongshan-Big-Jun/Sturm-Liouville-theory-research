# -*- coding: utf-8 -*-
"""R-209 M3: free-exponent fits a(u) = a0 + a1*u^s (+ optional a2*u^(2s))
for the large-R observables to identify the Puiseux exponent s of the
singular branch.  EVIDENCE only.
"""
import json
import numpy as np
from scipy.optimize import least_squares


def fit(v, u, two_terms=False):
	def fun(z):
		if two_terms:
			v0, v1, s, v2 = z
			return v - (v0 + v1*u**s + v2*u**(2*s))
		v0, v1, s = z
		return v - (v0 + v1*u**s)
	guess = [v[-1] - (v[-1]-v[0])*0.4, (v[-1]-v[0])/u[-1], 1.0]
	if two_terms:
		guess = guess + [0.0]
	sol = least_squares(fun, guess, xtol=1e-13, ftol=1e-13, gtol=1e-13, max_nfev=4000)
	res = np.max(np.abs(sol.fun))
	return sol.x, res


def main():
	rows = json.load(open(r'scripts/_gapn2_largeR_big.json', encoding='utf-8'))
	A = np.array(rows)
	R, u, K, a, b, Dku7, DR, Mu5 = A.T
	c = Dku7*u*u
	names = ['K', 'a', 'b', 'c=Dk/u5', 'D*R', 'M/u5']
	vals = [K, a, b, c, DR, Mu5]
	for name, v in zip(names, vals):
		for two in (False, True):
			z, res = fit(v, u, two)
			if two:
				print('%s  v0=%.6f v1=%.6f s=%.6f v2=%.6f resid=%.3e'
					% (name, z[0], z[1], z[2], z[3], res))
			else:
				print('%s  v0=%.6f v1=%.6f s=%.6f resid=%.3e'
					% (name, z[0], z[1], z[2], res))
		print()


if __name__ == '__main__':
	main()
