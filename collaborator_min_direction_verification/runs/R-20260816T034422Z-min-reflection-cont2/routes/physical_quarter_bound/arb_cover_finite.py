"""Finite Arb cover for the quarter ratios on the R17 compact inner cube.

The evaluator retains the exact common-angle equations.  Positivity
contractors are used only on boxes that may meet g<1 and rB>1, exactly as in
the frozen R17 checker.
"""

from __future__ import annotations

import importlib.util
import argparse
import json
from pathlib import Path


HERE = Path(__file__).resolve()
PROJECT = HERE.parents[4]
UPSTREAM = PROJECT / "runs/R-20260812T165103Z-mpo3a-cont4/routes/r17_min_n2_inner_box_arb_certificate/exact_checker.py"
SPEC = importlib.util.spec_from_file_location("r17", UPSTREAM)
assert SPEC and SPEC.loader
R17 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(R17)
R17.ctx.prec = 160


def ratio_uppers(v):
    names = ("g", "K", "cp2", "P", "X")
    if not all(R17.lower_positive(v[n]) for n in names):
        return None
    # First use the correlated Arb expressions directly when the entire
    # ambient box already has the physical signs.  This is much sharper
    # than independent endpoint products and remains a rigorous enclosure.
    direct_names = ("ebar", "rb-1", "W0", "W1", "U0", "U1")
    if all(R17.lower_positive(v[n]) for n in direct_names):
        h0 = v["X"] + v["ebar"] * v["W0"]
        h1 = v["X"] + v["ebar"] * v["W1"]
        l0 = 2 * h0 + v["ebar"] * v["U0"]
        l1 = 2 * h1 + v["ebar"] * v["U1"]
        sr = v["rb-1"]
        Delta = sr * (sr + 2)
        ns = (
            sr * v["U0"] * l0 / 2,
            (2 * sr * (v["U1"] * l0 + v["U0"] * l1) + Delta * v["U0"] * l0) / 6,
            (2 * sr * v["U1"] * l1 + Delta * (v["U1"] * l0 + v["U0"] * l1)) / 4,
            Delta * v["U1"] * l1,
        )
        base_ball = v["g"] * v["K"] * v["cp2"] ** 2
        direct = tuple(v["P"] * n / base_ball for n in ns)
        if all(q.is_finite() for q in direct):
            return direct

    emax = v["ebar"].upper()
    if emax <= 0:
        return None
    xup = v["X"].upper()
    w0up = max(R17.arb(0), v["W0"].upper())
    w1up = max(R17.arb(0), v["W1"].upper())
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
    base = v["g"].lower() * v["K"].lower() * v["cp2"].lower() ** 2
    return tuple(v["P"].upper() * n / base for n in nups)


def run(max_boxes=4_000_000):
    den, collar = R17.DEN, R17.COLLAR
    root = ((collar, den - collar),) * 3
    stack = [root]
    counts = {"visited": 0, "discard_g": 0, "discard_r": 0, "proved": 0, "split": 0, "singular": 0, "unresolved": 0}
    maxima = [None] * 4
    while stack and counts["visited"] < max_boxes:
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
            ratios = ratio_uppers(v)
            if ratios is not None and all(q < R17.arb(1) / 4 for q in ratios):
                counts["proved"] += 1
                for i, ratio in enumerate(ratios):
                    val = float(ratio.upper())
                    if maxima[i] is None or val > maxima[i]:
                        maxima[i] = val
                continue
        except Exception:
            counts["singular"] += 1
        widths = [hi - lo for lo, hi in box]
        j = max(range(3), key=lambda i: widths[i])
        lo, hi = box[j]
        if hi - lo <= 1:
            counts["unresolved"] += 1
            continue
        mid = (lo + hi) // 2
        left, right = list(box), list(box)
        left[j], right[j] = (lo, mid), (mid, hi)
        stack.extend((tuple(right), tuple(left)))
        counts["split"] += 1
    leaves = counts["discard_g"] + counts["discard_r"] + counts["proved"] + counts["unresolved"]
    complete = not stack and counts["unresolved"] == 0 and counts["singular"] == 0
    if complete:
        assert leaves == counts["split"] + 1
        assert counts["visited"] == leaves + counts["split"]
    return {
        "status": "FINITE_COMPUTATIONAL_RESULT",
        "claim": "all four full finite-t ratios are below 1/4 on the exact retained inner cube",
        "domain": {"k,t,y": ["1/64", "63/64"], "retained": ["g<1", "rB>1"]},
        "complete": complete,
        "counts": counts,
        "leaf_identity": [leaves, counts["split"] + 1],
        "stack_remaining": len(stack),
        "pending_boxes_dyadic": stack[:64],
        "max_certified_upper_by_ratio": maxima,
        "precision_bits": R17.ctx.prec,
        "partition_bits": R17.BITS,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-boxes", type=int, default=100_000)
    args = parser.parse_args()
    print(json.dumps(run(args.max_boxes), indent=2))
