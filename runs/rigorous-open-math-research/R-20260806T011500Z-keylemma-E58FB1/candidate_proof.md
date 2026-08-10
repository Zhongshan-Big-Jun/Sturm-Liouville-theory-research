# Candidate proof

Run: R-20260806T011500Z-keylemma-E58FB1
Statement: KEY LEMMA (see problem_contract.md for the normalized contract).
Status: RIGOROUS_PARTIAL_RESULT.  The proof is complete modulo four explicit analytic
lemmas (R1, R2, L4box, L5box), each numerically verified with quantified margins and
each strictly local.  No lemma is hidden; all open obligations are listed in Section 7.

Notation and conventions as in problem_contract.md:  q > 1, c in (0, 1/2),
Phi(alpha) = cos^2 alpha + q^2 sin^2 alpha, W(alpha) = 3 + 2 alpha cot alpha,
Mtilde(alpha;c) = alpha^2 sin^2 alpha / (q + c Phi(alpha)),
G(alpha;c) = -Phi W/(q + c Phi) + 2 c alpha Phi (q^2-1) sin alpha cos alpha / (q + c Phi)^2,
alpha_1(c), alpha_2(c) the unique intersections of beta = c alpha with the even/odd
secular curves (corrected odd equation q tan alpha_2 + tan(c alpha_2) = 0),
G_k = G(alpha_k(c);c), Mtilde_k = Mtilde(alpha_k(c);c),
Ftilde = Mtilde_1 - Mtilde_2,  H = G_2 - G_1,  J = G^2 + G' (total d/dc),
Ftilde' = Mtilde_1 G_1 - Mtilde_2 G_2,  Ftilde'' = Mtilde_1 J_1 - Mtilde_2 J_2.

# 1. Target

For all q > 1 and all c in (0, 1/2):

  (LOG)  (d/dc) log(M_1/M_2) = G_1 - G_2 < 0,      i.e. H = G_2 - G_1 > 0;
  (FP)   Ftilde'(c) = Mtilde_1 G_1 - Mtilde_2 G_2 < 0.

(FP) is the form actually consumed by T4 in the source report; (LOG) is the form as
stated in the task packet.  Audit finding C1 (problem_contract.md) records that the two
are not logically equivalent, so each is proved separately.

# 2. The reduction

## 2.1 Lemma L1: G_1 < 0 for all q > 1, c in (0, 1/2).  [PROVED]

Proof.  Write W_1 = W(alpha_1), Phi_1 = Phi(alpha_1).  Since alpha_1 in (0, pi/2),
sin alpha_1 cos alpha_1 > 0 and W_1 > 0.  From (q^2 - 1) sin alpha_1 cos alpha_1
<= Phi_1 cot alpha_1 (equivalent to -sin^2 alpha_1 <= cos^2 alpha_1, i.e. 0 <= 1),
the cross term of G_1 satisfies

  2 c alpha_1 Phi_1 (q^2-1) sin alpha_1 cos alpha_1 / (q + c Phi_1)^2
     <= 2 c alpha_1 Phi_1^2 cot alpha_1 / (q + c Phi_1)^2
     <= 2 alpha_1 cot alpha_1 .                                    (since c Phi_1 < q + c Phi_1)

Multiplying G_1 < 0 by (q + c Phi_1)^2 / Phi_1 > 0, the claim is equivalent to

  W_1 (q + c Phi_1) > 2 c alpha_1 (q^2 - 1) sin alpha_1 cos alpha_1.

The RHS is <= 2 c alpha_1 Phi_1 cot alpha_1 < 2 alpha_1 cot alpha_1 (q + c Phi_1)
< W_1 (q + c Phi_1), since W_1 = 3 + 2 alpha_1 cot alpha_1 > 2 alpha_1 cot alpha_1.  QED.

## 2.2 Lemma L2: if G_2 >= 0 then (LOG) and (FP) both hold.  [PROVED]

Proof.  G_1 < 0 <= G_2 gives H = G_2 - G_1 > 0.  Also Mtilde_1 G_1 < 0 and
-Mtilde_2 G_2 <= 0, so Ftilde' = Mtilde_1 G_1 - Mtilde_2 G_2 < 0.  QED.

## 2.3 Region split.  [REDUCTION]

