# -*- coding: utf-8 -*-
"""verify_dM2dq.py -- exact dM2/dq formula vs finite differences; sign scan."""
import sys, mpmath as mp
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T050000Z-keylemma2-5A35E5\reproducibility")
import numpy as np
mp.mp.dps = 40

def M2mp(q, u):
    A = mp.pi - mp.atan(u/q); t = mp.atan(u)
    return 4*A*A*u*q - 7*A*q*q - 9*A*u*u + 2*A*(q*q+u*u)/(1+u*u) + t*(4*A*u - 5*q - 9*q*u*u)

def dM2dq(q, u):
    A = mp.pi - mp.atan(u/q); t = mp.atan(u); S = q*q + u*u
    return (4*A*A*u + 8*A*u*u*q/S - 7*q*q*u/S - 14*A*q - 9*u**3/S
            + 2*u/(1+u*u) + 4*A*q/(1+u*u) + t*(4*u*u/S - 5 - 9*u*u))

print('=== dM2/dq formula vs central FD (mpmath 40d) ===')
ok = True
for qv in ['1.01','1.5','2','10','100']:
    for cv in ['0.05','0.2','0.4','0.49']:
        q = mp.mpf(qv); c = mp.mpf(cv)
        g = mp.pi - L_alpha2 if False else None
        # u from c via kl2
        import kl2_lib as L
        u = q*mp.tan(L.gamma_of(q, c))
        h = mp.mpf('1e-6')*q
        fd = (M2mp(q+h, u) - M2mp(q-h, u))/(2*h)
        f = dM2dq(q, u)
        rel = abs(fd-f)/abs(fd)
        ok &= rel < mp.mpf('1e-9')
        if rel > mp.mpf('1e-9'):
            print('  MISMATCH q=%s c=%s rel=%s' % (qv, cv, mp.nstr(rel,3)))
print('  formula OK:', ok)

print('=== dM2/dq sign scan over D (numpy) ===')
def M2v(q, u):
    A = np.pi - np.arctan(u/q); t = np.arctan(u)
    return 4*A*A*u*q - 7*A*q*q - 9*A*u*u + 2*A*(q*q+u*u)/(1+u*u) + t*(4*A*u - 5*q - 9*q*u*u)
h = 1e-6
qs = np.concatenate([np.linspace(1.0005, 2, 60), np.linspace(2, 10, 60), np.linspace(10, 100, 60), np.linspace(100, 2000, 50)])
worst = (-1e18, None); viol = 0
for q in qs:
    u = np.linspace(1e-6, np.sqrt(2*q+1), 400)
    d = (M2v(q+h, u) - M2v(q-h, u))/(2*h)
    mx = d.max()
    if mx > worst[0]: worst = (mx, (q, u[d.argmax()]))
    viol += (d >= 0).sum()
print('  max dM2/dq = %s at q=%s u=%s ; #violations = %d' % (worst[0], worst[1][0], worst[1][1], viol))

print('=== dM2/dq at q=1: g(u) profile and max ===')
def g(u):
    q = mp.mpf(1)
    return dM2dq(q, mp.mpf(u))
uu = np.linspace(1e-4, np.sqrt(3), 20000)
gv = np.array([float(g(u)) for u in uu])
print('  max g = %s at u=%s ; g(sqrt3)=%s g(0)=%s' % (gv.max(), uu[gv.argmax()], gv[-1], gv[0]))
