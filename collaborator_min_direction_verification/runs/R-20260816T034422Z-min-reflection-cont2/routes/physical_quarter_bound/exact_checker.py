"""Exact algebra audit for the physical t=0 quarter-bound route."""

from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path

import sympy as sp


def zero(expr):
    assert sp.factor(sp.cancel(expr)) == 0


# Original fixed-negative-phase t=0 ratios.
k, b, sigma = sp.symbols("k b sigma", positive=True)
A = (b**2 - 1) * (1 - k**2 * b**2)
D = b * (1 + k**2 * b) + k**2 * (1 + b) * sigma**2
E = b**2 + b + sigma**2 + k**2 * b * sigma**2
w0 = (1 + k**2 * b) / (1 + b)
w1 = k**2 * E / D
R2 = sigma**2 * A * w0**2 / (2 * D**2)
R3 = 3 * sigma**2 * A * w0 * w1 / (2 * D**2)
R4 = 3 * sigma**2 * A * w1**2 / D**2

# k=0 physical endpoint: theta=pi-atan(x), b=theta/x, sigma=theta.
x, theta = sp.symbols("x theta", positive=True)
zero(sp.limit(R2.subs({b: theta / x, sigma: theta}), k, 0) - x**2 * (theta - x) / (2 * (theta + x)))
zero(sp.limit(R3.subs({b: theta / x, sigma: theta}), k, 0))
zero(sp.limit(R4.subs({b: theta / x, sigma: theta}), k, 0))

# Pure analytic quarter proof constants.
R = x * (1 + 2 * x**2) / (2 * x**2 - 1)
hprime = 1 / (1 + x**2) + sp.diff(R, x)
zero(hprime - x**2 * (4 * x**4 - 13) / ((1 + x**2) * (2 * x**2 - 1) ** 2))
alpha = (sp.Rational(13, 4)) ** sp.Rational(1, 4)
assert alpha > sp.Rational(4, 3)
assert alpha < sp.Rational(27, 20)
Rprime_num = sp.factor(sp.together(sp.diff(R, x)).as_numer_denom()[0])
assert Rprime_num.subs(x, sp.Rational(27, 20)) == -sp.Rational(91759, 40000)
R27 = sp.factor(R.subs(x, sp.Rational(27, 20)))
assert R27 == sp.Rational(25083, 10580)
assert R27 - sp.Rational(33, 14) == sp.Rational(1011, 74060)

# Dalzell's positive integral proves pi<22/7 without an imported estimate.
u = sp.symbols("u", nonnegative=True)
integral = sp.integrate(u**4 * (1 - u) ** 4 / (1 + u**2), (u, 0, 1))
zero(integral - (sp.Rational(22, 7) - sp.pi))

# High-k B,T chart, with B=k*b and T=1/(k*sigma).
B, T = sp.symbols("B T", positive=True)
Q = (B**2 - k**2) * (1 - B**2)
Dt = B * (1 + k * B) * T**2 + k + B
Ft = (B**2 + k * B) * T**2 + 1 + k * B
H2 = T**2 * Q * (1 + k * B) ** 2 / (2 * (k + B) ** 2 * Dt**2)
H3 = 3 * T**2 * Q * (1 + k * B) * Ft / (2 * (k + B) * Dt**3)
H4 = 3 * T**2 * Q * Ft**2 / Dt**4
subs_high = {b: B / k, sigma: 1 / (k * T)}
zero(R2.subs(subs_high) - H2)
zero(R3.subs(subs_high) - H3)
zero(R4.subs(subs_high) - H4)

# Projective low corner.  k=r*p and x=r*X; s is physical sigma.
r, p, X, s = sp.symbols("r p X s", positive=True)
M = X + r * p**2 * s * (1 + r * s * X + r**2 * X**2)
N = s + r * X + r**2 * s * X**2 + r**3 * p**2 * s**2 * X
Qbar = X**2 - p**2 * s**2
C2 = r**2 * (s - r * X) * Qbar * (X + r * p**2 * s) ** 2 / (2 * (s + r * X) * M**2)
C3 = 3 * r**2 * p**2 * (s - r * X) * Qbar * (X + r * p**2 * s) * N / (2 * M**3)
C4 = 3 * r**2 * p**4 * (s - r * X) * (s + r * X) * Qbar * N**2 / M**4
subs_corner = {k: r * p, b: s / (r * X), sigma: s}
zero(R2.subs(subs_corner) - C2)
zero(R3.subs(subs_corner) - C3)
zero(R4.subs(subs_corner) - C4)

this_file = Path(__file__).resolve()
print(
    json.dumps(
        {
            "status": "PASS",
            "checks": [
                "k=0 common-angle limiting ratios",
                "single-minimum derivative factorization",
                "rational bounds at alpha=(13/4)^(1/4)",
                "positive-integral proof of pi<22/7",
                "high B,T chart identity",
                "projective low-corner chart identity",
            ],
            "python": platform.python_version(),
            "sympy": sp.__version__,
            "script_sha256": hashlib.sha256(this_file.read_bytes()).hexdigest(),
        },
        indent=2,
        sort_keys=True,
    )
)
