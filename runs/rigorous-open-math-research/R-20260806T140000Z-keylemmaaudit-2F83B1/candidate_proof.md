# Candidate proof (independent reconstruction of the audited chain)

Run: R-20260806T140000Z-keylemmaaudit-2F83B1
Audit of: R-20260806T070000Z-keylemma2b-0A6D8F (CANDIDATE_COMPLETE_PROOF)
Status of THIS file: the KEY LEMMA proof as independently reconstructed and
verified by this audit.  Every step below was re-derived in this run (symbolic,
numeric at high precision, and by the certificate re-verification with the audit
interval engine).  Definitions are in problem_contract.md.
STRICT: the proof chain below is analytic; the numerical evidence grids
(200k random points + 8M Region B points) are corroboration only and do
not constitute proof.

# Statement

For all q > 1, c in (0, 1/2):

  (LOG)  G_1 - G_2 < 0,   i.e. H := G_2 - G_1 > 0;
  (FP)   Ftilde' = Mtilde_1 G_1 - Mtilde_2 G_2 < 0.

with alpha_1, alpha_2 the unique roots of E(a) = c a and O(a) = c a
(E(a) = arctan(1/(q tan a)), O as in the contract), G, Mtilde as in the contract.

# 1. Reduction

L1: G_1 < 0 everywhere (elementary estimate, re-derived: with alpha_1 in (0, pi/2),
W_1 > 0 and (q^2-1) sin a1 cos a1 <= Phi_1 cot a1; multiplying G_1 < 0 by
(q + c Phi_1)^2/Phi_1 reduces to W_1(q + c Phi_1) > 2 c a1 Phi_1 cot a1, which
follows from W_1 > 2 a1 cot a1 and c Phi_1 < q + c Phi_1).  Numerically re-checked.

L2: if G_2 >= 0 then both (LOG) and (FP) hold (immediate from L1).

R1: G_2 >= 0 for q >= 2; R2: G_2 >= 0 for c <= 0.4, q > 1.
Hence Region B := {G_2 < 0} is contained in (1,2) x (0.4, 0.5).

On Region B (c < 1/2, [c, 1/2] x {q} inside the closed box [1,2]x[0.4,0.5]):
  L4box H' < 0 on the box  =>  H(c) > H(1/2) = B5 > 0  =>  (LOG).
  L5box Ftilde'' > 0 on the box  =>  Ftilde'(c) < Ftilde'(1/2) = B4 < 0  =>  (FP).

The KEY LEMMA is reduced to M2, CORNER, C4, R1, R2, L4box, L5box, B4, B5, L1, L2.

# 2. The (q,u) reformulation and the sign identity

gamma := pi - alpha_2 in (0, pi/2), u := q tan(gamma) = tan(c alpha_2) in
(0, sqrt(2q+1)), A := alpha_2 = pi - arctan(u/q), c = arctan(u)/A.
u is strictly increasing in c (d/dc[c alpha_2] = alpha_2 q/(q + c Phi_2) > 0),
u(0+) = 0, u(1/2) = sqrt(2q+1) (exact, derived from cos x = q/(q+1) at c = 1/2).

IN(q,u) := (q^2+u^2) A (2 A q - 3 u + 2 arctan u) - 3 u q (1+u^2) arctan u.

Identity (symbolic, diff = 0): IN = G_2 * POS with
POS = D^2 A (q^2+u^2) u / (Phi(alpha_2) q) > 0, D = q + c Phi(alpha_2).
Hence Sign(G_2) = Sign(IN) on the whole odd curve.

# 3. M2: dIN/du < 0 on D = {q > 1, 0 < u < sqrt(2q+1)}  [PROVED]

M2(q,u) := dIN/du = 4A^2 u q - 7A q^2 - 9A u^2 + 2A(q^2+u^2)/(1+u^2)
                   + arctan(u)(4Au - 5q - 9q u^2).

(i) M2(1,u) = pi h(u), h(u) = 4u(pi - arctan u) - 5 - 9u^2.  h'' = -8/(1+u^2)^2
    - 18 < 0; h'(0) = 4 pi > 0; h'(1/2) > 0.1016 > 0 (alternating-series upper
    bound on arctan(1/2), pi > 3.14); h'(0.53) < -0.52 < 0 (alternating lower
    bound arctan(0.53) > 0.48037433, pi < 3.142, 2.12/1.2809 > 2.12/1.3).
    Hence h' has a unique zero u* in (0.5, 0.53) and
    h(u) <= h(u*) = 4u*^2/(1+u*^2) + 9u*^2 - 5 < 13(0.53)^2 - 5 = -1.3483 < 0.
    So M2(1,u) < 0 for all u > 0.

