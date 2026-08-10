# -*- coding: utf-8 -*-
"""Gprime_J.py -- structure of G'(alpha;c) and J = G^2 + G' on the relevant ranges.
"""
import sys, mpmath as mp
sys.path.insert(0, r'F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-keylemma-E58FB1\reproducibility')
from keylemma_lib import Phi, Wfun, alpha1_of_c, alpha2_of_c, Gfun
mp.mp.dps = 25

def Gc(alpha, c, q):
    # partial dG/dc
    Ph = Phi(alpha, q); W = Wfun(alpha); s = mp.sin(alpha); co = mp.cos(alpha)
    den = q + c*Ph
    return Ph*Ph*W/den**2 + 2*alpha*Ph*(q*q-1)*s*co*(q - c*Ph)/den**3

def Ga(alpha, c, q):
    # partial dG/dalpha
    Ph = Phi(alpha, q); Php = 2*(q*q-1)*mp.sin(alpha)*mp.cos(alpha)
    W = Wfun(alpha); Wp = 2*(mp.cos(alpha)*mp.sin(alpha) - alpha)/mp.sin(alpha)**2
    s = mp.sin(alpha); co = mp.cos(alpha)
    den = q + c*Ph
    A = Ph*W; Ap = Php*W + Ph*Wp; Dp = c*Php
    B = 2*c*alpha*Ph*(q*q-1)*s*co
    Bp = 2*c*(q*q-1)*((Ph + alpha*Php)*s*co + alpha*Ph*(co*co - s*s))
    return -(Ap*den - A*Dp)/den**2 + (Bp*den - 2*B*Dp)/den**3

def Gprime(alpha, c, q):
    # total dG/dc along the curve: Ga*alpha' + Gc, alpha' = -alpha*Phi/(q+c*Phi)
    Ph = Phi(alpha, q)
    ap = -alpha*Ph/(q + c*Ph)
    return Ga(alpha,c,q)*ap + Gc(alpha,c,q)

def J(alpha, c, q):
    g = Gfun(alpha,c,q)
    return g*g + Gprime(alpha,c,q)

print('=== G\'(alpha;c) on (alpha0, pi-alpha0) for Region B samples ===')
for q in [mp.mpf('1.1'), mp.mpf('1.5'), mp.mpf('1.8')]:
    for c in [mp.mpf('0.46'), mp.mpf('0.49')]:
        a0 = 2*mp.asin(1/mp.sqrt(2*(q+1)))
        alo, ahi = a0, mp.pi - a0
        vals = [(a, Gprime(a,c,q)) for a in [alo, (alo+ahi)/2, ahi]]
        print(f'  q={mp.nstr(q,4)} c={mp.nstr(c,4)}: G\'({mp.nstr(alo,4)})={mp.nstr(vals[0][1],7)} '
              f'G\'(mid)={mp.nstr(vals[1][1],7)} G\'({mp.nstr(ahi,4)})={mp.nstr(vals[2][1],7)}')

print()
print('=== d/dalpha G\' sign on the range (check decreasing) ===')
for q in [mp.mpf('1.1'), mp.mpf('1.5'), mp.mpf('1.8')]:
    for c in [mp.mpf('0.46'), mp.mpf('0.49')]:
        a0 = 2*mp.asin(1/mp.sqrt(2*(q+1)))
        h = mp.mpf('1e-4')
        mn = mp.inf; mx = mp.ninf
        for k in range(1, 50):
            a = a0 + (mp.pi - 2*a0)*k/50
            d = (Gprime(a+h,c,q) - Gprime(a-h,c,q))/(2*h)
            mn = min(mn, d); mx = max(mx, d)
        print(f'  q={mp.nstr(q,4)} c={mp.nstr(c,4)}: dG\'/da in [{mp.nstr(mn,6)}, {mp.nstr(mx,6)}]')

print()
print('=== J(alpha;c) values and sign of J on the range ===')
for q in [mp.mpf('1.1'), mp.mpf('1.5'), mp.mpf('1.8')]:
    for c in [mp.mpf('0.46'), mp.mpf('0.49')]:
        a0 = 2*mp.asin(1/mp.sqrt(2*(q+1)))
        vals = [(a, J(a,c,q)) for a in [a0, (a0+mp.pi-a0)/2, mp.pi-a0]]
        print(f'  q={mp.nstr(q,4)} c={mp.nstr(c,4)}: J({mp.nstr(a0,4)})={mp.nstr(vals[0][1],7)} '
              f'J(mid)={mp.nstr(vals[1][1],7)} J({mp.nstr(mp.pi-a0,4)})={mp.nstr(vals[2][1],7)}')
