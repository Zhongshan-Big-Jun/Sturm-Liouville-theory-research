# -*- coding: utf-8 -*-
"""Symbolic dJ1_2d/dx, dJ1_2d/dq with c = E(x)/x substituted."""
import sympy as sp
x, q = sp.symbols('x q', positive=True)
# c = E(x)/x with E = atan(1/(q tan x))
c = sp.atan(1/(q*sp.tan(x)))/x
sx = sp.sin(x); cx = sp.cos(x)
Ph = cx**2 + q**2*sx**2
D = q + c*Ph
W = 3 + 2*x/sx*cx
Wp = 2*cx/sx - 2*x/sx**2
sc = sx*cx
G = -Ph*W/D + 2*c*x*Ph*(q**2-1)*sc/(D**2)
dPhi = 2*sc*(q**2-1); dD = c*dPhi; dsc = cx**2 - sx**2
term1 = -Ph*W/D; term2 = 2*c*x*Ph*(q**2-1)*sc/(D**2)
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

# J1_2d = J(x, E(x)/x, q). d/dx total:
dc_dx = sp.diff(c, x)
J1 = sp.simplify(J.subs(c, sp.atan(1/(q*sp.tan(x)))/x))
# Actually J already has c as symbol; build J1 explicitly
J1 = J  # c is already substituted
dJ1dx = sp.simplify(sp.diff(J1, x))
print("dJ1_2d/dx ops:", sp.count_ops(dJ1dx))
dJ1dq = sp.simplify(sp.diff(J1, q))
print("dJ1_2d/dq ops:", sp.count_ops(dJ1dq))
