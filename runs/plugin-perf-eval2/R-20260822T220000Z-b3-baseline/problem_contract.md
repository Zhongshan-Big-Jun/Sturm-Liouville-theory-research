# Problem contract: B3 fixed-n adjacent ratio supremum

Run: R-20260822T220000Z-b3-baseline
Contract version: 1
Source: `runs/plugin-perf-eval2/PROBLEM-B3-FIXEDN.md`, plus `docs/SL_fixed_n_supremum.tex`.

## Objects and definitions

- Dirichlet string equation: `-y'' = lambda rho(x) y`, `y(0)=y(1)=0`, `0 < a <= rho <= A`.
- Normalize `a=1`, `A=R>1` (scaling leaves ratios unchanged). Thus `rho in L^infty(0,1)`, `1 <= rho <= R` a.e.
- Eigenvalues `0 < lambda_1(rho) < lambda_2(rho) < ...` (simple).
- Fixed-n adjacent ratio: `Lambda_n^sup(R) = sup_rho lambda_{n+1}(rho)/lambda_n(rho)`.
- Alternating bang-bang family: `rho = [1, R, 1, R, ..., 1]` (2n+1 blocks), with all value-1 blocks width `w_1`, all value-R blocks width `w_2`, `w_1/w_2 = sqrt(R)`, `w_2 = t = 1/((n+1) sqrt(R) + n)`.
- Balanced phase variable `y = omega sqrt(R) t`, `F_n(y)` secular function for the alternating configuration; `Q_n(cos y)` polynomial after factoring `sin y`; `y_1 < ... < y_{2n}` roots in `(0,pi)`.
- Conjectured value `c_n(R) = ((pi - y_n)/y_n)^2`.

## Hypotheses

- `R > 1` fixed (finite).
- `n >= 1` fixed integer.
- `rho` may be any measurable function in the box; no continuity, symmetry, monotonicity, or finite-jump hypothesis.

## Target conclusion

The conjecture states:

1. Globally, `Lambda_n^sup(R) = c_n(R)`.
2. The supremum is attained by the alternating bang-bang configuration `[1,R,1,...,1]` with `w_1/w_2 = sqrt(R)`.
3. Within the alternating family, the ratio is maximized at `w_1/w_2 = sqrt(R)` and the balanced-phase root `y_n` gives `c_n(R)`.
4. For every `n>=1` and `R>1`, the alternating secular polynomial `F_n(y)` (equivalently `Q_n(cos y)`) has exactly `2n` roots in `(0,pi)`.

## Quantifiers and dependency of constants

- `R` is arbitrary but fixed finite `>1`.
- `n` is an arbitrary positive integer.
- All statements are quantified over every measurable density in the box for the global part.
- Constants in estimates may depend on `R` and `n`; no uniform bounds unless explicitly stated.

## Equivalent formulations that are actually proved equivalent

- `F_n(y)=0` with `y in (0,pi)` is equivalent to Dirichlet eigenvalues of the alternating `(2n+1)`-block configuration; scaling is fixed by `t`.
- Reflection symmetry `F_n(pi-y)=F_n(y)` is STRICT (`docs/SL_fixed_n_supremum.tex`, Theorem 1).
- If the 2n-root count is proved, then the balanced formula `lambda_{n+1}/lambda_n = ((pi-y_n)/y_n)^2 = c_n(R)` follows formally.
- For any `rho`, the ratio derivative formula (Feynman-Hellmann) gives `d/deps log(lambda_{n+1}/lambda_n) = int h (u_n^2 - u_{n+1}^2) dx` with the normalization `int rho u_k^2 = 1`; this is derived from the standard eigenvalue derivative and is exact.

## Boundary and degenerate cases

- `R=1`: the box degenerates to a single density; ratio `=1` for all n. The conjecture is trivially `c_n(1)=1` if extended continuously, but the problem fixes `R>1`.
- `n=1`: separate, but under the same formulas. `c_1(R)=nu(R)` is already SOLVED (`docs/SL_ratio_proof.tex`).
- `R -> infinity`: not in the allowed box; asymptotic limits are outside the strict contract.
- `rho` equal to endpoints on measure-zero sets: no effect on spectrum; allowed.

## Permitted outcomes

- affirmative proof of the full conjecture;
- negative proof / counterexample;
- rigorous partial theorem (e.g., finite bang-bang reduction, exact 2n-root count for a subclass, monotonicity for a restricted range);
- new reduction with a strictly smaller unresolved core;
- falsification of a sub-claim;
- exact obstruction.

## Completion criteria

- Full problem solved only if all three open obligations are closed with proof:
  (O1) global extremality via Keller-type reduction to alternating family;
  (O2) alternating-family monotonicity/uniqueness at `w_1/w_2=sqrt(R)`;
  (O3) general 2n-root count for the secular polynomial.
- A partial theorem is a valid result if it is a strict mathematical theorem or a precise reduction and is labeled with the matching status label.

## Acceptance criteria per subproblem

- (O3) `2n-root count`: a proof that `F_n` has exactly `2n` roots in `(0,pi)` for every `n>=1`, `R>1`. **CLOSED in this run** (see `candidate_proof.md` Part B).
- (O2) alternating monotonicity: a proof that in the symmetric alternating subfamily the ratio is maximized at the balanced phase width ratio. **OPEN**.
- (O1) global extremality: a proof ending in `Lambda_n^sup(R) <= c_n(R)` and attainment by the alternating configuration. **PARTIAL** (structure theorem proved; equal-width optimum/value open).

## Results that do not count as completion

- Numerical root counts, random searches, or high-precision scans;
- finite verified `n` cases without a general proof;
- a reduction whose missing lemma is equivalent to the original conjecture;
- unverified literature citations;
- a proof of the gap functional `D_n` instead of the ratio functional without a transfer argument.

## Forbidden moves

- Presenting numerical evidence as proof (global AGENTS.md rule).
- Silently changing `n`, `R`, boundary conditions, or allowed density class.
- Claiming novelty without a literature audit.
- Using an unproven `F_n` root count to derive `c_n(R)`.

## Tool, citation, and search constraints

- Project tools available: `balanced-phase`, `transfer-matrix-secular`, `keller-variational`, `bang-bang`, `reflection-branch-reduction`, `gap-band-extremals`, `band-selfconsistency-equivariance`, `switch-saturation-k-invariant`.
- Existing strict results in `docs/SL_gap_nge2_finite_reduction_proof.tex` and `docs/SL_gap_nge2_exact_2n_switches_proof.tex` concern the gap `D_n = lambda_{n+1}-lambda_n`, not the ratio; they may serve as analogies or tools but do not directly transfer without a new argument.
- Search allowed: local docs, scripts, web search.

## Ambiguities or competing interpretations

- The problem statement says "prove the fixed-n adjacent ratio supremum ... global extremality ... and/or the general 2n-root count". "And/or" means any rigorous partial result is acceptable, but final completion requires all three.
- The word "attained" in the conjecture is interpreted as existence of a maximizer and equality at the specific alternating configuration.

## Contract audit

- Read directly from `PROBLEM-B3-FIXEDN.md` and `docs/SL_fixed_n_supremum.tex`.
- No material ambiguity found beyond the "and/or" scope.
- This contract will be updated if a materially different interpretation is adopted.
