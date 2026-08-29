CANDIDATE_COMPLETE_PROOF

# Finite-interior scale-entry lemma for the exact M3 zero set

## Binding, status, and scope

- Target inference: `INF-R002-FINITE-INTERIOR-SCALE-EXHAUSTIVENESS-V1`.
- New gap-closing lemma statement: `lemma_statement.txt`, SHA-256
  `10358fe112ed5d183acf7417f80668b6c5d816756b31bcaba78ffb19a0e46bb8`.
- Run/round/route:
  `R-20260825T100044Z-b4-m3-blueprint/round-003/route-004-scale-entry-lemma-audit`.
- Author/researcher: `/root/scale_entry_lemma_researcher`.
- Formalization mode: off.
- Result status: **proved as a candidate lemma**; later independent proposal
  review is not claimed here.
- Scope: only exact real zeros in the frozen finite, nonzero, interior
  `n=2` symmetric INF M3 chart.  No statement is made about `K->0`,
  `K->infinity`, nonunit limiting `k3/k2`, vanishing phase denominators,
  SUP, `n>=3`, M1, M2, or global reflection symmetry.

## Exact theorem and quantifiers

Let `u` range over all sufficiently small positive reals, put `v=u^2`, and
let an arbitrary selection

```text
u |-> (K(u),p1(u),p3(u),r(u)),   r=k3/k2,
```

satisfy the exact hash-bound equations `E1=E2=E5=E6=0`.  No continuity,
measurability, transseries, or other regularity of this selection is assumed.
Assume that for some `0<K_-<K_+<infinity`, eventually

```text
K_- <= K <= K_+,
p1 -> pi/2,  p3 -> pi/4,  r -> 1,
```

and that the finite-interior phase denominators are nonzero.  Define only
afterward

```text
x=p1-pi/2,                 y=p3-pi/4,
q=(K*x-2*v)/v^2,           Cbr=K*(r-1)/v^2,
B=y/v.
```

Then there exist branch-dependent `M,u0>0` such that for every `0<u<u0`,

```text
|x-2*v/K| <= M*v^2,
|r-1| <= M*v^2,
|y| <= M*v.
```

Thus `q,Cbr,B` are bounded; moreover, with

```text
kappa=(18*pi-48/pi)^(1/3),
q0(K)=(18*pi-24-K^3)/(6*K),
C0(K)=16/(pi*K),
```

every such exact zero selection satisfies

```text
K=kappa+O(v),              B=1/kappa+O(v),
q=q0(kappa)+O(v),          Cbr=C0(kappa)+O(v).
```

It eventually enters the two-face IFT neighborhood of the existing route-002
proof and equals its unique analytic germ in `v`.  This closes the entry gap
without assuming the boundedness that it proves.

## Bound premises, definitions, and artifacts

1. Frozen problem contract, SHA-256
   `6dc56880458e66119f66c2a16f33df65afa799e03bbc681db5809e127e585e19`.
2. Exact closed residual source `scripts/_gapn2_largeR_closed.py`, SHA-256
   `e357d8e447ce998020c8dadc94eb27db884dd85932d592a9b4331366f8ac13a4`.
3. Existing finite-branch proof package, SHA-256
   `0f609135b8d8bd2c9d830d0c9b86ef3b41454c217578a18992c76a9afad404d8`.
4. Existing route-002 proof package, SHA-256
   `88be4d4c2a987729706aa8c7cf7860c9ede0a53f5bdd5732019fc683f7695008`.
5. Existing valuation audit, SHA-256
   `4e6b45befa420b7b65f49a93fd3157946d53c50482e4c1262f225964df3122b4`.
6. New exact replay `scale_entry_replay.py`, SHA-256
   `9abbe792df1fa5e74e113bdae8553a52d2e564d825a7d8a349052f1533f0c9c0`.
7. Passing replay log `scale_entry_replay.log`, SHA-256
   `3afc18c92388027a5f37ffdef5806839c78017610b7e4a5069403f8568eb3c67`.
8. New boundary/adversarial audit, SHA-256
   `0818e6510ef168eb5e599b651772f087be45908ae3fc8cffd3faa0423cabb5d8`.

The defective `_gapn2_largeR_Pbuild.py` D-mass coefficients are forbidden
inputs.  The replay independently transcribes the exact closed mass formula.

## Ordered proof

### 1. Two exact tangent identities

Set

```text
x=p1-pi/2,
xt=r*p1-pi/2,
p2=K*u/2-u^3*(p1+p3),
p2t=r*p2.
```

For small `u`, `p2/u` and `p2t/u` stay uniformly separated from zero, while
`p3,p3t` stay near `pi/4`.  Substituting

```text
cos(p1)=-sin(x),  sin(p1)=cos(x),
cos(r*p1)=-sin(xt),  sin(r*p1)=cos(xt)
```

