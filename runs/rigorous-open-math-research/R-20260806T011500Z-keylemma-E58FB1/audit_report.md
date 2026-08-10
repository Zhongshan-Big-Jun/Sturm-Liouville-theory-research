# Audit report

Run: R-20260806T011500Z-keylemma-E58FB1
Auditor: adversarial verifier pass, fresh context, single-agent fallback (skill Phase 8).
Audited artifact: candidate_proof.md against problem_contract.md and the task packet.

## Verdict

REPAIRABLE_GAP

The reduction is sound and all stated analytic lemmas check out; the proof is incomplete
only because four explicit, local, numerically-verified obligations (R1, R2, L4box, L5box)
are not yet proved.  No structural, semantic, or computational-to-theorem error was found
in the claimed parts.  The gaps are each concrete inequalities with quantified margins;
none is equivalent in strength to the original KEY LEMMA in an obvious way (each is
strictly narrower), so the label "reduced, not closed" is appropriate.

## 1. Semantic fidelity

- The target matches the contract: (LOG) G1 - G2 < 0 and (FP) F~' = M~1G1 - M~2G2 < 0
  for all q > 1, c in (0, 1/2).  Quantifiers and definitions agree with the source
  (agentA_O2_single_crossing.md, Sections 2.3, 2.4, 2.9) modulo finding C1.
