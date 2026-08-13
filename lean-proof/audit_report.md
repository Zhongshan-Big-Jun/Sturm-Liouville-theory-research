# Lean verification audit report (session 66)

Status: FORMALLY_VERIFIED (scope: SL/StabilityGrowth.lean + SL/MomentRecurrence.lean)
Run manifest: run-manifest.json (machine checks, hashes, environment)

Independence note: this is a single-agent run.  The audit pass below was
performed as a separate phase by the same model that wrote the proofs, by
re-deriving every obligation from the informal contracts without relying on
the draft proofs.  For strict independence, an external reviewer should
re-run the independent audit below.

## 1. Scope and contracts

- C1 (growth lemma, quantitative form): Theorem 2.1 of
  `docs/SL_stability_moment_jump.tex`.  For c0 > 0 and coefficient sequences
  A_m, B_m with B_m >= 0 and A_m - B_m >= c0 (m >= 2), the solution u of
  u_0 = 0, u_1 = 1, c0 u_m = A_m u_{m-1} - B_m u_{m-2} (m >= 2) is
  nondecreasing and u_m >= \prod_{k=2..m} (A_k - B_k)/c0
  = \prod_{k=2..m} (1 + eps_k) with eps_k = (A_k - B_k - c0)/c0 >= 0.
- C2 (moment recurrence): Section 3.2 of `docs/SL_h2_completeness_proof.tex`.
  For a linear functional M with moments mu_k = M(X^k), orthogonality
  M(K_c p_n) = 0 forces mu_0 = mu_1 = 0, the even/odd jump recurrences
  c mu_{2n} = A_n mu_{2n-2} - B_n mu_{2n-4} (and the odd analogue with
  A'_n, B'_n) for n >= 2, and the scaling mu_{2m} = mu_2 u_m,
  mu_{2m+1} = mu_3 u'_m with u the fundamental solution (u_0 = 0, u_1 = 1).

Formalization domain choices: StabilityGrowth is stated over any
`[Field K] [LinearOrder K] [IsStrictOrderedRing K]` (specializes to R and Q);
MomentRecurrence is stated over Q to match the exact rational coefficient
identities in `SL/KcPolynomial.lean` (the same algebra holds over R by change
of base).  Both choices are recorded in the file headers.

## 2. Obligation map and statement fidelity

C1 -> `SL/StabilityGrowth.lean`:

| Obligation | Declaration | Fidelity | Notes |
| --- | --- | --- | --- |
| O1 recurrence definition | `u` (line 33), `u_recurrence` (40), `u_recurrence'` (46) | FAITHFUL | c0 u_j = A_j u_{j-1} - B_j u_{j-2} for j >= 2; u_0 = 0, u_1 = 1. |
| O2 monotonicity | `monotone_pos` (106) | FAITHFUL | states 0 < u_j and u_j <= u_{j+1} for 1 <= j (u_1 = 1 > u_0 = 0, then step). |
| O3 product lower bound | `product_growth` (154) | FAITHFUL | prod over `Finset.Icc 2 j` of (A_k - B_k)/c0 <= u_j for 1 <= j; empty product for j = 1 gives 1 <= u_1 = 1. |
| O4 eps reformulation | `eps` (179), `one_add_eps` (183), `eps_nonneg` (188), `product_growth_eps` (192) | FAITHFUL | 1 + eps_k = (A_k - B_k)/c0 and eps_k >= 0 follow from c0 <= A_k - B_k and 0 < c0. |
| O5 hypothesis strength | `monotone_pos`/`key_growth`/`product_growth` take hB : 0 <= B m and hAB : c0 <= A m - B m for m >= 2 | MINOR_PARAPHRASE | The informal theorem lists "B_m >= 0, A_m >= B_m" but its proof uses A_m - B_m >= c0 (the last step uses A_m - B_m >= c0).  The formal statement uses the proof-required hypothesis c0 <= A_m - B_m, which strictly implies A_m >= B_m; the stated conclusion is otherwise reproduced exactly. |
C2 -> `SL/MomentRecurrence.lean`:

| Obligation | Declaration | Fidelity | Notes |
| --- | --- | --- | --- |
| O6 moments as linear functional | `moments` (43) | FAITHFUL | mu_k = M(X^k); the L2 inner product <g, .> of the source is a linear functional, so this is the correct abstraction. |
| O7 even recurrence from orthogonality | `even_recurrence` (51) | FAITHFUL | from M(K_c p_even n) = 0 and the coefficient identity K_c p_even n = c X^(2n) - A_n X^(2n-2) + B_n X^(2n-4) (`KcPolynomial.Kc_pEven`) plus linearity of M. |
| O8 odd recurrence from orthogonality | `odd_recurrence` (64) | FAITHFUL | odd analogue with A'_n, B'_n. |
| O9 mu_0 = 0, mu_1 = 0 | `constant_orth_moment_zero` (77), `linear_orth_moment_zero` (88) | FAITHFUL | K_c p_0 = c, K_c p_1 = c x; with c != 0 orthogonality gives mu_0 = mu_1 = 0 (c != 0 matches c > 0 in the source). |
| O10 scaling (uniqueness + explicit form) | `scaling` (99) | FAITHFUL | any solution v of the jump recurrence with v_0 = 0 is v_m = v_1 u_m; strong induction on m using the recurrence at m and the IH at m-1, m-2. |
| O11 even/odd scaling | `even_scaling` (133), `odd_scaling` (150) | FAITHFUL | even: mu_{2m} = mu_2 u_m (free parameter mu_2); odd: mu_{2m+1} = mu_3 u'_m (free parameter mu_3), matching "free parameters only mu_2 (even) and mu_3 (odd)". |
| O12 composite moment scaling | `even_moment_scaling` (167), `odd_moment_scaling` (176) | FAITHFUL | orthogonality + mu_0/mu_1 = 0 imply the scaling statements with the K_c coefficients (A c, B) and (A' c, B'). |

## 3. Machine verification (observed)

- Environment: Lean 4.31.0 (x86_64-w64-windows-gnu), Lake 5.0.0, toolchain
  `leanprover/lean4:v4.31.0`, mathlib v4.31.0 (`lake-manifest.json`).
