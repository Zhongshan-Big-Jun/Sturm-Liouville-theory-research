# -*- coding: utf-8 -*-
"""J1/J2 extrema on the actual alpha curves over Q=[1,2]x[0.4,0.5]."""
import mpmath as mp
mp.mp.dps = 40

def Phi(x, q): return mp.cos(x)**2 + q*q*mp.sin(x)**2
def E(x, q): return mp.atan(1.0/(q*mp.tan(x)))
def O(x, q):
    if x < mp.pi/2: return mp.pi - mp.atan(q*mp.tan(x))
    if x == mp.pi/2: return mp.pi/2
    return mp.atan(-q*mp.tan(x))
def alpha1(q, c):
    lo, hi = mp.mpf('1e-12'), mp.pi/2 - mp.mpf('1e-12')
    for _ in range(200):
        mid = (lo+hi)/2
        if E(mid,q) - c*mid > 0: lo = mid
        else: hi = mid
    return (lo+hi)/2
def alpha2(q, c):
    lo, hi = mp.mpf('1e-12'), mp.pi - mp.mpf('1e-12')
    for _ in range(200):
        mid = (lo+hi)/2
        if O(mid,q) - c*mid > 0: lo = mid
        else: hi = mid
    return (lo+hi)/2
def G(x, c, q):
    Ph = Phi(x, q); D = q + c*Ph; W = 3 + 2*x/mp.tan(x)
    return -Ph*W/D + 2*c*x*Ph*(q*q-1)*mp.sin(x)*mp.cos(x)/(D*D)
def J(x, c, q):
    Ph = Phi(x, q); D = q + c*Ph; xp = -x*Ph/D
    W = 3 + 2*x/mp.tan(x)
    Gv = G(x, c, q)
    h = mp.mpf('1e-6')
    Gpv = ((G(x+h,c,q)-G(x-h,c,q))/(2*h))*xp
    sc = mp.sin(x)*mp.cos(x)
    Gc_ = Ph*W*Ph/(D*D) + 2*x*Ph*(q*q-1)*sc/(D*D) - 2*(2*c*x*Ph*(q*q-1)*sc)*Ph/(D**3)
    return Gv*Gv + Gpv + Gc_

mn1=mp.inf; arg1=None; mx2=-mp.inf; arg2=None
for i in range(101):
    q = 1+1*i/100
    for j in range(101):
        c = mp.mpf('0.4')+mp.mpf('0.1')*j/100
        a1 = alpha1(q,c); a2 = alpha2(q,c)
        j1 = J(a1,c,q); j2 = J(a2,c,q)
        if j1<mn1: mn1=j1; arg1=(q,c,a1)
        if j2>mx2: mx2=j2; arg2=(q,c,a2)
print("J1 min on curve: %.6f at (q,c,a1)=%s" % (mn1,arg1))
print("J2 max on curve: %.6f at (q,c,a2)=%s" % (mx2,arg2))

# dJ1/dq and dJ2/dq on curves (total derivative along curve, c fixed)
def dJdq_oncurve(k, q, c):
    h = mp.mpf('1e-6')
    a = alpha1(q,c) if k==1 else alpha2(q,c)
    a2_ = alpha1(q+h,c) if k==1 else alpha2(q+h,c)
    a1_ = alpha1(q-h,c) if k==1 else alpha2(q-h,c)
    return (J(a2_,c,q+h) - J(a1_,c,q-h))/(2*h)
mn1=mp.inf; arg1=None; mx2=-mp.inf; arg2=None
for i in range(41):
    q = 1+1*i/40
    for j in range(41):
        c = mp.mpf('0.4')+mp.mpf('0.1')*j/40
        v1 = dJdq_oncurve(1,q,c); v2 = dJdq_oncurve(2,q,c)
        if v1<mn1: mn1=v1; arg1=(q,c)
        if v2>mx2: mx2=v2; arg2=(q,c)
print("dJ1/dq on curve: min %.4f at %s" % (mn1,arg1))
print("dJ2/dq on curve: max %.4f at %s" % (mx2,arg2))
