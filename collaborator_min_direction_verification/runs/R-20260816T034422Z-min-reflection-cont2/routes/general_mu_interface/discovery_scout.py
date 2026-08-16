#!/usr/bin/env python3
"""Discovery-only scan of the exact common-angle interface formulas.

This file is not a proof artifact.  It searches for failure of simple
pointwise sufficient bounds and records the smallest margins encountered.
"""

from __future__ import annotations

import math


def cell(mu: float, theta: float) -> dict[str, float]:
    s, S = math.sin(theta), math.sin(mu * theta)
    c, C = math.cos(theta), math.cos(mu * theta)
    F = S / s
    U = 1 / s + mu / S
    Q = s + mu * S
    x = (F * c - mu * C) / (F + mu)
    rho = (mu * F + 1) / (F + mu)
    p = Q / U
    e = (mu * mu - 1) * F * (c + C) / (F + mu) ** 2
    kappa = 1 - x * x - p
    return dict(F=F, U=U, x=x, rho=rho, p=p, e=e, k=kappa)


def main() -> None:
    worst_simple = (float("inf"), None)
    worst_amgm = (float("inf"), None)
    worst_phi = (float("inf"), None)
    retained = 0
    by_mu = {}
    for mu in [1.01, 1.03, 1.1, 1.25, 1.5, 2, 3, 5, 10, 30, 100]:
        edge = math.pi / (mu + 1)
        end = math.pi / mu
        for ia in range(1, 80):
            alpha = edge * ia / 80
            cp = cell(mu, alpha)
            for ib in range(1, 80):
                beta = edge + (end - edge) * ib / 80
                cm = cell(mu, beta)
                lam = cp["U"] / cm["U"]
                d = cp["rho"] - cm["rho"]
                eta = -cm["e"]
                rb = lam * cp["e"] / (eta + d * cm["x"])
                if rb <= 1:
                    continue
                retained += 1
                for ir in range(1, 80):
                    r = 1 + (rb - 1) * ir / 80
                    w = (cp["e"] - r * eta / lam) / d
                    u = cp["x"] + w
                    A0 = 1 - cp["x"] * u
                    delta = r * r - 1
                    simple = A0 - delta * w * u**3
                    amgm = 4 * lam * lam * cp["p"] * A0 - delta * cm["p"] * u**4
                    Phi = (
                        (lam * lam * w * w + r * r * cm["k"] + cm["p"])
                        * (A0 + delta * cp["p"] * u * u)
                        - delta * cm["p"] * w * u**3
                    )
                    scale = max(1e-300, abs(A0) + abs(delta * w * u**3))
                    item = (mu, alpha, beta, rb, r, simple, Phi)
                    if simple / scale < worst_simple[0]:
                        worst_simple = (simple / scale, item)
                    amgm_scale = max(
                        1e-300,
                        abs(4 * lam * lam * cp["p"] * A0)
                        + abs(delta * cm["p"] * u**4),
                    )
                    if amgm / amgm_scale < worst_amgm[0]:
                        worst_amgm = (amgm / amgm_scale, item + (amgm,))
                    old = by_mu.get(mu, (float("inf"), None))
                    if amgm / amgm_scale < old[0]:
                        by_mu[mu] = (amgm / amgm_scale, item + (amgm,))
                    if Phi < worst_phi[0]:
                        worst_phi = (Phi, item)
    print("retained", retained)
    print("worst_simple_relative", worst_simple)
    print("worst_amgm_relative", worst_amgm)
    print("worst_phi", worst_phi)
    print("worst_amgm_by_mu")
    for key, value in by_mu.items():
        print(key, value)


if __name__ == "__main__":
    main()