- Scan: 7 `.lean` files, sorry/admit/axiom hits: 0 (whitelist empty).
- Build: `lake build`, exit code 0, "Build completed successfully (8564 jobs)."
- Recorded in `run-manifest.json` (input hashes included for both new files).

## 4. Independent audit (re-derivation)

C1 proofs:
- O2: base u_1 = 1 > 0 and u_2 = A_2/c0 >= 1 (c0 <= A_2 - B_2 and B_2 >= 0 give
  c0 <= A_2; u_2 = (A_2 u_1 - B_2 u_0)/c0 = A_2/c0).  Step: if 0 < u_{j-1} <= u_j,
  then c0 u_{j+1} = A_{j+1} u_j - B_{j+1} u_{j-1} >= (A_{j+1} - B_{j+1}) u_j
  >= c0 u_j since B_{j+1} >= 0, u_{j-1} <= u_j, and A_{j+1} - B_{j+1} >= c0.
  Sound.
- O3: from O2, u_m >= ((A_m - B_m)/c0) u_{m-1} (recurrence, B_m >= 0,
  u_{m-2} <= u_{m-1}); iterate from m down to 2 and use u_1 = 1.  The Lean
  proof uses `Nat.le_induction` with `key_growth` as the step; the product is
  split with `prod_Icc_succ_top` (prod over 2..n+1 = (prod over 2..n) * term).
  Sound.
- O4: algebraic; `field_simp`/`ring` close the identities.  Sound.
- No circularity: the formal statements do not assume any part of the
  conclusion.
C2 proofs:
- O7: linearity of M expands M of the three-term polynomial into the moment
  combination; the coefficient identity is exactly `KcPolynomial.Kc_pEven`
  (previously machine-verified in this repo, covered by the same manifest).
  Sound.
- O9: `Kc c 1 = C c` and `Kc c X = C c * X` by direct differentiation (both
  second derivatives vanish); `M (C c * X^k) = c * M (X^k)` by linearity over Q.
  Sound.
- O10: strong induction on m.  Bases m = 0 (v_0 = 0 = v_1 u_0, u_0 = 0) and
  m = 1 (v_1 = v_1 u_1, u_1 = 1).  Step m >= 2:
  c0 v_m = A_m v_{m-1} - B_m v_{m-2} = v_1 (A_m u_{m-1} - B_m u_{m-2})
  = v_1 (c0 u_m) by the IH at m-1, m-2 and the recurrence for u; cancel c0
  (c0 != 0).  Sound.
- O11: substitution of the even/odd subsequences into O10; index identities
  (2n-2 = 2(n-1), 2n-4 = 2(n-2), 2n-1 = 2(n-1)+1, 2n-3 = 2(n-2)+1) are
  omega-closeable.  Sound.
- O12: composition of O7/O8 with O11.  Sound.
- External dependencies: `KcPolynomial.Kc_pEven`/`Kc_pOdd`
  (`SL/KcPolynomial.lean`, in-repo, machine-verified); no other external
  results are used.  No citation is fabricated.

## 5. Findings

- No critical errors found within the declared scope.
- F-001 (documented, not a formal defect): the informal theorem C1 states the
  weaker hypothesis A_m >= B_m while its proof uses A_m - B_m >= c0; the
  formalization uses the proof-required hypothesis (O5, MINOR_PARAPHRASE).
  The informal document should be corrected to state A_m - B_m >= c0.
- Limitation (not a finding against the artifact): the audit is a self-audit
  (see independence note); the moment recurrence is formalized over Q (exact
  rational coefficients) rather than over R; the R case is an identical change
  of base and is not separately formalized.

## 6. Remaining gaps (outside this scope)

- The full H^2 completeness theorem (isometric isomorphism, Weierstrass
  density, contradiction step) is not yet formalized; this session formalized
  its algebraic core (growth lemma + moment recurrence + scaling).
- The stability theorem (superpolynomial growth threshold
  sum min(eps,1) = omega(log m)) and the sharpness theorem are not formalized.
## 7. Addendum (2026-08-11): F-001 resolved in source

The informal contract C1 in `docs/SL_stability_moment_jump.tex` was corrected on
2026-08-11 (session 67): Theorem 2.1 and Theorem 2.2 (stability) now state the
proof-required hypothesis `B_m >= 0 and A_m - B_m >= c0` (equivalently eps_k >= 0)
instead of the weaker `A_m >= B_m`.  Obligation O5 is therefore FAITHFUL against the
current source text.  The Lean formalization (`SL/StabilityGrowth.lean`) already used
the corrected hypothesis and is unchanged; `lake build` re-run passed (see
run-manifest.json).  A remark with counterexamples showing the weak hypothesis fails
(A_m = B_m = 1 oscillates; A_m - B_m = 1/2 < c0 breaks the product bound) was added
after Theorem 2.1.  Historical findings above are preserved as recorded at audit time.

## 8. Addendum (2026-08-11): SL/MomentBound.lean (session 68)

Scope: `SL/MomentBound.lean` (H^2 completeness line, step 3 of the roadmap).

### 8.1 Contract

C3 (L2 moment bound), Section 3.3 (???) of
`docs/SL_h2_completeness_proof.tex`: for g in L2[-1,1] the moments
mu_k = <g, x^k>_{L2} = integral_{-1}^1 g(x) x^k dx satisfy the
Cauchy-Schwarz bound

    |mu_k| <= ||g||_2 * ||x^k||_2,   ||x^k||_2^2 = 2 / (2k+1).

(The source applies this to the even subsequence: ||x^(2j)||_2^2 = 2/(4j+1).)

### 8.2 Obligation map and statement fidelity

C3 -> `SL/MomentBound.lean`:

