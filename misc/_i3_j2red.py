# -*- coding: utf-8 -*-
"""J2_2d reduction: J(pi/3, q), J(0.6557, q), thin strip max."""
import mpmath as mp
mp.mp.dps = 40
def Phi(x, q): return mp.cos(x)**2 + q*q*mp.sin(x)**2
def G(x, c, q):
    Ph = Phi(x, q); D = q + c*Ph; W = 3 + 2*x/mp.tan(x)
    return -Ph*W/D + 2*c*x*Ph*(q*q-1)*mp.sin(x)*mp.cos(x)/(D*D)
def Jfull(x, c, q):
    Ph = Phi(x, q); D = q + c*Ph; xp = -x*Ph/D
    W = 3 + 2*x/mp.tan(x)
    Gv = G(x, c, q)
    h = mp.mpf('1e-6')
    Gpv = ((G(x+h,c,q)-G(x-h,c,q))/(2*h))*xp
    sc = mp.sin(x)*mp.cos(x)
    Gc_ = Ph*W*Ph/(D*D) + 2*x*Ph*(q*q-1)*sc/(D*D) - 2*(2*c*x*Ph*(q*q-1)*sc)*Ph/(D**3)
    return Gv*Gv + Gpv + Gc_
def J2(g,q):
    return Jfull(mp.pi-g, mp.atan(q*mp.tan(g))/(mp.pi-g), q)

# J(pi/3, q) for q in [1,2]
mn=mp.inf; mx=-mp.inf
for i in range(400+1):
    q = 1+1*i/400
    v = J2(mp.pi/3, q)
    mn=min(mn,v); mx=max(mx,v)
print("J2(pi/3, q) on [1,2]: [%.6f, %.6f]" % (mn,mx))
# J(0.6557, q)
mn=mp.inf; mx=-mp.inf
for i in range(400+1):
    q = 1+1*i/400
    v = J2(mp.mpf('0.6557'), q)
    mn=min(mn,v); mx=max(mx,v)
print("J2(0.6557, q) on [1,2]: [%.6f, %.6f]" % (mn,mx))
# thin strip g in [0.6557, 0.695], q in [1,2]: max
mx=-mp.inf; arg=None
for i in range(60+1):
    g = mp.mpf('0.6557')+(mp.mpf('0.695')-mp.mpf('0.6557'))*i/60
    for j in range(60+1):
        q = 1+1*j/60
        v = J2(g,q)
        if v>mx: mx=v; arg=(g,q)
print("strip [0.6557,0.695]x[1,2]: J2 max %.6f at %s" % (mx,arg))
# main region g in [0.695, pi/3]: max
mx=-mp.inf; arg=None
for i in range(60+1):
    g = mp.mpf('0.695')+(mp.pi/3-mp.mpf('0.695'))*i/60
    for j in range(60+1):
        q = 1+1*j/60
        v = J2(g,q)
        if v>mx: mx=v; arg=(g,q)
print("region [0.695,pi/3]x[1,2]: J2 max %.6f at %s" % (mx,arg))
# where does dJ2/dg change sign on the strip? scan finer
for g0 in [mp.mpf('0.656'), mp.mpf('0.66'), mp.mpf('0.67'), mp.mpf('0.68'), mp.mpf('0.69')]:
    mnv=mp.inf; mxv=-mp.inf
    h=mp.mpf('1e-6')
    for j in range(20+1):
        q = 1+1*j/20
        v = (J2(g0+h,q)-J2(g0-h,q))/(2*h)
        mnv=min(mnv,v); mxv=max(mxv,v)
    print("dJ2/dg at g=%.3f: [%.3f, %.3f]" % (g0,mnv,mxv))
