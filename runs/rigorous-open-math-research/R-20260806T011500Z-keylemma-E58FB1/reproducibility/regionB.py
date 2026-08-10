# -*- coding: utf-8 -*-
"""regionB.py -- characterize Region B = {G2<0}; margins of both forms there.
"""
import sys, mpmath as mp
sys.path.insert(0, r'F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-keylemma-E58FB1\reproducibility')
from keylemma_lib import Phi, Wfun, alpha1_of_c, alpha2_of_c, Gfun, G1_of_c, G2_of_c
mp.mp.dps = 30

def Mtil(alpha, c, q):
    return alpha*alpha*mp.sin(alpha)**2/(q + c*Phi(alpha, q))
def Fp(c, q):
    a1 = alpha1_of_c(c,q); a2 = alpha2_of_c(c,q)
    return Mtil(a1,c,q)*Gfun(a1,c,q) - Mtil(a2,c,q)*Gfun(a2,c,q)
def H(c, q):
    return G2_of_c(c,q) - G1_of_c(c,q)

print('=== q_*: G2(q, 1/2) = 0 ===')
for q in [mp.mpf('1.8'), mp.mpf('1.85'), mp.mpf('1.9'), mp.mpf('1.92'), mp.mpf('1.95'), mp.mpf('2.0')]:
    print(f'  q={mp.nstr(q,4)}: G2(q,1/2)={mp.nstr(G2_of_c(mp.mpf("0.5"), q),8)}')
# refine: find root
lo, hi = mp.mpf('1.8'), mp.mpf('2.0')
for _ in range(50):
    mid = (lo+hi)/2
    if G2_of_c(mp.mpf('0.5'), mid) > 0: lo = mid
    else: hi = mid
qstar = (lo+hi)/2
print(f'  q* = {mp.nstr(qstar, 12)}')

print()
print('=== Region B margins ===')
for q in [mp.mpf('1.0'), mp.mpf('1.1'), mp.mpf('1.3'), mp.mpf('1.5'), mp.mpf('1.7'), mp.mpf('1.9')]:
    # find c_G2(q): largest c in (0,1/2) where G2=0
    cs = [mp.mpf('0.3') + mp.mpf('0.2')*k/400 for k in range(401)]
    g2s = [G2_of_c(c,q) for c in cs]
    # G2 decreasing in c? find last sign change
    zc = None
    for i in range(len(cs)-1):
        if (g2s[i] < 0) != (g2s[i+1] < 0):
            zc = (cs[i], cs[i+1])
    if zc is None:
        print(f'  q={mp.nstr(q,4)}: G2 sign constant on (0.3,0.5): G2(0.3)={mp.nstr(g2s[0],6)} G2(0.5)={mp.nstr(g2s[-1],6)}')
        continue
    cG2 = (zc[0]+zc[1])/2
    # scan Region B = (cG2, 1/2)
    mF = mp.inf; mAbs = mp.inf
    for k in range(401):
        c = cG2 + (mp.mpf('0.5')-cG2)*k/400
        g2 = G2_of_c(c,q)
        if g2 < 0:
            fp = -Fp(c,q)                      # M1t|G1| - M2t|G2| (G1<0)
            ab = -G1_of_c(c,q) + g2            # |G1| - |G2| (g2<0 => -g2=|G2|)
            if fp < mF: mF = fp
            if ab < mAbs: mAbs = ab
    print(f'  q={mp.nstr(q,4)}: c_G2={mp.nstr(cG2,7)} | min(-Fp) over B = {mp.nstr(mF,7)} | min(|G1|-|G2|) over B = {mp.nstr(mAbs,7)}')

print()
print('=== log-form in Region B: where is |G1|-|G2| minimized over the whole domain? ===')
# global min of |G1|-|G2| over {(q,c): G2<0}, and of -Fp
for q in [mp.mpf('1.001'), mp.mpf('1.05'), mp.mpf('1.2'), mp.mpf('1.5'), mp.mpf('1.8')]:
    cs = [mp.mpf('0.4') + mp.mpf('0.0999')*k/300 for k in range(301)]
    mF = mp.inf; mAbs = mp.inf; cF = None; cA = None
    for c in cs:
        g2 = G2_of_c(c,q)
        if g2 < 0:
            fp = -Fp(c,q); ab = -G1_of_c(c,q) + g2
            if fp < mF: mF, cF = fp, c
            if ab < mAbs: mAbs, cA = ab, c
    print(f'  q={mp.nstr(q,4)}: min(-Fp)={mp.nstr(mF,7)} at c={mp.nstr(cF,5)} | min(|G1|-|G2|)={mp.nstr(mAbs,7)} at c={mp.nstr(cA,5)}')
