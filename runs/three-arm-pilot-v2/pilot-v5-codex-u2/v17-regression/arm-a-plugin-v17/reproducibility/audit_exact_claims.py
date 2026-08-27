#!/usr/bin/env python3
"""Exact finite replay for the v1.7 regression claims.

This script checks displayed identities and boundary conventions on a finite
domain. It is EVIDENCE and is not a proof of an asymptotic assertion.
"""

from collections import defaultdict
from fractions import Fraction
from math import comb, floor, sqrt


def step_triples(counts):
	next_counts = defaultdict(int)
	for (lower, upper, endpoint), multiplicity in counts.items():
		for increment in (-1, 1):
			new_endpoint = endpoint + increment
			next_counts[(min(lower, new_endpoint), max(upper, new_endpoint), new_endpoint)] += multiplicity
	return dict(next_counts)


def step_states(counts):
	next_counts = defaultdict(int)
	for (lamps, endpoint), multiplicity in counts.items():
		for increment in (-1, 1):
			new_endpoint = endpoint + increment
			for departure_bit in (0, 1):
				after_departure = set(lamps)
				if departure_bit:
					after_departure.add(endpoint)
				else:
					after_departure.discard(endpoint)
				for arrival_bit in (0, 1):
					after_arrival = set(after_departure)
					if arrival_bit:
						after_arrival.add(new_endpoint)
					else:
						after_arrival.discard(new_endpoint)
					next_counts[(frozenset(after_arrival), new_endpoint)] += multiplicity
	return dict(next_counts)


def translate_state(state, amount=2):
	lamps, endpoint = state
	return frozenset(site + amount for site in lamps), endpoint + amount


def visible_hull(state):
	lamps, endpoint = state
	support = set(lamps)
	support.add(endpoint)
	return min(support), max(support), endpoint


def tv_from_probability_tables(left, right):
	keys = set(left) | set(right)
	return sum(abs(left.get(key, 0) - right.get(key, 0)) for key in keys) / 2


def exact_range_mass(triples, start, state, time):
	lamps, endpoint = state
	anchors = set(lamps) | {start, endpoint}
	lower_anchor = min(anchors)
	upper_anchor = max(anchors)
	mass = Fraction(0)
	for (lower, upper, final_endpoint), multiplicity in triples.items():
		if final_endpoint != endpoint:
			continue
		if lower <= lower_anchor and upper >= upper_anchor:
			mass += Fraction(multiplicity, (2**time) * (2 ** (upper - lower + 1)))
	return mass


def audit_state_formula_and_visible_hull(limit=8):
	triples = {(0, 0, 0): 1}
	states = {(frozenset(), 0): 1}
	for time in range(limit + 1):
		if time >= 1:
			probability = {state: Fraction(count, 8**time) for state, count in states.items()}
			for state, mass in probability.items():
				assert mass == exact_range_mass(triples, 0, state, time)

			translated = {translate_state(state): mass for state, mass in probability.items()}
			full_tv = tv_from_probability_tables(probability, translated)
			left_hull = defaultdict(Fraction)
			right_hull = defaultdict(Fraction)
			for state, mass in probability.items():
				left_hull[visible_hull(state)] += mass
			for state, mass in translated.items():
				right_hull[visible_hull(state)] += mass
			assert full_tv == tv_from_probability_tables(left_hull, right_hull)
		if time < limit:
			triples = step_triples(triples)
			states = step_states(states)


def audit_endpoint_lower(limit=1000):
	for time in range(1, limit + 1):
		maximum_atom = Fraction(comb(time, floor(time / 2)), 2**time)
		assert float(maximum_atom) >= 1 / (4 * sqrt(time))


def translated_triple_tv(counts, time):
	translated = {(lower + 2, upper + 2, endpoint + 2): count
				  for (lower, upper, endpoint), count in counts.items()}
	keys = set(counts) | set(translated)
	l1 = sum(abs(counts.get(key, 0) - translated.get(key, 0)) for key in keys)
	return Fraction(l1, 2 * (2**time))


def harmonic(number):
	return sum((Fraction(1, index) for index in range(1, number + 1)), Fraction(0))


def audit_route_a_upper(limit=120):
	triples = {(0, 0, 0): 1}
	for time in range(limit + 1):
		if time >= 2:
			half = floor(time / 2)
			bound_float = 1 / sqrt(half + 1) + 2 * float(harmonic(half + 1)) / sqrt(time - half + 1)
			assert float(translated_triple_tv(triples, time)) <= bound_float + 1e-15
		if time < limit:
			triples = step_triples(triples)


def exact_h_value(time, width, start_offset, end_offset):
	triples = {(0, 0, 0): 1}
	for _ in range(time):
		triples = step_triples(triples)
	return triples.get((-start_offset, width - start_offset, end_offset - start_offset), 0)


def audit_route_c_counterexample():
	values = [exact_h_value(10, 4, offset, 2) for offset in (0, 2, 4)]
	assert values == [26, 16, 26]


def main():
	audit_state_formula_and_visible_hull()
	audit_endpoint_lower()
	audit_route_a_upper()
	audit_route_c_counterexample()
	print("PASS exact finite replay")
	print("state formula and visible-hull equality: 1<=t<=8")
	print("endpoint lower bound: 1<=t<=1000")
	print("Route A displayed upper bound: 2<=t<=120")
	print("Route C counterexample: h_10^4(a,2)=(26,16,26) for a=(0,2,4)")


if __name__ == "__main__":
	main()
