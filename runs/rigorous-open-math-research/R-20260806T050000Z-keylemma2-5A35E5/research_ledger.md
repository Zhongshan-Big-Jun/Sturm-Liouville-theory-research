# Research ledger

Run: R-20260806T050000Z-keylemma2-5A35E5
Problem: close R1, R2, L4box, L5box (KEY LEMMA four-lemma reduction)
Priority: Q1 and R1 first, then R2, L4box, L5box.

All timestamps approximate (wall-clock tracked per entry).  ASCII punctuation only.

## 2026-08-06 (handoff entries, from the predecessor model)

- Read task packet Q-20260806-keylemma2-5A35E5 and the parent run
  R-20260806T011500Z-keylemma-E58FB1 (candidate_proof.md, audit_report.md).
- Re-derived the normalized contract (problem_contract.md); confirmed the odd secular
  equation is q tan(alpha2) + tan(c alpha2) = 0 (packet product-of-tangents form is
  FALSE); confirmed the C1 finding ((LOG) and (FP) forms are not logically equivalent).
- Built independent mpmath core (kl2_lib.py), interval engine riarith.py (outward
  rounding, Decimal, certified sin/cos/atan/pi), rigorous box machinery (rigorous.py:
  iv_Phi, iv_W, iv_G, iv_dGdc, secular bracketing, alpha1_box, alpha2_box).
- Cross-checks: E1/E2/dGdc/E8/Hp/J margins all REAL identities pass.  L4box max
  -7.731744 at (1.05, 0.5); L5box min 14.167117 at (2.0, 0.5); R1 min 0.069181445 at
  (2, 1/2); R2 min ~0.415 (grid) near (1+, 0.4).  All four margins re-confirmed.

## 2026-08-06 (this session, entry 1): fixed dG2/dq closed-form bug

- verify_dG2dq_formula.py FAILED with relative errors up to 767x.
- Root cause found by hand derivation: in Gq_formula (partial G / partial q at fixed a),
  term t1 = -Ph_q*W/D + Ph*W*c*Ph_q/D^2 missed the q-derivative of D = q + c*Phi, i.e.
  the "+1" term.  Correct: t1 = -Ph_q*W/D + Ph*W*(1 + c*Ph_q)/D^2.
- After fix, all six test points agree with central finite differences to ~1e-13 rel
  (50 digits, h = 1e-6 q).  Script updated with the correction comment.
- Lesson: always write d/dq[1/D] with D = q + c*Phi; the explicit q in D is easy to drop.

## 2026-08-06 (this session, entry 2): global sign survey

- dG2/dc (J2) is NOT negative globally: positive at q=30..100 for c in (0.3, 0.45).
  So the "R1 via dG2/dc <= 0 + corner" route fails globally.
- dG1/dc (J1) is negative only for small q and small c; positive on the box (1,2]x[0.4,0.5].
- G2(1/2;q) increasing in q on the sampled grid: -0.388 (q=1), 0.069 (q=2), 18.29 (q=100).
- dG2/dgamma < 0 on the FULL gamma range (0, alpha0(q)) for q in (1,10] (min -8330 at
  small gamma).  Since dgamma/dc > 0, this gives dG2/dc < 0 for q <= 10, c in (0,1/2).
- dG1/dx is NOT negative globally (max +1.9 at q=2, x=1.55) but that x is outside the
  box range [alpha1(0.5), alpha1(0.4)] = [0.841, 0.93] for q=2.
- Tail fit: G2(c;q) = 4pi/sin(2pi c) + K(c)/q + M(c)/q^2 + ..., K(c) < 0 always;
  M(c) < 0 for c <= 0.1, > 0 for c >= 0.2, huge near c = 1/2 (M(0.49) ~ 5.4e8).
  The 1/q series is NOT a clean power series near c = 1/2 (fit does not converge).
- dG2/dq table: positive everywhere sampled; decays like |K(c)|/q^2; min over the
  table 5.01e-10 at (q=1e5, c=0.01).  This confirms Q1's tail is the hard part.

## 2026-08-06 (this session, entry 3): (q,u) reformulation -- R1/R2 collapse

KEY DISCOVERY:  parametrize the odd curve by u := q*tan(gamma) = tan(c*alpha2)
(gamma = pi - alpha2).  Then:

- The c = 1/2 boundary is exactly u = sqrt(2q+1)  (verified to 15+ digits for q in
  [1.01, 100]; proved: at c=1/2, u = q tan(alpha0) = sqrt(2q+1)).
