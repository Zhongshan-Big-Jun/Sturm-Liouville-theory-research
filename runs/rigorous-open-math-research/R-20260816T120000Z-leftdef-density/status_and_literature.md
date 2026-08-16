# Status and Literature — Left-Definite constrained density (O1' specialization)

Run: R-20260816T120000Z-leftdef-density
Date: 2026-08-16

## Current status (this run)

This-run status label: RIGOROUS_PARTIAL_RESULT

STRICT structural results + a decisive negative finding:
- L1' (s in {1,2,3}): whole-space recovery V = H^s via the sparse family holds
  (density); scoped because p_n in H^s exactly for s in {1,2,3}.
- L1'' (s >= 4): the sparse family is NOT a subset of H^s under the
  operator-domain reading (H^s = D(K_c^{s/2})); H^s ∩ C[x] = span{1,x}; so
  Q_sp = {1,x} and closure(span Q_sp) = span{1,x} != H^s (density FAILS).
- L2/L4 (s in {1,2,3}): structural projection density; "all p_n in V => V = H^s".
- L3: transfer descent to H^{s'}, s' in {0,1}; clean 3-term jump base at r=1.
- L5: STRICT non-density instance V = ker(Delta) in H^2 (parity/boundary
  obstruction).
- L6: O1' decided for V = H^s (s in {1,2,3} dense; s>=4 non-dense) and L5;
  reduced core O1'LD OPEN for general proper V.
- NEW STRUCTURAL FINDING: the packet's Q3 premise "H^s complete for all integer
  s>=1 [via the sparse family]" is FALSE for s>=4 under the operator-domain
  reading; completeness of H^s is via the SL_hs system {Q_n^{(s)}}, whose
  membership in D(K_c^{s/2}) for s>=4 is flagged open/ambiguous.

Reduced unsolved core O1'LD (inherited O1' in the class): for a general proper
closed V ⊆ H^s (s in {1,2,3}; or surviving candidates for s>=4), decide whether
closure(span{p_n in V}) = V.  OPEN (honest).

## Known / DERIVED results used (project, audited)

- Sparse family dense in H^s: SOLID only for s in {0,1,2,3} (L1' via first-moment
  for s=1, SL_h2 for s=2, SL_h3 for s=3).  For s >= 4 the sparse family is not
  even contained in H^s (L1''), so the project's denseness_criteria Theorem 8
  "span{p_n} dense in H^s for all integer s" is FALSE / needs re-scoping under
  the operator-domain interpretation (its step (i) also uses undefined H^s-moments
  for s>=2, confirmed by independent audit).
- SL_hs orthogonal system {Q_n^{(s)}} complete in H^s (Legendre/Krein-Sobolev
  transported by K_c^{-r}): the PROJECT's completeness statement; its membership
  in the operator domain D(K_c^{s/2}) for s >= 4 is flagged open (L6/14d).
- DensBC master/moment machinery (Theorems A-H, O1 Theorems 1-5 + O1'): audited
  upstream, used where hypotheses hold.
- Left-definite theory (Littlejohn-Wellman), Krein-Sobolev (Jones-Littlejohn-
  Quintero Roba): KNOWN literature.

## Novelty / openness status (target problem)

Web narrative sweep (2026-08-16): no published exact criterion for polynomial
density in constrained (functional-kernel) subspaces of the left-definite/Krein
spaces with the gapped sparse family surfaced.  Closest: Krein-Sobolev (Axioms
2025), exceptional OPS completeness (Gomez-Ullate et al.), moment-problem
characterizations.  None settles the finite-data decision in this class.
- Fetch status: target hits abstract/title-level; none fetched-and-verified as
  settling the target.  Novelty = POTENTIALLY_NEW (not claimed open as a fact;
  deeper arXiv/zbMATH full-text pass recommended).
- NEW potential novelty: the structural finding that the sparse family is not even
  a subset of H^s for s >= 4 (operator-domain reading), and that span{1,x} is the
  surviving whole-space candidate, correcting the packet's Q3 premise for s >= 4.

## Classification

- Project-derived (audited): DensBC Theorems A-H/E, DensBC O1 Theorems 1-5;
  H^s completeness for s in {0,1,2,3} (L1').
- This-run STRICT: L1', L1'', L2, L3, L4, L5, L6 (scoped); S1a-S1d facts.
- OPEN: O1'LD; membership of {Q_n^{(s)}} (s>=4) in D(K_c^{s/2}); O2'; O3.
- EVIDENCE (exact): structural facts incl. the p_4 notin H^4 counterexample.

## Novelty classification (Phase 11)

- L1'/L2/L4: refinements of project results (s in {1,2,3}) — INDEPENDENT_REDISCOVERY_POSSIBLE.
- L1'' (s>=4 negative), S1d, and the Q3-premise correction: the most novel concrete
  artifacts — POTENTIALLY_NEW.
- L5 (parity/boundary obstruction): POTENTIALLY_NEW.

Significance: useful lemma / structural reduction + a decisive structural
correction; not a major resolution (O1'LD open).
