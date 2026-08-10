# -*- coding: utf-8 -*-
"""Expand J numerator in powers of r = q^2-1, then in u = x*cot x, check coefficient signs on B1."""
import sympy as sp
x, c, q = sp.symbols('x c q', positive=True)
sx = sp.sin(x); cx = sp.cos(x)
Phi = cx**2 + q**2*sx**2
D = q + c*Phi
W = 3 + 2*x/sx*cx
Wp = 2*cx/sx - 2*x/sx**2
sc = sx*cx
G = -Phi*W/D + 2*c*x*Phi*(q**2-1)*sc/(D**2)
dPhi = 2*sc*(q**2-1); dD = c*dPhi; dsc = cx**2 - sx**2
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
num, den = sp.fraction(sp.together(J))

# express in s = sin x, keep cos via identity, substitute r = q^2 - 1
s = sp.symbols('s', positive=True)
r = sp.symbols('r', nonnegative=True)  # q^2-1
num2_ = num.subs(sp.sin(x), sp.sqrt(s)).subs(sp.cos(x), sp.sqrt(1-s)).subs(q, sp.sqrt(1+r))
num2_ = sp.expand(num2_)
# but sqrt expressions remain; instead expand in r first with sin/cos as symbols
num_r = sp.Poly(num, q)
print("degree in q:", num_r.degree())
# expand in q^2-1 via substitution q^2 = 1+r
num_q2 = num.as_poly(q) if num.is_polynomial(q) else None
if num_q2 is not None:
    q2 = sp.symbols('q2', positive=True)
    numq = num.subs(q**2, q2)
    numq = sp.expand(numq)
    poly_q2 = sp.Poly(numq, q2)
    print("degree in q2:", poly_q2.degree())
    # but q also appears linearly (not just q^2). Count:
    print("terms with odd powers of q present:", num.has(q))
