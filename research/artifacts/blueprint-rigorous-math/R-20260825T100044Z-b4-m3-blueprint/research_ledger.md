# Append-Only Research Ledger

## L-001. Goal start

- Time: `2026-08-25T10:00:44Z`.
- Event: A persistent goal was created to select and close one difficult or high-priority open problem in the repository with the Blueprint v2.3 test workflow.
- Usage baseline: `0` elapsed seconds and `0` tracked tokens at goal creation.

## L-002. Repository and plugin readiness

- Event: The remote was fetched and local `main` was confirmed at `df35eb6357ea1d75551af323848fc06f6e7b84b6`.
- Event: The repository had no Blueprint manifest. The plugin-provided v2.2 mathematics template was reused and deterministically migrated to the separated v1 project layout.
- Canonical snapshot: Blueprint `sha256:972fe8d8f84a98b1eb9abee896d5f19aacf0514c7226d06646bbf42a38d12793`; inventory `sha256:88c9b2d30ddd06ffd6531ccad7c76129ea658b442f676b5831f1f073fdab8aa0`.
- Snapshot contents: zero nodes, zero edges, zero inventory rows.

## L-003. Target triage and contract freeze

- Time: `2026-08-25T10:11:00Z`.
- Planner: `/root/route_planner`.
- Selected target: B4/P1 M3 large-`R` corrected branch and sector-determinant asymptotics for the `n = 2` symmetric INF branch.
- Alternatives retained: B3 equal-width optimum O2; A6 general minimal-solution asymptotic constant `K(c)`.
- Reason: M3 is the repository's exact next action, is a bottleneck for `(G1')`, has reusable audited structure, and has a precise prove-or-refute completion gate.
- Usage checkpoint: `624` elapsed seconds and `136165` tracked tokens.
- Contract artifact: `problem_contract.md`.
- Formalization status: `not_requested`.

## L-004. Seed proposal lineage

- Submission `SUB-20260825-B4M3-SEED-001` was finalized as `sha256:92f916cf413423c337653289757fdd68a3d943e00db90decbd1ce22f5526582f`.
- Deterministic validation rejected `SEED-001` with `INCOMPLETE_MATH_PREMISE_CONTRACT` because the problem-local hypothesis record lacked `contract_explanation`.
- Submission `SUB-20260825-B4M3-SEED-002` superseded `SEED-001`, added the missing explanation, and validated successfully as proposal `sha256:76683263c93b7c8d3226ab089abcc3395152fc6d5a62bf32b2632feddb95ffbe` and validation `sha256:1cfa01299c3952f404d6899b5dde5f96481c81e781d6fbebba59454d6a3f86fb`.
- An independent reviewer semantically approved `SEED-002`, but two consecutive deterministic structure checks reported the three mathematics research-state checks as nonpassing. The stage was stopped under the review contract after the repeated identical structural failure. No review was sealed and nothing was integrated.
- Submission `SUB-20260825-B4M3-SEED-003` is the second and default-final correction in this proposal lineage. It supersedes `SEED-002` without changing the mathematical contract.

## L-005. Final seed validation and fresh review handoff

- Time: `2026-08-25T10:28:13Z`.
- `SEED-003` proposal hash: `sha256:09b2d9d7542ea6d6c1cead3a2a43c6770d86b74365435501b7dc304c83454ecf`.
- `SEED-003` validation hash: `sha256:2e96df56c173fbdd124ea0bd26a32c3f72d2642b7a362cb2d0714a255510ab68`.
- Candidate hashes: Blueprint `sha256:bb65166ce7a7a72676ae5479795da036401455b56c1b4d3e434e663dc49bb521`; inventory `sha256:84a44b31fd51ce8d2c45399e83fe722faff4cd04ae43e66eae156a537887847f`.
- The machine-generated blank review draft was inspected before assignment. It requires only the existing `node_id`, `result`, and `reasoning` fields for each mathematics research-state check.
- A new disposable reviewer, `/root/seed_reviewer_final`, received only immutable inputs and the existing machine-generated draft. Delegation and canonical writes are forbidden.
- Usage checkpoint: `1707` elapsed seconds and `265189` tracked tokens.

## L-006. Seed review stage stopped without integration

- Time: `2026-08-25T10:40:51Z`.
- The fresh independent reviewer completed a full semantic review and approved `SEED-003` with all three mathematics research-state checks explicitly set to `result = valid` in the unmodified machine-generated field shape.
- Deterministic structure attempt 1 nevertheless returned `REVIEW_NOT_PASSING` for exactly those three records and required a full semantic re-review.
- The same reviewer repeated the full semantic review, retained the approval after binding the exact node statuses and validation-closure evidence, and changed no schema fields.
- Deterministic structure attempt 2 returned the identical `REVIEW_NOT_PASSING` reason. Under the review contract, this review stage is stopped after the repeated same-stage error. No review was sealed and no seed proposal was integrated.
- This is a test-plugin review-structure boundary, not a mathematical result and not a terminal condition for the run. The frozen contract and immutable proposal lineage are retained while substantive route research proceeds.
- Usage checkpoint: `2406` elapsed seconds and `305226` tracked tokens.

## L-007. Round 001 route dispatch

- Plan: `round-001/plan-001`, finalized as `sha256:197a723b399296fe371eeb42e55bc188348732cf2beee2d9188aabb99c059a76` against the unchanged empty canonical snapshot.
- Planner: `/root/route_planner`; planner performed route decomposition only and no mathematical research.
- Route `route-001-finite-r-branch-certification` was assigned to `/root/finite_branch_researcher` with mechanism key `finite-r-exact-system-implicit-certification`.
- Route `route-002-noninteger-balance-classification` was assigned to `/root/transseries_researcher` with mechanism key `newton-balance-puiseux-log-transseries`.
- The two first-pass researchers have distinct identities, no delegation, no cross-route access, route-specific artifact directories, bounded query envelopes, and machine-owned result forms.
- Conditional route `route-003-observable-determinant-closure` remains undispatched until reconciliation establishes a finite nondegenerate branch or a rigorously proved replacement scale with a finite-R bridge.

## L-008. Round 001 adversarial correction and seed convergence

- Both independent routes initially replayed an apparent bounded-chart obstruction proportional to `-1/(6 K^2)` from the staged Pbuild source.
- Route 001 rejected that provisional obstruction after comparison with the exact closed formula, an independent staged expansion, and a 100-digit original-residual check. Route 002 independently reproduced the rejection.
- Audited source discrepancy: the D-side coefficient corresponding to `b1 = cos(p1) / k` is shifted by the wrong power of `u` in the staged Pbuild mass term, with related D-side mass factors inconsistent with the exact closed formula. The N-side shifts are consistent. The repository source is not modified; the discrepancy is retained as an audited failed premise.
- Corrected exact leading relations from both routes are `C0 = 16 / (pi K0)`, `q0 = (18 pi - 24 - K0^3) / (6 K0)`, `B0 K0 = 1`, and `K0^3 = 18 pi - 48 / pi`.
- Therefore the positive seed candidate is `K0 = (18 pi - 48 / pi)^(1/3)` and `B0 = 1 / K0`.
- Route 001 reports the full blow-up Jacobian determinant `-6 (3 pi^2 - 8) / K0^8 < 0`. Route 002 independently reports the staged determinants `-pi / 16` and `16 / K0^5`, both nonzero.
- Status remains candidate-level pending spectral-index and INF-branch correspondence, effective neighborhood and remainder control, boundary-chart audit, result finalization, planner reconciliation, independent proposal review, and deterministic integration.
- Usage checkpoint: `6679` elapsed seconds and `397893` tracked tokens.

## L-009. Round 001 finalized candidate proofs

- Route 001 finalized as `candidate_proof`, result hash `sha256:a3f4499dc11735849efe2c55322a929cd54f73232565fa0116b9330a4e7d2b8c`, and proof package `sha256:0f609135b8d8bd2c9d830d0c9b86ef3b41454c217578a18992c76a9afad404d8`.
- Route 001 supplies the exact seed, the full four-variable blow-up Jacobian, a real-analytic finite-R branch with `O(u^2)` coefficient remainder, finite-u nondegeneracy, `lambda_2/lambda_3` spectral indexing, and the INF sign audit. Its `u0` and remainder constant are existential rather than numerically optimized.
- Route 002 finalized as `candidate_proof`, result hash `sha256:08af2e96bd4e250d5080d4bdbfc5136f54042ea423904658866b29425d5ea228`, and proof package `sha256:88be4d4c2a987729706aa8c7cf7860c9ede0a53f5bdd5732019fc683f7695008`.
- Route 002 independently supplies the same exact seed, two-stage nondegeneracy, an analytic `u^2` germ with uniform existential remainder, exhaustion of Puiseux, logarithmic, inverse-logarithmic, mixed, odd, and flat alternatives in the frozen finite-interior chart, and elimination of an interior shifted leading phase.
- Both results remain candidate proofs pending fresh independent mathematics review and deterministic integration.

## L-010. Round 002 observable and determinant closure dispatch

- Planner reconciliation found no exact disagreement between the two seed packages and determined that the conditional successor gate is met without an additional branch research route.
- Plan `round-002/plan-002` finalized as `sha256:a326e355533af36262d1a754436cd77266159168891864e968148293f7bea267`.
- Route `route-003-observable-determinant-closure` was assigned to the new identity `/root/determinant_closure_researcher`, distinct from both round-001 researchers.
- Required outputs are an unambiguous symbol/normalization map, exact `m3D-m3N`, the correctly identified upstream consistency relation, exact first nonzero terms and signs of both sector determinants, and a uniform finite-R remainder/sign bridge. False frozen exponents must be replaced by proved alternatives.
- Usage checkpoint: `7750` elapsed seconds and `448378` tracked tokens.

## L-011. Round 002 finalized correction and refutation result

- Route 003 finalized with calibrated status `refuted` and result hash `sha256:3a788d04113881f6ba61d0e9a368b38dd01d23099227b023a7fba0432a98e7a3`.
- Main exact refutation/correction package: `sha256:6d1c8cbbc7cb68b569675fcad5854288692f4fbc17ae87a76d8768ea8afd0dd8`.
- Corrected exact observable: `m3D - m3N = -(4 / kappa^5) u^4 + O(u^6) < 0`.
- The distinct upstream scalar is renamed `Chi_up`. Its corrected expansion is `Chi_up = 3/2 + 4 / (pi kappa) + O(u^2) > 0`; therefore the old `Chi_up = 0` assertion is refuted and is not the positive branch function `C(u)`.
- Corrected odd-sector determinant: `det Kp_odd = (128 kappa^2 / pi^2) u^20 + O(u^22) > 0`, equivalently the exponent is `R^(-10/3)`, not `R^(-7/2)`.
- Corrected regularized-sector determinant: `det Ko = (2048 kappa^2 / pi^4) u^26 + O(u^28) > 0`, equivalently the exponent is `R^(-13/3)`, not `R^(-9/2)`.
- An ORDER 34 exact guard replay reproduced the ORDER 30 coefficients. Higher branch jets cannot affect the first nonzero determinant coefficients by the proved analytic valuation factorization.
- The uniform finite-R sign bridge uses analytic normalized quotients in `v = u^2`, compact derivative suprema, a positive `v_star`, and `R0 = v_star^(-3)`.
- Interrupted unreduced computation and implementation dry-run failures are retained in the reproducibility manifest. High-precision pole-subtraction and determinant-ratio checks remain adversarial evidence only.

## L-012. Final immutable proposal preparation

- Submission `SUB-20260825-B4M3-FINAL-001` was prepared against the unchanged empty canonical snapshot.
- Proposal author identity: `/root/final_proposal_author`. Mathematical contributors and artifact producers remain the dedicated planner and three distinct route researchers; none may act as final reviewer.
- The final proposal must encode the complete problem premise, proved branch theorem, scale-exhaustiveness result, corrected observable and determinant theorem, separate refutations of the defective source cascade and old asymptotic assertions, and completed M3-only goal state.
- Usage checkpoint: `17389` elapsed seconds and `629818` tracked tokens.

## L-013. Candidate reconciliation and final-proposal retries

- Planner reconciliation was finalized in `final_reconciliation.md`, file SHA-256 `1810e483d2242129f004b9488f77b4216cce141d300770dd8620b31e395f076b`, with decision `CANDIDATE_COMPLETE_MIXED_PROOF_AND_REFUTATION` and no further substantive route required at that stage.
- `SUB-20260825-B4M3-FINAL-001` and `SUB-20260825-B4M3-FINAL-002` were retained as failed immutable attempts. Deterministic validation rejected their explicit `math_refutations` encodings with `MISSING_MATH_REFUTATION`; bounded public-interface probes did not find a schema-conforming redundant refutation item. Validator implementation source was not inspected.
- The final encoding therefore states one corrected established target theorem that proves the exact replacement laws and explicitly excludes the incompatible staged Pbuild cascade and legacy `Chi_up = 0`, `R^(-7/2)`, and `R^(-9/2)` assertions. It does not weaken the frozen M3 completion contract and does not promote historical numerical evidence.

## L-014. Final validated proposal

- Submission: `SUB-20260825-B4M3-FINAL-003`.
- Proposal hash: `sha256:e88cff6fcac76b008da38cba564c35ff01213d15c52cda8cb846a1676586d6be`.
- Deterministic validation hash: `sha256:47f488df8e9ca5229beeded33e58a98ebe8c304ec733d20c322b33b6bd65946d`; `valid = true`.
- Candidate Blueprint hash: `sha256:3b99f2090d73029fa77498a897979e614ddccbb205b613449fdd2181ce6ccc48`.
- Candidate inventory hash: `sha256:0c1e576e4902ffb8720e8a9b7c02a0df1c5425af805f1c9aba05b9968279ed5e`.
- Candidate structure: 9 nodes, 10 typed edges, 3 inventory rows, 3 proved mathematics inferences, no open, blocked, or refuted inference, and no contradiction.

## L-015. Scale-entry gap audit

- A fresh route, `round-003/route-004-scale-entry-lemma-audit`, was commissioned after adversarial review identified a possible circular entry into the bounded IFT chart.
- The route proves directly from the exact `E1` and `E2` tangent identities that `q` and `Cbr` are bounded, applies a first IFT with the phase displacement `y = p3 - pi/4` left unscaled, derives `y = v/K + O(v^2)` and hence bounded `B = y/v`, and then forces `K -> kappa` through the remaining exact scalar equation. Every admitted-class exact zero branch therefore enters the existing secondary IFT neighborhood and equals the unique analytic `v = u^2` germ.
- Proof package: `sha256:0e87c79d2bef460528846c92067c1df72f15304ea0c7cd5f6ba6c158e9d73f56`.
- Reproducibility manifest: `sha256:f9009fc00fe9155ffcc334c36422e483113e6cb9db29969a9b108937a51676c1`.
- Exact replay source: `sha256:9abbe792df1fa5e74e113bdae8553a52d2e564d825a7d8a349052f1533f0c9c0`; passing replay log: `sha256:3afc18c92388027a5f37ffdef5806839c78017610b7e4a5069403f8568eb3c67`.
- This extra package was not shown to or claimed as covered by the final proposal reviewer. The reviewer independently reconstructed and accepted the entry argument from the immutable proposal-bound route-001/002 packages during the required full re-review.

## L-016. Independent final review

- Reviewer identity: `independent-final-reviewer-002`, distinct from the coordinator, planner, proposal author, and all route researchers.
- After deterministic feedback identified incomplete proof-specific and state-specific bindings, the same reviewer performed a second full semantic pass rather than a field-only edit.
- The completed draft covered all 15 required audits, all three proof checks were `valid`, the goal state was `accurate`, and no finding or action remained.
- Immutable review hash: `sha256:40b1f066d827b2cb1a9a42bfdf84cecdc904747bb4b4a1d0b7d5440ab5a4c76f`; verdict `approve`.
- The subsequent review-seal cleanup/event step twice returned the same test-plugin internal path error because its work artifact was outside the Blueprint-root subpath. The stage was stopped after the repeated error. The immutable `review.json` itself had already been written, and the deterministic receiver later verified and accepted that exact review hash. No claim is made that the seal cleanup/event completed.

## L-017. Deterministic integration receipt

- Time: `2026-08-25T18:38:00.863330Z`.
- The single-writer receiver merged `SUB-20260825-B4M3-FINAL-003` with `feedback.reasons = []`.
- Receipt file SHA-256: `a34b92acd9b23eeb82a26649be75a2620b81d38d43f99e96519982ca90565ab4`.
- Receipt-bound proposal, validation, and review hashes independently match `sha256:e88cff6fcac76b008da38cba564c35ff01213d15c52cda8cb846a1676586d6be`, `sha256:47f488df8e9ca5229beeded33e58a98ebe8c304ec733d20c322b33b6bd65946d`, and `sha256:40b1f066d827b2cb1a9a42bfdf84cecdc904747bb4b4a1d0b7d5440ab5a4c76f`.
- Result canonical Blueprint hash: `sha256:3b99f2090d73029fa77498a897979e614ddccbb205b613449fdd2181ce6ccc48`.
- Result canonical inventory hash: `sha256:0c1e576e4902ffb8720e8a9b7c02a0df1c5425af805f1c9aba05b9968279ed5e`.

## L-018. Post-integration verification

- Time: `2026-08-25T18:42:58.574Z`.
- Independent filesystem SHA-256 calculations matched both receipt `result_*_hash` values exactly.
- Blueprint runtime `2.3.2-test.1` reported project `ready`. Deterministic canonical validation returned exit code 0: 9 nodes, 10 edges, acyclic graph, valid typed dependencies, 3 linked inventory rows, 3 proved inferences, zero open/blocked/refuted inferences, zero obligations, and no contradictions.
- Snapshot-bound retrieval confirmed `GOAL-SL-B4-M3-V1` has `status = solved`, `goal_resolved = true`, `research_outcome = proved`, and `requested_mode_satisfied = true`.
- Trusted closure contains the system hypothesis, the finite-`R` branch theorem, the finite-interior scale-exhaustiveness theorem, and the corrected M3 target theorem through all three proved inferences. `math-frontier` is empty, `missing_route_claim_ids` is empty, and all query warnings are empty.
- A separate read-only post-integration verifier independently repeated the receipt, hash, structural, closure, goal, and frontier checks and reported no discrepancy.

## L-019. Closeout usage checkpoint

- Research wall-clock interval from `2026-08-25T10:00:44Z` to the final pre-close checkpoint `2026-08-25T18:44:39.654Z`: `31435.654` seconds (`8 h 43 min 55.654 s`).
- Persistent-goal accounting immediately before closeout: `31309` tracked elapsed seconds (`8 h 41 min 49 s`) and `1556831` tracked tokens.
- The authoritative final token total is the completion report returned when the persistent goal is marked complete; it is reported to the user together with this ledger path.
