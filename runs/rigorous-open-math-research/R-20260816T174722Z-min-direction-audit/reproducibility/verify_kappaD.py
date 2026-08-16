# -*- coding: utf-8 -*-
"""Verify kappa_D formula and difference identity for n>=3 mu=2 section."""
import sympy as sp

X, Y = sp.symbols('X Y', positive=True)
C = (3*Y-1)*(1-Y)
E = C + 2*Y*(Y-X)
kappa_N = C/E
kappa_D = (X**2 + 2*X*Y - 4*X + 1)/((1-X)*(1-3*X))
diff = sp.simplify(kappa_D - kappa_N)
rhs = 2*(Y-X)**2*(1-X*Y)/((1-X)*(1-3*X)*E)
print('kappa_D - kappa_N identity holds:', sp.simplify(diff - rhs) == 0)
print('kappa_D expression:', sp.factor(kappa_D))
print('kappa_N expression:', sp.factor(kappa_N))
