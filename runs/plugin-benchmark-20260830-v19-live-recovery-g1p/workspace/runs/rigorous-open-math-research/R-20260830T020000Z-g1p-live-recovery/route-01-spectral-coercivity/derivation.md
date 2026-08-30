# Exact two-point semiseparable reduction

## 1. Accepted notation

Let `L=1/2`. On `[0,L]`, let `v_1` be the normalized first Dirichlet half-eigenfunction at

```text
lambda_2=mu_1^D,
```

and let `w_2` be the normalized second Neumann half-eigenfunction at

```text
lambda_3=mu_2^N.
```

Set `c^2=lambda_2/lambda_3`, `epsilon_1=1`, `epsilon_2=-1`, and `E=diag(epsilon_1,epsilon_2)`. At the two left-half switches, the accepted band identity is

```text
w_2(x_j)=epsilon_j c v_1(x_j), j=1,2.
```

Strict Sturm separation implies `v_1(x_j)!=0`, so all congruences below are valid.

The full eigenfunction restriction `u_2|_[0,L]` and `v_1` solve the same simple half-eigenvalue problem, so there is a fixed nonzero scalar `tau` with

```text
u_2(x)=tau v_1(x), 0<=x<=L.
```

Thus an entry identity after normalization by `v_1(x_j)` is equivalent, up to the common positive factor `tau^(-2)`, to the same identity after normalization by the actual sector values `u_j=u_2(x_j)`.

## 2. One-dimensional Green factorization

Fix a spectral parameter which is not an eigenvalue for the stated boundary problem. Let `s` solve the homogeneous equation and the left Dirichlet condition, and let `r_B` solve the same equation and the right boundary condition `B`. The ordinary Green kernel has the standard factorization

```text
G_B(x,y)=C_B s(min(x,y)) r_B(max(x,y)),
```

where the nonzero constant `C_B` is the reciprocal Wronskian with the sign fixed by the convention `(-d^2/dx^2-lambda rho)G=delta`. Only separability, not the sign of `C_B`, is used below.

At `lambda_3=mu_2^N`, the left solution for the Dirichlet cross Green kernel is proportional to `w_2`. Absorb the proportionality into `C_D`. Thus, for `i<=j`,

```text
G_D(x_i,x_j)=C_D w_2(x_i) r_D(x_j).
```

At `lambda_2=mu_1^D`, the left solution for the Neumann cross Green kernel is proportional to `v_1`. Absorb the proportionality into `C_N`. Thus, for `i<=j`,

```text
G_N(x_i,x_j)=C_N v_1(x_i) r_N(x_j).
```

Both cross parameters lie off the spectrum of the stated boundary problem by strict Dirichlet-Neumann interlacing, so both factorizations are legitimate.

## 3. Semiseparable theorem

Define

```text
H=E G_D E-c^2 G_N.
```

For `i<=j`, the band identity gives

```text
H_ij
	=epsilon_i epsilon_j C_D w_2(x_i)r_D(x_j)
		-c^2 C_N v_1(x_i)r_N(x_j)
	=v_1(x_i)h_j,
```

where

```text
h_j=epsilon_j c C_D r_D(x_j)-c^2 C_N r_N(x_j).
```

Put

```text
a=h_1/v_1(x_1),
b=h_2/v_1(x_2).
```

Since `H` is symmetric,

```text
diag(v_1(x_1),v_1(x_2))^(-1)
	H
	diag(v_1(x_1),v_1(x_2))^(-1)
	=[[a,b],[b,b]].
```

Equivalently, the exact entry identity is

```text
H_12/(v_1(x_1)v_1(x_2))=H_22/v_1(x_2)^2.
```

Consequently there are real scalars, renamed `a,b`, such that for the actual sector diagonal `U=diag(u_1,u_2)`,

```text
U^(-1) H U^(-1)=[[a,b],[b,b]].
```

No spectral-tail truncation or numerical approximation occurs.

## 4. Strict sign of `b`

Choose `v_1>0` on `(0,L)`. Then the band identity gives

```text
w_2(x_1)>0,
w_2(x_2)<0.
```

The second Neumann half-eigenfunction has exactly one interior zero, hence that zero lies in `(x_1,x_2)` and `w_2` has no zero on `[x_2,L]`. On the final density-`R` layer put

```text
k_2=sqrt(lambda_2 R),
k_3=sqrt(lambda_3 R),
ell=L-x_2,
theta_j=k_j ell.
```

There are nonzero constants `A,B` with

```text
v_1(x)=B sin(k_2(L-x)),
w_2(x)=A cos(k_3(L-x)).
```

The zero-free statements and `k_2=c k_3` give

```text
0<theta_3<pi/2,
0<theta_2=c theta_3<pi/2.
```

