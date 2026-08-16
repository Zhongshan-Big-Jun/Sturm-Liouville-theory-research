#!/usr/bin/env python3
"""Exact checker for the C2-J general-mu coefficient bridge.

The complete physical Cramer/Phi bridge is replayed from the frozen C2-H
checker by content hash.  This file independently checks the phase cube,
the analytic g split, the quartic Bernstein reduction, the exact stable
one-cell formulas, and G_i=cp^4 B_i.
"""

from __future__ import annotations

import contextlib
import hashlib
import io
import json
from pathlib import Path
import runpy
import sys

import sympy as sp


def zero(expr: sp.Expr, label: str) -> None:
    got = sp.factor(sp.cancel(expr))
    assert got == 0, (label, got)


checks: list[str] = []

# Hash-bind and dynamically replay the new, self-contained C2-H rederivation
# of both physical momentum matches and the normalized split bridge.
route_dir = Path(__file__).resolve().parent
c2h_dir = route_dir.parent / "general_mu_interface"
c2h_checker = c2h_dir / "exact_checker.py"
c2h_report = c2h_dir / "report.md"
expected_hashes = {
    c2h_checker: "2e0590c02109a1eca57382ecc5b5f5fa4f62da5a34a6fe7b9dc7dd104b256c9c",
    c2h_report: "32a4aea77442b1980e5d76fbc608b0ac73b034004eef816eaa9e790b2fd262b7",
}
for path, want in expected_hashes.items():
    assert hashlib.sha256(path.read_bytes()).hexdigest() == want
capture = io.StringIO()
with contextlib.redirect_stdout(capture):
    runpy.run_path(str(c2h_checker), run_name="__c2h_replay__")
c2h_result = json.loads(capture.getvalue())
assert c2h_result["status"] == "PASS"
assert "full_normalized_split_bridge" in c2h_result["checks"]
assert "left_schur_gap_positive_prefactor" in c2h_result["checks"]
assert "time_reversed_right_schur_gap_positive_prefactor" in c2h_result["checks"]
assert "three_cell_gamma_jump_schur_gluing" in c2h_result["checks"]
checks.append("hash_bound_full_cramer_phi_replay")

# Exact phase-coordinate bijection.
k, t, y = sp.symbols("k t y", positive=True)
mu = (1 + k) / (1 - k)
Aplus = sp.pi * t / 2
alpha = (1 - k) * Aplus
Aminus = sp.pi / 2 + y * sp.pi * (1 - k) / (2 * (1 + k))
beta = (1 - k) * Aminus
zero(alpha - sp.pi * (1 - k) * t / 2, "alpha inverse")
zero(
    beta
    - (
        sp.pi * (1 - k) / 2
        + y * sp.pi * (1 - k) ** 2 / (2 * (1 + k))
    ),
    "beta inverse",
)
zero(sp.pi / (mu + 1) - sp.pi * (1 - k) / 2, "threshold")
zero(
    sp.pi / mu - sp.pi / (mu + 1)
    - sp.pi * (1 - k) ** 2 / (2 * (1 + k)),
    "minus width",
)
checks.append("physical_phase_cube_bijection")

# The exact Phi/Psi split and the g>=1 analytic half.
lam2, w, r, kp, km, pp, pm, u, x, A0 = sp.symbols(
    "lam2 w r kp km pp pm u x A0", positive=True
)
delta = r**2 - 1
Phi = (lam2 * w**2 + r**2 * km + pm) * (
    A0 + delta * pp * u**2
) - delta * pm * w * u**3
Psi = lam2 * w**2 * A0 + delta * u**2 * (
    pp * lam2 * w**2 + pm * pp - pm * w * u
)
zero(
    Phi - Psi - (r**2 * km * A0 + pm * A0 + delta * pp * r**2 * km * u**2),
    "Phi minus Psi positive remainder",
)
g = sp.symbols("g", positive=True)
Psi_g = lam2 * w**2 * A0 + delta * pm * u**2 * (
    (g - 1) * w**2 + pp - x * w
)
zero(
    (Psi - Psi_g).subs({lam2: g * pm / pp, u: x + w}),
    "g decomposition",
)
checks.append("g_ge_one_analytic_half")

