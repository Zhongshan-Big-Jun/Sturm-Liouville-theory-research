# t3_duA2.py: numerator of du/dA, manual differentiation
import sympy as sp
A, c = sp.symbols('A c', positive=True)
S, C, S2, C2 = sp.symbols('S C S2 C2', real=True)
# u = A*S/(c*S-S2); dS/dA=2C, dS2/dA=2c*C2
Nu = (S + 2*A*C)*(c*S - S2) - A*S*(2*c*C - 2*c*C2)
Nu = sp.expand(Nu)
print('Nu =', Nu)
print()
# signs: S<0 (sin2A<0), S2>0 (sin2cA>0), C2<0 (cos2cA<0), C=cos2A unknown sign
# express with a=-S>0, s2=S2>0, b=-C2>0: S=-a, C2=-b
a, s2, b = sp.symbols('a s2 b', positive=True)
Nu_s = sp.expand(Nu.subs({S:-a, C2:-b}))
print('Nu in magnitudes (S=-a, C2=-b):')
print(Nu_s)
print('= c*a^2 + a*s2 - 2Ac*a*b - 2A*C*s2')
print()
# Case C<=0: then -2A*C*s2 >= 0, need c*a^2 + a*s2 - 2Ac*a*b >= 0
# Case C>0: need full
