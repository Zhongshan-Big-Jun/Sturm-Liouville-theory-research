# Problem contract

Run: R-20260806T011500Z-keylemma-E58FB1
Task packet: agenda/task-packets/Q-20260806-keylemma-E58FB1.md (sha256 608d3e7d...4b78)
Authoritative source of the statement: runs/rigorous-open-math-research/
  R-20260805T000000Z-gapn1-a1b2c3/agentA_O2_single_crossing.md, Section 2.9 (KEY LEMMA),
  with derivation in Sections 2.1-2.8.  This contract is an independent normalization
  and audit of that statement; it supersedes the packet's "equivalent forms" claim where
  the audit found it incorrect (see Contract audit, item C1).

## Objects and definitions

Constants: q > 1 (q = sqrt(R), R = box bound); c in (0, 1/2) (phase ratio).

Phase curves (secular equations of the half-problem, Dirichlet string on [0,1/2]):
  even curve:  beta = E(alpha) := arctan(1/(q tan alpha)),  alpha in (0, pi/2);
  odd curve:   beta = O(alpha) := pi - arctan(q tan alpha) for alpha < pi/2,
               O(alpha) := arctan(-q tan alpha) for alpha > pi/2,  O(pi/2) := pi/2,
               alpha in (0, pi).
Both are strictly decreasing with slope -q/Phi(alpha), Phi(alpha) := cos^2 alpha + q^2 sin^2 alpha.

Intersections with the line beta = c alpha (unique for each c > 0):
  alpha_1(c) in (0, pi/2): E(alpha_1) = c alpha_1;    strictly decreasing in c.
  alpha_2(c) in (0, pi):   O(alpha_2) = c alpha_2;    strictly decreasing in c.
  For c in (0, 1/2):  alpha_0 < alpha_1(c) < pi/2 < alpha_2(c) < pi, where
  alpha_0 = alpha_1(1/2) = pi - alpha_2(1/2),  sin(alpha_0/2) = 1/sqrt(2(q+1)).
  Set gamma(c) := pi - alpha_2(c) in (0, alpha_0); gamma(c) < alpha_1(c) for c < 1/2.

Auxiliary functions:
  Phi(alpha) = cos^2 alpha + q^2 sin^2 alpha;
  W(alpha)   = 3 + 2 alpha cot alpha;
  M(alpha;c) = q(q^2-1) alpha^2 sin^2 alpha / (q + c Phi(alpha));   M_k(c) := M(alpha_k(c);c);
  Mtilde(alpha;c) = alpha^2 sin^2 alpha / (q + c Phi(alpha))  (= M/(q(q^2-1)));
  F(c)  = M_1(c) - M_2(c);   Ftilde(c) = Mtilde_1(c) - Mtilde_2(c) = F/(q(q^2-1));
  G(alpha;c) = (d/dc) log Mtilde(alpha(c);c) along either curve (both have slope -q/Phi)
             = -Phi(alpha) W(alpha)/(q + c Phi(alpha))
               + 2 c alpha Phi(alpha) (q^2-1) sin(alpha) cos(alpha) / (q + c Phi(alpha))^2;
  G_k(c) := G(alpha_k(c);c).

## Hypotheses

1. q > 1 (equivalently R > 1) and c in (0, 1/2).
2. alpha_1, alpha_2 are the unique intersections defined above (the corrected odd secular
   equation q tan(alpha_2) + tan(c alpha_2) = 0; the task's older product-of-tangents form
   is FALSE and is not used).
3. All quantities are real-analytic in (q, c) on (1, inf) x (0, 1/2).

## Target conclusion

KEY LEMMA (log form, as stated in the packet):
  (d/dc) log( M_1(c)/M_2(c) ) < 0  for all q > 1, c in (0, 1/2),
equivalently (verified identity)  G_1(c) < G_2(c)  for all q > 1, c in (0, 1/2).

Needed companion (form (i), required by the reduction T4 in the source to close O2):
  F'(c) < 0  for all q > 1, c in (0, 1/2),
equivalently (verified identity)  Ftilde'(c) = Mtilde_1 G_1 - Mtilde_2 G_2 < 0.

Consequence (if both hold; T1-T4 in the source then close):
  f_sym has exactly one zero u*(R) in (0, 1/2), f_sym < 0 on (0, u*), > 0 on (u*, 1/2);
  D_sym(u) = lambda_2 - lambda_1 strictly increases then decreases with unique maximizer u*.

## Quantifiers and dependency of constants

- All constants are absolute (no hidden dependence on q, c, R).  The conclusion must hold
  uniformly in q > 1 and c in (0, 1/2).
- The endpoint values at c -> 0+ and c -> 1/2- are included in the statement via limits:
  F(0+) = q(q^2-1) pi^2/4 > 0;  F(1/2) < 0 (from T2);  alpha_1 -> pi/2, alpha_2 -> pi as c -> 0+.

## Equivalent formulations that are actually proved equivalent (audited)

