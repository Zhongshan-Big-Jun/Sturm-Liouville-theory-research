# Round 3 local Lean author handoff

Role: mathematical author. Machine checking below is complete. Independent blind readback and semantic acceptance remain pending. No independent review verdict is asserted.

## Frozen result and entry points

- Project addition: `/mnt/f/LaTeX/BVE research/lean-proof/SL/AuditRound3.lean`.
- 24 theorems and 10 definitions. Native Lean 4.31.0 compiled the final source with exit 0 and no warnings.
- Source SHA-256: `7e93fae0e42dd572d8d9127e8949c0caaa0ef965c321bf8a11cea46163a6c714`.
- Final olean SHA-256: `8ee57958d54da151f9a1c6a815ec5d6ced9ecc2a0fed43ae07988e76a0756b3a`.
- `final/READBACK_INPUTS.json` identifies clean, hash-bound readback inputs. The statement exports contain actual elaborated types and definition values, without informal intended-theorem commentary. Fully explicit output enables proof printing; `local-definition-closure.txt` also expands reachable local helper definitions, including the recursive function helper.
- `logs/14-unabridged-statement-export.stdout.txt` preserves actual `#print` and `#print axioms` output for all 34 selected declarations. `final/declarations.json` records types, universe and binder information, expression trees, definition bodies, transitive axioms, and the dependency closure.
- The 8032 dependency nodes have no missing constants or unsafe declarations. Transitive axiom sets are subsets of `propext`, `Classical.choice`, `Quot.sound`. No `sorry`, `admit`, new axiom, or `native_decide` is present in the target source. This is closure of the actual declarations, not an independent semantic match to the analytic paper.

## Exact formal scope

All scalar recurrence and rational statements use Lean `Real`. The recurrence predicate includes `u 0 = 0`, `u 1 = 1`, and the second-order equation at every index `n + 2`. A recursive solution is defined and proved to solve it when `c != 0`; uniqueness is proved for all indices.

1. `second_order_decomposition` proves the missing term `B/c * (v-w)` exactly. `second_order_lower_bound` assumes `c > 0`, `B >= 0`, `w <= v`, and the actual recurrence equation. `second_order_exact_iff` characterizes local equality as `B = 0` or `v = w`.
2. `recurrence_monotone_nonnegative` derives nonnegativity and successive monotonicity from the initial data, `c > 0`, and `B n >= 0`, `A n - B n >= c` for every `n >= 2`. `recurrence_product_lower_bound` proves the product bound for every `n >= 1`. `recurrence_product_eq_of_B_zero` proves equality under the explicit all-index `B n = 0` condition and `c != 0`. `product_bound_eq_epsilon` connects the product factors to `1 + epsilon`.
3. The constant recurrence `c=1, A=3, B=2` has the exact solution `2^n-1` for every natural `n`. Its epsilon is zero and its product is one at every index. `constant_recurrence_strict_gap` proves strict inequality at every `n+2`; `no_general_product_equality` refutes the all-index product-equality claim. This includes the initial values, not just one numerical recurrence step.
4. `perturbed_A` and `perturbed_B` are the explicit coefficient formulas from R3-F2. `perturbed_coefficient_difference` proves the full difference including `delta*(c-(2m-2)*(2m-3))`, for real `m != 1`. The `m=4,c=3,delta=1` instance gives `A=63`, `B=70`, gap `-7`; the erroneous expression equals `23` and is unequal to the actual gap.
5. The P2 portion proves rational identities for the stated moment and image-moment formulas, the general perturbation cancellation, the delta complement factorization, and the exact delta values at 2 and 3. All denominator nonzero conditions are explicit in the actual theorem types. These are algebraic identities for defined rational functions.

## Remaining assumptions and excluded conclusions

