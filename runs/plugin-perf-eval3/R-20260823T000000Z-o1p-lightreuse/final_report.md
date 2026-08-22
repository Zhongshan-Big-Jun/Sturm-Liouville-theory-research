# Final Report: O1' on H_{beta,lambda}

Status label: RIGOROUS_PARTIAL_RESULT
Run root: F:\LaTeX\BVE research\runs\plugin-perf-eval3\R-20260823T000000Z-o1p-lightreuse

## Summary

This run proves a STRICT exact criterion for the reduced core O1' on a new
non-diagonal weighted shift family

    H_{beta,lambda} = l^2(N_0),   x^k = (k+1)^beta e_k + lambda e_{k+1},
    beta >= 0, lambda in (-1,1),

with finite polynomial representers.  The criterion is

    closure(span Q_sp) = V
        <=>
    ker( T|_{B_adm} ) = {0},

where B_adm includes all finite-run free bases and also the infinite-run
free bases exactly when beta > 3/2.

This is a strict interpolation between the two previously closed subclasses:
lambda = 0 gives H_beta (R-20260816T210000Z), and beta = 0 gives H_lambda
(R-20260816T220000Z).  It therefore goes beyond the previously closed
bandwidth-1 non-diagonal subclass in the weighted direction, while keeping
the finite/infinite admissibility split of H_beta.

The parallel baseline run (R-20260823T000000Z-o1p-baseline) proved a
complementary criterion for stable banded-shift Toeplitz spaces
H_shift(m,lambda).  The two new families overlap at beta = 0, m = 1
(H_lambda); otherwise this run's weighted family is not covered by the
baseline's Toeplitz criterion.

## New STRICT statements

1. Theorem 1: N is cofinite in H_{beta,lambda}; finite run system.
2. Theorem 2: moment parameterization of V cap Q_sp^perp.
3. Lemma 3: a single infinite-run moment vector (and any nonzero combination
   of the even/odd infinite-run vectors) is realizable iff beta > 3/2.
4. Corollary 4: finite-support moment sequences are always realizable.
5. Theorem 5: exact O1' criterion = ker(T|_{B_adm}) = {0}.
6. Concrete example v_1 = x^4: non-density for every beta >= 0,
   lambda in (-1,1).

## What is not claimed

- General O1' is not closed.
- General banded or arbitrary non-diagonal H is not closed.
- The abstract moment-problem core remains open.

## Artifacts

All required minimum artifacts were written:
problem_contract.md, status_and_literature.md, approach_registry.md,
research_ledger.md, obligation_graph.md, candidate_proof.md,
escalation_ladder.md, audit_report.md (explicit self-audit note),
performance_log.md, final_report.md, plus reuse_summary.md.
