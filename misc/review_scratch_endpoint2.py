# -*- coding: utf-8 -*-
import mpmath as mp
mp.mp.dps = 60
pi = mp.pi

def phases(c, q):
    # alpha1 in (0,pi/2): f decreasing
    lo, hi = mp.mpf('1e-12'), pi/2
    f = lambda x: mp.atan(1/(q*mp.tan(x))) - c*x
    for _ in range(300):
        mid=(lo+hi)/2
        if f(mid)>0: lo=mid   # root to the right
        else: hi=mid
    a1=(lo+hi)/2
    # alpha2 in (pi/2,pi): f decreasing
    lo, hi = pi/2 + mp.mpf('1e-12'), pi - mp.mpf('1e-12')
    f = lambda x: mp.atan(-q*mp.tan(x)) - c*x
    for _ in range(300):
        mid=(lo+hi)/2
        if f(mid)>0: lo=mid
        else: hi=mid
    return a1, (lo+hi)/2

def Mf(x, c, q):
    return x*x*mp.sin(x)**2/(q + c*(mp.cos(x)**2 + q*q*mp.sin(x)**2))
def Fe(c, q):
    a1, a2 = phases(c, q)
    return Mf(a1,c,q) - Mf(a2,c,q)
def G(x, c, q):
    Phi = mp.cos(x)**2 + q*q*mp.sin(x)**2
    D = q + c*Phi
    return -Phi*(3+2*x*mp.cot(x))/D + 2*c*x*Phi*(q*q-1)*mp.sin(x)*mp.cos(x)/D**2

for qq in [mp.mpf('1.1'), mp.mpf('1.5'), mp.mpf('2.0')]:
    dFe = mp.diff(lambda c: Fe(c, qq), mp.mpf('0.5'))
    a1, a2 = phases(mp.mpf('0.5'), qq)
    viaG = Mf(a1,mp.mpf('0.5'),qq)*G(a1,mp.mpf('0.5'),qq) - Mf(a2,mp.mpf('0.5'),qq)*G(a2,mp.mpf('0.5'),qq)
    x = 2*mp.asin(1/mp.sqrt(2*(qq+1)))
    P = (pi-3*x)**2 + 3*(x-mp.sin(x))*(pi-2*x)
    closed = 2*pi*(mp.cos(x)-1)**3/mp.sin(x)**3*P
    print("q=",qq)
    print("  a1, a2, x =", a1, a2, x)
    print("  dFe(direct) =", dFe)
    print("  viaG        =", viaG)
    print("  closed form =", closed)
    print("  |closed-dFe| =", abs(closed-dFe))
