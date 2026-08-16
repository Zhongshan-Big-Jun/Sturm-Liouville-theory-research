"""Exact rational Bernstein audit for t->0 normalized gap numerators.

The first trial maps the algebraic superdomain
  0 <= k <= 1/8,
  1 <= b <= 1/k,
  0 <= sigma <= 4/(1-k)
to the unit cube.  No floating-point value is used in a sign decision.
"""

from __future__ import annotations

import json
import math
import platform

import sympy as sp


k, b, sigma = sp.symbols("k b sigma", positive=True)
h, x, z = sp.symbols("h x z", nonnegative=True)
k2 = k**2
A = (b**2 - 1) * (1 - k2 * b**2)
D = b * (1 + k2 * b) + k2 * (1 + b) * sigma**2
E = b**2 + b + sigma**2 + k2 * b * sigma**2

# Numerators of 1-Z0^2/2, 1-3Z0Z1/2, 1-3Z1^2.
polys = {
    "P2": 2 * (1 + b) ** 2 * D**2 - sigma**2 * A * (1 + k2 * b) ** 2,
    "P3": 2 * (1 + b) * D**3 - 3 * sigma**2 * A * k2 * E * (1 + k2 * b),
    "P4": D**4 - 3 * sigma**2 * A * k2**2 * E**2,
}


def bernstein_coefficients(poly: sp.Poly) -> list[sp.Rational]:
    degrees = poly.degree_list()
    coeff = poly.as_dict()
    out: list[sp.Rational] = []
    for I in range(degrees[0] + 1):
        for J in range(degrees[1] + 1):
            for L in range(degrees[2] + 1):
                value = sp.Rational(0)
                for i in range(I + 1):
                    for j in range(J + 1):
                        for ell in range(L + 1):
                            a = coeff.get((i, j, ell))
                            if a is None:
                                continue
                            value += (
                                a
                                * sp.Rational(math.comb(I, i), math.comb(degrees[0], i))
                                * sp.Rational(math.comb(J, j), math.comb(degrees[1], j))
                                * sp.Rational(math.comb(L, ell), math.comb(degrees[2], ell))
                            )
                out.append(sp.factor(value))
    return out


result = {}
subs = {
    k: h / 8,
    b: (k + (1 - k) * x) / k,
    sigma: 4 * z / (1 - k),
}
for name, original in polys.items():
    mapped = sp.cancel(original.subs(subs, simultaneous=True).subs(k, h / 8))
    num, den = sp.together(mapped).as_numer_denom()
    poly = sp.Poly(sp.expand(num), h, x, z, domain=sp.QQ)
    bern = bernstein_coefficients(poly)
    neg = [q for q in bern if q < 0]
    zero = [q for q in bern if q == 0]
    pos = [q for q in bern if q > 0]
    result[name] = {
        "degree": poly.degree_list(),
        "power_terms": len(poly.terms()),
        "bernstein_count": len(bern),
        "negative_count": len(neg),
        "zero_count": len(zero),
        "positive_count": len(pos),
        "min_positive": str(min(pos)) if pos else None,
        "first_negative": [str(q) for q in neg[:10]],
        "denominator": str(sp.factor(den)),
        "numerator_factor": "omitted_large",
    }

# Also test the same common-angle envelope on the full 0<=k<=1 range.
# This is deliberately limited to P3 and P4, whose coefficient signs are
# the non-elementary part of the boundary argument.
full_result = {}
full_subs = {
    k: h,
    b: (k + (1 - k) * x) / k,
    sigma: 4 * z / (1 - k),
}
for name in ("P2", "P3", "P4"):
    mapped = sp.cancel(polys[name].subs(full_subs, simultaneous=True).subs(k, h))
    num, den = sp.together(mapped).as_numer_denom()
    poly = sp.Poly(sp.expand(num), h, x, z, domain=sp.QQ)
    bern = bernstein_coefficients(poly)
    neg = [q for q in bern if q < 0]
    zero = [q for q in bern if q == 0]
    pos = [q for q in bern if q > 0]
    full_result[name] = {
        "degree": poly.degree_list(),
        "bernstein_count": len(bern),
        "negative_count": len(neg),
        "zero_count": len(zero),
        "positive_count": len(pos),
        "min_positive": str(min(pos)) if pos else None,
        "first_negative": [str(q) for q in neg[:10]],
        "denominator": str(sp.factor(den)),
    }

high_result = {}
high_k = (1 + 7 * h) / 8
high_subs = {
    k: high_k,
    b: (k + (1 - k) * x) / k,
    sigma: 4 * z / (1 - k),
}
for name in ("P2", "P3", "P4"):
    mapped = sp.cancel(polys[name].subs(high_subs, simultaneous=True).subs(k, high_k))
    num, den = sp.together(mapped).as_numer_denom()
    poly = sp.Poly(sp.expand(num), h, x, z, domain=sp.QQ)
    bern = bernstein_coefficients(poly)
    neg = [q for q in bern if q < 0]
    zero = [q for q in bern if q == 0]
    pos = [q for q in bern if q > 0]
    high_result[name] = {
        "degree": poly.degree_list(),
        "bernstein_count": len(bern),
        "negative_count": len(neg),
        "zero_count": len(zero),
        "positive_count": len(pos),
        "min_positive": str(min(pos)) if pos else None,
        "first_negative": [str(q) for q in neg[:10]],
        "denominator": str(sp.factor(den)),
    }

print(
    json.dumps(
        {
            "status": "EXACT_RATIONAL_DISCOVERY",
            "python": platform.python_version(),
            "sympy": sp.__version__,
            "map": {
                "k": "h/8",
                "kb": "k+(1-k)x",
                "sigma": "4z/(1-k)",
                "cube": "0<=h,x,z<=1",
            },
            "results": result,
            "full_k_results": full_result,
            "high_k_results": high_result,
        },
        indent=2,
        sort_keys=True,
    )
)
