#!/usr/bin/env python3
"""Exact replay for route-001-finite-r-branch-certification.

This script reads only the six hash-bound repository sources from the frozen
problem contract.  It imports the series builder without running its main
routine, so it does not create the repository pickle.  It intentionally
reproduces the bound builder output, including the D-side left-mass exponent
bug audited by finite_r_direct_check.py; its E5 output is therefore a failure
reproduction, not proof about the exact closed system.

Replay (PowerShell, from E:\\ai_benchmark\\source_repo):
  $env:PYTHONDONTWRITEBYTECODE='1'; python research/artifacts/blueprint-rigorous-math/R-20260825T100044Z-b4-m3-blueprint/round-001/route-001-finite-r-branch-certification/finite_r_replay.py
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import platform
import sys
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[6]
BOUND = {
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
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def load_builder():
    path = ROOT / "scripts/_gapn2_largeR_Pbuild.py"
    spec = importlib.util.spec_from_file_location("bound_gapn2_largeR_Pbuild", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load bound series builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    observed = {name: sha256(ROOT / name) for name in BOUND}
    if observed != BOUND:
        raise RuntimeError(json.dumps({"expected": BOUND, "observed": observed}, indent=2))

    builder = load_builder()
    P = builder.build()
    # Use the builder's own symbol objects; symbols with the same printed name
    # but different assumptions are distinct to SymPy.
    symbol_map = {
        symbol.name: symbol
        for expression in P.values()
        for symbol in expression.free_symbols
    }
    K, A, B, C = (symbol_map[name] for name in ("K", "A", "B", "C"))

    # Exact leading map in the original, uncleared equations.  The residual
    # normalization is forced by the first nonzero order in the bound series.
    lead = sp.Matrix([
        sp.factor(P[("E1", 0)]),
        sp.factor(P[("E2", 0)]),
        sp.factor(P[("E5", 2)]),
        sp.factor(P[("E6", 3)]),
    ])
    jac = sp.simplify(lead.jacobian([K, A, B, C]))
    on_constraint = {A: 2 / K}
    jac_on = sp.simplify(jac.subs(on_constraint))

    print("SOFTWARE")
    print(json.dumps({
        "python": sys.version.split()[0],
        "implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "sympy": sp.__version__,
    }, sort_keys=True))
    print("BOUND_HASHES")
    print(json.dumps(observed, sort_keys=True))
    print("SERIES_KEYS")
    print(json.dumps(sorted([f"{e}:{m}" for e, m in P]), separators=(",", ":")))
    print("LEADING_RAW")
    for name, value in zip(("E1_0", "E2_0", "E5_2", "E6_3"), lead):
        print(name, "=", sp.sstr(value))
    print("LEADING_JACOBIAN_ON_AK_EQ_2")
    print(sp.sstr(jac_on))
    print("GENERIC_RANK_FOR_K_NONZERO", jac_on.rank())
    print("GENERIC_NULLSPACE_FOR_K_NONZERO")
    for vector in jac_on.nullspace():
        print(sp.sstr(vector))

    # Reproduce the cleared versions used in the source addendum.  Clearing
    # by K^2, K^5, K is valid only in the chart K != 0.
    cleared = sp.Matrix([
        sp.factor(P[("E1", 0)]),
        sp.factor(K**2 * P[("E2", 0)]),
        sp.factor(K**5 * P[("E5", 2)]),
        sp.factor(K * P[("E6", 3)]),
    ])
    print("LEADING_K_CLEARED")
    for name, value in zip(("E1_0", "K2E2_0", "K5E5_2", "KE6_3"), cleared):
        print(name, "=", sp.sstr(value))

    # Exact denominator neighborhood: at u=0, p1=p1t=pi/2 and
    # p3=p3t=pi/4.  Hence sin(p1t), sin(p3), and cos(p3t) equal
    # 1, sqrt(2)/2, sqrt(2)/2 respectively.  Continuity gives a nonzero
    # neighborhood once K stays separated from zero.
    print("BOUNDARY_VALUES")
    print(json.dumps({
        "sin_p1t_at_u0": "1",
        "sin_p3_at_u0": "sqrt(2)/2",
        "cos_p3t_at_u0": "sqrt(2)/2",
        "K_clearance_required": "K != 0",
    }, sort_keys=True))

    # First justified blow-up.  The rank-one leading relation forces
    # A*K-2 = O(u^2), so introduce D=(A*K-2)/u^2 exactly, i.e.
    # A=(2+u^2 D)/K.  Dividing by the first surviving powers gives an
    # analytic endpoint map in the chart K != 0.
    u, D = sp.symbols("u D", real=True)
    A_blow = (2 + u**2 * D) / K

    def truncated(eq: str, order: int):
        return sp.Add(*[
            P[(eq, degree)] * u**degree
            for degree in range(order + 1)
            if (eq, degree) in P
        ])

    endpoint_specs = (("E1", 2), ("E2", 2), ("E5", 4), ("E6", 5))
    blowup_endpoint = []
    for eq, divisor in endpoint_specs:
        expression = truncated(eq, divisor).subs(A, A_blow)
        coefficient = sp.factor(sp.expand(expression).coeff(u, divisor))
        blowup_endpoint.append(coefficient)
    blowup_endpoint = sp.Matrix(blowup_endpoint)
    blowup_jac = sp.simplify(blowup_endpoint.jacobian([K, D, B, C]))
    print("FIRST_BLOWUP_ENDPOINT_RAW")
    for name, value in zip(("E1/u2", "E2/u2", "E5/u4", "E6/u5"), blowup_endpoint):
        print(name, "=", sp.sstr(sp.factor(value)))
    source_e5_u5 = sp.factor(
        sp.expand(truncated("E5", 5).subs(A, A_blow)).coeff(u, 5)
    )
    print("SOURCE_BUILDER_E5_U5_FIXED_D_C =", sp.sstr(source_e5_u5))

    # E1 and E2 imply the candidate endpoint relations below.  They are
    # substituted only after printing the original endpoint system.
    C_seed = sp.factor(16 / (sp.pi * K))
    D_seed = sp.factor(-(K**3 + 24 - 18 * sp.pi) / (6 * K))
    seed_sub = {C: C_seed, D: D_seed}
    endpoint_reduced = [sp.factor(value.subs(seed_sub)) for value in blowup_endpoint]
    print("FIRST_BLOWUP_SEED_RELATIONS")
    print("C =", sp.sstr(C_seed))
    print("D =", sp.sstr(D_seed))
    print("ENDPOINT_AFTER_RELATIONS")
    for name, value in zip(("E1/u2", "E2/u2", "E5/u4", "E6/u5"), endpoint_reduced):
        print(name, "=", sp.sstr(value))
    e5_num, e5_den = sp.cancel(endpoint_reduced[2]).as_numer_denom()
    print("REDUCED_E5_NUMERATOR =", sp.sstr(sp.factor(e5_num)))
    print("REDUCED_E5_DENOMINATOR =", sp.sstr(sp.factor(e5_den)))
    print("REDUCED_E5_NUMERATOR_DEGREE_IN_K", sp.Poly(e5_num, K).degree())
    print("REDUCED_E5_NUMERATOR_APPROX_ROOTS")
    for root in sp.nroots(sp.Poly(e5_num, K), n=30, maxsteps=200):
        print(sp.sstr(root))

    # Rank is evaluated at a root only after the exact scalar seed equation
    # has been isolated; B is absent from the endpoint, so no 4x4 ordinary
    # IFT can hold in this chart at this stage.
    print("FIRST_BLOWUP_B_COLUMN")
    print(sp.sstr(blowup_jac[:, 2]))
    print("AUDIT_VERDICT")
    print("INVALID_E5_SERIES: bound builder line 94 shifts cos(p1)/K by u^(+1),"
          " but exact cos(p1)/(K*u) requires u^(-1); use finite_r_direct_check.py")


if __name__ == "__main__":
    main()
