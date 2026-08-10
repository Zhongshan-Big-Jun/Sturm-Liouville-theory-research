# -*- coding: utf-8 -*-
"""verify_c4_details.py -- C4 certificate region coverage facts.
Establishes: (a) the predecessor verify script's region constants are stale
(x0 below 2pi/7 by 1.7e-20, x1 below 2pi/5 - 1e-3 by 4.44e-5);
(b) the certificate leaves tile [v_lo, v_hi] with v_lo < 2pi/7 and
v_hi > 2pi/5 - 1e-3, i.e. the certificate covers [2pi/7, 2pi/5 - 1e-3]
completely (overhang ~1e-60 on each side), so no continuity/Lipschitz
argument is needed for the C4 interval leg.
"""
import mpmath as mp
mp.mp.dps = 80
x1_pred = mp.mpf('1.25559265358979323846264338327950288419716939937510582097494')
x0_pred = mp.mpf('0.897597901025655210972033336078616704034170566267291310427109')
print('pred x1 - (2pi/5 - 1e-3) =', mp.nstr(x1_pred - (mp.mpf('0.4')*mp.pi - mp.mpf('1e-3')), 3))
print('pred x0 - 2pi/7         =', mp.nstr(x0_pred - 2*mp.pi/7, 3))
v_lo = mp.mpf('0.897597901025655210989326680937000824056334114107173091707127')
v_hi = mp.mpf('1.25563706143591729538505735331180115367886775975004232838998')
print('cert v_lo - 2pi/7       =', mp.nstr(v_lo - 2*mp.pi/7, 3))
print('cert v_hi - (2pi/5-1e-3) =', mp.nstr(v_hi - (mp.mpf('0.4')*mp.pi - mp.mpf('1e-3')), 3))
print('cert covers [2pi/7, 2pi/5-1e-3]:', v_lo <= 2*mp.pi/7 and v_hi >= mp.mpf('0.4')*mp.pi - mp.mpf('1e-3'))
# K values at the q=1 point and near the right edge (evidence)
def K_v(v):
    u = mp.tan(v); w = mp.pi - mp.mpf('2.5')*v
    q = mp.sin(v)*mp.cos(w)/(mp.cos(v)*mp.sin(w))
    return (q*q+u*u)*(5*v*q - 3*u + 2*v) - mp.mpf('1.2')*u*q*(1+u*u)
print('K(2pi/7) =', mp.nstr(K_v(2*mp.pi/7), 12))
print('K(2pi/5 - 1e-3) =', mp.nstr(K_v(mp.mpf('0.4')*mp.pi - mp.mpf('1e-3')), 12))
