# -*- coding: utf-8 -*-
"""derive_Fp12.py -- closed form of Fp(q,1/2) in x = alpha0; verify and simplify."""
import sympy as sp
x, pi = sp.symbols('x pi', positive=True)
# q = 1/(2 sin^2(x/2)) - 1 ; parametrize via s=sin(x/2)?  Use half-angle.
s2 = sp.Rational(1,1)
# use t = sin(x/2)^2
t = sp.symbols('t', positive=True)
q_expr = 1/(2*t) - 1
# sin x = 2 sqrt(t(1-t)), cos x = 1 - 2t
# work symbolically with s = sin x, co = cos x and relations
s, co = sp.symbols('s co', positive=True)
Phi_x = co**2 + q_expr**2*s**2
D = q_expr + Phi_x/2
Wx = 3 + 2*x*co/s
Wpix = 3 - 2*(pi-x)*co/s
G1 = -Phi_x*Wx/D + x*Phi_x*(q_expr**2-1)*s*co/D**2
G2 = -Phi_x*Wpix/D - (pi-x)*Phi_x*(q_expr**2-1)*s*co/D**2
M1 = x**2*s**2/D
M2 = (pi-x)**2*s**2/D
Fp12 = sp.expand(M1*G1 - M2*G2)
# substitute s^2 = 4t(1-t), co = 1-2t, s*co = 2sqrt(t(1-t))(1-2t)  -- keep s*co symbolic first
expr = sp.cancel(sp.together(Fp12*D**3/(s**2*Phi_x)))
print('N(x) numerator (before trig substitution):')
print(sp.factor(sp.together(expr).as_numer_denom()[0]))
