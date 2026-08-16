RIGOROUS_PARTIAL_RESULT

# MIN-REFL-C2-C: uniform closure of the two `t -> 0` triple corners

## 0. Calibrated result

Within the frozen R14/R17 common-angle reduction, the two previously open
triple corners are now closed analytically.  More precisely, there is one
uniform `t_* > 0` such that every exact common-angle interface in the
retained subset

```text
0 < t < t_*,   0 < k < 1,   g < 1,   rB > 1
```

has all four centered R17 gaps

```text
G_i = g Knew cp^4 - Pplus Nhat_i > 0,   i=1,2,3,4.       (0.1)
```

The new work is the uniform estimate at

```text
(z,epsilon,k)     -> (0,0,0),
(z,epsilon,1-k)   -> (0,0,0),
z=Aplus,  epsilon=1-kb.                                  (0.2)
```

It includes every finite or zero approach-rate ratio.  An infinite ratio is
proved incompatible with `rB>1`, rather than silently omitted.

This is a complete theorem for the frozen finite-dimensional reduction, but
it is **non-propagating** for the canonical Blueprint: R14/R17 are frozen
conditional artifacts, not trusted canonical premises, and this route does
not re-prove the full physical bridge.  Therefore global reflection symmetry
is not claimed.

## 1. Frozen inputs and scope

This route is bound to

```text
run_id: R-20260816T034422Z-min-reflection-cont2
route_id: MIN-REFL-C2-C
context_id: CTX-DEFAULT
blueprint_sha256:
  sha256:358354060d1429c27b18767092c8a7d481b09f767740f6498eda195513f70dc0
inventory_sha256:
  sha256:b6286574edbcb70ad22e5c6758a81f00dd01572c0764b8816be23cb6b166fb6f
```

Trusted canonical inputs are only the node IDs and semantic hashes listed in
the assignment envelope.  The actual coefficient theorem here additionally
uses the following frozen, non-canonical research artifacts:

```text
runs/R-20260815T181317Z-min-reflection/routes/t0_asymptotic/report.md
  sha256:f51ad684668ba12b541a15d2e89b49717a540735da23992010e6083c65494ae4

runs/R-20260815T181317Z-min-reflection/routes/t0_asymptotic/exact_checker.py
  sha256:6af7769af77597f0ef768e683434a44f7dfc4980867495c82d2534324f78093b

runs/R-20260815T181317Z-min-reflection/routes/event_inertia/report.md
  sha256:938f8ebe96bd10cb562b4ca98b49a22825ab9b9d5f145f34f265f7905d678c9c

runs/R-20260815T181317Z-min-reflection/routes/event_inertia/face_results.json
  sha256:e169fad11e365ba1764879d0beb6f8bb955bb5232526097a03798476193738ed
```

The first artifact proved exact positivity of the normalized `z=0` limits,
including the fixed-interior-`k` overlap with `epsilon -> 0`, and identified
only (0.2) as the remaining uniformity gap.  No interval subdivision or
floating positivity is used below.

## 2. Exact regularization common to both charts

Use the R17 exact common-angle coordinates

```text
q=tan(kz)/k,
a=tan(kz)/(k tan z),
sigma=tan(k Aminus)/k,
b=-tan(k Aminus)/(k tan Aminus).
```

On the upper negative-phase side put

```text
epsilon=1-kb,       b=(1-epsilon)/k,       0<epsilon<1,
u=1/rB=qD/[a sigma epsilon(2-epsilon)] in (0,1),       (2.1)
D=b(1+k^2ab)+k^2(a+b)sigma^2.
```

The last identity uses `1-k^2b^2=epsilon(2-epsilon)` and is exact.  A
second useful exact factorization is

```text
g = epsilon(2-epsilon)(1-a^2 k^4)
    /[(1-a^2 k^2)(1-k^2(1-epsilon)^2)].                (2.2)
```

All displayed factors are strict positive on the retained branch.

Let `U_i,L_i` be the centered R17 endpoint quantities.  With
`rB=1/u`, `s=rB-1`, and `Delta=rB^2-1`, multiplication by `u^2` removes
the apparent singularity at `u=0`:

