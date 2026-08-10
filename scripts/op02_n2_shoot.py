# -*- coding: utf-8 -*-
import numpy as np
from scipy.optimize import brentq

R = 4.0; s = np.sqrt(R); t = 1.0/(3*s+2)
a, b, c = s*t, t, s*t
print("a,b,c/2 =", a, b, c/2)

# half-string [1,R,1] widths (a,b,c/2) on [0, 0.5]
def shoot_half(w, endBC):
    """integrate -u''=w^2 rho u, u(0)=0, u'(0)=1; return u(0.5) or u'(0.5)."""
    x = 0.0; u = 0.0; up = 1.0
    blocks = [(a,1.0),(b,R),(c/2.0,1.0)]
    for L, cc in blocks:
        ww = w*np.sqrt(cc)
        # exact step over block
        uL = u*np.cos(ww*L) + up*np.sin(ww*L)/ww
        uLp = -u*ww*np.sin(ww*L) + up*np.cos(ww*L)
        u, up = uL, uLp
    return up if endBC=='mixed' else u

def roots_of(fun, k, lo=1e-6, hi=60.0, n=60000):
    ws = np.linspace(lo, hi, n)
    d = np.array([fun(w) for w in ws])
    sg = np.signbit(d[1:]) != np.signbit(d[:-1])
    idx = np.nonzero(sg)[0]
    out = []
    for i in idx:
        r = brentq(fun, ws[i], ws[i+1], xtol=1e-14, rtol=1e-14)
        out.append(r)
        if len(out)>=k: break
    return np.array(out)

mu = roots_of(lambda w: shoot_half(w,'mixed'), 4)
nu = roots_of(lambda w: shoot_half(w,'dir'), 4)
print("half mixed mu^2:", mu**2)
print("half dir   nu^2:", nu**2)
print("full eigenvalues from earlier: [4.7953, 16.7556, 71.7920, 107.6726, 157.9137, 217.7454]")
