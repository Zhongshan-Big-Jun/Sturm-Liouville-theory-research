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

# F_e'' > 0 on Q grid (numerical second derivative)
mn = mp.mpf('1e30')
for qq in [mp.mpf(1), mp.mpf('1.1'), mp.mpf('1.3'), mp.mpf('1.5'), mp.mpf('1.8'), mp.mpf(2)]:
    for cc in [mp.mpf('0.4'), mp.mpf('0.42'), mp.mpf('0.45'), mp.mpf('0.48'), mp.mpf('0.5')]:
        v = mp.diff(lambda c: Fe(c, qq), cc, 2)
        mn = min(mn, v)
        assert v > 0, (qq, cc, v)
print("Chain4: F_e''>0 on Q grid; min =", mn)

# J1^(2) >= 6499/7500 and J2^(2) < 0 cross-checks
# J(x;c) = G^2 - (x Phi/(q+cPhi)) G_x + G_c ; J1^(2)(x,q)=J(x; c1(x,q))
def J(x, c, q):
    Phi = mp.cos(x)**2 + q*q*mp.sin(x)**2
    D = q + c*Phi
    # G_x: differentiate G symbolically? do numeric
    Gv = lambda xx: G(xx, c, q)
    Gx = mp.diff(Gv, x)
    Gc = mp.diff(lambda cc: G(x, cc, q), c)
    return Gv(x)**2 - (x*Phi/D)*Gx + Gc
def c1(x, q):
    return mp.atan(1/(q*mp.tan(x)))/x
mnJ1 = mp.mpf('1e30'); mxJ2 = mp.mpf('-1e30')
for qq in [mp.mpf(1)+mp.mpf(k)/100 for k in range(1,101)]:
    for x in [mp.mpf('0.841')+mp.mpf('0.001')*k for k in range(0,282)]:
        cc = c1(x, qq)
        if mp.mpf('0.4') < cc < mp.mpf('0.5') and x < mp.mpf('1.1220'):
            mnJ1 = min(mnJ1, J(x, cc, qq))
    for gam in [mp.mpf('0.655')+mp.mpf('0.0005')*k for k in range(0,785)]:
        if gam > mp.mpf('1.0472'): break
        cc = mp.atan(qq*mp.tan(gam))/(pi-gam)
        if mp.mpf('0.4') < cc < mp.mpf('0.5'):
            mxJ2 = max(mxJ2, J(pi-gam, cc, qq))
print("J1^(2) min on T1 (grid) =", mnJ1, " >= 6499/7500 =", mp.mpf(6499)/7500)
print("J2^(2) max on T2 (grid) =", mxJ2, " < 0:", mxJ2 < 0)
