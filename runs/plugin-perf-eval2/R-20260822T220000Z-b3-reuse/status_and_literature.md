# Status and literature snapshot

## Problem status (at run start)

- B3 is PARTIAL in research_map.md.
- STRICT: reflection symmetry F_n(π-y)=F_n(y) (docs/SL_fixed_n_supremum.tex Theorem 1;
  Lean ReflectionSymmetry.lean F_reflection VERIFIED).
- EVIDENCE: 2n-root count for n ≤ 6 and R ∈ {2,4,7,10}; no strict proof in existing docs.
- EVIDENCE: n=2,R=4 five-block optimization converges to conjectured config; broader random search supports.
- OPEN: global extremality; alternating-family monotonicity; strict 2n-root count.

## Literature / project sources read

1. docs/SL_fixed_n_supremum.tex
2. docs/SL_ratio_proof.tex
3. docs/SL_gap_nge2_finite_reduction_proof.tex
4. docs/SL_gap_nge2_exact_2n_switches_proof.tex
5. research_map.md
6. tools/README.md and tools listed in the problem brief
7. lean-proof/LEMMA_INDEX.md
8. scripts/op02_*.py (fixed-n alternating-family numerical/symbolic tools)

## Prior art relevant to this run

- Keller 1976 (n=1 ratio minimum; variational bang-bang)
- Mahar-Willner 1976 (full-sequence ratio supremum via MW periodic extension)
- Project n≥2 gap finite reduction and exact 2n-switch proofs:
  the exact-2n-switch machinery uses Wronskian W<0, switch function
  F=λ_n u_n^2−λ_{n+1}u_{n+1}^2, and block-energy invariant K=−2D.
- The same W<0 and exact-zero-count framework is adapted in this run to the ratio
  functional, with switch function G=u_n^2−u_{n+1}^2 and invariant K_ratio=0.

## New results in this run (preliminary)

- STRICT general 2n-root count for the alternating secular polynomial via an
  elliptic-zone phase lemma (obligation 3).
- STRICT finite reduction + exact 2n switches + alternating 1,R,...,1 pattern for
  every global maximizer of the ratio (obligation 1 first half).
- The remaining obligations are: (a) uniqueness/width optimization inside the
  alternating family; (b) proof that the balanced point is the global maximizing
  point in that family.

## Novelty caveat

The project does not claim literature priority. The new 2n-root-count proof and
ratio exact-2n-switch reduction are presented as self-contained derivations in
this run; they should be checked against Willner-Mahar 1979 and related prior
work before any priority claim.
