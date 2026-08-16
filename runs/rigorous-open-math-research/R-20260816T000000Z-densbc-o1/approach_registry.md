# Approach Registry

Run: R-20260816T000000Z-densbc-o1

## Route cards

### Route 1: Projection-density reformulation
- Route key / family: PROJECTION / operator-theoretic.
- Core mechanism: P_V(Pi) dense in V always; density of Q_sp iff excluded
  projections are redundant.
- Target obligation: exact criterion, packet item 1.
- Why easier: removes "density in V" as an issue; isolates the selection effect.
- Required known results: (H1), continuity of P_V, upstream Theorem A.
- First concrete deliverable: Theorem 1 (STRICT).
- Fast falsification tests: finite-rank projection check (o1_projection_density.py).
- Expected bottleneck: the realization/membership step (not this route's concern).
- Status: PROVED (Theorem 1) / feeds Theorems 2-5.

### Route 2: Obstruction system in moment variables
- Route key / family: MOMENT-SYSTEM / linear algebra + moment problem.
- Core mechanism: write V cap Q_sp^\perp via kept recursions (R) + membership <w,v_j>=0.
- Target obligation: packet items 1 & 3.
- Why easier: recursions are pure linearity of moments (H-independent).
- First concrete deliverable: Theorems 2-3 (STRICT).
- Fast falsification: check kept set N from representer moments (scripts).
- Expected bottleneck: realization in V (O1').
- Status: PROVED for the structured system; realization core OPEN (O1').

### Route 3: Diagonal reduction
- Route key / family: REGRESSION / specialization.
- Core mechanism: coordinate L_j => representer moments delta; run graph = Theorem E.
- Target obligation: packet item 2.
- First concrete deliverable: Theorem 4 (STRICT).
- Status: PROVED.

### Route 4: Finite-rank vs moment-problem classification
- Route key / family: STRUCTURE / honesty boundary.
- Core mechanism: identify exactly which data decides the criterion.
- First concrete deliverable: Theorem 5 (STRICT).
- Status: PROVED (structure); the core O1' OPEN.

### Route 5: Generic-constraint emptiness
- Route key / family: NEGATIVE / generic behavior.
- Core mechanism: generic non-coordinate v_1 => no p_n in V.
- First concrete deliverable: Proposition 6 (STRICT) + EVIDENCE scripts.
- Status: PROVED (structural).

## Blocked / refuted

- "Closed-form for all non-diagonal H" : BLOCKED by Theorem 5 (needs O1').
- "Numerics close O1" : REFUTED (honesty rule).