- G2 >= 0  <=>  IN(q,u) >= 0, where with A := alpha2 = pi - arctan(u/q):
    IN = (q^2+u^2)*A*(2*A*q - 3*u + 2*arctan(u)) - 3*u*q*(1+u^2)*arctan(u).
  200 random points: 0 sign mismatches.  Sign(IN) = sign(G2) (IN = G2 * positive factor).
- F(q;u) := IN(q,u) is increasing in q at fixed u.  Exact formula verified at 1e-13:
    dF/dq = 6A^2 q^2 + 2A^2 u^2 - 2A q u + 4A q arctan(u) - 3u^2 - u(1+3u^2) arctan(u).
  Numerically dF/dq > 0 on the whole domain D = {(q,u): q>1, 0<u<sqrt(2q+1)}, min ~27.02
  at the corner (q->1+, c->1/2-), i.e. (q,u)->(1, sqrt(3)).
- dIN/du < 0 on D (4760 samples, 0 positive; formula verified at 1e-13):
    dIN/du = 4A^2 u q - 4A q^2 - 6A u^2 - A(q^2+u^2)(1+3u^2)/(1+u^2)
             + arctan(u)(4A u - 5q - 9q u^2).
  Margin: max (closest to zero) -5.96 at (q->1+, u ~ 0.52).
- R1 region (q>=2, c in (0,1/2)) = {(q,u): q>=2, 0<u<sqrt(2q+1)}.
  R2 region (q>1, c<=0.4) = {(q,u): q>1, 0<u<u_max(q)}, u_max(q) the c=0.4 curve.
- Boundary survey (IN minima, fine grids):
    q=2 curve:     min 6.6727 at u=sqrt(5)   [corner (2,1/2)]
    corner curve:  min 6.6727 at q=2
    q=1 curve:     min 5.8680 at u=tan(0.4*pi/1.4)=1.25396  [corner (1,0.4)]
    c=0.4 curve:   min 5.8709 at q->1+
  All boundary minima sit at the rectangle corners (q,c) in {1,2} x {0.4,1/2}.
- REDUCTION: with M1 (dIN/dq > 0 on D) and M2 (dIN/du < 0 on D):
    R1  <=  M1 ^ M2 ^ IN(2,sqrt5) > 0 ^ [corner curve IN(q,sqrt(2q+1)) >= 0 for q>=2]
            (corner curve <=> G2(1/2;q) >= 0, single-variable closed form)
    R2  <=  M1 ^ M2 ^ [q=1 curve IN(1,u) >= 0 for u in (0, tan(2pi/7))]
            ^ [c=0.4 curve IN >= 0 for q >= 1]
  The q=1 curve is covered by IN(1,1.25396) = 5.868 > 0 (single point) + M2.
  Exact corner values: G2(1/2;2) = 0.0691814447546..., G2(0.4;1) = 0.4136087142...
  (NOTE: the packet/parent "R2 slack 0.415004" is a grid min; the exact q=1 value is
  0.4136087; the difference is resolved by evaluating at q=1 exactly.)
- L4box/L5box unchanged: box (1,2]x[0.4,0.5], margins -7.73 / +14.17.

## 2026-08-06 (this session, entry 4): plan for the remaining work

- Primary route: prove M1 and M2 analytically (margins 27 / 5.96 in derivative units);
  if that stalls, certify by outward-rounded interval arithmetic on a compact exhaustion
  plus an analytic tail estimate (crude bound gives dF/dq > 0 for q >= 12; interval box
  covers q in [1, 12]).
- Boundary lemmas (1-variable):
    B6u: IN(2,u) >= 0 for u in (0,sqrt5)  [<=> G2(c;2) >= 0]
    Corner: G2(1/2;q) >= 0 for q >= 2  [closed form]
    B7u: IN(1,u) >= 0 for u in (0, tan(2pi/7))  [<=> G2(c;1) >= 0, parent B7]
    C4: G2(0.4;q) >= 0 for q >= 1  [new 1-variable curve]
- Q1 (dG2/dq >= 0) is NOT needed if M1/M2 route closes; Q1 remains as a fallback route.
- L4box/L5box: interval-certificate route (margins 7.7/14.2) or direct estimates.

## 2026-08-06 (this session, entry 5): M2 collapse and final reduction

