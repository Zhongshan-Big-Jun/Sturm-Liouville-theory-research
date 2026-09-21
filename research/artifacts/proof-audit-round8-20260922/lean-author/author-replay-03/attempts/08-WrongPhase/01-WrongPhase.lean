import AuditRound8
open AuditRound8
-- Deliberately demand the old global branch at the explicit small-u parameters.
example (lambda2 : ℝ) (h0 : 0 ≤ lambda2) (hmax : lambda2 ≤ 4 * Real.pi ^ 2) :
    Real.pi / 2 < phase lambda2 := (phase_bound lambda2 h0 hmax).2.1
