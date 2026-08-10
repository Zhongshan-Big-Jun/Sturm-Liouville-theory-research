# -*- coding: utf-8 -*-
"""J in fully-substituted trig form; try factor/together."""
import sympy as sp

x, c, q = sp.symbols('x c q', positive=True)
sx = sp.sin(x); cx = sp.cos(x)
Phi = cx**2 + q**2*sx**2
D = q + c*Phi
W = 3 + 2*x/sx*cx
Wp = 2*cx/sx - 2*x/sx**2
sc = sx*cx

G = -Phi*W/D + 2*c*x*Phi*(q**2-1)*sc/(D**2)

dPhi = 2*sc*(q**2-1)
dD = c*dPhi
dsc = cx**2 - sx**2

term1 = -Phi*W/D
term2 = 2*c*x*Phi*(q**2-1)*sc/(D**2)

dt1 = -(dPhi*W + Phi*Wp)/D + Phi*W*dD/(D**2)
A = 2*c*(q**2-1)
num2 = A*(x*dPhi*sc + Phi*dsc + Phi*sc)
dt2 = num2/(D**2) - 2*c*x*Phi*(q**2-1)*sc*2*dD/(D**3)
Gx_expr = sp.simplify(dt1 + dt2)

dt1c = Phi*W*Phi/(D**2)
dt2c = 2*x*Phi*(q**2-1)*sc/(D**2) - 2*(2*c*x*Phi*(q**2-1)*sc)*Phi/(D**3)
Gc_expr = sp.simplify(dt1c + dt2c)

xp = -x*Phi/D
Gp = sp.simplify(Gx_expr*xp + Gc_expr)
J = sp.simplify(G**2 + Gp)

# Put over common denominator
num, den = sp.fraction(sp.together(J))
print("den =", sp.factor(den))
print()
num = sp.expand(num)
print("num (expanded, len %d):" % sp.count_ops(num))
print(num)
