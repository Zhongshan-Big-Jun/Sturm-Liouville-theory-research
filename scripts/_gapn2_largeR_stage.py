# -*- coding: utf-8 -*-
"""R-209 M3: staged even-power-series solve of the exact 4-equation system.
Stage A: u=0 limit (K0,b0,c0).  All series algebra exact; root finding
numerical (EVIDENCE at machine precision).
"""
import pickle
import numpy as np
import sympy as sp
from scipy.optimize import least_squares

u = sp.symbols('u', positive=True)
K, A, B, C = sp.symbols('K A B C')


def loadP():
	with open(r'scripts/_gapn2_largeR_P.pkl', 'rb') as f:
		return pickle.load(f)


def sub_series(P, params, umax, kmult=8):
	Q = {}
	for key, coef in P.items():
		pc = sp.expand(sp.together(coef*K**kmult).subs(params))
		name, m = key
		deg = sp.Poly(pc, u).degree() if pc != 0 else 0
		for j in range(0, deg // 2 + 1):
			cj = pc.coeff(u, 2*j)
			if cj != 0:
				Q[(name, m, j)] = sp.simplify(cj)
	return Q


def totals(Q, name, n):
	return sp.simplify(sum(Q.get((name, m, j), 0) for m in range(0, 11) for j in range(0, 6)
		if m + 2*j == n))


def main():
	P = loadP()
	# stage A: limit-level equations in (K0, b0, c0), a0 = 2/K0
	K0, B0, C0 = sp.symbols('K0 B0 C0')
	params = {K: K0, A: 2/K0, B: B0, C: C0}
	QA = sub_series(P, params, 0)
	lim_eqs = [('E1', 2), ('E2', 2), ('E5', 2), ('E5', 5), ('E6', 5)]
	F = [totals(QA, name, n) for (name, n) in lim_eqs]
	print('limit-level equation sizes:', [sp.count_ops(f) for f in F])
	Fn = sp.lambdify((K0, B0, C0), F, 'numpy')
	guess = [3.4553, 0.2898, 1.4741]
	sol = least_squares(lambda z: np.array(Fn(*z), dtype=float), guess,
		xtol=1e-13, ftol=1e-13, gtol=1e-13, max_nfev=8000)
	print('=== stage A ===')
	for var, val in zip('K0 B0 C0'.split(), sol.x):
		print('  %s = %.12f' % (var, val))
	print('  |residual| = %.3e' % np.max(np.abs(sol.fun)))
	for (name, n), v in zip(lim_eqs, sol.fun):
		print('  %s_%d = %.3e' % (name, n, v))
	# rank check of the 5x3 Jacobian at the root
	J = np.zeros((5, 3))
	for i in range(5):
		for j in range(3):
			J[i, j] = float(sp.diff(F[i], (K0, B0, C0)[j]).subs({K0: sol.x[0], B0: sol.x[1], C0: sol.x[2]}))
	print('  jacobian singular values:', np.linalg.svd(J, compute_uv=False))
	print('K0 fit 3.4553 vs solved; a0 = 2/K0 = %.8f' % (2/sol.x[0]))


if __name__ == '__main__':
	main()
