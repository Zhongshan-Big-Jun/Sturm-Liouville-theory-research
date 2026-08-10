# Counterexample log

Run: R-20260806T070000Z-keylemma2b-0A6D8F

Purpose: record every serious attempt to falsify the claimed lemmas and the
precise mechanism of each failure.  The KEY LEMMA is claimed for all
q > 1, c in (0, 1/2); the lemmas R1, R2, L4box, L5box and the analytic parts
M2, CORNER, C4 were attacked.

## Attempts that failed to produce a counterexample (all confirmed claims)

1. Random and adversarial sampling of sign(G2) vs sign(IN): 300-500 points per
   region at 50-90 digits.  0 mismatches.  (Claim: sign identity.)
2. Random sampling of the u = tan(c A) parametrization identity:
   300 points including q -> 1+ and q -> 1e3, c -> 0+.  0 mismatches.
   (Note: my first fresh-audit script produced two false failures here because
   its alpha2 bisection upper bound 3.14 was below pi; fixed in v2, see
   research_ledger.md entry 4.  This was a script bug, not a mathematical
   counterexample.)
3. CORNER closed form at q in {2, 2.01, 3, 10, 1e3, 1e6}: exact match.
4. C4 curve identity IN = A*K(v) on 300 random v in [2pi/7, 2pi/5 - 1e-3]:
   0 mismatches.
5. R1 region (q >= 2, c in (0, 1/2)): 600 random points, 0 negatives
   (G2 < -1e-12).  Tightest value 0.069181 at (2, 1/2).
6. R2 region (q > 1, c in (0, 0.4]): 600 random points including q -> 1e4,
   0 negatives.  Tightest value 0.413609 at (1, 0.4).
7. Box (1,2) x (0.4, 0.5): H > 0 and Ftilde' < 0 on 500 random points,
   0 violations.  Edge points (q,c) = (1.0000000001, 0.499999999),
   (1.9999999999, 0.499999999), (1.05, 0.5), (1.5, 0.45) all satisfy
   (LOG) and (FP).
8. L4box H' < 0 and L5box F~'' > 0: 300 random box points with direct finite
   differences, 0 violations; both interval certificates (128 leaves each)
   pass both engines.
9. C4 tail: 500 random v in the tail with the T^3 K identity, 0 violations;
   the exact rational lower bound 178.85896 > 0 settles the tail leg.
10. Edge regimes: q -> 1+ with c -> 1/2- (G2 = -0.3877 < 0, i.e. Region B is
    nonempty, but H = 2.418 > 0 and Fp = -0.688 < 0 hold); q -> 1e6 with
    c in {1e-6, 0.4, 0.499}; c -> 0+.  0 violations of the KEY LEMMA.

## Confirmed counterexamples to ROUTES (not to the theorem)

1. dG2/dc <= 0 globally: REFUTED (predecessor ledger entry 2).  dG2/dc is
   positive for q in (30, 100), c in (0.3, 0.45).  The R1-via-dG2/dc route is
   dead.  Recorded in approach_registry.md.
2. The task packet's product-of-tangents odd secular equation: FALSE
   (origin report Section 2.1 and this run's contract).  The corrected form is
   q tan(alpha_2) + tan(c alpha_2) = 0.  Both forms were checked against the
   transfer-matrix solver in the origin run.
3. The C4 symbolic reduction to 0: FAILED in sympy (leftover atan(tan(...))
   terms).  Not a mathematical counterexample; documented as a verification
   caveat.  The identity is verified numerically and by certified re-evaluations.

## Status

No counterexample to the KEY LEMMA or to any of its premises (L1, L2, B4, B5,
B7, R1, R2, L4box, L5box, M2, CORNER, C4) was found.  The tested domain is
described in each item; universal truth is not inferred from these samples - the
proof obligations are closed by the analytic arguments and the certified
interval legs listed in obligation_graph.md.
