# Round 11 local Lean author handoff

This packet is an author delivery. It does not contain independent blind readback, semantic acceptance or a full mathematical audit of either round11 report. The authoritative final machine status and hashes are in `summary.json` and `source-environment-binding.json`.

## Delivered mathematics

`project/AuditRound11.lean` contains 14 named theorems including the conjunction root, plus 12 definitions/abbreviations. The block algebra quantifies over every natural `n` using `Fin n ⊕ Fin n` and real matrices. It proves the invertible sum/difference basis, transfer of reflection relations, the zero diagonal blocks for anticommutation and zero cross blocks for commutation, determinant invariance, and the sign `(-1)^n` in the cross-block determinant. The physical-reflection increment is exactly `-Pv`, with the preserving/reversing parity equivalences made explicit.

The boundary part proves the two determinant identities for every real `L`, positivity when `L≥4`, and unique solution of the four-dimensional real boundary system for every natural `L≥4`. The explicit matrix entries are formalized; deriving those entries from polynomial traces and connecting solvability to a Sobolev approximation argument are outside this packet.

`contract.md` states every interface and limitation. `contract.json` contains the complete exact expected conjunction and no reference to the root as its own specification. It was generated from declared signatures, so matching it does not replace a semantic audit.

## Evidence and failures

- `declarations-full.json`: all 37 actual namespace declarations, including 11 generated declarations, with full names, explicit types, universes, binder kinds, definition bodies and actual transitive axioms. The 14 count refers only to authored theorem names.
- `commands/print-01/stdout.log`: native `#print` and `#print axioms` for all 26 authored declarations.
- `evidence/exact-root-01/run-manifest.json`: unchanged installed verifier's actual root compilation, expected-type comparison, dependency closure, complete loaded-module inventory and source/environment hashes.
- `commands/receipt-recheck-01/`: saved-receipt consistency and current module-resolution check. This check is not another kernel replay or semantic review.
- `author-checks.json`, `closure-controls.json`, `execution-summary.json`: actual author checks and positive/negative controls, with immutable command pointers.
- `commands/main-01/`: preserved first failed compilation, including the exact old source and diagnostics. Later compilation succeeds after fixing matrix-vector notation scope and completing the final block simplification.
- `environment-baseline.json`, `readonly-postcheck.json`: runtime/package identities and the bounded read-only preservation checks. No complete Mathlib copy is included.

Math negative controls intentionally fail on the determinant sign, wrong diagonal-block formula, swapped boundary formula, and wrong physical-reflection sign. Verifier controls separately check an accepted closed target, rejected hidden axiom dependency, rejected expected-type mismatch, and rejected missing declaration. A file containing an unrelated axiom can still supply an axiom-free target; its contaminated target must fail closure.

The proof source includes no `sorry`, `admit`, extra axiom or unsafe declaration. Conjunction premise binder linter warnings are retained and harmless: the premises remain visible in the exported propositions. All allowed foundational axiom usage is extracted from the real declaration closure, not inferred from a text scan.

## Routing to new reviewers

Give a fresh blind reader only `formal-only/packet.json` and its listed files. The main source contains no comments and was copied unchanged and compiled separately; the packet has no intended prose or external-report conclusion. Give a different comparison reviewer the blind readback, contracts, original input snapshots and exact machine evidence. Both stages are pending; this author created no subagent and issued no independent acceptance verdict.

The exact relation to the physical ordering, symmetric basepoints, nonzero breaking directions, polynomial boundary traces, complex residuals, ODE/Python computations and Sobolev closure remains as stated in `contract.md`. No claim of full formalization should be attached to this packet.
