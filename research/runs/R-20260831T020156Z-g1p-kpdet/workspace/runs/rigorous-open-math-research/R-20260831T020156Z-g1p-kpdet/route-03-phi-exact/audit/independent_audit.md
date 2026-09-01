PASS

# Independent audit W3-AUDIT

## Input integrity and scope

The four supplied SHA-256 hashes match the audit packet exactly. I treated the package as a first-time submission and independently checked every strict identity and sign claim in `coordinator_direct.md` and `worker_result.md`. The open inequality `PHI-SIGN` and the target `KP-DET` are outside the claimed closure.

## Verdict

`PASS`. I found no critical error and no gap in the strict partial claims. The first erroneous step is `none`.

## Definition and domain audit

Write `k=cp`. Then

```text
lambda_3=p^2/m^2,
lambda_2=k^2/m^2.
```

For the right-Neumann shape `y=phi_3`, the left boundary value is

```text
F3=X cos(alpha)-Z sin(alpha)=y(0).
```

For the right-Dirichlet shape `phi_2`, the left boundary value is

```text
F2=Y cos(A)+T sin(A)=phi_2(0),
(A,B,H)=(c alpha,c beta,c theta).
```

The strict modal domain supplies

```text
sin(alpha)>0,
sin(c alpha)>0,
s>0,
C>0,
X<0,
Y=-sX/C>0,
m>1.
```

Thus every division by `sin(alpha)`, `sin(c alpha)`, `s`, `C`, or `X` in the audited package is valid. Also `r=m^2/(m^2-1)>0` is finite. No step divides by a middle-layer sine or cosine, so all interior zero sets of `sin(beta)`, `cos(beta)`, `sin(c beta)`, and `cos(c beta)` remain covered.

The pivot sign is independently recovered from

```text
Dtheta
=r[tan(theta)+c cot(c theta)]-[S C+c s Cc].
```

Indeed,

```text
tan(theta)-S C=S^3/C>0,
cot(c theta)-s Cc=Cc^3/s>0,
r>1,
```

so `Dtheta>0`. The switch-collision and mode-index faces named in the frozen contract are strict-domain boundary faces, and neither audited artifact makes a claim on them.

## Safe spectral elimination

At the two spectral roots,

```text
cot(alpha)=Z/X,
cot(c alpha)=-T/Y=C T/(sX).
```

Therefore, with

```text
K=c C T/s-Z,
U=D-c s N/C,
Psi=X^2 U-rK,
```

one has

```text
Dalpha=rK/X,
Phi=Dtheta Psi/X+X^2 Ttheta^2/C^2.
```

Multiplication by `X` gives the exact identity

```text
Xi=X Phi
  =Dtheta Psi+X^3 Ttheta^2/C^2.
```

Since `X<0`, this proves both directions and the equality case:

```text
Phi<0 if and only if Xi>0,
Phi=0 if and only if Xi=0.
```

No tangent chart in `beta` or `c beta` is introduced. The denominator-free band identity is exactly `CY+sX=0` after substituting the definitions of `X` and `Y`.

## Lagrange signs, scale factors, M3, and M2

For any right-normalized solution `h` of

```text
-h''=lambda rho h,
```

differentiation in `lambda` gives

```text
(h h_lambda'-h' h_lambda)'=-rho h^2.
```

At a left Dirichlet eigenvalue, the right boundary normalization is independent of `lambda`, while `h(0)=0`. Hence

```text
h'(0) h_lambda(0)=-integral_0^L rho h^2 dx.
```

This fixes the sign before any scale conversion.

For `y=phi_3`,

```text
y'(0)=pX/sin(alpha),
E3(F3)=p partial_p F3=(2p^2/m^2)y_lambda(0),
I3hat=p integral_0^L rho y^2 dx.
```

Substitution yields exactly

```text
I3hat=-m^2 X E3(F3)/(2 sin(alpha)).
```

