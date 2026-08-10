# Counterexample log (run R-20260806T140000Z-o3ac1-42F931)

Chronological log of refuted claims, edge cases, and certificate work.  CE
numbers continue the prior run (R-20260806T011500Z-o3abranch-E8E56F).

## CE-1 (RECHECKED this run): Lemma A (g1' > g2' pointwise) is false for large R

Statement attacked: for every R > 1, g1'(a) > g2'(a) on the common range.
Finding: FALSE for R >= ~1400.  Witness (R, a*) = (1500, 0.57364) and
(1e4, 0.57364).
Recheck this run: re-ran the interval-arithmetic certificate logic at
R = 1500, a* = 0.57364.  Certified h'(a*) in [-3.4298e-4, -3.4298e-4] < 0
(mpmath.iv, outward rounding, iv.prec = 220; root enclosures of width
~5e-28, sign-definite partials and denominators; good-root checks v(a*) > 0,
v(b2*) < 0 certified).  At R = 1e4: h'(a*) in [-3.2030e-3, -3.2030e-3] < 0.
The certificate file (prior run) is
runs/rigorous-open-math-research/R-20260806T011500Z-o3abranch-E8E56F/
reproducibility/cert_ce1.py; this run re-ran the point values through
c1_lib.py (float64) and confirmed h'(0.57364) = -3.4e-4 at R = 1500.
Trust model: mpmath.iv outward rounding; standard verified computation, not
machine-checked by a proof assistant.  Not a counterexample to C1 (h still
crosses zero exactly once).

## CE-2 (RECHECKED): spurious least-squares minima at large R are not roots

At large R, residual-minimization finds configurations with residual
~2.6e-7 and v(a) ~ 1 that are NOT roots (R1, R2 not simultaneously zero).
Excluded by good-root checks (residual tolerance is scale-dependent;
absolute residual alone is unreliable).  No effect on C1.

## CE-3 (NEW this run): the naive sufficient condition "g1' > 1 on I" is false

Statement attacked: sign of h via the MVT form sign(h) = sign(a - u(a)) *
sign(g1'(xi) - 1) would be settled if g1' > 1 on I.
Finding: FALSE for R >= ~1000.  g1' dips below 1 near a ~ 0.42-0.44:
- R = 1500: g1'(0.42) = 0.9804
- R = 1e4:  g1'(0.43) = 0.9897
- R = 1e6:  g1' min ~ 0.99 (dip persists)
The dip is shallow; g1'(fp) > 1 always (R=4: 2.752; R=1e4: 1.421; R=1e6:
1.411).  Consequence: the integral identity (R4.1) h(a) = integral_{u(a)}^a
(g1'(t) - 1) dt is the correct exact object; any proof of the sign of h must
use the full integral, not a pointwise bound.  Recorded in
candidate_proof.md Remark after R4 and in the ledger (R-106, R-108).

## CE-4 (NEW this run): multi-sheet structure of Gamma_2 at large R

At R = 1500, a = 0.57364 the equation R2(a, b) = 0 with v(b) < 0 has THREE
solutions (b ~ 0.57379, 0.57437, 0.57601); only the largest (through the
component (b0, b0)) is the main-sheet value g2(a).  At the extra points
v(a) < 0, so they are not sign-consistent good roots and do not affect O3a.
Consequence for method: direct tracing of Gamma_2 near the right end is
hazardous; this run computes g2 via the reflection formula g2(a) =
1 - g1^{-1}(1-a) from the single-sheeted g1 (Lemma R2).  Also at R = 1e4,
a <= 0.55 the R2-root is unique.

## Edge cases tested (no counterexample to C1)

- R -> 1+ (R = 1.02, 1.05, 1.1, 1.2): I = [a0, a_max1] with a_max1 slightly
  above a0; h(a0) < 0, h(a_max1) > 0; h' > 0 on I.
- R -> inf (R = 1e5, 1e6, 1e7): fp -> 1/2 (1/2 - fp ~ 0.118/sqrt(R));
  h(b0) ~ 0.38/sqrt(R) > 0; h' dips exist but h > 0 on (fp, beta].
- a = b (zero-width barrier): rho = 1 identically; f_0 has zeros a0, b0;
  not a good root for R > 1; excluded from I.
- Near-diagonal roots at large R (b - a ~ 4e-4 at R = 1e5): found only after
  switching to geometric b-scans (ledger R-104); these are the fp and nearby
  branch points, single roots on the main sheets.
- Multi-sheet Gamma_2 hazard (CE-4): excluded by the main-sheet convention.

## Search code and certificates

- c1_lib.py: secular roots (adaptive scan to 6 pi; ledger R-103), branch
  values, residuals, v, partials, a_fp.
- verify_refl.py / trace*.py: reflection identities R1, sigma(Gamma_1)
  subset Gamma_2.
- hshape.py, dip_study.py, final_shape.py: h and h' profiles (data in
  shape_v6.json, dip_study.json, final_shape.json).
- CE-1 certificate (prior run, rechecked): cert_ce1.py (mpmath.iv).

## Status

No counterexample to C1 found over the tested domain (R in {1.02..1e7},
fine a-grids).  Two routes refuted (Lemma A via CE-1; g1' > 1 via CE-3);
one method hazard documented (multi-sheet Gamma_2, CE-4).  All three are
registered as reusable lessons.