"""Rigorous Arb cover for the full common-angle t=0 quarter ratios.

This checker never relaxes the relation between the negative phase, b, and
sigma.  The high-k chart uses B=k*b and T=tan(v*h), which is regular at
k=1.  Finite covers remain conditional finite results until every endpoint
chart is included.
"""

from __future__ import annotations

import argparse
import json
from typing import Callable

from flint import arb, ctx, __version__ as flint_version


ctx.prec = 160
BITS = 36
DEN = 1 << BITS
TARGET = arb(249999) / 1000000  # 1/4 - 10^-6, an exact rational target.


def ball(lo: int, hi: int) -> arb:
    return arb((lo + hi, -BITS - 1), (hi - lo, -BITS - 1))


def upper(x: arb):
    return x.upper()


def high_eval(k: arb, y: arb) -> tuple[arb, tuple[arb, arb, arb]]:
    one, two = arb(1), arb(2)
    pi = arb.pi()
    h = pi * (one - k) / (two * (one + k))
    v = one + k - k * y
    yh, vh = y * h, v * h

    # B=tan(yh)/tan(vh), written with removable h=0 factors.
    B = y * yh.sinc() * vh.cos() / (v * vh.sinc() * yh.cos())
    T = vh * vh.sinc() / vh.cos()

    Q = (B * B - k * k) * (one - B * B)
    Dt = B * (one + k * B) * T * T + k + B
    Ft = (B * B + k * B) * T * T + one + k * B
    common = T * T * Q
    r2 = common * (one + k * B) ** 2 / (two * (k + B) ** 2 * Dt**2)
    r3 = 3 * common * (one + k * B) * Ft / (two * (k + B) * Dt**3)
    r4 = 3 * common * Ft**2 / Dt**4
    return B - k, (r2, r3, r4)


def low_eval(k: arb, y: arb) -> tuple[arb, tuple[arb, arb, arb]]:
    """Original (b,sigma) chart, regular at k=0 away from y=1."""
    one, two = arb(1), arb(2)
    pi = arb.pi()
    theta = pi / two + y * (pi / (one + k) - pi / two)
    kt = k * theta
    sigma = theta * kt.sinc() / kt.cos()
    b = -kt.sinc() * theta.cos() / (kt.cos() * theta.sinc())
    kk = k * k
    A = (b * b - one) * (one - kk * b * b)
    D = b * (one + kk * b) + kk * (one + b) * sigma * sigma
    E = b * b + b + sigma * sigma + kk * b * sigma * sigma
    w0 = (one + kk * b) / (one + b)
    w1 = kk * E / D
    common = sigma * sigma * A / (D * D)
    r2 = common * w0 * w0 / two
    r3 = 3 * common * w0 * w1 / two
    r4 = 3 * common * w1 * w1
    return b - one, (r2, r3, r4)


def corner_eval(r: arb, p: arb, kind: str) -> tuple[arb, tuple[arb, arb, arb]]:
    """Projective low-k/y=1 chart, regular at the exact corner.

    kind A: w=1-y=r and k=r*p (w>=k).
    kind B: k=r and w=r*p (k>=w).
    """
    one, two = arb(1), arb(2)
    pi = arb.pi()
    if kind == "A":
        Phi = pi * (one + 2 * p - r * p) / (2 * (one + r * p))
        kbar = p
    else:
        Phi = pi * (2 + p - p * r) / (2 * (one + r))
        kbar = one
    angle = r * Phi
    X = Phi * angle.sinc() / angle.cos()  # tan(angle)/r
    theta = pi - angle
    ktheta = r * kbar * theta
    S = theta * ktheta.sinc() / ktheta.cos()  # sigma
    M = X + r * kbar * kbar * S * (one + r * S * X + r * r * X * X)
    N = S + r * X + r * r * S * X * X + r**3 * kbar * kbar * S * S * X
    Qbar = X * X - kbar * kbar * S * S
    z0sq = r * r * (S - r * X) * Qbar * (X + r * kbar * kbar * S) ** 2 / ((S + r * X) * M**2)
    z0z1 = r * r * kbar * kbar * (S - r * X) * Qbar * (X + r * kbar * kbar * S) * N / M**3
    z1sq = r * r * kbar**4 * (S - r * X) * (S + r * X) * Qbar * N**2 / M**4
    order = S - r * X
    return order, (z0sq / two, 3 * z0z1 / two, 3 * z1sq)


