# Counterexample log

## Search targets

- Repeated roots of the reduced polynomial.
- A root at `x=0`, where a quadratic substitution could destroy simplicity.
- Missing endpoint intervals in an oscillation count.
- Exceptional values at `s=1`, `y=0`, `y=pi`, or `y=pi/2`.

No counterexample has yet been established. Absence of a found example will not be used as proof.

## Checker false alarm

- The first symbolic harness failed to normalize `q^3` under `c^2+q^2=1`. This is a checker-normalization defect, not a mathematical counterexample. The reducer was replaced by exact polynomial remainder.

## Uniform adversarial findings

- No exact counterexample was found by `SUB-ADV`.
- Endpoint contamination is excluded because `Q(+-1)=n+1+n/s>0`.
- A midpoint/vertex zero is excluded exactly: `G(pi/2)=(-s)^n`.
- Scalar multiple roots are excluded independently by both exact sign-count/degree and an irreducible symmetric-tridiagonal realization.
- Lifted multiple roots are excluded because every scalar root lifts at `x!=0`, where the quadratic substitution has nonzero derivative.
- The excluded boundary `s=1` remains nondegenerate and has the exact sine formula.
