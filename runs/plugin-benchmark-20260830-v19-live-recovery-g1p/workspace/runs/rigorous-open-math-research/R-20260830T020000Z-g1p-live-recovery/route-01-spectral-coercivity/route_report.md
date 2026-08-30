RIGOROUS_PARTIAL_RESULT

# Route report

## Terminal state

- Route: `W1-KP-SPECTRAL-COERCIVITY`.
- Status: `PARTIAL`.
- Scope: `KP-FIRSTZERO` and `KP-DET` only, on the prescribed finite-interior `n=2` symmetric INF branch.
- Frozen target: prove `det Kp_odd(R)>0` for every finite `R>1`, or rigorously expose a strictly smaller exact gap.
- Permitted premises: the exact sector formula and half-Green split, the strict near-one anchor, the accepted strict large-`R` anchor, and branch continuity from `problem_contract.md`.
- Excluded: `Ko`, SUP, `n>=3`, global `G1'`, branch construction, broad literature search, numerical evidence as proof, and any use of `J^{-1}` at a possible first sector zero.

## Strongest rigorous result

The two-point cross-resolvent difference has an exact semiseparable form after the band identity is imposed. Let

```text
H=E G_D(lambda_3) E-c^2 G_N(lambda_2),
E=diag(1,-1),
U=diag(u_2(x_1),u_2(x_2)),
```

where `v_1` is the first half-Dirichlet eigenfunction and `w_2(x_j)=epsilon_j c v_1(x_j)`. Then there are real scalars `a,b` such that

```text
U^(-1) H U^(-1)=[[a,b],[b,b]].
```

This is STRICT and follows from the one-dimensional Green factorization, not from a numerical fit. Moreover, `b>0` follows from exact last-layer Green formulas and Sturm nodal placement. These facts remove one independent entry from the unresolved two-point tail comparison and force any first singularity to have corank one with a same-sign null vector. In particular, the exceptional double-zero alternative left open in `direct_attempt.md` cannot occur at any finite-interior point. The proof and equality cases are in `derivation.md`.

## Exact remaining gap

Write

```text
gamma_j=-d_j/(2 lambda_2 u_j^4)
	=c|W(x_j)|/(lambda_2(R-1)u_j^4)>0.
```

Congruence by `U^2` shows that `Kp_odd<0` is exactly equivalent to negative definiteness of

```text
M=[[a-gamma_1,b],[b,b-gamma_2]].
```

At a hypothetical first zero, continuity from the strict negative-definite anchor forces

```text
gamma_2>b,
gamma_1-a=b^2/(gamma_2-b).
```

Thus the exact remaining `KP-FIRSTZERO` gap is to exclude this single positive-cone scalar equality on the compact middle branch. Equivalently, it is enough to prove

```text
gamma_1-a>b^2/(gamma_2-b)
```

at every candidate point with `gamma_2>b` reachable from the anchored negative-definite component.

The last-layer calculation proves `b>0`, but it does not determine `a` or compare the globally normalized Wronskian penalties with `b`. The abstract values

```text
a=0,
b=1,
gamma_1=1,
gamma_2=2
```

satisfy all scalar sign constraints obtained by this route and realize equality. This is not a branch counterexample. It proves that semiseparability, `b>0`, and positivity of the diagonal penalties alone cannot close `KP-DET`; a new branch-specific comparison controlling `a` and the normalized Wronskian terms is required.

## Verification

- Re-derived the Green factorization with the project spectral sign convention.
- Corrected the normalization layer by using congruence with `U^2`, which yields `gamma_j=-d_j/(2lambda_2u_j^4)`.
- Audited finite-interior, nodal, equality, double-zero, and corank-one cases.
- Used no numerical computation and no external theorem beyond the accepted Sturm and Green premises.

## Decision delta

`KP-DET` is not proved or refuted. The route strictly narrows the first-zero problem from an arbitrary two-dimensional kernel, including a possible double-zero matrix, to one positive-cone scalar equality, and it proves an exact off-diagonal sign.

## Observable counts

- Route artifacts: 3.
- Hash-bound inputs: 11.
- Strict new route lemmas: 3.
- Residual scalar equality gaps: 1.
- Numerical checks: 0.
- Web searches: 0.
- Subagents: 0.

## Numerical policy

No numerical result is used in the argument.
