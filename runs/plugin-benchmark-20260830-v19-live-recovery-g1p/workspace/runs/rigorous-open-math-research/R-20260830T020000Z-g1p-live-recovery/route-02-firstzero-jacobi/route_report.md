RIGOROUS_PARTIAL_RESULT

# Route 02 report: first-zero Jacobi realization

## Current status

- Route state: `PARTIAL`.
- Decision delta: the algebraic kernel equation for `Kp_odd` is now realized as an exact half-string Jacobi boundary value problem and as the transverse derivative of an explicit reflection-adapted branch chart. No inverse of the full Jacobian is used.
- Scope: only the hypothetical finite-interior first loss of `KP-DET` on the prescribed `n=2` symmetric INF branch.

## Exact theorem obtained

Let `L=1/2`, `tau=R-1`, and let the left-half INF density be `R,1,R` with switches `0<a<b<L`. Let `v=sqrt(2)u_2|_[0,L]` and `w=sqrt(2)u_3|_[0,L]`. Then `v` is the half-normalized first Dirichlet-Dirichlet eigenfunction at `lambda_2`, while `w` is the half-normalized second Dirichlet-Neumann eigenfunction at `lambda_3`. With

```text
c^2=lambda_2/lambda_3,
e=(1,-1),
w(a)=c v(a),
w(b)=-c v(b),
W_h=w'v-wv'=2W<0,
```

define, for `y=(y_1,y_2)`, the reflection-transverse switch curve

```text
x_1(t)=a+t y_1,
x_2(t)=b-t y_2,
x_3(t)=1-b-t y_2,
x_4(t)=1-a+t y_1.
```

Its density derivative is reflection-odd, and on the left half equals

```text
dot(rho)=tau[y_1 delta_a+y_2 delta_b].
```

Consequently `dot(lambda_2)=dot(lambda_3)=dot(c)=0`. The unique parity-crossing Jacobi fields `phi=dot(v)` and `psi=dot(w)` satisfy

```text
(-d^2/dx^2-lambda_2 rho)phi
	=lambda_2 tau sum_k y_k v(x_k)delta_(x_k),
phi(0)=0,
phi'(L)=0,

(-d^2/dx^2-lambda_3 rho)psi
	=lambda_3 tau sum_k y_k w(x_k)delta_(x_k),
psi(0)=0,
psi(L)=0,
```

where `(x_1,x_2)=(a,b)`. The cross problems are uniquely solvable because

```text
mu_1^N<lambda_2=mu_1^D<lambda_3=mu_2^N<mu_2^D.
```

For the two left band residuals `F_j=f(x_j)/lambda_3`, their exact transverse derivative is

```text
dot(F)|_(j=1,2)=-tau Kp_odd y.                 (T-KP)
```

Equivalently,

```text
Kp_odd y=0
```

if and only if the Jacobi fields obey the two linearized level conditions

```text
psi(x_j)-e_j c phi(x_j)
	+e_j y_j W_h(x_j)/v(x_j)=0,
j=1,2.                                         (J-KP)
```

This equivalence is exact and remains valid at `det Kp_odd=0`.

If the antisymmetric transfer residual is

```text
A=((F_1-F_4)/2,(F_2-F_3)/2)
```

in transverse coordinates `(p,q)=(y_1,-y_2)`, then

```text
D_(p,q)A=-tau Kp_odd E,
det D_(p,q)A=-tau^2 det Kp_odd.
```

This is the exact transfer-matrix transversality condition.

There is also a non-circular local parameterization of the symmetric branch at a `KP-DET` singularity. Let

```text
S(R,a,b)=(F_1,F_2)
```

be the left residual map evaluated on `(a,b,1-b,1-a)`. If `Ko` is nonsingular, then

```text
D_(a,b)S=-tau E Ko,
E=diag(1,-1).                                  (B-KO)
```

Hence the implicit function theorem parameterizes `(a,b)` analytically by `R` through a corank-one or double-zero singularity of `Kp_odd`. This uses only `Ko^(-1)`, which remains legitimate when `KP-DET` is the strictly first sector loss. Along that chart,

```text
(a',b')^T=tau^(-1)Ko^(-1)E S_R,                (P-KO)
```

and `Kp_odd'(R)` is well-defined without `J^(-1)`.

