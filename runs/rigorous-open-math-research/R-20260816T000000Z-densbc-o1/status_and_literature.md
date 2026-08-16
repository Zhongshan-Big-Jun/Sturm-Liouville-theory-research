# Status and Literature

Run: R-20260816T000000Z-densbc-o1
Task: Q-20260816-densbc-o1-A1B2C3D4 (DensBC O1, general non-diagonal H)

## Current status

Upstream: RIGOROUS_PARTIAL_RESULT (verbatim; O1 open).
This run: RIGOROUS_PARTIAL_RESULT — new STRICT structure theorems for O1
(projection-density, obstruction system, run/first-obstruction, diagonal
reduction, finite-rank structure), with a precise reduced core O1' (the
realizability/membership moment-problem step).  No complete closed-form for
general non-diagonal H is claimed; that requires resolving O1'.

## Target problem status (directed confirmation, 2026-08-16)

The specific problem — an exact, verifiable criterion for polynomial density in a
closed subspace V = Intersection ker L_j of a general Hilbert space when L_j are
non-coordinate — is, per this run's audit and the upstream novelty run, not known
to be settled in the literature.  The classical theory treats density in the
WHOLE space (Berg-Christensen; Dette-Zhigljavsky; Berg-Thill; Rodriguez), not in
a constrained closed subspace of a general H.  Fetch status for the target
problem: not found in literature survey; recorded as OPEN.

## Literature (stable links, from upstream + this run's sweep)

Upstream-verified (whole-space density; NO constrained-subspace criterion):
1. C. Berg, J.P.R. Christensen, "Density questions in the classical theory of
   moments", Ann. Inst. Fourier 31(3) (1981) 99-114, DOI 10.5802/aif.840.
2. H. Dette, A. Zhigljavsky, "Reproducing kernel Hilbert spaces, polynomials and
   the classical moment problems", arXiv:2101.11968.
3. C. Berg, M. Thill, "Rotation invariant moment problems", Acta Math. 167 (1991)
   207-227, DOI 10.1007/BF02392450.
4. J.M. Rodriguez, J. Approx. Theory 120 (2003) 185-216, DOI 10.1016/S0021-9045(02)00019-9.

This-run web sweep (2026-08-16) for "polynomial density constrained subspace
boundary functionals moment problem exact criterion": returned moment-problem and
approximation-theory material (Hausdorff moment problem; Pinkus "Density methods
and results in approximation theory", Zbl 1068.41011; local moment problem
arXiv:1311.0501); NONE states a constrained-subspace (kernel-intersection)
criterion for a general non-diagonal H.  Status of the novelty claim: recorded as
"no published exact criterion known to this audit" (fetch status: general-web
level; no direct confirmation of a competing result found).  Marked novelty
classification: POTENTIALLY_NEW (needs a deeper bibliographic pass before any
stronger claim; not asserted here beyond the project's own preflight).

## Reduced open core (this run)

- O1': decidability of the free run-base realization step (moment representability
  + membership in V) for general non-diagonal H.  Structurally reduced from O1 by
  Theorems 1-5 (candidate_proof.md).  Finite-rank exactly under Theorem 5's
  conditions.
- O2 (inherited): general L_j expansion killing free params in all beta.
- O3 (inherited): fractional left-definite window 3/2 <= s < 2.

## Honesty notes

- The projection-density theorem (Theorem 1) is STRICT and new to this run.
- The finite-rank/non-finite-rank answer (Theorem 5) resolves the packet's risk
  honestly: in general O1 requires moment-problem data, not a purely finite-rank
  closed form.  Audit-corrected: finiteness holds under a banded/diagonal-moment
  condition (diagonal case cleanly satisfies it), NOT merely from polynomial
  representers.
- No git commit/push; see repro_manifest.md.
