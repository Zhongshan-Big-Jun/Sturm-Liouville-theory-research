# t3_Gxsimple.py: Gx pieces in (p,r) = (2A, 2t) coords, factor each
import sympy as sp
A, t = sp.symbols('A t', positive=True)
c = t/A
s = sp.sin(A); cx = sp.cos(A)
q = -sp.tan(t)/sp.tan(A)
Phi = sp.trigsimp(q*q*s*s + cx*cx)
D = sp.trigsimp(q + c*Phi)
u = sp.trigsimp(A*Phi/D)
A0 = sp.Rational(3)/A + 2*cx/s
H = sp.trigsimp(2*c*(q*q-1)*s*cx/D)
V = sp.trigsimp(H - A0)
Phix = sp.trigsimp(2*(q*q-1)*s*cx)
ux = sp.trigsimp((Phi + A*Phix)/D - A*Phi*c*Phix/(D*D))
A0x = -3/(A*A) - 2/s**2
Hx = sp.trigsimp((2*c*(q*q-1)*(cx*cx - s*s)*D - 2*c*(q*q-1)*s*cx*c*Phix)/(D*D))
# substitute p=2A, r=2t  (c = r/p), then sin/cos of A, t in terms of sin(p/2),cos(p/2) etc
p, r = sp.symbols('p r', positive=True)
sub = {A: p/2, t: r/2}
for nm, ex in [('u',u),('V',V),('ux',ux),('Hx',Hx)]:
    e = ex.subs(sub)
    e = sp.trigsimp(e)
    e = sp.factor(sp.trigsimp(sp.expand(e)))
    print('== %s ==' % nm)
    print(e)
    print()
