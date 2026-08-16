# Status and Literature — Left-Definite constrained density (O1' specialization)

Run: R-20260816T120000Z-leftdef-density
Date: 2026-08-16

## Current status (this run)

This-run status label: RIGOROUS_PARTIAL_RESULT

The left-definite specialization is advanced with several STRICT structural
theorems (candidate_proof.md Theorems L1-L6):
- L1 V = H^s recovery (Q3): full-space density holds for all integer s >= 1.
- L2 structural projection density P_V(W_s) dense in V (W_s = span{p_n}).
- L3 transfer descent: the constrained problem in H^s descends isometrically to
  H^{s'} (s' in {0,1}) with the correct second-order moment base.
- L4 "all p_n in V => V = H^s" (proper constraints exclude some p_n).
- L5 concrete STRICT non-density instance: V = ker(Delta) in H^2, Q_sp = even
  sparse family, q = p_5 - 2 p_7 in V cap Q_sp^perp nonzero, so density fails.
- L6 honest O1' status: finite-data decidable for V = H^s (no obstruction);
  descends to H^{s'} otherwise and remains a genuine moment problem in general.

The reduced unsolved core is named O1'LD (inherited O1' in the left-definite
class): for a general proper closed V subset H^s, decide whether some free
run-base / jump-free parameter admits a nonzero realization in V.  It remains
OPEN (honest; not claimed).

## Known / DERIVED results used (project, audited)

- Derivations are in-project STRICT results (docs + DensBC runs), cited by
  source document, not re-derived here:
  - Sparse family {p_n} is dense in H^s for every integer s >= 0:
    docs/SL_h2_completeness_proof.tex (H^2), SL_h3_completeness_proof.tex (H^3),
    SL_denseness_criteria.tex Theorem 8 (all integer s), SL_hs_orthogonal_systems
    (explicit orthogonal systems).  Status: DERIVED / project-proof.
  - DensBC master / moment machinery:
    R-20260814T...densbc-3F8A2C candidate_proof.md Theorems A-H (Master Theorem A,
    Theorem E diagonal classification), R-20260816T...densbc-o1 candidate_proof.md
    Theorems 1-5 + reduced core O1' (audit REPORT: REPAIRABLE_GAP repaired; the
    O1' realizability/membership step is honestly OPEN).  Status: DERIVED (audited
    upstream), cited by run/name.
  - Left-definite theory (Littlejohn--Wellman), Krein-Sobolev polynomials
    (Jones--Littlejohn--Quintero Roba): KNOWN (literature), used for the scale
    H^s = D(K_c^{s/2}) and the H^1 basis.

## Novelty / openness status (target problem)

A web narrative sweep (2026-08-16, 4 queries) aimed specifically at
"left-definite space polynomial density constrained subspaces Krein orthogonal
polynomials criterion" and at "exceptional/analytic completeness gapped family
constrained" returned:
- Krein-Sobolev Orthogonal Polynomials II (Jones, Littlejohn, Quintero Roba,
  Axioms 14 (2025) no. 2, 115): https://www.mdpi.com/2075-1680/14/2/115
  (establishes H^1 orthogonal Krein-Sobolev basis; does NOT give a constrained-
  subspace density criterion for the gapped sparse family).
- Zbl 07015415 (left-definite survey context) and zbmath link:
  https://zbmath.org/pdf/07015415.pdf (context; no constrained-density criterion).
- Exceptional orthogonal polynomial completeness (Gomez-Ullate et al.,
  Corrigendum J. Approx. Theory 2019), https://doi.org/10.1016/j.jat.2019.105350
  (completeness of exceptional families; not the constrained-subspace question).
- Polynomial density on curves via matrix algebra (arXiv:1910.11633):
  https://ar5iv.labs.arxiv.org/html/1910.11633 (polynomial density on curves;
  different setting).

No published source shapes an exact finite-data decision for polynomial density
in a functional-kernel / structural constrained subspace of the Krein left-
definite spaces H^s with the gapped sparse family {p_n}.  The DensBC O1
machinery (project) is the only exact structured criterion found (and it is
in-project, not a published external source).

- Fetch status: all target hits are abstract/title-level or full secondary text;
  NONE fetched-and-verified as settling the constrained-density decision.  The
  openness claim for the EXACT constrained finite-data criterion rests on the
  absence of any such source in the sweep; per Phase-2 discipline this is
  recorded as: novelty = POTENTIALLY_NEW (needs a deeper arXiv/zbMATH full-text
  pass before claiming EXPERT_NOVELTY_CHECKED).  We do NOT claim the problem is
  definitely open in the literature; we only claim no external exact criterion
  was surfaced by this sweep.

## Classification

- Known/verified external full-text theorems: none settle the target.
- Project-derived (audited): DensBC Theorems A-H/E, DensBC O1 Theorems 1-5,
  left-definite H^s completeness.
- Open: O1'LD (constrained realization step); O2' inherited; O3 (fractional
  window 3/2 <= s < 2).
- Heuristic/EVIDENCE: structural facts (exact arithmetic) corroborate; not proof.

## Novelty classification (Phase 11)

- L1/L2/L4/L5: direct consequences of / refinements of project results +
  DensBC O1; classification: INDEPENDENT_REDISCOVERY_POSSIBLE at most (they are
  honest specializations, not claimed as major novel theorems).
- L3 (transfer descent): a clean structural reduction; POTENTIALLY_NEW as a
  formulation, but it is a straightforward consequence of the isometric transfer
  (K_c : H^t -> H^{t-2}) which is standard left-definite theory.
- The concrete obstruction mechanism (L5 parity/boundary selection) is the most
  novel concrete artifact; POTENTIALLY_NEW.

Significance: useful lemma / structural reduction level; not a major resolution
(the open core O1'LD remains).
