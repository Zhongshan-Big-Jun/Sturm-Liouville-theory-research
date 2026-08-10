# -*- coding: utf-8 -*-
"""c1trace_lib.py v12: profile() traces over [0.01, B0] (covers u(b0)=g1^{-1}(a0)); filters bad bottom points."""
import numpy as np
import sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fast_lib import sec, roots2_fast, y_at, norm_n

A0 = float(np.arccos(0.25)/np.pi)
B0 = 1 - A0

def R1R2(a, b, R, cache=None):
    key = None
    if cache is not None:
        key = (round(a,12), round(b,12), R)
        if key in cache:
            return cache[key]
    s1, s2 = roots2_fast(a, b, R)
    n1 = norm_n(s1, a, b, R); n2 = norm_n(s2, a, b, R)
    y1a = np.sin(s1*a)/s1; y2a = np.sin(s2*a)/s2
    y1b = y_at(s1, a, b, R, b); y2b = y_at(s2, a, b, R, b)
    R1 = s1**2*y1a**2/n1 - s2**2*y2a**2/n2
    R2 = s1**2*y1b**2/n1 - s2**2*y2b**2/n2
    out = (s1, s2, n1, n2, R1, R2)
    if cache is not None:
        cache[key] = out
    return out

def partials(a, b, R, h=1e-6, cache=None):
    def dsec(s, var, dh=h):
        if var == 's': return (sec(s+dh,a,b,R)-sec(s-dh,a,b,R))/(2*dh)
        if var == 'a': return (sec(s,a+dh,b,R)-sec(s,a-dh,b,R))/(2*dh)
        return (sec(s,a,b+dh,R)-sec(s,a,b-dh,R))/(2*dh)
    s1, s2, n1, n2, R1, R2 = R1R2(a, b, R, cache)
    def r1(ss1, ss2, aa, bb):
        nn1 = norm_n(ss1, aa, bb, R); nn2 = norm_n(ss2, aa, bb, R)
        return ss1**2*(np.sin(ss1*aa)/ss1)**2/nn1 - ss2**2*(np.sin(ss2*aa)/ss2)**2/nn2
    def r2(ss1, ss2, aa, bb):
        nn1 = norm_n(ss1, aa, bb, R); nn2 = norm_n(ss2, aa, bb, R)
        return ss1**2*y_at(ss1,aa,bb,R,bb)**2/nn1 - ss2**2*y_at(ss2,aa,bb,R,bb)**2/nn2
    ds1a = -dsec(s1,'a')/dsec(s1,'s'); ds1b = -dsec(s1,'b')/dsec(s1,'s')
    ds2a = -dsec(s2,'a')/dsec(s2,'s'); ds2b = -dsec(s2,'b')/dsec(s2,'s')
    def dr1(var):
        if var=='a': return (r1(s1,s2,a+h,b)-r1(s1,s2,a-h,b))/(2*h)
        if var=='b': return (r1(s1,s2,a,b+h)-r1(s1,s2,a,b-h))/(2*h)
        if var=='s1': return (r1(s1+h,s2,a,b)-r1(s1-h,s2,a,b))/(2*h)
        return (r1(s1,s2+h,a,b)-r1(s1,s2-h,a,b))/(2*h)
    def dr2(var):
        if var=='a': return (r2(s1,s2,a+h,b)-r2(s1,s2,a-h,b))/(2*h)
        if var=='b': return (r2(s1,s2,a,b+h)-r2(s1,s2,a,b-h))/(2*h)
        if var=='s1': return (r2(s1+h,s2,a,b)-r2(s1-h,s2,a,b))/(2*h)
        return (r2(s1,s2+h,a,b)-r2(s1,s2-h,a,b))/(2*h)
    R1a = dr1('a') + dr1('s1')*ds1a + dr1('s2')*ds2a
    R1b = dr1('b') + dr1('s1')*ds1b + dr1('s2')*ds2b
    R2a = dr2('a') + dr2('s1')*ds1a + dr2('s2')*ds2a
    R2b = dr2('b') + dr2('s1')*ds1b + dr2('s2')*ds2b
    return R1a, R1b, R2a, R2b