into the *exact* equations `E1=0` and `E2=0`, and only then dividing by the
nonzero local factors, gives

```text
tan(x)
 = u^3*(cot(p2)-u^3*tan(p3))
       /(1+u^3*tan(p3)*cot(p2)),                         (T1)

tan(xt)
 = u^3*(cot(p2t)+u^3*cot(p3t))
       /(1-u^3*cot(p3t)*cot(p2t)).                       (T2)
```

These identities are exact; no asymptotic expansion of the selected branch
has been assumed.

### 2. `E1` forces bounded `q`

Write

```text
p2=u*h,  h=K/2-v*(p1+p3).
```

The hypotheses put `h` in a fixed compact subset of `(0,infinity)`.  Taylor's
formula for `cot` is therefore uniform:

```text
u*cot(u*h)=1/h-v*h/3+O(v^2)=2/K+O(v).
```

The tangent and phase factors in (T1) are uniformly bounded and its
denominator is `1+O(v)`.  Hence

```text
tan(x)=2*v/K+O(v^2).
```

Since `x->0`, `x=tan(x)+O(tan(x)^3)`, and therefore

```text
x=2*v/K+O(v^2).
```

It follows immediately that `q=(K*x-2*v)/v^2=O(1)`.

### 3. `E2` forces bounded `Cbr`

Because `p2t=u*(r*h)`, the same uniform calculation in (T2) gives

```text
xt=2*v/(r*K)+O(v^2).
```

But exactly

```text
xt-x=(r-1)*p1.
```

Subtracting the two estimates yields

```text
(r-1)*(p1+2*v/(r*K))=O(v^2).
```

The factor in parentheses tends to `pi/2`, so it is bounded away from zero.
Consequently

```text
r-1=O(v^2),   Cbr=K*(r-1)/v^2=O(1).
```

This is the missing entry estimate for the spectral ratio and does not use
`E5`, the defective Pbuild cascade, or a series ansatz.

### 4. First spectral IFT with the phase displacement left unscaled

Now make the exact changes of variables

```text
p1=pi/2+(2*v+q*v^2)/K,
r=1+Cbr*v^2/K,
p3=pi/4+y,
```

where `y` is not divided by `v`.  In the finite-interior chart the exact
quotients

```text
F1=E1/v,  F2=E2/v,
L6=E6/u^5,  L5=E5/v^2
```

extend real-analytically in `(v,K,q,Cbr,y)`.  The exact replay checks every
coefficient below the displayed divisors is zero.  At `v=0,y=0`,

```text
F1=-sqrt(2)*(K^3+6*K*q-18*pi+24)/(24*K),
F2= sqrt(2)*(3*pi*Cbr*K+K^3+6*K*q-18*pi-24)/(24*K),
det d(F1,F2)/d(q,Cbr)=-pi/16.
```

Thus their unique zero is `(q0(K),C0(K))` and the first analytic IFT gives

```text
q=Q(v,K,y),  Cbr=D(v,K,y)
```

near the compact first-face manifold.

It remains to justify that an arbitrary admitted zero enters that local
graph.  If it did not, choose a sequence `u_n->0` staying a fixed distance
away.  Steps 2-3 make `q,Cbr` bounded, and `K` is compact, so a subsequence
converges to `(K*,q*,C*)`.  Passing to the analytic endpoint equations forces
`q*=q0(K*)` and `C*=C0(K*)`, a contradiction.  This argument requires no
regularity of the selected branch.

### 5. The unscaled `E6` zero graph forces bounded `B`

Substitute `Q,D` into the remaining exact quotients:

```text
S6(v,K,y)=L6(v,K,Q(v,K,y),D(v,K,y),y),
S5(v,K,y)=L5(v,K,Q(v,K,y),D(v,K,y),y).
```

Both vanish at `(v,y)=(0,0)` for every positive `K`.  Exact chain-rule
elimination in the replay gives

```text
partial_y S6(0,K,0)=8/K,
partial_v S6(0,K,0)=-8/K^2,

partial_y S5(0,K,0)=4*pi/K^5,
partial_v S5(0,K,0)
 =2*(pi*K^3-24*pi^2+48)/(3*pi*K^6).              (D)
```

The first derivative in (D) is uniformly nonzero on the compact `K` range.
The analytic IFT in the *unscaled* variable `y` therefore gives the unique
local `S6=0` graph

```text
y=Y(v,K),  Y(0,K)=0,
partial_v Y(0,K)=-(partial_v S6)/(partial_y S6)=1/K.
```

Uniform analyticity on a finite cover of the compact `K` interval gives

```text
y=v/K+O(v^2).
```

Therefore `B=y/v=1/K+O(v)` is bounded.  This is the key noncircular step:
`B` was not a parameter of the first IFT and was not assumed bounded.

### 6. The remaining exact mass equation forces the unique positive seed

Since `S5(0,K,Y(0,K))=0`, analytic divisibility in the one variable `v`
defines

