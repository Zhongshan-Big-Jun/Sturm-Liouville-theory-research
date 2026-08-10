import mpmath as mp
import numpy as np
mp.mp.prec = 120
pi = mp.pi; s15 = mp.sqrt(15); a0 = mp.acos(mp.mpf(1)/4)/pi
def dphi_eps(e):
    b = 1 - e
    u = np.cos(2*np.pi*b); v = np.sin(2*np.pi*b)
    N = (56*np.pi*a0 - 6*s15)*u**2 + (2*np.pi*a0 + 3*s15)*u + (3*s15 - 58*np.pi*a0) + 2*s15*np.pi*(1-b)*(1-4*u)*v
    return -N/(60*np.pi)
def dphi_np(b):
    a0n = float(a0); s15n = float(s15)
    u = np.cos(2*np.pi*b); v = np.sin(2*np.pi*b)
    N = (56*np.pi*a0n - 6*s15n)*u**2 + (2*np.pi*a0n + 3*s15n)*u + (3*s15n - 58*np.pi*a0n) + 2*s15n*np.pi*(1-b)*(1-4*u)*v
    return -N/(60*np.pi)
for e in (1e-3, 5e-4, 1e-4, 1e-5, 1e-6, 1e-7):
    v1 = dphi_eps(e)/e**2
    v2 = dphi_np(1-e)/(e**2)
    print("e=%.0e  mp-impl=%.9f  np-impl=%.9f" % (e, float(v1), float(v2)))
