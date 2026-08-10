# Approach registry

Run: R-20260806T011500Z-keylemma-E58FB1
Status legend: PROVED / PARTIAL / BLOCKED / REFUTED / ACTIVE / VERIFIED_NUMERICALLY

## Route cards

### A. Reduction-to-corner (region split) -- PROVED (the core skeleton)
- Mechanism: prove G1 < 0 everywhere; then G2 >= 0 settles both target forms trivially;
  the only remaining set is Region B = {G2 < 0}, which is (numerically) a thin strip
  (1,2) x (0.44, 0.5).  On that compact box, H' < 0 and F~'' > 0, so the log form and the
  F~' form follow from the exact corner values at c = 1/2 (B4, B5) by monotonicity in c.
- Status: PROVED as a reduction.  Dependencies: R1, R2 (Region B contained in the box),
  L4box, L5box (box signs), B1-B5 (bases).
- First concrete deliverable: the region-A theorem (L1 + L2), the box lemmas L4box/L5box,
  and the exact corner closed forms.
- Exact gap: R1, R2, L4box, L5box (see status_and_literature.md).

### B. Box q-monotonicity (R4-R6) -- SUPERSEDED
- Mechanism: prove dJ1/dq >= 0, dJ2/dq <= 0, dH'/dq <= 0 on (1,2] x [0.4, 0.5] and pull
  the q=1 boundary values B1-B3 into the box.
- Status: the monotonicity claims verify numerically with margins 4.87 / -2.69 / -9.55
  (qmono_box.py, r456_mpmath.py), but this route was SUPERSEDED by the direct box lemmas
  L4box/L5box: H' < 0 and F~'' > 0 hold directly on the whole box with margins -7.73 and
  +14.17, so the monotonicity-in-q structure is unnecessary.
- Lesson: verify the target signs on the full superset box before adding structural
  monotonicity lemmas; the direct check removes two layers of obligations.

### C. G2 q-monotonicity (Q1) -- VERIFIED_NUMERICALLY (candidate linchpin, unproved)
- Mechanism: dG2/dq >= 0 on (1, inf) x (0, 1/2).  If true, R1 reduces to the 1-variable
  boundary claim B6 (G2(c;2) >= 0) and R2 reduces to the exactly provable B7
  (G2(c;1) >= 0 for c <= 0.4).
- Status: verified on the full sampled domain (min ~5e-4 at (q=100, small c), decaying to
  ~0 at (q=1e6, c~0.01)); NOT proved.  Symbolic derivative is a large elementary expression
  with no visible factorization (sym_dG2dq.py).
- Why it could be strictly easier: reduces a 2-variable region to 1-variable boundaries.
- Expected bottleneck: the symbolic expression for dG2/dq has no obvious monotone
  factorization; a proof would likely need a change of variables (y = q tan gamma) plus
  case splits.
- Status: ACTIVE (recommended next route for closing R1, R2).

### D. gamma-parametrized margin (B(γ;q) >= 0) -- PARTIAL (bounds fail)
- Mechanism: with gamma = pi - alpha2, c = atan(q tan gamma)/(pi - gamma), the claim
  R1 becomes B := A(gamma)(q + c Phi) - 2 T (q^2-1) sin gamma cos gamma >= 0 with
  A = 2(pi-gamma)cot gamma - 3.
- Status: bounds A >= A(alpha0), T <= min(q tan gamma, pi/2), sin cos <= gamma all fail
  individually near (2, 1/2) (the slack is only ~8% in B there).  Corner-asymptotic
  analysis shows the tight balance is at c -> 1/2, q -> inf where B ~ (positive) q^(3/2);
  G2(1/2; q) ~ (pi/sqrt 2) sqrt q -> inf.  No usable elementary bound found.
- Lesson: at the tight corner the inequality is genuinely delicate; crude bounds lose too
  much.  A proof needs the exact c = 1/2 balance, not a generic bound.

### E. q=1 / c=1/2 exact bases -- PROVED
- Mechanism: at q = 1 the curves are explicit (alpha1 = pi/(2(1+c)),
  alpha2 = pi/(1+c), Phi = 1, G = -W/(1+c)); all needed signs reduce to elementary
  inequalities in W and its derivative (N1 > 0, N2 < 0, T' < 0).  At c = 1/2 all
  quantities are closed forms in x = alpha0 (cos x = q/(q+1)); B4 and B5 are exact.
- Status: PROVED (B1-B5, B7).

### F. Direct global sign scan -- VERIFIED_NUMERICALLY (evidence layer)
- Mechanism: dense grids of H, H', F~', F~'', J1, J2, G1, G2 over (q, c).
- Findings: H >= 2.4184 globally (sampled); -F~' >= 0.4253 on the bounded sampled range q <= 100 (for large q the margin shrinks toward 0 and the region-A argument applies instead); H' > 0 and F~'' < 0 occur only in
  Region A (G2 >= 0), where they are not needed; Region B margins: |G1|/|G2| >= 7.42,
  M~2/M~1 <= 6.94, |G1| - |G2| >= 2.418, F~'' >= 14.7, H' <= -7.1.
- Status: evidence; the region split means only Region B (inside the box) matters.

### G. Interval-arithmetic certificate (type-2 proof) -- NOT PURSUED (documented)
- Mechanism: rigorous outward-rounded interval evaluation of the box lemmas L4box/L5box
  and compact parts of R1/R2, plus analytic tails.
- Status: NOT PURSUED in this run.  mpmath 1.3.0 iv is not trusted to be fully
  outward-rounded for all functions (prior handoff warning); a sound certificate would
  require a hand-checked Taylor-monitor implementation (multi-hour engineering) and an
  independent audit of the soundness model.  Recorded as a viable completion route.
- Lesson: a computational certificate must be sound, not merely high-precision; label
  claims accordingly.

## Route allocation history
1. Route A (reduction) established first; it is the backbone.
2. Route B was built, then superseded by direct box checks (Route A extension).
3. Route C (dG2/dq >= 0) emerged as the cleanest unproved linchpin; it is ACTIVE.
4. Route D (gamma-bounds) produced the corner asymptotic picture; bounds fail.
5. Route E closed all q=1 and c=1/2 bases.
6. Route F provides the quantified evidence tables.
7. Route G is the only known path to a full computational proof; deferred.

## Next actions (for a future session)
- Route C: prove dG2/dq >= 0 (change of variables y = q tan gamma; case splits near
  q tan gamma ~ 1 and near c = 1/2), then close R1 via B6 and R2 via B7.
- Route A: prove L4box (H' < 0 on the box) and L5box (F~'' > 0 on the box) either by hand
  (their margins are 7.7 and 14.2) or by a sound interval certificate (Route G).
- Then the KEY LEMMA closes and T4 upgrades O2 to PROVED.