For the Dirichlet shape set `g=phi_2/k`, where `k=cp`. Then

```text
g(L)=0,
g'(L)=-1,
g'(0)=Y/sin(A),
F2=k g(0),
I2hat=k integral_0^L rho phi_2^2 dx
      =k^3 integral_0^L rho g^2 dx.
```

At the spectral root `g(0)=0`, so

```text
E2(F2)=k partial_k F2=k^2 g_k(0),
g_k=(2k/m^2)g_lambda.
```

The same Lagrange identity therefore gives

```text
I2hat=-m^2 Y E2(F2)/(2 sin(A)).
```

Thus the negative signs, factors `m^2`, and factors `1/2` in both `(M3)` and `(M2)` are correct. The use of `E3` and `E2` is also correct: at fixed physical switches, all three corresponding phase lengths scale linearly with `p` or `k`, respectively.

## Exact mass equation to M-slope

Insert `(M2)` and `(M3)` into

```text
C^2 I2hat=c^3 s^2 I3hat.
```

After cancelling the common nonzero factor `-m^2/2` and using `Y=-sX/C`, the equation becomes

```text
C E2(F2)/sin(c alpha)
+c^3 s E3(F3)/sin(alpha)=0.
```

Every cancellation uses a strict nonzero factor. Reversing the same algebra recovers the original mass equation, so `(M-slope)` is equivalent, not merely implied.

As an exact symbolic replay, SymPy 1.14.0 reduced the following two on-shell differences to zero:

```text
-m^2 X E3(F3)/(2 sin(alpha))-I3hat,
-m^2 Y E2(F2)/(2 sin(A))-I2hat.
```

For the first reduction I imposed the exact spectral substitutions

```text
cos(alpha)=Z sin(alpha)/X,
sin(alpha)^2=X^2/(X^2+Z^2).
```

For the second I imposed

```text
cos(A)=-T sin(A)/Y,
sin(A)^2=Y^2/(Y^2+T^2).
```

These substitutions are legitimate on the strict spectral domain and use no floating-point data.

## K sign and Xi split

The two spectral equations give

```text
K=c C T/s-Z
 =X[c cot(c alpha)-cot(alpha)].
```

For `f(t)=t cot(t)` on `(0,pi)`,

```text
f'(t)=[sin(t)cos(t)-t]/sin(t)^2<0,
```

because the derivative of `t-sin(t)cos(t)` is `2 sin(t)^2>0`. Since `0<c alpha<alpha<pi`,

```text
c cot(c alpha)-cot(alpha)>0.
```

Together with `X<0`, this proves `K<0` with the claimed strict sign.

Finally, direct expansion gives

```text
Xi
=Dtheta(X^2 U-rK)+X^3 Ttheta^2/C^2
=X^2[Dtheta U+X Ttheta^2/C^2]-rK Dtheta
=X^2 G-rK Dtheta.
```

Because `-rK Dtheta>0`, the condition `G>=0` is sufficient for `Xi>0`. The package does not use or claim the converse. Thus it correctly presents `G>=0` only as a smaller sufficient residual, not as an equivalent reduction.

## Boundary and adversarial audit

The most fragile points were the sign in the integrated Lagrange identity, the extra `k` introduced by `F2=k g(0)`, and the reversal of inequality when multiplying `Phi` by `X<0`. Independent derivation confirms all three. The strict domain excludes every vanishing denominator used in the proof, while middle-layer trigonometric zero sets remain included.

No numerical evidence enters any strict conclusion. The unresolved mass-to-`G` sign bridge is stated explicitly and is not used as a premise.

## Decision delta and residual risk

The W3 mass-slope and residual identities pass independent audit as a rigorous partial reduction. The remaining obligation is still to derive a sufficient sign bound from the complete spectral, band, modal-domain, and mass-slope system. This audit does not establish `G>=0`, `Xi>0`, `PHI-SIGN`, or `KP-DET`.