- The P2 formulas are not proved to equal integrals here. The nonzero norm, parity orthogonality, boundedness/asymptotics of the whole delta sequence, and L2 incompleteness are not formalized. The real-parameter cancellation theorem retains its denominator assumptions; it does not by itself discharge them at all integer indices.
- The coefficient definitions have not been connected by Lean to polynomial differentiation or the Krein operator domain. No analytic completeness, diagonal-space criterion, growth asymptotics, Gamma normalization, or full stability classification is certified.
- R3-F3 was read. No quotient construction, contractive-image density transfer, spectral truncation, or spectral theorem was added. The coordinator's later all-index `|delta| <= 1/(8m)` sufficient condition is outside this target set.
- Existing `StabilityGrowth.lean` and the `sharpA/sharpB/sharpU` part of `Stability.lean` were read. The former already states a lower bound; the latter explicitly sets B to zero. This new module imports only selected Mathlib modules and does not rebuild or mechanically bridge the legacy SL modules.
- Products start at index 2. The nontrivial lower bound is stated for `n >= 1`; it is not claimed at n=0, where the empty product is one while u0 is zero.

## Actual commands, controls, and environment

All Lean commands used project cwd `/mnt/f/LaTeX/BVE research/lean-proof`, whose native Windows path is recorded in every run. The runner sets a semicolon-separated Windows `LEAN_PATH` and passes it through `WSLENV` without path-translation flags. `command-index.json` and `logs/*.json` record exact argv, environment overrides, times, exit codes, executable/runner hashes, source snapshots and hashes, and stdout/stderr hashes.

The executable is `/mnt/f/DevCache/elan/toolchains/leanprover--lean4---v4.31.0/bin/lean.exe`. Its actual version output is in `logs/01-version.stdout.txt`. Project and Mathlib pins are 4.31.0, and all 9 package HEADs match their lake-manifest revisions. `environment.json` also binds the runtime executables and DLLs. The local compiler and existing package artifacts remain a trust boundary; no independent kernel replay or package rebuild is claimed.

Key runs:

| Run | Actual result |
| --- | --- |
| 10-final-clean-build | exit 0, 18.66 s, no warnings; fresh output under final/build |
| 11-inspect-types-axioms | exit 0; initial actual declaration and axiom extraction, preserved under attempts |
| 12-old-product-control | exit 1, unsolved `False`; attempts the false equality at index 2 |
| 13-old-perturbation-control | exit 1, unsolved `False`; attempts the omitted-derivative formula at m=4 |
| 14-unabridged-statement-export | exit 0, 22.74 s; final actual types, definitions, axioms and closure export |

Runs 02-07 are retained author development failures; run 05 is a real denominator-discharge diagnostic. Runs 08-09 succeeded with one style warning, removed before run 10. No failure was relabeled as success. The two old-formula controls are separate deliberate negative checks. Intermediate output artifacts may have been replaced during development; final/build is the uniquely bound final artifact, while each input attempt and compiler log is preserved.

`final/loaded-modules.json` records Lean's actual loaded environment. Both inspections returned the same module inventory. `final/module-artifact-hashes.json` binds 3270 modules and 13077 artifact files (2718265696 bytes), including available private/server/IR companions. Files were hashed after inspection 11 with stable metadata during reads, and metadata was rechecked after inspection 14. The current source and final root object match their actual compile and inspection bindings. This is not a rebuild of the dependency sources.

The exact final compile command is represented by argv in `logs/10-final-clean-build.json`; the inspection command is in `logs/14-unabridged-statement-export.json`. To reproduce in a separate reviewer-owned output tree, copy/adapt this runner's OUT constant and regenerate the inspection output path there, preserving the frozen author files. Do not run an author probe that rewrites these frozen final exports.

## Write boundary and freeze

The author's project write is only the new `lean-proof/SL/AuditRound3.lean`; all other author writes are inside this external lean-author directory. All 43 preexisting SL sources retain their initial hashes. Root AGENTS, old runner/report, plugin skill files and configuration were not edited. `protected-source-comparison.json` records the observed concurrent baseline change: /mnt/f/LaTeX/BVE research/lean-proof/STATUS.md. That path was not written or reverted by this author.

No commit, push, canonical write, full Lake build, dependency fetch, or edit to previous-round evidence was performed. `FINAL_CHECKS.json` gives machine status and pending independent review status. `FILE_HASHES.sha256` and `FREEZE.json` freeze the handoff by content hashes; this is a hash-bound snapshot, not a claim of operating-system immutability.
