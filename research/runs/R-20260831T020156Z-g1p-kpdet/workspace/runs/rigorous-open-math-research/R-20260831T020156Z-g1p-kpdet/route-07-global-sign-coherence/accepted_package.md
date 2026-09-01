# Accepted global sign-coherence partial package

## Status and bindings

`STRICT PARTIAL RESULT`.

This package contains only statements accepted by independent audit
`AUDIT-W10-W11-GLOBAL-01`, verdict `PASS`.

- W10 SHA-256:
  `8f5c381223b476fcf2b2d6af7f1a51e90086c3146b45a48bdd8362ad126f11aa`.
- W11 SHA-256:
  `18f2e57dfd18784527dac95d07477e89da935fff4065658f2a847af9137e4ba8`.
- Audit JSON SHA-256:
  `11b3b68b8aa9b1dcfd593b1e919169f9057f3daa63ef1dfb6ccb09a46da7e1db`.
- Audit Markdown SHA-256:
  `579cc71e692a26de07b5df2f45127910de637180634aee66d84b0f55f8cd04c5`.

Global `(SC)`, complete-system `G>=0`, `Xi>0`, `PHI-SIGN`, and `KP-DET`
remain `OPEN`.

## P8. Exact phase lock

Let

```text
M=m^2, k=M-1,
u=tan(theta), v=tan(c theta),
x=cot(alpha), y=cot(c alpha),
P=C^2+M S^2, Q=s^2+M Cc^2.
```

Every admissible spectral-band tuple satisfies the denominator-safe identity

```text
rho=(1+M x^2)/(1+M y^2)
   =s^2 P/(C^2 Q)
   =v^2(1+M u^2)/(M+v^2)>0.
```

This is a necessary signed phase identity. It is not used as a converse; the
common-`beta` orientation data are not recovered from it alone.

## P9. Exact factorization of G

Define

```text
H0=u v(1+v^2)(1+M u^2)+c(1+u^2)(M+v^2)>0,
E=M c u k(u^2 v^2-1)^2/[(M+v^2)H0]>=0,
q=x-c rho y.
```

Then

```text
G=X [M Dtheta/P] (q-E).
```

All denominators are positive on the strict modal domain. Since `X<0`,

```text
G<0 iff q>E.
```

Moreover, `E=0` exactly when `u v=1`, equivalently
`theta+c theta=pi/2`, and `G=0` exactly when `q=E`. The scalar `q` also has
the exact differential form

```text
q=(1+M x^2)/(2k) d/dalpha log(
  [sin(c alpha)^2+M cos(c alpha)^2]
  /[sin(alpha)^2+M cos(alpha)^2]).
```

## P10. Exact B-to-H identity and complete chamber exclusion

Let `e=1-c^2`. The exact phase lock implies

```text
m B/(s^2 X^2)
=(1+M y^2)[M H-k e C^2 s^2]/(C^2 Q).
```

Every factor outside the final bracket is positive. Therefore `B>=0` forces
`Lalpha>0`, `H>0`, and `A>0`, contradicting the complete mass balance

```text
alpha A+beta B+theta H=0.
```

The equality face `B=0` is also excluded. Hence every complete admissible
tuple satisfies

```text
B<0.
```

The remaining complete chambers are exactly

```text
Lalpha<=0: A<=0, B<0, H>0,

Lalpha>0: A>0, B<0, and
H/(s^2 X^2)
 =[beta(m-1/m)(1-c^2)-(alpha+m beta)Lalpha]/theta.
```

The unresolved sign-coherence step is to use the unsquared common-`beta`
orientation to prove that `q>E` and `B<0` force the forbidden same-sign
negative chamber, or directly to prove `q<=E` on the complete mass manifold.

## P11. Exact mass-defective negative-G family

For

```text
pi/6<h<pi/4,
c=4h/pi,
k=cos(2h),
m=(1-k)/k,
alpha=theta=pi/4,
beta=pi,
```

the spectral, band, modal, and strict reconstruction conditions hold exactly.
The coefficient chamber and sign are

```text
A>0, B>0, H>0, G<0.
```

The exact mass residual is

```text
Delta_M
=h(1-k)^2/k^3
 [(1+k)/2-(8h^2/pi^2)(1-k+k^2)]>0.
```

Thus this whole negative-`G` family remains strictly on the positive side of
the mass surface. It is a rigorous no-crossing obstruction for this slice,
not a complete-system counterexample. The W5 point is the specialization
`h=pi/5`.

## Evidence boundary

The floating-point complete branch and bounded spectral-band scan in W11 are
`EVIDENCE` only. They do not prove global absence of complete negative-`G`
components.