## First-zero alternatives

At a hypothetical first loss, `Kp_odd` is negative semidefinite.

- The off-diagonal entry satisfies the strict global sign

```text
(Kp_odd)12>0.                                  (OD-KP)
```

The proof uses only Sturm comparison and separation for the right Neumann solution at `lambda_2` and the right Dirichlet solution at `lambda_3`; it is given in `derivation.md`.
- Therefore the double-zero case `Kp_odd=0` is impossible at every finite-interior symmetric INF branch point.
- Any first zero is necessarily corank one. Its Jacobi kernel is one dimensional. Since the matrix is then nonzero negative semidefinite and its off-diagonal entry is positive, both diagonal entries are strictly negative and every kernel vector has `y_1y_2>0`.

When `Ko` is nonsingular, let `kappa(R)` be the analytic eigenvalue of `Kp_odd(R)` which vanishes in the corank-one case, with unit kernel vector `y_*`. Then

```text
kappa'(R_*)=y_*^T Kp_odd'(R_*) y_*.
```

At a first zero approached from smaller `R`, a first-order zero must satisfy `kappa'(R_*)>0`. Therefore any exact calculation giving `y_*^T Kp_odd'(R_*)y_*<0` excludes a corank-one first loss. If the derivative vanishes, the first nonzero Taylor coefficient supplies the corresponding higher-order one-sided sign condition. This is an exact local transversality certificate, not yet a sign proof.

Thus the double-zero case is excluded, the corank-one case is realized by an exact Jacobi condition, and neither step requires `J^(-1)`.

## Exact remaining gap

The double-zero alternative is closed by `(OD-KP)`. The route has not excluded a corank-one coupled Jacobi field on the compact middle branch. Excluding it requires proving that the two linearized level conditions are transverse, or that the exact crossing form above has the forbidden sign, at every finite interior first-zero candidate. A simultaneous `Kp_odd` and `Ko` singularity is not covered by `(B-KO)` and remains a separate exceptional case.

No numerical conditioning statement is used as proof.

## Verification performed

- Definition audit: re-derived the INF jump signs `s=(-tau,+tau)`, the half normalizations, `w(a)=cv(a)`, `w(b)=-cv(b)`, and the conversion from the frozen full-normalization matrix to `(T-KP)`.
- Logic audit: derived eigenvalue stationarity from reflection parity before constructing the Jacobi fields; no branch derivative or full Jacobian inverse enters `(T-KP)`, `(J-KP)`, or `(OD-KP)`.
- Boundary audit: used the parity-crossed endpoint conditions `phi'(L)=0`, `psi(L)=0`; checked that both cross spectral parameters are strictly between adjacent half eigenvalues, so neither Green operator has a pole.
- Adversarial audit: retained simultaneous `Kp_odd` and `Ko` singularity as an explicit exception to the branch chart; did not promote the corank-one reduction to a proof of `KP-DET`.
- Fresh-files convergence check: the three route files reconstruct a forward delta, namely exact Jacobi and transfer equivalence plus strict exclusion of double zero. They also reconstruct the unchanged corank-one gap without conversational context.

Structured self-audit:

```json
{
	"verdict": "REPAIRABLE_GAP",
	"critical_errors": [],
	"gaps": [
		{
			"location": "corank-one first-zero condition",
			"issue": "No strict sign theorem excludes the remaining one-dimensional Jacobi kernel on the compact middle branch."
		}
	],
	"repair_hints": "Prove sign regularity of the two-point Jacobi response, or evaluate the exact crossing form through the Ko-regular branch chart and show its first-zero sign is impossible.",
	"covered_scope": "n=2 symmetric finite-interior INF branch, KP-DET only, exact first-zero Jacobi and transfer identities, double-zero exclusion",
	"residual_risk": "Simultaneous Kp_odd and Ko singularity and the remaining corank-one Jacobi field are not excluded."
}
```

This audit is author-side, not an independent review.

## Observable counts

- Assigned parent input files read: `6`.
- Authoritative v1.9.0 skill entry files read: `1`.
- Non-authoritative skill version probe files read: `1`.
- Phase reference files read: `5`.
- Web queries: `0`.
- Subagents: `0`.
- Numerical proof premises: `0`.
- Route artifact files written: `3`.
