# Problem contract

Run: R-20260806T140000Z-keylemmaaudit-2F83B1
Task: Q-20260806-keylemma-audit-2F83B1 (independent audit of the KEY LEMMA candidate proof)
Audit target: runs/rigorous-open-math-research/R-20260806T070000Z-keylemma2b-0A6D8F
  (candidate_proof.md, problem_contract.md, audit_report.md, repro_manifest.md)
Status of this run: independent re-derivation and re-verification of the target.
This file is the audit's own normalized contract, written from the primary sources
(origin run, parent run, target run, and the primary definitions), NOT copied from
the target run's contract.

## Objects and definitions (normalized independently)

q > 1, c in (0, 1/2).

Secular curves:
  E(a) := arctan(1/(q tan a)) on (0, pi/2), strictly decreasing, E'(a) = -q/Phi(a).
  O(a) := pi - arctan(q tan a) on (0, pi/2), O(pi/2) := pi/2,
          O(a) := arctan(-q tan a) on (pi/2, pi).
  O is strictly decreasing on (0, pi) with O'(a) = -q/Phi(a).
  Phi(a) := cos^2 a + q^2 sin^2 a > 0.
  The odd secular equation in the packet/product-of-tangents form is FALSE; the
  correct form is q tan(alpha_2) + tan(c alpha_2) = 0, equivalent to O(alpha_2) = c alpha_2
  (verified in the origin run Section 2.1 against the transfer-matrix solver and
  re-derived here: tan(O(a)) = -q tan a for a in (pi/2, pi)).

alpha_1(c) in (0, pi/2): unique root of E(a) = c a.
alpha_2(c) in (0, pi):   unique root of O(a) = c a.
Existence/uniqueness: E and O strictly decreasing, line strictly increasing, endpoints
  E(0+) = pi/2, E(pi/2-) = 0; O(0+) = pi, O(pi-) = 0.  Unique intersections.
  c a < pi/2 forces alpha_2 > pi/2 (since O(a) < pi/2 for a > pi/2); hence
  alpha_2 in (pi/2, pi) for all c in (0, 1/2).

  W(a) := 3 + 2 a cot a.
  Mtilde(a;c) := a^2 sin^2 a / (q + c Phi(a)).
  G(a;c) := (d/dc) log Mtilde(a(c);c) along the curve
          = -Phi(a) W(a)/(q + c Phi(a))
            + 2 c a Phi(a) (q^2 - 1) sin a cos a / (q + c Phi(a))^2.
  G_k(c) := G(alpha_k(c); c),  Mtilde_k(c) := Mtilde(alpha_k(c); c).
  H(c) := G_2(c) - G_1(c).
  Ftilde(c) := Mtilde_1(c) - Mtilde_2(c).
  Ftilde'(c) := Mtilde_1 G_1 - Mtilde_2 G_2   (this is dFtilde/dc; exact).
  H'(c) := dG_2/dc - dG_1/dc (total derivatives along the curves).
  Ftilde''(c) := Mtilde_1 J_1 - Mtilde_2 J_2,  J_k := G_k^2 + dG_k/dc.
  Ftilde'' = dFtilde'/dc is exact: with Mtilde' = Mtilde G and dG_k/dc = J_k - G_k^2
  the two G^2 terms cancel.  [verified symbolically]

## Hypotheses

1. q > 1, c in (0, 1/2) for the KEY LEMMA.
2. alpha_1, alpha_2 are the unique intersections defined above.
3. All quantities are real-analytic on (1, inf) x (0, 1/2).

## Target conclusion

KEY LEMMA: for all q > 1, c in (0, 1/2):

  (LOG)  (d/dc) log(Mtilde_1/Mtilde_2) = G_1 - G_2 < 0,   i.e. H = G_2 - G_1 > 0.
  (FP)   Ftilde'(c) = Mtilde_1 G_1 - Mtilde_2 G_2 < 0.