```text
Psi(v,K)=S5(v,K,Y(v,K))/v.
```

Using (D) and `partial_v Y(0,K)=1/K`,

```text
Psi(0,K)
 = partial_v S5 + (partial_y S5)/K
 = 2*(pi*K^3-18*pi^2+48)/(3*pi*K^6).
```

Every positive-`u` exact zero has `Psi(v,K)=0`.  Any accumulation point of
its compact `K` values must therefore solve

```text
pi*K^3-18*pi^2+48=0.
```

The left side is strictly increasing for `K>0` and has the unique positive
root

```text
kappa=(18*pi-48/pi)^(1/3).
```

Thus `K->kappa`.  Moreover

```text
partial_K Psi(0,kappa)=2/kappa^4 != 0,
```

so the scalar analytic IFT gives the unique local `K(v)` and
`K=kappa+O(v)`.  Substitution into `Y,Q,D` gives all four estimates stated in
the theorem.

### 7. Exact bridge to the existing two-face proof

Set `y=v*B` after Step 5 has proved `B=O(1)`.  The directional derivatives
in (D) give exactly

```text
H6=8*(B*K-1)/K^2,
H5=2*(6*pi^2*B*K+pi*K^3-24*pi^2+48)/(3*pi*K^6).
```

At `(K,B)=(kappa,1/kappa)`,

```text
det d(H6,H5)/d(B,K)=16/kappa^5 != 0.
```

Hence every admitted exact zero has been proved to enter precisely the
secondary IFT neighborhood used by route-002.  Local uniqueness identifies it
with the already constructed exact analytic germ.  This proves exhaustion of
Puiseux, logarithmic, inverse-logarithmic, mixed power-log, odd-power, flat,
and non-transseries alternatives in the declared admitted class: none can be
a distinct exact branch.

## External theorem contracts

1. **Uniform Taylor remainder on a compact set.**  An analytic scalar
   function and its derivatives are bounded on a smaller compact
   neighborhood, yielding a uniform finite-order remainder.  Used for
   `u*cot(u*h)` and the final `O(v)` estimates.
2. **Bolzano-Weierstrass compactness.**  Every bounded real sequence has a
   convergent subsequence.  Used only in contradiction arguments; no branch
   continuity is inferred from it.
3. **Real-analytic implicit-function theorem.**  A real-analytic map with
   invertible variable derivative has a unique local analytic zero graph.
   Applied first in `(q,Cbr)`, then in the unscaled `y`, and finally in `K`.
   The displayed exact derivatives verify every rank hypothesis.

These are standard mathematical infrastructure; no unverified repository
claim is imported.

## Boundary, adversarial, and computation discharge

The complete definition, logic, boundary, and adversarial audit is bound in
`boundary_adversarial_audit.md`.  In particular it checks slowly divergent
`q`, `Cbr`, and `B`, discontinuous zero selections, phase/tangent
denominators, alternative positive `K` accumulation points, and all excluded
singular geometries.

The exact replay uses SymPy 1.13.1 with no floating arithmetic, sampling,
randomness, tolerance, or numerical acceptance threshold.  It checks source
hashes, analytic divisibility, the first determinant, the four derivatives in
(D), and the recovered `H6,H5` faces.  Computation certifies the algebraic
coefficients only; the universal proof bridge is the exact tangent,
compactness, and analytic-IFT argument above.

## Obligation map

| Obligation | Discharge |
| --- | --- |
| derive `q=O(1)` without assuming `A=O(1)` | exact (T1), Step 2 |
| derive `Cbr=O(1)` without assuming its scale | exact (T2)-(T1), Step 3 |
| use first IFT without assuming `B=O(1)` | unscaled `y` chart, Step 4 |
| derive `B=O(1)` | nonzero `partial_y S6`, Step 5 |
| exclude other positive finite seeds | exact scalar `Psi(0,K)`, Step 6 |
| enter existing secondary IFT neighborhood | convergence plus exact determinant, Step 7 |
| handle non-transseries/discontinuous selections | compactness and pointwise uniqueness |
| preserve singular boundary scope | explicit exclusions in theorem and audit |

`unresolved_obligations: []` for this scale-entry lemma.

## Provenance and calibrated confidence

- Human contribution: frozen repository problem and request to close the
  reviewer-identified entry gap.
- Prior model/tool contribution: route-001 and route-002 exact residual
  packages, used only with their recorded candidate status and hashes.
- This researcher contribution: the exact tangent-entry proof, unscaled
  phase IFT, scalar seed reduction, and audits.
- Tool contribution: SHA-256 verification and exact SymPy coefficient replay.
- Numerical evidence: none.
- Novelty status: `unknown`; no novelty claim is made.
- Confidence: semantic fidelity high; correctness high pending independent
  review; completeness high for the stated finite-interior entry lemma;
  novelty unknown; reproducibility high.
