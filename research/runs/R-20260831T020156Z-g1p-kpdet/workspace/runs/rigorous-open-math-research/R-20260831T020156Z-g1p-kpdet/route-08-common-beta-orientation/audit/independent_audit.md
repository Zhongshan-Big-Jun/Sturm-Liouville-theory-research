# Independent audit of W12 and W13

## Verdict

`PASS`.

Audit ID: `AUDIT-W12-W13-ORIENTATION-01`.

W12's strict claims are accepted as a partial result. They close the chamber

```text
Bcoef<0 and c alpha<=pi/2,
```

and therefore close KP-DET for every complete tuple with `0<c<=1/2`.
Arbitrary finite-`c` `PHI-SIGN` and KP-DET remain open. W13 remains
`EVIDENCE` only and is not used in this verdict.

## Integrity audit

Every bound input was hashed before mathematical use. All values matched the
audit packet exactly.

| Artifact | Verified SHA-256 |
|---|---|
| `problem_contract.md` | `67427fe00b6b7758552581cde19fdb449202b5e9ea7bf9013f6ba0a4135f3f9d` |
| `route-01-transfer-schur/derivation.md` | `a96fde4cfaaf3cb83fcf416d3d7e627a5d63c4a48c2cd8a0c562e9dd8636e7d3` |
| `route-03-phi-exact/worker_result.md` | `6c1bbbd871c9aef7c8c316d47d0b61c3ab34bfb806eb5ee715ed915df6103ee3` |
| `route-04-mass-g-wave/accepted_package.md` | `cd56d00daadad6315bc7fe267754c4516617e08832f6ffc5b3c77883c7e24192` |
| `route-07-global-sign-coherence/accepted_package.md` | `a24a0fe82e19ef6a1aeb2e29c2379bb2f8793818940d43df9d87b9abd14ef1dc` |
| `route-08-common-beta-orientation/prover_result.md` | `6ecc0ae44f6841414a8a8be8077ed919f1d66d285dc66abbdc79f85660c44d6d` |
| `route-08-common-beta-orientation/falsifier_result.md` | `61ff0e77fac55e0496d08720b0f06315f9617a8cb38d347e23fbbf43445d6135` |
| `route-08-common-beta-orientation/reconciliation.md` | `851daf75acc38d2f44cad1d231a4e40d28b87348484c5d56bb88b9f5f98a950e` |

## Definition and unsquared-transfer audit

Put `x=cot(alpha)` and `y=cot(c alpha)`. The DN equations are

```text
X=C cos(beta)-m S sin(beta),
x X=S cos(beta)+(C/m)sin(beta).
```

The coefficient matrix has determinant `P/m>0`. Direct inversion gives

```text
cos(beta)=X(C+M S x)/P,
sin(beta)=m X(C x-S)/P.
```

The DD equations are

```text
Y=s cos(c beta)+m Cc sin(c beta),
-y Y=Cc cos(c beta)-(s/m)sin(c beta).
```

Their coefficient matrix has determinant `-Q/m<0`. Using
`Y=-s X/C` gives

```text
cos(c beta)=s X(M Cc y-s)/(C Q),
sin(c beta)=-m s X(Cc+s y)/(C Q).
```

These inversions divide only by `P`, `Q`, `m`, and `C`, all strictly
positive. They do not divide by any middle-layer sine or cosine, so their
zero sets are retained.

## Quadrant and modal-interval audit

Use the standard convention `atan2(y,x)`. Since `sin(alpha)>0` and
`sin(c alpha)>0`, the definitions in W12 give

```text
A,B in (0,pi),
d,g in (0,pi/2),
cot(A)=-m x,
cot(B)=-m y,
cot(d)=m u,
tan(g)=v/m.
```

For the DN direction,

```text
1+M u x+i m(x-u)=(1-i m u)(1+i m x).
```

The two factors have arguments `d-pi/2` and `A-pi/2`. The remaining
real prefactor has the sign of `X`, hence is negative. Therefore
`beta=A+d` modulo `2pi`. The exact modal interval is
`d<beta<d+pi`, while `A+d` lies strictly in that interval. This removes
the multiple and proves `beta=A+d` exactly.

For the DD direction, extracting the positive prefactor
`-s X Cc/(C Q)` leaves

```text
v-M y+i m(1+v y)=(v+i m)(1+i m y),
```

whose argument is `B-g` modulo `2pi`. The exact DD interval is
`0<c beta<pi-g`. Since `B-g` lies in `(-pi/2,pi)`, a nonpositive value
would require the representative `2pi+B-g`, which cannot lie in the modal
interval. Hence `B>g` and `c beta=B-g` exactly. Thus

```text
B-g=c(A+d)
```

has no hidden `pi` multiple.

The accepted phase lock becomes

```text
sin(B)^2/sin(A)^2=sin(g)^2/sin(d)^2.
```

All four sines are strictly positive, so the only admissible square root is

```text
sin(B)/sin(A)=sin(g)/sin(d)=sigma>0.
```

This is audited only as a necessary identity. W12 does not use the squared
lock as a converse to reconstruct common-`beta` orientation.

## Coefficient dictionary audit

The phase angles `A,B` are kept distinct from the mass coefficients
`Acoef,Bcoef,Hcoef`. With `e=1-c^2`, `k=M-1`, and

```text
JA=c^2 cot(A)^2-cot(B)^2,
Jd=c^2 cot(d)^2-cot(g)^2,
D=c^2-sigma^(-2),
```

direct substitution gives

```text
Lalpha=e-JA/M,
Bcoef/(s^2 X^2)=(e-JA)/m,
Hcoef/(C^2 s^2)=e-Jd/M.
```

The accepted B-to-H identity has final bracket

