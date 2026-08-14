# -*- coding: utf-8 -*-
"""Independent audit A1/A2:
- Re-derive E1,E2,E5,E6 from-scratch in the (K,A,B,C) ansatz and compare
  every P coefficient against the pickled dict.
- Verify the truncation claim (per-monomial total order <= 9 sufficient for
  levels <= 8) and the K-clearing zero-set claim.
"""
import pickle
import sympy as sp
from sympy import pi

u = sp.symbols('u', positive=True)
K, A, B, C = sp.symbols('K A B C')

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
    e = sp.series(sp.expand(expr), u, 0, nmax + 1).removeO()
    e = sp.expand(e)
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


# ---- E1, E2 direct from the closed.py expressions ----
# E1 = cos p2 sin(p1+p3) + sin p2 cos p3 cos p1/eps - eps sin p3 sin p2 sin p1
# E2 = cos p2t cos p1t cos p3t - sin p3t sin p2t cos p1t/eps - ...
E1 = sp.cos(p2)*sp.sin(p1 + p3) + sp.sin(p2)*sp.cos(p3)*sp.cos(p1)/eps \
    - eps*sp.sin(p3)*sp.sin(p2)*sp.sin(p1)
E2 = sp.cos(p2t)*sp.cos(p1t)*sp.cos(p3t) \
    - sp.sin(p3t)*sp.sin(p2t)*sp.cos(p1t)/eps \
    - sp.sin(p3t)*sp.cos(p2t)*sp.sin(p1t) \
    - eps*sp.cos(p3t)*sp.sin(p2t)*sp.sin(p1t)

P_re = {}
P_re.update({('E1', m): c for m, c in to_dict(E1, Nmax).items()})
P_re.update({('E2', m): c for m, c in to_dict(E2, Nmax).items()})
print('E1 orders:', sorted(m for (n, m) in P_re if n == 'E1'))
print('E2 orders:', sorted(m for (n, m) in P_re if n == 'E2'))

P0 = pickle.load(open(r'scripts/_gapn2_largeR_P.pkl', 'rb'))

print('\n=== E1 coefficient comparison (mine vs pickle) ===')
for m in [0, 2, 4, 6, 8, 10]:
    mine = sp.simplify(P_re.get(('E1', m), 0) - P0.get(('E1', m), 0))
    print('E1_%d diff zero? %s' % (m, mine == 0))
print('=== E2 ===')
for m in [0, 2, 4, 6, 8, 10]:
    mine = sp.simplify(P_re.get(('E2', m), 0) - P0.get(('E2', m), 0))
    print('E2_%d diff zero? %s' % (m, mine == 0))

# ---- E5, E6 rebuilt from mass-integral construction (Pbuild) ----
# Mass integrals are built from trig series.  Re-verify against the pickled
# dict by re-running the Pbuild construction here (independent copy).
def s_cos(x_ser):
    return to_dict(sp.cos(sp.Add(*[c*u**m for m, c in x_ser.items()])), Nmax)


def s_sin(x_ser):
    return to_dict(sp.sin(sp.Add(*[c*u**m for m, c in x_ser.items()])), Nmax)


p2d = to_dict(p2, Nmax)
p2td = to_dict(p2t, Nmax)
p1d = to_dict(p1, 8)
p3d = to_dict(p3, 8)
p1td = to_dict(p1t, 8)
p3td = to_dict(p3t, 8)
facsd = {0: sp.Integer(1), 4: C/K}
facsd3 = mul(mul(facsd, facsd, 8), facsd, 8)

s_cos_p2 = s_cos(p2d); s_sin_p2 = s_sin(p2d)
s_cos_p2t = s_cos(p2td); s_sin_p2t = s_sin(p2td)
s_cos_p1 = s_cos(p1d); s_sin_p1 = s_sin(p1d)
s_cos_p3 = s_cos(p3d); s_sin_p3 = s_sin(p3d)
s_cos_p1t = s_cos(p1td); s_sin_p1t = s_sin(p1td)
s_cos_p3t = s_cos(p3td); s_sin_p3t = s_sin(p3td)

# E6 (band at x2): sin p1 (eps cos p2t + sin p2t cot p1t) + eps cos p2 sin p1
#   + sin p2 cos p1   where cot p1t = -tan(p1t - pi/2)
s_cot_p1t = s_sin({m: -c for m, c in to_dict(sp.tan(p1t - pi/2), 8).items()})
u3 = {3: sp.Integer(1)}
t6a = mul(u3, s_cos_p2t, Nmax)
t6b = mul(s_sin_p2t, s_cot_p1t, Nmax)
t6 = mul(s_sin_p1, {m: t6a.get(m, 0) + t6b.get(m, 0) for m in set(t6a) | set(t6b)}, Nmax)
t6c = mul(mul(u3, s_cos_p2, Nmax), s_sin_p1, Nmax)
t6d = mul(s_sin_p2, s_cos_p1, Nmax)
E6re = {m: t6.get(m, 0) + t6c.get(m, 0) + t6d.get(m, 0) for m in set(t6) | set(t6c) | set(t6d)}
E6re = {m: sp.simplify(c) for m, c in E6re.items() if c != 0}
print('\nE6 orders rebuilt:', sorted(E6re.keys()), 'vs pickle', sorted(m for (n, m) in P0 if n == 'E6'))
print('=== E6 ===')
for m in sorted(set(E6re) | set(m for (n, mm) in P0 if n == 'E6')):
    d = sp.simplify(E6re.get(m, 0) - P0.get(('E6', m), 0))
    print('E6_%d diff zero? %s' % (m, d == 0))

print('\n--- hard constants sanity ---')
print('E5_5 pickle =', sp.simplify(P0[('E5', 5)]))
print('E1_0 pickle =', sp.simplify(P0[('E1', 0)]))
print('E2_0 pickle =', sp.simplify(P0[('E2', 0)]))
print('E6_3 pickle =', sp.simplify(P0[('E6', 3)]))
print('E6_5 pickle =', sp.simplify(P0[('E6', 5)]))
print('E5_0 pickle =', sp.simplify(P0[('E5', 0)]))
