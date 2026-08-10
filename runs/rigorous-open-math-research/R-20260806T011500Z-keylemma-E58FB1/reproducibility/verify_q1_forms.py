# -*- coding: utf-8 -*-
"""verify_q1_forms.py -- check closed forms for J1(1,c), J2(1,c), Hp(1,c)."""
import numpy as np

def W(u):
    return 3 + 2*u/np.tan(u)
def Wp(u):
    return 2*(np.sin(u)*np.cos(u)-u)/np.sin(u)**2
def N1(u):
    return W(u)**2 + W(u) + u*Wp(u)
def N2(w):
    return W(w)**2 + W(w) + w*Wp(w)
def T(u):
    return u*Wp(u) + W(u)

print('=== signs on u in (pi/3, pi/2), w=2u in (2pi/3, pi) ===')
mn1 = min(N1(u) for u in np.linspace(np.pi/3+1e-9, np.pi/2-1e-9, 5001))
mn2 = min(N2(w) for w in np.linspace(2*np.pi/3+1e-9, np.pi-1e-9, 5001))
mxT = max(T(2*u)-T(u) for u in np.linspace(np.pi/3+1e-9, np.pi/2-1e-9, 5001))
print(f'  min N1 on (pi/3,pi/2) = {mn1:+.9f}')
print(f'  max N2 on (2pi/3,pi)  = {mn2:+.9f}')
print(f'  max [T(2u)-T(u)]      = {mxT:+.9f}')
# verify closed forms against direct computation at q=1
from scipy.optimize import brentq
def alpha1_q1(c): return np.pi/(2*(1+c))
def alpha2_q1(c): return np.pi/(1+c)
def G_q1(a, c):
    return -W(a)/(1+c)
def Gp_q1(a, c, ap):
    # d/dc G(a(c),c) = -W(a)/(1+c), G = -W/(1+c); G' = (W'(a)*a'(c)*(1+c) + W(a))/(1+c)^2
    return (Wp(a)*ap*(1+c) + W(a))/(1+c)**2
for c in [0.1, 0.3, 0.44, 0.49]:
    u = alpha1_q1(c)
    a1, a2 = u, 2*u
    a1p = -np.pi/(2*(1+c)**2)
    a2p = -np.pi/(1+c)**2
    J1_dir = G_q1(a1,c)**2 + Gp_q1(a1,c,a1p)
    J1_form = N1(u)/(1+c)**2
    J2_dir = G_q1(a2,c)**2 + Gp_q1(a2,c,a2p)
    J2_form = N2(2*u)/(1+c)**2
    Hp_dir = Gp_q1(a2,c,a2p) - Gp_q1(a1,c,a1p)
    Hp_form = (T(2*u)-T(u))/(1+c)**2
    print(f'  c={c}: J1 dir={J1_dir:+.9f} form={J1_form:+.9f} | J2 dir={J2_dir:+.9f} form={J2_form:+.9f} | Hp dir={Hp_dir:+.9f} form={Hp_form:+.9f}')
