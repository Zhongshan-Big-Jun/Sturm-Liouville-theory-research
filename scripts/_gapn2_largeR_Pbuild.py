# -*- coding: utf-8 -*-
"""R-209 M3: build the exact truncated power-series coefficient dict P for
E1,E2,E5,E6 in the (K,A,B,C) ansatz
	k2=K*u, k3=K*u+C*u^5, p1=pi/2+A*u^2, p3=pi/4+B*u^2, eps=u^3
and pickle it for the staged Puiseux solver.  All series algebra exact
(STRICT bookkeeping).
"""
import pickle
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


def build():
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
	Ms = mul(u3, mul(s_cos_p2, s_sin_p1, Nmax), Nmax)
	Ms2 = mul(s_sin_p2, s_cos_p1, Nmax)
	M = {m: Ms.get(m, 0) + Ms2.get(m, 0) for m in set(Ms) | set(Ms2)}
	M = {m: sp.simplify(c) for m, c in M.items() if c != 0}
	M2 = mul(M, M, Nmax)
	MNs = mul(u3, mul(s_cos_p2t, s_sin_p1t, Nmax), Nmax)
	MNs2 = mul(s_sin_p2t, s_cos_p1t, Nmax)
	MN = {m: MNs.get(m, 0) + MNs2.get(m, 0) for m in set(MNs) | set(MNs2)}
	MN = {m: sp.simplify(c) for m, c in MN.items() if c != 0}
	MN2 = mul(MN, MN, Nmax)
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
	sin2p1 = mul(s_sin_p1, s_sin_p1, Nmax)
	sin2p1t = mul(s_sin_p1t, s_sin_p1t, Nmax)
	E5 = mul(ID, sin2p1t, Nmax)
	E5b = mul(IN, sin2p1, Nmax)
	E5 = {m: E5.get(m, 0) - E5b.get(m, 0) for m in set(E5) | set(E5b)}
	E5 = {m: sp.simplify(c) for m, c in E5.items() if c != 0}
	t6a = mul(u3, s_cos_p2t, Nmax)
	t6b = mul(s_sin_p2t, s_cot_p1t, Nmax)
	t6 = mul(s_sin_p1, {m: t6a.get(m, 0) + t6b.get(m, 0) for m in set(t6a) | set(t6b)}, Nmax)
	t6c = mul(mul(u3, s_cos_p2, Nmax), s_sin_p1, Nmax)
	t6d = mul(s_sin_p2, s_cos_p1, Nmax)
	E6 = {m: t6.get(m, 0) + t6c.get(m, 0) + t6d.get(m, 0) for m in set(t6) | set(t6c) | set(t6d)}
	E6 = {m: sp.simplify(c) for m, c in E6.items() if c != 0}
	E1 = (sp.cos(p2)*sp.sin(p1 + p3) + sp.sin(p2)*sp.cos(p3)*sp.cos(p1)/eps
		- eps*sp.sin(p3)*sp.sin(p2)*sp.sin(p1))
	E2 = (sp.cos(p2t)*sp.cos(p1t)*sp.cos(p3t)
		- sp.sin(p3t)*sp.sin(p2t)*sp.cos(p1t)/eps
		- sp.sin(p3t)*sp.cos(p2t)*sp.sin(p1t)
		- eps*sp.cos(p3t)*sp.sin(p2t)*sp.sin(p1t))
	P = {('E1', m): c for m, c in to_dict(S(E1), u, Nmax).items()}
	P.update({('E2', m): c for m, c in to_dict(S(E2), u, Nmax).items()})
	P.update({('E5', m): c for m, c in E5.items()})
	P.update({('E6', m): c for m, c in E6.items()})
	return P


def main():
	P = build()
	with open(r'scripts/_gapn2_largeR_P.pkl', 'wb') as f:
		pickle.dump(P, f, protocol=4)
	print('P keys:', sorted(P.keys()))
	print('E1 u0 =', sp.nsimplify(P[('E1', 0)]))
	print('E5 u0 =', sp.nsimplify(P[('E5', 0)]))
	print('E6 u3 =', sp.nsimplify(P[('E6', 3)]))
	print('E6 u5 =', sp.nsimplify(P[('E6', 5)]))
	print('saved scripts/_gapn2_largeR_P.pkl')


if __name__ == '__main__':
	main()
