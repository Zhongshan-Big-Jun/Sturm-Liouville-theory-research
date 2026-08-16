"""Rigorous Arb cover for the four open R14 Bernstein coefficients.

This checker proves only the compact common-angle box recorded in
problem_contract.md.  It deliberately does not claim the open boundary
collars.  All boxes and endpoints are exact dyadics and all transcendental
evaluation uses Arb directed ball arithmetic.
"""
from __future__ import annotations

import json
import math

from flint import arb, ctx, __version__ as flint_version

ctx.prec = 128

BITS = 34
DEN = 1 << BITS
COLLAR = DEN // 64
MAX_BOXES = 1_000_000


def dyadic_ball(lo: int, hi: int) -> arb:
    return arb((lo + hi, -BITS - 1), (hi - lo, -BITS - 1))


def sinc_k_diff(k: arb, z: arb) -> arb:
    """Enclose sinc(k z)-sinc(z), for 0<=k<=1 and 0<=z<=pi.

    Its alternating expansion has positive term magnitudes
      (1-k^(2n))*z^(2n)/(2n+1)!.
    Consecutive magnitudes decrease: their ratio is at most pi^2/10<1
    for n=1, and the elementary bound improves with n.  Sixteen signed
    terms give the lower truncation and the seventeenth positive term
    gives the upper truncation.
    """
    k2 = k * k
    z2 = z * z
    terms = []
    kp = k2
    zp = z2
    for n in range(1, 18):
        terms.append((1 - kp) * zp / math.factorial(2 * n + 1))
        kp *= k2
        zp *= z2
    lower = sum(
        ((term if i % 2 == 0 else -term) for i, term in enumerate(terms[:16])),
        arb(0),
    )
    return lower.union(lower + terms[16])


def evaluate(k: arb, t: arb, y: arb) -> dict[str, arb]:
    one, two, four = arb(1), arb(2), arb(4)
    pi = arb.pi()

    # Exact common-angle coordinates.
    Ap = pi * t / two
    zp = k * Ap
    q = Ap * zp.sinc() / zp.cos()
    a = zp.sinc() * Ap.cos() / (zp.cos() * Ap.sinc())

    Am = pi / two + y * (pi / (one + k) - pi / two)
    zm = k * Am
    ss = Am * zm.sinc() / zm.cos()
    b = -zm.sinc() * Am.cos() / (zm.cos() * Am.sinc())

    # A=k*a, B=k*b, Q=k*q, S=k*ss.  These scaled variables remove the
    # k->0 cancellation for the compact calculation.
    k2 = k * k
    Dt = b * (one + k2 * a * b) + k2 * (a + b) * ss * ss
    rb = a * ss * (one - k2 * b * b) / (q * Dt)
    ebar = (one - k2) * (b * b - a * a) / (
        (one - k2 * k2 * b * b) * (one - k2 * a * a)
    )
    g = one - k2 * ebar

    # Positive common-angle factorization of X/k.  sinc_k_diff avoids
    # subtracting nearly equal quantities for a small plus phase.
    sd = sinc_k_diff(k, two * Ap)
    xden = Ap.sin() * zp.cos() * (
        Ap.sinc() * zp.cos() - k2 * zp.sinc() * Ap.cos()
    )
    X = sd / xden

    W0 = (one - k2 * a * a) * (
        a * ss - b * q + k2 * a * b * (q + ss)
    ) / (q * ss * (a + b) * (one - k2 * a))
    W1 = k2 * a * (one - k2 * a * a) * (
        b * b + b + ss * ss + k2 * b * ss * ss
    ) / (q * (one - k2 * a) * Dt)

    U0, U1 = k2 * X + W0, k2 * X + W1
    H0, H1 = X + ebar * W0, X + ebar * W1
    L0, L1 = two * H0 + ebar * U0, two * H1 + ebar * U1
    sr = rb - one
    Delta = rb * rb - one

    cp2 = (a * a + q * q) * (one + k2 * q * q) / (q * q)
    P = (one - k2 * a * a) * (one + k2 * a) / (one - k2 * a)
    K = (one - k2 * a * a) / ((a * a + q * q) * (one + k2 * q * q)) * (
        a * a * (one - k2) / (one - k2 * a) ** 2
        + q * q * b * (one + k2 * a) / (a + b)
    )

    return {
        "b-a": b - a,
        "rb-1": sr,
        "ebar": ebar,
        "g": g,
        "X": X,
        "W0": W0,
        "W1": W1,
        "U0": U0,
        "U1": U1,
        "P": P,
        "cp2": cp2,
        "K": K,
    }


