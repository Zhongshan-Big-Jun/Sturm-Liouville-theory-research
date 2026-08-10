# -*- coding: utf-8 -*-
"""regionB3.py -- verify J(alpha1)>=0, J(alpha2)<=0, G'(alpha1)>G'(alpha2) on Region B.
"""
import sys, mpmath as mp
sys.path.insert(0, r'F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-keylemma-E58FB1\reproducibility')
from keylemma_lib import Phi, Wfun, alpha1_of_c, alpha2_of_c, Gfun
mp.mp.dps = 25

def Ga(alpha, c, q):
    Ph = Phi(alpha, q); Php = 2*(q*q-1)*mp.sin(alpha)*mp.cos(alpha)
    W = Wfun(alpha); Wp = 2*(mp.cos(alpha)*mp.sin(alpha) - alpha)/mp.sin(alpha)**2
    s = mp.sin(alpha); co = mp.cos(alpha)
    den = q + c*Ph; Dp = c*Php
    A = Ph*W; Ap = Php*W + Ph*Wp
    B = 2*c*alpha*Ph*(q*q-1)*s*co
    Bp = 2*c*(q*q-1)*((Ph + alpha*Php)*s*co + alpha*Ph*(co*co - s*s))
    return -(Ap*den - A*Dp)/den**2 + (Bp*den - 2*B*Dp)/den**3

def Gc(alpha, c, q):
    Ph = Phi(alpha, q); W = Wfun(alpha); s = mp.sin(alpha); co = mp.cos(alpha)
    den = q + c*Ph
    return Ph*Ph*W/den**2 + 2*alpha*Ph*(q*q-1)*s*co*(q - c*Ph)/den**3

def Gprime(alpha, c, q):
    Ph = Phi(alpha, q)
    ap = -alpha*Ph/(q + c*Ph)
    return Ga(alpha,c,q)*ap + Gc(alpha,c,q)

def J(alpha, c, q):
    g = Gfun(alpha,c,q)
    return g*g + Gprime(alpha,c,q)

def cG2(q):
    prev = mp.mpf('0.35'); pv = G2_of_c(prev, q)
    for k in range(1, 1501):
        c = mp.mpf('0.35') + mp.mpf('0.15')*k/1500
        v = G2_of_c(c, q)
        if (pv < 0) != (v < 0):
            return (prev+c)/2
        prev, pv = c, v
    return None
from keylemma_lib import G2_of_c

print('=== (a) J(alpha1(c)) >= 0 and J(alpha2(c)) <= 0 on Region B ===')
for q in [mp.mpf('1.0'), mp.mpf('1.2'), mp.mpf('1.5'), mp.mpf('1.8')]:
    cb = cG2(q)
    if cb is None: continue
    mnJ1 = mp.inf; mxJ2 = mp.ninf
    for k in range(201):
        c = cb + (mp.mpf('0.5')-cb)*k/200
        a1 = alpha1_of_c(c,q); a2 = alpha2_of_c(c,q)
        mnJ1 = min(mnJ1, J(a1,c,q))
        mxJ2 = max(mxJ2, J(a2,c,q))
    print(f'  q={mp.nstr(q,4)}: min J(a1)={mp.nstr(mnJ1,7)}  max J(a2)={mp.nstr(mxJ2,7)}')

print()
print('=== (b) G\'(alpha1) - G\'(alpha2) > 0 on Region B (i.e. H\'<0) ===')
for q in [mp.mpf('1.0'), mp.mpf('1.2'), mp.mpf('1.5'), mp.mpf('1.8')]:
    cb = cG2(q)
    if cb is None: continue
    mn = mp.inf
    for k in range(201):
        c = cb + (mp.mpf('0.5')-cb)*k/200
        a1 = alpha1_of_c(c,q); a2 = alpha2_of_c(c,q)
        d = Gprime(a1,c,q) - Gprime(a2,c,q)
        if d < mn: mn = d
    print(f'  q={mp.nstr(q,4)}: min (G\'(a1)-G\'(a2)) = {mp.nstr(mn,7)}')

print()
print('=== (c) -Fp(q,1/2) closed form: verify against direct computation ===')
def Mtil(alpha, c, q):
    return alpha*alpha*mp.sin(alpha)**2/(q + c*Phi(alpha, q))
for q in [mp.mpf('1.001'), mp.mpf('1.5'), mp.mpf('1.8')]:
    a0 = 2*mp.asin(1/mp.sqrt(2*(q+1)))
    a1 = a0; a2 = mp.pi - a0
    Ph = Phi(a0, q); den = q + Ph/2
    M1t = a1*a1*mp.sin(a1)**2/den
    M2t = a2*a2*mp.sin(a2)**2/den
    s = mp.sin(a0); co = mp.cos(a0)
    G1 = -Ph*Wfun(a0)/den + a0*Ph*(q*q-1)*s*co/den**2
    G2 = -Ph*Wfun(a2)/den - a2*Ph*(q*q-1)*s*co/den**2
    mFp = -(M1t*G1 - M2t*G2)
    print(f'  q={mp.nstr(q,5)}: -Fp(1/2) = {mp.nstr(mFp,9)}')
