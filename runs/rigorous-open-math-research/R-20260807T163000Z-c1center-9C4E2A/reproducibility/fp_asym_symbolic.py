# -*- coding: utf-8 -*-
"""fp_asym_symbolic.py: exact symmetric-config secular + fp condition, expanded in eps=1/sqrt(R).
Variables: xi = delta*sqrt(R), kap = kappa*sqrt(R) (kappa = 2pi - s2).
"""
import sympy as sp

eps, xi, kap = sp.symbols("eps xi kap", positive=True)
delta = xi*eps
R = 1/eps**2

# --- s1 (even fundamental), small ---
# even secular: tan(s(1/2-delta))*tan(s*sqrt(R)*delta) = 1/sqrt(R)
s1 = sp.symbols("s1", positive=True)
E1 = sp.tan(s1*(sp.Rational(1,2)-delta))*sp.tan(s1*delta/eps) - eps
# expand in eps keeping s1 ~ eps^2 (lambda1 ~ eps^2): s1 = eps^2 * c1
c1 = sp.symbols("c1", positive=True)
s1e = eps**2*c1
E1s = sp.series(E1.subs(s1, s1e), eps, 0, 12).removeO().expand()
print("E1 expansion leading:")
print(sp.collect(E1s, eps))

# --- s2 (odd), s2 = 2pi - kap*eps ---
s2 = 2*sp.pi - kap*eps
# odd secular: tan(s2*sqrt(R)*delta) = -sqrt(R)*tan(s2*(1/2-delta))
LHS = sp.tan(s2*delta/eps)
RHS = -sp.tan(s2*(sp.Rational(1,2)-delta))/eps
E2 = LHS - RHS
E2s = sp.series(E2, eps, 0, 8).removeO().expand()
print("\nE2 expansion leading:")
print(sp.collect(sp.simplify(E2s), eps))
