"""Contractor-directed finite cover of the frozen C2-N IHL residual forest."""
from __future__ import annotations

import argparse
import importlib.util
import json
import math
import sys
from fractions import Fraction
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


def stable_probe(box):
    k, t, y = (R17.dyadic_ball(lo, hi) for lo, hi in box)
    one, two, pi = R17.arb(1), R17.arb(2), R17.arb.pi()
    c = pi / two
    h = c * (one - t)
    eta = pi * y * (one - k) / (two * (one + k))
    x, e = h.tan(), eta.tan()
    # Correlation-preserving original products; both arguments stay in
    # (0,pi/2) throughout IHL.
    p = (c * k * t).tan()
    s = (c * k * (one + y * (one - k) / (one + k))).tan()
    gdef = s * e - p * x
    denominator = e * (one + s * s) + x * p * s * (one + e * e)
    rdef = x * (one - s * s * e * e) - denominator
    return {"gdef": gdef, "rdef": rdef, "denominator": denominator}


def diameter(x) -> float:
    try:
        return max(0.0, float(x.upper() - x.lower()))
    except Exception:
        return math.inf


def order_empty(box):
    """Exact monotone box form of k*t>(1-k)*(1-y*k/(1+k))."""
    den = R17.DEN
    k0 = Fraction(box[0][0], den)
    t0 = Fraction(box[1][0], den)
    y0 = Fraction(box[2][0], den)
    return k0 * t0 > (1 - k0) * (1 - y0 * k0 / (1 + k0))


def stable_class(box, probe):
    if order_empty(box):
        return "discard_r_order"
    # The denominator is strictly positive analytically on IHL:
    # x,p,s>0 and e>=0, so x*p*s*(1+e^2)>0.
    if R17.upper_nonpositive(probe["gdef"]):
        return "discard_g_stable"
    if R17.upper_nonpositive(probe["rdef"]):
        return "discard_r_stable"
    return None


def classify(box):
    probe = stable_probe(box)
    outcome = stable_class(box, probe)
    if outcome is not None:
        return outcome, probe, None
    try:
        v = R17.evaluate(*(R17.dyadic_ball(lo, hi) for lo, hi in box))
        if R17.upper_nonpositive(v["b-a"]):
            return "discard_g_raw", probe, None
        if R17.upper_nonpositive(v["rb-1"]):
            return "discard_r_raw", probe, None
        gaps = R17.conditional_gap_lowers(v)
        if gaps is not None and all(gap > 0 for gap in gaps):
            return "proved", probe, gaps
        return "unresolved", probe, gaps
    except Exception as exc:
        return "raw_exception", probe, str(exc)


def children(box, axis):
    lo, hi = box[axis]
    mid = (lo + hi) // 2
    left, right = list(box), list(box)
    left[axis], right[axis] = (lo, mid), (mid, hi)
    return tuple(left), tuple(right)


def choose_axis(box, parent_probe):
    widths = [hi - lo for lo, hi in box]
    pg = max(diameter(parent_probe["gdef"]), 1e-300)
    pr = max(diameter(parent_probe["rdef"]), 1e-300)
    candidates = []
    for axis, width in enumerate(widths):
        if width <= 1:
            continue
        kids = children(box, axis)
        probes = [stable_probe(kid) for kid in kids]
        quick = [stable_class(kid, p) for kid, p in zip(kids, probes)]
        immediate = sum(q in ("discard_r_order", "discard_g_stable", "discard_r_stable") for q in quick)
        ambiguity = 0.0
        for q, p in zip(quick, probes):
            if q is None:
                ambiguity += diameter(p["gdef"]) / pg + diameter(p["rdef"]) / pr
        # max: more immediate stable leaves, smaller normalized ambiguity,
        # then larger dyadic width, then earlier axis.
        score = (immediate, -ambiguity, width, -axis)
        candidates.append((score, axis, kids))
    if not candidates:
        return None, None
    _, axis, kids = max(candidates, key=lambda item: item[0])
    return axis, kids


