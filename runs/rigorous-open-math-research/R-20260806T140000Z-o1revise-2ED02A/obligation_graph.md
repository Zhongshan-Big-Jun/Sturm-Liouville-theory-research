# Obligation graph - O1 revision (R-20260806T140000Z-o1revise-2ED02A)

Root: THEOREM_SUP_RED (sup_K D = max over barrier family, attained) and
      THEOREM_INF_RED (inf_K D = min over well family, attained).
Scope: O1 only (per the task packet).  O2/O3 are separate obligations of the
draft run and are listed for dependency context only.

## O1a - L^1 continuity of lambda_k on the box class K

Statement: for every k >= 1, rho |-> lambda_k(rho) is continuous in the L^1
topology on K, with explicit modulus
  |lambda_k(rho) - lambda_k(sigma)| <= (R/4)(k^2 pi^2)^2 ||rho-sigma||_1^{1/2}.
Quantifiers: R > 1 fixed; rho, sigma in K.
Depends on: P3 (Weyl inequality), P4 (comparison bounds), P5 (HS bound),
the similarity S_rho ~ T_rho, and the identity mu_k(S_rho) = 1/lambda_k(rho).
Evidence/status: PROVED (repaired; draft was PARTIAL).
Proof or citation: candidate_proof.md Lemma 1 (repair R1).
Known edge cases: rho = sigma (trivial); R -> 1+ (continuity persists).
Verifier notes: T_rho itself is not self-adjoint; the draft step is invalid
as written.  The corrected S_rho argument closes the obligation.

## O1b - FH derivative at a moving jump

Statement: for rho in K constant on a two-sided neighborhood of x_j with
values c_- (left), c_+ (right), c_- != c_+, the map eps |-> D(rho_eps)
(jump at x_j + eps) is differentiable at 0 with
  d/deps D(rho_eps)|_0 = -(c_+ - c_-) f(x_j),
f = lambda_1 u_1^2 - lambda_2 u_2^2.  Equivalently: moving right by delta
changes D by -(c_+ - c_-) f(x_j) delta + o(delta); moving left by
+(c_+ - c_-) f(x_j) delta + o(delta).
Quantifiers: as stated; x_j in (0,1); eps small enough that the jump stays
inside the constant-value neighborhood.
Depends on: P1 (AEH Lemma 2.1 applied to smoothed families), P6 (approximation
argument R4), continuity of eigenfunctions (from P5 + H^2 bounds).
Evidence/status: PROVED (repaired; draft was FAILED as stated).
Proof or citation: candidate_proof.md Lemma 3 (repairs R2 + R4).
Known edge cases: c_+ - c_- sign flip reverses the sign of the derivative;
f(x_j) = 0 gives zero derivative (stationarity).  The draft's wrong sign
((c_+ - c_-) f(x_j)) is REFUTED numerically and by the verified identity
dD/du = -2(R-1) f(u) for the symmetric barrier family (draft-run ledger
R-003 and audit cross-check).
Verifier notes: the audit's parenthetical about the two-sided derivative is
imprecise; the two-sided derivative of eps |-> D(jump at x_j + eps) exists for
every x_j (analyticity of the transfer-matrix/secular eigenvalue in the jump
position for piecewise constant rho; or directly from the approximation
argument).  The stationarity consequence at interior extremizers
(f_N(x_j) = 0) is identical under either formulation.

## O1c - structure of f (Wronskian)

Statement: for ANY rho in K, with u_1, u_2 the L^2(rho)-normalized
eigenfunctions and sign convention u_1 > 0 on (0,1), u_2 > 0 on (0,z_0),
u_2 < 0 on (z_0,1) (z_0 the unique zero of u_2): f = lambda_1 u_1^2
- lambda_2 u_2^2 has at most two zeros in (0,1), and {f > 0} is a single
interval containing z_0.
Quantifiers: any rho in K (bounded measurable, 1 <= rho <= R).
Depends on: P2 (AEH Lemma 2.2 structure; re-derived here with a global
W < 0 argument), P7 (Sturm oscillation).
Evidence/status: PROVED (unchanged from the draft; repair R3 = explicit sign
convention).
Proof or citation: candidate_proof.md Lemma 2.
Known edge cases: v(0+) <= c or v(1-) >= -c -> fewer zeros; {f>0} may touch
0 or 1; f(z_0) = lambda_1 u_1(z_0)^2 > 0 always.
Verifier notes: verified numerically on hostile configs (alternating
1/R blocks, 4-8 jumps); no violation found.

