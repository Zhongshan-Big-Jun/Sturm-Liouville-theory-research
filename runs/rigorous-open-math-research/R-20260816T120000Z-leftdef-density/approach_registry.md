# Approach Registry — R-20260816T120000Z-leftdef-density

Route portfolio for the left-definite constrained-density problem.

## Route A — Structural normalization / audit of DensBC O1 transfer
- Route ID / family: A-structural-audit (contract/audit).
- Core mechanism: re-derive which polynomials/monomials lie in H^s; detect DensBC
  (H1) failure; find the correct moment base.  CRITICAL OUTCOME: the sparse family
  {p_n} is in H^s ONLY for s in {1,2,3}; for s >= 4, H^s ∩ C[x] = span{1,x}.
- Target obligation: S1a-S1d.
- Status: PROVED (exact-verified; S1d is the decisive new fact).
- Exact gap: none for s in {1,2,3}; the s>=4 negative finding is closed (L1'').

## Route B — Whole-space recovery (V = H^s), CORRECT SCOPE
- Route ID / family: B-whole-space (direct).
- Core mechanism: for s in {1,2,3}, Q_sp = {p_n} and span{p_n} dense => density.
- Target obligation: L1' (s in {1,2,3}); first-obstruction (Q2).
- Status: PROVED (s=1 first-moment; s=2 SL_h2; s=3 SL_h3).
- Exact gap: for s >= 4 the sparse family fails (L1''); NOT a route to claim
  density there.

## Route B' — s >= 4 negative / correction
- Route ID / family: B'-s4-negative (counterexample/structural).
- Core mechanism: p_4 notin H^4 (K_c p_4 fails Krein BC), so sparse family not in
  H^s; H^s ∩ C[x] = span{1,x}; Q_sp = {1,x}; density fails.
- Target obligation: L1'' / S1d / packet Q3 correction for s >= 4.
- Status: PROVED (STRICT, exact witness).

## Route C — Transfer descent
- Route ID / family: C-transfer (isometry).
- Core mechanism: K_c : H^t -> H^{t-2} isometry descends constrained problem to
  H^{s'}, s' in {0,1}; clean 3-term jump base at r=1 (s=2,3); higher-order at s>=4.
- Target obligation: L3 core + remark.
- Status: PROVED.

## Route D — Concrete obstruction search (disproof)
- Route ID / family: D-counterexamples (minimal counterexample).
- Core mechanism: natural bounded functional V excludes one parity from Q_sp,
  leaving parity-orthogonal obstructions.
- Target obligation: L5 (V = ker(Delta) in H^2).
- Status: PROVED (airtight per independent audit).

## Route E — Finite-data decidability of O1' in the class (Q1)
- Route ID / family: E-finite-data (condition).
- Core mechanism: DensBC O1 Theorem 5 finiteness condition; H^1 moment matrix
  non-diagonal => finiteness not automatic.
- Target obligation: L6 / O1'LD.
- Status: PARTIAL (decided for V=H^s [L1'/L1''] and L5; general open O1'LD).
- Exact gap: O1'LD (realize free jump-base moment sequence in K_c^r V).

## Route F — Operator-domain vs abstract-completion (NEW open)
- Route ID / family: F-Hs-model (interpretation).
- Core mechanism: reconcile H^s = D(K_c^{s/2}) (operator domain) with the abstract
  completion reading needed by the SL_hs orthogonal system {Q_n^{(s)}} for s >= 4.
- Target obligation: N8 (open).
- Status: OPEN (flagged; affects project s>=4 whole-space completeness claims).

## Route G — Fractional window 3/2 <= s < 2 (inherited O3)
- Status: INHERITED OPEN / NOT addressed this run.

## Route states
A,B,B',C,D: PROVED.  E: PARTIAL.  F: OPEN.  G: INHERITED-OPEN.  Loop guarantee:
no route reopened without a materially new mechanism (B was scoped, B' added after
the FATAL finding; no re-open without new input).
