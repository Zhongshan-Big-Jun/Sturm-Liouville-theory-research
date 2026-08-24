#!/usr/bin/env python3
"""Deterministic symbolic checks for B3-O3; evidence only, never the proof."""

import sympy as sp


s, c, q, z = sp.symbols("s c q z", nonzero=True)
r = 1 / s
E = sp.Matrix([[c, q], [-q, c]])
C = sp.Matrix(
    [
        [c**2 - r * q**2, (1 + r) * c * q],
        [-(1 + s) * c * q, c**2 - s * q**2],
    ]
)


def trig_reduce(expr):
    """Reduce a rational expression modulo c^2+q^2-1."""
    numerator, denominator = sp.fraction(sp.together(expr))
    remainder = sp.rem(
        sp.Poly(sp.expand(numerator), q),
        sp.Poly(q**2 + c**2 - 1, q),
    ).as_expr()
    return sp.factor(remainder / denominator)


expected_z = c**2 - (s + r) * q**2 / 2
assert trig_reduce(C.det() - 1) == 0
assert sp.factor(C.trace() - 2 * expected_z) == 0
assert trig_reduce((E * C)[0, 1] - q * (2 * expected_z + r)) == 0

# Check the claimed matrix-power and G formulas for a deterministic finite range.
U = [sp.Integer(1), 2 * z]
for k in range(2, 8):
    U.append(sp.expand(2 * z * U[-1] - U[-2]))

for n in range(1, 7):
    u_nm1 = U[n - 1]
    u_nm2 = sp.Integer(0) if n == 1 else U[n - 2]
    matrix_formula = u_nm1.subs(z, expected_z) * C - u_nm2.subs(z, expected_z) * sp.eye(2)
    for entry in C**n - matrix_formula:
        assert trig_reduce(entry) == 0
    p_n = U[n].subs(z, expected_z) + r * U[n - 1].subs(z, expected_z)
    assert trig_reduce((E * C**n)[0, 1] - q * p_n) == 0

print("PASS: determinant, trace, EC entry, and n=1..6 recurrence identities")
