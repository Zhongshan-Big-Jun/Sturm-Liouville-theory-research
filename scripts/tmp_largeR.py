# -*- coding: utf-8 -*-
"""Fine search for large R: symmetric region + Hessian classification of all valid critical points."""
import numpy as np
from scipy.optimize import least_squares
from gap_lib import lams_fast, y_at, norm2

def s_of(blocks, npts=1500):
    return lams_fast(blocks, 2, npts=npts)

def f_at(blocks, x, s=None, npts=1500):
    if s is None:
        s = s_of(blocks, npts)
    lam = s**2
    x = np.atleast_1d(np.asarray(x, dtype=float))
    x = np.clip(x, 1e-12, 1-1e-12)
    u1 = y_at(blocks, s[0], x)/np.sqrt(norm2(blocks, s[0]))
    u2 = y_at(blocks, s[1], x)/np.sqrt(norm2(blocks, s[1]))
    return lam[0]*u1**2 - lam[1]*u2**2, s

def make_blocks(mode, R, a, b):
    c = 1.0 - a - b
    if mode == "SUP":
        return [(a,1.0),(b,R),(c,1.0)]
    return [(a,R),(b,1.0),(c,R)]

def resid(mode, R, ab):
    a, b = ab
    if not (1e-6 < a and 1e-6 < b and a+b < 1-1e-6):
        return np.array([1e3, 1e3])
    bl = make_blocks(mode, R, a, b)
    fv, s = f_at(bl, [a, a+b])
    return fv

def band_ok(mode, R, a, b, s):
    bl = make_blocks(mode, R, a, b)
    xm = np.linspace(a+1e-5, a+b-1e-5, 5)
    fvm, _ = f_at(bl, xm, s=s)
    xo = np.array([max(1e-6,(a-1e-4)/2), min(1-1e-6,(1+a+b)/2)])
    fvo, _ = f_at(bl, xo, s=s)
    return bool(np.all(fvm > 0) and np.all(fvo < 0))

def hess(mode, R, a, b, h=5e-5):
    D = lambda x,y: s_of(make_blocks(mode,R,x,y))[1]**2 - s_of(make_blocks(mode,R,x,y))[0]**2
    f00 = D(a,b)
    faa = (D(a+h,b)-2*f00+D(a-h,b))/h**2
    fbb = (D(a,b+h)-2*f00+D(a,b-h))/h**2
    fab = (D(a+h,b+h)-D(a+h,b)-D(a,b+h)+f00)/h**2
    return np.array([[faa,fab],[fab,fbb]]), f00

for R in (100.0, 1000.0, 10000.0):
    for mode in ("SUP","INF"):
        found = []
        # near-symmetric seeds
        seeds = [(0.5-eps, 2*eps) for eps in (0.02,0.01,0.005,0.0025,0.001,0.0005)]
        seeds += [(a, 1-2*a) for a in (0.45,0.47,0.49,0.495)]
        # full grid coarse
        for a in np.linspace(0.05,0.95,16):
            for b in np.linspace(0.0005,0.9,14):
                if not (0.01 < a+b < 0.99): continue
                seeds.append((a,b))
        for seed in seeds:
            a0,b0 = seed
            if not (1e-6 < a0 and 1e-6 < b0 and a0+b0 < 1-1e-6): continue
            res = least_squares(lambda ab: resid(mode,R,ab), [a0,b0], xtol=1e-11, ftol=1e-11, gtol=1e-11, max_nfev=150)
            a2,b2 = res.x
            if not (1e-5 < a2 and 1e-5 < b2 and a2+b2 < 1-1e-5): continue
            r = np.linalg.norm(res.fun)
            if r > 1e-5: continue
            bl = make_blocks(mode,R,a2,b2); s = s_of(bl)
            ok = band_ok(mode,R,a2,b2,s)
            D = s[1]**2-s[0]**2
            entry=(round(a2,7),round(b2,7))
            if not any(abs(entry[0]-t[0])<2e-5 and abs(entry[1]-t[1])<2e-5 for t in found):
                found.append((a2,b2,r,ok,D))
        valid = [(a,b,r,ok,D) for a,b,r,ok,D in found if ok]
        print(f"R={R:.0f} {mode}: valid critical pts = {len(valid)}")
        for a,b,r,ok,D in sorted(valid):
            H, Dv = hess(mode,R,a,b)
            ev = np.linalg.eigvalsh(H)
            kind = ("MAX" if ev[0]<0 and ev[1]<0 else "MIN" if ev[0]>0 and ev[1]>0 else "SADDLE")
            print(f"   a={a:.8f} b={b:.8f} c={1-a-b:.8f} D={D:.8f} hess_eig=({ev[0]:+.1f},{ev[1]:+.1f}) {kind}")
