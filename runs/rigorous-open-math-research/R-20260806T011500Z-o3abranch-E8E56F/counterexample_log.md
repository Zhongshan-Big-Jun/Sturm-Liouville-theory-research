# Counterexample log: O3a branch lemmas (run R-20260806T011500Z-o3abranch-E8E56F)

## CE-1 (accepted, RIGOROUS interval-arithmetic certificate): Lemma A is false for large R

Update 2026-08-06 (this continuation): CE-1 was upgraded from a float64
numerical finding to a rigorous interval-arithmetic certificate, produced
by reproducibility/cert_ce1.py (mpmath.iv, outward-directed rounding,
iv.prec = 220).  Certified claims at R = 1500, a* = 0.57364:

  - a* in (a0, b0) rigorously (cos(pi a*) < 1/4 and > -1/4 by interval
    evaluation; a0 = arccos(1/4)/pi, b0 = arccos(-1/4)/pi).
  - b1* in [0.5832744756851049..., width ~5e-28]: verified R1 root in
    (0.5830, 0.5836) via interval IVT bisection; dR1/db sign-definite
    (< 0) over the whole enclosure rectangle, so the root is unique in
    the bracket and the implicit function theorem applies.
  - b2* in [0.57600535897434566..., width ~3e-28]: verified R2 root in
    (0.5758, 0.5762); dR2/db sign-definite (< 0) on the rectangle.
  - good-root checks certified: v(a*) > 0 at branch 1 (a* = x_-),
    v(b2*) < 0 at branch 2 (b2* = x_+); v values enclosed in intervals
    bounded away from 0.
  - branch slopes (closed-form implicit derivatives via forward-mode
    interval AD over the enclosure rectangles; all partials verified
    against finite differences at high precision):
      g1'(a*) in [1.02055289534, 1.02055289534],
      g2'(a*) in [1.02089587749, 1.02089587749],
      h'(a*)  = g1' - g2' in [-3.4298e-4, -3.4298e-4] < 0.  RIGOROUS.
  - the same certificate at R = 1e4 gives h'(a*) in [-3.2030e-3, -3.2030e-3]
    < 0 (larger margin).
  - auxiliary rigorous checks: sec_s1, sec_s2, den1, den2 all
    sign-definite on the rectangles (simple secular roots; branch-slope
    formulas well-defined).

Consequence: the pointwise claim of Lemma A (g1'(a) > g2'(a) on the
common range for every R > 1) is REFUTED, with a reproducible
interval-arithmetic certificate (cert_ce1.py).  The claim remains
true for R <= 1000 (prior runs) and false for R >= ~1400.

Caveat recorded honestly: the certificate inherits the trust model of
mpmath.iv's outward rounding (libmp mpi_* with round_floor/round_ceiling
and rigorous enclosure implementations for sin/cos); this is standard
verified-computation practice but not machine-checked by a formal proof
assistant.  The evaluation point a* is the mpf value of the decimal
0.57364; R is exact.

Additional structural finding (2026-08-06): at R = 1500, a = 0.57364,
the equation R2(a, b) = 0 with v(b) < 0 has THREE solutions
(b ~ 0.57379, 0.57437, 0.57601; see dbg_r2profile2.py).  Only the
third is the main-sheet value g2(a) (the component through (b0, b0),
verified by continuation, dbg_trace_branches.py).  The extra sheets are
NOT sign-consistent fixed points: at those configs v(a) < 0, so
a != x_- and R1(a, b) != 0.  They therefore do not refute O3a; they
do show that the informal phrase "the good branches are the only
branch components of Gamma_2 cap {b = x_+}" (source Lemma C) must be
read as referring to the fixed-point-relevant components through the
endpoints (a0, a0) and (b0, b0), not to all points with R2 = 0 and
v(b) < 0.  The theorem-relevant content of Lemma C (every
sign-consistent fixed point lies on the main branches, a in the common
range) is unaffected.


