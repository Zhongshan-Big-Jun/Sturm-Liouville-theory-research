import SL.AuditRound5
open SL.AuditRound5
-- Deliberately false claim: rejected using the actual strict-inclusion theorem.
example : high_span 2 = oblique ⊓ krein_polynomials := by
  exact high_span_lt_krein_oblique 2
