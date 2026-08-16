RIGOROUS_PARTIAL_RESULT

# Exact `t -> 0` asymptotics for the four minimum-side Bernstein gaps

## 1. Result and exact scope

This route resolves the pointwise `Aplus -> 0` sign problem left by R17.
Put

```text
k=(mu-1)/(mu+1) in (0,1),
z=Aplus=pi*t/2,
q=tan(k z)/k,
a=tan(k z)/(k tan z).
```

For a fixed negative common-angle phase put

```text
sigma=tan(k Aminus)/k,
b=-tan(k Aminus)/(k tan(Aminus)).
```

On a retained sequence with fixed `(k,Aminus)` and `z -> 0`, `g<1`
eventually requires `b>=1` (strictly `b>1` away from the limiting
`g=1` face), while the common-angle range gives `b<1/k`.

The theorem proved here is:

> **Pointwise small-plus-phase theorem.**  For every fixed
> `0<k<1` and every fixed negative common-angle phase with
> `1<b<1/k`, all four R17 gaps `G_1,...,G_4` are strictly positive for
> all sufficiently small `z>0`.  The limiting face `b=1` has the same
> conclusion by the displayed asymptotics.  The retained region is not
> empty: `rB -> +infinity`.

The proof is exact.  Its only computer-assisted step is a fixed two-box,
exact-rational tensor-Bernstein coefficient calculation.  It is not an
Arb cover, does not adaptively subdivide, and makes no finite-sampling
inference.

This does **not** yet give one uniform `t` collar simultaneously up to the
triple corners where `k -> 0 or 1` and `y -> 1`.  Consequently it does not
finish the full R14 coefficient theorem, the minimum continuant theorem,
or global reflection symmetry.

## 2. Canonical and artifact binding

Canonical snapshot used for every query:

```text
blueprint sha256:76346e2fa9f880fd8c1c02bf4b001b38cb66f2f4688c8497c9d764ebb746c7a7
inventory sha256:b6286574edbcb70ad22e5c6758a81f00dd01572c0764b8816be23cb6b166fb6f
context CTX-DEFAULT
```

Trusted canonical inputs checked through `blueprint_query.py`:

```text
CLM-NGE2-MPO3A-FULL-RELAY
  established, Grade B
  semantic-sha256:59581f99dcf540ddca1c9ec94818da1568b7eaebdce0f06b41fac8b81a3d2a46

CLM-NGE2-MPO3A-PHYSICAL-CONTINUANT-R7
  established, Grade B
  semantic-sha256:5a4e8e40668e50766f7594724eb357bddcf7b94139b86e8fdbf14582e39088ee
```

The global minimum claim `CLM-NGE2-MPO3A-MIN` remains open, Grade D,
with semantic hash
`semantic-sha256:b66ad3a2ff5a8c8f56a1d6f48e6c96a72f01e114029c03b5789159dfe68a8d27`.
R14 and R17 are used only as frozen conditional research artifacts; their
presence is not treated as trusted canonical truth.

## 3. Stable leading variables

For the fixed negative phase define

```text
D = b(1+k^2 b)+k^2(1+b)sigma^2,
C = sigma(1-k^2 b^2)/D,
e = (b^2-1)/(1-k^4 b^2),
g0 = (1+k^2)(1-k^2 b^2)/(1-k^4 b^2),
E = b^2+b+sigma^2+k^2 b sigma^2,
omega0 = (1+k^2 b)/(1+b),
omega1 = k^2 E/D.
```

All denominators are strict positive on
`0<k<1`, `1<b<1/k`, `sigma>0`.  Direct Taylor expansion gives

```text
q=z+O(z^3),
a=1-(1-k^2)z^2/3+O(z^4),
rB=C/z+O(z),
cp^2=z^(-2)+O(1),
Pplus=1+k^2+O(z^2),
Knew=1+O(z^2),
Xbar=2z/3+O(z^3),
Wbar_i=omega_i/z+O(1),
Ubar_i=omega_i/z+O(1),
Lbar_i=3e omega_i/z+O(1).
```

In particular `C>0`, hence `rB -> +infinity`; the physical condition
`rB>1` does not empty the small-`t` region.

The four R17 definitions then give the exact lowest nonzero orders

```text
lim_(z->0) z^4 G_1 = g0,
lim_(z->0) z^4 G_2 = g0[1-Z0^2/2],
lim_(z->0) z^4 G_3 = g0[1-(3/2)Z0 Z1],
lim_(z->0) z^4 G_4 = g0[1-3Z1^2],
```

where

```text
A  =(b^2-1)(1-k^2 b^2),
Z0 =sigma sqrt(A) omega0/D,
Z1 =sigma sqrt(A) omega1/D.
```

Thus the apparent four-gap problem has only three normalized limiting
inequalities.  `G_1` is immediate because `g0>0`.

## 4. Exact sign proof for the three normalized limits

