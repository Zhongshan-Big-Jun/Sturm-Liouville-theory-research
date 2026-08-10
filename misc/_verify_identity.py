# -*- coding: utf-8 -*-
"""Verify W = T1+...+T8 exactly (sympy) from the NJ2 monomial data."""
import json, sympy as sp
with open('misc/t3_NJ2.json') as fh: rj = json.load(fh)
A, t, sg, cg, st, ct = sp.symbols('A t sg cg st ct')
NJ2 = sum(int(rj['coeffs'][i])*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(rj['monoms']))
NJ2 = sp.expand(NJ2)
W = sp.expand(NJ2/(32*A*A*cg))

B1 = A*cg - 2*sg
B2 = 4*A*A*cg*cg - A*A - 12*A*cg*sg + 6*sg*sg
B4 = 7*A*cg*cg - A*sg*sg - 4*cg*sg
B5 = A*A*cg*cg - A*A*sg*sg + 2*A*A + 12*A*cg*sg - 12*sg*sg
B7 = 3*A*cg*cg + A*sg*sg + 8*cg*sg
T1 = -2*A**3*B1*st*st*ct**4
T2 = A*A*cg*B2*st*st*ct*ct
T3 = -2*A**3*sg*t*st*ct**5
T4 = A*A*sg*t*B4*st*ct**3
T5 = -A*cg*cg*sg*t*B5*st*ct
T6 = 4*A*A*cg*sg*sg*t*t*ct**4
T7 = -A*cg*sg*sg*t*t*B7*ct*ct
T8 = 6*cg**3*sg**4*t*t
S = sp.expand(T1+T2+T3+T4+T5+T6+T7+T8)
diff = sp.expand(W - S)
print('W - sum(T) == 0 (raw polynomial identity)?', diff == 0)
# The doc claims the identity modulo sg^2+cg^2=1 and st^2+ct^2=1 only
# (W and the T_i contain the same monomials with different cg^2/st^2
#  usage).  Reduce powers of st^2, ct^2, sg^2, cg^2 via the circle
#  relations, then compare.
def reduce_sq(expr, v, other):
    p = sp.Poly(expr, v)
    if p.degree() < 0:
        return sp.Integer(0)
    res = sp.Integer(0)
    for k in range(p.degree()+1):
        ck = p.coeff_monomial(v**k)
        if ck == 0:
            continue
        if k % 2 == 0:
            res += ck * (1 - other)**(k//2)
        else:
            res += ck * v * (1 - other)**((k-1)//2)
    return sp.expand(res)
for _ in range(6):
    diff = reduce_sq(diff, st, ct**2)
    diff = reduce_sq(diff, ct, st**2)
    diff = reduce_sq(diff, sg, cg**2)
    diff = reduce_sq(diff, cg, sg**2)
print('W == sum(T) modulo trig relations ?', diff == 0)
# also verify T8 form: 6 cg^3 sg^4 t^2 = cg sg^2 t^2 * 6 cg^2 sg^2
print('T8 == cg*sg^2*t^2*(6cg^2 sg^2) ?', sp.expand(T8 - cg*sg*sg*t*t*6*cg*cg*sg*sg) == 0)
# check the composed identity at exact rational-ish points with high precision
import mpmath as mp
mp.mp.dps = 60
def J2comp(g, q):
    x = mp.pi - g; th = mp.atan(q*mp.tan(g)); c = th/x
    s, b = mp.sin(x), -mp.cos(x)
    S, C = mp.sin(th), mp.cos(th)
    Phi = b*b + q*q*s*s
    den = q + c*Phi
    u = x*Phi/den
    A0 = mp.mpf(3)/x - 2*b/s
    H = 2*c*(q*q-1)*s*(-b)/den
    V = H - A0
    Phix = 2*(q*q-1)*s*(-b)
    denx = c*Phix
    ux = (Phi + x*Phix)/den - x*Phi*denx/(den*den)
    A0x = -3/(x*x) - 2/(s*s)
    Hx = 2*c*(q*q-1)*((b*b - s*s)*den - s*(-b)*denx)/(den*den)
    G = u*V
    Gx = ux*V + u*(Hx - A0x)
    Gc = (-x*Phi*Phi/(den*den))*V + u*(-2*(q*q-1)*s*b*q/(den*den))
    return G*G + Gc - u*Gx
fN = sp.lambdify((A,t,sg,cg,st,ct), NJ2, 'mpmath')
worst = mp.mpf(0)
for (g,q) in [(0.7,1.5),(0.9,1.2),(1.0,1.1),(0.65565,2.0),(mp.pi/3,1.0),(0.8,1.9),(1.0472,2.0),(0.655,1.0)]:
    A_ = mp.pi-g; sg_ = mp.sin(g); cg_ = mp.cos(g)
    t_ = mp.atan(q*mp.tan(g)); st_ = mp.sin(t_); ct_ = mp.cos(t_)
    Delta = A_*st_*ct_ + t_*sg_*cg_
    d = abs(J2comp(g,q) - fN(A_,t_,sg_,cg_,st_,ct_)/(16*Delta**4))
    worst = max(worst, d)
    print('g=%.4f q=%.2f : |J2 - NJ2/16D4| = %.2e' % (g,q,d))
print('worst = %.2e' % worst)
