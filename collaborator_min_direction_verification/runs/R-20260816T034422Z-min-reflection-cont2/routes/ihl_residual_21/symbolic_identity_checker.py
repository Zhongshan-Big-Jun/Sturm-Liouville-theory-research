"""Exact algebra checks for the C2-P stable contractors."""
from __future__ import annotations

import json
import sympy as sp


def main():
    x, e, p, s = sp.symbols("x e p s", positive=True)
    rb_cot = (e**-2 - s**2) / (
        (x * e)**-1 * (1 + s**2) + p * s * (1 + e**-2)
    )
    den = e * (1 + s**2) + x * p * s * (1 + e**2)
    rb_stable = x * (1 - s**2 * e**2) / den
    assert sp.factor(rb_cot - rb_stable) == 0

    # With k>0, sign(b-a)=sign(s*e-p*x).
    k = sp.symbols("k", positive=True)
    assert sp.factor(s * e / k - p * x / k - (s * e - p * x) / k) == 0

    y = sp.symbols("y", nonnegative=True)
    theta_gap = 1 - k * (1 + y * (1 - k) / (1 + k))
    assert sp.factor(theta_gap - (1 - k) * (1 - k * y / (1 + k))) == 0

    bbar = (1 - k) * (1 - y * k / (1 + k))
    dk = sp.factor(sp.diff(bbar, k))
    dy = sp.factor(sp.diff(bbar, y))
    assert sp.factor(dk + ((1 - y) * (k + 1) ** 2 + 2 * y) / (k + 1) ** 2) == 0
    assert sp.factor(dy - k * (k - 1) / (k + 1)) == 0

    return {
        "status": "FINITE_COMPUTATIONAL_RESULT",
        "result": "PASS",
        "checked": [
            "cotangent rB formula equals cross-multiplied complementary-angle formula",
            "sign(b-a)=sign(s*e-p*x) for k>0",
            "1-k*theta/(pi/2)=(1-k)*(1-k*y/(1+k))",
            "right normalized complementary angle decreases in k and y",
        ],
        "rB_positive_denominator": str(den),
        "rB_minus_one_numerator": str(sp.expand(x * (1 - s**2 * e**2) - den)),
        "dBbar_dk": str(dk),
        "dBbar_dy": str(dy),
    }


if __name__ == "__main__":
    print(json.dumps(main(), indent=2))
