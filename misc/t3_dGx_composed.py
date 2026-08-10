# -*- coding: utf-8 -*-
"""t3_dGx_composed.py: composed partials of Gx via closed form, cancel-based."""
import sympy as sp
s, b, S, C, x, th = sp.symbols('s b S C x th', positive=True)
Delta = b*s*th + C*S*x
# N_Gx polynomial (40 terms) from t3_routeC_sympy3 output
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
# composed partials
dGxdx = sp.diff(Gx, x) + sp.diff(Gx, s)*(-b) + sp.diff(Gx, b)*s
dGxdt = sp.diff(Gx, th) + sp.diff(Gx, S)*C + sp.diff(Gx, C)*(-S)
for nm, e in [('dGxdx', dGxdx), ('dGxdt', dGxdt)]:
    e = sp.cancel(e)
    num = sp.expand(sp.numer(e)); den = sp.expand(sp.denom(e))
    print(nm, 'num terms:', len(sp.Add.make_args(num)), ' den terms:', len(sp.Add.make_args(den)))
    print('num sign-definite? grouped:', sp.expand(num))
    print()
