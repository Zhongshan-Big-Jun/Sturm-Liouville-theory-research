# -*- coding: utf-8 -*-
import mpmath as mp
mp.mp.dps = 60
pi = mp.pi

def phases(c, q):
    lo, hi = mp.mpf('1e-12'), pi/2
    f = lambda x: mp.atan(1/(q*mp.tan(x))) - c*x
    for _ in range(200):
        mid=(lo+hi)/2
        if f(mid)>0: lo=mid
        else: hi=mid
    a1=(lo+hi)/2
    lo, hi = pi/2 + mp.mpf('1e-12'), pi - mp.mpf('1e-12')
    f = lambda x: mp.atan(-q*mp.tan(x)) - c*x
    for _ in range(200):
        mid=(lo+hi)/2
        if f(mid)>0: lo=mid
        else: hi=mid
    return a1, (lo+hi)/2

def Mf(x, c, q):
    return x*x*mp.sin(x)**2/(q + c*(mp.cos(x)**2 + q*q*mp.sin(x)**2))
def G(x, c, q):
    Phi = mp.cos(x)**2 + q*q*mp.sin(x)**2
    D = q + c*Phi
    return -Phi*(3+2*x*mp.cot(x))/D + 2*c*x*Phi*(q*q-1)*mp.sin(x)*mp.cos(x)/D**2
def Fe(c, q):
    a1, a2 = phases(c, q)
    return Mf(a1,c,q) - Mf(a2,c,q)
def J(x, c, q):
    Phi = mp.cos(x)**2 + q*q*mp.sin(x)**2
    D = q + c*Phi
    Gv = lambda xx: G(xx, c, q)
    Gx = mp.diff(Gv, x)
    Gc = mp.diff(lambda cc: G(x, cc, q), c)
    return Gv(x)**2 - (x*Phi/D)*Gx + Gc

for (qq, cc) in [(mp.mpf(1), mp.mpf('0.4')), (mp.mpf(1), mp.mpf('0.5')),
                 (mp.mpf('1.01'), mp.mpf('0.4')), (mp.mpf('1.1'), mp.mpf('0.4'))]:
    a1, a2 = phases(cc, qq)
    F2 = Mf(a1,cc,qq)*J(a1,cc,qq) - Mf(a2,cc,qq)*J(a2,cc,qq)
    F2d = mp.diff(lambda c: Fe(c, qq), cc, 2)
    print("q,c =", qq, cc)
    print("  a1, a2 =", a1, a2)
    print("  analytic F'' = Mf1 J1 - Mf2 J2 =", F2)
    print("  numeric d^2 Fe =", F2d)
    print("  J1 =", J(a1,cc,qq), " J2 =", J(a2,cc,qq), " Mf1 =", Mf(a1,cc,qq), " Mf2 =", Mf(a2,cc,qq))
    print("  c1(x1,q) =", mp.atan(1/(qq*mp.tan(a1)))/a1)