(ii) dM2/dq < 0 on D:
    - On [1,20] x [0, sqrt(41)]: the union of cert_dM2dq_boxes.json
      ([1,20]x[0,y1], y1 = 40-digit truncation of sqrt(41), 84 leaves) and
      cert_dM2dq_strip_boxes.json ([1,20]x[y1, y1+1e-30], 10 leaves) covers the
      box (exact tiling; (y1+1e-30)^2 > 41 exactly, so sqrt(41) < y1+1e-30).
      All 94 leaves re-verified with the audit interval engine: dM2/dq < 0 with
      worst upper -0.19024 (main) and -448.745 (strip), 0 failures.
    - Tail q >= 20: with S = q^2+u^2, A <= pi, A >= pi - sqrt(2q+1)/q,
      u <= sqrt(2q+1), t := arctan u <= pi/2, u^2/S <= (2q+1)/q^2:
        dM2/dq <= B(q) := (4 pi^2+14) sqrt(2q+1) + 8 pi (2q+1)/q + 1
                          + 2 pi (2q+1)/q^2 - 10 pi q.
      B(20) = -232.723 < 0 and B' <= (4 pi^2+14)/sqrt(41) - 10 pi < 0 on
      [20, inf), so B(q) < 0 (all bounding arithmetic re-derived and checked).

(iii) M2 < 0 on D:
    - u <= sqrt(41): integrate dM2/dq along q' in [1,q] at fixed u; the
      certificate covers q' <= 20 (all u in [0,sqrt(41)], regardless of D) and
      the tail bound covers q' >= 20 (u <= sqrt(41) <= sqrt(2q'+1)).  Hence
      M2(q,u) < M2(1,u) = pi h(u) < 0.
    - u > sqrt(41): then q > 20.  With t := u/q <= t_max := sqrt(41)/20 < 0.33
      and q^2 t^2 > 41:
        M2/q^2 <= 4 pi^2 t_max - 7(pi - arctan t_max) + 2 pi (1+t_max^2)/42
               <= 4(3.15)^2(0.33) - 7(3.14 - 0.33) + 2(3.15)(1+0.33^2)/42 < 0.
      (Sharp value -7.018.)

Therefore dIN/du = M2 < 0 on D.  QED.

# 4. CORNER: G_2(1/2; q) >= 0 for q >= 2  [PROVED]

At c = 1/2: alpha_1 = x, alpha_2 = pi - x, x = 2 arcsin(1/sqrt(2(q+1))),
cos x = q/(q+1), sin x = sqrt(2q+1)/(q+1).  Exact closed form (symbolic + 1e-45):

  G_2(1/2;q) = 2q(q+1)(pi - x - 3 sin x)/(2q+1)^(3/2).

x -> pi - x - 3 sin x is strictly decreasing on (0, pi/2); q >= 2 iff
x <= arccos(2/3).  Hence min over q >= 2 is at q = 2:

  G_2(1/2;2) = 12(pi - arccos(2/3) - sqrt(5))/(5 sqrt(5)) = 0.0691814447546... > 0,

where pi > arccos(2/3) + sqrt(5) by the elementary certificate: y := pi - sqrt(5)
in (0.9, 1) (pi > 3.14, sqrt(5) < 2.24) and the alternating Taylor upper bound
cos(y) <= 1 - y^2/2 + y^4/24 < 0.6223375 < 2/3 (z(y) decreasing for y^2 < 6),
so cos(y) < 2/3 iff cos(sqrt(5)) > -2/3 iff arccos(2/3) < pi - sqrt(5).  QED.

# 5. C4: G_2(0.4; q) >= 0 for all q >= 1  [PROVED]

On the c = 0.4 curve put v := arctan(u) in [2pi/7, 2pi/5); then A = 2.5 v,
q = tan(v)/tan(pi - 2.5 v), u = tan(v), and (symbolic, diff = 0 with
atan(tan v) = v)  IN = A K(v) with

  K(v) := (q^2+u^2)(5 v q - 3 u + 2 v) - (6/5) u q (1+u^2).

v = 2pi/7 <-> q = 1, v -> 2pi/5 <-> q -> +inf (monotone), so C4 is equivalent to
K >= 0 on [2pi/7, 2pi/5).

