import Mathlib.Analysis.SpecialFunctions.Trigonometric.Deriv
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.NormNum

/-!
Round 7 local author candidate. No previous project module is imported.
The FH objects below are scalar contributions under explicit single-interface
assumptions, not a formalization of spectral differentiability. The endpoint
coefficient is algebra only, with no Taylor or remainder claim.
-/

namespace SL.AuditRound7

noncomputable section

open scoped BigOperators

def normalized_mode (n : ℕ) (x : ℝ) : ℝ :=
  Real.sqrt 2 * Real.sin ((n : ℝ) * Real.pi * x)

def normalized_mode_slope (n : ℕ) (x : ℝ) : ℝ :=
  Real.sqrt 2 * ((n : ℝ) * Real.pi) * Real.cos ((n : ℝ) * Real.pi * x)

theorem normalized_mode_has_deriv (n : ℕ) (x : ℝ) :
    HasDerivAt (normalized_mode n) (normalized_mode_slope n x) x := by
  simpa [normalized_mode, normalized_mode_slope, mul_comm, mul_left_comm, mul_assoc]
    using (((hasDerivAt_id x).const_mul ((n : ℝ) * Real.pi)).sin).const_mul (Real.sqrt 2)

def wronskian (n : ℕ) (x : ℝ) : ℝ :=
  normalized_mode n x * normalized_mode_slope (n + 1) x -
    normalized_mode_slope n x * normalized_mode (n + 1) x

theorem wronskian_is_derivative_expression (n : ℕ) (x : ℝ) :
    wronskian n x = normalized_mode n x * deriv (normalized_mode (n + 1)) x -
      deriv (normalized_mode n) x * normalized_mode (n + 1) x := by
  rw [(normalized_mode_has_deriv (n + 1) x).deriv,
    (normalized_mode_has_deriv n x).deriv]
  rfl

theorem trig_product_to_sum (a t : ℝ) :
    2 * ((a + 1) * Real.sin (a * t) * Real.cos ((a + 1) * t) -
      a * Real.cos (a * t) * Real.sin ((a + 1) * t)) =
    Real.sin ((2 * a + 1) * t) - (2 * a + 1) * Real.sin t := by
  have hAdd : (2 * a + 1) * t = a * t + (a + 1) * t := by ring
  have hSub : t = (a + 1) * t - a * t := by ring
  rw [hAdd, Real.sin_add]
  conv_rhs => arg 2; arg 2; rw [hSub, Real.sin_sub]
  ring

theorem wronskian_product_to_sum (n : ℕ) (x : ℝ) :
    wronskian n x = Real.pi *
      (Real.sin ((2 * (n : ℝ) + 1) * (Real.pi * x)) -
        (2 * (n : ℝ) + 1) * Real.sin (Real.pi * x)) := by
  have hSqrt : (Real.sqrt (2 : ℝ)) ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  rw [← trig_product_to_sum]
  unfold wronskian normalized_mode normalized_mode_slope
  push_cast
  simp only [mul_assoc]
  ring_nf
  rw [hSqrt]
  ring

def sin_square_sum (n : ℕ) (t : ℝ) : ℝ :=
  ∑ j ∈ Finset.range n, Real.sin (((j : ℝ) + 1) * t) ^ 2

theorem sin_odd_step (a t : ℝ) :
    Real.sin ((2 * a + 1) * t) - Real.sin ((2 * a - 1) * t) =
      2 * Real.sin t - 4 * Real.sin t * Real.sin (a * t) ^ 2 := by
  have hAdd : (2 * a + 1) * t = 2 * (a * t) + t := by ring
  have hSub : (2 * a - 1) * t = 2 * (a * t) - t := by ring
  rw [hAdd, hSub, Real.sin_add, Real.sin_sub, Real.cos_two_mul_eq_one_sub]
  ring

theorem finite_sin_square (n : ℕ) (t : ℝ) :
    Real.sin ((2 * (n : ℝ) + 1) * t) - (2 * (n : ℝ) + 1) * Real.sin t =
      -4 * Real.sin t * sin_square_sum n t := by
  induction n with
  | zero => simp [sin_square_sum]
  | succ n ih =>
    have hStep := sin_odd_step ((n : ℝ) + 1) t
    have hArg : (2 * ((n : ℝ) + 1) - 1) * t = (2 * (n : ℝ) + 1) * t := by ring
    rw [hArg] at hStep
    simp only [sin_square_sum, Finset.sum_range_succ, Nat.cast_add, Nat.cast_one] at ih ⊢
    nlinarith

