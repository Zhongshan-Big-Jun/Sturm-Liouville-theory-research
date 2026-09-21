# Independent finite-check verification: PASS

Execution role: **fresh independent finite-check verifier**. Disposition: **COMPLETE**. No required check failed. This is a bounded finite-check verdict, not a whole analytic theorem certification.

Read scope was PACKET.json, its 39 listed frozen files, installed Python/SymPy/mpmath runtime, and this execution's own outputs. All 39 packet-file SHA-256 values matched; PACKET.json itself was separately hashed. All frozen inputs remained byte-identical after execution and at finalization. `inputs/manifest.json` and all four of its snapshot entries are supplied, packet-listed, and match their SHA-256 and byte counts. Original source paths and historical commit labels were not followed.

The unchanged runner uses the labels `author execution evidence, not independent final review` and `independent executable-check author, not final reviewer`. These describe the provenance of the frozen code. **The execution documented here was performed and checked independently in this directory.**

## Actual process evidence

Executed argv exactly:

```json
["/usr/bin/python3", "-B", "run_checks.py"]
```

Working directory: `/mnt/f/tools/math-audit-round7-20260921/numerical-review-v2`. Started `2026-09-21T12:55:10.819483+00:00`; ended `2026-09-21T12:55:27.951110+00:00`. Actual outer exit: **0**; timeout: false; stderr: empty. Actual captured outer stdout:

```text
normal: exit=0, seconds=6.796039
optimized: exit=0, seconds=7.975391
negative-normal-old-fh: exit=1, seconds=0.821516
negative-optimized-old-fh: exit=1, seconds=1.277627
25/25 in both modes; details identical; both wrong-formula processes rejected.
```

| Child process | Actual exit | Expected exit | Elapsed seconds |
| --- | ---: | ---: | ---: |
| normal | 0 | 0 | 6.796039 |
| optimized | 0 | 0 | 7.975391 |
| negative-normal-old-fh | 1 | 1 | 0.821516 |
| negative-optimized-old-fh | 1 | 1 | 1.277627 |

Every child argv, raw stdout/stderr, source/output hash, timestamp and exit code is preserved in EXECUTION.json and the receipts. All 15 expected runner output files were observed as newly written during this run; none of those files existed before it. The receipts directory already existed and needed no repair.

Both old-FH controls failed at the intended formula comparison, ending with:

```text
RuntimeError: intentional old FH formula rejection: error=26.9404860801202857619399303749492449801291945661366696096904176100696272189699061222717259
```

Both have empty stdout and identical stderr. The expected formula rejection is distinguished from an unrelated crash. No required check failure was suppressed or relabeled. The optional `old-schrodinger` CLI control was not run; its exact counterexample is exercised in group 22.

Runtime: Python `3.14.4 (main, Aug 20 2026, 10:41:58) [GCC 15.2.0]`; SymPy `1.14.0`; mpmath `1.3.0`. Frozen checks use 90 decimal digits; supplemental calculations use 100. Both frozen Python files were inspected and contain zero `assert` AST nodes. The checker imports standard-library modules, mpmath and SymPy and reads itself, the manifest and its four snapshots. It does not import or execute frozen historical scripts.

Two verifier-owned report-preparation commands initially failed: a nested-quote SyntaxError and the resulting missing report-generator file. Their actual exit codes and errors are retained in `independent-execution-66hgfj6g/report_preparation_errors.json` and EXECUTION.json. Only this verifier's report generator was corrected; no frozen program or input was modified, and the required runner was executed once. These report-preparation failures are separate from the successful required checks.

## Completeness and normal/-O equality

The source registers **25 distinct named groups**. Each output contains precisely those names in source order, nonempty details, and all PASS statuses. Each actual stdout contains the corresponding 25 PASS lines and a mode-specific summary. Counts and names were independently recomputed, not inferred from returncode.

There are **16 symbolic/exact mathematical groups, 8 high-precision real numerical groups, and 1 bookkeeping group**. These are groups, not independent theorems; several share eigenpairs or helpers. The separate verification script passed 143 integrity and finite-computation gates, also not theorem counts.

For all groups, `name`, `kind`, `status`, and complete `details` are exactly equal between normal and -O. Their canonical detail digest is:

```text
622ad05ff281de32bfcd9ce839993314e33ab9faf0cb3f92ea77bca135bd8d88
```

Canonicalization: UTF-8 JSON, sorted keys, compact separators, ensure_ascii=False, no final newline. Raw output hashes differ because mode flags and elapsed times differ. Normal has optimize=0 and __debug__=true; optimized has optimize=1 and __debug__=false.

