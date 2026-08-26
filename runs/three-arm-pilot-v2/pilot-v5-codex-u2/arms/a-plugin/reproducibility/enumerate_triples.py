#!/usr/bin/env python3
"""Exact integer enumeration of simple-walk range triples.

Mathematical object: counts of length-t sign sequences by (minimum, maximum,
endpoint), for a walk started at zero.  Property checked exactly: the L1
difference between this count table and its diagonal translate by 2.  The
objective is identity discovery/falsification, never a theorem.  Domain is
t=0..the command-line limit; arithmetic is exact Python integers; there is no
randomness and no seed.  The count table itself is a replayable certificate.
"""

from collections import defaultdict
from math import sqrt
import sys


def step_counts(limit: int):
    counts = {(0, 0, 0): 1}
    yield 0, counts
    for t in range(1, limit + 1):
        nxt = defaultdict(int)
        for (lo, hi, z), n in counts.items():
            for dz in (-1, 1):
                w = z + dz
                nxt[(min(lo, w), max(hi, w), w)] += n
        counts = dict(nxt)
        yield t, counts


def triple_tv_numerator(counts):
    keys = set(counts)
    keys.update((lo + 2, hi + 2, z + 2) for lo, hi, z in counts)
    return sum(
        abs(counts.get(key, 0) - counts.get((key[0] - 2, key[1] - 2, key[2] - 2), 0))
        for key in keys
    )


def main():
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    print("t states numerator TV sqrt(t)*TV")
    for t, counts in step_counts(limit):
        num = triple_tv_numerator(counts)
        tv = num / (2 * (1 << t))
        scaled = sqrt(t) * tv if t else 0.0
        print(t, len(counts), num, f"{tv:.12g}", f"{scaled:.12g}")


if __name__ == "__main__":
    main()