```text
M Hcoef-k e C^2 s^2=C^2 s^2(e-Jd),
```

and every other factor is positive. Hence

```text
sign(Bcoef)=sign(e-Jd).
```

The positive phase lock yields

```text
JA-e=D/sin(A)^2,
Jd-e=D/sin(d)^2.
```

It follows, with strict equivalence in every line, that

```text
Bcoef<0 iff JA>e iff Jd>e iff sigma>1/c,
Acoef<0 iff JA>M e iff D>k e sin(A)^2,
Hcoef<0 iff Jd>M e iff D>k e sin(d)^2.
```

Also, `rho=sigma^2`, `x=-cot(A)/m`, and `y=-cot(B)/m`, so

```text
q=[c sigma cos(B)-cos(A)]/[m sin(A)].
```

Finally,

```text
u=cot(d)/m,
v=m tan(g),
u^2 v^2-1=(sigma^2-1)/cos(g)^2,
M+v^2=M/cos(g)^2.
```

Substitution into the accepted formula for `E`, followed by a common
positive denominator in `H0`, gives W12 equation `(13)` exactly. Under
`Bcoef<0`, one has `sigma>1/c>1`; hence every factor in its displayed
numerator and denominator is positive and `E>0`.

## Closed-chamber and boundary audit

The identity

```text
m Bcoef/(s^2 X^2)=e+M(y^2-c^2 x^2)
```

settles both sides of `alpha=pi/2`. If `alpha<=pi/2`, then
`y>x>=0`, so the right side is strictly positive. Thus this side, including
`alpha=pi/2`, is incompatible with `Bcoef<0`. On the other side,
`Bcoef<0` forces `alpha>pi/2`, hence `x<0`. If also
`c alpha<=pi/2`, then `y>=0`, and therefore

```text
q=x-c rho y<0.
```

On the boundary `c alpha=pi/2`, one has `y=0` and still `q=x<0`.
Together with `E>0`, this gives `q-E<0`. Since `X<0`, `Dtheta>0`, and
`P>0`, the accepted factorization gives `G>0`. Since `K<0`,

```text
Xi=X^2 G-r K Dtheta>0.
```

For completeness, the exact downstream sign identities are

```text
Phi=Xi/X,
det(M)=-(gamma_2-b_0) S_KP.
```

Here `X<0`, `gamma_2-b_0>0`, and W1 gives
`sign(S_KP)=sign(Phi)`. Hence

```text
G>0 -> Xi>0 -> Phi<0 -> S_KP<0 -> det(M)>0 -> KP-DET.
```

No equality is lost in this chain.

Every complete tuple has the accepted strict sign `Bcoef<0`. If
`0<c<1/2`, then `c alpha<c pi<pi/2`. If `c=1/2`, the strict modal bound
`alpha<pi` still gives `c alpha<pi/2`. Thus every complete tuple with
`0<c<=1/2` lies strictly inside the closed chamber and satisfies KP-DET.

## Remaining acute branch audit

Any possible `q>E` tuple with `Bcoef<0` must have

```text
c>1/2,
pi/(2c)<alpha<pi.
```

Then `A,B,d,g` are all acute. For fixed `m,c,alpha`, put
`kappa=B-c A`. The common-beta identity and positive lock require

```text
g=kappa-c d,
sin(kappa-c d)/sin(d)=sigma.
```

On the full admissible interval,

```text
d/dd log[sin(kappa-c d)/sin(d)]=-c cot(g)-cot(d)<0.
```

Thus there is at most one admissible `d`; an admissible tuple supplies it,
and `g` and `beta=A+d` are unique as well.

For `P_m(t)=atan(tan(t)/m)`, direct differentiation gives

```text
P_m''(t)=2m(M-1)sin(t)cos(t)/(M cos(t)^2+sin(t)^2)^2>0.
```

With `t=pi-alpha` and `h=pi/2-theta`, W12's identities `(22)` are exact.
Differentiating its scalar common-beta residual gives

```text
C'(h)=c[P_m'(c(pi/2-h))-P_m'(h)].
```

Since `P_m'` is strictly increasing, this residual increases before
`h=c pi/[2(1+c)]` and decreases after it, with the same conclusion on any
restricted admissible subinterval. This verifies the stated unimodality.

The scalar threshold

```text
q>E implies D>k e max{sin(A)^2,sin(d)^2}
```

is not derived from uniqueness or unimodality. It remains the first open
load-bearing step. If proved, it would make `Acoef,Bcoef,Hcoef` all strictly
negative, contradicting the exact mass balance. W12 labels this implication
as open and does not use it in the closed-chamber theorem.

## Evidence and adversarial audit

W13 is labeled `EVIDENCE` at file level, calls all reported tuples
floating-point evidence, disclaims exhaustiveness and interval certification,
and states that no arbitrary finite-`m` theorem follows. Its counts and
representative tuples are unused in every strict derivation above.

Adversarial checks found no notation collision, quadrant reversal, hidden
multiple, boundary omission, equality leak, or sign-direction error. The
phase symbols `A,B` are locally separated from `Acoef,Bcoef,Hcoef`; all
divided denominators are strictly positive on the modal domain; and the
arbitrary finite-`c` target is explicitly left open.

## Structured decision

- `critical_errors`: none.
- `gaps`: none in the strict partial claims under audit.
- `decision_delta`: accept the unsquared common-beta orientation, positive
  square-root lock, coefficient dictionary, unique acute reconstruction,
  and the closed KP-DET chamber, including all complete `0<c<=1/2` tuples.
  Keep the acute scalar threshold, arbitrary finite-`c` `PHI-SIGN`, and
  arbitrary finite-`c` KP-DET open.
