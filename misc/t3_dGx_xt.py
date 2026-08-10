# -*- coding: utf-8 -*-
"""t3_dGx_xt.py: numerators of dGx/dx and dGx/dth in (s,b,S,C,x,th) positive vars."""
import sympy as sp
s, b, S, C, x, th = sp.symbols('s b S C x th', positive=True)
q = S*b/(C*s)
Phi = b**2/C**2
D = b*s*th + C*S*x     # q + p*Phi after simplification: check
# verify D = q + p*Phi
Dexpr = q + (th/x)*Phi
print('D form check:', sp.simplify(sp.cancel(Dexpr - D)) == 0)
u = x*Phi/D
A0 = sp.Rational(3)/x - 2*b/s
H = 2*th*(C**2*s**2 - S**2*b**2)/D
V = H - A0
G = u*V
# partial derivatives at fixed q,p expressed via (x,th): chain rule
# d/dx |_th of f(x, th) with q=q(x,th), p=p(x,th) FIXED... NO.
