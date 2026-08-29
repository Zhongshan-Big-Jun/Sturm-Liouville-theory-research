CANDIDATE_COMPLETE_PROOF

# Corrected finite-seed theorem and transseries classification

## Binding and scope

- Run: `R-20260825T100044Z-b4-m3-blueprint`.
- Round/route: `round-001/route-002-noninteger-balance-classification`.
- Target node: `CLM-SL-B4-M3-TARGET-V1`.
- Route contract hash: `sha256:ae8ae2501857e2c89efd144589fe16e254d2acac5c503ace239a0296e00f7885`.
- Author/researcher: `transseries-researcher`.
- Formalization: off.
- Scope: the real symmetric `n=2` INF exact system `E1=E2=E5=E6=0`
  in the finite, nonzero, interior limiting geometry. No M1, M2, general
  `(G1')`, SUP, `n>=3`, global symmetry, observable, or determinant conclusion
  is asserted.

## Theorem proved by the candidate package

Let `u=R^(-1/6)` and use the frozen variables

```text
k2=K(u)u,
k3=K(u)u+C(u)u^5,
p1=pi/2+A(u)u^2,
p3=pi/4+B(u)u^2.
```

There are `u0>0`, `M<infinity`, and unique real-analytic functions of
`v=u^2`, denoted `K(v),A(v),B(v),C(v)`, for `|v|<u0^2`, such that all four
original exact residuals vanish and

```text
K(0)=K0=(18*pi-48/pi)^(1/3),
A(0)=A0=2/K0,
B(0)=B0=1/K0,
C(0)=C0=16/(pi*K0).
```

For `0<u<u0`, after increasing `M` if necessary,

```text
|K-K0|+|A-A0|+|B-B0|+|C-C0| <= M*u^2,
|k2-K0*u| <= M*u^3,
|(k3-k2)-C0*u^5| <= M*u^7,
|p1-(pi/2+A0*u^2)| <= M*u^4,
|p3-(pi/4+B0*u^2)| <= M*u^4.
```

Shrinking `u0` preserves the real phase box, positive half-widths, all mass
denominators, `K>0`, and `C>0`; hence `k3>k2`. Under the frozen contract's
equation-to-branch map, these exact roots form the finite-`R`, real,
symmetric, band-consistent `n=2` INF branch for every `R>u0^(-6)`.

Every exact zero branch with the same finite nonzero interior limits is this
analytic germ. Thus no distinct rational-Puiseux, logarithmic,
inverse-logarithmic, mixed power-log, odd-power, or flat correction branch
exists in the admitted class.

Numerically, only for orientation,

```text
K0=3.4557641714085382002415793930...,
B0=0.2893715978287977476174814028...,
C0=1.4737574459153001416014209050...,
q0=(8/pi-4)/K0=-0.4206076683575409196692151587...,
```

where `q=(A*K-2)/u^2`.

## Exact residual and symbol map

The bound closed source uses

```text
eps=u^3,
r=k3/k2=1+C*u^4/K,
p1t=r*p1, p3t=r*p3,
p2=K*u/2-u^3*(p1+p3), p2t=r*p2.
```

`E1,E2` are the two exact half-interval spectral equations, `E5` is the exact
mass/band equation at the first switch, and `E6` is the exact second band
equation. The proof uses the formulas in `_gapn2_largeR_closed.py` directly.
The staged `_gapn2_largeR_Pbuild.py` E5 coefficients are not used because the
D-side half-mass normalization fails the audit in `normalization_audit.md`.

## Imported theorem contract

The only general theorem used is the real-analytic implicit-function theorem:
if a real-analytic map `F(t,x)` vanishes at `(0,x0)` and `D_xF(0,x0)` is
invertible, there is a neighborhood of zero with one real-analytic solution
`x(t)` near `x0`, and every nearby zero belongs to that graph. This theorem is
used twice. No numerical existence theorem is used.

## Ordered proof

### 1. Analytic blow-up and parity

