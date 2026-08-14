# -*- coding: utf-8 -*-
"""Independent from-scratch rebuild of E5 (band at x1) via the mass-integral
construction, comparing every coefficient against the pickled P dict.
E5 = ID sin^2(p1t) - IN sin^2(p1);  ID, IN are the two inner-block masses.
This is a fully independent copy of the Pbuild E5 chain.
"""
import pickle
import sympy as sp
from sympy import pi

u = sp.symbols('u', positive=True)
K, A, B, C = sp.symbols('K A B C')
P0 = pickle.load(open(r'scripts/_gapn2_largeR_P.pkl', 'rb'))

Nmax = 10
eps = u**3
k2 = K*u
k3 = K*u + C*u**5
p1 = pi/2 + A*u**2
p3 = pi/4 + B*u**2
fac = 1 + C*u**4/K
p1t = p1*fac
p3t = p3*fac
p2 = k2/2 - eps*(p1 + p3)
p2t = k3/2 - eps*fac*(p1 + p3)


def to_dict(expr, nmax):
    e = sp.expand(sp.series(sp.expand(expr), u, 0, nmax + 1).removeO())
    out = {}
    for m in range(0, nmax + 1):
        c = e.coeff(u, m)
        if c != 0:
            out[m] = sp.simplify(sp.expand(c))
    return out


def mul(A, B, nmax):
    out = {}
    for m1, c1 in A.items():
        for m2, c2 in B.items():
            m = m1 + m2
            if m <= nmax:
                out[m] = out.get(m, 0) + c1*c2
    return {m: sp.simplify(c) for m, c in out.items() if c != 0}


def div_u6(A):
    out = {}
    for m, c in A.items():
        if m >= 6:
            out[m - 6] = c
    return out


s_cos_p2 = to_dict(sp.cos(p2), Nmax)
s_sin_p2 = to_dict(sp.sin(p2), Nmax)
s_cos_p2t = to_dict(sp.cos(p2t), Nmax)
s_sin_p2t = to_dict(sp.sin(p2t), Nmax)
s_cos_p1 = to_dict(sp.cos(p1), 8)
s_sin_p1 = to_dict(sp.sin(p1), 8)
s_cos_p3 = to_dict(sp.cos(p3), 8)
s_sin_p3 = to_dict(sp.sin(p3), 8)
s_cos_p1t = to_dict(sp.cos(p1t), 8)
s_sin_p1t = to_dict(sp.sin(p1t), 8)
s_cos_p3t = to_dict(sp.cos(p3t), 8)
s_sin_p3t = to_dict(sp.sin(p3t), 8)
s_sin2_p3 = to_dict(sp.sin(2*p3), 8)
s_sin2_p3t = to_dict(sp.sin(2*p3t), 8)
s_invsin2_p3 = to_dict(1/sp.sin(p3)**2, 8)
s_invcos2_p3t = to_dict(1/sp.cos(p3t)**2, 8)
s_invf3 = to_dict(1/fac**3, 8)
s_invf = to_dict(1/fac, 8)

u3 = {3: sp.Integer(1)}
u5 = {5: sp.Integer(1)}

# ---- D (sin inner block) ----
Ms = mul(u3, mul(s_cos_p2, s_sin_p1, Nmax), Nmax)
Ms2 = mul(s_sin_p2, s_cos_p1, Nmax)
M = {m: Ms.get(m, 0) + Ms2.get(m, 0) for m in set(Ms) | set(Ms2)}
M = {m: sp.simplify(c) for m, c in M.items() if c != 0}
M2 = mul(M, M, Nmax)
m1D = to_dict(sp.simplify((p1 - sp.sin(2*p1)/2)/(2*K**3)), 8)
p3half = to_dict(sp.simplify(p3 - sp.sin(2*p3)/2), 8)
m3D = div_u6(mul(mul(M2, p3half, Nmax), s_invsin2_p3, Nmax))
for m, c in m3D.items():
    m3D[m] = c/(2*K**3)
