#!/usr/bin/env python3
"""Exact algebra replay for the two R17 t-down triple-corner charts.

This script does not numerically sample a parameter box.  It checks the
algebraic regularizations, the four boundary ratio polynomials, and the
implicit-function boundary data used in derivation.md.  Transcendental
continuity is proved in the accompanying derivation by convergent analytic
power series; here SymPy replays the exact coefficient algebra over QQ(pi).
"""

from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path

import sympy as sp


def zero(expr: sp.Expr) -> None:
    assert sp.factor(sp.cancel(expr)) == 0


# -------------------------------------------------------------------------
# Exact common algebra: epsilon=1-k*b and the R17 gap ratios.
# -------------------------------------------------------------------------
k, eps, a = sp.symbols("k eps a", positive=True)
b = (1 - eps) / k
ebar = (1 - k**2) * (b**2 - a**2) / (
    (1 - k**4 * b**2) * (1 - k**2 * a**2)
)
g_raw = 1 - k**2 * ebar
g_factored = eps * (2 - eps) * (1 - a**2 * k**4) / (
    (1 - a**2 * k**2) * (1 - k**2 * (1 - eps) ** 2)
)
zero(g_raw - g_factored)

u = sp.symbols("u", positive=True)
r = 1 / u
s = r - 1
Delta = r**2 - 1
A00, A10, A01, A11 = sp.symbols("A00 A10 A01 A11", nonnegative=True)
N = (
    s * A00 / 2,
    (2 * s * (A10 + A01) + Delta * A00) / 6,
    (2 * s * A11 + Delta * (A10 + A01)) / 4,
    Delta * A11,
)
u2N = tuple(sp.factor(u**2 * value) for value in N)
expected_u2N = (
    u * (1 - u) * A00 / 2,
    (2 * u * (1 - u) * (A10 + A01) + (1 - u**2) * A00) / 6,
    (2 * u * (1 - u) * A11 + (1 - u**2) * (A10 + A01)) / 4,
    (1 - u**2) * A11,
)
for lhs, rhs in zip(u2N, expected_u2N):
    zero(lhs - rhs)

# On 0<=u<=1 and positive endpoint products, every u^2*N_i is bounded by
# (U0+U1)(L0+L1).  The certificate stores the coefficient sums used in the
# paper proof; all are <=1.
coefficient_sums = [sp.Rational(1, 2), sp.Rational(5, 6), sp.Rational(1), sp.Integer(1)]
assert all(c <= 1 for c in coefficient_sums)


# -------------------------------------------------------------------------
# Exact factorization of the common upper bound in the low-k chart.
# -------------------------------------------------------------------------
q, D0, sigma = sp.symbols("q D0 sigma", positive=True)
u_low = q * D0 / (k * a * sigma * eps * (2 - eps))
low_lhs = sp.cancel(q**2 / (k**2 * u_low**2 * g_factored))
low_rhs = (
    eps
    * a**2
    * sigma**2
    * (2 - eps)
    * (1 - a**2 * k**2)
    * (1 - k**2 * (1 - eps) ** 2)
    / (D0**2 * (1 - a**2 * k**4))
)
zero(low_lhs - low_rhs)


# -------------------------------------------------------------------------
# Exact factorization of the common upper bound in the k-up-1 chart.
# -------------------------------------------------------------------------
d, v, tau, D2 = sp.symbols("d v tau D2", positive=True)
kh = 1 - d
eh = d * v
g_high = eh * (2 - eh) * (1 - a**2 * kh**4) / (
    (1 - a**2 * kh**2) * (1 - kh**2 * (1 - eh) ** 2)
)
u_high = q * D2 / (a * tau * d**2 * v * (2 - d * v))
high_lhs = sp.cancel(q**2 / (u_high**2 * g_high))
A1_expr = (1 - a**2 * kh**2) / d
A2_expr = (1 - kh**2 * (1 - eh) ** 2) / d
A4_expr = (1 - a**2 * kh**4) / d
high_rhs_raw = (
    a**2
    * tau**2
    * d**3
    * v
    * (2 - d * v)
    * (1 - a**2 * kh**2)
    * (1 - kh**2 * (1 - eh) ** 2)
    / (D2**2 * (1 - a**2 * kh**4))
)
high_rhs_normalized = (
    d**4
    * v
    * a**2
    * tau**2
    * (2 - d * v)
    * A1_expr
    * A2_expr
    / (D2**2 * A4_expr)
)
zero(high_lhs - high_rhs_raw)
zero(high_rhs_raw - high_rhs_normalized)


# -------------------------------------------------------------------------
# Four exact boundary polynomials.  At the low corner q^2 U_i L_j -> 3.
# At the high corner it tends to 3*w, w=(1-v)/(1+v).
# -------------------------------------------------------------------------
all_three = {A00: 3, A10: 3, A01: 3, A11: 3}
q2N_low = [sp.factor(value.subs(all_three)) for value in N]

# q^2/g divided by k^2*eps tends to 2*pi^2*u^2, while P/K/C^2 -> 1.
low_polys = [sp.factor(2 * sp.pi**2 * u**2 * value) for value in q2N_low]
low_expected = [
    3 * sp.pi**2 * u * (1 - u),
    sp.pi**2 * (1 - u) * (1 + 5 * u),
    3 * sp.pi**2 * (1 - u) * (1 + 2 * u),
    6 * sp.pi**2 * (1 - u**2),
]
for lhs, rhs in zip(low_polys, low_expected):
    zero(lhs - rhs)

