# Third-audit scripts author handoff

Role: SOFTWARE/MATHEMATICS AUTHOR. Status: scoped repairs and author checks complete; final independent review pending. No blocking concern remains within this assignment.

## Scope and instructions followed

Read the project AGENTS.md and the submitted third audit, especially R3-F1 and R3-F2. The user assigned only five active scripts and this external directory. The later explicit instruction forbidding AGENTS edits overrides the general maintenance instruction. No repository write by this author was made outside these five scripts. No commit, staging or push was performed.

Protected scope: docs, cards, index, library, AGENTS files, Lean, canonical data, old artifacts and other pre-existing/concurrent work. These were not edited or reverted by this author. The coordinator's concurrent source/navigation changes are outside this report; an aggregate working-tree diff must not be attributed entirely to this author.

Changed repository paths, all under `/mnt/f/LaTeX/BVE research/`:

- `scripts/d3_stability_verify.py`
- `scripts/d3_stability_verify2.py`
- `scripts/op12_dichotomy_verify.py`
- `scripts/op12_threshold_verify.py`
- `scripts/op12_sparse_check.py`

All new verification programs, snapshots and logs are under `/mnt/f/tools/math-audit-round3-20260920/scripts-author/`. New Python code uses tabs, snake_case function names and PascalCase multiword variables. All five scripts have main guards and imports produce no output or global precision changes. Existing callable helpers were retained, including `solve_u`, `poly_growth_rate`, `check_growth_lemma`, `solve_u_log`, `lfact`, `u_sequence`, `diag_series`, `diag_partial`, `eps_sparse`, `is_sparse` and `lu`.

## Repairs

1. General second-order recurrence and B=0 product examples are explicitly separated. The general growth check tests a lower bound under c0>0, B>=0, eps>=0. Exact regressions include A=3, B=2 giving u_m=2^m-1 despite eps=0, and A=3+2/m, B=2 giving u_2=4 instead of product value 2. No upper growth bound is inferred from S=O(log m).
2. A shared coefficient helper computes the actual polynomial expression: A=2m(2m-1)+c*alpha, B=alpha*(2m-2)*(2m-3), alpha=m/(m-1)+delta. For c=3, m=4, delta=1 it gives A=63, B=70 and A-B=-7. Perturbation outputs now identify failed growth hypotheses rather than declaring stability. Formal polynomial expressions are distinguished from Krein operator-domain membership.
3. The log solver subtracts log(c0) at every step. It avoids exponentiating the forward recurrence ratio, uses log differences and expm1 for subtraction, and rejects invalid coefficients, nonpositive or numerically unresolved steps. A supplemental check found that naive sign checking could accept exact zero as a tiny positive value after logarithmic cancellation. The final solver conservatively rejects cancellation within 16 ULPs of the largest log-term scale. The retained red regression first failed at c=1, A2=2, A3=3, B=6.
4. Exact recurrence diagnostics take log(numerator)-log(denominator), avoiding conversion of astronomical fractions to float. The exact solver remains available for signed solutions that the positive-step log solver does not support.
5. Products start at k=2 with u0=0 and u1=1. The C/k formula uses Gamma(2+C); for C=2 the exact sequence is (m+1)(m+2)/6 and the asymptotic factor is 1/6. Finite sums are identified as finite. The analytic B=0 series label is divergent at beta=2.4 and beta=2.5 and convergent at beta=2.6; samples do not establish these classifications.
6. Logarithmic examples now evaluate the stated log(k), starting at k=2. Sparse indices are exactly 2^(2^j), j>=1: 4, 16, 256, 65536, etc. Log-space diagnostics use k+log1p(exp(-k)), never exp(k). The retained legacy `eps_sparse` helper uses arbitrary-precision mpmath for callers that need the value; the displayed sparse diagnostics use log-space throughout. `lu` remains callable after execution.

## Commands and actual results

Working directory: `/mnt/f/LaTeX/BVE research`. Python 3.14.4; mpmath 1.3.0. Reproduce the complete author validation with:

```bash
python3 -B /mnt/f/tools/math-audit-round3-20260920/scripts-author/run_validation.py
```

The runner invokes each of the five actual repository scripts with `/usr/bin/python3 -B`, followed by the external reproducer and behavioral suite. It captures stdout, stderr, exit codes, elapsed times and source SHA-256 values. Each job has a 60-second timeout. The final run is:

