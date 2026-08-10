# Status and literature - premise recheck for the O1 revision

Every premise used by the revised proof is listed with its exact source
statement and a verdict.  Status legend: KNOWN (verified from primary source),
DERIVED (proved in this run), CONJECTURED, HEURISTIC, RECALLED_UNVERIFIED.

## P1. AEH Lemma 2.1 (Feynman-Hellmann) - KNOWN

Source: M. Ahrami, Z. El Allali, E. M. Harrell II, "On the fundamental
eigenvalue gap of Sturm-Liouville operators", arXiv:2407.02459v2 (3 Jul 2024),
Lemma 2.1, papers/fundamental_gap.txt (verbatim):

"Suppose that V(.,t) and w(.,t) are one-parameter families of real-valued,
locally L1 functions, with inf V(x,kappa) > -inf, C >= w(x,kappa) >= 1/C for
some C > 0, and dV/dkappa(x,kappa) and dw/dkappa(x,kappa) in L1(0,pi). Then
d lambda_n(kappa)/dkappa = -lambda_n int_0^pi (dw/dkappa) u_n^2 dx
                          + int_0^pi (dV/dkappa) u_n^2 dx."

Normalization used in the proof: int w u_n^2 = 1.  Interval is [0,pi]; our
problem on [0,1] is an affine rescaling (harmless).

Use in this run: V = 0, w = rho in [1,R].  For L1 pointwise perturbations
w(kappa) = rho + kappa delta-rho with delta-rho in L1, hypotheses are met
exactly.  For moving-jump families the derivative dw/dkappa is a Dirac
measure (NOT in L1), so Lemma 2.1 is applied to smoothed families and the
limit is taken (repair R4); this is a NEW justification added by this run.

## P2. AEH Lemma 2.2 (monotonicity of u_2/u_1, structure of f) - KNOWN

Source: same paper, Lemma 2.2 (verbatim), items:
(1) u_2/u_1 is decreasing on (0,pi);
(2) |u_1| = |u_2| has one or two solutions on (0,pi);
(3) x_-, x_+ with u_1^2 > u_2^2 on (x_-,x_+) and u_1^2 <= u_2^2 on the complement;
(4) lambda_1|u_1^2| = lambda_2|u_2^2| has one or two solutions on (0,pi);
(5) xhat_-, xhat_+ with lambda_1 u_1^2 > lambda_2 u_2^2 on (xhat_-,xhat_+) and
    <= on the complement.
Hypotheses: same as Lemma 2.1 (V, w locally L1, inf V > -inf, C >= w >= 1/C);
sign convention u_{1,2} > 0 near 0.  Proof via W' = (lambda_1 - lambda_2) w u_1 u_2.

