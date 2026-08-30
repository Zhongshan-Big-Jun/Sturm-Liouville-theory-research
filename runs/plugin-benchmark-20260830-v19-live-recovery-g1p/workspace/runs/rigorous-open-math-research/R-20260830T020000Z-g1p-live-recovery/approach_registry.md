# Approach registry

| Route ID | Mechanism | Target | State | Exact gain or gap |
|---|---|---|---|---|
| `CF-INERTIA` | Continuous inertia and endpoint anchors | Four scalar signs | `RIGOROUS_PARTIAL_RESULT` | Reduces the four signs to two determinant signs and confines any failure to a compact middle first zero. |
| `M1-CHAIN` | Differentiate determinants along `R` using `x'=-J^{-1}F_R` | `KP-DET`, `KO-DET` | `BLOCKED` as a standalone closure route | The recorded formula is valid only where `J` is invertible, while `det J=(R-1)^4 det(Kp_odd)det(Ko)`. It lacks a non-circular singular-point continuation argument. |
| `SPECTRAL-COERCIVITY` | Exact half-Green spectral split and signed tail domination | `KP-FIRSTZERO` | `READY_IF_ESCALATED` | Must prove strict negativity of the exact `I1'` quadratic form uniformly on the compact middle interval, or isolate one explicit scalar tail inequality. |
| `JACOBI-FIRSTZERO` | Convert a sector kernel into a linearized half-string Jacobi field and use oscillation or transversality | `KP-FIRSTZERO` | `READY_IF_ESCALATED` | Must exclude a nonzero kernel, handle the double-zero case, or return an exact branch counterexample/certificate. |
| `NUMERICAL-SCAN` | Continuation and finite-difference determinant scan | Route selection only | `EVIDENCE` | Existing scans support positivity and decreasing determinants but do not prove any universal sign. |

## Avoid list

- Do not re-run a broad `R` scan as if it closes `KP-DET`.
- Do not identify `Kp_odd` with raw `Ko`.
- Do not use the superseded `R^(-7/2)` and `R^(-9/2)` asymptotics.
- Do not invert `J` at the hypothetical first singular point without an independently regular branch parameterization.
- Do not expand to SUP or global `G1'` before the INF `KP-FIRSTZERO` obligation changes state.
