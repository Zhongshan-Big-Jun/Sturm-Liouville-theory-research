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
def Fe(c, q):  # the residual F_e(c)
    a1, a2 = phases(c, q)
    return Mf(a1,c,q) - Mf(a2,c,q)
def dFe(c, q):
    h = mp.mpf('1e-6')
    return (Fe(c+h,q) - Fe(c-h,q))/(2*h)

mn = mp.mpf('1e30')
ok = True
for qq in [mp.mpf('1.05'), mp.mpf('1.5'), mp.mpf('1.9')]:
    d12 = dFe(mp.mpf('0.5'), qq)
    assert d12 < 0
    for cc in [mp.mpf('0.41'), mp.mpf('0.45'), mp.mpf('0.49')]:
        dc = dFe(cc, qq)
        mn = min(mn, d12 - dc)
        assert dc < d12 < 0, (qq, cc, dc, d12)
print("Chain4: F_e'(q,c) < F_e'(q,1/2) < 0 on grid; min (Fep12 - Fep(c)) =", mn)

# cross-check J1>=6499/7500 and J2<0 along real curves inside (1,2)x(0.4,0.5)
def G(x, c, q):
    Phi = mp.cos(x)**2 + q*q*mp.sin(x)**2
    D = q + c*Phi
    return -Phi*(3+2*x*mp.cot(x))/D + 2*c*x*Phi*(q*q-1)*mp.sin(x)*mp.cos(x)/D**2
def J(x, c, q):
    Phi = mp.cos(x)**2 + q*q*mp.sin(x)**2
    D = q + c*Phi
    Gx = mp.diff(lambda xx: G(xx, c, q), x)
    Gc = mp.diff(lambda cc: G(x, cc, q), c)
    return G(x,c,q)**2 - (x*Phi/D)*Gx + Gc
mnJ1 = mp.mpf('1e30'); mxJ2 = mp.mpf('-1e30')
for qq in [mp.mpf('1.01')+mp.mpf('0.02')*k for k in range(50)]:
    for cc in [mp.mpf('0.401')+mp.mpf('0.002')*k for k in range(50)]:
        if cc >= mp.mpf('0.5'): break
        a1, a2 = phases(cc, qq)
        mnJ1 = min(mnJ1, J(a1, cc, qq))
        mxJ2 = max(mxJ2, J(a2, cc, qq))
print("real-curve cross-check: min J(alpha1) =", mnJ1, " (>6499/7500=", mp.mpf(6499)/7500, "):", mnJ1 > mp.mpf(6499)/7500)
print("real-curve cross-check: max J(alpha2) =", mxJ2, " < 0:", mxJ2 < 0)
