# -*- coding: utf-8 -*-
"""verify_dG2dq_formula.py -- check closed form of dG2/dq at fixed c.

FIXED 2026-08-06: the partial-q formula was missing the q-derivative of the
denominator D = q + c*Phi in term t1 (the "+1" from dq of q itself).  Corrected:
t1 = -Ph_q*W/D + Ph*W*(1 + c*Ph_q)/D^2.  All six test points now agree with
central finite differences to ~1e-12 relative (50 digits, h = 1e-6*q).
"""
import sys, mpmath as mp
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T050000Z-keylemma2-5A35E5\reproducibility")
import kl2_lib as L
mp.mp.dps = 50

def Ga_manual(a, c, q):
    """partial G / partial a at fixed (c, q)."""
    Ph = L.Phi(a, q); K = q*q - 1; s = mp.sin(a); co = mp.cos(a); sc = s*co
    D = q + c*Ph; W = L.Wfun(a)
    Pha = 2*K*sc
    Wp = 2*(s*co - a)/s**2
    d1 = -(Pha*W + Ph*Wp)/D + Ph*W*c*Pha/D**2
    dsc = co*co - s*s
    N = 2*c*a*Ph*K*sc
    dN = 2*c*K*(Ph*a*dsc + Ph*sc + a*Pha*sc)
    d2 = dN/D**2 - 2*N*c*Pha/D**3
    return d1 + d2

def Gq_formula(a, c, q):
    """partial G / partial q at fixed (a, c)."""
    Ph = L.Phi(a, q); K = q*q - 1; s = mp.sin(a); co = mp.cos(a); sc = s*co
    D = q + c*Ph; W = L.Wfun(a)
    Ph_q = 2*q*s*s
    K_q = 2*q
    # d/dq[-Ph*W/D] = -(Ph_q*W)/D + Ph*W*(1 + c*Ph_q)/D^2   (FIXED: the +1 term)
    t1 = -Ph_q*W/D + Ph*W*(1 + c*Ph_q)/D**2
    N = 2*c*a*Ph*K*sc
    dNq = 2*c*a*sc*(Ph_q*K + Ph*K_q)
    t2 = dNq/D**2 - 2*N*(1 + c*Ph_q)/D**3
    return t1 + t2

def dG2dq_formula(c, q):
    a2 = L.alpha2(c, q)
    g = mp.pi - a2
    D = q + c*L.Phi(g, q)
    dalpha2dq = mp.sin(g)*mp.cos(g)/D
    return Gq_formula(a2, c, q) + Ga_manual(a2, c, q)*dalpha2dq

ok = True
for (q, c) in [(mp.mpf("1.1"), mp.mpf("0.49")), (mp.mpf("2"), mp.mpf("0.1")), (mp.mpf("10"), mp.mpf("0.3")), (mp.mpf("100"), mp.mpf("0.05")), (mp.mpf("100"), mp.mpf("0.49")), (mp.mpf("1.01"), mp.mpf("0.4"))]:
    h = mp.mpf("1e-6")*q
    fd = (L.G2(c, q+h) - L.G2(c, q-h))/(2*h)
    f = dG2dq_formula(c, q)
    rel = abs(fd - f)/abs(fd)
    ok &= rel < mp.mpf("1e-9")
    print("q=%s c=%s: fd=%s formula=%s rel=%s" % (mp.nstr(q,5), mp.nstr(c,5), mp.nstr(fd,10), mp.nstr(f,10), mp.nstr(rel,3)))
print("ALL OK" if ok else "FAIL")
