import sympy as sp
g = sp.symbols('g', positive=True)
A = sp.pi - g
sg, cg = sp.sin(g), sp.cos(g)
D2 = 1 + 3*sg**2
z = cg**2/D2
B7 = 3*A*cg**2 + A*sg**2 + 8*cg*sg
Qlo = 4*A**2*z**2 - A*B7*z + 6*cg**2*sg**2
dQ = sp.diff(Qlo, g)
dQ = sp.expand(dQ)
# group by powers of g
poly = sp.Poly(dQ, g)
print('degree in g:', poly.degree())
C2 = sp.expand(poly.coeff_monomial(g**2))
C1 = sp.expand(poly.coeff_monomial(g))
C0 = sp.expand(poly.coeff_monomial(g**0))
den = 2*cg/(D2**3)
print('C2 =', sp.factor(C2))
print()
print('C1 =', sp.factor(C1))
print()
print('C0 =', sp.factor(C0))
print()
# verify: dQ == den*(g^2*C2 + g*C1 + C0) ?  (up to sign; check)
test = sp.expand(den*(g**2*C2 + g*C1 + C0) - dQ)
print('check diff =', sp.simplify(test))
