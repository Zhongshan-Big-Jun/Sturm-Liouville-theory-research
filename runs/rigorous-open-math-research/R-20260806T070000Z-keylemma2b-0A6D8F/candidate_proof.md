# Candidate proof

Run: R-20260806T070000Z-keylemma2b-0A6D8F
Task: Q-20260806-keylemma2b-0A6D8F (resume of R-20260806T050000Z-keylemma2-5A35E5)
Status: CANDIDATE_COMPLETE_PROOF
Statement: KEY LEMMA (both (LOG) and (FP) forms) for all q > 1, c in (0, 1/2).

This run closes the four obligations inherited from the parent run
(R-20260806T011500Z-keylemma-E58FB1): R1, R2, L4box, L5box.  The four obligations
are reduced (ledger entries 3-5 of the interrupted run, re-derived and machine-
verified in this run) to one two-variable monotonicity lemma (M2), two one-variable
boundary lemmas (CORNER, C4), and two compact-box sign lemmas (L4box, L5box).
M2, CORNER and C4 are proved by elementary analysis; L4box and L5box are closed by
certified outward-rounded interval arithmetic whose certificates are independently
re-verified in this run by a second, from-scratch engine.  No theorem-strength
lemma is hidden; every identity is re-derived and machine-checked (scripts listed
in repro_manifest.md).

# 0. Objects and definitions

q > 1, c in (0, 1/2).

alpha_1(c), alpha_2(c): the unique roots of the even and odd secular equations
  E(alpha) = c alpha,  E(alpha) := arctan(1/(q tan alpha))   on (0, pi/2);
  O(alpha) = c alpha,  O(alpha) := pi - arctan(q tan alpha)  on (0, pi/2),
                             O(alpha) := arctan(-q tan alpha) on (pi/2, pi).
Both E and O are strictly decreasing with derivative -q/Phi(alpha),
  Phi(alpha) := cos^2 alpha + q^2 sin^2 alpha > 0.
(Note: the task packet's product-of-tangents form of the odd equation is false;
the form above is the one verified against the transfer-matrix solver in the
origin run R-20260805T000000Z-gapn1-a1b2c3, Section 2.1.)

  W(alpha) := 3 + 2 alpha cot alpha,
  Mtilde(alpha;c) := alpha^2 sin^2 alpha / (q + c Phi(alpha)),
  G(alpha;c) := (d/dc) log Mtilde(alpha(c);c)
              = -Phi W/(q + c Phi) + 2 c alpha Phi (q^2-1) sin alpha cos alpha
                / (q + c Phi)^2,
  G_k(c) := G(alpha_k(c);c),   Mtilde_k(c) := Mtilde(alpha_k(c);c),
  H(c) := G_2(c) - G_1(c),
  Ftilde(c) := Mtilde_1(c) - Mtilde_2(c),
  Ftilde'(c) = Mtilde_1 G_1 - Mtilde_2 G_2,
  H'(c) = dG_2/dc - dG_1/dc   (total derivatives along the curves),
  Ftilde''(c) = Mtilde_1 J_1 - Mtilde_2 J_2,   J_k := G_k^2 + dG_k/dc.
The identity Ftilde'' = dFtilde'/dc is exact: with Mtilde' = Mtilde G and
dG_k/dc = J_k - G_k^2 (the latter is the definition of J), the two G^2 terms
cancel.  [A2 in problem_contract.md; machine-verified.]

# 1. Target

For all q > 1 and all c in (0, 1/2):

  (LOG)  (d/dc) log(Mtilde_1/Mtilde_2) = G_1 - G_2 < 0,   i.e. H = G_2 - G_1 > 0;
  (FP)   Ftilde'(c) = Mtilde_1 G_1 - Mtilde_2 G_2 < 0.

(LOG) is the packet-form statement; (FP) is the form consumed by T4 in the origin
report.  Finding C1 (parent audit): the two forms are NOT logically equivalent, so
each is proved separately.

# 2. Reduction (audited in the parent run; rechecked in this run)

## 2.1 L1: G_1 < 0 for all q > 1, c in (0, 1/2).  [PROVED, parent]

