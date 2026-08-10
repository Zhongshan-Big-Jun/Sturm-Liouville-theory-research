# -*- coding: utf-8 -*-
"""vec_lib.py v4: return Y1b,Y2b and fix good-root classification (v(b)=Y2/Y1 propagated)."""
import numpy as np

def sec_m01(s, a, b, R):
    m = np.sqrt(R)
    s = np.atleast_1d(np.asarray(s, dtype=float))
    b = np.atleast_1d(np.asarray(b, dtype=float))
    S, B = np.broadcast_arrays(s[:, None], b[None, :])
    alpha = S*a; beta = S*(1.0-B); theta = S*m*(B-a)
    ca, sa = np.cos(alpha), np.sin(alpha)
    cb, sb = np.cos(beta), np.sin(beta)
    ct, st = np.cos(theta), np.sin(theta)
    return cb*ct*sa - m*sb*st*sa + (cb*st/m)*ca + sb*ct*ca

def sec_pointwise(s_arr, a, b_arr, R):
    m = np.sqrt(R)
    alpha = s_arr*a; beta = s_arr*(1.0-b_arr); theta = s_arr*m*(b_arr-a)
    ca, sa = np.cos(alpha), np.sin(alpha)
    cb, sb = np.cos(beta), np.sin(beta)
    ct, st = np.cos(theta), np.sin(theta)
    return cb*ct*sa - m*sb*st*sa + (cb*st/m)*ca + sb*ct*ca

def roots2_vect(a, b_grid, R, ns=3501, smax=2*np.pi, iters=70):
    s = np.linspace(1e-8, smax, ns)
    M = sec_m01(s, a, b_grid, R)
    sg = np.signbit(M)
    ch = sg[1:] != sg[:-1]
    has1 = ch.any(axis=0); ge2 = np.cumsum(ch, axis=0) >= 2
    has2 = ge2.any(axis=0)
    i1 = np.argmax(ch, axis=0)
    i2 = np.argmax(ge2, axis=0)
    b_grid = np.asarray(b_grid, dtype=float)
    s1 = np.full(len(b_grid), np.nan); s2 = np.full(len(b_grid), np.nan)
    if has1.any():
        lo = s[i1[has1]]; hi = s[i1[has1]+1]; bg = b_grid[has1]
        flo = sec_pointwise(lo, a, bg, R)
        for _ in range(iters):
            md = 0.5*(lo+hi); fmd = sec_pointwise(md, a, bg, R)
            same = np.signbit(fmd) == np.signbit(flo)
            lo = np.where(same, md, lo); hi = np.where(same, hi, md)
        s1[has1] = 0.5*(lo+hi)
    if has2.any():
        lo = s[i2[has2]]; hi = s[i2[has2]+1]; bg = b_grid[has2]
        flo = sec_pointwise(lo, a, bg, R)
        for _ in range(iters):
            md = 0.5*(lo+hi); fmd = sec_pointwise(md, a, bg, R)
            same = np.signbit(fmd) == np.signbit(flo)
            lo = np.where(same, md, lo); hi = np.where(same, hi, md)
        s2[has2] = 0.5*(lo+hi)
    return s1, s2

def norm_Y(s, a, b, R):
    m = np.sqrt(R)
    s = np.asarray(s, dtype=float); b = np.asarray(b, dtype=float)
    L = b-a; beta = 1-b
    alpha = s*a; theta = s*m*L
    b1 = a/2 - np.sin(2*alpha)/(4*s)
    Icc = L/2 + np.sin(2*theta)/(4*s*m)
    Iss = L/2 - np.sin(2*theta)/(4*s*m)
    Ics = np.sin(theta)**2/(2*s*m)
    A = np.sin(alpha); Bc = np.cos(alpha)/m
    b2 = A*A*Icc + Bc*Bc*Iss + 2*A*Bc*Ics
    Yb = A*np.cos(theta) + Bc*np.sin(theta)
    ypb = -m*np.sin(theta)*np.sin(alpha) + np.cos(theta)*np.cos(alpha)
    Icc3 = beta/2 + np.sin(2*s*beta)/(4*s)
    Iss3 = beta/2 - np.sin(2*s*beta)/(4*s)
    Ics3 = np.sin(s*beta)**2/(2*s)
    b3 = Yb*Yb*Icc3 + ypb*ypb*Iss3 + 2*Yb*ypb*Ics3
    return b1 + R*b2 + b3

def residuals_vec(a, b_grid, R, ns=3501):
    b_grid = np.atleast_1d(np.asarray(b_grid, dtype=float))
    s1, s2 = roots2_vect(a, b_grid, R, ns=ns)
    N1 = norm_Y(s1, a, b_grid, R)
    N2 = norm_Y(s2, a, b_grid, R)
    Y1a = np.sin(s1*a); Y2a = np.sin(s2*a)
    m = np.sqrt(R)
    th1 = s1*m*(b_grid-a); th2 = s2*m*(b_grid-a)
    Y1b = np.sin(s1*a)*np.cos(th1) + (np.cos(s1*a)/m)*np.sin(th1)
    Y2b = np.sin(s2*a)*np.cos(th2) + (np.cos(s2*a)/m)*np.sin(th2)
    R1 = s1**2*Y1a**2/N1 - s2**2*Y2a**2/N2
    R2 = s1**2*Y1b**2/N1 - s2**2*Y2b**2/N2
    return R1, R2, s1, s2, Y1b, Y2b

def good_roots_at(a, R, nb=500, ns=2501):
    """returns (left_roots, right_roots) with correct v-sign classification."""
    b_grid = np.linspace(a+1e-7, 1-1e-7, nb)
    R1, R2, s1, s2, Y1b, Y2b = residuals_vec(a, b_grid, R, ns=ns)
    goodL = np.isfinite(R1) & np.isfinite(s2) & (np.sin(s2*a) > 0)
    goodR = np.isfinite(R2) & np.isfinite(s2) & (np.signbit(Y2b) != np.signbit(Y1b)) & (np.abs(Y1b) > 0)
    vL = np.where(goodL, R1, np.nan)
    vR = np.where(goodR, R2, np.nan)
    outL = []; outR = []
    for i in range(nb-1):
        if vL[i]*vL[i+1] < 0:
            lo, hi = b_grid[i], b_grid[i+1]
            for _ in range(60):
                md = 0.5*(lo+hi)
                r = residuals_vec(a, np.array([md]), R, ns=1201)[0][0]
                if np.isfinite(r) and r*vL[i] < 0: hi = md
                else: lo = md
            outL.append(0.5*(lo+hi))
        if vR[i]*vR[i+1] < 0:
            lo, hi = b_grid[i], b_grid[i+1]
            for _ in range(60):
                md = 0.5*(lo+hi)
                r = residuals_vec(a, np.array([md]), R, ns=1201)[1][0]
                if np.isfinite(r) and r*vR[i] < 0: hi = md
                else: lo = md
            outR.append(0.5*(lo+hi))
    return outL, outR

if __name__ == "__main__":
    # spot check: a=0.1, R=4 (should have right-good roots per prior run)
    import sys, time
    sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-o3abranch-E8E56F\reproducibility")
    for a in [0.01, 0.1, 0.3, 0.42, 0.45, 0.5, 0.57]:
        t0 = time.time()
        L, Rr = good_roots_at(a, 4.0, nb=400)
        print(f"a={a}: left={[round(x,4) for x in L]} right={[round(x,4) for x in Rr]} (t={time.time()-t0:.1f}s)")
