# -*- coding: utf-8 -*-
"""asym1.py -- large-q behavior of G2: compute K(c) = lim q*(G2 - 4pi/sin(2pi c))."""
import sys, mpmath as mp
sys.path.insert(0, r'F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T050000Z-keylemma2-5A35E5\reproducibility')
import kl2_lib as L
mp.mp.dps = 40

def G2lim(c):
    return 4*mp.pi/mp.sin(2*mp.pi*c)

print('K(c) = q*(G2(c;q) - lim) at large q:')
for c in [mp.mpf('0.05'), mp.mpf('0.1'), mp.mpf('0.2'), mp.mpf('0.3'), mp.mpf('0.4'), mp.mpf('0.45'), mp.mpf('0.49')]:
    lim = G2lim(c)
    vals = []
    for q in [mp.mpf(1000), mp.mpf(10000), mp.mpf(100000)]:
        K = q*(L.G2(c, q) - lim)
        vals.append(K)
    print('  c=%s: q*delta at 1e3/1e4/1e5 = %s %s %s' % (mp.nstr(c,4),
          mp.nstr(vals[0],8), mp.nstr(vals[1],8), mp.nstr(vals[2],8)))
# higher order: q*(q*delta - K) to estimate next term
print()
print('next-order term q^2*(q*delta - K):')
for c in [mp.mpf('0.1'), mp.mpf('0.3'), mp.mpf('0.45')]:
    lim = G2lim(c)
    K = mp.mpf(100000)*(L.G2(c, mp.mpf(100000)) - lim)
    for q in [mp.mpf(10000), mp.mpf(100000)]:
        delta = L.G2(c, q) - lim
        print('  c=%s q=%s: q^2*(q*delta - K) = %s' % (mp.nstr(c,4), mp.nstr(q,4), mp.nstr(q*q*(q*delta - K), 8)))
