"""Deterministic longer local min-word scout; NUMERICAL_EVIDENCE only."""

from __future__ import annotations

import json
import math

import numpy as np

import local_triplet_scout as local


NS = (3, 4, 5, 6)
MUS = (1.05, 1.5, 3.0)
CONTRASTS = (1.01, 2.0, 100.0)
ENERGIES = (0.1, 1.0, 10.0)
P_VALUES = (-2.0, 0.0, 2.0)


def evaluate(n: int, mu: float, contrast: float, energy: float,
             initial_p: float) -> dict | None:
    state = np.asarray((1.0, initial_p, 1.0 / mu,
                        -math.sqrt(initial_p * initial_p + energy)))
    states = [state]
    phases = []
    epsilon = 1.0
    for edge in range(2 * n - 1):
        rho = 1.0 if edge % 2 == 0 else contrast
        desired_sign = 1.0 if edge % 2 == 0 else -1.0
        event = local.next_event(state, rho, mu, epsilon, desired_sign)
        if event is None:
            return None
        phase, state = event
        phases.append(phase)
        states.append(state)
        epsilon = -epsilon

    alpha = []
    for index, event_state in enumerate(states):
        u, p, v, r = event_state
        derivative = 2.0 * u * p - 2.0 * mu * mu * v * r
        jump = (1.0 - contrast) if index % 2 == 0 else (contrast - 1.0)
        value = -2.0 * jump * u**4 / derivative
        if value <= 0.0:
            return None
        alpha.append(value)

    kvals = []
    for index, phase in enumerate(phases):
        rho = 1.0 if index % 2 == 0 else contrast
        u0, u1 = states[index][0], states[index + 1][0]
        kvals.append((math.sin(phase) + mu * math.sin(mu * phase))
                      / (math.sqrt(rho) * u0 * u1))
    if any((value > 0.0) != (index % 2 == 0)
           for index, value in enumerate(kvals)):
        return None
    threshold = math.pi / (mu + 1.0)
    if any((phase < threshold) != (index % 2 == 0)
           for index, phase in enumerate(phases)):
        return None
    residual = max(abs(st[1] ** 2 - st[3] ** 2 + energy)
                   for st in states) / max(1.0, energy)
    if residual > 1.0e-9:
        return None

    a = np.asarray(alpha)
    # P consists of the n disjoint positive-edge two-by-two blocks.
    pinv = np.zeros((2 * n, 2 * n))
    for block in range(n):
        left, right = 2 * block, 2 * block + 1
        compliance = 1.0 / kvals[2 * block]
        determinant = a[left] * a[right] + compliance * (a[left] + a[right])
        pinv[left:left + 2, left:left + 2] = np.asarray((
            ((a[right] + compliance) / determinant, compliance / determinant),
            (compliance / determinant, (a[left] + compliance) / determinant),
        ))
    cmat = np.zeros((n - 1, 2 * n))
    for j in range(n - 1):
        cmat[j, 2 * j + 1] = -1.0
        cmat[j, 2 * j + 2] = 1.0
    weights = np.asarray(tuple(abs(kvals[2 * j + 1]) for j in range(n - 1)))
    hmat = cmat @ pinv @ cmat.T - np.diag(weights)
    gammas = np.asarray(tuple(
        (2.0 * st[0] * st[1] - 2.0 * mu * mu * st[2] * st[3])
        / (2.0 * st[0] ** 2) for st in states
    ))
    zvec = np.asarray(tuple(
        (gammas[2 * j + 2] - gammas[2 * j + 1]) / weights[j] ** 1.5
        for j in range(n - 1)
    ))
    hz = hmat @ zvec
    return {
        "n": n, "mu": mu, "R": contrast, "energy": energy,
        "initial_p": initial_p,
        "minimum_H_eigenvalue": float(np.linalg.eigvalsh(hmat)[0]),
        "minimum_z": float(zvec.min()), "minimum_Hz": float(hz.min()),
        "energy_relative_residual": float(residual),
    }


def main() -> None:
    retained = []
    for n in NS:
        for mu in MUS:
            for contrast in CONTRASTS:
                for energy in ENERGIES:
                    for initial_p in P_VALUES:
                        result = evaluate(n, mu, contrast, energy, initial_p)
                        if result is not None:
                            retained.append(result)
    print(json.dumps({
        "status_label": "NUMERICAL_EVIDENCE",
        "grid_size": len(NS) * len(MUS) * len(CONTRASTS) * len(ENERGIES) * len(P_VALUES),
        "retained_local_words": len(retained),
        "nonpositive_H_count": sum(row["minimum_H_eigenvalue"] <= 0.0 for row in retained),
        "nonpositive_z_count": sum(row["minimum_z"] <= 0.0 for row in retained),
        "nonpositive_Hz_count": sum(row["minimum_Hz"] <= 0.0 for row in retained),
        "minimum_H_record": min(retained, key=lambda row: row["minimum_H_eigenvalue"]) if retained else None,
        "minimum_Hz_record": min(retained, key=lambda row: row["minimum_Hz"]) if retained else None,
        "limitation": "local words omit common terminal/index/global initial predicates",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
