RIGOROUS_PARTIAL_RESULT

# Effective conditional cube-coverage audit

## 1. Three logically separate targets

This audit distinguishes:

1. **Coefficient cube:** sign the four R17 gaps on every retained point of
   `(k,t,y) in (0,1)^3`.
2. **Physical R14/R17 bridge:** prove that this cube parametrizes every
   premise-complete physical `n=2` interface needed by the continuant route.
3. **Canonical theorem:** propagate the physical conclusion through an
   independently reviewed Blueprint proposal.

Only target 1 is studied here.  Even a complete coefficient cube would not
by itself establish targets 2 or 3.

## 2. Effective dyadic cells already covered

Let `L=[0,1/64]`, `I=[1/64,63/64]`, and `H=[63/64,1]`, with state order
`(k,t,y)`.  Before this route the effective finite certificates covered

```text
III,
LII, HII, IHI, IIL, IIH,
LIL, HIL, LHI, IHH.
```

The first line is the old inner certificate, the second line the five old
single-face certificates, and the third line the completed C2-F intersection
boxes.  Existential analytic collars are deliberately absent from this list.

## 3. Four new exact retained-empty cells

Use the C2-E tangent variables

```text
p=tan(kz),  s=tan(k theta),  X=tan z,  T=-tan theta.
```

The exact formula

```text
rB=(T^2-s^2)/[XT(1+s^2)+ps(1+T^2)]
```

gives `rB<1/(ps)`.  Write

```text
A=kz=(pi/2)kt,
B=pi/2-k theta
 =(pi/2)(1-k)(1-yk/(1+k)).
```

Since `s=cot B`, `ps>1` is exactly `A>B`.  The left normalized angle
`kt` increases in `k,t`, while the right normalized angle decreases in
`k,y`.  Evaluating only rational lower endpoints proves the following
strict margins:

```text
HIH: 1921/260096,
HHL: 3905/4096,
HHI: 247999/260096,
HHH: 7811/8128.
```

Thus all four complete dyadic boxes have `rB<1` and empty strict contrast
fibers.  In particular the previous atomic or bounded-subdivision failures
in these boxes are now replaced by finite exact proofs.

The effective covered list is therefore

```text
III,
LII, HII, IHI, IIL, IIH,
LIL, HIL, LHI, IHH,
HIH, HHL, HHI, HHH.                                    (3.1)
```

There are fourteen of the twenty-seven dyadic cells in (3.1).

## 4. Exact uncovered dyadic cells

The thirteen cells not effectively covered are

```text
LLL, LLI, LLH,
ILL, ILI, ILH,
HLL, HLI, HLH,
LIH,
LHL, IHL, LHH.                                         (4.1)
```

They split into three mechanisms.

### 4.1 Unknown-thickness `t=0` annulus

The first nine cells in (4.1) are exactly the whole `t=L` slab.  C2-C
proves an existential collar `0<t<t_*` over the complete retained base, but
no numerical or rational lower bound on `t_*` was proved.  Consequently no
one of these nine `1/64`-thick cells follows from C2-C.

After deleting the unknown analytic collar, the formal leftover would be

```text
{t_* <= t <= 1/64} x (all k,y states),
```

but this is not a defined compact box until an effective `t_*` is supplied.

### 4.2 Unknown-thickness `y=1` annulus

`LIH` contains retained points and therefore cannot be discarded wholesale.
C2-E proves an empty neighborhood of its limiting edge `(k,y)=(0,1)` for
`t in I`, but gives no explicit thickness.  The remaining annulus is the
part of LIH below that unknown `y` cutoff.  The old Arb pass fails exactly
as the unspecified edge is approached.

### 4.3 Unknown-thickness `t=1` annuli

`LHL`, `IHL`, and `LHH` are not retained-empty as whole dyadic boxes.
C2-E signs an existential collar of their exact `t=1` boundary, including
the compensating `(0,1,0)` chart, but supplies no effective thickness.  The
three compact complements below the unknown `t` cutoff were therefore never
defined for a stable-coordinate finite cover.

The `LHH` corner also meets the existential `y=1` collar; neither unknown
modulus may be silently replaced by `1/64`.

## 5. First non-bypassable effectiveness gaps

The obstacle is not another sign-indefinite leading polynomial.  Both C2-C
and C2-E have nonnegative boundary polynomials and positive base limits.  The
first missing data are explicit uniform remainder bounds.

For C2-C the proof factors the common ratio bound as

```text
T=k^2 epsilon Psi_0       near k=0,
T=(1-k)^4 v Psi_1         near k=1,
```

and invokes boundedness of `Psi_0,Psi_1` on compact charts.  Neither

```text
M_0 >= sup Psi_0,       M_1 >= sup Psi_1                (5.1)
```

nor a finite effective cover of the complementary `t=0` strata was produced.
Without (5.1), no certified `t_*` can be compared with `1/64`.

For C2-E, at the sole compensating `t=1` corner,

```text
rho_i/h^2 = P_i(kappa,R)+O(h),
g Knew cp^4 = 1/2+O(h),                                 (5.2)
```

uniformly on the retained triangle, but no rational constants bounding the
two `O(h)` remainders were computed.  The first required effective package is

```text
|rho_i/h^2-P_i| <= M_E h,
|g Knew cp^4-1/2| <= M_B h                              (5.3)
```

on an explicitly bounded stable-coordinate chart, plus explicit empty-case
cutoffs for the other `t=1` strata.  Equations (5.3), not further raw
subdivision, are what would define a usable high-`t` cutoff.

## 6. Why a complete conditional cube cannot yet be claimed

The current union covers every exact limiting boundary stratum and fourteen
full dyadic cells, but an open neighborhood with unknown thickness is not a
finite certificate for its containing dyadic cell.  The thirteen cells in
(4.1) therefore remain outside the effective coefficient cover.

A valid restart is:

1. certify (5.1) and (5.3) with exact rational/Arb bounds in stable
   coordinates;
2. freeze the resulting rational cutoffs;
3. run one preregistered finite Arb cover only on the compact annuli left
   after those cutoffs.

Repeating subdivision in the original `(k,t,y)` coordinates before step 1
would reproduce the already audited dependency failures and is forbidden.

