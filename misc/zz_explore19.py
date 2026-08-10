import sympy as sp
g, q = sp.symbols('g q', positive=True)
A = sp.pi - g
sg, cg = sp.sin(g), sp.cos(g)
B1 = A*cg - 2*sg
M = 2*A**2*cg**2 - A**2 - 8*A*cg*sg + 6*sg**2
B2 = 4*A**2*cg**2 - A**2 - 12*A*cg*sg + 6*sg**2
B4 = 7*A*cg**2 - A*sg**2 - 4*cg*sg
B5 = A**2*cg**2 - A**2*sg**2 + 2*A**2 + 12*A*cg*sg - 12*sg**2
B7 = 3*A*cg**2 + A*sg**2 + 8*cg*sg
G5 = sp.expand(B5 - A*B4)
# c12: piecewise; use cg*max(|B2|,|M|)? no. For symbolic check use both variants.
t = sp.atan(q*sp.tan(g))
st, ct = sp.sin(t), sp.cos(t)
for label, c12 in [('B2var', cg*(-B2)), ('Mvar', cg*(-M))]:
    LB = c12*A**2*cg*st**2*ct**2 + 2*A**3*sg**2*t*ct**5 + G5*A*sg*t*st*ct*cg**2
    dL = sp.diff(LB, q)
    dL = sp.trigsimp(dL)
    print(label, 'dLB/dq =', sp.factor(dL))
    print()
