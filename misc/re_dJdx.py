# -*- coding: utf-8 -*-
"""Print dGxdx 48-term numerator factored; compute dJ/dx numerator."""
import sympy as sp
x, th = sp.symbols('x th', positive=True)
s, b, S, C = sp.symbols('s b S C', positive=True)
Delta = b*s*th + C*S*x
u = b*s*x**2/Delta
A0 = sp.Rational(3)/x - 2*b/s
H = 2*th*(C**2*s**2 - S**2*b**2)/Delta
V = H - A0

def Dx(f):
    return sp.expand(sp.diff(f, x) + sp.diff(f, s)*(-b) + sp.diff(f, b)*s)
def Dth(f):
    return sp.expand(sp.diff(f, th) + sp.diff(f, S)*C + sp.diff(f, C)*(-S))

ux = Dx(u); Hx = Dx(H); A0x = Dx(A0)
Gx = ux*V + u*(Hx - A0x)
G = u*V
Gc = Dth(G)
J = G**2 + Gc - u*Gx
dGxdx = sp.cancel(Dx(sp.cancel(Gx)))
dnum, dden = sp.fraction(dGxdx)
dnum = sp.expand(dnum)
print('dGxdx numerator (%d terms):' % len(sp.Add.make_args(dnum)))
print(sp.factor(dnum))
print()
# dJ/dx
dJdx = sp.cancel(Dx(sp.cancel(J)))
jn, jd = sp.fraction(dJdx)
jn = sp.expand(jn)
print('dJdx numerator (%d terms):' % len(sp.Add.make_args(jn)))
print('den:', sp.factor(jd))
import pickle
pickle.dump({'dGxdx_num': dnum, 'dGxdx_den': dden, 'dJdx_num': jn, 'dJdx_den': jd}, open('misc/re_deriv_nums.pkl','wb'))
