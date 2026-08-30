# Derivation of the half-string Jacobi condition

## 1. Reflection-adapted branch coordinates

At a symmetric finite-interior point write

```text
(x_1,x_2,x_3,x_4)=(a,b,1-b,1-a),
0<a<b<L=1/2.
```

Use local coordinates `(a,b,p,q)` defined by

```text
x_1=a+p,
x_2=b+q,
x_3=1-b+q,
x_4=1-a+p.
```

Reflection fixes `(a,b)` and sends `(p,q)` to `(-p,-q)`. The kernel coordinate used below is

```text
p=t y_1,
q=-t y_2.
```

For INF, the left switch jumps are `s_1=-tau`, `s_2=+tau`, where `tau=R-1`. Since a moving switch contributes `dot(rho)=-s_j dot(x_j)delta_(x_j)`, the left-half perturbation is

```text
dot(rho)=tau[y_1 delta_a+y_2 delta_b].          (1)
```

The full perturbation is reflection-odd. Since every squared base eigenfunction is reflection-even,

```text
dot(lambda_k)=-lambda_k int_0^1 dot(rho)u_k^2 dx=0,
k=2,3,                                           (2)
```

and hence `dot(c)=0`.

## 2. Half eigenfunctions and oscillation anchors

Set

```text
v=sqrt(2)u_2|_[0,L],
w=sqrt(2)u_3|_[0,L].
```

The half normalization is `int_0^L rho v^2=int_0^L rho w^2=1`. Full parity gives

```text
v(0)=v(L)=0,
w(0)=0,
w'(L)=0.
```

For `n=2`, `v` is the ground Dirichlet-Dirichlet mode and is positive on `(0,L)`. The function `w` is the second Dirichlet-Neumann mode and has exactly one zero `z` in `(0,L)`. The cell structure gives

```text
a<z<b,
w(a)=c v(a),
w(b)=-c v(b).
```

The half Wronskian

```text
W_h=w'v-wv'=2W
```

is strictly negative. Therefore the quotient `Q=w/v` obeys

```text
Q'=W_h/v^2<0,
Q(a)=c,
Q(b)=-c.                                        (3)
```

The half spectra interlace as

```text
mu_1^N<mu_1^D=lambda_2<mu_2^N=lambda_3<mu_2^D. (4)
```

This is the endpoint and oscillation input that makes both cross-boundary Jacobi operators below invertible, even though the full band Jacobian may be singular.

## 3. Parity-crossing Jacobi fields

The variation of the full odd mode `u_2` under the reflection-odd density perturbation is reflection-even. Its half restriction `phi=dot(v)` therefore has a Neumann condition at `L`. The variation of the full even mode `u_3` is reflection-odd, so `psi=dot(w)` has a Dirichlet condition at `L`. Differentiating the eigenvalue equations and using `(1)` and `(2)` gives

```text
L_2 phi=lambda_2 tau sum_k y_k v_k delta_(x_k),
phi(0)=0,
phi'(L)=0,

L_3 psi=lambda_3 tau sum_k y_k w_k delta_(x_k),
psi(0)=0,
psi(L)=0,                                        (5)
```

where `L_k=-d^2/dx^2-lambda_k rho`, `(x_1,x_2)=(a,b)`, and `v_k=v(x_k)`, `w_k=w(x_k)`. By `(4)`, these problems have unique solutions. In the exact Green convention of the frozen addendum,

```text
phi=lambda_2 tau G_N diag(v)y,
psi=lambda_3 tau G_D diag(w)y
	=lambda_3 tau c G_D E diag(v)y,               (6)
```

with `E=diag(1,-1)`.

## 4. Differentiation of the band equations

On the left half,

```text
F_j=[lambda_2 v(x_j)^2-lambda_3 w(x_j)^2]/(2lambda_3).
```

At a band point, `w_j=e_j c v_j`. The total derivative includes the motion of the evaluation point:

```text
dot(F_j)=dot(x_j)f'(x_j)/lambda_3
	+(lambda_2/lambda_3)v_j phi_j-w_j psi_j.       (7)
```

For INF,

```text
s_j=-tau e_j,
d_j=f'(x_j)/(lambda_3 s_j)
	=-2c|W(x_j)|/tau,
dot(x_j)=e_j y_j.                               (8)
```

Substituting `(6)` and `(8)` into `(7)`, and using `lambda_3 c^2=lambda_2`, gives

