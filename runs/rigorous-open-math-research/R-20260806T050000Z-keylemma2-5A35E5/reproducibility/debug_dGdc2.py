# -*- coding: utf-8 -*-
"""debug_dGdc2.py -- recheck Ga after fix."""
import sys, mpmath as mp
sys.path.insert(0, r'F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T050000Z-keylemma2-5A35E5\reproducibility')
import kl2_lib as L
mp.mp.dps = 40

def Ga_manual(a, c, q):
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

for (q, c, a) in [(mp.mpf('2'), mp.mpf('0.1'), L.alpha1(mp.mpf('0.1'), mp.mpf('2'))),
                  (mp.mpf('2'), mp.mpf('0.45'), L.alpha2(mp.mpf('0.45'), mp.mpf('2')))]:
    h = mp.mpf('1e-8')
    Ga_num = (L.Gfun(a+h, c, q) - L.Gfun(a-h, c, q))/(2*h)
    print(f'q={q} c={c} a={mp.nstr(a,6)}')
    print(f'  Ga num={mp.nstr(Ga_num,12)} manual={mp.nstr(Ga_manual(a,c,q),12)} diff={float(Ga_num-Ga_manual(a,c,q)):.2e}')
    # check d1 and d2 separately against numeric partials
    # total derivative check with the fixed formula via direct numeric differentiation of G along curve
    ak = L.alpha1 if a < mp.pi/2 else L.alpha2
    h2 = mp.mpf('1e-8')
    num_tot = (L.Gfun(ak(c+h2,q), c+h2, q) - L.Gfun(ak(c-h2,q), c-h2, q))/(2*h2)
    Ph = L.Phi(a, q); D = q + c*Ph
    ap = -a*Ph/D
    Gc = L.dGdc(a, c, q)  # after fix this is total derivative
    # recompute total from manual pieces
    tot_manual = ap*Ga_manual(a,c,q) + (Ph*Ph*W/D**2 + 2*a*Ph*K*sc*(D-2*c*Ph)/D**3)
    print(f'  total num={mp.nstr(num_tot,12)} lib={mp.nstr(Gc,12)} manual={mp.nstr(tot_manual,12)}')
    print(f'  diff num-lib={float(num_tot-Gc):.2e}  num-manual={float(num_tot-tot_manual):.2e}')
