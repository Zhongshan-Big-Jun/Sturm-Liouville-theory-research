# -*- coding: utf-8 -*-
"""Well-family landscape exploration (E3 evidence only; not a proof).
Q1: grid min location/value; Q2: boundary two-block; Q3: critical-point search;
Q4: fixed-point map T(a,b)=(zeros of f)."""
import numpy as np
from scipy.optimize import brentq, least_squares
from gap_lib import lams_fast, y_at, norm2, blocks_xs

def well_blocks(a, b, R):
    return [(a, R), (b-a, 1.0), (1-b, R)]

def eigs_well(a, b, R, k=2):
    return lams_fast(well_blocks(a, b, R), k)

def fval(a, b, R, x, npts=20000):
    """f(x)=lam2*u2(x)^2-lam1*u1(x)^2 with u_k L2(rho)-normalized."""
    blocks = well_blocks(a, b, R)
    s1, s2 = np.sqrt(eigs_well(a, b, R, 2))
    n1 = norm2(blocks, s1); n2 = norm2(blocks, s2)
    y1 = y_at(blocks, s1, np.array([x]))[0]
    y2 = y_at(blocks, s2, np.array([x]))[0]
    return (s2**2)*(y2*y2)/n2 - (s1**2)*(y1*y1)/n1

def zeros_of_f(a, b, R, ngrid=4001):
    """Find zeros of f in (0,1) by sign changes; return list."""
    xs = np.linspace(1e-9, 1-1e-9, ngrid)
    fv = np.array([fval(a, b, R, x) for x in xs])
    out = []
    for i in range(len(xs)-1):
        if fv[i]*fv[i+1] < 0:
            r = brentq(lambda x: fval(a, b, R, x), xs[i], xs[i+1], xtol=1e-12)
            out.append(r)
    return out

if __name__ == '__main__':
    import sys
    R = float(sys.argv[1]) if len(sys.argv) > 1 else 4.0
    # Q1: grid
    N = 60
    best = (1e9, None)
    grid = {}
    aa = np.linspace(0, 0.999, N)
    for ai, a in enumerate(aa):
        for b in np.linspace(a, 1.0, N):
            lam = eigs_well(a, b, R)
            D = lam[1]-lam[0]
            grid[(a, b)] = D
            if D < best[0]:
                best = (D, (a, b))
    print(f"R={R}: grid min D={best[0]:.6f} at (a,b)=({best[1][0]:.4f},{best[1][1]:.4f})  a+b={best[1][0]+best[1][1]:.4f}")
    # symmetric line scan
    vs = np.linspace(0.001, 0.499, 200)
    Ds = []
    for v in vs:
        lam = eigs_well(v, 1-v, R)
        Ds.append(lam[1]-lam[0])
    i = int(np.argmin(Ds))
    print(f"  symmetric-line min: D={Ds[i]:.6f} at v={vs[i]:.4f} (well width {1-2*vs[i]:.4f})")
    # Q2: boundary two-block D(0,b)
    bs = np.linspace(1e-6, 1-1e-6, 300)
    Db = []
    for b in bs:
        lam = eigs_well(0.0, b, R)
        Db.append(lam[1]-lam[0])
    print(f"  two-block a=0: min D={min(Db):.6f} at b={bs[int(np.argmin(Db))]:.4f};  D(0,0)~3pi^2/R={3*np.pi**2/R:.4f}")
    # constant R
    lam = eigs_well(0.0, 0.0, R)
    print(f"  rho==R: D={lam[1]-lam[0]:.6f} (3pi^2/R={3*np.pi**2/R:.4f})")
    # Q3: critical point search via f(a)=f(b)=0 with Newton from grid seeds
    crits = {}
    for a in np.linspace(0.05, 0.95, 19):
        for b in np.linspace(a+0.05, 0.999, 19):
            def res(ab):
                aa, bb = ab
                return [fval(aa, bb, R, aa), fval(aa, bb, R, bb)]
            sol = least_squares(res, [a, b], bounds=([1e-6, 1e-6], [0.999, 0.999]), xtol=1e-12, ftol=1e-12)
            if sol.cost < 1e-20:
                key = (round(sol.x[0], 6), round(sol.x[1], 6))
                if key not in crits:
                    crits[key] = res(sol.x)
    print(f"  interior critical points found: {len(crits)}")
    for k, v in sorted(crits.items()):
        print(f"    (a,b)=({k[0]:.6f},{k[1]:.6f}) a+b={k[0]+k[1]:.6f} resid={v}")
