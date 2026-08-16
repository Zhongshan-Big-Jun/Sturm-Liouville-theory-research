# Problem Contract: Left-Definite DensBC O1' Specialization — structural constrained polynomial density in H^s[-1,1]

Run root: runs/rigorous-open-math-research/R-20260816T120000Z-leftdef-density/
Task packet: agenda/task-packets/Q-20260816-leftdef-density-E5F6A7B8.md (project context, NOT a verified theorem contract)
Upstream: R-20260814T070000Z-densbc-3F8A2C (status RIGOROUS_PARTIAL_RESULT; O1 open) and
          R-20260816T000000Z-densbc-o1 (status RIGOROUS_PARTIAL_RESULT; reduced core O1' open).
This-run: independent normalization + audit of the exact statement; STRICT structural theorems
          for the left-definite specialization; honest O1' status.

## 0. Provenance and scope

- Authoritative problem is the task packet Q-20260816-leftdef-density-E5F6A7B8.
  It is treated as PROJECT CONTEXT, not as a verified theorem contract.
- The packet asks: specialize/advance the DensBC O1 reduced core `O1'`
  (realizability/membership of a free run-base moment sequence) to **left-definite
  spaces** `H^s[-1,1]` (Krein inner product, s >= 1) with structural/boundary
  constraints, and
  1. decide when O1' is decidable by finite data in the left-definite class;
  2. give the concrete first-obstruction degree / free-base characterization
     for the Krein spaces H^s with structural boundary constraints;
  3. recover the known full-space completeness results (`H^s` complete for all
     integer s >= 1) as the unconstrained case V = H.

- A web narrative sweep (2026-08-16) surfaces no published exact criterion for
  polynomial density in constrained (functional-kernel) subspaces of the
  left-definite/Krein spaces with the gapped sparse family; closest literature:
  Krein-Sobolev orthogonal polynomials (Jones--Littlejohn--Quintero Roba, Axioms
  14 (2025) 115), left-definite theory (Littlejohn--Wellman, JDE 181 (2002)),
  exceptional orthogonal polynomial completeness (Gomez-Ullate et al.). None
  settles the finite-data decision in this class. Novelty status: POTENTIALLY_NEW
  (needs deeper literature audit before claiming NEW; see status_and_literature.md).

## 1. Objects and definitions (NORMALIZED after independent audit)

- `K_c f = -f'' + c f` (c > 0) on L^2(-1,1), D(K_c) = { f,f' in AC, f'' in L^2,
  f'(+1) = f'(-1) = (f(1)-f(-1))/2 } (Krein boundary condition).
  K_c self-adjoint, positive, 0 not in sigma(K_c).
- Left-definite scale: H^s = D(K_c^{s/2}), (f,g)_s = (K_c^{s/2}f, K_c^{s/2}g)_{L^2},
  s >= 1 integer (this run; fractional 3/2 <= s < 2 is inherited open O3).
  Isometry (transfer): K_c : H^t -> H^{t-2} is an isometric isomorphism for t >= 2,
  and (f,g)_t = (K_c f, K_c g)_{t-2}.
- Sparse family (project basis): p_0 = 1, p_1 = x,
  p_{2m} = x^{2m} - (m/(m-1)) x^{2m-2}, p_{2m+1} = x^{2m+1} - (m/(m-1)) x^{2m-1}
  (m >= 2).  Index set D = {0,1} union {n >= 4}.
- **STRUCTURAL FACT (audited + exact-arithmetic verified):**
  For integer s >= 2, H^s ∩ C[x] = span{ p_n : n in D }, and the ONLY monomials
  in H^s are 1 and x; i.e. x^k is NOT in H^s for all k >= 2.
  (Verified for s = 2 by the Krein boundary condition; higher s by embedding
  H^s ⊂ H^2.)  For s = 1 (=H^1, Sobolev-type), ALL monomials lie in H^1.
  - **Consequence:** the DensBC O1 hypothesis (H1) "all polynomials in H and
    dense in H" is FALSE for H^s (s >= 2); the monomial moments
    M_k(w) = <w, x^k>_s are defined ONLY for k = 0,1 when s >= 2.

- Constrained subspace: V a closed linear subspace of H^s.  The packet's
  "boundary/structural constraints" are modeled as V closed; natural instances:
  FORM (a) V = Intersection ker L_j (bounded functionals), or structural
  subspaces.  (Note: the structural constraint "x^2,x^3 absent" is BAKED INTO
  H^s itself for s >= 2; it is not an extra V.)
- Candidate family: Q_sp = { p_n : p_n in V } (kept sparse elements in V).
  N = { n in D : p_n in V }.

## 2. Hypotheses

- H = H^s, s integer >= 1, c > 0 fixed.  (Concretely instantiated Krein scale.)
- V closed subspace of H^s (the additional constraint).
- No assumption that Q_sp is dense in V; that is exactly the question.
- The general DensBC O1 theorems (O1 candidate_proof.md Theorems 1-5, reduced
  core O1') and DensBC original (Theorems A-H, Theorem E) are used as audited
  upstream results where their hypotheses hold; in the left-definite class their
  monomial-moment machinery requires re-audit (see Section 6).

## 3. Target conclusion

Give an exact, verifiable criterion / honest account for
    closure(span Q_sp) = V   in H^s
that (a) correctly handles the STRUCTURAL absence of x^2,x^3 (and all x^k,
k>=2) for s >= 2; (b) decides when the DensBC O1' core is finite-data decidable
in this class; (c) gives the first-obstruction / free-base picture; (d) recovers
the full-space result V = H^s (all integer s >= 1).

A satisfactory answer must:
1. NORMALIZE the transfer of the DensBC monomial-moment machinery to H^s
   (correct moment base), and state precisely where it applies vs. degenerates.
2. Give the structural projection-density statement P_V(span{p_n}) dense in V.
3. Characterize the obstruction V ∩ Q_sp^⊥ and, for natural constrained V,
   give concrete density / non-density decisions.
4. State the honest status of O1' in the left-definite class (finite-data
   decidable vs. genuine moment problem), WITHOUT claiming closure if open.

## 4. Quantifiers and dependency of constants

- s, c fixed; all constants may depend on s, c, V, and the (bounded) constraint
  functionals.  V may be finite-codimension (FORM (a)) or general closed.
- N, Q_sp determined by the constraint data.

## 5. Equivalent formulations (audited)

- (Master, DensBC Theorem A, STRICT upstream) closure(span Q_sp) = V
  iff V ∩ Q_sp^perp = {0}.
- (Projection-density, structural version - THIS run Theorem L2) P_V(W_s) is
  dense in V for every closed V ⊆ H^s, where W_s = span{p_n} is dense in H^s.
  Hence closure(span Q_sp) = V iff the excluded projections P_V(p_n) (p_n notin V)
  are redundant relative to Q_sp.
- (Transfer descent - THIS run Theorem L3) For s >= 2 the problem
  "closure(span{p_n in V}) = V" in H^s is isometrically equivalent to
  "closure(span{K_c p_n : K_c p_n in K_c V}) = K_c V" in H^{s-2}; iterating it
  descends to H^{s'} with s' in {0,1}, where all monomials are present and the
  honest moment base is the SECOND-order jump recursion
  c N_{2m} = A_m N_{2m-2} - B_m N_{2m-4} (NOT the DensBC first-order run
  recursion M_{2m} = (m/(m-1)) M_{2m-2}).

## 6. Boundary and degenerate cases (including the DensBC O1 (H1) failure)

- s = 1: all monomials in H^1; monomial moments M_k all defined; DensBC O1
  Theorems 2-3 apply verbatim (with M_{2m} = (m/(m-1)) M_{2m-2} first-order
  recursion); first/moment + jump growth force density for V = H^1.
- s >= 2: x^k not in H^s for k >= 2; only M_0, M_1 defined; the DensBC O1
  monomial-moment run/free-base analysis DEGENERATES and does not transfer
  verbatim.  The correct base is via transfer to H^{s-2} (Theorem L3).
- V = {0}: trivial; closure = {0} = V.
- V = H^s: Q_sp = {p_n} (all in V), density holds (project completeness);
  no first obstruction survives.
- N empty: Q_sp empty => closure = {0}; density iff V = {0} (DensBC Lemma 6.1).
- **Concrete non-density instance (STRICT, THIS run Theorem L5):** V = ker(Delta),
  Delta f = f(1)-f(-1) (bounded functional on H^2).  Then Q_sp = {p_0} ∪ {p_{2n}},
  and q = p_5 - 2 p_7 in V ∩ Q_sp^perp, q != 0, so closure(span Q_sp) != V.

## 7. Permitted outcomes

- affirmative proof of density for identified subclasses (e.g. V = H^s);
- exact structural theorems + honest reduced core / transfer;
- negative / structure results with concrete obstructions (e.g. Theorem L5);
- precise reduction descending O1' to H^{s'}, s' in {0,1}.

## 8. Completion criteria

1. Normalized statement handling the structural absence of x^k (k>=2) [MET: Sections 1,6].
2. Structural projection density + "all p_n in V => V = H^s" [MET: Theorem L2, L4, STRICT].
3. Transfer-descent reducing the constrained problem to H^{s'} (s' in {0,1}),
   with the correct second-order moment base [MET: Theorem L3, STRICT].
4. Whole-space recovery V = H^s for all integer s >= 1 [MET: Theorem L1, STRICT].
5. Honest O1' status: finite-data decidable where proved; genuine moment problem
   flagged otherwise [MET: Theorem L6, STRICT conditional + honest open core O1'LD].

## 9. Answer space

The deliverable supports the decision: for H^s and a closed constrained V, decide
density; give the first obstruction and the honest status of the remaining
moment-problem core.  It must distinguish STRICT (proved) from EVIDENCE
(computed) and never present numerical checks as closure.

## 10. Acceptance criteria per subproblem

- Structural normalization: audited against SL_h2/h3/hs docs + exact arithmetic.
- V = H^s recovery: consistent with project completeness theorems (STRICT).
- Concrete non-density instance: STRICT proof (parity + boundary + orthogonality).
- Transfer descent: STRICT proof using K_c isometry + polynomial identity.

## 11. Results that do not count as completion

- Numerical verification of a candidate criterion (EVIDENCE only).
- Claiming O1' is finite-data decidable in general (false/unknown): it is open;
  only whole-space V = H^s and the concrete instances are decided.
- Claiming the DensBC monomial-moment machinery transfers verbatim to s >= 2
  (false: (H1) fails structurally).

## 12. Forbidden moves (discipline)

- Numerical evidence presented as proof.
- Silent quantifier/domain changes (e.g. assuming x^k in H^s for k>=2, s>=2).
- Claiming "solved" while any obligation (O1'LD) is open.
- Presenting the packet's framing as verified without re-audit.
- Using the DensBC O1 (H1) "all polynomials dense in H" beyond its domain.

## 13. Tool, citation, search constraints

- Python C:\Users\HuangZY\AppData\Local\Programs\Python\Python310\python.exe,
  PYTHONUTF8=1; sympy (exact rational arithmetic) for EVIDENCE.
- No git commit/push (per user: manager syncs at stage close).
- Novelty claims require status/literature note with fetch status.

## 14. Ambiguities or competing interpretations (RESOLVED)

- (14a) Does DensBC O1's monomial-moment machinery apply to H^s (s >= 2)?
  RESOLVED: NO as-is; (H1) fails; only transfer to H^{s'} (s' in {0,1}) makes
  the moment base legitimate.  This is the honest resolution of the packet's
  "structural constraints" ambiguity.
- (14b) Are "structural boundary constraints" part of H^s or an extra V?
  RESOLVED: the Krein BC / absence of x^2,x^3 IS part of H^s (s >= 2); the run
  treats V as an ADDITIONAL closed constraint on top of H^s.
- (14c) Is O1' finite-data decidable in the left-definite class?
  RESOLVED PARTIALLY: for V = H^s yes (proved: no obstruction); for general
  proper V it descends to H^{s'} (s' in {0,1}) and remains a genuine moment
  problem (O1'LD open) unless the constraint data are finite/structured.

## 15. Contract audit

- Contract built independently from: task packet; DensBC O1 problem_contract.md
  + candidate_proof.md + audit_report.md; DensBC original candidate_proof.md
  (Theorems A-H, Theorem E); docs/SL_h2_completeness_proof.tex,
  SL_h3_completeness_proof.tex, SL_hs_orthogonal_systems_proof.tex,
  SL_denseness_criteria.tex.
- No verbatim theorem copied; upstream audited results cited by run/name.
- The packet's "left-definite inner product nontrivial in monomial basis" risk is
  confirmed and sharpened: for s >= 2 the monomials x^k (k>=2) are absent, so the
  naive moment matrix is not even defined; the correct base is H^{s'} (s' in {0,1}).
- EVIDENCE (exact rational) corroborates structural facts; STRICT claims stand on
  their own proofs.