Finding C1 (parent audit, rechecked here): (LOG) and (FP) are NOT logically
equivalent; each is proved separately.  (FP) is the form consumed by T4 in the
origin report.  Semantic fidelity: the origin's M(a;c) = q(q^2-1) a^2 sin^2 a/(q + c Phi(a))
differs from Mtilde by the c-independent positive factor q(q^2-1), so
(d/dc) log(M_1/M_2) and sign(F') are identical for M and Mtilde; the contract is
faithful to the origin.

## Obligations audited (per the task packet)

  L1    G_1 < 0 for all q > 1, c in (0, 1/2).                      [base, parent]
  L2    if G_2 >= 0 then both (LOG) and (FP) hold.                 [base, parent]
  R1    G_2 >= 0 for all q >= 2, c in (0, 1/2).                    [target run]
  R2    G_2 >= 0 for all q > 1, c in (0, 0.4].                     [target run]
  L4box H' < 0 on (1,2] x [0.4, 0.5].                              [target run, certificate]
  L5box Ftilde'' > 0 on (1,2] x [0.4, 0.5].                        [target run, certificate]
  B4    Ftilde'(q, 1/2) < 0 for all q > 1.                         [base, parent]
  B5    H(q, 1/2) = 2 pi q (q+1)/(2q+1)^(3/2) > 0.                 [base, parent]
  M2    dIN/du < 0 on D := {(q,u) : q > 1, 0 < u < sqrt(2q+1)}.    [target run]
  CORNER G_2(1/2; q) >= 0 for q >= 2.                              [target run]
  C4    G_2(0.4; q) >= 0 for all q >= 1.                           [target run]

Certificates to re-verify with an independent engine:
  cert_dM2dq_boxes.json          (84 leaves, [1,20] x [0, y1], y1 = 40-digit sqrt(41) truncation)
  cert_dM2dq_strip_boxes.json    (10 leaves, [1,20] x [y1, y1 + 1e-30])
  cert_c4_boxes.json             (200 leaves, K > 0 on the interval leg)
  cert_L4box_boxes.json          (128 leaves, H' < 0 on [1,2] x [0.4,0.5])
  cert_L5box_boxes.json          (128 leaves, Ftilde'' > 0 on [1,2] x [0.4,0.5])

## Quantifiers and dependency of constants

All constants are absolute.  Endpoints are handled by closed-box certificates
(supersets of the required open boxes) and exact one-sided/endpoint values
(CORNER, B4, B5 are exact closed forms).

## Completion criteria for the audit

1. Every identity (E1-E9 in the target) re-derived or independently checked.
2. Every base lemma (B4, B5) verified against the primary definitions.
3. The reduction R1 ^ R2 ^ L4box ^ L5box ^ L1 ^ L2 ^ B4 ^ B5 => KEY LEMMA verified.
4. Every certificate re-verified with a sound independent interval engine,
   including tiling/coverage and sign conditions.
5. Per-obligation verdict and overall status label per the upstream protocol.

## Results that do not count as completion

- Numerical verification alone (reported as evidence).
- Interval arithmetic without a documented outward-rounding soundness model.
- Proving only one of (LOG)/(FP).
- Trusting the target run's own audit report.

## Boundary and degenerate cases

- q -> 1+ and q -> +inf are covered by the analytic lemmas (B4/B5 exact forms at
  c = 1/2, R1/R2 + M2/CORNER/C4, tail bounds).
- c -> 0+ : (LOG)/(FP) hold by L1/L2 since G_2(0+) = 2 pi^2 q^3 / POS > 0 (R2 side);
  also IN(q,0+) = 2 pi^2 q^3 > 0.
- c = 1/2 is not part of the KEY LEMMA domain; Region B uses one-sided limits:
  H(c) > H(1/2) and Ftilde'(c) < Ftilde'(1/2) for c < 1/2 via monotonicity on the
  closed box certificates.
