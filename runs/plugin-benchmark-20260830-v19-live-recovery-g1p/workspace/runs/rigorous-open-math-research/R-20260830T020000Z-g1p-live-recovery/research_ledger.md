# Research ledger

## 2026-08-30, step 1. Protocol and scope

- Read `rigorous-open-math-research` v1.9.0 `SKILL.md` completely.
- Read only the phase references required for phases 0-3 and closure-first: `phase-01-contract.md`, `phase-23-search.md`, and `closure-first-protocol.md`.
- Read the scoped `workspace/AGENTS.md`, task packet, and all three workspace reference files.
- Decision delta: closure-first is mandatory; no route portfolio or delegation is allowed before the gate.

## 2026-08-30, step 2. Provenance and dirty-tree audit

- Current checkout: `afc6044b22fcab4828cd4bda2aa6c824c4e63d2b`.
- Frozen parent commit object `2f2f41c9caf2a6aa21e74bbab577108d62b7dc01` exists locally.
- Observed unrelated modified LaTeX build files and untracked scratch scripts. None were touched.
- Recomputed all three workspace reference hashes and all four frozen parent artifact hashes. Every value exactly matched the task packet.
- Decision delta: the frozen sources are byte-consistent despite the later dirty checkout.

## 2026-08-30, step 3. Exact source audit

- Rechecked the parent local proof, exact open-core addendum, near-one anchor addendum, and accepted large-`R` observable package.
- Confirmed the corrected convention: `Kp_odd` is the conjugate of the even sector of raw `K`; raw odd `Ko` is a different matrix.
- Confirmed strict near-one negative definiteness for INF.
- Confirmed accepted large-`R` laws with positive determinant coefficients and negative leading traces.
- Confirmed that parent monotonicity is only `EVIDENCE` and that old exponents are superseded.
- Decision delta: endpoint anchors are strict, but they leave a compact middle regime.

## 2026-08-30, step 4. Direct closure-first attack

- Selected the earliest load-bearing sign obligation after contract normalization: `KP-DET`, not a separate trace bound.
- Proved the determinant-only inertia bridge. Positive determinant along a connected continuous sector path preserves the near-one negative inertia, so the trace sign follows automatically.
- Proved the compact first-loss reduction using the strict near-one and large-`R` anchors.
- Wrote the exact `Kp_odd` null-vector equation at a possible first loss.
- Audited the parent M1 derivative route. Its recorded use of `J^{-1}` is conditional on the nonvanishing product of the same two sector determinants. It therefore needs a separate extension or contradiction at a possible singular point.
- Decision delta: four scalar signs reduce to two determinant signs; the first is a compact-middle kernel exclusion.

## 2026-08-30, step 5. Cheapest falsification probe

- Boundary audit: both endpoint regimes are strict, so a counterexample must occur at finite interior `R`.
- Quantifier audit: finite numerical ladders do not decide the universal middle interval.
- Dependency audit: determinant monotonicity remains a viable conjecture, but the current chain-rule proof skeleton is not a self-contained first-zero certificate.
- No exact counterexample was produced.
- Gate effect: two mechanism-distinct bounded tasks can now change the decision, so escalation is justified.

## Observable work data

- Subagents spawned: `0`.
- Web calls: `0`.
- Project-local Python tools run or copied: `0`.
- Frozen files hash-checked: `7`.
- Frozen parent artifacts read: `4`.
- Skill phase references read: `3`, plus the complete skill entrypoint.
- Numerical claims promoted to proof: `0`.
- Checkpoint, run manifest, or handoff files created: `0`.
- End-to-end agent wall time and token/cost counters: unavailable to this collaboration agent. Shell-reported command wall times are observable in the parent trace and are not substituted for end-to-end wall time.