By L1 and L2, both target forms are proved on the set {G_2 >= 0}.  It remains to treat
Region B = {(q,c) : G_2 < 0}.  The two boundary lemmas

  R1  G_2 >= 0 for all q >= 2, c in (0, 1/2).                 [PENDING]
  R2  G_2 >= 0 for all q > 1, c in (0, 0.4].                  [PENDING]

imply Region B is contained in the compact box Box = (1, 2) x (0.4, 0.5).  On Box the
following two lemmas hold (numerically verified; proofs open):

  L4box  H' = G_2' - G_1' < 0 on Box.                          [PENDING]
  L5box  Ftilde'' = Mtilde_1 J_1 - Mtilde_2 J_2 > 0 on Box.    [PENDING]

(Note: H' and Ftilde'' denote total derivatives in c along the curves, exactly as in
problem_contract.md.)

## 2.4 Closure on Region B.  [PROVED given R1, R2, L4box, L5box]

Let c < 1/2 be in Region B.  By L4box, H is strictly decreasing in c on Box, hence
H(c) > H(1/2).  Lemma B5 below gives H(q, 1/2) = 2 pi q (q+1)/(2q+1)^(3/2) > 0, so
(LOG) holds.  By L5box, Ftilde' is strictly increasing in c on Box, hence
Ftilde'(c) < Ftilde'(q, 1/2).  Lemma B4 below gives Ftilde'(q, 1/2) < 0, so (FP) holds.

The whole KEY LEMMA is therefore reduced to R1, R2, L4box, L5box plus the bases B1-B5,
B7 proved in Section 3.

# 3. Base lemmas

## 3.1 B4: Ftilde'(q, 1/2) < 0 for all q > 1.  [PROVED, exact closed form]

At c = 1/2, alpha_1 = x and alpha_2 = pi - x with x := alpha_0(q) = 2 arcsin(1/sqrt(2(q+1))),
with cos x = q/(q+1), sin x = sqrt(2q+1)/(q+1), Phi(x) = 2 q^2/(q+1),
W(x) = 3 + 2 x q/sqrt(2q+1), W(pi - x) = 3 - 2(pi - x) q/sqrt(2q+1).
A direct (sympy-verified) computation gives, with q = cos x/(1 - cos x):

  Ftilde'(q, 1/2) = 2 pi (cos x - 1)^3 P(x) / sin^3 x,

  P(x) = 3 x^2 + 6 x sin x - 3 pi x - 3 pi sin x + pi^2.

For x in (0, pi/3) (equivalently q > 1):

  P(x) - (pi - 3x)^2 = 3 (x - sin x)(pi - 2x) > 0,

so P(x) > (pi - 3x)^2 >= 0.  Since (cos x - 1)^3 < 0 and sin^3 x > 0,
Ftilde'(q, 1/2) < 0.  QED.  (Verified numerically to 1e-13 for q in {1.001, ..., 10}.)
Note: the relation cos x = q/(q+1) is exact at c = 1/2 (source Section 2.3, formula (A0)).

## 3.2 B5: H(q, 1/2) = 2 pi q (q+1) / (2q+1)^(3/2) > 0 for all q > 1.  [PROVED, exact]

sympy derivation (corner_exact.py) gives the closed form.  Monotonicity:
  d/dq log H = 1/q + 1/(q+1) - 3/(2q+1) = (q^2 + q + 1)/(q(q+1)(2q+1)) > 0,
so H is strictly increasing in q and H(q,1/2) > H(1,1/2) = 4 pi/(3 sqrt 3) = 2.41840...
QED.

## 3.3 B1-B3: the q = 1 degenerate family.  [PROVED]

At q = 1:  alpha_1 = pi/(2(1+c)) =: u in (pi/3, pi/2), alpha_2 = 2u in (2pi/3, pi),
Phi = 1, G(alpha;c) = -W(alpha)/(1+c), and alpha_k' = -alpha_k/(1+c).  Direct
computation gives (verify_q1_forms2.py, exact):

  J_1(1,c) = N_1(u)/(1+c)^2,  N_1(u) = W(u)^2 + W(u) + u W'(u);
  J_2(1,c) = N_2(2u)/(1+c)^2,  N_2(w) = W(w)^2 + W(w) + w W'(w);
  H'(1,c) = [T(2u) - T(u)]/(1+c)^2,  T(u) = u W'(u) + W(u).

