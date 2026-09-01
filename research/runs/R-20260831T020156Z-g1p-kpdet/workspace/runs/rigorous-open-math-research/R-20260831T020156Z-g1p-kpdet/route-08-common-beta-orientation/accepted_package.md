# Accepted common-beta orientation partial package

## Status and bindings

`STRICT PARTIAL RESULT`.

This package contains only W12 statements accepted by independent audit
`AUDIT-W12-W13-ORIENTATION-01`, verdict `PASS`.

- W12 SHA-256:
  `6ecc0ae44f6841414a8a8be8077ed919f1d66d285dc66abbdc79f85660c44d6d`.
- W13 SHA-256:
  `61ff0e77fac55e0496d08720b0f06315f9617a8cb38d347e23fbbf43445d6135`.
- Audit JSON SHA-256:
  `bb1207baf181f37459345ed3cff4deb560b5c0acc18fdc3952b8410ffb6bd820`.
- Audit Markdown SHA-256:
  `22b69f39e6d5cb1f12cf6b112b9d0a48e6fe40e36c5bf78a03c9a109272cff99`.

W13 remains `EVIDENCE` only. The arbitrary finite-`c` acute threshold,
global `PHI-SIGN`, and global KP-DET remain `OPEN`.

## P12. Branch-safe common-beta identity

With the accepted variables, define

```text
A=pi/2+atan2(m cos(alpha),sin(alpha)),
B=pi/2+atan2(m cos(c alpha),sin(c alpha)),
d=atan(1/(m tan(theta))),
g=atan(tan(c theta)/m).
```

The strict modal intervals select the exact unsquared identities

```text
beta=A+d,
c beta=B-g,
B-g=c(A+d).
```

No hidden multiple of `pi` remains. The positive square-root phase lock is

```text
sin(B)/sin(A)=sin(g)/sin(d)=sigma>0.
```

## P13. Exact coefficient dictionary

Let `M=m^2`, `k=M-1`, `e=1-c^2`, and

```text
JA=c^2 cot(A)^2-cot(B)^2,
Jd=c^2 cot(d)^2-cot(g)^2,
D=c^2-sigma^(-2).
```

Then

```text
Bcoef/(s^2 X^2)=(e-JA)/m,
Hcoef/(C^2 s^2)=e-Jd/M,
Lalpha=e-JA/M,
sign(Bcoef)=sign(e-Jd),

Bcoef<0 iff JA>e iff Jd>e iff sigma>1/c,
Acoef<0 iff D>k e sin(A)^2,
Hcoef<0 iff D>k e sin(d)^2.
```

The accepted scalar has the exact branch-safe form

```text
q=[c sigma cos(B)-cos(A)]/[m sin(A)],
```

and the correction `E` is strictly positive whenever `Bcoef<0`.

## P14. Closed KP-DET chamber

Every spectral-band-modal tuple satisfying

```text
Bcoef<0 and c alpha<=pi/2
```

has

```text
q<0<E,
G>0,
Xi>0,
Phi<0,
KP-DET.
```

The boundary `c alpha=pi/2` is included and remains strict. Since every
complete tuple has accepted `Bcoef<0`, every complete tuple with

```text
0<c<=1/2
```

satisfies KP-DET.

## P15. Unique remaining acute branch

Any possible complete obstruction must satisfy

```text
c>1/2,
pi/(2c)<alpha<pi.
```

All orientation angles are then acute. With `kappa=B-c A`, common orientation
and the positive lock reduce to

```text
sin(kappa-c d)/sin(d)=sigma,
g=kappa-c d.
```

The logarithmic derivative is

```text
-c cot(g)-cot(d)<0,
```

so the admissible `d`, `g`, and common `beta` are unique.

The remaining exact obligation is to prove, at this unique root,

```text
q>E implies
D>k e max{sin(A)^2,sin(d)^2}.
```

This would force `Acoef`, `Bcoef`, and `Hcoef` all negative, contradicting
the positive-weight mass balance. The implication has not been proved.

## Evidence boundary

W13's bounded numerical scan found no mixed-chamber or numerically
mass-balanced `q>E` tuple. It is non-exhaustive `EVIDENCE` and is not used in
P12-P15.
