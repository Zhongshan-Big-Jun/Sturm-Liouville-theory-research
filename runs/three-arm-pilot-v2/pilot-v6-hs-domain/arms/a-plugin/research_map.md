# Research map

## Problem split

The central distinction is between the genuine inverse of the self-adjoint
Krein operator and the algebraic inverse of its differential expression on
polynomials.  They agree on affine functions and differ from degree 2 onward.

## Routes and outcomes

- Krein-form route: nonnegative by Cauchy--Schwarz; equality exactly affine.
- Power-domain route: integer recursion plus the spectral half-power criterion
  reduces polynomial membership to finitely many iterated endpoint conditions.
- Even route: L2 orthogonality forces equality in \(K_c\ge cI\), hence affinity.
- Odd route: form orthogonality forces equality in \(a_c\ge c\|\cdot\|^2\),
  hence affinity.
- Completion route: both constructions are unitary to the same base space, but
  their canonical representatives differ by boundary correction.
- Exact-computation route: finite symbolic probes support/falsify local formulas
  only; the first recurrence implementation was caught and repaired.

## Strongest current finding

The independently audited proof gives
\(Q_n^{(s)}\in D(K_c^{s/2})\iff n\in\{0,1\}\) under the polynomial reading,
canonical non-equality of completions, and failure of literal polynomial-span
density.  Genuine operator-inverse images instead all belong and are dense but
are generally nonpolynomial.

## Unexpected finding

The word "isometry" does not resolve the task unless its map is typed: the
abstract algebraic isometry and the operator inverse isometry send the same base
polynomial to different representatives.

## Failures and avoid list

- Do not identify the two inverses.
- Do not infer universal membership from finite degrees.
- Do not infer facts about all domain-compatible polynomial combinations from
  membership of individual OPS elements.
- Do not call unitary equivalence literal equality.
- Do not reuse the malformed first version of the computation recurrence.

## Open directions / first unresolved obligation

No mathematical obligation remains within the frozen contract.  The first
unperformed verification upgrade is optional formal proof-assistant encoding;
the first unavailable external obligation is literature/novelty verification,
which the user prohibited and which is not a correctness premise.

## Contributions

- Human/user: froze the theorem, constraints, completion gates, and audit rule.
- Coordinator model: contract normalization, proofs, exact probes, synthesis.
- Independent verifier session: strict PASS, hash-bound in `audit_report.md`.
- Tools: local shell for deterministic replay/version reporting and SHA256;
  SymPy for exact finite falsification checks only.
