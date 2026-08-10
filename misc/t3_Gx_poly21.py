# -*- coding: utf-8 -*-
"""t3_Gx_poly21.py: P := 10*x*N_Gx - 21*s*Delta^3; structure."""
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
P = sp.expand(10*x*N - 21*s*Delta**3)
print('P terms:', len(sp.Add.make_args(P)))
# group by monomial in s,b,S,C
print('negative coefficient terms:')
for t in sp.Add.make_args(P):
    cf = sp.Poly(t, s,b,S,C).LC()
    if cf < 0:
        print('   ', sp.expand(t))
