# -*- coding: utf-8 -*-
"""R-209 M3: fully symbolic asymptotic series of the exact closed 4-equation
system, assembled component-wise with truncated polynomial arithmetic
(power dicts up to u^10, truncation on every product).  eps = u^3,
u = R^(-1/6), k2 = K u, k3 = K u + c u^5, p1 = pi/2 + a u^2,
p3 = pi/4 + b u^2.  The u^2-corrected ansatz closes the truncated balance;
scipy solves the exact 8-equation system.  All series algebra is exact
(STRICT bookkeeping); matching the numerical branch is EVIDENCE.
"""
import numpy as np
from scipy.optimize import least_squares
import sympy as sp


def to_dict(expr, u, nmax):
	out = {}
	e = sp.expand(expr)
	for m in range(0, nmax + 1):
		c = e.coeff(u, m)
		if c != 0:
			out[m] = sp.simplify(c)
	return out


def mul(A, B, nmax):
	out = {}
	for m1, c1 in A.items():
		for m2, c2 in B.items():
			m = m1 + m2
			if m <= nmax:
				out[m] = out.get(m, 0) + c1*c2
	return {m: sp.simplify(c) for m, c in out.items() if c != 0}


def div_u6(A, u):
	out = {}
	for m, c in A.items():
		if m >= 6:
			out[m - 6] = c
	return out


