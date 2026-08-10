# -*- coding: utf-8 -*-
"""Verify Psi~' < 0 on full (0,pi) for m<=sqrt(1.5), and r~_tau decreasing at R=1.5 (E3)."""
import sympy as sp
import numpy as np

x, m = sp.symbols('x m', positive=True)
W = sp.sin(x)**2 + m**2*sp.cos(x)**2
Psi = x*sp.cot(x) + (m**2-1)*x*sp.sin(x)*sp.cos(x)/W
dPsi = sp.simplify(sp.diff(Psi, x))
f = sp.lambdify((x, m), dPsi, 'numpy')
xs = np.linspace(1e-4, np.pi-1e-4, 40001)
for mm in [1.20, 1.2247, 1.23, 1.25]:
    d = f(xs, mm)
    print(f"m={mm:.4f}: max dPsi over (0,pi) interior = {d.max():+.6f}")
# r~_tau decreasing check at m=sqrt(1.5), several tau
m0 = np.sqrt(1.5)
J = lambda t: np.sin(t)**2/(np.sin(t)**2 + m0*m0*np.cos(t)**2)
for tau in [1.2, 1.5, 1.9, 2.0]:
    xs2 = np.linspace(1e-6, np.pi/tau-1e-6, 40001)
    lr = np.log(J(tau*xs2)/J(xs2))
    d = np.diff(lr)
    print(f"  m=sqrt(1.5) tau={tau}: r~_tau decreasing (all steps <0): {bool(np.all(d<0))}  max step {d.max():+.4e}")
