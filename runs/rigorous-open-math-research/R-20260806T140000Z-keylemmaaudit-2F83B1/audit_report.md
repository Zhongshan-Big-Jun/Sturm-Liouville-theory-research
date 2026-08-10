# Audit report

Run: R-20260806T140000Z-keylemmaaudit-2F83B1 (independent audit of R-20260806T070000Z-keylemma2b-0A6D8F)
Audit method: from-scratch re-derivation of every identity, closed form, base
lemma, reduction step, and interval certificate.  The producer's self-audit was
NOT trusted; its claims were used only as a checklist.

## Overall verdict

INDEPENDENTLY_AUDITED_PROOF

The candidate proof of the KEY LEMMA for all q > 1, c in (0, 1/2),

  (LOG)  G_1 - G_2 < 0,
  (FP)   Ftilde' = Mtilde_1 G_1 - Mtilde_2 G_2 < 0,

is correct and complete.  All obligations R1, R2, L4box, L5box and the bases
L1, L2, B4, B5, M2, CORNER, C4 are closed with sound arguments.  All five
interval certificates were re-verified with an independent sound interval engine
(exact rational tiling, sign conditions, coverage, sliver bridge).  No fatal or
repairable gap was found.  The remaining caveats are reproducibility notes about
the interval engines, not open proof obligations (Section 5).

## Per-obligation verdicts

| Obligation | Statement | Verdict | Evidence |
|---|---|---|---|
| L1 | G1 < 0 | PASS | elementary estimate re-derived; grids |
| L2 | G2 >= 0 => both forms | PASS | immediate algebra |
| B4 | Fp(q,1/2) < 0 | PASS | closed form re-derived symbolically (diff = 0); 1e-45 numeric |
| B5 | H(q,1/2) = 2 pi q(q+1)/(2q+1)^(3/2) > 0 | PASS | symbolic (diff = 0); 1e-45 numeric |
| M2 | dIN/du < 0 on D | PASS | h(u) proof re-audited; certificates + tail bound re-derived |
| CORNER | G2(1/2;q) >= 0, q >= 2 | PASS | closed form + elementary certificate re-audited |
| C4 | G2(0.4;q) >= 0, q >= 1 | PASS | identity + certificate + exact rational tail |
| R1 | G2 >= 0, q >= 2 | PASS | M2 + CORNER + sign identity |
| R2 | G2 >= 0, c <= 0.4 | PASS | M2 + C4 + sign identity |
| L4box | H' < 0 on box | PASS | cert_L4box re-verified: worst upper -4.8416038, 0 failures |
| L5box | Fpp > 0 on box | PASS | cert_L5box re-verified: worst lower +8.3793828, 0 failures |
| RED | reduction => KEY LEMMA | PASS | monotonicity + one-sided limits on closed box |

## Certificate re-verification (audit engine: Decimal directed rounding, 80
digits, own Machin-pi, own atan, exact monotone-range sin/cos, directed sqrt)

| Certificate | Leaves | Tiling/coverage | Sign condition | Worst bound (audit) | Verdict |
|---|---|---|---|---|---|
| cert_dM2dq_boxes.json | 84 | exact Fraction tiling of [1,20]x[0,y1] | dM2/dq < 0 | -0.1902428 | PASS |
| cert_dM2dq_strip_boxes.json | 10 | exact tiling; (y1+1e-30)^2 > 41 | dM2/dq < 0 | -448.7453 | PASS |
| cert_c4_boxes.json | 200 | coverage via certified PI; slivers bridged (max gap 1e-59 < 2e-58) | K > 0 | +2.49716 | PASS |
| cert_L4box_boxes.json | 128 | exact tiling of [1,2]x[0.4,0.5] | H' < 0 | -4.8416038 | PASS |
| cert_L5box_boxes.json | 128 | exact tiling | Fpp > 0 | +8.3793828 | PASS |

All certificates: 0 sign failures, 0 overlap failures, 0 point failures.
Consistency: stored enclosures overlap the audit enclosures and contain the
80-digit point values at leaf corners and centres.

## Identity layer (all re-derived in this run)