# g<1 bridge: A0>Knew, Enew>0 => E>0 => Psi>0, and D>0 => Enew>0.
Knew, h, ell = sp.symbols("Knew h ell", positive=True)
E = g * w * A0 - delta * pp * u**2 * h
Enew = g * w * Knew - delta * pp * u**2 * h
zero(E - Enew - g * w * (A0 - Knew), "E-Enew")
zero(
    (
        Psi_g
        - ((pm * w / pp) * E + delta * pm * pp * u**2)
    ).subs({lam2: g * pm / pp, u: x + w, h: x + (1 - g) * w}),
    "Psi from E",
)
hdef = x + (1 - g) * w
elldef = 2 * hdef + (1 - g) * u
J = w * elldef - u * hdef
zero(
    J.subs(u, x + w) - (2 * (1 - g) * w**2 + x * w - x**2),
    "quadratic J",
)
Dmargin = g * Knew - delta * pp * u * elldef
checks.append("g_lt_one_D_to_Phi_chain")

# Degree-four Bernstein coefficients of D(r).  Here z is the affine
# coordinate on [1,rB], sR=rB-1, and DeltaB=rB^2-1=sR(sR+2).
z, sR = sp.symbols("z sR")
u0, u1, l0, l1 = sp.symbols("u0 u1 l0 l1")
DeltaB = sR * (sR + 2)
uz = u0 + (u1 - u0) * z
lz = l0 + (l1 - l0) * z
deltaz = 2 * sR * z + sR**2 * z**2
poly = sp.Poly(sp.expand(deltaz * uz * lz), z)


def bernstein_coefficient(poly: sp.Poly, degree: int, i: int) -> sp.Expr:
    return sp.factor(
        sum(
            poly.coeff_monomial(z**j)
            * sp.binomial(i, j)
            / sp.binomial(degree, j)
            for j in range(i + 1)
        )
    )


N = [bernstein_coefficient(poly, 4, i) for i in range(5)]
N_expected = [
    0,
    sR * u0 * l0 / 2,
    (2 * sR * (u1 * l0 + u0 * l1) + DeltaB * u0 * l0) / 6,
    (2 * sR * u1 * l1 + DeltaB * (u1 * l0 + u0 * l1)) / 4,
    DeltaB * u1 * l1,
]
for i, (got, want) in enumerate(zip(N, N_expected)):
    zero(got - want, f"Bernstein N{i}")
checks.append("quartic_Bernstein_coefficients")

# Stable scaling.  The C2-I evaluator uses
# cp*x=k*Xbar, cp*w_i=Wbar_i/k, 1-g=k^2*ebar.
cp, Xbar, ebar = sp.symbols("cp Xbar ebar", positive=True)
W0, W1 = sp.symbols("W0 W1", positive=True)
g_stable = 1 - k**2 * ebar


def stable_endpoint(W: sp.Expr) -> tuple[sp.Expr, sp.Expr, sp.Expr]:
    x_phys = k * Xbar / cp
    w_phys = W / (k * cp)
    u_phys = x_phys + w_phys
    h_phys = x_phys + (1 - g_stable) * w_phys
    ell_phys = 2 * h_phys + (1 - g_stable) * u_phys
    Ubar = k**2 * Xbar + W
    Hbar = Xbar + ebar * W
    Lbar = 2 * Hbar + ebar * Ubar
    zero(cp * u_phys - Ubar / k, "stable u")
    zero(cp * h_phys - k * Hbar, "stable h")
    zero(cp * ell_phys - k * Lbar, "stable ell")
    return Ubar, Hbar, Lbar


