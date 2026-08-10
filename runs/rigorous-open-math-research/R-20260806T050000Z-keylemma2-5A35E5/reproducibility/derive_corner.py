# -*- coding: utf-8 -*-
"""derive_corner.py -- closed forms at c=1/2 and dG2/dq structure."""
import sympy as sp

q = sp.symbols('q', positive=True)
x = sp.symbols('x', positive=True)  # x = alpha_0
# relations at c=1/2: cos x = q/(q+1), sin x = sqrt(2q+1)/(q+1)
sx = sp.sqrt(2*q+1)/(q+1)
cx = q/(q+1)

# gamma = x, alpha_2 = pi - x
Phi = 2*q**2/(q+1)
c = sp.Rational(1,2)
t = sx/cx
D = q + c*Phi
W2 = 3 - 2*(sp.pi - x)/t
sc = sx*cx
G2h = -Phi*W2/D - 2*c*(sp.pi - x)*Phi*(q**2-1)*sc/D**2
G2h = sp.simplify(sp.expand(G2h))

print('G2(1/2;q) =', G2h)
print()
# substitute x = alpha0(q) = 2 asin(1/sqrt(2(q+1)))
xsub = 2*sp.asin(1/sp.sqrt(2*(q+1)))
G2hq = sp.simplify(sp.expand(G2h.subs(x, xsub)))
print('G2(1/2;q) with x=alpha0(q):', G2hq)
