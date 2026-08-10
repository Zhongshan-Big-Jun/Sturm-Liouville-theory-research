# -*- coding: utf-8 -*-
"""regionB2.py -- monotonicity in c on Region B; ratio structure.
Checks: (1) d/dc(-F~') >= 0 on Region B  (2) dH/dc <= 0 on Region B
        (3) |G1|/|G2| vs rho = M2t/M1t on Region B
"""
import sys, mpmath as mp
sys.path.insert(0, r'F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-keylemma-E58FB1\reproducibility')
from keylemma_lib import Phi, Wfun, alpha1_of_c, alpha2_of_c, Gfun, G1_of_c, G2_of_c
mp.mp.dps = 25

def Mtil(alpha, c, q):
    return alpha*alpha*mp.sin(alpha)**2/(q + c*Phi(alpha, q))
def Fp(c, q):
    a1 = alpha1_of_c(c,q); a2 = alpha2_of_c(c,q)
    return Mtil(a1,c,q)*Gfun(a1,c,q) - Mtil(a2,c,q)*Gfun(a2,c,q)
def H(c, q):
    return G2_of_c(c,q) - G1_of_c(c,q)

def cG2(q):
    # find the unique c in (0.4, 0.5) with G2(c,q)=0 (Region B left boundary)
    prev = mp.mpf('0.40'); pv = G2_of_c(prev, q)
    for k in range(1, 1001):
        c = mp.mpf('0.40') + mp.mpf('0.10')*k/1000
        v = G2_of_c(c, q)
        if (pv < 0) != (v < 0):
            return (prev + c)/2
        prev, pv = c, v
    return None

print('=== (1) d/dc(-Fp) >= 0 ?  (2) dH/dc <= 0 ?  on Region B ===')
for q in [mp.mpf('1.0'), mp.mpf('1.2'), mp.mpf('1.5'), mp.mpf('1.8')]:
    cb = cG2(q)
    if cb is None: continue
    mneg = mp.inf; mpos = mp.ninf; worst1 = None; worst2 = None
    mF = mp.inf; mH = mp.inf
    for k in range(401):
        c = cb + (mp.mpf('0.5') - cb)*k/400
        h = mp.mpf('1e-4')
        dF = (Fp(c+h,q) - Fp(c-h,q))/(2*h)     # dFp/dc
        dH = (H(c+h,q) - H(c-h,q))/(2*h)
        if dF < mneg: mneg, worst1 = dF, c
        if dH > mpos: mpos, worst2 = dH, c
        if -Fp(c,q) < mF: mF = -Fp(c,q)
        if H(c,q) < mH: mH = H(c,q)
    print(f'  q={mp.nstr(q,4)}: cB={mp.nstr(cb,6)}: min dFp/dc={mp.nstr(mneg,6)} at c={mp.nstr(worst1,5)} | '
          f'max dH/dc={mp.nstr(mpos,6)} at c={mp.nstr(worst2,5)} | min(-Fp)={mp.nstr(mF,6)} | min H={mp.nstr(mH,6)}')

print()
print('=== (3) |G1|/|G2| vs rho = M2t/M1t on Region B ===')
for q in [mp.mpf('1.0'), mp.mpf('1.2'), mp.mpf('1.5'), mp.mpf('1.8')]:
    cb = cG2(q)
    if cb is None: continue
    mrat = mp.inf; mrho = mp.ninf; worst = None
    for k in range(401):
        c = cb + (mp.mpf('0.5') - cb)*k/400
        a1 = alpha1_of_c(c,q); a2 = alpha2_of_c(c,q)
        g1 = G1_of_c(c,q); g2 = G2_of_c(c,q)
        rho = Mtil(a2,c,q)/Mtil(a1,c,q)
        ratio = (-g1)/(-g2) if g2 < 0 else None
        if ratio is not None and ratio < mrat: mrat, worst = ratio, c
        if rho > mrho: mrho = rho
    print(f'  q={mp.nstr(q,4)}: min(|G1|/|G2|)={mp.nstr(mrat,7)} at c={mp.nstr(worst,5)} | max rho={mp.nstr(mrho,7)}')
