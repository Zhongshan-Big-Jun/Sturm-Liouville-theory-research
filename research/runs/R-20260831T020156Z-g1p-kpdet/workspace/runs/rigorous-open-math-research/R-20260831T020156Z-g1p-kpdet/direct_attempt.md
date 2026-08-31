# Direct closure-first attempt

## 1. Reused strict frontier

The prior audited package proves

```text
M=[[a_0-gamma_1,b_0],[b_0,b_0-gamma_2]],
b_0>0,
gamma_1,gamma_2>0,
```

and identifies a first zero with a same-sign corank-one kernel. The direct
attempt asks whether one diagonal sign can be closed globally before any worker
is dispatched.

## 2. Final-layer phase normalization

On the last half-layer `[b,L]`, the density is `R`. Put

```text
k_2=sqrt(lambda_2 R),
k_3=sqrt(lambda_3 R),
c=k_2/k_3,
theta_j=k_j(L-b).
```

The half-mode boundary conditions give nonzero constants `A,B` such that

```text
v(x)=B sin(k_2(L-x)),
w(x)=A cos(k_3(L-x)).
```

The ground-mode positivity, the absence of a zero of `w` on `[b,L]`, and
`w(b)=-c v(b)<0` allow `B>0`, `A<0`, and imply

```text
0<theta_3<pi/2,
0<theta_2=c theta_3<pi/2.
```

For `Q=w/v`, the band condition at `b` yields

```text
A/B=-c sin(theta_2)/cos(theta_3).
```

Differentiating with respect to `x` gives the exact strict formula

```text
Q'(b)=-c[k_3 tan(theta_3)+k_2 cot(theta_2)]<0.   (1)
```

## 3. Exact lower-right Green coefficient

The ordinary cross Green values in the prior normalization are

```text
G_D(b,b;lambda_3)=sin(theta_3)cos(theta_3)/k_3,
G_N(b,b;lambda_2)=-sin(theta_2)cos(theta_2)/k_2.
```

Since `u_2(b)^2=v(b)^2/2`, the semiseparable coefficient is

```text
b_0=2/[v(b)^2 k_3]
  [sin(theta_3)cos(theta_3)
   +c sin(theta_2)cos(theta_2)].                 (2)
```

This recovers `b_0>0` without a spectral truncation.

## 4. Strict theorem: gamma_2>b_0 everywhere

The Wronskian conventions give

```text
Q'=W/u_2^2,
gamma_2=-2c Q'(b)/[lambda_2 tau v(b)^2].
```

Using `(1)`, `c^2/lambda_2=R/k_3^2`, and `k_2=c k_3`, we obtain

```text
gamma_2-b_0=2/[v(b)^2 k_3] * Delta,

Delta=R/tau[tan(theta_3)+c cot(theta_2)]
  -[sin(theta_3)cos(theta_3)
    +c sin(theta_2)cos(theta_2)].                 (3)
```

Because `R/tau=1+1/tau>1` and both angles lie in `(0,pi/2)`,

```text
tan(t)-sin(t)cos(t)=sin(t)^3/cos(t)>0,
cot(t)-sin(t)cos(t)=cos(t)^3/sin(t)>0.
```

Every term in `(3)` is therefore strictly positive. Hence

```text
gamma_2>b_0>0.                                  (4)
```

No compactness, endpoint asymptotic, or numerical evidence enters this proof.

## 5. Consequences and exact remaining scalar

The congruence relation gives

```text
(Kp_odd)22=2lambda_2 u_2(b)^4(b_0-gamma_2)<0
```

at every finite-interior branch point. Thus the lower-right pivot can never be
the source of a first loss. The determinant identity becomes

```text
det M=(b_0-gamma_2)
  [a_0-gamma_1+b_0^2/(gamma_2-b_0)].             (5)
```

Since the first factor is strictly negative, KP-DET is equivalent to the single
strict Schur inequality

```text
S_KP:=a_0-gamma_1+b_0^2/(gamma_2-b_0)<0.         (6)
```

Equality in `(6)` is exactly the remaining same-sign Jacobi kernel. The new
theorem removes every hypothetical `gamma_2<=b_0` region globally, rather than
deducing `gamma_2>b_0` only after assuming a first singularity.

## 6. Cheapest falsification and dead-end audit

- The algebraic witness from the prior run does not satisfy the branch phase formulas and cannot refute `(6)`.
- Endpoint anchors remain strict but do not determine the sign of `S_KP` on the compact middle regime.
- A proof based only on `R` differentiation through the full inverse Jacobian remains circular at `S_KP=0`.
- No numerical value is used in the theorem above.

## 7. Decision delta

The direct attempt proves a new branch-uniform diagonal sign and reduces KP-DET
to one everywhere-defined scalar Schur margin. It does not determine the sign
of that margin. A minimal two-route escalation is justified: exact transfer
reduction of `S_KP`, and independent Jacobi or counterexample analysis of the
same equality.
