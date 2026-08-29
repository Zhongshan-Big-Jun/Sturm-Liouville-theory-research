"""Exact replay for route 002; prints identities and never writes source data."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

import sympy as sp


REPO = Path(__file__).resolve().parents[6]
SOURCES = {
    "runs/rigorous-open-math-research/R-20260812T090000Z-g1prime-g2/problem_contract.md":
        "1de731ba2eeb40b2e20a2f7817de0f6f1d13d42e888f42ce3d5719e9c2700148",
    "runs/rigorous-open-math-research/R-20260812T090000Z-g1prime-g2/run_notes_addendum_2026-08-14.md":
        "a4b5c8b72b08508e9e8f1a6ead786e837d0c316a564ba6a6dd06bb7d1d7284cb",
    "scripts/_gapn2_largeR_closed.py":
        "e357d8e447ce998020c8dadc94eb27db884dd85932d592a9b4331366f8ac13a4",
    "scripts/_gapn2_largeR_Pbuild.py":
        "58c98af44d074bdfd9412a1541d4a7a393f0cf3e074653c1108964b62ea6caea",
    "scripts/_gapn2_largeR_big.json":
        "1e3c924b8caa4b9424bf666f52bfcb826722de582d9e90d2658e36f1f0d66f45",
    "docs/SL_gap_nge2_symmetry_local_proof.tex":
        "6c2029fbd71885b8d94131ad93e865f13f42884d75e68a03d2d079bea79efe0a",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_pbuild():
    path = REPO / "scripts/_gapn2_largeR_Pbuild.py"
    spec = importlib.util.spec_from_file_location("gapn2_pbuild_bound", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    observed = {rel: sha256(REPO / rel) for rel in SOURCES}
    if observed != SOURCES:
        raise SystemExit(json.dumps({"hash_mismatch": observed}, indent=2))
    print(json.dumps({"source_hashes": observed}, sort_keys=True))
    print(json.dumps({"software": {"sympy": sp.__version__}}, sort_keys=True))

    module = load_pbuild()
    P = module.build()
    K, A, B, C = sp.symbols("K A B C")
    for eq in ("E1", "E2", "E5", "E6"):
        keys = sorted(m for name, m in P if name == eq)
        print(json.dumps({"equation": eq, "orders": keys}))
        for m in keys:
            print(f"{eq}[{m}] = {sp.factor(P[(eq, m)])}")

    # Exact low-order combinations on the finite-K chart.  These are useful
    # because E1 fixes x=A*K-2 up to order u^2, so the remaining equations
    # must be reduced modulo x before a valuation claim is made.
    x, q = sp.symbols("x q")
    sub_x = {A: (2 + x) / K}
    print("MOD_X_LOW_ORDER")
    for eq, m in (("E1", 0), ("E1", 2), ("E2", 0), ("E2", 2),
                  ("E5", 2), ("E5", 4), ("E5", 5),
                  ("E6", 3), ("E6", 5)):
        print(f"{eq}[{m}]|A=(2+x)/K = {sp.factor(P[(eq, m)].subs(sub_x))}")

    # Blow up x=q*u^2 at the exact displayed truncation and print the leading
    # coefficient after this forced scale.
    u = sp.symbols("u", positive=True)
    print("BLOWUP_X_Q_U2")
    for eq in ("E1", "E2", "E5", "E6"):
        expr = sum(P[(eq, m)] * u**m for name, m in P if name == eq)
        reduced = sp.series(expr.subs(A, (2 + q*u**2)/K), u, 0, 8).removeO()
        terms = sp.Poly(sp.expand(reduced), u).terms()
        print(f"{eq}|x=q*u^2 = {sp.factor(reduced)}")
        if terms:
            min_order = min(mon[0] for mon, _ in terms)
            coeff = sp.expand(reduced).coeff(u, min_order)
            print(f"{eq} leading order {min_order}: {sp.factor(coeff)}")

    # Solve the finite-nonzero leading chart exactly.  F6 is checked against
    # F1+F2, and the remaining E5 coefficient becomes a univariate seed
    # equation.  Its derivative controls whether a secondary Puiseux blow-up
    # is possible at this first Newton face.
    e1 = sum(P[("E1", m)] * u**m for name, m in P if name == "E1")
    e2 = sum(P[("E2", m)] * u**m for name, m in P if name == "E2")
    e5 = sum(P[("E5", m)] * u**m for name, m in P if name == "E5")
    e6 = sum(P[("E6", m)] * u**m for name, m in P if name == "E6")
    blown = {
        "F1": sp.expand(e1.subs(A, (2 + q*u**2)/K)).coeff(u, 2) * (-24*K/sp.sqrt(2)),
        "F2": sp.expand(e2.subs(A, (2 + q*u**2)/K)).coeff(u, 2) * (24*K/sp.sqrt(2)),
        "F5": sp.expand(e5.subs(A, (2 + q*u**2)/K)).coeff(u, 4),
        "F6": sp.expand(e6.subs(A, (2 + q*u**2)/K)).coeff(u, 5) * (-12*K),
    }
    for name in blown:
        blown[name] = sp.factor(blown[name])
        print(f"NORMALIZED_{name} = {blown[name]}")
    print(f"F6_MINUS_F1_MINUS_F2 = {sp.factor(blown['F6'] - blown['F1'] - blown['F2'])}")
    c_seed = sp.Rational(16, 1)/(sp.pi*K)
    q_seed = (18*sp.pi - 24 - K**3)/(6*K)
    seed_expr = sp.factor(blown["F5"].subs({C: c_seed, q: q_seed}))
    seed_num, seed_den = sp.fraction(seed_expr)
    print(f"C_SEED = {c_seed}")
    print(f"Q_SEED = {q_seed}")
    print(f"SEED_E5 = {seed_expr}")
    print(f"SEED_NUMERATOR = {sp.factor(seed_num)}")
    print(f"SEED_DENOMINATOR = {sp.factor(seed_den)}")

    J = sp.Matrix([blown["F1"], blown["F2"], blown["F5"]]).jacobian([q, C, K])
    det_j = sp.factor(J.det())
    det_j_seed = sp.factor(det_j.subs({C: c_seed, q: q_seed}))
    print(f"LEADING_JACOBIAN_DET = {det_j}")
    print(f"LEADING_JACOBIAN_DET_ON_SEED = {det_j_seed}")
    print(f"SEED_DERIVATIVE = {sp.factor(sp.diff(seed_num, K))}")

    # Numerical roots are evidence-only.  Print them solely to guide exact
    # interval isolation and adversarial tests.
    poly = sp.Poly(seed_num, K, extension=sp.pi)
    print(f"SEED_DEGREE = {poly.degree()}")
    print(f"SEED_NROOTS = {[str(z) for z in sp.nroots(poly, n=40, maxsteps=200)]}")


if __name__ == "__main__":
    main()