Interval leg [2pi/7, 2pi/5 - 1e-3]: cert_c4_boxes.json (200 leaves).  Audited:
leaves inside [first,last]; slivers (total 6.25e-58, max 1e-59) bridged by the
eps = 1e-58 inflated re-evaluation (max gap < 2 eps); coverage of
[2pi/7, 2pi/5-1e-3] by the certified Machin-pi interval; every leaf K > 0 with
worst lower bound 2.49716 > 0; 0 failures.

Tail leg [2pi/5 - 1e-3, 2pi/5): w := pi - 2.5 v in (0, 2.5e-3], T := tan w,
u = tan v, q = u/T.  Exact identity (symbolic, diff = 0):

  T^3 K = 5 v u^3 (1+T^2) - 3 u^3 T (1+T^2) + 2 v u^2 T (1+T^2)
          - (6/5) u^2 (1+u^2) T^2.

Constants verified with the audit engine: v >= 1.25, u >= 3.06, u <= 3.08,
T <= 2.50002e-3.  Dropping the nonnegative term 2 v u^2 T (1+T^2):

  T^3 K >= 5(5/4)(153/50)^3 - 3(77/25)^3(125001/5e7)(1 + (125001/5e7)^2)
           - (6/5)(77/25)^2(1+(77/25)^2)(125001/5e7)^2
          = 349333915896399959797475605401/1953125000000000000000000000
          = 178.85896 > 0.

Since T > 0, K > 0 on the tail.  QED.

# 6. R1 and R2  [PROVED]

R1: for q >= 2, u in (0, sqrt(2q+1)) (u strictly increasing in c, u(1/2) =
sqrt(2q+1)); by M2, IN(q,u) > IN(q, sqrt(2q+1)) = G_2(1/2;q) POS >= 0 (CORNER);
so G_2 >= 0.

R2: for q > 1, c in (0, 0.4], u in (0, u_c(q)] with u_c(q) = u(0.4;q) <
sqrt(2q+1); by M2, IN(q,u) >= IN(q, u_c(q)) = G_2(0.4;q) POS >= 0 (C4); so
G_2 >= 0.  (IN(q,0+) = 2 pi^2 q^3 > 0.)

# 7. L4box and L5box  [PROVED by certified interval arithmetic]

cert_L4box_boxes.json: 128 leaves tile [1,2]x[0.4,0.5] exactly (exact Fraction
area 1/10, no overlaps).  Every leaf re-evaluated with the audit engine:
H' < 0 with worst upper bound -4.8416038; 0 sign/overlap/point failures.

cert_L5box_boxes.json: 128 leaves tile exactly.  Every leaf re-evaluated:
Ftilde'' > 0 with worst lower bound +8.3793828; 0 failures.

The closed boxes are supersets of the required open box (1,2]x[0.4,0.5], so
L4box and L5box follow.

# 8. Base lemmas B4, B5  [PROVED]

B5: H(q,1/2) = G_2(1/2) - G_1(1/2) = 2 pi q (q+1)/(2q+1)^(3/2) > 0.
(symbolic diff = 0; numeric 1e-45; min 2.4184 at q -> 1+.)

B4: Ftilde'(q,1/2) = 2 pi (cos x - 1)^3 P(x)/sin^3 x with
P(x) = 3x^2 + 6x sin x - 3 pi x - 3 pi sin x + pi^2 and x = 2 arcsin(1/sqrt(2(q+1)))
in (0, pi/3).  P(x) - (pi - 3x)^2 = 3(x - sin x)(pi - 2x) > 0, so P(x) > 0;
(cos x - 1)^3 < 0 and sin^3 x > 0 give Ftilde'(q,1/2) < 0.
(symbolic diff = 0; numeric 1e-45; worst value -2.1e-5 at q -> 1+.)

# 9. Conclusion

For q > 1, c in (0, 1/2): if G_2 >= 0, L1+L2 give both forms.  Otherwise
(q,c) in Region B subset Box; L4box + B5 give (LOG), L5box + B4 give (FP).
Both (LOG) and (FP) hold for all q > 1, c in (0, 1/2).  QED.

# 10. Verification performed in this run

- Every identity: symbolic diff = 0 (audit_symbolic.py, audit_symbolic2.py,
  fresh B4/C4/POS checks).
- Every closed-form constant: 1e-45 numeric agreement.
- All five certificates: exact tiling/coverage + sign conditions with the audit
  engine (output/audit_certificates_v3.txt).
- Evidence grids: 200k random points + 8M Region B points (no violations).
- See audit_report.md for per-obligation verdicts and caveats.