| Obligation | Declaration | Fidelity | Notes |
| --- | --- | --- | --- |
| O13 moments | `moments` (36) | FAITHFUL | mu_k = integral_{-1}^1 g(x) x^k dx; the inner product <g, x^k>_{L2} of the source is the Lebesgue integral over [-1,1]. |
| O14 norm identity | `integral_x_pow_even` (40), `norm_sq_x_pow` (54) | FAITHFUL | integral_{-1}^1 x^(2k) = 2/(2k+1), proved from `integral_pow` plus (-1)^(2k) = 1; for k = 2j this is the source's ||x^(2j)||_2^2 = 2/(4j+1). |
| O15 Cauchy-Schwarz | `cs_moment` (65) | FAITHFUL | B^2 <= A*C for B = integral g*x^k, A = integral g^2, C = integral x^(2k), proved by the quadratic trick 0 <= integral (g - c x^k)^2 with c = B/C (C > 0 is proved first, so no degenerate case). |
| O16 moment bound | `moment_bound` (143) | MINOR_PARAPHRASE | |mu_k| <= sqrt(A) * sqrt(2/(2k+1)) = ||g||_2 * ||x^k||_2; formal hypothesis is `ContinuousOn g (Icc (-1) 1)` (enough for IntervalIntegrable) instead of g in L2; the L2 case follows by density and is left as a documented gap. |

### 8.3 Machine verification (observed)

- Environment: Lean 4.31.0 (x86_64-w64-windows-gnu), Lake 5.0.0,
  mathlib v4.31.0 (`lake-manifest.json`).
- Scan: 8 `.lean` files (SL/MomentBound.lean included), sorry/admit/axiom
  hits: 0 (whitelist empty).
- Build: `lake build`, exit code 0, "Build completed successfully (8565 jobs)."
- Recorded in `run-manifest.json` (input hashes include SL/MomentBound.lean).

### 8.4 Independent audit (re-derivation)

- O14: integral_pow gives (1^(2k+1) - (-1)^(2k+1))/(2k+1); (-1)^(2k) = 1 via
  pow_mul + neg_one_sq, (-1)^(2k+1) = -1 via pow_succ; result 2/(2k+1).
  Sound.
- O15: expand the square, use additivity/linearity of the interval integral
  (integral_add/integral_sub/integral_const_mul) with IntervalIntegrable
  hypotheses obtained from ContinuousOn.intervalIntegrable_of_Icc; the
  integrands are continuous on the closed interval, so no measurability gaps.
  With C > 0, 0 <= A - 2cB + c^2 C and c = B/C give 0 <= A - B^2/C and then
  B^2 <= A*C.  Sound.
- O16: B^2 <= A*C, A, C >= 0, sqrt is monotone on nonnegatives; apply
  sq_le_sq to get |B| <= sqrt A * sqrt C and substitute C = 2/(2k+1).
  Sound.
- External dependencies: `integral_pow`, `sq_le_sq`, `Real.sq_sqrt`,
  interval-integral linearity lemmas (all mathlib); no citation is
  fabricated.

## 9. Addendum (2026-08-11): SL/Completeness.lean (session 69)

Scope: `SL/Completeness.lean` -- the final steps of the H^2 completeness line
(source `docs/SL_h2_completeness_proof.tex`, Section 3.3 "moments vanish" and
Section 3.4 "Weierstrass conclusion"): a continuous g orthogonal to {K_c p_n}
in L2(-1,1) has all moments zero, hence integral g^2 = 0, hence g = 0 a.e.

### 9.1 Obligation map and statement fidelity

| Obligation | Declaration | Fidelity | Notes |
| --- | --- | --- | --- |
| O17 real coefficients | `qR/pEvenR/pOddR/AR/A'R/BR/B'R/KcR`, `KcR_pEven/KcR_pOdd` | FAITHFUL | Real mirror of `KcPolynomial` (Q): K_c p_{2n} = c x^{2n} - A_n x^{2n-2} + B_n x^{2n-4} and the odd analogue; A_n - B_n = 4n + c q_n, q_n = n/(n-1). |
| O18 moment functional | `momentFunctional` | FAITHFUL | M(p) = integral_{-1}^1 g(x) p(x) dx as a Real-linear map; linearity proved with `IntervalIntegrable` hypotheses obtained from `hg.mul (Polynomial.continuousOn p)`. |
| O19 moment recurrences | `even_recurrence/odd_recurrence` | FAITHFUL | Orthogonality M(K_c p_{2n}) = 0 plus O17 gives c mu_{2n} = A_n mu_{2n-2} - B_n mu_{2n-4} (odd analogue with A', B'). |
| O20 initial moments | `constant_orth_moment_zero/linear_orth_moment_zero` | FAITHFUL | K_c 1 = c and K_c X = c X force mu_0 = 0, mu_1 = 0 for c != 0. |
| O21 scaling | `even_moment_scaling/odd_moment_scaling` | FAITHFUL | mu_{2m} = mu_2 u_m and mu_{2m+1} = mu_3 u'_m with u the StabilityGrowth fundamental solution (Real instantiation). |
| O22 annihilation | `sqrt_bound_small/sqrt_bound_small'`, `bound_tendsto_annihilate`, `even/odd_annihilation` | FAITHFUL | u_m >= 1 (O2 via `monotone_pos` with B_m >= 0, A_m - B_m >= c) and the L2 bound |mu_{2m}| <= ||g||_2 sqrt(2/(4m+1)) (O16) contradict each other via the epsilon argument: sqrt(2/(4m+1)) -> 0 forces mu_2 = 0; odd case with 4m+3. |
| O23 all moments | `all_moments_zero` | FAITHFUL | Even/odd split by `Nat.even_or_odd`, scaling + mu_2 = mu_3 = 0. |
| O24 Weierstrass conclusion | `exists_polynomial_sup_approx`, `integral_sq_eq_zero_of_all_moments_zero`, `completeness_contradiction`, `completeness_ae_zero` | FAITHFUL | Polynomial density (mathlib `polynomialFunctions.topologicalClosure`) gives sup-approximations of g; the split integral trick gives integral g^2 <= ||g|| eps1 * 2 for every eps (via `norm_integral_le_of_norm_le_const` on the uIoc), so `le_of_forall_pos_le_add` gives integral g^2 <= 0; `integral_eq_zero_iff_of_nonneg` then gives g^2 = 0 a.e. on Ioc (-1,1), i.e. g = 0 a.e. |

### 9.2 Machine verification (observed)

- Environment: Lean 4.31.0 (x86_64-w64-windows-gnu), Lake 5.0.0, mathlib v4.31.0.
- Scan: 9 `.lean` files (SL/Completeness.lean included), sorry/admit/axiom hits: 0.
- Build: `lake build`, exit code 0, "Build completed successfully (8566 jobs)."
- Recorded in `run-manifest.json` (input hashes include SL/Completeness.lean).

