CANDIDATE_COMPLETE_PROOF

# Exact M3 observable and sector-determinant refutation package

## Theorem proved on the corrected branch

Let `u=R^(-1/6)` and let the exact closed residual have the locally unique real,
symmetric, band-consistent, finite-interior `n=2` INF branch described in the
two hash-bound round-001 candidate packages. Independently replaying the seed,
branch coefficients actually used, masses, Green matrices, and sector
normalizations gives, as `u->0+`,

```text
m3D-m3N = -(4/kappa^5) u^4+O(u^6),

Chi_up  = 3/2+4/(pi kappa)+O(u^2),

det Kp_odd = (128 kappa^2/pi^2) u^20+O(u^22),

det Ko = (2048 kappa^2/pi^4) u^26+O(u^28),
```

where

```text
kappa^3=18 pi-48/pi=6(3 pi^2-8)/pi,  kappa>0.
```

Consequently, for all sufficiently large finite `R`,

```text
m3D-m3N<0,
Chi_up>0,
det Kp_odd>0,
det Ko>0.
```

In `R` notation the determinant laws are

```text
det Kp_odd = (128 kappa^2/pi^2) R^(-10/3)+O(R^(-11/3)),
det Ko = (2048 kappa^2/pi^4) R^(-13/3)+O(R^(-14/3)).
```

Thus the frozen proposed exponents `R^(-7/2)` and `R^(-9/2)` are both
false. The upstream assertion `Chi_up=0` is also false on this branch. The
positive branch coefficient `Cbr(u)` is a different object and satisfies
`Cbr(0)=16/(pi kappa)>0`.

## Premises, status, and lineage

The finite branch theorem is used as an explicit conditional local hypothesis,
not as canonical trusted closure. Its two independently authored candidate
packages are:

1. `candidate_branch_proof.md`, SHA-256
   `0f609135b8d8bd2c9d830d0c9b86ef3b41454c217578a18992c76a9afad404d8`.
2. `proof_package.md`, SHA-256
   `88be4d4c2a987729706aa8c7cf7860c9ede0a53f5bdd5732019fc683f7695008`.

This route independently replays every seed and branch coefficient used below
against `scripts/_gapn2_largeR_closed.py`, SHA-256
`e357d8e447ce998020c8dadc94eb27db884dd85932d592a9b4331366f8ac13a4`.
It does not use any D-side E5 coefficient from the defective staged builder.

The exact basis, mass, Wronskian, Green, pole, and determinant conventions are
fixed in `normalization_and_symbol_map.md`. That contract is part of this
proof, not optional commentary.

## 1. Exact branch preflight and the required one-jet

Put `v=u^2` and use

```text
q=(A K-2)/u^2=q0(K)+u^2 X,
q0(K)=(18 pi-24-K^3)/(6K),
Cbr=16/(pi K)+u^2 Y.
```

At `v=0`, direct reduction of the exact closed residual gives

```text
K=kappa,  B=1/kappa,
X=X0,     Y=Y0,
```

with

```text
X0=-(kappa^6-90 pi kappa^3+120 kappa^3-1620 pi^2-3360+4320 pi)
   /(360 kappa^2),

Y0=4(pi kappa^3-96+36 pi^2)/(3 pi^2 kappa^2).
```

The round-001 third-blow-up Jacobian is nonzero, so uniqueness of the exact
analytic germ identifies every subsequently verified Taylor coefficient. The
one-jet required by the Kp determinant is

```text
K=kappa+K2 v+O(v^2),
B=1/kappa+B2 v+O(v^2),
X=X0+X2 v+O(v^2),
Y=Y0+Y2 v+O(v^2),
```

where

```text
K2=(-272 pi^2+576+81 pi^4)/(30 pi(3 pi^2-8)),

B2=-(-272 pi^2-480 pi+576+180 pi^3+81 pi^4)
   /(30 pi kappa^2(3 pi^2-8)),

X2=(-306180 pi^7-2462336 pi^4-3465216-16896 pi^2
    +3870720 pi+698880 pi^3+816480 pi^5+413424 pi^6+59049 pi^8)
   /(37800 pi^2(3 pi^2-8)^2),

Y2=2(-792 pi^2-160 pi+1536+81 pi^4)
   /(15 pi^2(3 pi^2-8)).
```