Use in this run: the draft's O1c re-derivation replaces AEH's reflection
argument with a global W < 0 argument on (0,1) (W(0) = W(1) = 0, sign pattern
of W'), which is valid for every bounded measurable rho >= c > 0 and is
rho-independent.  Both arguments prove (1),(4),(5).  This run states the u_2
sign convention explicitly (repair R3): u_2 > 0 on (0,z_0), u_2 < 0 on (z_0,1),
z_0 the unique interior zero of u_2 (Sturm oscillation, standard).

## P3. Weyl / min-max inequality for self-adjoint compact operators - KNOWN

Statement used: if A, B are self-adjoint compact operators on a Hilbert space
with eigenvalues mu_1 >= mu_2 >= ... (each repeated by multiplicity, tending
to 0), then |mu_k(A) - mu_k(B)| <= ||A - B|| for every k.
This is the standard Weyl inequality (e.g., from the min-max principle for
self-adjoint compact operators).  Draft misapplied it to the non-self-adjoint
T_rho (kernel G(x,t)rho(t)); the revised proof applies it to the symmetric
Hilbert-Schmidt operator S_rho with kernel sqrt(rho(x)) G(x,t) sqrt(rho(t))
(repair R1).  S_rho is similar to T_rho (conjugation by M_{sqrt(rho)}), so
the nonzero spectra coincide; mu_k(S_rho) = 1/lambda_k(rho).

Operator-formula correction recorded: the audit/packet write
S_rho = rho^(1/2) T_rho rho^(1/2), which as written is NOT symmetric when
T_rho = T_0 M_rho.  The correct identity is
S_rho = M_{sqrt(rho)} T_0 M_{sqrt(rho)} = M_{sqrt(rho)} T_rho M_{rho^{-1/2}}.
The kernel form sqrt(rho(x)) G(x,t) sqrt(rho(t)) is used throughout.

## P4. Eigenvalue comparison bounds lambda_k(rho) in [k^2 pi^2/R, k^2 pi^2] - DERIVED

Rayleigh quotient: lambda_k(rho) = min_{dim S = k} max_{0 != y in S}
(int y'^2)/(int rho y^2).  Since 1 <= rho <= R: int y'^2/(R int y^2) <= Q_rho
<= int y'^2/int y^2, so k^2 pi^2 / R <= lambda_k(rho) <= k^2 pi^2.
Derived in this run (also standard comparison principle for weighted strings);
verified numerically in verify_hs_bound.py.

## P5. Hilbert-Schmidt continuity bound - DERIVED (this run)

||S_rho - S_sigma||_HS <= (R/4) ||rho - sigma||_1^{1/2}.
Derivation: |sqrt(rho(x))sqrt(rho(t)) - sqrt(sigma(x))sqrt(sigma(t))|
  <= sqrt(R)/2 (|rho(x)-sigma(x)| + |rho(t)-sigma(t)|),
G(x,t) <= 1/4, and ||rho-sigma||_2^2 <= R ||rho-sigma||_1.
Gives ||S_rho-S_sigma||_HS^2 <= (R/16)||rho-sigma||_2^2 <= (R^2/16)||rho-sigma||_1.
Hence |1/lambda_k(rho) - 1/lambda_k(sigma)| <= (R/4) ||rho-sigma||_1^{1/2},
and |lambda_k(rho) - lambda_k(sigma)| <= (R/4)(k^2 pi^2)^2 ||rho-sigma||_1^{1/2}
via P4.  Verified numerically (random rho, sigma in K).

## P6. Moving-jump FH derivative (repair R2 + R4) - DERIVED (this run)

For rho constant on a two-sided neighborhood of x_j with one-sided values
c_- (left), c_+ (right), c_- != c_+, define rho_eps with the jump at x_j + eps.
Then d/deps lambda_k(rho_eps)|_{eps=0} = lambda_k(c_+ - c_-) u_k(x_j)^2
(signed displacement; two-sided derivative exists), hence
d/deps D(rho_eps)|_{0} = -(c_+ - c_-) f(x_j), f = lambda_1 u_1^2 - lambda_2 u_2^2.
Equivalently, moving the jump right by delta changes D by
-(c_+ - c_-) f(x_j) delta + o(delta), moving left by +(c_+ - c_-) f(x_j) delta
+ o(delta).  Proof by smoothing (R4): rho_eps^delta = c_- + (c_+-c_-) H_delta
(x - x_j - eps) with H_delta a C^inf smoothed Heaviside, apply AEH Lemma 2.1
to the delta-family (d/deps rho_eps^delta in L1), pass delta -> 0 using
uniform convergence of eigenfunctions (H^2 bounds + Arzela-Ascoli) and
dominated convergence.  Verified numerically in verify_fh_sign.py.

## P7. Sturm oscillation (u_k has exactly k-1 simple interior zeros) - KNOWN (standard)

For -y'' = lambda rho y, rho bounded with rho >= c > 0, Dirichlet BCs on
(0,1), the k-th eigenfunction has exactly k-1 zeros in (0,1), all simple.
Classical; used for z_0 (the zero of u_2).  Verified numerically.

## P8. Keller 1976 / Mahar-Willner 1976 - KNOWN (context only)

- Keller, "The Minimum Ratio of Two Eigenvalues", SIAM J. Appl. Math. 31(3)
  1976, 485-491 (papers/keller1976.txt): min of lambda_2/lambda_1 over
  piecewise continuous phi, 0 < a <= phi <= A, y'' + lambda phi y = 0,
  y(+-1/2) = 0; minimizer piecewise constant = a on (-x_0,x_0), A elsewhere.
- Mahar-Willner, "An Extremal Eigenvalue Problem", CPAM 29 (1976) 517-529
  (papers/mw1976.txt): over piecewise continuous phi with BOUNDED NUMBER OF
  JUMPS and 0 < a <= phi <= 1: Theorem 0 (Keller): extremizing function
  piecewise constant with values a,1; Theorem 1: no jumps or exactly two;
  Theorem 2: symmetric about 0; Theorem 3: periodic extension for lambda_{2n}/lambda_n.
Class difference: Keller/MW treat the RATIO in the bounded-jump class; O1
treats the GAP over the full measurable box class.  O1 is NOT a corollary of
Keller/MW; the N-jump approximation ladder (O1d/O1e) is needed.  No premise
obligation for O1 arises from P8; role is structural template and novelty
context.

## Known-theorem map (current status)

- Box-class gap SUP/INF reduction to 2-parameter families: target of O1
  (this run).  Draft PROVED with two repairable defects (O1a, O1b); audit
  verdict REPAIRABLE_GAP; this run delivers the revised proof.
- Symmetric 1-parameter analysis (O2) and 2-parameter symmetry (O3): out of
  scope of this run (packet scope = O1 only), listed in the obligation graph
  for context.
- Related published results: AEH 2024 minimize the gap over the
  single-barrier class (monotonicity constraint), not the box class; their
  Lemma 2.2 is class-free and is the source of the f-structure lemma.
  El Allali-Harrell 2022 (PAMS 150) minimize the gap over single-well V.
  Ashbaugh-Benguria 1989/1993, Lavine 1994: gap bounds for Schrodinger
  classes.  Huang 2007, Sun 2022: gap for strings, different classes.
- Novelty status of the O1 theorem: POTENTIALLY_NEW (pending Phase 11
  literature search); not found in the local sources P1-P8.

## Recheck verdicts for the packet's required repairs

- R1 (S_rho presentation): sound after the operator-formula correction above.
- R2 (sign): confirmed; the audit's sign and the draft's signed-derivative
  statement are reconciled; see P6 and obligation O1b.
- R3 (u_2 sign convention): trivial, adopted from AEH.
- R4 (approximation): provided in P6; the audit's "minor" classification is
  confirmed as standard but must be written out (it is, in this run).

## Novelty status (Phase 11, completed in the 2026-08-06 continuation session)

Supersedes the provisional "POTENTIALLY_NEW (pending Phase 11)" line in the
known-theorem map above.  Verdict: the O1 reduction theorem (SUP/INF over the
full measurable box class K equals SUP/INF over the 2-parameter barrier/well
families) is classified POTENTIALLY_NEW; the strongest known competitor, Sun
2022, is a MINIMUM-gap theorem over a STRICTLY NARROWER density class and does
not treat the SUP side.  Exact details and honesty caveats below.

### N1. Sun 2022 - full record retrieved from zbMATH Open API

Sun, Hongli, "On the minimum eigenvalue gap for vibrating string", J. Math.
Anal. Appl. 516 (2022), No. 1, Article 126513, 19 pp., Zbl 1506.34110,
DOI 10.1016/j.jmaa.2022.126513.  Closed access (OpenAlex is_oa = false; no
repository fulltext).  Record and review saved in this run under
research_cache/sun2022_zbmath.json (+ parsed text) and
research_cache/sun2022_openalex.json, research_cache/sun2022_crossref.json.

zbMATH Open review (reviewer Erdogan Sen, sign "Erdogan Sen (Tekirdag)"),
retrieved 2026-08-06 from api.zbmath.org (an:1506.34110):
  "In this paper, following [J. Qi et al., Qual. Theory Dyn. Syst. 19, No. 1,
  Paper No. 12, 15 p. (2020; Zbl 1456.34022)], the author deals with the
  minimum eigenvalue gap of the first two eigenvalues for rho(x), where
  rho(x) is piecewise continuous with a bounded of jumps.  Contrary to
  previous works in the literature, in this paper, the author considers a
  more general case of this density function."
(Quoted from the zbMATH JSON; "a bounded of jumps" is a typo in the review
for "a bounded number of jumps".)

Abstract sentence (ScienceDirect snippet, via search index, 2026-08-06):
  "The eigenvalue gap Gamma(rho) attains its minimum on each of the classes
  of S1 and S2 by rho0."
So Sun's main theorem is a MINIMUM (INF side) result over two classes S1, S2,
in the piecewise-continuous bounded-jump class, following the Qi-Li-Xie
approach.

### N2. Why this does not preempt O1

- Class: Sun's density class is piecewise continuous with a bounded number of
  jumps (per the zbMATH review); O1's class K is the full measurable box class
  1 <= rho <= R a.e.  These are DIFFERENT classes.  O1's theorem is stated for
  the full measurable class, and the reduction (sup_K D = sup_{K_2} D, inf_K D
  = min over the well family) is what makes the measurable class collapse to
  2-jump configs; this reduction step is not in Sun's paper (not claimed).
- Side: Sun treats the MINIMUM gap only; the SUP side (sup_K D = max over the
  barrier family) and the reduction theorem for the SUP side are NOT treated
  by Sun (per the review and the abstract).  No source treating sup_K D over
  the measurable box class was found in Phase 11.
- INF side: Sun's minimum-gap theorem over the bounded-jump class is
  compatible with O1's INF statement: O1 proves inf_K D = min over the well
  family, and the well family lies in the bounded-jump class, so the VALUE
  inf_K D coincides with the minimum over the bounded-jump subclass (which is
  what a bounded-jump-class theorem could pin down).  Whether Sun's S1/S2
  minimizers coincide with O1's well-family minimizers is NOT established
  here: the exact definitions of S1 and S2 are UNKNOWN (see N3), so O1's INF
  side is reported honestly as: new as stated over the full measurable class;
  possibly-known value for the bounded-jump subclass; identification with
  Sun's S1/S2 NOT_VERIFIABLE from public metadata.
- SUP + reduction: POTENTIALLY_NEW.  This is the honest classification.

### N3. S1/S2 definitions: UNKNOWN (access log)

Determination attempts for the exact definitions of S1 and S2 (2026-08-06):
- zbMATH Open API full record (200): review and reference list retrieved; the
  review does not define S1/S2.
- ScienceDirect landing page and r.jina.ai proxy: blocked (connection
  closed / connection failed).
- Peeref works/26609210: login wall.
- Semantic Scholar Graph API: HTTP 429 on two attempts (rate-limited).
- OpenAlex works/doi:10.1016/j.jmaa.2022.126513 (200): no abstract
  (abstract_inverted_index absent), is_oa false, no fulltext.
- Crossref works/10.1016/j.jmaa.2022.126513 (200): no abstract field.
- MaRDI portal Publication:2166449 (200): metadata page with no abstract.
- zbMATH pdf/07574902.pdf: HTTP 403.
- Web search: only the abstract sentence in N1 is exposed; no S1/S2
  definition text found.
Conclusion: the exact S1/S2 classes are NOT_VERIFIABLE from public metadata.
The zbMATH review's class description (piecewise continuous, bounded number of
jumps) suffices for the honest novelty verdict in N2; nothing in the available
record indicates a box-class SUP result.

