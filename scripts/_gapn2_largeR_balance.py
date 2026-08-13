# -*- coding: utf-8 -*-
"""R-209 M3: hybrid leading-balance solver for the large-R n=2 symmetric
branch.  Exact symbolic coefficients for E1/E2 (fast series), high-precision
mpmath Richardson extraction for E5/E6 (the slow series), all in the ansatz

	k2 = K u,  k3 = K u + c u^5,  p1 = pi/2 + a u^2,  p3 = pi/4 + b u^2,
	eps = u^3,  u = R^(-1/6),
	K = K0 + K2 u^2,  a = A0 + A2 u^2,  b = B0 + B2 u^2,  c = C0 + C2 u^2.

Balance equations: E1 u^0, E1 u^2 (u2^0 and u2^1), E2 u^2 (u2^0 and u2^1),
E5 u^6, E6 u^5, E6 u^6.  Residual checks: E1 u^4, E2 u^4, E5 u^8, E6 u^7.
All series algebra exact; everything numeric is EVIDENCE.
"""
import numpy as np
from scipy.optimize import least_squares
import mpmath as mp
import sympy as sp


def richardson(y, u0, powers, dps):
	mp.mp.dps = dps
	us = [mp.mpf(u0)*mp.mpf(2)**(-j) for j in range(len(y))]
	coefs = {}
	for m in powers:
		r = [(y[j] - sum(coefs.get(l, mp.mpf(0))*us[j]**l for l in powers if l < m))
			/us[j]**m for j in range(len(y))]
		for s in range(1, len(y)):
			fac = mp.mpf(2)**s
			r = [(fac*r[j+1] - r[j])/(fac - 1) for j in range(len(r) - 1)]
		coefs[m] = r[0]
	return coefs


def eval_e5_e6(X, u):
	K0, A0, B0, C0, K2, A2, B2, C2 = X
	u2 = u*u
	K = K0 + K2*u2
	A = A0 + A2*u2
	B = B0 + B2*u2
	C = C0 + C2*u2
	eps = u**3
	k2 = K*u
	k3 = K*u + C*u**5
	p1 = mp.pi/2 + A*u2
	p3 = mp.pi/4 + B*u2
	p1t = p1*(1 + C*u**4/K)
	p3t = p3*(1 + C*u**4/K)
	p2 = k2/2 - eps*(p1 + p3)
	p2t = k3/2 - eps*(1 + C*u**4/K)*(p1 + p3)
	E5 = 0
	ID = mass(k2, p1, p2, p3, eps, 'D')
	IN = mass(k3, p1t, p2t, p3t, eps, 'N')
	E5 = ID*mp.sin(p1t)**2 - IN*mp.sin(p1)**2
	E6 = (mp.sin(p1)*(eps*mp.cos(p2t) + mp.sin(p2t)*mp.cos(p1t)/mp.sin(p1t))
		+ eps*mp.cos(p2)*mp.sin(p1) + mp.sin(p2)*mp.cos(p1))
	return E5, E6


def mass(k, p1, p2, p3, eps, mode):
	if mode == 'D':
		BC = -(eps*mp.cos(p2)*mp.sin(p1)/k + mp.sin(p2)*mp.cos(p1)/k)/mp.sin(p3)
		m3 = BC**2*(p3 - mp.sin(2*p3)/2)/(2*k*eps)
	else:
		BC = (eps*mp.cos(p2)*mp.sin(p1)/k + mp.sin(p2)*mp.cos(p1)/k)/mp.cos(p3)
		m3 = BC**2*(p3 + mp.sin(2*p3)/2)/(2*k*eps)
	m1 = (p1 - mp.sin(2*p1)/2)*eps/(2*k**3)
	a = eps*mp.sin(p1)/k
	b = mp.cos(p1)/k
	mL = ((a*a + b*b)*p2/(2*k) + (a*a - b*b)*mp.sin(2*p2)/(4*k)
		+ a*b*(1 - mp.cos(2*p2))/(2*k))
	return m1 + m3 + mL