B1 (N_1 > 0 on (pi/3, pi/2)):  W >= 3, and u W'(u) = 2u(cot u - u csc^2 u)
>= -2 u^2 csc^2 u >= -2 (pi/2)^2 (4/3) = -2 pi^2/3 on (pi/3, pi/2) (csc^2 <= 4/3 there),
so N_1 >= 12 - 2 pi^2/3 > 0.  Hence J_1(1,c) > 0 on (0, 1/2).

B2 (N_2 <= 0 on w in [2 pi/3, 5 pi/7]):  with 2 w cot w = W - 3,
  N_2(w) = W^2 + W + w W' = W^2 + 2W - 3 - 2 w^2 csc^2 w = (W - 1)(W + 3) - 2 w^2 csc^2 w.
On [2 pi/3, 5 pi/7], W decreases (W' < 0 on (pi/2, pi)) from W(2 pi/3) = 3 - 4 pi/(3 sqrt 3)
= 0.58160... down to W(5 pi/7) = 3 - (10 pi/7) cot(2 pi/7) = -0.56765..., so
(W - 1)(W + 3) < 0 and N_2 < 0.  Hence J_2(1,c) < 0 on [0.4, 0.5].

B3 (T decreasing on (0, pi)):  T'(u) = 4[cot u - 2 u csc^2 u + u^2 csc^2 u cot u]; its sign
is that of N~(u) = cos u sin^2 u + u^2 cos u - 2 u sin u.  On (pi/2, pi), cos u < 0 so
N~ < 0.  On (0, pi/2), divide by cos u > 0:  N~/cos u = sin^2 u + u^2 - 2 u tan u <= 0,
because 2 u tan u >= 2 u^2 >= u^2 + sin^2 u (tan u >= u and sin u <= u).  Hence T' <= 0,
strictly < 0 on (0, pi) (equality only at 0).  Therefore H'(1,c) = [T(2u) - T(u)]/(1+c)^2
< 0 on (0, 1/2).  QED.

## 3.4 B7: G_2(c; 1) = -W(pi/(1+c))/(1+c) > 0 for c in (0, 0.4].  [PROVED]

At q = 1, alpha_2 = pi/(1+c).  W is strictly decreasing on (pi/2, pi) (W' = 2(cot - u csc^2)
< 0 there).  For c <= 0.4, pi/(1+c) >= 5 pi/7, so W(pi/(1+c)) <= W(5 pi/7).  Now
W(5 pi/7) = 3 - (10 pi/7) cot(2 pi/7) < 0 iff cot(2 pi/7) > 21/(10 pi) = 0.66845...,
which holds: with t = tan(pi/28) < (pi/28)/(1-(pi/28)^2) < 0.1137 < 1/8 (standard bound
tan x < x/(1-x^2) on (0,1)), tan(2 pi/7) = tan(pi/4 + pi/28) = (1+t)/(1-t) < 9/7, so
cot(2 pi/7) > 7/9 = 0.7778 > 21/(10 pi) = 0.6685).  Hence W(5 pi/7) < 0 and
G_2(c;1) = -W/(1+c) > 0 for c in (0, 0.4].  QED.

(Precise bound used numerically: W(5 pi/7) = -0.56765...)

## 3.5 B6 (auxiliary): G_2(c; 2) >= 0 on (0, 1/2).  [VERIFIED NUMERICALLY; proof open]

Grid min = 0.069181 at c -> 1/2 (exact corner value G_2(1/2; 2) = 0.0691814447546...).
A proof would show G_2(c;2) is decreasing in c (verified numerically) and evaluate the
closed corner value.  This is only needed if R1 is closed via the q-monotonicity route
Q1 (Section 6); it is not needed for the main reduction.

# 4. Identity layer (machine-verified, 50-60 digits)

