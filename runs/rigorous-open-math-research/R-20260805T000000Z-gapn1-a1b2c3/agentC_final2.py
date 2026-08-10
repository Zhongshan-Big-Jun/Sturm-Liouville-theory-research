# -*- coding: utf-8 -*-
"""Final check with tolerance + mpmath spot check at tight corners."""
import numpy as np
from scipy.optimize import brentq

def theta(x, mu):
    return np.arctan(mu*np.tan(x)) + np.pi*np.floor((x+np.pi/2)/np.pi)

def thp(x, mu):
    t = np.tan(x)
    return mu*(1+t*t)/(1+mu*mu*t*t)

def F(x, mu, c):
    return theta(x, mu) + c*x

g1 = np.linspace(1e-8, 2*np.pi, 30000)
g2 = np.linspace(1e-8, 3*np.pi, 30000)

def xk(mu, c, k, g):
    d = theta(g, mu) + c*g - k*np.pi
    sg = np.signbit(d)
    idx = np.nonzero(sg[1:] != sg[:-1])[0]
    lo, hi = g[idx[0]], g[idx[0]+1]
    return brentq(lambda a: F(a, mu, c) - k*np.pi, lo, hi)

PI2 = np.pi**2
fails = []
n = 0
for mu in [1.02, 1.05, 1.1, 1.2, 1.5, 2.0, 3.0, 5.0, 10.0, 100.0, 1e4]:
    for c in np.concatenate([np.logspace(-3, -0.6, 20), np.linspace(0.3, 1.0, 25), np.linspace(1.05, 5, 30), np.logspace(0.7, 4, 25)]):
        n += 1
        x1, x2 = xk(mu, c, 1, g1), xk(mu, c, 2, g2)
        W = (mu+c)**2*(x2**2-x1**2)
        rel = 1e-9
        assert W > 3*PI2*(1-rel) and W < 3*PI2*mu**2*(1+rel), (mu, c, W)
        if c >= 1:
            b2 = (mu+c)**2*(np.pi*mu/(1+mu*c))*(2*np.pi*mu/(1+mu*c) + np.pi/(1+c))
            assert W <= b2 + 1e-9 and b2 < 3*PI2*mu**2, (mu, c, "chain2")
            assert x1 <= np.pi/(1+c) + 1e-9
            assert x2 <= 2*np.pi*mu/(1+mu*c) + 1e-9
            assert x2 - x1 <= np.pi*mu/(1+mu*c) + 1e-9
        elif c >= 1/3:
            bB = 3*PI2*(mu+c)**2/(1+c)**2
            assert W <= bB + 1e-9 and bB < 3*PI2*mu**2, (mu, c, "chainB")
            assert x1 >= np.pi/(1+c) - 1e-9
            assert x2 <= 2*np.pi/(1+c) + 1e-9
        else:
            p1, p2 = thp(x1, mu), thp(x2, mu)
            U = x2**2 - x1**2
            Up = -2*x2**2/(p2+c) + 2*x1**2/(p1+c)
            Wp = 2*(mu+c)*U + (mu+c)**2*Up
            assert Wp < 0, (mu, c, "Wp")
print(f"checked {n} (mu,c) points with rel tol 1e-9: ALL PASS")

# mpmath spot check at the tightest corners
import mpmath as mp
mp.mp.dps = 60
def W_mp(mu, c):
    def Fm(x):
        th = mp.atan(mu*mp.tan(x))
        br = mp.floor((x + mp.pi/2)/mp.pi)
        return th + mp.pi*br + c*x
    roots = []
    for k in (1, 2):
        # bracket: Fm increasing; find via mpmath findroot with interval scan (coarse)
        lo, hi = mp.mpf('1e-12'), mp.mpf('2')*mp.pi
        # find crossing of k*pi
        f = lambda x: Fm(x) - k*mp.pi
        a, b = lo, hi
        # simple bisection-like via findroot on [a,b] after locating sign change with 4000 steps
        prev = None; xr = None
        xs = [a + (b-a)*i/8000 for i in range(8001)]
        vals = [f(x) for x in xs]
        for i in range(8000):
            if vals[i]*vals[i+1] <= 0:
                xr = mp.findroot(f, (xs[i], xs[i+1]))
                break
        roots.append(xr)
    x1, x2 = roots
    W = (mu+c)**2*(x2**2 - x1**2)
    return W

for mu, c in [(mp.mpf('1.001'), mp.mpf('1e-6')), (mp.mpf('1.05'), mp.mpf('1e-6')), (mp.mpf('100'), mp.mpf('1e-6')), (mp.mpf('1.05'), mp.mpf('1e-2'))]:
    W = W_mp(mu, c)
    lo = 3*mp.pi**2; hi = 3*mp.pi**2*mu**2
    print(f"mpmath mu={mp.nstr(mu,8)} c={mp.nstr(c,4)}: W-3pi^2 = {mp.nstr(W-lo, 5)}  (W-3pi^2mu^2) = {mp.nstr(W-hi, 5)}")
