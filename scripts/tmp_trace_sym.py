# -*- coding: utf-8 -*-
"""Trace symmetric critical points vs R: does f_sym(u;R)=0 have a solution? For SUP and INF."""
import numpy as np
from scipy.optimize import brentq, least_squares
from gap_lib import lams_fast, y_at, norm2

def s_of(blocks, npts=1500):
    return lams_fast(blocks, 2, npts=npts)

def f_sym_val(mode, R, u):
    b = 1-2*u
    if mode == "SUP":
        bl = [(u,1.0),(b,R),(u,1.0)]
    else:
        bl = [(u,R),(b,1.0),(u,R)]
    s = s_of(bl)
    lam = s**2
    u1 = y_at(bl, s[0], np.array([u]))[0]/np.sqrt(norm2(bl, s[0]))
    u2 = y_at(bl, s[1], np.array([u]))[0]/np.sqrt(norm2(bl, s[1]))
    return lam[0]*u1**2 - lam[1]*u2**2, s, bl

for mode in ("SUP","INF"):
    print(f"==== {mode}: trace symmetric critical point u*(R) ====")
    for R in (1.1,1.5,2,4,10,30,100,300,1000,3000,10000,30000,100000):
        # scan sign of f_sym on u grid
        us = np.linspace(0.01, 0.49, 200)
        vals = []
        for u in us:
            fv,_,_ = f_sym_val(mode,R,u)
            vals.append(fv)
        vals = np.array(vals)
        # count sign changes
        sg = np.signbit(vals)
        ch = np.nonzero(sg[1:] != sg[:-1])[0]
        roots = []
        for i in ch:
            a,b = us[i],us[i+1]
            try:
                r = brentq(lambda u: f_sym_val(mode,R,u)[0], a, b, xtol=1e-13)
                roots.append(r)
            except ValueError: pass
        if len(roots) >= 1:
            # refine best (largest |D| among roots - pick each)
            info=[]
            for r0 in roots:
                fv,s,bl = f_sym_val(mode,R,r0)
                info.append((r0, s[1]**2-s[0]**2))
            for r0,D in info:
                print(f"  R={R:8.0f}: u*={r0:.8f}  D={D:.8f}")
        else:
            # print sign pattern summary
            print(f"  R={R:8.0f}: NO zero of f_sym.  vals[0]={vals[0]:+.4e} vals[-1]={vals[-1]:+.4e}  (scan min {vals.min():+.2e} max {vals.max():+.2e})")