These four values are not numerical fits. Substitution into the exact scaled
map

```text
G=(E1/u^4,E2/u^4,E5/u^6,E6/u^7)
```

makes every coefficient through `v^1` exactly zero in the algebraic field

```text
Q(pi)[kappa,sqrt(2)]/(kappa^3-18 pi+48/pi, sqrt(2)^2-2).
```

The first unfilled branch term in each scaled equation is `O(v^2)`. This is an
exact recurrence replay of the one-jet. It also reconciles the two round-001
coordinate conventions because their `Delta` and `q` are literally the same
function.

## 2. Regenerated masses, the M3 difference, and Wronskians

Expanding the exact D and N formulas in the normalization contract and reducing
only by the seed cubic gives

```text
m3D-m3N = -pi^2 kappa/[9(3 pi^2-8)^2] u^4+O(u^6).
```

Since `kappa^6=36(3 pi^2-8)^2/pi^2`, the coefficient is exactly
`-4/kappa^5`. It is strictly negative.

The same direct regeneration gives, at both left switches,

```text
Wraw_1=Wraw_2=-4 pi/[3(3 pi^2-8)] u^6+O(u^8)
                 =-8/kappa^3 u^6+O(u^8).
```

Hence the absolute values in the INF diagonal term have the fixed local branch
`|Wraw_j|=-Wraw_j`. This resolves the absolute-value nonanalyticity before any
determinant expansion. The exact E5 mass relation supplies the normalization
`sqrt(ID IN)=ID sin(p1t)/sin(p1)`; no defective Pbuild mass coefficient enters.

## 3. The upstream consistency object is not the branch coefficient

The upstream addendum defines the seed-consistency candidate

```text
Chi_up=1+B K/2+3 pi/(2K)-K^2/12.
```

At the exact seed,

```text
Chi_up(0)=3/2+3 pi/(2 kappa)-kappa^2/12.
```

Using `kappa^3=18 pi-48/pi` gives

```text
kappa^2/12=3 pi/(2 kappa)-4/(pi kappa),
```

and therefore

```text
Chi_up(0)=3/2+4/(pi kappa)>0.
```

Analyticity gives `Chi_up=Chi_up(0)+O(u^2)`, so it stays positive for all
sufficiently small positive `u`. Thus `Chi_up=0` is refuted. Separately,
`Cbr(u)=16/(pi kappa)+O(u^2)>0`; confusing these two symbols would reverse the
meaning of the upstream statement.

## 4. Ordinary and reduced Green normalization

For each boundary condition, assembling the three exact interval
Dirichlet-to-Neumann maps gives the two-by-two matrices `A_D(z)` and `A_N(z)`
in the normalization contract. The derivative jump equation at a switch is
exactly `A(z)g=f`, hence the switch Green matrix is `A(z)^(-1)` with the source
spectral convention `1/(lambda-z^2)`.

At a simple half-eigenvalue `k^2`, write `delta=z/k-1` and

```text
A(z)=A0+A1 delta+A2 delta^2+O(delta^3).
```

For a symmetric two-by-two matrix, coefficient expansion of `adj(A)/det(A)`
gives

```text
D1=[delta] det A,
D2=[delta^2] det A,
N0=adj(A0),  N1=[delta] adj(A),
Lminus=N0/D1,
L0=N1/D1-N0 D2/D1^2.
```

On the other hand,

```text
1/(k^2-z^2)=-1/(2 k^2 delta)+1/(4 k^2)+O(delta).
```

Matching the eigenprojection residue and constant part proves
`Gt=L0+Lminus/2`. This is an exact derivation of the regularized-resolvent
normalization, independent of the old finite-difference code. The replay
script differentiates the cotangent, cosecant, and tangent stiffness entries
exactly to form `A0,A1,A2`.

## 5. Kp_odd coefficient and refutation of R^(-7/2)

In the exact orthonormal convention the first entry orders are

```text
(Kp_odd)11=-6 kappa(3 pi^2-8)/pi^2 u^4+O(u^6),
(Kp_odd)12= 4 kappa^2/pi u^8+O(u^10),
(Kp_odd)22=-16/pi u^12+O(u^14).
```

