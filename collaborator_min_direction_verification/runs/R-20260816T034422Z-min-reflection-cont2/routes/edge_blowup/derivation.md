RIGOROUS_PARTIAL_RESULT

# MIN-REFL-C2-E: nonzero-`t` side edges and the complete `t -> 1` blow-up

## 0. Calibrated result

Everything below is conditional on the frozen, noncanonical R14/R17
common-angle reduction.  It proves two exact boundary statements for the
four R17 gaps

```text
G_i = g Knew cp^4 - Pplus Nhat_i,   i=1,2,3,4.
```

1. For every fixed `z0>0`, the two retained side edges
   `(k,y)->(0,1)` and `(k,y)->(1,1)`, uniformly for
   `z=Aplus in [z0,pi/2]`, have an empty neighborhood: `rB<1`.
2. There is an existential uniform collar of the complete face `t=1`
   on which every retained point has all four `G_i>0`.  The only face
   corner which is not retained-empty is `(k,t,y)->(0,1,0)`.  Its exact
   compensating chart has `rho_i=O(h^2)`, where
   `rho_i=Pplus Nhat_i/(g Knew cp^4)`, and four manifestly nonnegative
   polynomial boundary limits are obtained below.

This signs a boundary collar of the finite-dimensional coefficient problem;
it does **not** prove the physical `n=2` theorem because the full R14/R17
bridge is not canonical.  It also does not assert that the conventional
dyadic high slabs are wholly covered.

## 1. Frozen scope

```text
run_id: R-20260816T034422Z-min-reflection-cont2
route_id: MIN-REFL-C2-E
context_id: CTX-DEFAULT
blueprint_sha256:
  sha256:358354060d1429c27b18767092c8a7d481b09f767740f6498eda195513f70dc0
inventory_sha256:
  sha256:b6286574edbcb70ad22e5c6758a81f00dd01572c0764b8816be23cb6b166fb6f
```

Noncanonical frozen inputs:

```text
runs/R-20260812T165103Z-mpo3a-cont4/routes/
  r14_min_n2_ratio_bernstein/derivation.md
  sha256:bc991d859eac196b08a719ded874a9208a648d2578ea0ce0320e4a0a5ced1fd3

runs/R-20260812T165103Z-mpo3a-cont4/routes/
  r17_min_n2_inner_box_arb_certificate/exact_checker.py
  sha256:ad1e084f40ed11a80576d2f768fe32c418db391d6d4d98700526a0b4e3b8584b
```

The atomic LIH/HIH and high-`t` failures are used only as falsification of
raw interval subdivision.  No subdivision is repeated here.

## 2. Exact tangent compactification

Put

```text
c=pi/2,       z=Aplus,       theta=Aminus,
p=tan(kz),    s=tan(k theta),
X=tan z,      T=-tan theta=tan(pi-theta).
```

The phase ranges give

```text
0<z<c<theta<pi/(1+k),       0<p<s<T.
```

The R17 variables are exactly

```text
q=p/k,       a=p/(kX),       sigma=s/k,       b=s/(kT).
```

Substitution into

```text
D=b(1+k^2ab)+k^2(a+b)sigma^2,
rB=a sigma(1-k^2b^2)/(qD)
```

and cancellation of positive factors gives the stable identity

```text
             T^2-s^2
rB = ---------------------------------.                 (2.1)
      XT(1+s^2)+ps(1+T^2)
```

It contains neither a cancellation of `1-kb` nor a vanishing `D`.
Two immediate exact bounds are

```text
rB < T/X,                 rB < 1/(ps).                 (2.2)
```

The retained condition `g<1` is exactly `b>a`.  Define

```text
u=a/b=pT/(sX),       v=p/X=ka.
```

Then `0<v<u<1` on the retained half-domain, and (2.1) is equivalently

```text
        s       u^2-v^2
rB = ----- -------------------------------.             (2.3)
        p   u(1+s^2)+u^2s^2+v^2
```

