# Problem Contract: Left-Definite DensBC O1' Specialization — structural constrained polynomial density in H^s[-1,1]

Run root: runs/rigorous-open-math-research/R-20260816T120000Z-leftdef-density/
Task packet: agenda/task-packets/Q-20260816-leftdef-density-E5F6A7B8.md (project context, NOT a verified theorem contract)
Upstream: R-20260814T070000Z-densbc-3F8A2C (status RIGOROUS_PARTIAL_RESULT; O1 open) and
          R-20260816T000000Z-densbc-o1 (status RIGOROUS_PARTIAL_RESULT; reduced core O1' open).
This-run: independent normalization + audit; STRICT structural theorems scoped to
          s in {1,2,3}; a decisive negative structural finding for s >= 4 recorded honestly.

## 0. Provenance and scope

- Authoritative problem: task packet Q-20260816-leftdef-density-E5F6A7B8 (project
  context, not a verified theorem contract).  It asks to specialize/advance DensBC
  O1' to left-definite spaces H^s[-1,1] (Krein inner product, s >= 1) with
  structural/boundary constraints, and to:
  1. decide when O1' is decidable by finite data in the left-definite class;
  2. give the concrete first-obstruction degree / free-base characterization;
  3. recover the known full-space completeness results (H^s complete, integer s>=1)
     as the unconstrained case V = H.
- Web narrative sweep (2026-08-16): no published exact criterion for polynomial
  density in constrained subspaces of the left-definite/Krein spaces with the
  gapped sparse family surfaced.  Novelty: POTENTIALLY_NEW (not claimed open as a
  fact; deeper literature audit recommended).

## 1. Normalized objects and definitions (after independent audit + correction)

- K_c f = -f'' + c f (c > 0) on L^2(-1,1), D(K_c) = { f,f' in AC, f'' in L^2,
  f'(+1) = f'(-1) = (f(1)-f(-1))/2 } (Krein BC).  Self-adjoint, positive, 0 notin sigma.
- H^s = D(K_c^{s/2}), (f,g)_s = (K_c^{s/2}f, K_c^{s/2}g)_{L^2}, s integer >= 1.
  THIS RUN uses the OPERATOR-DOMAIN interpretation H^s = D(K_c^{s/2}) (the one used
  in the project's concrete H^2/H^3 proofs).  Isometry (transfer): K_c : H^t -> H^{t-2}.
- Sparse family: p_0=1, p_1=x, p_{2m}=x^{2m}-(m/(m-1))x^{2m-2},
  p_{2m+1}=x^{2m+1}-(m/(m-1))x^{2m-1} (m>=2); index D = {0,1} ∪ {n>=4}.

## 2. Structural facts (EXACT, AUDIT-CORRECTED)

- S1a. s=2: H^2 ∩ C[x] = span{p_n}; only monomials 1,x in H^2; all p_n in H^2.
- S1b. s=3: H^3 ∩ C[x] = span{p_n}; all p_n in H^3.
- S1c. s in {1,2,3}: all p_n (n in D) lie in H^s.
- S1d. **s >= 4: the sparse p_n (n >= 4) are NOT in H^s.**  Exact: p_4 notin H^4
  because K_c p_4 fails the Krein BC (K_c p_4 = c x^4-(2c+12)x^2+4, its derivative
  at +1/-1 is -24/+24 while its endpoint difference is 0).  Hence H^s ∩ C[x] =
  span{1,x} for s >= 4 (only linear polynomials).  (p_0=1, p_1=x are in every H^s.)
- Consequences: DensBC O1 (H1) ("all polynomials in H, dense") FAILS for s >= 2;
  monomial moments <w,x^k>_s exist only for k=0,1 when s >= 2; and for s >= 4 the
  sparse family is not even a subset of H^s.

## 3. Target conclusion (CORRECTED SCOPE)

Give an exact, verifiable account of closure(span{p_n in V}) = V in H^s that:
(a) correctly handles the structural absence of x^k (k>=2) for s>=2, AND the
    absence of the entire sparse family from H^s for s >= 4;
(b) decides when O1' is finite-data decidable in the class;
(c) gives the first-obstruction / free-base picture;
(d) recovers the full-space result correctly: scoped to s in {1,2,3} via the
    sparse family (L1'), and honest about the s >= 4 failure (L1'').

## 4. Quantifiers

- s, c fixed; all constants depend on s, c, V, and the bounded constraint
  functionals.  V may be finite-codimension (FORM (a)) or general closed.

## 5. Equivalent formulations (audited)

- (Master, DensBC Theorem A) closure(span Q_sp) = V iff V ∩ Q_sp^perp = {0}.
- (Projection density, structural; s in {1,2,3}) P_V(W_s) dense in V, W_s=span{p_n}.
- (Transfer descent, s>=2) problem descends isometrically to H^{s-2}; iterates to
  H^{s'}, s' in {0,1}.
- (s >= 4 whole-space) Q_sp = {1,x}, closure(span Q_sp) = span{1,x} != H^s (L1'').

## 6. Boundary and degenerate cases (CORRECTED)

- s in {1,2,3}: all p_n in H^s; whole-space density holds (L1'); proper V analysis
  as in DensBC O1 adapted; L5 concrete non-density instance at s=2.
- s >= 4: sparse family not a subset of H^s; whole-space Q_sp = {1,x}, density
  fails (L1'').  Full-space completeness of H^s is via the DIFFERENT SL_hs system
  {Q_n^{(s)}}; membership of {Q_n^{(s)}} in D(K_c^{s/2}) for s >= 4 is flagged
  open/ambiguous (operator-domain vs abstract-completion reading).
- V = {0}: trivial.  V = H^s: L1'/L1''.  N empty: DensBC Lemma 6.1.

## 7. Permitted outcomes

- affirmative density results for s in {1,2,3} and concrete V;
- exact structural theorems + honest reduced core / transfer;
- negative / structure results (L1'' for s>=4; L5 for ker(Delta)); 
- precise reduction descending O1' to H^{s'}.

## 8. Completion criteria

1. Normalized statement handling structural absence of x^k (k>=2) AND the s>=4
   sparse-family absence.  [MET by S1a-S1d]
2. Structural projection density + "all p_n in V => V=H^s" (s in {1,2,3}).  [L2,L4]
3. Transfer descent to H^{s'} with correct moment base.  [L3]
4. Whole-space recovery, correctly scoped: s in {1,2,3} dense (L1'); s>=4 fails (L1'').  [MET]
5. Honest O1' status / O1'LD.  [L6]

## 9. Answer space

Supports the decision for H^s and a closed constrained V: decide density; give
the first obstruction; state the honest O1' status; and (new) report the s>=4
sparse-family failure.  STRICT vs EVIDENCE distinguished.

## 10. Acceptance criteria

- Structural facts: exact-arithmetic verified + audited (S1d is the decisive new check).
- L1'/L1'': STRICT proofs (L1' s in {1,2,3}; L1'' s>=4 negative).
- L5: STRICT (parity + boundary + orthogonality).
- L3: STRICT (isometry transfer).
- L6: honest; O1'LD open.

## 11. Results that do not count as completion

- Numerical verification of a candidate criterion (EVIDENCE only).
- Claiming O1' finite-data decidable in general (open).
- Claiming the sparse family recovers H^s for s >= 4 (FALSE; L1'').
- Claiming DensBC O1 monomial-moment machinery transfers to s >= 2 (false: (H1) fails).

## 12. Forbidden moves

- Numerical evidence presented as proof.
- Silent quantifier/domain changes (e.g. assuming x^k in H^s for k>=2, s>=2, or
  p_n in H^s for s>=4).
- Claiming "solved" while O1'LD open.
- Using the DensBC O1 (H1) beyond its domain.

## 13. Tool, citation, search constraints

- Python C:\Users\HuangZY\AppData\Local\Programs\Python\Python310\python.exe,
  PYTHONUTF8=1; sympy exact arithmetic (EVIDENCE).
- No git commit/push (per user; manager syncs at stage close).
- Novelty claims require a status/literature note with fetch status.

## 14. Ambiguities / competing interpretations (RESOLVED)

- (14a) DensBC O1 monomial-moment machinery in H^s (s>=2): does NOT transfer
  verbatim (H1 fails; x^k absent for k>=2, and p_n absent from H^s for s>=4).
- (14b) Structural constraints: the Krein BC / absence of x^k (and, for s>=4, of
  the sparse family) is PART of H^s; V is an ADDITIONAL closed constraint.
- (14c) O1' finite-data in the class: decided for V=H^s (s in {1,2,3} dense;
  s>=4 non-dense via L1''); general proper V descends to H^{s'} and remains a
  genuine moment problem (O1'LD open).
- (14d) NEW: the SL_hs orthogonal system {Q_n^{(s)}} (s>=4) membership in the
  operator domain D(K_c^{s/2}) — flagged OPEN (operator-domain vs abstract
  completion reading).

## 15. Contract audit

- Built independently from: task packet; DensBC O1 problem_contract/candidate
  proof/audit report; DensBC original candidate (Theorems A-H/E); docs
  SL_h2/h3/hs/denseness_criteria.  Corrected after independent re-verification:
  the earlier S1 equality for s>=4 and L1 s>=4 were invalid (exact counterexample
  p_4 notin H^4).  STRICT results scoped to s in {1,2,3}; s>=4 recorded honestly.
- EVIDENCE (exact) corroborates; STRICT claims stand on their own proofs.
