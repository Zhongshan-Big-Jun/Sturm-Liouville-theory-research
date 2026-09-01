PARTIAL

# W11 complete-system global falsifier result

## Binding audit

All five inputs were hashed before use. The observed SHA-256 values exactly
match the packet bindings:

```text
problem_contract.md                              67427fe00b6b7758552581cde19fdb449202b5e9ea7bf9013f6ba0a4135f3f9d
route-01-transfer-schur/derivation.md            a96fde4cfaaf3cb83fcf416d3d7e627a5d63c4a48c2cd8a0c562e9dd8636e7d3
route-03-phi-exact/worker_result.md               6c1bbbd871c9aef7c8c316d47d0b61c3ab34bfb806eb5ee715ed915df6103ee3
route-04-mass-g-wave/accepted_package.md          cd56d00daadad6315bc7fe267754c4516617e08832f6ffc5b3c77883c7e24192
route-06-alpha-pi/accepted_package.md             1177c02076694ebf95ce912719846b3143e5e9099614e66492586296ae7526ba
```

## STRICT: Exact chamber obstruction through the W5 seed

There is an exact one-parameter spectral-band family containing the W5 point
on which `G<0`, but the family stays strictly in the positive coefficient
orthant and stays strictly on the positive side of the mass surface.

Let

```text
pi/6<h<pi/4,
c=4h/pi,
k=cos(2h),
m=(1-k)/k,
alpha=theta=pi/4,
beta=pi.
```

Then `0<k<1/2`, `2/3<c<1`, and `m>1`. Put

```text
s=sin(h),
d=cos(h),
q=sin(2h),
x=cq.
```

On this family the exact transfer quantities reduce to

```text
C=S=1/sqrt(2),
X=Z=D=-1/sqrt(2),
Y=s,
T=-d,
N=d(4k-3).
```

Hence `(E_DN)`, `(E_DD)`, and `(E_band)` hold identically. The modal
inequalities are also strict. Indeed,

```text
delta_3=atan(1/m),
delta_3<pi<delta_3+pi,
delta_2=pi/2+2h,
c beta=4h<delta_2.
```

The phase inequalities and strict interior reconstruction follow directly
from `pi/6<h<pi/4` and

```text
p=(alpha+m beta+theta)/L,
a=alpha/p,
b=(alpha+m beta)/p.
```

The chamber signs are exact:

```text
A=H=1/2-c^2 s^2>1/2-s^2=k/2>0,
B=(1/2)[m(d^2-c^2 s^2)+(s^2/m)(1-c^2)]>0.
```

For the last inequality, both displayed summands are positive because
`d^2-c^2 s^2=k+(1-c^2)s^2>0`.

The norm formulas simplify exactly to

```text
I3hat=(pi/4)m(m^2+m+1),
I2hat=h(1-k)^2(1+k)/k^3.
```

Therefore the mass residual is

```text
Delta_M
=C^2 I2hat-c^3 s^2 I3hat
=h(1-k)^2/k^3
  [(1+k)/2-(8h^2/pi^2)(1-k+k^2)].
```

Since `8h^2/pi^2<1/2`, the bracket is strictly larger than

```text
[(1+k)-(1-k+k^2)]/2=k(2-k)/2>0.
```

Thus `Delta_M>0` on the entire family. It never meets the complete mass
surface.

It remains to audit `G`. On the same family,

```text
Ttheta=(1+x)/2,
Dtheta=(1-2k+2k^2+x)/[2(1-2k)],
U=-[1+x(4k-3)]/sqrt(2).
```

Define

```text
Q(x,k)=x^2-1+k+kx(4k-3).
```

Direct collection gives

```text
Dtheta[1+x(4k-3)]+2Ttheta^2
=(k-1)Q(x,k)/(1-2k),

G=-[Dtheta[1+x(4k-3)]+2Ttheta^2]/sqrt(2).
```

Now `x=cq<q`. Also

```text
partial_x Q=2x-k(3-4k)>2/sqrt(3)-9/16>0,
```

because `x>1/sqrt(3)` and
`max_[0,1/2] k(3-4k)=9/16`. Consequently

```text
Q(x,k)<Q(q,k)
=k[1-k+q(4k-3)]
<k(1-k-q)<0,
```

where `4k-3<-1` and
`q^2-(1-k)^2=2k(1-k)>0`. Since `k-1<0` and `1-2k>0`, the collected bracket is
positive. Hence

