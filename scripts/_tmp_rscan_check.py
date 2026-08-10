# -*- coding: utf-8 -*-
import numpy as np
from scipy.optimize import least_squares
from gap_lib import lams_fast, y_at, norm2

def fvals_blocks(blocks, pts):
    s = lams_fast(blocks, 3)
    lam = s**2
    u1 = y_at(blocks, s[0], np.array(pts))/np.sqrt(norm2(blocks, s[0]))
    u2 = y_at(blocks, s[1], np.array(pts))/np.sqrt(norm2(blocks, s[1]))
    return lam[0]*u1**2 - lam[1]*u2**2

def D_of(blocks):
    s = lams_fast(blocks, 3)
    return s[1]**2 - s[0]**2

def solve_fam(inner, cands):
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

def run(R):
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
    ss = solve_fam(sup_inner, cands)
    si = solve_fam(inf_inner, cands)
    out = []
    for lab, sols in (("SUP", ss), ("INF", si)):
        for (ab, res) in sols:
            a, b = ab
            bl = [(a,1.0),(b-a,R),(1-b,1.0)] if lab=="SUP" else [(a,R),(b-a,1.0),(1-b,R)]
            D = D_of(bl)
            s = lams_fast(bl, 3)
            xs = np.linspace(a,b,2001)
            u2 = y_at(bl, s[1], xs)
            z = np.where(np.diff(np.signbit(u2)) != 0)[0]
            x0 = xs[z[0]] if len(z) else None
            out.append((lab, a, b, res, D, x0))
    return out

for R in (1.5, 2.0, 3.0, 4.0, 10.0):
    for lab, a, b, res, D, x0 in run(R):
        print(f"R={R} {lab}: a={a:.6f} b={b:.6f} 1-b={1-b:.6f} res={res:.1e} D={D:.6f} x0={x0:.4f}")
