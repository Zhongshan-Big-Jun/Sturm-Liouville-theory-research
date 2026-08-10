# -*- coding: utf-8 -*-
"""Derive partials of u, V, ux, Hx, Gx, J w.r.t. x and theta; inspect numerators."""
import sympy as sp
x, th = sp.symbols('x th', positive=True)
s, b, S, C = sp.symbols('s b S C', positive=True)
Delta = b*s*th + C*S*x
u = b*s*x**2/Delta
A0 = sp.Rational(3)/x - 2*b/s
H = 2*th*(C**2*s**2 - S**2*b**2)/Delta
V = H - A0
Phi = b**2/C**2
q = S*b/(C*s)
c = th/x
D = q + c*Phi
# ux = du/dx at fixed theta
ux = sp.diff(u, x)
# Hx = dH/dx at fixed theta (partial, S,C,theta fixed)
Hx = sp.diff(H, x)
A0x = sp.diff(A0, x)
G = u*V
Gx = sp.diff(G, x)   # partial derivative wrt x at fixed theta (S,C fixed)
Gc = sp.diff(G, th)  # partial wrt theta at fixed x
J = G**2 + Gc - u*Gx

# For each, reduce modulo s^2+b^2-1, S^2+C^2-1 (careful: s,b are functions of x; but as partial at fixed theta, treat independently? NO!
# IMPORTANT: d/dx at fixed theta: s = sin x, b = -cos x are NOT independent of x.
# Correct: df/dx|th = f_x + f_s*cos x + f_b*sin x where f_s,f_b partials wrt s,b with x,th,S,C fixed, cos x = -b, sin x = s.
print("Need chain rule: d/dx|th f(x,s,b,S,C) = f_x + f_s*(-b) + f_b*(s) ; s^2+b^2=1")
