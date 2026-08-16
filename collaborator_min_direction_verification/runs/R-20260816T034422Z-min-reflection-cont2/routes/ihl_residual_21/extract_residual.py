"""Replay the frozen IHL cap and serialize its exact final stack.

The traversal through the first 1,000,000 visits is intentionally identical
to event_inertia/cover_collar.py.  Extra evaluation happens only after the
cap and cannot affect the residual coordinates.
"""
from __future__ import annotations

import importlib.util
import json
import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
PROJECT = HERE.parents[4]
sys.path.insert(0, str(PROJECT / "tmp/r12-flint312"))

UP = PROJECT / "runs/R-20260815T181317Z-min-reflection/routes/event_inertia/cover_collar.py"
SPEC = importlib.util.spec_from_file_location("cover", UP)
assert SPEC and SPEC.loader
C = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(C)
R17 = C.R17


def interval_record(x):
    """JSON-safe directed Arb diagnostic."""
    return {
        "ball": str(x),
        "lower": str(x.lower()),
        "upper": str(x.upper()),
    }


def stable_diagnostics(box):
    k, t, y = (R17.dyadic_ball(lo, hi) for lo, hi in box)
    one, two, pi = R17.arb(1), R17.arb(2), R17.arb.pi()
    c = pi / two
    h = c * (one - t)
    eta = pi * y * (one - k) / (two * (one + k))
    x = h.tan()
    e = eta.tan()
    p = (k * (c - h)).tan()
    s = (k * (c + eta)).tan()
    gdef = s * e - p * x
    rb_num = x * (one - s * s * e * e)
    rb_den = e * (one + s * s) + x * p * s * (one + e * e)
    rb_stable = rb_num / rb_den
    return {
        "h": interval_record(h),
        "eta": interval_record(eta),
        "stable_g_defect_se_minus_px": interval_record(gdef),
        "stable_rb_minus_one": interval_record(rb_stable - one),
        "stable_rb_denominator": interval_record(rb_den),
    }


def diagnostic(box):
    k, t, y = (R17.dyadic_ball(lo, hi) for lo, hi in box)
    v = R17.evaluate(k, t, y)
    gaps = R17.conditional_gap_lowers(v)
    names = ("g", "K", "cp2", "P", "X", "ebar", "W0", "W1", "U0", "U1")
    return {
        "raw_b_minus_a": interval_record(v["b-a"]),
        "raw_rb_minus_one": interval_record(v["rb-1"]),
        "conditional_inputs": {name: interval_record(v[name]) for name in names},
        "conditional_gaps": None if gaps is None else [interval_record(gap) for gap in gaps],
        "stable": stable_diagnostics(box),
    }


def replay():
    den = R17.DEN
    q = den // 64
    tup = den - (1 << (R17.BITS - 17))
    root = ((q, den - q), (den - q, tup), (0, q))
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
    max_boxes = 1_000_000
    while stack and counts["visited"] < max_boxes:
        box = stack.pop()
        counts["visited"] += 1
        try:
            k, t, y = (R17.dyadic_ball(lo, hi) for lo, hi in box)
            v = R17.evaluate(k, t, y)
            if R17.upper_nonpositive(v["b-a"]):
                counts["discard_g"] += 1
                continue
            if R17.upper_nonpositive(v["rb-1"]):
                counts["discard_r"] += 1
                continue
            gaps = R17.conditional_gap_lowers(v)
            if gaps is not None and all(gap > 0 for gap in gaps):
                counts["proved"] += 1
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
        stack.append(tuple(right))
        stack.append(tuple(left))
        counts["split"] += 1

    records = []
    for index, box in enumerate(stack):
        records.append({
            "stack_index": index,
            "box_dyadic_numerators": box,
            "endpoint_bits": R17.BITS,
            "width_numerators": [hi - lo for lo, hi in box],
            "diagnostic": diagnostic(box),
        })
    leaves = counts["discard_g"] + counts["discard_r"] + counts["proved"] + counts["unresolved"]
    return {
        "status": "FINITE_COMPUTATIONAL_RESULT",
        "purpose": "freeze exact IHL residual stack without increasing the original cap",
        "root_dyadic_numerators": root,
        "endpoint_bits": R17.BITS,
        "hard_cap": max_boxes,
        "counts": counts,
        "classified_leaves": leaves,
        "splits_plus_one": counts["split"] + 1,
        "stack_remaining": len(stack),
        "residual_stack": records,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rendered = json.dumps(replay(), indent=2)
    if args.output is None:
        print(rendered)
    else:
        args.output.write_text(rendered + "\n", encoding="utf-8")
        print(json.dumps({"wrote": str(args.output)}))
