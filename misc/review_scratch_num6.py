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
def Fe(c, q):
    a1, a2 = phases(c, q)
    return Mf(a1,c,q) - Mf(a2,c,q)
h = mp.mpf('1e-6')
mn = mp.mpf('1e30')
for qq in [mp.mpf(1), mp.mpf('1.05'), mp.mpf('1.1'), mp.mpf('1.3'), mp.mpf('1.5'), mp.mpf('1.8'), mp.mpf(2)]:
    for cc in [mp.mpf('0.4'), mp.mpf('0.42'), mp.mpf('0.45'), mp.mpf('0.48'), mp.mpf('0.5')]:
        v = (Fe(cc+h,qq) - 2*Fe(cc,qq) + Fe(cc-h,qq))/h**2
        mn = min(mn, v)
        assert v > 0, (qq, cc, v)
print("Chain4: F_e''>0 on Q grid (central diff h=1e-6); min =", mn)

# also verify key-lemma conclusion F_e'(q,c) < F_e'(q,1/2) < 0 on a grid
mn2 = mp.mpf('1e30')
for qq in [mp.mpf('1.05'), mp.mpf('1.5'), mp.mpf('1.9')]:
    for cc in [mp.mpf('0.41'), mp.mpf('0.45'), mp.mpf('0.49')]:
        d = Fe(mp.mpf('0.5'),qq) - Fe(cc,qq)
        mn2 = min(mn2, d)
        assert Fe(cc,qq) < Fe(mp.mpf('0.5'),qq) and Fe(mp.mpf('0.5'),qq) < 0, (qq,cc,Fe(cc,qq),Fe(mp.mpf('0.5'),qq))
print("Chain4: F_e'(q,c) < F_e'(q,1/2) < 0 on grid; min (Fep12 - Fe) =", mn2)