Written in the parent candidate (Section 2.1): with W_1 > 0, and
(q^2-1) sin a1 cos a1 <= Phi_1 cot a1 (equivalent to 0 <= 1), the cross term is
bounded by 2 c a1 Phi_1^2 cot a1/(q + c Phi_1)^2 < 2 a1 cot a1, while
W_1 (q + c Phi_1) > 2 a1 cot a1 (q + c Phi_1) > 2 c a1 (q^2-1) sin a1 cos a1,
so G_1 < 0.  Re-verified numerically on grids (0 violations, verify_parent_bases.py).

## 2.2 L2: if G_2 >= 0 then both forms hold.  [PROVED, parent]

H = G_2 - G_1 > 0 since G_1 < 0; Ftilde' = Mtilde_1 G_1 - Mtilde_2 G_2 < 0 since
Mtilde_1 G_1 < 0 and -Mtilde_2 G_2 <= 0.

## 2.3 Region split

By L1 and L2, both forms hold on the set {G_2 >= 0}.  The two boundary lemmas

  R1  G_2 >= 0 for all q >= 2, c in (0, 1/2).
  R2  G_2 >= 0 for all q > 1, c in (0, 0.4].

imply Region B := {(q,c) : G_2 < 0} is contained in (1,2) x (0.4, 1/2), hence in
Box := (1,2] x [0.4, 0.5].

## 2.4 Closure on Region B.  [PROVED given R1, R2, L4box, L5box, B4, B5]

For (q,c) in Region B, c < 1/2 and [c, 1/2] x {q} is inside Box.  L4box
(H' < 0 on Box) gives H(c) > H(1/2); B5 gives H(q, 1/2) > 0, so (LOG) holds.
L5box (Ftilde'' > 0 on Box) gives Ftilde' strictly increasing in c, so
Ftilde'(c) < Ftilde'(q, 1/2); B4 gives Ftilde'(q, 1/2) < 0, so (FP) holds.

The KEY LEMMA is therefore reduced to R1 ^ R2 ^ L4box ^ L5box plus the bases
L1, L2, B4, B5 (B7 and B6 are not needed on this route).

## 2.5 Base lemmas (parent, rechecked numerically in this run)

  B4  Ftilde'(q, 1/2) < 0 for all q > 1.  [closed form, parent Section 3.1]
  B5  H(q, 1/2) = 2 pi q (q+1)/(2q+1)^(3/2) > 0.  [exact, parent Section 3.2]
Both re-verified on grids (verify_parent_bases.py: 0 violations).

# 3. The (q,u) reformulation and the sign identity

Parametrize the odd curve by gamma := pi - alpha_2 in (0, pi/2) and

  u := q tan(gamma) = tan(c alpha_2),   A := alpha_2 = pi - gamma.

Then A = pi - arctan(u/q) and c = arctan(u)/A.  On c in (0, 1/2) the map
c -> u is strictly increasing (d/dc [c alpha_2] = alpha_2 q/(q + c Phi_2) > 0),
u(0+) = 0, u(1/2) = sqrt(2q+1) (exact; verified 15+ digits and derived: at
c = 1/2, u = q tan(alpha_0) = sqrt(2q+1)).  Hence the two regions become

  R1-region:  (q,u) in {(q,u) : q >= 2, 0 < u < sqrt(2q+1)};
  R2-region:  (q,u) in {(q,u) : q > 1,  0 < u <= u_c(q)},
      where u_c(q) = tan(0.4 alpha_2(0.4,q)) < sqrt(2q+1) is the c = 0.4 curve.

## 3.1 IN and the sign identity.  [DERIVED; verified 500 random points at 60
digits, 0 sign mismatches; symbolic check diff = 0]

  IN(q,u) := (q^2+u^2) A (2 A q - 3 u + 2 arctan(u)) - 3 u q (1+u^2) arctan(u),
  A = pi - arctan(u/q).

Identity (exact, verified symbolically):  IN = G_2 * POS with
  POS = D^2 A (q^2+u^2) u / (Phi(alpha_2) q) > 0,   D = q + c Phi(alpha_2).
Hence Sign(G_2) = Sign(IN) on the whole domain, and G_2 >= 0 iff IN >= 0.

Sketch of derivation (see research_ledger.md, entry 3): with t := arctan(u),
c = t/A, Phi(alpha_2) = q^2(1+u^2)/(q^2+u^2), W(alpha_2) = 3 - 2 A q/u,
sin(alpha_2)cos(alpha_2) = -u q/(q^2+u^2), one obtains after clearing the
positive denominators u, A, q^2+u^2, D^2/Phi:
  A (q^2+u^2) u D^2 G_2 / Phi = q [ A (q^2+u^2) (2 A q - 3 u + 2 t) - 3 t u q (1+u^2) ],
