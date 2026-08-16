"""Exact symbolic factorization of the t->0 normalized R17 gap limits.

This is a derivation aid.  It treats k, b, sigma as algebraic symbols and
prints factored numerators after clearing manifestly positive denominators.
"""

import sympy as sp


k, b, sigma = sp.symbols("k b sigma", positive=True)
k2 = k**2
D = b * (1 + k2 * b) + k2 * (1 + b) * sigma**2
C = sigma * (1 - k2 * b**2) / D
ebar = (b**2 - 1) / (1 - k**4 * b**2)
g = (1 + k2) * (1 - k2 * b**2) / (1 - k**4 * b**2)
w0 = (1 + k2 * b) / (1 + b)
w1 = k2 * (b**2 + b + sigma**2 + k2 * b * sigma**2) / D
P = 1 + k2

limits = {
    "L1": g,
    "L2": g - P * ebar * C**2 * w0**2 / 2,
    "L3": g - 3 * P * ebar * C**2 * w0 * w1 / 2,
    "L4": g - 3 * P * ebar * C**2 * w1**2,
}

for name, expr in limits.items():
    together = sp.factor(sp.together(expr))
    num, den = together.as_numer_denom()
    print(name)
    print("expr =", together)
    print("numerator =", sp.factor(num))
    print("denominator =", sp.factor(den))
    print()

print("w1/w0 =", sp.factor(w1 / w0))
print("C*w0 =", sp.factor(C * w0))
print("C*w1 =", sp.factor(C * w1))
print("w0-w1 =", sp.factor(w0 - w1))

# A coarse exact common-angle envelope is sigma*(1-k)<4.  Map the full
# algebraic superdomain 0<k,x,z<1 by kb=k+(1-k)x and
# sigma=4z/(1-k), then inspect ordinary monomial coefficients.
x, z = sp.symbols("x z", nonnegative=True)
bmap = (k + (1 - k) * x) / k
smap = 4 * z / (1 - k)
for name in ("L2", "L3", "L4"):
    mapped = sp.factor(sp.together(limits[name].subs({b: bmap, sigma: smap})))
    mnum, mden = mapped.as_numer_denom()
    mnum = sp.factor(mnum)
    poly = sp.Poly(sp.expand(mnum), k, x, z)
    coeffs = poly.coeffs()
    neg = [c for c in coeffs if c < 0]
    print(name, "mapped numerator factor =", mnum)
    print(name, "degrees =", poly.degree_list(), "terms =", len(coeffs), "negative =", len(neg))
    print(name, "negative coefficients =", neg[:30])
