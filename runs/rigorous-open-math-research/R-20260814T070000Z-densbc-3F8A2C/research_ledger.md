# Research Ledger

Run: R-20260814T070000Z-densbc-3F8A2C

## Phase 0-1: Normalization and first core finding (2026-08-14)

- Read task packet Q-20260814-densbc-3F8A2C and project matrices
  (docs/SL_denseness_criteria.tex, tools/denseness-criteria.md,
  tools/moment-jump-completeness.md). Verified source-bundle sha256 all match.
- Wrote problem_contract.md (two formal forms: (a) V = intersection of kernels of
  finitely many continuous functionals, (b) arbitrary closed subspace; master
  Hahn-Banach criterion; sparse family {p_n}).
- Ledger on the packet's KEY MECHANISM claim:
  "V = span{x^2,x^3}^\perp in H_beta. Then any w in V orthogonal to {p_n} has
  M_2 = M_3 = 0, so M_{2m} = m M_2 = 0 for all m, hence w = 0; density for EVERY beta."

  CONCERN: this assumes the recursion M_{2m} = m M_2 holds for ALL m. But that
  recursion comes from (w, p_{2m}) = 0, which requires p_{2m} in the candidate
  family. p_4 = x^4 - (4/3)x^2 has a degree-2 term, and x^2 in V^\perp means
  p_4 NOT in V. Hence p_4 is NOT a kept test vector, (w,p_4)=0 is not available,
  and M_4 is NOT locked to M_2 by any constraint. M_4 becomes a FREE parameter.

  R-001 (DISCOVERY): The packet's example is FALSIFIED. For beta > 3/2, density
  of the kept sparse family in V = span{x^2,x^3}^\perp FAILS. The free moment
  parameters shift from M_2, M_3 to M_4, M_5 (the next unconstrained base
  degrees above the constrained ones). A nonzero w with
    M_2 = M_3 = 0, M_4 = free (= (2/2) c), M_{2m} = (m/2) M_4 for m >= 2,
    M_5 = free, M_{2m+1} = (m/2) M_5 for m >= 3,
  lies in H_beta (series sum_m (m/2)^2(2m+1)^(-2b) converges for b>3/2) and is
  orthogonal to every KEPT p_n.
  Evidence: scripts/densbc_v1_verify_free_params.py confirms for the full
  two-parameter w: inner product with every kept p_n is 0 (max ~7e-15), and the
  H_beta norm partial sums saturate for beta in {1.6, 2.0, 3.0}.

- R-002 (on the mechanism, general form): The packet mechanism is CORRECT only
  when the recursion is NOT broken, i.e. when ALL sparse p_n lie in V AND
  x^2, x^3 in V^\perp (free params pinned). In that case density holds for every
  beta. The diagonal coordinate example fails because p_4 not in V (recursion
  broken).  In the diagonal/coordinate setting the mechanism is never active and
  the sparse family is never dense for beta > 3/2 (see diagonal classification).

## Phase 2: Diagonal-space complete classification (2026-08-14)

- Developed the complete classification for H_beta (diagonal, (x^j,x^k)=
  delta_jk(k+1)^{2b}), V = span{e_{j1},...,e_{jm}}^\perp, coordinate constraint
  set R = {j1,...,jm} (w in V iff w_i = 0 for i in R).
- See approach_registry.md + candidate_proof.md for statements; the crux:
  kept sparse p_n are those with no support degree in R. The recursion graph on
  even degrees has maximal runs of unconstrained evens as components; each run
  carries one free parameter y; a nonzero orthogonal w exists iff some run's
  series sum_m (m y)^2 (2m+1)^(-2b) converges. Infinite runs converge for b>3/2;
  finite runs converge trivially (finite support). Since R finite, there is
  always an infinite top unconstrained run on the even side (and odd side), so
  for b > 3/2 the sparse family is NEVER dense in any such V.
