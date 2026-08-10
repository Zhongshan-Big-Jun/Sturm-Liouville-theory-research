# -*- coding: utf-8 -*-
"""Vectorized robust eigenvalue solver + careful trace of f_sym(u;R)=0."""
import numpy as np
from scipy.optimize import brentq
from gap_lib import y_at, norm2

def M01_vec(s, blocks):
    s = np.atleast_1d(s)
    M00=np.ones(len(s)); M01v=np.zeros(len(s)); M10=np.zeros(len(s)); M11=np.ones(len(s))
    for L,c in blocks:
        w=s*np.sqrt(c); wL=w*L
        cw=np.cos(wL); sw=np.sin(wL)/w; sw2=-w*np.sin(wL)
        M00,M01v,M10,M11 = cw*M00+sw*M10, cw*M01v+sw*M11, sw2*M00+cw*M10, sw2*M01v+cw*M11
    return M01v

def evals_vec(blocks, k=2, n=60000):
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

def f_sym(mode, R, u, n=60000):
    b = 1-2*u
    bl = [(u,1.0),(b,R),(u,1.0)] if mode=="SUP" else [(u,R),(b,1.0),(u,R)]
    s = evals_vec(bl, 2, n)
    if len(s) < 2: return None, None, None, None
    lam = s**2
    u1 = y_at(bl, s[0], np.array([u]))[0]/np.sqrt(norm2(bl, s[0]))
    u2 = y_at(bl, s[1], np.array([u]))[0]/np.sqrt(norm2(bl, s[1]))
    return lam[0]*u1**2 - lam[1]*u2**2, s, bl, lam

print("=== sanity checks (vectorized) ===")
for mode,R,u in [("SUP",1000.0,0.147),("SUP",1000.0,0.148),("INF",10000.0,0.47794),("INF",1000.0,0.46568),("SUP",300.0,0.49),("SUP",1000.0,0.4885)]:
    fv,s,bl,lam = f_sym(mode,R,u)
    if s is None: print(f"{mode} R={R} u={u}: solver failed"); continue
    print(f"{mode} R={R:8.0f} u={u:.6f}: f_sym={fv:+.4e} lam1={lam[0]:.6f} lam2={lam[1]:.6f} D={lam[1]-lam[0]:.6f}")

print()
print("=== careful SUP trace near u~0.49 ===")
for R in (100.0, 200.0, 300.0, 400.0, 600.0, 1000.0, 2000.0, 3000.0):
    us = np.linspace(0.44, 0.49999, 250)
    vals = np.array([f_sym("SUP",R,u)[0] if f_sym("SUP",R,u)[0] is not None else 0.0 for u in us])
    sg = np.signbit(vals); ch = np.nonzero(sg[1:]!=sg[:-1])[0]
    roots=[]
    for i in ch:
        a,b = us[i],us[i+1]
        r = brentq(lambda u: f_sym("SUP",R,u)[0], a, b, xtol=1e-12)
        roots.append(r)
    print(f"R={R:6.0f}: zeros in (0.44,0.49999): {['%.7f'%r for r in roots]}")
    for r0 in roots:
        fv,s,bl,lam = f_sym("SUP",R,r0)
        print(f"      u*={r0:.8f} lam1={lam[0]:.6f} lam2={lam[1]:.6f} D={lam[1]-lam[0]:.8f}")