def run_high(max_boxes: int, root=None, chart_name="high_k_B_T", domain=None) -> dict:
    if root is None:
        root = ((DEN // 2, DEN), (0, DEN))
    if domain is None:
        domain = {"k": ["1/2", "1"], "y": ["0", "1"], "retained": "B>k"}
    stack = [root]
    counts = {"visited": 0, "discard_nonphysical": 0, "proved": 0, "split": 0, "unresolved": 0, "singular": 0}
    maxima = [None, None, None]
    while stack and counts["visited"] < max_boxes:
        box2 = stack.pop()
        counts["visited"] += 1
        try:
            order, ratios = high_eval(*(ball(lo, hi) for lo, hi in box2))
            if upper(order) <= 0:
                counts["discard_nonphysical"] += 1
                continue
            if all(upper(r) < TARGET for r in ratios):
                counts["proved"] += 1
                for i, ratio in enumerate(ratios):
                    value = float(upper(ratio))
                    if maxima[i] is None or value > maxima[i]:
                        maxima[i] = value
                continue
        except Exception:
            counts["singular"] += 1

        widths = [hi - lo for lo, hi in box2]
        j = max(range(2), key=lambda i: widths[i])
        lo, hi = box2[j]
        if hi - lo <= 1:
            counts["unresolved"] += 1
            continue
        mid = (lo + hi) // 2
        left, right = list(box2), list(box2)
        left[j], right[j] = (lo, mid), (mid, hi)
        stack.extend((tuple(right), tuple(left)))
        counts["split"] += 1

    leaves = counts["discard_nonphysical"] + counts["proved"] + counts["unresolved"]
    complete = not stack and counts["unresolved"] == 0 and counts["singular"] == 0
    if complete:
        assert leaves == counts["split"] + 1
        assert counts["visited"] == leaves + counts["split"]
    return {
        "status": "FINITE_COMPUTATIONAL_RESULT",
        "chart": chart_name,
        "domain": domain,
        "complete": complete,
        "counts": counts,
        "leaf_identity": [leaves, counts["split"] + 1],
        "stack_remaining": len(stack),
        "max_certified_upper_by_ratio": maxima,
        "precision_bits": ctx.prec,
        "partition_bits": BITS,
        "python_flint": flint_version,
    }


def run_low(max_boxes: int) -> dict:
    root = ((0, DEN // 2), (0, DEN - DEN // 64))
    stack = [root]
    counts = {"visited": 0, "discard_nonphysical": 0, "proved": 0, "split": 0, "unresolved": 0, "singular": 0}
    maxima = [None, None, None]
    while stack and counts["visited"] < max_boxes:
        box2 = stack.pop()
        counts["visited"] += 1
        try:
            order, ratios = low_eval(*(ball(lo, hi) for lo, hi in box2))
            if upper(order) <= 0:
                counts["discard_nonphysical"] += 1
                continue
            if all(upper(r) < TARGET for r in ratios):
                counts["proved"] += 1
                for i, ratio in enumerate(ratios):
                    value = float(upper(ratio))
                    if maxima[i] is None or value > maxima[i]:
                        maxima[i] = value
                continue
        except Exception:
            counts["singular"] += 1
        widths = [hi - lo for lo, hi in box2]
        j = max(range(2), key=lambda i: widths[i])
        lo, hi = box2[j]
        if hi - lo <= 1:
            counts["unresolved"] += 1
            continue
        mid = (lo + hi) // 2
        left, right = list(box2), list(box2)
        left[j], right[j] = (lo, mid), (mid, hi)
        stack.extend((tuple(right), tuple(left)))
        counts["split"] += 1
    leaves = counts["discard_nonphysical"] + counts["proved"] + counts["unresolved"]
    complete = not stack and counts["unresolved"] == 0 and counts["singular"] == 0
    if complete:
        assert leaves == counts["split"] + 1
        assert counts["visited"] == leaves + counts["split"]
    return {
        "status": "FINITE_COMPUTATIONAL_RESULT",
        "chart": "low_k_b_sigma",
        "domain": {"k": ["0", "1/2"], "y": ["0", "63/64"], "retained": "b>1"},
        "complete": complete,
        "counts": counts,
        "leaf_identity": [leaves, counts["split"] + 1],
        "stack_remaining": len(stack),
        "max_certified_upper_by_ratio": maxima,
        "precision_bits": ctx.prec,
        "partition_bits": BITS,
        "python_flint": flint_version,
    }


def run_corner(max_boxes: int, kind: str) -> dict:
    root = ((0, DEN // 64), (0, DEN))
    stack = [root]
    counts = {"visited": 0, "discard_nonphysical": 0, "proved": 0, "split": 0, "unresolved": 0, "singular": 0}
    maxima = [None, None, None]
    while stack and counts["visited"] < max_boxes:
        box2 = stack.pop()
        counts["visited"] += 1
        try:
            order, ratios = corner_eval(*(ball(lo, hi) for lo, hi in box2), kind)
            if upper(order) <= 0:
                counts["discard_nonphysical"] += 1
                continue
            if all(upper(q) < TARGET for q in ratios):
                counts["proved"] += 1
                for i, ratio in enumerate(ratios):
                    value = float(upper(ratio))
                    if maxima[i] is None or value > maxima[i]:
                        maxima[i] = value
                continue
        except Exception:
            counts["singular"] += 1
        widths = [hi - lo for lo, hi in box2]
        j = max(range(2), key=lambda i: widths[i])
        lo, hi = box2[j]
        if hi - lo <= 1:
            counts["unresolved"] += 1
            continue
        mid = (lo + hi) // 2
        left, right = list(box2), list(box2)
        left[j], right[j] = (lo, mid), (mid, hi)
        stack.extend((tuple(right), tuple(left)))
        counts["split"] += 1
    leaves = counts["discard_nonphysical"] + counts["proved"] + counts["unresolved"]
    complete = not stack and counts["unresolved"] == 0 and counts["singular"] == 0
    if complete:
        assert leaves == counts["split"] + 1
        assert counts["visited"] == leaves + counts["split"]
    return {
        "status": "FINITE_COMPUTATIONAL_RESULT",
        "chart": f"low_corner_{kind}",
        "domain": {"r": ["0", "1/64"], "p": ["0", "1"], "retained": "sigma>x"},
        "complete": complete,
        "counts": counts,
        "leaf_identity": [leaves, counts["split"] + 1],
        "stack_remaining": len(stack),
        "max_certified_upper_by_ratio": maxima,
        "precision_bits": ctx.prec,
        "partition_bits": BITS,
        "python_flint": flint_version,
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("chart", choices=("high", "low", "upper_mid", "corner_a", "corner_b", "all"))
    p.add_argument("--max-boxes", type=int, default=1_000_000)
    a = p.parse_args()
    if a.chart == "all":
        results = [
            run_low(a.max_boxes),
            run_high(
                a.max_boxes,
                root=((DEN // 64, DEN // 2), (DEN - DEN // 64, DEN)),
                chart_name="upper_mid_B_T",
                domain={"k": ["1/64", "1/2"], "y": ["63/64", "1"], "retained": "B>k"},
            ),
            run_high(a.max_boxes),
            run_corner(a.max_boxes, "A"),
            run_corner(a.max_boxes, "B"),
        ]
        result = {
            "status": "FINITE_COMPUTATIONAL_RESULT",
            "claim": "the three nonzero full-common-angle t=0 ratios are at most 1/4-10^-6",
            "certified_uniform_margin_from_one_quarter": "1/1000000",
            "complete": all(item["complete"] for item in results),
            "coverage": "low rectangle, upper-middle rectangle, high rectangle, and two projective low-corner charts cover the closed (k,y) square",
            "charts": results,
        }
    elif a.chart == "high":
        result = run_high(a.max_boxes)
    elif a.chart == "upper_mid":
        result = run_high(
            a.max_boxes,
            root=((DEN // 64, DEN // 2), (DEN - DEN // 64, DEN)),
            chart_name="upper_mid_B_T",
            domain={"k": ["1/64", "1/2"], "y": ["63/64", "1"], "retained": "B>k"},
        )
    elif a.chart == "corner_a":
        result = run_corner(a.max_boxes, "A")
    elif a.chart == "corner_b":
        result = run_corner(a.max_boxes, "B")
    else:
        result = run_low(a.max_boxes)
    print(json.dumps(result, indent=2))
    return 0 if result["complete"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
