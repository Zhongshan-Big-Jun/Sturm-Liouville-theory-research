#!/usr/bin/env python3
"""Rigorous Arb cover driver for selected R17 boundary collars.

The mathematical evaluator and conditional contractor are imported from the
frozen R17 checker.  Each run prints an exact-dyadic covering audit.  A pass
is only a finite result on the requested closed box.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve()
PROJECT = HERE.parents[4]
UPSTREAM = PROJECT / "runs/R-20260812T165103Z-mpo3a-cont4/routes/r17_min_n2_inner_box_arb_certificate/exact_checker.py"
SPEC = importlib.util.spec_from_file_location("r17_checker", UPSTREAM)
assert SPEC and SPEC.loader
R17 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(R17)


def run(root: tuple[tuple[int, int], ...], max_boxes: int) -> dict:
    stack = [root]
    use_stable_g = root[0][0] >= R17.DEN - R17.DEN // 64
    counts = {"visited": 0, "discard_g": 0, "discard_r": 0, "proved": 0, "split": 0, "singular": 0, "unresolved": 0}
    min_gaps = [None] * 4
    while stack and counts["visited"] < max_boxes:
        box = stack.pop()
        counts["visited"] += 1
        try:
            k, t, y = (R17.dyadic_ball(lo, hi) for lo, hi in box)
            if use_stable_g:
                # Stable form of sign(b-a)=sign(B-A), including k=1.  Write
                # h=pi(1-k)/(2(1+k)), A=k*a=tan(k Ap)/tan(Ap), and
                # B=k*b=tan(y h)/tan((1+k-k y)h).  The sinc form removes
                # both 0/0 limits at h=0.
                one, two, pi = R17.arb(1), R17.arb(2), R17.arb.pi()
                Ap = pi * t / two
                h = pi * (one - k) / (two * (one + k))
                vc = one + k - k * y
                A = k * (k * Ap).sinc() * Ap.cos() / (Ap.sinc() * (k * Ap).cos())
                B = y * (y * h).sinc() * (vc * h).cos() / (vc * (vc * h).sinc() * (y * h).cos())
                if R17.upper_nonpositive(B - A):
                    counts["discard_g"] += 1
                    continue
            v = R17.evaluate(k, t, y)
            if (not use_stable_g) and R17.upper_nonpositive(v["b-a"]):
                counts["discard_g"] += 1
                continue
            if R17.upper_nonpositive(v["rb-1"]):
                counts["discard_r"] += 1
                continue
            gaps = R17.conditional_gap_lowers(v)
            if gaps is not None and all(gap > 0 for gap in gaps):
                counts["proved"] += 1
                for i, gap in enumerate(gaps):
                    val = float(gap.lower())
                    if min_gaps[i] is None or val < min_gaps[i]:
                        min_gaps[i] = val
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
    leaves = counts["discard_g"] + counts["discard_r"] + counts["proved"] + counts["unresolved"]
    return {
        "root_dyadic": root,
        "bits": R17.BITS,
        "complete": not stack and counts["unresolved"] == 0,
        "counts": counts,
        "leaf_identity": [leaves, counts["split"] + 1],
        "stack_remaining": len(stack),
        "min_gaps": min_gaps,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("face", choices=("k0", "k1", "t0", "t1", "y0", "y1"))
    parser.add_argument("--width", type=int, default=64, help="collar denominator")
    parser.add_argument("--inner", type=int, default=64, help="other-coordinate collar denominator")
    parser.add_argument("--max-boxes", type=int, default=2_000_000)
    args = parser.parse_args()
    den = R17.DEN
    w = den // args.width
    c = den // args.inner
    root = [[c, den - c] for _ in range(3)]
    axis = "kty".index(args.face[0])
    root[axis] = [0, w] if args.face[1] == "0" else [den - w, den]
    result = run(tuple(tuple(x) for x in root), args.max_boxes)
    print(json.dumps(result, indent=2))
    return 0 if result["complete"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
