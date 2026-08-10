# -*- coding: utf-8 -*-
"""Gx range on B1/B2; J on c=0.5 face of B2 (fixed W bug)."""
import mpmath as mp
mp.mp.dps = 40

def Phi(x, q): return mp.cos(x)**2 + q*q*mp.sin(x)**2
def G(x, c, q):
    Ph = Phi(x, q); D = q + c*Ph; W = 3 + 2*x/mp.tan(x)
    return -Ph*W/D + 2*c*x*Ph*(q*q-1)*mp.sin(x)*mp.cos(x)/(D*D)
def Gx(x, c, q):
    h = mp.mpf('1e-6')
    return (G(x+h, c, q) - G(x-h, c, q))/(2*h)
def J(x, c, q):
    Ph = Phi(x, q); D = q + c*Ph; xp = -x*Ph/D
    W = 3 + 2*x/mp.tan(x)
    Gv = G(x, c, q)
    h = mp.mpf('1e-6')
    Gpv = ((G(x+h,c,q)-G(x-h,c,q))/(2*h))*xp
    sc = mp.sin(x)*mp.cos(x)
    Gc_ = Ph*W*Ph/(D*D) + 2*x*Ph*(q*q-1)*sc/(D*D) - 2*(2*c*x*Ph*(q*q-1)*sc)*Ph/(D**3)
    return Gv*Gv + Gpv + Gc_

def ranges2(f, x0,x1,nx, q0,q1,nq):
    mn=mp.inf; mx=-mp.inf; arg=None
    for i in range(nx+1):
        x = x0+(x1-x0)*i/nx
        for j in range(nq+1):
            q = q0+(q1-q0)*j/nq
            v = f(x,q)
            if v>mx: mx=v; arg=(x,q)
            if v<mn: mn=v
    return mn,mx,arg

mn,mx,arg = ranges2(lambda x,q: J(x,mp.mpf('0.5'),q), mp.mpf('2.0944'),mp.mpf('2.4859'),60, mp.mpf(1),mp.mpf(2),60)
print("B2 face c=0.5: J in [%.4f, %.4f], max at %s" % (mn,mx,arg))
mn,mx,arg = ranges2(lambda x,q: J(x,mp.mpf('0.5'),q), mp.mpf('0.8411'),mp.mpf('1.1220'),60, mp.mpf(1),mp.mpf(2),60)
print("B1 face c=0.5: J in [%.4f, %.4f], max at %s" % (mn,mx,arg))
mn,mx,arg = ranges2(lambda x,q: J(x,mp.mpf('0.4'),q), mp.mpf('2.0944'),mp.mpf('2.4859'),60, mp.mpf(1),mp.mpf(2),60)
print("B2 face c=0.4: J in [%.4f, %.4f], max at %s" % (mn,mx,arg))
