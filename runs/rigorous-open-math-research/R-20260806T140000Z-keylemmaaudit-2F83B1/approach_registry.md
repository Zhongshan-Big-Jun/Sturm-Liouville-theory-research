# Approach registry

Run: R-20260806T140000Z-keylemmaaudit-2F83B1 (independent audit)

Route families used by this audit (single-agent sequential execution of the
explorer / verifier / reviser / counterexample-hunter roles).

## R-AUD-SYM: symbolic re-derivation of every identity
Core mechanism: sympy simplification of the candidate formulas against the
primary definitions.
Target obligation: E1-E9, IN = G2*POS, M2, dM2/dq, CORNER, B4, B5, C4 tail.
Status: PROVED (all identities diff = 0; B4 closed form re-derived cleanly).
Exact gap: none.  Note: the earlier audit_symbolic.py B4 transcription diff was
nonzero; re-derived symbolically in a fresh script (diff = 0) and confirmed
numerically to 1e-45.  The C4 identity IN = A*K(v) leaves atan(tan v) which is
exactly v on the domain (0, pi/2); substitution gives 0.

## R-AUD-INT: sound Decimal interval engine (from scratch)
Core mechanism: directed-rounding Decimal arithmetic (ROUND_FLOOR/ROUND_CEILING
at 80 digits), own Machin-pi, own atan with explicit remainder, own sqrt with
explicit handling of the Python 3.10 Decimal.sqrt rounding-mode bug, exact
monotone-range sin/cos over intervals.
Target obligation: all five certificates.
Status: PROVED.  Engine bugs found and fixed during the audit (see
counterexample_log.md): (a) v1 computed products in the ambient 28-digit
context (unsound); (b) Decimal.sqrt ignores the rounding mode; (c) v3 Taylor
sin/cos over wide intervals had dependency blow-up, replaced by exact
monotone-range evaluation.  After the fixes, all five certificates pass.
Exact gap: none (documented soundness model).

## R-AUD-CERT: certificate re-verification harness
Core mechanism: exact Fraction tiling + interval sign conditions + stored
enclosure overlap + high-precision point cross-checks + certified-PI coverage +
sliver bridge.
Target obligation: cert_dM2dq_boxes, cert_dM2dq_strip, cert_c4_boxes,
cert_L4box_boxes, cert_L5box_boxes.
Status: PROVED (all five; see output/audit_certificates_v3.txt).
Exact gap: none.

## R-AUD-AN: elementary analysis of the analytic lemmas
Core mechanism: hand re-derivation of the h(u) proof, the B(q) tail bound, the
u > sqrt(41) rescaling bound, the CORNER elementary certificate, L1, B4/B5 sign
analysis, and the alpha_1/alpha_2 monotonicity facts.
Target obligation: M2, CORNER, C4 tail, L1, B4, B5, box bracketing premises.
Status: PROVED (all bounding arithmetic re-derived and numerically cross-checked).
Exact gap: none.

## R-AUD-NUM: independent numerical evidence grids
Core mechanism: float64 vectorized evaluation of (LOG), (FP), G1, G2, IN, M2,
dM2/dq, H, Ftilde' on 200k random points and dense Region B grids.
Target obligation: whole KEY LEMMA (evidence only).
Status: EVIDENCE (no violations on the sampled domains; min H = 2.4185 on
Region B, max Fp < 0).  Not load-bearing; the proof is the analytic/certificate
chain.

## R-CTR: counterexample hunting
Core mechanism: adversarial search of edge cases (q -> 1+, c -> 0+, c -> 1/2,
Region B corners, u = sqrt(41) boundary, tail q >= 20).
Status: no counterexample found to any obligation.  Two genuine defects found in
the AUDIT's own tools (not in the candidate proof): the interval-engine bugs
listed above, and an inverted bisection in the first numeric harness (fixed).
