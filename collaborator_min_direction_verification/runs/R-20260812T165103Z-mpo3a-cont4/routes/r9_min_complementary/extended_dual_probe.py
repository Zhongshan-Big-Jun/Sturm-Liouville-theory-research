"""Reconstruct the R8 retained roots and test the R9 dual min certificate.

Deterministic binary64 NUMERICAL_EVIDENCE only; writes no output file.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROUTES = HERE.parent
SEARCH = ROUTES / "finite_contrast_singularity_r7" / "search.py"
RESULTS = ROUTES / "r8_certified_search" / "results.json"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


sr = load_module("r9_min_phase_search", SEARCH)


def reconstruct(point: dict) -> dict:
    n, mu, q, contrast = int(point["n"]), float(point["mu"]), float(point["q"]), float(point["R"])
    event_count = 2 * n
    lengths, rhos, states, _tu, _tv = sr.phase_bounded_trace(mu, q, n, contrast, str(point["mode"]))
    events = states[1:event_count + 1]
    alpha, gamma = [], []
    for index, state in enumerate(events):
        u, p, v, r = (float(value) for value in state)
        jump = float(rhos[index + 1] - rhos[index])
        switch_derivative = 2.0 * u * p - 2.0 * mu * mu * v * r
        alpha.append(-2.0 * jump * u**4 / switch_derivative)
        gamma.append(switch_derivative / (2.0 * u * u))
    cell_k = []
    for index in range(event_count - 1):
        rho = float(rhos[index + 1])
        theta = np.sqrt(rho) * float(lengths[index + 1])
        u0, u1 = float(events[index][0]), float(events[index + 1][0])
        cell_k.append((np.sin(theta) + mu * np.sin(mu * theta)) / (np.sqrt(rho) * u0 * u1))

    a = np.abs(np.asarray(alpha))
    k = np.asarray(cell_k)
    g = np.asarray(gamma)
    block_count = n
    pmat = np.diag(a)
    for edge in range(0, len(k), 2):
        vector = np.zeros(2 * n)
        vector[edge:edge + 2] = (-1.0, 1.0)
        pmat += np.outer(vector, vector) / k[edge]
    negative_edges = np.arange(1, len(k), 2)
    cmat = np.zeros((n - 1, 2 * n))
    for row, edge in enumerate(negative_edges):
        cmat[row, edge:edge + 2] = (-1.0, 1.0)
    dual = cmat @ np.linalg.solve(pmat, cmat.T) - np.diag(np.abs(k[negative_edges]))
    gamma_jump = cmat @ g
    candidate = gamma_jump / np.abs(k[negative_edges]) ** 1.5
    image = dual @ candidate
    beta = []
    alpha_right = []
    block_off = []
    for block in range(block_count):
        left, right = 2 * block, 2 * block + 1
        compliance = 1.0 / k[2 * block]
        denominator = a[left] * a[right] + compliance * (a[left] + a[right])
        beta.append((a[left] + compliance) / denominator)       # right-right entry
        alpha_right.append((a[right] + compliance) / denominator)  # left-left entry
        block_off.append(compliance / denominator)
    beta = np.asarray(beta)
    alpha_right = np.asarray(alpha_right)
    block_off = np.asarray(block_off)
    diagonal_margin = beta[:-1] + alpha_right[1:] - np.abs(k[negative_edges])
    offdiag = -np.asarray([
        (1.0 / k[2 * block])
        / (a[2 * block] * a[2 * block + 1]
           + (1.0 / k[2 * block]) * (a[2 * block] + a[2 * block + 1]))
        for block in range(1, block_count - 1)
    ])
    cross_determinants = []
    for index in range(len(diagonal_margin) - 1):
        cross_determinants.append(diagonal_margin[index] * diagonal_margin[index + 1] - offdiag[index] ** 2)
    local_triplet_left = beta[:-1] - np.abs(k[negative_edges])
    local_triplet_right = alpha_right[1:] - np.abs(k[negative_edges])
    local_triplet_sum = beta[:-1] + alpha_right[1:] - np.abs(k[negative_edges])
    event_times = np.cumsum(np.asarray(lengths))[:event_count]
    length = float(sum(lengths))
    reflection_defect = max(abs(event_times[i] + event_times[-1 - i] - length) for i in range(event_count)) / max(1.0, length)
    return {
        "dual_min_eigenvalue": float(np.linalg.eigvalsh(dual)[0]),
        "candidate_min": float(np.min(candidate)),
        "image_min": float(np.min(image)),
        "minimum_diagonal_margin": float(np.min(diagonal_margin)),
        "minimum_adjacent_minor": float(min(cross_determinants)) if cross_determinants else None,
        "minimum_triplet_left": float(np.min(local_triplet_left)),
        "minimum_triplet_right": float(np.min(local_triplet_right)),
        "minimum_triplet_sum": float(np.min(local_triplet_sum)),
        "reflection_defect": reflection_defect,
    }


def main() -> None:
    payload = json.loads(RESULTS.read_text(encoding="utf-8"))
    points = [point for point in payload["retained_points"]
              if point["mode"] == "min" and point["contract_valid"] and point["trajectory_physical_valid"]]
    rows = []
    for index, point in enumerate(points):
        result = reconstruct(point)
        result.update({"index": index, "n": point["n"], "R": point["R"], "q": point["q"], "origin": point["origin"]})
        rows.append(result)
    summary = {
        "status_label": "NUMERICAL_EVIDENCE",
        "point_count": len(rows),
        "dual_positive_count": sum(row["dual_min_eigenvalue"] > 0.0 for row in rows),
        "candidate_certificate_count": sum(row["candidate_min"] > 0.0 and row["image_min"] > 0.0 for row in rows),
        "minimum_dual_eigenvalue": min(rows, key=lambda row: row["dual_min_eigenvalue"]),
        "minimum_candidate_image": min(rows, key=lambda row: row["image_min"]),
        "minimum_diagonal_margin": min(rows, key=lambda row: row["minimum_diagonal_margin"]),
        "minimum_adjacent_minor": min(
            (row for row in rows if row["minimum_adjacent_minor"] is not None),
            key=lambda row: row["minimum_adjacent_minor"],
        ),
        "minimum_triplet_left": min(rows, key=lambda row: row["minimum_triplet_left"]),
        "minimum_triplet_right": min(rows, key=lambda row: row["minimum_triplet_right"]),
        "minimum_triplet_sum": min(rows, key=lambda row: row["minimum_triplet_sum"]),
        "maximum_reflection_defect": max(rows, key=lambda row: row["reflection_defect"]),
        "limitation": "finite binary64 discovery evidence; no universal inference",
    }
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