| # | Named group | Evidence type | Normal / -O | Inspected evidence and scope |
| ---: | --- | --- | --- | --- |
| 1 | `W_product_to_sum_general` | symbolic/exact | PASS / PASS | Product-to-sum symbolic identity for the constant-density Wronskian; no variable-density theorem certified. |
| 2 | `W_sum_squares_general_recurrence` | symbolic/exact | PASS / PASS | Symbolic recurrence and n=0 base checked; no audit of the referenced derivation notes. |
| 3 | `W_finite_exact_Chebyshev_certificates` | symbolic/exact | PASS / PASS | Two exact polynomial identities at n=1,2,3,4,5,8,12 (14 identities). |
| 4 | `W_n2_half_counterexample` | symbolic/exact | PASS / PASS | Direct n=2, x=1/2 value is -4*pi; the old -6*pi value differs. |
| 5 | `Taylor_pi4_general` | symbolic/exact | PASS / PASS | Fixed-n x^2 coefficient is 2*pi^4*(n^4-(n+1)^4); independent n=2 sample is -130*pi^4. No uniform remainder bound. |
| 6 | `n2_exact_roots_and_reduction` | symbolic/exact | PASS / PASS | Both roots (11 +/- 2*sqrt(10))/36 satisfy the quadratic, lie in (0,1), and are simple. |
| 7 | `n2_normalized_determinant_exact` | symbolic/exact | PASS / PASS | Four-interface normalized determinant is 7030400000*pi^4/4782969 > 0; independently recomputed by a resultant. No Hessian definiteness implication. |
| 8 | `n2_four_root_order_signs_numeric` | real numerical | PASS / PASS | Four roots ordered in (0,1), residuals <=1e-80, slope signs +,-,+,-; determinant product checked at 1e-75. |
| 9 | `piecewise_L2rho_antiderivative_identity` | symbolic/exact | PASS / PASS | Segment mass primitive checked by differentiation and zero initial value. |
| 10 | `nonstationary_shooting_index_and_residual` | real numerical | PASS / PASS | rho=(1,4,1), a=1/4: two ordered shooting roots with residuals <=1e-75 and abs(f(a))>1. |
| 11 | `exact_segment_normalization_vs_quadrature` | real numerical | PASS / PASS | Both weighted segment norms compared with quadrature at 1e-80; reflected squared eigenfunction values compared at 1e-75. |
| 12 | `symmetric_FH_vs_independent_central_difference` | real numerical | PASS / PASS | Both interfaces move: new roots at h=1e-5,1e-8,1e-11; O(h^2) convergence; final error 9.23088812046e-20 <=1e-18. Individual eigenvalue derivatives also checked. |
| 13 | `legacy_symmetric_formula_is_half` | real numerical | PASS / PASS | Old mirrored formula is half the correct derivative; ratio approximately 2 and absolute discrepancy exceeds 20. |
| 14 | `one_interface_parameter_has_no_mirror_factor` | real numerical | PASS / PASS | Only left interface moves: derivative 26.940486080120... agrees with one-interface FH within 1e-18. |
| 15 | `u_second_derivative_true_nonzero_jump` | real numerical | PASS / PASS | One-sided second derivatives have jump -4.383575835224...; u and u-prime continuous in this example, u-second not continuous. |
| 16 | `trial_plateau_Gram_integrals_general` | symbolic/exact | PASS / PASS | Exact plateau mass 2*R*d+(h-2*d)/3 and energy 4/(h-2*d); integral identities only. |
| 17 | `trial_plateau_bound_finite_exact_instances` | symbolic/exact | PASS / PASS | 20 exact cases with n=1,2,3,5,8 and R=8,10^3,10^6,10^9; Rayleigh bound and support geometry tested. |
| 18 | `center_vanishing_subspace_finite_Gram_bounds` | symbolic/exact | PASS / PASS | 12 exact cases, 45 cells; positive leading minors for two-polynomial cell spaces (dimensions 4,6,8,12), not all of H_0^1. |
| 19 | `thin_density_spectral_bound_samples` | real numerical | PASS / PASS | Four real spectral samples: (1,1000),(2,1000),(3,1000),(2,1000000); reported inequalities independently rechecked. |
| 20 | `thin_density_scalar_limits_general_n` | symbolic/exact | PASS / PASS | Symbolic limits of scalar bounds for R=q^3 and d=q^-2; spectral theorem remains conditional on analytic bounds. |
| 21 | `constant_density_refutes_general_4pi2` | symbolic/exact | PASS / PASS | rho=1 gives gap (2*n+1)*pi^2; n=2 gives 5*pi^2, excluding a universal 4*pi^2 supremum limit for all n. No arbitrary branch limit certified. |
| 22 | `R7_P01_rho2_Schrodinger_counterexample` | symbolic/exact | PASS / PASS | Fixed-L2 potential model rho=2: weighted norm 1, ordinary squared norm 1/2; old derivative 1 versus exact derivative 2. |
| 23 | `R7_P01_generalized_FH_two_exact_models` | symbolic/exact | PASS / PASS | Generalized FH instantiated in two elementary models; no general operator differentiability proof. |
| 24 | `R7_P02_direct_matrix_and_switch_scaling` | symbolic/exact | PASS / PASS | Finite counterexamples: determinant/definiteness, missing eigenvalue scaling (8 versus 8/9), n=3 determinant sign, and matrix versus elementwise products. No historical NumPy scripts run. |
| 25 | `execution_contract_explicit_raise_and_input_identity` | bookkeeping | PASS / PASS | Bookkeeping only: zero assert AST nodes, intentional RuntimeError caught, four manifest snapshots hash-checked. |

