# -*- coding: utf-8 -*-
"""num_gapn1_landscape.py: global landscape of D(a,b) over SUP/INF families for several R.
Checks (i) is the symmetric critical config the global argmax/argmin, (ii) boundary values,
(iii) phase-transition for small R (off-center maximizers?)."""
import numpy as np
from scipy.optimize import least_squares
from gap_lib import lams_fast, y_at, norm2

def D_of(blocks, npts=4000):
    s = lams_fast(blocks, 2, npts=npts)
    return s[1]**2 - s[0]**2

def make_blocks(mode, R, a, b):
    if mode == "SUP":
        return [(a,1.0),(b-a,R),(1-b,1.0)]
    return [(a,R),(b-a,1.0),(1-b,R)]

def f_at(blocks, x):
    s = lams_fast(blocks, 2)
    lam = s**2
    u1 = y_at(blocks, s[0], np.array([x]))[0]/np.sqrt(norm2(blocks, s[0]))
    u2 = y_at(blocks, s[1], np.array([x]))[0]/np.sqrt(norm2(blocks, s[1]))
    return lam[0]*u1*u1 - lam[1]*u2*u2

def sym_critical(R, mode):
    def F(u0):
        u = float(np.atleast_1d(u0)[0])
        bl = make_blocks(mode, R, u, 1-u)
        return np.array([f_at(bl, u)])
    best = None
    for s0 in np.linspace(0.05, 0.49, 30):
        try:
            res = least_squares(F, [s0], xtol=1e-13, ftol=1e-13, gtol=1e-13, max_nfev=200)
        except Exception:
            continue
        u = float(res.x[0])
        if 0 < u < 0.5 and abs(F(u)[0]) < 1e-5:
            if best is None or abs(u-0.5) < abs(best[0]-0.5):
                best = (u, abs(F(u)))
    if best is None:
        return None, None
    u, res = best
    D = D_of(make_blocks(mode, R, u, 1-u), npts=20000)
    return u, D

def boundary_scan(R, mode, N=120):
    best = (-1e9, None) if mode=="SUP" else (1e9, None)
    consts = [[(1.0,1.0)],[(1.0,R)]]
    for t in np.linspace(0.001,0.999,N):
        for bl in ([(t,1.0),(1-t,R)],[(t,R),(1-t,1.0)]):
            D = D_of(bl)
            if (D > best[0] if mode=="SUP" else D < best[0]):
                best = (D, t, bl)
    for bl in consts:
        D = D_of(bl)
        if (D > best[0] if mode=="SUP" else D < best[0]):
            best = (D, -1, bl)
    return best

def grid_extremum(R, mode, N):
    aa = np.linspace(0.005, 0.99, N)
    bb = np.linspace(0.005, 0.99, N)
    best = (-1e9, None) if mode=="SUP" else (1e9, None)
    for i,a in enumerate(aa):
        for j,b in enumerate(bb):
            if a+b > 0.999 or b <= a: continue
            D = D_of(make_blocks(mode,R,a,b), npts=1500)
            if (D > best[0] if mode=="SUP" else D < best[0]):
                best = (D, (a,b))
    return best

def refine(R, mode, seed, span=0.02, N=25):
    a0,b0 = seed
    best = (-1e9, None) if mode=="SUP" else (1e9, None)
    for a in np.linspace(max(1e-4,a0-span), min(0.999,a0+span), N):
        for b in np.linspace(max(1e-4,b0-span), min(0.999,b0+span), N):
            if a+b > 0.999 or b <= a: continue
            D = D_of(make_blocks(mode,R,a,b), npts=6000)
            if (D > best[0] if mode=="SUP" else D < best[0]):
                best = (D, (a,b))
    return best

if __name__ == "__main__":
    for R in (1.05, 1.1, 1.2, 1.5, 2.0, 3.0, 4.0, 10.0):
        print(f"===== R={R} =====")
        for mode in ("SUP","INF"):
            u, Dsym = sym_critical(R, mode)
            bd = boundary_scan(R, mode, N=80)
            print(f"  {mode}: sym u*={u if u is None else round(u,6)} D_sym={Dsym if Dsym is None else round(Dsym,6)}")
            print(f"         boundary best D={round(bd[0],6)}")
            if Dsym is not None:
                ge = grid_extremum(R, mode, 55)
                print(f"         coarse grid extremum D={round(ge[0],6)} at a={ge[1][0]:.4f} b={ge[1][1]:.4f}")
                re = refine(R, mode, ge[1], span=0.03, N=20)
                print(f"         refined extremum    D={round(re[0],6)} at a={re[1][0]:.5f} b={re[1][1]:.5f} (1-b={1-re[1][1]:.5f})")




