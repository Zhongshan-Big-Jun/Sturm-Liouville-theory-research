# -*- coding: utf-8 -*-
"""Check nu(u)=v(u;u)=u2/u1 at jump vs mu(u)=sqrt(lam1/lam2): monotonicity & crossing."""
import numpy as np
from gap_lib import lams_fast, y_at, norm2

def blocks_of(mode, R, u):
    b = 1-2*u
    return [(u,1.0),(b,R),(u,1.0)] if mode=="SUP" else [(u,R),(b,1.0),(u,R)]

def nu_mu(mode, R, u, npts=90000):
    bl = blocks_of(mode, R, u)
    s = lams_fast(bl, 2, npts=npts)
    lam = s**2
    y1 = y_at(bl, s[0], np.array([u]))[0]
    y2 = y_at(bl, s[1], np.array([u]))[0]
    # v = u2/u1 = (y2/sqrt(N2))/(y1/sqrt(N1))
    n1 = norm2(bl, s[0]); n2 = norm2(bl, s[1])
    nu = (y2/np.sqrt(n2))/(y1/np.sqrt(n1))
    mu = np.sqrt(lam[0]/lam[1])
    return nu, mu, lam

for R in (2.0, 4.0, 100.0, 1000.0):
    for mode in ("SUP","INF"):
        us = np.linspace(0.005, 0.495, 25)
        nus=[]; mus=[]
        for u in us:
            nu,mu,lam = nu_mu(mode, R, float(u))
            nus.append(nu); mus.append(mu)
        nus=np.array(nus); mus=np.array(mus)
        dnu = np.diff(nus); dmu = np.diff(mus)
        print(f"R={R:5.0f} {mode}: nu: {nus[0]:.4f}..{nus[-1]:.4f} (monotone dec: {np.all(dnu<1e-9)});  mu: {mus[0]:.4f}..{mus[-1]:.4f} min={mus.min():.4f} max={mus.max():.4f} (monotone: {np.all(dmu>=-1e-9) or np.all(dmu<=1e-9)})")
        # crossing check
        h = nus - mus
        sg = np.signbit(h); ch = np.nonzero(sg[1:]!=sg[:-1])[0]
        print(f"        crossings of nu-mu on grid: {len(ch)}")