### N4. Related sources checked in Phase 11 (2026-08-06 continuation)

- Qi, Li, Xie, "Extremal problems of the density for vibrating string
  equations with applications to gap and ratio of eigenvalues", Qual. Theory
  Dyn. Syst. 19 (2020), No. 1, Paper No. 12, Zbl 1456.34022 (zbMATH record
  saved research_cache/qi2020.json): per its review, it obtains the INFIMUM
  OF THE DENSITIES in terms of gap and ratio of the first two eigenvalues
  (generalized Lyapunov inequality).  This is a density-infimum result, NOT a
  gap-extremization over a box class; different direction from O1.  Sun
  "follows" this paper in approach.
- Sun, Yang, "The fundamental gap of a kind of sub-elliptic operator", Zbl
  1521.34080 (zbMATH record saved research_cache/sun_subelliptic.json): review
  text license-blocked; sub-elliptic operator gap paper; its reference list
  (Harrell-El Allali 2022, Andrews-Clutterbuck 2011, Ashbaugh-Svirsky-Harrell
  1991, Horvath 2003, Chen-Huang 2012, Huang-Tsai 2009) confirms the
  single-well/fundamental-gap tradition; no box-class gap extremization.
- AEH published version: Ahrami, El Allali, Harrell II, "On the fundamental
  eigenvalue gap of Sturm-Liouville operators", Arch. Math. (Basel) 126 (2026),
  No. 2, 187-197, DOI 10.1007/s00013-025-02213-y (confirmed via search index
  and EBSCO records, 2026-08-06).  Same content family as arXiv:2407.02459v2
  (the premise source used here); it minimizes the gap over a monotonicity/
  shape-constrained class (single-well potential, single-barrier density),
  not over the box class.
- Keller 1976 / Mahar-Willner 1976 / Willner-Mahar 1982 / Huang 1999 /
  Hedhly 2021 (prior sessions): ratio problems in bounded-jump classes; not
  competitors for the box-class gap reduction.  See P8 and the summary docs.

### N5. Final novelty verdict for O1

- sup_K D = max over the barrier family, over the FULL measurable box class:
  POTENTIALLY_NEW (no source found).
- inf_K D = min over the well family, over the FULL measurable box class:
  POTENTIALLY_NEW as stated; the VALUE may coincide with Sun 2022's minimum
  over the bounded-jump subclass (identification with S1/S2 NOT_VERIFIABLE).
- The reduction mechanism itself (L^1 continuity + N-jump approximation ladder
  + bang-bang at extremizers): no published counterpart found in Phase 11.
- Honesty caveat: absence of a found source is not a proof of novelty; the
  classification POTENTIALLY_NEW/UNKNOWN is reported to the manager with the
  exact reasoning above.