### 9.3 Independent audit (re-derivation)

- O17: over Real the identities are the same algebra as `KcPolynomial` (Q);
  `KcR_sub` and the monomial derivative identities are proved directly
  (`derivative_sub`, `derivative_C_mul`, `derivative_X_pow`).  Sound.
- O18: additivity needs both integrands IntervalIntegrable; they are continuous
  products on the closed interval, so `hg.mul (Polynomial.continuousOn p)`
  applies.  The `map_smul` step uses `Polynomial.smul_eq_C_mul`.  Sound.
- O22: the epsilon argument: if |a| <= B * t_m for all m >= 1 and t_m -> 0 then
  a = 0; applied with B = ||g||_2, t_m = sqrt(2/(4m+1)) (and 4m+3 for odd);
  `sqrt_bound_small` is proved from `exists_nat_gt` + `Real.sqrt_lt`; no
  fabricated limit claims (the convergence is explicit in eps).  Sound.
- O24: `continuousMap_mem_polynomialFunctions_closure (-1) 1` is mathlib's
  Weierstrass theorem for Icc (-1) 1; the approximation is transferred to the
  integral via `norm_integral_le_of_norm_le_const` (the integrand is bounded by
  ||g|| * eps1 on the uIoc); `integral_eq_zero_iff_of_nonneg` is
  `MeasureTheory`'s lemma.  The formal statement assumes g ContinuousOn [-1,1]
  (the L2 density extension is the documented gap O16).  Sound.

### 9.4 Findings

- No new source-document errors were found in this session; the formal line
  confirms Sections 3.3/3.4 of `docs/SL_h2_completeness_proof.tex`.
- Remaining (documented, unchanged): the isometric-isomorphism step
  K_c : H^2 -> L^2 and the L2 density extension of `moment_bound` are not
  formalized; the formal completeness conclusion starts from L2 orthogonality
  of a continuous g against {K_c p_n}.

## 10. KreinHighGrowth.lean (session 88 continuation)

Status: MACHINE_ACCEPTED_PENDING_AUDIT (machine checks pass; independent
obligation-level audit is not yet closed and remains the documented next step)

Scope: `SL/KreinHighGrowth.lean`, formalizing the general part of Theorem
"high" from `docs/SL_krein_c0_limit.tex`: the two-sided Theta bounds
`a_n(c) = Theta(c^{-(n-2)/2})` (even) / `Theta(c^{-(n-3)/2})` (odd) for
`0 < c <= 1`, and the divergence `||K_n^{(c)}||^2 -> +infinity` as `c -> 0+`
for every `n >= 4`.

### 10.1 Obligation map (machine level)

| Obligation | Lean declaration | Statement |
| --- | --- | --- |
| K1 | `aSeq_rec` | coefficient recurrence (source (19)) in index form for n >= 2 |
| K2 | `aSeq_nonneg_step_ge`, `aSeq_nonneg`, `aSeq_step_ge` | nonnegativity and parity-wise monotonicity for c > 0 |
| K3 | `aSeq_lower_step`, `aSeq_upper_step` | one-step lower/upper recurrence bounds |
| K4 | `lowerEvenProd`, `lowerOddProd`, `upperEvenProd`, `upperOddProd` | explicit product constants for the Theta bounds |
| K5 | `aSeq_lower_even`, `aSeq_lower_odd` | lower Theta bounds, all c > 0 |
| K6 | `aSeq_upper_even`, `aSeq_upper_odd` | upper Theta bounds, 0 < c <= 1 |
| K7 | `norm_even_ge`, `norm_odd_ge` | norm lower bounds from the norm formula + lower bounds |
| K8 | `tendsto_norm_even_atTop`, `tendsto_norm_odd_atTop`, `tendsto_norm_atTop` | ||K_n||^2 -> +infinity for every n >= 4 |

The norm formula `||K_n||^2 = 2c a_n a_{n+2}/(2n+1)` is a literature fact
admitted as the hypothesis `KreinSobolevFacts` (imported from
`SL/HsOrthogonalSystems.lean`), exactly as in `SL/KreinDegenerateLimit.lean`;
the quotient-space theorems (Theorem "quotient", Theorem "complete" (b)-(d),
Theorem "unit") are not formalized anywhere in this project and remain
documented open.

### 10.2 Machine evidence

- `lake build`: exit 0, "Build completed successfully (8578 jobs)".
- `sorry`/`admit`/`axiom` scan: 0 hits across `SL/`.
- `run-manifest.json` regenerated with 21 scanned files (20 SL `.lean` files +
  `lakefile.lean`) and the new hash for `SL/KreinHighGrowth.lean`.

### 10.3 Independent audit status

Not yet closed. A strict independent pass must re-derive K1-K8 from the
source document without relying on this repair session, and verify the
statement fidelity of the Theta constants and the `c -> 0+` filter statements
against `docs/SL_krein_c0_limit.tex`. Until that pass is recorded, this file
is `MACHINE_ACCEPTED_PENDING_AUDIT`, not `FORMALLY_VERIFIED`.

## 11. SL/TransferMatrix.lean (session 91)

Status: MACHINE_ACCEPTED_PENDING_AUDIT (machine checks pass; independent
obligation-level audit is not yet closed)

Scope: `SL/TransferMatrix.lean`, formalizing the elementary matrix algebra in
`docs/SL_ratio_proof.tex` Sections 1-3: the balanced three-block transfer
matrices for `[1,R,1]` and `[R,1,R]`, their `(0,1)` product entries, the
equivalent Dirichlet secular equations, the fact that the balanced phases
`theta`, `pi - theta`, and `phi` satisfy the matrix condition, and the generic
monotonicity step `lambda_{n+1} <= lambda_{2n}`.

### 11.1 Obligation map (machine level)

