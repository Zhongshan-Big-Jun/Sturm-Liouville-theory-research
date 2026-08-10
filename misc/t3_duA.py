# t3_duA.py: simplify numerator of du/dA at fixed c
import sympy as sp
A, c = sp.symbols('A c', positive=True)
S, C, S2, C2 = sp.symbols('S C S2 C2', real=True)  # sin2A, cos2A, sin2cA, cos2cA
# u = A*S/(c*S - S2)
u = A*S/(c*S - S2)
# du/dA at fixed c: treat S,S2,C2 as functions of A: dS/dA=2C, dS2/dA=2c*C2
Nu = sp.diff(A*S, A)*(c*S-S2) - A*S*sp.diff(c*S-S2, A)
Nu = sp.expand(Nu)
print('Nu =', Nu)
# substitute C^2 = 1-S^2, C2^2 = 1-S2^2 to reduce, then try factor
Nu2 = Nu.subs({C**2: 1-S**2, C2**2: 1-S2**2})
print('Nu (reduced) =', sp.factor(Nu2))
