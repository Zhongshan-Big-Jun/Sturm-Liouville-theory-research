#!/usr/bin/env python3
"""Bounded minimum-relay reflection and singular-root scout.

The frozen protocol is computation_contract.md.  All floating calculations
are discovery evidence only; a null result is not a proof.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import platform
import sys
import time
from typing import Any

import mpmath as mp
import numpy as np
import scipy
from scipy.optimize import brentq, least_squares, minimize_scalar


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[3]
OLD_RUN = PROJECT / "runs" / "R-20260812T165103Z-mpo3a-cont4" / "routes"
FULL_RELAY = OLD_RUN / "full_relay_counterexample" / "full_relay_scan.py"
R7_SEARCH = OLD_RUN / "finite_contrast_singularity_r7" / "search.py"
RELAY_REDUCTION = (
    PROJECT / "runs" / "R-20260811T161135Z-multiphase-o3a"
    / "routes" / "symmetric_branch_route" / "relay_reduction.py"
)
CONTRACT = HERE / "computation_contract.md"
ADDENDUM = HERE / "computation_contract_addendum_v2.md"
RESULTS = HERE / "results.json"
REPORT = HERE / "report.md"
MANIFEST = HERE / "artifact_manifest.json"

EXPECTED_SOURCES = {
    FULL_RELAY: "3c7302fa637c3ea07df7538a86074e35f07d5f2a19c9798d7c5cd692e74b30da",
    R7_SEARCH: "328834301b02354356d8299893f68680bd79f8c9385c274bfa884f7dcc72821a",
    RELAY_REDUCTION: "b2f4cecc0e271858e929235c39f7967563f2138503a2b13fe3c2e530ff6d7f5b",
}

MASTER_SEED = 2026081603
MODE = "min"
A_MIN, A_MAX = -12.0, 12.0
XQ_MIN, XQ_MAX = math.log(1.0e-8), math.log(1.0e6)
COMPLETE_TOL = 5.0e-9
COMMON_TOL = 5.0e-9
PAIR_NORM_TOL = 5.0e-8
ASYM_TOL = 1.0e-7
JAC_STEPS = (4.0e-5, 2.0e-5, 1.0e-5)


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_sources() -> dict[str, str]:
    found: dict[str, str] = {}
    for path, expected in EXPECTED_SOURCES.items():
        actual = sha256_file(path)
        found[path.relative_to(PROJECT).as_posix()] = f"sha256:{actual}"
        if actual != expected:
            raise RuntimeError(
                f"source hash mismatch: {path}; expected {expected}, actual {actual}"
            )
    return found


r7 = load_module("min_reflection_r7_validator", R7_SEARCH)


def finite_json(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): finite_json(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [finite_json(v) for v in value]
    if isinstance(value, np.ndarray):
        return finite_json(value.tolist())
    if isinstance(value, (np.floating, float)):
        x = float(value)
        return x if math.isfinite(x) else None
    if isinstance(value, (np.integer, int)) and not isinstance(value, bool):
        return int(value)
    if isinstance(value, (np.bool_, bool)):
        return bool(value)
    return value


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(finite_json(payload), indent=2, sort_keys=True, allow_nan=False),
        encoding="utf-8",
    )


def spectral_mu_cap(n: int, R: float) -> float:
    return ((n + 1.0) / n) * math.sqrt(R)


def dedup_times(values: list[float], scale: float) -> list[float]:
    out: list[float] = []
    tol = 2.0e-9 * max(1.0, scale)
    for value in sorted(values):
        if not out or abs(value - out[-1]) > tol:
            out.append(value)
    return out


def trace_audit(mu: float, q: float, n: int, R: float, L: float) -> dict[str, Any]:
    lengths, rhos, states, event_times = r7.trajectory_data(
        mu, q, n, R, MODE, 1.06 * L
    )
    zeros_u: list[float] = []
    zeros_v: list[float] = []
    elapsed = 0.0
    law_cells: list[dict[str, Any]] = []
    used_rhos: list[float] = []
    for index, (length, rho, state) in enumerate(zip(lengths, rhos, states[:-1])):
        use = min(float(length), max(0.0, L - elapsed))
        if use <= 2.0e-13 * max(1.0, L):
            break
        U, Up, V, Vp = (float(x) for x in state)
        zeros_u.extend(
            elapsed + float(dt)
            for dt in r7.fr.zero_offsets(U, Up, math.sqrt(float(rho)), use)
        )
        zeros_v.extend(
            elapsed + float(dt)
            for dt in r7.fr.zero_offsets(V, Vp, mu * math.sqrt(float(rho)), use)
        )
        midpoint = r7.fr.rr.state_at(state, mu, float(rho), 0.5 * use)
        Um, _pm, Vm, _rm = (float(x) for x in midpoint)
        S = Um * Um - mu * mu * Vm * Vm
        denom = max(Um * Um + mu * mu * Vm * Vm, 1.0e-300)
        expected_rho = R if S < 0.0 else 1.0
        alternating_rho = R if index % 2 == 0 else 1.0
        law_cells.append(
            {
                "index": index,
                "rho": float(rho),
                "expected_rho_from_midpoint_sign": float(expected_rho),
                "expected_rho_from_alternation": float(alternating_rho),
                "normalized_abs_switch_value_midcell": abs(S) / denom,
                "law_sign_ok": bool(
                    (S < 0.0 and abs(float(rho) - R) <= 2.0e-12 * max(1.0, R))
                    or (S > 0.0 and abs(float(rho) - 1.0) <= 2.0e-12)
                ),
                "alternation_ok": bool(
                    abs(float(rho) - alternating_rho)
                    <= 2.0e-12 * max(1.0, R)
                ),
            }
        )
        used_rhos.append(float(rho))
        elapsed += use
        if elapsed >= L - 2.0e-12 * max(1.0, L):
            break
    zeros_u = dedup_times(zeros_u, L)
    zeros_v = dedup_times(zeros_v, L)
    cutoff_events = [
        float(t) for t in event_times if float(t) < L - 2.0e-9 * max(1.0, L)
    ]
    return {
        "zero_count_U_through_endpoint": len(zeros_u),
        "zero_count_V_through_endpoint": len(zeros_v),
        "zeros_U": zeros_u,
        "zeros_V": zeros_v,
        "event_times": cutoff_events,
        "used_rhos": used_rhos,
        "law_cells": law_cells,
        "minimum_law_ok": bool(law_cells and all(x["law_sign_ok"] for x in law_cells)),
        "alternation_ok": bool(law_cells and all(x["alternation_ok"] for x in law_cells)),
        "index_ok": bool(
            len(zeros_u) == n
            and len(zeros_v) == n + 1
            and zeros_u
            and zeros_v
            and abs(zeros_u[-1] - L) <= 3.0e-8 * max(1.0, L)
            and abs(zeros_v[-1] - L) <= 3.0e-8 * max(1.0, L)
        ),
    }


def validate_root(
    mu: float, q: float, n: int, R: float, *, complete: bool
) -> dict[str, Any]:
    validation = r7.physical_validation(
        float(mu), float(q), int(n), float(R), MODE, include_derivatives=True
    )
    trace = trace_audit(mu, q, n, R, float(validation["L"]))
    validation["trace_audit"] = trace
    validation["minimum_law_ok"] = trace["minimum_law_ok"]
    validation["index_ok"] = trace["index_ok"]
    validation["alternation_ok"] = trace["alternation_ok"]
    validation["common_terminal_residual_ok"] = bool(
        abs(float(validation["A_scaled"])) <= COMMON_TOL
    )
    validation["equal_norm_residual_ok"] = bool(
        (not complete)
        or abs(float(validation["C_log_integral_ratio"])) <= COMPLETE_TOL
    )
    validation["strict_valid"] = bool(
        validation["trajectory_physical_valid"]
        and validation["implementation_crosscheck_pass"]
        and validation["minimum_law_ok"]
        and validation["alternation_ok"]
        and validation["index_ok"]
        and validation["common_terminal_residual_ok"]
        and validation["equal_norm_residual_ok"]
    )
    return validation


def reflection_diagnostics(validation: dict[str, Any], *, complete: bool) -> dict[str, Any]:
    mu = float(validation["mu"])
    q = float(validation["q"])
    R = float(validation["R"])
    n = int(validation["n"])
    L = float(validation["L"])
    _U, p, _V, rv = (float(x) for x in validation["terminal_state"])
    q_sharp = abs(rv / p) if p != 0.0 else float("nan")
    hq = math.sqrt(max(0.0, 1.0 + (q * q - 1.0) / (p * p))) if p != 0.0 else float("nan")
    own_events = [float(x) for x in validation["event_times"]]
    self_error = max(
        (abs(own_events[j] + own_events[-1 - j] - L) for j in range(len(own_events))),
        default=0.0,
    )
    result: dict[str, Any] = {
        "q_sharp": q_sharp,
        "h_q": hq,
        "q_sharp_minus_h_q": q_sharp - hq,
        "q_sharp_minus_q": q_sharp - q,
        "relative_q_defect": abs(q_sharp - q) / max(1.0, q),
        "self_switch_reflection_max_error": self_error,
        "self_switch_reflection_normalized_error": self_error / max(1.0, L),
        "partner_valid": False,
    }
    if not (math.isfinite(q_sharp) and q_sharp > 1.0):
        result["partner_error"] = "q_sharp_outside_domain"
        return result
    try:
        partner = validate_root(mu, q_sharp, n, R, complete=complete)
        _U2, p2, _V2, _r2 = (float(x) for x in partner["terminal_state"])
        h2 = (
            math.sqrt(max(0.0, 1.0 + (q_sharp * q_sharp - 1.0) / (p2 * p2)))
            if p2 != 0.0 else float("nan")
        )
        partner_events = [float(x) for x in partner["event_times"]]
        partner_L = float(partner["L"])
        mirror_error = float("inf")
        if len(own_events) == len(partner_events):
            mirror_error = max(
                (
                    abs(own_events[j] + partner_events[-1 - j] - L)
                    for j in range(len(own_events))
                ),
                default=0.0,
            )
        result.update(
            {
                "partner_valid": bool(partner["strict_valid"]),
                "partner_A_scaled": float(partner["A_scaled"]),
                "partner_C_log_integral_ratio": float(partner["C_log_integral_ratio"]),
                "partner_event_count": int(partner["event_count"]),
                "partner_terminal_length": partner_L,
                "partner_terminal_length_difference": partner_L - L,
                "h_h_q": h2,
                "h_h_q_minus_q": h2 - q,
                "partner_q_sharp": abs(float(partner["terminal_state"][3]) / p2)
                if p2 != 0.0 else float("nan"),
                "partner_mirror_max_error": mirror_error,
                "partner_mirror_normalized_error": mirror_error / max(1.0, L),
            }
        )
    except Exception as exc:
        result["partner_error"] = f"{type(exc).__name__}: {exc}"
    return result


def compact_validation(validation: dict[str, Any], *, complete: bool) -> dict[str, Any]:
    reflection = reflection_diagnostics(validation, complete=complete)
    record = {
        "n": int(validation["n"]),
        "mode": MODE,
        "R": float(validation["R"]),
        "mu": float(validation["mu"]),
        "q": float(validation["q"]),
        "float_hex": validation.get("float_hex"),
        "A_scaled": float(validation["A_scaled"]),
        "C_log_integral_ratio": float(validation["C_log_integral_ratio"]),
        "TU": float(validation["TU"]),
        "TV": float(validation["TV"]),
        "L": float(validation["L"]),
        "IU": float(validation["IU"]),
        "IV": float(validation["IV"]),
        "event_count": int(validation["event_count"]),
        "event_times": list(validation["event_times"]),
        "minimum_normalized_cell_length": float(validation["minimum_normalized_cell_length"]),
        "maximum_normalized_switch_residual": float(validation["maximum_normalized_switch_residual"]),
        "minimum_normalized_transversality": float(validation["minimum_normalized_transversality"]),
        "terminal_state": list(validation["terminal_state"]),
        "terminal_position_residuals": list(validation["terminal_position_residuals"]),
        "energy_relative_error": float(validation["energy_relative_error"]),
        "endpoint_energy_relative_error": float(validation["endpoint_energy_relative_error"]),
        "validity_predicates": dict(validation["validity_predicates"]),
        "trajectory_physical_valid": bool(validation["trajectory_physical_valid"]),
        "derivative_stable": bool(
            validation.get("derivative_validation", {}).get("stable", False)
        ),
        "minimum_law_ok": bool(validation["minimum_law_ok"]),
        "alternation_ok": bool(validation["alternation_ok"]),
        "index_ok": bool(validation["index_ok"]),
        "zero_counts": [
            int(validation["trace_audit"]["zero_count_U_through_endpoint"]),
            int(validation["trace_audit"]["zero_count_V_through_endpoint"]),
        ],
        "implementation_crosscheck_pass": bool(validation["implementation_crosscheck_pass"]),
        "strict_valid": bool(validation["strict_valid"]),
        "reflection": reflection,
    }
    record["asymmetric_witness_predicate"] = bool(
        complete
        and record["strict_valid"]
        and reflection.get("partner_valid", False)
        and reflection["relative_q_defect"] > ASYM_TOL
        and reflection["self_switch_reflection_normalized_error"] > ASYM_TOL
        and reflection.get("partner_mirror_normalized_error", float("inf")) <= 2.0e-7
        and abs(float(reflection.get("h_h_q_minus_q", float("inf"))))
        <= 2.0e-7 * max(1.0, record["q"])
    )
    return record


def jacobian_diagnostics(z: np.ndarray, n: int, R: float) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for h in JAC_STEPS:
        jac = np.empty((2, 2), dtype=float)
        for j in range(2):
            plus = np.asarray(z, dtype=float).copy()
            minus = np.asarray(z, dtype=float).copy()
            plus[j] += h
            minus[j] -= h
            fp = np.asarray(r7.fixed_residual(plus, n, R, MODE), dtype=float)
            fm = np.asarray(r7.fixed_residual(minus, n, R, MODE), dtype=float)
            jac[:, j] = (fp - fm) / (2.0 * h)
        col_norms = np.linalg.norm(jac, axis=0)
        denom = max(float(np.prod(col_norms)), np.finfo(float).tiny)
        normalized = jac / np.maximum(col_norms, np.finfo(float).tiny)
        svals = np.linalg.svd(jac, compute_uv=False)
        normalized_svals = np.linalg.svd(normalized, compute_uv=False)
        rows.append(
            {
                "step": h,
                "matrix": jac.tolist(),
                "determinant": float(np.linalg.det(jac)),
                "normalized_determinant": float(np.linalg.det(jac) / denom),
                "singular_values": svals.tolist(),
                "normalized_singular_values": normalized_svals.tolist(),
                "column_norms": col_norms.tolist(),
            }
        )
    ndets = [float(x["normalized_determinant"]) for x in rows]
    abs_values = [abs(x) for x in ndets]
    nonzero_signs = [1 if x > 0.0 else -1 for x in ndets if x != 0.0]
    return {
        "steps": rows,
        "maximum_abs_normalized_determinant": max(abs_values),
        "minimum_abs_normalized_determinant": min(abs_values),
        "normalized_determinant_spread": max(ndets) - min(ndets),
        "same_nonzero_sign": bool(nonzero_signs and len(set(nonzero_signs)) == 1),
        "stable": bool(
            max(ndets) - min(ndets) <= max(2.0e-5, 0.08 * max(abs_values))
        ),
    }


def seed_design(
    count: int, rng: np.random.Generator, continuation: list[np.ndarray]
) -> list[np.ndarray]:
    fixed_a = (-10.0, -6.0, -2.0, 2.0, 6.0, 10.0)
    fixed_q = (-14.0, -7.0, -2.0, 3.0, 8.0)
    seeds = [np.asarray([a, xq], dtype=float) for a in fixed_a for xq in fixed_q]
    seeds = [np.asarray(x, dtype=float) for x in continuation] + seeds
    while len(seeds) < count:
        seeds.append(
            rng.uniform(
                np.asarray([A_MIN + 1.0e-6, XQ_MIN + 1.0e-6]),
                np.asarray([A_MAX - 1.0e-6, XQ_MAX - 1.0e-6]),
            )
        )
    return seeds[:count]


def same_root(old: dict[str, Any], mu: float, q: float) -> bool:
    return bool(
        max(
            abs(math.log(mu / float(old["mu"]))),
            abs(math.log((q - 1.0) / (float(old["q"]) - 1.0))),
        )
        < 2.0e-7
    )


def solve_complete_case(
    n: int,
    R: float,
    starts: int,
    rng: np.random.Generator,
    continuation: list[np.ndarray],
) -> dict[str, Any]:
    lower = np.asarray([A_MIN, XQ_MIN])
    upper = np.asarray([A_MAX, XQ_MAX])
    roots: list[dict[str, Any]] = []
    near_misses: list[dict[str, Any]] = []
    failures = 0
    for index, seed in enumerate(seed_design(starts, rng, continuation)):
        try:
            out = least_squares(
                r7.fixed_residual,
                np.minimum(np.maximum(seed, lower + 1.0e-9), upper - 1.0e-9),
                bounds=(lower, upper),
                args=(n, R, MODE),
                max_nfev=320,
                xtol=2.0e-12,
                ftol=2.0e-12,
                gtol=2.0e-12,
                x_scale="jac",
            )
            residual = np.asarray(r7.fixed_residual(out.x, n, R, MODE), dtype=float)
            score = float(np.max(np.abs(residual)))
            attempt = {
                "start_index": index,
                "seed": seed.tolist(),
                "solution": out.x.tolist(),
                "residual": residual.tolist(),
                "residual_inf": score,
                "nfev": int(out.nfev),
                "optimizer_success": bool(out.success),
            }
            if not np.all(np.isfinite(residual)) or score > COMPLETE_TOL:
                near_misses.append(attempt)
                continue
            mu, q = r7.decode_fixed(out.x, n, R)
            if any(same_root(old, mu, q) for old in roots):
                continue
            validation = validate_root(mu, q, n, R, complete=True)
            if not validation["strict_valid"]:
                attempt["rejected_validity"] = {
                    "predicates": validation["validity_predicates"],
                    "minimum_law_ok": validation["minimum_law_ok"],
                    "alternation_ok": validation["alternation_ok"],
                    "index_ok": validation["index_ok"],
                    "implementation_crosscheck_pass": validation["implementation_crosscheck_pass"],
                }
                near_misses.append(attempt)
                continue
            record = compact_validation(validation, complete=True)
            record["encoded_root"] = out.x.tolist()
            record["optimizer"] = attempt
            record["jacobian"] = jacobian_diagnostics(out.x, n, R)
            roots.append(record)
        except Exception as exc:
            failures += 1
            near_misses.append(
                {
                    "start_index": index,
                    "seed": seed.tolist(),
                    "error": f"{type(exc).__name__}: {exc}",
                    "residual_inf": None,
                }
            )
    roots.sort(key=lambda x: (float(x["mu"]), float(x["q"])))
    finite_near = [x for x in near_misses if x.get("residual_inf") is not None]
    finite_near.sort(key=lambda x: float(x["residual_inf"]))
    return {
        "n": n,
        "R": R,
        "R_hex": float(R).hex(),
        "starts": starts,
        "failure_count": failures,
        "distinct_strict_root_count": len(roots),
        "roots": roots,
        "best_near_misses": finite_near[:8],
    }


def singular_equations(w: np.ndarray, n: int = 2) -> np.ndarray:
    xr, a, xq = (float(x) for x in np.asarray(w, dtype=float))
    try:
        R = 1.0 + math.exp(xr)
        z = np.asarray([a, xq], dtype=float)
        base = np.asarray(r7.fixed_residual(z, n, R, MODE), dtype=float)
        if not np.all(np.isfinite(base)):
            raise ValueError("nonfinite base")
        h = 2.0e-5
        jac = np.empty((2, 2), dtype=float)
        for j in range(2):
            plus, minus = z.copy(), z.copy()
            plus[j] += h
            minus[j] -= h
            jac[:, j] = (
                np.asarray(r7.fixed_residual(plus, n, R, MODE), dtype=float)
                - np.asarray(r7.fixed_residual(minus, n, R, MODE), dtype=float)
            ) / (2.0 * h)
        norms = np.linalg.norm(jac, axis=0)
        ndet = float(np.linalg.det(jac) / max(float(np.prod(norms)), 1.0e-300))
        if not math.isfinite(ndet):
            raise ValueError("nonfinite determinant")
        return np.asarray([base[0], base[1], ndet], dtype=float)
    except Exception:
        return np.asarray([10.0, 10.0, 1.0], dtype=float)


def singular_start_task(task: tuple[int, list[float]]) -> dict[str, Any]:
    index, seed_list = task
    seed = np.asarray(seed_list, dtype=float)
    lower = np.asarray([math.log(1.0e-5), -10.0, math.log(1.0e-7)])
    upper = np.asarray([math.log(1.0e7), 10.0, math.log(1.0e5)])
    try:
        out = least_squares(
            singular_equations,
            np.minimum(np.maximum(seed, lower + 1.0e-8), upper - 1.0e-8),
            bounds=(lower, upper),
            max_nfev=220,
            xtol=5.0e-11,
            ftol=5.0e-11,
            gtol=5.0e-11,
            x_scale="jac",
        )
        residual = singular_equations(out.x)
        return {
            "start_index": index,
            "seed": seed.tolist(),
            "solution": out.x.tolist(),
            "residual": residual.tolist(),
            "score": float(np.max(np.abs(residual))),
            "nfev": int(out.nfev),
            "optimizer_success": bool(out.success),
        }
    except Exception as exc:
        return {
            "start_index": index,
            "seed": seed.tolist(),
            "error": f"{type(exc).__name__}: {exc}",
            "score": None,
        }


def singular_seeds(
    count: int, complete_cases: list[dict[str, Any]], rng: np.random.Generator
) -> list[np.ndarray]:
    seeds: list[np.ndarray] = []
    risk: list[tuple[float, np.ndarray]] = []
    for case in complete_cases:
        for root in case["roots"]:
            risk.append(
                (
                    float(root["jacobian"]["minimum_abs_normalized_determinant"]),
                    np.asarray(
                        [math.log(float(case["R"]) - 1.0), *root["encoded_root"]],
                        dtype=float,
                    ),
                )
            )
    seeds.extend(x[1] for x in sorted(risk, key=lambda x: x[0])[:24])
    for xr in (math.log(1.0e-4), math.log(1.0), math.log(1.0e4), math.log(1.0e6)):
        for a in (-8.0, 0.0, 8.0):
            for xq in (-10.0, -2.0, 6.0):
                seeds.append(np.asarray([xr, a, xq], dtype=float))
    lower = np.asarray([math.log(1.0e-5), -10.0, math.log(1.0e-7)])
    upper = np.asarray([math.log(1.0e7), 10.0, math.log(1.0e5)])
    while len(seeds) < count:
        seeds.append(rng.uniform(lower + 1.0e-6, upper - 1.0e-6))
    return seeds[:count]


def run_singular_search(
    count: int,
    complete_cases: list[dict[str, Any]],
    workers: int,
    rng: np.random.Generator,
) -> dict[str, Any]:
    seeds = singular_seeds(count, complete_cases, rng)
    tasks = [(i, seed.tolist()) for i, seed in enumerate(seeds)]
    if workers <= 1:
        attempts = [singular_start_task(task) for task in tasks]
    else:
        attempts = []
        with ProcessPoolExecutor(max_workers=workers) as pool:
            future_map = {pool.submit(singular_start_task, task): task[0] for task in tasks}
            for future in as_completed(future_map):
                attempts.append(future.result())
    attempts.sort(key=lambda x: int(x["start_index"]))
    candidates: list[dict[str, Any]] = []
    for attempt in attempts:
        if attempt.get("score") is None:
            continue
        residual = [float(x) for x in attempt["residual"]]
        if max(abs(residual[0]), abs(residual[1])) > 2.0e-8 or abs(residual[2]) > 2.0e-5:
            continue
        xr, a, xq = (float(x) for x in attempt["solution"])
        R = 1.0 + math.exp(xr)
        z = np.asarray([a, xq], dtype=float)
        mu, q = r7.decode_fixed(z, 2, R)
        try:
            validation = validate_root(mu, q, 2, R, complete=True)
            jac = jacobian_diagnostics(z, 2, R)
            if not validation["strict_valid"]:
                continue
            if jac["maximum_abs_normalized_determinant"] > 2.0e-4:
                continue
            record = compact_validation(validation, complete=True)
            record["encoded_root"] = z.tolist()
            record["log_delta_R"] = xr
            record["jacobian"] = jac
            record["optimizer"] = attempt
            if not any(
                max(
                    abs(math.log(record["R"] / old["R"])),
                    abs(math.log(record["mu"] / old["mu"])),
                    abs(math.log((record["q"] - 1.0) / (old["q"] - 1.0))),
                ) < 2.0e-6
                for old in candidates
            ):
                candidates.append(record)
        except Exception:
            continue
    finite = [x for x in attempts if x.get("score") is not None]
    finite.sort(key=lambda x: float(x["score"]))
    candidates.sort(key=lambda x: (x["R"], x["mu"], x["q"]))
    return {
        "start_count": count,
        "optimizer_failure_count": sum(x.get("score") is None for x in attempts),
        "floating_candidate_count": len(candidates),
        "candidates": candidates,
        "best_near_misses": finite[:30],
    }


def common_sample(mu: float, q: float, n: int, R: float) -> dict[str, Any]:
    try:
        residual, detail = r7.basic_eval(mu, q, n, R, MODE, detail=True)
        return {
            "ok": True,
            "q": q,
            "xq": math.log(q - 1.0),
            "A": float(residual[0]),
            "event_count": int(detail["event_count_before_endpoint"]),
        }
    except Exception as exc:
        return {"ok": False, "q": q, "xq": math.log(q - 1.0), "error": type(exc).__name__}


def common_a_xq(xq: float, mu: float, n: int, R: float) -> float:
    q = 1.0 + math.exp(float(xq))
    try:
        value = float(r7.scaled_a(mu, q, n, R, MODE))
        return value if math.isfinite(value) else float("nan")
    except Exception:
        return float("nan")


def pair_audit(roots: list[dict[str, Any]]) -> dict[str, Any]:
    roots = sorted(roots, key=lambda x: float(x["q"]))
    equal = [x for x in roots if abs(float(x["C_log_integral_ratio"])) <= PAIR_NORM_TOL]
    h_values = [float(x["reflection"]["h_q"]) for x in equal]
    violations: list[dict[str, Any]] = []
    for i in range(len(equal)):
        for j in range(i + 1, len(equal)):
            if h_values[i] > h_values[j] + 2.0e-7 * max(1.0, h_values[i], h_values[j]):
                violations.append(
                    {
                        "lower_q": float(equal[i]["q"]),
                        "upper_q": float(equal[j]["q"]),
                        "h_lower": h_values[i],
                        "h_upper": h_values[j],
                        "order_relation": "reflection_map_order_reversal",
                    }
                )
    matches: list[dict[str, Any]] = []
    for i, root in enumerate(roots):
        qsharp = float(root["reflection"]["q_sharp"])
        if not math.isfinite(qsharp):
            continue
        nearest = min(
            range(len(roots)),
            key=lambda j: abs(math.log(qsharp / float(roots[j]["q"]))),
            default=None,
        )
        if nearest is not None:
            defect = abs(math.log(qsharp / float(roots[nearest]["q"])))
            if defect <= 2.0e-6:
                matches.append(
                    {
                        "source_index": i,
                        "partner_index": nearest,
                        "source_q": float(root["q"]),
                        "partner_q": float(roots[nearest]["q"]),
                        "log_match_defect": defect,
                        "h_h_q_minus_q": root["reflection"].get("h_h_q_minus_q"),
                        "partner_mirror_normalized_error": root["reflection"].get("partner_mirror_normalized_error"),
                    }
                )
    return {
        "root_count": len(roots),
        "equal_norm_root_count_at_5e-8": len(equal),
        "equal_norm_root_q_values": [float(x["q"]) for x in equal],
        "reflection_h_values_on_equal_norm_roots": h_values,
        "order_preservation_violation_count": len(violations),
        "order_preservation_violations": violations,
        "matched_reflection_pairs": matches,
    }


def common_terminal_task(task: dict[str, Any]) -> dict[str, Any]:
    n = int(task["n"])
    R = float(task["R"])
    if "mu_override" in task:
        mu = float(task["mu_override"])
        u = (mu - 1.0) / (spectral_mu_cap(n, R) - 1.0)
    else:
        u = float(task["mu_fraction"])
        mu = 1.0 + u * (spectral_mu_cap(n, R) - 1.0)
    count = int(task["q_count"])
    q_minus_min = float(task["q_minus_min"])
    q_minus_max = float(task["q_minus_max"])
    q_values = 1.0 + np.geomspace(q_minus_min, q_minus_max, count)
    samples = [common_sample(mu, float(q), n, R) for q in q_values]
    roots: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []

    def accept_xq(xq: float, mechanism: str) -> None:
        q = 1.0 + math.exp(float(xq))
        if any(abs(math.log((q - 1.0) / (float(x["q"]) - 1.0))) < 2.0e-7 for x in roots):
            return
        try:
            validation = validate_root(mu, q, n, R, complete=False)
            if validation["strict_valid"]:
                record = compact_validation(validation, complete=False)
                record["mechanism"] = mechanism
                roots.append(record)
            else:
                rejected.append(
                    {
                        "q": q,
                        "mechanism": mechanism,
                        "A_scaled": float(validation["A_scaled"]),
                        "event_count": int(validation["event_count"]),
                        "minimum_law_ok": bool(validation["minimum_law_ok"]),
                        "index_ok": bool(validation["index_ok"]),
                        "predicates": validation["validity_predicates"],
                    }
                )
        except Exception as exc:
            rejected.append({"q": q, "mechanism": mechanism, "error": f"{type(exc).__name__}: {exc}"})

    for left, right in zip(samples[:-1], samples[1:]):
        if not (left.get("ok") and right.get("ok")):
            continue
        a, b = float(left["A"]), float(right["A"])
        if not (math.isfinite(a) and math.isfinite(b)) or a == 0.0 or b == 0.0 or a * b >= 0.0:
            continue
        try:
            xq = float(
                brentq(
                    lambda x: common_a_xq(x, mu, n, R),
                    float(left["xq"]),
                    float(right["xq"]),
                    xtol=2.0e-13,
                    rtol=2.0e-14,
                    maxiter=160,
                )
            )
            mechanism = (
                "same_event_count_sign_change"
                if int(left["event_count"]) == int(right["event_count"])
                else "cross_event_count_sign_change"
            )
            accept_xq(xq, mechanism)
        except Exception:
            continue

    contact_trials: list[dict[str, Any]] = []
    for i in range(1, len(samples) - 1):
        triple = samples[i - 1:i + 2]
        if not all(x.get("ok") and int(x["event_count"]) == 2 * n for x in triple):
            continue
        vals = [abs(float(x["A"])) for x in triple]
        if not (vals[1] < vals[0] and vals[1] < vals[2] and vals[1] < 2.0e-3):
            continue
        if float(triple[0]["A"]) * float(triple[1]["A"]) < 0.0 or float(triple[1]["A"]) * float(triple[2]["A"]) < 0.0:
            continue
        try:
            out = minimize_scalar(
                lambda x: abs(common_a_xq(float(x), mu, n, R)),
                bounds=(float(triple[0]["xq"]), float(triple[2]["xq"])),
                method="bounded",
                options={"xatol": 2.0e-11, "maxiter": 140},
            )
            contact_trials.append(
                {
                    "sample_xq": float(triple[1]["xq"]),
                    "sample_abs_A": vals[1],
                    "refined_xq": float(out.x),
                    "refined_abs_A": float(out.fun),
                    "success": bool(out.success),
                }
            )
            if float(out.fun) <= COMMON_TOL:
                accept_xq(float(out.x), "even_contact")
        except Exception:
            continue

    roots.sort(key=lambda x: float(x["q"]))
    finite_samples = [x for x in samples if x.get("ok") and math.isfinite(float(x["A"]))]
    finite_samples.sort(key=lambda x: abs(float(x["A"])))
    return {
        "n": n,
        "R": R,
        "mu_fraction": u,
        "mu": mu,
        "task_origin": task.get("origin", "registered_mu_fraction"),
        "q_minus_domain": [q_minus_min, q_minus_max, count],
        "successful_sample_count": len(finite_samples),
        "failed_sample_count": len(samples) - len(finite_samples),
        "roots": roots,
        "pair_audit": pair_audit(roots),
        "rejected_root_count": len(rejected),
        "rejected_roots": rejected[:8],
        "contact_trial_count": len(contact_trials),
        "contact_trials": contact_trials[:12],
        "smallest_sampled_abs_A": finite_samples[:5],
    }


def run_common_tasks(tasks: list[dict[str, Any]], workers: int) -> list[dict[str, Any]]:
    if workers <= 1:
        records = [common_terminal_task(task) for task in tasks]
    else:
        records = []
        with ProcessPoolExecutor(max_workers=workers) as pool:
            future_map = {pool.submit(common_terminal_task, task): task for task in tasks}
            for future in as_completed(future_map):
                records.append(future.result())
    records.sort(key=lambda x: (x["n"], x["R"], x["mu"]))
    return records


def high_precision_replay(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not candidates:
        return []
    r8_path = OLD_RUN / "r8_certified_search" / "search.py"
    r8 = load_module("min_reflection_r8_high_precision", r8_path)
    outputs: list[dict[str, Any]] = []
    for candidate in candidates:
        try:
            validation = validate_root(
                float(candidate["mu"]), float(candidate["q"]), int(candidate["n"]),
                float(candidate["R"]), complete=True,
            )
            point = r8.compact_point(validation, "min_reflection_search", "complete_o3a")
            replay = r8.mp_refine_point(point)
            reflection_replay = None
            if replay.get("status") == "ok" and replay.get("refined"):
                with mp.workdps(100):
                    refined = replay["refined"]
                    mu_mp = mp.mpf(refined["mu"])
                    q_mp = mp.mpf(refined["q"])
                    R_mp = mp.mpf(refined["R"])
                    guide = r8.make_mp_guide(point)
                    trace = r8.mp_trace(mu_mp, q_mp, R_mp, int(point["n"]), MODE, guide)
                    p_mp, rv_mp = trace["terminal"][1], trace["terminal"][3]
                    q_sharp = abs(rv_mp / p_mp)
                    h_q = mp.sqrt(1 + (q_mp * q_mp - 1) / (p_mp * p_mp))
                    reversed_lengths = list(reversed(trace["lengths"]))
                    partner_guide = {
                        "event_lengths": [mp.nstr(x, 100) for x in reversed_lengths[: 2 * int(point["n"])]],
                        "terminal_length": mp.nstr(reversed_lengths[2 * int(point["n"])], 100),
                    }
                    partner = r8.mp_trace(
                        mu_mp, q_sharp, R_mp, int(point["n"]), MODE, partner_guide
                    )
                    p2, rv2 = partner["terminal"][1], partner["terminal"][3]
                    h_h_q = mp.sqrt(1 + (q_sharp * q_sharp - 1) / (p2 * p2))
                    L_mp = (trace["TU"] + trace["TV"]) / 2
                    L2 = (partner["TU"] + partner["TV"]) / 2
                    own_times = trace["event_times"]
                    partner_times = partner["event_times"]
                    self_error = max(
                        abs(own_times[j] + own_times[-1 - j] - L_mp)
                        for j in range(len(own_times))
                    )
                    mirror_error = max(
                        abs(own_times[j] + partner_times[-1 - j] - L_mp)
                        for j in range(len(own_times))
                    )
                    fmt = lambda x: mp.nstr(x, 75)
                    reflection_replay = {
                        "q_sharp": fmt(q_sharp),
                        "h_q": fmt(h_q),
                        "q_sharp_minus_h_q": fmt(q_sharp - h_q),
                        "q_sharp_minus_q": fmt(q_sharp - q_mp),
                        "h_h_q": fmt(h_h_q),
                        "h_h_q_minus_q": fmt(h_h_q - q_mp),
                        "self_switch_reflection_max_error": fmt(self_error),
                        "self_switch_reflection_normalized_error": fmt(self_error / max(1, L_mp)),
                        "partner_mirror_max_error": fmt(mirror_error),
                        "partner_mirror_normalized_error": fmt(mirror_error / max(1, L_mp)),
                        "partner_terminal_length_difference": fmt(L2 - L_mp),
                        "partner_terminal_gap_scaled": fmt(
                            (partner["TU"] - partner["TV"]) / max(1, L2)
                        ),
                        "partner_log_integral_ratio": fmt(mp.log(partner["IU"] / partner["IV"])),
                        "partner_q_sharp": fmt(abs(rv2 / p2)),
                        "arithmetic": "mpmath 100 decimal digits; not interval arithmetic",
                    }
            outputs.append(
                {
                    "n": candidate["n"], "R": candidate["R"],
                    "mu": candidate["mu"], "q": candidate["q"],
                    "replay": replay,
                    "reflection_replay": reflection_replay,
                }
            )
        except Exception as exc:
            outputs.append(
                {
                    "n": candidate.get("n"), "R": candidate.get("R"),
                    "mu": candidate.get("mu"), "q": candidate.get("q"),
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )
    return outputs


def reconcile_high_precision_clusters(
    complete_cases: list[dict[str, Any]], hp: list[dict[str, Any]]
) -> dict[str, Any]:
    lookup = {
        (float(x["R"]), float(x["mu"]), float(x["q"])): x
        for x in hp
    }
    cases: list[dict[str, Any]] = []
    reconciled_total = 0
    for case in complete_cases:
        roots = case["roots"]
        if len(roots) <= 1:
            reconciled_total += len(roots)
            continue
        replays = [
            lookup.get((float(case["R"]), float(root["mu"]), float(root["q"])))
            for root in roots
        ]
        all_ok = bool(
            all(
                item is not None
                and item.get("replay", {}).get("status") == "ok"
                and item.get("replay", {}).get("refined")
                for item in replays
            )
        )
        clusters: list[tuple[mp.mpf, mp.mpf]] = []
        if all_ok:
            with mp.workdps(100):
                for item in replays:
                    refined = item["replay"]["refined"]
                    point = (mp.mpf(refined["mu"]), mp.mpf(refined["q"]))
                    if not any(
                        max(abs(point[0] - old[0]), abs(point[1] - old[1]))
                        <= mp.mpf("1e-70")
                        for old in clusters
                    ):
                        clusters.append(point)
        cluster_count = len(clusters) if all_ok else len(roots)
        reconciled_total += cluster_count
        cases.append(
            {
                "R": float(case["R"]),
                "binary_root_record_count": len(roots),
                "all_binary_records_replayed": all_ok,
                "high_precision_cluster_count": cluster_count if all_ok else None,
                "all_converged_to_one_root": bool(all_ok and cluster_count == 1),
                "refined_clusters": [
                    {"mu": mp.nstr(x[0], 75), "q": mp.nstr(x[1], 75)}
                    for x in clusters
                ],
            }
        )
    return {
        "binary_multiple_root_case_count": len(cases),
        "replayed_multiple_root_case_count": sum(x["all_binary_records_replayed"] for x in cases),
        "duplicate_cluster_resolved_case_count": sum(x["all_converged_to_one_root"] for x in cases),
        "unresolved_multiple_root_case_count": sum(not x["all_binary_records_replayed"] for x in cases),
        "reconciled_complete_root_count": reconciled_total,
        "cases": cases,
        "interpretation": "Binary records are not distinct roots when 100-digit refinement converges to the same cluster.",
    }


def make_common_tasks(scope: str, held_out: bool = False) -> list[dict[str, Any]]:
    if held_out:
        ns = (3, 4)
        Rs = (1.01, 2.0, 100.0, 1.0e4)
        fractions = (1.0e-4, 1.0e-3, 1.0e-2, 0.10, 0.40, 0.80, 0.97, 0.999)
        q_count = 180
        q_max = 1.0e5
    elif scope == "smoke":
        ns = (2,)
        Rs = (1.01, 2.0, 100.0)
        fractions = (1.0e-3, 0.05, 0.5, 0.95, 0.999)
        q_count = 100
        q_max = 1.0e4
    else:
        ns = (2,)
        Rs = (1.0001, 1.01, 1.1, 2.0, 10.0, 100.0, 1.0e4, 1.0e6)
        fractions = (
            1.0e-5, 1.0e-4, 1.0e-3, 1.0e-2, 0.05, 0.2,
            0.5, 0.8, 0.95, 0.99, 0.999, 0.9999,
        )
        q_count = 300
        q_max = 1.0e6
    return [
        {
            "n": n, "R": R, "mu_fraction": u,
            "q_count": q_count, "q_minus_min": 1.0e-8,
            "q_minus_max": q_max,
        }
        for n in ns for R in Rs for u in fractions
    ]


def summarize(payload: dict[str, Any]) -> dict[str, Any]:
    complete_roots = [
        root for case in payload["complete_search"]["cases"] for root in case["roots"]
    ]
    common_roots = [
        root for rec in payload["common_terminal_search"]["records"] for root in rec["roots"]
    ]
    held_roots = [
        root for rec in payload.get("held_out_search", {}).get("records", []) for root in rec["roots"]
    ]
    all_roots = complete_roots + common_roots + held_roots
    asym = [root for root in complete_roots if root["asymmetric_witness_predicate"]]
    singular = payload["singular_search"]["candidates"]
    order_violations = [
        item
        for rec in payload["common_terminal_search"]["records"]
        for item in rec["pair_audit"]["order_preservation_violations"]
    ]
    equal_pair_problems = [
        rec for rec in payload["common_terminal_search"]["records"]
        if rec["pair_audit"]["equal_norm_root_count_at_5e-8"] >= 2
    ]
    return {
        "complete_case_count": len(payload["complete_search"]["cases"]),
        "complete_start_count": sum(x["starts"] for x in payload["complete_search"]["cases"]),
        "complete_strict_binary_root_record_count": len(complete_roots),
        "complete_reconciled_root_count": payload["high_precision_cluster_reconciliation"]["reconciled_complete_root_count"],
        "complete_binary_multiple_root_case_count": sum(len(x["roots"]) > 1 for x in payload["complete_search"]["cases"]),
        "complete_hp_duplicate_cluster_resolved_case_count": payload["high_precision_cluster_reconciliation"]["duplicate_cluster_resolved_case_count"],
        "complete_unresolved_multiple_root_case_count": payload["high_precision_cluster_reconciliation"]["unresolved_multiple_root_case_count"],
        "asymmetric_complete_candidate_count": len(asym),
        "singular_start_count": payload["singular_search"]["start_count"],
        "singular_candidate_count": len(singular),
        "common_terminal_problem_count": len(payload["common_terminal_search"]["records"]),
        "common_terminal_strict_root_count": len(common_roots),
        "common_terminal_multiple_root_problem_count": sum(len(x["roots"]) > 1 for x in payload["common_terminal_search"]["records"]),
        "equal_norm_multiple_root_problem_count": len(equal_pair_problems),
        "equal_norm_order_preservation_violation_count": len(order_violations),
        "held_out_problem_count": len(payload.get("held_out_search", {}).get("records", [])),
        "held_out_root_count": len(held_roots),
        "maximum_relative_q_reflection_defect": max(
            (float(x["reflection"]["relative_q_defect"]) for x in all_roots), default=None
        ),
        "maximum_self_switch_reflection_normalized_error": max(
            (float(x["reflection"]["self_switch_reflection_normalized_error"]) for x in all_roots), default=None
        ),
        "maximum_abs_h_involution_defect": max(
            (abs(float(x["reflection"].get("h_h_q_minus_q", float("nan")))) for x in all_roots
             if math.isfinite(float(x["reflection"].get("h_h_q_minus_q", float("nan"))))),
            default=None,
        ),
        "maximum_partner_mirror_normalized_error": max(
            (float(x["reflection"].get("partner_mirror_normalized_error", float("nan"))) for x in all_roots
             if math.isfinite(float(x["reflection"].get("partner_mirror_normalized_error", float("nan"))))),
            default=None,
        ),
        "minimum_abs_complete_normalized_jacobian_determinant": min(
            (float(x["jacobian"]["minimum_abs_normalized_determinant"]) for x in complete_roots),
            default=None,
        ),
        "high_precision_replay_count": len(payload.get("high_precision_replay", [])),
    }


def write_report(payload: dict[str, Any]) -> None:
    s = payload["summary"]
    status = "COUNTEREXAMPLE_CANDIDATE" if s["asymmetric_complete_candidate_count"] else "NUMERICAL_EVIDENCE"
    lines = [
        status,
        "",
        "# MIN-REFL-C bounded search report",
        "",
        "## Outcome",
        "",
        f"The run retained {s['complete_strict_binary_root_record_count']} strict binary64 complete-root records from "
        f"{s['complete_start_count']} deterministic starts over {s['complete_case_count']} contrasts.",
        f"After 100-digit cluster reconciliation these represent {s['complete_reconciled_root_count']} roots on the sampled contrasts; "
        f"{s['complete_hp_duplicate_cluster_resolved_case_count']} apparent binary64 multiple-root cases collapsed to one root each, "
        f"and {s['complete_unresolved_multiple_root_case_count']} remain unresolved.",
        f"Asymmetric complete candidates: {s['asymmetric_complete_candidate_count']}; floating singular candidates: "
        f"{s['singular_candidate_count']} from {s['singular_start_count']} direct starts.",
        f"The fixed-mu layer evaluated {s['common_terminal_problem_count']} problems and retained "
        f"{s['common_terminal_strict_root_count']} common-terminal roots.  Problems with two equal-norm roots: "
        f"{s['equal_norm_multiple_root_problem_count']}; observed order-preservation violations: "
        f"{s['equal_norm_order_preservation_violation_count']}.",
        "",
        "## Reflection and singularity diagnostics",
        "",
        f"Maximum relative `|q_sharp-q|`: {s['maximum_relative_q_reflection_defect']}.",
        f"Maximum normalized self-switch reflection defect: {s['maximum_self_switch_reflection_normalized_error']}.",
        f"Maximum `|h(h(q))-q|`: {s['maximum_abs_h_involution_defect']}.",
        f"Maximum independently replayed partner mirror defect: {s['maximum_partner_mirror_normalized_error']}.",
        f"Smallest sampled absolute normalized complete-root Jacobian determinant: "
        f"{s['minimum_abs_complete_normalized_jacobian_determinant']}.",
        "",
        "Every retained root passed the indexed terminal, equal-time, event-count, minimum-law, positivity, "
        "switch residual, transversality, terminal, energy, and capped/uncapped implementation gates.  "
        "Complete roots additionally passed the equal-norm gate.",
        "",
        "## Epistemic limit",
        "",
        "This is a finite binary64 search.  It can miss disconnected or narrow chambers, roots beyond the "
        "declared boxes, tangencies above the contact threshold, and near-grazing roots.  A null result is "
        "evidence only.  A witness still requires outward-rounded interval inclusion; a universal theorem "
        "still requires an exact global order, invariant, or complete subdivision bridge.",
        "",
        "Exact domains, seeds, tolerances, versions, all retained records, near misses, and replay metadata "
        "are in `results.json`; hashes are in `artifact_manifest.json`.",
    ]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scope", choices=("smoke", "full"), default="smoke")
    parser.add_argument("--workers", type=int, default=min(4, os.cpu_count() or 1))
    args = parser.parse_args()
    started = time.time()
    source_hashes = verify_sources()

    if args.scope == "smoke":
        delta_R_values = np.geomspace(1.0e-4, 1.0e4, 7)
        complete_starts = 12
        singular_starts = 16
    else:
        delta_R_values = np.unique(
            np.concatenate(
                (
                    np.geomspace(1.0e-6, 1.0e8, 29),
                    np.asarray([1.0e-4, 1.0e-2, 1.0e-1, 1.0, 9.0, 99.0, 9999.0, 999999.0]),
                )
            )
        )
        complete_starts = 48
        singular_starts = 160

    complete_rng = np.random.default_rng(MASTER_SEED)
    complete_cases: list[dict[str, Any]] = []
    continuation: list[np.ndarray] = []
    for index, delta in enumerate(delta_R_values):
        R = 1.0 + float(delta)
        case_rng = np.random.default_rng(MASTER_SEED + 1000 + index)
        case = solve_complete_case(2, R, complete_starts, case_rng, continuation)
        complete_cases.append(case)
        continuation = [np.asarray(root["encoded_root"], dtype=float) for root in case["roots"]]
        print(
            f"complete {index + 1}/{len(delta_R_values)} R={R:.8g} roots={len(case['roots'])}",
            flush=True,
        )

    singular = run_singular_search(
        singular_starts,
        complete_cases,
        max(1, min(int(args.workers), 4)),
        np.random.default_rng(MASTER_SEED + 17),
    )
    print(f"singular candidates={len(singular['candidates'])}", flush=True)

    common_tasks = make_common_tasks(args.scope, held_out=False)
    if args.scope == "full":
        common_tasks.extend(
            {
                "n": int(root["n"]), "R": float(root["R"]),
                "mu_override": float(root["mu"]),
                "q_count": 300, "q_minus_min": 1.0e-8,
                "q_minus_max": 1.0e6, "origin": "complete_root_anchor",
            }
            for case in complete_cases for root in case["roots"]
        )
    common_records = run_common_tasks(common_tasks, max(1, min(int(args.workers), 4)))
    print(
        f"common-terminal problems={len(common_records)} roots={sum(len(x['roots']) for x in common_records)}",
        flush=True,
    )

    complete_roots = [root for case in complete_cases for root in case["roots"]]
    asymmetric = [x for x in complete_roots if x["asymmetric_witness_predicate"]]
    conditioning_triggers = sorted(
        (
            root for root in complete_roots
            if (not root["derivative_stable"])
            or root["jacobian"]["minimum_abs_normalized_determinant"] <= 2.0e-4
        ),
        key=lambda root: root["jacobian"]["minimum_abs_normalized_determinant"],
    )[:12]
    trigger_candidates = asymmetric + singular["candidates"] + conditioning_triggers
    unique_triggers: dict[tuple[float, float, float], dict[str, Any]] = {}
    for root in trigger_candidates:
        unique_triggers[(float(root["R"]), float(root["mu"]), float(root["q"]))] = root
    trigger_candidates = list(unique_triggers.values())
    hp = high_precision_replay(trigger_candidates)

    held_records: list[dict[str, Any]] = []
    if args.scope == "full" and not (asymmetric or singular["candidates"]):
        held_records = run_common_tasks(
            make_common_tasks(args.scope, held_out=True),
            max(1, min(int(args.workers), 4)),
        )
        print(
            f"held-out problems={len(held_records)} roots={sum(len(x['roots']) for x in held_records)}",
            flush=True,
        )

    payload: dict[str, Any] = {
        "status_label": "COUNTEREXAMPLE_CANDIDATE" if asymmetric else "NUMERICAL_EVIDENCE",
        "run_id": "R-20260815T181317Z-min-reflection",
        "route_id": "MIN-REFL-C",
        "scope": args.scope,
        "context_id": "CTX-DEFAULT",
        "canonical_snapshot": {
            "blueprint_sha256": "sha256:76346e2fa9f880fd8c1c02bf4b001b38cb66f2f4688c8497c9d764ebb746c7a7",
            "inventory_sha256": "sha256:b6286574edbcb70ad22e5c6758a81f00dd01572c0764b8816be23cb6b166fb6f",
        },
        "source_hashes": source_hashes,
        "runtime": {
            "python": sys.version,
            "python_executable": sys.executable,
            "platform": platform.platform(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "mpmath": mp.__version__,
            "workers": max(1, min(int(args.workers), 4)),
        },
        "seeds": {
            "master": MASTER_SEED,
            "complete_case_rule": "MASTER_SEED+1000+case_index",
            "singular": MASTER_SEED + 17,
        },
        "complete_search": {
            "parameter_domain": {
                "n": [2], "mode": [MODE],
                "delta_R": [float(delta_R_values[0]), float(delta_R_values[-1]), len(delta_R_values), "geometric"],
                "a": [A_MIN, A_MAX], "xq": [XQ_MIN, XQ_MAX],
                "starts_per_contrast": complete_starts,
            },
            "cases": complete_cases,
        },
        "singular_search": singular,
        "common_terminal_search": {
            "tasks": common_tasks,
            "records": common_records,
        },
        "held_out_search": {
            "triggered": bool(held_records),
            "records": held_records,
        },
        "high_precision_replay": hp,
        "elapsed_seconds": time.time() - started,
        "blind_spots": [
            "finite parameter boxes and multistarts are not complete",
            "binary64 and mpmath are not outward-rounded interval arithmetic",
            "disconnected or narrow relay chambers can be missed",
            "contact scout requires a sampled local abs(A) minimum below 2e-3",
            "imported evaluators may share an implementation bug",
        ],
        "proof_bridge": "exact global order/invariant or complete interval subdivision",
        "refutation_bridge": "outward-rounded interval root inclusion plus every premise and asymmetry predicate",
    }
    payload["high_precision_cluster_reconciliation"] = reconcile_high_precision_clusters(
        complete_cases, hp
    )
    payload["summary"] = summarize(payload)
    write_json(RESULTS, payload)
    write_report(payload)
    manifest = {
        "status_label": payload["status_label"],
        "generated_at_unix": time.time(),
        "files": {
            CONTRACT.name: f"sha256:{sha256_file(CONTRACT)}",
            ADDENDUM.name: f"sha256:{sha256_file(ADDENDUM)}",
            Path(__file__).name: f"sha256:{sha256_file(Path(__file__))}",
            RESULTS.name: f"sha256:{sha256_file(RESULTS)}",
            REPORT.name: f"sha256:{sha256_file(REPORT)}",
        },
        "source_hashes": source_hashes,
        "replay": (
            f"{sys.executable} {Path(__file__).relative_to(PROJECT)} "
            f"--scope {args.scope} --workers {max(1, min(int(args.workers), 4))}"
        ),
    }
    write_json(MANIFEST, manifest)
    print(json.dumps(finite_json(payload["summary"]), indent=2, sort_keys=True), flush=True)
    print(f"results sha256:{sha256_file(RESULTS)}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
