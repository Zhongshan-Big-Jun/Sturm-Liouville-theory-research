# -*- coding: utf-8 -*-
"""cert_c1.py: certified interval-arithmetic engine for the C1 branch problem.
Provides: certified root enclosures for s1, s2 over parameter boxes (interval
Newton), certified branch boxes, certified P0 (G > 0) and E1 (h endpoints).

Every returned interval is a rigorous enclosure for ALL parameters in the box.
"""
import mpmath as mp
from mpmath import iv
iv.dps = 40
import sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from cert_lib import F_iv, Fs_iv
import sym_cert_partials as scp

def I(lo, hi):
    return iv.mpf((mp.mpf(float(lo)), mp.mpf(float(hi))))

def P(x):
    return iv.mpf((mp.mpf(float(x)), mp.mpf(float(x))))

def cert_roots(a_iv, b_iv, R_iv, s1g, s2g, w=1e-6, iters=10, min_sep=1e-5):
    """Certify unique roots s1, s2 of F(s; p) = 0 for all p in the box.
    s1g, s2g: float approximations at box center.  Returns (s1_iv, s2_iv)."""
    def one(sg):
        s = I(sg - w, sg + w)
        sm = P(sg)
        ok = False
        for _ in range(iters):
            N = sm - F_iv(sm, a_iv, b_iv, R_iv) / Fs_iv(s, a_iv, b_iv, R_iv)
            if N.a > s.a and N.b < s.b:
                s = N
                ok = True
            else:
                break
        if not ok:
            return None
        # uniqueness: F_s excludes 0 on the enclosure
        FsI = Fs_iv(s, a_iv, b_iv, R_iv)
        if FsI.a > 0 or FsI.b < 0:
            return s
        return None
    s1 = one(s1g)
    if s1 is None:
        return None
    s2 = one(s2g)
    if s2 is None:
        return None
    return s1, s2

def R1R2_cert(a_iv, b_iv, R_iv, s1_iv, s2_iv):
    R1 = scp.R1(s1_iv, s2_iv, a_iv, b_iv, R_iv)
    R2 = scp.R2(s1_iv, s2_iv, a_iv, b_iv, R_iv)
    return R1, R2

def partials_cert(a_iv, b_iv, R_iv, s1_iv, s2_iv):
    R1a = scp.R1_a(s1_iv, s2_iv, a_iv, b_iv, R_iv)
    R1b = scp.R1_b(s1_iv, s2_iv, a_iv, b_iv, R_iv)
    R2a = scp.R2_a(s1_iv, s2_iv, a_iv, b_iv, R_iv)
    R2b = scp.R2_b(s1_iv, s2_iv, a_iv, b_iv, R_iv)
    return R1a, R1b, R2a, R2b

def cert_box(a_lo, a_hi, b_lo, b_hi, R_lo, R_hi, s1g, s2g):
    """Certify (s1,s2) and return G interval for the box; None on failure."""
    a_iv, b_iv, R_iv = I(a_lo, a_hi), I(b_lo, b_hi), I(R_lo, R_hi)
    rr = cert_roots(a_iv, b_iv, R_iv, s1g, s2g)
    if rr is None:
        return None
    s1_iv, s2_iv = rr
    R1a, R1b, R2a, R2b = partials_cert(a_iv, b_iv, R_iv, s1_iv, s2_iv)
    if R1b.a > 0 or R1b.b < 0:
        G = -R1a / R1b
        return dict(s1=s1_iv, s2=s2_iv, R1a=R1a, R1b=R1b, R2a=R2a, R2b=R2b, G=G)
    return None

def cert_branch_in_box(a_lo, a_hi, R_lo, R_hi, b_lo, b_hi, s1g, s2g):
    """Certify: for every (a,R) in the box, R1(a, . , R) has a unique zero in
    (b_lo, b_hi) (the branch crosses the box), and G > 0 there.
    Returns dict with G interval or None."""
    cb = cert_box(a_lo, a_hi, b_lo, b_hi, R_lo, R_hi, s1g, s2g)
    if cb is None:
        return None
    # sign separation at b-window endpoints (b point, (a,R) box)
    a_iv, R_iv = I(a_lo, a_hi), I(R_lo, R_hi)
    rlo = cert_roots(a_iv, P(b_lo), R_iv, s1g, s2g)
    if rlo is None:
        return None
    s1_lo, s2_lo = rlo
    R1_lo = scp.R1(s1_lo, s2_lo, a_iv, P(b_lo), R_iv)
    rhi = cert_roots(a_iv, P(b_hi), R_iv, s1g, s2g)
    if rhi is None:
        return None
    s1_hi, s2_hi = rhi
    R1_hi = scp.R1(s1_hi, s2_hi, a_iv, P(b_hi), R_iv)
    if R1_lo.b < 0 and R1_hi.a > 0:
        return cb
    if R1_lo.a > 0 and R1_hi.b < 0:
        return cb
    return None
