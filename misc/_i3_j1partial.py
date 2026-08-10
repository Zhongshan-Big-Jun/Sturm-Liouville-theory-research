# -*- coding: utf-8 -*-
"""Jx, Jc, Jq on the J1_2d 2D box (c=E(x)/x) and J2_2d box."""
import mpmath as mp
mp.mp.dps = 40
def Phi(x, q): return mp.cos(x)**2 + q*q*mp.sin(x)**2
def G(x, c, q):
    Ph = Phi(x, q); D = q + c*Ph; W = 3 + 2*x/mp.tan(x)
    return -Ph*W/D + 2*c*x*Ph*(q*q-1)*mp.sin(x)*mp.cos(x)/(D*D)
def Gc(x, c, q):
    Ph = Phi(x, q); D = q + c*Ph; W = 3 + 2*x/mp.tan(x)
    sc = mp.sin(x)*mp.cos(x)
    return Ph*W*Ph/(D*D) + 2*x*Ph*(q*q-1)*sc/(D*D) - 2*(2*c*x*Ph*(q*q-1)*sc)*Ph/(D**3)
def Gx(x, c, q):
    h = mp.mpf('1e-6')
    return (G(x+h, c, q) - G(x-h, c, q))/(2*h)
def Jfull(x, c, q):
    Ph = Phi(x, q); D = q + c*Ph; xp = -x*Ph/D
    W = 3 + 2*x/mp.tan(x)
    Gv = G(x, c, q)
    h = mp.mpf('1e-6')
    Gpv = ((G(x+h,c,q)-G(x-h,c,q))/(2*h))*xp
    sc = mp.sin(x)*mp.cos(x)
    Gc_ = Ph*W*Ph/(D*D) + 2*x*Ph*(q*q-1)*sc/(D*D) - 2*(2*c*x*Ph*(q*q-1)*sc)*Ph/(D**3)
    return Gv*Gv + Gpv + Gc_

def scan2(f, x0,x1,q0,q1,n=40):
    mn=mp.inf; mx=-mp.inf
    for i in range(n+1):
        x = x0+(x1-x0)*i/n
        for j in range(n+1):
            q = q0+(q1-q0)*j/n
            v = f(x,q)
            mn=min(mn,v); mx=max(mx,v)
    return mn,mx

# J1_2d box: c = atan(1/(q tan x))/x
def c1(x,q): return mp.atan(1.0/(q*mp.tan(x)))/x
def Jx1(x,q):
    h=mp.mpf('1e-6'); return (Jfull(x+h,c1(x+h,q),q)-Jfull(x-h,c1(x-h,q),q))/(2*h)
def Jc1(x,q):
    h=mp.mpf('1e-6'); return (Jfull(x,c1(x,q)+h,q)-Jfull(x,c1(x,q)-h,q))/(2*h)
def Jq1(x,q):
    h=mp.mpf('1e-6'); return (Jfull(x,c1(x,q),q+h)-Jfull(x,c1(x,q),q-h))/(2*h)
x0,x1 = mp.mpf('0.8411'),mp.mpf('1.1220')
mn,mx = scan2(Jx1,x0,x1,mp.mpf(1),mp.mpf(2))
print("J1_2d Jx (partial): [%.4f, %.4f]" % (mn,mx))
mn,mx = scan2(Jc1,x0,x1,mp.mpf(1),mp.mpf(2))
print("J1_2d Jc (partial): [%.4f, %.4f]" % (mn,mx))
mn,mx = scan2(Jq1,x0,x1,mp.mpf(1),mp.mpf(2))
print("J1_2d Jq (partial): [%.4f, %.4f]" % (mn,mx))

# dc/dx on box
mn=mp.inf; mx=-mp.inf
for i in range(40+1):
    x = x0+(x1-x0)*i/40
    for j in range(40+1):
        q = 1+1*j/40
        h=mp.mpf('1e-6')
        v=(c1(x+h,q)-c1(x-h,q))/(2*h)
        mn=min(mn,v); mx=max(mx,v)
print("dc1/dx: [%.4f, %.4f]" % (mn,mx))
