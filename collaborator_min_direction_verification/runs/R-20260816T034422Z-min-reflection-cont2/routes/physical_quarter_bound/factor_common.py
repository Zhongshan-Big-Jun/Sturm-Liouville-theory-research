"""Exact algebraic factor discovery for the t=0 quarter ratios."""

import sympy as sp


k, x, s = sp.symbols("k x s", positive=True)
b = s / x
A = (b**2 - 1) * (1 - k**2 * b**2)
D = b * (1 + k**2 * b) + k**2 * (1 + b) * s**2
E = b**2 + b + s**2 + k**2 * b * s**2
w0 = (1 + k**2 * b) / (1 + b)
w1 = k**2 * E / D
Z0sq = sp.factor(sp.cancel(s**2 * A * w0**2 / D**2))
Z0Z1 = sp.factor(sp.cancel(s**2 * A * w0 * w1 / D**2))
Z1sq = sp.factor(sp.cancel(s**2 * A * w1**2 / D**2))
for name, expr in (("Z0sq", Z0sq), ("Z0Z1", Z0Z1), ("Z1sq", Z1sq)):
    print(name, "=", expr)

print("w1/w0 =", sp.factor(sp.cancel(w1 / w0)))
print("dlogZ0sq/ds numerator =", sp.factor(sp.together(sp.diff(sp.log(Z0sq), s)).as_numer_denom()[0]))
