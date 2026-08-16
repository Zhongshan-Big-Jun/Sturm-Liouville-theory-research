#!/usr/bin/env python3
"""Discovery-only scan of the R14 coefficient certificate on the full cube."""

from __future__ import annotations

import argparse
import math
import random


def sinc(x: float) -> float:
    return 1.0 if x == 0 else math.sin(x) / x


def evaluate(k: float, t: float, y: float) -> dict[str, float] | None:
    Ap = math.pi * t / 2
    zp = k * Ap
    q = Ap * sinc(zp) / math.cos(zp)
    a = sinc(zp) * math.cos(Ap) / (math.cos(zp) * sinc(Ap))
    Am = math.pi / 2 + y * (math.pi / (1 + k) - math.pi / 2)
    zm = k * Am
    ss = Am * sinc(zm) / math.cos(zm)
    b = -sinc(zm) * math.cos(Am) / (math.cos(zm) * sinc(Am))
    k2 = k * k
    Dt = b * (1 + k2 * a * b) + k2 * (a + b) * ss * ss
    rb = a * ss * (1 - k2 * b * b) / (q * Dt)
    ebar = (1 - k2) * (b * b - a * a) / ((1 - k2 * k2 * b * b) * (1 - k2 * a * a))
    g = 1 - k2 * ebar
    # Direct formula for Xbar; stable enough away from machine coalescence.
    sd = sinc(2 * k * Ap) - sinc(2 * Ap)
    xden = math.sin(Ap) * math.cos(zp) * (sinc(Ap) * math.cos(zp) - k2 * sinc(zp) * math.cos(Ap))
    if abs(q * ss * (a + b) * (1 - k2 * a) * Dt * xden) < 1e-280:
        return None
    X = sd / xden
    W0 = (1 - k2 * a * a) * (a * ss - b * q + k2 * a * b * (q + ss)) / (q * ss * (a + b) * (1 - k2 * a))
    W1 = k2 * a * (1 - k2 * a * a) * (b * b + b + ss * ss + k2 * b * ss * ss) / (q * (1 - k2 * a) * Dt)
    U0, U1 = k2 * X + W0, k2 * X + W1
    H0, H1 = X + ebar * W0, X + ebar * W1
    L0, L1 = 2 * H0 + ebar * U0, 2 * H1 + ebar * U1
    sr, Delta = rb - 1, rb * rb - 1
    cp2 = (a * a + q * q) * (1 + k2 * q * q) / (q * q)
    P = (1 - k2 * a * a) * (1 + k2 * a) / (1 - k2 * a)
    K = (1 - k2 * a * a) / ((a * a + q * q) * (1 + k2 * q * q)) * (
        a * a * (1 - k2) / (1 - k2 * a) ** 2 + q * q * b * (1 + k2 * a) / (a + b)
    )
    if not (b > a and rb > 1 and min(g, X, W0, W1, U0, U1, H0, H1, L0, L1, K, P, cp2) > 0):
        return None
    Ns = (
        sr * U0 * L0 / 2,
        (2 * sr * (U1 * L0 + U0 * L1) + Delta * U0 * L0) / 6,
        (2 * sr * U1 * L1 + Delta * (U1 * L0 + U0 * L1)) / 4,
        Delta * U1 * L1,
    )
    base = g * K * cp2 * cp2
    gaps = tuple(base - P * n for n in Ns)
    return {"k": k, "t": t, "y": y, "rb": rb, "g": g, "base": base, **{f"G{i+1}": gaps[i] for i in range(4)}}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--draws", type=int, default=1_000_000)
    parser.add_argument("--seed", type=int, default=20260816)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    best = [None] * 4
    accepted = 0
    negative = [0] * 4
    for _ in range(args.draws):
        # Logistic coordinates heavily sample all six open faces.
        vals = [1 / (1 + math.exp(-rng.uniform(-18, 18))) for _ in range(3)]
        out = evaluate(*vals)
        if out is None:
            continue
        accepted += 1
        for i in range(4):
            key = f"G{i+1}"
            if out[key] <= 0:
                negative[i] += 1
            score = out[key] / out["base"]
            if best[i] is None or score < best[i][0]:
                best[i] = (score, out)
    print({"draws": args.draws, "accepted": accepted, "negative": negative, "best": best})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