| Obligation | Lean declaration | Statement |
| --- | --- | --- |
| T1 | `supM1`, `supM2`, `supM3` | transfer matrices and product for `[1,R,1]` |
| T2 | `supM3_top_right`, `supM3_top_right_eq_zero_iff` | sup `(0,1)` entry and secular equivalence |
| T3 | `sup_bracket_pi_sub`, `supM3_top_right_theta`, `supM3_top_right_pi_sub_theta` | the two balanced phases satisfy the sup matrix condition |
| T4 | `infM1`, `infM2`, `infM3` | transfer matrices and product for `[R,1,R]` |
| T5 | `infM3_top_right`, `infM3_top_right_eq_zero_iff` | inf `(0,1)` entry and Keller secular equivalence |
| T6 | `inf_bracket_phi`, `infM3_top_right_phi` | the first Keller phase satisfies the inf matrix condition |
| T7 | `le_of_strictMono_double` | `lambda_{n+1} <= lambda_{2n}` for a strictly increasing sequence |
| T8 | `ratio_le_of_strictMono_double` | positive-denominator ratio form of T7 |

### 11.2 Machine evidence

- `lake build`: exit 0, "Build completed successfully (8579 jobs)".
- `sorry`/`admit`/`axiom` scan: 0 hits across `SL/`.
- `run-manifest.json` regenerated with 22 scanned files (21 `SL/` files +
  `lakefile.lean`) and the hash of `SL/TransferMatrix.lean`.

### 11.3 Independent audit status

Not yet closed. The remaining non-formalized bridge is explicitly documented:
this file proves the matrix/secular algebra, but does not formalize the
spectral theorem that identifies the matrix Dirichlet condition with the
eigenvalues of the Sturm-Liouville problem, nor the MW period-extension and
zero-truncation arguments. A strict independent pass must re-derive T1-T8
against the source before this file can be labelled `FORMALLY_VERIFIED`.

## 12. SL/ReflectionSymmetry.lean (session 92)

Status: MACHINE_ACCEPTED_PENDING_AUDIT (machine checks pass; independent
obligation-level audit is not yet closed)

Scope: `SL/ReflectionSymmetry.lean`, formalizing the strictly proved
J-conjugacy argument from `docs/SL_fixed_n_supremum.tex` Theorem "reflection
symmetry".  For the cell/end transfer matrices of the alternating
configuration and `M_n(y) = T_end(y) * T_cell(y)^n`, the file proves
`M_n(pi - y) = -J * M_n(y) * J` and hence
`F_n(pi - y) = F_n(y)` for the secular entry.

### 12.1 Obligation map (machine level)

| Obligation | Lean declaration | Statement |
| --- | --- | --- |
| R1 | `J`, `J_mul_J` | reflection matrix `diag(1,-1)` and `J*J = 1` |
| R2 | `J_Tcell` | `J * T_cell(y) * J = T_cell(pi-y)` |
| R3 | `J_Tend` | `J * T_end(y) * J = -T_end(pi-y)` |
| R4 | `J_conj_pow` | conjugation commutes with matrix powers |
| R5 | `Tcell_pow_pi_sub` | `T_cell(pi-y)^n = J * T_cell(y)^n * J` |
| R6 | `M_reflection` | `M_n(pi-y) = -J * M_n(y) * J` |
| R7 | `J_conj_entry` | `(J * A * J)_{0,1} = -A_{0,1}` |
| R8 | `F_reflection` | `F_n(pi-y) = F_n(y)` |

### 12.2 Machine evidence

- `lake build`: exit 0, "Build completed successfully (8580 jobs)".
- `sorry`/`admit`/`axiom` scan: 0 hits across `SL/`.
- `run-manifest.json` regenerated with 23 scanned files (22 `SL/` files +
  `lakefile.lean`) and the hash of `SL/ReflectionSymmetry.lean`.

### 12.3 Independent audit status

Not yet closed.  The formal statement treats the frequency `ω` as a fixed
parameter, matching the source's conjugation proof but not the source's
phase normalization `y = ω * sqrt(R) * t`; the spectral identification of the
matrix condition with Dirichlet eigenvalues is also not formalized.  A strict
independent pass must verify R1-R8 against the source before
`FORMALLY_VERIFIED` may be used.

## 13. SL/DensenessCriteria.lean (session 93)

Status: MACHINE_ACCEPTED_PENDING_AUDIT (machine checks pass; independent
obligation-level audit is not yet closed)

Scope: `SL/DensenessCriteria.lean`, formalizing the algebraic core of
`docs/SL_denseness_criteria.tex` Theorem 2 ("矩刻画").  For a real-linear
functional `M` on polynomials, orthogonality to the sparse basis
`p_0 = 1`, `p_1 = X`,
`p_{2m} = X^{2m} - (m/(m-1)) X^{2m-2}`,
`p_{2m+1} = X^{2m+1} - (m/(m-1)) X^{2m-1}` is equivalent to the moment
conditions `M_0 = M_1 = 0`, `M_{2m} = m * M_2`,
`M_{2m+1} = m * M_3`.

### 13.1 Obligation map (machine level)

| Obligation | Lean declaration | Statement |
| --- | --- | --- |
| D1 | `moments` | `moments M k = M (X ^ k)` |
| D2 | `apply_C_mul_X_pow` | `M (C a * X^m) = a * moments M m` |
| D3 | `sparse_even_apply`, `sparse_odd_apply` | moment expansions of `pEvenR n` and `pOddR n` for `2 <= n` |
| D4 | `even_moments_of_orthogonal`, `odd_moments_of_orthogonal` | orthogonality to the sparse even/odd polynomials forces the even/odd moment recurrences |
| D5 | `even_orthogonal_of_moments`, `odd_orthogonal_of_moments` | the even/odd moment recurrences force orthogonality to the sparse polynomials |
| D6 | `sparse_moment_characterization` | Theorem 2 iff: `M 1 = 0 ∧ M X = 0 ∧ (∀n, 2 ≤ n → M pEvenR n = 0) ∧ (∀n, 2 ≤ n → M pOddR n = 0) ↔ (M_0 = 0 ∧ M_1 = 0 ∧ (∀m, 1 ≤ m → M_{2m} = m M_2) ∧ (∀m, 1 ≤ m → M_{2m+1} = m M_3))` |

The `Completeness.pEvenR`/`Completeness.pOddR` definitions are imported from
`SL/Completeness.lean` and were already machine-verified in this repository.

### 13.2 Machine evidence

- `lake build`: exit 0, "Build completed successfully (8581 jobs)".
- `sorry`/`admit`/`axiom` scan: 0 hits across `SL/`.
- `run-manifest.json` regenerated with 24 scanned files (23 `SL/` files +
  `lakefile.lean`) and the hash of `SL/DensenessCriteria.lean`.

