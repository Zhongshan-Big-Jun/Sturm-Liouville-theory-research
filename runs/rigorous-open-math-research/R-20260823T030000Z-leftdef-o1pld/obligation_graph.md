# Obligation Graph — O1'LD run

Run: R-20260823T030000Z-leftdef-o1pld
Repair status: RIGOROUS_PARTIAL_RESULT (repaired after independent audit)

## Claims and dependencies

| Claim | Status | Depends on |
|---|---|---|
| Lemma 1 (finite deletion monomials total in L^2) | STRICT | Müntz-Szász (classical, Lebesgue L^p form) |
| Corollary 2 (finite-support L^2 moments trivial) | STRICT | Lemma 1 |
| Lemma 3 (Cauchy-Schwarz L^2 moment bound / linear growth not realizable) | STRICT | Cauchy-Schwarz + L^2 moment bound |
| Claim 4 (tail L^2 rigidity) | NOT-YET-STRICT | SL_h2 growth lemma + unresolved minimal-solution case |
| Theorem 5 (cofinite-N dense in L^2) | NOT-YET-STRICT | Corollary 2 + Claim 4 (conditional) |
| Corollary 6 (proper V in H^2 non-cofinite) | NOT-YET-STRICT | Theorem 5 + K_c isometry (conditional) |
| Theorem 7 (parity split) | STRICT | even/odd orthogonality |
| Corollary 8 (parity-invariant density) | STRICT | Theorem 7 |
| Theorem 9 (μ_4 non-density) | STRICT | exact μ_4 formulas, parity split, SL_h2 odd growth lemma |
| H^1 polynomial moment bound | STRICT | prior H^1 proof |
| H^1 infinite-run inadmissibility | EVIDENCE / PLAUSIBLE | no proof; downgraded from STRICT |
| H^1 finite-support realizability | OPEN | EVIDENCE only; no proof |
| General O1'LD | OPEN | unresolved |

## Open root obligations
- O1-1: characterize closure(span Q_sp) for arbitrary W ⊆ L^2.
- O1-2: characterize closure of kept odd/even q_n subfamilies.
- O1-3: determine whether any nonzero finite-support H^1 moment sequence is realizable.
- O1-4: prove or refute Claim 4 (tail L^2 rigidity); Theorem 5 is conditional on it.
