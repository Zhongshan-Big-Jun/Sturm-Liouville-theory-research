# t3_Gxclosed.py: closed forms of V, ux, Hx, A0x, Gx pieces in (A,t) coords
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
for nm, ex in [('Phi',Phi),('D',D),('u',u),('V',V),('ux',ux),('Hx',Hx),('A0x',A0x)]:
    print('== %s ==' % nm)
    print(sp.factor(sp.trigsimp(ex)))
    print()
