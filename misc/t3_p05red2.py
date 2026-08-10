# -*- coding: utf-8 -*-
"""t3_p05red2: print Peven and Podd."""
import sympy as sp, json

with open('misc/t3_P05.json') as fh: r = json.load(fh)
u, su, cu = sp.symbols('u su cu', positive=True)
P05 = sum(int(c)*u**m[0]*su**m[1]*cu**m[2] for m,c in zip(r['monoms'], r['coeffs']))
P05r = sp.expand(P05)
for _ in range(12):
    P05r = sp.expand(P05r.subs(su**2, 1-cu**2))
w = sp.symbols('w', positive=True)
P_even = sp.expand(P05r.subs(su, 0))
P_odd = sp.expand((P05r - P_even)/su)
P_even = sp.expand(P_even.subs(cu**2, w))
P_odd = sp.expand(P_odd.subs(cu**2, w))
print('Podd(u,w) =', P_odd)
print('Peven(u,w) terms:')
for t in sorted(sp.Add.make_args(P_even), key=str):
    print('   ', t)
