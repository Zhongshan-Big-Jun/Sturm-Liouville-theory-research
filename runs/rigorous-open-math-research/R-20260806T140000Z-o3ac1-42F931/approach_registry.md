# Approach registry (run R-20260806T140000Z-o3ac1-42F931)

Registry of route families, states, and exact gaps.  Route states follow the
skill taxonomy: UNEXPLORED, ACTIVE, PROMISING, PARTIAL, BLOCKED, REFUTED,
MERGED, PROVED.

## Route A: reflection + integral identity (this run's main structural route)

Family: analytic reduction via symmetry.
Core mechanism: sigma(Gamma_1) = Gamma_2 gives h(a) = integral_{u(a)}^a
(g1'(t) - 1) dt and h'(a) = g1'(a) - 1/g1'(u(a)) (R3, R4).
Target obligation: C1 (via R6: E1 + M + Z).
Why easier: h' is expressed through the single branch function g1 and its
inverse; the two-dip structure of h' is a statement about g1' crossing 1.
First deliverable: Lemmas R1-R6 (PROVED).
Fast falsification tests: pointwise h values and h' at dips for
R in {1000..1e6} (pass; M-shape confirmed).
Expected bottleneck: proving the global shape of g1' (convexity/dip
structure) from the secular equation.
Status: PARTIAL.
Exact gap: (E1) endpoint signs; (M) M-shape of h' for every R > 1.
Next action: analyze g1' = A/B via the secular equation and the
Feynman-Hellmann/resolvent representation of A, B.

## Route B: M-shape of h' via g1' analysis

Family: one-variable real analysis on the branch function.
Core mechanism: h' < 0 iff g1'(a) < 1/g1'(u(a)); the dips of h' are where
g1' < 1 (CE-3: g1'(0.42) ~ 0.98 at R = 1500).  At fp, g1'(fp) ~ sqrt(2)
and h'(fp) ~ sqrt(2) - 1/sqrt(2) > 0.
Target obligation: M.
First concrete deliverable: exact implicit formula for g1' from the closed
secular equation (sec(s, a, b, R) = 0); compute g1'' and locate extrema of
g1' numerically over the R-grid.
Fast falsification: hunt for a third zero of h' (none found).
Expected bottleneck: proving the number of critical points of g1' uniformly
in R without a closed form for the branch.
Status: ACTIVE.
Exact gap: prove h' has at most two zeros with the sign pattern - + -.
Next action: derive g1'' in closed form; test a convexity conjecture for
(g1 - id) on subintervals split at fp.

## Route C: endpoint signs via asymptotics

Family: perturbation/asymptotic analysis.
Core mechanism: R -> 1+ (branches collapse to (a0, a0), (b0, b0)) and
R -> inf (point-mass limit: lambda_1 -> 0, lambda_2 -> 4 pi^2, h(b0) ~
0.38/sqrt(R)).
Target obligation: E1.
First deliverable: exact asymptotic expansions of h(a0), h(beta).
Fast falsification: none needed (signs verified over grid).
Expected bottleneck: the R -> 1+ limit is degenerate to first order
(dR1/db = 0 at R = 1 on the branch); a clean two-term expansion was not
closed in this run.
Status: PARTIAL.
Exact gap: a complete proof of sign(h(a0)) < 0 < sign(h(beta)) for every
R > 1.
Next action: matched asymptotic at R -> 1+ with the correct degeneracy
scale; point-mass matched expansion at R -> inf.

## Route D: continuation in R from a proved base

Family: homotopy/continuation.
Core mechanism: C1 holds at R = 1+ trivially (I = {a0}); propagate the
uniqueness of the zero of h using nondegeneracy det J_res != 0.
Target obligation: C1.
First deliverable: prove det J_res = AC + B^2 != 0 on the branches for all
R > 1 (so the good root varies smoothly and no bifurcation occurs).
Fast falsification: det J_res < 0 at fp for all tested R (e.g. -107576 at
R = 4, -1.4 at R = 1e6); off-fp values not certified.
Expected bottleneck: det J_res away from fp is not established; the branch
could develop extra intersections without det J_res vanishing at the
intersection points themselves.
Status: BLOCKED (the missing lemma is not strictly easier than C1).
Exact gap: off-fp nondegeneracy; also the R -> 1+ degenerate base.
Next action: reopen only with a new mechanism (e.g. a uniform spectral
bound forcing B, C signs).

## Route E: perturbation from R = 1 (naive IFT)

Family: implicit function theorem at the degenerate base.
Core mechanism: at R = 1 the branches are vertical/horizontal lines through
(a0, a0) and (b0, b0); expand in epsilon = R - 1.
Target obligation: C1 (small R).
First deliverable: first-order expansion of g1, g2 in epsilon.
Fast falsification: dR1/db = 0 at R = 1 on the branch -> the naive IFT
fails (zero denominator).
Expected bottleneck: degenerate first order; correct expansion scale unknown.
Status: BLOCKED (degenerate base; no clean expansion closed).
Exact gap: matched expansion with the correct scaling of (b - a) and
(a - a0) in epsilon.
Next action: none until a new idea (Route C partial).

## Route F: disproof / counterexample hunting (kept active)

Family: adversarial search.
Core mechanism: search for a second zero of h in I, or a good root off the
symmetric line, over R in {1.02..1e7} and fine a-grids; interval-arithmetic
certificates for any candidate.
Target obligation: C1 (polarity: negative outcome).
First deliverable: dense h-profile scans (shape_v6, dip_study,
final_shape.json) - no second zero found.
Fast falsification: h > 0 on (fp, beta] with margin >= 1e-5 in all tested
configurations; no sign change other than the fp crossing.
Expected bottleneck: a counterexample would require h to dip below 0 right
of fp; the dips are shallow (|h'| <= ~0.012) but h stays positive.
Status: ACTIVE (no counterexample found; domain tested is finite).
Exact gap: none (open-ended); next: interval-arithmetic certificates over a
compact R-grid for the M-shape (CE-1 pattern).

## Route G: interval-arithmetic certificates on a compact R-grid

Family: verified computation (mpmath.iv).
Core mechanism: reproduce cert_ce1.py pattern (prior run) for h' and h
signs over a grid of R values to upgrade finite-grid evidence.
Target obligation: E1, M (finite R-grid only).
First deliverable: cert at (1500, 0.57364) and (1e4, 0.57364) - DONE
(recheck, CE-1).
Fast falsification: certified h' < 0 at the right dip for R = 1500, 1e4.
Expected bottleneck: certification is per-point; it cannot close the "for
every R > 1" quantifier.
Status: PARTIAL.
Exact gap: the analytic part (E1, M) remains.
Next action: optional, if time permits after the analytic attempt.

## Route summary

PROVED: R1-R6 (reduction to E1 + M + Z), P1-P4 and T1-T3 (rechecked),
O1c (rechecked).
ACTIVE: B (M-shape via g1'), F (disproof search).
PARTIAL: A (reflection route, structural part done), C (endpoint
asymptotics), G (interval certificates).
BLOCKED: D (continuation), E (R = 1 perturbation).
REFUTED: T4's hypothesis (Lemma A, pointwise g1' > g2'); naive sufficient
condition g1' > 1 on I (CE-3).