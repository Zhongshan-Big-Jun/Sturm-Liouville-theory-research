CANDIDATE_COMPLETE_PROOF

# R10 min `n=2`, `mu=2`: independent full-interface sign audit

## 0. Scope and calibrated result

This route binds the canonical snapshot

```text
context_id: CTX-DEFAULT
blueprint_sha256:
  sha256:002a9f58d6ac878bd8620c65fa33d7110230372333c3f250c2ef47347af7af48
inventory_sha256:
  sha256:b6286574edbcb70ad22e5c6758a81f00dd01572c0764b8816be23cb6b166fb6f
```

and restricts the open min complementary-inertia problem to `n=2` and
`mu=2`.  It independently audits the exact full-momentum elimination in
`routes/r9_min_complementary/symbolic_split_gap_mu2.py` and proves the one
remaining residual polynomial positive by a rational tensor-Bernstein
certificate.  Consequently every admissible physical min three-cell word
with `mu=2` has

```text
H=beta_R+beta_L-abs(K_2)>0.                           (0.1)
```

No reflection symmetry or equality of the two positive-cell phases is
assumed.  The result does not cover `mu!=2` or `n>2` and hence does not close
the general min or O3a obligation.  The proof is candidate-complete pending
independent package audit.

Allowed trusted inputs are the R6 cell phase theorem, the R7 physical
continuant orientation, and the R8 sharp internal phase separation.  No
finite sample, weak gamma-interface witness, or unintegrated assertion is
used as a premise.

## 1. Exact scalar target and split certificate

For a positive-negative-positive min word, the double Schur reduction gives

```text
H=beta_R+beta_L-w,                 w=abs(K_2)>0.      (1.1)
```

On the middle negative cell write its amplitude ratio as `z_2=-B`, `B>0`,
and its positive inward switch factors as

```text
G=-g_2>0,                  J=-h_2>0.
```

The physical gamma values are

```text
gamma_2=-rG,               gamma_3=rJ,               r=sqrt(R)>1,
```

so the canonical scalar weight

```text
x_*=(gamma_3-gamma_2)/w=r(G+J)/w>0                  (1.2)
```

obeys

```text
H x_*=(beta_R x_*+gamma_2)+(beta_L x_*-gamma_3).
                                                               (1.3)
```

Thus it is enough to prove both strict split inequalities

```text
E_L=beta_R x_*+gamma_2>0,
E_R=beta_L x_*-gamma_3>0.                            (1.4)
```

This is stronger than (0.1), but the full interface equations make the two
splits instances of the same local polynomial.

## 2. Full two-momentum elimination

At a positive-negative interface put

```text
x=tan(theta_+/2),       y=tan(theta_-/2),       r=sqrt(R).
```

For `mu=2`, R8 gives the strict phase chamber

```text
r>1,               0<x<1/sqrt(3)<y<1.               (2.1)
```

Solving both independent `U_t` and `V_t` matching equations gives the
positive ratio `a` and negative ratio `b`:

```text
D_a=3rx^3y^2-rx^3-3rxy^2+rx+x^4y+2x^2y^3-4x^2y+y,
N_b=2rx^3y^2+rxy^4-4rxy^2+rx
    +3x^2y^3-3x^2y-y^3+y,

a=-y(x-y)(x+y)(1+x^2)/D_a,
b=N_b/[rx(x-y)(x+y)(1+y^2)].                        (2.2)
```

Since `0<x<y`, the physical ratio signs are exactly

```text
D_a>0,                       N_b>0.                  (2.3)
```

The exact replay script checks both momentum equations by rational-function
substitution.  Time reversal gives the right-interface ratios `1/a,1/b`,
without identifying the actual left and right phases of an asymmetric word.

After substituting (2.2), the left and time-reversed right split numerators
have the same primitive polynomial `P(x,y,r)`, with

```text
degree_(x,y,r) P=(16,12,6),      terms(P)=228,
sha256(expanded SymPy string)=
906da32475eb75bdcac45a5e04b490661722d9d356717301c5915c2c125c8591.
                                                               (2.4)
```

More exactly, the pre-elimination positive prefactors reduce (1.4) to

```text
N_L=P/[x^3(1+x^2)(1+y^2)^2D_a^3],

N_R=-rP/[x^2y^2(x-y)(x+y)(1+x^2)^3(1+y^2)N_bD_a].  (2.5)
```

Under (2.1)--(2.3), every denominator sign in (2.5) is explicit and both
`N_L,N_R` have the sign of `P`.  It remains only to prove `P>0`.

## 3. Exact Bernstein certificate for `P>0`

Set

```text
X=x^2,       Y=y^2,
kappa=r*x*(3Y-1)/[y*(1-3X)].                         (3.1)
```

The decomposition

```text
N_b=y(1-y^2)(1-3X)
    -rx[(1-y^2)(3Y-1)+2Y(Y-X)]                      (3.2)
```

together with `N_b>0` proves

```text
0<kappa<1.                                           (3.3)
```

