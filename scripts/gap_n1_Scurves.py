# -*- coding: utf-8 -*-
"""gap_n1_Scurves.py: S1(u), S2(u) individual structure for SUP."""
import numpy as np
from scipy.optimize import brentq
from gap_lib import lams_fast

def theta_half(mode, R, u, w):
    v = 0.5 - u
    x = w*u
    j = int(np.floor((x+np.pi/2)/np.pi))
    Phi = j*np.pi + np.arctan(np.sqrt(R)*np.tan(x))
    return Phi + w*np.sqrt(R)*v

def eigw(R, u, target):
    def G(w): return theta_half("SUP",R,u,w) - target
    wmax = 1.0
    while G(wmax) < 0 and wmax < 300: wmax *= 1.4
    return brentq(G, 0.01, wmax, xtol=1e-13)

def S(R, u, w):
    v = 0.5-u
    dth = np.sqrt(R)*u/(np.cos(w*u)**2+R*np.sin(w*u)**2) + np.sqrt(R)*v
    return np.sin(w*u)**2*2*w**2*np.sqrt(R)/((R*np.sin(w*u)**2+np.cos(w*u)**2)*dth)

R = 4.0
print("u      w1       w2       S1       S2       SC      dS1/du  dS2/du")
prev = None
for u in np.linspace(0.10, 0.485, 30):
    w1 = eigw(R, u, np.pi/2); w2 = eigw(R, u, np.pi)
    S1 = S(R,u,w1); S2 = S(R,u,w2)
    h=1e-5
    S1p = S(R,u+h,eigw(R,u+h,np.pi/2)); S2p = S(R,u+h,eigw(R,u+h,np.pi))
    print(f"{u:.3f}  {w1:7.4f} {w2:7.4f}  {S1:8.3f} {S2:8.3f}  {S1-S2:8.3f}  {(S1p-S1)/h:8.1f} {(S2p-S2)/h:8.1f}")
