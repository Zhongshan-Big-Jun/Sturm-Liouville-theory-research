# -*- coding: utf-8 -*-
"""Compose J2_2d on the true curve and inspect structure. Coordinates: (A,w) with A=pi-gamma, w=q tan gamma."""
import sympy as sp
sp.init_printing()
x, c, q = sp.symbols('x c q', positive=True)
A, w = sp.symbols('A w', positive=True)

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

# On the true curve for the 2nd phase: x = A, gamma = pi - A, w = q*tan(gamma) = -q*tan(A)
# sin x = w/sqrt(q^2+w^2), cos x = -q/sqrt(q^2+w^2), cot x = -q/w, c = atan(w)/A
# Substitute these; keep q and w as variables (or eliminate q via q = -w/tan A)
subs = {
    sp.sin(x): w/sp.sqrt(q**2+w**2),
    sp.cos(x): -q/sp.sqrt(q**2+w**2),
    x: A,
    c: sp.atan(w)/A,
}
J2 = sp.simplify(J.subs(subs))
print('J2 composed (A,w,q):')
print(sp.pretty(sp.factor(J2))[:3000])
