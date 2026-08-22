# Research Ledger

## 2026-08-23, pre-scan (light reuse)

- Read PROBLEM-O1P-GENERAL.md, research_map.md, tools/README.md (relevant
  entries), lean-proof/LEMMA_INDEX.md, and summaries of prior DensBC runs.
- Read in detail only the parts of prior candidate proofs needed to reuse:
  run/free-base definitions, H_beta and H_lambda criteria, the corrected
  rho formula.
- Reuse decision: no need to re-prove the run lemma or the master criterion.

## 2026-08-23, derivation

- Tried to extend H_lambda to bandwidth 2 shift family.  Found the natural
  moment realization; then realized a weighted diagonal + shift family
  H_{beta,lambda} solves a more interesting interpolation.
- Derived moment map J = D_beta + lambda B and characterized the range for
  run vectors.
- Key insight: infinite run moment vectors are realizable iff beta > 3/2,
  even when lambda != 0.  The H_lambda case is beta = 0 (never realizable);
  the H_beta case is lambda = 0 (realizable iff beta > 3/2).
- Consequence: the finite/infinite admissibility split is the same as H_beta,
  but the space itself is genuinely non-diagonal for lambda != 0.

## 2026-08-23, verification

- Symbolic/quick numerical probes were used as EVIDENCE only (not proof).
- The explicit v_1 = x^4 example was checked by hand and symbolically.

## Decisions

- Do not claim general O1'.  Record a strict subclass theorem only.
