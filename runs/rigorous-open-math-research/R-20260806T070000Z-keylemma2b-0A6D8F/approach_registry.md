# Approach registry

Run: R-20260806T070000Z-keylemma2b-0A6D8F

## Route cards (current run)

### ROUTE M2 (dIN/du < 0 on D)  -- STATUS: PROVED
- Core mechanism: reduce two-variable monotonicity to (i) the exact one-variable
  identity M2(1,u) = pi h(u) with h concave and max < 0, and (ii) dM2/dq < 0 on
  D, split into a certified compact part and an elementary tail bound B(q).
- Target obligation: M2 (feeds R1 and R2).
- Why strictly easier: h is a one-variable concave function with explicit
  critical-point location; the q-dependence is handled by a crude monotone bound.
- Required known results: none external; exact derivative identities re-derived.
- First concrete deliverable: M2(1,u) = pi(4u(pi - atan u) - 5 - 9u^2), h'' < 0.
- Fast falsification tests: 4760+ point scans (no violations; min -5.96);
  independent 80-digit random samples (no violations).
- Expected bottleneck: the strip [1,20]x[y1,sqrt(41)] not covered by the
  original certificate (found in this run); closed by cert_dM2dq_strip_boxes.json
  and independently re-verified.
- Exact gap: none.
- Status: PROVED.

### ROUTE CORNER (G_2(1/2;q) >= 0 for q >= 2)  -- STATUS: PROVED
- Core mechanism: exact closed form at c = 1/2; reduction to pi > arccos(2/3) +
  sqrt(5); elementary Taylor certificate for cos.
- Target obligation: R1 boundary curve.
- First deliverable: G_2(1/2;q) = 2q(q+1)(pi - x - 3 sin x)/(2q+1)^{3/2}.
- Falsification: q >= 2 grid scans (min 0.069181 at q = 2); symbolic diff = 0.
- Status: PROVED.

### ROUTE C4 (G_2(0.4;q) >= 0 for q >= 1)  -- STATUS: PROVED
- Core mechanism: parametrize the c = 0.4 curve by v = arctan(u); IN = A*K(v);
  interval certificate on [2pi/7, 2pi/5 - 1e-3]; elementary T^3 K > 0 tail.
- Target obligation: R2 boundary curve.
- First deliverable: K(v) = (q^2+u^2)(5vq - 3u + 2v) - 1.2 u q (1+u^2);
  T^3 K identity with exact rational lower bound 178.85896 > 0.
- Falsification: 500+ point checks, certificate re-evaluations, 0 failures.
- Caveat: the curve identity IN = A*K is verified numerically + certified
  re-evaluations; sympy did NOT reduce the symbolic difference to 0 (atan(tan)
  residue).  No symbolic claim is made for that step.
- Status: PROVED.

### ROUTE L4BOX / L5BOX (sign lemmas on (1,2]x[0.4,0.5])  -- STATUS: PROVED
- Core mechanism: certified outward-rounded interval arithmetic over a fixed
  box (128 leaves each), with monotonicity bracketing of alpha_1, alpha_2.
- Target obligation: closure on Region B.
- First deliverable: cert_L4box_boxes.json (worst -4.6569), cert_L5box_boxes.json
  (worst +6.2429), both independently re-verified (worst -4.8416 / +8.3794).
- Falsification: fresh 80-digit random and edge samples (0 failures); both
  engines agree on sign with large margins.
- Status: PROVED.

## Routes from the predecessor run (carried forward)

### ROUTE M1 (dIN/dq > 0)  -- STATUS: NOT NEEDED (recorded)
- Was PARTIAL in the predecessor.  The R1/R2 closure used M2 instead, so M1 is
  not required; kept for completeness.

### ROUTE Q1 (dG_2/dq >= 0)  -- STATUS: NOT NEEDED (fallback)
- Parent-run linchpin; superseded by the M2 route in the predecessor and closed
  obligations in this run.  Not used.

### ROUTE dG2/dc <= 0  -- STATUS: REFUTED (predecessor entry 2)
- dG2/dc is positive for q in (30,100), c in (0.3,0.45); the route fails
  globally.  Recorded as a falsified route.

## Dynamic policy notes

- Two independent verification engines (riarith Decimal and mpmath.iv) were kept
  adversarial to each other; every certificate must pass both.
- A counterexample-oriented pass was run in this run (audit_semantics_fresh2.py,
  edge parameters q -> 1+, q -> 1e6, c -> 0+, c -> 0.5-); no counterexamples to
  any claimed lemma were found.
