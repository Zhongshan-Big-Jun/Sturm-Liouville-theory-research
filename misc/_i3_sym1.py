# -*- coding: utf-8 -*-
"""Derive J = G^2 + G' symbolically, parametrize by s=sin x."""
import sympy as sp

x, c, q = sp.symbols('x c q', positive=True)
s = sp.symbols('s', positive=True)
# substitute sin x = s, cos x = sqrt(1-s^2)? Keep cos symbolic as cc with cc^2+s^2=1.
cc = sp.symbols('cc')
Phi = cc**2 + q**2*s**2
D = q + c*Phi
W = 3 + 2*x/mp_tan if False else sp.Symbol('W')  # placeholder

# We need W = 3 + 2x/tan x. Keep as symbol W but remember dW/dx.
W = sp.Symbol('W')
sc = s*cc
G = -Phi*W/D + 2*c*x*Phi*(q**2-1)*sc/(D**2)

# Partial derivatives with respect to x and c.
# dPhi/dx = 2*cc*(-s) + 2 q^2 s cc = 2 sc (q^2-1)
# dW/dx = 2/tan x - 2x/sin^2 x  -> keep symbolic as Wp
Wp = sp.Symbol('Wp')
dPhi = 2*sc*(q**2-1)
dsc = cc**2 - s**2

Gx = sp.diff(G, x)
# sympy needs x-dependent expressions; better to build manually.
# Let me just do it manually.
Ph = Phi
Dv = D
# G = -Ph*W/D + 2*c*x*Ph*(q**2-1)*sc/D^2
term1 = -Ph*W/Dv
term2 = 2*c*x*Ph*(q**2-1)*sc/(Dv**2)

dPh = 2*sc*(q**2-1)
dW = Wp
dD = c*dPh
dsc = cc**2 - s**2

# d term1/dx
dt1 = -(dPh*W + Ph*dW)/Dv + Ph*W*dD/(Dv**2)
# d term2/dx
A = 2*c*(q**2-1)
num2 = A*(x*dPh*sc + Ph*dsc + Ph*sc)
dt2 = num2/(Dv**2) - 2*c*x*Ph*(q**2-1)*sc*2*dD/(Dv**3)
Gx_expr = sp.simplify(dt1 + dt2)

# dG/dc
dt1c = Ph*W*Ph/(Dv**2)
dt2c = 2*x*Ph*(q**2-1)*sc/(Dv**2) - 2*(2*c*x*Ph*(q**2-1)*sc)*Ph/(Dv**3)
Gc_expr = sp.simplify(dt1c + dt2c)

# alpha'(c) = -x*Ph/Dv
xp = -x*Ph/Dv
Gp = sp.simplify(Gx_expr*xp + Gc_expr)
J = sp.simplify(G**2 + Gp)

print("G =", sp.simplify(G))
print()
print("Gx =", sp.simplify(Gx_expr))
print()
print("Gc =", sp.simplify(Gc_expr))
print()
print("J =", J)
