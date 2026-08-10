# -*- coding: utf-8 -*-
"""t3_j2_gq2: J2_2d in (gamma,q) via NJ2/P^4 with substitution; verify numerically."""
import sympy as sp, json, math

A, t = sp.symbols('A t', positive=True)
sg, cg, st, ct = sp.symbols('sg cg st ct', positive=True)
with open('misc/t3_NJ2.json') as fh: r = json.load(fh)
monoms = r['monoms']; coeffs = [int(c) for c in r['coeffs']]
NJ2 = sum(coeffs[i]*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(monoms))
P = 2*(A*st*ct + t*sg*cg)
g, q = sp.symbols('g q', positive=True)
D = sp.sqrt(1 + q**2*sp.tan(g)**2)
sub = {A: sp.pi-g, t: sp.atan(q*sp.tan(g)),
       sg: sp.sin(g), cg: sp.cos(g),
       st: q*sp.tan(g)/D, ct: 1/D}
J2gq = sp.expand(NJ2.subs(sub)/P.subs(sub)**4)
J2gq = sp.expand(J2gq)
print('J2(g,q) terms:', len(sp.Add.make_args(J2gq)))
# numeric check vs direct
f = sp.lambdify((g, q), J2gq, 'numpy')
def direct(gv, qv):
    Av = math.pi-gv; tv = math.atan(qv*math.tan(gv))
    sv = {A: Av, t: tv, sg: math.sin(gv), cg: math.cos(gv), st: math.sin(tv), ct: math.cos(tv)}
    nj = float(NJ2.subs(sv).evalf(20)); pv = float(P.subs(sv).evalf(20))
    return nj/pv**4
for gv, qv in [(0.655,1.0),(0.9,1.5),(1.0472,2.0),(math.pi/3,1.0),(0.7,1.2)]:
    print(f'g={gv:.4f} q={qv}: gq-form={float(f(gv,qv)):.4f} direct={direct(gv,qv):.4f}')
print(J2gq)