- Independently re-derived and machine-verified (1e-35) IN = G2 * POS with
  POS = D^2*A*(q^2+u^2)*u/(Ph*q) > 0 (D = q + c*Ph).  Sign(IN) = Sign(G2) exactly.
- Hand-derived dIN/du formula (4A^2uq - 7Aq^2 - 9Au^2 + 2A(q^2+u^2)/(1+u^2)
  + t(4Au - 5q - 9qu^2)) verified vs central FD at 1e-14.  NOTE: the ledger
  entry-3 transcription of M2 differs; the formula here is the verified one.
- KEY: M2(1,u) = pi*(4u(pi - atan u) - 5 - 9u^2) EXACTLY (1e-51).
- KEY: dM2/dq < 0 on D (fine scans to q=2000, u<sqrt(2q+1), max -12.687 at
  (q->1+, u~0.87); no violations).  Formula verified vs FD at 1e-12
  (note the +4Aq/(1+u^2) term from d/dq[2A(q^2+u^2)/(1+u^2)]).
- CONSEQUENCE: M2 < 0 on D  <=  (dM2/dq < 0 on D) ^ (h(u)<0 for all u>0),
  h(u) = 4u(pi - atan u) - 5 - 9u^2.  h is concave (h'' = -8/(1+u^2)^2 - 18
  < 0), h'(0.5) > 0, h'(0.53) < 0, so max at u* in (0.5,0.53) with
  h(u*) = 9u*^2 + 4u*^2/(1+u*^2) - 5 <= -1.35 < 0.  ANALYTIC.
- REDUCTION IMPROVEMENT: R1 <= M2 ^ CORNER and R2 <= M2 ^ C4; M1 no longer
  needed.  (R1 region q>=2: IN(q,u) >= IN(q,sqrt(2q+1)) by M2; CORNER gives
  IN >= 0.  R2 region: IN(q,u) >= IN(q,u_max(q)) by M2; C4 gives >= 0.)
- CORNER closed form: G2(1/2;q) >= 0 for q >= 2  <=>  pi > arccos(2/3)+sqrt(5)
  (equiv. (pi-x) >= 3 sin x at x = arccos(2/3)); elementary certificate:
  cos(sqrt5) > -2/3 via y = pi - sqrt5 < 0.906 and cos y <= 1 - y^2/2 + y^4/24
  <= 0.6177 < 2/3.  ANALYTIC (verified numerically).
- C4: on the c=0.4 curve parametrized by v = arctan(u) in [2pi/7, 2pi/5),
  q = tan v / tan(pi - 2.5v), A = 2.5v:  IN = A*K(v) with
  K(v) = (q^2+u^2)(5 v q - 3 u + 2 v) - 1.2 u q (1+u^2).  K increasing
  (min slope 88), min K = 2.615 at v = 2pi/7 (q=1).  K(2pi/7) = 2.615 > 0.
  (Earlier L(v) transcription in entry 3 had a factor slip; corrected here.)
- M1 (dIN/dq > 0) also has clean structure: dM1/du < 0 on D (no violations,
  min -69791), m(q) = M1(q,sqrt(2q+1)) increasing, min 27.05 at q->1+.
  M1 NOT needed on the current route; recorded for completeness.
- L4box/L5box margins re-confirmed: max Hp = -7.7317 at (1.05,0.5); min
  Fpp = 14.167 at (2.0,0.5).

## 2026-08-06 (this session, entry 6): tail bound for dM2/dq < 0

- Elementary upper bound B(q) for dM2/dq valid on q >= 1 (all u in (0,sqrt(2q+1))):
    B(q) = (4 pi^2 + 14) sqrt(2q+1) + 8 pi (2q+1)/q + 1 + 2 pi (2q+1)/q^2 - 10 pi q.
  Uses: A <= pi, A >= pi - atan(sqrt(2q+1)/q) >= pi - sqrt(2q+1)/q, t <= pi/2,
  u <= sqrt(2q+1), 2u/(1+u^2) <= 1, S >= q^2, (q^2+u^2)/(1+u^2) <= q^2.
- B(20) = -232.7 < 0 and B strictly decreasing for q >= 20, hence
  dM2/dq < 0 for all q >= 20 (pure elementary).  Compact (1,20)x(0,sqrt(41))
  will be closed by certified interval arithmetic.
- TO DO: interval certificate dM2/dq < 0 on (1,20)x(0,sqrt(41)); C4
  certificate/tail; L4box/L5box box certificates; assemble candidate_proof.md.
