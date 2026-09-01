---
title: KP-DET common-beta sign reduction
tags: [sturm-liouville, gap-extremal, kp-det, phase-reduction]
created: 2026-09-01
status: STRICT partial, independent audits PASS, global problem OPEN
---

# KP-DET common-beta sign reduction

## Scope

This tool applies to the exact five-phase system for the $n=2$ symmetric INF
finite-interior odd sector. It continues
[[kp-odd-firstzero-reduction]]. All strict statements below are bound to the
accepted W10 and W12 packages of run
`R-20260831T020156Z-g1p-kpdet`.

## STRICT results

Let

```text
M=m^2, k=M-1,
u=tan(theta), v=tan(c theta),
x=cot(alpha), y=cot(c alpha),
P=C^2+M S^2,
q=x-c rho y.
```

The exact signed phase lock is

```text
rho=(1+M x^2)/(1+M y^2)
   =v^2(1+M u^2)/(M+v^2)>0.
```

With the positive correction $E$ defined in the accepted package, the final
sign scalar has the exact factorization

```text
G=X [M Dtheta/P] (q-E).
```

All displayed denominators and $M Dtheta/P$ are positive, while $X<0$.
Therefore

```text
G<0 iff q>E.
```

The complete positive-weight mass balance, together with the exact
$B$-to-$H$ identity, excludes $Bcoef>=0$. Thus every complete tuple satisfies

```text
Bcoef<0.
```

The unsquared common-beta reconstruction can be written without branch loss as

```text
beta=A+d,
c beta=B-g,
B-g=c(A+d),
sin(B)/sin(A)=sin(g)/sin(d)=sigma>0.
```

This gives a closed strict chamber:

```text
Bcoef<0 and c alpha<=pi/2
  => q<0<E
  => G>0
  => Xi>0
  => Phi<0
  => KP-DET.
```

Because $0<alpha<pi$, every complete tuple with $0<c<=1/2$ lies in this
chamber. Hence KP-DET is proved for all complete tuples with

```text
0<c<=1/2.
```

The equality face $c alpha=pi/2$ is included and all conclusions remain
strict.

## Remaining exact obligation

Any unresolved complete obstruction must lie on the unique acute branch

```text
c>1/2,
pi/(2c)<alpha<pi.
```

At the unique common-beta root, it is enough to prove

```text
q>E implies D>k(1-c^2) max{sin(A)^2,sin(d)^2}.
```

That implication would force all three mass coefficients negative and
contradict the positive-weight mass balance. It remains OPEN for arbitrary
finite $c$.

## UNREVIEWED candidate extension

W14 proposes a monotonic compatibility scalar that would exclude the acute
branch for $c<=2/3$. W15 proposes a uniform mass-defective negative-$G$ collar
near $(alpha,theta,c)=(pi,0,2/3)$. Their joint independent audit did not run
because the service quota was exhausted. These claims remain immutable
`UNREVIEWED` candidates and are not used as strict results.

## EVIDENCE boundary

Bounded floating-point scans found no complete mass-balanced tuple with
$q>E$. This is non-exhaustive `EVIDENCE` only and does not prove the remaining
scalar implication or global KP-DET.

## Formalization status

`lean-proof/SL/KpDetCommonBeta_Scaffold.lean` checks only the algebraic sign
chain after the analytic hypotheses are supplied. The common-beta
trigonometric reconstruction and statement fidelity to the full
Sturm-Liouville contract are not encoded. The status is Tier 0 scaffold, not
`FORMALLY_VERIFIED`.

## Source and audit bindings

- Global sign package SHA-256:
  `a24a0fe82e19ef6a1aeb2e29c2379bb2f8793818940d43df9d87b9abd14ef1dc`.
- Common-beta package SHA-256:
  `2257a61c95cdcfa58b12cae577c5097ea4f124cd5d6077b6ebe550eb0779f8ed`.
- W10/W11 joint audit verdict: `PASS`.
- W12/W13 joint audit verdict: `PASS`.
- Sequence-20 recovery checkpoint ID:
  `sha256:db12944f10c127db1adca4fe977d1e4bc5063c9fe040750245db9699046b917b`.