theorem wronskian_finite_sum (n : ℕ) (x : ℝ) :
    wronskian n x = -4 * Real.pi * Real.sin (Real.pi * x) *
      sin_square_sum n (Real.pi * x) := by
  rw [wronskian_product_to_sum, finite_sin_square]
  ring

theorem sin_square_sum_pos (n : ℕ) (hn : 0 < n) (t : ℝ) (ht : 0 < t)
    (htpi : t < Real.pi) : 0 < sin_square_sum n t := by
  have hSin := Real.sin_pos_of_pos_of_lt_pi ht htpi
  have hTerm : 0 < Real.sin ((((0 : ℕ) : ℝ) + 1) * t) ^ 2 := by
    simpa using sq_pos_of_pos hSin
  exact Finset.sum_pos' (fun j _ => sq_nonneg _) ⟨0, Finset.mem_range.mpr hn, hTerm⟩

theorem wronskian_neg (n : ℕ) (hn : 0 < n) (x : ℝ) (hx : 0 < x)
    (hx1 : x < 1) : wronskian n x < 0 := by
  have ht : 0 < Real.pi * x := mul_pos Real.pi_pos hx
  have htpi : Real.pi * x < Real.pi := by nlinarith [Real.pi_pos]
  have hSum := sin_square_sum_pos n hn (Real.pi * x) ht htpi
  have hSin := Real.sin_pos_of_pos_of_lt_pi ht htpi
  rw [wronskian_finite_sum]
  nlinarith [mul_pos Real.pi_pos hSin, mul_pos (mul_pos Real.pi_pos hSin) hSum]

theorem wronskian_two_half : wronskian 2 (1 / 2) = -4 * Real.pi := by
  rw [wronskian_finite_sum]
  norm_num [sin_square_sum, Finset.sum_range_succ, Real.sin_pi_div_two,
    Real.sin_pi, show Real.pi * (1 / 2) = Real.pi / 2 by ring]
  ring

theorem old_wronskian_two_half :
    -2 * ((2 : ℝ) + 1) * Real.pi * Real.sin (Real.pi * (1 / 2)) = -6 * Real.pi := by
  rw [show Real.pi * (1 / 2) = Real.pi / 2 by ring, Real.sin_pi_div_two]
  ring

theorem old_wronskian_counterexample : wronskian 2 (1 / 2) ≠
    -2 * ((2 : ℝ) + 1) * Real.pi * Real.sin (Real.pi * (1 / 2)) := by
  rw [wronskian_two_half, old_wronskian_two_half]
  nlinarith [Real.pi_pos]

def endpoint_coefficient (n : ℕ) : ℝ :=
  2 * Real.pi ^ 4 * ((n : ℝ) ^ 4 - ((n : ℝ) + 1) ^ 4)

theorem endpoint_coefficient_algebra (n : ℕ) :
    ((n : ℝ) * Real.pi) ^ 2 * (Real.sqrt 2 * ((n : ℝ) * Real.pi)) ^ 2 -
      (((n : ℝ) + 1) * Real.pi) ^ 2 *
        (Real.sqrt 2 * (((n : ℝ) + 1) * Real.pi)) ^ 2 = endpoint_coefficient n := by
  have hSqrt : (Real.sqrt (2 : ℝ)) ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  simp only [mul_pow, hSqrt, endpoint_coefficient]
  ring

theorem endpoint_coefficient_expanded (n : ℕ) :
    endpoint_coefficient n = -2 * Real.pi ^ 4 *
      (4 * (n : ℝ) ^ 3 + 6 * (n : ℝ) ^ 2 + 4 * (n : ℝ) + 1) := by
  unfold endpoint_coefficient
  ring

theorem endpoint_coefficient_neg (n : ℕ) : endpoint_coefficient n < 0 := by
  rw [endpoint_coefficient_expanded]
  have hPoly : 0 < 4 * (n : ℝ) ^ 3 + 6 * (n : ℝ) ^ 2 + 4 * (n : ℝ) + 1 := by positivity
  have hPi : 0 < Real.pi ^ 4 := pow_pos Real.pi_pos _
  nlinarith [mul_pos hPi hPoly]

def fh_term (eigenvalue jump value velocity : ℝ) : ℝ :=
  -eigenvalue * jump * value ^ 2 * velocity

def gap_switch (lower upper lowerValue upperValue : ℝ) : ℝ :=
  lower * lowerValue ^ 2 - upper * upperValue ^ 2

theorem mirrored_pair_from_single_interface
    (eigenvalue jump leftValue rightValue leftContribution rightContribution : ℝ)
    (hLeft : leftContribution = fh_term eigenvalue jump leftValue 1)
    (hRight : rightContribution = fh_term eigenvalue (-jump) rightValue (-1))
    (hMirror : rightValue ^ 2 = leftValue ^ 2) :
    leftContribution + rightContribution = -2 * eigenvalue * jump * leftValue ^ 2 := by
  rw [hLeft, hRight]
  unfold fh_term
  rw [hMirror]
  ring

