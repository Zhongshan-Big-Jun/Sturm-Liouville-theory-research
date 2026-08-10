# -*- coding: utf-8 -*-
"""Fine shape of F(u)=f_sym(u), D_sym(u); exact u*, D*; margins vs 3pi^2, 3pi^2/R."""
import numpy as np
from scipy.optimize import brentq
from gap_lib import lams_fast, y_at, norm2

def blocks_of(mode, R, u):
    b = 1-2*u
    return [(u,1.0),(b,R),(u,1.0)] if mode=="SUP" else [(u,R),(b,1.0),(u,R)]

def D_and_F(mode, R, u, npts=90000):
    bl = blocks_of(mode, R, u)
    s = lams_fast(bl, 2, npts=npts)
    lam = s**2
    u1 = y_at(bl, s[0], np.array([u]))[0]/np.sqrt(norm2(bl, s[0]))
    u2 = y_at(bl, s[1], np.array([u]))[0]/np.sqrt(norm2(bl, s[1]))
    return lam[1]-lam[0], lam[0]*u1**2 - lam[1]*u2**2, lam

t3 = 3*np.pi**2
for mode in ("SUP","INF"):
    print(f"========== {mode} ==========")
    for R in (1.5, 2.0, 4.0, 10.0, 100.0, 1000.0):
        us = np.linspace(0.002, 0.498, 120)
        Fs = []; Ds = []
        for u in us:
            D,F,lam = D_and_F(mode, R, float(u))
            Fs.append(F); Ds.append(D)
        Fs=np.array(Fs); Ds=np.array(Ds)
        # sign changes of F
        sg = np.signbit(Fs); ch = np.nonzero(sg[1:]!=sg[:-1])[0]
        roots=[]
        for i in ch:
            r = brentq(lambda u: D_and_F(mode,R,u)[1], us[i], us[i+1], xtol=1e-13)
            roots.append(r)
        # global max/min of D over grid
        iD = int(np.argmax(Ds)) if mode=="SUP" else int(np.argmin(Ds))
        print(f"R={R:6.0f}: F zeros at u* = {['%.6f'%r for r in roots]}")
        if roots:
            u0 = roots[0]
            D0,_,lam0 = D_and_F(mode, R, u0)
            print(f"        u*={u0:.9f}  D*={D0:.9f}  lam1={lam0[0]:.6f} lam2={lam0[1]:.6f}")
            if mode=="SUP":
                print(f"        D*-3pi^2 = {D0-t3:+.6f}   (needs >0)")
            else:
                print(f"        3pi^2/R - D* = {t3/R-D0:+.6f}   (needs >0)")
        print(f"        grid: D min={Ds.min():.5f} max={Ds.max():.5f}; F min={Fs.min():+.4f} F max={Fs.max():+.4f}")
