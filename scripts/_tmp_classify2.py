# -*- coding: utf-8 -*-
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
    s = lams_fast(blocks, 3)
    return s[1]**2 - s[0]**2

def solve_family(inner, cands):
    sols = []
    for c in cands:
        try:
            sol = least_squares(inner, c, bounds=([0.005,0.505],[0.495,0.995]),
                                xtol=1e-14, ftol=1e-14, gtol=1e-14, max_nfev=400)
        except Exception:
            continue
        x = np.asarray(sol.x, dtype=float)
        res = np.max(np.abs(inner(x)))
        if res < 1e-8:
            if not any(np.linalg.norm(x - np.asarray(s[0])) < 1e-5 for s in sols):
                sols.append((x, res))
    return sols

def sup_inner(ab):
    a, b = ab
    return fvals_blocks([(a,1.0),(b-a,R),(1-b,1.0)], [a, b])

def inf_inner(ab):
    a, b = ab
    return fvals_blocks([(a,R),(b-a,1.0),(1-b,R)], [a, b])

cands = []
for a in np.linspace(0.01, 0.49, 25):
    for b in np.linspace(0.51, 0.99, 25):
        if b > a + 0.02:
            cands.append([a, b])

def report(fam, inner, mk):
    print(f"{fam} family self-consistent solutions (R=4):")
    sols = solve_family(inner, cands)
    for (ab, res) in sols:
        a, b = ab
        blocks = mk(a,b)
        D = D_of(blocks)
        s = lams_fast(blocks, 3)
        xs = np.linspace(a,b,2001)
        u2 = y_at(blocks, s[1], xs)
        z = np.where(np.diff(np.signbit(u2)) != 0)[0]
        x0 = xs[z[0]] if len(z) else None
        print(f"  (a,b)=({a:.6f},{b:.6f}) res={res:.1e} D={D:.6f} x0={x0:.4f}")
    return sols

sols_sup = report("SUP [1,R,1]", sup_inner, lambda a,b: [(a,1.0),(b-a,R),(1-b,1.0)])
sols_inf = report("INF [R,1,R]", inf_inner, lambda a,b: [(a,R),(b-a,1.0),(1-b,R)])

print("constants: rho=1 D=%.6f ; rho=R D=%.6f" % (3*np.pi**2, 3*np.pi**2/R))
best2 = (-1e9, None)
for c in np.linspace(0.001, 0.999, 500):
    D = D_of([(c,1.0),(1-c,R)])
    if D > best2[0]: best2 = (D, c)
print(f"2-block [1,R] max D={best2[0]:.6f} at c={best2[1]:.4f}")

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
        if fam=='SUP' and abs(ap-c) < 0.01 and bp > 0.99: found.append((fam, c, ap, bp))
        if fam=='INF' and ap < 0.01 and abs(bp-c) < 0.01: found.append((fam, c, ap, bp))
print("found:", found if found else "none")

def tau(blocks):
    s = lams_fast(blocks, 3)
    out = []
    for s0 in s:
        M00=1.; M01=0.; M10=0.; M11=1.
        for L, c in blocks:
            w = s0*np.sqrt(c); wL = w*L
            cw = np.cos(wL); sw = np.sin(wL)/w; sw2 = -w*np.sin(wL)
            M00, M01, M10, M11 = cw*M00+sw*M10, cw*M01+sw*M11, sw2*M00+cw*M10, sw2*M01+cw*M11
        out.append(M11)
    return out
sup_blocks = [(0.451485,1.0),(0.09703,R),(0.451485,1.0)]
inf_blocks = [(0.382598,R),(0.234804,1.0),(0.382598,R)]
for lab, bl in [("SUP",sup_blocks),("INF",inf_blocks)]:
    t = tau(bl)
    print(f"{lab}: tau1={t[0]:.6f} tau2={t[1]:.6f} |tau1|={abs(t[0]):.6f} |tau2|={abs(t[1]):.6f}")
