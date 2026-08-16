# -*- coding: utf-8 -*-
"""Derive N_b>0 condition in X,Y,kappa to identify kappa_0 (if possible)."""
import sympy as sp

x, y, r = sp.symbols('x y r', positive=True)
X, Y, kappa = sp.symbols('X Y kappa', positive=True)
# Original N_b
N_b = 2*r*x**3*y**2 + r*x*y**4 - 4*r*x*y**2 + r*x + 3*x**2*y**3 - 3*x**2*y - y**3 + y
# Substitute X=x^2, Y=y^2, kappa = r*x*(3Y-1)/(y(1-3X)) => r = kappa*y*(1-3X)/(x*(3Y-1))
r_sub = kappa*y*(1-3*X)/(x*(3*Y-1))
N_b_expr = sp.simplify(N_b.subs({x: sp.sqrt(X), y: sp.sqrt(Y), r: r_sub}))
print('N_b in X,Y,kappa:')
print(sp.factor(N_b_expr))
# solve N_b=0 for kappa
sol = sp.solve(sp.Eq(sp.factor(N_b_expr), 0), kappa)
print('solutions for kappa:', sol)
