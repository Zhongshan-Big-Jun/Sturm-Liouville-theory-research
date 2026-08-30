# Closure gate

- Target ID: `KP-DET`.
- Target claim: `det Kp_odd(R)>0` for every finite `R>1` on the prescribed exact n=2 symmetric INF branch.
- Shortest dependency chain: near-one negative inertia and large-R accepted anchor to `KP-DET`.
- First open load-bearing claim: `KP-DET`, exact determinant positivity on the connected branch.
- Why it is load-bearing: determinant positivity preserves negative inertia and makes the trace sign automatic.
- Existing support: `problem_contract.md`, `direct_attempt.md`, and the frozen endpoint anchors.
- Coordinator direct attempt: `direct_attempt.md`, strict inertia bridge and compact first-zero reduction, but no exclusion.
- Cheapest falsification probe: endpoint, quantifier, and dependency audit in `direct_attempt.md`, Section 6.
- Gate decision: ESCALATE
- Spawn trigger: either bounded worker can prove, refute, or strictly reduce the compact-middle first-zero obligation.
- Next decision-changing action: dispatch the two mechanism-distinct bounded tasks listed below.
- Root obligations: OPEN
- Completion manifest: none
- Fresh package audit: pending
- Load-bearing gaps: 2
- Fast-close decision: CONTINUE_REQUIRED
- Frontier upgrade: none
- Last updated: 2026-08-30T02:10:00Z

## Gate record

- First open load-bearing claim: `KP-DET`.
- Statement: `det Kp_odd(R)>0` for every finite `R>1` on the prescribed exact `n=2` symmetric INF branch.
- Direct attempt: `direct_attempt.md`.
- Cheapest falsification probe: endpoint, quantifier, and dependency audit in `direct_attempt.md`, Section 6.
- Exact gate decision: `ESCALATE`.
- Planner conclusion: root obligations remain open.

## Why escalation is earned

The direct attempt produced a strict inertia bridge and a compact first-zero null-vector reduction, but neither excludes the exact kernel equation. The parent determinant-derivative route is not a standalone first-zero certificate because its recorded branch derivative uses `J^(-1)`. Two genuinely mechanism-distinct bounded tasks can now change the decision: one can prove a signed spectral coercivity inequality, while the other can independently exclude or realize the first-zero Jacobi field.

## Bounded worker task 1

- Task ID: `W1-KP-SPECTRAL-COERCIVITY`.
- Exact claim: `KP-FIRSTZERO` is impossible because the quadratic form `(S-KP)` is strictly negative for every nonzero `z` on the compact middle branch.
- Mechanism: exact half-Green spectral decomposition, tail comparison, and a uniform analytic inequality.
- Required deliverable on success: a proof with explicit inequalities that closes `KP-DET`, including all equality cases and the possible double-zero case.
- Required deliverable on failure: one strictly smaller named scalar inequality, with every coefficient defined from exact branch data, or an exact counterexample witness. A numerical scan alone is zero gain.
- Budget stop: attack `Kp_odd` only. Do not open `Ko`, SUP, `n>=3`, global `G1'`, or a broad literature search.
- Decision changed by return: `KP-DET` becomes `PROVED`, `REFUTED`, or `OPEN` at a smaller exact inequality.
- Minimal read set:
	1. `workspace/refs/source_contract.md`, SHA256 `10decf901aca0f6dac72dc3fceacaf91967412cbbd38054a9cfa823d37dfe759`.
	2. `problem_contract.md`, hash to be sealed by the root checkpoint after this planner return.
	3. `direct_attempt.md`, hash to be sealed by the root checkpoint after this planner return.
	4. Parent exact open-core addendum `run_notes_addendum_2026-08-13d.md`, SHA256 `adee3958b6b1979f6687c03f11f23bc525960ba57ae2e6a9506117095b76e50d`.

## Bounded worker task 2

- Task ID: `W2-KP-FIRSTZERO-JACOBI`.
- Exact claim: no finite-interior first-loss point admits a corank-one or double-zero `Kp_odd` compatible with the band equations and half-string boundary conditions.
- Mechanism: convert `Kp_odd y=0` into a linearized half-string Jacobi field or transfer-matrix transversality condition; use Sturm oscillation, endpoint data, or an exact first-zero bifurcation normal form. This mechanism must not assume spectral-tail domination from worker 1.
- Required deliverable on success: a contradiction proof that excludes both the corank-one and double-zero alternatives, with a branch parameterization that does not invert `J` at the singular point.
- Required deliverable on failure: an exact singularity condition or exact branch witness, plus its implication for `KP-DET`. Numerical conditioning is not a witness.
- Budget stop: attack the first-zero `Kp_odd` obligation only. Do not retry determinant monotonicity through `J^(-1)` and do not open `Ko` unless a `Kp_odd` identity algebraically forces it.
- Decision changed by return: `KP-FIRSTZERO` becomes `PROVED`, `REFUTED`, or is replaced by a strictly smaller transversality obligation.
- Minimal read set:
	1. `workspace/refs/source_contract.md`, SHA256 `10decf901aca0f6dac72dc3fceacaf91967412cbbd38054a9cfa823d37dfe759`.
	2. `problem_contract.md`, hash to be sealed by the root checkpoint after this planner return.
	3. `direct_attempt.md`, hash to be sealed by the root checkpoint after this planner return.
	4. Parent local proof `docs/SL_gap_nge2_symmetry_local_proof.tex`, SHA256 `151c7ec65a67789a043b01a46f6c87c40e6827e9994be9fb4be88a45da0c0aaa`.
	5. Parent exact open-core addendum `run_notes_addendum_2026-08-13d.md`, SHA256 `adee3958b6b1979f6687c03f11f23bc525960ba57ae2e6a9506117095b76e50d`.

## Open obligations after the gate

1. `KP-FIRSTZERO`, hence `KP-DET`.
2. `KO-DET`, not yet attacked because closure-first stops at the earliest load-bearing claim.
3. The two trace obligations, which are blocked only by their determinant obligations under the proved inertia bridge.

## Control restrictions

- This planner dispatched no worker.
- The root owns all run manifests, checkpoint states, resume receipts, handoff files, and in-flight reconciliation.
- No completion manifest or completion audit is created because the root theorem is open.
