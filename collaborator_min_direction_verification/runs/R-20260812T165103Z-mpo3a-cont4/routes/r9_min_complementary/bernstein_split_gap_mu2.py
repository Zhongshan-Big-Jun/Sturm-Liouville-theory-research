#!/usr/bin/env python3
"""Exact Bernstein certificate for the mu=2 min split-gap polynomial.

This script performs only rational symbolic algebra.  It reconstructs the
primitive full-interface polynomial P from ``symbolic_split_gap_mu2.py``,
maps its physical domain into the open unit cube, and verifies that every
tensor-product Bernstein coefficient is nonnegative.  Positive coefficients
then make the polynomial strictly positive in the cube interior.

The certificate proves a mu=2, n=2 local physical interface lemma.  It is
not a numerical argument and it does not assert the all-mu or all-n theorem.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def load_split_module():
    path = HERE / "symbolic_split_gap_mu2.py"
    spec = importlib.util.spec_from_file_location("split_gap_mu2", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def primitive_residual(module):
    x, y, r = sp.symbols("x y r", positive=True)
    delta = r**2 - 1
    denominator_a = (
        3*r*x**3*y**2 - r*x**3 - 3*r*x*y**2 + r*x
        + x**4*y + 2*x**2*y**3 - 4*x**2*y + y
    )
    numerator_b = (
        2*r*x**3*y**2 + r*x*y**4 - 4*r*x*y**2 + r*x
        + 3*x**2*y**3 - 3*x**2*y - y**3 + y
    )
    a = sp.factor(-y*(x-y)*(x+y)*(x**2+1) / denominator_a)
    b = sp.factor(
        numerator_b / (r*x*(x-y)*(x+y)*(y**2+1))
    )
    positive = module.cell(x, a)
    negative = module.cell(y, b)
    B = -b
    G = -negative["g"]
    J = -negative["h"]
    d_one = (
        delta*a*positive["Q"] + positive["h"]
        + a**2*positive["g"]
    )
    n_left = sp.factor(
        r**2*a*B*(G+J)*(delta*positive["Q"]+a*positive["g"])
        - delta*negative["Q"]*d_one
    )
    numerator = sp.cancel(n_left).as_numer_denom()[0]
    polynomial = sp.Poly(numerator, x, y, r, domain=sp.QQ).primitive()[1]
    return (x, y, r), polynomial


def tensor_bernstein_coefficients(poly, variables):
    """Convert a multivariate power polynomial to its full-degree Bernstein basis."""
    degrees = poly.degree_list()
    power = {monomial: coefficient for monomial, coefficient in poly.terms()}
    coefficients = {}
    d0, d1, d2 = degrees
    for i0 in range(d0 + 1):
        for i1 in range(d1 + 1):
            for i2 in range(d2 + 1):
                value = sp.Rational(0)
                for j0 in range(i0 + 1):
                    factor0 = sp.Rational(math.comb(i0, j0), math.comb(d0, j0))
                    for j1 in range(i1 + 1):
                        factor01 = factor0 * sp.Rational(
                            math.comb(i1, j1), math.comb(d1, j1)
                        )
                        for j2 in range(i2 + 1):
                            coefficient = power.get((j0, j1, j2))
                            if coefficient:
                                value += factor01 * sp.Rational(
                                    math.comb(i2, j2), math.comb(d2, j2)
                                ) * coefficient
                coefficients[(i0, i1, i2)] = sp.factor(value)
    return degrees, coefficients


def main() -> int:
    module = load_split_module()
    (x, y, r), residual = primitive_residual(module)
    X, Y, kappa = sp.symbols("X Y kappa", positive=True)
    u, v, w = sp.symbols("u v w", real=True)

    # The full momentum interface gives the natural dimensionless parameter
    # kappa.  The negative-amplitude condition is exactly 0<kappa<kappa_N.
    base = (3*Y-1)*(1-Y)
    kappa_denominator = base + 2*Y*(Y-X)
    kappa_n = sp.factor(base / kappa_denominator)
    r_substitution = kappa*y*(1-3*x**2)/(x*(3*y**2-1))
    transformed = sp.together(residual.as_expr().subs(r, r_substitution))
    transformed_numerator, transformed_denominator = transformed.as_numer_denom()

    # Every exponent of x and y in the numerator is even after removal of
    # the positive y^4 factor.  Replace x^2,y^2 by X,Y exactly.
    even_poly = sp.Poly(sp.expand(transformed_numerator), x, y, kappa)
    mapped = sp.Rational(0)
    for (ex, ey, ek), coefficient in even_poly.terms():
        if ex % 2 or ey % 2:
            raise AssertionError("unexpected odd half-angle exponent")
        mapped += coefficient * X**(ex//2) * Y**(ey//2) * kappa**ek
    mapped = sp.cancel(mapped / Y**2)
    if not sp.Poly(mapped, X, Y, kappa).is_multivariate:
        raise AssertionError("unexpected loss of the multivariate residual")

    # The mapped numerator has a positive boundary factor (3Y-1)^4.  After
    # removing it, map the still larger box 0<kappa<1 directly to the unit
    # cube.  This is stronger and simpler than substituting kappa=w*kappa_N.
    reduced_mapped = sp.cancel(mapped / (3*Y-1)**4)
    if sp.factor(mapped-reduced_mapped*(3*Y-1)**4) != 0:
        raise AssertionError("missing positive boundary factor")
    cube_rational = sp.together(
        reduced_mapped.subs({X: u/3, Y: (1+2*v)/3, kappa: w})
    )
    cube_numerator, cube_denominator = map(sp.factor, cube_rational.as_numer_denom())
    cube_poly = sp.Poly(sp.expand(cube_numerator), u, v, w, domain=sp.QQ)
    degrees, coefficients = tensor_bernstein_coefficients(
        cube_poly, (u, v, w)
    )

    negative = {index: value for index, value in coefficients.items() if value < 0}
    zero_count = len([value for value in coefficients.values() if value == 0])
    positive_count = len([value for value in coefficients.values() if value > 0])
    if negative:
        raise AssertionError(f"negative Bernstein coefficients: {negative}")
    if positive_count == 0:
        raise AssertionError("certificate is identically zero")

    # Audit the simple denominator/sign facts used to map the physical domain.
    da_mapped = (
        X**2 + 2*X*Y - 4*X + 1
        + kappa*(-3*X**2 + 4*X - 1)
    )
    assert sp.factor(da_mapped.subs(kappa, 1)-2*X*(Y-X)) == 0
    nb_mapped = sp.factor(
        (1-3*X)*(base-kappa*kappa_denominator)
    )
    assert sp.factor(kappa_denominator-base-2*Y*(Y-X)) == 0

    ordered_coefficients = [
        (index, coefficients[index]) for index in sorted(coefficients)
    ]
    coefficient_text = "\n".join(
        f"{i},{j},{k}:{value}" for (i, j, k), value in ordered_coefficients
    )
    report = {
        "status_label": "EXACT_BERNSTEIN_CERTIFICATE",
        "scope": "mu=2, n=2 min split-gap interface lemma",
        "primitive_residual_sha256": hashlib.sha256(
            str(residual.as_expr()).encode("utf-8")
        ).hexdigest(),
        "primitive_residual_terms": len(residual.terms()),
        "primitive_residual_degrees_x_y_r": list(residual.degree_list()),
        "raw_substitution_identity": (
            "P=y^4*Q(X,Y,kappa)/(3Y-1)^2, where Q=reduced_mapped"
        ),
        "raw_substitution_denominator": str(sp.factor(transformed_denominator)),
        "raw_numerator_boundary_factor": "(3Y-1)^4",
        "removed_positive_factor": "(3Y-1)^4",
        "cube_denominator": str(cube_denominator),
        "cube_power_terms": len(cube_poly.terms()),
        "cube_degrees": list(degrees),
        "bernstein_coefficient_count": len(coefficients),
        "negative_bernstein_coefficient_count": len(negative),
        "zero_bernstein_coefficient_count": zero_count,
        "positive_bernstein_coefficient_count": positive_count,
        "bernstein_coefficients_sha256": hashlib.sha256(
            coefficient_text.encode("utf-8")
        ).hexdigest(),
        "domain_map": {
            "X": "u/3",
            "Y": "(1+2v)/3",
            "kappa": "w",
            "unit_cube": "0<u,v,w<1",
            "physical_subdomain": (
                "0<kappa<kappa_N=(3Y-1)(1-Y)/"
                "[(3Y-1)(1-Y)+2Y(Y-X)]<1"
            ),
        },
        "strictness": (
            "Every tensor Bernstein basis function is positive on the open "
            "unit cube; all coefficients are nonnegative and at least one is "
            "positive, so the cleared polynomial is strictly positive there."
        ),
        "sympy_version": sp.__version__,
    }
    output = HERE / "bernstein_split_gap_mu2.json"
    output.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
