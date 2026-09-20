# Fourth-round Lean author contract

Status: AUTHOR EVIDENCE ONLY. No independent acceptance, semantic-review verdict, canonical integration, status upgrade, commit, or push is asserted by this package.

## Source and object identity

The only project file authored here is `lean-proof/SL/AuditRound4.lean`, namespace `SL.AuditRound4`. It contains 41 theorems and 23 definitions. Exact elaborated types, universes, binder kinds, definition bodies, and dependency names are in `final/declarations.json`; readable and fully explicit exports are adjacent. These exports were produced by importing `final/build/SL/AuditRound4.olean`, not by parsing theorem signatures from source.

Source SHA-256: `491d8de06ded428de008dbc41dc83f68fe37b87a3af128be01664c418a4ba93e`.

Inspected root object SHA-256: `018651fe7c2a053f491a68642300550602fdc6de217ffe6f40bf4b8e5b8cb921`.

The informal contract comes from the two supplied files, frozen in `source-snapshot/`: `proof_audit_round4_20260920.md` and `constructive_repairs.md`. Those attachments are author inputs, not evidence of independent approval. `ContractChecks.lean` separately checks that the imported P,Q,R definitions equal the explicit formulas in constructive repair B, and that the principal theorem elaborates to the literal factorial-scaled recurrence and second differences. This is an author-written correspondence check, not independent semantic review.

## Domains and indexing

The general recurrence, difference kernel, finite summation, conjugacy, and reduction results are polymorphic over a Lean `Field K`. The concrete parity coefficients, factorial scaling, table example, and remainder sequence are over `ℚ`. The parameter assumptions in the concrete recurrence chain are `ε = 0 ∨ ε = 1` and `c ≠ 0`. Thus that chain covers positive rational c and also negative rational c; it is not a formal all-real-parameter theorem.

All third-order equations use `j = n + 3` with `n : ℕ`. The new `second_difference v n` is `v(n+2) - 2*v(n+1) + v(n)`, so it corresponds to the input's `d_(n+2)`, not `d_n`. `difference_weight ε c n` likewise means the input's `a_(n+2)`.

`p`, `q`, and `r` select the existing exact `PEven/QEven/REven` or `POdd/QOdd/ROdd` objects; their definitions are included in the exported local definition closure. `factorial_weight ε j = (2*j+ε)!` cast to ℚ. `scale_factor ε c j = c^j / factorial_weight ε j`, and `scaled_sequence ε c μ j = scale_factor ε c j * μ j`.

## Checked local mathematics

1. `factorial_weight_succ`, `factorial_weight_ne_zero`, and `factorial_step_ne_zero` prove the actual two-step factorial identity and cancellation hypotheses for every natural index. `parity_coefficient_factors` proves all three P,Q,R multiplier identities for both parities: P/(c*S_j)=2+θ_j, Q/(S_j*S_(j-1))=1+2θ_j, and c*R/(S_j*S_(j-1)*S_(j-2))=θ_j, with S_j=(2j+ε)(2j+ε-1). `scaled_coefficients` binds these to the actual factorial scale rather than a formal placeholder factor.

2. `moment_iff_scaled` and `moment_iff_second_difference` are full-sequence equivalences for the input equation c²μ_j=P_jμ_(j-1)-Q_jμ_(j-2)+R_jμ_(j-3). The general `recurrence_iff_second_difference` has no positivity or division assumptions and proves the exact equivalent first-order law for the second differences.

3. `difference_weight_recurrence`, `moment_difference_formula`, and `moment_finite_reconstruction` give every scaled moment sequence from its first two values and its initial second difference, with an explicit finite double sum of the factorial difference weights. `first_difference_sum` and `reconstruct_second_difference` prove the finite summation identities for arbitrary field-valued sequences. This is a finite-sum sequence reconstruction, not a proof about an infinite tail Φ.

4. `zero_second_difference_iff_affine` identifies the whole kernel of the second difference as v_n=v_0+(v_1-v_0)n. `affine_solution`, `scaled_affine_moment`, and `affine_moment_solution` construct arbitrary affine scaled solutions and unscale them back to actual moment solutions. `normalized_solution_with_zero_term` proves a solution with μ_0=1 and μ_3=0 for both parities and every nonzero rational c. It does not infer termwise nonvanishing from normalization.

5. `reduction_residual_identity` is the corrected residual identity for products z_j=E_j*r_j. It requires that E solves the recurrence but requires no division or nonzero assumption. `reduction_product_iff` gives its full-sequence equivalence. `reduction_iff` gives the quotient-difference equivalence under the explicit assumption `∀ j, E j ≠ 0`. It reuses the existing checked `ThirdOrderMinimal.reduction_named` in one direction and proves the other direction via the residual identity.

