# -*- coding: utf-8 -*-
"""Candidate lemmas for B1: verify margins for decomposition route and monotone route."""
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
def xp(x, c, q):
    Ph = Phi(x, q); D = q + c*Ph
    return -x*Ph/D
def J(x, c, q):
    Ph = Phi(x, q); D = q + c*Ph; W = 3 + 2*x/mp.tan(x)
    Gv = G(x, c, q)
    Gpv = Gx(x, c, q)*(-x*Ph/D)
    sc = mp.sin(x)*mp.cos(x)
    Gc_ = Ph*W*Ph/(D*D) + 2*x*Ph*(q*q-1)*sc/(D*D) - 2*(2*c*x*Ph*(q*q-1)*sc)*Ph/(D**3)
    return Gv*Gv + Gpv + Gc_

x0,x1,q0,q1,c0,c1 = mp.mpf('0.8411'),mp.mpf('1.1220'),mp.mpf(1),mp.mpf(2),mp.mpf('0.4'),mp.mpf('0.5')
def scan3d(f, n=10):
    mn=mp.inf; mx=-mp.inf; arg=None
    for i in range(n+1):
        x = x0+(x1-x0)*i/n
        for j in range(n+1):
            q = q0+(q1-q0)*j/n
            for k in range(n+1):
                c = c0+(c1-c0)*k/n
                v = f(x,c,q)
                if v<mn: mn=v; argmn=(x,c,q)
                if v>mx: mx=v; argmx=(x,c,q)
    return mn,mx,argmn,argmx

mn,mx,_,argmx = scan3d(G)
print("G on B1: [%.6f, %.6f] max at %s" % (mn,mx,argmx))
mn,mx,_,argmx = scan3d(Gc)
print("Gc on B1: [%.6f, %.6f] min-loc check" % (mn,mx))
mn,mx,_,argmx = scan3d(Gx)
print("Gx on B1: [%.6f, %.6f] max at %s" % (mn,mx,argmx))
mn,mx,_,argmx = scan3d(lambda x,c,q: -xp(x,c,q))
print("xPhi/D on B1: [%.6f, %.6f] max at %s" % (mn,mx,argmx))
# J lower bound pieces at worst combo
mnJ, mxJ, argmn, _ = scan3d(J)
print("J on B1: [%.6f, %.6f] min at %s" % (mnJ,mxJ,argmn))

# G on face c=0.5: max
mn,mx,_,argmx = scan3d(lambda x,c,q: G(x,mp.mpf('0.5'),q) if c==mp.mpf('0.5') else mp.inf)
print("G(x,0.5,q): max %.6f at %s" % (mx,argmx))
# Gc on face c=0.5, q=1: min
mn = mp.inf
for i in range(200+1):
    x = x0+(x1-x0)*i/200
    v = Gc(x, mp.mpf('0.5'), mp.mpf(1))
    mn = min(mn,v)
print("Gc(x,0.5,1) min: %.6f  (W/2.25 lower: %.6f)" % (mn, (3+2*x1/mp.tan(x1))/mp.mpf('2.25')))
# xPhi/D on face q=2, c=0.4
mn = mp.inf
for i in range(200+1):
    x = x0+(x1-x0)*i/200
    v = -xp(x, mp.mpf('0.4'), mp.mpf(2))
    mn = min(mn,v)
print("xPhi/D(x,0.4,2) max: %.6f" % mn)
# Gx max: face?
mn,mx,_,argmx = scan3d(lambda x,c,q: Gx(x,mp.mpf('0.5'),q))
print("Gx(x,0.5,q) max: %.6f at %s" % (mx,argmx))
mn,mx,_,argmx = scan3d(lambda x,c,q: Gx(x,c,mp.mpf(1)))
print("Gx(x,c,1) max: %.6f at %s" % (mx,argmx))
