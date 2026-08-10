# -*- coding: utf-8 -*-
"""cert_roots.py: verified root isolation for s1, s2 over a parameter box.
Usage: roots2_cert(a_int, b_int, R_int, s_lo, s_hi) -> (s1_iv, s2_iv)
Rigorous: for every (a,b,R) in the box, F(s1)=F(s2)=0 with s1 in s1_iv, s2 in s2_iv,
uniquely (F_s excludes 0 on the brackets).
"""
import mpmath as mp
from mpmath import iv
iv.dps = 40
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from cert_lib import F_iv, Fs_iv

def scan_signs(F_iv_fn, s_lo, s_hi, n=4000):
    """Return list of (s_i, s_{i+1}) brackets with verified sign separation."""
    pts = [s_lo + (s_hi - s_lo)*mp.mpf(k)/n for k in range(n+1)]
    vals = [F_iv_fn(pt) for pt in pts]
    out = []
    for i in range(n):
        v0, v1 = vals[i], vals[i+1]
        if v0.b < 0 and v1.a > 0:
            out.append((pts[i], pts[i+1]))
        elif v1.b < 0 and v0.a > 0:
            out.append((pts[i], pts[i+1]))
    return out

def refine_bracket(F_iv_fn, bracket, iters=40):
    """Bisection with correct sign convention: keep F(lo), F(hi) of opposite
    signs by comparing each midpoint interval with the sign of F(lo)."""
    lo, hi = bracket
    vlo = F_iv_fn(lo); vhi = F_iv_fn(hi)
    assert vlo.b < 0 < vhi.a or vhi.b < 0 < vlo.a
    if vlo.a > 0:
        # F(lo) > 0, F(hi) < 0
        for _ in range(iters):
            md = (lo+hi)/2
            vmd = F_iv_fn(md)
            if vmd.a > 0:
                lo = md
            elif vmd.b < 0:
                hi = md
            else:
                break
    else:
        # F(lo) < 0, F(hi) > 0
        for _ in range(iters):
            md = (lo+hi)/2
            vmd = F_iv_fn(md)
            if vmd.b < 0:
                lo = md
            elif vmd.a > 0:
                hi = md
            else:
                break
    return lo, hi

def roots2_cert(a, b, R, s_lo=None, s_hi=None, scan_n=6000, refine=45):
    """a,b,R: iv intervals.  Returns ((s1_lo,s1_hi),(s2_lo,s2_hi)) with verified
    sign-separated brackets containing the first two roots for all params in the box."""
    if s_lo is None: s_lo = mp.mpf('1e-9')
    if s_hi is None: s_hi = mp.mpf(2)*mp.pi + mp.mpf('0.7')
    F = lambda s: F_iv(s, a, b, R)
    br = scan_signs(F, s_lo, s_hi, n=scan_n)
    if len(br) < 2:
        return None
    out = []
    for bracket in br[:2]:
        lo, hi = refine_bracket(F, bracket, iters=refine)
        # verify simplicity: F_s excludes 0 on the bracket (interval over box)
        FsI = Fs_iv(iv.mpf((lo, hi)), a, b, R)
        if FsI.a > 0 or FsI.b < 0:
            out.append((lo, hi))
        else:
            return None
    return tuple(out)

if __name__ == "__main__":
    # test at a point and at a small box
    pt = lambda x: iv.mpf((mp.mpf(float(x)), mp.mpf(float(x))))
    for (aa, bb, RR) in [(0.45, 0.55, 4.0), (0.42, 0.58, 100.0), (0.46, 0.54, 1000.0)]:
        a, b, R = pt(aa), pt(bb), pt(RR)
        r = roots2_cert(a, b, R)
        print("point (%.4f,%.4f,%.4f):" % (aa, bb, RR), r)
    # small box test
    box = lambda lo, hi: iv.mpf((mp.mpf(float(lo)), mp.mpf(float(hi))))
    a, b, R = box(0.45, 0.46), box(0.54, 0.55), box(3.9, 4.1)
    r = roots2_cert(a, b, R)
    print("box a=[0.45,0.46] b=[0.54,0.55] R=[3.9,4.1]:", r)
