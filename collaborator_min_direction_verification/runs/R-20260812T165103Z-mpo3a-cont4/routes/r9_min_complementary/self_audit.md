RIGOROUS_PARTIAL_RESULT_WITH_RESTRICTED_THEOREM

# R9 min complementary-inertia author self-audit

This is an author-side audit of the frozen `mu=2,n=2` theorem package.  It
is not the independent review required for canonical promotion.

## 1. Definition audit: PASS

1. `M=D+B^T K^{-1}B` uses the accepted min sign convention, with odd
   internal cells positive and the middle even cell negative.
2. The dual matrix is `H=CP^{-1}C^T-W`; the Schur identity is
   `n_-(M)=n_+(H)`, not the sign-reversed false identity.
3. For `n=2`, `H`, `x_*`, `E_L`, and `E_R` are scalars.  The single middle
   cell defines one shared `x_*=(gamma_3-gamma_2)/abs(K_2)>0`.
4. The actual left phase pair is `(x_1,y_2)` and the time-reversed actual
   right pair is `(x_3,y_2)`.  No equality `x_1=x_3`, palindromy, or root
   symmetry is assumed.

## 2. Logic audit: PASS

1. The two-momentum equations are solved individually.  The exact rational
   no-go using gamma matching alone is retained only as a refutation of a
   weakened lemma and is never called a physical counterexample.
2. The positive prefactor identities from the physical gaps to `N_L,N_R`
   are checked symbolically in `symbolic_split_gap_mu2.py`.
3. Both `N_L` and the time-reversed `N_R` reduce to the same primitive `P`,
   with every cancelled denominator assigned its physical sign.
4. The natural-variable identity is exactly
   `P=Y^2 Q/(3Y-1)^2=y^4 Q/(3Y-1)^2`; hence the multiplier is strictly
   positive in the physical chamber.
5. `N_b>0` gives `0<kappa<kappa_N<1`.  The certificate is proved on the
   larger box `0<X<1/3`, `1/3<Y<1`, `0<kappa<1`, so no unproved use of the
   remaining branch or common-energy inequalities is needed for the sign.
6. All 539 same-degree tensor Bernstein coefficients are exact rationals:
   387 positive, 152 zero, 0 negative.  The script performs the complete
   inverse basis transform and recovers every power coefficient exactly.
7. On the open cube every Bernstein basis function is strictly positive;
   at least one positive coefficient therefore gives strict `Q>0` despite
   the 152 zero coefficients.
8. Applying the local lemma separately at both actual interfaces yields
   `E_L,E_R>0`; their exact sum is `Hx_*`, so `H>0`.  The dual Schur identity
   then gives `n_-(M)=1` and `n_0(M)=0`.
9. The R7 trusted equivalence is applied only after nonsingularity and gives
   `det(L_-)>0`, `J<0`, and `partial_q A_2<0` with the min sign.

## 3. Boundary audit: PASS

- `R=1`, grazing, phase-threshold equality, `y=1`, zero event amplitudes,
  and singular interface denominators are outside the strict theorem and
  are not reached by a premise-complete transverse root.
- The Bernstein argument is nonnegative on the closed containing box and
  strict at every physical interior point.
- Every finite `R>1` is allowed; no small-contrast or compactness bound is
  used.
- Both asymmetric roots and non-reflection-fixed phase triples are covered.
- The theorem is restricted to `mu=2,n=2`; general `mu>1` and `n>2` remain
  explicitly open.

## 4. Adversarial audit: PASS within restricted scope

- **Dual-sign attack:** both Schur complement orders were compared, fixing
  `n_-(M)=n_+(H)`.
- **One-momentum relaxation attack:** defeated by exact use of the separate
  `U` and `V` momentum matches.
- **Left/right identification attack:** defeated by two separate
  applications of one local interface lemma.
- **Wrong test-vector scaling attack:** the exact weight is
  `delta_gamma/abs(K_2)`; the failed `abs(K_2)^(-3/2)` discovery weight is
  quarantined as numerical evidence.
- **Floating-point positivity attack:** all sign coefficients and basis
  transformations are over `QQ`; finite numerical probes are unused.
- **Boundary-zero attack:** strictness follows from positivity of every
  interior Bernstein basis function, not from a claimed positive minimum.
- **Generalization attack:** no inference to `mu!=2` or `n>2` is made.

## Frozen exact certificate identifiers

```text
P expanded-string SHA-256:
  906da32475eb75bdcac45a5e04b490661722d9d356717301c5915c2c125c8591
Q core expanded-string SHA-256:
  622036e509741e9717fdf33a07340379510f642d42160fc8cf7ddd076dcfb247
Q_box expanded-string SHA-256:
  80a3aa1c535e2e47c32a7bf52a872d12c8e0e71dde726610b896c7fdfe49d2f4
Bernstein coefficient-table SHA-256:
  1a38cc16ec05e873e5f7d2fe205e0f0f31e999d2041e506c563d06242c394c7b
```

Final route-file byte hashes are communicated externally after this audit
file itself is frozen, avoiding a self-referential digest.

```text
definition audit: PASS
logic audit: PASS
boundary audit: PASS
adversarial audit: PASS within mu=2,n=2 scope
independent review for promotion: REQUIRED
general mu>1,n>=2 target: OPEN
physical counterexample: NONE
```