whose bracket is exactly IN.  [verified symbolically, verify_algebra_sym.py]

# 4. M2: dIN/du < 0 on D := {(q,u) : q > 1, 0 < u < sqrt(2q+1)}.  [PROVED]

## 4.1 Exact derivative.  [DERIVED; verified vs central finite differences at
1e-14; symbolic diff = 0]

  M2(q,u) := dIN/du = 4 A^2 u q - 7 A q^2 - 9 A u^2 + 2 A (q^2+u^2)/(1+u^2)
                      + t (4 A u - 5 q - 9 q u^2),   t := arctan(u).

## 4.2 h(u) < 0 for all u > 0.  [PROVED, elementary]

  h(u) := 4 u (pi - arctan u) - 5 - 9 u^2.

h''(u) = -8/(1+u^2)^2 - 18 < 0, so h is strictly concave and h' strictly
decreasing.  h'(0) = 4 pi > 0.  At u = 1/2:
  h'(1/2) = 4(pi - arctan(1/2)) - 1.6 - 9 > 4(3.14 - 0.46459) - 10.6 = 0.1016 > 0
(arctan(1/2) < 1/2 - 1/24 + 1/160 = 0.464583... < 0.46459 by the alternating series).  At
u = 0.53:
  h'(0.53) = 4(pi - arctan(0.53)) - 4(0.53)/(1+0.53^2) - 9.54
           < 4(3.142 - 0.48037433) - 2.12/1.3 - 9.54
           = 10.6465... - 1.6308 - 9.54 < 0
(arctan(0.53) > 0.53 - 0.53^3/3 = 0.48037433 by the alternating series;
pi < 3.142; 1.2809 < 1.3 gives 2.12/1.2809 > 2.12/1.3, so the negative term
-2.12/1.2809 is < -2.12/1.3).  Numerically h'(0.53) = -0.5781.
Hence h' has a unique zero u* in (0.5, 0.53), h increases on (0, u*) and
decreases on (u*, inf), and for all u > 0:
  h(u) <= h(u*) = 4 u*^2/(1+u*^2) + 9 u*^2 - 5   [using h'(u*) = 0]
         < 13 u*^2 - 5 < 13 (0.53)^2 - 5 = -1.3483 < 0.

## 4.3 M2(1,u) = pi h(u) < 0 for all u > 0.  [DERIVED; verified 1e-45; symbolic]

Direct substitution of q = 1 into M2 gives pi (4 u (pi - arctan u) - 5 - 9 u^2).

## 4.4 dM2/dq < 0 on D.  [PROVED: certified interval on the compact part,
elementary tail bound]

Exact derivative (verified vs central FD at 1e-14; symbolic diff = 0), with
S := q^2+u^2:

  dM2/dq = 4 A^2 u + 8 A u^2 q/S - 7 q^2 u/S - 14 A q - 9 u^3/S
           + 2 u/(1+u^2) + 4 A q/(1+u^2) + t (4 u^2/S - 5 - 9 u^2).

Compact part: cert_dM2dq_boxes.json encloses dM2/dq < 0 on the box
[1, 20] x [0, y1] with y1 = 6.403124237432848686488217674621813264520 (a
40-digit truncation of sqrt(41); 84 leaves; worst upper bound -0.19024...).
The remaining strip [1, 20] x [y1, sqrt(41)] is covered by
cert_dM2dq_strip_boxes.json: it certifies dM2/dq < 0 on
[1, 20] x [y1, y1 + 10^-30] (10 leaves; worst upper bound -448.745...), and
(y1 + 10^-30)^2 = 41.000...0000128 > 41 by exact squaring (cert_dM2dq_strip.py),
so sqrt(41) < y1 + 10^-30 and [1, 20] x [y1, sqrt(41)] is contained in the
certified strip.  Since D intersected with (1, 20] is contained in
[1, 20] x [0, sqrt(41)] (u < sqrt(2q+1) <= sqrt(41) for q <= 20), the two
certificates together certify dM2/dq < 0 on D intersect {q <= 20}.  Both
certificates are verified in this run by the predecessor verifier (with the
region constants as declared) and independently by a second, from-scratch
interval engine (verify_certificates_indep.py and verify_dM2dq_strip_indep.py).

