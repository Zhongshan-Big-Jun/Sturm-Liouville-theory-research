import sympy as sp
g = sp.symbols('g', positive=True)
A = sp.pi - g
sg, cg = sp.sin(g), sp.cos(g)
B7 = 3*A*cg**2 + A*sg**2 + 8*cg*sg
D2 = 1 + 3*sg**2
z_lo = cg**2/D2
Qlo = 4*A**2*z_lo**2 - A*B7*z_lo + 6*cg**2*sg**2
dQ = sp.diff(Qlo, g)
dQ = sp.trigsimp(dQ)
print('dQ(z_lo)/dg =', sp.factor(dQ))
print()
Qhi = 4*A**2*cg**4 - A*B7*cg**2 + 6*cg**2*sg**2
dQh = sp.trigsimp(sp.diff(Qhi, g))
print('dQ(z_hi)/dg =', sp.factor(dQh))
