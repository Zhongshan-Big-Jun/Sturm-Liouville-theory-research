# Final Scientific Reconciliation for `R-20260825T100044Z-b4-m3-blueprint`

## Reconciliation status

- Target: `CLM-SL-B4-M3-TARGET-V1`.
- Frozen mode: `prove_or_refute`.
- Planner decision: `CANDIDATE_COMPLETE_MIXED_PROOF_AND_REFUTATION`.
- Blueprint completion decision: **not yet canonical complete**. The mathematical-content gate for the frozen M3-only contract is reached at candidate level, but the contract's independent-review, immutable-proposal, deterministic-integration, and trusted-closure/refutation gates remain outstanding.
- New mathematical research route required before proposal review: **no**.
- Next stage: prepare an immutable proposal that keeps corrected positive claims, refuted legacy claims, and the source-normalization failure as distinct graph records; then obtain one fresh independent mathematics review and invoke deterministic integration only after approval.
- Formalization status: `not_requested` (`formalization_mode: off`).
- This document is planner reconciliation only. It adds no proof step, performs no independent review, and does not promote any candidate statement.

## Immutable bindings

### Frozen contract and snapshots

- Frozen problem contract: `problem_contract.md`, file SHA-256 `6dc56880458e66119f66c2a16f33df65afa799e03bbc681db5809e127e585e19`.
- Canonical Blueprint snapshot: `sha256:972fe8d8f84a98b1eb9abee896d5f19aacf0514c7226d06646bbf42a38d12793`.
- Canonical inventory snapshot: `sha256:88c9b2d30ddd06ffd6531ccad7c76129ea658b442f676b5831f1f073fdab8aa0`.
- The canonical graph was empty at route planning. None of the results below is currently in trusted closure.

### Round-001 branch results

- Route `route-001-finite-r-branch-certification`:
  - machine status: `candidate_proof`;
  - embedded result hash: `sha256:a3f4499dc11735849efe2c55322a929cd54f73232565fa0116b9330a4e7d2b8c`;
  - finalized-envelope file SHA-256: `cab5f43162bae1aea313d388a6930863bb90ede307e9c734ec3980098597aa7b`;
  - candidate package `candidate_branch_proof.md`: `sha256:0f609135b8d8bd2c9d830d0c9b86ef3b41454c217578a18992c76a9afad404d8`;
  - theorem statement: `sha256:b717ff0832a4ee050668eb04dc51d0056d8853235ce47d9af38cbc16a31870f2`;
  - source-failure package: `sha256:8e45d6a741b1e5e8cad56f3901309e60eff263fae46a7b3c528f6a3c3dd0a4b6`.
- Route `route-002-noninteger-balance-classification`:
  - machine status: `candidate_proof`;
  - embedded result hash: `sha256:08af2e96bd4e250d5080d4bdbfc5136f54042ea423904658866b29425d5ea228`;
  - finalized-envelope file SHA-256: `03e895073021fdb06f8aef106cd0bb2323e933389b38f864e34e0ee90a550222`;
  - proof package `proof_package.md`: `sha256:88be4d4c2a987729706aa8c7cf7860c9ede0a53f5bdd5732019fc683f7695008`;
  - completion report: `sha256:c4c952f9b2f093bec5b866d056cd959b0e335ff335a311b3d967847f1095ca61`;
  - normalization audit: `sha256:22caadc22e1c263af46bc980ee5c366e85a54482c4bd89f931ac6d32292054f6`.

### Round-002 successor result

- Finalized plan `plan-002.final.json`:
  - embedded plan hash: `sha256:a326e355533af36262d1a754436cd77266159168891864e968148293f7bea267`;
  - file SHA-256: `432df3e2d4dc19d886097482a39e4d8b8b052a98e4302ca039cfbeea02d8e2a9`.
- Route `route-003-observable-determinant-closure`:
  - machine status: `refuted`;
  - embedded result hash: `sha256:3a788d04113881f6ba61d0e9a368b38dd01d23099227b023a7fba0432a98e7a3`;
  - finalized-envelope file SHA-256: `bfd4143940bba9490e69f028bf72abdd3bfad85672ead107903ce3dd1aabd686`;
  - immutable refutation package `observable_determinant_refutation.md`: `sha256:6d1c8cbbc7cb68b569675fcad5854288692f4fbc17ae87a76d8768ea8afd0dd8`;
  - normalization and symbol contract: `sha256:4fdc1adf500d4d798de904e7dd81897c0d11fe00e99e17003c9084a8e525b1a8`;
  - finite-`R` remainder and sign bridge: `sha256:f3fc4a793b667e93c272c3358f1a5c57f3df75b7aa281dd9537dc2ae2f505917`;
  - exact replay certificate: `sha256:adc1bc744aaa2ec4c0d5f03eedb625f9570c6369d4c0fbf40baba086f4e9d899`;
  - reproducibility manifest: `sha256:2efd9ec66d779d19755b1e91a19ca704463fc7c90d187cf383dc968bea6116ea`.