Tail: for q >= 20 and 0 < u < sqrt(2q+1), with A <= pi, A >= pi - arctan(u/q)
>= pi - u/q >= pi - sqrt(2q+1)/q, t <= pi/2, u <= sqrt(2q+1), S >= q^2,
2u/(1+u^2) <= 1, (q^2+u^2)/(1+u^2) <= q^2:

  dM2/dq <= 4 pi^2 sqrt(2q+1) + 8 pi (2q+1)/q + 1 + 4 pi q
           - 14 pi q + 14 sqrt(2q+1) + 2 pi (2q+1)/q^2
         = B(q) := (4 pi^2 + 14) sqrt(2q+1) + 8 pi (2q+1)/q + 1
                   + 2 pi (2q+1)/q^2 - 10 pi q.

(Each negative term is bounded above by 0 or by the A lower bound; the term
t(4u^2/S - 5 - 9u^2) is bounded by 2 pi (2q+1)/q^2, since t <= pi/2 and
4u^2/S <= 4u^2/q^2 <= 4(2q+1)/q^2.)  B(20) = -232.723... < 0, and for q >= 20
  B'(q) = (4 pi^2+14)/sqrt(2q+1) - 8 pi/q^2 - 4 pi(q+1)/q^3 - 10 pi
        <= (4 pi^2+14)/sqrt(41) - 10 pi < 0
((4 pi^2+14)/sqrt(41) < 53.69/6.4 = 8.39 < 31.4 = 10 pi, using pi < 3.15,
pi > 3.14, sqrt(41) > 6.4).  Hence B is strictly decreasing on [20, inf) and
dM2/dq < 0 for all q >= 20, 0 < u < sqrt(2q+1).

## 4.5 M2 < 0 on D.  [PROVED]