def lower_positive(x: arb) -> bool:
    try:
        return x.lower() > 0
    except Exception:
        return False


def upper_nonpositive(x: arb) -> bool:
    try:
        return x.upper() <= 0
    except Exception:
        return False


def conditional_gap_lowers(v: dict[str, arb]) -> tuple[arb, ...] | None:
    """Lower bounds for g*K*cp^4-P*N_i on the physical subset.

    On that subset R14 gives ebar>=0, rb>=1 and X,W_i,U_i,H_i,L_i>0.
    Intersecting the ambient balls with these signs is a valid interval
    contractor; it is not an assumption about nonphysical points.
    """
    if not all(lower_positive(v[n]) for n in ("g", "K", "cp2", "P", "X")):
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
    base = v["g"].lower() * v["K"].lower() * v["cp2"].lower() ** 2
    return tuple(base - v["P"].upper() * n for n in nups)


def run_cover() -> dict:
    root = ((COLLAR, DEN - COLLAR),) * 3
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

    while stack and counts["visited"] < MAX_BOXES:
        box = stack.pop()
        counts["visited"] += 1
        try:
            v = evaluate(*(dyadic_ball(lo, hi) for lo, hi in box))
            if upper_nonpositive(v["b-a"]):
                counts["discard_g"] += 1
                continue
            if upper_nonpositive(v["rb-1"]):
                counts["discard_r"] += 1
                continue
            gaps = conditional_gap_lowers(v)
            if gaps is not None and all(gap > 0 for gap in gaps):
                counts["proved"] += 1
                for i, gap in enumerate(gaps):
                    # Record the directed lower endpoint, not the midpoint
                    # of the final Arb ball.  This number is diagnostic only;
                    # the proof test above is the rigorous `gap > 0` test.
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
            continue
        mid = (lo + hi) // 2
        left, right = list(box), list(box)
        left[j], right[j] = (lo, mid), (mid, hi)
        stack.append(tuple(right))
        stack.append(tuple(left))
        counts["split"] += 1

    leaves = counts["discard_g"] + counts["discard_r"] + counts["proved"]
    complete = not stack and counts["unresolved"] == 0
    assert complete
    assert counts["singular"] == 0
    assert leaves == counts["split"] + 1
    assert counts["visited"] == leaves + counts["split"]
    assert all(x is not None and x > 0 for x in min_gaps)

    return {
        "status": "FINITE_COMPUTATIONAL_RESULT",
        "result": "PASS",
        "scope": {
            "coordinates": ["k", "t", "y"],
            "box": ["1/64", "63/64"],
            "retained_subset": ["g<1", "rB>1"],
            "coefficients": ["B1", "B2", "B3", "B4"],
            "open": "all omitted boundary collars",
        },
        "arithmetic": {
            "library": "python-flint",
            "version": flint_version,
            "arb_precision_bits": ctx.prec,
            "partition_endpoint_bits": BITS,
        },
        "counts": counts,
        "leaf_identity": {
            "leaves": leaves,
            "splits_plus_one": counts["split"] + 1,
        },
        "stack_remaining": len(stack),
        "min_certified_gap_lower_float_by_index": min_gaps,
    }


if __name__ == "__main__":
    print(json.dumps(run_cover(), indent=2))
