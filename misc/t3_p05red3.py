# -*- coding: utf-8 -*-
"""t3_p05red3: clean split P05 = P0(u,w) + su*cu*P1(u,w)."""
import sympy as sp, json

with open('misc/t3_P05.json') as fh: r = json.load(fh)
u, su, cu = sp.symbols('u su cu', positive=True)
P05 = sum(int(c)*u**m[0]*su**m[1]*cu**m[2] for m,c in zip(r['monoms'], r['coeffs']))
P05r = sp.expand(P05)
for _ in range(12):
    P05r = sp.expand(P05r.subs(su**2, 1-cu**2))
# P05r = P0 + su*P1 where P0,P1 su-free
P0 = sp.expand(P05r.subs(su, 0))
P1s = sp.expand((P05r - P0)/su)   # su-free, but may contain cu to odd powers
w = sp.symbols('w', positive=True)
# substitute cu^2 -> w in P0 and P1s; then factor out cu if odd power remains
def sub_w(expr):
    e = sp.expand(expr)
    e = sp.expand(e.subs(cu**2, w))
    # if cu remains to power 1 (odd), factor: cu * poly(w)
    if e.has(cu):
        e = sp.expand(e/cu)
        return e, True
    return e, False
P0w, _ = sub_w(P0)
P1w, odd = sub_w(P1s)
print('odd cu left in P1?', odd)
print('P0(u,w) =')
for t in sorted(sp.Add.make_args(P0w), key=str): print('   ', t)
print('P1(u,w) =')
for t in sorted(sp.Add.make_args(P1w), key=str): print('   ', t)
import pickle
with open('misc/t3_P05split.pkl','wb') as fh: pickle.dump({'P0':P0w,'P1':P1w}, fh)
