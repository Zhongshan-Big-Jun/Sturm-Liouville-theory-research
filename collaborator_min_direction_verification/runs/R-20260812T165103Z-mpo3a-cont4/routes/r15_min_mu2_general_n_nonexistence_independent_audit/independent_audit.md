INDEPENDENTLY_AUDITED_PROOF

# Independent four-part audit of R15 minimum-law `mu=2`, all `n>=3`

## 0. Verdict, scope, and bindings

Verdict: `PASS` for the frozen mathematical package.

The audited statement is:

> For every finite `R>1` and every integer `n>=3`, there is no strict,
> premise-complete, transverse, common-terminal full-relay root with `2n`
> events obeying the minimum saturation law at `mu=2`.

The audit is bound byte-for-byte to

```text
derivation.md
  sha256:97816827f2044ee7abbc2f80b90d0323c48298d3f797dfb6a15379127ed9509e
general_n_exact_check.py
  sha256:e72deabb74c2e1b88f02dfdabae7e242d418e23354dff4640db4f1f088ecdb42
general_n_exact_check.json
  sha256:52c84d41496f406c1e83d6a8bd6e977b20fdef3d3c4bbaf6c7abbc73c2f93e65
```

and to the canonical snapshot

```text
blueprint sha256:0120d1fb32af1a30449575995efccb6d1afcce416ee671ad00a5f296400fd799
inventory sha256:b6286574edbcb70ad22e5c6758a81f00dd01572c0764b8816be23cb6b166fb6f
```

The mechanism-independent replay is
`independent_orientation_check.py`, SHA-256
`1a9c3e2d810eba915f6a3e9536d23ad4bd0e10caedb765c0f8b62c3431d6160a`.
It uses SymPy `1.14.0` and exact rational-function algebra.  The author's
checker and the independent checker both replayed without an assertion
failure.  No floating-point or finite-`n` observation is used in the proof.

This is a mathematical audit of a frozen candidate package.  It does not
edit canonical files and is not a proposal/validation-bound transaction
review; a later immutable proposal must still bind its own validation and
review records.

## 1. Definition audit: pass

### 1.1 Law and material order

For the minimum law, the reversal of the defining max allocation gives

```text
S=U^2-4V^2>0: rho=1,
S=U^2-4V^2<0: rho=R.
```

Thus a forward positive-negative pair has lower-mode material frequencies
`(1,r)`, where `r=sqrt(R)>1`.  A physical forward negative-positive pair
has order `(r,1)`; reversing time reverses the order and again gives
`(1,r)`.  The contrast in the canonical positive-negative formula is
therefore the same `r`, not `1/r`.

### 1.2 Event amplitudes and the meaning of `a,b`

Let the shared event amplitude of a positive-negative pair be normalized to
one.  Write its left and right event amplitudes as `L,B`.  With

```text
c_x=cos(theta_x), s_x=sin(theta_x),
C_x=cos(2theta_x), S_x=sin(2theta_x)
```

and analogously for `y`, momentum continuity is

```text
(c_x-L)/s_x = r(B-c_y)/s_y,
(-C_x-L)/S_x = r(B+C_y)/S_y.                         (1.1)
```

The exact solution has `L=1/a(x,y,r)` and `B=b(x,y,r)`.  Hence `a` is the
forward ratio across the positive cell and `b` the forward ratio across the
negative cell, exactly as used in R15.

All internal event amplitudes are nonzero: at an event, `U=0` would also
give `V=0`, and then the switching derivative would vanish, contradicting
transversality.  Thus every `z_j` and reciprocal in the proof exists.

### 1.3 Switch-sign gauge

The event quotient signs alternate.  Reversing a two-cell segment flips the
starting sign relative to the displayed canonical triple, but this is the
harmless gauge `V -> -V`.  In (1.1) the high-mode momentum equation is
unchanged after both sides are multiplied by `-1`.  The independent checker
solves both starting gauges and obtains identical `a,b`.  Therefore the
time-reversed segment remains in the same local object class.

No reflection symmetry, endpoint-cell phase law, or eigenfunction global
sign choice is embedded in these definitions.

## 2. Logic audit: pass

### 2.1 The local contraction

Put `X=x^2`, `Y=y^2`.  A strict physical positive-negative interface has

```text
1/3<Y<1, 0<X<(1-Y)^2/(4Y), kappa_0<kappa<kappa_N.
```

The last upper inequality is not an extra assumption.  A strict negative
cell has negative event-amplitude ratio.  In the standard one-cell normal
form, if that ratio were positive, the two required endpoint derivative
orientations would demand simultaneously `z<k(theta)` and
`z>1/k(theta)`, with `0<k(theta)<1`, which is impossible.  Hence `b<0`.
Since the denominator of `b` in the displayed phase chamber is negative,
`b<0` is equivalent to `N_b>0`; equation (2.4) of the package is then
equivalent to `kappa<kappa_N`.  Also `kappa=r kappa_0` and `r>1`, so
`kappa_0<kappa`.

The remaining sign chain is exact:

