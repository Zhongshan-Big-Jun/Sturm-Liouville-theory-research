# Problem contract - independent re-audit of O1 Lemma 1 and Lemma 3

Run type: independent verifier pass (audit only; the audited artifact is NOT
modified).  All files ASCII punctuation, UTF-8 no BOM.

## Authoritative problem source (provenance chain)

- Task packet: agenda/task-packets/Q-20260806-o1-reaudit-5A1C3D.md
  (sha256 323097EEFDD4F06D886C1D146CBA941CF5AAB20F2D38D4E303C74DBA429C4FD7).
- Audit target (REVISED O1 proof): runs/rigorous-open-math-research/
  R-20260806T140000Z-o1revise-2ED02A/candidate_proof.md
  (sha256 728BD2B8D9F3AA9249B2E2A701006461AABC8154B18F47586A35677417254404).
- Producer self-audit (NOT trusted; rechecked from scratch):
  runs/rigorous-open-math-research/R-20260806T140000Z-o1revise-2ED02A/audit_report.md
  (sha256 F7AB2963AFACFAD332F77E9D43F6021DD9ACC1F534C22D1E60A2A820BE9B5F6B).
- Prior independent audit (context): runs/rigorous-open-math-research/
  R-20260806T011500Z-o1audit-422A69/audit_report.md
  (sha256 E6D1688963184DCBB87EC71EF8DB3B095A322D8B10D229CF8547ADB198B162CA),
  verdicts O1a PARTIAL, O1b FAILED-as-stated, O1c-O1f PROVED.
- Original draft: runs/rigorous-open-math-research/R-20260805T000000Z-gapn1-
  a1b2c3/O1_reduction_draft.md (sha256 C647297430348618A5120A3EAE5FAD09003B25EAFB9C8A8CCD9F449D1B397341).
- Premise sources: AEH arXiv:2407.02459v2 (papers/fundamental_gap.txt, sha256
  2F3C90E6127C8A13356236CA8DBA87E7A86FF8BE62856C4FAD3A89137B0C3D14);
  Keller 1976 (papers/keller1976.txt, sha256
  7EEAB2777926C4BA5ED3C3806647B4D8A9A9750AD75A5B0BB2A77653F422EF3C);
  Mahar-Willner 1976 (papers/mw1976.txt, sha256
  0DCD8172BAA80ECE55DC64804DC709279C6C56DA83FE470122644F63332C7B01).

## The underlying theorem (O1, normalized from the audited candidate)

Let R > 1, K = {rho measurable on [0,1] : 1 <= rho <= R a.e.}.  For the
Dirichlet string -y'' = lambda rho y on (0,1), y(0) = y(1) = 0, with
eigenvalues 0 < lambda_1(rho) < lambda_2(rho) and D(rho) = lambda_2(rho)
- lambda_1(rho):

(i)  sup_{rho in K} D(rho) = max_{0<=a<=b<=1} D(rho^{bar}_{a,b}),   rho^{bar} = R on (a,b), 1 elsewhere;
(ii) inf_{rho in K} D(rho) = min_{0<=a<=b<=1} D(rho^{well}_{a,b}),  rho^{well} = 1 on (a,b), R elsewhere;

and both extrema over the two-parameter families are attained.

## Audit contract (this run)

Target of the audit: the two CHANGED points of the revised proof, re-derived
from scratch (not accepted on the authority of the draft, the prior audit, or
the producer self-audit):

- O1a = Lemma 1: L^1-continuity of lambda_k on K via the symmetric
  Hilbert-Schmidt operator S_rho = M_{sqrt(rho)} T_0 M_{sqrt(rho)} and Weyl's
  inequality, including the F-001-corrected HS-constant chain leading to
  ||S_rho - S_sigma||_HS <= (R/4)||rho - sigma||_1^{1/2}.
- O1b = Lemma 3: the moving-jump Feynman-Hellmann derivative with the
  corrected sign dD/d eps = -(c_+ - c_-) f(x_j) (rightward) and the
  smoothing approximation R4 (Dirac-measure limit via C^inf mollification),
  including the two-sided differentiability claim.

Additional obligations:
- Verify the F-001 repair-chain arithmetic (pre-correction line vs corrected
  chain; final constant unchanged).
- Confirm the theorem statement was not silently upgraded.
- Recheck every theorem used as a premise against its original source and
  exact version: AEH Lemma 2.1, AEH Lemma 2.2, Weyl/min-max, Sturm
  oscillation, Rayleigh comparison bounds, and the context classification of
  Keller 1976 / Mahar-Willner 1976 (context only, not premises).
- O1c-O1f and the synthesis: consistency read only (their from-scratch
  independent audit was the prior run 422A69, PROVED).
- Deliver per-obligation verdicts (O1a, O1b) and an overall verdict on
  whether the manager may close O1.

## Permitted outcomes

- PASS for each audited obligation, with the re-derivation and any findings;
- REPAIRABLE_GAP / PARTIAL / FAILED / NOT_VERIFIABLE with the smallest failing
  claim and a certificate if a defect is found;
- the overall status label from the upstream skill's output protocol.

## Completion criteria

1. Every step of Lemma 1 and Lemma 3 re-derived independently and checked
   against the delivered text.
2. Every premise rechecked against the primary source (exact version).
3. F-001 chain arithmetic verified.
4. Numerical checks (independent scripts) recorded as evidence only, with any
   computational claim used at proof level argued analytically.
5. Verdicts per obligation O1a/O1b and overall, with the status label verbatim.

## Results that do not count as completion

- Restating the producer self-audit or the prior audit verdicts.
- A verdict based on the audited text's own claims without re-derivation.
- Numerical evidence alone for any proof-level claim.

## Constraints

- READ-ONLY with respect to the audited candidate proof (the audit must not
  modify it; gaps are reported precisely).
- Bounded scope: no new research directions; O2/O3 excluded.
- Do not call manage-math-research-program from inside the solver run.
- Chinese final reporting; ASCII punctuation in all files; clickable links in
  the final report.

## Ambiguities and conventions

- "Rightward"/"leftward" refer to the displacement of the jump point.  The
  signed parametrization (jump at x_j + eps) is audited; the one-sided
  distance derivatives are audited as equivalent corollaries.
- The audited candidate's NOTE that "rho^{1/2} T_rho rho^{1/2}" is not
  symmetric as written is audited as correct; the intended symmetric operator
  is the kernel form S_rho = M_{sqrt(rho)} T_0 M_{sqrt(rho)}.
- AEH is stated on (0,pi); the problem here is on (0,1); the affine rescaling
  is documented as harmless.

## Contract audit

Performed by this run against the packet, the audited candidate, the producer
self-audit, and the prior audit.  Fidelity checks:
- The two changed points are exactly Lemma 1 (O1a) and Lemma 3 (O1b).
- The underlying theorem statement matches the draft and the prior audit.
- The packet's "do NOT trust the producer self-audit" instruction is honored:
  all audited claims are re-derived here, not copied.
- Unknown fields (e.g. model) are recorded in repro_manifest.md; no invented
  provenance.