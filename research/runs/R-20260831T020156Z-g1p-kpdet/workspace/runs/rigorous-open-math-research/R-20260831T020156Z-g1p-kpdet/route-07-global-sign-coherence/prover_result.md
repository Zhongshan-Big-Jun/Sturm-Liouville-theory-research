PARTIAL

# Global sign-coherence prover result

## Input audit

The five packet bindings were verified before use. The observed SHA-256 values were exactly

```text
problem_contract.md                                      67427fe00b6b7758552581cde19fdb449202b5e9ea7bf9013f6ba0a4135f3f9d
route-01-transfer-schur/derivation.md                    a96fde4cfaaf3cb83fcf416d3d7e627a5d63c4a48c2cd8a0c562e9dd8636e7d3
route-03-phi-exact/worker_result.md                      6c1bbbd871c9aef7c8c316d47d0b61c3ab34bfb806eb5ee715ed915df6103ee3
route-04-mass-g-wave/accepted_package.md                 cd56d00daadad6315bc7fe267754c4516617e08832f6ffc5b3c77883c7e24192
route-06-alpha-pi/accepted_package.md                    1177c02076694ebf95ce912719846b3143e5e9099614e66492586296ae7526ba
```

## W5 consistency test

STRICT. The accepted mass-defective W5 point does not refute `(SC)`. At

```text
m=sqrt(5), c=4/5, alpha=theta=pi/4, beta=pi,
```

one has, using `sin(pi/5)^2=(5-sqrt(5))/8`,

```text
Lalpha=18/25+2sqrt(5)/5>0,
m Lalpha-(m-1/m)(1-c^2)=2+54sqrt(5)/125>0,
H=(5+4sqrt(5))/50>0.
```

Since `s^2 X^2>0`, this gives `A>0`, `B>0`, and `H>0`. The accepted package proves `G<0` at this point. Hence W5 lies in the positive same-sign orthant, as `(SC)` predicts. Its positive mass residual remains the reason it is not a complete-system counterexample.

## STRICT theorem 1. Exact phase lock

Put

```text
M=m^2, k=M-1,
u=tan(theta), v=tan(c theta),
x=cot(alpha), y=cot(c alpha),
P=C^2+M S^2=(1+M u^2)/(1+u^2),
Q=s^2+M Cc^2=(M+v^2)/(1+v^2).
```

All these expressions are finite on the strict modal domain, and `u,v,P,Q` are positive. The two spectral equations and the band equation give

```text
Z=X x,
T=s X y/C,
Y=-s X/C.
```

Direct expansion of the middle-layer transfer formulas gives the energy identities

```text
X^2+M Z^2=P,
Y^2+M T^2=Q.
```

Consequently the complete spectral-band system satisfies the exact, signed-lossless phase lock

```text
R:=(1+M x^2)/(1+M y^2)
  =s^2 P/(C^2 Q)
  =v^2(1+M u^2)/(M+v^2)>0.                 (PL)
```

No mass equation and no numerical premise is used here.

## STRICT theorem 2. Denominator-safe factorization of G

Define

```text
H0=u v(1+v^2)(1+M u^2)+c(1+u^2)(M+v^2)>0,

E=M c u k(u^2 v^2-1)^2/[(M+v^2)H0]>=0,

q=x-c R y.
```

Then every admissible spectral-band tuple satisfies

```text
G=X [M Dtheta/P] (q-E).                    (F)
```

Proof. Transfer inversion gives

```text
sin(beta)=m X(C x-S)/P,
sin(c beta)=-m s X(Cc+s y)/(C Q).
```

Using `D=Z+(m-1/m)C sin(beta)` and `N=T-(m-1/m)s sin(c beta)` yields

```text
U/X=(M x-k S C)/P
    -[c s^2/C^2](M y+k s Cc)/Q.            (1)
```

Also

```text
Dtheta=[P u+c Q/v]/k>0.                    (2)
```

Substitute `(1)` and `(2)` into

```text
G/X=Dtheta U/X+Ttheta^2/C^2.
```

Collecting the coefficients of `x` and `y` gives `(F)`. The remaining constant term is exactly `-M Dtheta E/P`. The symbolic polynomial identity is independently replayable in `prover/verify_factorization.py`.

Because `X<0`, `M Dtheta/P>0`, and `E>=0`, the exact sign consequence is

```text
G<0 iff q>E>=0.                            (GS)
```

There is also a useful differential form

```text
q=(1+M x^2)/(2k) d/dalpha log(
    [sin(c alpha)^2+M cos(c alpha)^2]
    /[sin(alpha)^2+M cos(alpha)^2]).        (D)
```

Thus a negative `G` requires a strictly positive logarithmic slope, with the explicit positive defect `E` still to be overcome.

## Denominator and equality audit

STRICT.

