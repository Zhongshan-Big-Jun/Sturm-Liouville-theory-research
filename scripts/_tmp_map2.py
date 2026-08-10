# -*- coding: utf-8 -*-
"""Map T(a,b)->(a',b')={f>0} for [1,R,1] family: defect fields, Jacobian at fixed point,
and the curves Sigma_a={f(a)=0}, Sigma_b={f(b)=0}."""
import numpy as np
from gap_lib import lams_fast, y_at, norm2

R = 4.0

def pos_interval(blocks, npts=2001):
    s = lams_fast(blocks, 3)
    lam = s**2
    xs = np.linspace(0,1,npts)
    u1 = y_at(blocks, s[0], xs)/np.sqrt(norm2(blocks, s[0]))
    u2 = y_at(blocks, s[1], xs)/np.sqrt(norm2(blocks, s[1]))
    f = lam[0]*u1**2 - lam[1]*u2**2
    pos = f > 0
    nz = np.nonzero(pos)[0]
    if len(nz)==0: return (np.nan, np.nan)
    return (xs[nz[0]], xs[nz[-1]])

def f_at(blocks, x):
    s = lams_fast(blocks, 3)
    lam = s**2
    u1 = y_at(blocks, s[0], np.array([x]))[0]/np.sqrt(norm2(blocks, s[0]))
    u2 = y_at(blocks, s[1], np.array([x]))[0]/np.sqrt(norm2(blocks, s[1]))
    return lam[0]*u1**2 - lam[1]*u2**2

# defect map on a grid: (a,b) -> (a'-a, b'-b)
print("defect map da=a'-a, db=b'-b for [1,R,1] (R=4):")
print("    a     b   ->   a'    b'    da    db")
for a in np.linspace(0.30, 0.47, 6):
    for b in np.linspace(0.53, 0.70, 6):
        if a >= b: continue
        ap, bp = pos_interval([(a,1.0),(b-a,R),(1-b,1.0)])
        if np.isnan(ap): continue
        print(f"{a:.3f} {b:.3f} -> {ap:.4f} {bp:.4f} {ap-a:+.4f} {bp-b:+.4f}")

# Jacobian of T at the fixed point via finite differences
a0, b0 = 0.451485, 0.548515
eps = 1e-5
base = pos_interval([(a0,1.0),(b0-a0,R),(1-b0,1.0)])
Ta = pos_interval([(a0+eps,1.0),(b0-a0-eps,R),(1-b0,1.0)])
Tb = pos_interval([(a0,1.0),(b0+eps-a0,R),(1-b0-eps,1.0)])
J = np.array([[(Ta[0]-base[0])/eps, (Tb[0]-base[0])/eps],
              [(Ta[1]-base[1])/eps, (Tb[1]-base[1])/eps]])
print("\nJacobian of T at fixed point:\n", np.round(J, 4))
print("eigenvalues:", np.round(np.linalg.eigvals(J), 4))

# curves Sigma_a and Sigma_b (f(a)=0 and f(b)=0) on grid; count sign changes
print("\nSigma curves grid scan:")
Na = 40; Nb = 40
aa = np.linspace(0.05, 0.49, Na)
bb = np.linspace(0.51, 0.95, Nb)
za = []; zb = []
for a in aa:
    prev = None
    for b in bb:
        v = f_at([(a,1.0),(b-a,R),(1-b,1.0)], a)
        if prev is not None and prev*v < 0: za.append((round(a,3), round(b,3)))
        prev = v
for b in bb:
    prev = None
    for a in aa:
        v = f_at([(a,1.0),(b-a,R),(1-b,1.0)], b)
        if prev is not None and prev*v < 0: zb.append((round(a,3), round(b,3)))
        prev = v
print("Sigma_a crossings:", za)
print("Sigma_b crossings:", zb)
