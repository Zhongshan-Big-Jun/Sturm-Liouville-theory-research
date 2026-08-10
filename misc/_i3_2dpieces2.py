# -*- coding: utf-8 -*-
"""Decomposition pieces on J2_2d box (g in [0.6557,1.0472], q in [1,2], c=atan(q tan g)/(pi-g))."""
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

g0,g1 = mp.mpf('0.6557'),mp.mpf('1.0472')
mnG=mp.inf; mxG=-mp.inf; mnGc=mp.inf; mxGc=-mp.inf; mnGx=mp.inf; mxGx=-mp.inf; mnxp=mp.inf; mxxp=-mp.inf
for i in range(50+1):
    g = g0+(g1-g0)*i/50
    x = mp.pi - g
    for j in range(50+1):
        q = 1+1*j/50
        c = mp.atan(q*mp.tan(g))/(mp.pi-g)
        Ph = Phi(x,q); D = q+c*Ph
        vG=G(x,c,q); vGc=Gc(x,c,q); vGx=Gx(x,c,q); vxp=x*Ph/D
        mnG=min(mnG,vG); mxG=max(mxG,vG); mnGc=min(mnGc,vGc); mxGc=max(mxGc,vGc)
        mnGx=min(mnGx,vGx); mxGx=max(mxGx,vGx); mnxp=min(mnxp,vxp); mxxp=max(mxxp,vxp)
print("J2 2D box pieces: G[%.4f,%.4f] Gc[%.4f,%.4f] Gx[%.4f,%.4f] xPhi/D[%.4f,%.4f]" % (mnG,mxG,mnGc,mxGc,mnGx,mxGx,mnxp,mxxp))
# J upper bound: G^2 + Gc + Gx*xp, xp<0
# G^2 max, Gc max, Gx*xp max = Gx_min * xp_max (both need care: Gx>0? on B2 Gx>0)
print("Gx sign on box: [%.4f, %.4f]" % (mnGx,mxGx))
# if Gx>0 and xp<0: Gx*xp <= Gx_min * xp_max? no: Gx*xp = -Gx*|xp| <= -Gx_min*|xp|_min
# need |xp|_min = -xPhi/D max... xp_max = -mnxp
ub = mxG**2 + mxGc - mnGx*(-mxxp)  # Gx*xp <= -mnGx*(-mxxp)? wait
# Gx>=mnGx>0, xp<=-mnxp<0 => Gx*xp <= mnGx*(-mnxp)  ... hmm no.
# Gx*xp <= Gx_max * xp_max (xp_max<0)?? For Gx>0: Gx*xp <= Gx_max*xp_max = mxGx*(-mnxp)
ub1 = mxG**2 + mxGc + mxGx*(-mnxp)
# and tighter: Gx*xp <= mnGx * xp_max since xp<0? No: for fixed xp<0, Gx*xp decreasing in Gx => max at Gx_min: Gx*xp <= mnGx*xp_max
ub2 = mxG**2 + mxGc + mnGx*(-mnxp)
print("upper bound variant1: %.4f + %.4f - %.4f*%.4f = %.4f" % (mxG**2, mxGc, mxGx, mnxp, ub1))
print("upper bound variant2: %.4f + %.4f - %.4f*%.4f = %.4f" % (mxG**2, mxGc, mnGx, mnxp, ub2))
