# -*- coding: utf-8 -*-
"""boundary12.py -- closed forms at c=1/2; Region B monotonicity verification on fine grid.
H(q,1/2) = 2*pi*q*(q+1)/(2q+1)^1.5 (derived).  Need -Fp(q,1/2) > 0 for q in (1,q*).
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

print('=== -Fp(q,1/2) and H(q,1/2) vs closed forms ===')
alpha0 = lambda q: 2*mp.asin(1/mp.sqrt(2*(q+1)))
for q in [mp.mpf('1.001'), mp.mpf('1.1'), mp.mpf('1.3'), mp.mpf('1.5'), mp.mpf('1.7'), mp.mpf('1.85')]:
    a0 = alpha0(q); a1 = a0; a2 = mp.pi - a0
    Ph = Phi(a0, q)
    den = q + Ph/2
    M1t = a0*a0*mp.sin(a0)**2/den
    M2t = a2*a2*mp.sin(a0)**2/den
    W1 = Wfun(a0); W2 = Wfun(a2)
    s = mp.sin(a0); co = mp.cos(a0)
    G1 = -Ph*W1/den + a0*Ph*(q*q-1)*s*co/den**2     # c=1/2: 2c=1
    G2 = -Ph*W2/den - a2*Ph*(q*q-1)*s*co/den**2
    Fp12 = M1t*G1 - M2t*G2
    H12 = G2 - G1
    cf_H = 2*mp.pi*q*(q+1)/(2*q+1)**mp.mpf('1.5')
    print(f'  q={mp.nstr(q,5)}: -Fp(1/2)={mp.nstr(-Fp12,9)} | H(1/2)={mp.nstr(H12,9)} vs formula={mp.nstr(cf_H,9)} diff={mp.nstr(abs(H12-cf_H),6)}')

print()
print('=== Region B monotonicity on fine (q,c) grid ===')
# dFp/dc > 0 and dH/dc < 0 everywhere in Region B
worst_dF = mp.inf; worst_dH = mp.inf
for qi in range(1, 40):
    q = mp.mpf('1.0') + mp.mpf('0.86')*qi/39
    # c range: (c_G2(q), 1/2); find c_G2 by scan
    prev = mp.mpf('0.35'); pv = G2_of_c(prev, q)
    cb = None
    for k in range(1, 1501):
        c = mp.mpf('0.35') + mp.mpf('0.15')*k/1500
        v = G2_of_c(c, q)
        if (pv < 0) != (v < 0):
            cb = (prev+c)/2; break
        prev, pv = c, v
    if cb is None: continue
    for k in range(21):
        c = cb + (mp.mpf('0.5')-cb)*k/20
        h = mp.mpf('1e-4')
        dF = (Fp(c+h,q)-Fp(c-h,q))/(2*h)
        dH = (H(c+h,q)-H(c-h,q))/(2*h)
        if dF < worst_dF: worst_dF = dF
        if dH > worst_dH: worst_dH = dH
print(f'  min dFp/dc over Region B grid = {mp.nstr(worst_dF,7)}')
print(f'  max dH/dc over Region B grid   = {mp.nstr(worst_dH,7)}')
