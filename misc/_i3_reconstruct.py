# -*- coding: utf-8 -*-
"""Reconstruct I3 exploration: J = G^2 + G' on 3D relaxed boxes."""
import math
import mpmath as mp

mp.mp.dps = 60

def Phi(x, q):
    return mp.cos(x)**2 + q*q*mp.sin(x)**2

def E(x, q):
    return mp.atan(1.0/(q*mp.tan(x)))

def O(x, q):
    if x < mp.pi/2:
        return mp.pi - mp.atan(q*mp.tan(x))
    if x == mp.pi/2:
        return mp.pi/2
    return mp.atan(-q*mp.tan(x))

def alpha1(q, c):
    # root of E(x) - c*x = 0 on (0, pi/2), f>0 on left side
    lo, hi = mp.mpf('1e-12'), mp.pi/2 - mp.mpf('1e-12')
    for _ in range(200):
        mid = (lo+hi)/2
        fv = E(mid, q) - c*mid
        if fv > 0:
            lo = mid
        else:
            hi = mid
    return (lo+hi)/2

def alpha2(q, c):
    # root of O(x) - c*x = 0 on (0, pi), f>0 on left side
    lo, hi = mp.mpf('1e-12'), mp.pi - mp.mpf('1e-12')
    for _ in range(200):
        mid = (lo+hi)/2
        ov = O(mid, q)
        fv = ov - c*mid
        if fv > 0:
            lo = mid
        else:
            hi = mid
    return (lo+hi)/2

def G(x, c, q):
    Ph = Phi(x, q)
    D = q + c*Ph
    W = 3 + 2*x/mp.tan(x)
    return -Ph*W/D + 2*c*x*Ph*(q*q-1)*mp.sin(x)*mp.cos(x)/(D*D)

def Gc(x, c, q):
    # partial derivative of G w.r.t. c (x held fixed)
    Ph = Phi(x, q)
    D = q + c*Ph
    W = 3 + 2*x/mp.tan(x)
    sc = mp.sin(x)*mp.cos(x)
    g1 = -Ph*W/D
    g2 = 2*c*x*Ph*(q*q-1)*sc/(D*D)
    dg1c = Ph*W*Ph/(D*D)
    dg2c = 2*x*Ph*(q*q-1)*sc/(D*D) - 2*(2*c*x*Ph*(q*q-1)*sc)*Ph/(D**3)
    return dg1c + dg2c

def Gx(x, c, q):
    # partial derivative of G w.r.t. x (c, q held fixed)
    # numerical
    h = mp.mpf('1e-7')
    return (G(x+h, c, q) - G(x-h, c, q))/(2*h)

def J_on_curve(x, c, q):
    Ph = Phi(x, q)
    D = q + c*Ph
    xp = -x*Ph/D
    Gv = G(x, c, q)
    Gpv = Gx(x, c, q)*xp + Gc(x, c, q)
    return Gv*Gv + Gpv

# sanity: alpha values
for q,c in [(1.0,0.5),(1.0,0.4),(2.0,0.5),(2.0,0.4),(1.5,0.45)]:
    print("q=%.2f c=%.2f alpha1=%.6f alpha2=%.6f" % (q,c,alpha1(q,c),alpha2(q,c)))

# J on the actual alpha curves
mn1 = mp.inf; mx1 = -mp.inf; mn2 = mp.inf; mx2 = -mp.inf
for i in range(21):
    q = 1 + i*0.05
    for j in range(21):
        c = 0.4 + j*0.005
        a1 = alpha1(q,c); a2 = alpha2(q,c)
        j1 = J_on_curve(a1,c,q); j2 = J_on_curve(a2,c,q)
        mn1 = min(mn1,j1); mx1 = max(mx1,j1)
        mn2 = min(mn2,j2); mx2 = max(mx2,j2)
print("J1 on curve: [%.4f, %.4f]" % (mn1,mx1))
print("J2 on curve: [%.4f, %.4f]" % (mn2,mx2))
