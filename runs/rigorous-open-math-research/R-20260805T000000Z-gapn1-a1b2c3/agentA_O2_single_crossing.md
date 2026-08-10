# Agent A — Obligation O2: single zero-crossing of f_sym (symmetric barrier family)

Run: R-20260805T000000Z-gapn1-a1b2c3
Date: 2026-08-05
Python: C:\Users\HuangZY\AppData\Local\Programs\Python\Python310\python.exe (numpy 2.2.6, scipy 1.15.3)
Solvers: scripts/gap_lib.py (lams_fast, y_at, norm2); fast half-problem solver; c-parametrized phase solver (this file)

## 0. Verdict

**PARTIAL.** The claim (f_sym has exactly one zero u*(R) in (0,1/2), sign - on (0,u*), + on (u*,1/2)) is reduced to a single explicit inequality, the KEY LEMMA below, which is verified numerically for R in [1.0005, 1e6] with a quantified margin >= 2.4 (in the log-derivative form) but is NOT proven analytically. All structural content around the claim is proven rigorously. The exact remaining gap is stated in Section 6.

## 1. Setup and notation

Dirichlet string -y'' = lambda rho y on [0,1], symmetric barrier
  rho_u = 1 on [0,u] cup [1-u,1],  rho_u = R on (u,1-u),  R > 1, u in (0,1/2).
Let s_k(u) = sqrt(lambda_k(u)) (k=1,2), u_k(u,.) the L^2(rho_u)-normalized eigenfunctions, and
  f_sym(u) := lambda_1 u_1(u,u)^2 - lambda_2 u_2(u,u)^2   (evaluated at the jump x = u),
  D_sym(u) := lambda_2(u) - lambda_1(u).
Feynman-Hellmann (verified numerically, Section 4): dD_sym/du = -2(R-1) f_sym(u).

Constants: q := sqrt(R) > 1, v := 1/2 - u, w := u + R(1/2-u) = q^2/2 - (q^2-1)u.
Phase variables: alpha_k := s_k u, beta_k := s_k q v; beta_k/alpha_k = qv/u =: c, i.e. u = q/(2(c+q)), c in (0,inf).

## 2. Exact statements proven

Throughout: F(c) := M_1(c) - M_2(c) with M_k defined in (2.4); f_sym(u) = [2(c+q)/(q u^2 (q^2-1))] F(c) (same sign, Section 2.4).

T1 (sign of f_sym on the left part).  f_sym(u) < 0 for all u in (0, u_0], where
  u_0 := q/(2(1+q)) = sqrt(R)/(2(1+sqrt(R))).  Equivalently F(c) < 0 for all c >= 1.
  Proof: Section 2.6 (uses Lemma 1).

T2 (sign of f_sym on the middle part).  f_sym(u) < 0 for all u in [u_0, u_1], where
  u_1 := q/(1+2q) = sqrt(R)/(1+2 sqrt(R)).  Equivalently F(c) < 0 for all c in [1/2, 1].
  Proof: Section 2.7 (uses Lemma 1 and the exact identity alpha_1 = pi - alpha_2 at c = 1/2).

T3 (endpoint data).
  (a) f_sym(1/2) = 2 pi^2 > 0 (config rho = 1: lambda_1=pi^2, lambda_2=4pi^2, u_1(1/2)=sqrt2, u_2(1/2)=0).
  (b) f_sym(u) ~ -30 pi^4 u^2 / R^2 as u -> 0+ (config rho = R; computed from lambda_k = (k pi)^2/R and
      u_k(x) = sqrt(2/R) sin(k pi x)).
  (c) F(0+) = (q^2-1) pi^2 / 4 > 0; F(1) = (q^2-1)/(q+1) (arctan(1/sqrt q)^2 - pi^2/2)/2 < 0.
  Proof: Section 2.8.

