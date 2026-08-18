# Approach Registry: R-20260816T220000Z-densbc-o1p2

Task: Q-20260816-densbc-o1p2-F1A2B3C4

## Route families

### Route A: general banded-Gram finite reduction
- State: PARTIAL / BLOCKED for full generality.
- Idea: assume G_{i,k} = 0 for |i-k| > m and finite polynomial representers;
  prove N cofinite, finite free bases, and reduce O1' to a finite matrix.
- What succeeded:
  - N cofinite (banded Gram + finite polynomial representers).
  - Run/free-base system finite.
  - Membership part is a finite matrix T.
- Exact gap:
  - Realizability of infinite run moment sequences is not finite in arbitrary
    banded H.  H_beta uses explicit diagonal summability; general banded H
    needs a moment-problem condition (e.g. Riesz-basis/banded-inverse data).
- Verdict: not closed; folded into the concrete H_lambda route.

### Route B: concrete non-diagonal example H_lambda
- State: SUCCEEDED for the exact subclass H_lambda + finite polynomial
  representers, including v_1 = x^4 for all lambda in (-1,1).
- Idea: choose a Hilbert space with explicit banded Gram and explicit moment-map
  isomorphism, so realizability is exactly l^2 summability.
- What succeeded:
  - Exact finite-rank criterion: density iff ker(T|_{B_fin}) = {0}.
  - Complete non-density decision for v_1 = x^4 with explicit obstruction.
- Remaining:
  - H_lambda is one family; general H remains open.
  - Whether a single representer in H_lambda can make density hold was searched
    heuristically but not resolved/proven (no candidate found in grid search).

### Route C: weighted L^2 non-banded examples
- State: NOT pursued in this run.
- Note: in general weighted L^2, finite-support moment sequences need not be
  realizable; the moment problem is genuinely infinite-dimensional.  This is
  why H_lambda was chosen.

## Provenance
- Uses upstream Theorems A and run-machinery from R0/R1.
- No external literature search performed in this run; novelty is relative to
  the audited internal runs only.