def main():
	u = sp.symbols('u', positive=True)
	K, A, B, C = sp.symbols('K A B C')
	Nmax = 10
	eps = u**3
	k2 = K*u
	k3 = K*u + C*u**5
	p1 = sp.pi/2 + A*u**2
	p3 = sp.pi/4 + B*u**2
	fac = 1 + C*u**4/K
	p1t = p1*fac
	p3t = p3*fac
	p2 = k2/2 - eps*(p1 + p3)
	p2t = k3/2 - eps*fac*(p1 + p3)
	S = lambda x: sp.series(x, u, 0, Nmax + 1).removeO()
	s_cos_p2 = to_dict(S(sp.cos(p2)), u, Nmax)
	s_sin_p2 = to_dict(S(sp.sin(p2)), u, Nmax)
	s_cos_p2t = to_dict(S(sp.cos(p2t)), u, Nmax)
	s_sin_p2t = to_dict(S(sp.sin(p2t)), u, Nmax)
	s_cos_p1 = to_dict(S(sp.cos(p1)), u, 8)
	s_sin_p1 = to_dict(S(sp.sin(p1)), u, 8)
	s_cos_p3 = to_dict(S(sp.cos(p3)), u, 8)
	s_sin_p3 = to_dict(S(sp.sin(p3)), u, 8)
	s_cos_p1t = to_dict(S(sp.cos(p1t)), u, 8)
	s_sin_p1t = to_dict(S(sp.sin(p1t)), u, 8)
	s_cos_p3t = to_dict(S(sp.cos(p3t)), u, 8)
	s_sin_p3t = to_dict(S(sp.sin(p3t)), u, 8)
	s_sin2_p3 = to_dict(S(sp.sin(2*p3)), u, 8)
	s_sin2_p3t = to_dict(S(sp.sin(2*p3t)), u, 8)
	s_invsin2_p3 = to_dict(S(1/sp.sin(p3)**2), u, 8)
	s_invcos2_p3t = to_dict(S(1/sp.cos(p3t)**2), u, 8)
	s_invf3 = to_dict(S(1/fac**3), u, 8)
	s_invf = to_dict(S(1/fac), u, 8)
	s_cot_p1t = to_dict(S(-sp.tan(p1t - sp.pi/2)), u, 8)
	u3 = {3: sp.Integer(1)}
	u5 = {5: sp.Integer(1)}
	# M = eps cos p2 sin p1 + sin p2 cos p1
	Ms = {}
	Ms = mul(u3, mul(s_cos_p2, s_sin_p1, Nmax), Nmax)
	Ms2 = mul(s_sin_p2, s_cos_p1, Nmax)
	M = {m: Ms.get(m, 0) + Ms2.get(m, 0) for m in set(Ms) | set(Ms2)}
	M = {m: sp.simplify(c) for m, c in M.items() if c != 0}
	M2 = mul(M, M, Nmax)
	# MN = eps cos p2t sin p1t + sin p2t cos p1t
	MNs = mul(u3, mul(s_cos_p2t, s_sin_p1t, Nmax), Nmax)
	MNs2 = mul(s_sin_p2t, s_cos_p1t, Nmax)
	MN = {m: MNs.get(m, 0) + MNs2.get(m, 0) for m in set(MNs) | set(MNs2)}
	MN = {m: sp.simplify(c) for m, c in MN.items() if c != 0}
	MN2 = mul(MN, MN, Nmax)
	# D masses
	m1D = to_dict(S((p1 - sp.sin(2*p1)/2)/(2*K**3)), u, 8)
	p3half = to_dict(S(p3 - sp.sin(2*p3)/2), u, 8)
	m3D = div_u6(mul(mul(M2, p3half, Nmax), s_invsin2_p3, Nmax), u)
	for m, c in m3D.items():
		m3D[m] = c/(2*K**3)
	a1 = mul({2: sp.Integer(1)}, s_sin_p1, Nmax)
	for m in a1:
		a1[m] = a1[m]/K
	b1 = mul(s_cos_p1, {1: sp.Integer(1)}, Nmax)
	for m in b1:
		b1[m] = b1[m]/K
	a1a1 = mul(a1, a1, Nmax)
	b1b1 = mul(b1, b1, Nmax)
	p2d = to_dict(p2, u, Nmax)
	sin2p2d = to_dict(S(sp.sin(2*p2)), u, Nmax)
	cos2p2d = to_dict(S(sp.cos(2*p2)), u, Nmax)
	p2ou = {m - 1: c for m, c in p2d.items()}
	sin2p2ou = {m - 1: c for m, c in sin2p2d.items()}
	term1 = mul(mul({m: a1a1.get(m, 0) + b1b1.get(m, 0) for m in set(a1a1) | set(b1b1)}, p2ou, Nmax), {1: sp.Integer(1)/(2*K)}, Nmax)
	term2 = mul(mul({m: a1a1.get(m, 0) - b1b1.get(m, 0) for m in set(a1a1) | set(b1b1)}, sin2p2ou, Nmax), {1: sp.Integer(1)/(4*K)}, Nmax)
	term3 = mul(mul(mul(a1, b1, Nmax), {m: -c for m, c in cos2p2d.items()}, Nmax), {0: sp.Integer(1)/(2*K)}, Nmax)
	t3b = mul(mul(a1, b1, Nmax), {0: sp.Integer(1)/(2*K)}, Nmax)
	mL = {m: term1.get(m, 0) + term2.get(m, 0) + term3.get(m, 0) + t3b.get(m, 0)
		for m in set(term1) | set(term2) | set(term3) | set(t3b)}
	mL = {m: sp.simplify(c) for m, c in mL.items() if c != 0}
	ID = {m: m1D.get(m, 0) + m3D.get(m, 0) + mL.get(m, 0) for m in set(m1D) | set(m3D) | set(mL)}
	# N masses
	m1N = to_dict(S((p1t - sp.sin(2*p1t)/2)/(2*K**3)), u, 8)
	m1N = mul(m1N, s_invf3, Nmax)
	p3halfN = to_dict(S(p3t + sp.sin(2*p3t)/2), u, 8)
	m3N = div_u6(mul(mul(mul(MN2, p3halfN, Nmax), s_invcos2_p3t, Nmax), s_invf3, Nmax), u)
	for m in m3N:
		m3N[m] = m3N[m]/(2*K**3)
	a2 = mul(mul({2: sp.Integer(1)}, s_sin_p1t, Nmax), {0: sp.Integer(1)/K}, Nmax)
	a2 = mul(a2, s_invf, Nmax)
	b2 = mul({m - 1: c for m, c in s_cos_p1t.items()}, {0: sp.Integer(1)/K}, Nmax)
	b2 = mul(b2, s_invf, Nmax)
	a2a2 = mul(a2, a2, Nmax)
	b2b2 = mul(b2, b2, Nmax)
	p2td = to_dict(p2t, u, Nmax)
	sin2p2td = to_dict(S(sp.sin(2*p2t)), u, Nmax)
	cos2p2td = to_dict(S(sp.cos(2*p2t)), u, Nmax)
	inv_k3 = mul({-1: sp.Integer(1)/K}, s_invf, Nmax)
	t1n = mul(mul({m: a2a2.get(m, 0) + b2b2.get(m, 0) for m in set(a2a2) | set(b2b2)}, p2td, Nmax), {0: sp.Rational(1, 2)}, Nmax)
	t1n = mul(t1n, inv_k3, Nmax)
	t2n = mul(mul({m: a2a2.get(m, 0) - b2b2.get(m, 0) for m in set(a2a2) | set(b2b2)}, sin2p2td, Nmax), {0: sp.Rational(1, 4)}, Nmax)
	t2n = mul(t2n, inv_k3, Nmax)
	t3n = mul(mul(mul(a2, b2, Nmax), {m: -c for m, c in cos2p2td.items()}, Nmax), {0: sp.Rational(1, 2)}, Nmax)
	t3n = mul(t3n, inv_k3, Nmax)
	t3nb = mul(mul(mul(a2, b2, Nmax), {0: sp.Rational(1, 2)}, Nmax), inv_k3, Nmax)
	mLN = {m: t1n.get(m, 0) + t2n.get(m, 0) + t3n.get(m, 0) + t3nb.get(m, 0)
		for m in set(t1n) | set(t2n) | set(t3n) | set(t3nb)}
	mLN = {m: sp.simplify(c) for m, c in mLN.items() if c != 0}
	IN = {m: m1N.get(m, 0) + m3N.get(m, 0) + mLN.get(m, 0) for m in set(m1N) | set(m3N) | set(mLN)}
	# E5 = ID sin^2(p1t) - IN sin^2(p1)
	sin2p1 = mul(s_sin_p1, s_sin_p1, Nmax)
	sin2p1t = mul(s_sin_p1t, s_sin_p1t, Nmax)
	E5 = mul(ID, sin2p1t, Nmax)
	E5b = mul(IN, sin2p1, Nmax)
	E5 = {m: E5.get(m, 0) - E5b.get(m, 0) for m in set(E5) | set(E5b)}
	E5 = {m: sp.simplify(c) for m, c in E5.items() if c != 0}
	# E6 = sin p1 (eps cos p2t + sin p2t cot p1t) + eps cos p2 sin p1 + sin p2 cos p1
	t6a = mul(u3, s_cos_p2t, Nmax)
	t6b = mul(s_sin_p2t, s_cot_p1t, Nmax)
	t6 = mul(s_sin_p1, {m: t6a.get(m, 0) + t6b.get(m, 0) for m in set(t6a) | set(t6b)}, Nmax)
	t6c = mul(mul(u3, s_cos_p2, Nmax), s_sin_p1, Nmax)
	t6d = mul(s_sin_p2, s_cos_p1, Nmax)
	E6 = {m: t6.get(m, 0) + t6c.get(m, 0) + t6d.get(m, 0) for m in set(t6) | set(t6c) | set(t6d)}
	E6 = {m: sp.simplify(c) for m, c in E6.items() if c != 0}
	# E1, E2 direct series (fast)
	E1 = (sp.cos(p2)*sp.sin(p1 + p3) + sp.sin(p2)*sp.cos(p3)*sp.cos(p1)/eps
		- eps*sp.sin(p3)*sp.sin(p2)*sp.sin(p1))
	E2 = (sp.cos(p2t)*sp.cos(p1t)*sp.cos(p3t)
		- sp.sin(p3t)*sp.sin(p2t)*sp.cos(p1t)/eps
		- sp.sin(p3t)*sp.cos(p2t)*sp.sin(p1t)
		- eps*sp.cos(p3t)*sp.sin(p2t)*sp.sin(p1t))
	P = {('E1', m): c for m, c in to_dict(S(E1), u, 6).items()}
	P.update({('E2', m): c for m, c in to_dict(S(E2), u, 6).items()})
	P.update({('E5', m): c for m, c in E5.items()})
	P.update({('E6', m): c for m, c in E6.items()})
	print('coefficients:', sorted(P.keys()), flush=True)
	print('E1 u0 =', sp.nsimplify(P[('E1', 0)]), flush=True)
	print('E5 u0 =', sp.nsimplify(P[('E5', 0)]), flush=True)
	print('E6 u3 =', sp.nsimplify(P[('E6', 3)]), flush=True)
	print('E6 u5 =', sp.nsimplify(P[('E6', 5)]), flush=True)
	# ansatz
	u2 = sp.symbols('u2')
	K0, K2, A0, A2, B0, B2, C0, C2, K4, B4, C4 = sp.symbols('K0 K2 A0 A2 B0 B2 C0 C2 K4 B4 C4')
	params = {K: K0 + K2*u2 + K4*u2**2, A: 2/(K0 + K2*u2 + K4*u2**2), B: B0 + B2*u2 + B4*u2**2, C: C0 + C2*u2 + C4*u2**2}
	unk = [K0, B0, C0, K2, B2, C2, K4, B4, C4]
	Q = {}
	for key, coef in P.items():
		pc = sp.expand(sp.expand(sp.together(coef*K**8)).subs(params)*(K0 + K2*u2 + K4*u2**2)**8*K0**8)
		name, m = key
		for j in range(0, 5):
			cj = pc.coeff(u2, j)
			if cj != 0:
				Q[(name, m, j)] = sp.simplify(cj)
	print('Q keys:', sorted(Q.keys()), flush=True)
	print('E5 u4:', P[('E5', 4)], flush=True)
	print('E5 u4 numeric at (3.5,0.55,0.27,1.6):', P[('E5', 4)].subs({K: sp.Rational(35,10), A: sp.Rational(55,100), B: sp.Rational(27,100), C: sp.Rational(16,10)}), flush=True)
	orders = [('E1', 2), ('E1', 4), ('E1', 6), ('E2', 2), ('E2', 4), ('E2', 6), ('E5', 4), ('E5', 5), ('E5', 6), ('E6', 5), ('E6', 7)]
	sys = [sum(Q.get((name, m, j), 0) for m in range(0, 11) for j in range(0, 5)
			if m + 2*j == n) for (name, n) in orders]
	Fn = sp.lambdify(unk, sys, 'numpy')
	guess = [3.19, 0.28, 1.6, 1.5, -0.4, -3.0, 0.0, 0.0, 0.0]
	sol = least_squares(lambda z: np.array(Fn(*z), dtype=float), guess,
		xtol=1e-13, ftol=1e-13, gtol=1e-13, max_nfev=20000)
	print('=== scipy solve ===', flush=True)
	for var, val in zip(unk, sol.x):
		print('  %s = %.12f' % (var, val), flush=True)
	print('  |residual| = %.3e' % np.max(np.abs(sol.fun)), flush=True)
	rest = [(name, n) for name in ['E1', 'E2', 'E5', 'E6'] for n in [0, 2, 3, 4, 5, 6, 7, 8, 9, 10]
		if (name, n) not in orders]
	for o in rest:
		expr = sum(Q.get((o[0], m, j), 0) for m in range(0, 11) for j in range(0, 5)
			if m + 2*j == o[1])
		val = float(sp.N(sp.sympify(expr).subs(dict(zip(unk, sol.x))), 30))
		if abs(val) > 1e-12:
			print('  CHECK %s: residual %.3e' % (o, val), flush=True)

	K0v, B0v, C0v = sol.x[0], sol.x[1], sol.x[2]
	A0v = 2/K0v
	print('predicted limits: K=%.6f a=%.6f b=%.6f c=%.6f' % (K0v, A0v, B0v, C0v))
	print('a0*K0 = %.6f,  D*R -> 2*K*c = %.6f' % (A0v*K0v, 2*K0v*C0v))


if __name__ == '__main__':
	main()
