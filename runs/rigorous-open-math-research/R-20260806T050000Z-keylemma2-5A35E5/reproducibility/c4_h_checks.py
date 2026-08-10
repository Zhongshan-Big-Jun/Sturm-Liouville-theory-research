# -*- coding: utf-8 -*-
"""c4_h_checks.py -- corrected C4 curve K(v) and h(u) for all u>0."""
import numpy as np

# ---- C4: on c=0.4 curve, v=arctan(u) in [2pi/7, 2pi/5), q(v)=tan v/tan(pi-2.5v)
# IN = A*K, A=2.5v>0,  K = (q^2+u^2)(5 v q - 3 u + 2 v) - 1.2 u q (1+u^2)
def q_of_v(v): return np.tan(v)/np.tan(np.pi - 2.5*v)
def Kv(v):
    q = q_of_v(v); u = np.tan(v)
    return (q*q+u*u)*(5*v*q - 3*u + 2*v) - 1.2*u*q*(1+u*u)
vv = np.linspace(2*np.pi/7, 2*np.pi/5 - 1e-6, 40000)
K = Kv(vv)
print('=== C4: K(v) on [2pi/7, 2pi/5) ===')
print('  min K = %s at v=%s ; increasing? %s ; K(2pi/7)=%s' % (K.min(), vv[K.argmin()], np.all(np.diff(K) > 0), Kv(2*np.pi/7)))
dK = np.gradient(K, vv)
print('  dK/dv min = %s max = %s' % (dK.min(), dK.max()))

# ---- h(u) = 4u(pi - atan u) - 5 - 9u^2  (M2(1,u) = pi*h(u))
def h(u): return 4*u*(np.pi - np.arctan(u)) - 5 - 9*u*u
uu = np.linspace(0, 100, 200000)
hmax = h(uu).max()
print('=== h(u) for u in (0,100): max = %s at u=%s ; h(0)=%s ; h(100)=%s' % (hmax, uu[hmax==h(uu)][0], h(1e-9), h(100)))
# h(u) < 0 for ALL u>0? check far out and fine near critical point
uu2 = np.linspace(0.4, 0.7, 100000)
print('  h max on (0.4,0.7):', h(uu2).max())
# h'(u) = 4(pi - atan u) - 4u/(1+u^2) - 18u ; h'' < 0 (concave)
hp = 4*(np.pi - np.arctan(uu2)) - 4*uu2/(1+uu2**2) - 18*uu2
print('  h prime sign change: hprime(0.5)=%s hprime(0.53)=%s' % (4*(np.pi-np.arctan(0.5))-4*0.5/1.25-9, 4*(np.pi-np.arctan(0.53))-4*0.53/1.2809-9.54))

# ---- M2(2,u) on (0, sqrt5) (for R1 via q>=2 reduction, alternate route)
def M2v(q, u):
    A = np.pi - np.arctan(u/q); t = np.arctan(u)
    return 4*A*A*u*q - 7*A*q*q - 9*A*u*u + 2*A*(q*q+u*u)/(1+u*u) + t*(4*A*u - 5*q - 9*q*u*u)
uu3 = np.linspace(1e-6, np.sqrt(5), 100000)
m2 = M2v(2, uu3)
print('=== M2(2,u) on (0,sqrt5): max = %s at u=%s' % (m2.max(), uu3[m2.argmax()]))

# ---- corner curve M2 (for reference)
def corner_M2(q):
    u = np.sqrt(2*q+1)
    return M2v(q, u)
qq = np.linspace(1.0005, 100, 100000)
cm = corner_M2(qq)
print('=== M2 on corner curve q in (1,100]: max = %s at q=%s' % (cm.max(), qq[cm.argmax()]))
