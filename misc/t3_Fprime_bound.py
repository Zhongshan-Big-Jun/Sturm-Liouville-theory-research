# -*- coding: utf-8 -*-
"""t3_Fprime_bound.py: worst-case bound for F'(b) on [1/2,2/3]."""
from mpmath import mp, mpf, sqrt, pi as mppi
mp.dps = 40
def A(b): return mpf('147')/10*b**6 + mpf('189')/5*b**5 + mpf('21')/2*b**4 - 42*b**3 - mpf('63')/2*b**2 + mpf('21')/5*b + mpf('63')/10
def B(b): return 8*b**5 + mpf('10')/3*b**4 - mpf('32')/3*b**3 + mpf('16')/3*b - mpf('2')/3
def C(b): return mpf('35')/3*b**4 + mpf('44')/3*b**3 - 6*b**2 - mpf('28')/3*b - mpf('1')/3
def Fp(b): return A(b) + mppi*B(b) + sqrt(mpf(5))*C(b)
def Fp_wc(b): return A(b) + mpf('22')/7*abs(B(b)) + mpf('9')/4*abs(C(b))
lo, hi, loW, hiW = mpf(1e30), mpf(-1e30), mpf(1e30), mpf(-1e30)
for i in range(4001):
    b = mpf('0.5') + mpf(i)*mpf('1')/6000
    if b > mpf('2')/3: break
    v = Fp(b); w = Fp_wc(b)
    lo = min(lo, v); hi = max(hi, v)
    loW = min(loW, w); hiW = max(hiW, w)
print('Fp on [1/2,2/3]: [%.4f, %.4f]' % (lo, hi))
print('Fp worst-case (22/7, 9/4): [%.4f, %.4f]' % (loW, hiW))
# also check monotonicity of Fp directly and whether Fp'' helps
def Fpp(b, h=mpf('1e-6')): return (Fp(b+h)-Fp(b-h))/(2*h)
lo2, hi2 = mpf(1e30), mpf(-1e30)
for i in range(2001):
    b = mpf('0.5') + mpf(i)*mpf('1')/6000
    if b > mpf('2')/3: break
    v = Fpp(b)
    lo2 = min(lo2, v); hi2 = max(hi2, v)
print('Fpp on [1/2,2/3]: [%.3f, %.3f]' % (lo2, hi2))
# sign of B, C on interval
loB, hiB, loC, hiC = mpf(1e30), mpf(-1e30), mpf(1e30), mpf(-1e30)
for i in range(4001):
    b = mpf('0.5') + mpf(i)*mpf('1')/6000
    if b > mpf('2')/3: break
    loB = min(loB, B(b)); hiB = max(hiB, B(b))
    loC = min(loC, C(b)); hiC = max(hiC, C(b))
print('B on interval: [%.4f, %.4f]; C: [%.4f, %.4f]' % (loB, hiB, loC, hiC))