Fix (q,u) in D.
- If u <= sqrt(41): integrate dM2/dq along the path q' in [1, q] at fixed u.
  For q' <= 20 the point (q',u) lies in the certified box [1,20] x [0,sqrt(41)]
  (u <= sqrt(41)), where dM2/dq < 0 by the two certificates (main box + strip);
  for q' >= 20, dM2/dq < 0 by B(q') (u <= sqrt(41) <= sqrt(2q'+1)).  Hence M2(q,u) < M2(1,u) = pi h(u) < 0.
- If u > sqrt(41): then q > 20 (u < sqrt(2q+1) implies 2q+1 > u^2 > 41).  Put
  t := u/q in (0, t_max], t_max := sqrt(2q+1)/q <= sqrt(41)/20 (the function
  q -> sqrt(2q+1)/q is decreasing on q >= 1).  Since q^2 t^2 = u^2 > 41:

    M2/q^2 = 4 A^2 t - 7 A - 9 A t^2 + 2 A (1+t^2)/(1+q^2 t^2)
             + (t0/q)(4 A t - 5) - 9 q t0 t^2,   t0 := arctan(u),

  and the last two terms are <= 0 (4 A t - 5 <= 4 pi t_max - 5 < 0, t0/q > 0).
  Moreover 4 A^2 t <= 4 pi^2 t_max, -7 A <= -7(pi - arctan t_max),
  -9 A t^2 <= 0, 2 A (1+t^2)/(1+q^2 t^2) <= 2 pi (1+t_max^2)/42.  Hence

    M2/q^2 <= 4 pi^2 t_max - 7(pi - arctan t_max) + 2 pi (1+t_max^2)/42.

  With pi in (3.14, 3.15), t_max = sqrt(41)/20 < 0.33, arctan(t_max) < 0.33:
  RHS <= 4 (3.15)^2 (0.33) - 7 (3.14 - 0.33) + 2 (3.15)(1+0.33^2)/42
       = 13.10 - 19.67 + 0.1665 < 0.   (Numerically the sharp value is -7.018.)
  So M2(q,u) < 0.

Therefore dIN/du = M2 < 0 on D.  QED.

# 5. CORNER: G_2(1/2;q) >= 0 for all q >= 2.  [PROVED]

## 5.1 c = 1/2 curve.  At c = 1/2, alpha_1 = x and alpha_2 = pi - x with
x := alpha_0(q) = 2 arcsin(1/sqrt(2(q+1))), cos x = q/(q+1),
sin x = sqrt(2q+1)/(q+1)  [derived; used in the parent B4].

## 5.2 Closed form.  [DERIVED; verified symbolically, diff = 0, and at 1e-50]

With A := alpha_2 = pi - x, Phi(A) = 2q^2/(q+1), D = q(2q+1)/(q+1),
W(A) = 3 - 2(pi-x)q/sqrt(2q+1), sin(A)cos(A) = -q sqrt(2q+1)/(q+1)^2:

  G_2(1/2;q) = -Phi W/D - (pi-x) Phi (q^2-1) sin(A)cos(A)/D^2
             = 2 q (q+1) (pi - x - 3 sin x) / (2q+1)^(3/2)
             = 2 q ((pi-x)(q+1) - 3 sqrt(2q+1)) / (2q+1)^(3/2).

## 5.3 Reduction to a one-variable inequality.  q >= 2 is equivalent to
x <= arccos(2/3) (q = cos x/(1 - cos x)).  The prefactor 2q(q+1)/(2q+1)^(3/2)
is positive, and x -> pi - x - 3 sin x is strictly decreasing on (0, pi/2)
(derivative -1 - 3 cos x < 0).  Hence

  min_{q >= 2} G_2(1/2;q) = G_2(1/2;2) = 12 (pi - arccos(2/3) - sqrt(5)) / (5 sqrt(5)).

(At q = 2, x = arccos(2/3) and sin x = sqrt(5)/3.)

## 5.4 Elementary certificate: pi - arccos(2/3) - sqrt(5) > 0.

Let y := pi - sqrt(5).  The claim is arccos(2/3) < y.  Since cos is strictly
decreasing on (0, pi) and both arguments lie in (0, pi) (y in (0.9, 1)),

  arccos(2/3) < y  <=>  cos(arccos(2/3)) > cos(y)  <=>  2/3 > cos(pi - sqrt(5))
                    <=>  cos(sqrt(5)) > -2/3  <=>  cos(y) < 2/3.

Now pi > 3.14 and sqrt(5) < 2.24 give y > 0.9, and the alternating Taylor
upper bound (terms decreasing, y^2 < 30) gives

  cos(y) <= 1 - y^2/2 + y^4/24 < 1 - (0.9)^2/2 + (0.9)^4/24
          = 1 - 0.405 + 0.0273375 = 0.6223375 < 2/3,

because z -> 1 - z^2/2 + z^4/24 is decreasing on (0, sqrt(6)) and y > 0.9.
Hence pi > arccos(2/3) + sqrt(5) and G_2(1/2;q) > 0 for all q >= 2.  QED.

# 6. C4: G_2(0.4;q) >= 0 for all q >= 1.  [PROVED]

## 6.1 Curve parametrization.  On the c = 0.4 curve put v := arctan(u) in
[2 pi/7, 2 pi/5).  Then A = 2.5 v, q = tan(v)/tan(pi - 2.5 v),
u = tan(v), and [DERIVED; verified numerically on 50 points and in the
certificate re-evaluations]

  IN = A * K(v),   K(v) := (q^2+u^2)(5 v q - 3 u + 2 v) - 1.2 u q (1+u^2).

The endpoint v = 2 pi/7 corresponds to q = 1; as v -> 2 pi/5, q -> +inf.
So C4 is equivalent to K(v) >= 0 on [2 pi/7, 2 pi/5).

## 6.2 Interval leg: K > 0 on [2 pi/7, 2 pi/5 - 10^-3].  [CERTIFIED]

cert_c4_boxes.json contains 200 leaves with
  v_lo = 2 pi/7 - 2.64e-62,  v_hi = (2 pi/5 - 10^-3) + 2.16e-60.
The coverage facts are certified by outward-rounded interval arithmetic in
cert_tail_constants.py (Machin pi at 90 digits): iv(2 pi/7).lo >= v_lo and
iv(2 pi/5 - 10^-3).hi <= v_hi.  The stored leaf endpoints are 60-digit decimals
and are not exactly contiguous (max gap 1e-59, total 6.25e-58); the slivers are
covered by re-evaluating K on each epsilon-inflated box [a - 1e-58, b + 1e-58]
with the same interval engine (worst inflated lower bound 2.421764... > 0,
cert_tail_constants.py part C).  The stored worst lower bound over the leaves is
2.421764... > 0.  The certificate is verified in this run by the predecessor
verifier (with the corrected region constants; the shipped verifier used stale
constants, see audit_report.md Section 4) and independently by the second engine
(independently re-evaluated worst lower bound 2.497...; 0 sign / 0 overlap / 0
point failures).  Hence K > 0 on the whole [2 pi/7, 2 pi/5 - 10^-3].

## 6.3 Tail leg: K > 0 on [2 pi/5 - 10^-3, 2 pi/5).  [PROVED, elementary]

For v in this interval put w := pi - 2.5 v in (0, 2.5e-3], T := tan(w) > 0,
u = tan(v), q = u/T.  Then [DERIVED; verified numerically at 1e-40]

  T^3 K = 5 v u^3 (1+T^2) - 3 u^3 T (1+T^2) + 2 v u^2 T (1+T^2)
          - 1.2 u^2 (1+u^2) T^2.

On the tail, v >= 2 pi/5 - 10^-3 >= 1.25, u = tan(v) >= tan(2 pi/5 - 10^-3)
> 3.06, u <= tan(2 pi/5) < 3.08, and T <= tan(2.5e-3) <= 2.50002e-3.  These four
constant facts are certified by outward-rounded interval evaluations in
cert_tail_constants.py (part D): iv(2 pi/5 - 10^-3).lo > 1.25,
iv_tan(iv(2 pi/5 - 10^-3)).lo > 3.06, iv_tan(iv(2 pi/5)).hi < 3.08,
iv_tan(2.5e-3).hi <= 2.50002e-3.  Hence, dropping the nonnegative term
2 v u^2 T (1+T^2):

  T^3 K >= 5 (5/4)(153/50)^3 - 3 (77/25)^3 (125001/50000000)
               (1 + (125001/50000000)^2)
           - (6/5) (77/25)^2 (1 + (77/25)^2) (125001/50000000)^2
          = 349333915896399959797475605401 / 1953125000000000000000000000
          = 178.85896... > 0

(exact rational arithmetic, cert_tail_constants.py part E; the constants
3.06724... = tan(2 pi/5 - 10^-3), tan(2 pi/5) = 3.07768..., tan(2.5e-3) =
0.0025000052... are also verified to 60 digits in verify_analytic_parts.py).
Since T > 0 on the tail, K > 0 on the tail.

## 6.4 Conclusion: K > 0 on [2 pi/7, 2 pi/5), i.e. C4.  QED.

# 7. R1 and R2.  [PROVED]

## 7.1 R1: for q >= 2, c in (0,1/2), u ranges over (0, sqrt(2q+1)); by M2,
IN(q,u) is strictly decreasing in u, so IN(q,u) > IN(q, sqrt(2q+1)) >= 0
(CORNER).  Hence G_2 >= 0 by the sign identity.

## 7.2 R2: for q > 1, c in (0,0.4], u ranges over (0, u_c(q)] with
u_c(q) < sqrt(2q+1); by M2, IN(q,u) >= IN(q, u_c(q)) >= 0 (C4).
Hence G_2 >= 0.  (The c -> 0 endpoint is the positive limit IN(q,0+) = 2 pi^2 q^3.)

# 8. L4box and L5box.  [PROVED, certified interval arithmetic]

## 8.1 L4box: H' = dG_2/dc - dG_1/dc < 0 on (1,2] x [0.4, 0.5].
cert_L4box_boxes.json: 128 leaves tiling [1,2] x [0.4,0.5] (tiling verified;
total area 0.1), worst upper bound -4.656924..., independently re-evaluated
worst -4.841604... (0 sign failures, 0 point failures in the second engine).
Since the closed box [1,2] x [0.4,0.5] is a superset of the required open box,
L4box follows.

## 8.2 L5box: Ftilde'' = Mtilde_1 J_1 - Mtilde_2 J_2 > 0 on (1,2] x [0.4,0.5].
cert_L5box_boxes.json: 128 leaves, worst lower bound +6.242855..., independently
re-evaluated worst +8.379383... (0 failures).  L5box follows.

## 8.3 Soundness of the interval legs.
The certificates were produced by the interrupted run with: riarith.py (outward-
rounded Decimal interval arithmetic, directed ROUND_FLOOR/ROUND_CEILING, Taylor
series for sin/cos/atan/pi with explicit remainder bounds, audited in this run),
sound_bracket.py (bisection on strictly monotone secular functions that only
shrinks on sign-definite evaluations - a safe bracket), and rigorous.py (natural
interval extensions of Phi, W, Mtilde, G, dG/dc, J with the monotonicity of
alpha_1, alpha_2 used to bracket them over boxes; monotonicity re-derived in this
run: alpha_1 decreases in c and q, alpha_2 decreases in c and increases in q).
In this run every leaf of every certificate was re-evaluated with an independent,
from-scratch engine (mpmath.iv + own rigorous atan + own bisection), with 0 sign
failures, 0 overlap failures and 0 high-precision point failures; the exact
function values at leaf corners and centres (80-digit mpmath) all lie inside the
stored enclosures.  See verify_certificates_indep.py.  Tiling details: the
2-D certificates (dM2/dq main box, dM2/dq strip, L4box, L5box) tile their
regions exactly at 90-digit Decimal arithmetic (total area equals region area
exactly, so the closed-leaf union equals the closed region); the 1-D C4
certificate leaves miss slivers of total measure 6.25e-58 (max width 1e-59) at
the printed 60-digit endpoints, and these slivers are bridged by the
epsilon-inflated re-evaluation in cert_tail_constants.py (part C), so K > 0
holds on the entire interval leg.

# 9. KEY LEMMA: proof complete.

For q > 1, c in (0, 1/2): if G_2 >= 0, L1+L2 give both forms.  Otherwise
(q,c) in Region B subset Box; L4box + B5 give (LOG), and L5box + B4 give (FP).
Both forms hold for all q > 1, c in (0, 1/2).  QED.

# 10. Computational components and status

| Component | Certificate | Worst certified bound | Independent re-check | Status |
|---|---|---|---|---|
| dM2/dq < 0 on [1,20]x[0,y1] (main box) | cert_dM2dq_boxes.json (84 leaves) | upper -0.19024 | PASS (worst -0.19024) | PROVED |
| dM2/dq < 0 on [1,20]x[y1,sqrt(41)] (strip) | cert_dM2dq_strip_boxes.json (10 leaves) | upper -448.745 | PASS (independent -448.745) | PROVED |
| K > 0 on [2pi/7, 2pi/5-1e-3] | cert_c4_boxes.json (200 leaves) | lower 2.42176 | PASS (worst 2.49716) | PROVED |
| H' < 0 on [1,2]x[0.4,0.5] | cert_L4box_boxes.json (128 leaves) | upper -4.65692 | PASS (worst -4.84160) | PROVED |
| F~'' > 0 on [1,2]x[0.4,0.5] | cert_L5box_boxes.json (128 leaves) | lower 6.24286 | PASS (worst 8.37938) | PROVED |
| C4 tail constants (1.25, 3.06, 3.08, 2.50002e-3) + coverage + sliver bridge | cert_tail_constants.py | exact rational LB(T^3 K) = 178.85896 > 0 | 90-digit Machin-pi interval checks PASS | PROVED |

All five certificates (dM2/dq main box, dM2/dq strip, C4, L4box, L5box): tiling
verified (the 2-D certificates tile exactly at 90-digit Decimal precision; the
1-D C4 certificate misses slivers of total measure 6.25e-58 which are bridged by
epsilon-inflated re-evaluation), sign conditions hold, stored enclosures contain
the independent evaluations and the exact point values.  The C4 declared region
constants in the shipped verifier were stale and corrected; the correction is
documented in audit_report.md Section 4.

# 11. Novelty and significance

The KEY LEMMA is a project-derived statement (origin run R-20260805T000000Z-
gapn1-a1b2c3, Section 2.9); no external theorem is used as a premise.  The
reduction R1^R2^L4box^L5box -> KEY LEMMA is from the parent run; the (q,u)
reformulation, the M2/CORNER/C4 proofs and the certificate-based closure of
L4box/L5box are this project's contribution.  Novelty classification:
POTENTIALLY_NEW within the project (no literature claim is made; the statement
does not appear in the surveyed SL literature, status_and_literature.md).

# 12. Remaining gaps

- None in the KEY LEMMA proof as stated.  The three interval-certificate legs
  (dM2/dq compact part, C4 interval leg, L4box, L5box) are finite rigorous
  computations; their outward-rounding soundness model is documented (riarith.py
  header and audit_report.md Section 4), the certificates were independently
  re-verified with a second from-scratch engine, and the C4 slivers were bridged
  by an inflated re-evaluation.  The engines are not formally verified in a proof
  assistant (a reproducibility note, not an open proof obligation of the contract).
- The pointwise-verified facts used as constants (e.g. K(2 pi/7) > 0 is not used;
  the certificate covers it) are all either proved elementarily or covered by the
  certificates.
