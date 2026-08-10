# Obligation graph

Run: R-20260806T050000Z-keylemma2-5A35E5

Notation: q > 1, c in (0,1/2);  gamma = pi - alpha2;  A := alpha2 = pi - gamma;
u := q*tan(gamma) = tan(c*A) in (0, sqrt(2q+1));  A = pi - arctan(u/q).
IN(q,u) := (q^2+u^2) A (2 A q - 3 u + 2 arctan u) - 3 u q (1+u^2) arctan u.
Sign(IN) = Sign(G2), IN = G2 * (positive factor).
M1 := dIN/dq,  M2 := dIN/du (exact formulas in the ledger).

## Root obligations (from the parent run, rechecked in this run)

- R1: G2 >= 0 for q >= 2, c in (0,1/2).        slack 0.069181 at (2,1/2).
- R2: G2 >= 0 for q > 1, c in (0,0.4].         slack 0.413609 at (1,0.4) (exact q=1 value;
      the parent's 0.415004 was a grid min at q slightly > 1).
- L4box: H' = dG2/dc - dG1/dc < 0 on (1,2] x [0.4,0.5].  slack 7.7317 at (1.05,0.5).
- L5box: F~'' = M~1 J1 - M~2 J2 > 0 on (1,2] x [0.4,0.5].  slack 14.167 at (2,0.5).

Integration (parent, audited):  R1 ^ R2 ^ L4box ^ L5box ^ B1-B5 ^ B7  =>  (LOG) ^ (FP)
=>  T1-T4 close O2.

## New reduction (this run): R1, R2 collapse via (q,u) coordinates

ID: REDU
Statement: G2 >= 0 on region R <=> IN >= 0 on the corresponding (q,u) region.
Status: PROVED (identity, machine-verified at 40+ digits; 200 random points, 0 sign
mismatches; the positive multiplier is explicit).
Depends on: definitions, secular equation (checked against the parent run).

ID: M1
Statement: dIN/dq > 0 for all q > 1, 0 < u < sqrt(2q+1).
Status: PARTIAL -- analytic proof nearly complete:
  Case A (4 A q >= u + 3 u^3): M1 >= T1 + T2 > 0 (elementary).
  Case B: M1 >= BndB := 6A^2 q^2 + 2A q u + u^2(2A^2-4) - 3 u^4, and
    BndB >= B(q) := BndB(q, sqrt(2q+1)) with A = A_m(q) = pi - arctan(sqrt(2q+1)/q),
    via g(u) >= min(0, g(sqrt(2q+1))) (proven: g' > 0 on [0,u0], concave on [u0,umax]).
  B(q) > 0: elementary for q >= 4 (A >= pi/2); min over (1,4] is 21.8 at q ~ 1.018
  (numeric); the compact remainder (1,4] is certifiable by interval arithmetic.
Status of the claim: numerically min(M1) = 27.02 at (q->1+, c->1/2-).
Evidence: exact formula verified at 1e-13; fine grids.

ID: M2
Statement: dIN/du < 0 for all q > 1, 0 < u < sqrt(2q+1).
Status: NUMERICAL (4760 samples, 0 positive; min -5.96 at (q->1+, u~0.52)).  Analytic
proof open.  OPTIONAL: not required if the boundary curves are handled directly.
Evidence: exact formula verified at 1e-13.

ID: B6u
Statement: IN(2,u) >= 0 for u in (0, sqrt(5))  [<=> G2(c;2) >= 0, B6].
Status: NUMERICAL (min 6.6727 at u = sqrt(5)).  Proof open.

ID: CORNER
Statement: IN(q, sqrt(2q+1)) >= 0 for q >= 2  [<=> G2(1/2;q) >= 0].
Status: NUMERICAL (min 6.6727 at q=2; G2(1/2;q) increasing on [2,1e6], min 0.06918).
Closed form available: G2(1/2;q) = 2q(-q x + pi q - x - 3 sqrt(2q+1) + pi)/(2q+1)^{3/2},
x = 2 asin(1/sqrt(2(q+1))); verified at 1e-33.  Proof open.

ID: B7u
Statement: IN(1,u) >= 0 for u in (0, tan(2 pi/7))  [<=> G2(c;1) >= 0, parent B7].
Status: PROVED by the parent run (B7); this run rechecks it as a premise.
Numerical: min 5.8680 at u = tan(2 pi/7) (the corner (1,0.4)).

ID: C4c
Statement: IN >= 0 on the c = 0.4 curve, q in [1, inf)  [<=> G2(0.4;q) >= 0].
Status: NUMERICAL (min 5.8709 at q -> 1+; G2(0.4;q) min 0.4136 at q=1).  Proof open.

## Routes to the four obligations

R1  <=  REDU ^ M1 ^ (B6u or point IN(2,sqrt5)) ^ CORNER
      (with M2: u <= sqrt5 case uses point IN(2,sqrt5); without M2: full curve B6u)
R2  <=  REDU ^ M1 ^ (B7u) ^ (C4c or compact-box certificate on (1,4.25)x(0,tan(0.4 pi)))
L4box <=  certified interval on [1,2]x[0.4,0.5] (closure) or analytic estimates
L5box <=  certified interval on [1,2]x[0.4,0.5] (closure) or analytic estimates
Q1 (dG2/dq >= 0)  is NOT needed on this route; retained as a fallback route.

## Base lemmas (parent, rechecked)

B1-B3 (q=1 family), B4 (F~'(q,1/2) < 0, exact closed form), B5 (H(q,1/2) =
2 pi q (q+1)/(2q+1)^{3/2} > 0), B7 (G2(c;1) > 0 for c <= 0.4).
All are premises from the parent run; this run re-verifies the numerically checkable
ones and relies on the parent's audited proofs (cited as DERIVED from that run).

## Verifier notes

- M1's Case A/B split must be exhaustive: Case A = {4Aq >= u+3u^3}, Case B complement.
- BndB >= B(q) uses A >= A_m(q) with all A-appearances in positive coefficients; the
  u^2(2A^2-4) coefficient is positive (A > pi/2).  Verified numerically.
- g(u) endpoint-min argument: g' = 2A_m q + 2(2A_m^2-4)u - 12u^3 > 0 on [0,u0], and g
  concave on [u0, umax]; both verified numerically; needs a written proof.
- B(q) > 0 on (1,4]: numeric min 21.8; the interval certificate must cover it.
