# -*- coding: utf-8 -*-
"""t3_Gx_c12b.py: f(x)=Gx(x,x/2) and f'' structure via (s,b,x) reduction."""
import sympy as sp
s, b, x = sp.symbols('s b x', positive=True)
# S^2=(1+b)/2, C^2=(1-b)/2, SC = s/2
S2, C2 = (1+b)/2, (1-b)/2
SC = s/2
# Gx closed form from t3_routeC_sympy3: Gx = 2x*N/(s*Delta^3) with th=x/2
th = x/2
# N_Gx terms from sympy output (as polynomial in s,b,S,C,x,th)
N = (C2**3*b**4*s**3*th**2 - C2**3*b**3*s**4*th**2*x + C2**3*b**3*s**2*th**2*x + C2**3*b**2*s**5*th**2 - C2**3*b*s**6*th**2*x
     + 2*C2**2*sp.sqrt(S2)*b**3*s**2*th*x + C2**2*sp.sqrt(S2)*b**2*s**3*th*x**2 + 2*C2**2*sp.sqrt(S2)*b**2*s*th*x**2
     - 2*C2**2*sp.sqrt(S2)*b*s**4*th*x + 3*C2**2*sp.sqrt(S2)*s**5*th*x**2)