```text
u^2 Nhat_1 = u(1-u) U_0L_0/2,

u^2 Nhat_2 = [2u(1-u)(U_1L_0+U_0L_1)
               +(1-u^2)U_0L_0]/6,

u^2 Nhat_3 = [2u(1-u)U_1L_1
               +(1-u^2)(U_1L_0+U_0L_1)]/4,

u^2 Nhat_4 = (1-u^2)U_1L_1.                            (2.3)
```

R14 supplies positivity of all endpoint factors on the retained subset.
Consequently, for `0<u<1`, each expression in (2.3) is bounded above by

```text
S=(U_0+U_1)(L_0+L_1).                                 (2.4)
```

Indeed the sums of the deliberately loose nonnegative coefficients are
`1/2,5/6,1,1` for the four lines.

Set

```text
C=(a^2+q^2)(1+k^2q^2),       cp^4=C^2/q^4,
rho_i=Pplus Nhat_i/(g Knew cp^4).
```

Then (0.1) is equivalent to `rho_i<1`, and (2.3)-(2.4) give the common
upper bound

```text
0 <= rho_i <= T:=Pplus q^4 S/(u^2 g Knew C^2).          (2.5)
```

It remains to show `T -> 0` uniformly on the two physical blow-ups.

## 3. Low-frequency triple corner `k -> 0`

### 3.1 Compact chart and the negative phase

The physical negative phase is not relaxed.  From
`tan Aminus=-k sigma/(1-epsilon)` and the correct phase quadrants one gets
the exact equation

```text
atan(k sigma)/k + atan(k sigma/(1-epsilon)) = pi.       (3.1)
```

The left side minus `pi` extends analytically to `k=0`, where it equals
`sigma-pi` and has `sigma` derivative one.  The analytic implicit-function
theorem therefore gives a unique analytic physical branch

```text
sigma=sigma_0(k,epsilon),       sigma_0(0,epsilon)=pi.  (3.2)
```

Put

```text
x=z/(k epsilon),
D0=kD
  =(1-epsilon)+ka(1-epsilon)^2
    +k^3a sigma^2+k^2(1-epsilon)sigma^2.                (3.3)
```

Writing `q=z Q` with `Q=tan(kz)/(kz)`, (2.1) becomes

```text
u=x Q D0/[a sigma(2-epsilon)] -> x/(2pi).               (3.4)
```

Thus `u<1` bounds `x` on a fixed compact interval for all sufficiently
small `(k,epsilon)`.  In particular the purported regime
`z/(k epsilon)->infinity` contains no retained sequence.  The faces
`x=0` and `u=0` are retained in the compact closure through (2.3).

### 3.2 Uniform factor

Define the continuously regularized endpoint sums

```text
SU0=q(U_0+U_1),       SL0=q k^2(L_0+L_1).               (3.5)
```

Their removability follows directly from

```text
qW_0=(1-k^2a^2)[a sigma-bq+k^2ab(q+sigma)]
     /[sigma(a+b)(1-k^2a)],

qW_1=k^2a(1-k^2a^2)E/[(1-k^2a)D],
E=b^2+b+sigma^2+k^2b sigma^2,

qk^2L_i=2k^2qX+2(1-g)qW_i+(1-g)qU_i.                 (3.6)
```

After substituting (3.2)-(3.4), all right sides are analytic divided
differences of `tan` or `sinc`.  At the boundary,

```text
qW_i/k -> 1,       qU_i/k -> 1,
qk^2L_i/k -> 3,
SU0/k -> 2,        SL0/k -> 6.                         (3.7)
```

Using `S=SU0*SL0/(q^2 k^2)` and (2.1)-(2.2), (2.5) factors exactly as

```text
T = epsilon Phi_0,

Phi_0 = Pplus SU0 SL0 a^2 sigma^2(2-epsilon)
        (1-a^2k^2)(1-k^2(1-epsilon)^2)
        /[D0^2 Knew C^2(1-a^2k^4)].                    (3.8)
```

By (3.7), `Phi_0=k^2 Psi_0` with `Psi_0` continuous and bounded on the
compact chart.  Hence

