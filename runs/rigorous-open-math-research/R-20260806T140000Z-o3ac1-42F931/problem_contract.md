# Problem contract: C1 (unique zero of h = g1 - g2; uniqueness up to reflection of the sign-consistent critical point)

## 0. Provenance (Phase 0 summary)

Authoritative problem source: task packet
agenda/task-packets/Q-20260806-o3a-c1-42F931.md (2026-08-06, task state DRAFT),
which delegates the proof of Conjecture C1 as stated in
runs/rigorous-open-math-research/R-20260806T011500Z-o3abranch-E8E56F/candidate_proof.md,
Section C1, with supporting facts P1-P4 in the same file, the counterexample
certificate CE-1 in counterexample_log.md, and gaps G2-G4 in audit_report.md.
The upstream reduction T1-T4 is in runs/rigorous-open-math-research/
R-20260805T000000Z-gapn1-a1b2c3/agentB_O3a_fixed_point.md.

Per the packet, this contract is written independently: the packet is project
context, NOT a verified theorem contract. Every premise is re-derived or
re-verified against the cited source versions and first principles in this run.

Portfolio problem: O-2026-SL-GAP-3B7A2C (adjacent gap extremals n=1, box class).
Obligation: O3a (uniqueness up to reflection of the sign-consistent critical
point of D over the barrier family).

## 1. Objects and definitions (independently normalized)

Let R > 1 be fixed. Dirichlet vibrating string on [0,1]:

    -y''(x) = lambda rho(x) y(x),  y(0) = y(1) = 0,
    rho_(a,b)(x) = R for a < x < b, 1 otherwise, with 0 < a < b < 1.

Let 0 < lambda_1 < lambda_2 be the two smallest eigenvalues (simple; standard
SL theory for positive bounded weights).  Set s_k = sqrt(lambda_k).  Normalize
the eigenfunctions by y_k(0) = 0, y_k'(0) = 1 (slope normalization; the source
prose "y_k(0) = 1" in the 2026-08-05 run is a known typo; every invariant
object below is normalization-invariant).  Let u_k = y_k/||y_k||_{L^2(rho)}
and define

    f(x; a, b) = lambda_1 u_1(x)^2 - lambda_2 u_2(x)^2,
    R1(a,b) = f(a; a,b),   R2(a,b) = f(b; a,b),
    v(x; a, b) = y_2(x; a, b)/y_1(x; a, b),   q(a,b) = (s_1/s_2) * sqrt(n_2/n_1)
    with n_k = ||y_k||_{L^2(rho)}^2.

Known structure (re-verified in this run, see status_and_literature.md):
v is strictly decreasing on (0,1), v(0+) = 1, v(1-) < 0; f has at most two
zeros x_- < x_+ with v(x_-) = q, v(x_+) = -q; {f > 0} = (x_-, x_+) is a
single interval.  Good root (sign-consistent critical point, equivalently
fixed point of T; theorem T1): pair (a,b), 0 < a < b < 1, with
R1(a,b) = R2(a,b) = 0 and a = x_-(a,b), b = x_+(a,b) (equivalently
v(a) = q > 0, v(b) = -q < 0, a < z_0 < b where z_0 = v^{-1}(0)).

Branch Gamma_1 = {(a,b) : 0 < a < b < 1, R1(a,b) = 0, a = x_-(a,b)}
             = {(a, g1(a)) : a in I_1},  with I_1 = [a0, a_max1(R)].
Branch Gamma_2 = {(a,b) : 0 < a < b < 1, R2(a,b) = 0, b = x_+(a,b)}
             = {(a, g2(a)) : a in I_2},  with I_2 = [b_min2(R), b0].
