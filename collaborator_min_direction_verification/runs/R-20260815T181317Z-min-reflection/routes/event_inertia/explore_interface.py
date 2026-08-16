#!/usr/bin/env python3
"""Discovery-only scan of the exact general-mu one-interface reduction.

This does not certify a universal sign.  It retains the common-angle
relations exactly at floating precision and reports dimensionless margins
that may suggest an analytic inequality.
"""

from __future__ import annotations

import argparse
import math
import random


def endpoint(t: float, T: float, z: float) -> tuple[float, float, float, float]:
    c = (1.0 - t * t) / (1.0 + t * t)
    s = 2.0 * t / (1.0 + t * t)
    C = (1.0 - T * T) / (1.0 + T * T)
    S = 2.0 * T / (1.0 + T * T)
    return (
        (z - c) / s,
        (-z - C) / S,
        (c * z - 1.0) / (s * z),
        (1.0 + C * z) / (S * z),
    )


def sample(mu: float, alpha: float, beta: float, r: float) -> dict[str, float] | None:
    t = math.tan(alpha / 2.0)
    T = math.tan(mu * alpha / 2.0)
    s = math.tan(beta / 2.0)
    S = math.tan(mu * beta / 2.0)
    L = S * t * (1 + s * s) * (1 + T * T) - T * s * (1 + t * t) * (1 + S * S)
    D = (
        2 * T * r * t * (S * S * s * s - 1)
        + T * s * (t * t - 1) * (1 + S * S)
        + S * t * (1 + s * s) * (T * T - 1)
    )
    N = (
        r * T * s * (1 + t * t) * (S * S - 1)
        + r * S * t * (s * s - 1) * (1 + T * T)
        + 2 * S * s * (T * T * t * t - 1)
    )
    if abs(L * D) < 1e-300:
        return None
    a = L / D
    b = -N / (r * L)
    if not (a > 0 and b < 0):
        return None

    xp, yp, xp_r, yp_r = endpoint(t, T, a)
    xn, yn, _, _ = endpoint(s, S, b)
    if max(abs(xn - xp_r / r), abs(yn - yp_r / r)) > 1e-7 * (1 + abs(xn) + abs(yn)):
        return None

    dp = mu * T * T * t + T * t * t + T + mu * t
    np = mu * T * T * t - T * t * t + T - mu * t
    dn = mu * S * S * s + S * s * s + S + mu * s
    nn = mu * S * S * s - S * s * s + S - mu * s
    qpos = 2 * (t * (1 + T * T) + mu * T * (1 + t * t)) / ((1 + t * t) * (1 + T * T))
    qneg = 2 * (s * (1 + S * S) + mu * S * (1 + s * s)) / ((1 + s * s) * (1 + S * S))
    g = (dp * a - np) / (2 * T * t)
    h = (dp - np * a) / (2 * T * t * a)
    B = -b
    G = (nn + dn * B) / (2 * S * s)
    J = (dn + nn * B) / (2 * S * s * B)
    if min(g, h, G, J, qpos, qneg) <= 0:
        return None

    delta = r * r - 1.0
    dcell = delta * a * qpos + r * G + a * a * g
    nleft = r * r * a * B * (G + J) * (delta * qpos + a * g) - delta * qneg * dcell

    def normalized(theta: float) -> tuple[float, float, float, float, float, float, float]:
        st = math.sin(theta)
        sm = math.sin(mu * theta)
        ct = math.cos(theta)
        cm = math.cos(mu * theta)
        F = sm / st
        U = (F + mu) / (F * st)
        Q = st + mu * sm
        x = (F * ct - mu * cm) / (F + mu)
        rho = (mu * F + 1) / (F + mu)
        p = Q / U
        e = (mu * mu - 1) * F * (ct + cm) / ((F + mu) ** 2)
        k = mu * F * (ct + cm) ** 2 / ((F + mu) ** 2)
        return F, U, x, rho, p, e, k

    Fp, Up, xplus, rhop, pplus, eplus, kplus = normalized(alpha)
    Fm, Um, xminus, rhom, pminus, eminus, kminus = normalized(beta)
    lam = Up / Um
    dd = rhop - rhom
    eta = -eminus
    w = (eplus - (r / lam) * eta) / dd
    u = xplus + w
    A0 = 1 - u * xplus
    phi_lhs = (lam * lam * w * w + r * r * kminus + pminus) * (A0 + delta * pplus * u * u)
    phi_rhs = delta * pminus * w * u**3
    phi = phi_lhs - phi_rhs
    if max(abs(a - 1 / u), abs(B - (lam * w / r - xminus))) > 2e-6 * (1 + abs(a) + abs(B)):
        return None
    return {
        "mu": mu,
        "alpha": alpha,
        "beta": beta,
        "r": r,
        "a": a,
        "B": B,
        "nleft": nleft,
        "phi": phi,
        "ratio": phi_lhs / phi_rhs if phi_rhs > 0 else math.inf,
        "simple_ratio": (lam * lam * w * pplus) / (pminus * u),
        "w": w,
        "u": u,
        "A0": A0,
        "branch_B": lam * w / r - xminus,
        "r_cap_ratio": r * eta / (lam * eplus),
        "Fplus": Fp,
        "Fminus": Fm,
        "xplus": xplus,
        "xminus": xminus,
        "pplus": pplus,
        "pminus": pminus,
        "kminus": kminus,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--draws", type=int, default=500_000)
    parser.add_argument("--seed", type=int, default=20260816)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    best: dict[str, float] | None = None
    accepted = 0
    negatives = 0
    for _ in range(args.draws):
        mu = 1 + 10 ** rng.uniform(-4, 1.7)
        split = math.pi / (mu + 1)
        top = math.pi / mu
        # Bias to every phase boundary by a logit chart.
        ua = 1 / (1 + math.exp(-rng.uniform(-10, 10)))
        ub = 1 / (1 + math.exp(-rng.uniform(-10, 10)))
        alpha = split * ua
        beta = split + (top - split) * ub
        r = 1 + 10 ** rng.uniform(-5, 5)
        out = sample(mu, alpha, beta, r)
        if out is None:
            continue
        accepted += 1
        if out["phi"] <= 0 or out["nleft"] <= 0:
            negatives += 1
        if best is None or out["ratio"] < best["ratio"]:
            best = out
    print({"draws": args.draws, "accepted": accepted, "negatives": negatives, "best": best})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
