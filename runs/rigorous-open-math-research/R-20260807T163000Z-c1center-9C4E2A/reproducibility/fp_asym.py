# -*- coding: utf-8 -*-
"""fp_asym.py: robust high-precision machinery for the symmetric fixed point
(fp) of the barrier family and its R->inf asymptotics.

The full secular equation F(s) = 0 is used with a fine float scan plus
mpmath Newton refinement, because the factored even/odd equations have
spurious low roots (barrier modes) for wide barriers at large R.
"""
import numpy as np
import mpmath as mp
import sys, os
mp.mp.dps = 40
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fast_lib import sec, norm_n

def roots2_mp(aa, bb, RR, hi=8.0, n=400001):
    """Two smallest positive roots of the full secular equation, mpmath refined."""
    s = np.linspace(1e-9, hi, n)
    M = sec(s, float(aa), float(bb), float(RR))
    ch = np.signbit(M[1:]) != np.signbit(M[:-1])
    idx = np.nonzero(ch)[0][:2]
    out = []
    for i in idx:
        lo, hi_ = s[i], s[i+1]; flo = M[i]
        for _ in range(60):
            md = 0.5*(lo+hi_)
            if np.signbit(sec(md, float(aa), float(bb), float(RR))) == np.signbit(flo):
                lo = md
            else:
                hi_ = md
        out.append(0.5*(lo+hi_))
    if len(out) < 2:
        raise RuntimeError("roots2_mp fail (a,b,R)=%s" % ((aa,bb,RR),))
    mm = mp.sqrt(RR)
    def sec_mp(x):
        return (mp.cos(x*(1-bb))*mp.cos(x*mm*(bb-aa))*mp.sin(x*aa)
                - mm*mp.sin(x*(1-bb))*mp.sin(x*mm*(bb-aa))*mp.sin(x*aa)
                + (mp.cos(x*(1-bb))*mp.sin(x*mm*(bb-aa))/mm)*mp.cos(x*aa)
                + mp.sin(x*(1-bb))*mp.cos(x*mm*(bb-aa))*mp.cos(x*aa))
    res = []
    for r0 in out:
        x = mp.mpf(float(r0))
        for _ in range(15):
            fx = sec_mp(x); h = mp.mpf('1e-9')
            fpx = (sec_mp(x+h) - sec_mp(x-h))/(2*h)
            x = x - fx/fpx
        res.append(x)
    return res

def R1num(aa, bb, RR):
    s1, s2 = roots2_mp(aa, bb, RR)
    n1 = norm_n(float(s1), float(aa), float(bb), float(RR))
    n2 = norm_n(float(s2), float(aa), float(bb), float(RR))
    return mp.sin(s1*aa)**2/n1 - mp.sin(s2*aa)**2/n2

def R1sym(u, RR):
    return R1num(u, 1-u, RR)

def fp_mp(RR, lo=None, hi=mp.mpf('0.5')):
    """Bisect R1(u,1-u)=0.  lo defaults by R: 0.45 for R<1e4 else 0.49."""
    RR = mp.mpf(RR)
    if lo is None:
        lo = mp.mpf('0.49') if RR >= 1e4 else mp.mpf('0.45')
    f0 = R1sym(lo, RR)
    for _ in range(130):
        md = (lo+hi)/2
        fm = R1sym(md, RR)
        if fm*f0 < 0:
            hi = md
        else:
            lo = md
    return (lo+hi)/2

def G_at(aa, bb, RR):
    """G = -R1_a/R1_b via mpmath finite differences with re-solved roots."""
    h = mp.mpf('1e-6')
    R1a = (R1num(aa+h, bb, RR) - R1num(aa-h, bb, RR))/(2*h)
    R1b = (R1num(aa, bb+h, RR) - R1num(aa, bb-h, RR))/(2*h)
    return -R1a/R1b, R1a, R1b

def branch_mp(aa, RR, blo, bhi):
    """Solve R1(aa, b, R) = 0 in b over [blo, bhi]."""
    f0 = R1num(aa, blo, RR)
    for _ in range(90):
        md = (blo+bhi)/2
        if R1num(aa, md, RR)*f0 < 0:
            bhi = md
        else:
            blo = md
    return (blo+bhi)/2

def solve_a(bb, RR, alo, ahi):
    """Solve R1(a, bb, R) = 0 in a over [alo, ahi]."""
    f0 = R1num(alo, bb, RR)
    for _ in range(90):
        md = (alo+ahi)/2
        if R1num(md, bb, RR)*f0 < 0:
            ahi = md
        else:
            alo = md
    return (alo+ahi)/2
