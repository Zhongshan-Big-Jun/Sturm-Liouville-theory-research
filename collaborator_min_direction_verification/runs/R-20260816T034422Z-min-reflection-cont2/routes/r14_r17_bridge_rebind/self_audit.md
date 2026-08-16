# C2-J self-audit: general-`mu` coefficient bridge

## Verdict

`PASS_FOR_CONDITIONAL_BRIDGE`.

The implication

```text
complete retained-cube proof of G_1,...,G_4>0
 => every physical n=2 minimum interface has Phi>0
 => H>0 => partial_q A_2<0 => fixed-mu reflection
```

is candidate-complete and exactly replayed.  The antecedent is not proved by
this route.  Therefore the unconditional general-`mu`, `n=2` reflection
theorem remains non-propagating until the independent C2-I full coefficient
cover is complete, reviewed, and hash-bound.

## Provenance and premise audit

- Canonical Blueprint:
  `b93b42029f95d55489c71e344af329220c3182ff07c2d0b57b9e170b7d4f7056`.
- Canonical inventory:
  `b6286574edbcb70ad22e5c6758a81f00dd01572c0764b8816be23cb6b166fb6f`.
- The semantic and proof hashes of FULL-RELAY, INTERNAL-PHASE-R8,
  PHYSICAL-CONTINUANT-R7, MIN-DETERMINANT-PARITY-R35, and
  EITHER-CONDITIONAL-GLOBAL-ORDER-R11 are listed verbatim in
  `bridge_proof.md`.
- Historical R11/R14/R17 files were used only to locate formulas to be
  rederived.  No historical candidate statement is a premise.
- The full physical Cramer/Phi and three-cell gluing rederivation is
  dynamically replayed from C2-H only after checking the frozen hashes of
  both its checker and report.

## Coordinate and retained-domain audit

1. The map
   `(mu,alpha,beta)<->(k,t,y)` is given with both directions and is a
   bijection between the strict R8 chamber and `(0,1)^3`.
2. `g>0` everywhere.  The split `g>=1` versus `g<1` is exhaustive; the
   equality face belongs to the analytic half.
3. Every physical branch has `1<r<rB`, so `rB>1`.  Points with `rB<=1`
   cannot represent a retained physical interface and may be discarded only
   after that emptiness is certified.
4. C2-I must prove all four gaps on every retained interior cube point.  A
   central subcube, finite sample, or collection of unjoined collars is not
   enough.  An interval box may be discarded only by proving its
   intersection with `g<1,rB>1` empty.
5. Closed-cube faces are analytic limit devices, not physical premises.
   Nevertheless, the certified union must contain every retained interior
   sequence tending to `mu->1`, `mu->infinity`, either strict phase edge, or
   an intersection of such faces.

## Local algebra and sign audit

1. Both independent endpoint momenta are substituted into the Cramer
   solution.  The gamma combination alone is never used as an interface
   surrogate.
2. The exact physical split numerator is
   `U_+^2 Phi/(lambda u^3)` with a strict positive prefactor.
3. In the analytic half, `Phi-Psi` is a sum of positive terms and
   `Psi>0` follows from `g>=1` and the strict positive-cell response margin.
4. For `g<1`, strict decrease of `p(theta)/x(theta)^2` gives
   `lambda x_+<x_-`, hence `w>x_+` throughout the closed auxiliary interval
   `[1,rB]`.  The proof uses absolute cotangent bounds and does not assume a
   cotangent sign.
5. `D>0` implies `Enew>0` through the strict quadratic
   `w ell-u h=2(1-g)w^2+x_+w-x_+^2>0`; then
   `E>Enew`, `Psi>0`, and `Phi>0`.
6. The quartic Bernstein coefficients are reconstructed from the power
   polynomial.  `B_0=gKnew>0`; the only coefficient premises are
   `B_1,...,B_4>0`.
7. Repeated quartic roots and both `r` endpoints require no separate case:
   strict positive Bernstein coefficients give `D>0` on all of
   `[1,rB]`.  At `r=1`, `D=gKnew>0`; `r=rB` is an auxiliary branch boundary,
   not a division by the vanishing amplitude margin.

## Stable-coordinate and denominator audit

- `0<k<1`, `0<a0<1`, `0<kb0<1`, `q0,sigma0>0`.  The inequality
  `kb0<1` follows from `kA_-<pi-A_-` and monotonicity of `tan` on
  `(0,pi/2)`.
- On `g<1`, the exact formula for `ebar` gives `b0>a0`; hence
  `a0+b0>0`.
- The factors `1-k^2a0`, `1-k^2a0^2`, `1-k^4b0^2`, and
  `1-k^2b0^2` are strict positive.
- On the retained `rB>1` set, the exact positive numerator of `rB` forces
  `Dtilde>0`.  Thus no stable formula divides by zero.
- The checker derives, rather than assumes, the formulas for `rB`, both
  `Wbar` endpoints, the cancellation-safe sinc expression for `Xbar`, both
  `Ubar,Hbar,Lbar` endpoints, `Pplus`, `g`, and `Knew`.
- Since `cp>0`, `G_i=cp^4B_i` is a strict sign equivalence.  No square root
  sign is left implicit.

## Left/right gluing audit

- The actual positive phases may be unrelated.  The universal local result
  is applied to two distinct cube points.
- With the actual middle cell,
  `gamma_2=-rG<0<gamma_3=rJ` and
  `x_*=(gamma_3-gamma_2)/abs(K_2)>0`.
- The exact identity is `Hx_*=E_L+E_R`.
- C2-H now replays both positive Schur prefactors.  Time reversal sends
  `z->1/z`, swaps `g<->h` and `G<->J`, and gives
  `D_3=D_1/a^2`, `N_right=N_left/(a^2B)`.  All scaling factors are strict
  positive, so the right sign is not inferred from reflection.

## Determinant, singularity, and global-order audit

- For `n=2`, R35 makes `H` scalar and gives
  `sign det(L_-)=sign H`, including zero.
- R7 is polynomial in the terminal continuant.  Its singular q-Jacobi case
  is included: `det(L_-)=0` exactly when the distinguished terminal
  q-Jacobi position pair vanishes.  No matrix inverse is used there.
- The strict local conclusion `H>0` excludes that singular case and yields
  `partial_q A_2<0`.
- The conditional-global-order contract already supplies global residual
  continuity, chamber-closure compatibility, premise completeness of every
  zero, event-pair birth/death softness, and the reflected second-zero
  argument.  The bridge supplies exactly its missing uniform orientation
  `sigma=-1` for the minimum law.
- Equal norm is used only to select self-consistent solutions after every
  common-terminal zero has been reflection-fixed.  Existence, uniqueness of
  the full two-residual system, and `n>2` are not claimed.

## Exact replay and remaining obligation

`exact_checker_output.json` records a deterministic PASS under Python
3.12.13 and SymPy 1.14.0, with no randomness.  The single missing input is:

```text
a complete immutable C2-I certificate proving G_1,...,G_4>0 at every
retained g<1,rB>1 point of the full strict physical cube, including all
boundary/intersection approach regions and no unresolved boxes.
```

Formalization status: `not_requested`.  No canonical file, submission,
review, or integration artifact was changed.