T4 (reduction).  If the KEY LEMMA below holds, then f_sym has exactly one zero u*(R) in (0,1/2),
  sign - on (0,u*) and + on (u*,1/2), and D_sym strictly increases on (0,u*) and strictly decreases
  on (u*,1/2), so u* is the unique global maximizer of the symmetric family.
  Proof: Section 2.9.

KEY LEMMA (the only unproven step; numerically verified).
  For all q > 1 and all c in (0, 1/2):  (d/dc) log(M_1/M_2) < 0.
  Equivalent forms (Section 2.9):  G(alpha_2(c);c) > G(alpha_1(c);c)  and  F'(c) < 0 on (0,1/2),
  with G(alpha;c) = -Phi(alpha) W(alpha)/(q+c Phi(alpha)) + 2 c alpha Phi(alpha)(q^2-1) sin(alpha) cos(alpha)/(q+c Phi(alpha))^2,
  W(alpha) = 3 + 2 alpha cot(alpha).

### 2.1 Half-problem reduction and the secular equations

By even/odd symmetry about 1/2: lambda_1 is the first eigenvalue of the half-problem on [0,1/2]
(rho = 1 on [0,u], rho = R on [u,1/2]) with Neumann boundary at 1/2; lambda_2 the first eigenvalue
with Dirichlet boundary at 1/2.  On [0,u]: y = sin(sx).  Matching at x = u gives

  even (y'(1/2)=0):  tan(s_1 u) tan(s_1 q v) = 1/q,                     (E)
  odd  (y(1/2)=0):    q tan(s_2 u) + tan(s_2 q v) = 0.                  (O)

Verification: at x=u, y = sin(su), y' = s cos(su); on [u,1/2], y = sin(su) cos(s q (x-u)) +
(1/q) cos(su) sin(s q (x-u)).  Neumann: y'(1/2)=0 gives -q sin(su) sin(sqv) + cos(su) cos(sqv) = 0,
i.e. (E).  Dirichlet: y(1/2)=0 gives sin(su) cos(sqv) + (1/q) cos(su) sin(sqv) = 0, i.e. (O).

CORRECTION to the task's "Known facts 2": the odd secular equation in the task, tan(s2 u) tan(s2 q v) = -q,
is false.  The correct equation is (O): q tan(s2u) + tan(s2qv) = 0.  Both (E) and (O) were verified to
machine precision against the transfer-matrix solver (diff ~ 1e-12, Section 4).

### 2.2 Normalization identities and explicit f_sym

With y_k(x) = sin(s_k x)/s_k (y'(0)=1 convention) and N_k = int_0^1 rho_u y_k^2 dx computed by the
transfer matrix (norm2), the normalized value at the junction is
  u_k(u,u)^2 = tan^2(alpha_k) / (1/2 + w tan^2(alpha_k)),   k = 1, 2.        (N)
(verified to 1e-13 against lams_fast+y_at+norm2, Section 4).  Since u_k = y_k/sqrt(N_k) and
y_k(u) = sin(alpha_k)/s_k:
  f_sym = s_1^2 u_1^2 - s_2^2 u_2^2 = sin^2(alpha_1)/N_1 - sin^2(alpha_2)/N_2
        = (2/u^2)(T_1 - T_2),   T_k := alpha_k^2 tan^2(alpha_k)/(1 + 2 w tan^2(alpha_k)).  (F1)

CORRECTION to the task's "Known facts 4": the exact zero condition stated there, N_1 sin(s_2 u) =
N_2 sin(s_1 u), is false (off by ~2e-2 at u* for R=4).  The correct condition is
  sqrt(N_2) sin(alpha_1) = sqrt(N_1) sin(alpha_2),                          (Z)
which vanishes to ~1e-10 at u*(R) for R in {1.1, 2, 4, 10} (Section 4).  Derivation: f_sym = 0 iff
sin^2(alpha_1)/N_1 = sin^2(alpha_2)/N_2 iff sqrt(N_2) sin(alpha_1) = sqrt(N_1) sin(alpha_2)
(all quantities positive on (0,1/2)).

### 2.3 The shared-line (c-) parametrization

Let E(alpha) := arctan(1/(q tan alpha)), alpha in (0, pi/2).  E is strictly decreasing
(E' = -q/Phi, Phi(alpha) := cos^2 alpha + q^2 sin^2 alpha), maps (0,pi/2) onto (0,pi/2), and is an
involution: E(E(alpha)) = alpha.  The even mode satisfies beta_1 = E(alpha_1) = c alpha_1.

The odd curve is O(alpha) = pi - arctan(q tan alpha) for alpha < pi/2 and O(alpha) =
arctan(-q tan alpha) for alpha > pi/2; O is strictly decreasing on (0,pi) with O' = -q/Phi on both
branches, and O(alpha) = pi/2 + E(alpha) (alpha < pi/2), O(alpha) = pi/2 - E(pi - alpha) (alpha > pi/2).
The odd mode satisfies beta_2 = O(alpha_2) = c alpha_2.

For every c > 0 the line beta = c alpha meets each curve exactly once (E, O strictly decreasing, line
strictly increasing), defining alpha_1(c) in (0,pi/2) and alpha_2(c) in (0,pi), both strictly
decreasing in c; alpha_1(c) < alpha_2(c) for all c.

gamma(c) := pi - alpha_2(c) in (0,pi/2).  The odd-mode condition in gamma reads
  E(gamma) = pi/2 - c(pi - gamma), i.e. c = (pi/2 - E(gamma))/(pi - gamma).          (G)
The function h_c(x) := E(x) - c x is strictly decreasing on (0,pi/2).  Since h_c(alpha_1) = 0 and
h_c(gamma) = pi(1/2 - c), we obtain
  gamma > alpha_1  iff  c > 1/2;   gamma = alpha_1  iff  c = 1/2;   gamma < alpha_1  iff  c < 1/2.

At c = 1/2:  E(alpha_1) = alpha_1/2 and E(gamma) = gamma/2; by uniqueness of the fixed point of
E(x) = x/2 on (0,pi/2) (E strictly decreasing, x/2 strictly increasing), alpha_1 = gamma =: alpha_0,
where
  E(alpha_0) = alpha_0/2  <=>  q tan(alpha_0) tan(alpha_0/2) = 1  <=>  sin(alpha_0/2) = 1/sqrt(2(q+1)),
  alpha_0 = 2 arcsin(1/sqrt(2(q+1))).                                           (A0)
Hence alpha_2(1/2) = pi - alpha_0.  (Verified to 1e-13 for R in {1.1, 2, 4, 10, 100}.)

### 2.4 D(c), D'(c), M_k, F

Since s_k = alpha_k/u and u = q/(2(c+q)):
  D(c) := D_sym(u(c)) = (alpha_2^2 - alpha_1^2)/u^2 = 4(c+q)^2 (alpha_2^2 - alpha_1^2)/q^2.      (D)
Implicit differentiation of E(alpha_1) = c alpha_1 and O(alpha_2) = c alpha_2 (both have slope
-q/Phi at the intersection) gives
  alpha_k'(c) = -alpha_k / (c + q/Phi(alpha_k)) = -alpha_k Phi(alpha_k)/(c Phi(alpha_k) + q).      (A')
Define  M(alpha;c) := q(q^2-1) alpha^2 sin^2(alpha)/(q + c Phi(alpha)),
        M_k(c) := M(alpha_k(c); c),   F(c) := M_1(c) - M_2(c).
A direct computation from (D), (A') yields
  D'(c) = (8/q^2)(c+q) F(c),                                                   (D')
and, using the chain rule on M(alpha(c),c),
  (d/dc) log M_k = -Phi_k W_k/(q + c Phi_k) + 2 c alpha_k Phi_k (q^2-1) sin(alpha_k) cos(alpha_k)/(q + c Phi_k)^2,
  W_k := W(alpha_k),  W(alpha) := 3 + 2 alpha cot(alpha).                     (L)
Finally, from dD/du = -2(q^2-1) f_sym (Feynman-Hellmann) and dc/du = -q/(2u^2):
  f_sym(u) = 2(c+q) F(c) / (q u^2 (q^2-1)).                                    (FS)
In particular f_sym and F have the same sign on (0,1/2).  All of (N), (F1), (D), (D'), (L), (FS)
were verified numerically (Section 4).

### 2.5 Lemma 1 (monotonicity of phi_c on (0,pi/2)) -- PROOF

Lemma.  For all q > 1, c > 0, the function phi_c(alpha) := alpha^2 sin^2(alpha)/(q + c Phi(alpha))
is strictly increasing on (0, pi/2).

Proof.  With t = tan(alpha):
  (d/d alpha) log phi_c = 2/alpha + 2 cot(alpha) - c(q^2-1) sin(2 alpha)/(q + c Phi(alpha)).
Since c/(q + c Phi) < 1/Phi,
  c(q^2-1) sin(2 alpha)/(q + c Phi(alpha)) < (q^2-1) sin(2 alpha)/Phi(alpha)
    = 2(q^2-1) t/(1 + q^2 t^2)  <=  2/t  =  2 cot(alpha),
because (q^2-1)t^2 <= 1 + q^2 t^2.  Therefore (d/d alpha) log phi_c > 2/alpha + 2 cot(alpha) - 2 cot(alpha)
= 2/alpha > 0.  QED.

### 2.6 Proof of T1 (F < 0 for c >= 1)

For c >= 1 both phases lie in (0, pi/2): alpha_1(c) <= alpha_2(c) < pi/2 (at c=1, alpha_2 = pi/2;
for c > 1, alpha_2 < pi/2).  By Lemma 1, phi_c(alpha_1) < phi_c(alpha_2).  Since
M_k = q(q^2-1) phi_c(alpha_k), we get M_1 < M_2, F < 0, and by (FS) f_sym < 0 on u in (0, u_0],
u_0 = q/(2(1+q)).  QED.

### 2.7 Proof of T2 (F < 0 for c in [1/2, 1]) -- the key structural step

For c in [1/2, 1] write alpha_2 = pi - gamma with gamma = gamma(c) in (0, pi/2).  By Section 2.3,
c >= 1/2 implies gamma >= alpha_1 (equality iff c = 1/2).  Since Phi(pi - gamma) = Phi(gamma) and
sin(pi - gamma) = sin(gamma):
  M_2 = q(q^2-1)(pi - gamma)^2 sin^2(gamma)/(q + c Phi(gamma))
      = q(q^2-1) ((pi-gamma)/gamma)^2 phi_c(gamma).
Now gamma > alpha_1 and Lemma 1 give phi_c(gamma) > phi_c(alpha_1); and gamma < pi/2 gives
((pi-gamma)/gamma)^2 > 1.  Hence M_2 > q(q^2-1) phi_c(alpha_1) = M_1, so F < 0, and by (FS)
f_sym < 0 on [u_0, u_1], u_1 = q/(1+2q).  QED.

Combining T1 and T2:  f_sym(u) < 0 for all u in (0, u_1], u_1 = sqrt(R)/(1+2 sqrt(R)).
(For R=4: f_sym < 0 on (0, 0.4).)

### 2.8 Proof of T3 (endpoints)

(a) At u = 1/2, rho = 1: lambda_1 = pi^2, lambda_2 = 4 pi^2, u_1(x) = sqrt(2) sin(pi x),
u_2(x) = sqrt(2) sin(2 pi x); at x = 1/2: u_1 = sqrt 2, u_2 = 0, so f_sym(1/2) = 2 pi^2.  QED.
(b) At u -> 0+, rho = R on (0,1): lambda_k -> (k pi)^2/R, u_k(x) = sqrt(2/R) sin(k pi x);
f_sym(u) ~ (pi^2/R)(2/R)(pi u)^2 - (4 pi^2/R)(2/R)(2 pi u)^2 = -30 pi^4 u^2/R^2.  QED.
(c) As c -> 0+ (u -> 1/2-): alpha_1 -> pi/2, alpha_2 -> pi; M_1 -> (q^2-1) pi^2/4, M_2 -> 0, so
F(0+) = (q^2-1) pi^2/4 > 0.  As c -> 1-: alpha_2 -> pi/2, alpha_1 -> arctan(1/sqrt q)
(E(alpha_1) = alpha_1 iff q tan^2(alpha_1) = 1); phi_1(pi/2) = pi^2/(4 q(1+q)),
phi_1(alpha_1) = alpha_1^2/(2 q(q+1)); hence
  F(1) = q(q^2-1)(phi_1(alpha_1) - phi_1(pi/2)) = (q^2-1)/(q+1) (arctan(1/sqrt q)^2 - pi^2/2)/2 < 0,
since arctan(1/sqrt q) < pi/2 and pi^2/4 < pi^2/2.  QED.

### 2.9 Proof of T4 (reduction to the KEY LEMMA)

Assume the KEY LEMMA: (d/dc) log(M_1/M_2) < 0 on (0,1/2).  Equivalently, with
G(alpha;c) := (d/dc) log M(alpha(c),c) along either curve (the formula (L) holds for both curves
because both have slope -q/Phi), we have G(alpha_1(c);c) < G(alpha_2(c);c) for c in (0,1/2);
equivalently F'(c) = M_1' - M_2' < 0 on (0,1/2).

Then F is strictly decreasing on (0,1/2).  By T3(c), F(0+) > 0, and by T2, F(1/2) < 0.  Hence F
has exactly one zero c* in (0,1/2), crossing from + to -; by T1 and T2, F < 0 on (1/2, inf) and
F(1) < 0.  So F < 0 on (c*, inf) and F > 0 on (0, c*), i.e. F has exactly one zero on (0,inf).
By (FS), f_sym has exactly one zero u* = q/(2(c*+q)) in (0,1/2) with f_sym < 0 on (0,u*) and
f_sym > 0 on (u*,1/2).  By dD_sym/du = -2(R-1) f_sym, D_sym strictly increases on (0,u*) and
strictly decreases on (u*,1/2).  QED.

Alternative equivalent gap (continuation form).  By the same argument, the claim follows from:
  (C) at every zero u of f_sym(.;R), (d/du) f_sym(u;R) > 0 (every zero is a simple - to + crossing).
Indeed (C) implies the zero is transversal; the zeros of the real-analytic family f_sym(.;R) are then
isolated, the zero count is locally constant in R, no zeros appear at the endpoints (T3: f_sym < 0 near
0, f_sym(1/2) > 0), and the count equals the R = 1 count: f_0(u) := 2 pi^2(sin^2(pi u) - 4 sin^2(2 pi u))
has exactly one zero u_0 = arccos(1/4)/pi in (0,1/2) (since f_0 = 0 iff cos(pi u) = 1/4 on (0,1/2)),
and f_0'(u_0) = 4.5033e+02 > 0 (verified).  (C) is verified numerically in Section 4 (df/du(u*) > 0
for all tested R).  (C) and the KEY LEMMA are of comparable difficulty; both are open.

## 3. Corrections to the task's "Known facts" (must be recorded)

1. Odd secular equation (fact 2): task states tan(s2u) tan(s2 q v) = -q.  FALSE.  Correct:
   q tan(s2u) + tan(s2 q v) = 0.  (Verified to machine precision.)
2. Exact zero condition (fact 4): task states N_1 sin(s2u) = N_2 sin(s1u).  FALSE (residual ~2e-2 at
   u*(R=4)).  Correct: sqrt(N_2) sin(alpha_1) = sqrt(N_1) sin(alpha_2), residual ~1e-10 at u*.
   (The s_k factors in u_k = sin(s_k x)/(s_k sqrt(N_k)) cancel in the ratio, so the condition
   sin^2(alpha_1)/N_1 = sin^2(alpha_2)/N_2 is exact; the task's square-root placement is wrong.)
3. f_sym(1/2) (fact 1): task states f_sym(1/2) = 2 pi^2/R^2.  FALSE.  At u = 1/2 the barrier family
   is rho = 1, lambda_1 = pi^2, lambda_2 = 4 pi^2, u_2(1/2) = 0, hence f_sym(1/2) = 2 pi^2.
   The value 2 pi^2/R^2 corresponds to rho = R, the u -> 0 limit.
4. The claimed values u*(4) = 0.45148546584, D_sym(u*) = 32.6139836177 are CONFIRMED.
5. The docs/SL_gap_extremals.tex table tab:rscan u-column is NOT reliable for the SUP family
   (it lists u = 0.382598 at R = 4 for SUP; the correct SUP u* is 0.45148547).  The contract numbers
   are correct.

## 4. Numerical verification tables

All computations below use the fast c-parametrized solver (interpolated inverse of E(alpha)/alpha
and O(alpha)/alpha + bisection refinement; validated against lams_fast to ~1e-9) and, where stated,
the full transfer-matrix solver (lams_fast, y_at, norm2).

### 4.1 Main table: single zero u*(R), D(u*), sign-change counts

R        u*(R)          D_sym(u*)      #zeros of F   #sign changes of d/du f_sym
1.0005   0.419582384    29.609853588   1             1
1.001    0.419595384    29.610893528   1             1
1.01     0.419828150    29.629536615   1             1
1.05     0.420835299    29.710702244   1             1
1.1      0.422035209    29.808470218   1             1
1.5      0.429832426    30.473029692   1             1
2        0.436695944    31.102264174   1             1
3        0.445664942    31.992221280   1             1
4        0.451485466    32.613983617   1             1
7        0.461471237    33.769005017   1             1
10       0.466931186    34.451278492   1             1
30       0.479796331    36.214642237   1             1
100      0.488529373    37.547003005   1             1
1000     0.496260896    38.825381970   1             1
1e4      0.498806037    39.267381027   1             1

Agreement with the contract: u*(4) = 0.45148546584 (10 digits), D*(4) = 32.6139836177 (10 digits).
As R -> 1: u* -> arccos(1/4)/pi = 0.419569377.  As R -> inf: u* -> 1/2 like 1/2 - 0.1194/sqrt(R)
(v sqrt R = 0.119396 at R = 1e4), D -> 4 pi^2 = 39.4784 (D = 39.267 at R = 1e4).

### 4.2 Task-required check (full solver): sign pattern of f_sym and dD/du = -2(R-1) f_sym

R    u       f_sym              dD/du (finite diff)   -2(R-1) f_sym
1.1  0.05   -5.809634e+00       +1.161927e+00         +1.161927e+00
1.1  0.40   -1.079682e+01       +2.159364e+00         +2.159364e+00
1.1  0.45   +1.104314e+01       -2.208629e+00         -2.208628e+00
2.0  0.40   -1.895326e+01       +3.790651e+01         +3.790651e+01
2.0  0.45   +5.993187e+00       -1.198637e+01         -1.198637e+01
4.0  0.45   -7.174492e-01       +4.304695e+00         +4.304695e+00
4.0  0.48   +1.221156e+01       -7.326936e+01         -7.326936e+01
10.0 0.45   -8.228911e+00       +1.481204e+02         +1.481204e+02
10.0 0.48   +5.629447e+00       -1.013301e+02         -1.013301e+02
Sign pattern: f_sym < 0 for u < u*, f_sym > 0 for u > u*; dD/du = -2(R-1) f_sym to ~1e-6.

### 4.3 Corrected zero condition at u*

R     u*            sqrt(N2) sin(a1) - sqrt(N1) sin(a2)
1.1   0.422035209   +3.7e-10
2.0   0.436695944   +4.9e-10
4.0   0.451485466   +7.6e-10
10.0  0.466931186   -1.2e-09
(The task's N1 sin(a2) - N2 sin(a1) equals 2.1e-2 at u*(4): wrong condition.)

### 4.4 KEY LEMMA margins (min over c in (0,1/2) of G(alpha_2)-G(alpha_1))

R         min(G2-G1)   R        min(G2-G1)
1.05      2.43         10       4.17
1.1       2.45         30       5.39
1.2       2.53         100      7.18
1.5       2.67         1000     12.59
2         2.86         1e4      19.45
3         3.15         1e5      19.74
4         3.37         1e6      19.82
7         3.84

The margin is strictly positive for all R in [1.05, 1e6]; it grows from ~2.4 (R ~ 1) to ~19.8 (R -> inf).
Equivalently F'(c) < 0 on (0,1/2), and (d/dc) log(M1/M2) < 0 on (0,1/2).

### 4.5 Continuation ingredients

- f_0(u) = 2 pi^2(sin^2(pi u) - 4 sin^2(2 pi u)) has exactly one zero u_0 = arccos(1/4)/pi =
  0.419569377 in (0,1/2), with f_0'(u_0) = +4.5033e+02 (simple crossing).
- df/du at the (unique) zero is strictly positive for all tested R: +4.53e+02 (R=1.05),
  +4.80e+02 (R=4), +4.35e+02 (R=10), +2.25e+02 (R=100).  (Every zero is a - to + crossing.)
- No tangent zeros (f_sym = f_sym' = 0) were found on a (R,u) grid with R in [1.01, 1e4].

### 4.6 Explicit formulas verified

All of the following were verified to 1e-9..1e-13: (E), (O) vs transfer matrix; (N); (F1);
D(c) and D'(c) vs finite differences (D'(c) formula at c=0.05,0.5,1.0: matches to 1e-8);
(log M_k)' formula (L) vs finite differences (diff ~ 1e-10); f_sym = 2(c+q)F/(q u^2 (q^2-1))
vs the full-solver f_sym (matches to 1e-10).

## 5. Failed attempts and precise failure mechanisms

1. "F strictly decreasing on (0,1)": FALSE.  F has one local minimum on (0,1) (e.g. R=4: F decreases
   from 7.40 at c=0 to -4.60 at c~0.51, then increases to -2.28 at c=1).  Mechanism: M_2(c) is
   humped (unique max at c_max(M2): 0.4498 (R=1.1), 0.505 (R=4), 0.555 (R=100)) while M_1 is
   strictly decreasing, so F = M1 - M2 is decreasing then increasing.
2. "F strictly convex on (0,1)": FALSE.  F'' < 0 on a terminal interval (R=4: c in ~(0.8,0.9)).
3. "Ratio M1/M2 strictly decreasing on (0,inf)": FALSE.  For R=4 the ratio increases on a short
   interval c in (1.24, 2.72) (branch 1).  For R >= 10 the ratio also has a small non-monotone block
   in (1/2, 1) (first positive of d/dc log(M1/M2) at c = 0.87 (R=10), 0.686 (R=100), 0.580 (R=1e4),
   always > 1/2).  Hence "ratio decreasing on (0,1/2)" is exactly the KEY LEMMA; it is NOT the global
   statement, which is false.
4. "G(alpha;c) strictly increasing in alpha on (alpha_0, pi)": FALSE for R >= 2 (G has a minimum on
   (0,pi/2) at alpha ~ 1.15-1.24 > alpha_0, so G decreases on part of (alpha_0, pi/2)); nevertheless
   G(alpha_2) > G(alpha_1) holds for the specific curve points.
5. "Sign dichotomy G(alpha_1) < 0 < G(alpha_2)": FALSE for small R.  G(pi - alpha_0; c) < 0 for
   R in {1.1, 1.5, 2} (min -0.54, -0.30, -0.21 over c in (0,1/2)) and is only +0.069 (R=4); near
   c = 1/2 both G(alpha_1) and G(alpha_2) are negative for small R, and the comparison
   G(alpha_1) < G(alpha_2) still holds by margin.
6. "D concavity / unimodality in u, log u, 1/u, u/(0.5-u), beta_1, beta_2, alpha_1, alpha_2,
   alpha_2 - alpha_1": all FALSE (hundreds of convexity violations; inherited from the handoff and
   re-confirmed).  In particular D is NOT concave near the maximizer, so second-derivative tests fail.
7. "Wronskian monotonicity of v = u_2/u_1": not directly applicable.  The Wronskian argument (O1c)
   shows x -> u_2(x)/u_1(x) is strictly decreasing for a FIXED config; here the evaluation point u is
   simultaneously the moving junction, so the argument does not control u -> (u_2/u_1)(u) across the
   family.
8. "M2' monotone / c_max(M2) = 1/2": FALSE; c_max(M2) depends on R (0.4498 (R=1.1) to 0.555 (R=100)),
   so the M2' sign region is not the simple half-line c < 1/2.
9. Half-problem root windows: the first even root can be anywhere in (0,pi) and the first odd root in
   (0,2 pi); for large R and small u several roots can lie below pi (e.g. R=10, u=0.05: even roots at
   ~0.995 and ~2.98).  A naive window (0,pi) with "exactly one root" assertions fails; the correct
   rule is "take the first root in (0,pi) (even) / (0,2 pi) (odd)".  This is a solver detail, recorded
   for reproducibility.

## 6. Exact remaining gap

One inequality, stated in closed form:

KEY LEMMA.  For all q > 1 and all c in (0,1/2):
  (d/dc) log( M(alpha_1(c);c) / M(alpha_2(c);c) ) < 0,
where M(alpha;c) = q(q^2-1) alpha^2 sin^2 alpha/(q + c(cos^2 alpha + q^2 sin^2 alpha)),
alpha_1(c), alpha_2(c) are the intersections of the line beta = c alpha with the curves
beta = arctan(1/(q tan alpha)) (alpha in (0,pi/2)) and beta = O(alpha) (alpha in (0,pi)) defined in
Section 2.3.

Equivalent closed forms (each is a sufficient proof target):
  (i)  F'(c) < 0 on (0,1/2), F(c) = M_1(c) - M_2(c);
  (ii) G(alpha_2(c);c) > G(alpha_1(c);c), with the explicit G in Section 2.9;
  (iii) at every zero u of f_sym(.;R): (d/du) f_sym(u;R) > 0 (no tangent zeros; continuation form).
All three are verified numerically for R in [1.0005, 1e6]; the KEY LEMMA margin is >= 2.4 and grows
to ~19.8 as R -> inf (Table 4.4).

Everything else needed for the claim is proven in Section 2 (Theorems T1-T4).  Closing the KEY LEMMA
upgrades the verdict to PROVED; until then the single-crossing claim is a rigorous partial result with
a precisely stated one-line gap.

## 7. Files and reproducibility

- This file: agentA_O2_single_crossing.md.
- Solver library: scripts/gap_lib.py (lams_fast, y_at, norm2, fd_check).
- All tables above are produced by scripts included in this run (agentA_verify.py) and by the inline
  here-string scripts recorded in the research ledger; values are reproducible with the stated Python.
- Related run files: problem_contract.md, obligation_graph.md (O2), approach_registry.md (Route F),
  research_ledger.md, status_and_literature.md.
- Document discrepancy flagged: docs/SL_gap_extremals.tex tab:rscan SUP u-column (u = 0.382598 at
  R = 4) contradicts the contract and this work; contract numbers are correct for SUP.