```text
dot(F)|_(1,2)
=-tau{diag(d)
	+lambda_2 diag(v)[E G_D E-c^2 G_N]diag(v)}y
=-tau Kp_odd y.                                  (9)
```

The last equality uses `v=sqrt(2)u_2`, so the bracket equals the frozen full-normalization formula

```text
diag(d)+2lambda_2 diag(u)[G_D o (ee^T)-c^2G_N]diag(u).
```

This proves `(T-KP)` without differentiating a branch as a function of `R` and without inverting `J`.

## 5. Quotient form of the Jacobi condition

Since `Q=w/v`, its field variation at fixed `x` is

```text
dot(Q)=(psi-Q phi)/v.
```

The moving switch remains on the level `Q=e_j c` to first order exactly when

```text
0=dot(Q)(x_j)+Q'(x_j)dot(x_j)-e_j dot(c).
```

Using `(2)`, `(3)`, and `dot(x_j)=e_j y_j`, this is

```text
psi(x_j)-e_j c phi(x_j)
	+e_j y_j W_h(x_j)/v(x_j)=0.                  (10)
```

Equations `(9)` and `(10)` are equivalent because at a band point the residual is a nonzero scalar multiple of `Q-e_j c`. The factors `v(x_j)` and `W_h(x_j)` are nonzero by the Sturm and Wronskian facts above.

## 6. Exact transfer-matrix transversality form

For a constant density value `rho_0`, define

```text
T_(rho_0)(lambda,l)
= [[cos(k l), sin(k l)/k],
	[-k sin(k l), cos(k l)]],
k=sqrt(lambda rho_0).
```

The half-string transfer matrix is

```text
T(lambda;a,b)
=T_R(lambda,L-b)T_1(lambda,b-a)T_R(lambda,a).  (11)
```

The two simple eigenvalues are selected by

```text
T(lambda_2;a,b)_(1,2)=0,
T(lambda_3;a,b)_(2,2)=0,                       (12)
```

with the oscillation indices fixed by `(4)`. If `Y_D(x,lambda)` and `Y_N(x,lambda)` are the solutions with initial data `(0,1)` selected at `lambda_2` and `lambda_3`, and `I_D,I_N` are their exact weighted squared norms, then

```text
v=Y_D/sqrt(I_D),
w=Y_N/sqrt(I_N),
Q=w/v,
c=sqrt(lambda_2/lambda_3),
Q(a)=c,
Q(b)=-c.                                       (13)
```

Equations `(11)` to `(13)` provide a branch chart that does not divide by `det J`. Extending the full four-switch transfer product in the transverse coordinates `(p,q)`, the two antisymmetric band residuals have transverse derivative `-tau Kp_odd` by `(9)`. Hence

More explicitly, for the full switch chart of Section 1 define

```text
A(R,a,b,p,q)
=((F_1-F_4)/2,(F_2-F_3)/2).
```

Reflection makes `A(R,a,b,0,0)=0`. Since `(p,q)=E y`, equation `(9)` is exactly

```text
D_(p,q)A=-tau Kp_odd E,
det D_(p,q)A=-tau^2 det Kp_odd.                 (13a)
```

Thus the exact transfer-matrix transversality condition is `det D_(p,q)A!=0`. Its failure is precisely `det Kp_odd=0`.

Hence

```text
det Kp_odd=0
```

is exactly the failure of transfer-matrix transversality in the reflection-breaking directions, not a failure of the half spectral parameterization `(12)`.

For completeness, define the symmetric residual map

```text
S(R,a,b)=(F_1,F_2)
```

on the symmetric embedding

```text
X_s(a,b)=(a,b,1-b,1-a).
```

Let `B_e,B_o` be the normalized palindromic and anti-palindromic pair bases. Then

```text
dX_s=sqrt(2)B_o d(a,b),
K B_o=B_o Ko,
diag(s)B_o=B_e diag(-tau,+tau)=-tau B_e E.
```

Since `J=diag(s)K`, the left two components of `J dX_s` give the exact identity

```text
D_(a,b)S=-tau E Ko.                            (14)
```

Thus, if `Ko` is nonsingular at a `Kp_odd` first-zero candidate, the symmetric branch has an analytic local parameterization through that point by the implicit function theorem applied to `S`, irrespective of the singularity of the full `J`. Differentiating `S(R,a(R),b(R))=0` yields

```text
(a',b')^T=tau^(-1)Ko^(-1)E S_R.               (15)
```

