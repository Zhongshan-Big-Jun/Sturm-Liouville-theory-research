"""Rigorous inner-box test of the physical uniform-quarter candidate.

This imports the frozen R17 directed-Arb evaluator, but replaces its target
``base - P*N_i > 0`` by the strictly stronger
``base/4 - P*N_i > 0``.  It proves only the exact inner cube and makes no
claim about omitted collars or the noncanonical physical bridge.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

from flint import arb


HERE = Path(__file__).resolve().parent
SOURCE = (
    HERE.parents[2]
    / "R-20260812T165103Z-mpo3a-cont4"
    / "routes"
    / "r17_min_n2_inner_box_arb_certificate"
    / "exact_checker.py"
)
SPEC = importlib.util.spec_from_file_location("frozen_r17", SOURCE)
assert SPEC is not None and SPEC.loader is not None
R17 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(R17)

MAX_BOXES = 7_000_000


def quarter_gap_lowers(v: dict[str, arb]) -> tuple[arb, ...] | None:
    """Directed lower bounds for base/4-P*N_i on the retained subset."""
    if not all(R17.lower_positive(v[n]) for n in ("g", "K", "cp2", "P", "X")):
        return None
    emax = v["ebar"].upper()
    if emax <= 0:
        return None

    xup = v["X"].upper()
    w0up = max(arb(0), v["W0"].upper())
    w1up = max(arb(0), v["W1"].upper())
    u0up, u1up = v["U0"].upper(), v["U1"].upper()
    if u0up <= 0 or u1up <= 0:
        return None

    h0up, h1up = xup + emax * w0up, xup + emax * w1up
    l0up = 2 * h0up + emax * u0up
    l1up = 2 * h1up + emax * u1up
    rup = 1 + v["rb-1"].upper()
    if rup <= 1:
        return None
    sup, deltaup = rup - 1, rup * rup - 1
    nups = (
        sup * u0up * l0up / 2,
        (2 * sup * (u1up * l0up + u0up * l1up) + deltaup * u0up * l0up) / 6,
        (2 * sup * u1up * l1up + deltaup * (u1up * l0up + u0up * l1up)) / 4,
        deltaup * u1up * l1up,
    )
    base_quarter = (
        v["g"].lower() * v["K"].lower() * v["cp2"].lower() ** 2 / 4
    )
    return tuple(base_quarter - v["P"].upper() * n for n in nups)


def run_cover() -> dict:
    root = ((R17.COLLAR, R17.DEN - R17.COLLAR),) * 3
    stack = [root]
    counts = {
        "visited": 0,
        "discard_g": 0,
        "discard_r": 0,
        "proved": 0,
        "split": 0,
        "singular": 0,
        "unresolved": 0,
    }
    min_gaps: list[float | None] = [None] * 4
    first_unresolved = None

    while stack and counts["visited"] < MAX_BOXES:
        box = stack.pop()
        counts["visited"] += 1
        try:
            v = R17.evaluate(*(R17.dyadic_ball(lo, hi) for lo, hi in box))
            if R17.upper_nonpositive(v["b-a"]):
                counts["discard_g"] += 1
                continue
            if R17.upper_nonpositive(v["rb-1"]):
                counts["discard_r"] += 1
                continue
            gaps = quarter_gap_lowers(v)
            if gaps is not None and all(gap > 0 for gap in gaps):
                counts["proved"] += 1
                for i, gap in enumerate(gaps):
                    value = float(gap.lower())
                    if min_gaps[i] is None or value < min_gaps[i]:
                        min_gaps[i] = value
                continue
        except Exception:
            counts["singular"] += 1

        widths = [hi - lo for lo, hi in box]
        j = max(range(3), key=lambda i: widths[i])
        lo, hi = box[j]
        if hi - lo <= 1:
            counts["unresolved"] += 1
            if first_unresolved is None:
                first_unresolved = box
            continue
        mid = (lo + hi) // 2
        left, right = list(box), list(box)
        left[j], right[j] = (lo, mid), (mid, hi)
        stack.append(tuple(right))
        stack.append(tuple(left))
        counts["split"] += 1

    complete = not stack and counts["unresolved"] == 0
    return {
        "status": "FINITE_COMPUTATIONAL_RESULT",
        "result": "PASS" if complete else "INCOMPLETE",
        "target": "Pplus*Nhat_i/(g*Knew*cp^4) < 1/4 for i=1..4",
        "scope": {
            "coordinates": ["k", "t", "y"],
            "box": ["1/64", "63/64"],
            "retained_subset": ["g<1", "rB>1"],
            "open": "all omitted boundary collars",
        },
        "source": str(SOURCE),
        "counts": counts,
        "stack_remaining": len(stack),
        "residual_stack": stack,
        "first_unresolved": first_unresolved,
        "min_certified_quarter_gap_lower_by_index": min_gaps,
    }


if __name__ == "__main__":
    print(json.dumps(run_cover(), indent=2))