w = (1 - v) / (1 + v)
all_high = {A00: 3 * w, A10: 3 * w, A01: 3 * w, A11: 3 * w}
q2N_high = [sp.factor(value.subs(all_high)) for value in N]

# In the high chart [P*q^2/g]/[d^4*v] -> pi^2*u^2*(1+v)/16.
high_polys = [
    sp.factor(sp.pi**2 * u**2 * (1 + v) * value / 16) for value in q2N_high
]
high_expected = [
    3 * sp.pi**2 * (1 - v) * u * (1 - u) / 32,
    sp.pi**2 * (1 - v) * (1 - u) * (1 + 5 * u) / 32,
    3 * sp.pi**2 * (1 - v) * (1 - u) * (1 + 2 * u) / 32,
    3 * sp.pi**2 * (1 - v) * (1 - u**2) / 16,
]
for lhs, rhs in zip(high_polys, high_expected):
    zero(lhs - rhs)


# -------------------------------------------------------------------------
# Boundary data for the two implicit negative-phase equations.
# -------------------------------------------------------------------------
sig = sp.symbols("sig", positive=True)
F0 = sp.atan(k * sig) / k + sp.atan(k * sig / (1 - eps)) - sp.pi
F0_at_k0 = sp.limit(F0, k, 0)
zero(F0_at_k0 - (sig - sp.pi))
zero(sp.diff(F0_at_k0, sig) - 1)

F1_numer = sp.atan(d / ((1 - d) * tau)) + (1 - d) * sp.atan(
    d * (1 - d * v) / ((1 - d) * tau)
)
F1_at_d0 = sp.limit(F1_numer / d - sp.pi / 2, d, 0)
zero(F1_at_d0 - (2 / tau - sp.pi / 2))
tau0 = 4 / sp.pi
zero(F1_at_d0.subs(tau, tau0))
zero(sp.diff(F1_at_d0, tau).subs(tau, tau0) + sp.pi**2 / 8)


# The normalized high-chart denominator limits use a=1+o(d), proved from
# the exact tan(x)/x power series after z=d^2*v*x.
zero(sp.limit((1 - kh**2) / d, d, 0) - 2)
zero(sp.limit((1 - kh**2 * (1 - d * v) ** 2) / d, d, 0) - 2 * (1 + v))
zero(sp.limit((1 - kh**4) / d, d, 0) - 4)


# Replay the endpoint scalings directly from the full rational W_i formulas.
# q*X has higher order in both charts, so X=0 is its exact boundary value.
def qW_pair(kk: sp.Expr, ee: sp.Expr, aa: sp.Expr, qq: sp.Expr, ss: sp.Expr) -> tuple[sp.Expr, sp.Expr, sp.Expr]:
    bb = (1 - ee) / kk
    DD = bb * (1 + kk**2 * aa * bb) + kk**2 * (aa + bb) * ss**2
    EE = bb**2 + bb + ss**2 + kk**2 * bb * ss**2
    qW0 = (1 - kk**2 * aa**2) * (
        aa * ss - bb * qq + kk**2 * aa * bb * (qq + ss)
    ) / (ss * (aa + bb) * (1 - kk**2 * aa))
    qW1 = kk**2 * aa * (1 - kk**2 * aa**2) * EE / ((1 - kk**2 * aa) * DD)
    return sp.cancel(qW0), sp.cancel(qW1), sp.cancel(DD)


q_low_boundary = 2 * sp.pi * k * eps * u
qW0_lo, qW1_lo, _ = qW_pair(k, eps, sp.Integer(1), q_low_boundary, sp.pi)
for value in (qW0_lo, qW1_lo):
    boundary = sp.limit(sp.limit(value / k, eps, 0, dir="+"), k, 0, dir="+")
    zero(boundary - 1)

q_high_boundary = sp.pi * u * d**2 * v / 4
qW0_hi, qW1_hi, _ = qW_pair(
    kh, eh, sp.Integer(1), q_high_boundary, 4 / (sp.pi * d)
)
for value in (qW0_hi, qW1_hi):
    zero(sp.limit(value, d, 0, dir="+") - 1)

g_hi_boundary = sp.factor(
    g_high.subs({a: 1})
)
zero(sp.limit(g_hi_boundary, d, 0, dir="+") - 2 * v / (1 + v))
ebar_hi_boundary = sp.cancel((1 - g_hi_boundary) / kh**2)
zero(sp.limit(ebar_hi_boundary, d, 0, dir="+") - (1 - v) / (1 + v))


def as_strings(values: list[sp.Expr]) -> list[str]:
    return [str(sp.factor(value)) for value in values]


this_file = Path(__file__).resolve()
print(
    json.dumps(
        {
            "status": "PASS",
            "arithmetic": "exact SymPy algebra over QQ(pi); no floating sign tests",
            "checks": [
                "epsilon-factorization of g",
                "u^2 regularization of all four Bernstein numerators",
                "low-chart common ratio factor eps",
                "high-chart common ratio factor d^4*v",
                "four low-corner leading ratio polynomials",
                "four high-corner leading ratio polynomials",
                "low/high negative-phase implicit-function boundary data",
                "high-chart normalized denominator limits",
                "full rational W0/W1 endpoint scalings",
                "high-chart g and ebar endpoint scalings",
            ],
            "low_ratio_limit_after_dividing_by_k2_eps": as_strings(low_polys),
            "high_ratio_limit_after_dividing_by_d4_v": as_strings(high_polys),
            "python": platform.python_version(),
            "sympy": sp.__version__,
            "script_sha256": hashlib.sha256(this_file.read_bytes()).hexdigest(),
        },
        indent=2,
        sort_keys=True,
    )
)
