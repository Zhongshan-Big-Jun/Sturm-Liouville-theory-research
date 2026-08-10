# -*- coding: utf-8 -*-
"""2D parametrization: J1(x,q)=J(x,E(x)/x,q); J2(g,q)=J(pi-g, arctan(q*tan g)/(pi-g), q). Margins on 2D boxes."""
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

def E1(x,q): return mp.atan(1.0/(q*mp.tan(x)))
def J1_2d(x,q):
    c = E1(x,q)/x
    return Jfull(x,c,q)
def J2_2d(g,q):
    x = mp.pi - g
    c = mp.atan(q*mp.tan(g))/(mp.pi-g)
    return Jfull(x,c,q)

# J1 on 2D box [0.8411,1.1220]x[1,2]
mn=mp.inf; mx=-mp.inf; arg=None
for i in range(60+1):
    x = mp.mpf('0.8411')+(mp.mpf('1.1220')-mp.mpf('0.8411'))*i/60
    for j in range(60+1):
        q = 1+1*j/60
        v = J1_2d(x,q)
        if v<mn: mn=v; arg=(x,q)
        if v>mx: mx=v
print("J1_2d on [0.8411,1.1220]x[1,2]: [%.6f, %.6f] min at %s" % (mn,mx,arg))
# also c range on that box
mnc=mp.inf; mxc=-mp.inf
for i in range(30+1):
    x = mp.mpf('0.8411')+(mp.mpf('1.1220')-mp.mpf('0.8411'))*i/30
    for j in range(30+1):
        q = 1+1*j/30
        c = E1(x,q)/x
        mnc=min(mnc,c); mxc=max(mxc,c)
print("c1 range on box: [%.4f, %.4f]" % (mnc,mxc))

# J2 on 2D box [0.6557,1.0472]x[1,2]
mn=mp.inf; mx=-mp.inf; arg=None
for i in range(60+1):
    g = mp.mpf('0.6557')+(mp.mpf('1.0472')-mp.mpf('0.6557'))*i/60
    for j in range(60+1):
        q = 1+1*j/60
        v = J2_2d(g,q)
        if v>mx: mx=v; arg=(g,q)
        if v<mn: mn=v
print("J2_2d on [0.6557,1.0472]x[1,2]: [%.6f, %.6f] max at %s" % (mn,mx,arg))
mnc=mp.inf; mxc=-mp.inf
for i in range(30+1):
    g = mp.mpf('0.6557')+(mp.mpf('1.0472')-mp.mpf('0.6557'))*i/30
    for j in range(30+1):
        q = 1+1*j/30
        c = mp.atan(q*mp.tan(g))/(mp.pi-g)
        mnc=min(mnc,c); mxc=max(mxc,c)
print("c2 range on box: [%.4f, %.4f]" % (mnc,mxc))
