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
