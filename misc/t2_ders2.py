# -*- coding: utf-8 -*-
"""Composed partial derivatives in (gamma,t): numeric sign ranges + factorization attempt."""
import sympy as sp
import numpy as np

x, c, q = sp.symbols('x c q', positive=True)
g = sp.symbols('gamma', positive=True)
t = sp.symbols('t', positive=True)
sx, cx = sp.sin(x), sp.cos(x)
Ph = cx**2 + q**2*sx**2
D = q + c*Ph
W = 3 + 2*x*cx/sx
sc = sx*cx
G = -Ph*W/D + 2*c*x*Ph*(q**2-1)*sc/(D**2)
Gx = sp.simplify(sp.diff(G, x))
Gc = sp.simplify(sp.diff(G, c))
u = x*Ph/D
qexpr = (sp.sin(t)/sp.cos(t))/(sp.sin(g)/sp.cos(g))
subs = {x: sp.pi - g, c: t/(sp.pi - g), q: qexpr}

G2, Gc2, Gx2, u2 = sp.simplify(G.subs(subs)), sp.simplify(Gc.subs(subs)), sp.simplify(Gx.subs(subs)), sp.simplify(u.subs(subs))
fn = {}
for name, f in [('G',G2),('Gc',Gc2),('Gx',Gx2),('u',u2)]:
    fn[name] = sp.lambdify((g,t), f, 'numpy')
    for var, vn in [(g,'g'),(t,'t')]:
        d = sp.simplify(sp.diff(f, var))
        fn[name+'_d'+vn] = sp.lambdify((g,t), d, 'numpy')
        num, den = sp.fraction(sp.together(d))
        try:
            fac = sp.factor(sp.expand_trig(sp.expand(num)))
            print('%s d/d%s factor: %s' % (name, vn, fac))
        except Exception as e:
            print('%s d/d%s factor failed: %s' % (name, vn, e))

# numeric ranges on region R: g in [0.655, pi/3], t in [0.4*(pi-g), 0.5*(pi-g)]
pi = np.pi
Ng, Nt = 240, 200
gv = np.linspace(0.655, pi/3, Ng+1)
lo = 0.4*(pi-gv); hi = 0.5*(pi-gv)
GG = np.repeat(gv, Nt+1)
TT = np.concatenate([np.linspace(lo[i], hi[i], Nt+1) for i in range(Ng+1)])
print('region pts:', GG.size)
for k in ['G','Gc','Gx','u']:
    for vn in ['g','t']:
        v = fn[k+'_d'+vn](GG, TT)
        print('%s d/d%s: min=%.4f max=%.4f' % (k, vn, v.min(), v.max()))
    v = fn[k](GG, TT)
    print('%s value: min=%.5f max=%.5f' % (k, v.min(), v.max()))