Indeed all factors in (3.1) are positive, and dropping the positive last
term in the bracket of (3.2) gives
`rx(3Y-1)<y(1-3X)`.

Substitute

```text
r=kappa*y*(1-3X)/[x*(3Y-1)]                         (3.4)
```

into `P`.  Exact cancellation gives

```text
P = y^4 Q(X,Y,kappa)/(3Y-1)^2,                      (3.5)
```

where `Q` is a rational polynomial of degree `(10,6,6)`.  Now map the closed
box containing the physical domain to the unit cube:

```text
X=(1-A)/3,          Y=(1+2B)/3,          kappa=C,
0<=A,B,C<=1.                                           (3.6)
```

The exact tensor Bernstein expansion of
`Q((1-A)/3,(1+2B)/3,C)` at multi-degree `(10,6,6)` has

```text
539 coefficients total,
387 strictly positive,
152 zero,
0 negative.                                         (3.7)
```

The ordered coefficient table has SHA-256

```text
bfbe12429a0b1b4469b61f6aca7996ade58c86d76d5422b3a8cc5a0d1a7794bc.
                                                               (3.8)
```

All arithmetic in (3.5)--(3.8) is over `QQ`.  The smallest positive
coefficient is exactly `1024/7381125`.  The implementation independently
reconstructs the polynomial from its Bernstein coefficients at
`(A,B,C)=(2/5,3/7,4/9)` and obtains the exact positive value

```text
235638343593672704/1831743228779296875.              (3.9)
```

For every physical point, (2.1) and (3.3) put `A,B,C` strictly inside
`(0,1)^3`.  Every tensor Bernstein basis function is then strictly positive.
Because every coefficient is nonnegative and 387 are positive, their sum is
strictly positive.  Therefore

```text
Q(X,Y,kappa)>0,             hence P(x,y,r)>0.         (3.10)
```

This strictness argument is important: zero coefficients do not permit an
interior equality because no Bernstein basis function vanishes in the open
cube.

## 4. Chain back to the physical scalar

Apply (3.10) to the actual left interface.  Equations (2.5) and the positive
prefactor relation give `E_L>0`.  Apply the same local result after time
reversal to the actual right interface; this does not require equal phases
and gives `E_R>0`.  Then (1.3)--(1.4) yield

```text
H x_*=E_L+E_R>0.
```

Since `x_*>0`, (0.1) follows.  By the exact dual inertia identity
`n_-(M)=n_+(H)`, the scalar `H>0` gives `n_-(M)=1=n-1` for this restricted
`n=2,mu=2` min problem.

## 5. Boundary and adversarial audit

* `R=1` is excluded; `r>1` is part of the target domain.
* Phase equality `x=1/sqrt(3)` or `y=1/sqrt(3)` would be zero energy and is
  excluded by the strict R8 phase theorem.
* `y=1` corresponds to `theta_- = pi/2=pi/mu`; the physical phase upper
  bound is strict.
* `kappa=0,1` are not physical interior points; the Bernstein certificate is
  nevertheless nonnegative on the larger closed box and strict inside it.
* `D_a=0` or `N_b=0` are singular ratio/interface boundaries and are excluded
  by (2.3).
* The two positive-cell phases may differ.  Time reversal transports the
  same local theorem to the second interface rather than imposing
  palindromy.
* Common negative energy and strict first crossing enter through the R8
  phase chamber and physical ratio/branch hypotheses.  The algebra never
  replaces the two independent momentum equations by their gamma
  combination.
* The proof is special to `mu=2`.  No continuity-in-`mu` or finite-sample
  extrapolation is asserted.

## 6. Reproducibility and provenance

Replay from the project root:

```text
E:\\ai_auto_solve\\O3a_blueprint_v22_research_20260808\\.venv\\Scripts\\python.exe runs\\R-20260812T165103Z-mpo3a-cont4\\routes\\r9_min_complementary\\symbolic_split_gap_mu2.py

E:\\ai_auto_solve\\O3a_blueprint_v22_research_20260808\\.venv\\Scripts\\python.exe runs\\R-20260812T165103Z-mpo3a-cont4\\routes\\r10_min_full_interface\\independent_bernstein_audit.py
```

The second script uses Python 3.12.13 and SymPy 1.14.0, reconstructs `P`,
checks (3.5), computes all 539 exact coefficients, rejects any negative
coefficient, and checks an independent rational reconstruction.  Its JSON
record is `independent_bernstein_audit.json`.

Human contribution: problem scope and continuation request.  Model
contribution: independent parameter/sign audit, coarser-box Bernstein
certificate, strictness proof, and physical chain.  Tool contribution: exact
`QQ` expansion, hashing, coefficient enumeration, and replay checks.

```text
exact result: min n=2, mu=2 physical H>0
general mu>1 result: OPEN
general n result: OPEN
physical counterexample: NONE
novelty_status: unknown
confidence_semantic_fidelity: high
confidence_exact_computation: high
confidence_proof_correctness: medium-high pending independent audit
confidence_general_target_completeness: low
confidence_reproducibility: high
```
