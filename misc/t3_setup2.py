# -*- coding: utf-8 -*-
"""t3_setup2: fast atom-based (gamma,t) forms. Uses derived closed forms directly."""
import sympy as sp

g, t, A = sp.symbols('gamma t A', positive=True)
sg, cg, st, ct = sp.symbols('sg cg st ct', positive=True)
rels = {sg**2: 1 - cg**2, st**2: 1 - ct**2}

def red(expr):
    # reduce using sg^2=1-cg^2, st^2=1-ct^2; expand
    e = sp.expand(expr)
    for _ in range(6):
        e2 = e.subs(rels)
        e2 = sp.expand(e2)
        if e2 == e: break
        e = e2
    return sp.expand(e)

P = 2*(A*st*ct + t*sg*cg)
# D = q + c*Phi = cg*P/(2*A*sg*ct^2)
# G = -Phi*W/D + 2*c*A*Phi*(q^2-1)*sc/D^2
G  = red((4*A**2*cg**2 - 6*A*sg*cg)/P + 8*A**2*t*sg*cg*(cg**2-ct**2)/P**2)
# Gc = [12A^2 sg^2 cg^2 - 8A^3 sg cg (2cg^2 - ct^2)]/P^2 - 32 A^3 t sg^2 cg^2 (cg^2-ct^2)/P^3
Gc = red((12*A**2*sg**2*cg**2 - 8*A**3*sg*cg*(2*cg**2-ct**2))/P**2
         - 32*A**3*t*sg**2*cg**2*(cg**2-ct**2)/P**3)
u  = red(2*A**2*sg*cg/P)
print('G  terms:', len(sp.Add.make_args(sp.expand(G))))
print('Gc terms:', len(sp.Add.make_args(sp.expand(Gc))))

# Gx: recompute via sympy from G as function of x (A) with c,q fixed
# Use original defs to get Gx = diff(G,x) symbolic then substitute atom forms.
x, c, q = sp.symbols('x c q', positive=True)
sx, cx = sp.sin(x), sp.cos(x)
Ph = cx**2 + q**2*sx**2
Dq = q + c*Ph
W = 3 + 2*x*cx/sx
sc_ = sx*cx
Gfun = -Ph*W/Dq + 2*c*x*Ph*(q**2-1)*sc_/Dq**2
Gxfun = sp.diff(Gfun, x)
# substitute: x=A, sin x = sg, cos x = -cg, q = st cg/(sg ct), c = t/A
subs = {sp.sin(x): sg, sp.cos(x): -cg, x: A, q: st*cg/(sg*ct), c: t/A}
Gx = red(Gxfun.subs(subs))
print('Gx terms:', len(sp.Add.make_args(sp.expand(Gx))))

# J2_2d = G^2 + Gc - u*Gx
J2 = sp.expand(G**2 + Gc - u*Gx)
# put over P^4: compute numerator
num, den = sp.fraction(sp.together(J2))
num = sp.expand(num*1)
print('J2 denominator:', sp.factor(den))
NJ = red(num/4/A**2)
print('NJ terms:', len(sp.Add.make_args(NJ)))

# composed derivatives: dG/dq sign = dG/dt; dG/dg = dG/dg_partial + dG/dt * st ct/(sg cg)
dG_dt = sp.diff(G, t)
dG_dg_part = sp.diff(G, g)  # NOTE: A is a function of g: A = pi - g => dA/dg = -1
# handle A dependence: replace A by pi-g everywhere first
G_in_g = G.subs(A, sp.pi - g)
dG_dg = sp.diff(G_in_g, g)
dG_dt_in = dG_dt.subs(A, sp.pi - g)
comp_dG_dg = red(dG_dg + dG_dt_in*st*ct/(sg*cg))
print('dG/dt (sign for dG/dq): num terms:', len(sp.Add.make_args(sp.expand(dG_dt))))
print('comp dG/dg: num terms:', len(sp.Add.make_args(sp.expand(comp_dG_dg))))

# same for Gc, Gx
Gc_in_g = Gc.subs(A, sp.pi - g)
dGc_dg = sp.diff(Gc_in_g, g)
dGc_dt = sp.diff(Gc, t).subs(A, sp.pi - g)
comp_dGc_dg = red(dGc_dg + dGc_dt*st*ct/(sg*cg))
dGc_dt2 = sp.diff(Gc, t).subs(A, sp.pi - g)
print('dGc/dt (sign for dGc/dq): num terms:', len(sp.Add.make_args(sp.expand(dGc_dt2))))
print('comp dGc/dg: num terms:', len(sp.Add.make_args(sp.expand(comp_dGc_dg))))

Gx_in_g = Gx.subs(A, sp.pi - g)
dGx_dg = sp.diff(Gx_in_g, g)
dGx_dt = sp.diff(Gx, t).subs(A, sp.pi - g)
comp_dGx_dg = red(dGx_dg + dGx_dt*st*ct/(sg*cg))
print('comp dGx/dg: num terms:', len(sp.Add.make_args(sp.expand(comp_dGx_dg))))

import pickle
data = dict(G=G, Gc=Gc, Gx=Gx, u=u, J2=J2, P=P, NJ=NJ,
            dG_dt=dG_dt.subs(A, sp.pi-g), comp_dG_dg=comp_dG_dg,
            dGc_dt=dGc_dt, comp_dGc_dg=comp_dGc_dg,
            dGx_dt=dGx_dt, comp_dGx_dg=comp_dGx_dg)
with open('misc/t3_symbols2.pkl','wb') as fh:
    pickle.dump(data, fh)
print('saved misc/t3_symbols2.pkl')
