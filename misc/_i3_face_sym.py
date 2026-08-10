# -*- coding: utf-8 -*-
"""J on face c=0.5 in y=pi-x coords: factor numerator."""
import sympy as sp
x, q = sp.symbols('x q', positive=True)
y = sp.Symbol('y', positive=True)
# work with x, then substitute x = pi - y at the end
sx = sp.sin(x); cx = sp.cos(x)
Ph = cx**2 + q**2*sx**2
c = sp.Rational(1,2)
D = q + c*Ph
W = 3 + 2*x/sx*cx
Wp = 2*cx/sx - 2*x/sx**2
sc = sx*cx
G = -Ph*W/D + 2*c*x*Ph*(q**2-1)*sc/(D**2)
dPhi = 2*sc*(q**2-1); dD = c*dPhi; dsc = cx**2 - sx**2
term1 = -Ph*W/D
term2 = 2*c*x*Ph*(q**2-1)*sc/(D**2)
dt1 = -(dPhi*W + Ph*Wp)/D + Ph*W*dD/(D**2)
A = 2*c*(q**2-1)
num2 = A*(x*dPhi*sc + Ph*dsc + Ph*sc)
dt2 = num2/(D**2) - 2*c*x*Ph*(q**2-1)*sc*2*dD/(D**3)
Gx_expr = sp.simplify(dt1 + dt2)
dt1c = Ph*W*Ph/(D**2)
dt2c = 2*x*Ph*(q**2-1)*sc/(D**2) - 2*(2*c*x*Ph*(q**2-1)*sc)*Ph/(D**3)
Gc_expr = sp.simplify(dt1c + dt2c)
xp = -x*Ph/D
Gp = sp.simplify(Gx_expr*xp + Gc_expr)
J = sp.simplify(G**2 + Gp)
num, den = sp.fraction(sp.together(J))
print("den =", sp.factor(den))
num2_ = sp.expand(num)
print("num ops:", sp.count_ops(num2_))
# try to factor
f1 = sp.factor(num2_)
print("factor:", f1)
# try collecting in q
poly = sp.Poly(num2_, q)
print("poly in q, degree:", poly.degree())
for dg in range(poly.degree()+1):
    cf = sp.simplify(poly.coeff_monomial(q**dg))
    print("coeff q^%d: ops=%d" % (dg, sp.count_ops(cf)))