U0, H0, L0 = stable_endpoint(W0)
U1, H1, L1 = stable_endpoint(W1)
Nhat = [
    0,
    sR * U0 * L0 / 2,
    (2 * sR * (U1 * L0 + U0 * L1) + DeltaB * U0 * L0) / 6,
    (2 * sR * U1 * L1 + DeltaB * (U1 * L0 + U0 * L1)) / 4,
    DeltaB * U1 * L1,
]
u0_phys, u1_phys = U0 / (k * cp), U1 / (k * cp)
l0_phys, l1_phys = k * L0 / cp, k * L1 / cp
Nphys = [
    0,
    sR * u0_phys * l0_phys / 2,
    (
        2 * sR * (u1_phys * l0_phys + u0_phys * l1_phys)
        + DeltaB * u0_phys * l0_phys
    )
    / 6,
    (
        2 * sR * u1_phys * l1_phys
        + DeltaB * (u1_phys * l0_phys + u0_phys * l1_phys)
    )
    / 4,
    DeltaB * u1_phys * l1_phys,
]
for i in range(1, 5):
    zero(Nhat[i] - cp**2 * Nphys[i], f"Nhat scaling {i}")
Pplus = cp**2 * pp
Bcoef = [g * Knew - pp * Nphys[i] for i in range(5)]
Gcoef = [g * Knew * cp**4 - Pplus * Nhat[i] for i in range(5)]
for i in range(5):
    zero(Gcoef[i] - cp**4 * Bcoef[i], f"G=B scaling {i}")
checks.append("stable_G_equals_cp4_B")

# Derive the nontrivial stable one-cell formulas from the exact common-angle
# half-sum tangents.  a,b,qv,sv are positive stable phase variables.
a, b, qv, sv = sp.symbols("a b qv sv", positive=True)
mu_k = (1 + k) / (1 - k)


def cell_from_half_sum(TA: sp.Expr, TB: sp.Expr, cosA_sign: int):
    root = sp.sqrt((1 + TA**2) * (1 + TB**2))
    fac = sp.Integer(cosA_sign) / root
    sn = (TA - TB) * fac
    sm = (TA + TB) * fac
    cc = (1 + TA * TB) * fac
    CC = (1 - TA * TB) * fac
    FF = sm / sn
    UU = 1 / sn + mu_k / sm
    QQ = sn + mu_k * sm
    xx = (FF * cc - mu_k * CC) / (FF + mu_k)
    rho = (mu_k * FF + 1) / (FF + mu_k)
    pcell = QQ / UU
    ecell = (mu_k**2 - 1) * FF * (cc + CC) / (FF + mu_k) ** 2
    kcell = 1 - xx**2 - pcell
    return tuple(map(sp.factor, (UU, xx, rho, pcell, ecell, kcell)))


plus = cell_from_half_sum(qv / a, k * qv, 1)
minus = cell_from_half_sum(-sv / b, k * sv, -1)
Up, xp, rhop, pplus, ep, kappap = plus
Um, xm, rhom, pminus, em, kappam = minus
lam = sp.factor(Up / Um)
d = sp.factor(rhop - rhom)
eta = -em
cp2 = (a**2 + qv**2) * (1 + k**2 * qv**2) / qv**2
Pplus_formula = (1 - k**2 * a**2) * (1 + k**2 * a) / (1 - k**2 * a)
zero(cp2 * pplus - Pplus_formula, "Pplus formula")
ebar_formula = (1 - k**2) * (b**2 - a**2) / (
    (1 - k**4 * b**2) * (1 - k**2 * a**2)
)
zero(lam**2 * pplus / pminus - (1 - k**2 * ebar_formula), "g formula")
Knew_derived = sp.factor(kappap + pplus * (1 - rhom) / d)
Knew_formula = (1 - k**2 * a**2) / (
    (a**2 + qv**2) * (1 + k**2 * qv**2)
) * (
    a**2 * (1 - k**2) / (1 - k**2 * a) ** 2
    + qv**2 * b * (1 + k**2 * a) / (a + b)
)
zero(Knew_derived - Knew_formula, "Knew formula")

