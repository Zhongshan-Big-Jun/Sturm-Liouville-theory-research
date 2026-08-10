import sympy as sp
g = sp.symbols('g', positive=True)
A = sp.pi - g
sg, cg = sp.sin(g), sp.cos(g)
D2 = 1 + 3*sg**2
z = cg**2/D2
B7 = 3*A*cg**2 + A*sg**2 + 8*cg*sg
Qlo = 4*A**2*z**2 - A*B7*z + 6*cg**2*sg**2
dQ = sp.expand(sp.diff(Qlo, g))
# collect by powers of g manually
def coeff_g(expr, k):
    e = sp.expand(expr)
    return sp.expand(sum(term for term in sp.Add.make_args(e) if sp.degree(term, g) == k))
C2 = coeff_g(dQ, 2)
C1 = coeff_g(dQ, 1)
C0 = coeff_g(dQ, 0)
print('C2 =', sp.factor(C2))
print()
print('C1 =', sp.factor(C1))
print()
print('C0 =', sp.factor(C0))
print()
# verify dQ == 2cg/D2^3 * (g^2 C2 + g C1 + C0)
test = sp.expand(2*cg/(D2**3)*(g**2*C2 + g*C1 + C0) - dQ)
print('check diff (should be 0):', sp.simplify(test))
