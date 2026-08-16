#!/usr/bin/env python3
"""Run the frozen conditional R17 contractor on exact boundary intersections."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve()
PROJECT = HERE.parents[4]
UPSTREAM = PROJECT / "runs/R-20260815T181317Z-min-reflection/routes/event_inertia/cover_collar.py"
SPEC = importlib.util.spec_from_file_location("cover_collar", UPSTREAM)
assert SPEC and SPEC.loader
COVER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(COVER)

TARGETS = (
    "LIL", "LIH", "HIL", "HIH",
    "LHL", "LHI", "LHH", "IHL", "IHH", "HHL", "HHI", "HHH",
)


def state_interval(state: str, den: int) -> tuple[int, int]:
    collar = den // 64
    if state == "L":
        return 0, collar
    if state == "I":
        return collar, den - collar
    if state == "H":
        return den - collar, den
    raise ValueError(state)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("codes", nargs="+", choices=TARGETS)
    parser.add_argument("--max-boxes", type=int, default=500_000)
    args = parser.parse_args()
    den = COVER.R17.DEN
    results = {}
    exit_code = 0
    for code in args.codes:
        root = tuple(state_interval(letter, den) for letter in code)
        result = COVER.run(root, args.max_boxes)
        results[code] = result
        if not result["complete"]:
            exit_code = 2
    print(json.dumps({"targets": args.codes, "results": results}, indent=2))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())

