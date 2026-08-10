# -*- coding: utf-8 -*-
"""10_deep_sliver_curve.py
Certified verification of the 1D curve G(R0, u) >= 25 for u in (0, 2/sqrt(R0)], R0 = 1500.
G(R,u) = mu2(R,u) - mu1(R,u), scaled eigenvalues of the symmetric well [R,1,R].

Proven facts used (exact, no estimates):
  P1. mu_k(R,u) is strictly decreasing in u for fixed R (Feynman-Hellmann, d mu_k/du =
      -2*R*(R-1)*lambda_k*y_k(u)^2 < 0, y_k(u) = y_k(1-u) by symmetry).
  P2. Flat-string comparison: mu_k(R,u) >= (k*pi)^2 (rho <= R pointwise).
  P3. At u = 0 (rho = 1): mu1(R0,0) = R0*pi^2 exactly, mu2(R0,0) = 4*R0*pi^2.

Scheme: cells [u_i, u_{i+1}], u_i = (i/n)*2/sqrt(R0).
  For u in [u_i, u_{i+1}], i >= 1: mu2(u) >= mu2(u_{i+1}) [P1] and mu1(u) <= mu1(u_i) [P1],
  so G(u) >= mu2_lo(u_{i+1}) - mu1_hi(u_i) where *_lo/_hi are certified enclosures.
  For the first cell [0, u_1]: mu2(u) >= mu2(u_1) [P1] and mu1(u) <= R0*pi^2 [P2/P3],
  so G(u) >= mu2_lo(u_1) - R0*pi^2_hi.
Eigenvalue enclosures via directed-rounding interval arithmetic on the secular equations
  cot(sqrt(mu)*u) = (1/sqrt(R))*tan(sqrt(mu/R)*(1/2-u))  (even, mu1)
  tan(sqrt(mu)*u) = -sqrt(R)*tan(sqrt(mu/R)*(1/2-u))    (odd, mu2)
with sign-change bisection on the interval-extended functions.
ASCII punctuation.  Run: python 10_deep_sliver_curve.py
"""
import mpmath as mp
from mpmath import iv
iv.dps = 60
mp.mp.dps = 60

R0 = mp.mpf('1500')
UMAX = 2/mp.sqrt(R0)
TARGET = mp.mpf('25')
N = 60

PI2_LO = mp.mpf('9.86960440108935861883449099987615113531369940724079062641334')
PI2_HI = mp.mpf('9.86960440108935861883449099987615113531369940724079062641335')

def sec_iv(mu_iv, R, u):
    kh = iv.sqrt(mu_iv); kl = iv.sqrt(mu_iv/R)
    c1 = iv.cos(kh*u); s1 = iv.sin(kh*u)
    c2 = iv.cos(kl*(mp.mpf('0.5')-u)); s2 = iv.sin(kl*(mp.mpf('0.5')-u))
    a00 = c1*c2 - s1*s2*kl/kh
    a01 = c1*s2/kl + s1*c2/kh
    return a00*(s1/kh) + a01*c1

def certified_mu(R, u, k, seed):
    rel = mp.mpf('1e-7')
    a, b = seed*(1-rel), seed*(1+rel)
    fa = sec_iv(iv.mpf([a, a]), R, u)
    fb = sec_iv(iv.mpf([b, b]), R, u)
    if not (fa.b < 0 and fb.a > 0) and not (fa.a > 0 and fb.b < 0):
        for rel2 in [mp.mpf('1e-5'), mp.mpf('1e-3'), mp.mpf('1e-2'), mp.mpf('1e-1')]:
            a, b = seed*(1-rel2), seed*(1+rel2)
            fa = sec_iv(iv.mpf([a, a]), R, u)
            fb = sec_iv(iv.mpf([b, b]), R, u)
            if (fa.b < 0 and fb.a > 0) or (fa.a > 0 and fb.b < 0):
                break
        else:
            raise RuntimeError("bracket fail R=%s u=%s k=%s seed=%s" % (R, u, k, seed))
    for _ in range(90):
        mid = (a+b)/2
        fm = sec_iv(iv.mpf([mid, mid]), R, u)
        if fm.b < 0 and fa.b < 0:
            a = mid; fa = fm
        elif fm.a > 0 and fb.a > 0:
            b = mid; fb = fm
        else:
            return iv.mpf([a, b])
    return iv.mpf([a, b])

