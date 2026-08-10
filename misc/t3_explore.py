# t3_explore: explicit formulas for G, Gc, Gx, u in (A,c) coords; look for structure
import sympy as sp
A, c, q = sp.symbols('A c q', positive=True)
g = sp.pi - A
s, cx = sp.sin(g), sp.cos(g)   # sin x, cos x with x = A
# q = tan(cA)/tan(g) = -tan(cA)/tan A ; express via tan
Phi = q*q*s*s + cx*cx
D = q + c*Phi
u = A*Phi/D
A0 = sp.Rational(3)/A + 2*cx/s
H = 2*c*(q*q-1)*s*cx/D
G = u*(H - A0)
# now substitute q = -tan(cA)/tan A
sub = {q: -sp.tan(c*A)/sp.tan(A)}
# simplify Phi, D with this
Phi_s = sp.trigsimp(Phi.subs(sub))
D_s = sp.trigsimp(D.subs(sub))
u_s = sp.trigsimp(u.subs(sub))
G_s = sp.trigsimp(G.subs(sub))
print('Phi =', sp.factor(Phi_s))
print('D =', sp.factor(D_s))
print('u =', sp.trigsimp(u_s))
print('G =', sp.trigsimp(sp.expand(G_s)))
