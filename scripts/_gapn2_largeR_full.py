# -*- coding: utf-8 -*-
"""R-209 M3: full integer-power-series solve of the exact closed 4-equation
system (E1,E2,E5,E6) with all powers u^0..u^8 in (K,a,b,c).  The even-only
ansatz is inconsistent (E5_5 = 1/(2K^2) is a hard constant), so odd powers
are mandatory.  Series algebra exact (STRICT bookkeeping); root finding
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


def smul(X, Y, nmax):
	out = {}
	for i, cx in X.items():
		for j, cy in Y.items():
			m = i + j
			if m <= nmax:
				out[m] = out.get(m, 0) + cx*cy
	return out


def spow(X, n, nmax):
	if n == 0:
		return {0: sp.Integer(1)}
	out = spow(X, n // 2, nmax)
	out = smul(out, out, nmax)
	if n % 2 == 1:
		out = smul(out, X, nmax)
	return out


def build_system(P, unk, nmax=9):
	K0, K1, K2, K3, K4, K5, K6, K7, K8 = unk[0:9]
	A0, A1, A2, A3, A4, A5, A6, A7, A8 = unk[9:18]
	B0, B1, B2, B3, B4, B5, B6 = unk[18:25]
	C0, C1, C2, C3, C4, C5, C6 = unk[25:32]
	Ks = {i: v for i, v in enumerate([K0, K1, K2, K3, K4, K5, K6, K7, K8])}
	As = {i: v for i, v in enumerate([A0, A1, A2, A3, A4, A5, A6, A7, A8])}
	Bs = {i: v for i, v in enumerate([B0, B1, B2, B3, B4, B5, B6])}
	Cs = {i: v for i, v in enumerate([C0, C1, C2, C3, C4, C5, C6])}
	degK = []
	degA = []
	degB = []
	degC = []
	for coef in P.values():
		num, den = sp.fraction(sp.together(coef))
		pd = sp.Poly(num, K, A, B, C)
		degK.append(pd.degree(K))
		degA.append(pd.degree(A))
		degB.append(pd.degree(B))
		degC.append(pd.degree(C))
	Kmax = max(degK) + 8
	Amax = max(degA)
	Bmax = max(degB)
	Cmax = max(degC)
	print('max degrees: K=%d A=%d B=%d C=%d' % (Kmax, Amax, Bmax, Cmax), flush=True)
	Kpow = {n: spow(Ks, n, nmax) for n in range(0, Kmax + 1)}
	Apow = {n: spow(As, n, nmax) for n in range(0, Amax + 1)}
	Bpow = {n: spow(Bs, n, nmax) for n in range(0, Bmax + 1)}
	Cpow = {n: spow(Cs, n, nmax) for n in range(0, Cmax + 1)}
	Q = {}
	for key, coef in P.items():
		num, den = sp.fraction(sp.together(coef))
		if den != 1 and den.has(K):
			pdn = sp.Poly(den, K).degree()
			num2 = sp.together(coef*K**pdn)
			assert sp.fraction(num2)[1] == 1, ('non-K denominator for', key, den)
			num = num2
		poly = sp.Poly(num, K, A, B, C)
		acc = {}
		for mon, cmon in zip(poly.monoms(), poly.coeffs()):
			s = {0: cmon}
			if mon[0]:
				s = smul(s, Kpow[mon[0]], nmax)
			if mon[1]:
				s = smul(s, Apow[mon[1]], nmax)
			if mon[2]:
				s = smul(s, Bpow[mon[2]], nmax)
			if mon[3]:
				s = smul(s, Cpow[mon[3]], nmax)
			for m, c in s.items():
				acc[m] = acc.get(m, 0) + c
		name, m = key
		for j, c in acc.items():
			if c != 0:
				Q[(name, m, j)] = sp.simplify(c)
	Sys = {}
	for name in ['E1', 'E2', 'E5', 'E6']:
		mmax = max(m for (nm, m) in P if nm == name)
		for n in range(0, nmax + 1):
			total = sum(Q.get((name, m, j), 0) for m in range(0, mmax + 1) for j in range(0, nmax + 1)
				if m + j == n)
			if total != 0:
				Sys[(name, n)] = sp.simplify(total)
	return Sys, Q


def main():
	P = loadP()
	unk = sp.symbols('K0 K1 K2 K3 K4 K5 K6 K7 K8 A0 A1 A2 A3 A4 A5 A6 A7 A8 B0 B1 B2 B3 B4 B5 B6 C0 C1 C2 C3 C4 C5 C6')
	Sys, Q = build_system(P, unk)
	orders = ([( 'E1', n) for n in range(0, 9)]
		+ [('E2', n) for n in range(0, 9)]
		+ [('E5', n) for n in range(0, 10)]
		+ [('E6', n) for n in [3, 5, 7, 9]])
	print('system: %d equations, %d unknowns' % (len(orders), len(unk)), flush=True)
	Fn = sp.lambdify(unk, [Sys[o] for o in orders], 'numpy')
	guess = np.zeros(len(unk))
	g = {'K0': 3.4553, 'K1': 0.02, 'K2': 2.937,
		'A0': 2/3.4553, 'A2': -0.643,
		'B0': 0.2898, 'B2': -0.469,
		'C0': 1.4741, 'C2': 3.466}
	for i, s in enumerate(unk):
		guess[i] = g.get(str(s), 0.0)
	# A1 tied by A1 = a0 K1 + a1 K0 = 0
	guess[unk.index(sp.Symbol('A1'))] = -guess[unk.index(sp.Symbol('A0'))]*guess[unk.index(sp.Symbol('K1'))]/guess[unk.index(sp.Symbol('K0'))]
	fun = lambda z: np.array(Fn(*z), dtype=float)
	print('initial |res| = %.3e' % np.max(np.abs(fun(guess))), flush=True)
	sol = least_squares(fun, guess, x_scale='jac', xtol=1e-13, ftol=1e-13, gtol=1e-13, max_nfev=20000)
	print('=== full solve ===', flush=True)
	for s, val in zip(unk, sol.x):
		if abs(val) > 1e-10:
			print('  %s = %.12f' % (s, val), flush=True)
	print('  |residual| = %.3e' % np.max(np.abs(sol.fun)), flush=True)
	for (name, n), v in zip(orders, sol.fun):
		if abs(v) > 1e-8:
			print('  RES %s_%d = %.3e' % (name, n, v), flush=True)
	z = dict(zip(unk, sol.x))
	# validate against data at last row u = 0.149409...
	import json
	rows = json.load(open(r'scripts/_gapn2_largeR_big.json', encoding='utf-8'))
	Rlast, ulast = rows[-1][0], rows[-1][1]
	def val_series(ser, uu):
		return float(sum(z[s]*uu**i for s, i in zip(unk, ser) if i <= 8))
	Kser = list(range(0, 9))
	Aser = list(range(0, 9))
	Bser = list(range(0, 7))
	Cser = list(range(0, 7))
	Kv = val_series(Kser, ulast)
	av = val_series(Aser, ulast)
	bv = val_series(Bser, ulast)
	cv = val_series(Cser, ulast)
	k2s = Kv*ulast
	k3s = Kv*ulast + cv*ulast**5
	p1s = np.pi/2 + av*ulast**2
	p3s = np.pi/4 + bv*ulast**2
	print('validation at R=%.4g (data row):' % Rlast)
	print('  series: k2=%.9f k3=%.9f p1=%.9f p3=%.9f' % (k2s, k3s, p1s, p3s))
	print('  series D*R=%.6f Dk/u7=%.6f' % ((k3s**2-k2s**2)/ulast**6, (k3s-k2s)/ulast**7))
	print('  data:   K=%.6f a=%.6f b=%.6f D*R=%.6f Dk/u7=%.6f' % (rows[-1][2], rows[-1][3], rows[-1][4], rows[-1][6], rows[-1][5]))
	# leading observables
	K0v, C0v, B0v, A0v = z[sp.Symbol('K0')], z[sp.Symbol('C0')], z[sp.Symbol('B0')], z[sp.Symbol('A0')]
	print('limit: K0=%.8f a0=%.8f b0=%.8f c0=%.8f, a0*K0=%.10f' % (K0v, A0v, B0v, C0v, A0v*K0v))
	print('D*R -> 2 K0 c0 = %.8f' % (2*K0v*C0v))


if __name__ == '__main__':
	main()