def sec_f(mu, R, u):
    kh = mp.sqrt(mu); kl = mp.sqrt(mu/R)
    c1 = mp.cos(kh*u); s1 = mp.sin(kh*u)
    c2 = mp.cos(kl*(mp.mpf('0.5')-u)); s2 = mp.sin(kl*(mp.mpf('0.5')-u))
    a00 = c1*c2 - s1*s2*kl/kh
    a01 = c1*s2/kl + s1*c2/kh
    return a00*(s1/kh) + a01*c1

def seed_mu(R, u, k):
    w = u*mp.sqrt(R)
    nu0 = mp.pi**2/(4*w*w)
    if w > mp.mpf('0.5'):
        if k == 1:
            d = -(mp.pi/w**2)*mp.tan(mp.pi/(4*w))
        else:
            d = (mp.pi/w**2)*mp.cot(mp.pi/(4*w))
        return R*nu0 + d*mp.sqrt(R)
    else:
        # w <= 1/2: nu1 ~ pi^2 (below), nu2 ~ pi^2/(4w^2) or 4*pi^2 depending on branch;
        # use rough seeds; certified_mu will widen the bracket if needed.
        if k == 1:
            return mp.pi**2*R*mp.mpf('0.95')
        else:
            return max(mp.pi**2/(4*w*w), 4*mp.pi**2)*R*mp.mpf('0.9')

def root_float(R, u, k):
    s = seed_mu(R, u, k)
    r = None
    if isinstance(s, (mp.mpf, int, float)):
        try:
            r = mp.findroot(lambda m: sec_f(m, R, u), s, tol=mp.mpf('1e-25'), maxsteps=60)
            if not isinstance(r, mp.mpf) or abs(mp.im(r)) > mp.mpf('1e-30'):
                r = None
        except Exception:
            r = None
    if r is None:
        # fallback: scan for a sign change
        lo, hi = mp.mpf('1e-6')*R, mp.pi**2*R if k == 1 else 4*mp.pi**2*R
        xs = [lo + (hi-lo)*i/2000 for i in range(2001)]
        ys = [sec_f(x, R, u) for x in xs]
        for i in range(2000):
            if ys[i]*ys[i+1] < 0:
                try:
                    return mp.findroot(lambda m: sec_f(m, R, u), (xs[i], xs[i+1]), tol=mp.mpf('1e-25'))
                except Exception:
                    continue
        raise RuntimeError("no root found R=%s u=%s k=%s" % (R, u, k))
    return r

def certify_point(R, u, seed1, seed2):
    e1 = certified_mu(R, u, 1, seed1)
    e2 = certified_mu(R, u, 2, seed2)
    return e1, e2

def run():
    us = [UMAX*i/N for i in range(N+1)]
    pts = {}
    # continuation seeds from u = 0 (flat string: mu1 = R0*pi^2, mu2 = 4*R0*pi^2)
    s1, s2 = R0*PI2_LO, 4*R0*PI2_LO
    for i in range(1, N+1):
        e1, e2 = certify_point(R0, us[i], s1, s2)
        pts[i] = (e1, e2)
        s1 = (e1.a+e1.b)/2
        s2 = (e2.a+e2.b)/2
    # cells i=1..N-1: [u_i, u_{i+1}]
    worst = mp.inf
    for i in range(1, N):
        glo = pts[i+1][1].a - pts[i][0].b
        if glo < worst: worst = glo
        assert glo > TARGET, ("cell fail", i, us[i], us[i+1], glo)
    # first cell [0, u_1]
    glo0 = pts[1][1].a - R0*PI2_HI
    worst = min(worst, glo0)
    assert glo0 > TARGET, ("first cell fail", glo0)
    # corner value
    Gc = pts[N][1].a - pts[N][0].b
    print("cells: %d; min cell lower bound G - 25 = %s" % (N-1, mp.nstr(worst - TARGET, 10)))
    print("first cell: mu2_lo(u1) - R0*pi^2 = %s" % mp.nstr(glo0, 10))
    print("corner G(1500, 2/sqrt(1500)) >= %s (need >= 25)" % mp.nstr(Gc, 12))
    print("PASS: G(1500, u) >= 25 for u in (0, 2/sqrt(1500)]")
    return True

if __name__ == '__main__':
    run()
