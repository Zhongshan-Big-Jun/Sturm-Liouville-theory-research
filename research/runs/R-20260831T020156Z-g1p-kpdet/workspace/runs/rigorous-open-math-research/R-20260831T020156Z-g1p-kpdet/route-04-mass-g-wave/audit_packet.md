# Fresh independent audit packet for W4 and W5

## Independence and scope

- Audit ID: `AUDIT-W4-W5-MASS-G-01`.
- You did not author either reviewed artifact.
- Use exactly one model response and do not spawn subagents.
- Review the artifacts as a first-time submission. Do not infer correctness
  from prior summaries.
- Write only `route-04-mass-g-wave/audit/independent_audit.md` and
  `route-04-mass-g-wave/audit/independent_audit.json`.

## Bound inputs

- `problem_contract.md`, SHA256
  `67427fe00b6b7758552581cde19fdb449202b5e9ea7bf9013f6ba0a4135f3f9d`.
- `route-01-transfer-schur/derivation.md`, SHA256
  `a96fde4cfaaf3cb83fcf416d3d7e627a5d63c4a48c2cd8a0c562e9dd8636e7d3`.
- `route-03-phi-exact/worker_result.md`, SHA256
  `6c1bbbd871c9aef7c8c316d47d0b61c3ab34bfb806eb5ee715ed915df6103ee3`.
- `route-03-phi-exact/audit/independent_audit.json`, SHA256
  `3bace4993b5a14c55950043322dd410e65f7f0135df5e03c95dde18a5ad6b3dd`.
- `route-04-mass-g-wave/prover_result.md`, SHA256
  `d55114570d516c69e446f2c228a76fb8827335e596df6c62e3d355a5232f9ffa`.
- `route-04-mass-g-wave/falsifier_result.md`, SHA256
  `03a06fbe30ae7acea06a7da21d694f3d07bb3140458c93ce78b16b911fefb9e9`.

Verify every hash before review.

## Mandatory checks

### W4

1. Independently rederive the phase quadratics `Q3,Q2` and equations
   `(1)-(3)` from the audited mass-slope equation.
2. Check formulas `(4)-(5)`, all powers of `c`, and every sign.
3. Check the mixed-sign conclusion and the equality cases in `(6)-(7)`.
4. Confirm that `(SC)` is only a sufficient open implication and is not
   presented as proved or equivalent.

### W5

1. Check the exact tuple, both spectral equations, band equation, all modal
   inequalities, and interior reconstruction.
2. Recompute `G`, `Xi`, and the exact mass residual. Check that the rational
   interval bounds are genuinely outward and sufficient for strict signs.
3. Confirm that the witness is explicitly mass-defective and therefore does
   not refute `G>=0` or `PHI-SIGN` on the complete system.
4. Audit the restricted near-one theorem. In particular, decide whether the
   claimed convergence of phases, norms, and endpoint separation follows
   uniformly from the stated hypotheses. Reject or downgrade it if any
   compactness or branch-continuity step is missing.

### Joint boundary

Check denominators, excluded faces, exact versus numerical labels, and whether
any accepted statement would change `PHI-SIGN` or `KP-DET`.

## Verdict and output

Use one verdict: `PASS`, `REPAIRABLE_GAP`, or `FATAL_GAP`. A partial PASS is
not allowed: if one independently claimed theorem has a gap, return
`REPAIRABLE_GAP` or `FATAL_GAP` and identify the first load-bearing error.
The JSON must contain `audit_id`, `verdict`, `critical_errors`, `gaps`,
`repair_hints`, `covered_scope`, `residual_risk`, `reviewed_artifacts`,
`first_error`, and `decision_delta`. The Markdown must show enough algebra to
make the verdict independently checkable. Return compact JSON with artifact
paths and SHA256 values in the final response.
