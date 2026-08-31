# Jacobi falsification route

RIGOROUS_PARTIAL_RESULT

## 1. Scope and conventions

Work only on the prescribed finite-interior `n=2` symmetric INF half-string
branch. Put

```text
L=1/2,
tau=R-1,
0<a<b<L,
c^2=lambda_2/lambda_3,
v=sqrt(2)u_2|_[0,L],
w=sqrt(2)u_3|_[0,L].
```

The frozen oscillation data are

```text
v>0 on (0,L),
w(a)=c v(a),
w(b)=-c v(b),
Q=w/v,
Q'<0,
```

and `w` has its unique interior zero `z` in `(a,b)`. Suppose, only for the
purpose of extracting necessary consequences, that the remaining Schur
equality holds. The prior audited reduction then supplies a kernel vector
`y=(y_1,y_2)` with

```text
y_1>0,
y_2>0.
```

Let `phi` and `psi` be the corresponding parity-crossing Jacobi fields:

```text
(-d^2/dx^2-lambda_2 rho)phi
	=lambda_2 tau[y_1 v(a)delta_a+y_2 v(b)delta_b],
phi(0)=0,
phi'(L)=0,

(-d^2/dx^2-lambda_3 rho)psi
	=lambda_3 tau[y_1 w(a)delta_a+y_2 w(b)delta_b],
psi(0)=0,
psi(L)=0.
```

The two moving-level conditions are

```text
psi(a)-c phi(a)+y_1 W_h(a)/v(a)=0,
psi(b)+c phi(b)-y_2 W_h(b)/v(b)=0,
```

where `W_h=w'v-wv'=v^2 Q'<0`.

## 2. A common projective flux

Away from `a`, `b`, and the zero of `w`, define

```text
alpha=phi/v,
beta=psi/w.
```

The projective fluxes are

```text
P_v=v^2 alpha'=v phi'-phi v',
P_w=w^2 beta'=w psi'-psi w'.
```

On each open density cell they are constant. Across a source `x_j`, the
Jacobi equations give

```text
[phi']_(x_j)=-lambda_2 tau y_j v(x_j),
[psi']_(x_j)=-lambda_3 tau y_j w(x_j).
```

Therefore

```text
[P_v]_(x_j)=-lambda_2 tau y_j v(x_j)^2,
[P_w]_(x_j)=-lambda_3 tau y_j w(x_j)^2.
```

At both switches, `w(x_j)^2=c^2v(x_j)^2` and
`lambda_3c^2=lambda_2`. The two flux jumps are consequently equal. Before
the first source, `phi` is a constant multiple of `v` and `psi` is a
constant multiple of `w`, because each pair solves the same homogeneous
equation and vanishes at `0`. Hence both fluxes vanish there. It follows
without any determinant or branch derivative that

```text
P_v=P_w=:P,

P(x)=0,                                      0<x<a,
P(x)=-lambda_2 tau y_1 v(a)^2,               a<x<b,
P(x)=-lambda_2 tau[y_1v(a)^2+y_2v(b)^2],     b<x<L.       (PF)
```

This identity is valid through the simple zero of `w` in the Wronskian
form, even though `beta` itself has a pole there.

## 3. The exact quotient geometry forced by a same-sign kernel

Set `delta=beta-alpha` where it is defined and set

```text
h=v psi-w phi=vw delta.
```

Dividing the moving-level conditions by `cv(a)` and `-cv(b)` respectively
gives

```text
delta(a)=-y_1 Q'(a)/c>0,
delta(b)=-y_2 Q'(b)/c>0.                       (L)
```

From `(PF)`,

```text
delta'=P(1/w^2-1/v^2).                         (D)
```

Since `Q` decreases strictly from `c` to `-c` on `[a,b]`,

```text
|w|<v
```

there. Thus `delta'<0` on both `(a,z)` and `(z,b)`. At `z`, the common
flux satisfies

```text
P=-psi(z)w'(z).
```

Here `P<0` and `w'(z)<0`, so

```text
psi(z)<0.                                      (Z)
```

Consequently `beta`, and hence `delta`, tends to `-infinity` from the left
of `z` and to `+infinity` from the right. Equations `(L)` and `(D)` now show
that there is exactly one point

```text
xi in (a,z)
```

such that `delta(xi)=0`. It is a simple downward crossing. Indeed,

```text
h(xi)=0,
h'(xi)=P[v(xi)^2-w(xi)^2]/[v(xi)w(xi)]<0.       (LOCK)
```

There are no other zeros of `h`. On `(0,a]`, `P=0`, so `delta` is the
positive constant `delta(a)`. On `(z,b]`, `delta` decreases from
`+infinity` to the positive number `delta(b)`. On the final layer, write
with `t=L-x`

```text
v=B sin(k_2t),
w=A cos(k_3t),
phi=C cos(k_2t),
psi=D sin(k_3t),
```

where `B>0`, `A<0`, `0<k_3t<=theta_3<pi/2`, and
`0<k_2t<=theta_2<pi/2`. The common negative flux gives

```text
P=BCk_2=-ADk_3<0,
```

so `C<0` and `D<0`. Hence `alpha<0<beta` on `[b,L)`. Thus `h<0` from
`z` through `L`, whereas `h>0` from `0` through `a`.