def make_symbolic():
	u = sp.symbols('u', positive=True)
	K, A, B, C = sp.symbols('K A B C')
	eps = u**3
	k2 = K*u
	k3 = K*u + C*u**5
	p1 = sp.pi/2 + A*u**2
	p3 = sp.pi/4 + B*u**2
	p1t = p1*(1 + C*u**4/K)
	p3t = p3*(1 + C*u**4/K)
	p2 = k2/2 - eps*(p1 + p3)
	p2t = k3/2 - eps*(1 + C*u**4/K)*(p1 + p3)
	E1 = (sp.cos(p2)*sp.sin(p1 + p3) + sp.sin(p2)*sp.cos(p3)*sp.cos(p1)/eps
		- eps*sp.sin(p3)*sp.sin(p2)*sp.sin(p1))
	E2 = (sp.cos(p2t)*sp.cos(p1t)*sp.cos(p3t)
		- sp.sin(p3t)*sp.sin(p2t)*sp.cos(p1t)/eps
		- sp.sin(p3t)*sp.cos(p2t)*sp.sin(p1t)
		- eps*sp.cos(p3t)*sp.sin(p2t)*sp.sin(p1t))
	u2 = sp.symbols('u2')
	K0, K2, A0, A2, B0, B2, C0, C2 = sp.symbols('K0 K2 A0 A2 B0 B2 C0 C2')
	params = {K: K0 + K2*u2, A: A0 + A2*u2, B: B0 + B2*u2, C: C0 + C2*u2}
	unk = [K0, A0, B0, C0, K2, A2, B2, C2]
	sym = {}
	for name, expr, nterms in [('E1', E1, 6), ('E2', E2, 6)]:
		s = sp.series(expr, u, 0, nterms).removeO()
		for m in range(nterms):
			coef = s.coeff(u, m)
			if coef != 0:
				pc = sp.expand(coef.subs(params))
				for j in range(0, 3):
					cj = sp.simplify(pc.coeff(u2, j))
					if cj != 0:
						sym[(name, m, j)] = sp.lambdify(unk, cj, 'numpy')
	return sym


def make_residual():
	sym = make_symbolic()
	orders = [('E1', 0, 0), ('E1', 2, 0), ('E1', 2, 1),
		('E2', 2, 0), ('E2', 2, 1)]
	extra_orders = [('E1', 4, 0), ('E2', 4, 0)]

	def residual(X):
		Xl = [float(x) for x in X]
		vals = [float(sym[o](*Xl)) for o in orders]
		# numeric Richardson extraction for E5 u^6 and E6 u^5, u^6
		u0 = 0.25
		J = 13
		dps = 90
		Xm = [mp.mpf(str(x)) for x in Xl]
		y5 = []
		y6 = []
		us = [mp.mpf(u0)*mp.mpf(2)**(-j) for j in range(J)]
		for uu in us:
			e5, e6 = eval_e5_e6(Xm, uu)
			y5.append(e5)
			y6.append(e6)
		c5 = richardson(y5, u0, [0, 2, 4, 6], dps)
		c6 = richardson(y6, u0, [3, 5, 7], dps)
		vals.append(float(c5[4]))
		vals.append(float(c6[5]))
		vals.append(float(c5[6]))
		return np.array(vals)

	def extra(X):
		Xl = [float(x) for x in X]
		vals = [float(sym[o](*Xl)) for o in extra_orders]
		u0 = 0.25
		J = 13
		dps = 90
		Xm = [mp.mpf(str(x)) for x in Xl]
		y5 = []
		y6 = []
		us = [mp.mpf(u0)*mp.mpf(2)**(-j) for j in range(J)]
		for uu in us:
			e5, e6 = eval_e5_e6(Xm, uu)
			y5.append(e5)
			y6.append(e6)
		c5 = richardson(y5, u0, [0, 2, 4, 6, 8], dps)
		c6 = richardson(y6, u0, [3, 5, 7, 9], dps)
		vals.append(float(c5[8]))
		vals.append(float(c6[9]))
		return np.array(vals)

	return residual, extra


def main():
	residual, extra = make_residual()
	guess = [3.19, 2/3.19, 0.28, 1.55, 1.5, -0.5, -0.2, -3.0]
	sol = least_squares(residual, guess, xtol=1e-12, ftol=1e-12,
		gtol=1e-12, max_nfev=5000, diff_step=1e-6)
	print('=== balance solution ===')
	for name, val in zip(['K0', 'A0', 'B0', 'C0', 'K2', 'A2', 'B2', 'C2'], sol.x):
		print('  %s = %.10f' % (name, val))
	print('  |residual| = %.3e' % np.max(np.abs(sol.fun)))
	ext = extra(sol.x)
	print('  extra constraints:', ['%.3e' % v for v in ext])
	K0v, A0v, B0v, C0v = sol.x[0], sol.x[1], sol.x[2], sol.x[3]
	print('predicted limits: K=%.6f a=%.6f b=%.6f c=%.6f' % (K0v, A0v, B0v, C0v))
	print('a0 - 2/K0 = %.3e,  D*R -> 2*K*c = %.6f' % (A0v - 2/K0v, 2*K0v*C0v))
	print('M/u^5 -> c_M = 3*pi/(2K) - K^2/12 = %.6f (observed ~0.59)' %
		(3*np.pi/(2*K0v) - K0v**2/12))


if __name__ == '__main__':
	main()
