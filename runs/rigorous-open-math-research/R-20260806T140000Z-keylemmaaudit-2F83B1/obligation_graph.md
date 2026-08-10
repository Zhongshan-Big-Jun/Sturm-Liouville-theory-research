# Obligation graph

Run: R-20260806T140000Z-keylemmaaudit-2F83B1 (independent audit)

Each node: ID / statement / depends on / status (audit verdict) / verifier notes.
Status values are the audit verdicts, not the target run's labels.

## Root

ID: KEY
Statement: for all q > 1, c in (0, 1/2): (LOG) G1 - G2 < 0 and (FP) Ftilde' < 0.
Depends on: L1, L2, R1, R2, L4box, L5box, B4, B5
Status: PROVED (independent audit)

## Reduction

ID: RED
Statement: if G2 >= 0 then L1+L2 give both forms; if G2 < 0 then (q,c) in
  Region B := (1,2) x (0.4, 0.5), and L4box+B5 give (LOG), L5box+B4 give (FP).
Depends on: L1, L2, R1, R2, L4box, L5box, B4, B5
Status: PROVED.  Verifier notes: Region B = {(q,c): G2<0} subset (1,2)x(0.4,0.5)
  follows from R1 (excludes q >= 2) and R2 (excludes c <= 0.4); c < 1/2 by the
  KEY LEMMA domain.  Monotonicity on the closed box [1,2]x[0.4,0.5] (certified
  superset of the open box) gives H(c) > H(1/2) and Ftilde'(c) < Ftilde'(1/2)
  for c < 1/2.

## Base lemmas

ID: L1
Statement: G1 < 0 for all q > 1, c in (0, 1/2).
Depends on: none (elementary estimate)
Status: PROVED.  Verifier notes: W1 > 0 (alpha1 in (0, pi/2)); cross term
  bounded by 2 c a1 Phi1^2 cot a1/(q + c Phi1)^2 < 2 a1 cot a1 < W1 (q + c Phi1)/
  (q + c Phi1)... re-derived: multiplying G1 < 0 by (q + c Phi1)^2/Phi1 reduces to
  W1(q + c Phi1) > 2 c a1 (q^2-1) sin a1 cos a1; RHS <= 2 c a1 Phi1 cot a1
  < 2 a1 cot a1 (q + c Phi1) < W1 (q + c Phi1).  Numerically re-checked on grids.

ID: L2
Statement: if G2 >= 0 then (LOG) and (FP) both hold.
Depends on: L1
Status: PROVED.  H = G2 - G1 > 0; Ftilde' = M1 G1 - M2 G2 < 0 since M1 G1 < 0
  and -M2 G2 <= 0.

ID: B4
Statement: Ftilde'(q, 1/2) < 0 for all q > 1.
Depends on: closed form at c = 1/2
Status: PROVED.  Verifier notes: independently derived the closed form
  Ftilde'(q,1/2) = 2 pi (cos x - 1)^3 P(x)/sin^3 x with x = 2 arcsin(1/sqrt(2(q+1)))
  (symbolic diff = 0 with q = cos x/(1 - cos x)); P(x) - (pi - 3x)^2 =
  3(x - sin x)(pi - 2x) > 0 for x in (0, pi/3); (cos x - 1)^3 < 0, sin^3 x > 0.
  Numeric: matches direct evaluation to 1e-45 for q in [1+1e-7, 1e4].

ID: B5
Statement: H(q, 1/2) = 2 pi q (q+1)/(2q+1)^(3/2) > 0.
Depends on: closed form at c = 1/2
Status: PROVED.  Verifier notes: symbolic diff = 0; numeric to 1e-45; the min is
  2 pi/3^(3/2) = 2.4184 at q = 1+.

## Target-run obligations

ID: R1
Statement: G2 >= 0 for all q >= 2, c in (0, 1/2).
Depends on: M2, CORNER, sign identity IN = G2*POS
Status: PROVED (audit).  Verifier notes: u = q tan(gamma) strictly increasing in c
  with u(1/2) = sqrt(2q+1); IN strictly decreasing in u on (0, sqrt(2q+1)) (M2);
  IN(q,u) > IN(q, sqrt(2q+1)) = G2(1/2;q)*POS >= 0 (CORNER).

ID: R2
Statement: G2 >= 0 for all q > 1, c in (0, 0.4].
Depends on: M2, C4, sign identity
Status: PROVED (audit).  Verifier notes: u in (0, u_c(q)] with u_c(q) < sqrt(2q+1);
  IN(q,u) >= IN(q, u_c(q)) = G2(0.4;q)*POS >= 0 (C4).  IN(q,0+) = 2 pi^2 q^3 > 0.

