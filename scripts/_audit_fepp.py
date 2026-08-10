# -*- coding: utf-8 -*-
import mpmath as mp
mp.mp.dps = 80
def phi_q(q, x): return mp.cos(x)**2 + q*q*mp.sin(x)**2
def Mf(q, c, x): return x*x*mp.sin(x)**2/(q + c*phi_q(q, x))
def alpha1_of_c(q, c):
    f = lambda x: mp.atan(1/(q*mp.tan(x))) - c*x
    lo, hi = mp.mpf('0'), mp.pi/2 - mp.mpf('1e-14')
    for _ in range(400):
        mid = (lo+hi)/2
        if f(mid) > 0: lo = mid
        else: hi = mid
    return (lo+hi)/2
def alpha2_of_c(q, c):
    f = lambda x: mp.atan(-q*mp.tan(x)) - c*x
    lo, hi = mp.pi/2 + mp.mpf('1e-14'), mp.pi - mp.mpf('1e-14')
    for _ in range(400):
        mid = (lo+hi)/2
        if f(mid) > 0: lo = mid
        else: hi = mid
    return (lo+hi)/2
def Fe(q, c): return Mf(q, c, alpha1_of_c(q, c)) - Mf(q, c, alpha2_of_c(q, c))
for q in [1.0, 1.1, 1.3, 1.5, 1.7, 1.9, 2.0]:
    for c in [0.4, 0.42, 0.45, 0.48, 0.5]:
        Fpp = mp.diff(lambda t: Fe(q, t), mp.mpf(c), 2)
        flag = "OK" if Fpp > 0 else "FAIL"
        print("q=", q, "c=", c, "Fe''=", mp.nstr(Fpp, 12), flag)
