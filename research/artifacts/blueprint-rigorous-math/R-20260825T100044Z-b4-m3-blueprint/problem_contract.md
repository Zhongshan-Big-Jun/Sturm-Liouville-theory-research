# Frozen Problem Contract

- Run ID: `R-20260825T100044Z-b4-m3-blueprint`.
- Contract version: `1`.
- Frozen at: `2026-08-25T10:11:00Z`.
- Selection source: `README.md`, `research_map.md`, `state/RESUME.md`, and the M3 run artifacts listed below.
- Research mode: `prove_or_refute`.
- Write mode: `closed_loop`.
- Formalization mode: `off`.
- Proposal correction cap: two superseding submissions per proposal lineage. This is not a run-level hard limit.
- User time or token limit: none.
- Backup: not requested, so no canonical backup is created.

## Mathematical objects

Let `R > 1` and `u = R^(-1/6)`. The exact four-equation M3 system is the system named `E1 = E2 = E5 = E6 = 0` in the source artifacts below. Its branch variables are normalized by

```text
k2 = K(u) u,
k3 = K(u) u + C(u) u^5,
p1 = pi/2 + A(u) u^2,
p3 = pi/4 + B(u) u^2.
```

The target branch is the real, symmetric, band-consistent `n = 2` INF branch of the adjacent-gap extremal problem. A candidate branch must correspond to the exact finite-`R` system, not only to a truncated coefficient system.

## Target claim

Determine whether a finite, nondegenerate real branch exists as `R -> infinity`, allowing integer-power, Puiseux, and logarithmic corrections rather than assuming a pure integer-power expansion. If it exists, identify its leading seed and close all of the following M3 outputs:

1. the branch-defining leading data, including the variables represented in the repository by `{K0, K1, C0, C1}` or the correctly rescaled replacements;
2. the leading behavior and sign of `m3D - m3N`;
3. the exact consistency relation denoted by `C = 0` in the upstream M3 artifacts;
4. exact nonzero leading terms, normalizations, and signs for both sector determinants, including a proof or refutation of
   `det Kp_odd ~ c1 R^(-7/2)` and `det Ko ~ c2 R^(-9/2)`.

If the stated branch or determinant exponents are false, a complete refutation must locate the first incompatibility in the full system or prove the correct alternative scale, with a proof bridge to the finite-`R` branch.

## Quantifier and scope contract

- The conclusion concerns the `n = 2` symmetric INF branch only.
- Every asymptotic assertion must hold for all sufficiently large finite `R`, with an explicit remainder or branch-continuation argument.
- No M3 result alone closes M1, M2, general `(G1')`, the SUP branch, `n >= 3`, or global `n >= 2` reflection symmetry.

## Accepted starting status

The repository records the following as previously audited mathematical state, but it is not a canonical Blueprint premise until separately admitted through the immutable proposal workflow:

- `(G2)` is closed for `n >= 2`.
- The local `R -> 1+` branch and the odd/even sector reduction are strict results.
- The M3 cascade records `a0 K0 = 2`, `a1 = -2 K1/K0^2`, and a hard `E5_5` term that forces an odd component.
- Failure of numerical multistart searches near `K0 approximately 3.46` is evidence only and is not an impossibility theorem.

## Forbidden substitutes

- A numerical root, fit, continuation table, or multistart failure without a proof bridge.
- Reusing the failed pure integer-power truncation as if it described the full branch.
- Formal coefficient matching without remainder control and finite-`R` branch correspondence.
- Inferring a determinant sign from a numerical trend toward zero.
- Replacing the determinant target by a stronger unproved positivity hypothesis.
- Transferring an INF conclusion to SUP, `n >= 3`, or all solution components.

## Boundary and adversarial cases

- The degenerate attractor `K0 -> 0` versus the required finite nonzero branch.
- First appearances of odd, Puiseux, or logarithmic terms.
- Singular behavior at `R = infinity` versus existence for every sufficiently large finite `R`.
- Separate normalization and leading signs of `Kp_odd` and `Ko`.
- Spurious roots of truncated systems and branch switching.

## Completion conditions

The goal is complete only when a content-hashed proof or refutation package contains the exact equations, branch selection, leading coefficients or alternative scale, remainder control, finite-`R` correspondence, and determinant signs; it then passes independent definition, logic, boundary, and adversarial audits, is integrated by the deterministic Blueprint receiver, and the target is confirmed in the trusted closure or accepted refutation state.

Numerical evidence, a formal series without error control, a partial lemma, a merged partial node, or closure of M3 without the determinant outputs does not complete this contract.

## Bound repository sources

- `runs/rigorous-open-math-research/R-20260812T090000Z-g1prime-g2/problem_contract.md`, SHA-256 `1DE731BA2EEB40B2E20A2F7817DE0F6F1D13D42E888F42CE3D5719E9C2700148`.
- `runs/rigorous-open-math-research/R-20260812T090000Z-g1prime-g2/run_notes_addendum_2026-08-14.md`, SHA-256 `A4B5C8B72B08508E9E8F1A6EAD786E837D0C316A564BA6A6DD06BB7D1D7284CB`.
- `scripts/_gapn2_largeR_closed.py`, SHA-256 `E357D8E447CE998020C8DADC94EB27DB884DD85932D592A9B4331366F8AC13A4`.
- `scripts/_gapn2_largeR_Pbuild.py`, SHA-256 `58C98AF44D074BDFD9412A1541D4A7A393F0CF3E074653C1108964B62EA6CAEA`.
- `scripts/_gapn2_largeR_big.json`, SHA-256 `1E3C924B8CAA4B9424BF666F52BFCB826722DE582D9E90D2658E36F1F0D66F45`.
- `docs/SL_gap_nge2_symmetry_local_proof.tex`, SHA-256 `6C2029FBD71885B8D94131AD93E865F13F42884D75E68A03D2D079BEA79EFE0A`.

## Role ledger

- Coordinator: `/root`.
- Dedicated planner and contract source: `/root/route_planner`.
- Route researchers: unassigned at contract freeze.
- Reviewer: reserved and unassigned; it must be fresh and absent from every contributor identity.