`/mnt/f/tools/math-audit-round3-20260920/scripts-author/validation-20260920T134202807617Z/`

| Job | Exit | Time | Output files in the final run directory |
| --- | --- | --- | --- |
| d3_stability_verify.py | 0 | 0.096 s | d3_stability_verify.py.stdout.log, d3_stability_verify.py.stderr.log |
| d3_stability_verify2.py | 0 | 0.110 s | d3_stability_verify2.py.stdout.log, d3_stability_verify2.py.stderr.log |
| op12_dichotomy_verify.py | 0 | 1.293 s | op12_dichotomy_verify.py.stdout.log, op12_dichotomy_verify.py.stderr.log |
| op12_threshold_verify.py | 0 | 2.573 s | op12_threshold_verify.py.stdout.log, op12_threshold_verify.py.stderr.log |
| op12_sparse_check.py | 0 | 0.127 s | op12_sparse_check.py.stdout.log, op12_sparse_check.py.stderr.log |
| reproduce_defects.py | 0 | 0.327 s | reproduce_defects.py.stdout.log, reproduce_defects.py.stderr.log |
| behavior_checks.py | 0 | 7.626 s | behavior_checks.py.stdout.log, behavior_checks.py.stderr.log |

The final behavioral log reports `Ran 15 tests ... OK`. The original minimal reproducer went from 0/5 to 5/5 passing. These author-written checks use independent calculations, not an independent reviewer:

- Exact polynomial differentiation checks both perturbed coefficients and the endpoint derivative at 270 parameter combinations.
- Exact integration against P2 cross-checks the bounded-perturbation construction for m=2..30 and checks its moment recurrence. This is a finite algebraic regression, not a new proof by enumeration.
- 3,000 log values are compared against exact Fraction recurrence values evaluated independently at 90 decimal digits, including c0=1/2, 1, 3, 5 and 5/2, with and without perturbation; absolute tolerance 5e-10.
- All 1,000 constructed exact-zero recurrence steps are rejected, as is unresolved cancellation; a resolvable positive step of size about 1e-12 is accepted. Nonpositive/nonfinite inputs, huge ratios, decreasing positive solutions and logs outside float magnitude range are covered.
- Rational products and finite diagonal sums independently check gamma normalization and summation. Behavioral probes inspect the actual main callbacks to distinguish log(k) from log(k+1).
- Sparse membership is checked through 70,000 and at large generated indices; log sums through 65,536 are compared to an independent 90-digit evaluation.
- Ten deliberate assertion failures, one per script under normal Python and `-O`, all exit nonzero with AssertionError. Exact commands and outputs are in `assertion-failure-probes.json` in the final run directory.
- Syntax parsing, tab indentation and `git diff --check` passed. The captured command and result are in `scope-style-check.json` in the final run directory.

## Handoff artifacts and identity

- `result.json`: machine-readable AUTHOR_SELF_CHECK result, summaries, exact commands, output paths, source hashes, evidence hashes, protected scope and empty blocking-concern list. A matching result is saved in the final run directory.
- `before/` and `baseline.json`: original five script bytes and SHA-256 values at base HEAD `aac44f5a5831d9c4b7140027a09a06e8af4250f5`.
- `after/`: frozen final copies of the five scripts, checked against the hashes produced by the successful final run.
- `scripts.patch`: exact scoped repository diff for the coordinator.
- `before-reproduction.log` and `before-command.json`: the initial five expected regression failures.
- `cancellation-probe-before.json`, `cancellation-regression-before.log` and `cancellation-command-before.json`: the additional cancellation finding and red regression before its repair.
- `behavior_checks.py`, `reproduce_defects.py` and `run_validation.py`: executable external checks and capture runner.

The first validation directory is retained as intermediate history; use `validation-20260920T134202807617Z` and the final source hashes for review.

## Limits

This report certifies only completion of the assigned author work and the stated checks. It does not constitute final independent review, an interval error certificate, an infinite-dimensional completeness proof, or a convergence proof from finite sums. The floating-point log solver may conservatively reject ill-conditioned positive steps; exact Fraction evaluation remains available. The mathematical source, navigation, tool-library corrections, Lean and global mathematical completeness are handled separately. No further source edit is proposed before the coordinator's independent review.