### 13.3 Independent audit status

Not yet closed.  This file proves only the finite-dimensional/algebraic
moment characterization; it does not formalize the Hilbert-space embedding of
`M`, the first-moment criterion (`beta < 1`), the critical-exponent theorem,
or the final density/Weierstrass conclusion in
`docs/SL_denseness_criteria.tex`.  A strict independent pass must re-derive
D1-D6 against the source before `FORMALLY_VERIFIED` may be used.
## 14. SL/SymlineTensionRatio.lean (session 95)

Status: MACHINE_ACCEPTED_PENDING_AUDIT (machine checks pass; independent
obligation-level audit is not yet closed)

Scope: `SL/SymlineTensionRatio.lean`, formalizing the STRICT (proved)
algebraic core of `docs/SL_gap_n1_symline_allR_proof.tex` (symmetry line of
the n=1 gap theorem): the comparison lemma P1
(`c/(q+c) <= t/(y+t)` from `u <= tan u` with `c = arctan(q*t)/y`), the
common-denominator form of the left-hand functional `FeEquiv` on the
symmetry line, and the equivalence `FeEquiv < 0 <-> rho < 1` for
`Delta > 0`.

### 14.1 Obligation map (machine level)

| Obligation | Lean declaration | Statement |
| --- | --- | --- |
| S1 | `Phi`, `Mf`, `FeEquiv`, `Delta`, `T`, `rho` | named quantities of the source |
| S2 | `Phi_nonneg`, `Phi_eq` | `0 <= Phi q x`; `Phi q x = 1 - (1 - q^2) * sin x^2` |
| S3 | `P1`, `P1_tan` | `0<q, 0<t, 0<y, c = arctan(q*t)/y => c/(q+c) <= t/(y+t)`; `t = tan gamma` version |
| S4 | `FeEquiv_eq` | common-denominator form: `FeEquiv A gamma c q = (c*(1-q^2)*sinA^2*sinG^2*T - (q+c)*Delta) / ((q+c*Phi q A)*(q+c*Phi q (pi-gamma)))` |
| S5 | `FeEquiv_iff_rho_lt_one` | `0<q, 0<c, 0<Delta A gamma => FeEquiv A gamma c q < 0 <-> rho A gamma c q < 1` |

### 14.2 Machine evidence

- `lake build`: exit 0, "Build completed successfully (8582 jobs)".
- `sorry`/`admit`/`axiom` scan: 0 hits across `SL/`.
- `run-manifest.json` regenerated with 25 scanned files (24 `SL/` files +
  `lakefile.lean`) and the hash of `SL/SymlineTensionRatio.lean`.

### 14.3 Independent audit status

Not yet closed.  This file proves only the algebraic core: the source's
transcendental facts (existence and location of `gamma_0*`, the inequality
`(y * sin gamma)^2 >= pi^2/4`, the three-term nonnegative decomposition of
Lemma P2, and the full tension-ratio chain of Theorem 1) are NOT formalized
and remain pending.  Numerical evidence in the source is not used.  A strict
independent pass must re-derive S1-S5 against the source before
`FORMALLY_VERIFIED` may be used.
## 15. SL/SymlineTensionRatio.lean P2 + tension-ratio chain (session 96)

Status: MACHINE_ACCEPTED_PENDING_AUDIT (machine checks pass; independent
obligation-level audit is not yet closed)

Scope: continuation of `SL/SymlineTensionRatio.lean`, formalizing Lemma P2
and the tension-ratio chain of `docs/SL_gap_n1_symline_allR_proof.tex`
(section 张力比链): with the strict Lemma ys2 bound
`p < y^2 * sin gamma^2` as a documented hypothesis,

* `P2`: `s1^2 * s2^2 * T / Delta * (1-q^2) <= Q0(gamma)` for every real `q`
  (the source states `0 < q < 1`; the formal statement is stronger and the
  proof uses only `1 - q^2 <= 1`);
* `tension_ratio_chain`: with `c = arctan(q*tan gamma)/(pi-gamma)`,
  `rho A gamma c q <= rho0 gamma = t/(y+t) * Q0(gamma)`, the product of P1
  and P2.

P2's proof follows the source: cross-multiply to `E >= 0`, bound
`W <= W0` (from `1 - q^2 <= 1`), and use the three-term nonnegative
decomposition `E0/y^2 = cos^2(gamma)*(p-A^2) + cos^2(A)*(y^2*s2^2-p)
+ cos^2(A)*A^2*cos^2(gamma)`.

### 15.1 Obligation map (machine level)

| Obligation | Lean declaration | Statement |
| --- | --- | --- |
| S6 | `p`, `Q0`, `rho0` | `p = pi^2/4`; `Q0(gamma) = s2^2*(y^2-p)/(y^2*s2^2-p)`; `rho0(gamma) = t/(y+t)*Q0(gamma)` |
| S7 | `one_sub_sq_nonneg`, `p_eq_sq_half`, `p_sub_sq_nonneg`, `T_pos`, `Delta_pos` | positivity facts used by P2 (`1-q^2 >= 0` for `0<q<1`; `p-A^2 >= 0` for `0<A<pi/2`; `T A gamma > 0`; `Delta A gamma > 0` under ys2) |
| S8 | `t_div_add_le_one`, `Q0_nonneg` | `t/(y+t) <= 1` for `t,y>0`; `Q0(gamma) >= 0` under ys2 |
| S9 | `P2` | `s1^2*s2^2*T/Delta*(1-q^2) <= Q0(gamma)` for all real `q`, given `gamma < pi/2`, `0<A<pi/2`, ys2 |
| S10 | `tension_ratio_chain` | `rho A gamma (arctan(q*tan gamma)/(pi-gamma)) q <= rho0 gamma` given `0<q<1`, `0<gamma<pi/2`, `0<A<pi/2`, ys2 |

### 15.2 Machine evidence

- `lake build`: exit 0, "Build completed successfully (8582 jobs)";
  `SL.SymlineTensionRatio` rebuilt in this run.
