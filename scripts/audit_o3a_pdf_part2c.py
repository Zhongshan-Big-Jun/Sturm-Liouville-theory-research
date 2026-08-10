# -*- coding: utf-8 -*-
"""Audit Part 2c (fast): large R via float64 fine grid + mpmath root refinement."""
import numpy as np
from scipy.optimize import brentq
import mpmath as mp
mp.mp.dps = 60

def y1_grid(a, b, q, sgrid):
    s = sgrid
    y = np.zeros_like(s); dy = np.ones_like(s)
    om = s; t = a
    c, sn = np.cos(om*t), np.sin(om*t)
    y, dy = y*c + dy*sn/om, -y*om*sn + dy*c
    om = s*q; t = b-a
    c, sn = np.cos(om*t), np.sin(om*t)
    y, dy = y*c + dy*sn/om, -y*om*sn + dy*c
    om = s; t = 1-b
    c, sn = np.cos(om*t), np.sin(om*t)
    y, dy = y*c + dy*sn/om, -y*om*sn + dy*c
    return y

def eigvals_fast(a, b, q, kmax=2, N=60000):
    top = 2*np.pi + 1e-3
    grid = np.linspace(1e-9, top, N)
    ys = y1_grid(a, b, q, grid)
    idx = np.where(np.diff(np.sign(ys)) != 0)[0]
    assert len(idx) >= kmax, (a, b, q, len(idx))
    res = []
    for i in range(kmax):
        s = brentq(lambda t: float(y1_grid(a, b, q, np.array([t]))[0]), grid[idx[i]], grid[idx[i]+1], xtol=1e-14, rtol=1e-14)
        res.append(s)
    return res

def residual_fast(a, b, q, N=60000):
    s1, s2 = eigvals_fast(a, b, q, N=N)
    l1, l2 = s1**2, s2**2
    def mode(s):
        om1 = s
        yA, dyA = np.sin(om1*a)/om1, np.cos(om1*a)
        om2 = s*q
        ya, dya = yA, dyA
        c, sn = np.cos(om2*(b-a)), np.sin(om2*(b-a))
        yb, dyb = ya*c + dya*sn/om2, -ya*om2*sn + dya*c
        om3 = s
        n = (a/2 - np.sin(2*s*a)/(4*s))/s**2
        amp2 = ya**2 + (dya/om2)**2
        cross = ya*dya/om2
        L = b-a
        n += q**2 * ( amp2*L/2 + (ya**2 - (dya/om2)**2)*np.sin(2*om2*L)/(4*om2) + cross*(1-np.cos(2*om2*L))/(2*om2) )
        amp2b = yb**2 + (dyb/om3)**2
        crossb = yb*dyb/om3
        L = 1-b
        n += amp2b*L/2 + (yb**2 - (dyb/om3)**2)*np.sin(2*om3*L)/(4*om3) + crossb*(1-np.cos(2*om3*L))/(2*om3)
        return ya, yb, n
    ya1, yb1, n1 = mode(s1)
    ya2, yb2, n2 = mode(s2)
    R1 = l1*ya1**2/n1 - l2*ya2**2/n2
    R2 = l1*yb1**2/n1 - l2*yb2**2/n2
    return R1, R2, ya2/ya1, yb2/yb1, s1, s2

print("=== Part 2c: large R, symmetric line ===")
for R in [1000.0, 1e6]:
    q = np.sqrt(R)
    vals = []
    # log-scale points near 1/2 catch the sharp root (1/2 - xi* ~ 1/q^2 at large q);
    # float64 transfer matrices are reliable here because the barrier is thin.
    for xi in [0.40, 0.45, 0.48, 0.49, 0.495, 0.498, 0.499, 0.4995, 0.4999, 0.49999, 0.499999, 0.4999995]:
        R1, R2, v_a, v_b, s1, s2 = residual_fast(xi, 1-xi, q)
        vals.append((xi, R1))
        print(f"   R={R} xi={xi}: R1={R1:.4e} v_a={v_a:+.5f} v_b={v_b:+.5f} s2-2pi={s2-2*np.pi:.3e}")
    sc = sum(1 for i in range(len(vals)-1) if vals[i][1]*vals[i+1][1] < 0)
    print(f"   R={R}: SR sign changes = {sc}")
    assert sc == 1

print("=== Part 2d: mpmath root refinement at R=1000,1e6 ===")
def y1_mp(a, b, q, s):
    y, dy = mp.mpf('0'), mp.mpf('1')
    om = s; t = a
    c, sn = mp.cos(om*t), mp.sin(om*t)
    y, dy = y*c + dy*sn/om, -y*om*sn + dy*c
    om = s*q; t = b-a
    c, sn = mp.cos(om*t), mp.sin(om*t)
    y, dy = y*c + dy*sn/om, -y*om*sn + dy*c
    om = s; t = 1-b
    c, sn = mp.cos(om*t), mp.sin(om*t)
    y, dy = y*c + dy*sn/om, -y*om*sn + dy*c
    return y

