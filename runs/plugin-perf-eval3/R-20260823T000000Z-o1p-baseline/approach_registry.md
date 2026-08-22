# Approach registry

Run: R-20260823T000000Z-o1p-baseline
Status: RIGOROUS_PARTIAL_RESULT (new STRICT theorem on H_shift, general O1' open)

## Route A: Stable banded-shift Toeplitz extension

- Route ID: A-BANDED-SHIFT
- Family: analytic/operator-theoretic + finite linear algebra
- Core mechanism: represent H as l^2 with x^k = e_k + sum lambda_s e_{k+s};
  if L(z)=1+sum lambda_s z^s has no zeros in the closed unit disk, the moment
  map J = I + sum lambda_s B^s is a bounded invertible Toeplitz operator, so
  realizability of a moment sequence is exactly l^2 membership. The run
  machinery then makes infinite runs inadmissible and leaves a finitely
  supported obstruction space isomorphic to ker(T|B_fin).
- Target obligation: deliver a finite-rank criterion for bandwidth m >= 1,
  beyond the m=1 H_lambda closure.
- Why it could be strictly easier: the explicit invertible moment map removes
  the general moment-problem core, leaving only finite linear algebra.
- Required known results: run lemma (pure linearity), master criterion,
  Toeplitz reciprocal series.
- First concrete deliverable: Theorem 2.3 (abstract band-invertible
  structure theorem), Theorem 2.1 (`dense <=> ker(T|B_fin)={0}` for H_shift),
  and Theorem 4.1 (`v_1=x^4` non-dense for all stable bandwidth 2).
- Fast falsification tests: m=1 regression to H_lambda, lambda=0 regression to
  H_0, numerical checks of N and T.
- Expected bottleneck: proving J invertible; boundary roots of L.
- Cost tier: 1 (after Tier 0 reading).
- Minimal first step: write down J and its inverse via 1/L series.
- Escalation criteria: none needed; route succeeded.
- Status: PROVED (STRICT theorem).
- Exact gap: only finite polynomial representers and stable shifts.

## Route B: General banded Gram matrices

- Route ID: B-GENERAL-BANDED
- Family: operator theory / Toeplitz index
- Core mechanism: for an arbitrary banded Gram matrix, try to show the moment
  map has closed range and infinite-run moment vectors are not in the range.
- Target obligation: extend criterion to all banded non-diagonal H.
- Why it could be easier: bandedness gives cofinite kept set and finite
  combinatorial data.
- Required known results: range characterization of the moment map.
- First concrete deliverable: none reached.
- Fast falsification tests: two-band Toeplitz with symbol winding nonzero;
  banded Gram from non-invertible moment map.
- Expected bottleneck: invertibility/range of J is not automatic; a banded
  Gram can have a moment map with non-closed range or with nonzero index.
- Cost tier: 2.
- Minimal first step: check a banded Gram with `x^k = e_k + 2 e_{k+1}` (L has
  zero inside unit disk); Pi not dense, so outside H1.
- Escalation criteria: not reached.
- Status: BLOCKED (needs a materially new mechanism or a narrower class).
- Exact gap: general banded moment map realizability.

## Route C: Weighted L^2 / non-Toeplitz non-diagonal H

- Route ID: C-WEIGHTED
- Family: moment problem / weighted spaces
- Core mechanism: use growth conditions on weighted moments to rule out
  infinite-run obstructions.
- Target obligation: exact decision for a concrete weighted L^2 H.
- Why it could be easier: known moment-problem theory for weighted L^2.
- Required known results: classical Hamburger/stieltjes moment realizability.
- First concrete deliverable: no concrete candidate chosen.
- Fast falsification tests: beta threshold in H_beta already shows growth can
  allow infinite-run obstructions.
- Expected bottleneck: realizability and membership are infinite-dimensional
  linear feasibility.
- Cost tier: 2.
- Minimal first step: read H_beta analysis (already done).
- Escalation criteria: not met.
- Status: BLOCKED (not advanced in this run).
- Exact gap: explicit weighted H with a non-polynomial representer not
  analyzed.

## Route D: General O1' moment core

- Route ID: D-GENERAL-CORE
- Family: abstract functional analysis / moment problem
- Core mechanism: characterize `V cap Q_sp^\perp` as a moment-representability
  problem.
- Target obligation: decide general O1'.
- Why it could be easier: no.
- Required known results: full moment-problem classification for arbitrary H.
- First concrete deliverable: already exists as Theorem 5 of
  R-20260816T000000Z.
- Fast falsification tests: H_beta and H_lambda show the criterion depends on
  H-specific realizability.
- Expected bottleneck: infinite-dimensional moment feasibility.
- Cost tier: 3.
- Minimal first step: none performed; recognised as requiring new machinery.
- Escalation criteria: not met.
- Status: BLOCKED (honest reduced core).
- Exact gap: no known closed form for moment representability in general H.

## Route E: Literature/external theorem hunt

- Route ID: E-LIT
- Family: literature verification
- Core mechanism: search for an existing general non-diagonal criterion.
- Target obligation: novelty/status check.
- Why useful: avoids duplicating known work.
- Required known results: none.
- First concrete deliverable: status_and_literature.md with degraded search.
- Fast falsification tests: n/a.
- Expected bottleneck: no exact literature found.
- Cost tier: 0.
- Minimal first step: web queries.
- Escalation criteria: not met.
- Status: PARTIAL (searched, no relevant result).
- Exact gap: no external source found.
