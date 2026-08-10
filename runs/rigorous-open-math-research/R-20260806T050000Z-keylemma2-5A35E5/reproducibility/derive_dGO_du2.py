# -*- coding: utf-8 -*-
"""derive_dGO_du2.py -- numerator structure of dG2/du."""
import sympy as sp

q, u = sp.symbols('q u', positive=True)
th = sp.atan(u/q)
sg = u/sp.sqrt(q**2+u**2); cg = q/sp.sqrt(q**2+u**2)
Phi = cg**2 + q**2*sg**2
c = sp.atan(u)/(sp.pi - th)
D = q + c*Phi
K = q**2 - 1
W2 = 3 - 2*(sp.pi - th)*cg/sg
G2 = -Phi*W2/D - 2*c*(sp.pi - th)*Phi*K*sg*cg/D**2
dG2du = sp.diff(G2, u)
num, den = sp.fraction(sp.cancel(dG2du))
N = sp.expand(num)
print('num = ')
print(N)
