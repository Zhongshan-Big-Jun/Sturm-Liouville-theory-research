# -*- coding: utf-8 -*-
"""Check monotonicity of J on B1 and B2 boxes."""
import mpmath as mp
mp.mp.dps = 40

def Phi(x, q): return mp.cos(x)**2 + q*q*mp.sin(x)**2

def G(x, c, q):
    Ph = Phi(x, q); D = q + c*Ph; W = 3 + 2*x/mp.tan(x)
    return -Ph*W/D + 2*c*x*Ph*(q*q-1)*mp.sin(x)*mp.cos(x)/(D*D)

def Gc(x, c, q):
    Ph = Phi(x, q); D = q + c*Ph; W = 3 + 2*x/mp.tan(x)
    sc = mp.sin(x)*mp.cos(x)
    dg1c = Ph*W*Ph/(D*D)
    dg2c = 2*x*Ph*(q*q-1)*sc/(D*D) - 2*(2*c*x*Ph*(q*q-1)*sc)*Ph/(D**3)
    return dg1c + dg2c

def Gx(x, c, q):
    h = mp.mpf('1e-6')
    return (G(x+h, c, q) - G(x-h, c, q))/(2*h)

def J(x, c, q):
    Ph = Phi(x, q); D = q + c*Ph; xp = -x*Ph/D
    Gv = G(x, c, q)
    return Gv*Gv + Gx(x, c, q)*xp + Gc(x, c, q)

def Jc(x, c, q):
    h = mp.mpf('1e-6')
    return (J(x, c+h, q) - J(x, c-h, q))/(2*h)

def Jq(x, c, q):
    h = mp.mpf('1e-6')
    return (J(x, c, q+h) - J(x, c, q-h))/(2*h)

def Jx(x, c, q):
    h = mp.mpf('1e-6')
    return (J(x+h, c, q) - J(x-h, c, q))/(2*h)

def scan3(f, x0,x1,nx, q0,q1,nq, c0,c1,nc):
    mn = mp.inf; mx = -mp.inf; arg=None
    for i in range(nx+1):
        x = x0 + (x1-x0)*i/nx
        for j in range(nq+1):
            q = q0 + (q1-q0)*j/nq
            for k in range(nc+1):
                c = c0 + (c1-c0)*k/nc
                v = f(x,c,q)
                if v < mn: mn = v; arg=(x,c,q)
                if v > mx: mx = v
    return mn, mx, arg

# B1
b1 = (mp.mpf('0.8411'),mp.mpf('1.1220'),mp.mpf(1),mp.mpf(2),mp.mpf('0.4'),mp.mpf('0.5'))
b2 = (mp.mpf('2.0944'),mp.mpf('2.4859'),mp.mpf(1),mp.mpf(2),mp.mpf('0.4'),mp.mpf('0.5'))
for name, box in [("B1",b1),("B2",b2)]:
    x0,x1,q0,q1,c0,c1 = box
    for fname, f in [("Jc",Jc),("Jq",Jq),("Jx",Jx)]:
        mn,mx,arg = scan3(f,x0,x1,8,q0,q1,8,c0,c1,8)
        print("%s %s: [%.4f, %.4f] (arg %s)" % (name, fname, mn, mx, arg))