```text
T=O(k^2 epsilon) -> 0                                  (3.9)
```

uniformly for every relative rate of `k`, `epsilon`, and `x`.

### 3.3 Exact four boundary polynomials

The sharper individual limits are useful for an adversarial sign audit.
Since `q^2U_iL_j -> 3` for every `i,j`, exact substitution in (2.3) gives

```text
lim rho_1/(k^2 epsilon) = 3pi^2 u(1-u),
lim rho_2/(k^2 epsilon) = pi^2(1-u)(1+5u),
lim rho_3/(k^2 epsilon) = 3pi^2(1-u)(1+2u),
lim rho_4/(k^2 epsilon) = 6pi^2(1-u^2).                (3.10)
```

All are nonnegative on `0<=u<=1`.  Their zeros are harmless: the entire
ratio still has the vanishing prefactor `k^2 epsilon`; at `u=1` the exact
numerators in (2.3) vanish.

## 4. High-frequency triple corner `k -> 1`

### 4.1 Compact chart and physical exclusion of `v>1`

Put

```text
d=1-k,       epsilon=dv,       tau=d sigma,
x=z/(d epsilon)=z/(d^2v).                              (4.1)
```

Writing `Aminus=pi/2+alpha` and using the correct phase quadrants gives

```text
{atan[d/((1-d)tau)]
 +(1-d)atan[d(1-dv)/((1-d)tau)]}/d = pi/2.             (4.2)
```

At `d=0` the left side minus `pi/2` is `2/tau-pi/2`; its derivative at
`tau=4/pi` is `-pi^2/8`.  Hence the physical branch is analytic and

```text
tau=tau_1(d,v) -> 4/pi                                 (4.3)
```

uniformly for `v` in a compact interval.

The retained inequality `g<1` is `b>a`.  Since
`b=(1-dv)/(1-d)` and the exact plus-angle formula has
`1-a=O(dz^2)`, it implies

```text
v < 1+(1-d)(1-a)/d = 1+o(1).                          (4.4)
```

Thus every retained triple-corner sequence eventually lies in, for
example, `0<v<2`, and every limiting retained point has `0<=v<=1`.

Let `D2=d^2D`.  Equations (2.1) and (4.1) give

```text
D2 -> 2tau^2,
u=x Q D2/[a tau(2-dv)] -> 4x/pi.                       (4.5)
```

Again `u<1` makes `x` compact and excludes
`z/[(1-k)epsilon]->infinity` from the physical retained set.

### 4.2 Uniform factor

Define

```text
SU1=q(U_0+U_1),       SL1=q(L_0+L_1),
A1=(1-a^2k^2)/d,
A2=(1-k^2(1-dv)^2)/d,
A4=(1-a^2k^4)/d.                                      (4.6)
```

The same exact `qW_i` formulas in (3.6) show continuous extension, with

```text
A1 -> 2,       A2 -> 2(1+v),       A4 -> 4,
qW_i -> 1,     qU_i -> 1,
SU1 -> 2.                                                (4.7)
```

On a limiting retained point,

```text
g -> 2v/(1+v),
ebar -> (1-v)/(1+v),
qL_i -> 3(1-v)/(1+v),
SL1 -> 6(1-v)/(1+v).                                  (4.8)
```

In particular all quantities are bounded also at `v=0` and `v=1`.

Now `S=SU1*SL1/q^2`, and exact cancellation in (2.5) gives

```text
T=d^4 v Phi_1,

Phi_1=Pplus SU1 SL1 a^2 tau^2(2-dv)A1A2
      /[Knew C^2 D2^2 A4].                             (4.9)
```

Every factor in `Phi_1` extends continuously and is bounded on the compact
physical closure; its denominators have strict positive boundary limits.
Therefore

```text
T=O(d^4v) -> 0                                         (4.10)
```

uniformly, including `v->0`, `v->1`, `u->0`, and `u->1`.

### 4.3 Exact four boundary polynomials

Here `q^2U_iL_j -> 3(1-v)/(1+v)`.  Exact substitution yields

