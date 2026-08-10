# Status and literature

Run: R-20260806T070000Z-keylemma2b-0A6D8F

## Problem status

The KEY LEMMA for all q > 1, c in (0, 1/2):

  (LOG)  (d/dc) log(Mtilde_1/Mtilde_2) = G_1 - G_2 < 0;
  (FP)   Ftilde'(c) = Mtilde_1 G_1 - Mtilde_2 G_2 < 0.

Status after this run: PROVED (candidate proof complete; the four inherited
obligations R1, R2, L4box, L5box are all closed).  The proof combines elementary
one-variable analysis (M2, CORNER, C4) with certified outward-rounded interval
arithmetic (L4box, L5box, the compact part of M2, and the interval leg of C4),
independently re-verified with a second from-scratch interval engine.  The
audit verdict is in audit_report.md.

## Provenance of the statement

The KEY LEMMA is a project-derived statement.  It appears in:
- origin run R-20260805T000000Z-gapn1-a1b2c3, agentA_O2_single_crossing.md,
  Section 2.9 (stated as "(d/dc) log(M_1/M_2) < 0" with equivalent forms
  G(alpha_2) > G(alpha_1) and F'(c) < 0; T4 consumes the F' form);
- parent run R-20260806T011500Z-keylemma-E58FB1 (four-lemma reduction to
  R1, R2, L4box, L5box plus bases L1, L2, B4, B5, B7; status RIGOROUS_PARTIAL_RESULT);
- predecessor run R-20260806T050000Z-keylemma2-5A35E5 ((q,u) reformulation,
  M2/CORNER/C4 routes, interval certificates, status not finalized).

The (LOG) and (FP) forms are NOT logically equivalent (parent audit finding C1,
rechecked in this run); each is proved separately.  This is the only known
technical subtlety in the statement layer.

## Exact known theorems used as premises

No external theorem is used as a premise.  The premises are:

- L1: G_1 < 0 for all q > 1, c in (0, 1/2).  [PROVED, parent candidate
  Section 2.1; re-derived and re-verified in this run on grids, 0 violations.]
- L2: if G_2 >= 0 then both (LOG) and (FP) hold.  [PROVED, elementary.]
- B4: Ftilde'(q, 1/2) < 0 for all q > 1.  [PROVED, parent candidate Section 3.1,
  exact closed form with P(x) - (pi - 3x)^2 = 3(x - sin x)(pi - 2x) > 0;
  re-verified numerically in this run, 0 violations.]
- B5: H(q, 1/2) = 2 pi q (q+1)/(2q+1)^(3/2) > 0 for all q > 1.  [PROVED, parent;
  re-verified numerically in this run, 0 violations.]
- B7: G_2(c;1) > 0 for c in (0, 0.4].  [PROVED, parent candidate Section 3.4;
  re-verified numerically in this run, 0 violations.  Not needed on the current
  route, recorded for completeness.]

All of these were rechecked against their exact sources in this run (parent
candidate_proof.md sections 2.1-3.4 and the origin report sections 2.1-2.9).

## Background literature (surveyed, NOT used as premises)

The n = 1 gap-extremal problem belongs to the Sturm-Liouville eigenvalue-ratio
program of this project:
- Keller 1976, The Minimum Ratio of Two Eigenvalues, SIAM J. Appl. Math.
  10.1137/0131042.
- Mahar-Willner 1976, Extremum problems for the differential equation
  y'' + lambda p(x) y = 0, CPAM 29:517-529, 10.1002/cpa.3160290505.
- Ahrami-El Allali-Harrell, arXiv:2407.02459 (fundamental gap).
These do not state the KEY LEMMA and are not premises.  The KEY LEMMA is a
statement local to this project's reduction of the symmetric-barrier family
f_sym(u) (origin report Section 2.9).

## Novelty risk

- Novelty classification: POTENTIALLY_NEW within the project.  No literature
  claim is made.  The statement does not appear in the surveyed SL literature;
  it is a technical monotonicity lemma of the project's own reduction.
- Significance classification: useful lemma (closes obligation O2 of the n = 1
  gap-extremal proof).  It is not claimed to be a major standalone theorem.
- Risks: (a) the same statement may exist under different notation in the
  literature (not checked exhaustively); (b) the certified-computation legs
  depend on the audited interval-arithmetic engines (reproducibility, not
  formal verification).
