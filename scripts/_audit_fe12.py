# -*- coding: utf-8 -*-
import mpmath as mp
mp.mp.dps = 60
def phi_q(q, x): return mp.cos(x)**2 + q*q*mp.sin(x)**2
def Mf(q, c, x): return x*x*mp.sin(x)**2/(q + c*phi_q(q, x))
def alpha1_of_c(q, c):
    f = lambda x: mp.atan(1/(q*mp.tan(x))) - c*x
    lo, hi = mp.mpf('0'), mp.pi/2 - mp.mpf('1e-12')
    for _ in range(300):
        mid = (lo+hi)/2
        if f(mid) > 0: lo = mid
        else: hi = mid
    return (lo+hi)/2
def alpha2_of_c(q, c):
    f = lambda x: mp.atan(-q*mp.tan(x)) - c*x
    lo, hi = mp.pi/2 + mp.mpf('1e-12'), mp.pi - mp.mpf('1e-12')
    for _ in range(300):
        mid = (lo+hi)/2
        if f(mid) > 0: lo = mid
        else: hi = mid
    return (lo+hi)/2
def Fe(q, c): return Mf(q, c, alpha1_of_c(q, c)) - Mf(q, c, alpha2_of_c(q, c))
for q in [1.0, 1.5, 2.0]:
    x = 2*mp.asin(1/mp.sqrt(2*(q+1)))
    Fp_num = mp.diff(lambda t: Fe(q, t), mp.mpf('0.5'), 1)
    P = 3*x*x + 6*x*mp.sin(x) - 3*mp.pi*x - 3*mp.pi*mp.sin(x) + mp.pi*mp.pi
    formula = 2*mp.pi*(mp.cos(x)-1)**3/mp.sin(x)**3 * P
    print("q=", float(q))
    print("  x =", float(x), "pi/3 =", float(mp.pi/3))
    print("  Fp_num   =", mp.nstr(Fp_num, 20))
    print("  formula  =", mp.nstr(formula, 20))
    print("  P(x)     =", mp.nstr(P, 20))
    print("  ratio    =", mp.nstr(Fp_num/formula, 20))