## Round-to-round scientific reconciliation

### Exact agreements

All three route results use the same frozen variables and scope:

- `R > 1`, `u = R^(-1/6) -> 0+`;
- the exact `E1 = E2 = E5 = E6 = 0` finite-`R` system;
- the locally unique real, symmetric, band-consistent, finite-interior `n = 2` INF germ;
- no propagation to M1, M2, SUP, `n >= 3`, general `(G1')`, global reflection symmetry, or another singular chart.

The two independently authored round-001 packages agree exactly on the candidate branch data

```text
kappa^3 = 18*pi - 48/pi,
A0 = 2/kappa,
B0 = 1/kappa,
Cbr0 = 16/(pi*kappa),
K1 = C1 = 0,
```

an even analytic germ in `v = u^2`, an `O(u^2)` coefficient remainder, and existence/correspondence for every sufficiently large finite `R`. Route-003 explicitly replays every seed and branch coefficient that its successor calculation uses and reports no disagreement with either package.

The round-001 nondegeneracy descriptions are compatible, not contradictory:

- route-001 gives the combined blown-up Jacobian determinant `-6*(3*pi^2-8)/kappa^8`;
- route-002 factors the same local resolution through sequential determinants `-pi/16` and `16/kappa^5`.

Route-003 reconciles the coordinate names `Delta = q = (A*K-2)/u^2`, with the subsequent `X,Y` blow-up, and reports the same analytic branch.

### Source-normalization failure

Both round-001 routes independently identify the same first invalid source step: the D-side powers of `u` in `scripts/_gapn2_largeR_Pbuild.py` do not reproduce the D-side half-mass in the exact closed residual. Route-003 excludes that staged D-side E5 cascade and regenerates the masses from the exact formula.

This source failure must remain a separate accepted research-state/refutation record. It must not be silently folded into the corrected branch theorem. In particular, the following legacy claims are not premises of the corrected packages:

- staged `E5_5 = 1/(2K^2)`;
- forced nonzero odd pair `(K1,C1)`;
- the even-only contradiction derived from that coefficient;
- downstream E5 or observable coefficients that were not regenerated from the exact closed mass formula.

The earlier multistart observation that a truncated integer-power system moved toward `K0 -> 0` remains `EVIDENCE` tied to the defective staged normalization. It is neither a proof of nonexistence nor an independent refutation and must not be promoted.

### No exact route disagreement

No exact hypothesis, scope, quantifier, seed, normalization, or branch-correspondence disagreement remains among the finalized routes. Route-003's new statements address obligations deliberately left open by both round-001 routes; they do not contradict the corrected branch theorem.

Route-003 additionally binds two exact sector-definition sources:

- `scripts/_gapn2_rawko_closed.py`, `sha256:8bb79393282c481a0b83332e044bf5740d0809086d7fabce3d24207242c04b6e`;
- `scripts/_gapn2_largeR_probe2.py`, `sha256:b0d5589920bbae963da2f6483bec85576a060b47a5351d75bab0274a5bfd00e7`.

These are used as replayed definitional sources, not trusted theorem premises. Their addition does not change the frozen target, hypotheses, or quantifiers, but the final proposal and reviewer must bind and audit their statement fidelity, basis conventions, and source-policy provenance explicitly.

## Frozen completion-contract accounting

| Frozen obligation | Reconciled candidate disposition | Epistemic label |
| --- | --- | --- |
| Determine whether a finite, nondegenerate real branch exists in the frozen finite-interior `n=2` INF geometry | Exists with the exact seed above, an even analytic `u^2` germ, nondegeneracy, controlled remainder, and all-sufficiently-large-finite-`R` correspondence | `CANDIDATE_COMPLETE_PROOF`, pending review/integration |
| Identify `{K0,K1,C0,C1}` or corrected replacements | `K0=kappa`, branch `C0=16/(pi*kappa)`, `K1=C1=0`; `A0=2/kappa`, `B0=1/kappa` | candidate established claim |
| Close `m3D-m3N` | `m3D-m3N = -(4/kappa^5)R^(-2/3) + O(R^(-1)) < 0` for all sufficiently large finite `R` | candidate established claim |
| Resolve the upstream consistency relation called `C=0` | The branch coefficient is renamed `Cbr` and is positive. The distinct upstream scalar is `Chi_up = 3/2 + 4/(pi*kappa) + O(R^(-1/3)) > 0`; therefore `Chi_up=0` is false | candidate refutation plus corrected claim |
| Prove or refute `det Kp_odd ~ c1 R^(-7/2)` | Refuted. Corrected law: `(128*kappa^2/pi^2)R^(-10/3) + O(R^(-11/3)) > 0` | candidate exact refutation plus corrected claim |
| Prove or refute `det Ko ~ c2 R^(-9/2)` | Refuted. Corrected law: `(2048*kappa^2/pi^4)R^(-13/3) + O(R^(-14/3)) > 0` | candidate exact refutation plus corrected claim |
| Give normalization, nonzero constants, signs, and a finite-`R` bridge | Orthonormal mirror bases, Green finite-part convention, exact positive coefficients, analytic normalized quotients, compact derivative bounds, and existential `R0` are supplied | candidate complete within M3 scope |

