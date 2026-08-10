# -*- coding: utf-8 -*-
"""Monotonicity of G, Gc, Gx in c and q on B1."""
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

def d(f, var, x, c, q):
    h = mp.mpf('1e-6')
    if var=='c': return (f(x,c+h,q)-f(x,c-h,q))/(2*h)
    if var=='q': return (f(x,c,q+h)-f(x,c,q-h))/(2*h)
    if var=='x': return (f(x+h,c,q)-f(x-h,c,q))/(2*h)

x0,x1,q0,q1,c0,c1 = mp.mpf('0.8411'),mp.mpf('1.1220'),mp.mpf(1),mp.mpf(2),mp.mpf('0.4'),mp.mpf('0.5')
def scan3d(f, var):
    mn=mp.inf; mx=-mp.inf
    for i in range(8+1):
        x = x0+(x1-x0)*i/8
        for j in range(8+1):
            q = q0+(q1-q0)*j/8
            for k in range(8+1):
                c = c0+(c1-c0)*k/8
                v = d(f,var,x,c,q)
                mn=min(mn,v); mx=max(mx,v)
    return mn,mx

for fname,f in [("G",G),("Gc",Gc),("Gx",Gx)]:
    for var in ['c','q','x']:
        mn,mx = scan3d(f,var)
        print("%s d/d%s on B1: [%.4f, %.4f]" % (fname,var,mn,mx))
