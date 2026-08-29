# Stage summary 2026-08-28 -- B4/P1 M3 closure and independent replication

## Outcome

`M3 CLOSED IN THE STATED LARGE-R CHART`.

The accepted Blueprint graph proves the n=2 symmetric INF result for the finite-nonzero-interior branch. The final proposal passed deterministic validation, independent mathematics review, deterministic integration, and post-integration closure checks. A later Codex plus Whiteboard run independently reproduced all headline formulas without reading the Blueprint process or result before freeze.

## Strict theorem

Let `u=R^(-1/6)` and `kappa^3=18pi-48/pi`. On the exact locally unique real-analytic branch in the admitted finite interior chart, there is a finite existential `R0` such that for every `R>R0`,

```text
m3D-m3N = -4/kappa^5 u^4 + O(u^6) < 0,
Chi_up = 3/2 + 4/(pi kappa) + O(u^2) > 0,
det Kp_odd = 128kappa^2/pi^2 u^20 + O(u^22) > 0,
det Ko = 2048kappa^2/pi^4 u^26 + O(u^28) > 0.
```

The branch is analytic in `v=u^2`, so the old odd candidates `u^21=R^(-7/2)` and `u^27=R^(-9/2)` cannot be leading terms.

## Blueprint closure record

- Canonical graph: `blueprint/blueprint.json`.
- Target node: `CLM-SL-B4-M3-TARGET-V1`.
- Blueprint SHA-256: `sha256:3b99f2090d73029fa77498a897979e614ddccbb205b613449fdd2181ce6ccc48`.
- Evidence inventory SHA-256: `sha256:0c1e576e4902ffb8720e8a9b7c02a0df1c5425af805f1c9aba05b9968279ed5e`.
- Final receipt: `blueprint/submissions/SUB-20260825-B4M3-FINAL-003/receipt.json`, status `merged`.
- Closure: 4 available claims, 3 proved inferences, 0 contradictions, 0 open obligations.

## Independent replication

The separate run `runs/rigorous-open-math-research/R-20260828T061236Z-b4-m3-independent-replication/` independently reproduced the scale, seed, mass difference, scalar, determinant exponents, determinant coefficients, and signs. Its determinant layer remains labeled `VERIFIED_REPLICATION`, while theorem-grade exact closure remains bound to the accepted Blueprint package.

## Correction of the old route

The 2026-08-14 staged Pbuild route used incorrect D-side mass powers. Its resulting hard odd-correction obstruction and log-correction hypothesis are superseded. The corrected closed residual has an even analytic branch and the positive seed above.

## Resource record

- Blueprint closed loop: `31435.654` seconds. The final pre-close tracker recorded `1556831` tokens; the authoritative final total is absent from the stored artifact.
- Independent run: `8206.798828` seconds. Exact tokens are unavailable because no goal token tracker was active; no estimate is substituted.

## Remaining scope

This closes M3 only in its declared n=2 symmetric INF large-R finite-interior chart. It does not close the remaining all-R `(G1')`, `(G2)`, or global n>=2 symmetry obligations.
