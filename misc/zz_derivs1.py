import sympy as sp
g = sp.symbols('g', positive=True)
A = sp.pi - g
sg, cg = sp.sin(g), sp.cos(g)
D2 = 1 + 3*sg**2
D = sp.sqrt(D2)
tmax = sp.atan(2*sp.tan(g))
TB = 2*A**3*sg**2*tmax*cg**5/D**5
dTB = sp.trigsimp(sp.diff(TB, g))
print('dTB/dg =', sp.factor(dTB))
print()
B1 = A*cg - 2*sg
M = 2*A**2*cg**2 - A**2 - 8*A*cg*sg + 6*sg**2
B2 = 4*A**2*cg**2 - A**2 - 12*A*cg*sg + 6*sg**2
G5 = sp.expand((A**2*cg**2 - A**2*sg**2 + 2*A**2 + 12*A*cg*sg - 12*sg**2) - A*(7*A*cg**2 - A*sg**2 - 4*cg*sg))
TC = G5*A*sg*cg**2
dTC = sp.trigsimp(sp.diff(TC, g))
print('dTC/dg =', sp.factor(dTC))
print()
B7 = 3*A*cg**2 + A*sg**2 + 8*cg*sg
z = cg**2/D2
Qlo = 4*A**2*z**2 - A*B7*z + 6*cg**2*sg**2
TD = tmax**2*cg*sg**2*Qlo
dTD = sp.trigsimp(sp.diff(TD, g))
print('dTD/dg =', sp.factor(dTD))