## O1d - compactness and at most two effective jumps for K_N extremizers

Statement: for each N >= 0, D attains its maximum and minimum on K_N (the
piecewise-constant subclass of K with at most N jumps), and any extremizer
admits a minimal representation with at most two effective jumps.
Quantifiers: N >= 0, R > 1.
Depends on: O1a (continuity), O1b (stationarity), O1c (zero count).
Evidence/status: PROVED (given O1a and O1b repaired).
Proof or citation: candidate_proof.md Lemma 4.
Known edge cases: N = 0 (constants); boundary configurations reduce to the
smaller family; coalesced jumps reduce the effective count.
Verifier notes: minimal representation = all effective jumps interior with
adjacent distinct values; each effective jump is then a free interior
parameter, so the stationarity condition applies independently.

## O1e - step functions are dense (M_N -> sup_K D)

Statement: sup over step functions in K equals sup_K D; with
M_N = max_{K_N} D, M_N is nondecreasing and M_N -> sup_K D.  Mirror
statement for inf with m_N = min_{K_N} D.
Quantifiers: N -> inf.
Depends on: O1a (continuity) + standard L^1 block-averaging.
Evidence/status: PROVED (unchanged; requires O1a).
Proof or citation: candidate_proof.md Lemma 5.
Known edge cases: none (block averages stay in [1,R] and converge in L^1).
Verifier notes: fine.

## O1f - bang-bang structure at a global extremizer

Statement: any global maximizer rho~ of D over K satisfies rho~ = R a.e. on
{f~ > 0} and rho~ = 1 a.e. on {f~ < 0}; any global minimizer satisfies the
reversed assignment.  With O1c, maximizers are a.e. barrier configs and
minimizers a.e. well configs.
Quantifiers: global extremizers over K (which exist by O1d + O1e).
Depends on: O1a, O1d, O1e, P1 (AEH Lemma 2.1 with L^1 perturbations),
O1c (interval structure).
Evidence/status: PROVED (unchanged; correct FH sign at pointwise level).
Proof or citation: candidate_proof.md Section "Global bang-bang".
Known edge cases: f~ = 0 on a set -> rho~ free there (null-effect for D);
density values in (1,R) on {f~ != 0} contradict extremality via an open
perturbation interval.
Verifier notes: at a maximizer all admissible one-sided perturbations have
nonpositive derivative; the sign of dD/dt = int delta-rho f~ dx was
independently confirmed (audit C-007 corrected test; this run re-runs it).

## Synthesis (SUP/INF)

sup_K D = sup_{K_2} D (O1d + O1e), attained at rho~ in K_2 (compactness);
rho~ is a global maximizer, hence barrier config a.e. (O1f + O1c); therefore
sup_K D = max over the closed barrier family (continuity of (a,b) |-> D and
compactness of [0,1]^2).  Mirror argument for the well family.  Attainment
holds.  Status: PROVED (given O1a-O1f).

## Out of scope (context only)

O2 (symmetric 1-parameter family), O3 (2-parameter critical point symmetry),
O4 (independent audit of the final gap theorem), O5 (novelty audit of the
full theorem) - owned by the draft run/manager; this run covers O1 and
performs its own novelty scan in Phase 11.

## Dependency summary

THEOREM_SUP_RED = O1a + O1b + O1c + O1d + O1e + O1f
THEOREM_INF_RED = same (mirror)
O1d depends on O1a, O1b, O1c; O1e depends on O1a; O1f depends on O1a, O1c, O1d, O1e.
