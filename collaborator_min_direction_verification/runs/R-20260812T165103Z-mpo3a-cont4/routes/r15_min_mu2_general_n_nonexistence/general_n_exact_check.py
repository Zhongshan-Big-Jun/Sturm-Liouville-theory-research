"""Exact checks for the candidate mu=2 minimum-law all-n no-go theorem.

Symbolic algebra checks the local interface formulas and contraction
identities.  Deterministic index tables attack orientation mistakes for
small words; the universal quantifier is discharged in derivation.md.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp


CANONICAL_BLUEPRINT_SHA256 = (
    "0120d1fb32af1a30449575995efccb6d1afcce416ee671ad00a5f296400fd799"
)
CANONICAL_INVENTORY_SHA256 = (
    "b6286574edbcb70ad22e5c6758a81f00dd01572c0764b8816be23cb6b166fb6f"
)
R13_DERIVATION_SHA256 = (
    "cd4f1a387c4729e0902c64843560e5643ac03b49565b21128cf8618022965e11"
)
R13_PRIMARY_SHA256 = (
    "cb2418d63eb49d4dc68ca977e1dcf14befa8ebe342a5f3d008c1ed346c3d60e4"
)
R13_INDEPENDENT_SHA256 = (
    "b987d4c2b9302bf2bf00e53667a63f0b86541ba0780d192181a01c60fc6fdafd"
)


def file_binding(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def half_angle(t: sp.Expr) -> tuple[sp.Expr, sp.Expr]:
    return (1 - t**2) / (1 + t**2), 2 * t / (1 + t**2)


def phase_pair(t: sp.Expr) -> tuple[sp.Expr, sp.Expr, sp.Expr, sp.Expr]:
    c, s = half_angle(t)
    double_tangent = 2 * t / (1 - t**2)
    C, S = half_angle(double_tangent)
    return c, s, C, S


def zero(name: str, value: sp.Expr, residuals: dict[str, str]) -> None:
    reduced = sp.factor(sp.cancel(value))
    assert reduced == 0, (name, reduced)
    residuals[name] = "0"


def local_symbolic_checks() -> tuple[dict[str, str], dict[str, str]]:
    x, y, r = sp.symbols("x y r", positive=True)
    X, Y, kappa = sp.symbols("X Y kappa", positive=True)
    c1, s1, C1, S1 = phase_pair(x)
    c2, s2, C2, S2 = phase_pair(y)

    # Raw two-momentum solve, normalized by U=1 at the positive/negative
    # interface.  The left and right event amplitudes determine a and b.
    determinant = sp.factor(s1 * S2 - s2 * S1)
    p = sp.factor(((c1 + C1) * S2 + r * (c2 + C2) * S1) / determinant)
    v = sp.factor((s1 * r * (c2 + C2) + s2 * (c1 + C1)) / determinant)
    u_left = sp.factor(c1 - s1 * p)
    u_right = sp.factor(c2 + s2 * p / r)
    a_raw = sp.factor(1 / u_left)
    b_raw = sp.factor(u_right)

    Da = (
        3 * r * x**3 * y**2
        - r * x**3
        - 3 * r * x * y**2
        + r * x
        + x**4 * y
        + 2 * x**2 * y**3
        - 4 * x**2 * y
        + y
    )
    Nb = (
        2 * r * x**3 * y**2
        + r * x * y**4
        - 4 * r * x * y**2
        + r * x
        + 3 * x**2 * y**3
        - 3 * x**2 * y
        - y**3
        + y
    )
    a = sp.factor(-y * (x - y) * (x + y) * (1 + x**2) / Da)
    b = sp.factor(Nb / (r * x * (x - y) * (x + y) * (1 + y**2)))

    residuals: dict[str, str] = {}
    zero("raw_a_minus_displayed_a", a_raw - a, residuals)
    zero("raw_b_minus_displayed_b", b_raw - b, residuals)

    T = r * x * (3 * y**2 - 1) + y * (2 * x**2 + y**2 - 1)
    zero("a_minus_one_identity", a - 1 - (1 - x**2) * T / Da, residuals)

    C = (3 * Y - 1) * (1 - Y)
    E = C + 2 * Y * (Y - X)
    kappa_N = C / E
    kappa_D = (X**2 + 2 * X * Y - 4 * X + 1) / (
        (1 - X) * (1 - 3 * X)
    )
    positive_gap = (Y - X) * ((1 - Y) ** 2 - 4 * X * Y)
    feasibility_left = Y * (1 - Y) ** 2 * (1 - 3 * X) ** 2 - X * E**2
    feasibility_right = -(X - Y) * (X * Y - 1) * (
        4 * X * Y - (1 - Y) ** 2
    )
    zero("feasibility_factorization", feasibility_left - feasibility_right, residuals)
    zero(
        "crossing_gap_factorization",
        (1 - Y - 2 * X) * E - (1 - 3 * X) * C - positive_gap,
        residuals,
    )
    zero(
        "boundary_bracket",
        kappa_N * (1 - 3 * X) + 2 * X + Y - 1 + positive_gap / E,
        residuals,
    )
    zero(
        "denominator_gap",
        kappa_D
        - kappa_N
        - 2 * (Y - X) ** 2 * (1 - X * Y)
        / ((1 - X) * (1 - 3 * X) * E),
        residuals,
    )

    r_from_kappa = kappa * y * (1 - 3 * x**2) / (x * (3 * y**2 - 1))
    T_natural = y * (kappa * (1 - 3 * X) + 2 * X + Y - 1)
    Da_natural = y * (
        X**2
        + 2 * X * Y
        - 4 * X
        + 1
        - kappa * (1 - X) * (1 - 3 * X)
    )
    Nb_natural = y * (1 - 3 * X) * (C - kappa * E) / (3 * Y - 1)
    zero(
        "T_natural_coordinate",
        T.subs(r, r_from_kappa) - T_natural.subs({X: x**2, Y: y**2}),
        residuals,
    )
    zero(
        "Da_natural_coordinate",
        Da.subs(r, r_from_kappa) - Da_natural.subs({X: x**2, Y: y**2}),
        residuals,
    )
    zero(
        "Nb_natural_coordinate",
        Nb.subs(r, r_from_kappa) - Nb_natural.subs({X: x**2, Y: y**2}),
        residuals,
    )

    # The transfer matrix of either oscillator is time-reversal invariant:
    # J M J=M^{-1}.  Substitution omega=sqrt(rho) and 2sqrt(rho) covers both
    # relay equations without changing the material contrast.
    omega, t = sp.symbols("omega t", positive=True)
    M = sp.Matrix(
        [
            [sp.cos(omega * t), sp.sin(omega * t) / omega],
            [-omega * sp.sin(omega * t), sp.cos(omega * t)],
        ]
    )
    J = sp.diag(1, -1)
    reverse_residual = (J * M * J - M.inv()).applyfunc(sp.trigsimp)
    assert reverse_residual == sp.zeros(2), reverse_residual
    residuals["time_reversal_transfer_matrix"] = "[[0, 0], [0, 0]]"

    formulas = {
        "a": str(a),
        "b": str(b),
        "Da": str(sp.expand(Da)),
        "Nb": str(sp.expand(Nb)),
        "T": str(sp.expand(T)),
        "kappa_N": str(sp.factor(kappa_N)),
        "positive_gap": "(Y-X)*((1-Y)^2-4*X*Y)",
        "contraction_sign_chain": (
            "physical domain -> 0<kappa<kappa_N<kappa_D; "
            "Da>0, T<0, 1-x^2>0, a>0; hence 0<a<1"
        ),
    }
    return residuals, formulas


def index_table(n: int) -> dict[str, object]:
    assert n >= 2
    last_cell = 2 * n - 1
    forward_pairs = []
    reverse_pairs = []
    negative_compatibilities = []
    positive_compatibilities = []

    # Forward positive j followed by negative j+1.
    for j in range(1, last_cell, 2):
        forward_pairs.append(
            {
                "cells": [j, j + 1],
                "ratios": [f"z{j}=a(x{j},y{j+1},r)", f"z{j+1}=b(x{j},y{j+1},r)"],
            }
        )

    # Physical order is negative j followed by positive j+1.  Reverse the
    # two-cell segment before applying the canonical positive-negative map.
    for j in range(2, last_cell, 2):
        reverse_pairs.append(
            {
                "cells": [j, j + 1],
                "reversed_ratios": [
                    f"1/z{j+1}=a(x{j+1},y{j},r)",
                    f"1/z{j}=b(x{j+1},y{j},r)",
                ],
            }
        )

    for j in range(2, last_cell, 2):
        negative_compatibilities.append(
            f"b(x{j-1},y{j},r)*b(x{j+1},y{j},r)=1"
        )
    for j in range(3, last_cell, 2):
        positive_compatibilities.append(
            f"a(x{j},y{j-1},r)*a(x{j},y{j+1},r)=1"
        )

    assert len(forward_pairs) == n - 1
    assert len(reverse_pairs) == n - 1
    assert len(negative_compatibilities) == n - 1
    assert len(positive_compatibilities) == n - 2
    assert len(negative_compatibilities) + len(positive_compatibilities) == 2 * n - 3
    assert bool(positive_compatibilities) == (n >= 3)
    if n >= 3:
        assert positive_compatibilities[0] == "a(x3,y2,r)*a(x3,y4,r)=1"

    return {
        "n": n,
        "event_count": 2 * n,
        "internal_cell_count": last_cell,
        "forward_pairs": forward_pairs,
        "reverse_pairs": reverse_pairs,
        "negative_compatibilities": negative_compatibilities,
        "positive_compatibilities": positive_compatibilities,
    }


def main() -> None:
    here = Path(__file__).resolve().parent
    project = here.parents[3]
    canonical = project / "statistics" / "blueprint.json"
    inventory = project / "statistics" / "evidence_inventory.csv"
    r13 = here.parent / "r13_min_n3_composition_r1"

    bindings = {
        "canonical_blueprint": file_binding(canonical),
        "canonical_inventory": file_binding(inventory),
        "r13_derivation": file_binding(r13 / "derivation.md"),
        "r13_primary_checker": file_binding(r13 / "amplitude_contraction_mu2.py"),
        "r13_independent_checker": file_binding(r13 / "independent_amplitude_audit.py"),
    }
    assert bindings["canonical_blueprint"]["sha256"] == CANONICAL_BLUEPRINT_SHA256
    assert bindings["canonical_inventory"]["sha256"] == CANONICAL_INVENTORY_SHA256
    assert bindings["r13_derivation"] == {"bytes": 10202, "sha256": R13_DERIVATION_SHA256}
    assert bindings["r13_primary_checker"] == {"bytes": 6257, "sha256": R13_PRIMARY_SHA256}
    assert bindings["r13_independent_checker"] == {
        "bytes": 4870,
        "sha256": R13_INDEPENDENT_SHA256,
    }

    residuals, formulas = local_symbolic_checks()
    full_tables = {str(n): index_table(n) for n in range(2, 13)}
    tables = {}
    for key, table in full_tables.items():
        pos = table["positive_compatibilities"]
        neg = table["negative_compatibilities"]
        tables[key] = {
            "event_count": table["event_count"],
            "internal_cell_count": table["internal_cell_count"],
            "forward_pair_count": len(table["forward_pairs"]),
            "reverse_pair_count": len(table["reverse_pairs"]),
            "negative_compatibility_count": len(neg),
            "positive_compatibility_count": len(pos),
            "first_positive_compatibility": pos[0] if pos else None,
            "last_positive_compatibility": pos[-1] if pos else None,
        }
    payload = {
        "status_label": "CANDIDATE_COMPLETE_PROOF",
        "result": (
            "For every finite R>1 and integer n>=3, no strict premise-complete "
            "transverse common-terminal mu=2 minimum-law full-relay root exists."
        ),
        "bindings": bindings,
        "sympy_version": sp.__version__,
        "symbolic_residuals": residuals,
        "local_formulas": formulas,
        "universal_index_identity": {
            "range": "odd j with 3<=j<=2n-3",
            "left_reversal": "1/z_j=a(x_j,y_(j-1),r)",
            "right_forward": "z_j=a(x_j,y_(j+1),r)",
            "compatibility": "a(x_j,y_(j-1),r)*a(x_j,y_(j+1),r)=1",
            "minimal_index": "j=3 exists iff n>=3",
            "contradiction": "both a factors are in (0,1)",
        },
        "adversarial_finite_index_tables": tables,
        "orientation_sample": {
            "forward_cells_1_2": full_tables["3"]["forward_pairs"][0],
            "reverse_cells_2_3": full_tables["3"]["reverse_pairs"][0],
        },
        "finite_check_limitation": (
            "The n=2..12 tables test indexing only; derivation.md proves the "
            "displayed arbitrary-index identity for every n>=3."
        ),
        "scope": {
            "law": "minimum only",
            "included": "strict physical mu=2 interfaces, arbitrary asymmetry and reflection",
            "excluded": "n=2, maximum law, boundary/grazing/collapsed words",
            "endpoint_note": (
                "endpoint and norm equations add constraints to an already empty "
                "internal compatibility system"
            ),
        },
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
