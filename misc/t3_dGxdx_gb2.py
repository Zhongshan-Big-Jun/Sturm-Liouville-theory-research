# -*- coding: utf-8 -*-
"""t3_dGxdx_gb2.py: reduce dGx/dx numerator mod ideal over Q(x,th)."""
import sympy as sp
s, b, S, C, x, th = sp.symbols('s b S C x th', positive=True)
Delta = b*s*th + C*S*x
N = (C**6*b**4*s**3*th**2 - C**6*b**3*s**4*th**2*x + C**6*b**3*s**2*th**2*x + C**6*b**2*s**5*th**2 - C**6*b*s**6*th**2*x
     + 2*C**5*S*b**3*s**2*th*x + C**5*S*b**2*s**3*th*x**2 + 2*C**5*S*b**2*s*th*x**2 - 2*C**5*S*b*s**4*th*x + 3*C**5*S*s**5*th*x**2
     + C**4*S**2*b**5*s**2*th**2*x + 2*C**4*S**2*b**4*s**3*th**2 + C**4*S**2*b**3*s**4*th**2*x + 3*C**4*S**2*b**3*s**2*th**2*x
     + 2*C**4*S**2*b**2*s**5*th**2 + C**4*S**2*b**2*s*x**2 + 2*C**4*S**2*b*s**2*x**3 + C**4*S**2*b*x**3 - 3*C**4*S**2*s**3*x**2
     - C**3*S**3*b**4*s*th*x**2 + 6*C**3*S**3*b**3*s**2*th*x - 4*C**3*S**3*b**2*s**3*th*x**2 + 4*C**3*S**3*b**2*s*th*x**2
     - 2*C**3*S**3*b*s**4*th*x + C**3*S**3*s**5*th*x**2
     + C**2*S**4*b**4*s**3*th**2 + C**2*S**4*b**3*s**4*th**2*x + 3*C**2*S**4*b**3*s**2*th**2*x - 2*C**2*S**4*b**3*x**3
     + C**2*S**4*b**2*s**5*th**2 + 4*C**2*S**4*b**2*s*x**2 + C**2*S**4*b*s**6*th**2*x + C**2*S**4*b*x**3
     + C*S**5*b**4*s*th*x**2 + 4*C*S**5*b**3*s**2*th*x - C*S**5*b**2*s**3*th*x**2 + 2*C*S**5*b**2*s*th*x**2
     - S**6*b**5*s**2*th**2*x - S**6*b**3*s**4*th**2*x + S**6*b**3*s**2*th**2*x)
Gx = 2*x*N/(s*Delta**3)
dGxdx = sp.cancel(sp.diff(Gx, x) + sp.diff(Gx, s)*(-b) + sp.diff(Gx, b)*s)
num = sp.Poly(sp.expand(sp.numer(dGxdx)), s, b, S, C, domain=sp.QQ.frac_field(x, th))
G = [s**2 + b**2 - 1, S**2 + C**2 - 1]
B = sp.groebner(G, s, b, S, C, domain=sp.QQ.frac_field(x, th))
red = B.reduce(num)[0]
red = sp.expand(sp.simplify(red.as_expr()))
print('reduced terms:', len(sp.Add.make_args(red)))
print(red)
