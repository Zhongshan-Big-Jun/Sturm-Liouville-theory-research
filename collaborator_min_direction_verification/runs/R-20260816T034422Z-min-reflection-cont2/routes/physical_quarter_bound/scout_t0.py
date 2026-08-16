"""Discovery-only scout for the exact common-angle t=0 ratios."""

from __future__ import annotations

import argparse
import math
import random


def ratios(k: float, y: float):
    theta = math.pi / 2 + y * (math.pi / (1 + k) - math.pi / 2)
    if k < 1e-7:
        # Adequate only for discovery; the proof uses exact limiting formulas.
        sigma = theta + (k * theta) ** 2 * theta / 3
        b = -sigma / math.tan(theta)
    else:
        tk = math.tan(k * theta)
        sigma = tk / k
        b = -tk / (k * math.tan(theta))
    if not (1 < b < 1 / k):
        return None
    kk = k * k
    A = (b * b - 1) * (1 - kk * b * b)
    D = b * (1 + kk * b) + kk * (1 + b) * sigma * sigma
    E = b * b + b + sigma * sigma + kk * b * sigma * sigma
    w0 = (1 + kk * b) / (1 + b)
    w1 = kk * E / D
    z0 = sigma * math.sqrt(A) * w0 / D
    z1 = sigma * math.sqrt(A) * w1 / D
    return z0 * z0 / 2, 1.5 * z0 * z1, 3 * z1 * z1, theta, b, sigma


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--draws", type=int, default=1_000_000)
    p.add_argument("--seed", type=int, default=20260816)
    a = p.parse_args()
    rng = random.Random(a.seed)
    best = [(-1.0, None) for _ in range(3)]
    accepted = 0
    for _ in range(a.draws):
        # Include endpoint-heavy and ordinary samples.
        k = 1 / (1 + math.exp(-rng.uniform(-18, 18)))
        y = 1 / (1 + math.exp(-rng.uniform(-18, 18)))
        out = ratios(k, y)
        if out is None:
            continue
        accepted += 1
        for i in range(3):
            if out[i] > best[i][0]:
                best[i] = (out[i], (k, y, *out[3:]))
    print({"draws": a.draws, "accepted": accepted, "best": best})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
