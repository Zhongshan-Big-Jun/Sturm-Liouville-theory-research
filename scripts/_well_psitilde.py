# -*- coding: utf-8 -*-
"""Psi~'(x;m) threshold: clean analytic derivative scan (E3 evidence)."""
import sympy as sp
import numpy as np

x, m = sp.symbols('x m', positive=True)
W = sp.sin(x)**2 + m**2*sp.cos(x)**2
Psi = x*sp.cot(x) + (m**2-1)*x*sp.sin(x)*sp.cos(x)/W
dPsi = sp.simplify(sp.diff(Psi, x))
print("dPsi~ =", sp.factor(sp.trigsimp(dPsi)))

# numeric threshold via lambdify
f = sp.lambdify((x, m), dPsi, 'numpy')
xs = np.linspace(1e-6, np.pi-1e-6, 20001)
for mm in [1.01, 1.05, 1.10, 1.15, 1.20, 1.25, 1.30, 1.35, 1.40]:
    d = f(xs, mm)
    # exclude boundary artifacts: look at interior min (x < pi - 0.05)
    mask = xs < np.pi - 0.02
    print(f"m={mm:.2f}: min dPsi over (0, pi-0.02) = {d[mask].min():+.6f} at x={xs[mask][np.argmin(d[mask])]:.4f}")
