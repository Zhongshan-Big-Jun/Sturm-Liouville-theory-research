# Status and literature

## Scope status

`LIKELY_OPEN_PROJECT_SPECIFIC_FORMULATION` is retained from the bounded preflight. This is not a global novelty claim.

## Frozen project mathematics

### KNOWN, frozen and rechecked

1. `docs/SL_gap_nge2_symmetry_local_proof.tex`, SHA256 `151c7ec65a67789a043b01a46f6c87c40e6827e9994be9fb4be88a45da0c0aaa`.
	- Supplies the exact band-consistent definitions, Wronskian sign, matrix reduction, Hessian relation, and a strict near-`R=1` branch theorem.
	- It does not close the all-finite-`R` sector signs.
2. `runs/rigorous-open-math-research/R-20260812T090000Z-g1prime-g2/run_notes_addendum_2026-08-13d.md`, SHA256 `adee3958b6b1979f6687c03f11f23bc525960ba57ae2e6a9506117095b76e50d`.
	- Supplies the corrected half Green normalization and the exact `Kp_odd` and `Ko` formulas.
	- It explicitly corrects the false identification of `Kp_odd` with raw `Ko`.
3. `runs/rigorous-open-math-research/R-20260812T090000Z-g1prime-g2/run_notes_addendum_2026-08-13e.md`, SHA256 `399b6f66db94fd6eeff873badc08b8e1bdd8afee14a97b0b6734d42d9e28d437`.
	- Supplies strict near-one sign-definiteness.
	- Its determinant monotonicity statements are `EVIDENCE`, not proof.
4. `research/artifacts/blueprint-rigorous-math/R-20260825T100044Z-b4-m3-blueprint/round-002/route-003-observable-determinant-closure/observable_determinant_refutation.md`, SHA256 `6d1c8cbbc7cb68b569675fcad5854288692f4fbc17ae87a76d8768ea8afd0dd8`.
	- Supplies the accepted exact large-`R` INF determinant asymptotics on the corrected finite-interior branch.
	- Correct laws are `det Kp_odd=(128 kappa^2/pi^2)R^(-10/3)+O(R^(-11/3))` and `det Ko=(2048 kappa^2/pi^4)R^(-13/3)+O(R^(-14/3))`.
	- It expressly does not close M1, M2, SUP, `n>=3`, or global `G1'`.

### DERIVED in this run

1. Determinant-only inertia bridge. On a connected continuous branch, the strict near-one negative inertia plus positive sector determinant everywhere forces negative definiteness and the negative trace everywhere.
2. Compact first-loss reduction. The strict near-one and large-`R` anchors confine any sign failure to a compact middle interval and to a zero of one of the two sector determinants.
3. The direct parent M1 chain-rule route is not a self-contained first-zero certificate in its recorded form because `x'(R)=-J^{-1}F_R` requires `J` invertible, while `det J=(R-1)^4 det(Kp_odd)det(Ko)` for `n=2`. A separate continuation or singular-point argument is required.

## Literature preflight

The scoped preflight records three related but non-identical eigenvalue-gap papers:

1. Hongli Sun, `On the minimum eigenvalue gap for vibrating string`, JMAA 516(1), 2022, DOI `10.1016/j.jmaa.2022.126513`.
2. Y. Ahrami, E. M. El Allali, and E. M. Harrell II, `On the fundamental eigenvalue gap of Sturm-Liouville operators`, Archiv der Mathematik 126(2), 2026, DOI `10.1007/s00013-025-02213-y`.
3. `Sharp bounds of Neumann eigenvalue gaps and ratios for Sturm-Liouville equations`, JDE 476, 2026, DOI `10.1016/j.jde.2026.114478`.

These are navigation leads only. No theorem from them is used here, so no additional source fetch is load-bearing for this closure gate. The novelty risk remains medium because the bounded search does not prove global unpublished status.

## Coverage and gaps

- Covered: exact branch-local normalization, near-one anchor, large-`R` anchor, sector decomposition, first-zero topology, chain-rule dependency audit.
- Not covered: a uniform compact-middle coercive estimate for `Kp_odd`, a non-circular singular-point continuation theorem, and the corresponding `Ko` compact-middle certificate.
- Current earliest load-bearing gap: `KP-DET`, equivalently exclusion of a nonzero kernel of `Kp_odd` at a compact-middle first loss.