```text
G<0
```

strictly throughout this exact family.

This is a rigorous slice obstruction: the W5 negative-`G` mechanism persists
on an open exact spectral-band family, but that family is trapped in the
`(+,+,+)` coefficient chamber and has `Delta_M>0`, so it cannot cross the
complete mass surface.

## STRICT: Exact W5 sign audit and effect on Phi

The W5 seed is the member `h=pi/5`, so

```text
c=4/5,
k=(sqrt(5)-1)/4,
m=sqrt(5).
```

The preceding formulas prove exactly

```text
A=H=(5+4sqrt(5))/50>0,
B>0,
G<0,
Delta_M>0.
```

The bound accepted W5 package additionally certifies `Xi<0` by exact rational
interval arithmetic. From

```text
Phi=XG-Dtheta Dalpha,
K=X[c cot(c alpha)-cot(alpha)],
Dalpha=r[c cot(c alpha)-cot(alpha)],
```

one obtains the exact identity

```text
Xi=X^2G-rK Dtheta=X Phi.
```

Since `X=-1/sqrt(2)<0`, the certified W5 sign `Xi<0` implies `Phi>0`.
Thus W5 is not a counterexample to `(SC)`: its coefficient signs are
`(+,+,+)`. It is a mass-free spectral-band counterexample to `Phi<0`, but it
is not a complete-system counterexample because `Delta_M>0`.

## EVIDENCE: Bounded complete-system continuation map

Floating-point least-squares solves of the four complete equations
`(E_DN)`, `(E_DD)`, `(E_band)`, and `(E_mass)` gave the following branch.
Every row passed the strict modal inequalities numerically. The largest
displayed-equation residual over the table was `1.14e-13`.

| `m` | `c` | `alpha` | `beta` | `theta` | `G` | `sign(A,B,H)` |
|---:|---:|---:|---:|---:|---:|:---:|
| 1.05 | 0.677606 | 2.388888 | 1.182867 | 1.096809 | 20.079161 | `+--` |
| 1.20 | 0.707262 | 2.324108 | 1.152406 | 1.072236 | 5.561623 | `+--` |
| 1.50 | 0.755267 | 2.217702 | 1.101150 | 1.033555 | 2.619336 | `+--` |
| 2.00 | 0.812410 | 2.090345 | 1.036278 | 0.988717 | 1.592427 | `+--` |
| 3.00 | 0.879332 | 1.941487 | 0.949498 | 0.936323 | 1.017903 | `+--` |
| 5.00 | 0.936682 | 1.810573 | 0.846797 | 0.888332 | 0.660964 | `+--` |
| 10.00 | 0.975682 | 1.708144 | 0.714319 | 0.847864 | 0.392522 | `+--` |

A separate bounded spectral-band scan used
`m in {1.02,1.1,1.5,sqrt(5),3,5,10,30}`, a 30-point `c` grid in
`[0.12,0.99]`, and eight deterministic random starts per grid point. Every
located admissible root with `G<0` lay in a same-sign coefficient orthant. No
mixed-chamber negative-`G` root was found. This scan is only `EVIDENCE`: it
does not exclude missed components, roots between grid points, or narrow
near-boundary branches.

An interval upgrade would require interval Newton boxes for all four complete
equations, outward-rounded verification of every strict modal inequality and
sign, and an interval continuation cover with an implicit-Jacobian bound.
Certifying the displayed positive-`G` branch would still not prove global
`G>=0`; all admissible connected components would have to be covered, or a
global analytic `(SC)` implication would have to be proved.

## OPEN

- No exact or interval-certified complete admissible tuple with `G<0` was
  found.
- No exact spectral-band tuple with `G<0` outside both same-sign orthants was
  found, so `(SC)` is not refuted.
- The exact family above proves only a slice obstruction. It does not prove
  global `(SC)` or exclude a different negative-`G` component meeting the mass
  surface.
- Complete-system `G>=0`, `(SC)`, `PHI-SIGN`, and `KP-DET` remain open.

decision_delta: The W5 seed is promoted to an exact one-parameter negative-G family with strict (+,+,+) chamber signs and an explicit positive mass-residual formula, proving a rigorous no-crossing obstruction for that whole slice while leaving global SC and complete PHI-SIGN open.
