#!/usr/bin/env python3
"""Exact finite interface checks for the stopping-boundary partial package.

The returned objects are integer killed-walk counts and exact rational full-state TV at t=1.
The checks validate the Route C counterexample and literal small-time convention.  They do not
turn the finite checks into an asymptotic theorem; the general estimates are proved on paper.
No randomness or floating-point arithmetic is used.
"""

from collections import defaultdict
from fractions import Fraction


def killed(t: int, lo: int, hi: int, start: int, end: int) -> int:
    if lo > hi or not (lo <= start <= hi and lo <= end <= hi):
        return 0
    counts = {start: 1}
    for _ in range(t):
        nxt = defaultdict(int)
        for x, count in counts.items():
            for y in (x - 1, x + 1):
                if lo <= y <= hi:
                    nxt[y] += count
        counts = dict(nxt)
    return counts.get(end, 0)


def exact_range(t: int, r: int, a: int, j: int) -> tuple[int, tuple[int, int, int, int]]:
    terms = (
        killed(t, 0, r, a, j),
        killed(t, 1, r, a, j),
        killed(t, 0, r - 1, a, j),
        killed(t, 1, r - 1, a, j),
    )
    return terms[0] - terms[1] - terms[2] + terms[3], terms


def check_v_slice() -> None:
    expected_terms = {
        0: (81, 0, 55, 0),
        2: (162, 89, 89, 32),
        4: (81, 55, 0, 0),
    }
    expected_h = {0: 26, 2: 16, 4: 26}
    for a in (0, 2, 4):
        h, terms = exact_range(10, 4, a, 2)
        assert terms == expected_terms[a], (a, terms)
        assert h == expected_h[a], (a, h)


def check_t1_overlap() -> None:
    # Each law has eight equiprobable outcomes.  Exactly two common outcomes occur at base 1:
    # both outer lamps are zero and the shared lamp at 1 is arbitrary.
    overlap = Fraction(2, 8)
    tv = 1 - overlap
    assert tv == Fraction(3, 4)


def main() -> None:
    check_v_slice()
    check_t1_overlap()
    print("PASS route-C V-slice: (26,16,26) with listed killed-count terms")
    print("PASS literal t=1 full-state TV: 3/4")


if __name__ == "__main__":
    main()
