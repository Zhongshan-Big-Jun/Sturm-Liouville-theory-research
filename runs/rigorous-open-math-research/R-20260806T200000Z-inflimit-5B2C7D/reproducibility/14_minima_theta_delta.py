# -*- coding: utf-8 -*-
"""14_minima_theta_delta.py
Find the numerical minima of the elementary deep-sliver bounds over their
regions, for certification planning:
  THB on (wcap, 2], D2B on (wdelta, 2] (D2B valid where pi - eps tan x > 0),
  max(THB, D2B) on (0.5, 2], and the B3 value at wcap.
ASCII punctuation.
"""
import numpy as np
import mpmath as mp
mp.mp.dps = 30
PI2 = mp.mpf('9.86960440108935861883449099987615113531369940724079062641334937622')

def THB(w, R, eps):
    c = 1/(2*w) - eps
    t1m = mp.atan(mp.cot(c*mp.pi/2)/eps)
    t1p = mp.pi/2 - mp.atan(eps*mp.tan(c*t1m))
    return (mp.pi/2 - t1p)*(mp.pi/2 + t1m)/(w*w*eps*eps)

def D2B(w, R, eps):
    x = mp.pi/(4*w)
    c = 1/(2*w) - eps
    if mp.pi - eps*mp.tan(x) <= 0:
        return None
    d2p = mp.atan(eps*mp.cot(x - eps*mp.pi/2))
    arg = x - eps*mp.pi/2 + c*d2p
    if arg >= mp.pi/2:
        return None
    d2m = mp.atan(eps*mp.cot(arg))
    return d2m*(mp.pi - eps*mp.tan(x))/(w*w*eps*eps)

for R in ['1500', '1e4', '1e6', '1e8']:
    RR = mp.mpf(R); eps = 1/mp.sqrt(RR)
    wcap = mp.mpf('0.5')*(1 + 25/(PI2*RR))**-mp.mpf('0.5')
    # theta bound on (wcap, 2]
    mth = mp.inf; mth_at = None
    for k in range(4000):
        w = wcap + (mp.mpf('2') - wcap)*k/4000
        if w > 2: break
        v = THB(w, RR, eps)
        if v < mth: mth = v; mth_at = w
    # delta bound on its validity region
    md = mp.inf; md_at = None
    for k in range(4000):
        w = mp.mpf('0.5') + mp.mpf('1.5')*k/4000
        if w > 2: break
        v = D2B(w, RR, eps)
        if v is not None and v < md: md = v; md_at = w
    # max of the two on (0.5, 2]
    mx = mp.inf; mx_at = None
    for k in range(8000):
        w = mp.mpf('0.5') + mp.mpf('1.5')*k/8000
        if w > 2: break
        th = THB(w, RR, eps)
        d2 = D2B(w, RR, eps)
        v = th if d2 is None else max(th, d2)
        if v < mx: mx = v; mx_at = w
    print("R=%s: wcap=%s; min THB=%s at w=%s; min D2B=%s at w=%s; min max=%s at w=%s" % (
        R, mp.nstr(wcap, 8), mp.nstr(mth, 8), mp.nstr(mth_at, 7),
        mp.nstr(md, 8), mp.nstr(md_at, 7), mp.nstr(mx, 8), mp.nstr(mx_at, 7)))
print("done")
