# -*- coding: utf-8 -*-
"""J(x,0.5,q) on B2 face: strip margins + piece structure."""
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
def J(x, c, q):
    Ph = Phi(x, q); D = q + c*Ph; xp = -x*Ph/D
    W = 3 + 2*x/mp.tan(x)
    Gv = G(x, c, q)
    Gpv = Gx(x, c, q)*xp
    sc = mp.sin(x)*mp.cos(x)
    Gc_ = Ph*W*Ph/(D*D) + 2*x*Ph*(q*q-1)*sc/(D*D) - 2*(2*c*x*Ph*(q*q-1)*sc)*Ph/(D**3)
    return Gv*Gv + Gpv + Gc_

c05 = mp.mpf('0.5')
for (x0,x1) in [(mp.mpf('2.0944'),mp.mpf('2.20')),(mp.mpf('2.20'),mp.mpf('2.30')),(mp.mpf('2.30'),mp.mpf('2.40')),(mp.mpf('2.40'),mp.mpf('2.4859'))]:
    mx=-mp.inf; arg=None
    for i in range(40+1):
        x = x0+(x1-x0)*i/40
        for j in range(40+1):
            q = 1+1*j/40
            v = J(x,c05,q)
            if v>mx: mx=v; arg=(x,q)
    print("face strip [%.3f,%.3f]: J max %.6f at %s" % (x0,x1,mx,arg))

# piece ranges on the whole face c=0.5
mnG=mp.inf; mxG=-mp.inf; mnGc=mp.inf; mxGc=-mp.inf; mnGx=mp.inf; mxGx=-mp.inf; mnxp=mp.inf; mxxp=-mp.inf
for i in range(20+1):
    x = mp.mpf('2.0944')+(mp.mpf('2.4859')-mp.mpf('2.0944'))*i/20
    for j in range(20+1):
        q = 1+1*j/20
        Ph = Phi(x,q); D = q+c05*Ph
        vG=G(x,c05,q); vGc=Gc(x,c05,q); vGx=Gx(x,c05,q); vxp=-x*Ph/D
        mnG=min(mnG,vG); mxG=max(mxG,vG); mnGc=min(mnGc,vGc); mxGc=max(mxGc,vGc)
        mnGx=min(mnGx,vGx); mxGx=max(mxGx,vGx); mnxp=min(mnxp,vxp); mxxp=max(mxxp,vxp)
print("face c=0.5 pieces: G[%.3f,%.3f] Gc[%.3f,%.3f] Gx[%.3f,%.3f] xp[%.3f,%.3f]" % (mnG,mxG,mnGc,mxGc,mnGx,mxGx,mnxp,mxxp))
