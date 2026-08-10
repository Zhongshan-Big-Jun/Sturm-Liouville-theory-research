# -*- coding: utf-8 -*-
"""explore3.py -- q-monotonicity tests for H and F~'; G1 sign; corner strip analysis.
"""
import sys, mpmath as mp
sys.path.insert(0, r'F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-keylemma-E58FB1\reproducibility')
from keylemma_lib import Phi, Wfun, alpha1_of_c, alpha2_of_c, Gfun, G1_of_c, G2_of_c
mp.mp.dps = 30

def Ftil_p(c, q):
    a1 = alpha1_of_c(c, q); a2 = alpha2_of_c(c, q)
    M1t = a1*a1*mp.sin(a1)**2/(q + c*Phi(a1, q))
    M2t = a2*a2*mp.sin(a2)**2/(q + c*Phi(a2, q))
    return M1t*Gfun(a1, c, q) - M2t*Gfun(a2, c, q)

def H(c, q):
    return G2_of_c(c, q) - G1_of_c(c, q)

q1 = mp.mpf(1)
cs = [mp.mpf('1e-4') + mp.mpf('0.4998')*k/500 for k in range(501)]

print('=== A) H(q,c) - H(1,c) and F~\'(q,c) - F~\'(1,c): min over c ===')
for q in [mp.mpf('1.001'), mp.mpf('1.01'), mp.mpf('1.05'), mp.mpf('1.1'), mp.mpf('1.5'),
          mp.mpf('2'), mp.mpf('4'), mp.mpf('10'), mp.mpf('100')]:
    mH = mp.inf; mF = mp.inf; cH = None; cF = None
    for c in cs:
        dH = H(c,q) - H(c,q1); dF = Ftil_p(c,q) - Ftil_p(c,q1)
        if dH < mH: mH, cH = dH, c
        if dF < mF: mF, cF = dF, c
    print(f'  q={mp.nstr(q,5)}: min(H-H1)={mp.nstr(mH,6)} at c={mp.nstr(cH,4)} | min(Fp-Fp1)={mp.nstr(mF,6)} at c={mp.nstr(cF,4)}')

print()
print('=== B) dH/dq at q=1 (finite difference, h=1e-4): shape over c ===')
for q in [mp.mpf('1.00005')]:
    h = mp.mpf('1e-4')
    vals = []
    for c in cs:
        d = (H(c, q+h) - H(c, q-h))/(2*h)
        vals.append((c, d))
    mn = min(vals, key=lambda t: t[1]); mx = max(vals, key=lambda t: t[1])
    print(f'  min dH/dq(1,c) = {mp.nstr(mn[1],6)} at c={mp.nstr(mn[0],4)} | max = {mp.nstr(mx[1],6)} at c={mp.nstr(mx[0],4)}')
    # sample values
    for c in [mp.mpf('0.05'), mp.mpf('0.2'), mp.mpf('0.4'), mp.mpf('0.4999')]:
        d = (H(c, q+h) - H(c, q-h))/(2*h)
        print(f'    c={mp.nstr(c,4)}: dH/dq = {mp.nstr(d,6)}')

print()
print('=== C) dH/dq for q in {1.05, 1.5, 2, 4, 10}: sign check ===')
for q in [mp.mpf('1.05'), mp.mpf('1.5'), mp.mpf('2'), mp.mpf('4'), mp.mpf('10')]:
    h = mp.mpf('1e-4')
    mn = mp.inf; mx = mp.ninf
    for c in cs:
        d = (H(c, q+h) - H(c, q-h))/(2*h)
        if d < mn: mn = d
        if d > mx: mx = d
    print(f'  q={mp.nstr(q,4)}: dH/dq in [{mp.nstr(mn,6)}, {mp.nstr(mx,6)}]')

print()
print('=== D) G1 sign: min G1 over (q,c) grid ===')
for q in [mp.mpf('1.001'), mp.mpf('1.1'), mp.mpf('2'), mp.mpf('10'), mp.mpf('100'), mp.mpf('1e4')]:
    mn = mp.inf
    for c in cs:
        g = G1_of_c(c, q)
        if g < mn: mn = g
    print(f'  q={mp.nstr(q,5)}: min G1 = {mp.nstr(mn,7)}')

print()
print('=== E) closed form check: H(q,1/2) vs 2*pi*q*(q+1)/(2q+1)^1.5 ===')
for q in [mp.mpf('1.001'), mp.mpf('1.5'), mp.mpf('2'), mp.mpf('4'), mp.mpf('10')]:
    c = mp.mpf('0.5')
    hval = H(c, q)
    cf = 2*mp.pi*q*(q+1)/(2*q+1)**mp.mpf('1.5')
    print(f'  q={mp.nstr(q,4)}: H(q,1/2)={mp.nstr(hval,10)}  formula={mp.nstr(cf,10)}  diff={mp.nstr(abs(hval-cf),10)}')
