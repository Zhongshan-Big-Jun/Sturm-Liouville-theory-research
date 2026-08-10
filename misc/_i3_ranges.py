# -*- coding: utf-8 -*-
"""Ranges of G, G', J components on B1/B2; and P(x)=W^2+xW'+W."""
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
    Gv = G(x, c, q)
    return Gv*Gv + Gx(x, c, q)*xp + Gc(x, c, q)

def ranges(f, x0,x1,nx, q0,q1,nq, c0,c1,nc):
    mn = mp.inf; mx = -mp.inf
    for i in range(nx+1):
        x = x0 + (x1-x0)*i/nx
        for j in range(nq+1):
            q = q0 + (q1-q0)*j/nq
            for k in range(nc+1):
                c = c0 + (c1-c0)*k/nc
                v = f(x,c,q)
                if v < mn: mn = v
                if v > mx: mx = v
    return mn, mx

b1 = (mp.mpf('0.8411'),mp.mpf('1.1220'),mp.mpf(1),mp.mpf(2),mp.mpf('0.4'),mp.mpf('0.5'))
b2 = (mp.mpf('2.0944'),mp.mpf('2.4859'),mp.mpf(1),mp.mpf(2),mp.mpf('0.4'),mp.mpf('0.5'))
for name, box in [("B1",b1),("B2",b2)]:
    x0,x1,q0,q1,c0,c1 = box
    for fname, f in [("G",G),("Gc",Gc),("J",J)]:
        mn,mx = ranges(f,x0,x1,10,q0,q1,10,c0,c1,10)
        print("%s %s: [%.4f, %.4f]" % (name, fname, mn, mx))

# P(x) = W^2 + x W' + W  on B1 x-range and B2 x-range
def P(x):
    W = 3 + 2*x/mp.tan(x)
    Wp = 2/mp.tan(x) - 2*x/mp.sin(x)**2
    return W*W + x*Wp + W
for lo,hi,name in [(mp.mpf('0.8411'),mp.mpf('1.1220'),"B1x"),(mp.mpf('2.0944'),mp.mpf('2.4859'),"B2x")]:
    mn = mp.inf; mx=-mp.inf
    for i in range(4001):
        x = lo + (hi-lo)*i/4000
        v = P(x)
        mn=min(mn,v); mx=max(mx,v)
    print("P on %s: [%.6f, %.6f]" % (name, mn, mx))
