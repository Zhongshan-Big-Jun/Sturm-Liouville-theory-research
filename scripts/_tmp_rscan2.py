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

def solve_fam(inner):
    best = []
    for a in np.linspace(0.03, 0.47, 15):
        for b in np.linspace(0.53, 0.97, 15):
            if b > a + 0.05:
                r = np.max(np.abs(inner([a, b])))
                best.append((r, a, b))
    best.sort(key=lambda t: t[0])
    sols = []
    for (r0, a0, b0) in best[:4]:
        try:
            sol = least_squares(inner, [a0,b0], bounds=([0.005,0.505],[0.495,0.995]),
                                xtol=1e-13, ftol=1e-13, gtol=1e-13, max_nfev=300)
        except Exception:
            continue
        x = np.asarray(sol.x, dtype=float)
        res = np.max(np.abs(inner(x)))
        if res < 1e-7:
            if not any(np.linalg.norm(x - np.asarray(s[0])) < 1e-4 for s in sols):
                sols.append((x, res))
    return sols

def run(R):
    def sup_inner(ab):
        a, b = ab
        return fvals_blocks([(a,1.0),(b-a,R),(1-b,1.0)], [a, b])
    def inf_inner(ab):
        a, b = ab
        return fvals_blocks([(a,R),(b-a,1.0),(1-b,R)], [a, b])
    out = []
    for lab, inner, mk in (("SUP", sup_inner, lambda a,b:[(a,1.0),(b-a,R),(1-b,1.0)]),
                           ("INF", inf_inner, lambda a,b:[(a,R),(b-a,1.0),(1-b,R)])):
        sols = solve_fam(inner)
        for (ab, res) in sols:
            a, b = ab
            bl = mk(a,b)
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