The frozen quantifier requires statements for all sufficiently large finite `R`, not an effective decimal `R0`. The existential uniform bridge returned in `finite_R_remainder_and_signs.md` matches that quantifier. Lack of an optimized or numerical `R0` is not a remaining mathematical obligation under the frozen contract.

The unclassified charts `K -> 0`, `K -> infinity`, nonunit limiting `k3/k2`, and vanishing phase denominators are outside the finite, nondegenerate target branch. Since the requested branch has been constructed in the frozen chart, global classification of those other geometries is not required to complete this M3-only target and must not be inferred from it.

## Claims that must remain separate in the proposal graph

### Corrected candidate claims

1. Existence, local uniqueness, even analyticity, seed, remainder, eigenvalue indexing, band consistency, and finite-`R` correspondence of the corrected finite-interior branch.
2. The exact negative leading law for `m3D-m3N`.
3. The exact positive leading value and finite-`R` sign of `Chi_up`.
4. The corrected positive `det Kp_odd` law with exponent `R^(-10/3)`.
5. The corrected positive `det Ko` law with exponent `R^(-13/3)`.
6. The normalization and remainder bridge needed to connect each leading law to the exact finite-`R` branch.

These are candidate proof claims until fresh review and integration.

### Legacy claims to refute explicitly

1. The staged hard coefficient `E5_5 = 1/(2K^2)` for the exact closed residual.
2. The resulting forced odd-component/even-only-obstruction claim.
3. The upstream assertion `Chi_up = 0` on the corrected branch.
4. `det Kp_odd ~ c1 R^(-7/2)` with nonzero `c1`.
5. `det Ko ~ c2 R^(-9/2)` with nonzero `c2`.

Each refutation must bind its exact attacked statement and source normalization. The route-003 machine status `refuted` applies to these legacy successor assertions. It must not be misread as refuting the existence of the corrected branch or as automatically setting the overall research goal to `refuted`.

### Evidence-only historical records

- numerical continuation values;
- high-precision determinant-ratio checks;
- multistart convergence toward `K0 -> 0` in the defective staged system;
- numerical exponent fits.

These may remain provenance or adversarial evidence but cannot enter the trusted closure.

## Remaining obligations and next-stage gate

No new mathematical route is required before final proposal review. According to the finalized packages, there is no unresolved mathematical step inside the conditional M3-only proof/refutation package.

The following workflow obligations remain and are not mathematical research routes:

1. Create an immutable proposal that binds the frozen contract, both round-001 branch packages, the route-003 refutation package, normalization map, remainder bridge, exact replay certificates, and all source hashes.
2. Represent corrected claims and refuted legacy claims as distinct claim/inference records with exact statement hashes and accurate statuses. Do not overwrite or silently mutate a frozen legacy statement.
3. Run deterministic proposal validation.
4. Assign one fresh reviewer who is absent from the coordinator, planner, all three researchers, all artifact authors, and all proposal contributors.
5. Require definition, logic, boundary, and adversarial audits covering:
   - the exact closed-mass transcription and Pbuild failure;
   - branch-coordinate and quantifier fidelity;
   - standard analytic IFT and Sturm inputs;
   - overloaded `Cbr` versus `Chi_up` notation;
   - sector bases, signs, prefactors, Green pole subtraction, and omitted-jet audit;
   - uniform finite-`R` remainder and sign bridge;
   - the distinction between the route-003 subclaim refutations and the overall goal outcome.
6. After approval, invoke deterministic integration and recompute trusted closure/refutation status.

A new research route is reopened only if fresh review rejects a substantive branch identity, source transcription, determinant coefficient, normalization convention, or remainder argument. The restart target must be the first rejected step identified by that review; no speculative round-003 route is planned now.

## Final decision

```text
research_content_status: candidate_complete_mixed_proof_and_refutation
mathematical_route_needed_before_review: no
proposal_review_ready: yes
canonical_goal_status: open_pending_review_and_integration
transaction_status: not_submitted
formalization_status: not_requested
```

After successful review and integration, the overall M3 research goal should be closed as a resolved prove-or-refute task with mixed subclaim outcomes: the corrected branch and alternative asymptotic laws established, and the explicitly attacked legacy assertions refuted. Before that receipt exists, neither `solved` nor `refuted` may be assigned canonically to the overall goal.
