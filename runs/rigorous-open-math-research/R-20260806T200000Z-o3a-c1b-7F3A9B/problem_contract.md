# Problem contract: O3a/C1 (unique zero of h = g1 - g2; uniqueness up to reflection of the sign-consistent critical point)

## 0. Provenance (Phase 0 summary)

Task packet: agenda/task-packets/Q-20260806-o3a-c1b-7F3A9B.md (2026-08-06, task state DRAFT).
Portfolio problem: O-2026-SL-GAP-3B7A2C (n=1 adjacent-gap extremals, box class).
Obligation: O3a (uniqueness up to reflection of the sign-consistent critical point of
D = lambda_2 - lambda_1 over the barrier family).  The packet delegates the proof of
Conjecture C1 as stated in
runs/rigorous-open-math-research/R-20260806T140000Z-o3ac1-42F931/candidate_proof.md
(Lemmas R1-R6 PROVED, C1 OPEN reduced to E1 + M + Z), with gaps G-E1/G-M/G-C/G-Z/G-N in
the same run's audit_report.md, and the origin of C1 in
runs/rigorous-open-math-research/R-20260806T011500Z-o3abranch-E8E56F/candidate_proof.md
(P1-P4, CE-1 refuting Lemma A) and the T1-T4 chain in
runs/rigorous-open-math-research/R-20260805T000000Z-gapn1-a1b2c3/agentB_O3a_fixed_point.md.

Per the packet, this contract is written independently: the packet is project context,
NOT a verified theorem contract.  Every premise is re-derived or re-verified against the
cited source versions and first principles in this run.  No premise from the prior runs
is accepted without recheck.

## 1. Objects and definitions (independently normalized)

Fix R > 1.  Dirichlet vibrating string on [0,1]:

    -y''(x) = lambda rho(x) y(x),  y(0) = y(1) = 0,
    rho_(a,b)(x) = R on (a,b), 1 otherwise, 0 < a < b < 1.

Let 0 < lambda_1 < lambda_2 be the two smallest eigenvalues (simple by standard SL
theory for positive bounded weights).  s_k = sqrt(lambda_k).  Slope normalization:
y_k(0) = 0, y_k'(0) = 1.  (The prose "y_k(0) = 1" in the 2026-08-05 run is a known typo;
all invariant objects below are normalization-invariant.)  u_k = y_k / ||y_k||_{L^2(rho)},
n_k = ||y_k||_{L^2(rho)}^2.  Define

    f(x; a, b) = lambda_1 u_1(x)^2 - lambda_2 u_2(x)^2,
    R1(a,b) = f(a; a,b),   R2(a,b) = f(b; a,b),
    v(x; a, b) = y_2(x; a, b)/y_1(x; a, b),   q(a,b) = (s_1/s_2) sqrt(n_2/n_1).

Known structure (re-verified in this run, see status_and_literature.md and the audit):
v is strictly decreasing on (0,1), v(0+) = 1, v(1-) = c_v < 0; f has at most two zeros
x_- < x_+ with v(x_-) = q > 0, v(x_+) = -q; {f > 0} = (x_-, x_+) is a single interval.

Good root (sign-consistent critical point, equivalently fixed point of T = (x_-, x_+)):
pair (a,b), 0 < a < b < 1, with R1(a,b) = R2(a,b) = 0 and a = x_-(a,b), b = x_+(a,b)
(equivalently v(a) = q > 0, v(b) = -q < 0, a < z_0 < b where z_0 = v^{-1}(0)).

Branches (main sheets, defined by continuation from the R = 1 degenerate limits:
Gamma_1 through (a0, a0), Gamma_2 through (b0, b0)):

    Gamma_1 = {(a, g1(a)) : a in I_1},  I_1 = [a0, a_max1(R)]  (R1 = 0, a = x_-),
    Gamma_2 = {(a, g2(a)) : a in I_2},  I_2 = [1 - g1(a_max1), b0]  (R2 = 0, b = x_+).

