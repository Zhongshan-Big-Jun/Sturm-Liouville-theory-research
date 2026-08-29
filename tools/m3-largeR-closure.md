---
slug: m3-largeR-closure
title: M3 large-R closure for the n=2 symmetric INF branch
tags: [spectral-gap, large-R, asymptotics, determinant, blueprint]
status: STRICT
source: Blueprint run R-20260825T100044Z-b4-m3-blueprint; independent replication R-20260828T061236Z-b4-m3-independent-replication
related: ["[[largeR-level-cascade]]", "[[m3-log-correction]]", "[[band-selfconsistency-equivariance]]"]
---

# M3 large-R closure

## Theorem

Let `u=R^(-1/6)` and `kappa=(18pi-48/pi)^(1/3)`. In the finite-nonzero-interior n=2 symmetric INF chart, the exact four-equation system has a locally unique real-analytic even branch with

```text
k2 = kappa u + O(u^3),
k3 = kappa u + 16/(pi kappa) u^5 + O(u^7),
p1 = pi/2 + 2/kappa u^2 + O(u^4),
p3 = pi/4 + 1/kappa u^2 + O(u^4).
```

There is a finite existential `R0` such that for every `R>R0`,

```text
m3D-m3N = -4/kappa^5 u^4 + O(u^6) < 0,
Chi_up = 3/2 + 4/(pi kappa) + O(u^2) > 0,
det Kp_odd = 128kappa^2/pi^2 u^20 + O(u^22) > 0,
det Ko = 2048kappa^2/pi^4 u^26 + O(u^28) > 0.
```

Equivalently, the determinant powers are `R^(-10/3)` and `R^(-13/3)`. The odd candidates `R^(-7/2)` and `R^(-9/2)` are excluded by even analyticity.

## Proof chain

1. Two exact blow-ups and a nonzero seed Jacobian prove the local finite-R analytic branch.
2. Two Newton faces and local uniqueness prove scale exhaustiveness in the admitted finite interior class.
3. Exact one-jet reconstruction, full two-by-two sector determinants, omitted-jet audits, and analytic normalized remainders prove the coefficients and finite-R signs.

The canonical target is `CLM-SL-B4-M3-TARGET-V1` in `blueprint/blueprint.json`. The immutable review and merge record is `blueprint/submissions/SUB-20260825-B4M3-FINAL-003/`.

## Historical correction

The old staged Pbuild D-side mass used incorrect powers of `u`. Its hard `E5_5` obstruction, forced odd correction, and subsequent log-correction hypothesis do not apply to the exact closed residual. They are retained only as superseded route history.

## Independent replication

The later Codex plus Whiteboard run independently reproduced every headline formula using a separately written cascade and full transfer-Jacobian implementation. It also found a physical finite-u root with residual about `6.6e-50` at `u=0.06`. These checks are valuable `VERIFIED_REPLICATION` evidence but are not substituted for the exact Blueprint proof.

## Scope

The theorem does not classify singular `K` limits, denominator-collapse geometries, nonunit `k3/k2` limits, or all-R n>=2 branches. Global `(G1')` and `(G2)` remain open outside this M3 chart.