def eigvals_mp_br(a, b, q, brackets):
    res = []
    for lo, hi in brackets:
        f = lambda s: y1_mp(a, b, q, s)
        for _ in range(200):
            mid = (lo+hi)/2
            if f(mid)*f(lo) <= 0: hi = mid
            else: lo = mid
        res.append((lo+hi)/2)
    return res

def mode_mp(s, am, bm, qm):
    om1 = s
    yA, dyA = mp.sin(om1*am)/om1, mp.cos(om1*am)
    om2 = s*qm
    ya, dya = yA, dyA
    c, sn = mp.cos(om2*(bm-am)), mp.sin(om2*(bm-am))
    yb, dyb = ya*c + dya*sn/om2, -ya*om2*sn + dya*c
    om3 = s
    n = (am/2 - mp.sin(2*s*am)/(4*s))/s**2
    amp2 = ya**2 + (dya/om2)**2
    cross = ya*dya/om2
    L = bm-am
    n += qm**2 * ( amp2*L/2 + (ya**2 - (dya/om2)**2)*mp.sin(2*om2*L)/(4*om2) + cross*(1-mp.cos(2*om2*L))/(2*om2) )
    amp2b = yb**2 + (dyb/om3)**2
    crossb = yb*dyb/om3
    L = 1-bm
    n += amp2b*L/2 + (yb**2 - (dyb/om3)**2)*mp.sin(2*om3*L)/(4*om3) + crossb*(1-mp.cos(2*om3*L))/(2*om3)
    return ya, yb, n

for R in [1000.0, 1e6]:
    q = np.sqrt(R)
    qm = mp.sqrt(mp.mpf(R))
    # float64 bisection (30 iterations -> width ~1e-11) locates the root to
    # float64 accuracy; the mpmath bisection then runs on a window widened by
    # 1e-9 so that both endpoints straddle the true root even when float64
    # cancellation makes the residual sign unreliable within ~1e-13 of it.
    lo, hi = 0.49, 0.5
    def srf(xi): return residual_fast(xi, 1-xi, q)[0]
    for _ in range(30):
        mid = (lo+hi)/2
        if srf(mid)*srf(lo) <= 0: hi = mid
        else: lo = mid
    xi0 = (lo+hi)/2
    # initial eigenvalue brackets from float64 at xi0, widened to 1e-3
    s1f, s2f = eigvals_fast(xi0, 1-xi0, q)
    s1b = [(mp.mpf(s1f)-mp.mpf('1e-3'), mp.mpf(s1f)+mp.mpf('1e-3'))]
    s2b = [(mp.mpf(s2f)-mp.mpf('1e-3'), mp.mpf(s2f)+mp.mpf('1e-3'))]
    def residual_mp(xi):
        am = mp.mpf(xi); bm = 1-am
        s1m, s2m = eigvals_mp_br(am, bm, qm, s1b+s2b)
        ya1, yb1, n1 = mode_mp(s1m, am, bm, qm)
        ya2, yb2, n2 = mode_mp(s2m, am, bm, qm)
        R1 = s1m**2*ya1**2/n1 - s2m**2*ya2**2/n2
        R2 = s1m**2*yb1**2/n1 - s2m**2*yb2**2/n2
        return R1, R2, ya2/ya1, yb2/yb1
    ml = mp.mpf(xi0) - mp.mpf('1e-9')
    mh = mp.mpf(xi0) + mp.mpf('1e-9')
    Rl, *_ = residual_mp(ml)
    Rh, *_ = residual_mp(mh)
    assert Rl*Rh < 0, (R, mp.nstr(Rl,4), mp.nstr(Rh,4))
    for _ in range(120):
        mm = (ml+mh)/2
        Rm, *_ = residual_mp(mm)
        if Rm*Rl <= 0: mh = mm
        else: ml = mm; Rl = Rm
    xi_star = (ml+mh)/2
    R1, R2, v_a, v_b = residual_mp(xi_star)
    print(f"R={R}: xi*={mp.nstr(xi_star,18)} R1={mp.nstr(R1,6)} R2={mp.nstr(R2,6)} v_a={mp.nstr(v_a,6)} v_b={mp.nstr(v_b,6)}")
    assert abs(R1) < mp.mpf('1e-30') and abs(R2) < mp.mpf('1e-30') and v_a > 0 and v_b < 0
print("OK")
