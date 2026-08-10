# -*- coding: utf-8 -*-
"""c1_sys.py v2: Newton continuation.
G1: unknowns (a, s1, s2), parameter b (curve through (a0, a0)).
G2: unknowns (b, s1, s2), parameter a (curve through (b0, b0)).
"""
import numpy as np
from c1_lib import sec, y_at, norm_n

def r1_expl(s1, s2, a, b, R):
    n1 = norm_n(s1, a, b, R); n2 = norm_n(s2, a, b, R)
    return s1 ** 2 * (np.sin(s1 * a) / s1) ** 2 / n1 - s2 ** 2 * (np.sin(s2 * a) / s2) ** 2 / n2

def r2_expl(s1, s2, a, b, R):
    n1 = norm_n(s1, a, b, R); n2 = norm_n(s2, a, b, R)
    return s1 ** 2 * y_at(s1, a, b, R, b) ** 2 / n1 - s2 ** 2 * y_at(s2, a, b, R, b) ** 2 / n2

def F1sys(x, b, R):
    a, s1, s2 = x
    return np.array([r1_expl(s1, s2, a, b, R), sec(s1, a, b, R), sec(s2, a, b, R)])

def F2sys(x, a, R):
    b, s1, s2 = x
    return np.array([r2_expl(s1, s2, a, b, R), sec(s1, a, b, R), sec(s2, a, b, R)])

def _J(F, x, *args, h=1e-6):
    F0 = F(x, *args)
    J = np.zeros((3, 3))
    for j in range(3):
        xp = x.copy(); xm = x.copy()
        xp[j] += h; xm[j] -= h
        J[:, j] = (F(xp, *args) - F(xm, *args)) / (2 * h)
    return J

def solve(F, x0, *args, tol=1e-12, maxit=40):
    x = np.array(x0, dtype=float)
    for _ in range(maxit):
        Fv = F(x, *args)
        if np.max(np.abs(Fv)) < tol:
            return x
        J = _J(F, x, *args)
        try:
            dx = np.linalg.solve(J, -Fv)
        except np.linalg.LinAlgError:
            return None
        x = x + dx
        if np.max(np.abs(dx)) < 1e-13:
            break
    return x if np.max(np.abs(F(x, *args))) < 1e-9 else None

def trace_g1(R, n=400, d0=1e-4, bmax=1 - 1e-6):
    a0 = np.arccos(0.25) / np.pi
    b = a0 + d0
    x = solve(F1sys, [a0 + d0 * 0.5, np.pi, 2 * np.pi], b, R)
    pts = [(x[0], b)]
    for i in range(n - 1):
        bn = b + (bmax - b) / (n - i - 1)
        if bn - b < 1e-10:
            break
        x2 = solve(F1sys, [x[0], x[1], x[2]], bn, R)
        if x2 is None or not (0 < x2[0] < bn - 1e-8) or x2[1] >= x2[2]:
            break
        pts.append((x2[0], bn))
        x, b = x2, bn
    return pts

def trace_g2(R, n=400, d0=1e-4, amin=0.001):
    b0 = np.arccos(-0.25) / np.pi
    a = b0 - d0
    x = solve(F2sys, [b0 - d0 * 0.5, np.pi, 2 * np.pi], a, R)
    pts = [(a, x[0])]
    for i in range(n - 1):
        an = a - (a - amin) / (n - i - 1)
        if a - an < 1e-10:
            break
        x2 = solve(F2sys, [x[0], x[1], x[2]], an, R)
        if x2 is None or not (an < x2[0] < 1) or x2[1] >= x2[2]:
            break
        pts.append((an, x2[0]))
        x, a = x2, an
    return pts

if __name__ == "__main__":
    for R in [1.02, 1.05, 1.2, 4.0, 100.0, 1000.0, 1e4]:
        g1 = trace_g1(R)
        g2 = trace_g2(R)
        print(f"R={R}: G1 {len(g1)} pts a[{min(p[0] for p in g1):.6f},{max(p[0] for p in g1):.6f}] b[{min(p[1] for p in g1):.6f},{max(p[1] for p in g1):.6f}]")
        print(f"      G2 {len(g2)} pts a[{min(p[0] for p in g2):.6f},{max(p[0] for p in g2):.6f}] b[{min(p[1] for p in g2):.6f},{max(p[1] for p in g2):.6f}]")
        aL = max(min(p[0] for p in g1), min(p[0] for p in g2))
        aR = min(max(p[0] for p in g1), max(p[0] for p in g2))
        if aL < aR:
            import numpy as np
            def interp(pts, aa):
                xs = np.array([p[0] for p in pts]); ys = np.array([p[1] for p in pts])
                o = np.argsort(xs)
                return np.interp(aa, xs[o], ys[o])
            b1L, b2L = interp(g1, aL), interp(g2, aL)
            b1R, b2R = interp(g1, aR), interp(g2, aR)
            print(f"      common [{aL:.6f},{aR:.6f}]: h(L)={b1L-b2L:+.6f} h(R)={b1R-b2R:+.6f}")
