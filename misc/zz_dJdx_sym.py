# -*- coding: utf-8 -*-
"""Numerator of dJ/dx|th with CORRECT Gc, in six-variable algebra (s,b,S,C,x,th)."""
import sympy as sp
x, th = sp.symbols('x th', positive=True)
s, b, S, C = sp.symbols('s b S C', positive=True)

q = S*b/(C*s)
Phi = b*b/(C*C)
c = th/x
D = q + c*Phi
u = x*Phi/D
A0 = sp.Rational(3)/x - 2*b/s
Nsc = -s*b   # sin x cos x
H = 2*c*(q*q-1)*Nsc/D
V = H - A0
G = u*V
Phix = 2*(q*q-1)*Nsc
ux_c = (Phi + x*Phix)/D - x*Phi*(c*Phix)/(D*D)
A0x_c = -sp.Rational(3)/(x*x) - 2/(s*s)
Hx_c = 2*c*(q*q-1)*((b*b - s*s)*D - s*(-b)*(c*Phix))/(D*D)
Gx_c = sp.cancel(ux_c*V + u*(Hx_c - A0x_c))
Gc_c = sp.cancel((-x*Phi*Phi/(D*D))*V + u*(2*(q*q-1)*Nsc*q/(D*D)))
J = sp.cancel(G*G + Gc_c - u*Gx_c)

def Dx(f):
    return sp.expand(sp.diff(f, x) + sp.diff(f, s)*(-b) + sp.diff(f, b)*s)

dJdx = sp.cancel(Dx(sp.cancel(J)))
num, den = sp.fraction(dJdx)
num = sp.expand(num)
print('dJ/dx|th numerator terms:', len(sp.Add.make_args(num)))
print('denominator factors:', sp.factor(den))
# also print Gx numerator for comparison
print()
dGdx = sp.cancel(Dx(sp.cancel(Gx_c)))
gn, gd = sp.fraction(dGdx)
gn = sp.expand(gn)
print('dGx/dx numerator terms:', len(sp.Add.make_args(gn)))
print('denominator:', sp.factor(gd))
sp.pickle.dump({'num': num, 'den': den, 'gnum': gn, 'gden': gd}, open('misc/zz_dJdx_num.pkl','wb'))
