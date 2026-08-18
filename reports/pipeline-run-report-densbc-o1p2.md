# Pipeline run report: DensBC O1' round 2

- Date: 2026-08-16
- Run ID: R-20260816T220000Z-densbc-o1p2
- Task packet: Q-20260816-densbc-o1p2-F1A2B3C4
- Status: (to be filled after solver returns)

## Purpose of this round

1. Continue DensBC O1' beyond the diagonal subclass (banded / finitely
   supported representer-moment extension).
2. Run a plugin performance test and identify optimization points that prevent
   detours and avoid re-inventing the wheel.

## Performance test summary

See `reports/plugin-performance-test-round2.md`. Key findings:
- `lean-proof/LEMMA_INDEX.md` was missing before this round; regenerated
  (487 declarations) for reuse.
- `research_map.md` is the cheap entry point (117 lines) vs full proofs
  (15KB+); agents should default to it and read proofs on demand.
- Duplicate/colliding audit reports and overlapping registration files can be
  canonicalized.
- Token budget should be operational (budget_state.json + safe-boundary checks).

## O1' continuation outcome

Status: RIGOROUS_PARTIAL_RESULT (subclass closed; general O1' open).

New STRICT result (this round):
- H_lambda = l^2(N_0) with x^k = e_k + lambda e_{k+1}, lambda in (-1,1): a
  genuinely non-diagonal, banded (bandwidth 1) Hilbert space with an explicit
  moment map J(w)_k = w_k + lambda w_{k+1}, invertible with
  w_k = sum_{j>=0} (-lambda)^j M_{k+j}.
- For finite polynomial representers (r finite, d_j finite), the kept set N is
  cofinite and O1' reduces to a finite linear algebra condition:
  closure(span Q_sp) = V  <=>  ker(T|_{B_fin}) = {0}.
- Concrete case v_1 = x^4: the sparse family is NOT dense in V for every
  lambda in (-1,1), with explicit obstruction w = lambda^2 e_0 - lambda e_1 +
  e_2 (M_2 = 1, all other kept moments zero).

## Bugs / issues this round

- Two independent audits both found the same arithmetic typo: in the kept-set
  computation for p_7 the sparse coefficient was written 4/3 instead of 3/2
  (p_7 = x^7 - (3/2) x^5). The conclusion (7 notin N when lambda != 0) is
  unchanged, but the STRICT line was wrong. Fixed in candidate_proof.md.
- 5 small omissions flagged by the second audit: explicit pinned {0,1} handling
  in the Theorem 2 converse, injectivity of the t <-> w maps (density of Pi),
  explicit r/d_j finiteness, and a reworded {0,1} sentence in Theorem 1. All
  repaired.

## Unexpected behaviors / judgments

- Positive: both audits converged on "main architecture sound"; the only real
  slip was one arithmetic typo, and it did not change any conclusion. The
  double audit caught the same issue twice - evidence that cross-checking
  works, and also a hint that audit results should be deduplicated (P2 in the
  performance report).
- Positive: the solver returned a concrete explicit obstruction and a negative
  exploratory search (EVIDENCE only, recorded to avoid repeating the search).
- Good: status honestly labeled RIGOROUS_PARTIAL_RESULT; general O1' left open.
- Note: the performance optimization points (P1-P6) identified in
  `reports/plugin-performance-test-round2.md` were applied partially this
  round (LEMMA_INDEX regenerated, research map updated, lightweight entry
  point used); remaining items are plugin-level workflow changes.