- `sorry`/`admit`/`axiom` scan: 0 hits across `SL/`.
- `run-manifest.json` regenerated with 25 scanned files (24 `SL/` files +
  `lakefile.lean`).

### 15.3 Independent audit status

Not yet closed.  The transcendental facts of the source (existence and
location of `gamma_0*`, and Lemma ys2, i.e. `(y * sin gamma)^2 >= pi^2/4`
on `[gamma_0*, pi/2]`) are NOT formalized; P2 and the chain take the
strict form of ys2 as a hypothesis, documented in the file header.  The
source's `0 < q < 1` in P2 is relaxed to all real `q` (stronger
statement).  A strict independent pass must re-derive S6-S10 against the
source before `FORMALLY_VERIFIED` may be used.

## 16. SL/SymlineTensionRatio.lean GammaStar + Lemma ys2 (session 100)

Status: MACHINE_ACCEPTED_PENDING_AUDIT (machine checks pass; independent
obligation-level audit is not yet closed)

Scope: continuation of `SL/SymlineTensionRatio.lean`, formalizing the two
transcendental facts that sessions 95/96 left as hypotheses: the source
threshold `gamma_0*` and Lemma ys2 of
`docs/SL_gap_n1_symline_allR_proof.tex` (lemmas `lem:gstar`, `lem:ys2`).

Source contract: `gamma_0*` is the root of `tan gamma = 2 * (pi - gamma) / 3`
(equivalently `tan gamma = 2 * y / 3`, `y = pi - gamma`) located in
`(0.961, 0.97)`; Lemma ys2 states `(y * sin gamma)^2 >= pi^2/4` for
`gamma in [gamma_0*, pi/2]`.  Only `gamma_0* > pi/4` is used by the chain.

Formal route (certificate-free deviation, documented in the file header):
`exists_gamma_star` proves by IVT that the root exists in
`(pi/4, 9*pi/20)` with endpoint checks `phi(pi/4) = 1 - pi/2 < 0`
(from `pi > 3`) and `phi(9*pi/20) > 0` (from `tan x > x` plus a linear
comparison); `GammaStar` is `Classical.choose exists_gamma_star`.
`ys2_of_ge_gamma_star` proves the strict form
`p < (pi - gamma)^2 * sin gamma^2` on `[GammaStar, pi/2)` using strict
concavity of `f(gamma) = (pi - gamma) * sin gamma` on `[pi/4, pi/2]`
(`f'' < 0`) and the chord bound `f(pi/4) = 3*pi*sqrt2/8 > pi/2`,
`f(pi/2) = pi/2`.  The source's rational location certificates
(`gamma_0* in (0.961, 0.97)` via alternating series for tan) are not
reproduced; only `gamma_0* > pi/4` is needed, and the formal root's
defining equation matches the source exactly.  Numerical evidence is
never used.

### 16.1 Obligation map (machine level)

| Obligation | Lean declaration | Statement |
| --- | --- | --- |
| S11 | `exists_gamma_star`, `GammaStar` | `exists gamma, pi/4 < gamma ∧ gamma < 9*pi/20 ∧ tan gamma = 2*(pi-gamma)/3`; `GammaStar` = chosen root |
| S12 | `gamma_star_gt_pi_div_four`, `gamma_star_lt_nine_pi_div_twenty`, `gamma_star_tan`, `gamma_star_pos`, `gamma_star_lt_pi_div_two` | location and defining equation of `GammaStar` |
| S13 | `strictConcaveOn_f`, `f_pi_div_four_gt`, `ys2_of_ge_gamma_star` | strict concavity of `f` on `[pi/4, pi/2]`; `f(pi/4) > pi/2`; Lemma ys2 in strict form `p < (pi-gamma)^2 * sin gamma^2` for `gamma in [GammaStar, pi/2)` |
| S14 | `Delta_pos`, `Q0_nonneg`, `P2`, `tension_ratio_chain` | rewired: hypothesis `hγs : GammaStar <= gamma` replaces the raw ys2 hypothesis; `hys2` is derived inside from `ys2_of_ge_gamma_star` |

### 16.2 Machine evidence

- `lake build`: exit 0, "Build completed successfully (8582 jobs)";
  `SL.SymlineTensionRatio` rebuilt in this run.
- `sorry`/`admit`/`axiom` scan: 0 hits across `SL/`.
- `run-manifest.json` regenerated: 25 scanned files (24 `SL/` files +
  `lakefile.lean`); the temporary `ScratchCheck.lean` was removed before
  this run and is not scanned.

### 16.3 Independent audit status

Not yet closed.  S11-S14 must be re-derived against
`docs/SL_gap_n1_symline_allR_proof.tex` (lem:gstar, lem:ys2) in an
independent pass: check that `gamma_0*`'s defining equation matches, that
the formal interval `(pi/4, 9*pi/20)` is compatible with the source's
`(0.961, 0.97)` (pi/4 ~ 0.7854 and 9*pi/20 = 1.4137..., so the source
interval is a subset), and that the strict form of ys2 implies the
source's `(y*sin gamma)^2 >= pi^2/4`.  The strict-concavity chord argument
is a different proof of ys2 than the source's monotonicity argument; this
is a documented deviation, not a weakening.  The rewiring S14 keeps the
statements of `Delta_pos`/`Q0_nonneg`/`P2`/`tension_ratio_chain` from
section 15 unchanged apart from the hypothesis packaging.


## 17. SL/SymlineKeyLemma.lean P1/P2 + W0 lemma (session 101)

Status: MACHINE_ACCEPTED_PENDING_AUDIT (machine check green; independent
re-derivation of S15-S21 against the source not yet executed).

`SL/SymlineKeyLemma.lean` (namespace `SL.SymlineKeyLemma`) formalizes the
algebraic core of `docs/SL_gap_n1_symline_proof.tex` sections 4.2-4.3
(Lemma P1, Lemma P2, the W0 lemma) that drives the KEY LEMMA (unique zero
of `Fe` on `(0,1/2)`).

Content:
- `q0 = sqrt(2/3)` (`q0_sq`) with location `4/5 < q0 < 5/6`
  (`q0_gt_four_fifths`, `q0_lt_five_sixths`), `0 < q0 <= 1`.
