# -*- coding: utf-8 -*-
"""13_verify_elementary_bounds.py
Verify the corrected elementary deep-sliver bounds for G(R,u) = mu2-mu1,
u = w/sqrt(R), R >= 1500, w in (0,2].  Every bound must satisfy
    bound(w,R) <= G_exact(w,R)   and   bound >= 25 on its region.
Bounds:
  B1 (0,0.19]:   3*pi^2 R - 32*pi^4 R eps w^2 / c,            c = 1/(2w) - eps
  B2 [0.19,w_c]: pi^2 R ((1-2 eps w)^-2 - 1),                 w_c = 1/(2(1+eps))
  B3 (w_c,wcap]: pi^2 R (1/(4w^2) - 1),                       wcap = 0.5 (1+25/(pi^2 R))^-1/2
  THB (wcap,2]:  (pi/2 - t1p)(pi/2 + t1m)/(w^2 eps^2),
                 t1m = arctan(cot(c pi/2)/eps), t1p = pi/2 - arctan(eps tan(c t1m))
  D2B (wd,2]:    d2m (pi - eps tan x)/(w^2 eps^2),  x = pi/(4w),
                 d2p = arctan(eps cot(x - eps pi/2)),
                 d2m = arctan(eps cot(x - eps pi/2 + c d2p))
Coverage: (0,2] = (0,0.19] u [0.19,w_c] u (w_c,wcap] u (wcap,2];
  on (wcap,2] use max(THB, D2B) (D2B valid where pi - eps tan x > 0).
Also verify derivation auxiliaries:
  A1 theta1 < pi w on (0,1/2];  A4 theta1 in [t1m, t1p];  A5 theta2 >= pi/2 (w>=w_c);
  A6 delta2 in [d2m, d2p];  A7 delta1 >= -eps tan x.
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
    mu_grid = np.linspace(0.0, hi, 60001)
    y = m12_np(mu_grid, Rf, uf)
    idx = np.where(y[:-1]*y[1:] < 0)[0]
    if len(idx) < 2:
        raise RuntimeError("fewer than 2 roots R=%s u=%s n=%d" % (R, u, len(idx)))
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

def G_th_mu(R, w):
    u = w/mp.sqrt(R)
    m1, m2 = roots(R, u)
    t1 = mp.sqrt(m1)*w/mp.sqrt(R)
    t2 = mp.sqrt(m2)*w/mp.sqrt(R)
    return m2-m1, t1, t2

def B1(w, R, eps):
    c = 1/(2*w) - eps
    return 3*PI2*R - 32*mp.pi**4*R*eps*w*w/c

def B2(w, R, eps):
    return PI2*R*((1-2*eps*w)**-2 - 1)

def B3(w, R, eps):
    return PI2*R*(1/(4*w*w) - 1)

def THB(w, R, eps):
    c = 1/(2*w) - eps
    t1m = mp.atan(mp.cot(c*mp.pi/2)/eps)
    t1p = mp.pi/2 - mp.atan(eps*mp.tan(c*t1m))
    return (mp.pi/2 - t1p)*(mp.pi/2 + t1m)/(w*w*eps*eps)

def D2B(w, R, eps):
    x = mp.pi/(4*w)
    c = 1/(2*w) - eps
    d2p = mp.atan(eps*mp.cot(x - eps*mp.pi/2))
    arg = x - eps*mp.pi/2 + c*d2p
    if arg >= mp.pi/2:
        return None
    d2m = mp.atan(eps*mp.cot(arg))
    val = d2m*(mp.pi - eps*mp.tan(x))/(w*w*eps*eps)
    if mp.pi - eps*mp.tan(x) <= 0:
        return None
    return val

def cover_bound(w, R, eps):
    wc = 1/(2*(1+eps))
    wcap = mp.mpf('0.5')*(1 + 25/(PI2*R))**-mp.mpf('0.5')
    if w <= mp.mpf('0.19'):
        return B1(w, R, eps)
    if w <= wc:
        return B2(w, R, eps)
    if w <= wcap:
        return B3(w, R, eps)
    th = THB(w, R, eps)
    d2 = D2B(w, R, eps)
    if d2 is None:
        return th
    return max(th, d2)

Rlist = ['1500', '1e4', '1e6', '1e8']
worst_overall = mp.inf; worst_info = None
viol = 0
for R in Rlist:
    RR = mp.mpf(R); eps = 1/mp.sqrt(RR)
    wc = 1/(2*(1+eps)); wcap = mp.mpf('0.5')*(1+25/(PI2*RR))**-mp.mpf('0.5')
    for k in range(600):
        w = mp.mpf('1e-3') + (mp.mpf('2') - mp.mpf('1e-3'))*k/600
        if w > 2: break
        G, t1, t2 = G_th_mu(RR, w)
        B = cover_bound(w, RR, eps)
        if B > G*(1+mp.mpf('1e-6')):
            viol += 1
            if viol < 8:
                print("  VIOLATION bound>G:", R, w, "B=", B, "G=", G)
        if B < worst_overall:
            worst_overall = B; worst_info = (R, w, B, G)
        if B < 25:
            print("  BOUND BELOW 25:", R, w, B, G)
    # fine w near 0.5 and near 2
    for k in range(400):
        w = mp.mpf('0.49') + (mp.mpf('0.52') - mp.mpf('0.49'))*k/400
        G, t1, t2 = G_th_mu(RR, w)
        B = cover_bound(w, RR, eps)
        if B > G*(1+mp.mpf('1e-6')):
            viol += 1
            if viol < 8:
                print("  VIOLATION bound>G:", R, w, "B=", B, "G=", G)
        if B < worst_overall:
            worst_overall = B; worst_info = (R, w, B, G)
        if B < 25:
            print("  BOUND BELOW 25:", R, w, B, G)
print("global worst bound = %s at (R,w)=(%s,%s); G there = %s; violations: %d" % (
    mp.nstr(worst_overall, 8), worst_info[0], mp.nstr(worst_info[1], 6), mp.nstr(worst_info[3], 8), viol))

print("== auxiliaries ==")
ok = True
for R in ['1500', '1e4', '1e6']:
    RR = mp.mpf(R); eps = 1/mp.sqrt(RR)
    wc = 1/(2*(1+eps))
    for k in range(200):
        w = mp.mpf('1e-3') + (mp.mpf('2') - mp.mpf('1e-3'))*k/200
        G, t1, t2 = G_th_mu(RR, w)
        c = 1/(2*w) - eps
        x = mp.pi/(4*w)
        if w <= mp.mpf('0.5'):
            if not (t1 < mp.pi*w):
                print("  A1 fail", R, w, t1, mp.pi*w); ok = False
        if w > wc:
            if not (t2 >= mp.pi/2 - mp.mpf('1e-12')):
                print("  A5 fail", R, w, t2); ok = False
            t1m = mp.atan(mp.cot(c*mp.pi/2)/eps)
            t1p = mp.pi/2 - mp.atan(eps*mp.tan(c*t1m))
            if not (t1m <= t1 <= t1p + mp.mpf('1e-12')):
                print("  A4 fail", R, w, t1m, t1, t1p); ok = False
        if w > mp.mpf('0.5'):
            d2p = mp.atan(eps*mp.cot(x - eps*mp.pi/2))
            arg = x - eps*mp.pi/2 + c*d2p
            if arg < mp.pi/2:
                d2m = mp.atan(eps*mp.cot(arg))
                if not (d2m <= t2 - mp.pi/2 <= d2p + mp.mpf('1e-12')):
                    print("  A6 fail", R, w, d2m, t2-mp.pi/2, d2p); ok = False
            if not (t1 - mp.pi/2 >= -eps*mp.tan(x) - mp.mpf('1e-12')):
                print("  A7 fail", R, w, t1-mp.pi/2, -eps*mp.tan(x)); ok = False
print("auxiliaries ok:", ok)
print("done")