Common range I = I_1 cap I_2 = [a0, beta], beta = min(a_max1(R), b0).
Constants: a0 = arccos(1/4)/pi ~ 0.4195694, b0 = arccos(-1/4)/pi = 1 - a0
~ 0.5804305 (P4: the zeros of f at R = 1).
h(a) = g1(a) - g2(a) on I.
a_fp(R): the symmetric fixed point, (a_fp, 1 - a_fp) is a good root
(existence = obligation O2, separate; assumed available in the chain that
C1 completes).

## 2. Hypotheses

H1. R > 1 fixed but arbitrary.
H2. (Branch structure, part of Lemma C) Gamma_1 and Gamma_2 are each single
     connected curves that are graphs over the intervals I_1, I_2, with
     g1, g2 real-analytic on the interiors; I = [a0, beta] with a0 < beta
     nonempty; the symmetric fixed point lies in I when it exists.
H3. All quantities are evaluated on the fixed-point-relevant (main) sheets,
     defined by continuation from the R = 1 degenerate limits: Gamma_1
     through (a0, a0), Gamma_2 through (b0, b0) (see counterexample_log.md
     CE-1 multi-sheet note: there exist extra points with R2 = 0, v(b) < 0,
     v(a) < 0 at R = 1500 which are NOT on these sheets and are NOT
     sign-consistent fixed points).

## 3. Target conclusion (Conjecture C1, exact statement)

For every R > 1: h = g1 - g2 has exactly one zero in the common range
I = [a0, beta]; the zero is the symmetric fixed point a_fp(R).
Equivalently (given T1, T2 and O2): O3a holds, i.e. the sign-consistent
critical point of D = lambda_2 - lambda_1 over the barrier family is unique
up to reflection (and hence, being unique, symmetric with b = 1 - a).

## 4. Quantifiers and dependency of constants

All constants (branch ranges, slopes, the fixed point) depend on R.  No
uniform-in-R bound is required for C1 itself; the refuted R-uniform bound
of the old Lemma A is not part of this contract.  The zero of h is required
to be a_fp(R) exactly (not merely "at most one zero").

## 5. Equivalent formulations actually proved equivalent (audited in prior runs, re-verified here)

T1: sign-consistent c.p. <=> fixed point of T <=> good root.  PROVED.
T2: T o sigma = sigma o T (sigma(a,b) = (1-b, 1-a)); uniqueness of the
    fixed point implies b = 1 - a.  PROVED.
T3: dR1/db = -dR2/da (closed 1-form identity).  PROVED (via P1 + Schwarz;
    the FH formula must carry the eigenvalue factor; see P1).
T4: conditional uniqueness from monotonicity of h.  Logically sound but
    hypothesis (b) (g1' > g2') is FALSE for R >= ~1400 (CE-1); T4 is NOT
    usable for the full theorem.  C1 replaces it.
P1: FH with eigenvalue factor: d lambda_k/da = (R-1) lambda_k u_k(a)^2,
    d lambda_k/db = -(R-1) lambda_k u_k(b)^2; hence dD/da = -(R-1) R1,
    dD/db = (R-1) R2.  PROVED (re-verified numerically in this run).
P2: T3 identity.  PROVED.
P3: branch-slope identities at a good root: with A = dR1/da, B = dR2/da,
    C = dR2/db: g1' = A/B, g2' = -B/C; at the symmetric fp, A = -C hence
    g1' g2' = 1 and h' = g1' - 1/g1'.  PROVED (algebraic; re-verified).
P4: R = 1 base: v = cos(pi x), q = 1/4, zeros of f at a0, b0.  PROVED.

## 6. Boundary and degenerate cases

- R -> 1+: branches degenerate (Gamma_1 -> {a = a0} vertical segment,
  Gamma_2 -> {b = b0} horizontal segment); I shrinks to {a0}.  The
  perturbation is degenerate to first order (dR1/db = 0 at R = 1 on the
  branch); this is why the R -> 1+ perturbation route was left incomplete.
