RIGOROUS_PARTIAL_RESULT

# W1 transfer and Schur route report

## Route card

- Route ID and family: `W1-TRANSFER-SCHUR`, exact transfer elimination.
- Core mechanism: use right-normalized three-layer modes, both band equations,
  and exact half masses to eliminate Green kernels, Wronskians, and amplitudes.
- Target obligation: `KP-SCHUR`.
- Cost tier: `1`.
- Status: `PARTIAL`.
- Exact gap: prove the elementary constrained sign `Phi<0` in
  `derivation.md`, equation `(23)`.
- Excluded scope: KO-DET, simultaneous sector singularity, SUP, n greater than
  2, non-symmetric roots, and global G1 prime.

## Strict results

1. The direct theorem `gamma_2>b_0` is independently reproduced from the last
   layer. The factors `2`, `R/(R-1)`, `v=sqrt(2)u_2`, and the domains
   `0<theta,c theta<pi/2` have all been checked.
2. The first diagonal data have exact phase formulas:

```text
a_0-gamma_1
=2[X D+c Y N-Dalpha]/(Bv^2 p Y^2).
```

3. The Schur margin has the exact amplitude-free reduction

```text
S_KP<0  if and only if  Phi<0,

Phi
=Dtheta[X(D-c s N/C)-Dalpha]
 +X^2 Ttheta^2/C^2.
```

4. The full admissible phase domain, two spectral equations, quotient band
   equation, and exact mass band equation are explicit in `derivation.md`.
   No denominator vanishes there.
5. Equality is lossless: `S_KP=0` if and only if the exact branch phase system
   and `Phi=0` hold. Boundary collisions and wrong-index phase faces are
   excluded explicitly.

## Verification and stress tests

- The formulas for both cross Green diagonals were derived twice through their
  right-boundary Wronskians and checked against the frozen last-layer formulas
  at the second switch.
- The penalty conversion was checked from the whole-string Wronskian to the
  half-normalized quotient. This is where the factor `2` enters.
- The sign `Dtheta>0` is termwise strict, using
  `tan(t)-sin(t)cos(t)>0` and
  `cot(t)-sin(t)cos(t)>0` on `(0,pi/2)`.
- The sign `Dalpha>0` uses strict decrease of `t cot(t)` on `(0,pi)`.
- No numerical value, local script, external source, or spectral truncation is
  used.

## Why the result changes the decision problem

The previous scalar `S_KP` still contained four Green and Wronskian objects
whose branch dependence was implicit. The new `Phi` contains only elementary
trigonometric functions of five phase variables constrained by four exact
branch equations and modal inequalities. This permits a finite exact sign
certificate or a branch-realizable equality witness. An abstract two-by-two
matrix can no longer enter the reduced problem.

## Remaining gap

The exact mass equation has not yet been converted into an inequality strong
enough to dominate the positive term `X^2 Ttheta^2/C^2`. Thus neither
`Phi<0` nor an equality witness is established. KP-DET remains open, while the
route terminates with a strict, hashable reduction.

## Contributions and restrictions

- Solver contribution: exact hand derivation and sign audit.
- Tool contribution: read-only hash and file inspection only.
- Subagents: none.
- Web searches: none.
- Project-local Python executions: none.
- Numerical claims used as proof: none.
