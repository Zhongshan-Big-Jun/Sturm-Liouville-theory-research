# -*- coding: utf-8 -*-
"""Agent C: subclaim 2, fast analytic version."""
import numpy as np
from scipy.optimize import brentq

def M_block(L, c, s):
    w = s*np.sqrt(c); q = np.sqrt(c)
    return np.array([[np.cos(w*L), np.sin(w*L)/q], [-q*np.sin(w*L), np.cos(w*L)]])

def blocks_of(u, R, sup):
    c1, c2 = (1.0, R) if sup else (R, 1.0)
    return [(u, c1), (1-2*u, c2), (u, c1)]

def M01_blocks(blocks, s):
    M = np.eye(2)
    for L, c in blocks:
        M = M_block(L, c, s) @ M
    return M[0,1]

def lams(blocks, k=3, smax=None):
    if smax is None:
        smax = np.pi*np.sqrt(max(c for _, c in blocks))*(k+2)+10
    s = np.linspace(1e-9, smax, 120000)
    d = np.array([M01_blocks(blocks, x) for x in s])
    sg = np.signbit(d[1:]) != np.signbit(d[:-1])
    idx = np.nonzero(sg)[0]
    roots = []
    for i in idx[:k]:
        roots.append(brentq(lambda x: M01_blocks(blocks, x), s[i], s[i+1]))
    return np.array(roots)

def norm2(blocks, s):
    xs = [0.0]
    for L, c in blocks: xs.append(xs[-1]+L)
    nrm = 0.0
    M = np.eye(2)
    for i, (L, c) in enumerate(blocks):
        w = s*np.sqrt(c)
        y0 = M[0,1]; yp0 = M[1,1]
        A, B = y0, yp0/w
        Icc = 0.5*(L + np.sin(2*w*L)/(2*w)); Iss = 0.5*(L - np.sin(2*w*L)/(2*w)); Ics = np.sin(w*L)**2/(2*w)
        nrm += c*(A*A*Icc + B*B*Iss + 2*A*B*Ics)
        M = M_block(L, c, s) @ M
    return nrm

def y_at(blocks, s, x):
    xs = [0.0]
    for L, c in blocks: xs.append(xs[-1]+L)
    bi = max(i for i in range(len(xs)-1) if xs[i] <= x)
    M = np.eye(2)
    for i in range(bi):
        M = M_block(blocks[i][0], blocks[i][1], s) @ M
    L, c = blocks[bi]; d = x - xs[bi]
    M = M_block(d, c, s) @ M
    return M[0,1]

def f_at(u, R, sup):
    blocks = blocks_of(u, R, sup)
    s = lams(blocks, 2)
    n = np.array([np.sqrt(norm2(blocks, sk)) for sk in s])
    y = np.array([y_at(blocks, s[0], u), y_at(blocks, s[1], u)])
    U = y/n
    return s[0]**2*U[0]**2 - s[1]**2*U[1]**2

def ustar(R, sup, npts=300):
    uu = np.linspace(1e-5, 0.5-1e-5, npts)
    ff = np.array([f_at(u, R, sup) for u in uu])
    sg = np.signbit(ff)
    idx = np.nonzero(sg[1:] != sg[:-1])[0]
    zeros = []
    for i in idx:
        zeros.append(brentq(lambda u: f_at(u, R, sup), uu[i], uu[i+1]))
    return zeros, ff[0], ff[-1]

PI2 = np.pi**2
print("R, SUP zeros-of-f, D(u*), D-3pi^2 | INF zeros-of-f, D(u*), D*R, 3pi^2/R-D")
for R in [1.02, 1.05, 1.2, 1.5, 2.0, 4.0, 10.0, 100.0, 1e4]:
    zs, f0, f1 = ustar(R, True, 300)
    zt, g0, g1 = ustar(R, False, 300)
    def Dof(blocks):
        s = lams(blocks, 2); return s[1]**2 - s[0]**2
    if len(zs) == 0: print(f"R={R}: SUP no zero f0={f0:.2e} f1={f1:.2e}"); continue
    us = zs[0]
    Dsup = Dof(blocks_of(us, R, True))
    ui = zt[0]
    Dinf = Dof(blocks_of(ui, R, False))
    print(f"R={R:8.1f}: SUP z={len(zs)} u*={us:.7f} D={Dsup:.8f} D-3pi^2={Dsup-3*PI2:+.6e} | INF z={len(zt)} u*={ui:.7f} D={Dinf:.8f} D*R={Dinf*R:.8f} 3pi^2/R-D={3*PI2/R-Dinf:+.6e}")
