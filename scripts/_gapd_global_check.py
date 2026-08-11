# -*- coding: utf-8 -*-
"""Gap (d) EVIDENCE cross-check: INF minimizer of the well family is a
sign-consistent good root on the symmetric line (a+b=1), for several R.

Checks (EVIDENCE only, NOT a proof):
  C1  interior critical points (R1=R2=0): all have a+b=1 (rigidity) and
      z0 in (a,b) (sign-consistency automatic), for R in {1.2,2,4,10,100}.
  C2  D at every critical point >= D(symmetric); symmetric D < 3pi^2/R.
  C3  boundary of Omega: D(0,b), D(a,1) > 3pi^2/R; D(t,t) = 3pi^2/R.
  C4  coarse grid scan: min over grid >= D(symmetric) - eps.
  C5  at the symmetric critical point: fval < 0 on (a,b) (structure lemma:
      {lambda1 u1^2 - lambda2 u2^2 > 0} = (a,b) contains the zero z0 of y2).
"""
import numpy as np
from scipy.optimize import least_squares, brentq, minimize_scalar
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gap_lib import lams_fast, norm2, y_at

def eigs_s(a, b, R, k=2, npts=30000):
    """s = sqrt(lambda) via fast vectorized TM."""
    return lams_fast([(a, R), (b - a, 1.0), (1 - b, R)], k, npts=npts)

def D_well(a, b, R):
    s = eigs_s(a, b, R)
    return s[1] ** 2 - s[0] ** 2

def norm2_well(a, b, R, s):
    """int rho y^2 via exact per-block integration (gap_lib)."""
    return norm2([(a, R), (b - a, 1.0), (1 - b, R)], s)

def fval(a, b, R, x):
    """residual f(x) = lam2*u2^2 - lam1*u1^2, u_k L2(rho)-normalized."""
    s1, s2 = eigs_s(a, b, R)
    blocks = [(a, R), (b - a, 1.0), (1 - b, R)]
    n1 = norm2_well(a, b, R, s1)
    n2 = norm2_well(a, b, R, s2)
    y1 = y_at(blocks, s1, np.array([x]))[0]
    y2 = y_at(blocks, s2, np.array([x]))[0]
    return (s2 ** 2) * (y2 ** 2) / n2 - (s1 ** 2) * (y1 ** 2) / n1

def z2_zero(a, b, R):
    """zero of y2 (slope-normalized) in (0,1) via brentq."""
    s2 = eigs_s(a, b, R)[1]
    blocks = [(a, R), (b - a, 1.0), (1 - b, R)]
    xs = np.linspace(1e-9, 1 - 1e-9, 4001)
    ys = y_at(blocks, s2, xs)
    signs = np.signbit(ys[1:]) != np.signbit(ys[:-1])
    idx = np.nonzero(signs)[0]
    assert len(idx) == 1, (a, b, R, len(idx))
    i = idx[0]
    return brentq(lambda x: y_at(blocks, s2, np.array([x]))[0], xs[i], xs[i + 1], xtol=1e-14)

def crit_search(R, nseed=12, max_nfev=50):
    out = []
    # include the symmetric-line minimizer as a seed (known critical point)
    _, vs = symline_crit(R)
    seeds = [(vs, 1 - vs)]
    grid = np.linspace(0.03, 0.97, nseed)
    for a0 in grid:
        for b0 in grid:
            if b0 > a0:
                seeds.append((a0, b0))
    for (a0, b0) in seeds:
        def res(ab):
            return [fval(ab[0], ab[1], R, ab[0]), fval(ab[0], ab[1], R, ab[1])]
        sol = least_squares(res, [a0, b0], bounds=([1e-7, 1e-7], [1 - 1e-7, 1 - 1e-7]),
                            xtol=1e-13, ftol=1e-13, max_nfev=max_nfev)
        if sol.cost < 1e-18 and sol.x[0] < sol.x[1] - 1e-4:
            key = (round(sol.x[0], 6), round(sol.x[1], 6))
            if not any(abs(key[0] - k[0]) < 2e-5 and abs(key[1] - k[1]) < 2e-5 for k in out):
                out.append((sol.x[0], sol.x[1], sol.cost))
    return out