- `Gamma0 = arccos(q0/(1+q0))`: `0 < Gamma0 < pi/2`,
  `Gamma0 < pi/2 - 4/9` (`Gamma0_lt_pi_div_two_sub_four_ninths`, from
  `sin(4/9) < 4/9 < q0/(1+q0) = cos Gamma0` and cos antitone on
  `[0, pi]`), `cos_Gamma0`, `cot_Gamma0_gt_half` (from `sin^2 + cos^2 = 1`
  and `q0 < 5/6`), `cot_ge_cot_Gamma0` (cot antitone on `(0, pi/2)`).
- W0 lemma (`W0_lt_four_thirds_q0`): for `0 < gamma <= Gamma0`,
  `3 - 2*(pi-gamma)*cot gamma < 4*q0/3`, via
  `pi/2 + 4/9 < 2*(pi-gamma)*cot gamma` (from `Gamma0 < pi/2 - 4/9` and
  `cot gamma > 1/2`), `3 - (pi/2 + 4/9) <= 19/18` (from `pi > 3`) and
  `19/18 < 16/15 < 4*q0/3`.
- `Phi q x = cos^2 x + q^2 sin^2 x` with `Phi_nonneg`, `Phi_le_one`
  (`q in [0,1]`), `Phi_ge_sq` (`q^2 <= Phi`).
- Lemma P1 (`P1_bound`): for `q in [q0,1]`, `c in (0,1/2)`,
  `x in (0,pi/2)`: `G q c x <= -(6*sqrt 6 - 6)/5 < -4/3`.  Proof:
  bound `-Phi*(3 + 2*x*cot x)/(q + c*Phi) <= -3/(1/q0 + 1/2)` via
  `Phi/(q + c*Phi) = 1/(q/Phi + c)`, `q/Phi <= 1/q <= 1/q0`, and the
  constant identity `3/(1/q0 + 1/2) = (6*sqrt 6 - 6)/5` (`hconst`, from
  `q0 = sqrt 6 / 3`).
- Lemma P2 (`P2_bound`): for the same parameter range and
  `0 < gamma <= Gamma0`: `-4/3 < G q c (pi-gamma)`.  Split on the sign of
  `W0 gamma`: if `W0 gamma <= 0` both terms of `G(pi-gamma)` are
  nonnegative; else `Phi*W0/D < 4/3` via `Phi/D <= 1/q <= 1/q0` and the
  W0 lemma, then `-4/3 < -Phi*W0/D`.
- `P1_neg`, `P1_lt_P2` (via
  `six_sqrt_six_sub_six_div_five_gt_four_thirds`),
  `Fep_lt_zero_of_nonneg` (the KEY-LEMMA monotonicity step
  `(M1-M2)*G1 + M2*(G1-G2) < 0` from `M2 <= M1`, `G1 < 0`, `G1 < G2`),
  `gamma0_mono` (`gamma_0(q) = arccos(q/(1+q)) <= Gamma0` for `q0 <= q`).

Honesty notes (also in the file header):
- Certificate-free deviation: the source locates `Gamma0` with exact
  rational certificates (alternating-series bounds for cos/cot at 10/9,
  `pi > 22/7`).  The formal proof instead uses `sin(4/9) < 4/9`,
  `q0 in (4/5, 5/6)`, `pi > 3`, and antitone cos/cot; the constants are
  rational.  Numerical evidence is never used.
- Phase-branch hook: the source's P2 requires
  `gamma = pi - alpha2(c) <= gamma_0(q) <= Gamma0` from the phase-branch
  analysis (alpha2 decreasing in c).  Only the second half
  (`gamma0_mono`) is formalized; `P2_bound` takes `gamma <= Gamma0` as a
  hypothesis.  The branch reduction `pi - alpha2(c) <= gamma_0(q)` and
  the endpoint signs of `Fe` are not formalized.
- No `sorry`/`admit`/`axiom`.

### 17.1 Obligation map (machine level)

| Obligation | Lean declaration | Statement |
| --- | --- | --- |
| S15 | `q0_sq`, `q0_pos`, `q0_gt_four_fifths`, `q0_lt_five_sixths`, `q0_le_one` | `q0 = sqrt(2/3)`; `4/5 < q0 < 5/6` |
| S16 | `Gamma0_pos`, `Gamma0_lt_pi_div_two`, `Gamma0_lt_pi_div_two_sub_four_ninths`, `cos_Gamma0`, `cot_Gamma0_gt_half`, `cot_ge_cot_Gamma0` | location of `Gamma0`; `cot Gamma0 > 1/2`; cot antitone |
| S17 | `W0_lt_four_thirds_q0` | `0 < gamma <= Gamma0` => `W0 gamma < 4*q0/3` |
| S18 | `P1_bound`, `P1_neg` | `G q c x <= -(6*sqrt 6 - 6)/5 < -4/3` (Lemma P1) |
| S19 | `P2_bound` | `-4/3 < G q c (pi-gamma)` for `gamma <= Gamma0` (Lemma P2; branch hook documented) |
| S20 | `P1_lt_P2`, `Fep_lt_zero_of_nonneg` | sign consequences used by the KEY LEMMA |
| S21 | `gamma0_mono` | `gamma_0(q) <= Gamma0` for `q0 <= q` |

### 17.2 Machine evidence

- `lake build`: exit 0, "Build completed successfully (8583 jobs)";
  `SL.SymlineKeyLemma` built in this run.
- `sorry`/`admit`/`axiom` scan: 0 hits across `SL/`.
- `run-manifest.json` regenerated: 26 scanned files (25 `SL/` files +
  `lakefile.lean`); the temporary `ScratchCheck.lean` was removed before
  this run and is not scanned.

### 17.3 Independent audit status

Not yet closed.  S15-S21 must be re-derived against
`docs/SL_gap_n1_symline_proof.tex` sections 4.2-4.3 in an independent
pass: check that `P1_bound`/`P2_bound` match the source's Lemma P1/P2
(log-derivative bounds of `Mf` at `alpha1`, `alpha2`), that the W0 lemma
matches the source's bound on `3 - 2*(pi-gamma)*cot gamma`, and that the
certificate-free location of `Gamma0` is a documented deviation, not a
weakening.  The phase-branch reduction `gamma = pi - alpha2(c) <=
gamma_0(q)` remains an unformalized hook.