Using the right Dirichlet solution `sin(k_3(L-x))/k_3` at `lambda_3`, the exact diagonal cross Green value is

```text
G_D(x_2,x_2;lambda_3)=sin(theta_3)cos(theta_3)/k_3>0.
```

Using the right Neumann solution `cos(k_2(L-x))` at `lambda_2`, the exact diagonal cross Green value is

```text
G_N(x_2,x_2;lambda_2)=-sin(theta_2)cos(theta_2)/k_2<0.
```

These signs agree with the spectral convention `sum phi_m(x)phi_m(y)/(mu_m-lambda)`. Therefore

```text
H_22=G_D(x_2,x_2;lambda_3)-c^2G_N(x_2,x_2;lambda_2)>0,
b=H_22/u_2(x_2)^2>0.
```

More explicitly,

```text
b=[sin(theta_3)cos(theta_3)/k_3
	+c^2 sin(theta_2)cos(theta_2)/k_2]/u_2(x_2)^2>0.
```

All inequalities are strict because the branch is finite-interior and neither half eigenfunction vanishes at a switch.

## 5. Exact KP reduction

The accepted sector formula is

```text
Kp_odd=diag(d)+2 lambda_2 diag(u)Hdiag(u),
u_j=u_2(x_j),
d_j=-2c|W(x_j)|/(R-1)<0.
```

Define

```text
gamma_j=-d_j/(2 lambda_2 u_j^4)
	=c|W(x_j)|/(lambda_2(R-1)u_j^4)>0.
```

Congruence by the invertible diagonal matrix `U^2=diag(u_1^2,u_2^2)` and division by the positive number `2 lambda_2` give

```text
(2 lambda_2)^(-1)U^(-2)Kp_odd U^(-2)
	=M=[[a-gamma_1,b],[b,b-gamma_2]].
```

Therefore `KP-DET` is equivalent to

```text
(a-gamma_1)(b-gamma_2)-b^2>0
```

together with the negative-inertia anchor. Pointwise negative definiteness is equivalently

```text
a-gamma_1<0,
(a-gamma_1)(b-gamma_2)-b^2>0.
```

The quadratic form has the exact square-coordinate expression

```text
z^T M z
	=b(z_1+z_2)^2
	+(a-b)z_1^2
	-gamma_1 z_1^2
	-gamma_2 z_2^2.
```

This isolates the two signed Green quantities `b` and `a-b`.

## 6. Equality and first-zero cases

If `det Kp_odd=0`, then `det M=0`. If `M` is not the zero matrix, every null vector is proportional to either

```text
(b,gamma_1-a)
```

or

```text
(gamma_2-b,b),
```

with the nonzero choice selected according to which row is nonzero. The exceptional double-zero case is exactly

```text
b=0,
a=gamma_1,
gamma_2=0.
```

It is impossible here because `gamma_2>0`. Hence the exact positive diagonal penalty rules out the double-zero matrix for `M`, and therefore rules out `Kp_odd=0`, at every finite-interior point. Any first zero of `KP-DET` must be corank one.

At a first loss from the negative-definite component, `M` is negative semidefinite and singular. Since `b>0`, both diagonal entries are strictly negative and the kernel is spanned by

```text
(b,gamma_1-a),
```

whose two entries are strictly positive. Congruence by the positive diagonal `U^2` preserves component signs. Thus the first-zero null vector for `Kp_odd` has two nonzero components of the same sign. Equivalently, any first zero must satisfy

```text
gamma_2>b,
gamma_1-a=b^2/(gamma_2-b).
```

This last exclusion is a strict improvement over the two alternatives left open in `direct_attempt.md`.

## 7. Remaining analytic task

The unresolved claim is the scalar inequality

```text
gamma_2>b,
gamma_1-a>b^2/(gamma_2-b)
```

on the compact middle branch. If `gamma_2<=b` at a point, the lower-right quadratic value is already nonnegative, so that point is outside the negative-definite component. The exact first-zero exclusion problem is therefore only the displayed positive-cone equality, not an arbitrary two-dimensional kernel equation.

The structural information obtained here does not itself imply the strict inequality. The abstract scalar assignment

```text
a=0,
b=1,
gamma_1=1,
gamma_2=2
```

obeys `b>0`, `gamma_j>0`, and gives

```text
M=[[-1,1],[1,-1]],
```

which is negative semidefinite of corank one. This algebraic witness is not claimed to arise from the Sturm-Liouville branch. It shows exactly why a further branch-specific estimate is load-bearing: one must control `a` and the normalized Wronskian penalties strongly enough to rule out

```text
gamma_1-a=b^2/(gamma_2-b).
```

The exact last-layer formula determines the sign of `b` but contains neither `a=H_11/u_1^2` nor enough global normalization information to establish that comparison. Therefore the bounded spectral-coercivity route terminates as `PARTIAL`.
