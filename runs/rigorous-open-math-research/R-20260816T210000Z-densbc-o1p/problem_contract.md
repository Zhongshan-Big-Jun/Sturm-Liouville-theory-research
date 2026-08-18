# Problem Contract: DensBC O1' on H_beta with finite polynomial constraint data

Run root: runs/rigorous-open-math-research/R-20260816T210000Z-densbc-o1p/
Task packet: Q-20260816-densbc-o1p-F6E7D8A9
Upstream: R-20260816T000000Z-densbc-o1 (status RIGOROUS_PARTIAL_RESULT; reduced core O1' open)

## Chosen structured subclass

We do NOT attempt O1' in full generality.  We fix the following subclass:

- H = H_beta, beta >= 0, the diagonal weighted sequence space:
  elements w = (w_k)_{k>=0} with ||w||_beta^2 = Sum_k |w_k|^2 (k+1)^{2 beta} < inf,
  inner product <w,v>_beta = Sum_k w_k \overline{v_k} (k+1)^{2 beta},
  monomial x^k = e_k.  Moments: M_k(w) = <w,x^k>_beta = w_k (k+1)^{2 beta}.
- Constraints are finite polynomial moment conditions:
  L_j(w) = Sum_{k=0}^{d_j} c^{(j)}_k M_k(w),  j=1..r,
  with d_j finite and the coefficient vectors linearly independent.
  V = Intersection_{j=1..r} ker L_j.
  Equivalently each Riesz representer v_j = Sum_{k=0}^{d_j} \overline{c^{(j)}_k} x^k
  is a polynomial of degree at most d_j.
- The sparse family p_0=1, p_1=x, p_{2m}=x^{2m}-(m/(m-1))x^{2m-2},
  p_{2m+1}=x^{2m+1}-(m/(m-1))x^{2m-1} (m>=2), and Q_sp = {p_n : p_n in V}.

## Why this subclass is the right next step

1. It contains the audited coordinate/diagonal Theorem E as the special case
   where each L_j is a coordinate moment condition.
2. It is the simplest non-coordinate case in which the representer moments
   a^{(j)}_k = <v_j,x^k> are finitely supported; hence the kept set N is
   cofinite and the run system is finite.
3. The moment-realization step of O1' becomes a finite-dimensional linear
   algebra condition together with a one-parameter summability threshold
   beta <= 3/2 vs beta > 3/2.

## Target conclusion for this run

Prove an exact, verifiable decision criterion on this subclass:

    closure(span Q_sp) = V

in terms of
- the finite run decomposition of the kept sparse family,
- the finite matrix A = (c^{(j)}_k)_{j,k} of the moment constraints,
- and the summability classification of each run (finite, or infinite with
  beta <= 3/2, or infinite with beta > 3/2).

This closes O1' on this subclass.  It does NOT claim to close O1' for general
non-diagonal H, arbitrary bounded representers, or infinite-band moment data.

## Deliverables

- candidate_proof.md: STRICT theorem(s) and proofs, plus explicit non-coordinate
  example.
- whiteboard.md, research_ledger.md, approach_registry.md, run-manifest.json.

## Boundary cases

- r = 0 (unconstrained H_beta): the criterion must recover Theorem E/Theorem 11
  (dense iff beta <= 3/2).
- Coordinate constraints M_i = 0 for i in R finite: the criterion must recover
  Theorem E (dense iff beta <= 3/2 AND no finite run).
- N empty: Lemma 6.1 of upstream applies; Q_sp empty, density fails unless V={0}.
- D = -1 (r=0) is handled by the same finite matrix formalism (T is the zero
  map from the free-base space to {0}).

## Honesty

- All theorems are STRICT and proven in candidate_proof.md.
- Numerical checks are not used as proof.  If any are added later they must be
  labeled EVIDENCE.
- Status label: RIGOROUS_PARTIAL_RESULT (partial because the general O1' remains
  open; the subclass is fully decided).