6. `integrate_from_zero` reuses `ThirdOrderMinimal.withInitial` with its parameter adjusted to r_0+s_1. `integrate_initial` establishes r_0, r_1=r_0+s_1, and r_2=r_0+s_1+s_2. `integrate_increment` and `reduction_reconstruction` bind the reconstructed solution to the original reduced differences at every positive index. Reconstruction reuses the existing `reduction_converse`, recompiled from an import-restricted source copy. There is no hidden assumption s_0=0 or s_1=0.

7. `table_cancellation` proves the general rational-function cancellation for a=τ+1/2, b=τ/2, cc=τ, d=0, with both j and j+τ nonzero. `missed_table_parameter` discharges those denominator conditions for the audit's τ=-3/4 at every positive natural j. `missed_table_not_in_old_branches` checks that both old b formulas miss -3/8. This repairs a parameter representation; it is not a new classification of all rational ratios.

8. `legendre2` and `legendre3` are the explicit polynomial expressions (3x²-1)/2 and (5x³-3x)/2. They are not identified with a separate library's Legendre object here. `low_mode_representative_differences` proves the differences 1/a and x/b algebraically over any field; `low_mode_difference_nonzero` proves nonidentity at x=0 and x=1 under nonzero a,b. No Gram-Schmidt, square-root normalization theorem, integral, or norm computation is encoded by these lemmas.

9. `coefficient_step` records the supplied a_(n+2) recurrence. `remainder_coefficients_from_initials` checks a_4=1+15/c and a_6=1+105/c+945/c² from the initial values. `remainder_identity` proves a_6-(63/c)a_4=1+42/c. `remainder_unbounded_on_reciprocals` proves that for every rational bound M and natural cutoff N there is n>N with positive c=1/(n+1) and remainder>M. This is an explicit arbitrarily late algebraic counterexample family; no topological `Tendsto` or Lean `IsBigO` theorem is claimed. Lean's totalized division permits the standalone identity at c=0, but all reciprocal examples use positive c.

10. `printed_reduction_counterexample` evaluates the exact old printed intermediate expression at c=1,j=3, with z-scaled factorial E+ and E-, to 69/224. `corrected_reduction_same_data` evaluates the corrected expression on the same data to zero. These are concrete residual checks, separately from the generic sequence theorems.

## Compiler, imports, and axiom boundary

The executable was the requested native Lean 4.31.0 (commit 68218e876d2a38b1985b8590fff244a83c321783). `environment.json` pins its executable and ten executable/DLL files total, configuration files, and package manifest. No dependencies were downloaded and no whole-project Lake build ran.

The four original local dependencies import all Mathlib. The first broad import was cancelled after 379.79 seconds and retained as a failed/cancelled attempt. To keep local checking bounded, external copies of Basic, ThirdOrder, ThirdOrderClosedForms, and ThirdOrderMinimal replace only the initial `import Mathlib` line with an explicit smaller import list. Every byte after that line is equal to the original source; `DEPENDENCY_ADAPTATION.json` and source snapshots record this. All four copies were freshly compiled into scratch. `LEAN_PATH` excludes the project's `.lake/build/lib/lean`, so no stale project-local object is used. These checks certify the actual external imported objects and their unchanged mathematical bodies, not successful recompilation of the original broad-import project.

Inspection loaded 3217 modules. Their actual .olean files and available private/server/IR companions are fully hashed in `final/module-artifact-hashes.json` (12853 artifacts). The declaration dependency graph contains 6247 nodes. For each of the 64 exported declarations, the transitive closure and axiom set are recorded. Only propext, Classical.choice, and Quot.sound occur; no missing or unsafe node or sorryAx is in the inspected closure. `closure-consistency.json` separately recomputes the per-declaration graph closure and compares axiom sets with Lean's `collectAxioms` result.

The root object is hashed before and after inspection, positive/negative controls, input contract checks, and replay in the execution JSON records. A fresh source compilation into `replay/build/SL/AuditRound4.olean` produced identical bytes. This is reproducibility evidence with the same compiler and pinned dependency environment, not a second independent kernel implementation.

## Explicit exclusions and handoff

Not formalized: ordinary Sobolev or quotient convergence, Gram-Schmidt identification, Legendre orthogonality or norm integrals, fixed-order analytic asymptotics, convergence/positivity of the infinite Φ series, normalized backward-iteration limits, minimal-solution classification, general K(c) closed forms or tail estimates, all-degree rational-function classification, pole arguments, general nonhomogeneous source control, M3/KP results, or any canonical acceptance.

No claim is made that the whole original Lean library has no sorry or that every imported theorem is part of this root's mathematical conclusion. The root's actual closure is the audited scope.

`final/READBACK_INPUTS.json` names the comment-free actual source plus object-derived declarations and definitions for a blind reader. It excludes this contract and the intended input claims. `SEMANTIC_REVIEW_INPUTS.json` separately supplies the inputs, this author contract, exact export identity, and execution evidence for a semantic reviewer. No review verdict has been created by this author.
