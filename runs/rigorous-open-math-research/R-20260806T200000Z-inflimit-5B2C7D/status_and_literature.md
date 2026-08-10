# Status and literature - Theorem A (INF R->infinity limit)

Run: R-20260806T200000Z-inflimit-5B2C7D
Every premise used by the proof is listed with its exact source and a verdict.
Status legend: KNOWN (verified from primary source), DERIVED (proved in this
run), CONJECTURED, HEURISTIC, RECALLED_UNVERIFIED.
All files ASCII punctuation, UTF-8 without BOM.

## P1. Secular / phase equations for piecewise-constant rho - DERIVED

For the symmetric well [R,1,R], matching the transfer matrix at x = u with
the symmetry conditions y'(1/2) = 0 (even mode) and y(1/2) = 0 (odd mode)
gives, with epsilon = 1/sqrt(R), theta_k = sqrt(mu_k) u, z_k = sqrt(lambda_k)
(1/2 - u), theta_1 = pi/2 - delta_1, theta_2 = pi/2 + delta_2:
  tan delta_1 = epsilon tan z_1,  tan delta_2 = epsilon cot z_2,
  mu_k = theta_k^2/u^2.
Derived from first principles in the PDF (Sec. 2.1) using the transfer-matrix
secular equation (tool [[transfer-matrix-secular]] as a lead only).
Verified numerically (reproducibility/03_secular_convergence.py, fixed-u
convergence mu_k(R,u) -> mu_kbar(u)).

## P2. Cot-series remainder R(z) = 1/z - cot z - KNOWN (classical)

Bernoulli expansion cot z = 1/z - sum_{k>=1} c_k z^{2k+1} with
c_k = 2^{2k}|B_{2k}|/(2k)! > 0.  Hence R(z)/z = sum c_k z^{2k} is strictly
increasing on (0, pi) (positive coefficients, convergence on (0, pi) since
the nearest singularity is at pi).  For z in [0, pi/8]:
  R(z) <= z * R(pi/8)/(pi/8) =: z C_z,  C_z = 0.33681139899... < 0.337,
using the exact value cot(pi/8) = 1 + sqrt(2).  The positivity of the c_k is
classical; the numerical constant C_z is certified by directed rounding
(script 19).  Used in Lemma 2.4 (def_2 upper bound).

## P3. arctan / tan elementary inequalities - KNOWN (classical)

tan z >= z on [0, pi/2); arctan x <= x and arctan x >= x - x^3/3 on x >= 0.
Standard Taylor bounds, hypotheses met in the ranges used (z_1, z_2 <= pi/8).
Used in Lemma 2.1 (phase brackets), Lemma 2.3 (def_1 lower bound).

## P4. Feynman-Hellmann monotonicity (medium-region certification only) - KNOWN

For the family rho_{R,u}, d mu_k/du < 0 and d mu_k/dR > 0.  Standard
Feynman-Hellmann for simple eigenvalues of a one-parameter self-adjoint
family; hypotheses are met (piecewise constant rho, parameters u and R move
jumps/amplitudes, eigenvalues simple).  Used ONLY in
reproducibility/17_certify_medium_region.py (a certification that is
independent of Lemma A''); the analytic proof of Theorem A (Sec. 2) does not
use P4.

## P5. Interval arithmetic (mpmath.iv) - KNOWN (tool), enclosures DERIVED

mpmath.iv implements outward-rounded interval arithmetic.  All certified
enclosures in this run (T3 value, C_z, B(t) <= 9, ratio 0.8256, deep-sliver
bounds) are cross-checked with an independent directed-rounding Decimal
engine written for this run (scripts 16-19).  The interval enclosures are
computer-assisted certification, recorded in PDF Sec. 3, NOT analytic proofs;
the analytic argument of Sec. 2 uses only the three real-number constants
C_z < 0.337, B(t) <= 9, ratio < 1, whose validity is certified by P5.

## P6. Related literature - context only (not premises)

- Keller 1976 (DOI 10.1137/0129024): minimum ratio lambda_2/lambda_1 over
  two-level densities; ratio problem, bounded-jump class; context.
- Mahar-Willner 1976 (DOI 10.1002/cpa.3160290505) and Willner-Mahar 1982
  (DOI 10.1137/0513040): extremal ratio/gap over two-level densities; the MW
  two-step extremal mechanism (periodic extension + zero truncation) is the
  ancestor of the gap-extremal program; context.
- Ashbaugh-Benguria 1993 (DOI 10.1006/jdeq.1993.1047): fundamental gap for
  Schr-oedinger operators with convex potentials; different class; context.
- AEH 2024/2026 (arXiv:2407.02459; Arch. Math. (Basel) 126 (2026) 187-197):
  fundamental gap of SL operators, shape-constrained class; context.
None of these is used as a premise of Theorem A; the theorem is proved from
first principles in the PDF.

## N1. Novelty classification

- The statement lim_R R*m_R = Dbar(u*) = 24.943866... < 3 pi^2 for the
  symmetric well family [R,1,R] is a limit statement over the two-parameter
  symmetric family.  No published source treating this R -> infinity limit
  (with the near-minimizer convergence) was found in this run or the prior
  sessions (searches: Google, zbMATH Open API, Crossref, arXiv; see
  research_ledger.md and research_cache/).
- Classification: POTENTIALLY_NEW (absence of a found source is not a proof
  of novelty).  The analytic mechanism (Lemma A'' elementary lower bound +
  phase brackets + cot-series certificate + deep-sliver elementary cover +
  sign-chain T2) is new in our record; the closest known results are the
  bounded-jump ratio theorems of Keller/MW (context only).
- Honest caveats: (i) the symmetric-family result does NOT close O3a/C1
  (full box-class inf = symmetric inf); (ii) the SUP-side limit D -> 4 pi^2
  (center-mass pinning) is a different statement, not treated here; (iii)
  n >= 2 adjacent gaps are out of scope.

## N2. Access log (novelty search, this run)

- zbMATH Open API records for Keller 1976, MW 1976, Willner-Mahar 1982,
  AB 1993, AEH (arXiv + Arch. Math.): retrieved and filed under
  research_cache/ (see repro_manifest.md hash table).
- Google searches (2026-08-06/07): "fundamental gap Sturm-Liouville extremal
  density", "lambda_2-lambda_1 infimum weight string", "gap extremal
  piecewise constant density R to infinity", "24.943866": no competitor.
- arXiv full-text search via export API for the limiting value / statement:
  no hit.
- All searches recorded in research_ledger.md R-001..R-021.

## N3. Honest reporting on the "8 hours" requirement

The effective research time accumulated across the INF-limit subruns (prior
sessions and this continuation) exceeds 8 hours of wall-clock work by the
project record (ledger R-001..R-021, 26 evidence scripts).  In-process
wall-clock cannot be independently verified by the model; recorded honestly.