## Substantive mirror-derivative comparison

For `-u''=lambda*rho*u` on [0,1] with Dirichlet endpoints, use rho=(1,4,1), interfaces a=1/4 and 1-a=3/4, and integral(rho*u^2)=1. The eigenvalues are approximately 2.829586034443622 and 14.602077453837592. Here f(a)=-8.980162026706762, so the sample is substantially nonstationary.

Moving a to a+h moves the mirror to 1-a-h. The corrected gap derivative is 2*(1-4)*f(a):

```text
FH               = 53.880972160240571523695242987489219318052973256092167942806432826
FD at h=1e-11    = 53.880972160240571523787551868693854639155681194182753581093634023
absolute error  = 9.23088812046353211027079380905856e-20
old half formula= 26.940486080120285761847621493744609659026486628046083971403216413
```

Errors for h=1e-5,1e-8,1e-11 are approximately 9.23088812327e-8, 9.23088812046e-14, 9.23088812046e-20. Roots are recomputed at both perturbed geometries. Moving only the left interface gives 26.940486080120... and correctly uses no extra mirror factor.

The separate verifier calculation did not import `checks.py`. It used characteristic equations on [0,1/2], with a Neumann center condition for the first mode and Dirichlet condition for the second. At a=1/4, sqrt(lambda) is 4*acos(sqrt(5/6)) and 4*acos(1/sqrt(3)), respectively. It normalized by weighted quadrature, differentiated characteristic equations implicitly, and resolved roots at h=1e-12. Implicit and FH derivatives agree within 1e-90; the independent finite-difference error is approximately **9.23088812046e-22**. The old half formula still misses by approximately **26.94048608012**. These are numerical tolerances, not certified enclosures.

## Exact samples independently recomputed

For sqrt(2)*sin(2*pi*x) and sqrt(2)*sin(3*pi*x), direct differentiation gives W(1/2)=-4*pi; the old value is -6*pi. A separate series expansion gives coefficient -130*pi^4 for n=2, matching 2*pi^4*(n^4-(n+1)^4).

For F=f/(9*pi^2), the four-interface determinant is exactly **7030400000*pi^4/4782969**, approximately 143179.8687395738. A separate resultant computation with P(t)=144*t^2-88*t+9 and t*(1-t)^3*P'(t)^2 takes the product over both algebraic roots; it does not merely copy radical substitutions. This verifies only the stated normalization and determinant sample.

## SHA-256 bindings and evidence

EXECUTION.json contains all packet/input hashes before, after and at finalization; all produced payload, receipt, log and verifier-script hashes; actual outer and child process results; every group with details and scope; supplemental computations; and explicit limits. README.md is also bound there. **SHA256SUMS** additionally binds EXECUTION.json. SHA256SUMS excludes its own bytes, avoiding a recursive self-hash. Runtime identities do not hash the full dependency closure.

Evidence directory: `independent-execution-66hgfj6g`. Raw runner outputs are `outputs.json`, `outputs.optimized.json` and the 13 receipt files listed in EXECUTION.json. The independent implementation is `independent-execution-66hgfj6g/verify_evidence.py`; its actual process receipt, stdout, stderr and detailed results are retained.

## Limits

- This verdict covers only this packet's explicit symbolic identities, finite exact cases, real high-precision samples, and execution/input integrity.

- No whole analytic theorem certification: no Volterra, full variational/min-max argument, full H_0^1 bound, arbitrary spectral branch, global extremality, or general operator differentiability certification.

- mpmath results use floating-point working precision, not rigorous interval arithmetic. Residuals and tolerances are numerical evidence, not certified error enclosures.

- General symbolic checks establish the displayed algebraic identities or scalar limits only, subject to their parameter domains. They do not validate untested analytic hypotheses or uniform Taylor remainders.

- Matrix counterexamples and the normalized determinant are finite algebra; they do not certify G2 or refute a specific spectral branch.

- Frozen source-scan files were hashed as data. No historical scripts, missing appendices, referenced derivations.md, repository originals, old certificates, Lean, or mathlib were run or consulted.

- No memory, authors' conversations or prior execution results, other agents' directories, or main project working tree were read. Source paths appearing inside documents were not followed.

- Manifest commit/provenance labels and matches_report_base claims were not verified against Git or original locations. SHA bindings establish identity to the supplied packet, not authenticity or current working-tree identity.

- Runtime versions, interpreter hash, and SymPy/mpmath entrypoint hashes were recorded; the entire installed runtime dependency closure was not hashed.

- Outer process capture and rechecked child receipts provide execution evidence; no separate kernel-level process or filesystem trace was collected.