Thus `u` is the stable approach-rate coordinate for the simultaneous
`t->1,y->0` compensation; relaxing it would lose the physical condition.

## 3. The two assigned `y -> 1` side edges are empty

Fix `z in [z0,c]`, `z0>0`.

At `(k,y)->(0,1)`, the negative angle tends to `pi`, hence `T->0`, while
`X>=tan z0`.  The first bound in (2.2) gives `rB->0` uniformly, independent
of the ratio between `1-y` and `k`.  This includes the regimes in which
`epsilon=1-kb` tends to zero, a number in `(0,1)`, or one; `epsilon` alone
is therefore not a complete low-edge coordinate.

At `(k,y)->(1,1)`, `s=tan(k theta)->infinity`, while
`p>=tan(kz0)` stays uniformly away from zero.  The second bound in (2.2)
gives `rB->0`.  This also includes `t->1` and every relative rate of
`1-k`, `1-y`, and `c-z`.

For `k` in a compact subinterval of `(0,1)`, the exact numerator of (2.1)
vanishes on `y=1` because `s=T`; compactness supplies the intervening
empty collar.  Consequently the entire `y=1` face away from `t=0` has a
retained-empty neighborhood, and in particular both LIH and HIH atomic
dependency failures have an analytic boundary explanation.

## 4. Blow-up of the complete `t=1` face

Consider an arbitrary sequence with `z->c`, `g<1`, and `rB>1`.

### 4.1 All limits with `k` bounded away from zero are empty

If `k->1`, then both `p` and `s` diverge and (2.2) gives `rB->0`.

If `k->k0 in (0,1)` and `theta` stays away from `c`, then `u->0` in
(2.3), hence `rB->0`.  If also `theta->c`, pass to a limit of
`u in [0,1]`.  Here `s/p->1` and `v->0`, so

```text
rB -> u/[1+p0^2+u p0^2] <= 1/(1+2p0^2) < 1,            (4.1)
p0=tan(k0 pi/2).
```

The inequality is uniform on every compact `k` interval.  Therefore every
retained sequence approaching `t=1` must have `k->0`.

If, in addition, `theta` does not tend to `c`, (2.3) again gives `u->0`
and `rB->0`.  The sole nonempty compensating corner is thus

```text
(k,z,theta) -> (0,c,c),
```

which is the cube vertex `(k,t,y)=(0,1,0)`.

### 4.2 The compact retained chart at `(0,1,0)`

Put

```text
h=c-z,
k^2=kappa h,
u=1-alpha h.                                            (4.2)
```

These are not assumptions on approach rates.  From (2.3), `rB>1` first
forces `u->1`.  The upper bound

```text
rB <= (s/p)u/[1+s^2+u s^2]
```

then forces `k^2=O(h)` and `1-u=O(h)`.  Hence every retained sequence has
a subsequence in the compact closure `kappa,alpha>=0` of (4.2); sequences
with either quotient unbounded are excluded by `rB>1`.

Write `theta=c+eta`.  The exact definition of `u` gives

```text
eta=h+(alpha-2/c)h^2+O(h^3)                             (4.3)
```

uniformly on compact `(kappa,alpha)` sets.  Substitution in (2.3) yields

```text
rB = 1+h R+O(h^2),
R=2/c-alpha-2c^2 kappa
 =4/pi-alpha-(pi^2/2)kappa.                             (4.4)
```

The exact retained condition therefore compactifies to the triangle

```text
kappa>=0,       alpha>=0,       R>=0.                   (4.5)
```

Strict interior retained sequences have positive prelimit margin; `R=0`
is retained only as a boundary limit and is included in the uniform audit.

## 5. Exact leading forms of all four coefficient ratios

In the chart (4.2), the R17 endpoint quantities have the uniform limits

