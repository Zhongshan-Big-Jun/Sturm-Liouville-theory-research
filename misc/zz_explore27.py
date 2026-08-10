import sympy as sp
g = sp.symbols('g', positive=True)
A = sp.pi - g
sg, cg = sp.sin(g), sp.cos(g)
D = sp.sqrt(1 + 3*sg**2)
tmax = sp.atan(2*sp.tan(g))
B1 = A*cg - 2*sg
M = 2*A**2*cg**2 - A**2 - 8*A*cg*sg + 6*sg**2
B2 = 4*A**2*cg**2 - A**2 - 12*A*cg*sg + 6*sg**2
B4 = 7*A*cg**2 - A*sg**2 - 4*cg*sg
B5 = A**2*cg**2 - A**2*sg**2 + 2*A**2 + 12*A*cg*sg - 12*sg**2
B7 = 3*A*cg**2 + A*sg**2 + 8*cg*sg
G5 = sp.expand(B5 - A*B4)
# c12: use cg*(-B2) for gamma<=g0 and cg*(-M) for gamma>=g0; compute derivative of each variant
for label, c12 in [('A_B2', cg*(-B2)), ('A_M', cg*(-M))]:
    TA = 4*c12*A**2*sg**2*cg**3/D**4
    dTA = sp.diff(TA, g)
    dTA = sp.trigsimp(dTA)
    print('TA(%s) derivative =' % label)
    print('  ', sp.factor(dTA))
    print()
TB = 2*A**3*sg**2*tmax*cg**5/D**5
dTB = sp.trigsimp(sp.diff(TB, g))
print('TB derivative =', sp.factor(dTB))
print()
TC = G5*A*sg*cg**2
dTC = sp.trigsimp(sp.diff(TC, g))
print('TC derivative (without m) =', sp.factor(dTC))
print()
TD = tmax**2*cg*sg**2*(4*A**2*(cg**2/D**2)**2 - A*B7*cg**2/D**2 + 6*cg**2*sg**2)
dTD = sp.trigsimp(sp.diff(TD, g))
print('TD derivative =', sp.factor(dTD))
