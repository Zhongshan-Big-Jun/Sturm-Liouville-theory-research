# Research ledger

Run: R-20260806T011500Z-keylemma-E58FB1
Format: chronological entries; every substantial computation / proof attempt / route
decision / failure mechanism is recorded.  Status labels at the end.

## 2026-08-06 (continuation of the run)

### L01 Contract and premise audit
- Re-read the task packet, the source report (agentA_O2_single_crossing.md, Sections
  2.1-2.9), the skill workflow, and the inherited artifacts (problem_contract.md,
  obligation_graph.md, run-manifest.json).
- Finding C1 (inherited but re-confirmed): the source's claim that the log form and F' < 0
  are "equivalent forms" is FALSE as a matter of logic (F' = M1G1 - M2G2 is not
  proportional to G1 - G2).  Both are true numerically; each needs its own proof.  T4 only
  consumes F' < 0, so closing the F~' form repairs the reduction.
- Re-ran verify_premises.py (60-digit): P1-P8, P9a, P10 pass; P9a has one tolerance flag
  at (q=10, c=0.05): central finite difference differs from M1G1-M2G2 by 2.7e-7 on a
  ~1386-magnitude derivative.  Confirmed artifact (truncation error), not a formula
  failure: the identity was verified to 1e-12 via debug_Fpp.py's first-difference check.

### L02 Reproducibility runs
- q1_analysis.py: PASS.  P(u)-P(2u) >= 1.5485 on (pi/3, pi/2); H(1,c) decreasing; corner
  4*pi/(3*sqrt 3) = 2.41840.