- Finding C1 re-checked: the source's "equivalently F'(c) < 0" is not a logical
  equivalence (F' = M1G1 - M2G2 is not proportional to G1 - G2).  The run proves both
  forms separately; T4 only consumes (FP).  No silent weakening: (LOG) is kept as the
  packet-form statement and (FP) is proved as the operative form.  ACCEPTED.
- Boundary cases: c -> 0+ (F(0+) > 0, H -> +inf, F~' -> -3 pi^2/4), c -> 1/2- (B4, B5
  exact), q -> 1+ (B1-B3, B7), q -> inf (corner asymptotics recorded).  ACCEPTED.

## 2. Logical structure (the reduction)

Audited chain:

  C1 ^ C2  <=  [Region A: L1 ^ L2]  +  [Region B: L4box ^ L5box ^ R1 ^ R2 ^ B4 ^ B5].

- L1 (G1 < 0): algebra re-checked.  Key inequality (q^2-1) sin a1 cos a1 <= Phi1 cot a1
  reduces to 0 <= cos^2 + sin^2; the cross-term bound uses c Phi1 < q + c Phi1 and
  W1 > 2 a1 cot a1.  All factors positive where used.  PASS.
- L2 (G2 >= 0 implies both forms): M~1 G1 < 0, -M~2 G2 <= 0; H = G2 - G1 > 0.  PASS.
- Region B containment: R1 (q >= 2) and R2 (c <= 0.4) give G2 < 0 => (1 < q < 2) ^
  (0.4 < c < 1/2).  PASS (assuming R1, R2).
- L4box => H(c) > H(1/2): H strictly decreasing on the box, c < 1/2, interval
  [c, 1/2] inside the box.  B5 gives H(1/2) > 0.  PASS.
- L5box => F~'(c) < F~'(1/2): F~' strictly increasing on the box (F~'' > 0), c < 1/2.
  B4 gives F~'(1/2) < 0.  PASS.
- No circularity: R1, R2, L4box, L5box are statements about G2, H', F~'' only; they do
  not use C1/C2.  The bases use only q=1 / c=1/2 elementary identities.  PASS.
- The identity layer E1-E9 (P1-P10, debug_Fpp, verify_Fp12) is machine-verified at
  50-60 digits and independent of the target sign claims.  PASS.

## 3. Base lemmas (hand re-derivation)

- B4: closed form F~'(q,1/2) = 2 pi (cos x - 1)^3 P(x)/sin^3 x with q = cos x/(1-cos x).
  Reproduced symbolically (corner_Fp12b.py).  P - (pi-3x)^2 = 3(x - sin x)(pi - 2x) > 0
  on (0, pi/2); q > 1 gives x in (0, pi/3).  Signs: (cos x - 1)^3 < 0.  PASS.
- B5: H(q,1/2) = 2 pi q(q+1)/(2q+1)^(3/2); derivative of log = (q^2+q+1)/(q(q+1)(2q+1))
  > 0; min 4 pi/(3 sqrt 3) at q = 1.  PASS.
- B1: N1 >= 12 - 2 pi^2/3 > 0 via W >= 3 and uW' >= -2 u^2 csc^2 u >= -2(pi/2)^2(4/3).
  Check: csc^2 max on (pi/3, pi/2) is 4/3 (csc decreasing on (0, pi/2)); u <= pi/2.
  12 - 2 pi^2/3 = 12 - 6.5797 = 5.42 > 0.  PASS.
- B2: N2 = (W-1)(W+3) - 2 w^2 csc^2 w on [2 pi/3, 5 pi/7]; W decreasing from
  3 - 4 pi/(3 sqrt 3) = 0.5816 to 3 - (10 pi/7) cot(2 pi/7) = -0.5677, both in (-1, 1);
  (W-1)(W+3) < 0.  PASS.
- B3: T' sign.  T' sin^3/4 = cos u sin^2 u + u^2 cos u - 2 u sin u.  On (pi/2, pi):
  < 0 termwise.  On (0, pi/2): divide by cos > 0: sin^2 u + u^2 - 2 u tan u <= 0, since
  2 u tan u >= 2 u^2 >= u^2 + sin^2 u (strict for u > 0).  PASS.
- B7: W(pi/(1+c)) <= W(5 pi/7) < 0 for c <= 0.4.  W(5 pi/7) < 0 iff cot(2 pi/7) >
  21/(10 pi).  Elementary certificate: tan(pi/28) < (pi/28)/(1-(pi/28)^2) < 0.1137 < 1/8 (standard bound tan x < x/(1-x^2) on (0,1)), so
  tan(2 pi/7) = tan(pi/4 + pi/28) < (1 + 1/8)/(1 - 1/8) = 9/7, hence
  cot(2 pi/7) > 7/9 = 0.7778 > 21/(10 pi) = 0.6685.  PASS (the sketch in the candidate
  is sound; the audit fills in the elementary bound).
- B6 (auxiliary): verified numerically only, correctly labeled OPEN.  PASS as labeling.

## 4. Computation audit

- The margin tables (candidate_proof Section 5) come from deterministic bisection on
  strictly monotone equations at 30-60 digit precision.  No random sampling, no seeds.
- check_Fpp.py's second-difference column is unreliable and was discarded in favor of the
  first-difference identity check (debug_Fpp.py); the run documents this.  ACCEPTED.
- The numeric claims are correctly labeled "evidence, not proofs" everywhere.  No
  finite-test-to-theorem leap is made in the candidate proof: R1, R2, L4box, L5box are
  explicitly marked PENDING / OPEN with exact statements.  ACCEPTED.

## 5. Exact gap list (smallest failing claims)

G1. R1: prove G2 >= 0 for all q >= 2, c in (0, 1/2).  Local, 2-variable, slack >= 0.069
     (min at (2, 1/2)).  Believed route: Q1 (dG2/dq >= 0) + B6, or gamma-parametrized
     B >= 0 with the exact c = 1/2 balance.
G2. R2: prove G2 >= 0 for all q > 1, c in (0, 0.4].  Slack >= 0.415 (min at (1+, 0.4)).
     Believed route: Q1 + B7 (B7 proved).
G3. L4box: prove H' < 0 on (1, 2] x [0.4, 0.5].  Slack 7.7.
G4. L5box: prove F~'' > 0 on (1, 2] x [0.4, 0.5].  Slack 14.2.

Each gap is locally repairable (a single analytic inequality).  None of the gaps is
masked or hidden; none requires a result comparable to the whole KEY LEMMA.

## 6. Remaining risk / observations

- R1 is the delicate one: the slack 0.069 at (2, 1/2) means generic bounds fail; the
  exact corner value G2(1/2; 2) = 0.0691814... must be part of any proof.
- L4box/L5box margins are large; a sound interval-arithmetic certificate (with a
  hand-verified outward-rounding model) would close G3/G4, and compact parts of G1/G2,
  but mpmath.iv soundness was not relied upon in this run.
- Novelty is unaffected by the audit: the statement is project-derived; the reduction
  structure is this run's contribution.

## 7. Verdict summary

- Semantic fidelity: PASS (modulo C1, which is documented and handled).
- Mathematical correctness of claimed parts: PASS.
- Completeness: FAIL (four open lemmas; exact list above).
- Novelty: POTENTIALLY_NEW (not asserted as resolved).
- Reproducibility: PASS (commands and hashes in repro_manifest.md).
- Final: REPAIRABLE_GAP.  Status label: RIGOROUS_PARTIAL_RESULT.
