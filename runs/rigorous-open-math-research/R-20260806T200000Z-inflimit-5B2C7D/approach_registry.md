# Approach registry - Theorem A (R-20260806T200000Z-inflimit-5B2C7D)

Route families by mechanism.  Statuses: UNEXPLORED | ACTIVE | PROMISING |
PARTIAL | BLOCKED | REFUTED | MERGED | PROVED.
All files ASCII punctuation, UTF-8 without BOM.

## R1 - T2 sign chain (K~ -> J -> G -> S) - PROVED

Core mechanism: parametrize a in (pi/2, pi) |-> u(a); derive the identities
J' = 4a K~/sin^2 a, G' = 4 sin^2 a * J, Dbar'(u(a)) = S(u(a)) = -c(a) G(a)
with c(a) > 0; prove h' sin^3 a < 0 (each term negative), giving the unique
zeros a_1 (K~), a* (J), a_G (G) and hence S < 0 / = 0 / > 0 with the unique
root u* and global strict minimum of Dbar.
Why it works: pure elementary calculus, no numerical input; all signs are
forced by the monotonicity chain.
Required known results: P1-P3 (classical Taylor bounds); no external theorem.
First concrete deliverable: PDF Sec. 2.5; symbolic re-verification script 07.
Fast falsification tests: numeric zero locations and sign pattern (script 02).
Status: PROVED.  Exact gap: closed (with the a_G/a* labeling correction).

## R2 - Lemma A'' elementary phase-coordinate proof - PROVED

Core mechanism: exact identity G - Dbar = (def_1 - def_2)/u^2; bracket the
phases delta_1, delta_2, z_2, psi_2 by monotone functions; lower-bound
def_1 and upper-bound def_2; control the ratio by B(t) = 2t^4/(t^2+v^2+v)
<= 9 with v = -t cot t.
Why it works: the singular perturbation epsilon -> 0 is fully absorbed by the
phase coordinates; the heavy-block phase theta_k stays in its branch while
the light-block phase z_k collapses to 0 with an explicit cot-series
remainder.
Required known results: cot-series certificate (P2), phase brackets (L1.1,
derived), arctan bounds (P3).
First concrete deliverable: PDF Sec. 2.3; certificate scripts 18-19.
Fast falsification tests: pointwise G - Dbar >= 0 on grids R in
{1500,1e4,1e6,1e8} (minimum margin 3.97e-10, evidence), def_1 LB vs def_2 UB
(evidence), identity to 1e-42 (evidence).
Status: PROVED (analytic; constants certified).  Exact gap: closed.

## R3 - Deep sliver elementary cover (w <= 2) - PROVED (certified)

Core mechanism: split w in (0,2] into regions A (B_1), B (B_2), C (B_3,
analytic, = 25 at w_cap), D (max(THB, D2B)); certify grids on R in
[1500, 1e8] with directed rounding; analytic tails R >= 57050 (A, B) and
R >= 1e8 (D).
Why it works: the sliver u <= 2/sqrt(R) makes the light block nearly
degenerate; elementary one-sided bounds on the phases suffice.
First concrete deliverable: PDF Sec. 2.4 + Sec. 3.1; script 16 (PASS,
worst 42724/293.36/25/77.67).
Status: PROVED (elementary bounds + computer-assisted certification).
Exact gap: closed.

## R4 - Medium region monotonicity grid (w >= 2, u in [0.02,0.2]) - PROVED (certified)

Core mechanism: delta brackets + Feynman-Hellmann monotonicity d mu_k/du < 0,
d mu_k/dR > 0; certify G >= 25 on 115185 cells (script 17, worst corner
bound 27.99).
Why it works: needed only to extend the w >= 2 lower bound to the full
domain (Lemma A'' already gives G >= Dbar(u), and Dbar(u) is large away from
u*; this grid is an independent cross-check, not part of the analytic chain).
Status: PROVED (certified).  Exact gap: closed.

## R5 - T3 interval enclosure - PROVED (certified)

Core mechanism: mpmath.iv bisection on S, interval propagation to Dbar,
rational margin vs 3 pi^2 and 25.
Status: PROVED (verified computation).  Exact gap: closed.