```text
lim rho_1/(d^4v) = 3pi^2(1-v)u(1-u)/32,
lim rho_2/(d^4v) = pi^2(1-v)(1-u)(1+5u)/32,
lim rho_3/(d^4v) = 3pi^2(1-v)(1-u)(1+2u)/32,
lim rho_4/(d^4v) = 3pi^2(1-v)(1-u^2)/16.              (4.11)
```

They are nonnegative on the complete limiting physical rectangle
`0<=u,v<=1`.  The only zero faces (`u=1` or `v=1`) are already controlled
by the exact vanishing/extra-order formulas (2.3) and (4.9), so there is no
sign-indefinite leading chart.

## 5. Uniform collar conclusion

Equations (3.9) and (4.10) give neighborhoods of both triple corners on
which `T<1`, hence all `rho_i<1`.  The prior exact `t->0` artifact already
proved strict positive boundary coefficients on the complement and at the
fixed-interior-`k` `epsilon/z` overlap.  After adjoining the two compact
charts above, the full compactified `t=0` retained boundary has a finite
positive open cover.  Continuity supplies one common `t_*>0` and proves
(0.1) throughout the frozen common-angle retained domain.

This is an existential analytic collar; no decimal value of `t_*` is
asserted.  No unbounded subdivision is needed.

## 6. Adversarial and boundary audit

- **Arbitrary approach rates.**  Low-chart `epsilon/k`, high-chart `v`, and
  both zero blow-up ratios are unrestricted.  Infinite `x` is excluded by
  the exact `u<1` compactifier.
- **`u=0`.**  The apparent `rB=infinity` singularity is removable after
  (2.3); all four limits in (3.10) and (4.11) exist.
- **`u=1`.**  This is the closure `rB=1`; every exact `u^2Nhat_i` vanishes.
- **`v=0`.**  Formula (4.9) has an additional factor `v`; no exchange of a
  fixed-`v` limit is made.
- **`v=1`.**  The endpoint factor `ebar` vanishes at leading order, and the
  exact common bound remains `O(d^4v)`.
- **Denominators.**  Low-chart limits are
  `D0=1`, `Knew=1`, `C=1`, `sigma=pi`.  High-chart limits are
  `D2=2(4/pi)^2`, `Knew=1`, `C=1`, `A4=4`; all are strict positive.
- **Common-angle fidelity.**  `sigma` is never made independent of `b`;
  equations (3.1) and (4.2) are exact rewritings of the same angle.
- **Logical scope.**  The theorem signs the frozen R17 coefficient gaps.
  It does not turn R14/R17 into canonical truth and does not by itself prove
  a physical `n=2` root theorem.

## 7. Exact replay

Run from the project root:

```powershell
& 'E:\ai_auto_solve\O3a_blueprint_v22_research_20260808\.venv\Scripts\python.exe' `
  'runs\R-20260816T034422Z-min-reflection-cont2\routes\corner_blowup\exact_replay.py'
```

The replay uses exact SymPy algebra over `QQ(pi)` and performs no floating
sign test.  It checks (2.2), all four identities (2.3), the exact common
factorizations (3.8)/(4.9), the eight boundary polynomials
(3.10)/(4.11), and the two implicit-function boundary derivatives.

## 8. Route ledger

```text
route_id: MIN-REFL-C2-C
target: conditional uniform n=2 t-down event-orientation collar
method_family: analytic compactification, physical u=1/rB blow-up,
               exact endpoint-ratio factorization
status: rigorous_partial_result
local_result: complete conditional uniform proof
propagation_status: non_propagating
counterexample: none
first_failing_step: full premise-complete physical R14/R17 bridge is not
                    canonical and was not re-proved in this route
restart_condition: hash-bind or independently re-prove the full
                   common-angle-to-physical-continuant bridge, then reuse
                   this collar theorem as a proof input
novelty_status: unknown
formalization_status: not_requested
confidence_exact_algebra: high
confidence_uniform_boundary_logic: high
confidence_canonical_global_conclusion: none; scope deliberately conditional
```

Human contribution: frozen target and route boundary.  Model contribution:
the two compact charts, exact ratio factorizations, boundary polynomials, and
uniformity proof.  Tool contribution: deterministic exact symbolic replay
and hashing.
