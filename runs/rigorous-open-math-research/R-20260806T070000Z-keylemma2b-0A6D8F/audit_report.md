# Audit report

Run: R-20260806T070000Z-keylemma2b-0A6D8F
Task: Q-20260806-keylemma2b-0A6D8F (resume of R-20260806T050000Z-keylemma2-5A35E5)
Audited artifact: candidate_proof.md (this run)
Audited statement: KEY LEMMA, both (LOG) and (FP) forms, for all q > 1,
c in (0, 1/2).

## Verdict

PASS

The proof is complete modulo the documented non-load-bearing caveats in
Section 4.  No open proof obligation of the contract remains.  The status label
per the skill output protocol is CANDIDATE_COMPLETE_PROOF (the interval engines
are audited but not formalized in a proof assistant; the audit was performed by
a single agent with an adversarial pass, not by a second independent entity).

## Audit scope and method

The verifier re-derived every formula from the primary definitions (secular
equations), re-ran every verification script with fresh captures, wrote and ran
a from-scratch semantic audit (audit_semantics_fresh2.py), inspected the two
interval engines line by line, and manually re-derived each analytic bound
(M2 tail B(q), the u > sqrt(41) bound, h(u), CORNER, C4 tail T^3 K, L1, the
total derivative dG/dc, and the monotonicity of alpha_1, alpha_2).

## 1. Semantic fidelity

- The normalized statements of R1, R2, L4box, L5box, the KEY LEMMA, and the
  base lemmas match the predecessor contract and the parent candidate after
  re-derivation.  No quantifier, domain, or endpoint was silently changed.
