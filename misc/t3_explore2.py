# t3_explore2: simplify G in terms of p=2A, t=2Ac
import sympy as sp
A, c = sp.symbols('A c', positive=True)
p, t = sp.symbols('p t', positive=True)
s, cx = sp.sin(sp.pi-A), sp.cos(sp.pi-A)
Phi = sp.cos(A)**2/sp.cos(c*A)**2
u = A*sp.sin(2*A)/(c*sp.sin(2*A)-sp.sin(2*A*c))
A0 = sp.Rational(3)/A + 2*cx/s
H = 2*c*(1-1)*s*cx/0  # placeholder
# recompute G directly: G = u*(H - A0), H = 2c(q^2-1) s cx / D
q = -sp.tan(c*A)/sp.tan(A)
D = q + c*Phi
H = sp.trigsimp(2*c*(q*q-1)*s*cx/D)
G = sp.trigsimp(sp.expand(u*(H - A0)))
G2 = sp.simplify(G)
print('G =', G2)
# substitute p=2A, t=2Ac: A=p/2, c=t/p
Gp = sp.simplify(G2.subs({A: sp.Rational(1,2)*p, c: t/p}))
print()
print('G(p,t) =', sp.factor(sp.trigsimp(Gp)))
