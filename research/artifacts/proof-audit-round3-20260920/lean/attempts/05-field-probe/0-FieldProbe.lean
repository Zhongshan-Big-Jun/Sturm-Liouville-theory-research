import Mathlib.Data.Real.Basic
import Mathlib.Algebra.BigOperators.Intervals
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring


set_option trace.Tactic.field_simp true in
example (m : ℝ) (hm : m - 1 ≠ 0) (h3 : 2 * m + 3 ≠ 0) (hq : 4 * m ^ 2 - 6 * m - 7 ≠ 0) :
    1 - 6 * m * (2 * m + 5) / ((m - 1) * (2 * m + 3) * (4 * m ^ 2 - 6 * m - 7)) =
      (m - 3) * (2 * m - 1) * (4 * m ^ 2 + 10 * m + 7) /
        ((m - 1) * (2 * m + 3) * (4 * m ^ 2 - 6 * m - 7)) := by
  have hd : (m - 1) * (2 * m + 3) * (4 * m ^ 2 - 6 * m - 7) ≠ 0 :=
    mul_ne_zero (mul_ne_zero hm h3) hq
  field_simp [hm, h3, hq, hd]
  trace_state
  ring
