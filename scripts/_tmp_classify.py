# -*- coding: utf-8 -*-
"""Comprehensive classification of self-consistent configs for D=lam2-lam1, 1<=rho<=R.
1) SUP family [1,R,1]_{a,b}: solve f(a)=f(b)=0. 2) INF family [R,1,R]_{a,b}. 
3) 1-jump self-consistent. 4) constants. 5) tau ratios, non-degeneracy. 6) D(u) unimodality."""
import numpy as np
from scipy.optimize import least_squares
from gap_lib import lams_fast, y_at, norm2

R = 4.0

def fvals_blocks(blocks, pts):
    s = lams_fast(blocks, 3)
    lam = s**2
    out = []
    for k in (0,1):
        y = y_at(blocks, s[k], np.array(pts))
        u = y/np.sqrt(norm2(blocks, s[k]))
        out.append(u)
    u1, u2 = out
    return lam[0]*u1**2 - lam[1]*u2**2

def D_of(blocks):
    return lams_fast(blocks, 3)[1]**2 - lams_fast(blocks, 3)[0]**2

def solve_family(inner, cands):
    """inner(a,b) -> [f(a), f(b)] for the family; refine all candidates."""
    sols = []
    for c in cands:
        sol = least_squares(inner, c, bounds=([0.005,0.505],[0.495,0.995]),
                            xtol=1e-14, ftol=1e-14, gtol=1e-14, max_nfev=400)
        res = np.max(np.abs(inner(sol.x)))
        if res < 1e-8:
            # dedupe
            if not any(np.linalg.norm(sol.x-s) < 1e-5 for s in sols):
                sols.append((sol.x, res))
    return sols

# SUP family
def sup_inner(ab):
    a, b = ab
    return fvals_blocks([(a,1.0),(b-a,R),(1-b,1.0)], [a, b])
# INF family
def inf_inner(ab):
    a, b = ab
    return fvals_blocks([(a,R),(b-a,1.0),(1-b,R)], [a, b])

# candidate grid
cands = []
for a in np.linspace(0.01, 0.49, 25):
    for b in np.linspace(0.51, 0.99, 25):
        if b > a + 0.02:
            cands.append([a, b])
print("SUP family self-consistent solutions (R=4):")
for (ab, res) in solve_family(sup_inner, cands):
    a, b = ab
    D = D_of([(a,1.0),(b-a,R),(1-b,1.0)])
    s = lams_fast([(a,1.0),(b-a,R),(1-b,1.0)], 3)
    x0 = None
    xs = np.linspace(a,b,2001)
    u2 = y_at([(a,1.0),(b-a,R),(1-b,1.0)], s[1], xs)
    z = np.where(np.diff(np.signbit(u2)) != 0)[0]
    if len(z): x0 = xs[z[0]]
    print(f"  (a,b)=({a:.6f},{b:.6f}) res={res:.1e} D={D:.6f} x0={x0:.4f}")
print("INF family self-consistent solutions (R=4):")
for (ab, res) in solve_family(inf_inner, cands):
    a, b = ab
    D = D_of([(a,R),(b-a,1.0),(1-b,R)])
    s = lams_fast([(a,R),(b-a,1.0),(1-b,R)], 3)
    xs = np.linspace(a,b,2001)
    u2 = y_at([(a,R),(b-a,1.0),(1-b,R)], s[1], xs)
    z = np.where(np.diff(np.signbit(u2)) != 0)[0]
    x0 = xs[z[0]] if len(z) else None
    print(f"  (a,b)=({a:.6f},{b:.6f}) res={res:.1e} D={D:.6f} x0={x0:.4f}")

# constants and 2-block family scan
print("constants: rho=1 D=%.6f ; rho=R D=%.6f" % (3*np.pi**2, 3*np.pi**2/R))
best2 = (-1e9, None)
for c in np.linspace(0.001, 0.999, 500):
    D = D_of([(c,1.0),(1-c,R)])
    if D > best2[0]: best2 = (D, c)
print(f"2-block [1,R] max D={best2[0]:.6f} at c={best2[1]:.4f}")

# 1-jump self-consistency (SUP-type: need a'=c and b'=1; INF-type: a'=0 and b'=c)
def pos_int(blocks, npts=4001):
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
print("1-jump self-consistent search:")
found = []
for c in np.linspace(0.02, 0.98, 97):
    for fam in ('SUP','INF'):
        blocks = [(c,1.0),(1-c,R)] if fam=='SUP' else [(c,R),(1-c,1.0)]
        ap, bp = pos_int(blocks)
        # SUP-type fixed: a'=c, b'=1 ; INF-type: a'=0, b'=c
        if fam=='SUP' and abs(ap-c) < 0.01 and bp > 0.99: found.append((fam, c, ap, bp))
        if fam=='INF' and ap < 0.01 and abs(bp-c) < 0.01: found.append((fam, c, ap, bp))
print("found:", found if found else "none")

# tau ratios at SUP and INF self-consistent points
def tau(blocks):
    s = lams_fast(blocks, 3)
    # unnormalized y with y'(0)=1: slope at 1 from TM
    M00=1.; M01=0.; M10=0.; M11=1.
    for L, c in blocks:
        w = s*np.sqrt(c); wL = w*L
        cw = np.cos(wL); sw = np.sin(wL)/w; sw2 = -w*np.sin(wL)
        M00, M01, M10, M11 = cw*M00+sw*M10, cw*M01+sw*M11, sw2*M00+cw*M10, sw2*M01+cw*M11
    # y(1)=0, y'(1) = M10*0 + M11*1 = M11
    return M11  # y'(1)/y'(0)
sup_blocks = [(0.451485,1.0),(0.548515-0.451485,R),(1-0.548515,1.0)]
inf_blocks = [(0.382598,R),(0.617402-0.382598,1.0),(1-0.617402,R)]
for lab, bl in [("SUP",sup_blocks),("INF",inf_blocks)]:
    s = lams_fast(bl, 3)
    t1, t2 = tau(bl)
    print(f"{lab}: tau1={t1[0]:.6f} tau2={t2[0]:.6f} |tau1|={abs(t1[0]):.6f} |tau2|={abs(t2[0]):.6f}")