theorem mirrored_gap_from_single_interface
    (lower upper jump lowerLeft lowerRight upperLeft upperRight
      lowerDL lowerDR upperDL upperDR : ℝ)
    (hLL : lowerDL = fh_term lower jump lowerLeft 1)
    (hLR : lowerDR = fh_term lower (-jump) lowerRight (-1))
    (hUL : upperDL = fh_term upper jump upperLeft 1)
    (hUR : upperDR = fh_term upper (-jump) upperRight (-1))
    (hLM : lowerRight ^ 2 = lowerLeft ^ 2)
    (hUM : upperRight ^ 2 = upperLeft ^ 2) :
    (upperDL + upperDR) - (lowerDL + lowerDR) =
      2 * jump * gap_switch lower upper lowerLeft upperLeft := by
  rw [mirrored_pair_from_single_interface upper jump upperLeft upperRight upperDL upperDR
    hUL hUR hUM,
    mirrored_pair_from_single_interface lower jump lowerLeft lowerRight lowerDL lowerDR
    hLL hLR hLM]
  unfold gap_switch
  ring

theorem mirrored_stationarity_iff (jump f : ℝ) (hJump : jump ≠ 0) :
    2 * jump * f = 0 ↔ f = 0 := by
  simp [mul_eq_zero, hJump]

theorem old_mirror_factor_counterexample :
    2 * (1 - 4 : ℝ) * gap_switch 1 4 1 1 ≠
      (1 - 4 : ℝ) * gap_switch 1 4 1 1 := by
  norm_num [gap_switch]

-- This explicit conjunction is the exact root contract. It asserts no limits.
theorem local_algebra_root :
    (∀ (n : ℕ) (x : ℝ), HasDerivAt (normalized_mode n) (normalized_mode_slope n x) x) ∧
    (∀ (n : ℕ) (x : ℝ), wronskian n x = Real.pi *
      (Real.sin ((2 * (n : ℝ) + 1) * (Real.pi * x)) -
        (2 * (n : ℝ) + 1) * Real.sin (Real.pi * x))) ∧
    (∀ (n : ℕ) (t : ℝ), Real.sin ((2 * (n : ℝ) + 1) * t) -
      (2 * (n : ℝ) + 1) * Real.sin t = -4 * Real.sin t * sin_square_sum n t) ∧
    (∀ (n : ℕ), 0 < n → ∀ (x : ℝ), 0 < x → x < 1 → wronskian n x < 0) ∧
    (wronskian 2 (1 / 2) = -4 * Real.pi) ∧
    (wronskian 2 (1 / 2) ≠ -2 * ((2 : ℝ) + 1) * Real.pi * Real.sin (Real.pi * (1 / 2))) ∧
    (∀ (n : ℕ), ((n : ℝ) * Real.pi) ^ 2 * (Real.sqrt 2 * ((n : ℝ) * Real.pi)) ^ 2 -
      (((n : ℝ) + 1) * Real.pi) ^ 2 * (Real.sqrt 2 * (((n : ℝ) + 1) * Real.pi)) ^ 2 =
        endpoint_coefficient n) ∧
    (∀ (n : ℕ), endpoint_coefficient n < 0) ∧
    (∀ (lower upper jump lowerLeft lowerRight upperLeft upperRight
        lowerDL lowerDR upperDL upperDR : ℝ),
      lowerDL = fh_term lower jump lowerLeft 1 →
      lowerDR = fh_term lower (-jump) lowerRight (-1) →
      upperDL = fh_term upper jump upperLeft 1 →
      upperDR = fh_term upper (-jump) upperRight (-1) →
      lowerRight ^ 2 = lowerLeft ^ 2 → upperRight ^ 2 = upperLeft ^ 2 →
      (upperDL + upperDR) - (lowerDL + lowerDR) =
        2 * jump * gap_switch lower upper lowerLeft upperLeft) ∧
    (∀ (jump f : ℝ), jump ≠ 0 → (2 * jump * f = 0 ↔ f = 0)) := by
  exact ⟨normalized_mode_has_deriv, wronskian_product_to_sum, finite_sin_square,
    wronskian_neg, wronskian_two_half, old_wronskian_counterexample,
    endpoint_coefficient_algebra, endpoint_coefficient_neg,
    mirrored_gap_from_single_interface, mirrored_stationarity_iff⟩

end

end SL.AuditRound7