ID: M2
Statement: dIN/du < 0 on D = {(q,u): q > 1, 0 < u < sqrt(2q+1)}.
Depends on: h(u) < 0; dM2/dq < 0 (certificates + tail bound)
Status: PROVED (audit).  Verifier notes: M2(1,u) = pi h(u) < 0 (elementary h proof
  re-audited: h'' < 0, h'(1/2) > 0, h'(0.53) < 0 with explicit rational bounds,
  max < 13(0.53)^2 - 5 < 0); dM2/dq < 0 on [1,20]x[0,sqrt(41)] by certificates and
  on q >= 20 by the B(q) tail bound (all bounding arithmetic re-derived and
  numerically checked); for u <= sqrt(41) integrate along q' in [1,q] (path leaves
  D for small q' but the certificate covers the whole box); for u > sqrt(41) use
  the t = u/q rescaling with the explicit bound (checked numerically, margin ~7).

ID: CORNER
Statement: G2(1/2;q) >= 0 for q >= 2.
Depends on: exact closed form
Status: PROVED (audit).  Verifier notes: G2(1/2;q) = 2q(q+1)(pi - x - 3 sin x)/
  (2q+1)^(3/2); min over q >= 2 at x = arccos(2/3) (q = 2), value
  12(pi - arccos(2/3) - sqrt(5))/(5 sqrt(5)) = 0.0691814447546... > 0; the
  elementary certificate pi > arccos(2/3) + sqrt(5) re-audited (all bounds sound:
  y = pi - sqrt(5) in (0.9,1), alternating Taylor upper bound cos(y) < 0.6224 < 2/3).

ID: C4
Statement: G2(0.4;q) >= 0 for all q >= 1.
Depends on: identity IN = A*K(v); interval certificate; tail elementary bound
Status: PROVED (audit).  Verifier notes: v = arctan(u) in [2pi/7, 2pi/5) maps
  q from 1 to +inf monotonically; K > 0 on [2pi/7, 2pi/5 - 1e-3] by the
  certificate (re-verified, worst lower bound 2.49716 with my engine); tail
  [2pi/5 - 1e-3, 2pi/5) by the exact rational bound T^3K >= 178.85896 > 0 with
  the four constants (v >= 1.25, u >= 3.06, u <= 3.08, T <= 2.50002e-3) verified
  with my engine.

ID: L4box
Statement: H' < 0 on (1,2] x [0.4, 0.5].
Depends on: certificate cert_L4box_boxes.json
Status: PROVED (audit).  Verifier notes: 128 leaves tile [1,2]x[0.4,0.5] exactly
  (exact Fraction area = 1/10, no overlaps); every leaf re-evaluated with the
  audit engine (sound outward-rounded Decimal interval arithmetic with exact
  monotone-range sin/cos): sign condition H' < 0 holds with worst upper bound
  -4.8416038 < 0; 0 sign/overlap/point failures.

ID: L5box
Statement: Ftilde'' > 0 on (1,2] x [0.4, 0.5].
Depends on: certificate cert_L5box_boxes.json
Status: PROVED (audit).  Verifier notes: 128 leaves tile exactly; every leaf
  re-evaluated: worst lower bound +8.3793828 > 0; 0 failures.

## Certificates (computational sub-obligations)

ID: CERT_DM2DQ_MAIN  [1,20]x[0,y1] dM2/dq < 0, 84 leaves.
  Status: PROVED.  Exact Fraction tiling (area = target exactly); worst upper
  -0.1902428 < 0; 0 failures.  y1 is the printed 40-digit lower truncation of
  sqrt(41).

ID: CERT_DM2DQ_STRIP  [1,20]x[y1, y1+1e-30] dM2/dq < 0, 10 leaves.
  Status: PROVED.  Exact tiling; worst upper -448.7453; 0 failures;
  (y1 + 1e-30)^2 = 41.000...0000128 > 41 exact, so sqrt(41) < y1 + 1e-30 and the
  union covers [1,20]x[0, sqrt(41)].

ID: CERT_C4  K > 0 on the interval leg, 200 leaves.
  Status: PROVED.  Leaves inside [first,last]; internal gaps (slivers) total
  6.25e-58, max 1e-59, bridged by eps = 1e-58 inflated re-evaluation (max gap <
  2 eps); coverage [2pi/7, 2pi/5-1e-3] subset [first,last] verified with the
  certified Machin-pi interval; worst lower bound 2.49716 > 0; 0 failures.

ID: CERT_L4 / CERT_L5  see L4box/L5box.

## Meta notes

- No circular dependence found.  M2 uses the certificates; CORNER/C4 are
  elementary; R1/R2 combine them; the KEY LEMMA is closed by the reduction.
- Every premise's source was read and re-derived in this run (origin, parent,
  target).  No citation-only premises.
- Computation-to-theorem leaps: the finite rigorous computations are the
  certificates; their soundness model is documented (audit_iv.py) and the sign
  conditions were reproduced by the independent engine.
