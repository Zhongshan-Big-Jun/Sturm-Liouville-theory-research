# Approach Registry — R-20260816T210000Z-densbc-o1p

Task: DensBC O1' on a structured subclass.

## Approaches tried

### 1. H_beta + finite polynomial constraints (CHOSEN, SUCCEEDED)
- Description: specialize to diagonal H_beta with L_j finite linear moment
  conditions.  Representer moments are finitely supported; kept set cofinite;
  run/free-base system finite.
- Result: exact decision criterion
  closure(span Q_sp)=V iff ker(T|_{B_adm})={0}; coordinate case reduces to
  Theorem E.
- Status: SUCCEEDED (STRICT).  O1' closed on this subclass.

### 2. General banded non-diagonal H (NOT CHOSEN, PARTIAL/BLOCKED)
- Description: assume banded moment matrix <x^i,x^k> and finitely supported
  representer moments, attempt finite-dimensional decision in arbitrary H.
- Status: PARTIAL/BLOCKED for this run.  The membership and kept-set parts
  become finite, but the moment-realization step still depends on the infinite
  Gram matrix and its completion; not resolved.

### 3. Numerical exploration (NOT USED)
- Description: not used.  All results are proven analytically; numerical
  checks would be EVIDENCE only and are not needed for the STRICT theorem.

### 4. Single-column zero criterion (CONSIDERED, REJECTED as incomplete)
- Description: conjecture that density fails iff some admissible free base
  individually satisfies A m_b = 0.
- Status: REFUTED/REJECTED.  Non-coordinate constraints can couple free bases:
  a nonzero linear combination of admissible columns can lie in ker T even
  when no individual column is zero.  The final criterion uses ker(T|B_adm).

## Status summary
- O1' general: OPEN.
- O1' on H_beta + finite polynomial constraints: CLOSED (STRICT).
- Coordinate/diagonal Theorem E: recovered as a corollary.
- Non-coordinate example with finite obstruction: constructed.
