import sympy as sp
t = sp.symbols('t', positive=True)
g = sp.atan(t)
A = sp.pi - g
sg = t/sp.sqrt(1+t**2); cg = 1/sp.sqrt(1+t**2)
z = 1/(1+4*t**2)
B7 = (A*(3+t**2) + 8*t)/(1+t**2)
Qlo = 4*A**2*z**2 - A*B7*z + 6*t**2/(1+t**2)**2
Qlo = sp.expand(Qlo)
print('Qlo(t) =', sp.simplify(Qlo))
print()
dQ = sp.simplify(sp.diff(Qlo, t))
print('dQlo/dt =', sp.factor(dQ))