The locking point has the branch-only integral characterization

```text
-Q'(a)/c
	=lambda_2 tau v(a)^2
	 int_a^xi [1/w(x)^2-1/v(x)^2] dx.             (I-LOCK)
```

The right side increases from `0` to `+infinity` as `xi` moves from `a`
to `z`. Therefore `(I-LOCK)` is always solvable and does not itself exclude
the kernel. This is the exact reason why quotient monotonicity alone cannot
close `KP-DET`.

## 4. Independent audit of the theorem `gamma_2>b_0`

On `[b,L]`, put

```text
k_2=sqrt(lambda_2R),
k_3=sqrt(lambda_3R),
theta_j=k_j(L-b).
```

The mode indices and signs give

```text
0<theta_3<pi/2,
theta_2=c theta_3 in (0,pi/2),
v=B sin(k_2(L-x)),
w=A cos(k_3(L-x)),
B>0,
A<0.
```

The level condition at `b` gives

```text
A/B=-c sin(theta_2)/cos(theta_3).
```

Direct differentiation therefore yields

```text
Q'(b)=-c k_3[tan(theta_3)+c cot(theta_2)]<0.     (Qb)
```

The signs of the two cross Green kernels can be checked without a spectral
series. For the Dirichlet cross problem at `lambda_3`, use the left
Neumann eigenfunction `cos(k_3(L-x))` and the endpoint-normalized right
Dirichlet solution `sin(k_3(L-x))/k_3`. For the Neumann cross problem at
`lambda_2`, use the left Dirichlet eigenfunction `sin(k_2(L-x))` and the
right Neumann solution `cos(k_2(L-x))`. The derivative jump convention for
`-d^2/dx^2-lambda rho` gives

```text
G_D(b,b;lambda_3)=sin(theta_3)cos(theta_3)/k_3,
G_N(b,b;lambda_2)=-sin(theta_2)cos(theta_2)/k_2.
```

Since `u_2(b)^2=v(b)^2/2` and `k_2=ck_3`, the normalized lower-right
Green coefficient is

```text
b_0=2/[v(b)^2k_3]
	[sin(theta_3)cos(theta_3)
	 +c sin(theta_2)cos(theta_2)].                 (b0)
```

Also, the frozen Wronskian normalization gives

```text
gamma_2=-2cQ'(b)/[lambda_2 tau v(b)^2].
```

Using `(Qb)`, `c^2=lambda_2/lambda_3`, and
`k_3^2=lambda_3R`, one obtains

```text
gamma_2-b_0=2/[v(b)^2k_3] Delta,

Delta=R/tau[tan(theta_3)+c cot(theta_2)]
	-[sin(theta_3)cos(theta_3)
	  +c sin(theta_2)cos(theta_2)].                (Delta)
```

For `0<t<pi/2`,

```text
tan(t)-sin(t)cos(t)=sin(t)^3/cos(t)>0,
cot(t)-sin(t)cos(t)=cos(t)^3/sin(t)>0.
```

Since `R/tau>1`, every part of `Delta` is strictly positive. Therefore

```text
gamma_2>b_0>0.                                  (AUDIT-KP22)
```

The independent audit verdict for this theorem is `PASS`. All angle ranges,
Green signs, normalization factors, and strict inequalities agree with the
contract.

## 5. Endpoint ratio check for a hypothetical kernel

The common flux gives an additional exact consistency check on the second
kernel row. On the final layer, the representations in Section 3 imply at
`b`

```text
alpha(b)=P sin(theta_2)cos(theta_2)/[v(b)^2c k_3],
beta(b)=-P sin(theta_3)cos(theta_3)/[v(b)^2c^2 k_3].
```

Substitute

```text
P=-lambda_2 tau[y_1v(a)^2+y_2v(b)^2]
```

and equate `beta(b)-alpha(b)` with the second equation in `(L)`. This gives

```text
y_1v(a)^2/[y_2v(b)^2]
	=R/tau
	 [tan(theta_3)+c cot(theta_2)]
	 /[sin(theta_3)cos(theta_3)
	   +c sin(theta_2)cos(theta_2)]-1
	=(gamma_2-b_0)/b_0>0.                         (RATIO)
```

Thus the Jacobi flux calculation independently recovers the exact positive
kernel ratio forced by the normalized matrix. It finds no sign
contradiction.

## 6. Decision

The direct theorem `gamma_2>b_0` passes independent audit. A hypothetical
same-sign kernel must satisfy the new exact projective-flux law `(PF)`, the
unique locking-point theorem `(LOCK)`, the branch-only location formula
`(I-LOCK)`, and the endpoint ratio `(RATIO)`.

These conditions are mutually compatible. In particular, `(I-LOCK)` always
has a unique solution before the zero of `w`. Pure Sturm comparison and
quotient monotonicity therefore do not exclude `S_KP=0`.

No exact branch-realizable witness was constructed. The exact remaining gap
is the sign of the first-switch level residual after the positive ratio
`(RATIO)` is propagated through the middle layer. Proving its strict sign, or
constructing an exact zero satisfying the full transfer, band, normalization,
and mode-index conditions, is still required.

No numerical evidence is used.
