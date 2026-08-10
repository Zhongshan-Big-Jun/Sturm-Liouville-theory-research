# -*- coding: utf-8 -*-
"""verify_m2collapse.py -- (1) M2(1,u) = pi*(4u(pi-atan u)-5-9u^2) exact?
(2) dM2/dq < 0 over D (fine scan incl. large q)?
(3) dM1/du < 0 and m(q)=M1(q,sqrt(2q+1)) increasing?
"""
import sys, mpmath as mp
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T050000Z-keylemma2-5A35E5\reproducibility")
import numpy as np
mp.mp.dps = 50

def M2v(q, u):
    A = np.pi - np.arctan(u/q); t = np.arctan(u)
    return 4*A*A*u*q - 7*A*q*q - 9*A*u*u + 2*A*(q*q+u*u)/(1+u*u) + t*(4*A*u - 5*q - 9*q*u*u)
def M2mp(q, u):
    A = mp.pi - mp.atan(u/q); t = mp.atan(u)
    return 4*A*A*u*q - 7*A*q*q - 9*A*u*u + 2*A*(q*q+u*u)/(1+u*u) + t*(4*A*u - 5*q - 9*q*u*u)

print('=== (1) M2(1,u) = pi*(4u(pi-atan u) - 5 - 9u^2) ===')
maxrel = 0
for uv in ['0.1','0.3','0.52','1.0','1.5','1.73']:
    u = mp.mpf(uv)
    lhs = M2mp(mp.mpf(1), u)
    rhs = mp.pi*(4*u*(mp.pi - mp.atan(u)) - 5 - 9*u*u)
    rel = abs(lhs-rhs)/abs(lhs)
    maxrel = max(maxrel, rel)
    print('  u=%s: rel=%s' % (uv, mp.nstr(rel,3)))
print('  max rel err =', mp.nstr(maxrel,3))

print('=== (2) dM2/dq scan over D (numpy, fine) ===')
h = 1e-6
qs = np.concatenate([np.linspace(1.0005, 2, 60), np.linspace(2, 10, 60), np.linspace(10, 100, 60), np.linspace(100, 1000, 40)])
worst = (-1e18, None); viol = 0
for q in qs:
    u = np.linspace(1e-6, np.sqrt(2*q+1), 300)
    d = (M2v(q+h, u) - M2v(q-h, u))/(2*h)
    mx = d.max()
    if mx > worst[0]: worst = (mx, (q, u[d.argmax()]))
    viol += (d >= 0).sum()
print('  max dM2/dq = %s at q=%s u=%s ; #violations = %d' % (worst[0], worst[1][0], worst[1][1], viol))

print('=== (3) dM1/du < 0 and m(q)=M1(q,sqrt(2q+1)) ===')
def M1v(q, u):
    A = np.pi - np.arctan(u/q); t = np.arctan(u)
    return 6*A*A*q*q + 2*A*A*u*u - 2*A*q*u + 4*A*q*t - 3*u*u - u*(1+3*u*u)*t
worst1 = (1e18, None); viol1 = 0
for q in qs:
    u = np.linspace(1e-6, np.sqrt(2*q+1), 300)
    d = (M1v(q, u+h) - M1v(q, u-h))/(2*h)
    mn = d.min()
    if mn < worst1[0]: worst1 = (mn, (q, u[d.argmin()]))
    viol1 += (d >= 0).sum()
print('  min dM1/du = %s at q=%s u=%s ; #violations = %d' % (worst1[0], worst1[1][0], worst1[1][1], viol1))
qq = np.linspace(1.0005, 50, 4000)
m = M1v(qq, np.sqrt(2*qq+1))
print('  m(q)=M1(q,sqrt(2q+1)): min=%s at q=%s ; increasing? %s ; m(1)=%s' % (m.min(), qq[m.argmin()], np.all(np.diff(m) > 0), m[0]))

print('=== (4) C4: L(v) on [2pi/7, 2pi/5) - is it increasing? ===')
def q_of_v(v): return np.tan(v)/np.tan(np.pi - 2.5*v)
def Lv(v):
    q = q_of_v(v); u = np.tan(v)
    return (q*q+u*u)*(2*2.5*v*q - 3*u + 2*v) - 3*u*q*v*(1+u*u)
vv = np.linspace(2*np.pi/7, 2*np.pi/5 - 1e-6, 20000)
L = Lv(vv)
inc = np.all(np.diff(L) > 0)
print('  L increasing?', inc, ' min L =', L.min(), ' at v =', vv[L.argmin()])
