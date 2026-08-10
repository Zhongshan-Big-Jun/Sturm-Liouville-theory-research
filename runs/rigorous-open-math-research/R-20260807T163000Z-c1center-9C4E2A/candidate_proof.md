# Candidate proof - C1 (O3a): uniqueness of the interior critical point

Run: R-20260807T163000Z-c1center-9C4E2A
Date: 2026-08-07 (session 33 continuation), updated 2026-08-08
Status: RIGOROUS_PARTIAL_RESULT
  - N1 (reduction), A2 (endpoints), and the E1-inf inequality (A3) are STRICT.
  - A4/A5 are complete derivations at leading order with explicitly stated
    error terms; the uniform error control is Gap 1 (G-EST), not yet written.
  - A9 (R -> 1+): closed form of phi and phi' derived and verified; phi' > 0
    on [a0, 1) is CERTIFIED (interval arithmetic on [a0, 0.999]) + STRICT
    (elementary tail bound on (0.999, 1)); b_top* >= 7/10 > b0 is STRICT
    (implicit function theorem).  E1/U'/P0 for R in (1, 1+eps_0) are reduced
    to Gap 1 (explicit O(eps) error bounds + explicit b_top(eps) upper bound).
  - U' is reduced to an explicit transition-layer single-crossing statement
    (A6); that statement is not yet proved.
  - The certified bulk (Part B) is designed but not yet run to coverage.
  - CORRECTION this session (F-016): the previous A9/C8 claim that the
    fp-component limits to the curve sin(2 pi b) = -sin(pi a)/2 (slope 1/14)
    as R -> 1+ is FALSE.  Replaced by the verified structure: S3 is the sheet
    a = a0 + (R-1) phi(b) + O((R-1)^2) through the degenerate point (a0,a0)
    (g_1(a0) = a0 exactly for small R), with phi from first-order perturbation
    theory (explicit, verified to 6 digits).  E1 for small R becomes
    h(a0) = 2a0-1 + O(eps) < 0 and h(beta) -> b_top* - b0 > 0 with O(1)
    margins; P0 and U' reduce to phi' > 0.  Details in A9.
Audit note: sections are labeled [STRICT PROOF] / [DERIVATION] / [CERTIFIED] /
[EVIDENCE].  No [EVIDENCE] item is used to conclude a [STRICT PROOF] statement.
All punctuation ASCII.

## Notation (as in problem_contract.md)