```text
Xbar -> c,
Wbar_0/h -> (2-c alpha)/(2c^2),
Wbar_1/h -> c kappa,

Ubar_0/h -> A0=c kappa+(2-c alpha)/(2c^2),
Ubar_1/h -> A1=2c kappa,
Lbar_0,Lbar_1 -> 2c,

g Knew cp^4 -> 1/2,       Pplus -> 1.                  (5.1)
```

Using `rB-1=hR+O(h^2)` and `rB^2-1=2hR+O(h^2)` in the four exact R17
definitions gives

```text
Nhat_1/h^2 -> c R A0,
Nhat_2/h^2 -> (2cR/3)(2A0+A1),
Nhat_3/h^2 -> cR(A0+2A1),
Nhat_4/h^2 -> 4cR A1.                                  (5.2)
```

Eliminate `alpha` using `alpha=2/c-2c^2 kappa-R`.  Then

```text
A0=2c kappa+R/(2c),       A1=2c kappa,
```

and the four normalized coefficient ratios satisfy the manifestly
nonnegative exact boundary limits

```text
rho_1/h^2 -> R(R+pi^2 kappa),
rho_2/h^2 -> (2R/3)(2R+3pi^2 kappa),
rho_3/h^2 -> R(R+3pi^2 kappa),
rho_4/h^2 -> 4pi^2 R kappa.                             (5.3)
```

Every denominator in (5.1) has a strict boundary limit.  The formulas are
analytic after the compactification, so the remainders are uniform on the
compact triangle (4.5).  Hence `rho_i->0` uniformly, including all zero
faces `R=0`, `kappa=0`, and `alpha=0`.  In particular `rho_i<1`, so all
four `G_i>0`, in one common neighborhood of this corner.

Combining this chart with the empty cases in Section 4 proves an
existential uniform conditional `t=1` coefficient collar over every
`0<k,y<1`.

## 6. Boundary and adversarial audit

- **All approach rates.**  The apparent escapes `k^2/h->infinity` and
  `(1-u)/h->infinity` contradict `rB>1`; finite rates are exactly the
  compact `(kappa,alpha)` chart.  Zero and boundary rates occur in (5.3).
- **`g<1`.**  It is used only through the exact inequality `u=a/b<1`.
  No closure point with `g>=1` is inserted into the retained interior.
- **`rB>1`.**  It produces the limiting triangle (4.5).  The face `R=0`
  is included only to make the uniform remainder audit closed.
- **`y=1` vertices.**  `(0,1,1)` is empty by `rB<T/X`; `(1,1,1)` is empty
  by `rB<1/(ps)`.
- **`y=0` vertices.**  `(1,1,0)` is empty by `ps->infinity`.
  `(0,1,0)` is the sole compensating chart and is signed by (5.3).
- **No interval repetition.**  The old atomic dependency leaves are not
  subdivided again.  This route changes variables before certification.
- **Logical scope.**  R14/R17 remain noncanonical.  No determinant sign,
  physical `n=2` theorem, or global reflection theorem is asserted.

## 7. Exact replay and route ledger

Run from the project root:

```powershell
& 'E:\ai_auto_solve\O3a_blueprint_v22_research_20260808\.venv\Scripts\python.exe' `
  'runs\R-20260816T034422Z-min-reflection-cont2\routes\edge_blowup\exact_replay.py'
```

The replay checks (2.1), (2.3), the chart expansions, `Knew->1/2`, and all
four nonnegative polynomials (5.3) using exact SymPy algebra over `QQ(pi)`.

```text
route_id: MIN-REFL-C2-E
target: conditional non-t0 y-high edges and complete t-up boundary collar
method_family: tangent elimination, physical retained-ratio blow-up,
               exact asymptotic coefficient certificate
status: rigorous_partial_result
local_result: complete conditional edge/collar lemma
propagation_status: non_propagating
counterexample: none
first_failing_step: the premise-complete physical R14/R17 bridge remains
                    noncanonical and was not re-proved here
restart_condition: independently re-prove and hash-bind that full bridge;
                   then combine this collar with the other conditional cover
formalization_status: not_requested
```