def a_fp(R, lo=0.40, hi=0.5, cache=None):
    def f(u): return R1R2(u, 1-u, R, cache)[4]
    fl = f(lo)
    for _ in range(120):
        md = 0.5*(lo+hi)
        if np.signbit(f(md)) == np.signbit(fl): lo = md
        else: hi = md
    return 0.5*(lo+hi)

def _newton_b(a, binit, R, cache, atol=1e-12, maxit=40):
    b = binit
    for _ in range(maxit):
        R1a, R1b, R2a, R2b = partials(a, b, R, cache=cache)
        R1 = R1R2(a, b, R, cache)[4]
        if abs(R1b) < 1e-9:
            return None
        db = -R1/R1b
        b2 = b + db
        if not (1e-6 < b2 < 1 - 1e-6):
            return None
        b = b2
        if abs(db) < atol:
            break
    R1 = R1R2(a, b, R, cache)[4]
    return b if abs(R1) < 1e-8 else None

def _newton_a(ainit, b, R, cache, atol=1e-12, maxit=40):
    a = ainit
    for _ in range(maxit):
        R1a, R1b, R2a, R2b = partials(a, b, R, cache=cache)
        R1 = R1R2(a, b, R, cache)[4]
        if abs(R1a) < 1e-9:
            return None
        da = -R1/R1a
        a2 = a + da
        if not (1e-6 < a2 < 1 - 1e-6):
            return None
        a = a2
        if abs(da) < atol:
            break
    R1 = R1R2(a, b, R, cache)[4]
    return a if abs(R1) < 1e-8 else None

def _bisect_b(a, b_pred, R, cache, win=0.5, iters=70, nprobe=60):
    lo0 = max(1e-6, b_pred - win); hi0 = min(1 - 1e-6, b_pred + win)
    xs = np.linspace(lo0, hi0, nprobe)
    vals = [R1R2(a, float(x), R, cache)[4] for x in xs]
    for i in range(nprobe-1):
        if vals[i] * vals[i+1] < 0:
            lo, hi = xs[i], xs[i+1]
            flo = vals[i]
            for _ in range(iters):
                md = 0.5*(lo+hi)
                if np.signbit(R1R2(a, float(md), R, cache)[4]) == np.signbit(flo):
                    lo = md
                else:
                    hi = md
            return 0.5*(lo+hi)
    xs = np.linspace(1e-6, 1-1e-6, nprobe)
    vals = [R1R2(a, float(x), R, cache)[4] for x in xs]
    for i in range(nprobe-1):
        if vals[i] * vals[i+1] < 0:
            lo, hi = xs[i], xs[i+1]
            flo = vals[i]
            for _ in range(iters):
                md = 0.5*(lo+hi)
                if np.signbit(R1R2(a, float(md), R, cache)[4]) == np.signbit(flo):
                    lo = md
                else:
                    hi = md
            return 0.5*(lo+hi)
    return None

def trace_branch(R, a_lo, a_hi, nstep=400, cache=None, max_total=40000):
    fp = a_fp(R, cache=cache)
    bfp = 1 - fp
    pts = [(fp, bfp)]
    a, b = fp, bfp
    step = (a_hi - fp) / nstep
    gp = None
    guard = 0
    while a < a_hi - 1e-10 and guard < max_total:
        guard += 1
        a_new = min(a + step, a_hi)
        b_pred = b + (gp if gp is not None else 0.0) * (a_new - a)
        b_new = _newton_b(a_new, b_pred, R, cache)
        if b_new is None:
            b_new = _bisect_b(a_new, b_pred, R, cache)
        if b_new is None:
            step = step / 2
            continue
        if abs(b_new - b_pred) > 0.35:
            step = step / 2
            continue
        pts.append((a_new, b_new))
        R1a, R1b, R2a, R2b = partials(a_new, b_new, R, cache=cache)
        gp = -R1a / R1b
        a, b = a_new, b_new
        if step < 1e-9:
            break
    a, b = fp, bfp
    step = (fp - a_lo) / nstep
    gp = None
    guard = 0
    while a > a_lo + 1e-10 and guard < max_total:
        guard += 1
        a_new = max(a - step, a_lo)
        b_pred = b + (gp if gp is not None else 0.0) * (a_new - a)
        b_new = _newton_b(a_new, b_pred, R, cache)
        if b_new is None:
            b_new = _bisect_b(a_new, b_pred, R, cache)
        if b_new is None:
            step = step / 2
            continue
        if abs(b_new - b_pred) > 0.35:
            step = step / 2
            continue
        pts.append((a_new, b_new))
        R1a, R1b, R2a, R2b = partials(a_new, b_new, R, cache=cache)
        gp = -R1a / R1b
        a, b = a_new, b_new
        if step < 1e-9:
            break
    pts2 = []
    for p in pts:
        if not pts2 or abs(p[0] - pts2[-1][0]) > 1e-10:
            pts2.append(p)
    pts2.sort()
    return pts2

