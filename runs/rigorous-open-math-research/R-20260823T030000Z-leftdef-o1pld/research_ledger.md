# Research Ledger — O1'LD run

Run: R-20260823T030000Z-leftdef-o1pld

## Chronological entries

1. 2026-08-23T~03:00Z — Read task packet, prior left-definite run, DensBC O1/O1p/O1p2 artifacts, research_map, tools, LEMMA_INDEX.
2. 2026-08-23T~03:10Z — Set up formal descent: s=2 -> L^2, s=3 -> H^1.  Noted that finite polynomial constraints in L^2 produce non-cofinite N (e.g. W=ker μ_4).
3. 2026-08-23T~03:30Z — Numerical probe of monomial gap totality in L^2/H^1.  L^2 appeared total by Müntz; H^1 residual ~0.064 stable (EVIDENCE, not proof).
4. 2026-08-23T~04:00Z — Proved finite-support L^2 moment rigidity via Müntz-Szász finite-deletion corollary.
5. 2026-08-23T~04:20Z — Proved infinite-run inadmissibility in L^2 and H^1.
6. 2026-08-23T~04:40Z — Formulated cofinite-N density theorem for s=2, later downgraded to NOT-YET-STRICT after audit (conditional on Claim 4).
7. 2026-08-23T~05:00Z — Derived parity decomposition theorem and the μ_4 non-density example (exact formula verified by sympy).
8. 2026-08-23T~05:30Z — Wrote candidate proof and run artifacts; wrote Lean scaffold.

## Decisions
- Do not blindly transfer H_beta/H_lambda finite-rank criterion.
- Do not claim H^1 finite-support realizability from EVIDENCE.
- Keep status RIGOROUS_PARTIAL_RESULT.

## Failures/blocked
- R1 (copy banded criterion) was shown inapplicable by Corollary 5 and Corollary 2.
- R7 (H^1 finite-support) remains open.