Common range I = I_1 cap I_2 = [a0, beta],  beta = min(a_max1(R), b0).
Constants: a0 = arccos(1/4)/pi ~ 0.4195694, b0 = 1 - a0 ~ 0.5804305.
h(a) = g1(a) - g2(a) on I.  a_fp(R): the symmetric fixed point (a_fp, 1 - a_fp).

## 2. Hypotheses

H1. R > 1 fixed but arbitrary.
H2. (Branch structure, prior-run Lemma C, OPEN as a premise) Gamma_1 and Gamma_2 are
     each single connected curves, graphs over I_1, I_2, with g1, g2 real-analytic on
     the interiors, g1' > 0 on I; I = [a0, beta] nonempty; the symmetric fixed point
     lies in I when it exists.  Status: numerically verified; multi-sheet hazards
     documented (CE-1 note, R-104/105); PROOF OPEN.  Any theorem of this run that uses
     H2 states it explicitly.
H3. All quantities are evaluated on the main sheets (fixed-point-relevant components
     through (a0, a0) and (b0, b0)); extra R2 = 0 sheets at large R are NOT sign-
     consistent fixed points (v(a) < 0 there), hence irrelevant to O3a.
H4. O2 (existence of the symmetric fixed point) is assumed available from the portfolio
     chain; C1 uses it only through (Z) h(fp) = 0 and the final "the zero equals fp".

## 3. Target conclusion (Conjecture C1, exact statement)

For every R > 1: h = g1 - g2 has exactly one zero in the common range I = [a0, beta],
namely the symmetric fixed point a_fp(R).  Equivalently (given T1, T2 and O2): O3a
holds, i.e. the sign-consistent critical point of D = lambda_2 - lambda_1 over the
barrier family is unique up to reflection (and hence, being unique, symmetric).

## 4. Quantifiers and dependency of constants

All constants (branch ranges, slopes, the fixed point) depend on R.  No uniform-in-R
bound is required for C1 itself.  The zero of h must be a_fp(R) exactly.

## 5. Equivalent formulations proved equivalent (re-verified in this run)

T1: sign-consistent c.p. <=> fixed point of T <=> good root (R1 = R2 = 0, a = x_-,
    b = x_+).  PROVED (elementary, uses O1c).
T2: T o sigma = sigma o T (sigma(a,b) = (1-b, 1-a)); every fixed point is
    sigma-invariant iff it is unique.  PROVED.
T3: dR1/db = -dR2/da (closed 1-form identity, from P1 + Schwarz).  PROVED.
T4: conditional uniqueness from pointwise g1' > g2'.  LOGICALLY SOUND but the needed
    hypothesis is FALSE for R >= ~1400 (CE-1, interval certificate); NOT usable.
P1: FH with eigenvalue factor: d lambda_k/da = (R-1) lambda_k u_k(a)^2,
    d lambda_k/db = -(R-1) lambda_k u_k(b)^2; dD/da = -(R-1) R1, dD/db = (R-1) R2.
    PROVED (re-verified numerically in this run).
P2: T3 identity.  PROVED.
P3: branch-slope identities at a good root: g1' = A/B, g2' = -B/C (A = dR1/da,
    B = dR2/da, C = dR2/db); at the symmetric fp, A = -C hence g1' g2' = 1.  PROVED.
P4: R = 1 base: v = cos(pi x), q = 1/4, f_0 = 2 pi^2 sin^2(pi x)(1 - 16 cos^2(pi x)),
    zeros a0, b0.  PROVED.
O1c: v strictly decreasing on (0,1).  PROVED (Wronskian argument; matches AEH
    arXiv:2407.02459v2 Lemma 2.2(1); source version v2 verified in this run).
R1-R6: reflection structure and C1-reduction to E1 + M + Z.  PROVED in the prior run;
    re-verified in this run (see status_and_literature.md).

