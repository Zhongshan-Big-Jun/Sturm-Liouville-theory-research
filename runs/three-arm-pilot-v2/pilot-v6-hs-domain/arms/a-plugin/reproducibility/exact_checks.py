#!/usr/bin/env python3
"""Deterministic exact probes; evidence only, not the general proof."""

import sympy as sp

x = sp.symbols("x", real=True)
c = sp.symbols("c", positive=True)
k = sp.symbols("k", positive=True)


def formal_inverse_power(poly, power):
    degree = sp.Poly(poly, x).degree()
    return sp.expand(
        sum(
            sp.binomial(power + j - 1, j)
            * sp.diff(poly, x, 2 * j)
            / c ** (power + j)
            for j in range(degree // 2 + 1)
        )
    )


def krein_residual(poly):
    delta = sp.expand(poly.subs(x, 1) - poly.subs(x, -1))
    return (
        sp.factor(sp.diff(poly, x).subs(x, 1) - delta / 2),
        sp.factor(sp.diff(poly, x).subs(x, -1) - delta / 2),
    )


for power in range(1, 5):
    for n in range(9):
        p = sp.legendre(n, x)
        q = formal_inverse_power(p, power)
        if power > 1:
            previous = formal_inverse_power(p, power - 1)
            assert sp.simplify(c * q - sp.diff(q, x, 2) - previous) == 0
        else:
            assert sp.simplify(c * q - sp.diff(q, x, 2) - p) == 0
        residual = krein_residual(q)
        is_zero = all(sp.simplify(entry) == 0 for entry in residual)
        assert is_zero == (n <= 1)
        print(f"r={power} n={n} B={residual}")

u_poly = x**2 / k**2 + 2 / k**4
u_operator = u_poly - 2 * sp.cosh(k * x) / (k**3 * sp.sinh(k))
assert sp.simplify(-sp.diff(u_operator, x, 2) + k**2 * u_operator - x**2) == 0
assert all(sp.simplify(entry) == 0 for entry in krein_residual(u_operator))
assert any(sp.simplify(entry) != 0 for entry in krein_residual(u_poly))
print("x^2 formal residual:", krein_residual(u_poly))
print("x^2 operator residual:", krein_residual(u_operator))
print("ALL_EXACT_CHECKS_PASS")
