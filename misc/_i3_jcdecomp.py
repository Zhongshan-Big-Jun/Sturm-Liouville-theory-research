# -*- coding: utf-8 -*-
"""Decompose Jc and Jq into terms on B1/B2 (fixed)."""
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
def scan3(f, x0,x1,q0,q1,c0,c1,n=8):
    mn=mp.inf; mx=-mp.inf
    for i in range(n+1):
        x = x0+(x1-x0)*i/n
        for j in range(n+1):
            q = q0+(q1-q0)*j/n
            for k in range(n+1):
                c = c0+(c1-c0)*k/n
                v = f(x,c,q)
                mn=min(mn,v); mx=max(mx,v)
    return mn,mx
def xp(x,c,q):
    Ph = Phi(x,q); D = q+c*Ph
    return -x*Ph/D
def xpc(x,c,q):
    h=mp.mpf('1e-6'); return (xp(x,c+h,q)-xp(x,c-h,q))/(2*h)
def xpq(x,c,q):
    h=mp.mpf('1e-6'); return (xp(x,c,q+h)-xp(x,c,q-h))/(2*h)

boxes = {"B1": (mp.mpf('0.8411'),mp.mpf('1.1220'),mp.mpf(1),mp.mpf(2),mp.mpf('0.4'),mp.mpf('0.5')),
         "B2": (mp.mpf('2.0944'),mp.mpf('2.4859'),mp.mpf(1),mp.mpf(2),mp.mpf('0.4'),mp.mpf('0.5'))}
for name,(x0,x1,q0,q1,c0,c1) in boxes.items():
    print(name)
    t1 = lambda x,c,q: 2*G(x,c,q)*Gc(x,c,q)
    t2 = lambda x,c,q: d(Gx,'c',x,c,q)*xp(x,c,q)
    t3 = lambda x,c,q: Gx(x,c,q)*xpc(x,c,q)
    t4 = lambda x,c,q: d(Gc,'c',x,c,q)
    for tn,f in [("2G*Gc",t1),("Gxc*xp",t2),("Gx*xpc",t3),("Gcc",t4)]:
        mn,mx = scan3(f,x0,x1,q0,q1,c0,c1)
        print("  Jc %s: [%.4f, %.4f]" % (tn,mn,mx))
    t1q = lambda x,c,q: 2*G(x,c,q)*d(G,'q',x,c,q)
    t2q = lambda x,c,q: d(Gx,'q',x,c,q)*xp(x,c,q)
    t3q = lambda x,c,q: Gx(x,c,q)*xpq(x,c,q)
    t4q = lambda x,c,q: d(Gc,'q',x,c,q)
    for tn,f in [("2G*Gq",t1q),("Gxq*xp",t2q),("Gx*xpq",t3q),("Gcq",t4q)]:
        mn,mx = scan3(f,x0,x1,q0,q1,c0,c1)
        print("  Jq %s: [%.4f, %.4f]" % (tn,mn,mx))
