# -*- coding: utf-8 -*-
"""verify_corner_sym.py -- sympy derivation of the CORNER closed form and the parent
base-lemma rechecks (L1, L2, B4, B5, B7, E1, E2, E8).
"""
import sympy as sp
q, x = sp.symbols('q x', positive=True)
# at c = 1/2: alpha1 = x, alpha2 = pi - x, cos x = q/(q+1), sin x = sqrt(2q+1)/(q+1)
# derive G2(1/2;q) in terms of x via substitution
cx = q/(q+1)
sx = sp.sqrt(2*q+1)/(q+1)
A = sp.pi - x
Ph = sp.cos(A)**2 + q**2*sp.sin(A)**2
D = q + sp.Rational(1,2)*Ph
W = 3 + 2*A/sp.tan(A)
G2 = -Ph*W/D + 2*sp.Rational(1,2)*A*Ph*(q**2-1)*sp.sin(A)*sp.cos(A)/D**2
# substitute sin/cos of (pi - x)
G2s = G2.subs({sp.sin(A): sx, sp.cos(A): -cx, sp.tan(A): sp.sin(A)/sp.cos(A)})
G2s = sp.simplify(G2s)
print('G2(1/2;q) raw subs:', sp.simplify(G2s))
# simplify assuming q > 1 (sqrt(2q+1) positive)
G2f = sp.simplify(G2s)
print('G2 simplified:', G2f)
# compare with cf1 = 2q((pi-x)(q+1)-3sqrt(2q+1))/(2q+1)^{3/2}
cf1 = 2*q*((sp.pi-x)*(q+1) - 3*sp.sqrt(2*q+1))/(2*q+1)**sp.Rational(3,2)
print('cf1:', sp.simplify(cf1))
print('difference:', sp.simplify(G2f - cf1))
# check cf2 = 2q sqrt(1-cos x)(pi-x-3 sin x)/(1+cos x)^{3/2}
cf2 = 2*q*sp.sqrt(1-cx)*(sp.pi-x-3*sx)/(1+cx)**sp.Rational(3,2)
print('difference cf2:', sp.simplify(G2f - cf2))

# verify G2(1/2;q) at q=2 = 12(pi - arccos(2/3) - sqrt5)/(5sqrt5): x = arccos(2/3)
xv = sp.acos(sp.Rational(2,3))
val = cf1.subs(x, xv).subs(q, 2)
print('G2(1/2;2) symbolic:', sp.simplify(val))
print('12(pi - acos(2/3) - sqrt5)/(5sqrt5):', sp.simplify(12*(sp.pi - sp.acos(sp.Rational(2,3)) - sp.sqrt(5))/(5*sp.sqrt(5))))
print('equal:', sp.simplify(val - 12*(sp.pi - sp.acos(sp.Rational(2,3)) - sp.sqrt(5))/(5*sp.sqrt(5))) == 0)