Statement attacked (Lemma A, source Section 4 and task packet): for every
R > 1, on the common a-range I = [alpha, beta] where both good branches exist,
g1'(a) > g2'(a) > 0.

Finding: FALSE for R >= R* with R* in (1200, 1500).  Concrete witness:
R = 1500, a = 0.57364 (which lies in the common range [a0, b0];
a0 = 0.4195694, b0 = 0.5804305):

  branch-1 point: g1(0.57364) = 0.58327448  (R1 = 0, v(a) > 0)
  branch-2 point: g2(0.57364) = 0.57600536  (R2 = 0, v(b) < 0)
  g1' = +1.020553,  g2' = +1.020897,  h' = g1' - g2' = -0.000344 < 0.

Both slopes are still positive, so only g1' > g2' fails.

Verification (three independent methods, float64):
1. Finite differences of branch roots using the prior-run solver
   agentB_lib (crosscheck_hp.py, threshold.py).
2. Finite differences of branch roots using clean_lib (verify_hp.py):
   h' = -0.003203 at R = 1e4, stable for FD steps h = 1e-6 .. 1e-4; direct
   values of h(a) at a = 0.5730 .. 0.5744 decrease monotonically.
3. Closed-form implicit derivatives (closed_check.py): g1' = +1.020553,
   g2' = +1.020897 at R = 1500.  (No branch finite differences.)
Additionally an ODE-shooting check (ode_check.py) confirms the branch
structure without using the secular equation.

Family of witnesses:
  R        h'(0.57364)
  1200     +0.00466
  1500     -0.00034
  2000     -0.00286
  3000     -0.00392
  5000     -0.00389
  1e4      -0.00320
  1e5      -0.00119

Structure of h near the right end (R = 1e4): h increases to a peak
h ~ 2.6415e-3 at a ~ 0.552, then decreases (h' < 0 on [0.5532, 0.5789],
min h' ~ -3.45e-3) to h(b0) = 3.795e-3 > 0.  For R = 1e5/1e6 the negative-h'
region persists (h' ~ -1.2e-3 / -4e-4) and h stays positive up to b0
(h(b0) ~ 0.38/sqrt(R)).

Status: REFUTED rigorously (interval-arithmetic certificate, see the update at
the top of this entry).  The float64-level finding is additionally reproducible
from reproducibility/crosscheck_hp.py, verify_hp.py, closed_check.py, threshold.py.

## CE-2 (rejected): spurious large-R "fixed points" are not counterexamples

During the 2-parameter scan at R = 1e5 and 1e6, least-squares returned
(a, b) = (0.4, 0.6) (R = 1e5) and (0.48, 0.52) (R = 1e6) with residual
magnitude ~2.6e-7 and v(a) ~ +1, v(b) ~ -1.  These are NOT sign-consistent
good roots: the residual is not zero at the relevant scale (the eigenvalues
are tiny, ~1e-3), and for these configs f has NO zeros with the required sign
pattern (v stays near 1 on (0,1), so f < 0 everywhere).  Excluded by the
good-root checks (|R1|, |R2| < 1e-9; v(a) > 0 with v(a) small; zero-location
check x_- = a, x_+ = b).  Same class of artifact as the prior run's R=50/100
fptable rows (a ~ 0.002, b ~ 0.998).

## Non-findings (tested, no counterexample)
- No second zero of h = g1 - g2 in the common range for any R in {1.02, 1.05,
  1.2, 1.5, 2, 3, 4, 10, 50, 100, 200, 500, 1000, 3000, 1e4, 3e4, 1e5, 1e6}
  (h_trace2.py; h > 0 on the whole tail; h(b0) > 0 to 1e7).
- No asymmetric good root found; the unique zero of h is at the symmetric
  fixed point a_fp(R).
- The Hessian of D is not negative definite on the whole triangle (so no
  global-Hessian proof of Lemma A is possible), but this is a proof-route
  obstruction, not a counterexample to O3a.

