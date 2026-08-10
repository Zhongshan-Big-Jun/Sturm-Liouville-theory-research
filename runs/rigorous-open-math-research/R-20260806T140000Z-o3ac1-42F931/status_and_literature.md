# Status and literature (run R-20260806T140000Z-o3ac1-42F931)

## One-line status

C1 (Conjecture C1 of the source run) is OPEN.  This run proved a new,
elementary reflection structure (Lemmas R1-R6 in candidate_proof.md) that
reduces C1 to two structural facts: (E1) endpoint signs h(a0) < 0 < h(beta)
and (M) the M-shape of h'.  Both are numerically verified over a wide R-grid
(R in {1.02 ... 1e7}) but not analytically closed.  Overall run status:
RIGOROUS_PARTIAL_RESULT.

## Exact statement under study (independently normalized)

Dirichlet string on [0,1], weight rho_(a,b) = R on (a,b), 1 elsewhere,
0 < a < b < 1, R > 1.  lambda_1 < lambda_2 the two smallest eigenvalues,
u_k the L^2(rho)-normalized eigenfunctions, f = lambda_1 u_1^2 - lambda_2
u_2^2, R1 = f(a), R2 = f(b).  Branch Gamma_1 = {(a, g1(a)) : a in I_1 =
[a0, a_max1(R)]} is the R1 = 0 sheet with a = x_- (sign-consistent), Gamma_2
= {(a, g2(a)) : a in I_2 = [b_min2(R), b0]} is the R2 = 0 sheet with
b = x_+.  Common range I = I_1 cap I_2 = [a0, beta], beta = min(a_max1, b0).
h = g1 - g2 on I.  Conjecture C1: for every R > 1, h has exactly one zero in
I, namely the symmetric fixed point a_fp(R) (equivalently O3a: the
sign-consistent critical point of D = lambda_2 - lambda_1 is unique up to
reflection).  Full normalized contract: problem_contract.md.

## Proved results and exact sources

P1 (Feynman-Hellmann with eigenvalue factor):
d lambda_k/da = (R-1) lambda_k u_k(a)^2, d lambda_k/db = -(R-1) lambda_k
u_k(b)^2; dD/da = -(R-1) R1, dD/db = (R-1) R2.
Source: candidate_proof.md of run R-20260806T011500Z-o3abranch-E8E56F
(P1).  RECHECKED this run: algebra re-derived; FD agreement to 1e-6 at
(0.42, 0.56, 4).

P2 (dR1/db = -dR2/da).  Source: same run (P2).  RECHECKED: follows from P1 +
real-analyticity + Schwarz; verified ~1e-8 at four points.

P3 (branch-slope identities at a good root: g1' = A/B, g2' = -B/C; at the
symmetric fixed point g1' g2' = 1, h' = g1' - 1/g1').  Source: same run (P3).
RECHECKED: g1' g2' = 1 to ~1e-12 at fixed points for R up to 1e7.

P4 (R = 1 base: v = cos(pi x), q = 1/4, zeros of f at a0 = arccos(1/4)/pi
~ 0.419569, b0 = 1 - a0 ~ 0.580431).  Source: same run (P4).  RECHECKED by
direct computation: v = sin(2 pi x)/(2 sin(pi x)) = cos(pi x), q = 1/4,
f_0 = 2 pi^2 sin^2(pi x) (1 - 16 cos^2(pi x)).  Correct.

O1c (v = y_2/y_1 is strictly decreasing on (0,1); f has at most two zeros).
Source: prior run, Wronskian argument; AEH arXiv:2407.02459v2 Lemma 2.2
(local copy papers/fundamental_gap.txt).  RECHECKED this run: sign of the
Wronskian derivative; consistent with all numerics.

R1-R6 (this run, PROVED; full statements and proofs in candidate_proof.md):
- R1: R1(sigma(a,b)) = R2(a,b), R2(sigma(a,b)) = R1(a,b), sigma(a,b) =
  (1-b, 1-a).  Verified to 1e-16 at generic points, R in {2,4,100,1000,1e4}.
- R2: sigma(Gamma_1) = Gamma_2 on the main sheets; on I,
  g2(a) = 1 - g1^{-1}(1-a).  Verified to ~1e-6 (trace-limited); max|R2| on
  the image ~1e-9..1e-11.
- R3: h(a) = g1(a) - 1 + u(a), h'(a) = g1'(a) - 1/g1'(u(a)),
  u(a) = g1^{-1}(1-a).
- R4: h(a) = integral_{u(a)}^a (g1'(t) - 1) dt (exact, FTC); MVT corollary
  sign(h) = sign(a - u(a)) * sign(g1'(xi) - 1).
- R5: good roots = zeros of h; C1 iff {R1 = R2 = 0} has a unique solution;
  fixed points of J(a) = 1 - g1(1 - g1(a)) are zeros of h.
- R6: C1 follows from (E1) + (M) + (Z) h(fp) = 0 (proved reduction).

## Numerical verification (evidence, not proof)

R-grid {1.02, 1.05, 1.1, 1.2, 2, 4, 10, 100, 1000, 1350, 1500, 2000, 3000,
1e4, 1e5, 1e6, 1e7}: h(a0) < 0, h(beta) > 0, h > 0 on (fp, beta],
h'(fp) > 0 for all tested R.  M-shape: R <= ~1350 -> h' > 0 on I;
R >= ~1500 -> h' < 0 near the right end; R >= ~3000 -> additionally h' < 0
left of fp.  Data: reproducibility/shape_v6.json, dip_study.json,
final_shape.json; scripts: hshape.py, dip_study.py (see ledger R-106).

## Literature audit and novelty

- O1c is standard Sturm-Liouville oscillation content; the Wronskian form is
  AEH arXiv:2407.02459v2 Lemma 2.2 (fundamental gap paper of Ahrami,
  El Allali, Harrell).  Exact version checked: v2.
- The extremal-eigenvalue-ratio literature (Keller 1976, Mahar-Willner 1976,
  Huang 1999, Hedhly 2021) concerns n=1 ratio lambda_2/lambda_1 over
  one-parameter classes; it does not contain the two-parameter barrier
  critical-point uniqueness statement O3a or the branch-intersection
  statement C1.
- No published proof of C1-type statements (branch uniqueness for the
  two-parameter barrier family) was found in this run's literature checks.
  C1 is an internal project conjecture (O3a in portfolio
  O-2026-SL-GAP-3B7A2C); novelty risk is low but the result is not known to
  be published.
- Novelty claims are NOT made for C1 in this run; only the structural
  lemmas R1-R6 are claimed as new elementary results of this run.

## Exact remaining gaps (see obligation_graph.md and audit_report.md)

- G-E1: prove h(a0) < 0 and h(beta) > 0 for every R > 1 (endpoint signs).
- G-M: prove the M-shape of h' (at most two zeros, sign pattern - + -,
  h(x1) < 0 < h(x2), ordered around fp) for every R > 1.
- G-C: Lemma C structure (single-graph branches and coverage of all good
  roots by I) remains hypothesis H2, not proved.
- G-Z: h(fp) = 0 relies on O2 (existence of the symmetric fixed point),
  a separate obligation assumed in this chain.

## Confidence by axis (preliminary; final in audit_report.md)

- Semantic fidelity: high (contract audited against packet and source run).
- Mathematical correctness of R1-R6: high (elementary proofs; numerics).
- Completeness of C1: low (main gap open).
- Novelty: not claimed.
- Reproducibility: high (scripts and data under reproducibility/).