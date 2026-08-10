# -*- coding: utf-8 -*-
"""12_branch_explore.py
Numerical exploration of theta1, theta2 (theta_k = sqrt(mu_k)*u) and G = mu2-mu1
across w in (0,2], R in {1500,1e4,1e6}, to anchor the elementary deep-sliver bounds.
Prints a table and checks candidate inequalities:
  C1: theta1 < pi*w for w <= 1/2
  C2: theta2 vs pi/(2c), vs pi/2, vs pi*w etc. (branch structure)
  C3: theta2 - pi/2 sign; theta1 vs pi/2.
ASCII punctuation.
"""
import numpy as np
import mpmath as mp
mp.mp.dps = 30
PI2 = mp.mpf('9.86960440108935861883449099987615113531369940724079062641334937622')

def m12_np(mu, R, u):
    kh = np.sqrt(mu); kl = np.sqrt(mu/R)
    c1 = np.cos(kh*u); s1 = np.sin(kh*u)
    c2 = np.cos(kl*(1-2*u)); s2 = np.sin(kl*(1-2*u))
    a00 = c1*c2 - s1*s2*kl/kh
    a01 = c1*s2/kl + s1*c2/kh
    return a00*(s1/kh) + a01*c1

def m12_mp(mu, R, u):
    Rm = mp.mpf(R); um = mp.mpf(u)
    kh = mp.sqrt(mu); kl = mp.sqrt(mu/Rm)
    c1 = mp.cos(kh*um); s1 = mp.sin(kh*um)
    c2 = mp.cos(kl*(1-2*um)); s2 = mp.sin(kl*(1-2*um))
    a00 = c1*c2 - s1*s2*kl/kh
    a01 = c1*s2/kl + s1*c2/kh
    return a00*(s1/kh) + a01*c1

def roots(R, u):
    Rf = float(R); uf = float(u)
    hi = 4*float(np.pi**2)*Rf*1.0000001
    mu_grid = np.linspace(0.0, hi, 120001)
    y = m12_np(mu_grid, Rf, uf)
    idx = np.where(y[:-1]*y[1:] < 0)[0]
    out = []
    for i in idx[:3]:
        a, b = mp.mpf(mu_grid[i]), mp.mpf(mu_grid[i+1])
        fa = m12_mp(a, R, u)
        for _ in range(220):
            m = (a+b)/2
            fm = m12_mp(m, R, u)
            if (fm < 0) == (fa < 0):
                a = m; fa = fm
            else:
                b = m
        out.append((a+b)/2)
    return out

def table(R):
    eps = 1/mp.sqrt(R)
    print("R = %s (eps = %s), w_c = %s" % (R, mp.nstr(eps, 6), mp.nstr(1/(2*(1+eps)), 6)))
    print("%6s %12s %12s %12s %12s %12s %10s %10s %10s" % (
        "w", "mu1", "mu2", "th1", "th2", "G", "th1-piw", "th2-pi/2", "th2-pi/(2c)"))
    ws = ['0.001','0.01','0.05','0.1','0.19','0.25','0.3','0.4','0.45','0.48','0.49',
          '0.499','0.4999','0.5','0.5005','0.505','0.51','0.55','0.6','0.8','1.0','1.2','1.5','1.8','2.0']
    for w in ws:
        ww = mp.mpf(w)
        u = ww/mp.sqrt(R)
        rs = roots(R, u)
        m1, m2 = rs[0], rs[1]
        t1 = mp.sqrt(m1)*ww/mp.sqrt(R)
        t2 = mp.sqrt(m2)*ww/mp.sqrt(R)
        c = 1/(2*ww) - eps
        print("%6s %12.6f %12.6f %12.6f %12.6f %12.6f %10.5f %10.5f %10.5f" % (
            w, m1, m2, t1, t2, m2-m1,
            t1 - mp.pi*ww, t2 - mp.pi/2, t2 - mp.pi/(2*c)))

for R in ['1500', '1e4', '1e6']:
    table(R)
    print()
print("done")
