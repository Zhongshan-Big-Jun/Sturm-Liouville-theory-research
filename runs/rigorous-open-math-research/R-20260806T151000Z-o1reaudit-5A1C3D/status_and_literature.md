# Status and literature - independent re-audit of O1 Lemma 1 and Lemma 3

## Status of the audited theorem (O1 reduction)

After this independent re-audit: INDEPENDENTLY_AUDITED_PROOF for the O1
reduction theorem (sup_K D = max over the barrier family, inf_K D = min over
the well family, attained).  The two changed points (Lemma 1, Lemma 3) were
re-audited from scratch in this run; O1c-O1f rest on the prior independent
audit (R-20260806T011500Z-o1audit-422A69, PROVED) plus this run's consistency
read.  O2/O3 (symmetric family analysis) remain open obligations of the
portfolio problem and are outside this run.

## Premise status

| Premise | Source and version | Status |
|---|---|---|
| AEH Lemma 2.1 (FH formula) | arXiv:2407.02459v2, papers/fundamental_gap.txt (sha256 2F3C90...) | VERIFIED (verbatim, lines 84-101) |
| AEH Lemma 2.2 (structure of u_2/u_1) | same source, lines 197-220 | VERIFIED (items (1)-(5)) |
| Weyl/min-max | standard (self-adjoint compact) | VERIFIED; applied to S_rho, not T_rho |
| Sturm oscillation | classical | VERIFIED (numerically on hostile configs) |
| Rayleigh comparison bounds | derived in the audited run | VERIFIED (derived + numeric) |
| Keller 1976 | DOI 10.1137/0131042, papers/keller1976.txt | CONTEXT ONLY (not a premise of O1) |
| Mahar-Willner 1976 | DOI 10.1002/cpa.3160290505, papers/mw1976.txt | CONTEXT ONLY (not a premise of O1) |

## Literature context (novelty, from the revise run's status_and_literature.md)

- The box-class reduction theorem (O1) and the SUP side appear not to be in
  the literature (searched by the revise run R-20260806T140000Z-o1revise-
  2ED02A, Phase 11).
- Sun 2022 (DOI 10.1016/j.jmaa.2022.126513) treats the minimum gap in a
  bounded-jump piecewise-continuous subclass (S1/S2 class definitions
  NOT_VERIFIABLE from public metadata); the relationship of its INF-side value
  to O1's inf_K D over the full measurable class is identified but unverified.
- This audit run does not perform a new novelty search; the audit target is
  correctness of the revised proof, not novelty.  Novelty classification of
  the revise run: POTENTIALLY_NEW for the SUP side + reduction; see the revise
  run's artifacts.

## Known ambiguities relevant to this audit

- The audited candidate's NOTE on the operator form: "rho^{1/2} T_rho
  rho^{1/2}" is not symmetric as written; the symmetric Hilbert-Schmidt
  operator is S_rho = M_{sqrt(rho)} T_0 M_{sqrt(rho)}.  Audited as correct.
- Moving-jump sign convention: rightward derivative of D is -(c_+ - c_-)
  f(x_j); leftward distance derivative is +(c_+ - c_-) f(x_j).  Audited as
  correct, with the two-sided derivative of the signed parametrization
  existing at every jump position (F-002 resolution).
- Interval convention: AEH on (0,pi) vs problem on (0,1); affine rescaling,
  harmless and documented.

## Status labels used in this run

- Audited artifact (revised candidate): CANDIDATE_COMPLETE_PROOF (producer
  self-label, unchanged).
- This run's verdict label: INDEPENDENTLY_AUDITED_PROOF (O1 scope), per the
  upstream skill's output protocol.