- The odd secular equation is the corrected form q tan(alpha_2) +
  tan(c alpha_2) = 0 (the packet's product-of-tangents form is false); this is
  consistent with the origin report Section 2.1 and with the transfer-matrix
  verification recorded there.
- The (q,u) reformulation: u = q tan(gamma) = tan(c A), A = pi - arctan(u/q),
  c = arctan(u)/A; the map c -> u is strictly increasing from 0 to sqrt(2q+1)
  on (0, 1/2).  Re-verified (identity + monotonicity) at 50-90 digits.
- Sign identity IN = G_2 * POS with explicit POS > 0: symbolic diff = 0 and
  300 random-point checks.  Semantic match to the contract.
- The corner value G_2(0.4;1) = 0.413608714230935284 and the R2 tight point are
  computed at q = 1 exactly; the parent's "0.415004" was a grid minimum at
  q slightly above 1 and is correctly superseded.
- Finding C1 ((LOG) not equivalent to (FP)) is respected: both forms are proved
  separately, and (FP) is the form consumed by T4 in the origin report.

## 2. Logical structure

- Dependency chain: KEY LEMMA <= L1 ^ L2 ^ R1 ^ R2 ^ L4box ^ L5box ^ B4 ^ B5.
  R1 <= REDU ^ M2 ^ CORNER.  R2 <= REDU ^ M2 ^ C4.  Region B =
  {G_2 < 0} subset (1,2) x (0.4, 0.5) subset Box.  Every node has a written
  proof; no circularity.
- The integration on Region B uses L4box (H strictly decreasing in c) and
  L5box (F~' strictly increasing in c) on the segment [c, 1/2] x {q}, which is
  contained in the certified closed box [1,2] x [0.4, 0.5].  Valid.
- The M2 proof integrates dM2/dq at fixed u over q' in [1, q]: the path stays
  in D because u < sqrt(2q+1) <= sqrt(2q'+1) for q' in [1, q].  Valid.
- The case split u <= sqrt(41) / u > sqrt(41) is exhaustive; the boundary
  u = sqrt(41), q = 20 is covered by the closed certified boxes (the B(q) bound
  needs only u <= sqrt(2q+1), not strict).
- CORNER: q >= 2 iff x <= arccos(2/3); x -> pi - x - 3 sin x strictly
  decreasing, so the minimum over q >= 2 is at q = 2.  Valid.
- C4: K >= 0 on [2pi/7, 2pi/5) splits into the certified interval leg and the
  elementary tail; the split point v = 2pi/5 - 1e-3 is covered by both.  Valid.

## 3. Analysis and probability

- h(u) = 4u(pi - arctan u) - 5 - 9u^2: h'' < 0, h'(1/2) > 0 (elementary
  alternating-series bound), h'(0.53) < 0 (elementary bounds), so the unique
  maximum lies in (0.5, 0.53) and h(u*) = 4u*^2/(1+u*^2) + 9u*^2 - 5
  < 13(0.53)^2 - 5 < 0.  Valid.
- M2 tail bound B(q): each term checked by hand (see research_ledger.md
  entry 6); B(20) < -232 with elementary bounds (pi < 3.142, sqrt(41) < 6.41);
  B'(q) < 0 for q >= 20 via (4 pi^2 + 14)/sqrt(41) < 8.39 < 10 pi.  Valid.
- u > sqrt(41) case: M2/q^2 <= 4 pi^2 t_max - 7(pi - arctan t_max)
  + 2 pi (1 + t_max^2)/42 < 0 with t_max = sqrt(41)/20 < 0.33; the dropped
  terms are non-positive.  Valid (sharp value -7.018).
- CORNER pi certificate: y = pi - sqrt(5) in (0.9, 1); cos(y) <=
  1 - y^2/2 + y^4/24 (alternating Taylor, y^2 < 30) and z -> 1 - z^2/2 + z^4/24
  decreasing on (0, sqrt(6)) gives cos(y) < 0.6223375 < 2/3.  Valid.
- C4 tail: T^3 K >= exact rational 349333915896399959797475605401 /
  1953125000000000000000000000 = 178.85896 > 0 using v >= 5/4, u in (153/50,
  77/25), T <= 125001/50000000; the four constants are certified by outward-
  rounded evaluations (cert_tail_constants.py part D).  Valid.
- The C4 curve identity IN = A*K(v) is verified numerically (300+ points) and
  on the certified re-evaluations; sympy did NOT reduce the symbolic difference
  to 0 (leftover atan(tan(...)) terms).  This is a verification-method caveat,
  not a proof gap: the certificate is a rigorous interval computation of K
  itself, and the analytic tail never uses the symbolic identity.

## 4. Computation (findings, fixes, and the soundness model)

### 4.1 Certificate verification results (reported verbatim)

Shipped verifier (predecessor verify_certificates.py):
- dM2dq: PASS, worst <= -0.19024277945171448312...
- C4: FAIL on tiling only (leaf 199 outside the declared region); 0 sign
  failures in the leaf re-evaluations, worst lower bound 2.42176456...
- L4box: PASS, worst <= -4.65692440779...
- L5box: PASS, worst >= +6.24285527001...

Fixed-constants verifier (C4 region constants corrected to the certificate's
own first/last leaf endpoints): ALL FOUR CERTIFICATES VERIFIED.

Independent from-scratch engine (mpmath.iv 50 dps + own rigorous atan + own
bisection): ALL FOUR CERTIFICATES VERIFIED; worst bounds dM2/dq -0.19024,
C4 2.49716, L4 -4.84160, L5 +8.37938; 0 sign / 0 overlap / 0 point failures.

### 4.2 Finding: stale C4 region constants in the shipped verifier

The shipped verifier declared x0 = 2pi/7 rounded up at 20 digits
(0.89759790102565521097...) and x1 = 2pi/5 - 1e-3 - 4.44e-5, neither of which
is the certificate's actual region.  The certificate's leaves span
[0.897597901025655210989326680937000824056334114107173091707127,
1.25563706143591729538505735331180115367886775975004232838998], which fully
contains [2pi/7, 2pi/5 - 1e-3] (overhang 2.64e-62 left, 2.16e-60 right;
interior slivers total 6.25e-58, max 1e-59, bridged by epsilon-inflated
re-evaluation with eps = 1e-58, worst inflated lower bound 2.42176456 > 0).
Fix applied: the fixed-constants verifier; the C4 certificate is VALID.

### 4.3 Finding: the dM2/dq certificate does not reach sqrt(41)

The region upper bound y1 = 6.403124237432848686488217674621813264520 is a
40-digit truncation of sqrt(41) (4.2e-40 below).  The strip
[1,20] x [y1, sqrt(41)] was not covered by cert_dM2dq_boxes.json.  Fix: new
certificate cert_dM2dq_strip_boxes.json certifies dM2/dq < 0 on
[1,20] x [y1, y1 + 1e-30] (exact squaring: (y1 + 1e-30)^2 = 41.000...0000128
> 41), worst upper bound -448.745..., independently re-verified with the
mpmath.iv engine (verify_dM2dq_strip_indep.py).  The M2 compact part is now
fully covered.

### 4.4 Finding: riarith.iv_sqrt is not strictly outward-rounded

Decimal.sqrt() uses the ambient rounding mode (ROUND_HALF_EVEN), so the lower
bound of iv_sqrt can exceed the true sqrt by about 1e-60 (verified on
sqrt(2): the returned lower bound ...7317668 exceeds the true value
...73176673799...).  This is a defect of the certificate-GENERATION engine and
of the SHIPPED re-verification engine (both use riarith.iv_atan, which calls
iv_sqrt for arguments in (0.5, 1]).

Impact assessment: NOT LOAD-BEARING for the final proof.  Every sign conclusion
was re-derived by the independent engine (mpmath.iv), which is sound and does
not use iv_sqrt, with 0 failures and margins of at least 0.19 (dM2/dq), 2.42
(C4), 4.84 (L4), 6.24 (L5) in absolute value.  The 80-digit point cross-checks
put the exact function values inside the stored enclosures.  For full
certification hygiene, the strip certificate (also produced by riarith) was
additionally re-verified by the sound engine.  The defect is recorded here and
in repro_manifest.md.

### 4.5 Soundness model of the engines

- riarith: outward-rounded Decimal arithmetic (ROUND_FLOOR/ROUND_CEILING) for
  +,-,*,/, pow, sin, cos, atan (Taylor series with explicit remainders), pi
  (Machin).  Defect: iv_sqrt (Section 4.4).  Division never by 0-containing
  intervals.  Secular bracketing (sound_bracket.py): bisection shrinks only on
  sign-definite interval evaluations; the bracket always contains the root.
- Independent engine: mpmath.iv (libmp outward-rounded interval arithmetic);
  own atan with explicit remainder R = x^(2n+3)/(2n+3) on [0,1] and reduction
  atan(x) = pi/2 - atan(1/x) for x > 1 (monotone endpoint evaluation); own
  sign-safe bisection for alpha_1, alpha_2 with monotonicity bracketing
  (alpha_1 decreasing in c and q; alpha_2 decreasing in c, increasing in q;
  re-derived from the implicit equations).  Assessed sound.
- The alpha bracketing over boxes relies on the monotonicity facts, which were
  re-derived analytically in this run (sign of O_q on the branch (pi/2, pi)).
- Tiling: the three 2-D certificates tile their regions exactly at 90-digit
  Decimal arithmetic (total area equals region area); the 1-D C4 certificate
  leaves miss slivers of total measure 6.25e-58 which are bridged by the
  epsilon-inflated re-evaluation.  The dM2/dq compact part now consists of two
  certificates (main box + strip) whose union covers [1,20] x [0, sqrt(41)].

## 5. Algebra, combinatorics, geometry

- The total derivative dG/dc in rigorous.py (and its independent re-derivation
  in verify_certificates_indep.py) was checked term by term: Ga*ap + Gc with
  ap = -a Phi/D matches the chain rule on G = -Phi W/D + 2 c a Phi K sc/D^2.
- F~'' = M~1 J1 - M~2 J2 = dF~'/dc exactly (G^2 terms cancel).  Verified.
- The sign identity POS factor and the C4 factor A = 2.5 v are positive on the
  relevant domains; no sign or orientation error found.
- The (q,u) region maps: R1-region = {q >= 2, 0 < u < sqrt(2q+1)}; R2-region =
  {q > 1, 0 < u <= u_c(q)} with u_c(q) < sqrt(2q+1).  Verified.

## 6. References

- No external theorem is used as a premise.  The premises L1, L2, B4, B5, B7
  are cited to the parent run's candidate_proof.md (sections 2.1-3.4) and were
  re-derived/re-verified in this run (verify_parent_bases.py, 0 violations;
  hand re-derivation of L1 and B4's P(x) identity).
- Definitions and the KEY LEMMA are cited to the origin report
  agentA_O2_single_crossing.md (sections 2.1-2.9); the secular equations, G,
  alpha_k', and the T4 consumption of (FP) were checked against that file.
- Background literature (Keller, Mahar-Willner, Ahrami-El Allali-Harrell) is
  not used as a premise; novelty is classified POTENTIALLY_NEW within the
  project (no literature claim).

## 7. Gap list

- No load-bearing gap remains.
- Caveat A (non-load-bearing): riarith.iv_sqrt rounding defect (Section 4.4);
  the independent engine covers every sign conclusion.
- Caveat B (verification method): the C4 curve identity IN = A*K(v) is
  verified numerically and by certified re-evaluations, not by full symbolic
  reduction; the certificate and tail legs are rigorous interval statements
  that do not depend on the symbolic identity.
- Caveat C (reproducibility): the interval engines are audited but not
  formalized in a proof assistant; this is a reproducibility note, not an open
  proof obligation of the contract.
- Cosmetic: two numeric display slips in the draft proof (arctan(1/2) bound
  display and the h'(0.53) numeric value; the 13.08 vs 13.10 arithmetic in the
  u > sqrt(41) bound) were corrected during the audit.

## 8. Repairs performed during the audit

1. C4 region constants corrected in the verifier (stale constants documented).
2. Strip certificate produced and integrated (Section 4.3).
3. Independent re-verification of the strip with the sound engine.
4. Cosmetic numeric fixes in candidate_proof.md sections 4.2 and 4.5.
5. Fresh from-scratch semantic audit script written and run (0 failures);
   the v1 script's own alpha2-bisection bug was found and fixed (research
   ledger entry 4), and v2 passes.

## 9. Confidence by axis

- Semantic fidelity: HIGH (statements re-derived from primary definitions;
  fresh audit 0 failures).
- Mathematical correctness: HIGH (analytic lemmas fully elementary and checked
  by hand; interval legs certified by two engines).
- Completeness: HIGH (all four inherited obligations closed; closure argument
  verified).
- Novelty: POTENTIALLY_NEW within the project; no literature claim.
- Reproducibility: HIGH (every script re-run with fresh captures in this run;
  exact commands in repro_manifest.md).