The following identities were re-derived and machine-verified to 50-60 digits:
  E1  (d/dc) log(M_1/M_2) = G_1 - G_2.                                   [P8 PASS]
  E2  Ftilde' = Mtilde_1 G_1 - Mtilde_2 G_2.                            [P9a PASS]
  E3  D'(c) = (8/q^2)(c+q) F(c);   f_sym = 2(c+q) F/(q u^2 (q^2-1));     [P5, P7 PASS]
  E4  (N) u_k(u,u)^2 = tan^2(alpha_k)/(1/2 + w tan^2 alpha_k), w = u + R(1/2-u).  [P3 PASS]
  E5  (F1) f_sym = (2/u^2)(T_1 - T_2).                                  [P4 PASS]
  E6  alpha_1(1/2) = alpha_0 = 2 arcsin(1/sqrt(2(q+1))), alpha_2(1/2) = pi - alpha_0.
  E7  H(q,1/2) := G_2(1/2) - G_1(1/2) = 2 pi q (q+1) / (2q+1)^(3/2).    [derived exactly, verified 1e-25]

AUDIT FINDING C1 (inequivalence of the source's "equivalent forms"):
  The source claims (d/dc)log(M_1/M_2) < 0  <=>  F'(c) < 0.  This is FALSE as a matter of
  logic:  F' = M_1 G_1 - M_2 G_2 = M_1 M_2 (G_1/M_2 - G_2/M_1), which is not proportional
  to G_1 - G_2.  Both inequalities are numerically true on the whole domain, but each needs
  its own proof.  This run proves both (log form and F'-form); the F'-form is the one that
  the source's T4 actually consumes, so closing it repairs the reduction.

## Boundary and degenerate cases

- c -> 0+: alpha_1 -> pi/2, alpha_2 -> pi; F(0+) > 0; H -> +infinity; Ftilde' -> -3 pi^2/4 < 0.
- c -> 1/2-: alpha_1 = gamma -> alpha_0, alpha_2 -> pi - alpha_0; all quantities have exact
  closed forms on the boundary c = 1/2 (E7 and the explicit G_1, G_2, Mtilde_1, Mtilde_2).
- q -> 1+ (R -> 1+): alpha_1 = pi/(2(1+c)), alpha_2 = pi/(1+c), Phi = 1, G = -W/(1+c);
  q = 1 is a degenerate limit (M = 0) handled by rescaling with Mtilde.
- q -> inf: alpha_1 ~ 1/sqrt(q c), alpha_2 ~ pi - tan(c pi)/q.
- Region B (where G_2 < 0) is nonempty only for q in (1, q*), q* in (1.85, 1.9), and is a
  thin strip c in (c_G2(q), 1/2).  Outside Region B, G_2 >= 0 and both target inequalities
  follow from G_1 < 0 (Lemma G1, proved below).

## Permitted outcomes

- affirmative proof of both the log form and the F'-form (closes O2);
- negative proof / counterexample (with certificate);
- rigorous partial result (reduction to a strictly smaller core) with exact remaining gap.

## Completion criteria

1. Prove (d/dc) log(M_1/M_2) < 0 on (1, inf) x (0, 1/2), and
2. Prove F'(c) < 0 on (1, inf) x (0, 1/2) (so that T1-T4 in the source close O2), or
   prove a strictly smaller equivalent core and repair T4 accordingly.
3. Every cited premise rechecked (see repro_manifest and the premise audit).
4. Adversarial audit of the final proof with verdict PASS / REPAIRABLE_GAP / FATAL_GAP etc.

## Results that do not count as completion

- Numerical verification alone (recorded separately in the ledger and reproducibility/).
- A proof of only one of the two forms, unless the T4 chain is explicitly repaired and the
  remaining implication is proved.
- Bounds valid only on a subset of the parameter domain unless the complement is closed.

## Tool, citation, and search constraints

- All claims must be externally checkable; computations recorded with exact commands.
- Python 3.10 (C:\Users\HuangZY\AppData\Local\Programs\Python\Python310\python.exe),
  numpy 2.2.6, scipy 1.15.3, mpmath 1.3.0, sympy 1.13.1.
- No use of manage-math-research-program inside this run (upstream constraint).
- Literature premises (Feynman-Hellmann, Wronskian monotonicity, AEH Lemma 2.2) are
  background; the KEY LEMMA itself is project-derived and must be proved from first
  principles (no external theorem can be cited for it).

## Ambiguities or competing interpretations

- A1  The packet states the KEY LEMMA in log form and claims F' < 0 is an equivalent form.
      The audit shows they are not equivalent; this run proves both, and the F'-form is the
      operative one for T4 (see C1).
- A2  The normalization convention for the eigenfunctions switches between y = sin(sx)
      (secular equations) and y = sin(sx)/s (identity (N), y'(0) = 1).  Both conventions are
      used consistently within their own derivations; (N) was re-verified with the y'(0)=1
      convention (P3 PASS at 1e-55).
- A3  The odd secular equation: the packet's "Known facts 2" product form is false; the
      corrected form q tan(alpha_2) + tan(c alpha_2) = 0 is used throughout (P1 PASS).

## Contract audit

- Conducted by the coordinator (this run) against the task packet and the source report.
- The source report's own correction list (Section 3) was re-checked and reproduced:
  odd secular equation, zero condition sqrt(N2) sin(a1) = sqrt(N1) sin(a2), f_sym(1/2) = 2 pi^2,
  u*(4) = 0.45148546584, D*(4) = 32.6139836177.
- Finding C1 (non-equivalence of the two "equivalent forms") is new to this run and is the
  only substantive correction to the source's write-up.
- Status of this contract: normalized independently; matches the source statement modulo C1.
