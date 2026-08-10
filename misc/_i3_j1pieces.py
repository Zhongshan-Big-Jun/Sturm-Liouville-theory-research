# -*- coding: utf-8 -*-
"""J1 2D box: locations/monotonicity of G, Gc, Gx, xPhi/D extremes."""
import mpmath as mp
mp.mp.dps = 40
def Phi(x, q): return mp.cos(x)**2 + q*q*mp.sin(x)**2
def c1(x,q): return mp.atan(1.0/(q*mp.tan(x)))/x
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
def xpabs(x,c,q):
    Ph = Phi(x,q); D = q+c*Ph
    return x*Ph/D

x0,x1 = mp.mpf('0.8411'),mp.mpf('1.1220')
# extremes with locations
def scan(name, f, want_max):
    best = -mp.inf if want_max else mp.inf; arg=None
    for i in range(60+1):
        x = x0+(x1-x0)*i/60
        for j in range(60+1):
            q = 1+1*j/60
            v = f(x,q)
            if (want_max and v>best) or ((not want_max) and v<best):
                best=v; arg=(x,q)
    return best, arg
for nm, f, wm in [("G max", lambda x,q: G(x,c1(x,q),q), True),
                  ("Gc min", lambda x,q: Gc(x,c1(x,q),q), False),
                  ("Gx max", lambda x,q: Gx(x,c1(x,q),q), True),
                  ("xpabs max", lambda x,q: xpabs(x,c1(x,q),q), True)]:
    b,arg = scan(nm,f,wm)
    print("%s: %.6f at (x,q)=%s" % (nm,b,arg))
# monotonicity of G, Gc, Gx, xpabs on 2D box: partial w.r.t x and q (total along the curve param)
def d2(f, var, x, q):
    h=mp.mpf('1e-6')
    if var=='x': return (f(x+h,q)-f(x-h,q))/(2*h)
    if var=='q': return (f(x,q+h)-f(x,q-h))/(2*h)
for nm, f in [("G",lambda x,q: G(x,c1(x,q),q)),
              ("Gc",lambda x,q: Gc(x,c1(x,q),q)),
              ("Gx",lambda x,q: Gx(x,c1(x,q),q)),
              ("xpabs",lambda x,q: xpabs(x,c1(x,q),q))]:
    mnx=mp.inf; mxx=-mp.inf; mnq=mp.inf; mxq=-mp.inf
    for i in range(20+1):
        x = x0+(x1-x0)*i/20
        for j in range(20+1):
            q = 1+1*j/20
            vx = d2(f,'x',x,q); vq = d2(f,'q',x,q)
            mnx=min(mnx,vx); mxx=max(mxx,vx); mnq=min(mnq,vq); mxq=max(mxq,vq)
    print("%s: d/dx [%.3f, %.3f], d/dq [%.3f, %.3f]" % (nm,mnx,mxx,mnq,mxq))
