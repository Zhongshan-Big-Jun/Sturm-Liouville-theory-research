# Candidate proof - audited artifact reference

This run is an independent re-audit (verifier pass) of the REVISED O1 proof.
Per the task packet, the audit must NOT modify the audited candidate.  This
file therefore records the audited artifact's location, normalized statement,
and the post-audit status; it is NOT a substitute for the audited text.

## Audited artifact

- Path: runs/rigorous-open-math-research/R-20260806T140000Z-o1revise-2ED02A/candidate_proof.md
  (sha256 728BD2B8D9F3AA9249B2E2A701006461AABC8154B18F47586A35677417254404)
- Producer self-label: CANDIDATE_COMPLETE_PROOF
- Post-audit label (this run): INDEPENDENTLY_AUDITED_PROOF (O1 scope)
- Audit report: audit_report.md in this run (R-20260806T151000Z-o1reaudit-5A1C3D)

## Normalized theorem statement (O1, as audited)

Let R > 1 and K = {rho measurable on [0,1] : 1 <= rho <= R a.e.}.  For the
Dirichlet string -y'' = lambda rho y on (0,1), y(0) = y(1) = 0, with
eigenvalues 0 < lambda_1(rho) < lambda_2(rho) and D(rho) = lambda_2(rho)
- lambda_1(rho):

(i)  sup_{rho in K} D(rho) = max_{0<=a<=b<=1} D(rho^{bar}_{a,b}),
     rho^{bar}_{a,b} = R on (a,b), 1 elsewhere;
(ii) inf_{rho in K} D(rho) = min_{0<=a<=b<=1} D(rho^{well}_{a,b}),
     rho^{well}_{a,b} = 1 on (a,b), R elsewhere;

and both extrema over the two-parameter families are attained.

Edge cases are inside the closed families (a = b, (a,b) = (0,1), a = 0,
b = 1); R = 1 is excluded as trivial.

## Changed points audited in this run

- Lemma 1 (O1a): L^1-continuity of lambda_k on K via the symmetric
  Hilbert-Schmidt operator S_rho = M_{sqrt(rho)} T_0 M_{sqrt(rho)} and Weyl's
  inequality; HS constant chain (F-001 corrected).  Verdict: PASS.
- Lemma 3 (O1b): moving-jump FH derivative dD/d eps = -(c_+ - c_-) f(x_j)
  (rightward) via smoothing (R4); two-sided differentiability; stationarity.
  Verdict: PASS.

## Proof obligation status (post-audit)

O1a PASS, O1b PASS, O1c-O1f PASS (prior independent audit + consistency
read), synthesis PASS, theorem-statement fidelity PASS, F-001 chain VERIFIED.
No residual gap within O1 scope.  O2/O3 out of scope.

## Not modified

The audited candidate proof was not modified by this run.  Any future repair
must be issued by a reviser role in a separate run, per the upstream skill's
revision policy.