- R-003: For beta > 3/2 and ANY finite coordinate-constraint subspace V
  (including the packet's span{x^2,x^3}^\perp), the kept sparse family is NOT
  dense in V. The only dense case is beta <= 3/2.

## Phase 3: Literature (in progress; updates as subagents land)

- R-004 (Berg-Christensen AIF 1981, deep-read complete): Target is density of
  polynomials in the WHOLE L^p(R,mu). Criterion: Naimark L^1 (extreme point of
  V^mu, iff determinate); M. Riesz L^2 iff mu is N-extremal; determinate => dense
  in L^p for 1<=p<=2 only. It contains NO theorem on density in a CLOSED PROPER
  SUBSPACE of a Hilbert space and NO boundary-condition/linear-side-constraint
  result. All "orthogonal to P => zero" arguments are in the whole L^p.
  IMPLICATION: any claim that BC1981 proves boundary-constrained polynomial
  density would be over-reading. It supplies methods (moment-functional inner
  product, reproducing kernel of the moment functional, N-extremality dichotomy)
  but no constrained-subspace theorem. Strong novelty support for the constrained
  program. Cite: C. Berg, J.P.R. Christensen, Ann. Inst. Fourier 31(3) (1981)
  99-114, DOI 10.5802/aif.840 (Zbl 0437.42007, MR 84i:44006).
  Detail: tmp_ai4math/densbc_lit/berg_christensen_DEEPREAD.md

## Phase 2.5-3: Diagonal classification refinement, evidence, literature (2026-08-14)

- R-005 (CORRECTED DIAGONAL CLASSIFICATION - CROWN RESULT): The packet's naive
  "constraints restore density for every beta" is subtly WRONG in two ways:
  (a) For beta > 3/2 the kept sparse family is NEVER dense in any finite
      coordinate-constraint subspace V (even the packet's span{x^2,x^3}^perp).
      Because p_4 = x^4 - (4/3)x^2 involves degree 2, so p_4 NOT in V; the
      recursion M_4 = (4/3) M_2 is broken and M_4 becomes a FREE parameter.
      The free base shifts to the top infinite unconstrained run; for beta>3/2
      its series sum_m (my)^2(2m+1)^(-2b) converges => nonzero orthogonal w in
      H_beta.  Verified for 12 constraint sets at beta in {1.6,2.0,3.0}
      (scripts/densbc_v3_diagonal_universal.py): all produce a finite-norm
      orthogonal w (max inner product ~1e-13).

  (b) Even MORE subtle: for beta <= 3/2, constraints can still DESTROY density
      via a "finite run" phenomenon.  A bounded maximal interval of consecutive
      unconstrained same-parity degrees is a recursion component with a free
      parameter; since it has FINITE support, the associated w is in H_beta for
      EVERY beta, and is orthogonal to all kept p_n.  So e.g. R={4} leaves
      degree 2 as a finite singleton run (M_2 free) => NOT dense at beta<=3/2.
      Confirmed (scripts/densbc_v4/v5 ...): R={4},{2,6},{4,8},{5},{3,9},{3,7}
      yield finite-support orthogonal w at beta in {1.0,1.4,1.5}.

  CORRECTED DIAGONAL THEOREM (to be proven strictly):
    kept sparse family dense in V (coordinate R, finite)
      <=>  beta <= 3/2  AND  R creates NO finite run.
    finite even run <=> exists constrained even 2q>=4 with 2q-2 not in R;
    finite odd run  <=> exists constrained odd 2q+1>=5 with 2q-1 not in R.
    (So R={2,3},{2,4},{2},{3},{2,3,4} etc are dense at beta<=3/2; R with an even
     >=4 not backed by 2, or odd >=5 not backed by 3, is NOT dense at ANY beta.)
  Verified (scripts/densbc_v5_classification_verdict.py): all 11 test R agree.

- R-006 (mechanism, corrected general form): the packet's "constraints kill free
  params => density" mechanism is CORRECT only when the sparse recursion is NOT
  broken, i.e. ALL p_n in V (no p_n has a constrained degree in its support),
  AND M_2, M_3 pinned to 0 (x^2, x^3 in V^perp).  Under those two hypotheses the
  recursion forces all moments 0 => w=0 => dense, for EVERY beta.  This is
  exactly the concrete Krein H^s situation (whole space with structural
  constraints), NOT the coordinate subspace situation.

- R-007 (monomial candidate family in diagonal space): for coordinate R, the
  monomial family {x^k : k not in R} is an ORTHOGONAL basis of V (diagonal
  coordinates decouple), hence ALWAYS dense in V for every beta.  The failure of
  density is specific to the SPARSE family {p_n}, not to monomials.

- Literature (deep-reads landing):
  R-004 Berg-Christensen AIF 1981: only whole L^p density (Naimark L1, M.Riesz
       L2 N-extremal); NO closed-subspace / boundary-constraint theorem.
  R-008 Dette-Zhigljavsky arXiv:2101.11968v5: OPPOSITE direction (determinate
       measure => nonzero constants/monomials NOT in the RKHS); NO constrained-
       subspace density criterion.
  R-009 Berg-Thill "Rotation invariant moment problems": Acta Math. 167 (1991)
       207-227 (NOT Math. Ann. 1992). Rotation-invariant determinate mu:
       polynomials not dense in L^2(mu) iff mu is spherical-atomic
       sum alpha_n omega_{r_n}. No constrained-subspace result. Full text
       paywalled (Project Euclid bot-block, sci-hub CAPTCHA); resting on zbMATH
       review by Leviatan.

- R-010 (Rodriguez JAT 2003 deep-read): The packet's JAT lead DOI
  10.1006/jath.2002.3709 actually resolves to "Weighted Sobolev Spaces on
  Curves" (Alvarez-Pestana-Rodriguez-Romera, JAT 119 (2002) 41-85), a DIFFERENT
  paper.  The stated-topic paper is J.M. Rodriguez, "Approximation by
  polynomials and smooth functions in Sobolev spaces with respect to measures",
  J. Approx. Theory 120 (2003) 185-216, DOI 10.1016/S0021-9045(02)00019-9
  (Zbl 1014.41007, MR1959864).  Central Thm 4.1: under coercivity, P dense in
  W^{k,p}(Delta,mu) iff P dense in L^p(Delta,mu_k) (L^p-reduction).  It treats
  density in the WHOLE space only; NO boundary-constrained / vanishing-on-boundary
  subspace result.  Transferable: L^p-reduction template + p-admissible measure
  language.  Detail: tmp_ai4math/densbc_lit/jat2002_shobolev_density_DEEPREAD.md

## Phase 4: Evidence scripts produced
- scripts/densbc_v1_verify_free_params.py (CORRECTED odd support)
- scripts/densbc_v2_diagonal_classify.py
- scripts/densbc_v3_diagonal_universal.py (beta>3/2 universal non-density, 12 R)
- scripts/densbc_v4_finite_run_phenomenon.py (finite-run phenomenon)
- scripts/densbc_v5_classification_verdict.py (corrected classification, 11 R)

## R-AUDIT (2026-08-14, coordinator-conducted; fresh-agent independence UNAVAILABLE)
- Fresh-agent adversarial audits attempted 3x (a79cd94f, 6133fa9a, cf0e9c26) + minimal spawn probe; all failed with 'subagent run failed' (agent-provider outage at audit time).  Audit performed by the coordinator with independent re-derivation; limitation recorded in audit_report.md header.
- Verdicts: A1/A2/A3/A4/A5/A6/A7/A8/A9/A10 PASS except F-densbc-01 (statement).
- F-densbc-01: Lemma 4.1 odd-run ratio formula M_{2m+1} = ((m+1)/b) M_{2b+1} with idx(2m+1)=m+1 is INCORRECT as stated; the recursion (w,p_{2m+1})=0 iterates to M_{2m+1} = (m/2) M_5 for odd lowest degree 5 (exact check M_11/M_5 = 5/2 vs stated 2; stated formula yields 37 exact violations on the R={2,3} counterexample, corrected chain 0).  Corrected uniform statement: M_k = (floor(k/2)/floor(L/2)) M_L within a run.  Theorem E thresholds and both falsifications UNAFFECTED (both ratios linear in m).
- Both packet conjectures falsified SOUNDLY (exact 0-violation re-verification): (a) R={2,3}, beta>3/2 non-density via free M_4/M_5 (p_4,p_5 not kept); (b) R={4} finite singleton run at degree 2 kills density at every beta.
- Verification script: scripts/_audit_densbc_coord.py (exact sympy, reproducible).