def g1inv_table(y, aa, bb, tol=1e-9):
    if y <= bb[0] + tol:
        return aa[0]
    if y >= bb[-1] - tol:
        return aa[-1]
    lo, hi = aa[0], aa[-1]
    for _ in range(90):
        md = 0.5*(lo+hi)
        if np.interp(md, aa, bb) < y:
            lo = md
        else:
            hi = md
    return 0.5*(lo+hi)

def solve_u(a, R, cache, aa, bb):
    y = 1 - a
    u = g1inv_table(y, aa, bb)
    if u is None:
        return None
    for _ in range(30):
        bu0 = float(np.interp(u, aa, bb))
        bu = _newton_b(u, bu0, R, cache)
        if bu is None:
            bu = bu0
        R1a, R1b, R2a, R2b = partials(u, bu, R, cache=cache)
        g1pu = -R1a / R1b
        if abs(g1pu) < 1e-12:
            return None
        F = bu - y
        du = -F / g1pu
        u2 = u + du
        if not (aa[0] - 1e-6 < u2 < aa[-1] + 1e-6):
            return None
        u = u2
        if abs(du) < 1e-13:
            break
    bu = _newton_b(u, float(np.interp(u, aa, bb)), R, cache)
    if bu is None:
        return None
    return u if abs(bu - y) < 1e-8 else None

def profile(R, nstep=400, cache=None, a_lo=0.01):
    fp = a_fp(R, cache=cache)
    pts = trace_branch(R, a_lo, B0, nstep=nstep, cache=cache)
    if len(pts) < 5:
        return None
    # filter: keep b > 0.05 to drop spurious near-boundary points
    pts = [p for p in pts if p[1] > 0.05]
    if len(pts) < 5:
        return None
    aa = np.array([p[0] for p in pts]); bb = np.array([p[1] for p in pts])
    a_max1 = float(aa[-1])
    beta = min(a_max1, B0)
    rows = []
    grid = sorted(set(list(aa[aa >= A0 - 1e-12]) + [A0, beta, fp]))
    for a in grid:
        if a < A0 - 1e-12 or a > beta + 1e-12:
            continue
        b0t = float(np.interp(a, aa, bb))
        b = _newton_b(a, b0t, R, cache)
        if b is None:
            b = b0t
        R1a, R1b, R2a, R2b = partials(a, b, R, cache=cache)
        g1p = -R1a / R1b
        u = solve_u(a, R, cache, aa, bb)
        if u is None:
            rows.append((float(a), float(b), float(g1p), None, None, float('nan'), float('nan')))
            continue
        bu = 1 - a
        Ru1a, Ru1b, Ru2a, Ru2b = partials(u, bu, R, cache=cache)
        g1pu = -Ru1a / Ru1b
        Phi = g1p * g1pu
        h = b - 1 + u
        hp = g1p - 1 / g1pu
        rows.append((float(a), float(b), float(g1p), float(u), float(Phi), float(h), float(hp)))
    rows.sort(key=lambda r: r[0])
    return dict(R=R, fp=float(fp), a0=A0, beta=beta, a_max1=a_max1, rows=rows)