## 6. Boundary and degenerate cases

- R -> 1+: branches degenerate (Gamma_1 -> {a = a0} vertical, Gamma_2 -> {b = b0}
  horizontal); I shrinks to {a0}; first-order IFT is degenerate (dR1/db = 0 at R = 1
  on the branch).
- R -> inf: fp -> 1/2, delta = 1/2 - a_fp ~ 0.118/sqrt(R); lambda_1 -> 0,
  lambda_2 -> 4 pi^2; h(b0) ~ 0.38/sqrt(R) -> 0+ (numerical fits, constants unproved).
- a = b (zero-width barrier): rho = 1, f = f_0 has zeros a0, b0; not a good root.
- Multi-sheet structure at large R: extra R2 = 0 sheets excluded by the main-sheet
  definition (H3); they are not sign-consistent fixed points (CE-1 note).
- Spurious least-squares minima at large R are NOT roots (good-root checks, CE-2).

## 7. Permitted outcomes

- affirmative proof of C1 (all obligations closed, independent audit);
- negative proof / counterexample (a second zero of h in I, or a good root off the
  symmetric line, with a certificate);
- rigorous partial result (C1 under an explicit structural hypothesis, or a decisive
  sub-lemma such as endpoint signs, or a new reduction with a strictly smaller
  unresolved core) with the exact remaining gap stated;
- BLOCKED_REDUCTION or NO_MATERIAL_PROGRESS with honest gaps.

## 8. Completion criteria

A complete proof of C1 must establish, for every R > 1:
(1) h(a0) < 0 and h(beta) > 0 (endpoint signs);
(2) h has at most one zero in I;
(3) the unique zero (whose existence follows from (1) by IVT) equals a_fp(R)
    (this follows from O2 + the good-root structure once (2) holds).

Results that do NOT count: numerical evidence alone; a proof for a subclass of R; a
proof relying on the refuted Lemma A or on the refuted "g1' > 1 on I" condition; a
proof of a different uniqueness statement.

## 9. Tool, citation, and search constraints

- Every cited theorem rechecked against the exact source version:
  O1c (AEH arXiv:2407.02459v2 Lemma 2.2, local copy papers/fundamental_gap.txt),
  P1-P4 (R-20260806T011500Z-o3abranch-E8E56F/candidate_proof.md),
  T1-T4 (R-20260805T000000Z-gapn1-a1b2c3/agentB_O3a_fixed_point.md),
  R1-R6 (R-20260806T140000Z-o3ac1-42F931/candidate_proof.md).
- Computation is evidence only unless accompanied by a certificate or proof.
- ASCII punctuation in all files; Chinese final reporting.
- Do NOT call manage-math-research-program from inside this solver run.
- Do NOT modify files outside RUN_ROOT except optionally adding evidence scripts
  under scripts/.

## 10. Ambiguities or competing interpretations

(a) "Common range" I = [a0, beta] with beta = min(a_max1(R), b0); a_max1(R) is the
    right endpoint of the domain I_1 of the main-sheet branch g1 (part of H2/Lemma C).
    Numerically beta = b0 for R >= ~4 and beta = a_max1(R) < b0 for R close to 1.
(b) "The zero is a_fp(R)" presupposes a_fp(R) in I (part of H2 coverage; in the
    completion chain it follows from O2 + coverage).
(c) h is real-analytic on the interior of I; endpoint values are defined by continuity
    of the branch functions; endpoint signs must use the correct limiting definitions
    (g1(a0) = a0, g2(b0) = b0).

## 11. Contract audit

Conducted by the coordinator pass of this run against the packet and the two source
documents.  No change to any quantifier or to the mathematical content of C1.
Clarifications recorded: (i) the main-sheet convention (H3) is explicit; (ii) the
"zero is a_fp" part is reduced to O2 + coverage; (iii) the refuted Lemma A plays no
role.  Status: AUDITED, faithful to the sources.
