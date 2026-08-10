# -*- coding: utf-8 -*-
"""Interior max of dPsi~ over (0, pi/2) -> threshold m_c (E3)."""
import sympy as sp
import numpy as np

x, m = sp.symbols('x m', positive=True)
W = sp.sin(x)**2 + m**2*sp.cos(x)**2
Psi = x*sp.cot(x) + (m**2-1)*x*sp.sin(x)*sp.cos(x)/W
dPsi = sp.simplify(sp.diff(Psi, x))
f = sp.lambdify((x, m), dPsi, 'numpy')
xs = np.linspace(1e-4, np.pi/2 - 1e-4, 20001)
for mm in [1.0, 1.05, 1.1, 1.15, 1.2, 1.25, 1.3, 1.35, 1.4, 1.5]:
    d = f(xs, mm)
    print(f"m={mm:.2f}: max dPsi over (0,pi/2) = {d.max():+.6f} at x={xs[np.argmax(d)]:.4f}")
# bisect
def mx(mm):
    return f(xs, mm).max()
lo, hi = 1.0, 1.6
for _ in range(40):
    mid = 0.5*(lo+hi)
    if mx(mid) > 0: hi = mid
    else: lo = mid
mc = 0.5*(lo+hi)
print(f"m_c(Psi~'>=0 first) = {mc:.6f} -> R_c = {mc**2:.6f}")