a1 = mul({2: sp.Integer(1)}, s_sin_p1, Nmax)
a1 = {m: a1[m]/K for m in a1}
b1 = mul(s_cos_p1, {1: sp.Integer(1)}, Nmax)
b1 = {m: b1[m]/K for m in b1}
a1a1 = mul(a1, a1, Nmax)
b1b1 = mul(b1, b1, Nmax)
p2d = to_dict(p2, Nmax)
sin2p2d = to_dict(sp.sin(2*p2), Nmax)
cos2p2d = to_dict(sp.cos(2*p2), Nmax)
p2ou = {m - 1: c for m, c in p2d.items()}
sin2p2ou = {m - 1: c for m, c in sin2p2d.items()}
ss = {m: a1a1.get(m, 0) + b1b1.get(m, 0) for m in set(a1a1) | set(b1b1)}
term1 = mul(mul(ss, p2ou, Nmax), {1: sp.Rational(1, 2)/K}, Nmax)
dd = {m: a1a1.get(m, 0) - b1b1.get(m, 0) for m in set(a1a1) | set(b1b1)}
term2 = mul(mul(dd, sin2p2ou, Nmax), {1: sp.Rational(1, 4)/K}, Nmax)
term3 = mul(mul(mul(a1, b1, Nmax), {m: -c for m, c in cos2p2d.items()}, Nmax), {0: sp.Rational(1, 2)/K}, Nmax)
t3b = mul(mul(a1, b1, Nmax), {0: sp.Rational(1, 2)/K}, Nmax)
mL = {m: term1.get(m, 0) + term2.get(m, 0) + term3.get(m, 0) + t3b.get(m, 0)
      for m in set(term1) | set(term2) | set(term3) | set(t3b)}
mL = {m: sp.simplify(c) for m, c in mL.items() if c != 0}
ID = {m: m1D.get(m, 0) + m3D.get(m, 0) + mL.get(m, 0) for m in set(m1D) | set(m3D) | set(mL)}

# ---- N (cos inner block) ----
MNs = mul(u3, mul(s_cos_p2t, s_sin_p1t, Nmax), Nmax)
MNs2 = mul(s_sin_p2t, s_cos_p1t, Nmax)
MN = {m: MNs.get(m, 0) + MNs2.get(m, 0) for m in set(MNs) | set(MNs2)}
MN = {m: sp.simplify(c) for m, c in MN.items() if c != 0}
MN2 = mul(MN, MN, Nmax)
m1N = to_dict(sp.simplify((p1t - sp.sin(2*p1t)/2)/(2*K**3)), 8)
m1N = mul(m1N, s_invf3, Nmax)
p3halfN = to_dict(sp.simplify(p3t + sp.sin(2*p3t)/2), 8)
m3N = div_u6(mul(mul(mul(MN2, p3halfN, Nmax), s_invcos2_p3t, Nmax), s_invf3, Nmax))
for m in m3N:
    m3N[m] = m3N[m]/(2*K**3)
a2n = mul(mul({2: sp.Integer(1)}, s_sin_p1t, Nmax), {0: sp.Integer(1)/K}, Nmax)
a2n = mul(a2n, s_invf, Nmax)
b2n = mul({m - 1: c for m, c in s_cos_p1t.items()}, {0: sp.Integer(1)/K}, Nmax)
b2n = mul(b2n, s_invf, Nmax)
a2n2 = mul(a2n, a2n, Nmax)
b2n2 = mul(b2n, b2n, Nmax)
p2td = to_dict(p2t, Nmax)
sin2p2td = to_dict(sp.sin(2*p2t), Nmax)
cos2p2td = to_dict(sp.cos(2*p2t), Nmax)
s_invf = to_dict(1/fac, Nmax)
inv_k3 = mul({-1: sp.Integer(1)/K}, s_invf, Nmax)
ssN = {m: a2n2.get(m, 0) + b2n2.get(m, 0) for m in set(a2n2) | set(b2n2)}
t1n = mul(mul(ssN, p2td, Nmax), {0: sp.Rational(1, 2)}, Nmax)
t1n = mul(t1n, inv_k3, Nmax)
ddN = {m: a2n2.get(m, 0) - b2n2.get(m, 0) for m in set(a2n2) | set(b2n2)}
t2n = mul(mul(ddN, sin2p2td, Nmax), {0: sp.Rational(1, 4)}, Nmax)
t2n = mul(t2n, inv_k3, Nmax)
t3n = mul(mul(mul(a2n, b2n, Nmax), {m: -c for m, c in cos2p2td.items()}, Nmax), {0: sp.Rational(1, 2)}, Nmax)
t3n = mul(t3n, inv_k3, Nmax)
t3nb = mul(mul(mul(a2n, b2n, Nmax), {0: sp.Rational(1, 2)}, Nmax), inv_k3, Nmax)
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

print('E5 orders rebuilt:', sorted(E5.keys()))
print('E5 orders pickle:  ', sorted(m for (n, mm) in P0 if n == 'E5'))
ok = True
for m in sorted(set(E5) | set(mm for (n, mm) in P0 if n == 'E5')):
    d = sp.simplify(E5.get(m, 0) - P0.get(('E5', m), 0))
    if d != 0:
        ok = False
        print('E5_%d MISMATCH, diff=' % m, d)
    else:
        print('E5_%d : match' % m)
print('ALL E5 MATCH' if ok else 'E5 MISMATCHES FOUND')
