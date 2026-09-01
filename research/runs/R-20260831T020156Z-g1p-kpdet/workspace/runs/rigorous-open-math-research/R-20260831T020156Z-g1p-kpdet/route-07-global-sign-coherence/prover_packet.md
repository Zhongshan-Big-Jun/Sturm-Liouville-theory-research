# W10 global sign-coherence prover packet

## Contract

- Subtask ID: `W10-GLOBAL-SIGN-COHERENCE-PROVER`.
- One model response. Do not spawn subagents.
- Work on the complete exact admissible finite-interior phase system for
  arbitrary finite `m>1`.
- Write only `route-07-global-sign-coherence/prover_result.md` and optional
  deterministic checks under `route-07-global-sign-coherence/prover/`.
- Do not edit shared state, accepted packages, Blueprint, Lean, or indexes.
- Numerical evidence cannot prove the global implication.

## Bound inputs

- `problem_contract.md`, SHA256
  `67427fe00b6b7758552581cde19fdb449202b5e9ea7bf9013f6ba0a4135f3f9d`.
- `route-01-transfer-schur/derivation.md`, SHA256
  `a96fde4cfaaf3cb83fcf416d3d7e627a5d63c4a48c2cd8a0c562e9dd8636e7d3`.
- `route-03-phi-exact/worker_result.md`, SHA256
  `6c1bbbd871c9aef7c8c316d47d0b61c3ab34bfb806eb5ee715ed915df6103ee3`.
- `route-04-mass-g-wave/accepted_package.md`, SHA256
  `cd56d00daadad6315bc7fe267754c4516617e08832f6ffc5b3c77883c7e24192`.
- `route-06-alpha-pi/accepted_package.md`, SHA256
  `1177c02076694ebf95ce912719846b3143e5e9099614e66492586296ae7526ba`.

Verify every hash.

## Exact task

On the spectral-band system, analyze the open implication

```text
G<0 implies
  (A>0 and B>0 and H>0)
  or
  (A<0 and B<0 and H<0).                            (SC)
```

Here `(A,B,H)` and their exact formulas in terms of `Lalpha` are in the
accepted mass-to-sign package. On the complete mass system, `(SC)`
contradicts the accepted strict mixed-sign theorem and would prove `G>=0`,
then `Xi>0`, `Phi<0`, and KP-DET.

Seek, in decreasing order of value:

1. Prove `(SC)` globally with a denominator-safe factorization or monotonicity
   argument.
2. Prove directly that complete mass admissibility excludes `G<0`, even if
   `(SC)` is stronger than necessary.
3. Close one full sign chamber, for example `H<=0`, `Lalpha<=0`, or
   `B<=0`, and identify the exact remaining chamber.
4. Derive an exact identity that expresses `G` in terms of
   `A,B,H,Lalpha` plus manifestly signed factors, with equality cases.

First test whether the accepted exact mass-defective W5 point, which has
`G<0`, is consistent with `(SC)`; do not accidentally claim a statement that
it already refutes. Audit every use of spectral, band, modal, and mass data.
Do not repeat the near-one work.

## Required output

The first line must be `PROVED`, `PARTIAL`, or `NO_GAIN`. State the exact
theorem, chamber analysis, factorization, denominator and equality audit, and
first unresolved step. End with one `decision_delta:` line. Return compact
JSON with `subtask_id`, `status`, `artifact_path`, `artifact_sha256`,
`exact_gap`, `failure_mechanism`, and `decision_delta`.
