# -*- coding: utf-8 -*-
"""Locate c* (F_tilde(c)=0) for large q and verify residual at xi*=q/(2(c*+q))."""
import mpmath as mp
mp.mp.dps = 60
import numpy as np

def phi_q(q, x): return mp.cos(x)**2 + q*q*mp.sin(x)**2
def Mf(q, c, x): return x*x*mp.sin(x)**2/(q + c*phi_q(q, x))
def alpha1_of_c(q, c):
    f = lambda x: mp.atan(1/(q*mp.tan(x))) - c*x
    lo, hi = mp.mpf('1e-20'), mp.pi/2 - mp.mpf('1e-20')
    for _ in range(120):
        mid = (lo+hi)/2
        if f(mid) > 0: lo = mid
        else: hi = mid
    return mp.findroot(f, (lo+hi)/2, tol=mp.mpf('1e-55'))
def alpha2_of_c(q, c):
    f = lambda x: mp.atan(-q*mp.tan(x)) - c*x
    lo, hi = mp.pi/2 + mp.mpf('1e-20'), mp.pi - mp.mpf('1e-20')
    for _ in range(120):
        mid = (lo+hi)/2
        if f(mid) > 0: lo = mid
        else: hi = mid
    return mp.findroot(f, (lo+hi)/2, tol=mp.mpf('1e-55'))
def Fe(q, c): return Mf(q, c, alpha1_of_c(q, c)) - Mf(q, c, alpha2_of_c(q, c))

for qv in [10.0, 100.0, 1000.0, 1e6]:
    q = mp.mpf(qv)
    # Fe decreasing on (0,1/2); bracket root
    lo, hi = mp.mpf('1e-30'), mp.mpf('0.4999')
    f = lambda c: Fe(q, c)
    assert f(lo) > 0 and f(hi) < 0, (qv, f(lo), f(hi))
    for _ in range(120):
        mid = (lo+hi)/2
        if f(mid)*f(lo) <= 0: hi = mid
        else: lo = mid
    c_star = (lo+hi)/2
    xi_star = q/(2*(c_star+q))
    print(f"q={qv}: c*={mp.nstr(c_star,15)} xi*={mp.nstr(xi_star,15)} 1/2-xi*={mp.nstr(mp.mpf('0.5')-xi_star,10)} Fe(c*)={mp.nstr(f(c_star),6)}")
