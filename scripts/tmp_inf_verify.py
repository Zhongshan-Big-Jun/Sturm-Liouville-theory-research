# -*- coding: utf-8 -*-
"""Verify candidate critical points at R=1000 INF with robust eigenvalue solver."""
import numpy as np
from scipy.optimize import least_squares
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

def f_vals(blocks, xs, s):
    lam = s**2
    xs = np.atleast_1d(np.asarray(xs,float))
    u1 = y_at(blocks, s[0], xs)/np.sqrt(norm2(blocks, s[0]))
    u2 = y_at(blocks, s[1], xs)/np.sqrt(norm2(blocks, s[1]))
    return lam[0]*u1**2 - lam[1]*u2**2

def resid(ab, R):
    a,b = ab
    bl = [(a,R),(b,1.0),(1-a-b,R)]
    s = evals_vec(bl)
    return f_vals(bl, [a, a+b], s)

R = 1000.0
print("Candidates from coarse search (INF R=1000):")
for a0,b0 in [(0.13812195,0.06407064),(0.46568213,0.06863573),(0.79780743,0.06407063),(0.33480385,0.33039230)]:
    # refine with robust solver
    res = least_squares(lambda ab: resid(ab,R), [a0,b0], xtol=1e-13, ftol=1e-13, gtol=1e-13, max_nfev=100)
    a,b = res.x
    bl = [(a,R),(b,1.0),(1-a-b,R)]
    s = evals_vec(bl)
    fv = f_vals(bl, [a,a+b], s)
    # band check
    xm = np.linspace(a+1e-6, a+b-1e-6, 5); fm = f_vals(bl,xm,s)
    print(f"  refined a={a:.10f} b={b:.10f} c={1-a-b:.10f} |resid|={np.max(np.abs(fv)):.2e} D={s[1]**2-s[0]**2:.8f} fmid>0: {np.all(fm>0)}")

print()
print("=== INF trace (robust): zeros of f_sym(u) for R=100,1000,3000 ===")
from scipy.optimize import brentq
for R in (100.0, 1000.0, 3000.0):
    us = np.linspace(0.005, 0.4999, 500)
    roots=[]
    prev = None; prevu=None
    for u in us:
        b = 1-2*u
        bl = [(u,R),(b,1.0),(u,R)]
        s = evals_vec(bl)
        fv = f_vals(bl, [u], s)[0]
        if prev is not None and np.signbit(prev) != np.signbit(fv):
            r = brentq(lambda uu: f_vals([(uu,R),(1-2*uu,1.0),(uu,R)], [uu], evals_vec([(uu,R),(1-2*uu,1.0),(uu,R)]))[0], prevu, u, xtol=1e-12)
            roots.append(r)
        prev=fv; prevu=u
    print(f"R={R:.0f} INF: {len(roots)} zeros")
    for r0 in roots:
        bl=[(r0,R),(1-2*r0,1.0),(r0,R)]
        s=evals_vec(bl)
        print(f"   u*={r0:.8f} lam1={s[0]**2:.6f} lam2={s[1]**2:.6f} D={s[1]**2-s[0]**2:.8f}")
