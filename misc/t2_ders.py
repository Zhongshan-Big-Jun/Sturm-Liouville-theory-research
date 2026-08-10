# -*- coding: utf-8 -*-
"""Composed partial derivatives in (gamma,t) coords. d/dq sign = d/dt sign (since dt/dq>0).
d/dg|_q = d/dg + (q/Phi)*d/dt. Compute numerators and try to factor."""
import sympy as sp

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
sg, cg, st, ct = sp.sin(g), sp.cos(g), sp.sin(t), sp.cos(t)

def comp(f):
    return sp.simplify(f.subs(subs))

G2, Gc2, Gx2, u2 = comp(G), comp(Gc), comp(Gx), comp(u)

# partials in (g,t)
for name, f in [('G',G2),('Gc',Gc2),('Gx',Gx2),('u',u2)]:
    print('===== %s =====' % name)
    for var, vn in [(g,'g'), (t,'t')]:
        d = sp.simplify(sp.diff(f, var))
        num, den = sp.fraction(sp.together(d))
        print(' d/d%s: den=%s' % (vn, sp.factor(den)))
        nume = sp.expand_trig(sp.expand(num))
        print('   num terms: %d' % len(sp.Add.make_args(nume)))
        print('   factor:', sp.factor(nume)[:600])
    print()
