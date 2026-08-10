# -*- coding: utf-8 -*-
"""R=1000 INF: robust check of z(u)-u with high-res vectorized solver."""
import numpy as np
from gap_lib import y_at, norm2

def M01_vec(s, blocks):
    s = np.atleast_1d(s)
    M00=np.ones(len(s)); M01v=np.zeros(len(s)); M10=np.zeros(len(s)); M11=np.ones(len(s))
    for L,c in blocks:
        w=s*np.sqrt(c); wL=w*L
        cw=np.cos(wL); sw=np.sin(wL)/w; sw2=-w*np.sin(wL)
        M00,M01v,M10,M11 = cw*M00+sw*M10, cw*M01v+sw*M11, sw2*M00+cw*M10, sw2*M01v+cw*M11
    return M01v

def evals_vec(blocks, k=2, n=90000):
    smax = (k+2)*np.pi*np.sqrt(max(c for _,c in blocks))
    s = np.linspace(1e-9, smax, n)
    d = M01_vec(s, blocks)
    sg = np.signbit(d)
    ch = np.nonzero(sg[1:] != sg[:-1])[0]
    roots = []
    for i in ch[:k]:
        a,b = s[i], s[i+1]
        for _ in range(4):
            mid = np.linspace(a,b,200)
            dm = M01_vec(mid, blocks)
            sgm = np.signbit(dm)
            c2 = np.nonzero(sgm[1:]!=sgm[:-1])[0]
            if len(c2)==0: break
            a,b = mid[c2[0]], mid[c2[0]+1]
        roots.append(0.5*(a+b))
    return np.array(sorted(roots))[:k]

def f_of_x(mode, R, u, xs):
    b = 1-2*u
    bl = [(u,1.0),(b,R),(u,1.0)] if mode=="SUP" else [(u,R),(b,1.0),(u,R)]
    s = evals_vec(bl)
    lam = s**2
    xs = np.atleast_1d(np.asarray(xs,float))
    u1 = y_at(bl, s[0], xs)/np.sqrt(norm2(bl, s[0]))
    u2 = y_at(bl, s[1], xs)/np.sqrt(norm2(bl, s[1]))
    return lam[0]*u1**2 - lam[1]*u2**2, s, bl

def z_of(mode, R, u):
    lo, hi = 1e-8, 0.5
    for _ in range(55):
        mid = 0.5*(lo+hi)
        fm,_,_ = f_of_x(mode, R, u, [mid])
        if fm > 0: hi = mid
        else: lo = mid
    return 0.5*(lo+hi)

R = 1000.0
for mode in ("SUP","INF"):
    print(f"==== {mode} R=1000 (robust) ====")
    us = np.linspace(0.005, 0.495, 60)
    prev = None; ok=True; worst=(0,0)
    zs = []
    for u in us:
        z = z_of(mode, R, float(u))
        d = z - u
        zs.append((u,z,d))
        if prev is not None and d > prev + 1e-9:
            ok = False
            worst = (u, d-prev)
        prev = d
    print(f"  strictly decreasing: {ok}  worst increment {worst[1]:.3e} at u={worst[0]:.4f}")
    # print table around where nonmonotonic if any
    for u,z,d in zs:
        print(f"  u={u:.4f} z={z:.6f} z-u={d:+.6f}")
