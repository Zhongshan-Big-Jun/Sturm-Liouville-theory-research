#!/usr/bin/env python3
"""Exact algebra and bounded discovery checks for MIN-REFL-C2-G.

The exact part reconstructs the general-mu positive--negative interface from
both momentum matching equations, proves the shared-contrast middle-cell
compatibility polynomial, and audits the n=3 forced-charge determinant
factorization.  The grid scout is only diagnostic and never certifies a
universal sign.
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "exact_checker.json"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def exact_audit() -> dict[str, object]:
    # Positive-cell phase data (c,s,C,S), negative-cell phase data
    # (d,t,D,T), shared contrast r, and the two amplitude ratios a,b.
    c, s, C, S, d, t, D, T, r = sp.symbols(
        "c s C S d t D T r", nonzero=True
    )
    Delta = sp.expand(t * S - s * T)
    A0 = sp.expand(t * S * c + s * T * C)
    A1 = sp.expand(s * S * (d + D))
    B0 = sp.expand(t * T * (c + C))
    B1 = sp.expand(t * S * D + s * T * d)
    inva = sp.cancel((A0 + r * A1) / Delta)
    a = sp.cancel(1 / inva)
    b = sp.cancel(-(B0 + r * B1) / (r * Delta))

    # Both physical momenta are divided by the common interface amplitude.
    u_residual = sp.factor((c - inva) / s - r * (b - d) / t)
    v_residual = sp.factor(-(inva + C) / S - r * (b + D) / T)
    assert u_residual == 0
    assert v_residual == 0

    boundary_comparison = sp.expand(A1 * B0 - B1 * (A0 - Delta))
    xi_algebraic = sp.cancel(
        -d * T / (D * t) - (S / s) * (1 - c) / (1 + C)
    )
    xi_factor = sp.cancel(s * t * Delta * (1 + C) * (-D) * xi_algebraic)
    xi_identity_residual = sp.factor(boundary_comparison - xi_factor)
    assert xi_identity_residual == 0

    # Two negative neighbours, the same positive-cell phase, and one shared
    # contrast.  The left interface is time-reversed, so its positive ratio
    # is the reciprocal of the actual middle-cell ratio.
    Dl, Dr, A0l, A0r, A1l, A1r = sp.symbols(
        "Delta_l Delta_r A0_l A0_r A1_l A1_r", nonzero=True
    )
    al = Dl / (A0l + r * A1l)
    ar = Dr / (A0r + r * A1r)
    compat = sp.factor(
        (A0l + r * A1l) * (A0r + r * A1r) - Dl * Dr
    )
    compat_from_product = sp.factor(
        sp.together(al * ar - 1)
        * (A0l + r * A1l)
        * (A0r + r * A1r)
    )
    assert sp.factor(compat_from_product + compat) == 0
    compat_poly = sp.Poly(sp.expand(compat), r)

    # Forced-charge identity at n=3.  These variables are the four physical
    # positive-cell response margins and the middle off-diagonal compliance.
    A_left, B_left, A_right, B_right, sm, v1, v2 = sp.symbols(
        "A_left B_left A_right B_right s_m v1 v2"
    )
    e = sm * v1 * v2
    q1 = v1 * (A_left + B_left - sm * v2)
    q2 = v2 * (A_right + B_right - sm * v1)
    forest = sp.factor(q1 * q2 + e * (q1 + q2))
    compensated = sp.factor(
        v1
        * v2
        * ((A_left + B_left) * (A_right + B_right) - sm**2 * v1 * v2)
    )
    assert sp.factor(forest - compensated) == 0
    total_charge = sp.factor(q1 + q2)
    delta_edge_left = sp.factor(v1 * A_left)
    delta_middle = sp.factor(
        v1 * B_left + v2 * A_right - 2 * sm * v1 * v2
    )
    delta_edge_right = sp.factor(v2 * B_right)
    block_deficit_sum = sp.factor(
        delta_edge_left + delta_middle + delta_edge_right
    )
    assert sp.factor(total_charge - block_deficit_sum) == 0
    loaded_robin_det = sp.factor(
        (B_left / v1) * (A_right / v2) - sm**2
    )
    D_middle = sp.factor(sm**2 * v1 * v2 - A_right * B_left)
    assert sp.factor(D_middle + v1 * v2 * loaded_robin_det) == 0

    # Reflection-fixed specialization, retained only as an exact parity
    # decomposition; no sign is asserted.
    Aedge, Bmid, v = sp.symbols("A_edge B_mid v")
    reflected = sp.factor(
        compensated.subs(
            {
                A_left: Aedge,
                B_right: Aedge,
                B_left: Bmid,
                A_right: Bmid,
                v1: v,
                v2: v,
            },
            simultaneous=True,
        )
    )
    expected_reflected = sp.factor(
        v**2 * (Aedge + Bmid - sm * v) * (Aedge + Bmid + sm * v)
    )
    assert sp.factor(reflected - expected_reflected) == 0

    # Independent half-angle chart.  X and Y denote the high-frequency
    # half-angle tangents here (not squares as in the old mu=2 chart).
    x, X, y, Y = sp.symbols("x X y Y", positive=True)
    half = {
        c: (1 - x**2) / (1 + x**2),
        s: 2 * x / (1 + x**2),
        C: (1 - X**2) / (1 + X**2),
        S: 2 * X / (1 + X**2),
        d: (1 - y**2) / (1 + y**2),
        t: 2 * y / (1 + y**2),
        D: (1 - Y**2) / (1 + Y**2),
        T: 2 * Y / (1 + Y**2),
    }
    half_delta = sp.factor(Delta.subs(half, simultaneous=True))
    half_A0 = sp.factor(A0.subs(half, simultaneous=True))
    half_A1 = sp.factor(A1.subs(half, simultaneous=True))
    half_B0 = sp.factor(B0.subs(half, simultaneous=True))
    half_B1 = sp.factor(B1.subs(half, simultaneous=True))
    half_feasibility = sp.factor((B0 + B1).subs(half, simultaneous=True))
    half_comparison = sp.factor(
        (A1 * B0 - B1 * (A0 - Delta)).subs(half, simultaneous=True)
    )
    X_at_comparison_zero = sp.cancel(
        Y * (1 - y**2) / (x * y * (Y**2 - 1))
    )
    feasibility_at_comparison_zero = sp.factor(
        half_feasibility.subs(X, X_at_comparison_zero)
    )
    triple = lambda z: sp.cancel((3 * z - z**3) / (1 - 3 * z**2))
    mu3_sub = {X: triple(x), Y: triple(y)}
    mu3_delta = sp.factor(half_delta.subs(mu3_sub, simultaneous=True))
    mu3_A0 = sp.factor(half_A0.subs(mu3_sub, simultaneous=True))
    mu3_A1 = sp.factor(half_A1.subs(mu3_sub, simultaneous=True))
    mu3_B0 = sp.factor(half_B0.subs(mu3_sub, simultaneous=True))
    mu3_B1 = sp.factor(half_B1.subs(mu3_sub, simultaneous=True))
    mu3_feasibility = sp.factor(
        half_feasibility.subs(mu3_sub, simultaneous=True)
    )
    mu3_comparison = sp.factor(
        half_comparison.subs(mu3_sub, simultaneous=True)
    )

    return {
        "interface": {
            "Delta": str(Delta),
            "A0": str(A0),
            "A1": str(A1),
            "B0": str(B0),
            "B1": str(B1),
            "a": str(a),
            "b": str(b),
            "momentum_residuals": [str(u_residual), str(v_residual)],
            "boundary_comparison": str(sp.factor(boundary_comparison)),
            "Xi_algebraic": str(xi_algebraic),
            "Xi_factor_identity": (
                "A1*B0-B1*(A0-Delta)="
                "s*t*Delta*(1+C)*(-D)*Xi"
            ),
            "Xi_factor_identity_residual": str(xi_identity_residual),
        },
        "shared_contrast_middle_cell": {
            "compatibility_polynomial": str(compat),
            "coefficients_r_ascending": [
                str(compat_poly.coeff_monomial(r**j)) for j in range(3)
            ],
            "product_identity_residual": str(
                sp.factor(compat_from_product + compat)
            ),
        },
        "forced_charge": {
            "forest_expression": str(forest),
            "compensated_expression": str(compensated),
            "identity_residual": str(sp.factor(forest - compensated)),
            "reflection_factorization": str(reflected),
            "reflection_identity_residual": str(
                sp.factor(reflected - expected_reflected)
            ),
            "total_charge": str(total_charge),
            "block_deficits": [
                str(delta_edge_left),
                str(delta_middle),
                str(delta_edge_right),
            ],
            "block_deficit_sum_residual": str(
                sp.factor(total_charge - block_deficit_sum)
            ),
            "loaded_middle_robin_determinant": str(loaded_robin_det),
            "D_middle": str(D_middle),
            "D_middle_identity_residual": str(
                sp.factor(D_middle + v1 * v2 * loaded_robin_det)
            ),
        },
        "half_angle_chart": {
            "Delta": str(half_delta),
            "A0": str(half_A0),
            "A1": str(half_A1),
            "B0": str(half_B0),
            "B1": str(half_B1),
            "r_equal_one_b_feasibility": str(half_feasibility),
            "boundary_comparison": str(half_comparison),
            "r1_feasibility_at_boundary_comparison_zero": str(
                feasibility_at_comparison_zero
            ),
        },
        "mu3_chart": {
            "Delta": str(mu3_delta),
            "A0": str(mu3_A0),
            "A1": str(mu3_A1),
            "B0": str(mu3_B0),
            "B1": str(mu3_B1),
            "r_equal_one_b_feasibility": str(mu3_feasibility),
            "boundary_comparison": str(mu3_comparison),
        },
    }


def interface(mu: float, theta: float, eta: float, r: float) -> dict[str, float]:
    c, s = math.cos(theta), math.sin(theta)
    C, S = math.cos(mu * theta), math.sin(mu * theta)
    d, t = math.cos(eta), math.sin(eta)
    D, T = math.cos(mu * eta), math.sin(mu * eta)
    Delta = t * S - s * T
    A0 = t * S * c + s * T * C
    A1 = s * S * (d + D)
    B0 = t * T * (c + C)
    B1 = t * S * D + s * T * d
    den = A0 + r * A1
    a = Delta / den
    b = -(B0 + r * B1) / (r * Delta)
    inva = 1.0 / a

    # Event crossing orientations at all four ends of the two cells.
    xpl = (a - c) / s
    ypl = -(a + C) / S
    xpr = (c * a - 1.0) / (s * a)
    ypr = -(1.0 + C * a) / (S * a)
    xnl = r * (b - d) / t
    ynl = r * (b + D) / T
    xnr = r * (d * b - 1.0) / (t * b)
    ynr = r * (1.0 + D * b) / (T * b)
    gammas = (
        xpl - mu * ypl,
        xpr + mu * ypr,
        xnl + mu * ynl,
        xnr - mu * ynr,
    )
    return {
        "a": a,
        "b": b,
        "Delta": Delta,
        "den": den,
        "Bnumerator": B0 + r * B1,
        "A0": A0,
        "A1": A1,
        "B0": B0,
        "B1": B1,
        "F0": A0 - Delta,
        "boundary_comparison": A1 * B0 - B1 * (A0 - Delta),
        "momentum_error": max(abs(xpr - xnl), abs(ypr - ynl)),
        "gamma_positive_left": gammas[0],
        "gamma_positive_right": gammas[1],
        "gamma_negative_left": gammas[2],
        "gamma_negative_right": gammas[3],
    }


def diagnostic_scout() -> dict[str, object]:
    rows: list[dict[str, float]] = []
    counts: dict[str, dict[str, float | int | None]] = {}
    for mu in (1.02, 1.1, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0, 4.0, 6.0):
        physical = 0
        expanding = 0
        min_a = math.inf
        max_a = -math.inf
        first_expander = None
        feasible_phase_pairs = 0
        negative_boundary_comparison_pairs = 0
        minimum_boundary_comparison = math.inf
        positive_simple_gap_pairs = 0
        cut = math.pi / (mu + 1.0)
        top = math.pi / mu
        for it in range(1, 35):
            theta = cut * it / 35.0
            for ie in range(1, 35):
                eta = cut + (top - cut) * ie / 35.0
                try:
                    phase_probe = interface(mu, theta, eta, 1.0 + 1.0e-9)
                except ZeroDivisionError:
                    continue
                if (
                    phase_probe["A1"] < 0.0
                    and phase_probe["B1"] < 0.0
                    and phase_probe["A0"] / (-phase_probe["A1"]) > 1.0
                    and phase_probe["B0"] / (-phase_probe["B1"]) > 1.0
                ):
                    feasible_phase_pairs += 1
                    minimum_boundary_comparison = min(
                        minimum_boundary_comparison,
                        phase_probe["boundary_comparison"],
                    )
                    if phase_probe["boundary_comparison"] < -1.0e-12:
                        negative_boundary_comparison_pairs += 1
                    if 2.0 * math.tan(theta / 2.0) * math.tan(eta / 2.0) + math.tan(eta / 2.0) ** 2 >= 1.0:
                        positive_simple_gap_pairs += 1
                for ir in range(1, 55):
                    r = math.exp(math.log(1.0005) + ir / 55.0 * math.log(80.0))
                    try:
                        z = interface(mu, theta, eta, r)
                    except (ValueError, ZeroDivisionError, OverflowError):
                        continue
                    pred = (
                        z["Delta"] > 0.0
                        and z["den"] > 0.0
                        and z["a"] > 0.0
                        and z["b"] < 0.0
                        and z["gamma_positive_left"] > 0.0
                        and z["gamma_positive_right"] < 0.0
                        and z["gamma_negative_left"] < 0.0
                        and z["gamma_negative_right"] > 0.0
                        and z["momentum_error"] < 2.0e-9
                    )
                    if not pred:
                        continue
                    physical += 1
                    min_a = min(min_a, z["a"])
                    max_a = max(max_a, z["a"])
                    if z["a"] > 1.0 + 1.0e-10:
                        expanding += 1
                        if first_expander is None:
                            first_expander = {
                                "mu": mu,
                                "theta": theta,
                                "eta": eta,
                                "r": r,
                                "a": z["a"],
                                "b": z["b"],
                            }
        counts[str(mu)] = {
            "retained_local_interfaces": physical,
            "expanding_a_count": expanding,
            "min_a": None if physical == 0 else min_a,
            "max_a": None if physical == 0 else max_a,
            "feasible_phase_pairs": feasible_phase_pairs,
            "negative_boundary_comparison_pairs": negative_boundary_comparison_pairs,
            "minimum_boundary_comparison": (
                None if feasible_phase_pairs == 0 else minimum_boundary_comparison
            ),
            "nonnegative_2xy_plus_y2_minus1_pairs": positive_simple_gap_pairs,
        }
        if first_expander is not None:
            rows.append(first_expander)
    return {
        "arithmetic": "binary64 diagnostic grid",
        "grid": "34x34x54 per listed mu; r in (1.0005,80) logarithmic",
        "validity_predicate": (
            "strict phase chambers; a>0>b; four event gamma orientations; "
            "both momentum residuals below 2e-9"
        ),
        "counts": counts,
        "first_expanders": rows,
        "limitation": (
            "local two-cell predicates only; no middle composition, endpoints, "
            "common-terminal action, or completeness certificate"
        ),
    }


def main() -> int:
    payload = {
        "status_label": "RIGOROUS_PARTIAL_RESULT",
        "exact_audit": exact_audit(),
        "sympy_version": sp.__version__,
        "computation_scope": (
            "exact symbolic identities only; no numerical or finite-search "
            "claim is included in the frozen output"
        ),
    }
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=False),
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "output": str(OUTPUT),
                "output_sha256": sha256_file(OUTPUT),
                "script_sha256": sha256_file(Path(__file__)),
                "exact_residuals_zero": True,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
