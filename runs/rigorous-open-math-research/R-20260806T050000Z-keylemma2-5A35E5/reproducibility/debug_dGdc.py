# -*- coding: utf-8 -*-
"""debug_dGdc.py -- compare partials of G with numerical differentiation."""
import sys, mpmath as mp
sys.path.insert(0, r'F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T050000Z-keylemma2-5A35E5\reproducibility')
import kl2_lib as L
mp.mp.dps = 40

def Gpartial_a(a, c, q):
    Ph = L.Phi(a, q); K = q*q - 1; s = mp.sin(a); co = mp.cos(a); sc = s*co
    D = q + c*Ph; W = L.Wfun(a)
    Pha = 2*K*sc
    Wp = 2*(s*co - a)/s**2
    d1 = -(Pha*W + Ph*Wp)/D + Ph*W*c*Pha/D**2
    dsc = co*co - s*s
    N = 2*c*a*Ph*K*sc
    dN = 2*c*K*(Ph*a*dsc + Ph*sc + a*Pha*sc)
    d2 = dN/D**2 + N*(-4*c*Pha)/D**3
    return d1 + d2

def Gpartial_c(a, c, q):
    Ph = L.Phi(a, q); K = q*q - 1; s = mp.sin(a); co = mp.cos(a); sc = s*co
    D = q + c*Ph; W = L.Wfun(a)
    return Ph*Ph*W/D**2 + 2*a*Ph*K*sc*(D - 2*c*Ph)/D**3

for (q, c, a) in [(mp.mpf('2'), mp.mpf('0.1'), L.alpha1(mp.mpf('0.1'), mp.mpf('2'))),
                  (mp.mpf('2'), mp.mpf('0.45'), L.alpha2(mp.mpf('0.45'), mp.mpf('2')))]:
    h = mp.mpf('1e-8')
    Ga_num = (L.Gfun(a+h, c, q) - L.Gfun(a-h, c, q))/(2*h)
    Gc_num = (L.Gfun(a, c+h, q) - L.Gfun(a, c-h, q))/(2*h)
    Ga_cl = Gpartial_a(a, c, q)
    Gc_cl = Gpartial_c(a, c, q)
    print(f'q={q} c={c} a={mp.nstr(a,6)}')
    print(f'  Ga: num={mp.nstr(Ga_num,10)} closed={mp.nstr(Ga_cl,10)} diff={float(Ga_num-Ga_cl):.2e}')
    print(f'  Gc: num={mp.nstr(Gc_num,10)} closed={mp.nstr(Gc_cl,10)} diff={float(Gc_num-Gc_cl):.2e}')
    # total derivative: alpha' * Ga + Gc
    Ph = L.Phi(a, q); D = q + c*Ph
    ap = -a*Ph/D
    tot = ap*Ga_cl + Gc_cl
    # numeric total: G along the curve
    ak = L.alpha1 if a < mp.pi/2 else L.alpha2
    num_tot = (L.Gfun(ak(c+h,q), c+h, q) - L.Gfun(ak(c-h,q), c-h, q))/(2*h)
    print(f'  total: num={mp.nstr(num_tot,10)} closed={mp.nstr(tot,10)} diff={float(num_tot-tot):.2e}')