def ball_record(x):
    return {"lower": str(x.lower()), "upper": str(x.upper()), "ball": str(x)}


def residual_record(box, origin, outcome, probe, extra):
    rec = {
        "origin_stack_index": origin,
        "box_dyadic_numerators": box,
        "width_numerators": [hi - lo for lo, hi in box],
        "endpoint_bits": R17.BITS,
        "outcome": outcome,
        "stable_g_defect": ball_record(probe["gdef"]),
        "stable_r_defect_numerator": ball_record(probe["rdef"]),
        "stable_r_denominator": ball_record(probe["denominator"]),
    }
    if isinstance(extra, tuple):
        rec["conditional_gaps"] = [ball_record(g) for g in extra]
    elif extra is not None:
        rec["extra"] = extra
    return rec


def run(input_path: Path, max_visits: int):
    frozen = json.loads(input_path.read_text(encoding="utf-8"))
    assert frozen["stack_remaining"] == 21
    roots = []
    for rec in frozen["residual_stack"]:
        box = tuple(tuple(int(z) for z in pair) for pair in rec["box_dyadic_numerators"])
        roots.append((box, int(rec["stack_index"])))
    stack = roots.copy()
    counts = {
        "visited": 0,
        "discard_g_stable": 0,
        "discard_r_stable": 0,
        "discard_r_order": 0,
        "discard_g_raw": 0,
        "discard_r_raw": 0,
        "proved": 0,
        "split": 0,
        "raw_exception": 0,
        "atomic_unresolved": 0,
    }
    min_gaps = [None] * 4
    atomic = []
    while stack and counts["visited"] < max_visits:
        box, origin = stack.pop()
        counts["visited"] += 1
        outcome, probe, extra = classify(box)
        if outcome in counts and outcome != "raw_exception":
            counts[outcome] += 1
            if outcome == "proved":
                for i, gap in enumerate(extra):
                    value = float(gap.lower())
                    if min_gaps[i] is None or value < min_gaps[i]:
                        min_gaps[i] = value
            continue
        if outcome == "raw_exception":
            counts[outcome] += 1
        axis, kids = choose_axis(box, probe)
        if axis is None:
            counts["atomic_unresolved"] += 1
            atomic.append(residual_record(box, origin, outcome, probe, extra))
            continue
        left, right = kids
        stack.append((right, origin))
        stack.append((left, origin))
        counts["split"] += 1

    classified = sum(counts[name] for name in (
        "discard_g_stable", "discard_r_stable", "discard_r_order", "discard_g_raw", "discard_r_raw", "proved", "atomic_unresolved"
    ))
    residual = []
    for box, origin in stack[:100]:
        outcome, probe, extra = classify(box)
        residual.append(residual_record(box, origin, outcome, probe, extra))
    return {
        "status": "FINITE_COMPUTATIONAL_RESULT",
        "input": str(input_path),
        "initial_roots": len(roots),
        "endpoint_bits": R17.BITS,
        "hard_cap_local_visits": max_visits,
        "complete": not stack and not atomic,
        "counts": counts,
        "classified_leaves": classified,
        "forest_identity": {
            "classified_plus_stack": classified + len(stack),
            "splits_plus_initial_roots": counts["split"] + len(roots),
        },
        "stack_remaining": len(stack),
        "serialized_stack_prefix_count": len(residual),
        "stack_prefix": residual,
        "atomic_residuals": atomic[:100],
        "min_certified_gap_lower_float_by_index": min_gaps,
        "proof_note": "Floating scores choose splits only; all leaf predicates are directed Arb inequalities.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--max-visits", type=int, default=1_000_000)
    args = parser.parse_args()
    rendered = json.dumps(run(args.input, args.max_visits), indent=2)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
        print(json.dumps({"wrote": str(args.output)}))
    else:
        print(rendered)
