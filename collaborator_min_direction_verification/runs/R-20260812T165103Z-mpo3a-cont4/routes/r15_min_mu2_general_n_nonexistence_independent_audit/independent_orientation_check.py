"""Mechanism-independent exact audit of the R15 orientation step.

This checker does not import the author's formulas or checker.  It solves
the two momentum-continuity equations twice: once for a forward
positive--negative material pair and once for a forward
negative--positive pair.  The second solution must be the reciprocal,
order-reversed first solution.  Both switch-sign gauges are checked.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
AUTHOR = HERE.parent / "r15_min_mu2_general_n_nonexistence"
EXPECTED = {
    "derivation.md": "97816827f2044ee7abbc2f80b90d0323c48298d3f797dfb6a15379127ed9509e",
    "general_n_exact_check.py": "e72deabb74c2e1b88f02dfdabae7e242d418e23354dff4640db4f1f088ecdb42",
    "general_n_exact_check.json": "52c84d41496f406c1e83d6a8bd6e977b20fdef3d3c4bbaf6c7abbc73c2f93e65",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def trig_from_half_angle(q: sp.Expr) -> tuple[sp.Expr, sp.Expr, sp.Expr, sp.Expr]:
    c = (1 - q**2) / (1 + q**2)
    s = 2 * q / (1 + q**2)
    C = (1 - 6 * q**2 + q**4) / (1 + q**2) ** 2
    S = 4 * q * (1 - q**2) / (1 + q**2) ** 2
    return c, s, C, S


def solve_pair(
    first_material: sp.Expr,
    second_material: sp.Expr,
    first_phase: tuple[sp.Expr, sp.Expr, sp.Expr, sp.Expr],
    second_phase: tuple[sp.Expr, sp.Expr, sp.Expr, sp.Expr],
    switch_gauge: int,
) -> tuple[sp.Expr, sp.Expr]:
    """Return endpoint amplitudes (left, right), shared amplitude fixed to 1."""

    c1, s1, C1, S1 = first_phase
    c2, s2, C2, S2 = second_phase
    k1, k2 = first_material, second_material
    sigma0 = sp.Integer(switch_gauge)
    sigma1 = -sigma0
    sigma2 = sigma0
    left, right = sp.symbols("left right")

    # Lower-frequency momentum at the shared event: right derivative of
    # cell 1 equals left derivative of cell 2.
    lower = k1 * (c1 - left) / s1 - k2 * (right - c2) / s2

    # At an event V=sigma*U/2.  After the factor 2 from the high frequency
    # cancels the event normalization 1/2, its shared momenta are below.
    high_left = k1 * (sigma1 * C1 - sigma0 * left) / S1
    high_right = k2 * (sigma2 * right - sigma1 * C2) / S2
    high = high_left - high_right

    matrix, rhs = sp.linear_eq_to_matrix((lower, high), (left, right))
    solution = matrix.inv() * rhs
    return tuple(sp.factor(sp.cancel(v)) for v in solution)


def main() -> None:
    for name, expected in EXPECTED.items():
        actual = sha256(AUTHOR / name)
        assert actual == expected, (name, actual, expected)

    x, y, r = sp.symbols("x y r", positive=True)
    positive = trig_from_half_angle(x)
    negative = trig_from_half_angle(y)

    solutions: dict[int, tuple[sp.Expr, sp.Expr, sp.Expr, sp.Expr]] = {}
    for gauge in (1, -1):
        # Minimum law: positive S-cell has rho=1, negative S-cell rho=R.
        # Material frequencies are therefore 1 and r=sqrt(R).
        left_pn, right_pn = solve_pair(1, r, positive, negative, gauge)
        left_np, right_np = solve_pair(r, 1, negative, positive, gauge)

        # Direct time reversal: (negative,positive) forward is
        # (positive,negative) backward.  Endpoint amplitudes swap, while
        # the shared amplitude remains one.
        assert sp.factor(sp.cancel(left_np - right_pn)) == 0
        assert sp.factor(sp.cancel(right_np - left_pn)) == 0

        # For the canonical positive--negative pair, the cell ratios are
        # a=1/left_pn and b=right_pn.  Thus the forward negative--positive
        # ratios are 1/left_np=1/b and right_np=1/a.
        a = sp.factor(1 / left_pn)
        b = sp.factor(right_pn)
        assert sp.factor(sp.cancel(1 / left_np - 1 / b)) == 0
        assert sp.factor(sp.cancel(right_np - 1 / a)) == 0
        solutions[gauge] = (left_pn, right_pn, left_np, right_np)

    # Flipping all event quotient signs is the harmless V -> -V gauge.
    for i in range(4):
        assert sp.factor(sp.cancel(solutions[1][i] - solutions[-1][i])) == 0

    omega, tau = sp.symbols("omega tau", positive=True)
    M = sp.Matrix(
        [
            [sp.cos(omega * tau), sp.sin(omega * tau) / omega],
            [-omega * sp.sin(omega * tau), sp.cos(omega * tau)],
        ]
    )
    J = sp.diag(1, -1)
    assert (J * M * J - M.inv()).applyfunc(sp.trigsimp) == sp.zeros(2)

    # The universal index claim is arithmetic, not finite enumeration.
    # n>=3 implies 1<=2<3<4<=2n-1 and 3<=2n-3.
    n = sp.symbols("n", integer=True, positive=True)
    index_gaps = {
        "last_cell_minus_4": 2 * n - 5,
        "upper_j_minus_3": 2 * n - 6,
    }
    assert index_gaps["last_cell_minus_4"].subs(n, 3) == 1
    assert index_gaps["upper_j_minus_3"].subs(n, 3) == 0

    print("author_hash_bindings PASS")
    print("minimum_material_forward positive-negative=(1,r) PASS")
    print("minimum_material_reversed negative-positive->positive-negative=(1,r) PASS")
    print("direct_negative_positive_ratios (1/b,1/a) PASS")
    print("left_positive_ratio_after_reversal 1/z_j=a PASS")
    print("both_switch_sign_gauges PASS")
    print("transfer_time_reversal JMJ=M^-1 PASS")
    print("j=3_range_for_every_n_ge_3 PASS")


if __name__ == "__main__":
    main()