The apparent `u^16` determinant coefficient cancels by the seed cubic. After
the corrected `X0,Y0` are inserted, the entire `u^18` coefficient also
cancels. Inserting the exact branch one-jet above gives

```text
[u^20] det Kp_odd=128 kappa^2/pi^2
                   =768(3 pi^2-8)/(pi^3 kappa)>0.
```

For the omitted-jet audit, let `Dp=diag(u^2,u^6)`. Direct coefficient
extraction gives

```text
Kp_odd=Dp H(v) Dp,
```

where `H` is analytic in `v` after the removable phase factors are extracted.
The coefficient of `v^0` in `det H` is the structural leading rank-one
cancellation. Its coefficient of `v^1` uses only the endpoint values
`kappa,B0,X0,Y0` and is zero. Its coefficient of `v^2` uses the displayed
one-jet and no later branch coefficient: in the blow-up coordinates, every
unfilled `v^2` coefficient enters the reduced phases only one order later, and
the structural `v^0` determinant is identically zero. The replay performs this
coefficient bookkeeping before determinant promotion. Thus the `u^20`
coefficient is not an artifact of setting an unknown branch coefficient to
zero.

Because `R^(-7/2)=u^21`, the claimed law also violates the exact even-`u`
parity of this determinant. The correct first term is the positive `u^20`
term above.

## 6. Ko coefficient and refutation of R^(-9/2)

The regularized-sector matrix begins

```text
Ko=-(16/pi) u^12 [[1,2],[2,4]]+O(u^14).
```

The `u^24` determinant vanishes because this leading matrix has rank one. Exact
coefficient extraction at the next even order gives

```text
[u^26] det Ko=2048 kappa^2/pi^4>0.
```

Equivalently, `Ko=u^12 M(v)` with analytic `M`, `det M(0)=0`, and
`[v]det M=2048 kappa^2/pi^4`. Therefore no uncomputed branch coefficient can
enter this first nonzero term; such a coefficient begins at `v^2` in the
branch, while this determinant coefficient is only first order in `v`.

Because `R^(-9/2)=u^27`, the proposed law again contradicts exact even parity.
The correct first term is the positive `u^26` term above.

## 7. Exact computation and adversarial evidence separation

`exact_algebraic_sector_replay.py` is the authoritative exact certificate. It
hash-checks the closed residual, implements the two algebraic quotient
relations, verifies the branch one-jet in all four scaled residuals, rebuilds
both masses and both kinds of Green matrix, and prints the first nonzero
coefficients. Its arithmetic contains no decimal numbers.

`high_precision_adversarial_check.py` is labeled evidence only. At exact
closed-system roots found with 100 digits, it compares the delta-jet finite
part with a direct pole-subtracted limit and evaluates determinant ratios. The
agreement is a transcription and sign check, never a premise of this proof.

## 8. Boundary cases and scope audit

1. `kappa>0` because `18 pi-48/pi>0`; the `K->0` and `K->infinity` charts are
   excluded by the branch contract.
2. `sin(p1)->1`, `sin(p3),cos(p3)->1/sqrt(2)`, and
   `sin(p2)/u->kappa/2`, so every divided phase factor used above has a
   nonzero analytic limit.
3. `ID->pi/(4 kappa^3)>0`; E5 then keeps both normalization factors positive.
4. The Wronskians are strictly negative for small positive `u`, so the INF
   absolute-value branch is fixed.
5. Both mirror bases are orthonormal. The only Kp basis change is conjugation
   by `diag(1,-1)`, whose determinant square is one.
6. The reduced Green formula removes the simple spectral pole before `u=0` is
   taken. No singular inverse is silently evaluated at the endpoint.
7. The finite-`R` remainder and sign bridge is proved separately in
   `finite_R_remainder_and_signs.md` and is part of this package.
8. No conclusion propagates to M1, M2, SUP, `n>=3`, general `(G1')`, global
   reflection symmetry, or another singular geometry.

## Conclusion and epistemic status

The exact full formulas refute both frozen determinant exponents and the
upstream zero-consistency assertion, while supplying the correct alternative
scales, coefficients, normalizations, signs, and finite-branch interpretation.
This is a `CANDIDATE_COMPLETE_PROOF` package for a route result with machine
status `refuted`. Independent mathematics review and deterministic Blueprint
integration remain required before any canonical promotion.
