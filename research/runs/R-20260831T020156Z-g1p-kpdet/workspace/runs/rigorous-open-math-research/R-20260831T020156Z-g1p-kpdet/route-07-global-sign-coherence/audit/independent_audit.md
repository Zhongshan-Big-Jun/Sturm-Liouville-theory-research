# Independent joint audit of W10 and W11

## Verdict

`PASS`

Audit ID: `AUDIT-W10-W11-GLOBAL-01`.

This verdict accepts only the exact partial claims listed below. It does not prove global `(SC)`, complete-system `G>=0`, `Xi>0`, `PHI-SIGN`, or `KP-DET`.

## Binding audit

Every bound input was hashed before mathematical use. The observed SHA-256 values were:

```text
problem_contract.md                                      67427fe00b6b7758552581cde19fdb449202b5e9ea7bf9013f6ba0a4135f3f9d
route-01-transfer-schur/derivation.md                    a96fde4cfaaf3cb83fcf416d3d7e627a5d63c4a48c2cd8a0c562e9dd8636e7d3
route-03-phi-exact/worker_result.md                      6c1bbbd871c9aef7c8c316d47d0b61c3ab34bfb806eb5ee715ed915df6103ee3
route-04-mass-g-wave/accepted_package.md                 cd56d00daadad6315bc7fe267754c4516617e08832f6ffc5b3c77883c7e24192
route-07-global-sign-coherence/prover_result.md          8f5c381223b476fcf2b2d6af7f1a51e90086c3146b45a48bdd8362ad126f11aa
route-07-global-sign-coherence/falsifier_result.md       18f2e57dfd18784527dac95d07477e89da935fff4065658f2a847af9137e4ba8
route-07-global-sign-coherence/reconciliation.md         ecaa7a9d572a72f117b7b0055c571f67f5e515eead0cd3bd3ac6b4ee92f3646d
```

All seven values exactly match the audit packet.

## W10 audit

### Unsquared phase lock

Write `M=m^2`, `k=M-1`, `u=tan(theta)`, `v=tan(c theta)`, `x=cot(alpha)`, and `y=cot(c alpha)`. The strict modal domain gives

```text
u>0, v>0, sin(alpha)>0, sin(c alpha)>0,
C>0, s>0, P=C^2+M S^2>0, Q=s^2+M Cc^2>0.
```

Thus all cotangents and denominators used below are finite. The two unsquared spectral equations and the signed band equation give, without choosing a square-root branch,

```text
Z=Xx,
Y=-sX/C,
T=-Yy=sXy/C.
```

Directly expanding the middle transfer shapes gives

```text
X^2+MZ^2=P,
Y^2+MT^2=Q.
```

Substitution therefore yields the necessary signed phase lock

```text
rho=(1+Mx^2)/(1+My^2)
   =s^2P/(C^2Q)
   =v^2(1+Mu^2)/(M+v^2)>0.
```

Here `rho` denotes W10's locally redefined `R`, not the physical density ratio. W10 uses the lock only in the forward direction and explicitly records that it loses the common-`beta` orientation if treated as a converse. No squaring-based sufficiency claim is made.

### Exact factorization of G

The unsquared transfer formulas independently give

```text
C x-S=P sin(beta)/(mX),
Cc+s y=-C Q sin(c beta)/(m s X).
```

Hence

```text
sin(beta)=mX(Cx-S)/P,
sin(c beta)=-m s X(Cc+s y)/(CQ).
```

Using `D=Z+(m-1/m)C sin(beta)` and `N=T-(m-1/m)s sin(c beta)` then gives

```text
U/X=(Mx-kSC)/P-[c s^2/C^2](My+k sCc)/Q.
```

The accepted definition of `Dtheta` also reduces exactly to

```text
Dtheta=[Pu+cQ/v]/k
      =H0/[k v(1+u^2)(1+v^2)]>0,
```

where

```text
H0=u v(1+v^2)(1+Mu^2)+c(1+u^2)(M+v^2)>0.
```

In `G/X=Dtheta(U/X)+Ttheta^2/C^2`, the coefficients of `x` and `y` are respectively

```text
M Dtheta/P,
-(M Dtheta/P)c rho.
```

Putting the remaining terms over a common denominator gives

