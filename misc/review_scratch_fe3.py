# -*- coding: utf-8 -*-
import mpmath as mp
mp.mp.dps = 80
pi = mp.pi

def phases(c, q):
    lo, hi = mp.mpf('1e-12'), pi/2
    f = lambda x: mp.atan(1/(q*mp.tan(x))) - c*x
    for _ in range(300):
        mid=(lo+hi)/2
        if f(mid)>0: lo=mid
        else: hi=mid
    a1=(lo+hi)/2
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

q = mp.mpf(1); c0 = mp.mpf('0.4')
for h in [mp.mpf('1e-3'), mp.mpf('1e-4'), mp.mpf('1e-5'), mp.mpf('1e-6'), mp.mpf('1e-8')]:
    d2 = (Fe(c0+h, q) - 2*Fe(c0, q) + Fe(c0-h, q))/h**2
    print("h =", h, " d2Fe =", d2)
print("mp.diff order2:", mp.diff(lambda c: Fe(c, q), c0, 2))
