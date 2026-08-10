# Status and literature

Run: R-20260806T140000Z-keylemmaaudit-2F83B1 (independent audit)

## Problem status

The audited statement is the KEY LEMMA of the origin run
R-20260805T000000Z-gapn1-a1b2c3 (agentA_O2_single_crossing.md, Section 2.9):
the single remaining unproven step in the proof that the symmetric two-block
barrier family has a unique maximizer of the spectral gap (obligation O2 of the
project problem O-2026-SL-GAP-3B7A2C).

The target run R-20260806T070000Z-keylemma2b-0A6D8F claims CANDIDATE_COMPLETE_PROOF
with obligations R1, R2, L4box, L5box closed (upstream_status_verbatim:
CANDIDATE_COMPLETE_PROOF).  This run independently audits that claim.

## Audit result in one line

INDEPENDENTLY_AUDITED_PROOF: every obligation of the KEY LEMMA (both (LOG) and
(FP)) is re-derived and re-verified from first principles; all five interval
certificates are re-verified with a sound independent Decimal interval engine;
no fatal or repairable gap was found.  See audit_report.md for per-obligation
verdicts and the exact caveats.

## Sources used (all read in this run)

- Task packet: agenda/task-packets/Q-20260806-keylemma-audit-2F83B1.md
- Target run: runs/rigorous-open-math-research/R-20260806T070000Z-keylemma2b-0A6D8F/
  (candidate_proof.md, problem_contract.md, audit_report.md, repro_manifest.md,
  reproducibility/verify_certificates_indep.py and the other shipped scripts)
- Parent run: runs/rigorous-open-math-research/R-20260806T011500Z-keylemma-E58FB1/
  (candidate_proof.md: the four-lemma reduction, L1, L2, B4, B5, B7)
- Origin run: runs/rigorous-open-math-research/R-20260805T000000Z-gapn1-a1b2c3/
  agentA_O2_single_crossing.md (definitions of E, O, alpha_k, G, H, Ftilde,
  the KEY LEMMA, T1-T4)
- Certificates: R-20260806T050000Z-keylemma2-5A35E5/reproducibility/
  cert_{dM2dq,c4,L4box,L5box}_boxes.json and
  R-20260806T070000Z-keylemma2b-0A6D8F/reproducibility/cert_dM2dq_strip_boxes.json

## Known theorems used as premises (all re-verified here)

No external mathematical theorem is used as a premise.  The proof is elementary
(calculus: monotonicity, implicit differentiation, Taylor/alternating series with
explicit remainders) plus finite rigorous interval computations.  The following
are project-derived lemmas, each re-verified in this run:

- E' = O' = -q/Phi and the implicit derivative alpha' = -a Phi/(q + c Phi).
- G formula (d/dc log Mtilde along the curve).  [symbolic diff = 0]
- IN = G_2 * POS with POS > 0 on the odd curve.  [symbolic diff = 0]
- M2 = dIN/du, dM2/dq.  [symbolic diff = 0]
- M2(1,u) = pi h(u).  [symbolic diff = 0]
- C4 identity IN = A*K(v) on the c = 0.4 curve.  [symbolic diff = 0 with the
  domain fact atan(tan v) = v for v in (0, pi/2)]
- C4 tail identity T^3 K (exact).  [symbolic diff = 0]
- CORNER closed form G_2(1/2;q) = 2q(q+1)(pi - x - 3 sin x)/(2q+1)^(3/2),
  x = 2 arcsin(1/sqrt(2(q+1))).  [symbolic + 1e-45 numeric]
- B5: H(q,1/2) = 2 pi q (q+1)/(2q+1)^(3/2).  [symbolic diff = 0]
- B4: Ftilde'(q,1/2) = 2 pi (cos x - 1)^3 P(x)/sin^3 x < 0, P(x) = 3x^2 + 6x sin x
  - 3 pi x - 3 pi sin x + pi^2, with P(x) - (pi - 3x)^2 = 3(x - sin x)(pi - 2x) > 0.
  [symbolic diff = 0 + 1e-45 numeric]

## Novelty status

POTENTIALLY_NEW within the project.  No claim of external novelty is made; the
KEY LEMMA is a project-derived statement.  The surveyed SL literature
(Keller 1976, Mahar-Willner 1976, Hedhly 2021, AEH arXiv:2407.02459, etc.) does
not contain this exact inequality; no external theorem is used as a premise.

## Known risks and caveats (see audit_report.md Section 5)

1. riarith.py (the producer's Decimal engine) has a confirmed non-strict iv_sqrt
   (Decimal.sqrt ignores the rounding mode in Python 3.10).  This run's engine
   implements its own directed sqrt (validated on 3000 random cases) and does not
   rely on riarith.  All sign conclusions were reproduced with the audit engine.
2. The shipped C4 verifier used stale region constants; this run uses the
   certificate's own leaf endpoints plus certified-PI coverage checks.
3. The interval engines are not formally verified in a proof assistant; the
   soundness model is documented in reproducibility/audit_iv.py and the
   certificate re-verification is an executable check (repro_manifest.md).
