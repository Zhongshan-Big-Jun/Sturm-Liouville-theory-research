# Approach Registry — R-20260816T120000Z-leftdef-density

Route portfolio for the left-definite constrained-density problem.

## Route A — Structural normalization / audit of DensBC O1 transfer
- Route ID / family: A-structural-audit (contract/audit).
- Core mechanism: independent re-derivation of which polynomials/monomials lie in
  H^s; detect DensBC (H1) failure for s >= 2; identify correct moment base.
- Target obligation: N0 (S1), the normalization of the problem statement.
- Why strictly easier: purely structural; uses docs + exact arithmetic, no
  open core.
- Required known results: SL_h2 Lemma 1 (BC), Sobolev embedding.
- First concrete deliverable: S1 + corrected projection density (L2).
- Fast falsification: find a monomial x^k (k>=2) in H^2 -> would refute S1;
  exact check says none.  Status: PROVED.
- Expected bottleneck: none (structural).
- Exact gap: none.
- Next action: null.

## Route B — Whole-space recovery (V = H^s)
- Route ID / family: B-whole-space (direct).
- Core mechanism: Q_sp = {p_n}; project completeness (N1).
- Target obligation: N2 (L1).
- First concrete deliverable: Theorem L1 + first-obstruction remark (Q2/Q3).
- Status: PROVED.

## Route C — Transfer descent
- Route ID / family: C-transfer (isometry).
- Core mechanism: K_c : H^t -> H^{t-2} isometry maps constrained problem
  down to H^{s'}, s' in {0,1}.
- Target obligation: N4 (L3); the honest moment base for s >= 2.
- First concrete deliverable: Theorem L3 (descent to H^{s'}).
- Status: PROVED.

## Route D — Concrete obstruction search (disproof)
- Route ID / family: D-counterexamples (minimal counterexample).
- Core mechanism: find a natural bounded functional V that excludes one parity
  from Q_sp, leaving parity-orthogonal obstructions.
- Target obligation: N6 (L5).
- Fast falsification: test V = ker(Delta); exact check confirms q in V∩Q_sp^perp.
- Status: PROVED (STRICT non-density instance).

## Route E — Finite-data decidability of O1' in the class (Q1)
- Route ID / family: E-finite-data (condition).
- Core mechanism: DensBC O1 Theorem 5 finiteness condition (banded/diagonal
  moment data) specialized to H^{s'}; non-diagonality of the Krein moment matrix.
- Target obligation: N7 (L6).
- Status: PARTIAL (V=H^s and L5 instance decided; general O1'LD open).
- Exact gap: O1'LD (realize free jump-base moment sequence in K_c^r V).

## Route F — Fractional window 3/2 <= s < 2 (inherited O3)
- Status: INHERITED OPEN / NOT addressed this run (out of scope for integer s).

## Route states
A,B,C,D: PROVED.  E: PARTIAL.  F: INHERITED-OPEN.  Loop guarantee: no route
reopened without a materially new mechanism.
