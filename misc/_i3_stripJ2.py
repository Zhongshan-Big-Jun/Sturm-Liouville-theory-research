# -*- coding: utf-8 -*-
"""Decomposition upper bound for J2_2d on gamma-strips."""
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

def strip_bounds(g0, g1, n=30):
    mnG=mp.inf; mxG=-mp.inf; mnGc=mp.inf; mxGc=-mp.inf; mnGx=mp.inf; mxGx=-mp.inf; mnxp=mp.inf; mxxp=-mp.inf
    for i in range(n+1):
        g = g0+(g1-g0)*i/n
        x = mp.pi - g
        for j in range(n+1):
            q = 1+1*j/n
            c = mp.atan(q*mp.tan(g))/(mp.pi-g)
            Ph = Phi(x,q); D = q+c*Ph
            vG=G(x,c,q); vGc=Gc(x,c,q); vGx=Gx(x,c,q); vxp=x*Ph/D
            mnG=min(mnG,vG); mxG=max(mxG,vG); mnGc=min(mnGc,vGc); mxGc=max(mxGc,vGc)
            mnGx=min(mnGx,vGx); mxGx=max(mxGx,vGx); mnxp=min(mnxp,vxp); mxxp=max(mxxp,vxp)
    # J <= mxG^2 + mxGc + Gx*xp upper: Gx>0, xp<0 => Gx*xp <= mxGx*(-mnxp)
    ub = mxG**2 + mxGc - mxGx*mnxp
    # better: Gx*xp <= mxGx * xp_max = mxGx*(-mnxp)? xp_max = -mnxp. yes.
    return mnG,mxG,mnGc,mxGc,mnGx,mxGx,mnxp,mxxp,ub

for (g0,g1) in [(mp.mpf('0.6557'),mp.mpf('0.75')),(mp.mpf('0.75'),mp.mpf('0.85')),(mp.mpf('0.85'),mp.mpf('0.95')),(mp.mpf('0.95'),mp.mpf('1.0472'))]:
    mnG,mxG,mnGc,mxGc,mnGx,mxGx,mnxp,mxxp,ub = strip_bounds(g0,g1)
    print("strip [%.3f,%.3f]: G[%.3f,%.3f] Gc[%.3f,%.3f] Gx[%.3f,%.3f] xp[%.3f,%.3f] -> J<=%.4f" % (g0,g1,mnG,mxG,mnGc,mxGc,mnGx,mxGx,mnxp,mxxp,ub))
