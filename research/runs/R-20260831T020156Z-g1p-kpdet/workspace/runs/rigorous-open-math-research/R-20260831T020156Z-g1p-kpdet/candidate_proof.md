RIGOROUS_PARTIAL_RESULT

# Candidate partial proof package

This package is frozen for fresh independent audit. It does not claim KP-DET,
KO-DET, or global G1 prime.

## Contract

Work on the prescribed finite-interior n=2 symmetric INF branch. The target is

```text
KP-DET: det Kp_odd(R)>0 for every finite R>1.
```

Use the audited prior congruence

```text
M=(2lambda_2)^(-1)U^(-2)Kp_odd U^(-2)
 =[[a_0-gamma_1,b_0],[b_0,b_0-gamma_2]],
b_0>0.
```

## P1. Strict global lower-right pivot

On the final half-layer, put

```text
k_j=sqrt(lambda_j R),
theta_j=k_j(L-b),
c=k_2/k_3,
tau=R-1.
```

The mode indices give `0<theta_3<pi/2` and
`theta_2=c theta_3`. Exact endpoint Green and quotient formulas yield

```text
gamma_2-b_0=2/[v(b)^2 k_3]
  {R/tau[tan(theta_3)+c cot(theta_2)]
   -[sin(theta_3)cos(theta_3)
     +c sin(theta_2)cos(theta_2)]}.
```

Since `R/tau>1` and, for `0<t<pi/2`,

```text
tan(t)-sin(t)cos(t)=sin(t)^3/cos(t)>0,
cot(t)-sin(t)cos(t)=cos(t)^3/sin(t)>0,
```

one has

```text
gamma_2>b_0>0,
(Kp_odd)22<0.                                  (P1)
```

The root derivation is in `direct_attempt.md`. Both bounded routes reproduced
the angle range, Green signs, half/full normalization, and factor `2`
independently.

## P2. Exact scalar Schur frontier

Because the lower-right pivot is strictly negative,

```text
det M=(b_0-gamma_2)S_KP,
S_KP=a_0-gamma_1+b_0^2/(gamma_2-b_0).
```

Therefore

```text
KP-DET  if and only if  S_KP<0.                 (P2)
```

This equivalence is global on the finite-interior branch. It no longer depends
on first assuming a singular point.

## P3. Lossless elementary phase reduction

Set

```text
m=sqrt(R)>1,
p=sqrt(lambda_3 R),
alpha=p a,
beta=p(b-a)/m,
theta=p(L-b),
0<c<1.
```

With the abbreviations and exact spectral, band, mass, and modal-domain
constraints in `route-01-transfer-schur/derivation.md`, define

```text
Phi
=Dtheta[X(D-c s N/C)-Dalpha]
 +X^2 Ttheta^2/C^2.
```

Every denominator removed in the derivation is strictly positive, and the
four exact branch equations reconstruct the normalized finite-interior branch
point. Hence

```text
S_KP<0  if and only if  Phi<0,                  (P3)
S_KP=0  if and only if  Phi=0
```

on the complete admissible phase constraint set. No Green kernel, Wronskian,
eigenfunction amplitude, or spectral truncation remains in `Phi`.

## P4. Exact Jacobi geometry and route closure

If a same-sign kernel exists, let `phi,psi` be its parity-crossing Jacobi
fields and put

```text
alpha_J=phi/v,
beta_J=psi/w.
```

Their projective fluxes agree exactly:

```text
v^2 alpha_J'=w^2 beta_J'=P,

P=0                                             on (0,a),
P=-lambda_2 tau y_1v(a)^2                       on (a,b),
P=-lambda_2 tau[y_1v(a)^2+y_2v(b)^2]            on (b,L).
```

Let `h=v psi-w phi`. Then `h` has exactly one simple downward zero `xi` in
`(a,z)`, where `z` is the unique zero of `w`, and

```text
-Q'(a)/c=lambda_2 tau v(a)^2
  int_a^xi [1/w^2-1/v^2] dx.                    (P4a)
```

The endpoint impulse ratio is

```text
y_1v(a)^2/[y_2v(b)^2]
  =(gamma_2-b_0)/b_0>0.                         (P4b)
```

The right side of `(P4a)` increases from zero to infinity as `xi` moves from
`a` to `z`. Thus this Sturm condition is always uniquely realizable and cannot
by itself exclude the kernel. Pure quotient monotonicity is therefore a closed
dead end for KP-DET. Full details are in
`route-02-jacobi-falsifier/derivation.md`.

## Exact remaining obligation

Prove

```text
Phi(m,c,alpha,beta,theta)<0
```

on the exact phase system in the W1 derivation, or construct an admissible
interior tuple satisfying the same system and `Phi=0`. Equivalently, determine
the first-switch residual sign after the positive endpoint ratio `(P4b)` is
propagated through the middle layer.

## Status boundary

- P1 is a new candidate strict theorem, independently reproduced by W1 and W2.
- P2-P4 are candidate strict reductions, not a proof of KP-DET.
- KP-DET remains `OPEN`.
- No numerical result appears in this package.