- verify_q1_forms2.py: PASS (J1 = N1/(1+c)^2, J2 = N2/(1+c)^2, H' = (T(2u)-T(u))/(1+c)^2).
- verify_Fp12.py: PASS (closed form F~'(q,1/2) matches to 1e-13; P(x) > 0).
- regionB.py: PASS except its q* bisection prints "q* = 2.0" due to an inverted update
  (lo := mid when G2(mid) > 0).  The printed G2 values give the true root q* ~ 1.855.
  Recorded as a cosmetic script bug (does not affect the math).
- qmono_box.py: margins dJ1/dq >= 4.866, dJ2/dq <= -2.765, dH'/dq <= -9.552.
- global_min_Fp.py: min(-F~') = 0.425342 at (q ~ 3.120, c ~ 0.4999) on q <= 100.  NOTE: at larger q the margin shrinks toward 0 (e.g. F~'(10000, 0.230) = -1.79e-10); the inequality is still true there via region A (R1 + L1 + L2), and the 0.4253 number is NOT used in the proof.
- debug_Fpp.py: confirms d(M1G1)/dc = M1J1 (3.7013974647 vs 3.7013974644) and
  dFp/dc = M1J1 - M2J2 (17.75350148) at (q=1.3, c=0.49).  The identity F~'' = M1J1-M2J2
  holds; check_Fpp.py's second-difference column is numerically unreliable.

### L03 Failure: second-difference Fpp (check_Fpp.py)
- Mechanism: (Fp(c+h) - 2Fp(c) + Fp(c-h))/h^2 with Fp evaluated via brentq root solving;
  root noise ~1e-12 in alpha amplifies to O(100) errors in the second difference.
- Lesson: never certify second derivatives of implicitly-defined functions via finite
  differences of root-solved values; use the exact identity (chain-rule form) instead.
- Recorded: check_Fpp.py flagged as unreliable as written; debug_Fpp.py is the valid check.

### L04 Global sign structure (new scan)
- global_scan.py over q in {1.01..1000}, c in (0.001, 0.499): H >= 2.4377 everywhere;
  H' > 0 and F~'' < 0 occur only in Region A (e.g., q=30, c=0.33: H' = +4.27; q=1.01,
  c=0.001: F~'' = -168).  Since Region A has G2 >= 0, these do not threaten the proof.
- Conclusion: the region split is necessary; Region B is the only place requiring the
  box machinery.

### L05 R1/R2 margin quantification
- r1r2_margins.py: min G2 over {q >= 2} = 0.070593 at (2, 0.4999); min G2 over
  {c <= 0.4} = 0.415004 at (q -> 1+, 0.4).
- G2 c-structure (G2c_struct.py): for q = 2, G2 decreasing in c (min at c=1/2); for
  q >= ~30, G2 has a shallow interior minimum near c ~ 0.25 with value >= 12.37; the
  global min over q >= 2 is at (2, 1/2).
- dG2/dq >= 0 on the whole sampled domain (G2qmono.py, dG2dq_stress.py): min ~5.0e-4 at
  (q=100, c small), ~5e-12 at (q=1e6, c=0.0125), consistent with G2(c;q) -> 4*pi/sin(2 pi c)
  for fixed c < 1/2 (dG2/dq ~ O(1/q^2)).

### L06 Failure: extended-box q-monotonicity of B (Bmono.py)
- Hypothesis "B(gamma;q) increasing in q on gamma in (0, alpha0(2)]" is FALSE: at
  (q=100, gamma=0.837) B is hugely negative (-11091).  The gamma-range depends on q
  (gamma <= alpha0(q)); the extended box includes spurious points.  Lesson: respect the
  per-q domain (gamma <= alpha0(q)) when comparing across q.

### L07 Failure: corner-envelope bound (corner_envelope.py)
- Hypothesis "B(gamma;q) >= B(gamma; q(gamma))" (q(gamma) solving alpha0(q)=gamma) is
  FALSE (large negative differences at q=1000, small gamma).  Discarded.

### L08 Failure: crude tail bounds for R1 (r1_tail.py, hand analysis)
- Bounds A >= A(alpha0), T <= min(q tan gamma, pi/2), sin cos <= gamma, q + c Phi >= q
  all individually fail to prove B >= 0 near (2, 1/2); the naive "tail" bound L(q) < 0
  for all q.  Lesson: the corner is genuinely delicate (only ~8% slack in B at (2,1/2));
  a proof must reproduce the exact c=1/2 balance.

### L09 Corner asymptotics (asym_corner.py, hand analysis)
- Corrected an earlier wrong guess: G2(1/2; q) ~ (pi/sqrt 2) sqrt q -> inf as q -> inf
  (not 0).  The previous confusion came from wrongly estimating Phi ~ 3 instead of
  Phi ~ 2q at gamma = alpha0(q) ~ sqrt 2 / sqrt q.  With the right size, the corner
  balance B ~ (pi sqrt 2) q^(3/2) > 0 with positive margin.
- Fixed-c limit: G2(c; q) -> 4*pi/sin(2 pi c) for c < 1/2.
- Lesson: asymptotic size estimates must be recomputed numerically before trusting them.

### L10 Exact corner forms (corner_exact.py, corner_Fp12b.py)
- H(q,1/2) = 2 pi q (q+1)/(2q+1)^(3/2) (sympy-exact; increasing in q; min 4pi/(3sqrt3)).
- F~'(q,1/2) = 2 pi (cos x - 1)^3 P(x)/sin^3 x with x = alpha0, P(x) = 3x^2 + 6x sin x
  - 3 pi x - 3 pi sin x + pi^2; P(x) - (pi - 3x)^2 = 3(x - sin x)(pi - 2x) > 0, so
  F~'(q,1/2) < 0 for all q > 1.  (B4, B5 closed.)

### L11 Box lemmas supersede R4-R6 (box_Hp_Fpp.py, box2.py, box_margins2.py)
- On the whole box (1,2] x [0.4, 0.5]: H' <= -7.73 (max at q=1.05, c=0.5) and
  F~'' = M1t J1 - M2t J2 >= 14.17 (min at q=2, c=0.5).  No violations.
- Consequence: the q-monotonicity obligations R4-R6 are unnecessary; L4box/L5box hold
  directly on a superset of Region B.  obligation_graph.md updated accordingly.
- First box scan mistakenly included q up to 3.0 (qi/20 for qi in 1..40); corrected to
  q in (1,2] (qi in 1..20).  The erroneous scan's Fpp column also used the unreliable
  second difference; the corrected scan uses the identity form.

### L12 Analytic proofs completed
- L1 (G1 < 0): via (q^2-1) sin a1 cos a1 <= Phi1 cot a1 (equivalent to sin^2 + cos^2 = 1),
  the cross term is < 2 a1 cot a1 (q + c Phi1)-scaled, so W1(q + c Phi1) > RHS.
- B1 (N1 > 0 on (pi/3, pi/2)): W >= 3 and uW' >= -2 u^2 csc^2 u >= -2(pi/2)^2(4/3), so
  N1 >= 12 - 2 pi^2/3 > 0.
- B2 (N2 < 0 on [2pi/3, 5pi/7]): N2 = (W-1)(W+3) - 2 w^2 csc^2 w, with
  W in [3 - 4pi/(3 sqrt3), 3 - (10 pi/7) cot(2 pi/7)] subset (-1, 1).
- B3 (T decreasing on (0, pi)): T' = 4[cot - 2u csc^2 + u^2 csc^2 cot]; sign via
  N~ = cos u sin^2 u + u^2 cos u - 2u sin u <= 0 (on (pi/2, pi) trivial; on (0, pi/2)
  divide by cos: 2u tan u >= u^2 + sin^2 u since tan u >= u).
- B7 (G2(c;1) > 0 for c <= 0.4): W(pi/(1+c)) <= W(5pi/7) < 0 (W decreasing on (pi/2, pi);
  W(5pi/7) = 3 - (10pi/7) cot(2pi/7) < 0 since cot(2pi/7) > 21/(10 pi)).
- B6 (G2(c;2) >= 0): numerically verified; proof open (would need G2 decreasing in c at
  q=2 plus the exact corner value G2(1/2;2) = 0.0691814...).

### L13 Final margin tables (final_margins.py, box_margins2.py)
- R1 grid min G2 = 0.070593 at (2, 0.4999); R2 grid min = 0.415005 at (1.001, 0.3999);
  L4box max H' = -7.7317; L5box min F~'' = 14.167.
- q -> 1+ boundary: H' <= -7.12, F~'' >= 17.79 on c in [0.4, 0.5].

### L14 Route decisions
- Route B (R4-R6) SUPERSEDED by L4box/L5box (L11).
- Route C (dG2/dq >= 0) ACTIVE as the recommended linchpin for R1/R2 (verified, unproved).
- Route G (sound interval certificate) recorded as the only known path to a full
  computational proof; not pursued (soundness engineering cost).
- The run closes with status RIGOROUS_PARTIAL_RESULT (see status_and_literature.md and
  audit_report.md).

## Failure / lesson summary
1. Second differences of root-solved functions are unreliable (L03).
2. Per-q domains must be respected in monotonicity comparisons (L06).
3. Corner inequalities can be delicate; exact boundary balance required (L08, L09).
4. Asymptotic size estimates must be checked numerically (L09).
5. Check target signs on the full superset box before adding structural lemmas (L11).
6. Symbolic derivatives of G2 in (gamma, q) do not factor usefully (L14, sym_dG2dq.py);
   a variable change (y = q tan gamma) is the natural next step.

## Inherited failures (recorded by the earlier segment, re-confirmed)
- O_curve at alpha = pi/2 must be special-cased (tan(pi/2) blowup).
- Normalization identity needs the y = sin(sx)/s (y'(0)=1) convention.
- dG/dq needs Phi's q-derivative (Phi_q = 2q sin^2 a).
- F~' is not monotone in q (counterexample: -F~' is smaller for larger q at small c).
- B-D (itemwise q-monotonicity of the decomposition G2-G1 = (A-C)+(B-D)) is FALSE
  (c=0.01, q 5000 -> 20000: 199.79 -> 193.99).
- G2 is not monotone in c globally (q=100 has an interior minimum at c ~ 0.25).
- J is not monotone in alpha globally.
- The two "equivalent forms" are not logically equivalent (C1).

### L15 Large-q margin behavior of F~' (new finding during final check)
- final_check.py found min(-F~') = 1.79e-10 at (q=10000, c=0.230): F~' is negative but the
  margin shrinks toward 0 for large q because M~ ~ 1/q^3 there.  This does NOT threaten
  the proof: for q >= 2, R1 + L1 + L2 (region A) give F~' < 0 without any margin.  The
  often-quoted "global margin 0.4253" applies only to the bounded sampled range q <= 100
  and is not used in the proof.  All artifact mentions of that number were corrected to
  say "bounded sampled range (q <= 100)".
- Lesson: quoted margins must state their q-range; asymptotic regimes can have margins
  that vanish while the proof mechanism (region split) still applies.
