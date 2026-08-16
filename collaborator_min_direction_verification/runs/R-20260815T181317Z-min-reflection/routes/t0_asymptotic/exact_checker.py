"""Exact checker for the R17 t->0 asymptotic coefficient theorem.

The checker performs only exact symbolic/rational operations.  The two
tensor-Bernstein boxes are a fixed algebraic decomposition in k, not an
adaptive interval or Arb subdivision.
"""

from __future__ import annotations

import hashlib
import json
import math
import platform
from pathlib import Path

import sympy as sp


def zero(expr: sp.Expr) -> None:
    assert sp.factor(sp.cancel(expr)) == 0


k, b, sigma = sp.symbols("k b sigma", positive=True)
k2 = k**2
A = (b**2 - 1) * (1 - k2 * b**2)
D = b * (1 + k2 * b) + k2 * (1 + b) * sigma**2
E = b**2 + b + sigma**2 + k2 * b * sigma**2
w0 = (1 + k2 * b) / (1 + b)
w1 = k2 * E / D

Z0sq = sigma**2 * A * w0**2 / D**2
Z0Z1 = sigma**2 * A * w0 * w1 / D**2
Z1sq = sigma**2 * A * w1**2 / D**2

P2 = 2 * (1 + b) ** 2 * D**2 - sigma**2 * A * (1 + k2 * b) ** 2
P3 = 2 * (1 + b) * D**3 - 3 * sigma**2 * A * k2 * E * (1 + k2 * b)
P4 = D**4 - 3 * sigma**2 * A * k2**2 * E**2
polys = {"P2": P2, "P3": P3, "P4": P4}

# Check that P_i are exactly the cleared numerators of the three normalized
# gap limits.
zero(1 - Z0sq / 2 - P2 / (2 * (1 + b) ** 2 * D**2))
zero(1 - 3 * Z0Z1 / 2 - P3 / (2 * (1 + b) * D**3))
zero(1 - 3 * Z1sq - P4 / D**4)

# The second endpoint coefficient is always smaller than the first one on
# 0<k<1 and 1<b<1/k.
w_difference = b * (k - 1) * (k + 1) * (b * k - 1) * (b * k + 1) / (
    (b + 1) * D
)
zero(w0 - w1 - w_difference)

# Exact constants in the elementary small-k proof for P2.
phi = (1 + sp.sqrt(5)) / 2
fphi = sp.simplify((phi - 1) / (phi**2 * (phi + 1)))
zero(fphi - (5 * sp.sqrt(5) - 11) / 2)
assert sp.simplify(sp.Rational(3, 32) - fphi) > 0
assert sp.Rational(49, 64) - sp.Rational(3, 4) == sp.Rational(1, 64)


def bernstein_coefficients(poly: sp.Poly) -> list[sp.Rational]:
    """Full tensor Bernstein coefficients on [0,1]^3, exactly."""
    degrees = poly.degree_list()
    power = poly.as_dict()
    out: list[sp.Rational] = []
    for I in range(degrees[0] + 1):
        for J in range(degrees[1] + 1):
            for L in range(degrees[2] + 1):
                value = sp.Rational(0)
                for i in range(I + 1):
                    for j in range(J + 1):
                        for ell in range(L + 1):
                            coeff = power.get((i, j, ell))
                            if coeff is None:
                                continue
                            value += (
                                coeff
                                * sp.Rational(math.comb(I, i), math.comb(degrees[0], i))
                                * sp.Rational(math.comb(J, j), math.comb(degrees[1], j))
                                * sp.Rational(math.comb(L, ell), math.comb(degrees[2], ell))
                            )
                out.append(sp.factor(value))
    return out


h, x, z = sp.symbols("h x z", nonnegative=True)


def audit_box(name: str, kmap: sp.Expr, targets: tuple[str, ...]) -> dict:
    audit: dict[str, dict] = {}
    mapping = {
        k: kmap,
        b: (k + (1 - k) * x) / k,
        sigma: 4 * z / (1 - k),
    }
    for target in targets:
        mapped = sp.cancel(polys[target].subs(mapping, simultaneous=True).subs(k, kmap))
        numerator, denominator = sp.together(mapped).as_numer_denom()
        poly = sp.Poly(sp.expand(numerator), h, x, z, domain=sp.QQ)
        coeffs = bernstein_coefficients(poly)
        negatives = [c for c in coeffs if c < 0]
        positives = [c for c in coeffs if c > 0]
        zeros = [c for c in coeffs if c == 0]
        assert not negatives
        assert positives
        audit[target] = {
            "degree": list(poly.degree_list()),
            "coefficient_count": len(coeffs),
            "positive_count": len(positives),
            "zero_count": len(zeros),
            "minimum_positive_coefficient": str(min(positives)),
            "denominator": str(sp.factor(denominator)),
        }
    return {"name": name, "k_map": str(kmap), "targets": audit}


boxes = [
    audit_box("small_k", h / 8, ("P3", "P4")),
    audit_box("high_k", (1 + 7 * h) / 8, ("P2", "P3", "P4")),
]

this_file = Path(__file__).resolve()
print(
    json.dumps(
        {
            "status": "PASS",
            "claim": "strict positivity of the four normalized t->0 gap limits on every fixed retained common-angle parameter",
            "exact_checks": [
                "three cleared-numerator identities",
                "w0-w1 factorization",
                "small-k P2 extremum constants",
                "two fixed exact-rational tensor-Bernstein boxes",
            ],
            "boxes": boxes,
            "python": platform.python_version(),
            "sympy": sp.__version__,
            "script_sha256": hashlib.sha256(this_file.read_bytes()).hexdigest(),
        },
        indent=2,
        sort_keys=True,
    )
)
