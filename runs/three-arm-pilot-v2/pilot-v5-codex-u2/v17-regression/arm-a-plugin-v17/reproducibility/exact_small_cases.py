#!/usr/bin/env python3
"""Exact small-case probes for the frozen switch-walk-switch chain.

Mathematical objects returned:
  (i) integer path counts for (minimum, maximum, endpoint), and
  (ii) integer transition counts for full (finite lamp support, endpoint) states.
Property checked exactly:
  TV distance from the spatial translate by two, plus sqrt(t)*TV.
Objective/penalty:
  no optimization and no invalid states admitted.
Parameter domain:
  integer 0 <= t <= command-line bound (defaults: triples 80, full states 12).
Arithmetic:
  exact integer counts; only the displayed decimal quotient/square root is floating point.
Time/memory:
  caller-controlled; intended for small cases.
Random seeds:
  none.
Certificate:
  printed integer L1 numerator and common denominator.
Proof bridge:
  none by itself; this script only falsifies candidate constants/scales and checks conventions.
Known blind spot:
  finite survival cannot prove a uniform asymptotic estimate.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from math import sqrt


def translated_triple_tv(max_t: int) -> None:
    d = {(0, 0, 0): 1}
    for t in range(max_t + 1):
        translated = {(lo + 2, hi + 2, z + 2): n for (lo, hi, z), n in d.items()}
        keys = d.keys() | translated.keys()
        l1_num = sum(abs(d.get(k, 0) - translated.get(k, 0)) for k in keys)
        tv_num, tv_den = l1_num, 2 * (2**t)
        if t <= 20 or t in {30, 40, 60, 80, max_t}:
            print(f"triple t={t:3d} l1_num={tv_num} den={tv_den} "
                  f"tv={tv_num/tv_den:.12f} sqrt_t_tv={sqrt(t)*tv_num/tv_den if t else 0:.12f}")
        if t == max_t:
            break
        nd = defaultdict(int)
        for (lo, hi, z), n in d.items():
            for dz in (-1, 1):
                w = z + dz
                nd[(min(lo, w), max(hi, w), w)] += n
        d = dict(nd)


def shifted_state(state: tuple[frozenset[int], int], amount: int = 2):
    lamps, z = state
    return frozenset(k + amount for k in lamps), z + amount


def full_state_tv(max_t: int) -> None:
    d = {(frozenset(), 0): 1}
    for t in range(max_t + 1):
        translated = {shifted_state(k): n for k, n in d.items()}
        keys = d.keys() | translated.keys()
        l1_num = sum(abs(d.get(k, 0) - translated.get(k, 0)) for k in keys)
        tv_num, tv_den = l1_num, 2 * (8**t)
        print(f"full   t={t:3d} states={len(d):8d} l1_num={tv_num} den={tv_den} "
              f"tv={tv_num/tv_den:.12f} sqrt_t_tv={sqrt(t)*tv_num/tv_den if t else 0:.12f}")
        if t == max_t:
            break
        nd = defaultdict(int)
        for (lamps, z), n in d.items():
            for dz in (-1, 1):
                w = z + dz
                for a in (0, 1):
                    after_a = set(lamps)
                    if a:
                        after_a.add(z)
                    else:
                        after_a.discard(z)
                    for b in (0, 1):
                        after_b = set(after_a)
                        if b:
                            after_b.add(w)
                        else:
                            after_b.discard(w)
                        nd[(frozenset(after_b), w)] += n
        d = dict(nd)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--triple-max", type=int, default=80)
    parser.add_argument("--full-max", type=int, default=12)
    args = parser.parse_args()
    translated_triple_tv(args.triple_max)
    full_state_tv(args.full_max)


if __name__ == "__main__":
    main()