### 4.1 Common-angle envelope

Since

```text
pi/2 < Aminus < pi/(1+k),
```

monotonicity of `tan`, `sin x < x`, concavity of `sin` on
`[0,pi/2]`, and `pi<4` give

```text
sigma < tan(k pi/(1+k))/k
      < pi/(1-k)
      < 4/(1-k).                                      (4.1)
```

No relaxation other than the proved superdomain (4.1) is used below.

### 4.2 Cleared polynomial inequalities

The three normalized brackets have positive denominators and the following
cleared numerators:

```text
P2 = 2(1+b)^2 D^2-sigma^2 A(1+k^2 b)^2,
P3 = 2(1+b)D^3-3sigma^2 A k^2 E(1+k^2 b),
P4 = D^4-3sigma^2 A k^4 E^2.
```

The exact identities are

```text
1-Z0^2/2       = P2/[2(1+b)^2D^2],
1-(3/2)Z0 Z1  = P3/[2(1+b)D^3],
1-3Z1^2       = P4/D^4.                               (4.2)
```

### 4.3 Elementary closure of `P2` for `0<k<=1/8`

Because `D>=b(1+k^2b)`, (4.1) yields

```text
Z0^2/2
 < 8 A/[(1-k)^2 b^2(1+b)^2]
 = 8 f(b)(1-k^2b^2)/(1-k)^2,
f(b)=(b-1)/[b^2(b+1)].
```

On `b>1`, `f` has its unique maximum at
`phi=(1+sqrt(5))/2`, and

```text
f(phi)=(5sqrt(5)-11)/2 < 3/32.
```

For `k<=1/8`, `(1-k)^2>=49/64>3/4`; hence

```text
Z0^2/2 < (3/4)/(49/64)=48/49<1.
```

Therefore `P2>0` on the entire small-`k` superdomain.

### 4.4 Fixed exact-rational Bernstein certificate

Map the remaining algebraic superdomain to a unit cube by

```text
kb=k+(1-k)x,       sigma=4zeta/(1-k),
0<x,zeta<1.
```

There are only two fixed `k` boxes:

```text
small: k=h/8,             0<h<1,
high:  k=(1+7h)/8,        0<h<1.
```

The full tensor Bernstein coefficients, computed over the rationals, are:

| box | polynomial | multidegree | coefficients | positive | zero | negative |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| small | `P3` | `(16,7,6)` | 952 | 882 | 70 | 0 |
| small | `P4` | `(20,8,8)` | 1701 | 1611 | 90 | 0 |
| high | `P2` | `(12,6,4)` | 455 | 371 | 84 | 0 |
| high | `P3` | `(16,7,6)` | 952 | 760 | 192 | 0 |
| high | `P4` | `(20,8,8)` | 1701 | 1341 | 360 | 0 |

Every Bernstein basis function is positive in the open cube.  Thus
nonnegative coefficients plus at least one positive coefficient prove
strict positivity there.  Together with Section 4.3, this proves all
three brackets in (4.2), and hence all four limiting gap coefficients.

The useful exact auxiliary identity

```text
omega0-omega1
 = b(k-1)(k+1)(bk-1)(bk+1)/[(b+1)D] >0               (4.3)
```

was also checked.  It is not needed to replace either Bernstein
certificate.

## 5. Boundary-intersection audit

### 5.1 Lower negative-phase face

At `y=0`, `Aminus=pi/2` and `b=0`, whereas `a->1`; hence `g<1`
cannot persist as `t->0`.  The exact face is automatically excluded.
This route does not claim a sharp largest uniform lower-`y` exclusion
collar.

### 5.2 The limiting `g=1` interface

At fixed `b=1`, `A=0`, so `Z0=Z1=0` and all three normalized brackets
equal one.  Thus approaching the limiting `g=1` interface does not create
a mixed leading-sign obstruction.

### 5.3 Upper negative-phase face at fixed `k`

Let

```text
epsilon=1-kb -> 0,
sigma_*=tan(k pi/(1+k))/k,
D_*=(1+k)(1/k+k sigma_*^2).
```

If `epsilon/z -> c in (0,+infinity)` with fixed `0<k<1`, then

```text
rB -> 2 sigma_* c/D_*.
```

Thus `rB>1` requires `c>=D_*/(2sigma_*)` in the limiting closure; in
particular the forbidden scale `epsilon=o(z)` is physically excluded.
On every such finite-ratio sequence, direct expansion gives, for all
`i=1,2,3,4`,

```text
lim z^3 G_i = 2c(1+k^2)/(1-k^2) >0.                   (5.1)
```

If `epsilon/z -> +infinity`, the same expansion gives
`Pplus Nhat_i/[g Knew cp^4]=O(epsilon)+O(z)` (and the `Nhat_1` ratio is
`O(z)`), so the gaps again remain positive.  Hence the `t/y=1` overlap
has no negative leading form for fixed interior `k`.

