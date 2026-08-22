# Interrupted run handoff

Run: R-20260822T220000Z-b3-reuse
Status: RIGOROUS_PARTIAL_RESULT
Stop time (UTC): 2026-08-22T23:30Z (resource boundary)

## Completed work

- Pre-scan of required context (docs, tools, Lean index, op02 scripts).
- Independently derived and wrote STRICT proofs for:
  1. Ratio extremizer structure: every global fixed-n maximizer is an
     alternating [1,R,1,...,1] bang-bang with exactly 2n switches.
  2. General 2n-root count for the balanced alternating secular polynomial,
     via an elliptic-zone phase lemma.
- Cross-checked both against the baseline run
  runs/plugin-perf-eval2/R-20260822T220000Z-b3-baseline, which already
  contains the same results (with a Jacobi-matrix proof for the 2n-root count).

## Routes tried with outcomes

- R1 (2n-root count): SUCCESS STRICT.
- R2 (ratio exact switches): SUCCESS STRICT.
- R3 (self-consistency uniqueness for alternating family): EXPLORED. Found at
  least one asymmetric self-consistent [1,R,1,R,1] solution for n=2,R=4 with
  ratio ~2.55, below the balanced ratio ~4.28. This shows self-consistency +
  alternating pattern does NOT imply equal widths or global maximality.
- R4 (one-parameter monotonicity): OPEN; only EVIDENCE from baseline probes.
- R5 (literature): searched web; no direct fixed-n ratio result found in first
  pass.

## Tools/methods tried

- Transfer-matrix symbolic/numerical (numpy, sympy).
- Chebyshev/second-kind + phase-function argument for O3.
- Wronskian Q monotonicity and block-energy invariant for ratio.
- Ratio self-consistency least-squares solver (Windows Python/scipy).
- Web search (first pass).

## Exact remaining obligations

- O1: prove among all [1,R,1,...,1] bang-bang maximizers the equal-width
  balanced configuration is optimal; prove the value c_n(R).
- O2: prove the one-parameter equal-within-type alternating family is maximized
  at w_1/w_2 = sqrt(R).
- Audit/formalization: consider Lean scaffolding for the two STRICT results.

## Next actions

1. Read baseline run (already read) and reuse its Jacobi-matrix proof to avoid
   re-deriving O3.
2. Attack O2/O1 using the Jacobi-matrix form of Q_n or the full ratio
   self-consistency system.
3. Try to prove a comparison/monotonicity theorem for the ratio over the width
   simplex of alternating [1,R,...,1] configurations.
4. If new results are found, update research_map.md, tools/, and Lean scaffold.

## Files in run root

- problem_contract.md, status_and_literature.md, approach_registry.md,
  research_ledger.md, candidate_proof.md, escalation_ladder.md,
  performance_log.md, final_report.md,
  verify_b3_r1r2.py, ratio_selfsolve.py, ratio_selfsolve_multi.py.
