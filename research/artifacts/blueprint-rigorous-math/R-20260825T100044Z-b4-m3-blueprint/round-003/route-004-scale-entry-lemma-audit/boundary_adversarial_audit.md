# Scale-entry lemma: definition, logic, boundary, and adversarial audit

Audit status: **PASS for the lemma stated in `proof_package.md`**, subject to
later independent proposal review.  This is a researcher self-audit and is
not an independent Blueprint review.

## Definition audit

- The exact variables are
  `u=R^(-1/6)>0`, `K=k2/u`, `r=k3/k2`,
  `x=p1-pi/2`, and `y=p3-pi/4`.
- The quantities whose boundedness was missing are defined only after the
  exact equations force their scales:

  ```text
  v=u^2,
  q=(K*x-2*v)/v^2=(A*K-2)/v,
  Cbr=K*(r-1)/v^2,
  B=y/v.
  ```

  Thus no boundedness of `A`, `B`, `q`, or `Cbr` is smuggled into the
  admitted-class hypotheses.
- `p2=K*u/2-u^3*(p1+p3)` and `p2t=r*p2` agree exactly with the hash-bound
  closed residual.  No coefficient from the defective Pbuild D-mass block is
  used.
- The proof stays in the real finite-nonzero-interior chart.  The limiting
  denominators are `sin(p1t)=1`, `sin(p3)=sqrt(2)/2`, and
  `cos(p3t)=sqrt(2)/2`.

## Logic and quantifier audit

- Quantifier order: for every exact zero selection on all sufficiently small
  positive `u` satisfying the admitted limits, there are branch-dependent
  constants `M,u0` giving the stated bounds for every `0<u<u0`.
- No continuity, differentiability, transseries, or measurability of the
  selected zero branch is assumed.  Compactness is used only by contradiction
  on arbitrary sequences `u_n -> 0`.
- Local IFT uniqueness is invoked only after the exact tangent identities
  prove bounded `q,Cbr` and a subsequence argument proves approach to the
  first-face graph.  The second phase variable is initially the unscaled
  `y=p3-pi/4`; hence the proof does not assume the conclusion `B=y/v=O(1)`.
- The implication direction is one-way: admitted exact zeros are forced into
  the certified germ.  No claim is made that singular geometries are absent.
- The final equality with the existing analytic germ uses exact local
  uniqueness, not agreement of formal coefficients.

## Boundary audit

- `K -> 0` or `K -> infinity`: excluded by the admitted compact-subset
  hypothesis.  These cases are not divided away and are not refuted.
- `r -> r0 != 1`: excluded.  The comparison of the two tangent identities
  specifically uses `r -> 1`.
- `p3` or `p3t` at a phase-denominator endpoint: excluded.  The admitted
  limits instead give `p3,p3t -> pi/4`.
- `p1t` at a sine zero: excluded; here `p1t -> pi/2`.
- `p2=0` or `p2t=0` at finite `u`: for sufficiently small `u`,
  `p2/u -> K/2` and `p2t/u -> K/2`, uniformly away from zero because
  `K>=K_->0`.  The exact tangent divisions are therefore legal.
- Negative `u`: not part of the asymptotic branch quantifier.  Analytic
  extensions in `v=u^2` are used only after the positive-`u` entry bounds.
- Discontinuous branch switching: the compactness and local-uniqueness
  argument applies pointwise and therefore also excludes a discontinuous
  selection among hypothetical nearby roots.

## Adversarial scale tests

1. **Slowly divergent `A`.**  Allow `x/u^2` to diverge as slowly as desired.
   The exact `E1` tangent identity has right side `2v/K+O(v^2)`, so such a
   branch cannot be a zero.
2. **Slowly divergent `Cbr`.**  Allow `(r-1)/v^2` to diverge while `r->1`.
   Subtracting the two exact tangent estimates gives
   `(r-1)*(p1+2v/(rK))=O(v^2)`, forcing bounded `Cbr`.
3. **Slowly divergent `B`.**  Allow `y/v` to diverge while `y->0`.  After the
   first spectral IFT, the reduced exact equation has
   `partial_y S6(0,K,0)=8/K`, uniformly nonzero.  Its local zero graph is
   `y=v/K+O(v^2)`; hence no such branch survives.
4. **Puiseux/log/inverse-log/flat deviations.**  None of the three entry
   arguments assumes an asymptotic expansion.  Once inside the analytic
   graph, local uniqueness excludes every distinct correction mechanism.
5. **Alternative positive `K` accumulation point.**  The remaining reduced
   mass equation has endpoint
   `2*(pi*K^3-18*pi^2+48)/(3*pi*K^6)`.  It has exactly one positive zero
   because the numerator is strictly increasing in `K>0`.
6. **Tangent periodicity.**  The hypotheses give `x,xt -> 0`; the proof uses
   the local tangent chart around zero, so no `pi`-shifted solution is lost.
7. **Source-normalization defect.**  Exact replay transcribes the closed mass
   formula and verifies all coefficients against its SHA-256.  The known
   Pbuild hard-odd term is neither imported nor regenerated.

## Computation audit and limitation

`scale_entry_replay.py` uses exact SymPy 1.13.1 arithmetic, verifies every
bound input hash, checks the analytic divisibilities, and independently
computes the first-face determinant plus the four reduced `(y,v)`
derivatives.  There is no sampling, random seed, floating-point tolerance, or
numerical acceptance predicate.  The symbolic replay certifies coefficient
identities; the universal conclusion is supplied by the analytic tangent,
compactness, and IFT proof in `proof_package.md`.
