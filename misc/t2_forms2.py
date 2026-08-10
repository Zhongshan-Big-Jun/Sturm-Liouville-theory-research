# -*- coding: utf-8 -*-
"""G, Gc, Gx, u in (gamma,t) coords: A=pi-g, c=t/A, q=tan t/tan g. Print factored numerators."""
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

for name, f in [('G',G),('Gc',Gc),('Gx',Gx),('u',u)]:
    fc = sp.simplify(f.subs(subs))
    num, den = sp.fraction(sp.together(fc))
    print('===== %s =====' % name)
    print('den:', sp.factor(den))
    nume = sp.expand_trig(sp.expand(num))
    print('num terms:', len(sp.Add.make_args(nume)))
    print('num:', sp.pretty(sp.factor(nume))[:1200])
    print()
