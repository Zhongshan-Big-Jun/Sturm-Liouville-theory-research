# Independent audit of Route 10

## Verdict

`REPAIRABLE_GAP`.

Audit ID: `AUDIT-DIRECT-PSI-QUAD-01`.

The reviewer did not author Route 10. All four authorized input SHA-256 values were recomputed before mathematical use and matched exactly. No solver was rerun, and no web search or numerical evidence was used.

## Input integrity

| Input | Verified SHA-256 |
| --- | --- |
| `problem_contract.md` | `67427fe00b6b7758552581cde19fdb449202b5e9ea7bf9013f6ba0a4135f3f9d` |
| `route-08-common-beta-orientation/accepted_package.md` | `2257a61c95cdcfa58b12cae577c5097ea4f124cd5d6077b6ebe550eb0779f8ed` |
| `route-09-acute-threshold/accepted_package.md` | `c76ed655d854bb327fc3755cbd0c2438cddd6eaf37f64111944dcf13db7be45d` |
| `route-10-psi-quadrature/coordinator_direct.md` | `e156f97b449daef0eac35ed7ae7ef30ceb2c6eac35983bc24534cf6f1b1a4634` |

## Verification of Q1-Q3

The acute identities give

```text
c alpha=pi-H_m(B),
c theta=H_m(g),
c beta=B-g.
```

Therefore

```text
cW
=c alpha+c theta+mc beta
=pi-H_m(B)+H_m(g)+m(B-g)
=pi+F_m(g)-F_m(B),
```

which is Q1.

The positive lock and `r=sigma^(-2)` give

```text
sin(A)^2=r sin(B)^2,
sin(d)^2=r sin(g)^2.
```

Hence

```text
cN
=c alpha sin(A)^2+c theta sin(d)^2
=r[(pi-H_m(B))sin(B)^2+H_m(g)sin(g)^2],
```

which is Q2.

For `M=m^2` and `k=M-1`,

```text
H_m'(z)=m/[1+k sin(z)^2].
```

Thus

```text
F_m'(z)
=H_m'(z)-m
=-m k sin(z)^2/[1+k sin(z)^2].
```

Since `0<g<B<pi/2`, integration in the correct orientation gives

```text
F_m(g)-F_m(B)
=m k integral_[g,B] sin(z)^2/[1+k sin(z)^2] dz>0.
```

This verifies Q3, including its strict sign.

## Verification of Q4-Q6

With the Route 10 definitions,

```text
V=cW,
rU=cN.
```

Therefore the accepted residual `Psi=DW-k e N` satisfies

```text
cPsi=DV-k e rU.
```

Here `c`, `k`, `e`, and `V` are strictly positive. Division is safe and gives

```text
Psi>0 iff D/(k e)>rU/V=T_quad.
```

This is Q4.

Expanding `V` by Q1 gives

```text
V
=pi-H_m(B)+H_m(g)+m(B-g).
```

Consequently,

```text
V sin(B)^2-U
=H_m(g)[sin(B)^2-sin(g)^2]
 +m(B-g)sin(B)^2.
```

This is Q5 exactly. Both terms are strictly positive because `H_m(g)>0`, `0<g<B<pi/2`, `m>1`, and `B-g=c beta>0`. There is no equality case in the strict branch. Division by `V>0` yields

```text
U/V<sin(B)^2,
T_quad=rU/V<r sin(B)^2=sin(A)^2.
```

Thus Q6 and the claimed strict quadrature gain are correct.

## Q7-Q8 branch and denominator audit

Because `A` and `d` are acute and the positive lock gives their sines, the principal reconstructions are exactly

```text
A=asin(sqrt(r)sin(B)),
d=asin(sqrt(r)sin(g)).
```

Their cosines are the positive square roots displayed in Q7. No squared equation creates an extra branch.

The displayed denominator

```text
cos(d)(1+k sin(g)^2)
+c sqrt(r)cos(g)(1+k r sin(g)^2)
```

is strictly positive term by term. The accepted q formula also verifies the first term of `Q_quad` directly:

```text
q=[c sigma cos(B)-cos(A)]/[m sin(A)],
sigma=1/sqrt(r),
sin(A)=sqrt(r)sin(B),
```

so

```text
mrq=[c cos(B)-sqrt(r)cos(A)]/sin(B).
```

This is exactly the first term of Q7.

## First load-bearing gap

The first unsupported step is the E substitution in Q7. None of the four authorized hash-bound inputs states the exact formula defining E:

- The Route 08 accepted package states only that E is strictly positive when `Bcoef<0`.
- The Route 09 accepted package uses E in the open implication but does not define it.
- Route 10 asserts substitution in an accepted E formula but does not state that formula or bind an input containing it.

Therefore an independent reviewer cannot identify the second term of `Q_quad` with `mrE`. The positivity of its displayed denominator is verified, but the equality

```text
q-E=Q_quad/(mr)
```

does not follow from the authorized dependency closure. This is a dependency-layer gap at Q7-Q8, not evidence of a false formula.

The smallest repair is to bind an immutable accepted source that states the exact E formula, or to restate the exact formula with provenance in a hash-bound repair artifact, and then display the algebra from that formula to the second term of Q7. A fresh audit need only recheck that substitution and Q8.

## Global status and Q9

Q1-Q6, the acute reconstructions, the Q7 denominator sign, and the q contribution to Q8 are verified. Q7-Q8 as a complete q-E identity are not yet accepted. Accordingly, the claimed exact reduction to Q9 is not yet in the audited closure.

Q9 itself remains open, as required. Complete `c>2/3` `PHI-SIGN` and KP-DET remain open. No numerical statement is used as proof.
