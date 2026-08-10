# -*- coding: utf-8 -*-
"""qderiv2.py -- corrected decomposition of dH/dq and dF~'/dq."""
import sys, mpmath as mp
sys.path.insert(0, r'F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-keylemma-E58FB1\reproducibility')
from keylemma_lib import Phi, Wfun, alpha1_of_c, alpha2_of_c, Gfun
mp.mp.dps = 30

def dalpha_dq(alpha, q, c):
    Ph = Phi(alpha, q); t = mp.tan(alpha)
    return -t*Ph/((1+q*q*t*t)*(q + c*Ph))

def dG_dq(alpha, c, q):
    Ph = Phi(alpha, q); Phq = 2*q*mp.sin(alpha)**2
    W = Wfun(alpha); s = mp.sin(alpha); co = mp.cos(alpha)
    den = q + c*Ph
    t1 = (-Phq*W*den + Ph*W*(1 + c*Phq))/den**2
    t2 = 2*c*alpha*s*co*((Phq*(q*q-1) + Ph*2*q)*den - Ph*(q*q-1)*2*(1 + c*Phq))/den**3
    return t1 + t2

def dG_da(alpha, c, q):
    Ph = Phi(alpha, q); Php = 2*(q*q-1)*mp.sin(alpha)*mp.cos(alpha)
    W = Wfun(alpha); Wp = 2*(mp.cos(alpha)*mp.sin(alpha) - alpha)/mp.sin(alpha)**2
    s = mp.sin(alpha); co = mp.cos(alpha)
    den = q + c*Ph
    t1 = (-(Php*W + Ph*Wp)*den + Ph*W*c*Php)/den**2
    t2 = 2*c*(q*q-1)*((Ph + alpha*Php)*s*co + alpha*Ph*(co*co - s*s))/den**2 \
         - 2*c*alpha*Ph*(q*q-1)*s*co*2*c*Php/den**3
    return t1 + t2

def Mtil(alpha, c, q):
    return alpha*alpha*mp.sin(alpha)**2/(q + c*Phi(alpha, q))

def H_of(c, q):
    return Gfun(alpha2_of_c(c,q), c, q) - Gfun(alpha1_of_c(c,q), c, q)

def dH_dq_an(c, q):
    a1 = alpha1_of_c(c,q); a2 = alpha2_of_c(c,q)
    return (dG_dq(a2,c,q) - dG_dq(a1,c,q)) + (dG_da(a2,c,q)*dalpha_dq(a2,q,c) - dG_da(a1,c,q)*dalpha_dq(a1,q,c))

print('=== verify dH/dq analytic vs fd, then decompose ===')
for q in [mp.mpf('1.05'), mp.mpf('2'), mp.mpf('10')]:
    for c in [mp.mpf('0.1'), mp.mpf('0.3'), mp.mpf('0.499')]:
        h = mp.mpf('1e-6')
        fd = (H_of(c,q+h) - H_of(c,q-h))/(2*h)
        an = dH_dq_an(c,q)
        a1 = alpha1_of_c(c,q); a2 = alpha2_of_c(c,q)
        br1 = dG_dq(a2,c,q) - dG_dq(a1,c,q)
        br2 = dG_da(a2,c,q)*dalpha_dq(a2,q,c) - dG_da(a1,c,q)*dalpha_dq(a1,q,c)
        print(f'  q={mp.nstr(q,4)} c={mp.nstr(c,4)}: fd={mp.nstr(fd,7)} an={mp.nstr(an,7)} '
              f'[dq-part]={mp.nstr(br1,7)} [da-part]={mp.nstr(br2,7)}')

print()
print('=== dFp/dq: analytic vs fd ===')
def dMtil_dq(alpha, c, q):
    aq = dalpha_dq(alpha, q, c)
    Ph = Phi(alpha, q); Phq = 2*q*mp.sin(alpha)**2
    Php = 2*(q*q-1)*mp.sin(alpha)*mp.cos(alpha)
    s = mp.sin(alpha); den = q + c*Ph
    partq = -alpha*alpha*s*s*(1 + c*Phq)/den**2
    parta = (2*alpha*s*s + 2*alpha*alpha*s*mp.cos(alpha))/den - alpha*alpha*s*s*c*Php/den**2
    return partq + parta*aq

def Fp_of(c, q):
    a1 = alpha1_of_c(c,q); a2 = alpha2_of_c(c,q)
    return Mtil(a1,c,q)*Gfun(a1,c,q) - Mtil(a2,c,q)*Gfun(a2,c,q)

def dFp_dq_an(c, q):
    a1 = alpha1_of_c(c,q); a2 = alpha2_of_c(c,q)
    M1t = Mtil(a1,c,q); M2t = Mtil(a2,c,q)
    G1 = Gfun(a1,c,q); G2 = Gfun(a2,c,q)
    dM1 = dMtil_dq(a1,c,q); dM2 = dMtil_dq(a2,c,q)
    dG1 = dG_dq(a1,c,q) + dG_da(a1,c,q)*dalpha_dq(a1,q,c)
    dG2 = dG_dq(a2,c,q) + dG_da(a2,c,q)*dalpha_dq(a2,q,c)
    return dM1*G1 + M1t*dG1 - dM2*G2 - M2t*dG2

for q in [mp.mpf('1.01'), mp.mpf('1.1'), mp.mpf('2'), mp.mpf('10'), mp.mpf('100')]:
    cs = [mp.mpf('1e-4') + mp.mpf('0.4998')*k/100 for k in range(101)]
    mn = mp.inf; mx = mp.ninf; cmin=None
    worst = 0
    for c in cs:
        h = mp.mpf('1e-6')
        fd = (Fp_of(c,q+h) - Fp_of(c,q-h))/(2*h)
        an = dFp_dq_an(c,q)
        worst = max(worst, abs(fd-an))
        if an < mn: mn, cmin = an, c
        if an > mx: mx = an
    print(f'  q={mp.nstr(q,4)}: dFp/dq in [{mp.nstr(mn,6)} at c={mp.nstr(cmin,4)}, {mp.nstr(mx,6)}]  max|an-fd|={mp.nstr(worst,5)}')
