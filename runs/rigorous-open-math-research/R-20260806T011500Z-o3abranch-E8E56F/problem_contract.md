# Problem contract: O3a branch lemmas (Lemma A/B/C), run R-20260806T011500Z-o3abranch-E8E56F

# 1. Provenance (Phase 0 summary)

Authoritative problem source: runs/rigorous-open-math-research/
R-20260805T000000Z-gapn1-a1b2c3/agentB_O3a_fixed_point.md (2026-08-05), Section 4,
"Exact remaining gap": Lemma A, Lemma B, Lemma C. Supporting theory T1-T4 in Sections
1-3 of the same file. Task packet Q-20260806-o3a-branch-E8E56F summarizes the three
lemmas; per the packet instructions this summary is NOT trusted verbatim and was
rechecked against the source and against first principles in this run.

The overarching claim (O3a, from the prior run): for the barrier family
rho_(a,b) = R on (a,b), 1 elsewhere, 0 < a < b < 1, R > 1, the map T (defined below)
has at most one fixed point in 0 < a < b < 1; with the existence of a fixed point
(obligation O2, separate), exactly one, hence symmetric b = 1 - a by T2.

# 2. Objects and definitions (independently normalized; audited against source)

Let R > 1. Dirichlet vibrating string on [0,1]:
    -y''(x) = lambda rho(x) y(x), y(0) = y(1) = 0,
    rho_(a,b)(x) = R for a < x < b, 1 otherwise, 0 < a < b < 1.
Let 0 < lambda_1 < lambda_2 be the two smallest eigenvalues (simple, standard SL
theory), s_k = sqrt(lambda_k). Normalize y_k by y_k(0) = 0, y_k'(0) = 1 (the source
writes y_k(0) = 1, which contradicts y_k(0) = 0; the code and all invariant objects
use the slope normalization; all objects below are normalization-invariant).
u_k = y_k / ||y_k||_{L^2(rho)}, f(x) = lambda_1 u_1(x)^2 - lambda_2 u_2(x)^2,
R1(a,b) = f(a), R2(a,b) = f(b), v = y_2/y_1.

Fact O1c (proved in prior run; re-derived in this run, see status_and_literature.md):
v is strictly decreasing on (0,1), v(0+) = 1, v(1-) < 0; f = u_1^2 (lambda_1 -
lambda_2 v^2) has exactly two zeros x_- < x_+ (when they exist), with
{f > 0} = (x_-, x_+) a single interval containing z_0 = v^{-1}(0), and
v(x_-) = q, v(x_+) = -q where q = sqrt(lambda_1/lambda_2) * ||y_2||/||y_1||.

T(a,b) = (x_-, x_+) when f has the sign pattern (-,+,-).
Good root: (a,b) with R1 = R2 = 0, a = x_-, b = x_+ (equivalently fixed point of T,
equivalently sign-consistent critical point; T1 in source).

Gamma_1 = {(a,b) : 0 < a < b < 1, R1(a,b) = 0, a = x_-(a,b)}.
Gamma_2 = {(a,b) : 0 < a < b < 1, R2(a,b) = 0, b = x_+(a,b)}.
The prior run establishes numerically that Gamma_1 (resp. Gamma_2) is the graph of a
function b = g1(a) (resp. b = g2(a)) over an interval; the common range is
I = I_1 cap I_2 = [alpha, beta] (nonempty for all tested R).

# 3. Hypotheses

H1. R > 1 fixed but arbitrary.
H2. The good branches Gamma_1, Gamma_2 are each single connected curves that are
     graphs over a-intervals I_1, I_2, and I = I_1 cap I_2 is a closed interval
     [alpha, beta] with alpha < beta. (This is part of Lemma C below; it is stated
     here as the structural hypothesis within which A and B operate. The full
     Lemma C asks for the proof of this structure plus coverage of all fixed points.)

# 4. Target conclusions (the three lemmas, exact statements)

Lemma A (monotone branch gap). On the common range I, g1 and g2 are C^1 and
    g1'(a) > g2'(a) > 0  for every a in I.
Remarks. (i) The task packet additionally claims "an R-uniform positive lower bound
on g1' - g2'"; this run establishes numerically that the uniform bound is FALSE
(min(g1'-g2') -> 0 as R -> infinity; see research_ledger R-007, R-008). The
theorem T4 only needs the pointwise inequality, so Lemma A is restated without the
uniform bound. (ii) C^1 follows from real-analyticity of the defining system (IFT);
the content is the strict sign inequality.

Lemma B (endpoint signs of h = g1 - g2).
    h(alpha) < 0 < h(beta).