This is the promised non-circular branch derivative. It uses the still-regular symmetric sector `Ko`, not the singular transverse sector `Kp_odd`.

## 7. Corank-one and double-zero audit

Because `Kp_odd` is symmetric and two dimensional:

- `det Kp_odd=0` and `Kp_odd!=0` is equivalent to a one-dimensional space of impulse vectors satisfying `(5)` and `(10)`.
- `Kp_odd=0` is equivalent to both canonical impulse vectors satisfying `(5)` and `(10)`, so the entire first transverse derivative of the antisymmetric band map vanishes.

The cross operators in `(5)` remain invertible in both cases. Therefore singularity of the band map cannot be attributed to a pole of either half Green function. The remaining issue is a two-point response transversality inequality, not existence of the Jacobi fields.

### Strict off-diagonal sign and exclusion of double zero

Take the canonical impulse `y=(0,1)`. On `(0,b)`, before its only source, uniqueness for the homogeneous initial-value equations gives

```text
phi=A v,
psi=B w.                                        (16)
```

Let `r_N` solve

```text
L_2 r_N=0,
r_N(L)=1,
r_N'(L)=0.
```

The solution at the larger parameter `lambda_3` with the same right Neumann data is a nonzero multiple of `w` and has its first zero to the left of `L` at `z`. Sturm comparison, applied from `L` toward `0`, places the first zero of `r_N` strictly to the left of `z`. Hence

```text
r_N(b)>0.                                       (17)
```

For `x>b`, write `phi=C r_N`. Continuity at `b` and the derivative jump

```text
phi'(b+)-phi'(b-)=-lambda_2 tau v(b)
```

give

```text
A=lambda_2 tau v(b)/D_v,
D_v=v'(b)-[r_N'(b)/r_N(b)]v(b).
```

The Wronskian identity

```text
D_v=-W(v,r_N)(b)/r_N(b),
W(v,r_N)(L)=-v'(L)>0
```

and `(17)` show `D_v<0`, and therefore

```text
A<0.                                            (18)
```

Next let `r_D` solve

```text
L_3 r_D=0,
r_D(L)=0,
r_D'(L)=-1.
```

It is positive immediately to the left of `L`. The functions `r_D` and `w` are linearly independent solutions of the same equation. Since `w` has no zero in `(z,L)` and `r_D(L)=0`, Sturm separation forbids another zero of `r_D` in `(z,L)`. Therefore

```text
r_D(b)>0.                                       (19)
```

For `x>b`, write `psi=C_D r_D`. The jump

```text
psi'(b+)-psi'(b-)=-lambda_3 tau w(b)
```

gives

```text
B=lambda_3 tau w(b)/D_w,
D_w=w'(b)-[r_D'(b)/r_D(b)]w(b).
```

Again,

```text
D_w=-W(w,r_D)(b)/r_D(b),
W(w,r_D)(L)=-w(L)>0.
```

Since `w(b)=-c v(b)<0`, `(19)` implies `D_w<0` and hence

```text
B>0.                                            (20)
```

At `a`, the switch itself does not move for this canonical impulse. Using `w(a)=cv(a)`, equations `(16)`, `(18)`, and `(20)` yield

```text
dot(F_1)=c^2 v(a)^2[A-B]<0.
```

But `(9)` gives `dot(F_1)=-tau(Kp_odd)12`. Thus

```text
(Kp_odd)12>0.                                   (21)
```

In particular `Kp_odd` can never be the zero matrix. At a first loss it is nonzero negative semidefinite, hence has corank exactly one. Its diagonal entries are strictly negative, and its kernel vector has components of the same nonzero sign.

If `Ko` is nonsingular, `(14)` supplies an analytic matrix path `Kp_odd(R)` through the candidate. In the corank-one case, standard analytic perturbation for symmetric matrices gives an analytic zero eigenvalue branch `kappa` and

```text
kappa'(R_*)=y_*^T Kp_odd'(R_*)y_*,

Kp_odd'=partial_R Kp_odd
	+partial_a Kp_odd a'
	+partial_b Kp_odd b',
```

where `(a',b')` is given by `(15)`. Negative definiteness for `R<R_*` forces `kappa'(R_*)>0` when the root is first order. If this derivative vanishes, let `m` be the first order with `kappa^(m)(R_*)!=0`; the exact one-sided requirement is

```text
(-1)^m kappa^(m)(R_*)<0.
```

The double-zero Taylor alternative is eliminated by `(21)`. The remaining scalar crossing-form signs have not been established by the present route.
