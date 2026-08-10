# -*- coding: utf-8 -*-
"""Robust eigenvalue solver + careful trace of f_sym(u;R)=0."""
import numpy as np
from scipy.optimize import brentq
from gap_lib import y_at, norm2

def M01(s, blocks):
    """Dirichlet secular value M01."""
    M00=1.0; M01v=0.0; M10=0.0; M11=1.0
    for L,c in blocks:
        w=s*np.sqrt(c); wL=w*L
        cw=np.cos(wL); sw=np.sin(wL)/w; sw2=-w*np.sin(wL)
        M00,M01v,M10,M11 = cw*M00+sw*M10, cw*M01v+sw*M11, sw2*M00+cw*M10, sw2*M01v+cw*M11
    return M01v

def evals_robust(blocks, k=2, smax=None, n=400000):
    """Robust: dense scan then bisect each sign change."""
    # smax heuristic: eigenvalues <= (k+1)*pi*sqrt(max rho)
    if smax is None:
        smax = (k+2)*np.pi*np.sqrt(max(c for _,c in blocks))
    s = np.linspace(1e-9, smax, n)
    d = np.array([M01(x, blocks) for x in s])
    sg = np.signbit(d)
    ch = np.nonzero(sg[1:] != sg[:-1])[0]
    roots = []
    for i in ch[:k]:
        a,b = s[i], s[i+1]
        try:
            r = brentq(lambda x: M01(x, blocks), a, b, xtol=1e-14)
        except ValueError:
            continue
        roots.append(r)
    return np.array(sorted(roots))[:k]

def f_sym(mode, R, u):
    b = 1-2*u
    if mode=="SUP":
        bl = [(u,1.0),(b,R),(u,1.0)]
    else:
        bl = [(u,R),(b,1.0),(u,R)]
    s = evals_robust(bl)
    if len(s) < 2: return None, None, None, None
    lam = s**2
    x = np.array([u])
    u1 = y_at(bl, s[0], x)[0]/np.sqrt(norm2(bl, s[0]))
    u2 = y_at(bl, s[1], x)[0]/np.sqrt(norm2(bl, s[1]))
    return lam[0]*u1**2 - lam[1]*u2**2, s, bl, lam

# First sanity-check the suspicious huge-D cases with the robust solver
print("=== sanity checks ===")
for mode,R,u in [("SUP",1000.0,0.147),("SUP",1000.0,0.148),("INF",10000.0,0.47794),("INF",1000.0,0.46568),("SUP",300.0,0.49)]:
    fv,s,bl,lam = f_sym(mode,R,u)
    if s is None:
        print(f"{mode} R={R} u={u}: solver failed"); continue
    print(f"{mode} R={R:8.0f} u={u:.6f}: f_sym={fv:+.4e} lam1={lam[0]:.6f} lam2={lam[1]:.6f} D={lam[1]-lam[0]:.6f}")

print()
print("=== careful SUP trace ===")
for R in (100.0, 200.0, 300.0, 400.0, 600.0, 1000.0, 3000.0):
    us = np.linspace(0.40, 0.4999, 400)
    vals=[]
    for u in us:
        fv,_,_,_ = f_sym("SUP",R,u)
        vals.append(fv if fv is not None else 0.0)
    vals = np.array(vals)
    sg = np.signbit(vals); ch = np.nonzero(sg[1:]!=sg[:-1])[0]
    roots=[]
    for i in ch:
        a,b = us[i],us[i+1]
        r = brentq(lambda u: f_sym("SUP",R,u)[0], a, b, xtol=1e-13)
        roots.append(r)
    print(f"R={R:6.0f}: SUP zeros in (0.40,0.4999): {['%.7f'%r for r in roots]}")
    if len(roots):
        r0 = roots[0]
        fv,s,bl,lam = f_sym("SUP",R,r0)
        print(f"      -> u*={r0:.8f} lam1={lam[0]:.6f} lam2={lam[1]:.6f} D={lam[1]-lam[0]:.8f}")
