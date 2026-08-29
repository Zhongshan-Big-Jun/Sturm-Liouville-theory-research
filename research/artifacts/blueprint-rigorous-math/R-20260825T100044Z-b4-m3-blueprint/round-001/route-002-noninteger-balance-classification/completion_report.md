CANDIDATE_COMPLETE_PROOF

# Route 002 completion report

## Exact route result

The frozen finite-nonzero `n=2` symmetric INF seed exists in the interior
limiting geometry. Its corrected leading data are

```text
K0^3 = 18*pi-48/pi,
A0 = 2/K0,
B0 = 1/K0,
C0 = 16/(pi*K0).
```

The exact desingularized residual has first and second Jacobian determinants
`-pi/16` and `16/K0^5`, respectively. Two real-analytic implicit-function
steps in `v=u^2` therefore give one exact local branch for every sufficiently
small positive `u`, equivalently every sufficiently large finite `R`, with a
quantified `O(u^2)` coefficient remainder. Local uniqueness excludes a
distinct Puiseux, logarithmic, inverse-logarithmic, mixed power-log, odd, or
flat branch with the same limiting geometry.

The bound staged P builder's hard `E5_5=1/(2K^2)` is false for the exact
residual because its D-side half-mass shifts powers of `u` incorrectly. The
exact branch is even in `u`; no hard odd correction is forced.

## Verification performed

- All six repository inputs matched their frozen SHA-256 hashes.
- The exact closed mass formula was reconciled line by line with the staged
  helper, locating four D-side exponent-shift errors.
- Corrected low-order identities and both Jacobians were computed exactly by
  SymPy 1.13.1 from a direct transcription of the closed residual.
- A separate 100-digit mpmath 1.3.0 replay of the original residual cancelled
  the defective coefficient and reproduced both corrected secondary
  coefficients at an off-seed point.
- The O(1) interior `p3`-shift chart was eliminated and returns `pi/4`.
- The manifest's artifact hashes were rechecked and all matched.

## Remaining work outside the route theorem

- Independent definition, logic, boundary, and adversarial review has not yet
  occurred; therefore this is a candidate proof, not an audited proof.
- The exact IFT radius `u0` and remainder constant `M` are non-effective.
- `K->0/infinity`, nonunit limiting `k3/k2`, and phase-denominator boundary
  geometries are explicitly outside the admitted class and are not globally
  classified.
- `m3D-m3N`, the upstream consistency relation, and both sector determinants
  are reserved for the successor route and remain open in this report.
- Deterministic proposal validation and Blueprint integration remain pending.

## Failed and corrected attempts

- Replaying `_gapn2_largeR_Pbuild.py` initially produced the apparent
  obstruction `E5/u^4=-1/(6K^2)`. Direct original-residual reconciliation
  refuted it and identified the source defect; this is retained as an audited
  failure rather than silently discarded.
- A monolithic exact general-phase SymPy expansion was computationally
  impractical and was replaced by a power-audited truncated-algebra replay.
- The 270-row continuation is consistent with the exact seed but remains
  evidence only.

## Novelty and significance

- Novelty: `unknown`. No literature search was permitted or performed.
- Significance: high for the bounded M3 seed bottleneck, because it restores
  an exact finite branch and removes the previously recorded false odd-term
  obstruction. It does not close the frozen overall target's observables and
  determinants.

## Contribution provenance

- Human/user contribution: the frozen problem, route, source, scope, and
  completion contracts.
- Model contribution: source audit, blow-up selection, exact elimination,
  IFT proof, scale-exhaustiveness reasoning, boundary classification, and
  packaging.
- Tool contribution: SHA-256 checks, exact SymPy coefficient algebra, and
  100-digit mpmath adversarial evaluation.
- Repository contribution: the exact closed residual and non-trusted prior
  cascade/continuation records. No other route content was used.

## Calibrated confidence

| Axis | Confidence | Reason |
| --- | --- | --- |
| semantic fidelity | high | bound hashes, exact route scope, and explicit admitted class |
| mathematical correctness | high but not independently audited | two exact ranks plus direct residual reconciliation |
| route completeness | high within the admitted finite interior class | existence, uniqueness, remainder, and finite-R bridge are included |
| global scale exhaustiveness | deliberately limited | separate singular geometries are not globally classified |
| novelty | low/unknown | no literature audit |
| reproducibility | high | exact commands, versions, scripts, hashes, and validity predicates are frozen |

Primary artifacts: `proof_package.md`, `normalization_audit.md`,
`valuation_and_exhaustiveness.md`, and `reproducibility_manifest.json`.