- E1  (d/dc) log(M_1/M_2) = G_1 - G_2.                       [verify_premises P8]
- E2  Ftilde' = Mtilde_1 G_1 - Mtilde_2 G_2.                 [P9a, debug_Fpp to 1e-12]
- E3  D'(c) = (8/q^2)(c+q) F(c);  f_sym = 2(c+q)F/(q u^2 (q^2-1)).   [P5, P7]
- E4  u_k(u,u)^2 = tan^2(alpha_k)/(1/2 + w tan^2 alpha_k).   [P3]
- E5  f_sym = (2/u^2)(T_1 - T_2).                            [P4]
- E6  alpha_1(1/2) = pi - alpha_2(1/2) = alpha_0, sin(alpha_0/2) = 1/sqrt(2(q+1)). [P2]
- E7  H(q,1/2) = 2 pi q (q+1)/(2q+1)^(3/2).                  [exact]
- E8  Ftilde'' = Mtilde_1 J_1 - Mtilde_2 J_2.                [debug_Fpp: dFp/dc match to 2e-9]
- E9  Ftilde'(q,1/2) closed form (B4).                       [verify_Fp12 to 1e-13]

All premises P1-P10 of the source chain are re-checked (problem_contract.md, C3).

# 5. Numerical evidence for the four open lemmas

Grids: q log/linear spaced, c linear; mpmath 30-60 digits; root solves by bisection on
strictly monotone functions (keylemma_lib.py).  All values are minimum/maximum over the
stated grids; they are evidence, not proofs.

| Obligation | Claim | Verified bound | Tight location |
|---|---|---|---|
| R1 | G_2 >= 0, q >= 2 | >= 0.069181 (exact corner; grid min 0.070593) | (2, 1/2) |
| R2 | G_2 >= 0, c <= 0.4 | min 0.415004 | (q -> 1+, 0.4) |
| L4box | H' < 0 on (1,2]x[0.4,0.5] | max -7.7317 | (1.05, 0.5) |
| L5box | Ftilde'' > 0 on (1,2]x[0.4,0.5] | min 14.167 | (2.0, 0.5) |

Additional Region B margins:  |G_1|/|G_2| >= 7.42,  Mtilde_2/Mtilde_1 <= 6.94,
|G_1| - |G_2| >= 2.418,  Ftilde'' >= 14.7,  H' <= -7.1 (on the sampled Region B).

# 6. Future-proofing: the minimal remaining core

R1 and R2 both reduce (numerically verified, unproved) to the single two-variable
monotonicity lemma

  Q1   dG_2/dq >= 0 on (1, inf) x (0, 1/2)          [verified: min ~5e-4, decays to 0]

namely R1 <= Q1 + B6 and R2 <= Q1 + B7 (B7 is proved, B6 verified).  The symbolic
derivative of G_2 in (gamma, q) does not factor (sym_dG2dq.py); a variable change
y = q tan gamma is the natural next step.  L4box and L5box can be attempted directly
(margins 7.7 and 14.2) or by a sound interval-arithmetic certificate.

# 7. Exact remaining gaps (completion criteria)

To upgrade to a complete proof of the KEY LEMMA (both (LOG) and (FP)), it remains to
prove:

  (i)   R1: G_2 >= 0 for q >= 2, c in (0, 1/2);       [analytic proof open]
  (ii)  R2: G_2 >= 0 for q > 1, c in (0, 0.4];        [analytic proof open]
  (iii) L4box: H' < 0 on (1, 2] x [0.4, 0.5];         [analytic proof open]
  (iv)  L5box: Ftilde'' > 0 on (1, 2] x [0.4, 0.5].   [analytic proof open]

Until (i)-(iv) close, the run reports RIGOROUS_PARTIAL_RESULT (skill output protocol).
The reduction itself is sound:  R1 ^ R2 ^ L4box ^ L5box ^ B1-B5 ^ B7  ==>  (LOG) ^ (FP)
==>  T1-T4 close obligation O2 of the source program.

# 8. Repair of T4 (source report, Section 2.9)

The source's T4 text states the KEY LEMMA in log form and lists F' < 0 as an "equivalent
form".  Finding C1: the equivalence is false in general, but the specific implication used
by T4 is "F strictly decreasing on (0,1/2)", which follows from (FP).  This run therefore
proves (FP) separately (reduced to R1, R2, L5box, B4, L1, L2) and keeps (LOG) as the
packet-form statement.  With both forms closed, T4's conclusion (unique zero u*, sign
pattern, D_sym strictly increasing then decreasing) follows verbatim from the source text.
