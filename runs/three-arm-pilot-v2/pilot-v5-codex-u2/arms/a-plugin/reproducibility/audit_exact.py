#!/usr/bin/env python3
"""Exact finite audits for U2-TV identities; finite checks are not proofs."""

from collections import defaultdict
from math import comb
import sys


def translated_l1(table, shift):
    keys = set(table)
    keys.update(tuple(x + d for x, d in zip(k, shift)) for k in table)
    return sum(
        abs(table.get(k, 0) - table.get(tuple(x - d for x, d in zip(k, shift)), 0))
        for k in keys
    )


def central_count(t):
    return comb(t, t // 2)


def main():
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    triples = {(0, 0, 0): 1}
    expected_numerators = [2, 4, 8, 14, 28, 50, 100]
    for t in range(limit + 1):
        triple_l1 = translated_l1(triples, (2, 2, 2))
        if t < len(expected_numerators):
            assert triple_l1 == expected_numerators[t]
        # The computation-supported AVI target, checked only on this finite domain.
        assert triple_l1 <= 8 * central_count(t)

        lower_endpoint = defaultdict(int)
        upper_endpoint = defaultdict(int)
        for (lo, hi, z), n in triples.items():
            lower_endpoint[(lo, z)] += n
            upper_endpoint[(hi, z)] += n
        one_sided_l1 = translated_l1(lower_endpoint, (2, 2))
        other_l1 = translated_l1(upper_endpoint, (2, 2))
        assert one_sided_l1 == other_l1
        # The path-specific marginal-comparison conjecture, again only finite evidence.
        assert triple_l1 <= one_sided_l1 + other_l1

        if t == limit:
            break
        nxt = defaultdict(int)
        for (lo, hi, z), n in triples.items():
            for dz in (-1, 1):
                w = z + dz
                nxt[(min(lo, w), max(hi, w), w)] += n
        triples = dict(nxt)
    print(f"PASS exact finite identities and conjecture probes for 0<=t<={limit}")


if __name__ == "__main__":
    main()