Barrier family rho = 1 + (R-1) 1_{(a,b)} on (0,1), 0<a<b<1, R>1, Dirichlet.
s_k = sqrt(lambda_k), slope-normalized y_k (y(0)=0, y'(0)=1), u_k = y_k/||y_k||,
n_k = ||y_k||^2, f = lambda_1 u_1^2 - lambda_2 u_2^2, R1 = f(a), R2 = f(b).
q = sqrt(R); w = b-a; W = w q (scaled barrier width); eps = 1/q, t = 1/sqrt(q).
fp-component S3: connected component of {R1=0} through (a_fp, 1-a_fp);
b = g_1(a) on I_1 = [a0, a_max1].
u(a) = g_1^{-1}(1-a); h(a) = g_1(a) - 1 + u(a); G(a) = g_1'(a);
Phi(a) = G(a) G(u(a));  h'(a) = (Phi(a) - 1)/G(u(a)).
a0 = arccos(1/4)/pi ~ 0.4195693767;  b0 = 1 - a0.
I = [a0, beta], beta = 1 - g_1(a0)  (right endpoint of the domain of u; u(beta) = a0).

C1: {R1=0, R2=0} has exactly one solution in 0<a<b<1 for every R>1, namely the fp.

================================================================================
PART A - STRICT PROOFS AND DERIVATIONS
================================================================================

## A1. Reduction N1: C1 follows from (E1)+(U')+(P0)   [STRICT PROOF]

Conditions:
  (E1)  h(a0) < 0 < h(beta).
  (U')  Phi - 1 has at most two zeros x1 <= x2 in [a0, beta] with sign pattern
        - + - on [a0,x1), (x1,x2), (x2,beta] (intervals may be empty).
  (P0)  G(a) > 0 for all a in [a0, beta].

Note.  The earlier formulation "Phi unimodal with maximum at a_fp" is STRONGER
than needed and is false for large R (Phi dips below 1 near a0; Part C).  U' is
the condition actually used.  This correction was registered in this run.

Proof.  h'(a) = G(a) - 1/G(u(a)) = (Phi(a) - 1)/G(u(a)) by the chain rule and
u'(a) = -1/G(u(a)) (from G(u(a)) u'(a) = -1).  By (P0), sign(h') = sign(Phi-1).
By (U') h is strictly decreasing on [a0,x1], strictly increasing on (x1,x2),
strictly decreasing on (x2,beta].  (E1) gives h(a0) < 0, hence h < 0 on
[a0,x1].  Since h(beta) > 0 and h is decreasing on (x2,beta], h(x2) >= h(beta)
> 0.  On (x1,x2) h is strictly increasing from h(x1) < 0 to h(x2) > 0, so h has
exactly one zero there.  By O2 and R5 the unique zero is a_fp.  The empty-
interval cases are identical (fewer monotonicity pieces).  By the audited
reduction R1-R6, zeros of h on I are exactly the interior good roots; hence C1.
QED.

## A2. Endpoints and the exact identity chain   [STRICT PROOF]

Lemma.  beta = 1 - g_1(a0) and u(beta) = a0.
Proof.  u(a) is defined iff 1-a lies in the range of g_1, i.e. 1-a >= g_1(a0)
(since g_1 is increasing under (P0) and its range on I_1 is [g_1(a0), g_1(a_max1)]).
Hence the domain of u is a <= 1 - g_1(a0) = beta, and u(beta) = g_1^{-1}(g_1(a0)) = a0.
QED.

Lemma (endpoint asymptotics, conditional on the branch asymptotics (BA)).
Assume (BA): g_1(a) = a + W(a)/q + o(1/q) uniformly near {a0, beta} on S3 with
W continuous there.  Then
  h(a0)   = [W(a0)   - W(1-a0)]/q + o(1/q),
  h(beta) = [W(1-a0) - W(a0)]/q   + o(1/q).
Proof.  u(a0) solves g_1(u) = 1 - a0 = b0; with (BA), u(a0) = b0 - W(b0)/q +
o(1/q) = 1 - a0 - W(1-a0)/q + o(1/q).  Then h(a0) = g_1(a0) - 1 + u(a0) =
[W(a0) - W(1-a0)]/q + o(1/q).  For beta: beta = 1 - g_1(a0) = b0 - W(a0)/q +
o(1/q) and u(beta) = a0, so h(beta) = g_1(beta) - 1 + a0 =
[W(b0) - W(a0)]/q + o(1/q) = [W(1-a0) - W(a0)]/q + o(1/q).  QED.

Consequence.  For large q, (E1) is implied by (E1-inf):  W(1-a0) > W(a0),
plus control of the o(1/q) terms (Gap 1).  (E1-inf) is proved in A3.

## A3. (E1-inf) is an elementary inequality   [STRICT PROOF, conditional on A4]

Setup.  The profile limits (derived in A4, error bounds = Gap 1):
  W(a0)   -> W_L(a0)  := (1-a0) u/pi,   where u in (0, pi/2) solves  sin(u) = sqrt(2 a0) u;
  W(1-a0) -> W_R(1-a0) := (1-a0) x/pi,  where x in (pi/2, pi) solves x^2 cot^2(x) = 1/(2 a0).

Lemma.  u and x exist and are unique; moreover x > u.
Proof.
  (i) sin(u)/u is strictly decreasing on (0, pi/2), from 1 down to 2/pi.
      sqrt(2 a0) in (2/pi, 1) because a0 = arccos(1/4)/pi in (2/pi^2, 1/2)
      (numeric bounds: 2/pi^2 ~ 0.2026, a0 ~ 0.4196, 1/2).  Hence u is unique.
  (ii) Y(x) := x^2 cot^2(x) is strictly increasing on (pi/2, pi):
      Y'(x) = 2 x cot(x) (cot(x) - x csc^2(x));  on (pi/2, pi), cot(x) < 0 and
      cot(x) - x csc^2(x) < 0 (since sin(x)cos(x) < 0 and -x < 0), so Y' > 0.
      Y(pi/2+) = 0, Y(pi-) = +inf; 1/(2a0) > 0, so x is unique.
  (iii) From sin(u) = sqrt(2a0) u:  1/(2a0) = u^2/sin^2(u).  Hence
      x^2 cot^2(x) = u^2/sin^2(u).  With x in (pi/2, pi), cot(x) < 0, so
      -x cot(x) = u/sin(u) > 0.
  (iv) The map Y1(x) := -x cot(x) is strictly increasing on (pi/2, pi):
      Y1'(x) = -cot(x) + x csc^2(x) > 0 (both terms positive).
      Since u in (0, pi/2), Y1(u) = -u cot(u) < 0 < u/sin(u) = Y1(x).
      By strict monotonicity of Y1, u < x.  QED.

Theorem (E1-inf).  W_R(1-a0) - W_L(a0) = (1-a0)(x - u)/pi > 0.  Numerically the
gap is 0.2474707 = (0.5804306 * 1.3394402)/pi (u = 0.7189759, x = 2.0584161).

Corollary.  Under Gap 1 (uniform rate O(1/q) for the two limits in (BA) at a0
and 1-a0, with explicit constants), there is q0(R0, constants) such that
h(a0) < 0 < h(beta) for all q >= q0.  The margin to absorb is 0.2474707
vs. an O(1/q) error (numerically 0.0025 at q = 1000, i.e. ~1%).

## A4. Leading-order profile equations (mechanism: pin, secular, norm, branch)   [DERIVATION]

Exact secular equation.  With w = b - a, theta = q s w:
  F(s) = cos(theta) sin(s(1-w)) - q sin(sa) sin(s(1-b)) sin(theta)
         + q^{-1} cos(sa) sin(theta) cos(s(1-b)) = 0.        (SEC)
(derived from the transfer matrix; exact).
Exact norms (closed form; used for n1, n2):
  n(s) = [a/2 - sin(2sa)/(4s)]/s^2
         + q^2 * { y(a)^2 [w/2 + sin(2 theta)/(4qs)] + (y'(a)/(qs))^2 [w/2 - sin(2 theta)/(4qs)]
                   + 2 y(a) y'(a)/(qs) * sin^2(theta)/(2qs) }
         + y(b)^2 [(1-b)/2 + sin(2s(1-b))/(4s)] + (y'(b)/s)^2 [(1-b)/2 - sin(2s(1-b))/(4s)]
         + 2 y(b) y'(b)/s * sin^2(s(1-b))/(2s),
  y(a) = sin(sa)/s, y'(a) = cos(sa), y(b) = y(a)cos(theta) + y'(a)sin(theta)/(qs),
  y'(b) = -y(a) q s sin(theta) + y'(a) cos(theta).
Branch condition:  R1 = sin^2(s1 a)/n1 - sin^2(s2 a)/n2 = 0.       (BR)

Ground state.  s1 = O(q^{-1/2}).  From (SEC) at leading order (expand in t =
q^{-1/2}, w = W t^2, s1 = alpha t):
  F(s1) = alpha t * [1 - alpha^2 W a (1-b)] + O(t^3),
so alpha^2 = 1/(W a (1-a)) + O(1/q), i.e.
  s1^2 = 1/(q W a (1-a)) + O(q^{-2}),  and  n1 = q a^2 W + O(1).  (GS)

Second mode: one-sided pinning.  For a in a compact subset of (1/2, 1):
  (SEC) with s2 = pi/a + kappa/q, w = W/q, expanded at O(1/q), gives
  cos(theta) + delta sin(theta) = O(1/q),  delta := (pi - s2 a) q,  theta = s2 W,
  i.e.  delta = -cot(theta) + O(1/q).                          (PIN+)
  (The term q sin(s2 a) ... in (SEC) is O(1) because sin(s2 a) = O(1/q); this
  forces the displayed balance.  On the left half-interval, a in (a0, 1/2), the
  pin is at the right edge: v2 = s2 (1-b) = pi - delta/q and the same relation
  delta = -cot(theta) + O(1/q) holds.  Both are derived from (SEC) with the
  appropriate pin; details in the audit report.)
  Norm: for a > 1/2, n2 = a^3/(2 pi^2) + O(1/q)  (the mode is a half-wave in the
  left well (0,a); barrier and right-well contributions are O(1/q) and O(1/q)).
  Branch (BR):  sin^2(s1 a)/n1 = sin^2(s2 a)/n2:
    [alpha^2 a^2/q] / [q a^2 W] = [(delta/q)^2] / [a^3/(2 pi^2)] + ...
  With alpha^2 = 1/(W a (1-a)) and delta = -cot(s2 W), s2 = pi/a:
    2 (pi/a)^2 cot^2(pi W/a) = 1/(W^2 (1-a))                       (P+)
  equivalently, with x = pi W/a in (pi/2, pi):  x^2 cot^2(x) = 1/(2(1-a)).
  Solving for kappa:  kappa = -delta/a = cot(theta)/a, so
    kappa^2 = 1/(2 pi^2 (1-a) W^2) + O(1/q).                      (P+k)
  For a < 1/2 (mode in the right well; n2 dominated by the right region):
    n2 = sin^2(u2) cos^2(theta) (1-b) q^2/(2 s2^2 delta^2) + O(q),  u2 = s2 a,
  and (BR) with delta = -cot(theta) and s2 = pi/(1-a) gives
    sin(pi W/(1-a)) = sqrt(2a) pi W/(1-a).                        (P-)
  Both (P+) and (P-) have unique solutions:
  - (P-): sin(v)/v strictly decreasing on (0, pi/2), sqrt(2a) in (0.916, 1) for
    a in [a0, 1/2); unique v in (0, pi/2); W_L(a) = (1-a) v/pi.
  - (P+): Y(x) = x^2 cot^2 x strictly increasing on (pi/2, pi) (A3(ii)); unique
    x; W_R(a) = a x/pi.
  Uniformity: all displayed O's are uniform on compact subsets of (a0,1/2) and
  (1/2, 1-a0) with constants depending on the subset; this is Gap 1.

## A5. Symmetric fixed point at large q   [DERIVATION; error terms = Gap 1]

On the diagonal: a = 1/2 - xi/q, b = 1/2 + (W - xi)/q, W = q(b-a), s1 = alpha t,
s2 = 2 pi - kappa/q.  Expansions (all at leading order):
  (SEC at s1)  alpha^2 = 2/xi;
  (SEC at s2)  two-sided pin: sin(s2 a) = delta/q, sin(s2(1-b)) = delta/q,
               delta := (pi - s2 a) q = 2 pi xi + kappa/2, theta = q s2 w = 4 pi xi;
               sin(theta)(1 - delta^2) = 2 delta cos(theta);         (SEC*)
  (BR)         n2 = (1-w)/(2 s2^2) -> 1/(8 pi^2),  sin^2(s1 a) = alpha^2 a^2/q,
               n1 = q a^2 W -> q xi/2,  giving  delta^2 = 1/(8 pi^2 xi^2).  (BR*)
From (BR*): delta = 1/(2 sqrt(2) pi xi) > 0.  With kappa = 2(delta - 2 pi xi),
(SEC*) becomes  tan(4 pi xi) = 2 delta/(1 - delta^2) = tan(2 arctan(delta));
since 4 pi xi in (0, 2 pi) and arctan(delta) in (0, pi/2), we get
  4 pi xi = 2 arctan(delta),  i.e.  2 pi xi = arctan(1/(2 sqrt(2) pi xi)),
  i.e.  xi tan(2 pi xi) = 1/(2 sqrt(2) pi).                       (FP*)

Lemma.  (FP*) has a unique solution xi* in (0, 1/4):  xi tan(2 pi xi) is
strictly increasing on (0, 1/4) (product of two positive strictly increasing
functions; tan(2 pi xi) ranges 0 -> +inf), so the equation has exactly one root.
Numerically xi* = 0.119937215937...  Consequently alpha*^2 = 2/xi*
= 16.67539124..., alpha* = 4.0835513..., and
  kappa* = 2(tan(2 pi xi*) - 2 pi xi*) = 2 delta* - 4 pi xi* = 0.36946535...

Theorem (large-q fp limit, modulo Gap 1).  As q -> inf,
  a_fp = 1/2 - xi*/q + o(1/q),   s1(fp) sqrt(q) -> alpha*,
  (2 pi - s2(fp)) q -> kappa*.
[EVIDENCE (Part C1): 0.119396, 0.119766, 0.119883 at q = 1e2, 3.16e2, 1e3 ->
 xi* = 0.119937; s1 sqrt(q): 4.068, 4.079, 4.082 -> 4.0835; (2 pi - s2)q:
 0.3627, 0.3673, 0.3688 -> 0.3695.]

## A6. U' reduced to the transition-layer single-crossing statement   [STRICT REDUCTION]

Generic regime.  For a in a compact subset of (a0, 1/2) (resp. (1/2, 1-a0)),
with W(a) -> W_L(a) (resp. W_R(a)) uniformly (A4 + Gap 1):
  G(a) = 1 + W'(a)/q + O(1/q^2),
  Phi(a) - 1 = [W'(a) + W'(u(a))]/q + O(1/q^2),  u(a) = 1 - a - W(1-a)/q + O(1/q^2).

Lemma (sign of the leading term; strict calculus, conditional on A4).
  (i) W_L' < 0 on (a0, 1/2).  From sin(u) = sqrt(2a) u:
      u'(a) = u / [sqrt(2a)(cos(u) - sqrt(2a))] < 0  (cos(u) < sin(u)/u on
      (0, pi/2)), and W_L' = [(1-a) u' - u]/pi < 0.
  (ii) W_R' > 0 on (1/2, 1-a0).  From x^2 cot^2 x = 1/(2(1-a)):
      x'(a) = x cot(x) / [2(1-a)(cot(x) - x csc^2(x))] > 0,  W_R' = (x + a x')/pi > 0.
  (iii) S(a) := W_L'(a) + W_R'(1-a) < 0 on [a0, 1/2):
      S(a0) = -0.38433 (evaluated from the explicit formulas); W_L' is strictly
      decreasing with W_L' -> -inf as a -> 1/2 while W_R'(1-a) stays in the narrow
      band (0.6986, 0.7311).  [EVIDENCE: S is strictly decreasing on (a0, 0.49)
      on a 200-point grid; S in (-1.3887, -0.3843).]  The analytic monotonicity
      proof of the two explicit derivatives (elementary calculus) is part of Gap 1.
  Consequently Phi(a) - 1 < 0 on the generic regimes for q >= q0 (Gap 1).
  [EVIDENCE (Part C6): S(a0) = -0.3843 vs. measured q(Phi(a0)-1) = -0.374 at
  q = 1000 (1.4% agreement); S(0.45) = -0.482 vs. -0.428.]

Transition layer.  Parametrize a = 1/2 - xi/q.  Along S3,
  G = 1 - W'(xi),  Phi(xi) - 1 = (1 - W'(xi))(1 - W'(xi_u)) - 1,
  xi_u := (0.5 - u)q satisfies W(xi_u) = xi + xi_u, and W = W(xi) solves the
  layer branch equation (two-sided balance, exact statement in audit report).
  By symmetry Phi(u(a)) = Phi(a), so Phi-1's sign is u-invariant.
  [EVIDENCE (Part C7): for q = 1000, Phi-1 < 0 on [a0, 0.4800), > 0 on
  (0.4800, 0.5200), < 0 on (0.5200, beta]; Phi(a0)-1 = -0.000374, Phi(fp)-1 =
  +0.991.  The left zero z0(q) satisfies (0.5 - z0) q ~ 4.3, 5.3, 10.5, 20.0
  for q = 70.7, 100, 316, 1000, i.e. it moves with q and converges to 1/2.]

U'-inf :=  U'-generic (Lemma above)  +  U'-layer:  the layer profile satisfies
  Phi(xi) - 1 > 0 for all xi in [xi_low, xi*] and < 0 for all xi in (xi*, xi_hi]
  with a single crossing, where xi_low/xi_hi are the layer boundaries supplied by
  Gap 1 and the matching of (P-)/(P+) with the layer equation.
Status: U'-generic: (i),(ii) strict calculus; (iii) S < 0 complete modulo an
elementary monotonicity check (Gap 1).  U'-layer is OPEN.

## A7. P0 (branch slope positivity)   [STATUS]

Generic regimes: G = 1 + W'/q + O(1/q^2) > 0 for q >= q0 (W' bounded; uniform,
Gap 1).  Layer: G = 1 - W'(xi); data give W' in (-0.41, ~0.02) (Part C4), so
G in (0.998, 1.411).  P0-inf :=  |W'(xi)| <= c < 1 on the layer, plus the
generic uniform bound.  Status: OPEN, with numerical margin.  R -> 1+ end:
G(a0) -> +inf (branch nearly vertical, db/da = O(1/eps)); P0 holds with a
large margin once phi' > 0 on the sheet (A9).

## A8. Status of obligations

  N1    (E1)+(U')+(P0) => C1                     PROVED (A1; audited).
  G-E1  h(a0) < 0 < h(beta)                      REDUCED: (E1-inf) PROVED (A3)
        + Gap 1 (uniform error terms).  Also needs R -> 1+ end (A9).
  G-U'  M-shape of Phi-1                         REDUCED to U'-generic (PROVED
        calculus) + U'-layer (OPEN) (A6).
  G-P0  G > 0 on I                               REDUCED to uniform Gap 1 bound
        + |W'| < 1 on the layer (A7); margin large.
  Boundary: R -> 1+                              REDUCED (A9): E1/P0/U' for
        small eps follow from phi' > 0 + b_top* > b0 + O(eps) error bounds
        (Gap 1); R -> inf covered by A3-A5 modulo Gap 1.
  Certified bulk (finite R)                      NOT achieved (Part B).

## A9. R -> 1+ structure (CORRECTED this run; replaces the refuted "limit curve" claim)   [DERIVATION + EVIDENCE]

Refuted claim (F-016).  The previous A9/C8 claim stated: "at R = 1 the
fp-component limit curve through (a0, 1-a0) is sin(2 pi b) = -sin(pi a)/2,
slope 1/14 at a0, so G(a0) -> 1/14".  This is FALSE:
  (i) direct continuation of S3 at R = 1.05, 1.1 shows the branch is nearly
      vertical (db/da in (48, 531) at R = 1.05, in (25, 270) at R = 1.1), not
      slope 1/14 ~ 0.0714; G(a0) -> +inf as R -> 1+;
  (ii) no point of S3 at R = 1.05 lies on sin(2 pi b) = -sin(pi a)/2 (e.g. the
      branch point (a,b) = (0.4199, 0.5) has sin(2 pi b) = 0 while
      -sin(pi a)/2 = -0.48);
  (iii) the object is not a limit curve: the branch at R = 1+eps stays within
      a = a0 + O(eps) while spanning b in [a0, b_top] with b_top ~ 0.936.
The correct limit of S3 as R -> 1+ is the vertical segment {a = a0} (with the
first-order sheet below).  The formula "R1(a,b,1) = 2 pi^2 sin^2(pi a) - 8 pi^2
sin^2(2 pi b)" in the old A9 was also wrong: at R = 1 the second term carries
sin^2(2 pi a) (both terms evaluated at x = a).  Registered in audit_report.md
(F-016).

Correct structure (verified).  eps := R - 1.  For small eps the fp-component
S3 is the sheet
  a = A_eps(b) = a0 + eps phi(b) + O(eps^2),  b in [a0, b_top(eps)],
with
  phi(b) = -R1_1(a0; a0, b)/f_const'(a0),
  f_const(a) = 2 pi^2 (sin^2(pi a) - 4 sin^2(2 pi a)),
  f_const'(a0) = 15 pi^3 sqrt(15)/4,
and R1_1 the first-order term of R1 (explicit closed formulas below).
Exact facts:
  (i) (a0, a0) lies on {R1 = 0} for EVERY R: the barrier (a0, a0) is empty,
      R1(a0, a0, R) = f_const(a0) = 0.  For small R the fp-component is the
      component through (a0, a0), i.e. g_1(a0) = a0 exactly (continuation
      from (a0,a0) climbs through the fp; R2 has exactly one interior zero on
      the sheet, at the fp).
  (ii) h(a0) = g_1(a0) - 1 + u(a0) = u(a0) - b0 with u(a0) = A_eps(b0), so
      h(a0) = (2 a0 - 1) + eps phi(b0) + O(eps^2)
            = -0.160861 + 0.026021 eps + O(eps^2) < 0   (margin 0.16).
  (iii) beta = a_max1 < b0 for small R, and h(beta) = b_top - 1 + u(a_max1)
      with u(a_max1) -> a0: h(beta) -> b_top* - b0 > 0 (b_top* ~ 0.936,
      margin 0.35).
  (iv) G(a) = g_1'(a) = 1/(eps phi'(b)) (1 + O(eps)) > 0  (P0) once
      phi'(b) > 0 on the sheet.
  (v) Phi(a) - 1 = 1/(eps^2 phi'(b) phi'(b_u)) - 1 > 0  (U' holds trivially,
      zero zeros) once phi' is bounded away from 0.
Closed form of phi and phi'  [DERIVATION; sym_phi_closedform3.py; verified
against the exact secular solver to ~1e-10 at eps = 1e-4, verify_sheet_exact.py].
With s15 = sqrt(15), m = 56 pi a0 - 6 s15 > 0, n = 2 pi a0 + 3 s15 > 0:
  phi(b) = s15 [ -1920 s15 pi^2 a0^2 + 1920 s15 pi^2 a0 b
            - 64 s15 pi a0 sin(2 pi b) - 448 s15 pi a0 sin(4 pi b)
            - 2700 pi a0 + 1920 pi b cos^2(2 pi b) - 960 pi b cos(2 pi b)
            - 960 pi b - 960 sin(2 pi b) + 480 sin(4 pi b)
            - 1920 pi cos^2(2 pi b) + 960 pi cos(2 pi b) + 225 s15 + 2310 pi ]
            / (57600 pi^2);
  phi'(b) = -N/(60 pi),  N = m u^2 + (2 pi a0 + 3 s15) u + (3 s15 - 58 pi a0)
            + 2 s15 pi (1-b) (1-4u) v,   u = cos(2 pi b), v = sin(2 pi b).
Factored form:  phi'(b) 60 pi = (1-u)(m(1+u)+n) + 2 s15 pi (1-b) (4u-1) v,
with (1-u) = 2 sin^2(pi b).  Exact: phi(a0) = 0, phi(b0) = 0.0260217.

Strict result (phi' > 0 on [a0, 1))  [CERTIFIED + STRICT PROOF]
  Part 1 [CERTIFIED]: cert_phi_prime.py, mpmath.iv interval arithmetic
  (200-bit, correctly-rounded interval extensions of cos/sin), uniform
  4000-cell grid on [a0, 0.999]: phi' > 0 in every cell; worst enclosure
  lower bound 8.896e-6 (at b ~ 0.9989).
  Part 2 [STRICT, elementary]: for b = 1-e, 0 < e <= 1/1000, the standard
  bounds sin(pi e) >= pi e (1-(pi e)^2/6), cos(pi e) >= 1-(pi e)^2/2,
  sin(2 pi e) <= 2 pi e, 4 cos(2 pi e) - 1 <= 3, and m, n > 0 give
    phi'(b) 60 pi >= 2 (pi e)^2 (1-d1)^2 (2 m (1-d2)^2 + n) - 12 s15 pi^2 e^2
                   = C_tail e^2,   d1 = (pi/1000)^2/6, d2 = (pi/1000)^2/2,
  with C_tail >= 9.651926 (interval-certified; m > 50.5, n > 14.2).  Hence
  phi' > 0 on (0.999, 1).  Conclusion: phi' > 0 on [a0, 1).

Structural lemma (b_top* > b0)  [STRICT PROOF]
  Fix b-bar = 7/10 in (b0, 1).  R1 is real-analytic in (a, b, eps); at
  eps = 0 the barrier is empty, so R1(a, b-bar, 0) = f_const(a),
  R1(a0, b-bar, 0) = f_const(a0) = 0, and partial_a R1(a0, b-bar, 0) =
  f_const'(a0) = 15 pi^3 s15/4 != 0.  By the implicit function theorem at
  (a0, 0), uniformly for b-bar in [a0, 7/10] by compactness and smoothness,
  there is eps_2 > 0 and a unique real-analytic a = A(b-bar, eps) solving
  R1(a, b-bar, eps) = 0 with A(b-bar, 0) = a0.  At b-bar = a0 the solution
  is A(a0, eps) = a0 exactly (empty-barrier degeneracy).  The fp satisfies
  R1(a_fp, b_fp, eps) = 0 with (a_fp, b_fp) -> (a0, b0), so by uniqueness
  a_fp = A(b_fp, eps) for small eps; hence the arc b |-> (A(b, eps), b),
  b in [a0, 7/10], lies in the fp-component S3.  Therefore
  b_top(eps) >= 7/10 and b_top* := liminf b_top(eps) >= 7/10 > b0 ~ 0.5804.

Consequences (all modulo Gap 1: explicit O(eps) error bounds and an explicit
upper bound b_top(eps) <= 1 - delta_0):
  (i)   h(a0) = 2 a0 - 1 + eps phi(b0) + O(eps^2)
        = -0.160861 + 0.026022 eps + O(eps^2) < 0        (margin 0.16);
  (ii)  h(beta) = b_top - 1 + u(a_max1) -> b_top* - b0
        >= 7/10 - b0 ~ 0.1196 > 0                        (margin 0.12);
  (iii) P0: G = 1/A_eps'(b) = 1/(eps phi'(b) + O(eps^2)) > 0 once phi' > 0
        and eps is below the explicit threshold;
  (iv)  U': Phi - 1 = 1/(eps^2 phi'(b) phi'(b_u)) (1 + O(eps)) - 1 > 0 for
        eps below the explicit threshold (b, b_u in [a0, b_top(eps)] subset
        [a0, 1), where phi' > 0).
All R -> 1+ obligations are thereby reduced to Gap 1 (explicit uniform O(eps)
error bounds for A_eps - a0 - eps phi, b_top(eps), h, G, Phi) plus the
explicit upper bound on b_top(eps).

First-order machinery (closed formulas; verified against finite differences of
the exact secular solver to 6 digits, F-016).  With y_k^0 = sin(k pi x)/(k pi),
u_k^0 = sqrt(2) sin(k pi x), n_k^0 = 1/(2 k^2 pi^2):
  lam_k' = -k^2 pi^2 [(b-a) - (sin(2k pi b) - sin(2k pi a))/(2 k pi)];
  y_k^1(x) = -(1/(k pi)) Int_0^x sin(k pi (x-s)) [lam_k' + k^2 pi^2 1_(a,b)](s)
             sin(k pi s)/(k pi) ds   (Green's function sign checked this run);
  n_k^1 = 2 Int_0^1 y_k^0 y_k^1 + Int_a^b (y_k^0)^2;
  w_k^1 = y_k^1/sqrt(n_k^0) - u_k^0 n_k^1/(2 n_k^0);
  R1_1 = lam_1' (u_1^0)^2 + 2 pi^2 u_1^0 w_1^1 - lam_2' (u_2^0)^2 - 8 pi^2 u_2^0 w_2^1
         (all evaluated at x = a0; w_k = y_k/sqrt(n_k) is the L^2(rho)-normalized
         mode used by R1).
Every integral is elementary (products of trig functions), so phi(b) is an
explicit elementary function of b once the algebra is written out; this is the
declared route for the strict R -> 1+ proof (Gap 1 covers the O(eps), O(eps^2)
remainders and the uniformity over b in [a0, b_top(eps)]).

[EVIDENCE (Part C8, script s33_r1plus.py): phi(a0) = 0 to machine precision
(exact identity R1(a0,a0,R) = 0); phi' in (0.006, 0.428) on [a0, 0.98];
phi(b0) = 0.026021; h(a0) measured -0.16052 (R=1.02), -0.15975 (R=1.05) vs
-0.160861 + 0.026021 eps = -0.16034, -0.15956 (agreement to O(eps^2));
b_top(R) = 0.9361, 0.9365, 0.9368 at R = 1.02, 1.05, 1.1; Phi-1 > 0 and G > 0
on the whole domain for all R <= 1000 (min Phi-1 = +0.0005 at R = 1000, min
G = 0.9753 at R = 1000; margins for R <= 100 are >= 0.35 and >= 2.1).]

[EVIDENCE (follow-up 2026-08-09): closed form of phi/phi' matches the exact
secular solver: sheet a*(b, eps) vs a0 + eps phi(b) at eps = 1e-4 differs
< 1e-9 for b in [0.45, 0.9] (verify_sheet_exact.py); phi'(b) closed form vs
finite differences of the exact sheet agrees to 5 digits.  phi' dense scan on
[a0, 0.999] is > 0 with min 3.85e-3 on [a0, 0.98]; near b = 1, phi' ~
9.6521 (1-b)^2 (both consistent with the certification, not part of it).]

================================================================================
PART B - COMPUTER-ASSISTED CERTIFICATION (status)
================================================================================

## B1. Architecture (built in this and prior runs)
  cert_lib.py, cert_roots.py, cert_c1.py, sym_cert_partials.py: exact symbolic
  expressions (sympy) for F, F_s, R1, R2 and their partials, with mpmath.iv
  interval evaluations, intended to certify over boxes (a,b,R):
    - enclosure of the two secular roots s1, s2;
    - sign of R1_a, R1_b (hence G = -R1_a/R1_b and P0) on the branch;
    - sign of h at endpoints and of Phi - 1 (U').

## B2. What is certified so far
  Point-level tests: float vs exact-sympy agreement to 1e-39; P2 identity
  R1_b = -R2_a at the fp to ~2e-9 (finite differences).  The interval-Newton
  step fails at moderate box widths (e.g. da=1e-4, db=5e-3, dR=1e-3 R at R=4):
  the Newton quotient N = s - F/F_s on enclosures is wider than the enclosure
  (division-width blowup).  Recommended replacement (implemented but not tuned):
  sign-based certification - certify F(s0) excludes 0 and F_s has a fixed sign
  on an s-enclosure; monotonicity then yields existence + uniqueness.
  => The certified bulk (finite R-cells) is NOT yet achieved.

## B3. Certification plan (unchanged)
  Partition (1, inf) x I into R-cells x a-cells; per cell certify (E1) endpoints
  (1-D in R at certified branch endpoints), (P0) via certified G, (U') via
  certified sign of Phi-1 on an a-grid refined where the sign changes.  Tail
  covered by A3-A6 + Gap 1; boundary R -> 1+ by A9 (open).

================================================================================
PART C - NUMERICAL EVIDENCE (explicitly NOT proofs)
================================================================================

All values are float (numpy) or mpmath (20-40 digits); they are reproducible
from the scripts and data files in reproducibility/ (see repro_manifest.md).
No value in this part is used as a proof in Parts A or B.

## C1. Fixed-point asymptotics (verify_profile_asym.py)
  xi* = 0.119937215937 ;  alpha*^2 = 2/xi* = 16.67539124 ;  kappa* = 0.36946535
  R        (0.5-fp)*q      s1*sqrt(q)     (2 pi - s2)*q
  1e4      0.119396        4.067793       0.362716
  1e5      0.119766        4.078545       0.367323
  1e6      0.119883        4.081966       0.368787
  limits   xi*=0.119937    4.0835         0.3695

## C2. Branch profile at q = 1000 (verify_profile_asym.py; clean S3 trace)
  a<1/2 (P-):  sin(u) vs u sqrt(2a),  u = pi W/(1-a)
    a=0.45: 0.52710 vs 0.52669 ;  a=0.47: 0.42583 vs 0.42648
  a>1/2 (P+):  kappa^2 vs 1/(2 pi^2 (1-a) W^2)
    a=0.51: 0.9553 vs 0.9561 ;  a=0.55: 0.8775 vs 0.8780 ;  a=0.58: 0.8355 vs 0.8357
  ground state: s1 sqrt(q) = 1/sqrt(W a (1-a)) to 0.1% (a=0.43..0.58)

## C3. Endpoint h and G(fp) (tracew_*.json, fp_G_data.json)
  R        h(a0)*q     h(beta)*q    G(fp)
  1e3      -0.28883    +0.29623     1.446054
  1e4      -0.25606    +0.25801     1.421065
  1e5      -0.25002    +0.25062     1.413496
  1e6      -0.24826    +0.24846     1.411142
  1e8      ~-0.2476    ~+0.2476     1.410156
  limit from A3: -0.2474707, +0.2474707.  (The R=1e3 row is polluted by
  sheet-crossing; see C5.)

## C4. Shape facts
  - Phi-1: R=1000: no zeros, Phi-1 > 0 on [a0, beta]; R>=1500: exactly 2 zeros,
    pattern - + -, with left zero z0: (0.5-z0)q ~ 4.3 (q=70.7), 5.3 (q=100),
    10.5 (q=316), 20.0 (q=1000).  z0 -> 1/2 as q -> inf.  (C7)
  - Phi(a0)-1 = -0.000374 (q=1000), consistent with S(a0)/q = -0.3843/1000.
  - G: 0.9989 at a0, dips to 0.9988 near a~0.457, rises to 1.4111 at fp, then
    ~1.0007 on [0.51, beta].  G-1 = O(1/q) generically, O(1) on the layer.

## C5. Sheet structure (important caveat for data files)
  tracew_*.json rows for a > ~1/2 and near the diagonal are POLLUTED by sheet
  jumps (e.g. rows with W ~ 1.0-1.2 at a = 0.51 are NOT on S3).  The clean S3
  values used in C2/C3 were recomputed by targeted continuation in this run
  (scripts s33_profile.py); use tracew only for the left part a <= fp.

## C6. U' generic term S(a) = W'_L(a) + W'_R(1-a) (leading order; s33_e1.py)
  a        W'_L        W'_R(1-a)   S
  a0      -1.1154      0.7311     -0.3843
  0.43    -1.1320      0.7262     -0.4058
  0.45    -1.1996      0.7174     -0.4821
  0.47    -1.3748      0.7094     -0.6654
  0.48    -1.5802      0.7057     -0.8745
  0.49    -2.0908      0.7020     -1.3887   (edge of the layer; (P-) degrades)
  S < 0 on the whole generic left; matches q(Phi-1) to ~1% where (P-) holds.

## C7. Phi-1 zero motion (s33_zeros.py)
  R        q       left zero z0    (0.5-z0)q
  5000     70.7    0.4392          4.3
  10000    100.0   0.4468          5.3
  100000   316.2   0.4669          10.5
  1000000  1000.0  0.4800          20.0
  (0.5-z0) ~ c q^0.58; z0 -> 1/2 as q -> inf; by symmetry the right zero is
  u(z0) ~ 1 - z0.

## C8. R -> 1+ structure (s33_r1plus.py; replaces the old "limit curve" entry)
  REFUTED (F-016): the old claim "fp-component limit curve sin(2 pi b) =
  -sin(pi a)/2, slope 1/14" is false; see A9 for the refutation points.
  Verified structure at R = 1+eps: S3 is the sheet a = a0 + eps*phi(b) +
  O(eps^2) with phi from first-order perturbation theory (s33_r1plus.py):
    phi(a0) = 0 (exact), phi(b0) = 0.026021, phi' in (0.006, 0.428) on
    [a0, 0.98] (phi strictly increasing).
    g_1(a0) = a0 exactly (degenerate point (a0,a0) on the fp-component for
    small R; direct root-finding: R1(a0,.,R) has a unique root at b = a0 for
    R = 1.001..1.05).
    h(a0) = 2a0-1 + phi(b0)*eps + O(eps^2): -0.16052 (R=1.02), -0.15975
    (R=1.05) measured vs -0.16034, -0.15956 predicted.
    h(beta) -> b_top* - b0 > 0, b_top ~ 0.936 (R=1.02..1.1).
    Phi-1 > 0 and G > 0 on the whole domain for R <= 1000 (e15 data); margins
    for R <= 100: min Phi-1 >= +0.35, min G >= 2.1.
  Note: the e15 first-row b values for R <= 100 (constant 0.41939681) are an
  off-branch artifact of max_root_col; the h(a0), u(a0) values are still
  accurate because h(a0) = u(a0) - b0 (g_1(a0) = a0).

================================================================================
PART D - EXACT REMAINING GAP (honest)
================================================================================
1. G-EST (master gap): explicit uniform error bounds for A4/A5 (the displayed
   O-terms), with explicit q0 and constants, including the convergence rates of
   W(a0), W(1-a0), W, s1, s2, a_fp.  Elementary but long: implicit function
   theorem on the scaled exact equations (SEC)/(BR) + Lipschitz bounds on the
   explicit trig formulas.  Until this is written out, A3's corollary, A6's
   generic sign lemma, and A5's theorem are conditional.
2. U'-layer: the transition-layer single-crossing statement (A6); requires the
   layer profile W(xi) (two-sided balance) and the map xi -> xi_u.
3. R -> 1+ perturbation (A9): DONE (2026-08-09) - the closed form of phi(b)
   and factored phi'(b) are written out (DERIVATION, verified); phi' > 0 on
   [a0, 1) is CERTIFIED (mpmath.iv 200-bit, 4000-cell grid on [a0, 0.999],
   worst lower bound 8.896e-6) + STRICT (elementary tail bound C_tail >=
   9.651926 on (0.999, 1)); b_top* >= 7/10 > b0 is STRICT (implicit function
   theorem, structural).  REMAINING (Gap 1): explicit uniform O(eps) error
   bounds for A_eps - a0 - eps phi, b_top(eps), h, G, Phi, and an explicit
   upper bound b_top(eps) <= 1 - delta_0.  This closes E1, U', P0 for R in
   (1, 1+eps0).  The old "limit curve" formulation is refuted (F-016); the
   base facts are explicit (phi(a0) = 0, g_1(a0) = a0 for small R, h(a0) =
   2a0-1+phi(b0)eps + O(eps^2), h(beta) -> b_top* - b0).
4. Certified bulk: finite-R cells (Part B); engineering task with a concrete
   design and one known blocker (interval-Newton division-width).
5. Closed forms (not needed for C1): lim G(fp) ~ 1.41005 and the endpoint
   constant c ~ 0.24747 are numerically determined; exact expressions open.
