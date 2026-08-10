# -*- coding: utf-8 -*-
"""3D relaxed box scan for J on B1 (alpha1 box) and B2 (alpha2 box)."""
import mpmath as mp
mp.mp.dps = 50

def Phi(x, q):
    return mp.cos(x)**2 + q*q*mp.sin(x)**2

def G(x, c, q):
    Ph = Phi(x, q)
    D = q + c*Ph
    W = 3 + 2*x/mp.tan(x)
    return -Ph*W/D + 2*c*x*Ph*(q*q-1)*mp.sin(x)*mp.cos(x)/(D*D)

def Gc(x, c, q):
    Ph = Phi(x, q)
    D = q + c*Ph
    W = 3 + 2*x/mp.tan(x)
    sc = mp.sin(x)*mp.cos(x)
    dg1c = Ph*W*Ph/(D*D)
    dg2c = 2*x*Ph*(q*q-1)*sc/(D*D) - 2*(2*c*x*Ph*(q*q-1)*sc)*Ph/(D**3)
    return dg1c + dg2c

def Gx(x, c, q):
    h = mp.mpf('1e-6')
    return (G(x+h, c, q) - G(x-h, c, q))/(2*h)

def J(x, c, q):
    Ph = Phi(x, q)
    D = q + c*Ph
    xp = -x*Ph/D
    Gv = G(x, c, q)
    Gpv = Gx(x, c, q)*xp + Gc(x, c, q)
    return Gv*Gv + Gpv

def scan(x0,x1,nx,q0,q1,nq,c0,c1,nc):
    mn = mp.inf; mx = -mp.inf; arg = None
    for i in range(nx+1):
        x = x0 + (x1-x0)*i/nx
        for j in range(nq+1):
            q = q0 + (q1-q0)*j/nq
            for k in range(nc+1):
                c = c0 + (c1-c0)*k/nc
                v = J(x,c,q)
                if v < mn: mn = v; arg = (x,c,q)
                if v > mx: mx = v
    return mn, mx, arg

mn1,mx1,arg1 = scan(mp.mpf('0.8411'),mp.mpf('1.1220'),30,mp.mpf(1),mp.mpf(2),30,mp.mpf('0.4'),mp.mpf('0.5'),30)
print("B1 (alpha1 box) J: min=%.6f max=%.6f at %s" % (mn1,mx1,arg1))
mn2,mx2,arg2 = scan(mp.mpf('2.0944'),mp.mpf('2.4859'),30,mp.mpf(1),mp.mpf(2),30,mp.mpf('0.4'),mp.mpf('0.5'),30)
print("B2 (alpha2 box) J: min=%.6f max=%.6f at %s" % (mn2,mx2,arg2))
