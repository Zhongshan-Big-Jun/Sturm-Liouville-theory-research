RIGOROUS_PARTIAL_RESULT

# Coordinator direct elimination for PHI-SIGN

## Scope

This is the direct resume action `FUTURE-PHI-EXACT-ROUTE`. It uses only the
audited phase definitions and exact branch equations from the frozen W1
derivation. It does not claim `PHI-SIGN` or `KP-DET`.

## Safe spectral elimination

The strict phase domain gives

```text
sin(alpha)>0,
sin(c alpha)>0,
s=sin(c theta)>0,
C=cos(theta)>0,
X<0,
Y=-sX/C>0.
```

Therefore the two spectral equations may be divided without adding or losing
an admissible point. They give

```text
cot(alpha)=Z/X,
cot(c alpha)=-T/Y=C T/(s X).
```

With `r=m^2/(m^2-1)>1`, the left penalty becomes

```text
Dalpha
=r[c cot(c alpha)-cot(alpha)]
=r[c C T/s-Z]/X.
```

Define the exact middle-layer residual

```text
Psi
=X^2[D-c s N/C]-r[c C T/s-Z].
```

Substitution into the frozen expression for `Phi` yields

```text
Phi=Dtheta Psi/X+X^2 Ttheta^2/C^2.
```

Since `X<0`, this is the lossless equivalence

```text
Phi<0 iff Xi>0,

Xi=Dtheta Psi+X^3 Ttheta^2/C^2.
```

No division by `cos(beta)` or `cos(c beta)` was used. In particular, middle
phase points at which either of those cosines vanishes remain covered.

## Exact band identity

The band equation can be retained in the denominator-free form

```text
C[s cos(c beta)+m Cc sin(c beta)]
+s[C cos(beta)-m S sin(beta)]=0.
```

Thus a continuation route may reduce `Xi` modulo this identity and the exact
mass equation without introducing tangent-chart exclusions.

## Cheapest falsification probe

The elimination was replayed symbolically by substituting

```text
cot(alpha)=Z/X,
cot(c alpha)=C T/(s X)
```

into the W1 formula. Both directions use only multiplication by the strict
nonzero factors `X`, `s`, and `C`. Hence the reduction is exact, including
the equality case `Phi=Xi=0`.

The probe does not determine the sign of `Xi`. The positive term in the
original `Phi` becomes the negative term `X^3 Ttheta^2/C^2` in `Xi`, and no
sign estimate obtained from the spectral and band equations alone dominates
it. The exact mass identity is still load-bearing.

## Gate decision

`OPEN_EXACT_GAP -> ESCALATE`.

One mechanism-distinct worker is justified: propagate the mass identity
through `Psi` and decide `Xi>0`, or construct a fully admissible exact equality
tuple. A return that only restates `Phi<0`, repeats quotient monotonicity, or
uses finite numerics has zero decision value.
