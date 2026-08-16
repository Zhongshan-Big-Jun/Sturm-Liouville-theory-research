#!/usr/bin/env python3
"""Audit the frozen MIN-REFL-C numerical result without rerunning the search."""

from __future__ import annotations

import hashlib
import json
import math
from decimal import Decimal
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[3]
RESULTS = HERE / "results.json"
OUTPUT = HERE / "audit.json"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    payload = json.loads(RESULTS.read_text(encoding="utf-8"), parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
    complete = [root for case in payload["complete_search"]["cases"] for root in case["roots"]]
    common = [root for rec in payload["common_terminal_search"]["records"] for root in rec["roots"]]
    held = [root for rec in payload["held_out_search"]["records"] for root in rec["roots"]]
    all_roots = complete + common + held
    hp_lookup = {
        (float(x["R"]), float(x["mu"]), float(x["q"])): x
        for x in payload["high_precision_replay"]
    }

    def partner_valid_or_hp(root):
        if root["reflection"].get("partner_valid"):
            return True
        hp = hp_lookup.get((float(root["R"]), float(root["mu"]), float(root["q"])))
        if not hp or not hp.get("reflection_replay"):
            return False
        replay = hp["reflection_replay"]
        return bool(
            abs(Decimal(replay["partner_terminal_gap_scaled"])) <= Decimal("1e-50")
            and abs(Decimal(replay["partner_log_integral_ratio"])) <= Decimal("1e-50")
            and abs(Decimal(replay["h_h_q_minus_q"])) <= Decimal("1e-50")
        )

    source_checks = {}
    for relative, recorded in payload["source_hashes"].items():
        actual = f"sha256:{sha256_file(PROJECT / relative)}"
        source_checks[relative] = {"recorded": recorded, "actual": actual, "match": actual == recorded}

    checks = {
        "strict_json_parse": True,
        "source_hashes_match": all(x["match"] for x in source_checks.values()),
        "all_roots_strict_valid": all(x["strict_valid"] for x in all_roots),
        "all_event_counts_exact": all(x["event_count"] == 2 * x["n"] for x in all_roots),
        "all_terminal_indices_exact": all(x["zero_counts"] == [x["n"], x["n"] + 1] for x in all_roots),
        "all_minimum_law_checks_pass": all(x["minimum_law_ok"] and x["alternation_ok"] for x in all_roots),
        "all_implementation_crosschecks_pass": all(x["implementation_crosscheck_pass"] for x in all_roots),
        "all_complete_norm_residuals_pass": all(abs(x["C_log_integral_ratio"]) <= 5.0e-9 for x in complete),
        "all_common_terminal_residuals_pass": all(abs(x["A_scaled"]) <= 5.0e-9 for x in all_roots),
        "all_reflection_partners_valid_or_hp_replayed": all(partner_valid_or_hp(x) for x in all_roots),
        "no_asymmetric_complete_candidate": not any(x["asymmetric_witness_predicate"] for x in complete),
        "no_singular_candidate": payload["singular_search"]["floating_candidate_count"] == 0,
        "all_hp_replays_ok": all(x.get("replay", {}).get("status") == "ok" for x in payload["high_precision_replay"]),
        "all_hp_reflection_replays_present": all(x.get("reflection_replay") for x in payload["high_precision_replay"]),
        "hp_multiple_clusters_reconciled": payload["high_precision_cluster_reconciliation"]["unresolved_multiple_root_case_count"] == 0,
    }
    counts = {
        "complete_binary_records": len(complete),
        "complete_reconciled_roots": payload["high_precision_cluster_reconciliation"]["reconciled_complete_root_count"],
        "common_terminal_roots": len(common),
        "held_out_roots": len(held),
        "high_precision_replays": len(payload["high_precision_replay"]),
        "binary_reflection_partner_invalid_records": sum(
            not x["reflection"].get("partner_valid") for x in all_roots
        ),
    }
    summary = payload["summary"]
    count_checks = {
        "complete_binary": counts["complete_binary_records"] == summary["complete_strict_binary_root_record_count"],
        "complete_reconciled": counts["complete_reconciled_roots"] == summary["complete_reconciled_root_count"],
        "common": counts["common_terminal_roots"] == summary["common_terminal_strict_root_count"],
        "held": counts["held_out_roots"] == summary["held_out_root_count"],
        "hp": counts["high_precision_replays"] == summary["high_precision_replay_count"],
    }
    checks["all_count_checks_pass"] = all(count_checks.values())
    verdict = "PASS" if all(checks.values()) else "FAIL"
    result = {
        "status_label": "NUMERICAL_EVIDENCE",
        "audit_verdict": verdict,
        "results_sha256": f"sha256:{sha256_file(RESULTS)}",
        "checks": checks,
        "counts": counts,
        "count_checks": count_checks,
        "source_checks": source_checks,
        "scope_warning": "Internal reproducibility/consistency audit only; not interval certification or a universal proof.",
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
