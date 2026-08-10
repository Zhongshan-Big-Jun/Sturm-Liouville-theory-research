# -*- coding: utf-8 -*-
"""struct_m1m2.py -- fast numpy structure of M1, M2 over D.
Asks: (a) is M1 increasing in u (then min at u->0 or corner)?  (b) is M2
increasing in q (then max at q->1+)?  (c) C4 curve L(v) monotone?
"""
import numpy as np

def M1v(q, u):
    A = np.pi - np.arctan(u/q); t = np.arctan(u)
    return 6*A*A*q*q + 2*A*A*u*u - 2*A*q*u + 4*A*q*t - 3*u*u - u*(1+3*u*u)*t
def M2v(q, u):
    A = np.pi - np.arctan(u/q); t = np.arctan(u)
    return 4*A*A*u*q - 7*A*q*q - 9*A*u*u + 2*A*(q*q+u*u)/(1+u*u) + t*(4*A*u - 5*q - 9*q*u*u)

# (a) dM1/du sign on a fine grid
print('=== dM1/du on grid (q in 1.001..50, u in 0..sqrt(2q+1)) ===')
h = 1e-6
qs = np.concatenate([np.linspace(1.001, 2, 40), np.linspace(2, 10, 40), np.linspace(10, 50, 20)])
worst = (1e9, None)
pos = 0
for q in qs:
    u = np.linspace(1e-4, np.sqrt(2*q+1), 200)
    d = (M1v(q, u+h) - M1v(q, u-h))/(2*h)
    dmin = d.min()
    if dmin < worst[0]: worst = (dmin, (q, u[d.argmin()]))
    pos += (d > 0).sum()
print('  min dM1/du = %s at q=%s u=%s ; #positive = %d' % (worst[0], worst[1][0], worst[1][1], pos))

# (b) dM2/dq sign on a fine grid
print('=== dM2/dq on grid ===')
worst2 = (-1e9, None); neg = 0
for q in qs:
    u = np.linspace(1e-4, np.sqrt(2*q+1), 200)
    d = (M2v(q+h, u) - M2v(q-h, u))/(2*h)
    dmax = d.max()
    if dmax > worst2[0]: worst2 = (dmax, (q, u[d.argmax()]))
    neg += (d < 0).sum()
print('  max dM2/dq = %s at q=%s u=%s ; #negative = %d' % (worst2[0], worst2[1][0], worst2[1][1], neg))

# (c) C4 curve: v = arctan(u) in [2pi/7, 2pi/5), q(v) = tan v / tan(pi - 2.5v)
print('=== C4 curve: L(v) and dL/dv ===')
def q_of_v(v):
    return np.tan(v)/np.tan(np.pi - 2.5*v)
def Lv(v):
    q = q_of_v(v); u = np.tan(v)
    A = 2.5*v
    return (q*q+u*u)*(2*A*q - 3*u + 2*v) - 3*u*q*v*(1+u*u)
vv = np.linspace(2*np.pi/7, 2*np.pi/5 - 1e-4, 4000)
L = Lv(vv); qq = q_of_v(vv)
i = L.argmin()
print('  min L = %s at v=%s (q=%s)' % (L.min(), vv[i], qq[i]))
dL = np.gradient(L, vv)
print('  dL/dv min = %s max = %s' % (dL.min(), dL.max()))
print('  L(2pi/7)=%s L(2pi/5-eps)=%s' % (Lv(2*np.pi/7), Lv(2*np.pi/5-1e-4)))

# (d) B6u: IN(2,u) for u in (0, sqrt5)
print('=== B6u: IN(2,u) on (0,sqrt5) ===')
def IN(q, u):
    A = np.pi - np.arctan(u/q); t = np.arctan(u)
    return (q*q+u*u)*A*(2*A*q - 3*u + 2*t) - 3*u*q*(1+u*u)*t
uu = np.linspace(1e-6, np.sqrt(5), 4000)
IN2 = IN(2, uu)
i = IN2.argmin()
print('  min IN(2,u) = %s at u=%s' % (IN2.min(), uu[i]))
print('  IN(2,sqrt5)=%s  IN(2,0+)=%s' % (IN2[-1], IN2[0]))
print('  monotone decreasing in u?', np.all(np.diff(IN2) < 0))

# (e) CORNER curve: G2(1/2;q) closed form monotone?
print('=== corner: G2(1/2;q) for q>=2 ===')
def G2_12(q):
    x = 2*np.arcsin(1/np.sqrt(2*(q+1)))
    return 2*q*((np.pi-x)*(q+1) - 3*np.sqrt(2*q+1))/(2*q+1)**1.5
qq2 = np.linspace(2, 50, 5000)
G = G2_12(qq2)
print('  min G2(1/2;q) = %s at q=%s ; increasing? %s' % (G.min(), qq2[G.argmin()], np.all(np.diff(G) > 0)))