```text
C=(3Y-1)(1-Y)>0,
E=C+2Y(Y-X)>0,
kappa_D-kappa_N
 =2(Y-X)^2(1-XY)/[(1-X)(1-3X)E]>0.
```

Thus `kappa<kappa_N<kappa_D` gives `D_a>0`.  Since `x<y`, the numerator of
`a` is positive, hence `a>0`.  Finally

```text
a-1=(1-X)T/D_a,
T=y[kappa(1-3X)+2X+Y-1],
```

and at `kappa_N` the bracket equals

```text
-(Y-X)[(1-Y)^2-4XY]/E<0.
```

It is strictly increasing in `kappa`, so it is also negative for the
physical `kappa<kappa_N`.  Therefore `0<a<1`.  Every cancelled or divided
factor above is strict and has the displayed sign.  The author's exact
checker independently verifies all polynomial identities used here.

### 2.2 Direct attack on time reversal and the reciprocal

For a generic oscillator transfer matrix,

```text
M_omega(t)=[cos(omega t), sin(omega t)/omega;
            -omega sin(omega t), cos(omega t)],
J=diag(1,-1),
J M_omega(t) J=M_omega(t)^(-1).                      (2.1)
```

This reverses momenta and preserves positions.  To exclude a misleading
pictorial argument, the independent checker also solves the physical
negative-positive pair directly, without invoking (2.1).  With its shared
amplitude again equal to one, the exact endpoint solution is

```text
left amplitude  =b(x,y,r),
right amplitude =1/a(x,y,r).
```

Consequently its forward ratios are `(1/b,1/a)`.  For the actual left pair
`(I_(j-1),I_j)`, this says

```text
z_(j-1)=1/b(x_j,y_(j-1),r),
z_j    =1/a(x_j,y_(j-1),r),
```

or equivalently

```text
1/z_j=a(x_j,y_(j-1),r).                              (2.2)
```

The right pair `(I_j,I_(j+1))` is already positive-negative and gives

```text
z_j=a(x_j,y_(j+1),r).                                (2.3)
```

Equations (2.2)--(2.3) yield the claimed compatibility product one.  This
checks the exact concern most likely to reverse the theorem: the left
relation contains `1/z_j`, and neither `a,b` nor `r,1/r` are interchanged.

### 2.3 Local-to-global implication

Both adjacent interfaces are restrictions of the same assumed physical
trajectory.  They use the same `x_j` and contrast `r` but may have different
negative phases.  The local theorem applies separately to both, so

```text
0<a(x_j,y_(j-1),r)<1,
0<a(x_j,y_(j+1),r)<1.
```

Their product cannot equal one.  Endpoint and norm equations only add
constraints to this already empty internal compatibility system; no
necessity/sufficiency direction is reversed.

## 3. Boundary audit: pass

- For `n>=3`, there are `2n-1>=5` internal cells, so `I_2,I_3,I_4` all
  exist.  Moreover `3<=2n-3`, with equality at `n=3`.  Thus the fixed choice
  `j=3` is valid for every quantified `n`, not only in a finite table.
- `I_3` is odd and positive; `I_2,I_4` are even and negative.  Both
  interfaces are internal, so the sharper internal phase theorem applies.
- For `n=2`, the upper index is `2n-3=1`; no flanked internal positive cell
  exists.  The proof correctly excludes this case.
- `R=1`, `a=1`, `b=0`, phase endpoints, collapsed feasibility, grazing,
  collision, zero-length cells, and endpoint escape are excluded by the
  strict premise contract rather than obtained by closure.
- Arbitrary asymmetry is retained: no equality between `y_2` and `y_4` or
  between reflected cells is used.
- The endpoint cells, global norm equation, reflection, and overall signs
  of the eigenfunctions cannot repair an inconsistent internal product.

## 4. Adversarial audit: pass

The weakest step was attacked in four independent ways:

1. the material law was applied before and after reversal, confirming
   `(R,1)` forward becomes `(1,R)` backward with unchanged `r`;
2. `J M J=M^{-1}` was checked for a symbolic generic frequency;
3. the negative-positive momentum equations were solved directly and gave
   ratios `(1/b,1/a)`, hence exactly `1/z_j=a`;
4. both possible starting quotient-sign gauges were solved and gave the
   same amplitudes.

The smallest words were checked symbolically: `n=2` lacks the obstruction,
while `n=3` has exactly the triple `I_2,I_3,I_4`.  The finite tables in the
author package are corroborative only; the inequalities
`2n-1>=5` and `3<=2n-3` discharge the universal quantifier.

No counterexample, circular premise, missing interface, material inversion,
or endpoint exception survived these attacks.

## 5. Disposition

```text
definition_audit:   PASS
logic_audit:        PASS
boundary_audit:     PASS
adversarial_audit:  PASS
unresolved_mathematical_obligations: []
mathematical_status: independently audited proof on the frozen scope
canonical_transaction_status: unchanged / no proposal submitted
novelty_status: unknown
```

The theorem may be carried forward only with its exact restrictions:
minimum law, `mu=2`, finite `R>1`, strict premise-complete transverse
full-relay roots, and `n>=3`.  It supplies no statement for `n=2`, the
maximum law, general `mu`, or boundary words.