Numerically alpha = a0 := arccos(1/4)/pi and beta = min(a_max1(R), b0) with
b0 := arccos(-1/4)/pi = 1 - a0, where a_max1(R) is the right end of I_1; the branch
Gamma_1 reaches the diagonal point (a0, a0) (rho == 1) and Gamma_2 reaches
(b0, b0). Verified for R in {1.02..100}: h(alpha) in [-0.155,-0.034], h(beta) in
[+0.038,+0.41].

Lemma C (coverage / single-graph structure). Every sign-consistent fixed point
(a,b) satisfies a in I and b = g1(a) = g2(a). Equivalently: the good sets
Gamma_1 cap {a = x_-} and Gamma_2 cap {b = x_+} are exactly the graphs of g1, g2
over I_1, I_2 (single components, no other components), and the (unique, when it
exists) fixed point lies in the common range.

# 5. Quantifiers and dependency of constants

All constants (a0, b0, the branch ranges, slopes) depend on R; no constant is
required to be uniform in R for the theorem, with the single correction noted in
Lemma A(i). The fixed point a-coordinate a_fp(R) satisfies a0 < a_fp(R) < beta(R)
numerically for all tested R; this is the content needed to turn Lemma A into
Lemma B (h increasing + h(a_fp) = 0).

# 6. Equivalent formulations that are actually proved equivalent

T1: sign-consistent c.p.  <=>  fixed point of T  <=>  good root. (Proved, audited.)
T2: T o sigma = sigma o T; uniqueness of the fixed point implies b = 1 - a.
    (Proved, audited.)
T3: dR1/db = -dR2/da on 0 < a < b < 1. (Proved via FH + Schwarz; numerically
    verified to 1e-7.)
T4: conditional uniqueness: if g1, g2 exist as in Lemma C(a), with g1' > g2'
    (Lemma A) and endpoint signs (Lemma B), then at most one fixed point; with
    existence (O2), exactly one and symmetric. (Proved, audited.)

# 7. Boundary and degenerate cases

- a = b (diagonal): rho == 1 a.e.; f is the rho == 1 function with zeros at
  a0, b0; the branch endpoints (a0, a0) and (b0, b0) lie on Gamma_1, Gamma_2
  respectively as boundary limits (R1(a0, b) < 0 for b > a0; the root at b = a0
  is at the domain boundary).
- R -> 1+: I_1, I_2 degenerate to the vertical lines a = a0 (G1) and b = b0 (G2);
  the common range collapses to {a0}; h' -> infinity.
- R -> infinity: alpha = a0, beta -> b0 for R >= R* (R* in (3,4) numerically);
  h(alpha), h(beta) -> 0; min h' -> 0 (NO uniform bound).
- 0 < a < b < 1 strictly; the degenerate members a = 0, b = 1, a = b are excluded
  from the branch analysis (they are limits).

# 8. Permitted outcomes

- affirmative proof of Lemma A, B, C (individually or together);
- negative result / counterexample (none found);
- rigorous partial theorem (e.g., Lemma B or C proved; Lemma A reduced to an
  explicit inequality);
- falsified subclaim (e.g., the R-uniform bound);
- precise remaining gaps with audited numerics.

# 9. Completion criteria

For THIS run: deliver, under the run root, the standard artifact set with
(i) an audited contract (this file), (ii) an obligation graph, (iii) a research
ledger recording every numerical experiment and proof attempt, (iv) a
candidate_proof.md containing any proved lemma or reduction, (v) an audit report
listing open gaps. Full completion of O3a (all of Lemma A, B, C) is the target but
not guaranteed; the run must report the strongest audited status.

# 10. Results that do not count as completion

- Numerical verification of Lemma A/B/C for finitely many R.
- A proof for a different constraint class.
- The R-uniform bound claim as stated in the packet (shown false numerically);
  proving pointwise g1' > g2' > 0 is the real target.

# 11. Tool, citation, and search constraints

- Premises rechecked against primary sources: AEH arXiv:2407.02459v2 (FH formula
  Lemma 2.1; Wronskian Lemma 2.2), the prior run's agentB_O3a_fixed_point.md
  (T1-T4), and standard SL theory (simplicity, Sturm oscillation).
- Computation is evidence only; every computational claim needs a proof bridge or
  a certificate.
- ASCII punctuation in all files; Chinese final reporting per project policy.

# 12. Ambiguities or competing interpretations

