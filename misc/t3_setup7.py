# -*- coding: utf-8 -*-
"""t3_setup7: numeric verification with float substitution."""
import sympy as sp
exec(open('misc/t3_setup6.py', encoding='utf-8').read().split("import mpmath")[0])  # redefines everything up to mpmath import
import mpmath as mp
mp.mp.dps = 30

# verify with plain floats
def feval(expr, gv, qv):
    import math
    Av = math.pi - gv; tv = math.atan(qv*math.tan(gv))
    sv = {A: Av, t: tv, sg: math.sin(gv), cg: math.cos(gv), st: math.sin(tv), ct: math.cos(tv)}
    return float(expr.subs(sv).evalf(25))

x0, c0, q0 = sp.symbols('x0 c0 q0', positive=True)
sx0, cx0 = sp.sin(x0), sp.cos(x0)
Ph0 = cx0**2 + q0**2*sx0**2
D0  = q0 + c0*Ph0
W0  = 3 + 2*x0*cx0/sx0
sc0 = sx0*cx0
G0  = -Ph0*W0/D0 + 2*c0*x0*Ph0*(q0**2-1)*sc0/D0**2
Gx0 = sp.diff(G0, x0); Gc0 = sp.diff(G0, c0); u0 = x0*Ph0/D0
fG0 = sp.lambdify((x0,c0,q0), G0, 'mpmath'); fGx0 = sp.lambdify((x0,c0,q0), Gx0, 'mpmath')
fGc0 = sp.lambdify((x0,c0,q0), Gc0, 'mpmath'); fu0 = sp.lambdify((x0,c0,q0), u0, 'mpmath')

maxerr = 0
for gv, qv in [(0.7,1.5),(0.9,1.2),(1.0,1.5),(0.66,1.9),(1.0472,1.0),(0.85,2.0),(0.75,1.05)]:
    import math
    Av = math.pi - gv; tv = math.atan(qv*math.tan(gv))
    Gv  = feval(G, gv, qv); Gcv = feval(Gc, gv, qv); Gxv = feval(Gx, gv, qv); uv = feval(u, gv, qv)
    xv, cv, qvf = Av, tv/Av, qv
    r0 = (float(fG0(xv,cv,qvf)), float(fGx0(xv,cv,qvf)), float(fGc0(xv,cv,qvf)), float(fu0(xv,cv,qvf)))
    for a,b in zip((Gv,Gxv,Gcv,uv), r0):
        maxerr = max(maxerr, abs(a-b))
    print('g=%.4f q=%.3f  atom=(%.6f,%.6f,%.6f,%.6f) orig=(%.6f,%.6f,%.6f,%.6f)' % (gv,qv,Gv,Gxv,Gcv,uv,*r0))
print('max abs err:', maxerr)
