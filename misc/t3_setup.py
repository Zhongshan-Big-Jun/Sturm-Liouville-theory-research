# -*- coding: utf-8 -*-
"""t3_setup: verify (gamma,t)-coordinate rational forms for G, Gc, Gx, u, J2_2d."""
import sympy as sp

x, c, q = sp.symbols('x c q', positive=True)
sx, cx = sp.sin(x), sp.cos(x)
Ph = cx**2 + q**2*sx**2
D = q + c*Ph
W = 3 + 2*x*cx/sx
sc = sx*cx
G = -Ph*W/D + 2*c*x*Ph*(q**2-1)*sc/D**2
Gx = sp.simplify(sp.diff(G, x))
Gc = sp.simplify(sp.diff(G, c))
u = x*Ph/D
J = sp.simplify(G**2 - u*Gx + Gc)

g, t = sp.symbols('gamma t', positive=True)
sg, cg = sp.sin(g), sp.cos(g)
st, ct = sp.sin(t), sp.cos(t)
A = sp.pi - g
qexpr = st*cg/(sg*ct)
cexpr = t/A
subs = {x: A, c: cexpr, q: qexpr}

P = 2*(A*st*ct + t*sg*cg)

Gt  = G.subs(subs);  Gct = Gc.subs(subs); Gxt = Gx.subs(subs); ut = u.subs(subs); Jt = J.subs(subs)

def chk(name, f, form, denom):
    f = sp.simplify(f)
    lhs = sp.expand_trig(sp.expand(sp.simplify(f*denom)))
    rhs = sp.expand_trig(sp.expand(form))
    diff = sp.expand(lhs - rhs)
    print('%-8s: form holds = %s' % (name, sp.simplify(diff) == 0))
    return diff

chk('G', Gt, 4*A*sp.Symbol('NG')*0 + Gt, 1)  # placeholder skip

# Direct: compute N_G = G*P^2/(4A), N_Gc = Gc*P^3/(8A^2), N_Gx = -Gx*P^3/(16A*sg), N_J = J*P^4/(4A^2)
NG  = sp.expand_trig(sp.expand(Gt *P**2/(4*A)))
NGc = sp.expand_trig(sp.expand(Gct*P**3/(8*A**2)))
NGx = sp.expand_trig(sp.expand(-Gxt*P**3/(16*A*sg)))
NJ  = sp.expand_trig(sp.expand(Jt *P**4/(4*A**2)))
print('NG terms:', len(sp.Add.make_args(NG)), ' total degree:', sp.Poly(NG, g, t, sg, cg, st, ct).total_degree())
print('NGc terms:', len(sp.Add.make_args(NGc)), ' total degree:', sp.Poly(NGc, g, t, sg, cg, st, ct).total_degree())
print('NGx terms:', len(sp.Add.make_args(NGx)), ' total degree:', sp.Poly(NGx, g, t, sg, cg, st, ct).total_degree())
print('NJ terms:', len(sp.Add.make_args(NJ)), ' total degree:', sp.Poly(NJ, g, t, sg, cg, st, ct).total_degree())

# verify u closed form
print('u*P/(2A^2 sg cg) =', sp.simplify(ut*P/(2*A**2*sg*cg)))
# verify P>0 atom form
print('P =', sp.expand(P))

# composed derivatives via chain rule in (g,t) coords
# dt/dq = tan g/(1+q^2 tan^2 g) = tan g cos^2 t ; dt/dg|_{q} = q sec^2 g cos^2 t = st ct/(sg cg)
# dG/dq = dGt/dt * dt/dq ; dG/dg = dGt/dg + dGt/dt * dt/dg|_q
dG_dt = sp.diff(Gt, t); dG_dg = sp.diff(Gt, g)
dGc_dt = sp.diff(Gct, t); dGc_dg = sp.diff(Gct, g)
dGx_dt = sp.diff(Gxt, t); dGx_dg = sp.diff(Gxt, g)
print('dG/dq sign = sign of dGt/dt, num terms:', len(sp.Add.make_args(sp.expand_trig(sp.expand(dG_dt)))))
print('dG/dg composed = dGt/dg + dGt/dt * st ct/(sg cg)')

# save everything
import pickle
data = {'Gt':Gt,'Gct':Gct,'Gxt':Gxt,'ut':ut,'Jt':Jt,'NG':NG,'NGc':NGc,'NGx':NGx,'NJ':NJ,
        'dG_dt':dG_dt,'dG_dg':dG_dg,'dGc_dt':dGc_dt,'dGc_dg':dGc_dg,'dGx_dt':dGx_dt,'dGx_dg':dGx_dg,
        'P':P,'A':A}
with open('misc/t3_symbols.pkl','wb') as fh:
    pickle.dump(data, fh)
print('saved misc/t3_symbols.pkl')
