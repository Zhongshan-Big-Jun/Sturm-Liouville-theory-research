# Research map

## Current question

Closed: the transfer-matrix root count reduces to an exact scalar polynomial theorem, and all named boundary cases have passed independent audit.

## Active mechanisms

1. determinant/trace plus Cayley-Hamilton and Chebyshev polynomials;
2. exact trigonometric sign bracketing;
3. counterexample and multiplicity attack.

## Intermediate findings

- Candidate exact reduction: with `r=1/s`, `a=(s+r)/2`, `z=(1+a)x^2-a`,
  `Q_{n,s}(x)=U_n(z)+rU_{n-1}(z)`.
- Candidate scalar root proof: alternating signs at the exact mesh `theta=j*pi/n` produce `n` disjoint roots, and degree `n` forces completeness and simplicity.
- The quadratic pullback is safe when `s>1`: `a>1`, so every scalar root in `(-1,1)` lifts to two nonzero `x`-roots in `(-1,1)`.

## Unexpected findings

- A second, mechanism-distinct proof exists: the product is a shooting transfer for a positive piecewise-constant Sturm--Liouville problem, and exact phase calibration at `y=pi` gives the count.
- The scalar polynomial is also a characteristic polynomial of a symmetric irreducible tridiagonal matrix, giving a third proof of root reality, location, and simplicity.

## Failures and reasons

- The first two symbolic-check runs failed because of checker normalization and a native/symbolic integer mismatch; both were tooling defects, recorded in the ledger and repaired before a passing run.

## Open directions

- Optional only: formalize the proof in a proof assistant if repository inspection is later authorized.
- Optional only: perform a post-blind literature/novelty audit if the user later lifts the prohibition.

## Avoid list

- numerical root scans as a substitute for a proof;
- root pairing without a count;
- invoking interlacing without exact sign and endpoint checks.

## Contributions

- User: problem, constraints, required skill, and request for subagents.
- Coordinator: contract, routes, and synthesis ownership.
- `SUB-ALG`: exact Cayley-Hamilton/Chebyshev proof and alternate sign mesh.
- `SUB-OSC`: independent Sturm shooting/Pruefer proof.
- `SUB-ADV`: exact counterexample attack and symmetric-tridiagonal audit.
