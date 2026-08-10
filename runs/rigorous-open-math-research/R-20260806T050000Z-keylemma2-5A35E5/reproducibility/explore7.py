# -*- coding: utf-8 -*-
"""explore7.py -- decompose dG2/dq into partials in (q,gamma) space."""
import sys, mpmath as mp
sys.path.insert(0, r'F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T050000Z-keylemma2-5A35E5\reproducibility')
import kl2_lib as L
mp.mp.dps = 30

def GO(g, q):
    c = L.odd_beta(mp.pi - g, q)/(mp.pi - g)
    return L.Gfun(mp.pi - g, c, q)

def dGOdq_partial(g, q):
    h = mp.mpf('1e-6')*q
    return (GO(g, q+h) - GO(g, q-h))/(2*h)

def dGOdg(g, q):
    h = mp.mpf('1e-7')
    return (GO(g+h, q) - GO(g-h, q))/(2*h)

def dgammadq(c, q):
    """dgamma/dq at fixed c."""
    g = L.gamma_of(q, c)
    Ph = L.Phi(g, q)
    return -mp.sin(g)*mp.cos(g)/(q + c*Ph)

for (q, c) in [(mp.mpf('2'), mp.mpf('0.1')), (mp.mpf('2'), mp.mpf('0.49')),
               (mp.mpf('10'), mp.mpf('0.3')), (mp.mpf('100'), mp.mpf('0.05')),
               (mp.mpf('100'), mp.mpf('0.49')), (mp.mpf('1.1'), mp.mpf('0.49'))]:
    g = L.gamma_of(q, c)
    dq_fd = (L.G2(c, q*mp.mpf('1.000001')) - L.G2(c, q*mp.mpf('0.999999')))/(mp.mpf('2e-6')*q)
    part_q = dGOdq_partial(g, q)
    part_g = dGOdg(g, q)
    dg = dgammadq(c, q)
    chain = part_q + part_g*dg
    print('q=%s c=%s gamma=%s: dG2/dq(fd)=%s ; partial_q=%s ; partial_g*dgamma/dq=%s ; chain=%s'
          % (mp.nstr(q,5), mp.nstr(c,4), mp.nstr(g,5), mp.nstr(dq_fd,7), mp.nstr(part_q,7), mp.nstr(part_g*dg,7), mp.nstr(chain,7)))