### 5.4 First unresolved step

The first step not proved here is a **uniform remainder estimate** in the
two triple-corner regimes

```text
(z,1-kb,k) -> (0,0,0),
(z,1-kb,1-k) -> (0,0,0),
```

under the exact common-angle equations and `rB>1`.  Formula (5.1) is
pointwise in fixed `k`; its `O(.)` remainder has not been bounded uniformly
as `sigma_*` and `D_*` change scale.  Therefore compactness alone cannot
yet turn this report into one global numerical value `t0>0`.

This is strictly weaker than the original four-gap problem: all fixed
interior parameters and the fixed-`k` `y=1` overlap are now discharged.
The only remaining `t=0` issue is uniformity in the two endpoint charts.

**Restart condition.**  Introduce the exact physical compactifier

```text
u=1/rB=q D(a)/[a sigma(1-k^2b^2)] in (0,1)
```

and `epsilon=1-kb`.  Rewrite the exact gaps in `(k,epsilon,u)` together
with the common-angle relation for `sigma`.  At `k->0` use the scaled
ratio `z/(k epsilon)`; at `k->1` use `z/[(1-k)epsilon]`.  A proof that the
cleared exact gaps have a positive constant term and a uniformly
nonnegative remainder on these two compact charts would close the full
`t` collar.  A premise-complete point in either chart with one gap
nonpositive would refute this route.

## 6. Verification and audits

### Definition audit

- `z,k,a,q,b,sigma,D,C,E,omega_i` are exact reparametrizations of the R17
  common-angle formulas; no independent `b,sigma` pair is asserted to be
  physically realizable.
- The algebraic certificate is deliberately proved on a superdomain
  containing every realizable pair through the exact envelope (4.1).
- The checked `G_i` are the centered R17 quantities
  `g Knew cp^4-Pplus Nhat_i`, whose signs equal the R14 `B_i` signs.

### Logic audit

- Positive leading coefficients imply an eventual sign only for each
  fixed parameter.  The report does not exchange this pointwise
  quantifier with a uniform one.
- `rB -> +infinity` proves nonemptiness only of the R14 contrast interval
  for the fixed retained phase; it is not an existence theorem for a full
  self-consistent global trajectory.
- R14/R17 are conditional research artifacts and are not promoted to
  trusted canonical premises.

### Boundary audit

- `b=1`, exact `y=0`, and fixed-`k` `y->1` were checked separately.
- The two remaining `k` endpoint intersections are stated explicitly and
  are not hidden behind continuity.
- Equality `rB=1` is a boundary closure, not part of the strict retained
  branch.

### Adversarial/computation audit

- Discovery scans were not used in any sign inference.
- The proof checker uses exact SymPy rationals and symbolic identities.
- The Bernstein calculation uses exactly two prescribed boxes and no
  interval arithmetic, tolerance, random seed, adaptive split, or omitted
  leaf.
- Zero Bernstein coefficients are harmless because each open-cube basis
  function is positive and every audited polynomial has positive
  coefficients as well.

## 7. Reproduction and hashes

Replay from the project root:

```powershell
& 'E:\ai_auto_solve\O3a_blueprint_v22_research_20260808\.venv\Scripts\python.exe' -X utf8 `
  'runs\R-20260815T181317Z-min-reflection\routes\t0_asymptotic\exact_checker.py'
```

Expected result: `status: PASS`, Python `3.12.13`, SymPy `1.14.0`.

| artifact | SHA-256 |
| --- | --- |
| R14 `derivation.md` | `bc991d859eac196b08a719ded874a9208a648d2578ea0ce0320e4a0a5ced1fd3` |
| R17 `exact_checker.py` | `ad1e084f40ed11a80576d2f768fe32c418db391d6d4d98700526a0b4e3b8584b` |
| current `cover_collar.py` | `6c3a4af844a4730b6df577b28c26ded3ac23e1e86f59538ce824c740708c97c2` |
| current `explore_coefficients.py` | `3a72be8b988fccb97e872d9280c31cbee4858a08e95086901c672922afb1b108` |
| current `explore_interface.py` | `1b5ed5797ccb31f09936c47a51cb3435bc280fb5261a1a9987c2878af03d5d34` |
| this route `exact_checker.py` | `6af7769af77597f0ef768e683434a44f7dfc4980867495c82d2534324f78093b` |

The checker-reported script hash agrees with the independently computed
file hash.  The report hash is recorded after freeze outside this text.

## 8. Calibrated status

```text
research_status: rigorous_partial_result
transaction_status: not_submitted_by_this_agent
formalization_status: not_requested
novelty_status: unknown
semantic_fidelity_confidence: high
correctness_confidence: high for the pointwise theorem and exact coefficients
completeness_confidence: high for the stated pointwise scope, low for a uniform global t collar
reproducibility_confidence: high
```
