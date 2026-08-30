# Problem contract

## Authority and frozen inputs

- Task ID: `Q-20260830-g1p-live-recovery`.
- Contract date: `2026-08-30`.
- Authoritative project source record: `workspace/refs/source_contract.md`, SHA256 `10decf901aca0f6dac72dc3fceacaf91967412cbbd38054a9cfa823d37dfe759`.
- Accepted-knowledge snapshot: `workspace/refs/blueprint_snapshot.md`, SHA256 `64369e93d6d13146ed65ab615e8a76b93d7aca955a6d0e38c330237da6962359`.
- Novelty preflight: `workspace/refs/literature_status.md`, SHA256 `845ba3e4a390c4dbd74203b99868c1505e7f28769911b703c77a30a34ad4219a`.
- Frozen parent commit: `2f2f41c9caf2a6aa21e74bbab577108d62b7dc01`.
- The current checkout is later than the frozen commit. The four named parent artifacts were re-hashed in the working tree and exactly match the frozen SHA256 values. Unrelated dirty build and scratch files were observed and not touched.

## Objects and definitions

Let `R>1`. Consider the prescribed exact `n=2` symmetric, band-consistent, finite-interior INF branch from the task packet. Its four full switches are

```text
0<x1<x2<1-x2<1-x1<1.
```

The density pattern is INF, so it starts and ends with density `R` and alternates between `R` and `1`. Let `lambda_2<lambda_3` be the full Dirichlet eigenvalues, let `u_2,u_3` be normalized by `int rho u_k^2=1`, and set

```text
c^2=lambda_2/lambda_3,
f=lambda_2 u_2^2-lambda_3 u_3^2.
```

At a band-consistent point, `f` vanishes at all switches. The normalized symmetric-sector matrices are the exact two-by-two matrices from the frozen parent convention:

```text
Kp_odd=diag(d)+2 lambda_2 diag(u)
	[G_D o (e e^T)-c^2 G_N] diag(u),

Ko=diag(d)+2 r (eps v)(eps v)^T
	+2 lambda_2 diag(u)[Gt_N-c^2 Gt_D o (e e^T)]diag(u),
```

where `u=(u_2(x1),u_2(x2))`, `v_j=u_j^2`, `eps=(1,-1)`, `e=eps`,

```text
d_j=-2c|W(x_j)|/(R-1),
r=2 lambda_2 (lambda_3-lambda_2)/lambda_3^2,
```

and the four half Green matrices use the exact ordinary or pole-removed normalization fixed in the parent addendum. In particular, `Kp_odd` is not the raw odd sector `Ko`.

## Hypotheses

1. The prescribed symmetric INF branch is the branch object quantified by the task packet. This run proves matrix signs conditional on that branch object; it does not prove global existence or uniqueness of symmetric roots.
2. Along every finite-interior portion of the branch, the switches, eigenpairs, Green matrices, `Kp_odd`, and `Ko` depend continuously on `R`. Analytic dependence is available on nonsingular local charts.
3. The strict near-one anchor and the accepted strict large-`R` INF chart are admissible frozen premises in exactly their declared ranges.
4. No SUP, non-symmetric, `n>=3`, boundary-collapse, or global `G1'` conclusion is included.

## Target conclusion

For every finite `R>1` on the prescribed branch,

```text
trace(Kp_odd(R))<0,  det(Kp_odd(R))>0,
trace(Ko(R))<0,      det(Ko(R))>0.
```

Equivalently, both real symmetric two-by-two matrices are negative definite.

## Quantifiers and dependency of constants

- The quantifier is every finite `R>1` on the single prescribed `n=2` symmetric INF branch.
- The near-one anchor may use an unspecified `delta>0`.
- The large-`R` chart may use an unspecified finite `R_infty` after which its exact asymptotic remainders fix the signs.
- A partial bridge must name the remaining compact interval and the exact sector determinant or trace obligation.

