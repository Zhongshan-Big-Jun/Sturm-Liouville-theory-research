"""Deterministic discovery-only probes for min L_- supersolutions.

Reads the already frozen R8 phase-probe records and prints aggregate signs.
No output file is written.  Finite binary64 results are NUMERICAL_EVIDENCE.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "r8_phase_variation" / "phase_probe_results.json"


def lminus(a: np.ndarray, k: np.ndarray) -> np.ndarray:
    size = len(k)
    out = np.zeros((size, size), dtype=float)
    for i in range(size):
        out[i, i] = 1.0 / a[i] + 1.0 / a[i + 1] + k[i]
        if i + 1 < size:
            out[i, i + 1] = out[i + 1, i] = -1.0 / a[i + 1]
    return out


def main() -> None:
    payload = json.loads(SOURCE.read_text(encoding="utf-8"))
    records = [record for record in payload["records"] if record["mode"] == "min"]
    names = (
        "effective", "minus_X", "minus_Y", "abs_K_inv", "cell_amplitude",
        "ones", "abs_K", "sqrt_abs_K", "inv_sqrt_abs_K", "phase_numerator",
        "abs_gamma_left", "abs_gamma_right", "abs_gamma_geomean",
        "inv_abs_gamma_geomean", "abs_gamma_sum", "phase_threshold_gap",
        "tan_product_gap",
    )
    stats = {name: {"positive": 0, "nonpositive": 0, "worst": float("inf"), "where": None}
             for name in names}
    local_even = {"positive": 0, "nonpositive": 0, "worst": float("inf"), "where": None}
    odd_pair_blocks = {"positive_definite": 0, "not_positive_definite": 0,
                       "worst": float("inf"), "where": None}
    odd_pair_elimination = {"positive": 0, "nonpositive": 0,
                            "worst": float("inf"), "where": None}
    even_schur_row_sums = {"positive": 0, "nonpositive": 0,
                           "worst": float("inf"), "where": None}
    dual_negative_edge = {
        "positive_definite": 0, "not_positive_definite": 0,
        "positive_row_sums": 0, "nonpositive_row_sums": 0,
        "worst_eigenvalue": float("inf"), "worst_row_sum": float("inf"),
        "where_eigenvalue": None, "where_row_sum": None,
    }
    dual_diagonal_margin = {"positive": 0, "nonpositive": 0,
                            "worst": float("inf"), "where": None}
    constant_positive_cell_subspace = {"positive": 0, "nonpositive": 0,
                                       "worst": float("inf"), "where": None}
    dual_time_translation = {"positive_vector_and_image": 0, "failure": 0,
                             "worst_vector": float("inf"), "worst_image": float("inf"),
                             "where_vector": None, "where_image": None}
    dual_candidate_names = (
        "ones", "abs_K_even", "inv_abs_K_even", "sqrt_abs_K_even",
        "inv_sqrt_abs_K_even", "phase_numerator_even", "cell_amplitude_even",
        "gamma_jump", "scaled_gamma_jump", "phase_gap_even", "tan_gap_even",
        "U_product", "inv_U_product", "U_geomean", "inv_U_geomean",
        "U_sum", "inv_U_sum", "event_a_geomean", "inv_event_a_geomean",
        "gamma_geomean_even", "inv_gamma_geomean_even",
    )
    dual_candidates = {name: {"positive": 0, "nonpositive": 0,
                              "worst": float("inf"), "where": None}
                       for name in dual_candidate_names}
    power_grid = np.linspace(-3.0, 3.0, 121)
    dual_power_scan = {
        family: {float(power): 0 for power in power_grid}
        for family in ("ones", "phase_numerator", "cell_amplitude", "gamma_jump", "U_sum")
    }

    for record_index, record in enumerate(records):
        a = np.abs(np.asarray(record["alpha"], dtype=float))
        k = np.asarray(record["K"], dtype=float)
        gamma = np.asarray(record["gamma"], dtype=float)
        lam = np.asarray(record["lambda"], dtype=float)
        theta = np.asarray(record["theta"], dtype=float)
        mu = float(record["mu"])
        contrast_energy = float(record["q"]) ** 2 - 1.0
        matrix = lminus(a, k)
        effective = -(gamma[1:] - gamma[:-1]) / k
        phase_numerator = np.sin(theta) + mu * np.sin(mu * theta)
        t_half = np.tan(theta / 2.0)
        big_t_half = np.tan(mu * theta / 2.0)
        gamma_geomean = np.sqrt(np.abs(gamma[:-1] * gamma[1:]))
        u_abs = np.sqrt(a * np.abs(gamma) / (float(record["R"]) - 1.0))
        candidates = {
            "effective": effective,
            "minus_X": effective - contrast_energy * lam,
            "minus_Y": effective + contrast_energy * (1.0 - lam),
            "abs_K_inv": 1.0 / np.abs(k),
            "cell_amplitude": (
                phase_numerator
            ) / (np.sqrt(np.where(np.arange(len(k)) % 2 == 0, 1.0, float(record["R"]))) * np.abs(k)),
            "ones": np.ones_like(k),
            "abs_K": np.abs(k),
            "sqrt_abs_K": np.sqrt(np.abs(k)),
            "inv_sqrt_abs_K": 1.0 / np.sqrt(np.abs(k)),
            "phase_numerator": phase_numerator,
            "abs_gamma_left": np.abs(gamma[:-1]),
            "abs_gamma_right": np.abs(gamma[1:]),
            "abs_gamma_geomean": gamma_geomean,
            "inv_abs_gamma_geomean": 1.0 / gamma_geomean,
            "abs_gamma_sum": np.abs(gamma[:-1]) + np.abs(gamma[1:]),
            "phase_threshold_gap": np.abs(np.pi / (mu + 1.0) - theta),
            "tan_product_gap": np.abs(big_t_half * t_half - 1.0),
        }
        for name, vector in candidates.items():
            image = matrix @ vector
            scale = np.maximum(np.abs(vector), np.finfo(float).tiny)
            margin = float(np.min(image / scale))
            ok = bool(np.all(vector > 0.0) and np.all(image > 0.0))
            stats[name]["positive" if ok else "nonpositive"] += 1
            if margin < stats[name]["worst"]:
                stats[name]["worst"] = margin
                stats[name]["where"] = {
                    "record_index": record_index,
                    "n": record["n"], "R": record["R"], "q": record["q"],
                    "min_vector": float(np.min(vector)),
                    "min_image": float(np.min(image)),
                }

        for i in range(1, len(k), 2):
            margin = 1.0 / a[i] + 1.0 / a[i + 1] - abs(k[i])
            ok = margin > 0.0
            local_even["positive" if ok else "nonpositive"] += 1
            scaled = margin / abs(k[i])
            if scaled < local_even["worst"]:
                local_even["worst"] = float(scaled)
                local_even["where"] = {
                    "record_index": record_index,
                    "edge": i + 1,
                    "n": record["n"], "R": record["R"], "q": record["q"],
                    "raw_margin": float(margin),
                }

        # Pair each positive odd edge K_(2j-1)>0 with its following negative
        # edge K_(2j)<0.  The associated 2-by-2 principal block of L_- is a
        # natural target for a block-Cholesky proof.
        for i in range(0, len(k) - 1, 2):
            block = matrix[i:i + 2, i:i + 2]
            eigmin = float(np.linalg.eigvalsh(block)[0])
            ok = eigmin > 0.0
            odd_pair_blocks["positive_definite" if ok else "not_positive_definite"] += 1
            scaled = eigmin / max(float(np.max(np.abs(block))), np.finfo(float).tiny)
            if scaled < odd_pair_blocks["worst"]:
                odd_pair_blocks["worst"] = scaled
                odd_pair_blocks["where"] = {
                    "record_index": record_index,
                    "edges": [i + 1, i + 2],
                    "n": record["n"], "R": record["R"], "q": record["q"],
                    "minimum_eigenvalue": eigmin,
                }


        # Natural non-overlapping 2-by-2 LDL elimination of indices
        # (1,2),(3,4),...; after every pair, keep the scalar Schur update on
        # the next diagonal.  This tests the exact local inequality that a
        # future block proof would need, rather than merely principal blocks.
        work = matrix.copy()
        for i in range(0, len(k) - 1, 2):
            block = work[i:i + 2, i:i + 2]
            eigmin = float(np.linalg.eigvalsh(block)[0])
            ok = eigmin > 0.0
            odd_pair_elimination["positive" if ok else "nonpositive"] += 1
            scaled = eigmin / max(float(np.max(np.abs(block))), np.finfo(float).tiny)
            if scaled < odd_pair_elimination["worst"]:
                odd_pair_elimination["worst"] = scaled
                odd_pair_elimination["where"] = {
                    "record_index": record_index,
                    "indices": [i + 1, i + 2],
                    "n": record["n"], "R": record["R"], "q": record["q"],
                    "minimum_eigenvalue": eigmin,
                }
            if not ok:
                break
            if i + 2 < len(k):
                coupling = work[i:i + 2, i + 2].copy()
                work[i + 2, i + 2] -= float(coupling @ np.linalg.solve(block, coupling))

        even_indices = np.arange(1, len(k), 2)
        odd_indices = np.arange(0, len(k), 2)
        even_diag = matrix[even_indices, even_indices]
        schur = matrix[np.ix_(odd_indices, odd_indices)].copy()
        if len(even_indices):
            cross = matrix[np.ix_(odd_indices, even_indices)]
            schur -= (cross / even_diag) @ cross.T
        row_sums = schur.sum(axis=1)
        for j, value in enumerate(row_sums):
            ok = value > 0.0
            even_schur_row_sums["positive" if ok else "nonpositive"] += 1
            scale = max(float(np.max(np.abs(schur[j]))), np.finfo(float).tiny)
            scaled = float(value / scale)
            if scaled < even_schur_row_sums["worst"]:
                even_schur_row_sums["worst"] = scaled
                even_schur_row_sums["where"] = {
                    "record_index": record_index,
                    "odd_index": int(odd_indices[j] + 1),
                    "n": record["n"], "R": record["R"], "q": record["q"],
                    "row_sum": float(value),
                }

        # Dualize around the disjoint positive edges.  P=D+B_odd^T
        # K_odd^-1 B_odd is block diagonal.  The min target is equivalent to
        # H=C P^-1 C^T-diag(|K_even|)>0 on the n-1 negative edges.
        event_count = len(a)
        pmat = np.diag(a.copy())
        for i in range(0, len(k), 2):
            vector = np.zeros(event_count)
            vector[i:i + 2] = (-1.0, 1.0)
            pmat += np.outer(vector, vector) / k[i]
        negative_edges = list(range(1, len(k), 2))
        cmat = np.zeros((len(negative_edges), event_count))
        for row, i in enumerate(negative_edges):
            cmat[row, i:i + 2] = (-1.0, 1.0)
        dual = cmat @ np.linalg.solve(pmat, cmat.T) - np.diag(np.abs(k[negative_edges]))
        eigmin = float(np.linalg.eigvalsh(dual)[0])
        ok = eigmin > 0.0
        dual_negative_edge["positive_definite" if ok else "not_positive_definite"] += 1
        scaled_eig = eigmin / max(float(np.max(np.abs(dual))), np.finfo(float).tiny)
        if scaled_eig < dual_negative_edge["worst_eigenvalue"]:
            dual_negative_edge["worst_eigenvalue"] = scaled_eig
            dual_negative_edge["where_eigenvalue"] = {
                "record_index": record_index, "n": record["n"],
                "R": record["R"], "q": record["q"], "minimum_eigenvalue": eigmin,
            }
        for row, value in enumerate(np.diag(dual)):
            ok_diag = value > 0.0
            dual_diagonal_margin["positive" if ok_diag else "nonpositive"] += 1
            scaled_diag = float(value) / max(abs(float(k[negative_edges[row]])), np.finfo(float).tiny)
            if scaled_diag < dual_diagonal_margin["worst"]:
                dual_diagonal_margin["worst"] = scaled_diag
                dual_diagonal_margin["where"] = {
                    "record_index": record_index, "negative_edge": negative_edges[row] + 1,
                    "n": record["n"], "R": record["R"], "q": record["q"],
                    "raw_margin": float(value),
                }
        # Cruder but algebraically transparent test obtained by restricting
        # d to be constant across every positive edge.  This replaces each
        # P block by A_j=a_(2j-1)+a_(2j), and asks whether
        # C diag(1/A_j) C^T-diag(|K_even|) is positive definite.
        block_mass = a.reshape(-1, 2).sum(axis=1)
        coarse_c = np.zeros((len(negative_edges), len(block_mass)))
        for row in range(len(negative_edges)):
            coarse_c[row, row:row + 2] = (-1.0, 1.0)
        coarse = coarse_c @ np.diag(1.0 / block_mass) @ coarse_c.T \
            - np.diag(np.abs(k[negative_edges]))
        coarse_eigmin = float(np.linalg.eigvalsh(coarse)[0])
        coarse_ok = coarse_eigmin > 0.0
        constant_positive_cell_subspace["positive" if coarse_ok else "nonpositive"] += 1
        coarse_scaled = coarse_eigmin / max(float(np.max(np.abs(coarse))), np.finfo(float).tiny)
        if coarse_scaled < constant_positive_cell_subspace["worst"]:
            constant_positive_cell_subspace["worst"] = coarse_scaled
            constant_positive_cell_subspace["where"] = {
                "record_index": record_index, "n": record["n"],
                "R": record["R"], "q": record["q"], "minimum_eigenvalue": coarse_eigmin,
            }
        for row, value in enumerate(dual.sum(axis=1)):
            row_ok = value > 0.0
            dual_negative_edge["positive_row_sums" if row_ok else "nonpositive_row_sums"] += 1
            scaled_row = float(value) / max(float(np.max(np.abs(dual[row]))), np.finfo(float).tiny)
            if scaled_row < dual_negative_edge["worst_row_sum"]:
                dual_negative_edge["worst_row_sum"] = scaled_row
                dual_negative_edge["where_row_sum"] = {
                    "record_index": record_index, "negative_edge": negative_edges[row] + 1,
                    "n": record["n"], "R": record["R"], "q": record["q"],
                    "row_sum": float(value),
                }

        # Project the exact time-translation comparison onto the negative-edge
        # dual.  With f=M gamma and y=diag(1/|K_even|) C gamma, exact block
        # algebra gives H y=-C P^-1 f.  If both sides are positive, this is
        # the missing M-matrix certificate for min.
        bfull = np.zeros((len(k), event_count))
        for i in range(len(k)):
            bfull[i, i:i + 2] = (-1.0, 1.0)
        mmat = np.diag(a) + bfull.T @ np.diag(1.0 / k) @ bfull
        forcing = mmat @ gamma
        ydual = (cmat @ gamma) / np.abs(k[negative_edges])
        projected = -cmat @ np.linalg.solve(pmat, forcing)
        identity_error = float(np.max(np.abs(dual @ ydual - projected)))
        ok = bool(np.all(ydual > 0.0) and np.all(projected > 0.0))
        dual_time_translation["positive_vector_and_image" if ok else "failure"] += 1
        vector_margin = float(np.min(ydual))
        image_margin = float(np.min(projected))
        if vector_margin < dual_time_translation["worst_vector"]:
            dual_time_translation["worst_vector"] = vector_margin
            dual_time_translation["where_vector"] = {
                "record_index": record_index, "n": record["n"], "R": record["R"],
                "q": record["q"], "identity_error": identity_error,
            }
        if image_margin < dual_time_translation["worst_image"]:
            dual_time_translation["worst_image"] = image_margin
            dual_time_translation["where_image"] = {
                "record_index": record_index, "n": record["n"], "R": record["R"],
                "q": record["q"], "identity_error": identity_error,
            }
        neg = np.asarray(negative_edges, dtype=int)
        dual_vectors = {
            "ones": np.ones(len(neg)),
            "abs_K_even": np.abs(k[neg]),
            "inv_abs_K_even": 1.0 / np.abs(k[neg]),
            "sqrt_abs_K_even": np.sqrt(np.abs(k[neg])),
            "inv_sqrt_abs_K_even": 1.0 / np.sqrt(np.abs(k[neg])),
            "phase_numerator_even": phase_numerator[neg],
            "cell_amplitude_even": candidates["cell_amplitude"][neg],
            "gamma_jump": cmat @ gamma,
            "scaled_gamma_jump": ydual,
            "phase_gap_even": candidates["phase_threshold_gap"][neg],
            "tan_gap_even": candidates["tan_product_gap"][neg],
            "U_product": u_abs[neg] * u_abs[neg + 1],
            "inv_U_product": 1.0 / (u_abs[neg] * u_abs[neg + 1]),
            "U_geomean": np.sqrt(u_abs[neg] * u_abs[neg + 1]),
            "inv_U_geomean": 1.0 / np.sqrt(u_abs[neg] * u_abs[neg + 1]),
            "U_sum": u_abs[neg] + u_abs[neg + 1],
            "inv_U_sum": 1.0 / (u_abs[neg] + u_abs[neg + 1]),
            "event_a_geomean": np.sqrt(a[neg] * a[neg + 1]),
            "inv_event_a_geomean": 1.0 / np.sqrt(a[neg] * a[neg + 1]),
            "gamma_geomean_even": np.sqrt(np.abs(gamma[neg] * gamma[neg + 1])),
            "inv_gamma_geomean_even": 1.0 / np.sqrt(np.abs(gamma[neg] * gamma[neg + 1])),
        }
        for name, vector in dual_vectors.items():
            image = dual @ vector
            margin = float(np.min(image / np.maximum(np.abs(vector), np.finfo(float).tiny)))
            vector_ok = bool(np.all(vector > 0.0) and np.all(image > 0.0))
            dual_candidates[name]["positive" if vector_ok else "nonpositive"] += 1
            if margin < dual_candidates[name]["worst"]:
                dual_candidates[name]["worst"] = margin
                dual_candidates[name]["where"] = {
                    "record_index": record_index, "n": record["n"],
                    "R": record["R"], "q": record["q"],
                    "min_vector": float(np.min(vector)), "min_image": float(np.min(image)),
                }
        power_bases = {
            "ones": np.ones(len(neg)),
            "phase_numerator": phase_numerator[neg],
            "cell_amplitude": candidates["cell_amplitude"][neg],
            "gamma_jump": cmat @ gamma,
            "U_sum": u_abs[neg] + u_abs[neg + 1],
        }
        for family, base_vector in power_bases.items():
            for power in power_grid:
                vector = base_vector * np.abs(k[neg]) ** power
                if np.all(vector > 0.0) and np.all(dual @ vector > 0.0):
                    dual_power_scan[family][float(power)] += 1

    power_scan_summary = {
        family: sorted(
            ({"power": power, "positive_records": count} for power, count in values.items()),
            key=lambda item: (-item["positive_records"], abs(item["power"])),
        )[:10]
        for family, values in dual_power_scan.items()
    }
    print(json.dumps({"status_label": "NUMERICAL_EVIDENCE", "min_record_count": len(records),
                      "supersolution_candidates": stats,
                      "even_cell_diagonal_margin": local_even,
                      "odd_pair_principal_blocks": odd_pair_blocks,
                      "odd_pair_ldl_elimination": odd_pair_elimination,
                      "even_schur_row_sums": even_schur_row_sums,
                      "dual_negative_edge_matrix": dual_negative_edge,
                      "dual_diagonal_margin": dual_diagonal_margin,
                      "constant_positive_cell_subspace": constant_positive_cell_subspace,
                      "dual_time_translation_certificate": dual_time_translation,
                      "dual_supersolution_candidates": dual_candidates,
                      "dual_power_scan_top": power_scan_summary}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
