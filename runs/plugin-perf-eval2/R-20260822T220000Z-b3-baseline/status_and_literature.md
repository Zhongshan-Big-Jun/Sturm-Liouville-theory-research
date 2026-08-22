# Status and literature map

Run: R-20260822T220000Z-b3-baseline
Last updated: 2026-08-22T22:40Z (approx)

## Current status

- Overall B3 status in project map: PARTIAL.
- Already STRICT from project:
  - Reflection symmetry of alternating secular polynomial `F_n(pi-y)=F_n(y)` (all `n`, `R>1`).
  - B1 full sequence ratio supremum `sup_{n,rho} lambda_{n+1}/lambda_n = nu(R)`, with `n=1` reaching `c_1=nu(R)`.
- New STRICT partial result from this run (R1):
  - Every global fixed-n ratio maximizer is bang-bang with exactly `2n` switches and material order `[1,R,1,R,...,1]`.
  - This follows from a ratio adaptation of the gap exact-2n-switch theorem: H switching function, energy invariant `E=0`, and endpoint ratios `q0 = 1/c`, `q1 = -1/c`.
- New STRICT result (O3):
  - The alternating balanced secular polynomial `F_n(y)` has exactly `2n` simple roots in `(0,pi)` for every `n>=1`, `R>1`.
  - Proof via transfer-matrix recurrence `G_n=tau G_{n-1}-G_{n-2}`, square variable `x=C^2`, and identification with a Jacobi matrix / Chebyshev combination `U_n(t)+1/s U_{n-1}(t)`.
- Not proved:
  - O1: global fixed-n extremality to the specific equal-width alternating family (and value `c_n(R)`).
  - O2: alternating-family monotonicity at width ratio `sqrt(R)`.

## Known exact results in project

### B1 (SOLVED)
- Theorem: `sup_{n>=1} sup_{1<=rho<=R} lambda_{n+1}/lambda_n = nu(R)`; maximizer `[1,R,1]` with `t=1/(2sqrt(R)+1)`.
- Proof: trivial `lambda_{n+1} <= lambda_{2n}` + independently reproved Mahar-Willner Lemma 2 (`sup_rho lambda_{2n}/lambda_n = nu(R)` and `inf = mu(R)`) + balanced-phase closed form.
- Source: `docs/SL_ratio_proof.tex`.

### B4 gap extremals (STRICT for different functional)
- `D_n(rho) = lambda_{n+1}(rho)-lambda_n(rho)`:
  - `D_n` attains max/min on the full measurable box.
  - Every global maximizer/minimizer is bang-bang and has at most `2n` switches (`SL_gap_nge2_finite_reduction_proof.tex`).
  - Every global extremizer has exactly `2n` effective switches; max pattern `[1,R,1,...,1]`, min `[R,1,R,...,R]` (`SL_gap_nge2_exact_2n_switches_proof.tex`).
- Caveat: these results are for the gap functional, not the ratio; the switching function for gap is `F_gap = lambda_n u_n^2 - lambda_{n+1} u_{n+1}^2`, while for ratio it is `H = u_n^2 - u_{n+1}^2` after normalization.

### `R=1` base case for n>=2 gap family (STRICT)
- `f_1(x)` has exactly `2n` simple zeros for `R=1`; used as base for band-selfconsistency/equivariance framework. This is gap-side, not directly ratio-side.

## Literature (external)

- J. B. Keller, "The minimum ratio of two eigenvalues", SIAM J. Appl. Math. 31 (1976) 485-491. DOI 10.1137/0131042. Used for variational conditions; proved min `lambda_2/lambda_1 = mu(R)` and general bang-bang structure.
- T. J. Mahar and B. Willner, "An extremal eigenvalue problem", CPAM 29 (1976) 517-529. DOI 10.1002/cpa.3160290505. Used for sup `lambda_{2n}/lambda_n` via periodic extension and zero truncation.
- B. E. Willner and T. J. Mahar, "Extrema of functions of eigenvalues", JMAA 72 (1979) 730-739. DOI 10.1016/0022-247X(79)90260-9. Explicit prior-work risk for general eigenvalue-functional extrema; not fully page-audited.
- H. Sun, "On the minimum eigenvalue gap for vibrating string", JMAA 516 (2022) 126513. DOI 10.1016/j.jmaa.2022.126513. n=1 gap minimization, not ratio fixed-n.
- Q. Kong and A. Zettl, "Eigenvalues of Regular Sturm-Liouville Problems", JDE 131 (1996) 1-19. DOI 10.1006/jdeq.1996.0154. Standard regularity/continuity.
- G. Teschl, ODE and Dynamical Systems, GSM 140. Standard Prufer/nodal theory.

## Novelty risk

- The project itself has already produced a large body on gap extremals. The ratio fixed-n problem is explicitly recorded as OPEN.
- No local or external source has been found that simultaneously asserts the fixed-n ratio supremum and the alternating family/2n-root count. However, no claim of novelty is made.

## Coverage dimensions

- Global existence/bang-bang reduction for ratio: currently gap-side only; ratio-side reduction is a target.
- Alternating family optimization: only numerical evidence for `n=2,R=4` etc.
- 2n-root count: only numerical evidence for `n<=6`, `R` sampled.
- Literature on general eigenvalue functional extrema: Willner-Mahar 1979 risk, not fully audited.

## Gaps in knowledge

- Is there a published theorem for the fixed-n ratio supremum? Not known; not searched yet at full-text level.
- Is there a known Sturmian proof that `Q_n` has all real roots? Unknown.
- Does the exact 2n-switch gap theorem transfer to ratio via a change of objective? Not established.
