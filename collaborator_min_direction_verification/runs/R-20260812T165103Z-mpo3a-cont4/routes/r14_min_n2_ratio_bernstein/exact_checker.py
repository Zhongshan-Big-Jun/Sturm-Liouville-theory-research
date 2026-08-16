"""Exact algebra checks for R14.

This script verifies polynomial/rational identities only.  Inequality
directions and domain assumptions are audited in derivation.md.
"""

import json
import platform
import sympy as sp


def zero(expr):
    assert sp.factor(sp.cancel(expr)) == 0


checks = []

# Section 2: the local r_A identity, reduced modulo the circle relation.
m, F, c, C = sp.symbols("m F c C")
x = (F * c - m * C) / (F + m)
rho = (m * F + 1) / (F + m)
e = (m**2 - 1) * F * (c + C) / (F + m) ** 2
K = (1 - x**2) / x
target = (
    F
    * (m - 1) ** 2
    * (1 + c * C - F * (1 - c**2))
    / ((F + m) * (F * c - m * C))
)
num = sp.together((rho - 1) * K - e - target).as_numer_denom()[0]
poly = sp.Poly(num, C)
rem = sp.rem(poly, sp.Poly(C**2 - (1 - F**2 + F**2 * c**2), C)).as_expr()
zero(rem)
checks.append("local_rA_identity")

# Section 1: kappa=1-x^2-p, again modulo the circle relation.
p_local = F * (1 - c**2) * (1 + m * F) / (F + m)
kappa_local = m * F * (c + C) ** 2 / (F + m) ** 2
num = sp.together(1 - x**2 - p_local - kappa_local).as_numer_denom()[0]
poly = sp.Poly(num, C)
rem = sp.rem(poly, sp.Poly(C**2 - (1 - F**2 + F**2 * c**2), C)).as_expr()
zero(rem)
checks.append("local_kappa_identity")

# Section 3: exact half-sum reduction of the plus-only lemma.
sa, ca, sb, cb, k = sp.symbols("sa ca sb cb k")
mu = (1 + k) / (1 - k)
Q0 = (mu + 1) * (sa * cb + k * ca * sb)
D0 = (mu + 1) * (sa * cb - k * ca * sb)
S_minus_s = 2 * ca * sb
Sc_minus_musC = (mu + 1) * (sb * cb - k * sa * ca)
c_plus_C = 2 * ca * cb
J0 = sp.expand(Q0 * D0 * S_minus_s - (mu + 1) * Sc_minus_musC * c_plus_C)
core = k * sa * cb - ca * sb * (cb**2 + k**2 * sb**2)
diff = sp.together(J0 - 2 * (mu + 1) ** 2 * ca**2 * core).as_numer_denom()[0]
diff = sp.expand(diff).subs(sa**2, 1 - ca**2).subs(sb**2, 1 - cb**2)
zero(diff)
checks.append("plus_lemma_half_sum_reduction")

# Section 4: G difference and Psi decomposition.
Fp, Fm = sp.symbols("Fp Fm")
G = lambda z: 1 + m**2 + m * (z + 1 / z)
zero(G(Fp) - G(Fm) - m * (Fp - Fm) * (Fp * Fm - 1) / (Fp * Fm))
checks.append("G_difference")

g, q, p, w, u, xx, delta, A0 = sp.symbols("g q p w u xx delta A0")
lambda2 = g * q / p
Psi = lambda2 * w**2 * A0 + delta * u**2 * (
    p * lambda2 * w**2 + q * p - q * w * u
)
Psi_target = lambda2 * w**2 * A0 + delta * q * u**2 * (
    (g - 1) * w**2 + p - xx * w
)
zero((Psi - Psi_target).subs(u, xx + w))
checks.append("Psi_g_decomposition")

# Section 5: phase-ratio identities.
zeta = sp.symbols("zeta", positive=True)
Gz = (zeta + 1) * (zeta + m**2) / zeta
zero(zeta * sp.diff(Gz, zeta) / Gz - (zeta**2 - m**2) / ((zeta + 1) * (zeta + m**2)))
gap = (zeta - 1) / (zeta + 1) - (zeta**2 - m**2) / (
    (zeta + 1) * (zeta + m**2)
)
zero(gap - (m**2 - 1) * zeta / ((zeta + 1) * (zeta + m**2)))
checks.append("phase_ratio_log_derivative_gap")

# Sections 6-7: retained-margin, bridge, and derivative identities.
rho_p, rho_m, ep, eta, lam, d, r, kap = sp.symbols(
    "rho_p rho_m ep eta lam d r kap"
)
M = p * (rho_p - 1) - xx * ep
wdef = (ep - r * eta / lam) / d
refined = (M + p * (1 - rho_m) + xx * r * eta / lam) / d
zero((p - xx * wdef - refined).subs(d, rho_p - rho_m))
checks.append("retained_margin_refinement")

h = xx + (1 - g) * w
uu = xx + w
bridge = w * (2 * h + (1 - g) * uu) - uu * h
zero(bridge - (2 * (1 - g) * w**2 + xx * w - xx**2))
checks.append("quadratic_bridge")

c0, Knew = sp.symbols("c0 Knew")
Dmargin = g * Knew - (r**2 - 1) * p * uu * (2 * h + (1 - g) * uu)
Enew = g * w * Knew - (r**2 - 1) * p * uu**2 * h
# Differentiate along w'=u'=-c0 and h'=-(1-g)c0.
formal_derivative = (
    sp.diff(Enew, r)
    + sp.diff(Enew, w) * (-c0)
)
zero(formal_derivative - (-c0 * Dmargin - 2 * r * p * uu**2 * h))
checks.append("Enew_derivative_identity")

# Section 8: Bernstein product coefficients.
t, s, q0 = sp.symbols("t s q0")
u0, u1, ell0, ell1, DeltaB = sp.symbols("u0 u1 ell0 ell1 DeltaB")
ut = u0 + (u1 - u0) * t
ellt = ell0 + (ell1 - ell0) * t
deltat = 2 * s * t + s**2 * t**2
prod = sp.Poly(sp.expand(deltat * ut * ellt), t)


def bernstein_coeff(poly, degree, i):
    return sp.factor(
        sum(
            poly.coeff_monomial(t**j)
            * sp.binomial(i, j)
            / sp.binomial(degree, j)
            for j in range(i + 1)
        )
    )


bern = [bernstein_coeff(prod, 4, i) for i in range(5)]
expected = [
    0,
    s * u0 * ell0 / 2,
    (2 * s * (u1 * ell0 + u0 * ell1) + DeltaB * u0 * ell0) / 6,
    (2 * s * u1 * ell1 + DeltaB * (u1 * ell0 + u0 * ell1)) / 4,
    DeltaB * u1 * ell1,
]
for got, want in zip(bern, expected):
    zero((got - want).subs(DeltaB, s * (s + 2)))
checks.append("quartic_Bernstein_coefficients")

print(
    json.dumps(
        {
            "status": "PASS",
            "checks": checks,
            "python": platform.python_version(),
            "sympy": sp.__version__,
            "note": "Identity checker only; four coefficient signs remain open.",
        },
        sort_keys=True,
    )
)
