# t3_explore4: full closed forms in (A,t) coords
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
V = H - A0
# Gc = dG/dc at fixed (q, x): use chain: G(A,c) with c=t/A -> dG/dt at fixed A,q * dt/dc
# easier: G as function of (A,c), q=q(A,c): G_c = du_c*(H-A0) + u*dH_c
du_c = -A*Phi*Phi/(D*D)
dH_c = 2*(q*q-1)*s*cx/D - 2*c*(q*q-1)*s*cx*Phi/(D*D)
Gc = sp.trigsimp(du_c*V + u*dH_c)
# Gx = dG/dx at fixed (q,c), x=A
Phix = 2*(q*q-1)*s*cx
denx = c*Phix
ux = (Phi + A*Phix)/D - A*Phi*denx/(D*D)
A0x = -3/(A*A) - 2/s**2
Hx = (2*c*(q*q-1)*(cx*cx - s*s)*D - 2*c*(q*q-1)*s*cx*denx)/(D*D)
Gx = sp.trigsimp(ux*V + u*(Hx - A0x))
for nm, ex in [('u',u),('G',G),('Gc',Gc),('Gx',Gx)]:
    ex2 = sp.factor(sp.trigsimp(ex))
    print('== %s ==' % nm)
    print(ex2)
    print()
