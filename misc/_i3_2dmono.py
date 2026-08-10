# -*- coding: utf-8 -*-
"""Monotonicity of J1_2d(x,q) and J2_2d(g,q)."""
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
def J1_2d(x,q):
    return Jfull(x, mp.atan(1.0/(q*mp.tan(x)))/x, q)
def J2_2d(g,q):
    return Jfull(mp.pi-g, mp.atan(q*mp.tan(g))/(mp.pi-g), q)

def d1(f, var, a, b):
    h=mp.mpf('1e-6')
    if var=='x': return (f(a+h,b)-f(a-h,b))/(2*h)
    if var=='q': return (f(a,b+h)-f(a,b-h))/(2*h)

# J1_2d derivatives on box
mnx=mp.inf; mxx=-mp.inf; mnq=mp.inf; mxq=-mp.inf
for i in range(30+1):
    x = mp.mpf('0.8411')+(mp.mpf('1.1220')-mp.mpf('0.8411'))*i/30
    for j in range(30+1):
        q = 1+1*j/30
        vx = d1(J1_2d,'x',x,q); vq = d1(J1_2d,'q',x,q)
        mnx=min(mnx,vx); mxx=max(mxx,vx); mnq=min(mnq,vq); mxq=max(mxq,vq)
print("J1_2d d/dx: [%.4f, %.4f]; d/dq: [%.4f, %.4f]" % (mnx,mxx,mnq,mxq))

# J2_2d derivatives on box
mnx=mp.inf; mxx=-mp.inf; mnq=mp.inf; mxq=-mp.inf
for i in range(30+1):
    g = mp.mpf('0.6557')+(mp.mpf('1.0472')-mp.mpf('0.6557'))*i/30
    for j in range(30+1):
        q = 1+1*j/30
        vg = d1(J2_2d,'x',g,q); vq = d1(J2_2d,'q',g,q)
        mnx=min(mnx,vg); mxx=max(mxx,vg); mnq=min(mnq,vq); mxq=max(mxq,vq)
print("J2_2d d/dg: [%.4f, %.4f]; d/dq: [%.4f, %.4f]" % (mnx,mxx,mnq,mxq))
