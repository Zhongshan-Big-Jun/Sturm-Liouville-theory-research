RIGOROUS_PARTIAL_RESULT

# Route 02 report: Jacobi falsification and diagonal-sign audit

## Verdict

- Route status: `PARTIAL_NOT_COMPLETE`.
- Direct theorem audit: `PASS` for `gamma_2>b_0`.
- `KP-DET`: still `OPEN`.
- Exact counterexample: none constructed.

## Strict result obtained

Assume a same-sign Jacobi kernel exists at a finite-interior point on the
prescribed `n=2` symmetric INF branch. For its fields `phi`, `psi`, define

```text
alpha=phi/v,
beta=psi/w.
```

Then the two projective Wronskian fluxes agree exactly:

```text
v^2 alpha'=w^2 beta'=P,

P=0                                           on (0,a),
P=-lambda_2 tau y_1v(a)^2                     on (a,b),
P=-lambda_2 tau[y_1v(a)^2+y_2v(b)^2]          on (b,L).
```

This uses only the two Jacobi equations and the band identities
`lambda_3w(x_j)^2=lambda_2v(x_j)^2`. It does not use determinant
monotonicity, a singular Jacobian inverse, or numerical evidence.

Let

```text
h=v psi-w phi.
```

There is exactly one simple zero `xi` of `h`, it lies in `(a,z)`, and it is a
strict downward crossing. Here `z` is the unique zero of `w`. Its exact
location obeys

```text
-Q'(a)/c
	=lambda_2 tau v(a)^2
	 int_a^xi [1/w^2-1/v^2] dx.
```

There are no further zeros on `(z,L]`. This is a new necessary Sturm-geometric
condition for a parity-crossing same-sign kernel.

The final-layer endpoint calculation also fixes the positive impulse ratio:

```text
y_1v(a)^2/[y_2v(b)^2]
	=R/tau
	 [tan(theta_3)+c cot(theta_2)]
	 /[sin(theta_3)cos(theta_3)
	   +c sin(theta_2)cos(theta_2)]-1
	=(gamma_2-b_0)/b_0>0.
```

This independently reproduces the second normalized kernel row.

## Independent audit of `gamma_2>b_0`

The last-layer mode indices imply

```text
0<theta_3<pi/2,
theta_2=c theta_3 in (0,pi/2).
```

Endpoint-normalized Green solutions give

```text
G_D(b,b;lambda_3)=sin(theta_3)cos(theta_3)/k_3,
G_N(b,b;lambda_2)=-sin(theta_2)cos(theta_2)/k_2.
```

The exact difference `gamma_2-b_0` is a positive factor times

```text
R/tau[tan(theta_3)+c cot(theta_2)]
	-[sin(theta_3)cos(theta_3)
	  +c sin(theta_2)cos(theta_2)].
```

It is strictly positive because `R/tau>1` and, on `(0,pi/2)`,

```text
tan(t)>sin(t)cos(t),
cot(t)>sin(t)cos(t).
```

The audit found no sign, scale, endpoint, or quantifier defect. Its verdict
for the direct theorem is `PASS`.

## Why this route does not close KP-DET

The locking-point integral is strictly increasing from `0` to `+infinity` as
`xi` runs from `a` to `z`. Hence the new Sturm condition is automatically
realizable on every base branch. It constrains the shape of a kernel but does
not forbid one.

The exact remaining gap is the sign of the first-switch moving-level residual
after the ratio above is propagated through the middle layer. The route does
not determine that sign and does not construct an exact branch witness.

## Scope audit

- No statement about `KO-DET` was made.
- No statement about simultaneous sector singularity was made.
- No statement about SUP, nonsymmetric roots, `n>2`, or global G1 prime was made.
- No project-local Python tool was run or copied.
- No numerical evidence was used.
- No subagent was used.

## Structured self-audit

```json
{
	"direct_theorem_verdict": "PASS",
	"route_verdict": "PARTIAL_NOT_COMPLETE",
	"critical_errors": [],
	"strict_delta": [
		"common projective-flux identity",
		"unique simple locking point in (a,z)",
		"branch-only locking-point integral",
		"exact positive endpoint impulse ratio"
	],
	"exact_remaining_gap": "Determine the sign of the first-switch level residual after the positive endpoint ratio is propagated through the middle layer, or construct an exact branch-realizable zero.",
	"excluded_claims": [
		"KP-DET proved",
		"KP-DET refuted",
		"KO-DET",
		"global G1 prime"
	]
}
```
