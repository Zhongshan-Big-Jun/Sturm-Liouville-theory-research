# C2-H self-audit

## Verdict

`RIGOROUS_PARTIAL_RESULT`.  The arbitrary-`mu`, phase-dependent weak-
contrast collar is candidate-complete for independent review.  The global
all-finite-contrast interface lemma remains open.

## Definition audit

- `r=sqrt(R)` and `delta=r^2-1=R-1`; no `r-1`/`R-1` substitution is made.
- `+` and `-` denote positive and negative internal cells, not left and
  right endpoints.  The right interface is treated only after time reversal.
- `p,kappa,U,lambda,d,eta,w,u,A0` use the normalized common-angle definitions
  in `report.md`; the checker reconstructs them from the two half-angle
  momentum equations.
- The checker verifies the exact bridge from the pre-normalized physical
  split numerator to `U_+^2 Phi/(lambda u^3)`.
- The three-cell gluing is now internal to this package.  With
  `gamma_2=-rG<0<gamma_3=rJ` and `W=abs(K_2)>0`, it verifies
  `x_*=(gamma_3-gamma_2)/W>0` and
  `Hx_*=E_L+E_R` directly.
- The checker reconstructs both positive Schur prefactors.  In the left
  orientation `E_L=rG N_L/(delta D_1Q_-)`; after time reversal it obtains
  `E_R=rJ_RN_R/(delta D_3B_RQ_-)`.
- `H` is the scalar `n=2` dual Schur complement.  No all-`n` determinant or
  reflection conclusion is silently inserted.

## Logic audit

- Every denominator divided by in the proof is positive on the strict
  physical branch.
- The positive-cell lemma proves `A00>kappa_+>0`; positivity of the collar
  thresholds is therefore strict.
- With `tau=max(tau_1,tau_2)`, `delta<tau` means `delta` is below whichever
  of the two sufficient thresholds is larger, so the union logic is valid.
- The physical branch independently requires `r<rB`; hence the certified
  interval is `1<R<min(rB^2,1+tau)`.
- The asymmetric corollary applies the local sign theorem twice and takes
  the minimum threshold; it never assumes equal phase data.
- Time reversal was checked at the level of both momenta, not only the
  gamma combination: `z->1/z` swaps `g<->h` and `G<->J`, while
  `D_3=D_1/a^2` and `N_R=N_L/(a^2B)`.  The latter factor is strictly
  positive on the physical amplitude branch.
- Every denominator in the two Schur prefactors is positive:
  `delta,D_1,D_3,Q_-,B_R>0`; no zero determinant or endpoint ratio is
  cancelled in the gluing.
- A pointwise phase threshold is not promoted to a uniform small-contrast
  theorem over every root.

## Boundary audit

- `R=1` is excluded but the one-sided limit is strictly positive.
- `mu=1`, `mu=infinity`, phase thresholds, grazing, and `B0=0` are not in
  the quantified strict domain.  No uniform limiting threshold is claimed.
- If `rB<=1`, the local physical branch is empty.
- The result is restricted to `n=2`; no transfer argument for `n>2` is
  asserted.
- At `mu=2`, the existing canonical full-contrast theorem is stronger; the
  new scope is general finite `mu`, particularly `mu!=2`.

## Adversarial audit

- The exact rational `mu=2` witness in the checker lies on the common-angle
  curve, satisfies the strict phase and amplitude branch, and has both
  sufficient factors `Lambda,Xi` negative while `Phi` remains positive.
  It blocks the tempting global extension but is not a counterexample to
  the target interface sign.
- A discovery grid also searched small and large `mu`, both phase edges,
  and `r` near both ends of the physical interval.  Those floating-point
  observations are not proof inputs.
- The canonical fixed-`n` small-contrast uniqueness theorem does not render
  this result a duplicate: it has a different conclusion and supplies no
  local Schur sign or explicit phase-dependent threshold.  Conversely, this
  route does not recover global uniqueness or reflection.

## Exact remaining obligation

Outside the collar, both

```text
Lambda=A0-(R-1)w u^3
```

and

```text
Xi=4lambda^2 p_+ A0-(R-1)p_-u^4
```

may be negative on a fully physical interface.  A restart must redistribute
the still-positive `kappa_-` and `p_+` blocks in the exact decomposition, or
introduce a new common-angle curvature/total-positivity invariant.  Proving
either `Lambda>0` or `Xi>0` globally is refuted by the exact witness.