## Equivalent formulations that are actually proved equivalent

1. Pointwise, a real symmetric two-by-two matrix is negative definite if and only if its trace is negative and its determinant is positive.
2. Along a connected continuous matrix path that is negative definite at one point, positivity of its determinant everywhere is sufficient to preserve negative definiteness everywhere. Thus, under the branch-continuity hypothesis and the near-one anchor, the two determinant inequalities imply both trace inequalities. A proof is in `direct_attempt.md`.
3. At a hypothetical first loss of negative definiteness for `Kp_odd`, the exact null-vector equation is the two-switch Green-kernel equation displayed in `direct_attempt.md`.

## Boundary and degenerate cases

- `R=1` is not in the target, but its rescaled right limit supplies a strict anchor.
- `R=infinity` is not in the target. The accepted asymptotic chart supplies strict signs for all sufficiently large finite `R`.
- A zero sector determinant is a genuine failure of the target even if numerical conditioning is poor.
- A double zero matrix at a first loss is not silently excluded. It is an explicit exceptional case of the first-zero obligation.
- Switch collision and non-finite-interior charts are outside this contract.

## Permitted outcomes

- A complete proof of all four signs.
- An exact counterexample on the prescribed branch.
- A rigorous compact-interval or first-zero reduction with the exact remaining sign obligation.

## Completion criteria

Completion requires a rigorous argument, valid for every finite `R>1` on the branch, that closes both sector determinant signs. The inertia bridge may then close both trace signs. A candidate completion must be independently audited before any canonical promotion.

## Answer space

The result must decide whether the exact branch-local negative-definiteness statement is proved, refuted, or still open with a strictly smaller exact gap.

## Acceptance criteria per subproblem

- `KP-DET`: prove `det Kp_odd(R)>0` for every finite `R>1`, or give an exact branch witness with determinant at most zero.
- `KO-DET`: prove `det Ko(R)>0` for every finite `R>1`, or give an exact branch witness with determinant at most zero.
- `KP-TRACE` and `KO-TRACE`: close directly, or derive from the determinant signs and the strict near-one inertia anchor.

## Results that do not count as completion

- A finite numerical scan.
- Positivity only near `R=1` or only for large `R`.
- A derivative formula that assumes invertibility of the same Jacobian whose nonvanishing is the target, without a separate continuation argument through a possible singular point.
- A proof for SUP, a non-symmetric branch, or a differently normalized sector matrix.
- A claim about global `G1'`.

## Forbidden moves

- Numerical evidence as proof.
- Conflating `Kp_odd` with the raw odd sector `Ko`.
- Using the superseded large-`R` exponents `R^(-7/2)` or `R^(-9/2)`.
- Treating `x'(R)=-J^{-1}F_R` as available at a possible first zero of a sector determinant.
- Silent expansion of the contract to branch existence, uniqueness, SUP, or global `G1'`.

## Tool, citation, and search constraints

- `rigorous-open-math-research` v1.9.0 closure-first protocol is binding.
- No subagent delegation by this planner.
- No project-local Python tool is run or copied.
- No web result is used as a proof premise. The bounded novelty record is status context only.
- All numerical material is labeled `EVIDENCE` and not proof.
- No commit or push.

## Ambiguities or competing interpretations

The named frozen artifacts prove a near-one branch and a separate accepted large-`R` branch chart. They do not, by themselves, re-prove a single globally connected all-`R` branch. The task packet treats the prescribed all-`R` branch as the object of study. This run therefore makes matrix-sign conclusions conditional on that object and records global branch construction as outside the sign contract rather than silently claiming it.

## Contract audit

The normalized target agrees with `refs/source_contract.md`. It preserves the INF-only, `n=2`, symmetric, finite-interior, branch-local scope. The matrix convention correction in the frozen addendum has been applied. The four frozen parent hashes and three workspace reference hashes were checked. The contract does not claim global novelty or global `G1'` closure.
