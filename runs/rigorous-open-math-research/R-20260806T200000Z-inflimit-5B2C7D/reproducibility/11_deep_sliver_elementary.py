# -*- coding: utf-8 -*-
"""11_deep_sliver_elementary.py (v2, numpy scan + mpmath bisection)
Verify numerically the elementary deep-sliver bounds for G(R,u) = mu2 - mu1,
u = w/sqrt(R), R >= 1500, w in (0,2].  Each bound must satisfy
    bound(w,R) <= G_exact(w,R)  and  bound >= 25 on its regime.
Bounds: B1 (w<=0.19), B2 (0.19..w_c), B3 (w_c..wcap), B4 (cap), B5 (1/2..2, R-012).
Auxiliary: A1 theta1 < pi*w (w<=1/2); A2 theta2 branch; A3 j >= 0.0634 on cap.
ASCII punctuation.
"""
import numpy as np
import mpmath as mp
mp.mp.dps = 40
PI2 = mp.mpf('9.86960440108935861883449099987615113531369940724079062641334937622')

def m12_np(mu, R, u):
    kh = np.sqrt(mu); kl = np.sqrt(mu/R)
    c1 = np.cos(kh*u); s1 = np.sin(kh*u)
    c2 = np.cos(kl*(1-2*u)); s2 = np.sin(kl*(1-2*u))
    a00 = c1*c2 - s1*s2*kl/kh
    a01 = c1*s2/kl + s1*c2/kh
    return a00*(s1/kh) + a01*c1

def m12_mp(mu, R, u):
    Rm = mp.mpf(R); um = mp.mpf(u)
    kh = mp.sqrt(mu); kl = mp.sqrt(mu/Rm)
    c1 = mp.cos(kh*um); s1 = mp.sin(kh*um)
    c2 = mp.cos(kl*(1-2*um)); s2 = mp.sin(kl*(1-2*um))
    a00 = c1*c2 - s1*s2*kl/kh
    a01 = c1*s2/kl + s1*c2/kh
    return a00*(s1/kh) + a01*c1

def roots(R, u):
    Rf = float(R); uf = float(u)
    hi = 4*float(np.pi**2)*Rf*1.0000001
    mu_grid = np.linspace(0.0, hi, 80001)
    y = m12_np(mu_grid, Rf, uf)
    # find first two sign changes
    idx = np.where(y[:-1]*y[1:] < 0)[0]
    if len(idx) < 2:
        raise RuntimeError("fewer than 2 sign changes R=%s u=%s n=%d" % (R, u, len(idx)))
    out = []
    for i in idx[:2]:
        a, b = mp.mpf(mu_grid[i]), mp.mpf(mu_grid[i+1])
        fa = m12_mp(a, R, u)
        for _ in range(220):
            m = (a+b)/2
            fm = m12_mp(m, R, u)
            if (fm < 0) == (fa < 0):
                a = m; fa = fm
            else:
                b = m
        out.append((a+b)/2)
    return out

def G_exact(R, w):
    u = w/mp.sqrt(R)
    m1, m2 = roots(R, u)
    return m2 - m1

def check(w_lo, w_hi, Rlist, bound_fn, name, npts=40):
    worst_slack = mp.inf; worst_at = None
    for R in Rlist:
        eps = 1/mp.sqrt(R)
        for k in range(npts+1):
            w = w_lo + (w_hi - w_lo)*k/npts
            if w <= mp.mpf('1e-9'): continue
            G = G_exact(R, w)
            B = bound_fn(w, R, eps)
            assert B <= G*(1+mp.mpf('1e-7')), ("bound>G", name, R, w, B, G)
            if B < worst_slack:
                worst_slack = B; worst_at = (R, w)
            assert B >= 25, ("bound<25", name, R, w, B, G)
    print("%s: min bound = %s at %s (>= 25, <= G)" % (name, mp.nstr(worst_slack, 8), worst_at))
    return worst_slack

def B1(w, R, eps):
    c = 1/(2*w) - eps
    return 3*PI2*R - 32*mp.pi**4*R*eps*w*w/c

def B2(w, R, eps):
    return PI2*R*((1-2*eps*w)**-2 - 1)

def B3(w, R, eps):
    return PI2*R*(1/(4*w*w) - 1)

def B5(w, R, eps):
    x = mp.pi/(4*w)
    B2t = eps*mp.cot(x - eps*mp.pi)
    M = mp.cot(x - eps*mp.pi)
    if not (x - eps*mp.pi > 0 and x + B2t/(2*w) < mp.pi/2):
        return None
    return (mp.tan(x) + mp.cot(x + B2t/(2*w)))*(1 - eps**2*M**2/3)*(mp.pi - eps*mp.tan(x))/(w*w*eps)

print("== B5 (w in (0.5,2], R-012 elementary bound) ==")
worst = mp.inf; worst_at = None; valid_all = True; bad = 0
for R in ['1500', '1e4', '1e6']:
    RR = mp.mpf(R); eps = 1/mp.sqrt(RR)
    for k in range(800):
        w = mp.mpf('0.5') + mp.mpf('1.5')*k/800
        if w > 2: break
        G = G_exact(RR, w)
        B = B5(w, RR, eps)
        if B is None:
            valid_all = False; continue
        if B > G*(1+mp.mpf('1e-7')):
            bad += 1
            if bad < 5: print("  B5>G at", R, w, B, G)
        if B < worst:
            worst = B; worst_at = (R, w)
print("B5 min = %s at %s; invalid pts: %s; overestimates: %d" % (mp.nstr(worst, 8), worst_at, not valid_all, bad))

print("== A1/A2/A3 ==")
for R in ['1500', '1e4', '1e6']:
    RR = mp.mpf(R); eps = 1/mp.sqrt(RR)
    wc = 1/(2*(1+eps))
    wcap = mp.mpf('0.5') - 25/(2*PI2*RR)
    for w in [mp.mpf('0.001'), mp.mpf('0.01'), mp.mpf('0.05'), mp.mpf('0.1'),
              mp.mpf('0.19'), mp.mpf('0.25'), mp.mpf('0.3'), mp.mpf('0.4'),
              mp.mpf('0.45'), mp.mpf('0.49'), mp.mpf('0.4999'), mp.mpf('0.5')]:
        u = w/mp.sqrt(RR)
        m1, m2 = roots(RR, u)
        t1 = mp.sqrt(m1)*w/mp.sqrt(RR)
        t2 = mp.sqrt(m2)*w/mp.sqrt(RR)
        assert t1 < mp.pi*w, ("A1 fail", R, w, t1, mp.pi*w)
        c = 1/(2*w) - eps
        if w <= wc:
            assert t2 > mp.pi/(2*c), ("A2a fail", R, w, t2, mp.pi/(2*c))
        else:
            assert t2 >= mp.pi/2, ("A2b fail", R, w, t2)
        if w >= wcap:
            j = 1 - t1/(mp.pi*w)
            assert j >= mp.mpf('0.0634'), ("A3 fail", R, w, j)
print("A1/A2/A3 PASS")

check(mp.mpf('0.001'), mp.mpf('0.19'), [mp.mpf('1500'), mp.mpf('1e4')], B1, "B1 (w<=0.19)")
check(mp.mpf('0.19'), mp.mpf('0.487'), [mp.mpf('1500'), mp.mpf('1e4')], B2, "B2 (0.19..w_c)")
check(mp.mpf('0.487'), mp.mpf('0.499'), [mp.mpf('1500'), mp.mpf('1e4')], B3, "B3 (strip)")
print("done")