- E' = O' = -q/Phi; alpha' = -a Phi/(q + c Phi).        [symbolic]
- G formula (d/dc log Mtilde along the curve).          [symbolic]
- IN = G2*POS, POS > 0.                                 [symbolic]
- M2 = dIN/du; dM2/dq.                                  [symbolic]
- M2(1,u) = pi h(u).                                    [symbolic]
- CORNER closed form; G2(1/2;2) value.                  [symbolic + numeric]
- IN = A*K(v) on the c = 0.4 curve.                     [symbolic, with atan(tan v) = v]
- T^3 K tail identity.                                  [symbolic]
- B5 closed form.                                       [symbolic + numeric]
- B4 closed form.                                       [symbolic + numeric]
- Fpp = dFp/dc identity.                                [algebraic]

## Fidelity audit

- The contract's Mtilde differs from the origin's M = q(q^2-1) Mtilde by a
  c-independent positive factor; (LOG) and sign(F') are unchanged.  Fidelity OK.
- The odd secular equation is q tan(alpha_2) + tan(c alpha_2) = 0; the
  product-of-tangents form in the task packet is false (confirmed in the origin
  run and re-derived here).  All subsequent formulas use the corrected form.
- C1: (LOG) and (FP) are not logically equivalent; both are proved separately.
- Quantifiers and constants: no hidden dependence; the closed-box certificates
  cover the required open boxes; the c -> 1/2 boundary is handled by B4/B5 and
  monotonicity, not by CORNER (G2(1/2;q) < 0 for q in (1,2), which is expected).

## Adversarial checks performed

- Counterexample hunting on all obligations (200k random points, 8M Region B
  points, edge cases q -> 1+, c -> 0+, c -> 1/2, u = sqrt(41), q >= 20 tail):
  no violation of any obligation.
- Independent engine bugs found and fixed during the audit (see
  counterexample_log.md): ambient-precision products; Decimal.sqrt rounding-mode
  defect in the producer's riarith (confirmed); Taylor sin/cos dependency
  blow-up (replaced by exact monotone-range); a factorial transcription error in
  the audit's own atan series (caught by the PI containment sanity check); an
  inverted-bisection bug in the audit's first numeric harness.  None of these
  affect the candidate proof; all were audit-side artifacts.

## Caveats (reproducibility notes, not open proof obligations)

1. riarith.iv_sqrt defect (producer's engine): confirmed non-strict.  This audit
   does not rely on riarith for any sign conclusion; the audit engine implements
   a directed sqrt with documented soundness (validated on 3000 random cases).
2. The C4 identity IN = A*K(v): the producer's caveat said it was not
   symbolically zeroed; this audit's fresh symbolic check confirms the identity
   exactly (the residual is atan(tan v) - v = 0 on the domain v in (0, pi/2)).
   The producer's caveat is thus resolved, not load-bearing.
3. Shipped verifier's C4 region constants were stale; the audit uses the
   certificate's own leaf endpoints and certified-PI coverage, so this does not
   affect the conclusion.
4. The interval engines are soundness-documented executables, not formally
   verified in a proof assistant.  The certificates and the audit re-verification
   are fully reproducible (repro_manifest.md).
5. The audit's own interval library (audit_iv.py v3) is new in this run and was
   validated against mpmath at 120 digits on point and interval tests; the
   certificate re-verification uses it.

## Verdict taxonomy

PASS for every obligation; the overall verdict is INDEPENDENTLY_AUDITED_PROOF.
No REPAIRABLE_GAP, FATAL_GAP, WRONG_PROBLEM, CIRCULAR_OR_EQUIVALENT_REDUCTION,
UNVERIFIED_CITATION, or COMPUTATIONAL_ONLY issue was found.  (The computational
steps are rigorous certificates re-verified independently, which is the standard
for this class of proof.)

## Files

- problem_contract.md (normalized contract, this audit)
- status_and_literature.md
- obligation_graph.md
- approach_registry.md
- research_ledger.md
- counterexample_log.md
- candidate_proof.md (independent reconstruction)
- reproducibility/audit_iv.py, audit_functions.py, audit_symbolic.py,
  audit_symbolic2.py, audit_certificates.py, dbg_iv.py, dbg_iv2.py
- reproducibility/output/ (audit_symbolic.txt, audit_symbolic2.txt,
  audit_iv_sanity_v3c.txt, audit_functions_sanity_v3.txt,
  audit_certificates_v3.txt)