## R6 - T1 assembly - PROVED

Core mechanism: limsup via fixed-u convergence at u*; liminf via the two
lower bounds; near-minimizer convergence via the accumulation-point argument
with T2 strict monotonicity and the tail limits.
Status: PROVED.  Exact gap: closed.

## F1 - dG/dR|w > 0 route for the deep sliver - REFUTED (abandoned)

Core mechanism: prove G increasing in R along constant w and reduce the
sliver to the R = 1500 curve.
Evidence: numerically true on grids (worst slack 0.93 at (w=2, R=1500)) but
no elementary proof was found; the constant-w rescaling couples w and
epsilon.  Replaced by the region cover (R3).  Ledger R-012.

## F2 - H > 0 route (dG/du < 0) - ABANDONED

Core mechanism: prove H = dG/du < 0 on the sliver to restrict the minimum to
the boundary.  Numerics: H > 0 on R >= 1500, w <= 2 (min 0.65050 at the
corner), but H values at w <= 1/2, R >= 1e5 are branch-unreliable (bisect
bracket sensitivity); H > 0 is NOT needed by the final architecture.
Ledger R-012.

## F3 - 2D P1-only corner scheme - REFUTED

Core mechanism: single linear bound across the corner cell.  Fails near
R ~ 1e6 (d mu_1/dR ~ 0.617 along w = 2 exceeds G/Delta R) and near u -> 0
(mu_1(R_2, 0) = R_2 pi^2 too crude).  Replaced by the 1D-curve + region
cover.  Ledger R-012.

## F4 - R-012 elementary bound for w in (1/2, 2] - REFUTED (bogus)

The formula [tan x + cot(x + B_2/(2w))]*(1 - eps^2 M^2/3)*(pi - eps tan x)/
(w^2 eps) uses delta_2 - delta_1 >= delta_2 + eps tan x with the WRONG
direction (delta_1 >= -eps tan x gives delta_2 - delta_1 <= delta_2 + eps tan
x).  Verified overestimate: 12186 > true G = 2460 at (1500, 0.50375); the
formula even goes negative near w = 0.5.  Correct replacement:
A = theta_2^2 - theta_1^2 >= delta_2^- (pi - eps tan x) with the nested
delta_2^- bracket.  Ledger R-013.

## F5 - Seed bug for w <= 1/2 (fourth-eigenvalue branch) - CORRECTED

The "certified corner" diagnostics for w <= 1/2 used seed
max(pi^2/(4w^2), 4 pi^2)*R*0.9999 for mu_2, which converges to the FOURTH
eigenvalue branch (4 pi^2 R), not the second.  Correct second eigenvalue at
(R=1e6, w=0.5): mu_2 = 9.8696e6 (nu_2 -> pi^2), G/R -> 0.384; at w = 0.4:
mu_2 = 1.5413e7 (nu_2 -> pi^2/(4w^2) = 15.42).  Corrected A-limit:
A_inf(w) = pi^2(1/4 - w^2) for w in (1/4, 1/2), 3 pi^2 w^2 for w in (0, 1/4].
Ledger R-009, R-012.

## F6 - Script 19 v1 wrong parameter v - CORRECTED

v = u/ell = -t cot t (from tan t = -t ell/u), NOT -cot t.  Because
f(t) = 2t^4/(t^2+v^2+v) decreases in v >= 0, the v1 certificate (smaller v)
remained a valid upper bound, but the formula was wrong; v2 certifies with
the correct v: f-max = 5.422510, ratio 0.825511 < 1.  Recorded in the PDF,
the tool file lemma-A-doubleprime.md, and repro_manifest.md.

## V1 - Numeric battery (evidence only)

Scripts 01-04: packet claims, limiting curve, secular convergence, sliver
profiles.  Scripts 05-07: interval value, symbolic identities, part-1
symbolic.  Scripts 08-15: certified part 2, deep-sliver probes/elementary
bounds/region D, minima of theta/delta.  Scripts 16-19: final certifications
(PASS, outputs recorded in repro_manifest.md).  All scripts print a checksum
of their own source; per-file sha256 in repro_manifest.md.
Status: COMPLETED (evidence; none of it is a proof).