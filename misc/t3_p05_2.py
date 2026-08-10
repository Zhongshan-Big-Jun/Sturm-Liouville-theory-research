# -*- coding: utf-8 -*-
"""t3_p05_2: correct P05 = NJ2(2u, 1/2), factor."""
import sympy as sp, json, math

A, t = sp.symbols('A t', positive=True)
sg, cg, st, ct = sp.symbols('sg cg st ct', positive=True)
with open('misc/t3_NJ2.json') as fh: r = json.load(fh)
monoms = r['monoms']; coeffs = [int(c) for c in r['coeffs']]
NJ2 = sum(coeffs[i]*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(monoms))
# slice c=1/2: A = 2u, t = u, gamma = pi - 2u => sg = sin(2u), cg = cos(2u)?? wait: gamma = pi-A, cg = cos(gamma) = cos(pi-2u) = -cos(2u), sg = sin(pi-2u) = sin(2u)
u, su, cu = sp.symbols('u su cu', positive=True)
# use t = u; gamma = pi - 2u; sg = sin(2u) = 2 su cu; cg = -cos(2u) = -(cu^2 - su^2) = su^2 - cu^2
sub = {A: 2*u, t: u, sg: 2*su*cu, cg: su**2 - cu**2, st: su, ct: cu}
P05_2 = sp.expand(NJ2.subs(sub))
P05_2 = sp.expand(P05_2)
print('P05_2 terms:', len(sp.Add.make_args(P05_2)))
# reduce su^2 = 1 - cu^2
for _ in range(12):
    P05_2 = sp.expand(P05_2.subs(su**2, 1-cu**2))
w = sp.symbols('w', positive=True)
P05_2 = sp.expand(P05_2)
# factor out and try factor
try:
    print('factor:', sp.factor(P05_2))
except Exception as e:
    print('factor failed:', e)