```text
-M^2 c u(u^2v^2-1)^2
 /[v(1+v^2)(1+Mu^2)(M+v^2)]
=-(M Dtheta/P)E,
```

with

```text
E=M c u k(u^2v^2-1)^2/[(M+v^2)H0]>=0.
```

Therefore

```text
G=X(M Dtheta/P)(q-E),
q=x-c rho y.
```

Every displayed denominator is strictly positive. Since `X<0`, this proves exactly

```text
G<0 iff q>E.
```

Also, `E=0` exactly when `uv=1`. On the open angle ranges this is equivalent to `theta+c theta=pi/2`. Since the prefactor is nonzero, `G=0` exactly when `q=E`. The deterministic symbolic replay returned `PASS` for this factorization and both identities below, but the audit conclusion rests on the independent expansion above.

For the declared differential form, differentiating

```text
log([sin(c alpha)^2+M cos(c alpha)^2]
    /[sin(alpha)^2+M cos(alpha)^2])
```

and multiplying by `(1+Mx^2)/(2k)` gives `x-c rho y=q` exactly. No sign conclusion is inferred from this reformulation.

### Exact B-to-H identity and B=0

Let `e=1-c^2`. Direct expansion gives

```text
M Lalpha-k e=(1+My^2)(1-c^2 rho).
```

Using the right-hand expression for `rho` gives

```text
1-c^2 rho=[M H-k e C^2s^2]/(C^2Q).
```

Because

```text
B/(s^2X^2)=[M Lalpha-k e]/m,
```

the exact identity is

```text
mB/(s^2X^2)
=(1+My^2)[M H-k e C^2s^2]/(C^2Q).
```

All factors outside the final bracket are positive. Thus `B>=0` forces

```text
Lalpha>=k e/M>0,
H>=k e C^2s^2/M>0,
A=s^2X^2Lalpha>0.
```

This contradicts `alpha A+beta B+theta H=0`, since `alpha`, `beta`, and `theta` are positive. If `B=0`, both displayed lower bounds are equalities and remain strictly positive, so the same contradiction excludes the equality face. The complete system therefore satisfies `B<0`.

### Strength of the remaining chamber statement

The proved chamber split is exact:

```text
Lalpha<=0 implies A<=0, B<0, H>0.

Lalpha>0 implies A>0, B<0, and
H/(s^2X^2)
 =[beta(m-1/m)(1-c^2)-(alpha+m beta)Lalpha]/theta.
```

W10 does not claim that `q>E` implies `Lalpha<0` and `H<0`. It labels that implication `(SC-rem)` as the first open orientation-sensitive step. On the complete mass manifold its consequent is impossible, so `(SC-rem)` is target-strength rather than an already proved global sign theorem. If same-sign orthants are read as closed, the corresponding boundary formulation uses `Lalpha<=0` and `H<=0`; the exact mass split excludes the equality faces as well. No accepted conclusion depends on silently strengthening closed to strict signs.

## W11 audit

### Spectral, band, modal, and interior formulas

Let

```text
pi/6<h<pi/4,
c=4h/pi,
k=cos(2h),
m=(1-k)/k,
alpha=theta=pi/4,
beta=pi.
```

Then `0<k<1/2`, `2/3<c<1`, and `m>1`. With `s=sin(h)`, `d=cos(h)`, and `x=c sin(2h)`, direct substitution gives

```text
C=S=1/sqrt(2),
X=Z=D=-1/sqrt(2),
Y=s,
T=-d,
N=d(4k-3).
```

Consequently both spectral equations and `Y=-sX/C` hold identically. The modal parameters are

```text
delta_3=atan(1/m),
delta_2=pi/2+2h,
```

so

```text
delta_3<pi<delta_3+pi,
0<c beta=4h<delta_2.
```

All phase inequalities are strict. The reconstruction formula gives `0<a<b<L` because `alpha`, `m beta`, and `theta` are positive.

### Chamber and mass residual

The coefficient signs reduce to

```text
A=H=1/2-c^2s^2>k/2>0,
B=(1/2)[m(d^2-c^2s^2)+(s^2/m)(1-c^2)]>0.
```

Both terms in `B` are positive because `d^2-c^2s^2=k+(1-c^2)s^2>0`.

Independent evaluation of the exact norm expressions gives

```text
I3hat=(pi/4)m(m^2+m+1),
I2hat=h(1-k)^2(1+k)/k^3.
```

