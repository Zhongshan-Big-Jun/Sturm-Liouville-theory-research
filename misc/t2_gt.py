# -*- coding: utf-8 -*-
"""J2_2d in (gamma,t) coords: x=A=pi-gamma, c=t/A, q=tan t / tan gamma.
Check numerator is polynomial in (gamma, t, sin g, cos g, sin t, cos t)."""
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
J = sp.simplify(G**2 - u*Gx + Gc)

sg, cg = sp.sin(g), sp.cos(g)
st, ct = sp.sin(t), sp.cos(t)
subs = {
    x: sp.pi - g,
    c: t/(sp.pi - g),
    q: st/cg * cg/st,  # placeholder to keep q as tan t/tan g = (st/ct)/(sg/cg)
}
# q = tan(t)/tan(g)
qexpr = (st/ct)/(sg/cg)
subs2 = {x: sp.pi - g, c: t/(sp.pi - g), q: qexpr}
J2 = sp.simplify(J.subs(subs2))
num, den = sp.fraction(sp.together(J2))
print('den:', sp.factor(den))
# check polynomial in atoms
atoms = [g, t, sg, cg, st, ct]
try:
    p = sp.Poly(num, *atoms)
    print('numerator is polynomial in 6 atoms. total terms:', p.total_degree() if False else len(sp.Add.make_args(num)))
    # collect info
    print('num terms:', len(sp.Add.make_args(sp.expand(num))))
except Exception as e:
    print('NOT polynomial:', e)
    print('num head:', sp.pretty(num)[:1500])
