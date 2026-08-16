"""Deterministic local positive-negative-positive relay-triplet scout.

NUMERICAL_EVIDENCE only.  Tests whether the n=2 dual scalar inequality is a
consequence of local physical gluing plus the R8 phase thresholds, without
common terminal conditions.
"""

from __future__ import annotations

import json
import math

import numpy as np
from scipy.optimize import brentq


MUS = (1.05, 1.2, 1.5, 2.0, 3.0)
CONTRASTS = (1.01, 1.5, 2.0, 10.0, 100.0)
ENERGIES = (0.01, 0.1, 1.0, 10.0)
P_VALUES = (-5.0, -2.0, -1.0, 0.0, 1.0, 2.0, 5.0)


def propagate(state: np.ndarray, rho: float, mu: float, theta: float) -> np.ndarray:
    u, p, v, r = state
    root = math.sqrt(rho)
    c, s = math.cos(theta), math.sin(theta)
    high = mu * theta
    ch, sh = math.cos(high), math.sin(high)
    return np.asarray((
        c * u + s * p / root,
        -root * s * u + c * p,
        ch * v + sh * r / (mu * root),
        -mu * root * sh * v + ch * r,
    ))


def next_event(state: np.ndarray, rho: float, mu: float, epsilon: float,
               desired_sign: float) -> tuple[float, np.ndarray] | None:
    # At the right endpoint the quotient label is -epsilon, hence
    # U+epsilon*mu*V=0.  Find its first nontrivial zero.
    upper = math.pi / mu * (1.0 - 1.0e-10)

    def target(theta: float) -> float:
        trial = propagate(state, rho, mu, theta)
        return float(trial[0] + epsilon * mu * trial[2])

    grid = np.linspace(1.0e-8, upper, 4001)
    previous_x, previous_value = float(grid[0]), target(float(grid[0]))
    for x in grid[1:]:
        value = target(float(x))
        if value == 0.0 or value * previous_value < 0.0:
            root = brentq(target, previous_x, float(x), xtol=1.0e-13, rtol=1.0e-13)
            right = propagate(state, rho, mu, root)
            middle = propagate(state, rho, mu, root / 2.0)
            switch = middle[0] ** 2 - mu * mu * middle[2] ** 2
            if desired_sign * switch <= 1.0e-11:
                return None
            if abs(right[0]) <= 1.0e-10:
                return None
            return root, right
        previous_x, previous_value = float(x), value
    return None


def evaluate(mu: float, contrast: float, energy: float, initial_p: float) -> dict | None:
    initial_r = -math.sqrt(initial_p * initial_p + energy)
    state = np.asarray((1.0, initial_p, 1.0 / mu, initial_r))
    states = [state]
    phases = []
    epsilon = 1.0
    for rho, desired_sign in ((1.0, 1.0), (contrast, -1.0), (1.0, 1.0)):
        event = next_event(state, rho, mu, epsilon, desired_sign)
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
        jump = (-1.0, contrast - 1.0, 1.0 - contrast, contrast - 1.0)[index]
        # The first jump is actually R -> 1 and equals 1-R.
        if index == 0:
            jump = 1.0 - contrast
        value = -2.0 * jump * u**4 / derivative
        if value <= 0.0:
            return None
        alpha.append(value)

    cell_k = []
    for index, (rho, phase) in enumerate(zip((1.0, contrast, 1.0), phases)):
        u0, u1 = states[index][0], states[index + 1][0]
        cell_k.append((math.sin(phase) + mu * math.sin(mu * phase))
                      / (math.sqrt(rho) * u0 * u1))
    if not (cell_k[0] > 0.0 and cell_k[1] < 0.0 and cell_k[2] > 0.0):
        return None
    threshold = math.pi / (mu + 1.0)
    if not (phases[0] < threshold < phases[1] and phases[2] < threshold):
        return None

    a = np.asarray(alpha)
    contributions = []
    for block, edge in enumerate((0, 2)):
        left, right = 2 * block, 2 * block + 1
        compliance = 1.0 / cell_k[edge]
        determinant = a[left] * a[right] + compliance * (a[left] + a[right])
        contributions.append(((a[left] + compliance) if block == 0 else
                              (a[right] + compliance)) / determinant)
    margin = contributions[0] + contributions[1] - abs(cell_k[1])
    path_diag = np.asarray((
        1.0 / a[0] + 1.0 / a[1] + cell_k[0],
        1.0 / a[1] + 1.0 / a[2] + cell_k[1],
        1.0 / a[2] + 1.0 / a[3] + cell_k[2],
    ))
    path_off = np.asarray((-1.0 / a[1], -1.0 / a[2]))
    pivots = [float(path_diag[0])]
    pivots.append(float(path_diag[1] - path_off[0] ** 2 / pivots[-1]))
    pivots.append(float(path_diag[2] - path_off[1] ** 2 / pivots[-1]))
    energy_residual = max(abs(state_[1] ** 2 - state_[3] ** 2 + energy)
                          for state_ in states) / max(1.0, energy)
    if energy_residual > 1.0e-9:
        return None
    return {
        "mu": mu, "R": contrast, "energy": energy, "initial_p": initial_p,
        "phases": phases, "alpha": alpha, "K": cell_k,
        "dual_scalar_margin": margin,
        "path_pivots": pivots,
        "energy_relative_residual": energy_residual,
    }


def main() -> None:
    retained = []
    for mu in MUS:
        for contrast in CONTRASTS:
            for energy in ENERGIES:
                for initial_p in P_VALUES:
                    result = evaluate(mu, contrast, energy, initial_p)
                    if result is not None:
                        retained.append(result)
    negative = [row for row in retained if row["dual_scalar_margin"] <= 0.0]
    summary = {
        "status_label": "NUMERICAL_EVIDENCE",
        "grid_size": len(MUS) * len(CONTRASTS) * len(ENERGIES) * len(P_VALUES),
        "retained_local_triplets": len(retained),
        "nonpositive_margin_count": len(negative),
        "minimum_margin_record": min(retained, key=lambda row: row["dual_scalar_margin"]) if retained else None,
        "minimum_second_pivot_record": min(retained, key=lambda row: row["path_pivots"][1]) if retained else None,
        "minimum_third_pivot_record": min(retained, key=lambda row: row["path_pivots"][2]) if retained else None,
        "limitation": "local triplets omit common terminal/index/global initial predicates",
    }
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