- `k>0` because `m>1`.
- `u,v>0` because `0<theta<pi/2` and `0<c theta<pi/2`.
- `P,Q,H0,Dtheta` are strictly positive sums or accepted positive factors.
- `sin(alpha)` and `sin(c alpha)` are positive, so `x` and `y` are finite. They may vanish, and no division by either one occurs.
- `C,s,X` are nonzero on the strict domain. The only divisions inherited from the accepted system are therefore safe.
- No division by `sin(beta)`, `cos(beta)`, `sin(c beta)`, or `cos(c beta)` occurs. Their zero sets remain included.
- `E=0` exactly when `u v=1`, equivalently `theta+c theta=pi/2` on the present open angle ranges.
- Since `X M Dtheta/P` is nonzero, `G=0` holds exactly when `q=E`. No equality case is introduced or discarded.

## STRICT theorem 3. Exact B-to-H identity and exclusion of the complete B>=0 chamber

Let `e=1-c^2>0`. Since

```text
Lalpha=1+y^2-c^2(1+x^2),
```

the left side of `(PL)` gives

```text
M Lalpha-k e=(1+M y^2)(1-c^2 R).           (3)
```

The right side of `(PL)` gives

```text
1-c^2 R=[M H-k e C^2 s^2]/(C^2 Q).         (4)
```

Combining `(3)` and `(4)`, and using

```text
B=s^2 X^2[m Lalpha-(m-1/m)e],
```

proves the exact identity

```text
m B/(s^2 X^2)
=(1+M y^2)[M H-k e C^2 s^2]/(C^2 Q).       (BH)
```

All factors outside the last bracket are strictly positive. Hence

```text
B>=0 implies
Lalpha>=k e/M>0,
H>=k e C^2 s^2/M>0.
```

In particular `A=s^2 X^2 Lalpha>0`. The complete mass identity

```text
alpha A+beta B+theta H=0
```

is then impossible because `alpha,beta,theta>0`. Therefore every complete admissible tuple satisfies the new strict chamber exclusion

```text
B<0.                                           (C-B)
```

The equality face `B=0` is also excluded, not lost: `(BH)` forces `H=k e C^2 s^2/M>0`, while the left formula forces `Lalpha=k e/M>0`, so the mass sum is still strictly positive.

## Exact chamber reduction

STRICT. On the complete system, `(C-B)` leaves only the following algebraic possibilities.

```text
Lalpha<=0: A<=0, B<0, and the mass balance forces H>0.

Lalpha>0:  A>0, B<0, and
H/(s^2 X^2)=[beta(m-1/m)e-(alpha+m beta)Lalpha]/theta.
```

Thus the whole `B>=0` chamber is closed. Any complete counterexample with `G<0` must lie in `B<0` and must satisfy `(GS)`. The original `(SC)` is now equivalent, on this remaining chamber, to proving

```text
q>E and B<0 imply Lalpha<0 and H<0.          (SC-rem)
```

Together with the mass balance, `(SC-rem)` would be contradictory and would prove `G>=0` globally.

## EVIDENCE and route audit

EVIDENCE ONLY. The deterministic scripts under `prover/` were used only as falsification probes.

- `search_sign.py` found no spectral-band root with `G<0` and mixed `(A,B,H)` in its fixed-seed sample. This does not prove `(SC)`.
- The weaker phase lock `(PL)` alone is insufficient to prove `(SC-rem)`. Fixed-parameter lock-only probes near `m=10`, `c=0.95` produce mixed-sign points with `q>E`; these points were not shown to satisfy the common middle phase `beta`, so they are not counterexamples to `(SC)`.
- `verify_factorization.py` performs exact symbolic numerator checks for `(F)`, `(3)`, and `(4)` and returns three `PASS` lines. This verifies algebraic identities, not the global inequality.

The failure mechanism is now precise: squaring the two transfer energy identities retains `(PL)` but loses the common-`beta` orientation data. That lost orientation is load-bearing for any proof of `(SC-rem)`.

## OPEN first unresolved step

Prove the one-dimensional orientation-sensitive monotonicity statement `(SC-rem)` using the unsquared common-`beta` transfer formulas, or prove directly on the complete mass manifold that

```text
q<=E.                                           (OPEN)
```

By `(F)`, the latter is exactly sufficient for `G>=0`. The required next argument must use the fact that the two reconstructed angles are the same `beta` and `c beta`; `(PL)`, denominator signs, and modal inequalities alone have not supplied it. Global `(SC)`, global `G>=0`, `Xi>0`, `Phi<0`, and KP-DET therefore remain open.

decision_delta: Derived the exact factorization `G=X(M Dtheta/P)(q-E)`, proved the exact B-to-H identity and strict complete-system exclusion `B<0`, and reduced the remaining global decision to the orientation-sensitive scalar implication `(SC-rem)`; the common-beta orientation, not mass or denominator control, is the first unresolved mechanism.
