"""Exact retained-empty certificates used by MIN-REFL-C2-I."""
from __future__ import annotations

from fractions import Fraction as F
import json
import sympy as sp


def main() -> dict:
    p, s, X, T = sp.symbols("p s X T", positive=True)
    rb = (T**2 - s**2) / (X*T*(1+s**2) + p*s*(1+T**2))
    # Exact positive difference proving rB < 1/(p*s).
    diff = sp.factor(1/(p*s) - rb)
    assert sp.simplify(diff - (
        X*T*(1+s**2) + p*s*(1+s**2)
    ) / (p*s*(X*T*(1+s**2) + p*s*(1+T**2)))) == 0

    k, y = sp.symbols("k y", real=True)
    Bbar = (1-k) * (1-y*k/(1+k))
    dk = sp.factor(sp.diff(Bbar, k))
    dy = sp.factor(sp.diff(Bbar, y))
    # On 0<k<1, 0<=y<=1 both derivatives are negative.
    assert sp.simplify(dk + ((1-y)*(k+1)**2 + 2*y)/(k+1)**2) == 0
    assert sp.simplify(dy - k*(k-1)/(k+1)) == 0

    boxes = {
        # name: lower endpoints (k,t,y)
        "HIH": (F(63,64), F(1,64), F(63,64)),
        "HHL": (F(63,64), F(63,64), F(0,1)),
        "HHI": (F(63,64), F(63,64), F(1,64)),
        "HHH": (F(63,64), F(63,64), F(63,64)),
    }
    margins = {}
    for name, (k0,t0,y0) in boxes.items():
        # A=k*z=(pi/2)kt and B=pi/2-k*theta
        #       =(pi/2)(1-k)(1-yk/(1+k)).
        # tan(A)cot(B)>1 iff A>B.
        margin = k0*t0 - (1-k0)*(1-y0*k0/(1+k0))
        assert margin > 0
        margins[name] = f"{margin.numerator}/{margin.denominator}"

    return {
        "status": "FINITE_COMPUTATIONAL_RESULT",
        "result": "PASS",
        "criterion": "k*t > (1-k)*(1-y*k/(1+k)) implies p*s>1 and rB<1",
        "monotonicity": {
            "Abar=k*t": "increasing in k,t",
            "Bbar": "decreasing in k,y",
        },
        "exact_lower_margins": margins,
        "retained_empty_boxes": sorted(margins),
        "floating_sign_tests": 0,
    }


if __name__ == "__main__":
    print(json.dumps(main(), indent=2))
