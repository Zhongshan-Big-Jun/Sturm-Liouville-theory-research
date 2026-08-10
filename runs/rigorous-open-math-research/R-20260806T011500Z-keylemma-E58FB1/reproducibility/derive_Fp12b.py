# -*- coding: utf-8 -*-
"""derive_Fp12b.py -- Fp(q,1/2) via x parametrization q = cosx/(1-cosx)."""
import sympy as sp
x = sp.symbols('x', positive=True)
s = sp.sin(x); co = sp.cos(x)
q = co/(1-co)
Phi_x = sp.expand(co**2 + q**2*s**2)
D = sp.simplify(q + Phi_x/2)
Wx = 3 + 2*x*co/s
Wpix = 3 - 2*(sp.pi-x)*co/s
G1 = -Phi_x*Wx/D + x*Phi_x*(q**2-1)*s*co/D**2
G2 = -Phi_x*Wpix/D - (sp.pi-x)*Phi_x*(q**2-1)*s*co/D**2
M1 = x**2*s**2/D
M2 = (sp.pi-x)**2*s**2/D
Fp12 = sp.expand(M1*G1 - M2*G2)
# sign of Fp12 * D^3/(s^2 Phi) (positive prefactor)
N = sp.cancel(sp.together(Fp12*D**3/(s**2*Phi_x)))
num, den = sp.fraction(N)
num = sp.trigsimp(sp.expand(num))
print('q  =', sp.simplify(q))
print('Phi =', sp.trigsimp(Phi_x))
print('D   =', sp.simplify(D))
print()
print('N num =', sp.factor(num))
print('den   =', sp.factor(den))
