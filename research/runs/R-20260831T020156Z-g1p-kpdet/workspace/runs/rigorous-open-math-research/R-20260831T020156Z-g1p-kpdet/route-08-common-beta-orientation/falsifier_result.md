EVIDENCE

# Bounded common-beta orientation falsification result

## Binding verification

Every declared input binding was verified before use.

| Input | Verified SHA-256 |
|---|---|
| `problem_contract.md` | `67427fe00b6b7758552581cde19fdb449202b5e9ea7bf9013f6ba0a4135f3f9d` |
| `route-01-transfer-schur/derivation.md` | `a96fde4cfaaf3cb83fcf416d3d7e627a5d63c4a48c2cd8a0c562e9dd8636e7d3` |
| `route-03-phi-exact/worker_result.md` | `6c1bbbd871c9aef7c8c316d47d0b61c3ab34bfb806eb5ee715ed915df6103ee3` |
| `route-04-mass-g-wave/accepted_package.md` | `cd56d00daadad6315bc7fe267754c4516617e08832f6ffc5b3c77883c7e24192` |
| `route-07-global-sign-coherence/accepted_package.md` | `a24a0fe82e19ef6a1aeb2e29c2379bb2f8793818940d43df9d87b9abd14ef1dc` |
| `route-07-global-sign-coherence/audit/independent_audit.json` | `11b3b68b8aa9b1dcfd593b1e919169f9057f3daa63ef1dfb6ccb09a46da7e1db` |

## Exact admissibility level

No exact or interval-certified counterexample was found. The reported tuples are floating-point `EVIDENCE` only.

The replay solves the direct shared-`beta` equations

```text
F3(alpha,beta,theta)=0,
F2(c alpha,c beta,c theta)=0,
Y+s X/C=0.
```

Thus one unsquared `beta` is used simultaneously in both spectral equations and in the oriented band equation. The phase-lock identity alone is never used as a converse. Each retained tuple separately passes

```text
delta_3<beta<delta_3+pi,
0<c beta<delta_2,
X<0,
Y>0,
0<a<b<1/2.
```

The complete-system probe also imposes the exact mass formula numerically, but its equality is not interval certified.

## Bounded map

The deterministic replay is `falsifier/common_beta_scan.py`, SHA-256
`15435d645d0fe6a540fc896117ffab2b27f7f559b86672da9135ab605b66ff9a`.
It uses seed `20260901`, double precision, and `scipy.optimize.least_squares` on

```text
1.01<=m<=40,
0.10<=c<=0.99,
0.02<=alpha<=pi-0.02,
0.02<=beta<=3pi/2-0.02,
0.02<=theta<=pi/2-0.02.
```

Raw solver returns are not asserted to be distinct roots or an exhaustive root count.

The accepted W11 specialization `h=pi/5` was used only as a regression seed. It gave spectral-band residual `1.12e-16`, `q-E=0.3275098671`, chamber `(A,B,H)=(+,+,+)`, and positive mass defect `Delta_M=4.095401539`. This reproduces its known mass-defective orientation.

The spectral-band map retained 134 admissible solver returns. Among them, 24 had `q>E`. Their chamber counts were

```text
(+,+,+): 5,
(-,-,-): 19,
mixed: 0.
```

A representative positive-chamber hit was

```text
(m,c,alpha,beta,theta)
=(2.75466169187,0.828181818182,0.776295163379,3.14709851501,0.785855579699),
q-E=0.3058923756,
(A,B,H)=(0.2462790399,0.5448223082,0.2477872289),
normalized Delta_M=0.1376223082.
```

A representative negative-chamber hit was

```text
(m,c,alpha,beta,theta)
=(1.97160224611,0.67,3.12031345643,0.0214122649818,1.54986371112),
q-E=582.5506187,
(A,B,H)=(-0.3327985343,-0.6564175748,-0.3328029800),
normalized Delta_M=-0.1331313424.
```

Both are mass defective. They numerically exhibit the same-sign separation predicted by `(SC-rem)` and do not refute it.

Among all retained mixed-chamber spectral-band returns, the largest observed margin was

```text
q-E=-0.01792481890,
(A,B,H)=(0.5034994126,-0.8047406981,-0.05001795285),
normalized Delta_M=0.0006513585.
```

The complete-system probe retained 35 admissible numerical mass roots and found zero with `q>E`. The closest observed complete return was

```text
(m,c,alpha,beta,theta)
=(17.1139823433,0.988621134902,1.66285177704,0.617838410875,0.828564619159),
q-E=-0.02086274309,
(A,B,H)=(0.4789504125,-1.2022158728,-0.06474860132),
normalized Delta_M=-1.06e-16.
```

Its spectral residual was below `1.78e-15`. This is numerical mass equality only.

## Failure mechanism

The counterexample search failed at the orientation step. On this bounded map, direct common-`beta` solutions with `q>E` split into the two same-sign chambers. The all-positive hits have positive mass defect, while the all-negative hits have negative mass defect. Every mixed chamber and every numerically mass-balanced return had `q<E`. This is evidence for, not a proof of, the missing implication behind `(SC-rem)`.

## First certification gap

The first gap is an exhaustive, outward-rounded interval cover of the common-`beta` zero set. Pointwise floating roots do not exclude an unobserved mixed-chamber component or a narrow complete `q>E` component. The solver Jacobian also degenerates toward the collar

```text
alpha=pi,
beta=0,
theta=pi/2,
c=2/3,
```

where the large negative-chamber margins occur.

An interval certification should proceed as follows.

1. Use outward-rounded interval sine, cosine, and tangent on the stated compact box.
2. Bisect the `(m,c)` parameter rectangles and apply a parameterized interval Krawczyk operator to `(F3,F2,Fband)` in `(alpha,beta,theta)`.
3. Discard boxes by the strict modal and orientation inequalities before testing chamber signs.
4. On every surviving mixed-sign box, certify `q-E<=0`, or isolate a box with `q-E>0` as an interval-certified `(SC-rem)` counterexample.
5. For the complete system, apply the four-equation Krawczyk operator to `(F3,F2,Fband,Delta_M)` in `(c,alpha,beta,theta)` over interval `m` cells, then certify the sign of `q-E` on every root tube.
6. Treat the degenerate collar analytically by a blown-up variable such as `(pi-alpha,beta,pi/2-theta,c-2/3)` before joining it to the regular interval cover.

No global statement for arbitrary finite `m>1` follows until the compact cover, the excluded collars, and the tails `m<1.01` and `m>40` are closed.

decision_delta: No refutation was found. Direct unsquared common-beta search produced q>E only in same-sign chambers and no numerically mass-balanced q>E return on the stated box, so SC-rem remains live and the next decision-changing action is a parameterized interval cover plus an analytic audit of the degenerate collar.
