# -*- coding: utf-8 -*-
"""t3_p05red: reduce P05 using su^2+cu^2=1; test u-partition bounds for P05<0 and dP05/du<0."""
import sympy as sp, json, math

with open('misc/t3_P05.json') as fh: r = json.load(fh)
u, su, cu = sp.symbols('u su cu', positive=True)
P05 = sum(int(c)*u**m[0]*su**m[1]*cu**m[2] for m,c in zip(r['monoms'], r['coeffs']))
# reduce: su^2 -> 1-cu^2 repeatedly
P05r = sp.expand(P05)
for _ in range(12):
    P05r = sp.expand(P05r.subs(su**2, 1-cu**2))
# now su appears at most to power 1; split even/odd
P05r = sp.expand(P05r)
w = sp.symbols('w', positive=True)  # w = cu^2
# replace cu^2 -> w, and su -> sqrt(1-w) handled via odd part factor su*cu
# terms with su^1: factor su; terms with su^0: pure w
P_even = sp.expand(P05r.subs(su, 0))          # drop odd-su terms
P_odd = sp.expand((P05r - P_even))            # su^1 terms
P_odd = sp.simplify(P_odd/su)
P_even = sp.expand(P_even.subs(cu**2, w))
P_odd = sp.expand(P_odd.subs(cu**2, w))       # after dividing by su, odd part is polynomial in cu^2? check
print('P05 = Peven(u,w) + su*cu*Podd(u,w)  (w=cu^2)')
print('Peven terms:', len(sp.Add.make_args(P_even)))
print('Podd terms:', len(sp.Add.make_args(P_odd)))
# check P_odd has no leftover cu odd power
print('P_odd still has cu?', P_odd.has(cu))
# numerical check
import numpy as np
def ev(Av, cv=0.5):
    tv = cv*Av; wv = math.cos(tv)**2
    return float(P_even.subs({u: tv, w: wv}).evalf(20)) + math.sin(tv)*math.cos(tv)*float(P_odd.subs({u: tv, w: wv}).evalf(20))
def ev_direct(Av):
    sv = {u: Av/2, su: math.sin(Av/2), cu: math.cos(Av/2)}
    return float(P05.subs(sv).evalf(20))
for Av in [2*math.pi/3, 2.2, 2.35, 2.45, math.pi-0.655]:
    print('A=%.4f: reduced=%.4f direct=%.4f' % (Av, ev(Av), ev_direct(Av)))
