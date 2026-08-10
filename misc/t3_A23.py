# t3_A23.py: closed forms at A=2pi/3 for u, Gx, H2 as functions of c (or q)
import sympy as sp
c = sp.symbols('c', positive=True)
A = 2*sp.pi/3
t = c*A
q = -sp.tan(t)/sp.tan(A)
s = sp.sin(A); cx = sp.cos(A)
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
Gx = sp.trigsimp(ux*V + u*(Hx - A0x))
for nm, ex in [('Phi',Phi),('D',D),('u',u),('V',V),('Gx',Gx)]:
    print('== %s ==' % nm)
    print(sp.factor(sp.trigsimp(ex)))
    print()
# H2 = u*Gx
H2 = sp.trigsimp(u*Gx)
print('== H2 ==')
print(sp.factor(sp.trigsimp(H2)))
