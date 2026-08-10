# -*- coding: utf-8 -*-
"""Prove H(x)=2N0+N1 >= 0 on (0,pi): numeric check + derivative structure."""
import sympy as sp
import numpy as np

x = sp.symbols('x', positive=True)
H = 18*x - 10*sp.sin(2*x) + 2*x*sp.cos(4*x) + 4*x*sp.cos(2*x) - sp.sin(4*x)
H1 = sp.simplify(sp.diff(H, x))
H2 = sp.simplify(sp.diff(H, x, 2))
H3 = sp.simplify(sp.diff(H, x, 3))
print("H  =", sp.trigsimp(H))
print("H' =", sp.trigsimp(H1))
print("H''=", sp.trigsimp(H2))
print("H'''=", sp.factor(sp.trigsimp(H3)))
f = sp.lambdify(x, H, 'numpy')
f1 = sp.lambdify(x, H1, 'numpy')
f2 = sp.lambdify(x, H2, 'numpy')
xs = np.linspace(1e-6, np.pi-1e-6, 20001)
print("min H =", f(xs).min(), "at", xs[np.argmin(f(xs))])
print("min H' =", f1(xs).min())
print("min H'' =", f2(xs).min())
print("max H'' =", f2(xs).max())
# roots of H1
rts = []
for i in range(len(xs)-1):
    if f1(xs[i])*f1(xs[i+1]) < 0:
        rts.append(0.5*(xs[i]+xs[i+1]))
print("H' zeros:", [round(r,4) for r in rts])
