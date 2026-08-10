# -*- coding: utf-8 -*-
"""t3_z2: NJ2(pi/3, q) for q in [1,2] - factor."""
import sympy as sp, json, math

A, t = sp.symbols('A t', positive=True)
sg, cg, st, ct = sp.symbols('sg cg st ct', positive=True)
with open('misc/t3_NJ2.json') as fh: r = json.load(fh)
monoms = r['monoms']; coeffs = [int(cf) for cf in r['coeffs']]
NJ2 = sum(coeffs[i]*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(monoms))

# gamma = pi/3: A = 2pi/3, sg = sqrt(3)/2, cg = 1/2, t = u, q = tan u / tan(pi/3) = tan u / sqrt(3)
u = sp.symbols('u', positive=True)
sub = {A: 2*sp.pi/3, t: u, sg: sp.sqrt(3)/2, cg: sp.Rational(1,2), st: sp.sin(u), ct: sp.cos(u)}
NJ_p3 = sp.expand(NJ2.subs(sub))
NJ_p3 = sp.trigsimp(NJ_p3)
print('NJ2(pi/3, q=tan u/sqrt3) terms:', len(sp.Add.make_args(sp.expand(NJ_p3))))
try:
    print('factor:', sp.factor(sp.expand(NJ_p3)))
except Exception as e:
    print('factor failed:', e)
# also try as polynomial in su, cu
su, cu = sp.symbols('su cu', positive=True)
NJ_p3b = sp.expand(NJ_p3.subs({sp.sin(u): su, sp.cos(u): cu}))
print('as poly in su,cu: terms:', len(sp.Add.make_args(NJ_p3b)))
try:
    print('factor:', sp.factor(NJ_p3b))
except Exception as e:
    print('factor failed:', e)
# numeric: NJ2(pi/3, q) values
f = sp.lambdify((u,), NJ_p3, 'numpy')
for q in [1.0, 1.25, 1.5, 1.75, 2.0]:
    uv = math.atan(q*math.sqrt(3))
    print('q=%.2f: NJ2 = %.4f' % (q, float(f(uv))))