Put `v=u^2` and

```text
q=(A*K-2)/v,  equivalently A=(2+v*q)/K.
```

Near `K=K0>0`, `p1=pi/2`, and `p3=pi/4`, the three phase denominators in the
closed system are nonzero. Direct inspection under `u -> -u` shows that
`E1,E2,E5` are even and `E6` is odd. The exact numerators and the `q` blow-up
give analytic quotients

```text
F1=E1/u^2, F2=E2/u^2, F6=E6/u^5, F5=E5/u^4
```

as functions of `(v,K,B,q,C)`. The apparent negative powers in the mass
formulas cancel: `cos(p1)=O(u^2)`, `eps/k2=O(u^2)`, and the D and N mass
numerators have the exact powers replayed in `corrected_bounded_general.py`.

### 2. First Newton face

Exact expansion of the original residual gives at `v=0`

```text
F1=-sqrt(2)*(K^3+6*K*q-18*pi+24)/(24*K),
F2= sqrt(2)*(3*pi*C*K+K^3+6*K*q-18*pi-24)/(24*K),
F6=-(3*pi*C*K+2*K^3+12*K*q-36*pi)/(12*K).
```

The corrected `F5` face vanishes after `F1=F2=0`; there is no hard odd term.
The first two equations give

```text
q0(K)=(18*pi-24-K^3)/(6*K),
C0(K)=16/(pi*K),
```

and

```text
det d(F1,F2)/d(q,C)=-pi/16 != 0.
```

The first analytic implicit-function step therefore gives unique analytic
functions `q=Q(v,K,B)` and `C=D(v,K,B)` solving the exact `F1=F2=0` near the
first-face manifold.

### 3. Secondary Newton face

Substitute `Q,D` into `F6,F5`. Both reduced functions vanish identically at
`v=0`, so analyticity factors one additional `v`. Their exact quotients at
`v=0` are

```text
H6=8*(B*K-1)/K^2,
H5=2*(6*pi^2*B*K+pi*K^3-24*pi^2+48)/(3*pi*K^6).
```

The full chain-rule elimination, including the required second-face
corrections to `q,C`, is printed by `corrected_bounded_general.py`. It gives

```text
q2=-(1440*B*K+K^6-90*pi*K^3+120*K^3
     -1620*pi^2-4800+4320*pi)/(360*K^2),
C2=4*(pi*K^3-96+36*pi^2)/(3*pi^2*K^2),
```

and the displayed `H6,H5`; no term of the same or lower valuation is omitted.

### 4. Exact seed and rank

`H6=0` gives `B*K=1`. Substitution in `H5=0` gives

```text
K^3=18*pi-48/pi.
```

The radicand is positive, so there is exactly one positive `K0`; the other
real-domain possibility is absent because the cube map is strictly
increasing. At `(K0,B0=1/K0)`, exact differentiation gives

```text
det d(H6,H5)/d(B,K)=16/K0^5 != 0.
```

The second analytic implicit-function step gives unique analytic
`K(v),B(v)`. Composing with `Q,D` and `A=(2+v*q)/K` gives the asserted exact
branch and solves all four original residuals, not a truncation.

### 5. Remainder and finite-R bridge

Analyticity gives a closed smaller neighborhood and a finite derivative bound,
hence the quantified `M*v` bound on `(K,A,B,C)` by the mean-value theorem. The
four original-variable estimates follow by direct substitution. With
`v=R^(-1/3)`, the theorem applies to every finite `R>u0^(-6)`.

At the seed `K0,A0,B0,C0` are positive. Continuity permits a smaller `u0` for
which

```text
K>0, C>0,
p1,p1t in (pi/3,2*pi/3),
p3,p3t in (pi/6,pi/3),
p2,p2t>0,
sin(p3), cos(p3t), sin(p1t)>0.
```

