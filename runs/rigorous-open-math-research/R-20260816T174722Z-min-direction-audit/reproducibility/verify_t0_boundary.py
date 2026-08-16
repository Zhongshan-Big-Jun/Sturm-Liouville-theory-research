# -*- coding: utf-8 -*-
"""Verify t=0 boundary analytic proof identities (Section 11.2)."""
import sympy as sp

x = sp.symbols('x', positive=True)
R = x*(1+2*x**2)/(2*x**2-1)
h = R + sp.atan(x) - sp.pi
hp = sp.diff(h, x)
print('h prime:', sp.factor(hp))
# R(27/20)
print('R(27/20):', sp.Rational(27,20), sp.simplify(R.subs(x, sp.Rational(27,20))))
print('25083/10580:', sp.Rational(25083,10580))
print('33/14:', sp.Rational(33,14))
print('3*pi/4 approx:', float(3*sp.pi/4), '33/14 approx:', float(sp.Rational(33,14)))