# The branch endpoint and the two stable endpoint values are not definitions:
# derive them from the physical Cramer variables above.  Positivity of all
# symbols lets powdenest remove the square roots introduced by cp.
Dtilde_formula = b * (1 + k**2 * a * b) + k**2 * (a + b) * sv**2
rB_derived = sp.factor(lam * ep / (eta + d * xm))
rB_formula = a * sv * (1 - k**2 * b**2) / (qv * Dtilde_formula)
zero(rB_derived - rB_formula, "rB formula")

w0_derived = sp.factor((ep - eta / lam) / d)
w1_derived = sp.factor((ep - rB_derived * eta / lam) / d)
W0_formula = (1 - k**2 * a**2) * (
    a * sv - b * qv + k**2 * a * b * (qv + sv)
) / (qv * sv * (a + b) * (1 - k**2 * a))
W1_formula = k**2 * a * (1 - k**2 * a**2) * (
    b**2 + b + sv**2 + k**2 * b * sv**2
) / (qv * (1 - k**2 * a) * Dtilde_formula)
zero(
    sp.powdenest(k * sp.sqrt(cp2) * w0_derived, force=True) - W0_formula,
    "Wbar0 formula",
)
zero(
    sp.powdenest(k * sp.sqrt(cp2) * w1_derived, force=True) - W1_formula,
    "Wbar1 formula",
)

Xbar_derived = sp.powdenest(sp.sqrt(cp2) * xp / k, force=True)
# Reduce the cancellation-safe sinc formula in bridge_proof.md (6.5) to
# half-sum tangents and compare it with cp*x_+/k.  Here A,B=kA are both in
# (0,pi/2), so both cosine square roots take their positive branch.
TAp = qv / a
TBp = k * qv
cos_Ap = 1 / sp.sqrt(1 + TAp**2)
sin_Ap = TAp * cos_Ap
cos_Bp = 1 / sp.sqrt(1 + TBp**2)
sin_Bp = TBp * cos_Bp
Xbar_sinc_reduced = (
    sin_Bp * cos_Bp / k - sin_Ap * cos_Ap
) / (
    sin_Ap
    * cos_Bp
    * (sin_Ap * cos_Bp - k * sin_Bp * cos_Ap)
)
zero(
    sp.powdenest(Xbar_sinc_reduced - Xbar_derived, force=True),
    "Xbar cancellation-safe sinc formula",
)
for endpoint, w_endpoint, W_formula in (
    (0, w0_derived, W0_formula),
    (1, w1_derived, W1_formula),
):
    u_endpoint = xp + w_endpoint
    h_endpoint = xp + (1 - lam**2 * pplus / pminus) * w_endpoint
    ell_endpoint = 2 * h_endpoint + (
        1 - lam**2 * pplus / pminus
    ) * u_endpoint
    Ubar_formula = k**2 * Xbar_derived + W_formula
    Hbar_formula = Xbar_derived + ebar_formula * W_formula
    Lbar_formula = 2 * Hbar_formula + ebar_formula * Ubar_formula
    zero(
        sp.powdenest(sp.sqrt(cp2) * u_endpoint, force=True)
        - Ubar_formula / k,
        f"physical Ubar{endpoint}",
    )
    zero(
        sp.powdenest(sp.sqrt(cp2) * h_endpoint, force=True)
        - k * Hbar_formula,
        f"physical Hbar{endpoint}",
    )
    zero(
        sp.powdenest(sp.sqrt(cp2) * ell_endpoint, force=True)
        - k * Lbar_formula,
        f"physical Lbar{endpoint}",
    )
checks.append("stable_common_angle_rB_W_U_H_L_P_g_Knew_formulas")

print(
    json.dumps(
        {
            "status": "PASS",
            "route": "MIN-REFL-C2-J",
            "checks": checks,
            "upstream_c2h_hashes": {
                path.name: want for path, want in expected_hashes.items()
            },
            "conditional_missing_input": (
                "complete hash-bound C2-I proof that G1..G4>0 on every "
                "retained g<1,rB>1 point of the full physical open cube"
            ),
            "python": sys.version.split()[0],
            "sympy": sp.__version__,
        },
        indent=2,
        sort_keys=True,
    )
)
