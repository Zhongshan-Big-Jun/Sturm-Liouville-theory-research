# -*- coding: utf-8 -*-
"""derive_dGO_du.py -- dG2/dgamma via u=q*tan(gamma); look for structure."""
import sympy as sp

q, u = sp.symbols('q u', positive=True)
# gamma = atan(u/q); all odd-curve quantities in (u, q)
th = sp.atan(u/q)          # gamma
sg = u/sp.sqrt(q**2+u**2); cg = q/sp.sqrt(q**2+u**2)
Phi = cg**2 + q**2*sg**2   # = q^2(1+u^2)/(q^2+u^2)
c = sp.atan(u)/(sp.pi - th)
D = q + c*Phi
K = q**2 - 1
W2 = 3 - 2*(sp.pi - th)*cg/sg
G2 = -Phi*W2/D - 2*c*(sp.pi - th)*Phi*K*sg*cg/D**2

# dG2/dgamma = dG2/du * du/dgamma ; du/dgamma = q sec^2(gamma) > 0
dG2du = sp.diff(G2, u)
expr = sp.cancel(dG2du)
num, den = sp.fraction(expr)
print('denom factors:', sp.factor(den))
print()
print('num (degree in u:', sp.degree(num, u), '):')
print(sp.expand(num))
