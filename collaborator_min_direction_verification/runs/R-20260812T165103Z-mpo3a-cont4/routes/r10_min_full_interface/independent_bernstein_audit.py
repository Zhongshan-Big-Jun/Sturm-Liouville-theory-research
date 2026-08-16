#!/usr/bin/env python3
"""Independent exact Bernstein audit of the mu=2 interface residual.

This script reconstructs the already frozen primitive residual P from the
exact interface script, applies a different (coarser) box substitution, and
checks all tensor Bernstein coefficients over QQ.  It is proof-supporting
exact computation, not a floating-point positivity test.
"""

from __future__ import annotations

import hashlib
import json
from math import comb
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "r9_min_complementary" / "symbolic_split_gap_mu2.py"


def load_residual():
    source = SOURCE.read_text(encoding="utf-8")
    marker = "print(json.dumps(report, indent=2, sort_keys=True))"
    replacement = 'globals()["_R10_CAPTURE"] = residual.as_expr()'
    if marker not in source:
        raise RuntimeError("source emission marker changed")
    namespace: dict[str, object] = {}
    exec(compile(source.replace(marker, replacement), str(SOURCE), "exec"), namespace)
    namespace["main"]()
    return namespace["_R10_CAPTURE"]


def bernstein_coefficients(poly: sp.Poly):
    degrees = poly.degree_list()
    monomial = poly.as_dict()
    values = []
    for i0 in range(degrees[0] + 1):
        for i1 in range(degrees[1] + 1):
            for i2 in range(degrees[2] + 1):
                value = sp.Integer(0)
                for j0 in range(i0 + 1):
                    for j1 in range(i1 + 1):
                        for j2 in range(i2 + 1):
                            value += (
                                monomial.get((j0, j1, j2), 0)
                                * sp.Rational(comb(i0, j0), comb(degrees[0], j0))
                                * sp.Rational(comb(i1, j1), comb(degrees[1], j1))
                                * sp.Rational(comb(i2, j2), comb(degrees[2], j2))
                            )
                values.append(((i0, i1, i2), sp.factor(value)))
    return degrees, values


def main() -> int:
    P = load_residual()
    x, y, r = sp.symbols("x y r", positive=True)
    X, Y, kappa = sp.symbols("X Y kappa", positive=True)

    # kappa is the exact dimensionless interface ratio.  The physical
    # chamber implies 0<kappa<1; the proof below only uses this weaker box.
    r_of_kappa = kappa * y * (1 - 3 * x**2) / (x * (3 * y**2 - 1))
    raw = sp.cancel(P.subs(r, r_of_kappa))
    numerator, denominator = sp.fraction(raw)
    numerator = sp.factor(numerator / y**4)
    denominator = sp.factor(denominator)
    assert denominator == (3 * y**2 - 1) ** 2

    # Every exponent of x,y is even after the harmless y^4 removal.
    raw_poly = sp.Poly(numerator, x, y, kappa)
    assert all(i % 2 == 0 and j % 2 == 0 for (i, j, _), _ in raw_poly.terms())
    Q = sp.Poly(
        sp.expand(numerator.subs({x: sp.sqrt(X), y: sp.sqrt(Y)})),
        X,
        Y,
        kappa,
        domain=sp.QQ,
    ).as_expr()

    # Map 0<=X<=1/3, 1/3<=Y<=1, 0<=kappa<=1 to the unit cube.
    a, b, c = sp.symbols("a b c")
    cube = sp.Poly(
        sp.cancel(Q.subs({X: (1 - a) / 3, Y: (1 + 2 * b) / 3, kappa: c})),
        a,
        b,
        c,
        domain=sp.QQ,
    )
    degrees, coefficients = bernstein_coefficients(cube)
    negative = [(index, str(value)) for index, value in coefficients if value.is_negative]
    zero = [index for index, value in coefficients if value == 0]
    positive = [(index, value) for index, value in coefficients if value.is_positive]
    assert not negative
    assert positive

    # Independent formula audit at a rational interior point.  Since every
    # tensor Bernstein basis function is strictly positive there and at
    # least one coefficient is positive, this also certifies strict
    # positivity throughout the open cube, not merely nonnegativity.
    point = (sp.Rational(2, 5), sp.Rational(3, 7), sp.Rational(4, 9))
    reconstructed = sp.Integer(0)
    for (i0, i1, i2), value in coefficients:
        basis = (
            sp.binomial(degrees[0], i0)
            * point[0] ** i0
            * (1 - point[0]) ** (degrees[0] - i0)
            * sp.binomial(degrees[1], i1)
            * point[1] ** i1
            * (1 - point[1]) ** (degrees[1] - i1)
            * sp.binomial(degrees[2], i2)
            * point[2] ** i2
            * (1 - point[2]) ** (degrees[2] - i2)
        )
        reconstructed += value * basis
    direct = cube.as_expr().subs(dict(zip((a, b, c), point)))
    assert sp.factor(reconstructed - direct) == 0
    assert reconstructed > 0

    coeff_text = "\n".join(
        f"{index}:{value}" for index, value in coefficients
    )
    report = {
        "status_label": "EXACT_BERNSTEIN_CERTIFICATE",
        "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "residual_sha256": hashlib.sha256(str(sp.expand(P)).encode("utf-8")).hexdigest(),
        "kappa_definition": "r*x*(3*Y-1)/(y*(1-3*X))",
        "box": "0<=X<=1/3, 1/3<=Y<=1, 0<=kappa<=1",
        "cube_map": "X=(1-a)/3, Y=(1+2*b)/3, kappa=c",
        "degrees_a_b_c": list(degrees),
        "coefficient_count": len(coefficients),
        "negative_count": len(negative),
        "zero_count": len(zero),
        "positive_count": len(positive),
        "smallest_positive": str(min(value for _, value in positive)),
        "coefficient_sha256": hashlib.sha256(coeff_text.encode("utf-8")).hexdigest(),
        "strictness": (
            "All tensor Bernstein basis functions are positive for 0<a,b,c<1; "
            "all coefficients are nonnegative and at least one is positive."
        ),
        "rational_reconstruction_point": [str(value) for value in point],
        "rational_reconstruction_value": str(sp.factor(reconstructed)),
        "sympy_version": sp.__version__,
    }
    output = HERE / "independent_bernstein_audit.json"
    output.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