- R -> infinity: fp -> 1/2; delta = 1/2 - a_fp ~ 0.118/sqrt(R); lambda_1 -> 0,
  lambda_2 -> 4 pi^2; h(b0) ~ 0.38/sqrt(R) -> 0+.
- a = b (degenerate zero-width barrier): rho = 1, not a good root for R > 1
  (f = f_0 has zeros a0, b0 with x_- = a0; a = b not in I).
- Multi-sheet structure at large R: extra R2 = 0 sheets exist; excluded by
  the main-sheet definition (H3).  They are not sign-consistent fixed points
  (v(a) < 0 there), so O3a is unaffected (CE-1 note).
- Spurious least-squares minima at large R (residual ~2.6e-7, v(a) ~ 1) are
  NOT roots; excluded by the good-root checks (CE-2).

## 7. Permitted outcomes

- affirmative proof of C1 (all obligations closed, independent audit);
- negative proof / counterexample (a second zero of h in I, or a good root
  off the symmetric line, with a certificate);
- rigorous partial result (e.g. C1 under an explicit structural hypothesis,
  or a decisive sub-lemma such as nondegeneracy of all good roots, or
  endpoint signs) with the exact remaining gap stated;
- BLOCKED_REDUCTION or NO_MATERIAL_PROGRESS with honest gaps.

## 8. Completion criteria

A complete proof of C1 must establish, for every R > 1:
(1) h(a0) < 0 and h(beta) > 0 (endpoint signs; Lemma B);
(2) h has at most one zero in I;
(3) the unique zero (whose existence follows from (1) by IVT) equals a_fp(R)
    (this follows from O2 + the good-root structure once (2) holds: the
    symmetric fp is a good root, hence a zero of h by H2/Lemma C coverage).
Results that do NOT count: numerical evidence alone; a proof for a subclass
of R; a proof relying on the refuted Lemma A; a proof of a different
uniqueness statement.

## 9. Tool, citation, and search constraints

- Every cited theorem rechecked against the exact source version:
  P1-P4 (candidate_proof.md of R-20260806T011500Z-o3abranch-E8E56F),
  T1-T4 (agentB_O3a_fixed_point.md of R-20260805T000000Z-gapn1-a1b2c3),
  O1c (Wronskian argument, AEH arXiv:2407.02459v2 Lemma 2.2, local copy
  papers/fundamental_gap.txt), P4 base facts (direct computation at R = 1).
- Computation is evidence only unless accompanied by a certificate or proof.
- ASCII punctuation in all files; Chinese final reporting (project policy).
- Do NOT call manage-math-research-program from inside this solver run.

## 10. Ambiguities or competing interpretations

(a) "Common range" I: the packet and source define I = [a0, beta] with
    beta = min(a_max1(R), b0).  a_max1(R) is the right endpoint of the
    domain I_1 of the main-sheet branch function g1; its definition is
    part of Lemma C's structural hypothesis (H2).  Numerically a_max1(R)
    < b0 for R close to 1 and a_max1(R) > b0 for R large; beta = b0 for
    large R.
(b) The claim "the zero is a_fp(R)" presupposes a_fp(R) in I, which is
    part of the content of H2/Lemma C coverage; in the completion chain it
    follows from O2 (fp exists) and the coverage part of Lemma C.
(c) h is real-analytic on the interior of I (real-analytic defining system,
    simple secular roots, implicit function theorem); at the endpoints h is
    defined by continuity of the branch functions; endpoint signs must be
    checked with the correct limiting definitions (g1(a0) = a0, g2(b0) = b0).

## 11. Contract audit

Conducted by the coordinator pass of this run against the packet and the two
source documents.  No change to any quantifier or to the mathematical content
of C1.  Clarifications recorded: (i) the main-sheet convention (H3) is made
explicit; (ii) the "zero is a_fp" part is reduced to O2 + coverage; (iii) the
refuted Lemma A plays no role in this contract.  Status of the contract:
AUDITED, faithful to the sources.
