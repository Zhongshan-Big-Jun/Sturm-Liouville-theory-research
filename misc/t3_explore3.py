# t3_explore3: G, Gc, Gx, u in (A,t) coords, t=cA, fully simplified
import sympy as sp
A, t = sp.symbols('A t', positive=True)
c = t/A
s = sp.sin(A); cx = sp.cos(A)
Phi = sp.cos(A)**2/sp.cos(t)**2
u = A*sp.sin(2*A)/(c*sp.sin(2*A)-sp.sin(2*t))
A0 = sp.Rational(3)/A + 2*cx/s
q = -sp.tan(t)/sp.tan(A)
D = q + c*Phi
H = sp.trigsimp(2*c*(q*q-1)*s*cx/D)
G = sp.trigsimp(sp.expand(u*(H - A0)))
G = sp.factor(sp.trigsimp(G))
print('u  =', sp.factor(u))
print('G  =', sp.factor(G))
# Gc = dG/dc with (q, A=x) fixed. In (A,t) coords we want dG/dt at fixed A,q... 
# but easier: G as function of (A,c) with q=q(A,c); we already have that.