The half-widths represented by `u^3*p1/k2`, `u^3*p3/k2`, and
`p2/k2=1/2-u^3*(p1+p3)/k2` are positive. Symmetry is built into the half-map,
and `E5=E6=0` are the exact band equations. The fixed phase box and
`k3>k2` select the intended adjacent `n=2` INF component and prevent local
branch switching. This is an exact finite-`R` correspondence, while the
continuation table is used only as an adversarial numerical check.

### 6. Exhaustion of noninteger and logarithmic corrections

Any exact branch in the admitted class eventually enters the two IFT
uniqueness neighborhoods. It must therefore equal the analytic `v` germ.
This argument does not assume the branch has a transseries, so it covers all
listed Puiseux/log/inverse-log/mixed scales and flat corrections at once.
Since the germ is analytic in `v=u^2`, all odd `u` coefficients vanish.

An additional exact chart with `p3->theta` and `0<theta<pi/2` checks a possible
`B~u^(-2)` hiding transformation. The leading `E2` and `E6` equations give

```text
C=8/(pi*K*sin(theta)*cos(theta)),
C=16*tan(theta)/(pi*K),
```

so `sin(theta)^2=1/2` and the interior phase box forces `theta=pi/4`.

## Boundary and adversarial audit

- `K0 -> 0`: not divided away; it is a separate denominator-singular,
  degenerate attractor and not the finite seed proved here.
- `K0 -> infinity`: outside the finite seed chart and not used.
- `u=0` versus finite `u`: the two analytic blow-ups produce exact roots for
  every `0<u<u0`, not merely a formal point at infinity.
- even-only/odd correction: exact parity and both nonzero Jacobians prove the
  branch is even in `u`; the old odd-forcing identity is refuted by the mass
  audit.
- fractional/log/mixed/flat terms: local uniqueness excludes them as distinct
  branches in the admitted class.
- changed `p3` leading phase: the interior chart returns `pi/4`; endpoint
  phase limits are denominator-singular separate geometries.
- nonunit limiting `k3/k2`: a different spectral limiting geometry, not a
  coordinate representation of this branch and not globally classified.
- denominators: positive in the selected phase box.
- realness, positive widths, symmetry, band consistency: preserved after
  shrinking `u0`.
- multiple root or rank change: the two exact determinants are nonzero.
- spurious truncated roots: existence and uniqueness are for the original
  closed residual; the corrected truncations only compute its derivatives.
- branch switching: excluded inside the IFT neighborhood and fixed phase box.

## Proof, exact computation, and evidence separation

- Proof: the parity/divisibility argument, the two IFT applications, exact
  seed elimination, uniqueness, remainder, and continuity bridge.
- Exact formal computation: coefficient extraction and simplification in
  `corrected_bounded_general.py`, `corrected_seed_face.py`, and
  `seed_rank_check.py` under SymPy 1.13.1.
- Evidence only: the 100-digit residual limits in
  `high_precision_residual_check.py` and the 270-row bound continuation table.
- Refuted reused identity: the staged P builder's hard `E5_5` and forced odd
  correction, for the exact line-level reason in `normalization_audit.md`.

## Obligation map

| Obligation | Discharge |
| --- | --- |
| finite nonzero seed | exact radical and positive values above |
| all four exact equations | two-stage analytic IFT on original residual |
| Newton/Puiseux/log/mixed classification | local analytic uniqueness in `v` |
| no omitted equal/lower valuation | exact two-face quotient construction |
| seed nondegeneracy | determinants `-pi/16` and `16/K0^5` |
| controlled remainder | quantified `M*u^2` and original-variable bounds |
| all sufficiently large finite `R` | `R>u0^(-6)` |
| branch selection and positivity | fixed phase box, widths, signs, uniqueness |
| denominator audit | strictly positive phase denominators |
| boundary distinctions | listed above without global overclaim |

`unresolved_obligations` for this route theorem: `[]`.

Independent proof audit, deterministic proposal validation, and the frozen
target's observable/determinant successor work remain outside this route
proof and are not claimed complete here.