def symline_crit(R):
    """unique critical point v* of D over the symmetric line: solve
    fval(v,1-v,v)=0 on (0,1/2) by coarse scan + brentq (KEY LEMMA (a'))."""
    vs = np.linspace(1e-4, 0.4999, 2001)
    fv = np.array([fval(v, 1 - v, R, v) for v in vs])
    idx = np.nonzero((fv[1:] * fv[:-1]) < 0)[0]
    assert len(idx) == 1, (R, len(idx))
    i = idx[0]
    vstar = brentq(lambda v: fval(v, 1 - v, R, v), vs[i], vs[i + 1], xtol=1e-14, rtol=1e-14)
    return D_well(vstar, 1 - vstar, R), vstar

def symline_min(R):
    """alias: min of D over symmetric line at its unique critical point."""
    return symline_crit(R)

def main():
    Rs = [1.2, 2.0, 4.0, 10.0, 100.0]
    allok = True
    for R in Rs:
        print(f"===== R = {R} =====")
        crits = crit_search(R)
        print(f"  interior critical points found: {len(crits)}")
        rows = []
        for (a, b, cost) in crits:
            D = D_well(a, b, R)
            z0 = z2_zero(a, b, R)
            sc = (z0 > a) and (z0 < b)
            sym = abs(a + b - 1) < 1e-6
            rows.append((D, a, b, z0, sc, sym))
            print(f"    (a,b)=({a:.6f},{b:.6f}) a+b={a+b:.6f} D={D:.8f} "
                  f"z0={z0:.6f} z0in(a,b)={sc} symmetric={sym}")
        Dline_min, vstar = symline_min(R)
        ok1 = all(sc for (D, a, b, z0, sc, sym) in rows)
        ok2 = all(D >= Dline_min - 1e-7 for (D, a, b, z0, sc, sym) in rows)
        ok3 = Dline_min < 3 * np.pi ** 2 / R - 1e-6
        bs = [0.1, 0.3, 0.5, 0.7, 0.9]
        bnd_two, bnd_diag = [], []
        for t in bs:
            bnd_two.append(D_well(0.0, t, R))
            bnd_two.append(D_well(t, 1.0, R))
            bnd_diag.append(D_well(t, t, R))
        ok4 = np.all(np.array(bnd_two) > 3 * np.pi ** 2 / R + 1e-6) and \
              np.all(np.abs(np.array(bnd_diag) - 3 * np.pi ** 2 / R) < 1e-4)
        g = np.linspace(0.01, 0.99, 31)
        gmin = np.inf
        for a in g:
            for b in g:
                if b < a:
                    continue
                D = D_well(a, b, R)
                if D < gmin:
                    gmin = D
        ok5 = gmin >= Dline_min - 1e-6
        a0, b0 = vstar, 1 - vstar
        xs = np.linspace(a0 + 1e-4, b0 - 1e-4, 25)
        fv = np.array([fval(a0, b0, R, x) for x in xs])
        ok6 = np.all(fv < 1e-8)
        print(f"  Dline_min = {Dline_min:.10f} at v*={vstar:.10f}; 3pi^2/R = {3*np.pi**2/R:.6f}; "
              f"margin = {3*np.pi**2/R - Dline_min:.6f}")
        print(f"  checks: C1(rigid+sign)={ok1} C2(crit>=line)={ok2} C3(Dline<3pi2/R)={ok3} "
              f"C4(boundary)={ok4} C5(grid>=line)={ok5} C6(fval<0 on (a,b))={ok6}")
        allok = allok and ok1 and ok2 and ok3 and ok4 and ok5 and ok6
    print("ALL OK" if allok else "SOME CHECKS FAILED")

if __name__ == '__main__':
    main()
