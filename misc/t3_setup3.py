# -*- coding: utf-8 -*-
"""t3_setup3: fast atom-based forms. All quantities in atoms (A,t,sg,cg,st,ct), g=pi-A.
Relations: sg^2+cg^2=1, st^2+ct^2=1, A+g=pi. d/dg = -d/dA + cg d/dsg - sg d/dcg."""
import sympy as sp

A, t = sp.symbols('A t', positive=True)
sg, cg, st, ct = sp.symbols('sg cg st ct', positive=True)

def rat(num, den):
    return sp.expand(num)/sp.expand(den)

P = 2*(A*st*ct + t*sg*cg)
# --- G ---
# G = (4A^2 cg^2 - 6A sg cg)/P + 8A^2 t sg cg (cg^2-ct^2)/P^2
G = rat(4*A**2*cg**2 - 6*A*sg*cg, P) + rat(8*A**2*t*sg*cg*(cg**2-ct**2), P**2)
# --- Gc ---
Gc = rat(12*A**2*sg**2*cg**2 - 8*A**3*sg*cg*(2*cg**2-ct**2), P**2) \
     - rat(32*A**3*t*sg**2*cg**2*(cg**2-ct**2), P**3)
# --- u ---
u = rat(2*A**2*sg*cg, P)
# --- Gx (derived by hand; D=cg P/(2A sg ct^2)) ---
# terms: Gx = -(Phi_x W + Phi W_x)/D + Phi W c Phi_x/D^2
#            + 2c[Phi(q2-1)sc + x Phi_x(q2-1)sc + x Phi(q2-1)cos2x]/D^2
#            - 4 c^2 x Phi^2 (q2-1) sc / D^3
q2m1 = (cg**2-ct**2)/(sg**2*ct**2)     # q^2-1
Phi  = cg**2/ct**2
Phi_x= -2*q2m1*sg*cg
W    = 3 - 2*A*cg/sg
W_x  = -2*cg/sg - 2*A/sg**2
sc_  = -sg*cg
cos2x= cg**2 - sg**2
c    = t/A
D    = cg*P/(2*A*sg*ct**2)
D_x  = c*Phi_x
Gx = -(Phi_x*W + Phi*W_x)/D + Phi*W*c*Phi_x/D**2 \
     + 2*c*(Phi*q2m1*sc_ + A*Phi_x*q2m1*sc_ + A*Phi*q2m1*cos2x)/D**2 \
     - 4*c**2*A*Phi**2*q2m1*sc_/D**3
Gx = sp.cancel(Gx)
# --- J2 = G^2 + Gc - u Gx ---
J2 = sp.cancel(G**2 + Gc - u*Gx)

def Dg(f):
    # d/dg at fixed t: g=pi-A, sg=sin g, cg=cos g
    return -sp.diff(f, A) + cg*sp.diff(f, sg) - sg*sp.diff(f, cg)

def num_of(f, den):
    n = sp.cancel(f*den)
    n = sp.expand(n)
    return n

dG_dt  = sp.diff(G, t)
dG_dg  = Dg(G)
dGc_dt = sp.diff(Gc, t)
dGc_dg = Dg(Gc)
dGx_dt = sp.diff(Gx, t)
dGx_dg = Dg(Gx)

# composed along curve: d/dq sign = d/dt sign (dt/dq>0); d/dg along q fixed = dg_partial + dt * st ct/(sg cg)
composed = {
 'dG_dq': dG_dt,
 'dG_dg': sp.cancel(dG_dg + dG_dt*st*ct/(sg*cg)),
 'dGc_dq': dGc_dt,
 'dGc_dg': sp.cancel(dGc_dg + dGc_dt*st*ct/(sg*cg)),
 'dGx_dq': dGx_dt,
 'dGx_dg': sp.cancel(dGx_dg + dGx_dt*st*ct/(sg*cg)),
}
import pickle
data = dict(G=G,Gc=Gc,Gx=Gx,u=u,J2=J2,P=P,composed=composed)
with open('misc/t3_symbols3.pkl','wb') as fh: pickle.dump(data, fh)

print('G =', sp.srepr(sp.expand(G))[:80], '...')
print('Gx rational?', isinstance(sp.cancel(Gx), sp.core.mul.Mul) or True)
for k,v in composed.items():
    n = sp.cancel(v)
    nn, dd = sp.fraction(sp.together(n))
    print('%-8s: num terms=%d, den factored=%s' % (k, len(sp.Add.make_args(sp.expand(nn))), sp.factor(dd)[:100]))
print('saved misc/t3_symbols3.pkl')
