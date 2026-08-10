# Research ledger - independent re-audit of O1 Lemma 1 and Lemma 3

Run: R-20260806T151000Z-o1reaudit-5A1C3D.  Chronological entries.  All entries
record actual work; no invented data.

## R-001 (15:10Z) - Ingest and provenance
Read the task packet; created the run root; read the audited candidate proof
(candidate_proof.md, 318 lines), the producer self-audit (audit_report.md),
the prior independent audit (422A69), the repair-list candidate (422A69), and
the original draft.  Recorded hashes of all inputs.

## R-002 - Contract normalization
Normalized the audit contract (problem_contract.md): audited objects are
O1a (Lemma 1) and O1b (Lemma 3) in the REVISED proof; F-001 chain; theorem
statement fidelity; premises vs primary sources; O1c-O1f consistency read.

## R-003 - Premise recheck (AEH)
Read papers/fundamental_gap.txt lines 84-101 (Lemma 2.1) and 197-220 (Lemma
2.2); verified the FH formula, the normalization int w u_n^2 = 1, the sign
convention, and items (1)-(5).  Confirmed interval (0,pi) with the affine
rescaling documented.  Keller 1976 and Mahar-Willner 1976 headers verified as
the ratio problems in the bounded-jump class (context only; not premises of
O1).

## R-004 - Lemma 1 analytic re-derivation
Re-derived the S_rho presentation, the similarity algebra, the eigenvalue
identity, the HS bound with the corrected constant chain, the Weyl step, and
the lambda conversion.  All steps checked (audit_report.md Section 2).

## R-005 - Lemma 3 analytic re-derivation
Re-derived the moving-jump sign from the distributional identity
d/d eps rho_eps = -(c_+ - c_-) delta_{x_j} and AEH Lemma 2.1; re-derived the
smoothing limit (uniform H^2 bounds, Dirac family, DCT, two-sided
differentiability) and the stationarity consequence (audit_report.md
Section 3).

## R-006 - F-001 chain arithmetic
Verified the corrected chain (R/32)(||A||_2^2 + ||A||_1^2) <= (R^2/16)||A||_1
and the final constant (R/4)||A||_1^{1/2}; confirmed the pre-correction line
was not derivable and the repair does not change the conclusion.

## R-007 - Independent numerics part 1 (HS/Weyl)
Wrote fd_lib.py (finite-difference solver, written from scratch) and
verify_hs_weyl_independent.py.  Ran: H1 11/11 HS-bound pairs (ratios
0.073-0.165), H2 22/22 Weyl cases, H3 22/22 comparison bounds, H4 11/11
F-001 chain checks.  All PASS.

## R-008 - Independent numerics part 2 (moving-jump FH)
First attempt used the fixed-grid FD solver for sub-cell jump motion; produced
gross artifacts (grid-pinning).  Diagnosed and recorded as a check-method
failure (F-102), NOT a mathematical counterexample.  Replaced with the exact
transfer-matrix solver tm_lib.py.  Final run: V1 16/16 lambda derivatives
within 5.3e-6 at eps = 1e-4; V2 16/16 D derivatives within 5.3e-6; V2b sign
flip confirmed; V3 dD/du = -2(R-1)f(u) errors <= 1.9e-6; V4 stationarity at
u*: f(u*) ~ 2.9e-7, right/left = -0.0144/+0.0144.  All PASS.

## R-009 - Independent numerics part 3 (smoothing + Dirac)
verify_smoothing_dirac_independent.py: D1 Dirac-family point evaluation error
O(delta^2) (7.2e-3 at delta = 0.05 to 1.9e-6 at delta = 0.001); D2 smoothed
moving-jump derivative within 0.03-0.3% of the Dirac limit for delta in
[0.002, 0.04].  PASS (evidence).

## R-010 - Independent numerics part 4 (AEH pointwise, H^2 bounds, contract)
verify_aeh_pointwise_independent.py: A1 AEH pointwise FH to 9e-11 / 6e-8; A2
H^2 bounds 8/8; A3 R=4 contract sanity sup barrier ~ 32.6138 (rel 5e-6),
inf well ~ 6.7845 (rel 1.6e-6), argmax ~ (0.451, 0.548) on the symmetric
line.  PASS (evidence; A3 is O2/O3 territory, sanity only).

## R-011 - O1c-O1f consistency read
Re-read Lemma 2 (Wronskian), Lemma 4 (compactness + stationarity), Lemma 5
(density), Lemma 6 (bang-bang), and the synthesis in the revised text.
Consistent with the prior independent audit; no new gap.  F-003 (presentational
hypothesis phrasing) remains valid; no circularity.

## R-012 - Synthesis of the audit report
Composed audit_report.md with per-obligation verdicts (O1a PASS, O1b PASS),
the F-001 verification, premise rechecks, findings log (F-101 presentational
uniformity note; F-102 check-method artifact), residual gaps (none), and the
overall status label INDEPENDENTLY_AUDITED_PROOF (O1 scope).

## R-013 - Manifest and run record
Wrote repro_manifest.md (hashes of all inputs and outputs), status_and_
literature.md, counterexample_log.md, approach_registry.md, obligation_graph.
md, problem_contract.md, candidate_proof.md (audited-artifact pointer), and
updated run-manifest.json (completed_at, upstream_status_verbatim, artifact
hashes).  Verified all outputs written UTF-8 no BOM.