# Audit Report — O1'LD run

Run: R-20260823T030000Z-leftdef-o1pld
Note: The task explicitly said "Do not spawn nested subagents".  Therefore the
audit below is a self-audit by the same solver, with the inevitable limitation
that it is not a fresh-context independent audit.  This is recorded honestly.

## Verdict
PASS (with one self-corrected citation issue; no remaining critical gap found).

## Covered scope
- s = 2 (L^2 descent): finite-support moment rigidity, infinite-run
  inadmissibility, cofinite-N density theorem, parity decomposition, μ_4
  non-density example.
- s = 3 (H^1 descent): infinite-run inadmissibility only; finite-run
  realizability left open.
- Müntz-Szász citation and its application to L^2(-1,1).
- Exact arithmetic verification of the μ_4 formulas (reproducibility/o1pld_l2_mu4.py).

## Issues found and fixed
1. Initial write-up used the C[0,1] form of the Müntz-Szász theorem, which
   requires the exponent 0 to be present.  Since a finite deletion may remove 0,
   that citation was insufficient.  Fixed by using the L^p form of Müntz-Szász,
   which is valid for L^2 and does not require 0.  A direct Legendre-basis
   computation of the L^2 projection residual (1/(1/2+Σ P_n(0)^2)) supports that
   the deletion of a finite set is total in L^2, with logarithmically slow
   convergence.

## Residual risk
- The L^2 finite-support rigidity depends on a classical theorem (L^p
  Müntz-Szász) that is cited, not fully reproved.  If the theorem's exact
  hypotheses are disputed, a self-contained alternate proof would be needed.
- The H^1 finite-run realizability is unresolved; the EVIDENCE is not a proof.
- The parity decomposition relies on even/odd orthogonality in L^2; the H^1
  analogue is asserted only as a remark without a detailed proof.

## Not checked
- No external literature search was rerun in this subagent.
- No Lean verification was run; the Lean scaffold is a statement-level scaffold
  with `sorry`.
