# -*- coding: utf-8 -*-
"""Full chain-rule partial derivatives at fixed theta for u,V,ux,Hx,Gx,Gc,J."""
import sympy as sp
x, th = sp.symbols('x th', positive=True)
s, b, S, C = sp.symbols('s b S C', positive=True)
Delta = b*s*th + C*S*x
u = b*s*x**2/Delta
A0 = sp.Rational(3)/x - 2*b/s
H = 2*th*(C**2*s**2 - S**2*b**2)/Delta
V = H - A0

def Dx(f):
    # d/dx at fixed theta, with s=sin x (ds/dx=-b), b=-cos x (db/dx=s)
    fx = sp.diff(f, x)
    fs = sp.diff(f, s)
    fb = sp.diff(f, b)
    return sp.cancel(fx + fs*(-b) + fb*s)

def Dth(f):
    # d/dth at fixed x, with S=sin th (dS/dth=C), C=cos th (dC/dth=-S)
    ft = sp.diff(f, th)
    fS = sp.diff(f, S)
    fC = sp.diff(f, C)
    return sp.cancel(ft + fS*C + fC*(-S))

G = u*V
ux = Dx(u)
Gx = Dx(G)
Gc = Dth(G)
J = G**2 + Gc - u*Gx
dJdx = Dx(J)

objs = {'u': u, 'V': V, 'ux': ux, 'G': G, 'Gx': Gx, 'Gc': Gc, 'J': J, 'dJdx': dJdx}
for nm in ['u','V','ux','G','Gx','Gc']:
    du_dx = Dx(objs[nm]); du_dth = Dth(objs[nm])
    print('== d%s/dx, d%s/dth ==' % (nm, nm))
    for lbl, e in [('dx', du_dx), ('dth', du_dth)]:
        num, den = sp.fraction(e)
        num = sp.expand(num)
        nterms = len(sp.Add.make_args(num))
        print('  %s: num terms=%d, den sign: %s' % (lbl, nterms, sp.Poly(den, s,b,S,C).is_constant() if False else 'var'))
print('== dJ/dx ==')
num, den = sp.fraction(dJdx)
num = sp.expand(num)
print('  num terms:', len(sp.Add.make_args(num)))
import pickle
pickle.dump({'u':u,'V':V,'ux':ux,'G':G,'Gx':Gx,'Gc':Gc,'J':J,'dJdx':dJdx,
             'du_dx':Dx(u),'du_dth':Dth(u),'dV_dx':Dx(V),'dV_dth':Dth(V),
             'dux_dx':Dx(ux),'dux_dth':Dth(ux),'dGx_dx':Dx(Gx),'dGx_dth':Dth(Gx),
             'dG_dx':Dx(G),'dG_dth':Dth(G),'dGc_dx':Dx(Gc),'dGc_dth':Dth(Gc)},
            open('misc/re_derivs.pkl','wb'))
print('saved')
