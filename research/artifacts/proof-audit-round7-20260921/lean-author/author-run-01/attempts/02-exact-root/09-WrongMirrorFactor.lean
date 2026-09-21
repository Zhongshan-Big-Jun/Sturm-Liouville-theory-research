import SL.AuditRound7

open SL.AuditRound7

-- Intentional failure: the two moving interfaces contribute a factor 2.
example (eigenvalue jump leftValue rightValue leftContribution rightContribution : ℝ)
    (hLeft : leftContribution = fh_term eigenvalue jump leftValue 1)
    (hRight : rightContribution = fh_term eigenvalue (-jump) rightValue (-1))
    (hMirror : rightValue ^ 2 = leftValue ^ 2) :
    leftContribution + rightContribution = -eigenvalue * jump * leftValue ^ 2 := by
  exact mirrored_pair_from_single_interface eigenvalue jump leftValue rightValue
    leftContribution rightContribution hLeft hRight hMirror
