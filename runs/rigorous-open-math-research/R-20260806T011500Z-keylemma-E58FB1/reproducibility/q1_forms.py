# -*- coding: utf-8 -*-
"""q1_forms.py -- closed forms of J1, J2, Hp at q=1, in u = pi/(2(1+c))."""
import sympy as sp
u = sp.symbols('u', positive=True)
s, co = sp.sin(u), sp.cos(u)
W = 3 + 2*u*co/s
Wp = 2*(s*co - u)/s**2
# J1(1,c)*(1+c)^2 = W(u)^2 + W(u) + u*W'(u)
N1 = sp.expand(W**2 + W + u*Wp)
print('N1(u) = W^2 + W + uW\x27:')
print(sp.factor(sp.trigsimp(sp.expand(N1))))
print()
# J2(1,c)*(1+c)^2 with w = 2u: W(w)^2 + W(w) + w*W'(w)
w = 2*u
sw, cw = sp.sin(w), sp.cos(w)
Ww = 3 + 2*w*cw/sw
Ww_p = 2*(sw*cw - w)/sw**2
N2 = sp.expand(Ww**2 + Ww + w*Ww_p)
print('N2(2u) = W(2u)^2 + W(2u) + 2u*W\x27(2u):')
print(sp.factor(sp.trigsimp(sp.expand(N2))))
print()
# Hp(1,c)*(1+c)^2 = [2u W'(2u) + W(2u)] - [u W'(u) + W(u)]
Th = sp.expand((2*u*Ww_p + Ww) - (u*Wp + W))
print('Hp(1,c)*(1+c)^2 = T(2u)-T(u), T(u)=uW\x27(u)+W(u):')
print(sp.factor(sp.trigsimp(sp.expand(Th))))
print()
Tu = sp.expand(u*Wp + W)
print('T(u) = uW\x27 + W =', sp.trigsimp(Tu))
