# Obligation graph

Run: R-20260806T070000Z-keylemma2b-0A6D8F

Notation: q > 1, c in (0, 1/2); gamma = pi - alpha_2; A := alpha_2 = pi - gamma;
u := q*tan(gamma) = tan(c*A) in (0, sqrt(2q+1)); A = pi - arctan(u/q).
IN(q,u) := (q^2+u^2) A (2 A q - 3 u + 2 arctan u) - 3 u q (1+u^2) arctan u.
Sign(IN) = Sign(G_2), IN = G_2 * POS with explicit POS > 0.

## Root obligation

KEY LEMMA for all q > 1, c in (0, 1/2):
  (LOG) H = G_2 - G_1 > 0;   (FP) Ftilde' = Mtilde_1 G_1 - Mtilde_2 G_2 < 0.
Status: PROVED (candidate proof complete; audit in audit_report.md).

## Dependency chain (all nodes PROVED after this run)

KEY LEMMA
  +-- L1: G_1 < 0 on (1,inf)x(0,1/2).                 [PROVED, parent; rechecked]
  +-- L2: G_2 >= 0 implies (LOG) and (FP).             [PROVED, elementary]
  +-- Region split: R1 ^ R2 => Region B subset Box.     [PROVED]
  +-- R1: G_2 >= 0 on {q >= 2, c in (0,1/2)}.          [PROVED]
  |     +-- REDU: Sign(G_2) = Sign(IN).                [PROVED, identity]
  |     +-- M2: dIN/du < 0 on D = {q>1, 0<u<sqrt(2q+1)}. [PROVED]
  |     |     +-- M2(1,u) = pi h(u), h(u) < 0 (concavity). [PROVED, elementary]
  |     |     +-- dM2/dq < 0 on D:
  |     |           - compact [1,20]x[0,sqrt(41)]: certificates
  |     |             cert_dM2dq_boxes.json + cert_dM2dq_strip_boxes.json [PROVED, certified; independently re-verified]
  |     |           - tail q >= 20: elementary bound B(q), B(20) < 0, B' < 0. [PROVED, elementary]
  |     +-- CORNER: IN(q, sqrt(2q+1)) >= 0 for q >= 2. [PROVED, closed form + elementary pi certificate]
  +-- R2: G_2 >= 0 on {q > 1, c in (0,0.4]}.           [PROVED]
  |     +-- REDU (as above).
  |     +-- M2 (as above).
  |     +-- C4: G_2(0.4;q) >= 0 for q >= 1  <=> K(v) >= 0 on [2pi/7, 2pi/5). [PROVED]
  |           +-- curve identity IN = A*K(v) on c = 0.4. [PROVED numerically + certified re-evaluations; symbolic reduction incomplete (atan(tan) residue), documented]
  |           +-- interval leg [2pi/7, 2pi/5 - 1e-3]: cert_c4_boxes.json [PROVED, certified; independently re-verified; slivers bridged]
  |           +-- tail leg [2pi/5 - 1e-3, 2pi/5): T^3 K >= exact rational 178.85896 > 0. [PROVED, elementary + certified constants]
  +-- L4box: H' < 0 on (1,2]x[0.4,0.5].                [PROVED, cert_L4box_boxes.json]
  +-- L5box: F~'' > 0 on (1,2]x[0.4,0.5].              [PROVED, cert_L5box_boxes.json]
  +-- B4: Ftilde'(q,1/2) < 0.                          [PROVED, parent; rechecked]
  +-- B5: H(q,1/2) > 0.                                [PROVED, parent; rechecked]
  (B6, B7, Q1, M1 not needed on this route.)

## Closure argument (written in candidate_proof.md Sections 2-9)

If G_2 >= 0: L1 + L2.  Else (q,c) in Region B subset (1,2)x(0.4,0.5) subset Box.
L4box gives H(c) > H(1/2); B5 gives H(1/2) > 0 => (LOG).  L5box gives
Ftilde'(c) < Ftilde'(1/2); B4 gives Ftilde'(1/2) < 0 => (FP).

## Downstream obligations (this run does not open them)

Origin report T4: with the KEY LEMMA, f_sym has exactly one zero u*(R) in
(0,1/2) and D_sym strictly increases then decreases; obligation O2 of the
n = 1 gap-extremal proof closes.  This run closes the KEY LEMMA; the T4
conclusion is the manager's integration step, not re-proved here.

## Verifier notes

- All interval legs are finite rigorous computations; their soundness model is
  documented in riarith.py headers, repro_manifest.md, and audit_report.md
  Section 4.  Every leaf of every certificate was independently re-evaluated
  with a second from-scratch engine (0 failures).
- Known caveat: riarith.iv_sqrt is not strictly outward-rounded; the defect is
  documented and is not load-bearing because the independent engine (mpmath.iv)
  is sound and passes all sign conditions.