(a) The packet's Lemma A includes an R-uniform lower bound on g1'-g2'; the source
    document (agentB_O3a_fixed_point.md) states Lemma A without the uniform bound
    in the theorem statement (Section 4: "g1'(a) > g2'(a) > 0") and only discusses
    the uniform bound in the numerics paragraph. This run treats the pointwise
    statement as authoritative (matching T4's needs) and records the uniform-bound
    claim as false.
(b) "y_k(0) = 1" in the source prose is a typo for the slope normalization; no
    invariant object changes.
(c) Lemma B's "endpoints originate from arccos(1/4)/pi and arccos(-1/4)/pi" is
    made precise as: alpha = a0 for all tested R (Gamma_1 reaches the diagonal at
    a0) and beta = min(a_max1(R), b0), with a_max1(R) -> a0 as R -> 1+ and
    a_max1(R) > b0 for R >= R*.

# 13. Contract audit

Conducted by the coordinator (this run) against task packet
Q-20260806-o3a-branch-E8E56F and the prior-run source file. Corrections applied:
Lemma A restated without the R-uniform bound (false; see ledger R-008); Lemma B
endpoint claim sharpened to the a0/b0 diagonal structure; Lemma C made precise as
single-graph + coverage. No quantifier was changed that affects the theorem.

# 14. Revision 2026-08-06 (this run): Lemma A falsified, contract updated

This run (R-20260806T011500Z-o3abranch-E8E56F) established, by three
independent numerical methods AND a rigorous interval-arithmetic certificate
(reproducibility/cert_ce1.py; outward-directed interval arithmetic,
iv.prec = 220), that the pointwise claim in Lemma A is FALSE for large R:

  g1(a) - g2(a) is NOT strictly increasing on the whole common range for R
  approximately >= 1400.  Specifically, at R = 1500, a = 0.57364, one finds
  g1's = +1.020553, g2's = +1.020897 (closed-form implicit derivatives), so
  h'(a) = -0.000344 < 0, on a genuine subinterval of the common range
  [a0, b0].  The sign flip threshold is R* in (1200, 1500), approximately 1350.
  Verified with (i) finite differences of branch roots via the prior-run solver
  agentB_lib, (ii) finite differences of branch roots via the clean_lib solver,
  (iii) closed-form implicit derivatives (no branch FD), all in agreement.
  Direct values of h(a) near a = 0.5736 confirm the decrease.  An ODE-shooting
  cross-check (no secular equation) confirms the branch structure.

Consequences for the contract:
- Section 10 (b) is now obsolete in a stronger sense: not only the R-uniform
  bound but the pointwise inequality g1' > g2' fails for large R.  The
  statement "Lemma A: g1' > g2' on the common range for every R > 1" is
  REFUTED rigorously: the interval-arithmetic certificate proves
  h'(a*) in [-3.4298e-4, -3.4298e-4] < 0 at (R, a*) = (1500, 0.57364) and
  h' in [-3.2030e-3, -3.2030e-3] < 0 at (1e4, 0.57364), with verified root
  enclosures (width ~5e-28), sign-definite denominators, and certified
  good-root checks (see audit_report.md and counterexample_log.md CE-1).
- The fixed point uniqueness claim (O3a) is NOT refuted: h = g1 - g2 has exactly
  one zero in the common range for every R in {1.02, ..., 1e6} tested in this
  run (zero located at the symmetric fp a_fp(R); see research_ledger and
  counterexample_log.md).  h(b0) = g1(b0) - b0 ~ 0.38/sqrt(R) > 0 for R up to
  1e7, so no second zero appears from the right end in the computable range.
- The T4 route (conditional uniqueness via monotonicity of h) is invalidated for
  large R because hypothesis (b) of T4 fails.  The corrected structural
  conjecture C1 (h has exactly one zero; h' sign pattern "+, then a negative
  interval near the right end, then possibly + again", with h(b0) > 0) is
  numerically supported and is the replacement target.

New target conclusions for THIS run's deliverables (superseding Section 4 only
in what is claimed as proved; the lemmas as stated in Section 4 remain the
objects of study):
- T1-T4 audited: T1, T2, T4 logic sound; T3 proof valid once the FH formula is
  written with the eigenvalue factor (d lambda_k/d eps = -lambda_k int rho_eps
  u_k^2 dx); identity dR1/db = -dR2/da verified to 1e-8.
- Proposition P1-P4 (see candidate_proof.md): FH with lambda factor; T3;
  branch-slope identities and Hessian reduction at the fixed point; R = 1 base
  facts (v -> cos(pi x), q -> 1/4, endpoint constants a0, b0).
- Lemma A as stated: REFUTED rigorously for R >= ~1400 (interval
  certificate; CE-1).
- Lemma B (endpoint signs): verified numerically for R in {1.02 .. 1e6}, not
  proved.
- Lemma C (single-graph branches + coverage): verified numerically, not proved.
- O3a (unique fixed point): numerically supported for R in {1.02 .. 1e6}, open.


