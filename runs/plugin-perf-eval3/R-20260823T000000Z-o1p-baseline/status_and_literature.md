# Status and literature

## Current status of target problem

- Target: O1' reduced core (DensBC general non-diagonal Hilbert space H).
- Status as of this run: OPEN in general. Partial STRICT advances:
  - R-20260816T000000Z: projection density, obstruction moments, run/first
    obstruction, diagonal reduction. Reduced core O1' made precise.
  - R-20260816T210000Z: O1' CLOSED for diagonal H_beta + finite polynomial
    constraints (criterion `dense <=> ker(T|B_adm)={0}`).
  - R-20260816T220000Z: O1' CLOSED for H_lambda (bandwidth 1 shift) + finite
    polynomial representers (criterion `dense <=> ker(T|B_fin)={0}`).
- This run: O1' CLOSED for a new abstract "band-invertible" family (bounded
  invertible moment map + banded Gram), including the stable banded-shift
  family H_shift(m,lambda) for every bandwidth m >= 1, with finite polynomial
  representers. General O1' remains open.

## Known external/internal theorems used

- Upstream master criterion (Theorem A): closure(span Q_sp)=V iff
  V cap Q_sp^\perp={0}. (Project-local, audited.)
- Projection density (Theorem 1 of R-20260816T000000Z): P_V(Pi) dense in V.
- Run lemma/moment recursion: pure linearity, independent of H.
- H_lambda criterion (R-20260816T220000Z): m=1 case.
- H_beta criterion (R-20260816T210000Z): lambda=0 / diagonal case.

## Literature search summary

- Local knowledge base: tool library and prior runs are authoritative for this
  internal reduced core. `tools/constrained-denseness-runs.md` documents the
  run graph and diagonal classification.
- External web search (2026-08-23, three keyword queries):
  - query 1: "sparse polynomial family completeness constrained subspace
    Hilbert space non-diagonal orthogonality"
  - query 2: "DensBC O1' boundary constrained polynomial density general
    non-diagonal Hilbert space"
  - query 3: "polynomial density in constrained subspace moment problem
    Hilbert space sparse basis"
- Result status: degraded. The returned sources were mostly unrelated (kernel
  density estimation, sparse matrix factorization, polynomial dimensional
  decomposition, Hamburger moment problem pages). No source states the exact
  reduced core O1' or a general non-diagonal finite-rank constrained criterion.
- Honest note: no external source was found that settles or even states the
  exact target problem. The outer literature on polynomial density and the
  Hamburger moment problem is background only; we did not rely on any external
  theorem except the standard Toeplitz/analytic reciprocal fact, which is
  proved locally in Lemma 0.1.

## Novelty surface

- The stable banded-shift family H_shift(m,lambda) with finite polynomial
  representers appears to be a natural extension of H_lambda to higher
  bandwidth. The exact finite-rank criterion is new in this project.
- External literature on constrained sparse polynomial density in arbitrary
  non-diagonal Hilbert spaces is not known to us; no direct citation was found.
- Classification: POTENTIALLY_NEW within the project. The mathematical
  ingredients (Toeplitz invertibility, run algebra) are standard, but the
  combination is not a direct corollary of a cited external paper.

## Coverage gaps

- General weighted L^2 / non-Toeplitz non-diagonal H: not covered.
- General representers (non-polynomial, infinite degree): not covered.
- General O1' realization step (moment representability in arbitrary H):
  not covered.
- Lean formalization: scaffold only, not verified.

## Fetch status

- External source that mentions exact O1': none found (no fetch required).
- Local/historical sources: all required context files were read.
