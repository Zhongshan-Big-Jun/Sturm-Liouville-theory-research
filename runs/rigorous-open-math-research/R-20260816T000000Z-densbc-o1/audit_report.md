# Audit Report — R-20260816T000000Z-densbc-o1

- Audit date: 2026-08-16.
- Independent adversarial audit: a fresh subagent (spawn provider, no shared
  chain-of-thought) audited candidate_proof.md against problem_contract.md and
  the upstream audited results (Theorems A-H, Theorem E, F-densbc-01 correction).
  This is genuinely independent (fresh context), unlike the upstream run whose
  audit was coordinator-conducted.
- Audit target: candidate_proof.md (Theorems 1-5, Lemma 6.1, Heuristic 6.2,
  reduced core O1').

## Audit verdict (pre-revision): REPAIRABLE_GAP

The independent verifier found the central logical structure sound (Theorems 1-4
correct; Theorem 3 run ratio and first-obstruction minimality correct; honest
reduced core O1'), with three localized, repairable issues:

1. **Theorem 4 (representer normalization)** — the representer moment formula
   was stated as a^{(j)}_k = (k+1)^{2 beta} delta_{k,i_j}; the correct Riesz
   representer v_j = x^{i_j}/(i_j+1)^{2 beta} gives a^{(j)}_k = delta_{k,i_j}.
   The kept set is unaffected, so the conclusion is unchanged (typo-level).
2. **Theorem 5 (sufficiency condition)** — "every representer v_j is a
   polynomial => finite support / finite N" is FALSE in a general H: even a
   polynomial representer has a^{(j)}_k = <v_j,x^k> = sum_i \bar c_i <x^i,x^k>
   which need not be finitely supported, and determining N requires infinitely
   many values <v_j,x^k>.  The correct finite/structured sufficient condition
   requires banded/diagonal moment structure (diagonal case cleanly satisfies it).
3. **Proposition 6 (genericity)** — split into Lemma 6.1 (STRICT: N empty => Q_sp
   empty => density fails unless V={0}) and Heuristic 6.2 (genericity = EVIDENCE/
   HEURISTIC, not a proven theorem, since no topology/measure on representer
   moment sequences is specified).

Audit verdict on the honesty/scope: the run does NOT claim a closed form for
general non-diagonal H; it honestly reduces O1 to the moment/membership core O1'
and labels {P_V(p_n)} projection density as STRICT.  No circularity, no
equivalent-of-target used as premise, boundary cases (V={0}, r=0, N empty,
coordinate diagonal) all addressed.

## Per-obligation verdicts (post-revision, re-checked from changed points)

- Theorem 1 (projection density): PASS (continuous surjective-image-of-dense-set
  argument sound; P_V : H -> V bounded surjective, Pi dense in H).
- Theorem 2 (obstruction system): PASS (direct from Theorem A + linearity).
- Theorem 3 (run lemma + first obstruction): PASS (corrected ratio M_k =
  (floor(k/2)/floor(L/2)) M_L on both parities; first-obstruction minimality
  sound at the abstract moment-system level).
- Theorem 4 (diagonal reduction): PASS after normalization repair (a^{(j)}_k =
  delta_{k,i_j}); reduction to Theorem E exact.
- Theorem 5 (finite-rank structure): PASS after repair (main claim: not purely
  finite-rank in general, correct; finite/structured condition now properly
  requires banded/diagonal moment structure).
- Lemma 6.1 (empty kept set): PASS (STRICT).  Heuristic 6.2 (genericity):
  relabeled EVIDENCE/HEURISTIC (not load-bearing).
- Reduced core O1': honestly OPEN (the realizability/membership step).

## Residual risk

- O1' remains open: deciding whether a free run-base admits a nonzero w in V with
  the prescribed moments is a genuine moment problem in general H; the exact
  criterion is conditional on it.  No claim of a closed form is made.
- Heuristic 6.2's genericity assertion is not a rigorous Baire/measure theorem.
- Numerical EVIDENCE (scripts) corroborates Theorem 1 / Lemma 6.1 but does not
  prove them; the STRICT proofs stand on their own.

## Overall

Run status: RIGOROUS_PARTIAL_RESULT (inherited verbatim from upstream; the O1
core is still open as O1').  STRICT structure theorems produced and independently
audited (REPAIRABLE_GAP -> repaired -> re-verified at changed points).
