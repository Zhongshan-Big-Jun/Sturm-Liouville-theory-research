# -*- coding: utf-8 -*-
import mpmath as mp
mp.mp.dps = 90
def phi_q(q, x): return mp.cos(x)**2 + q*q*mp.sin(x)**2
def Mf(q, c, x): return x*x*mp.sin(x)**2/(q + c*phi_q(q, x))

def alpha1_of_c(q, c):
    f = lambda x: mp.atan(1/(q*mp.tan(x))) - c*x
    lo, hi = mp.mpf('1e-20'), mp.pi/2 - mp.mpf('1e-20')
    for _ in range(100):
        mid = (lo+hi)/2
        if f(mid) > 0: lo = mid
        else: hi = mid
    x0 = (lo+hi)/2
    return mp.findroot(f, x0, tol=mp.mpf('1e-80'))

def alpha2_of_c(q, c):
    f = lambda x: mp.atan(-q*mp.tan(x)) - c*x
    lo, hi = mp.pi/2 + mp.mpf('1e-20'), mp.pi - mp.mpf('1e-20')
    for _ in range(100):
        mid = (lo+hi)/2
        if f(mid) > 0: lo = mid
        else: hi = mid
    x0 = (lo+hi)/2
    return mp.findroot(f, x0, tol=mp.mpf('1e-80'))

def Fe(q, c): return Mf(q, c, alpha1_of_c(q, c)) - Mf(q, c, alpha2_of_c(q, c))

bad = 0
for q in [1.0, 1.1, 1.3, 1.5, 1.7, 1.9, 2.0]:
    for c in [0.4, 0.42, 0.45, 0.48, 0.5]:
        Fpp = mp.diff(lambda t: Fe(q, t), mp.mpf(c), 2)
        if Fpp <= 0: bad += 1
        print("q=", q, "c=", c, "Fe''=", mp.nstr(Fpp, 10), "OK" if Fpp > 0 else "FAIL")
print("bad:", bad)