The non-`h` trigonometric terms in `I2hat` cancel by `sin(4h)=2k sin(2h)` and `sin(2h)^2=1-k^2`. Therefore

```text
Delta_M
=h(1-k)^2/k^3
 [(1+k)/2-(8h^2/pi^2)(1-k+k^2)].
```

Since `8h^2/pi^2<1/2`, its bracket is strictly greater than `k(2-k)/2>0`. Thus the whole family lies strictly on the positive side of the mass surface.

### Exact sign of G

The remaining quantities are

```text
Ttheta=(1+x)/2,
Dtheta=(1-2k+2k^2+x)/[2(1-2k)],
U=-[1+x(4k-3)]/sqrt(2).
```

Direct collection gives

```text
Dtheta[1+x(4k-3)]+2Ttheta^2
=(k-1)Q(x,k)/(1-2k),

Q(x,k)=x^2-1+k+kx(4k-3).
```

On the open interval, `1/sqrt(3)<x<sin(2h)`. Moreover,

```text
partial_x Q=2x-k(3-4k)
            >2/sqrt(3)-9/16>0.
```

Thus

```text
Q(x,k)<Q(sin(2h),k)
=k[1-k+sin(2h)(4k-3)]
<k[1-k-sin(2h)]<0.
```

Because `k-1<0` and `1-2k>0`, the collected bracket is positive and hence `G<0` throughout the exact family.

### Endpoint and W5 checks

At `h` decreasing to `pi/6`, the excluded endpoint has `m` decreasing to `1`. The modal gaps stay positive, `A`, `B`, and `H` tend to `7/18`, `Delta_M` tends to `7pi/36`, and `G` tends to negative infinity. Thus no interior strict sign is lost near the lower endpoint.

At `h` increasing to `pi/4`, one has `m` tending to infinity and `c` tending to `1`. The two limiting modal gaps tend to zero from above, corresponding to excluded mode and switch-collision faces. Also `A=H` tends to zero from above, `B` tends to `1/2+1/pi`, `Delta_M` tends to positive infinity, and `G` tends to zero from below. Hence the proof asserts strict signs only on the correct open family and does not include its degenerate endpoint.

For `h=pi/5`, the formulas specialize to

```text
c=4/5,
k=(sqrt(5)-1)/4,
m=sqrt(5),
A=H=(5+4sqrt(5))/50>0,
B>0,
G<0,
Delta_M>0.
```

Finally, the accepted W5 certificate gives `Xi<0`. From the exact identities

```text
Phi=XG-Dtheta Dalpha,
K=X[c cot(c alpha)-cot(alpha)],
Dalpha=r[c cot(c alpha)-cot(alpha)],
```

one gets `Xi=X Phi`. Since `X=-1/sqrt(2)`, `Xi<0` implies `Phi>0`. This remains a mass-defective spectral-band obstruction, not a complete-system counterexample.

## Evidence isolation and four-way audit

W11 labels its floating-point continuation table and bounded scan as `EVIDENCE`. It states residual sizes and search bounds, lists the missing interval-coverage obligations, and makes no completeness claim from the scan. Neither W10 nor the reconciliation uses numerical output to prove a universal statement.

- Definition audit: Phase variables, physical reconstruction, modal indices, mass normalization, local notation collisions, and complete versus mass-defective systems are consistent.
- Logic audit: All accepted implications have the correct direction. The phase lock is used only as a necessary identity, equality cases are retained, and all global sign claims remain open.
- Boundary audit: All divisions are safe on the strict domain. The lower and upper endpoints of the W11 family approach only excluded boundary faces, with the stated one-sided signs.
- Adversarial audit: No hidden common-`beta` converse, orientation choice, square-root branch, same-sign equality case, or computation-to-theorem step was found.

## Decision delta

Accept W10's exact phase lock, factorization, equality set, differential form, `B`-to-`H` identity, and complete-system exclusion `B<0`. Accept W11's exact open one-parameter family with strict `G<0`, strict positive coefficient chamber, and strict positive mass residual, including its W5 specialization. Keep `(SC-rem)`, global `(SC)`, complete-system `G>=0`, `Xi>0`, `PHI-SIGN`, and `KP-DET` open.

Critical errors: none.

Gaps in the claims submitted for acceptance: none.
