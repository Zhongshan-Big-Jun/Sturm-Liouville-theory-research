# -*- coding: utf-8 -*-
"""survey_m1m2.py -- structure of M1=dIN/dq and M2=dIN/du over D (light grid)."""
import sys, mpmath as mp
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T050000Z-keylemma2-5A35E5\reproducibility")
import kl2_lib as L
mp.mp.dps = 25

def u_of(q, c):
    return q*mp.tan(L.gamma_of(q, c))
def A_of(q, u):
    return mp.pi - mp.atan(u/q)
def IN(q, u):
    A = A_of(q, u); t = mp.atan(u)
    return (q*q+u*u)*A*(2*A*q - 3*u + 2*t) - 3*u*q*(1+u*u)*t
def M1(q, u):
    A = A_of(q, u); t = mp.atan(u)
    return 6*A*A*q*q + 2*A*A*u*u - 2*A*q*u + 4*A*q*t - 3*u*u - u*(1+3*u*u)*t
def M2(q, u):
    A = A_of(q, u); t = mp.atan(u)
    return 4*A*A*u*q - 7*A*q*q - 9*A*u*u + 2*A*(q*q+u*u)/(1+u*u) + t*(4*A*u - 5*q - 9*q*u*u)

qs = [mp.mpf('1.001'),mp.mpf('1.01'),mp.mpf('1.05'),mp.mpf('1.1'),mp.mpf('1.2'),mp.mpf('1.5'),mp.mpf('2'),mp.mpf('2.5'),mp.mpf('3'),mp.mpf('4'),mp.mpf('5'),mp.mpf('8'),mp.mpf('10'),mp.mpf('20'),mp.mpf('50'),mp.mpf('100')]
cs = [mp.mpf('0.005'),mp.mpf('0.05'),mp.mpf('0.1'),mp.mpf('0.2'),mp.mpf('0.3'),mp.mpf('0.4'),mp.mpf('0.45'),mp.mpf('0.49')]

print('=== M1 ===')
mn1 = mp.inf; mx1 = -mp.inf; atmn1 = atmx1 = None; viol = 0
for q in qs:
    for c in cs:
        u = u_of(q, c)
        v = M1(q, u)
        if v < mn1: mn1, atmn1 = v, (q, c)
        if v > mx1: mx1, atmx1 = v, (q, c)
        if v <= 0: viol += 1
print('min M1=%s at %s %s | max=%s at %s %s | M1<=0 count=%d' % (mp.nstr(mn1,7), mp.nstr(atmn1[0],5), mp.nstr(atmn1[1],4), mp.nstr(mx1,7), mp.nstr(atmx1[0],5), mp.nstr(atmx1[1],4), viol))

print('=== M2 ===')
mn2 = mp.inf; mx2 = -mp.inf; atmn2 = atmx2 = None; viol2 = 0
for q in qs:
    for c in cs:
        u = u_of(q, c)
        v = M2(q, u)
        if v < mn2: mn2, atmn2 = v, (q, c)
        if v > mx2: mx2, atmx2 = v, (q, c)
        if v >= 0: viol2 += 1
print('min M2=%s at %s %s | max=%s at %s %s | M2>=0 count=%d' % (mp.nstr(mn2,7), mp.nstr(atmn2[0],5), mp.nstr(atmn2[1],4), mp.nstr(mx2,7), mp.nstr(atmx2[0],5), mp.nstr(atmx2[1],4), viol2))

print('=== M2 max along u at fixed q (closest to 0) ===')
for qv in ['1.01','1.1','1.5','2','3','5','10']:
    q = mp.mpf(qv); umax = mp.sqrt(2*q+1)
    mx = -mp.inf; at = None
    for i in range(1, 400):
        u = umax*mp.mpf(i)/400
        v = M2(q, u)
        if v > mx: mx, at = v, u
    print('q=%s: max M2 over u = %s at u=%s' % (qv, mp.nstr(mx,6), mp.nstr(at,5)))

print('=== C4: G2(0.4;q) and its q-derivative ===')
for qv in ['1.0001','1.01','1.1','1.5','2','3','5','10','100']:
    q = mp.mpf(qv)
    dq = (L.G2(mp.mpf('0.4'), q*mp.mpf('1.000001')) - L.G2(mp.mpf('0.4'), q*mp.mpf('0.999999')))/(mp.mpf('2e-6')*q)
    print('q=%s: G2(0.4)=%s  dG2/dq=%s' % (qv, mp.nstr(L.G2(mp.mpf('0.4'), q),8), mp.nstr(dq,6)))

print('=== corner curve: G2(1/2;q) and dG2/dq ===')
for qv in ['1.0001','1.1','2','3','10','100']:
    q = mp.mpf(qv)
    dq = (L.G2(mp.mpf('0.5'), q*mp.mpf('1.000001')) - L.G2(mp.mpf('0.5'), q*mp.mpf('0.999999')))/(mp.mpf('2e-6')*q)
    print('q=%s: G2(1/2)=%s  dG2/dq=%s' % (qv, mp.nstr(L.G2(mp.mpf('0.5'), q),8), mp.nstr(dq,6)))
