# Approach registry

## Route families attempted/considered in this run

### R1: General equal-within-type alternating Chebyshev representation (NEW STRICT)
- **State**: STRICT result; route active for O2.
- **Mechanism**: For `p = r x`, `q = s x`, `s = sqrt(R)`, with
  `C = T_1(p) T_R(q)` and `M_n = C^n T_1(p)`, the secular element is
  `M_n[0,1] = sin(p) [ U_n(m) + delta U_{n-1}(m) ]`,
  where `m = tr(C)/2`, `delta = sin(q)/(s sin(p))`.
- **Exact gap**: Does not by itself show monotonicity of the root ratio
  `x_{n+1}/x_n` in `r`.

### R2: Elliptic-zone phase equation
- Derived from R1: in `|m| < 1`, roots satisfy
  `sin((n+1)theta) + delta(x) sin(n theta) = 0`,
  `m = cos theta`.
- **State**: Strict derivation; **exact gap**: `delta` varies with x, so
  standard fixed-delta Chebyshev root-location lemma does not immediately
  control the pair `x_n,x_{n+1}`.

### R3: fixed-delta Chebyshev root-location in `delta`
- Strict lemma: for fixed `0 < delta < 1`, the n roots of
  `U_n(m)+delta U_{n-1}(m)` are simple, real, and lie in `(-1,1)`
  (equivalent to the Jacobi-matrix argument; extends baseline to general delta).
- **State**: STRICT. **Gap**: the actual O2 family has x-dependent delta.

### R4: Energy-invariant amplitude equality
- From `E=0` in any global maximizer, on each constant block the two
  eigenfunction amplitudes are equal in magnitude.
- **State**: STRICT corollary of baseline; **Gap**: does not determine switch
  positions or widths.

### R5: Width-simplex optimization / numerical scanning
- Used scipy to scan the equal-width family and random width-simplex
  optimization for n=2,R=4.
- **State**: EVIDENCE only; not proof.

### R6: Literature route
- Searched Keller/MW/Qi/Huang and web. No direct result found.
- **State**: degraded; no new theorem imported.

## Avoid list / dead ends

- Do not claim O1/O2 from numerical maxima.
- Do not claim that self-consistent configurations are unique; reuse round
  found asymmetric self-consistent solutions with lower ratio.
- The MW bound `lambda_{2n}/lambda_n <= nu(R)` is insufficient for O1.
