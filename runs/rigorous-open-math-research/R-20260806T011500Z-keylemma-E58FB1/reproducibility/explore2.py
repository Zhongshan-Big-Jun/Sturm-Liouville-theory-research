# -*- coding: utf-8 -*-
"""explore2.py -- margins of the KEY LEMMA forms; G2<0 region; G1 sign; q-derivative of H.
"""
import sys, mpmath as mp
sys.path.insert(0, r'F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-keylemma-E58FB1\reproducibility')
from keylemma_lib import (Phi, Wfun, alpha1_of_c, alpha2_of_c, Gfun, G1_of_c, G2_of_c)
mp.mp.dps = 35

def Ftil_p(c, q):
    a1 = alpha1_of_c(c, q); a2 = alpha2_of_c(c, q)
    M1t = a1*a1*mp.sin(a1)**2/(q + c*Phi(a1, q))
    M2t = a2*a2*mp.sin(a2)**2/(q + c*Phi(a2, q))
    return M1t*Gfun(a1, c, q) - M2t*Gfun(a2, c, q)

def H(c, q):
    return G2_of_c(c, q) - G1_of_c(c, q)

print('=== F~\' margin: max F~\' over c in (0,1/2); and H margin ===')
for q in [mp.mpf('1.001'), mp.mpf('1.01'), mp.mpf('1.025'), mp.mpf('1.05'), mp.mpf('1.1'),
          mp.mpf('1.3'), mp.mpf('1.5'), mp.mpf('1.7'), mp.mpf('2'), mp.mpf('3'), mp.mpf('4'),
          mp.mpf('10'), mp.mpf('100')]:
    cs = [mp.mpf('1e-4') + mp.mpf('0.4998')*k/400 for k in range(401)]
    best = (mp.ninf, None)  # max Fp
    bestH = (mp.inf, None)
    minG1 = mp.inf
    for c in cs:
        Fp = Ftil_p(c, q); h = H(c, q); g1 = G1_of_c(c, q)
        if Fp > best[0]: best = (Fp, c)
        if h < bestH[0]: bestH = (h, c)
        if g1 < minG1: minG1 = g1
    print(f'  q={mp.nstr(q,6)}: max F~\'={mp.nstr(best[0],8)} at c={mp.nstr(best[1],5)} | '
          f'min H={mp.nstr(bestH[0],8)} at c={mp.nstr(bestH[1],5)} | minG1={mp.nstr(minG1,7)}')

print()
print('=== G2 = 0 boundary c_G2(q) ===')
def G2(c, q):
    return G2_of_c(c, q)
for q in [mp.mpf('1.0'), mp.mpf('1.05'), mp.mpf('1.2'), mp.mpf('1.5'), mp.mpf('1.7'), mp.mpf('1.9'), mp.mpf('2.0')]:
    # find c where G2 = 0 by scanning (0, 1/2)
    lo, hi = None, None
    prev = mp.mpf('1e-6'); pv = G2(prev, q)
    for k in range(1, 5001):
        c = mp.mpf('1e-6') + mp.mpf('0.499999')*k/5000
        v = G2(c, q)
        if (pv > 0 and v < 0) or (pv < 0 and v > 0):
            lo, hi = prev, c; break
        prev, pv = c, v
    if lo is None:
        g2half = G2(mp.mpf('0.5'), q)
        print(f'  q={mp.nstr(q,4)}: no zero in (0,1/2); G2(1/2)={mp.nstr(g2half,7)}')
    else:
        import mpmath
        cz = mp.findroot(lambda c: G2(c, q), (lo, hi))
        print(f'  q={mp.nstr(q,4)}: c_G2={mp.nstr(cz,7)}')

print()
print('=== log-form margin in the G2<0 region: |G1|-|G2| ===')
for q in [mp.mpf('1.0'), mp.mpf('1.05'), mp.mpf('1.2'), mp.mpf('1.5')]:
    cs = [mp.mpf('0.45') + mp.mpf('0.0499')*k/300 for k in range(301)]
    m = mp.inf; mc = None
    for c in cs:
        g1 = G1_of_c(c, q); g2 = G2_of_c(c, q)
        if g2 < 0:
            d = -g1 - (-g2)   # |G1| - |G2|
            if d < m: m, mc = d, c
    print(f'  q={mp.nstr(q,4)}: min(|G1|-|G2| over {G2<0}) = {mp.nstr(m,7)} at c={mp.nstr(mc,5)}')

print()
print('=== F~\' margin in the G2<0 region: M1t|G1| - M2t|G2| ===')
def FP(c, q):
    return -Ftil_p(c, q)  # = M1t|G1| - M2t|G2| when G2<0 (and G1<0)
for q in [mp.mpf('1.0'), mp.mpf('1.05'), mp.mpf('1.2'), mp.mpf('1.5')]:
    cs = [mp.mpf('0.45') + mp.mpf('0.0499')*k/300 for k in range(301)]
    m = mp.inf; mc = None
    for c in cs:
        g2 = G2_of_c(c, q)
        if g2 < 0:
            fp = FP(c, q)
            if fp < m: m, mc = fp, c
    print(f'  q={mp.nstr(q,4)}: min(-F~\') over {G2<0} = {mp.nstr(m,7)} at c={mp.nstr(mc,5)}')
