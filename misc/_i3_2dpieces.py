# -*- coding: utf-8 -*-
"""Decomposition pieces on the 2D box with c=E(x)/x (J1_2d box)."""
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

x0,x1 = mp.mpf('0.8411'),mp.mpf('1.1220')
mnG=mp.inf; mxG=-mp.inf; mnGc=mp.inf; mxGc=-mp.inf; mnGx=mp.inf; mxGx=-mp.inf; mnxp=mp.inf; mxxp=-mp.inf
for i in range(50+1):
    x = x0+(x1-x0)*i/50
    for j in range(50+1):
        q = 1+1*j/50
        c = mp.atan(1.0/(q*mp.tan(x)))/x
        Ph = Phi(x,q); D = q+c*Ph
        vG=G(x,c,q); vGc=Gc(x,c,q); vGx=Gx(x,c,q); vxp=x*Ph/D
        mnG=min(mnG,vG); mxG=max(mxG,vG); mnGc=min(mnGc,vGc); mxGc=max(mxGc,vGc)
        mnGx=min(mnGx,vGx); mxGx=max(mxGx,vGx); mnxp=min(mnxp,vxp); mxxp=max(mxxp,vxp)
print("2D box pieces: G[%.4f,%.4f] Gc[%.4f,%.4f] Gx[%.4f,%.4f] xPhi/D[%.4f,%.4f]" % (mnG,mxG,mnGc,mxGc,mnGx,mxGx,mnxp,mxxp))
# J lower bound from decomposition: G^2 + Gc + Gx*(-xp)
print("decomp lower bound at extremes: %.4f + %.4f - %.4f*%.4f = %.4f" % (mxG**2 if mxG<0 else mnG**2, mnGc, mxGx, mxxp, (mxG**2 if mxG<0 else mnG**2)+mnGc-mxGx*mxxp))
