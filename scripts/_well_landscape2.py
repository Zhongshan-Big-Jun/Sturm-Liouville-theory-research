# -*- coding: utf-8 -*-
"""Well-family landscape exploration v2 (E3 evidence only; NOT a proof).
Fast closed-form well secular solver. D = lam2-lam1 = s2^2 - s1^2."""
import numpy as np
from scipy.optimize import brentq, least_squares

def well_secular(s, a, b, R):
    """Dirichlet secular value for well rho=R on [0,a]u[b,1], 1 on (a,b)."""
    m = np.sqrt(R)
    A = m*s*a; psi = s*(b-a); B = m*s*(1-b)
    return (np.cos(psi)*np.sin(A) + m*np.sin(psi)*np.cos(A))*np.cos(B) \
         + (-np.sin(psi)*np.sin(A)/m + np.cos(psi)*np.cos(A))*np.sin(B)

def well_s(s, a, b, R):
    m = np.sqrt(R)
    A = m*s*a; psi = s*(b-a); B = m*s*(1-b)
    return A, psi, B

def eigs_well(a, b, R, k=2):
    """first k eigenvalues (as LAMBDA values) via bracket+refine."""
    m = np.sqrt(R)
    smax = 2 + k*np.pi*m + 4
    sp = np.linspace(1e-9, smax, 12000)
    d = well_secular(sp, a, b, R)
    signs = np.signbit(d[1:]) != np.signbit(d[:-1])
    idx = np.nonzero(signs)[0]
    out = []
    for i in idx[:k]:
        lo, hi = sp[i], sp[i+1]
        r = brentq(lambda x: well_secular(x, a, b, R), lo, hi, xtol=1e-13, rtol=1e-13)
        out.append(r*r)
    return np.sort(out)[:k]

def y_well(a, b, R, s, x):
    """slope-normalized y (y(0)=0,y'(0)=1) at x."""
    m = np.sqrt(R)
    if x <= a:
        return np.sin(m*s*x)/(m*s)
    if x <= b:
        y0 = np.sin(m*s*a)/(m*s); yp0 = np.cos(m*s*a)
        return y0*np.cos(s*(x-a)) + (yp0/s)*np.sin(s*(x-a))
    # x in (b,1]
    y0 = np.sin(m*s*a)/(m*s); yp0 = np.cos(m*s*a)
    yb = y0*np.cos(s*(b-a)) + (yp0/s)*np.sin(s*(b-a))
    ypb = -y0*s*np.sin(s*(b-a)) + yp0*np.cos(s*(b-a))
    return yb*np.cos(m*s*(x-b)) + (ypb/(m*s))*np.sin(m*s*(x-b))

def norm2_well(a, b, R, s, n=800):
    """int rho y^2 for slope-normalized y."""
    xs = np.linspace(0, 1, n+1)
    ys = np.array([y_well(a, b, R, s, x) for x in xs])
    rho = np.where((xs >= a) & (xs <= b), 1.0, R)
    return np.trapezoid(rho*ys*ys, xs)

def fval(a, b, R, x):
    """f(x)=lam2*u2^2-lam1*u1^2, u_k L2(rho)-normalized."""
    lam1, lam2 = eigs_well(a, b, R)
    s1 = np.sqrt(lam1); s2 = np.sqrt(lam2)
    n1 = norm2_well(a, b, R, s1); n2 = norm2_well(a, b, R, s2)
    y1 = y_well(a, b, R, s1, x); y2 = y_well(a, b, R, s2, x)
    return lam2*y2*y2/n2 - lam1*y1*y1/n1

if __name__ == '__main__':
    import sys
    R = float(sys.argv[1]) if len(sys.argv) > 1 else 4.0
    # Q1: coarse grid
    N = 45
    best = (1e9, None)
    aa = np.linspace(1e-4, 0.998, N)
    for a in aa:
        for b in np.linspace(a, 1.0, N):
            lam = eigs_well(a, b, R)
            D = lam[1]-lam[0]
            if D < best[0]:
                best = (D, (a, b))
    print(f"R={R}: grid min D={best[0]:.6f} at (a,b)=({best[1][0]:.4f},{best[1][1]:.4f}) a+b={best[1][0]+best[1][1]:.4f}")
    # symmetric line
    vs = np.linspace(1e-4, 0.499, 300)
    Ds = []
    for v in vs:
        lam = eigs_well(v, 1-v, R)
        Ds.append(lam[1]-lam[0])
    i = int(np.argmin(Ds))
    print(f"  symmetric-line min: D={Ds[i]:.6f} at v={vs[i]:.4f} (well width {1-2*vs[i]:.4f})")
    # boundary two-block a=0
    bs = np.linspace(1e-5, 1-1e-5, 200)
    Db = []
    for b in bs:
        lam = eigs_well(0.0, b, R)
        Db.append(lam[1]-lam[0])
    print(f"  two-block a=0: min D={min(Db):.6f} at b={bs[int(np.argmin(Db))]:.4f}")
    lam = eigs_well(0.0, 0.0, R)
    print(f"  rho==R: D={lam[1]-lam[0]:.6f} (3pi^2/R={3*np.pi**2/R:.4f})")
    # Q3: critical points
    crits = {}
    for a in np.linspace(0.05, 0.93, 15):
        for b in np.linspace(a+0.05, 0.99, 15):
            def res(ab):
                aa, bb = ab
                return [fval(aa, bb, R, aa), fval(aa, bb, R, bb)]
            sol = least_squares(res, [a, b], bounds=([1e-6, 1e-6], [0.999, 0.999]), xtol=1e-11, ftol=1e-11)
            if sol.cost < 1e-18:
                key = (round(sol.x[0], 5), round(sol.x[1], 5))
                if key not in crits:
                    crits[key] = [float(v) for v in res(sol.x)]
    print(f"  interior critical points: {len(crits)}")
    for k, v in sorted(crits.items()):
        print(f"    (a,b)=({k[0]:.5f},{k[1]:.5f}) a+b={k[0]+k[1]:.5f} resid={v}")
