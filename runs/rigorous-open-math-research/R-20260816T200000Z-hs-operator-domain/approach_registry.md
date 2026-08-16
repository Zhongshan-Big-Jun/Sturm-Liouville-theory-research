# Approach registry — R-20260816T200000Z-hs-operator-domain

## Route R1: Operator-domain boundary conditions at transport levels (ACTIVE, main)
- Family: direct functional-analytic / boundary-value analysis.
- Core mechanism: characterize D(K_c^{s/2}) by iterated Krein boundary conditions;
  reduce Q_n membership to positivity of a transport deficit.
- Target obligation: MO (Q_n membership), Q1a, SPD, ND.
- Why strictly easier: reduces to one-variable boundary-value sums (Legendre endpoint
  derivatives) with explicit positivity, not the full operator-convergence question.
- Required results: P_n^{(m)}(1) closed form; Krein-Sobolev a_m recurrence; D(K_c^r)
  definition.
- First deliverable: strict proof D_n > 0 (even), D_m increasing, L(K_n)>0 (odd).
- Fast falsification test: exact check K_c^{-1}P_n in D(K_c) for n=0..10 (fails n>=2).
- Expected bottleneck: Krein-Sobolev odd-case positivity.
- Status: PROVED for the load-bearing assertions (MO-even, MO-odd, SPD, ND).
- Exact gap: none for load-bearing; "every degree >= 2r+2 present" lemma is
  EVIDENCE-level (not load-bearing).

## Route R2: Abstract-completion / transfer isometry comparison (ACTIVE, supporting)
- Family: transfer isometries K_c^r : H_op^s -> L^2 and H_abs^s -> L^2.
- Core mechanism: both scales are isometric to L^2; difference is which elements are
  "concrete functions in D(K_c^{s/2})" vs "abstract polynomial classes".
- Target obligation: SPD, EMB.
- Deliverable: difference statement + (partial) density of Pi ∩ H_op^s.
- Bottleneck: the difference requires identifying Q_2^(s) in H_abs^s \ H_op^s; done.
- Status: PROVED (SPD); EMB is PARTIAL (depends on EVIDENCE-level degree lemma).

## Route R3: Sparse-family correction (subordinate, from upstream)
- Family: reuse / correct the left-def sparse-family analysis.
- Core mechanism: verify/falsify upstream S1d "H^s ∩ C[x] = span{1,x}".
- Status: REFUTED (S1d over-reach: degree-6 poly in H^4); L1'' (sparse family,
  Q_sp={1,x}, density fails) STANDS and is reused.
- Outcome recorded: upstream auxiliary claim corrected; conclusion L1'' preserved.

## Closed/blocked
- No route was blocked; all three produced verified content. R1 carries the strict
  proof; R2 gives the space comparison; R3 is a recorded correction.
