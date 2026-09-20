import Mathlib.Analysis.SpecialFunctions.Trigonometric.Deriv
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Inverse
import Mathlib.Data.Nat.Factorial.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.LinearCombination
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Ring

/-!
# Local algebraic bridges for the second proof audit (2026-09-20)

Author contribution, not a final acceptance certificate.

Sources: audit B05-B07; `docs/SL_third_order_K1_proof.tex`, finite backward
solutions; `docs/SL_mw_lemma_reproof.tex`, affine invariance and cell extension;
`docs/SL_ratio_proof.tex`, the candidate calculation and doubling argument.

This file is an independent algebraic layer. `third_order_solution` has the
formula of `SL.ThirdOrder.IsSolution`; `k1_p`, `k1_q`, `k1_r` specialize
`SL.ThirdOrderClosedForms.PEven/QEven/REven` at c=1; `candidate_theta` has the
formula of `SL.BalancedPhase.theta`. These source comparisons are documented,
but this file deliberately does not import the existing SL modules. No kernel
identity with those existing declarations is claimed.
MW proves signed slope matching and the chain-rule scaling of a smooth cell.
The order lemmas use arbitrary bounded real sets; they do not identify these
sets with a Sturm-Liouville spectrum. The explicit countermodel refutes the
abstract inference, not the candidate spectral formula. No assertion here proves
the K1 infinite limit, global piecewise gluing, oscillation/doubling, or the
first-pair global variational optimum.
-/

namespace SL.AuditRound2

section Differences

variable {K : Type*} [Field K]

/-- Backward second difference. The recurrence uses this only at indices >= 2. -/
def second_difference (v : ℕ → K) (j : ℕ) : K :=
  v j - 2 * v (j - 1) + v (j - 2)

theorem terminal_difference {v : ℕ → K} {N : ℕ}
    (hN : v N = 0) (hPrev : v (N - 1) = 0) :
    second_difference v N = v (N - 2) := by
  simp [second_difference, hN, hPrev]

/-- Factorization of the scaled recurrence is an equivalence, not an extra
assumption that the difference already solves its desired recurrence. -/
theorem difference_step_iff (c a b d e : K) :
    a = (2 + c) * b - (1 + 2 * c) * d + c * e ↔
      a - 2 * b + d = c * (b - 2 * d + e) := by
  constructor <;> intro h <;> linear_combination h

/-- Independent copy of the existing general recurrence interface. -/
def third_order_solution (a1 a2 a3 v : ℕ → K) : Prop :=
  ∀ n, v (n + 3) = a1 (n + 3) * v (n + 2) +
    a2 (n + 3) * v (n + 1) + a3 (n + 3) * v n

/-- The scaled recurrence implies the first-order difference recurrence. -/
theorem solution_difference_step {c v : ℕ → K}
    (hSol : third_order_solution
      (fun j => 2 + c j) (fun j => -(1 + 2 * c j)) c v) (n : ℕ) :
    second_difference v (n + 3) = c (n + 3) * second_difference v (n + 2) := by
  have h := hSol n
  dsimp at h
  simp only [second_difference,
    show n + 3 - 1 = n + 2 by omega,
    show n + 3 - 2 = n + 1 by omega,
    show n + 2 - 1 = n + 1 by omega,
    show n + 2 - 2 = n by omega]
  linear_combination h

end Differences

/-- Coefficients in the K1 source, equivalently the old even family at c=1. -/
def k1_p (j : ℕ) : ℚ :=
  8 * (j : ℚ) ^ 2 - 4 * (j : ℚ) + (j : ℚ) / ((j : ℚ) - 1)

def k1_q (j : ℕ) : ℚ :=
  4 * (j : ℚ) * ((j : ℚ) - 1) * (2 * (j : ℚ) - 1) * (2 * (j : ℚ) - 3) +
    4 * (j : ℚ) * (2 * (j : ℚ) - 3)

def k1_r (j : ℕ) : ℚ :=
  4 * (j : ℚ) * ((j : ℚ) - 2) * (2 * (j : ℚ) - 3) * (2 * (j : ℚ) - 5)

/-- Finite factorial shift used below, over exact rational arithmetic. -/
theorem factorial_shift_four (n : ℕ) :
    (Nat.factorial (2 * (n + 3)) : ℚ) =
      (2 * n + 6 : ℚ) * (2 * n + 5 : ℚ) *
      (2 * n + 4 : ℚ) * (2 * n + 3 : ℚ) *
      (Nat.factorial (2 * (n + 1)) : ℚ) := by
  rw [show 2 * (n + 3) = 2 * (n + 1) + 4 by omega]
  simp only [Nat.factorial_succ, Nat.cast_mul, Nat.cast_add, Nat.cast_one]
  push_cast
  ring

/-- The actual factorial scaling used in the K1 document. -/
def k1_scaled (mu : ℕ → ℚ) (j : ℕ) : ℚ :=
  mu j / (Nat.factorial (2 * j) : ℚ)

/-- N = n+3 covers every terminal index N >= 3. Only the last original
recurrence equation is needed. Its coefficients are explicitly defined above from the source.
This does not assume the claimed terminal difference as a hypothesis. -/
theorem k1_terminal_value (mu : ℕ → ℚ) (n : ℕ)
    (hTop : mu (n + 4) = 1) (hN : mu (n + 3) = 0)
    (hPrev : mu (n + 2) = 0)
    (hStep : mu (n + 4) =
      k1_p (n + 4) * mu (n + 3) -
      k1_q (n + 4) * mu (n + 2) +
      k1_r (n + 4) * mu (n + 1)) :
    second_difference (k1_scaled mu) (n + 3) =
      (n + 3 : ℚ) / ((n + 4 : ℚ) * (Nat.factorial (2 * (n + 3)) : ℚ)) := by
  have hR : k1_r (n + 4) =
      4 * (n + 4 : ℚ) * (n + 2 : ℚ) * (2 * n + 5 : ℚ) * (2 * n + 3 : ℚ) := by
    unfold k1_r
    push_cast
    ring
  have hRpos : 0 < k1_r (n + 4) := by
    rw [hR]
    positivity
  have hLast : mu (n + 1) = 1 / k1_r (n + 4) := by
    apply (eq_div_iff (ne_of_gt hRpos)).2
    simpa [hTop, hN, hPrev, mul_comm] using hStep.symm
  have hFact := factorial_shift_four n
  have hFactNe : (Nat.factorial (2 * (n + 1)) : ℚ) ≠ 0 := by positivity
  simp only [second_difference, k1_scaled,
    show n + 3 - 1 = n + 2 by omega,
    show n + 3 - 2 = n + 1 by omega, hN, hPrev, zero_div, mul_zero,
    sub_zero, zero_add]
  rw [hLast, hR, hFact]
  field_simp [hFactNe]
  ring

theorem k1_terminal_formula_pos (n : ℕ) :
    0 < (n + 3 : ℚ) /
      ((n + 4 : ℚ) * (Nat.factorial (2 * (n + 3)) : ℚ)) := by
  positivity

/-- A concrete terminal solution segment at N=3: mu_1=1/480, mu_2=mu_3=0,
mu_4=1. It satisfies the last original equation and has d_3=1/960, not zero. -/
def k1_n3_segment (j : ℕ) : ℚ :=
  if j = 1 then 1 / 480 else if j = 4 then 1 else 0

theorem k1_n3_last_equation :
    k1_n3_segment 4 =
      k1_p 4 * k1_n3_segment 3 -
      k1_q 4 * k1_n3_segment 2 +
      k1_r 4 * k1_n3_segment 1 := by
  norm_num [k1_n3_segment, k1_r]

theorem k1_n3_difference :
    second_difference (k1_scaled k1_n3_segment) 3 = 1 / 960 := by
  norm_num [second_difference, k1_scaled, k1_n3_segment, Nat.factorial]

theorem k1_n3_difference_ne_zero :
    second_difference (k1_scaled k1_n3_segment) 3 ≠ 0 := by
  rw [k1_n3_difference]
  norm_num

/-- The sign belongs to the transmission factor. No positivity assumption. -/
noncomputable def signed_transmission (Left Right : ℝ) : ℝ := Right / Left

theorem mw_signed_slope_matching (Left Right Scale : ℝ) (j : ℕ)
    (hLeft : Left ≠ 0) :
    signed_transmission Left Right ^ j * Scale * Right =
      signed_transmission Left Right ^ (j + 1) * Scale * Left := by
  have h : signed_transmission Left Right * Left = Right := by
    exact div_mul_cancel₀ Right hLeft
  rw [pow_succ]
  calc
    _ = signed_transmission Left Right ^ j * Scale *
        (signed_transmission Left Right * Left) := by rw [h]
    _ = _ := by ring

theorem mw_transmission_ne_zero {Left Right : ℝ}
    (hLeft : Left ≠ 0) (hRight : Right ≠ 0) :
    signed_transmission Left Right ≠ 0 := div_ne_zero hRight hLeft

/-- Chain rule for a cell pullback, including its amplitude and scale. -/
theorem mw_affine_has_deriv {y : ℝ → ℝ} {dy A c d x : ℝ}
    (hy : HasDerivAt y dy (c * x + d)) :
    HasDerivAt (fun z => A * y (c * z + d)) (A * c * dy) x := by
  have hAffine : HasDerivAt (fun z : ℝ => c * z + d) c x := by
    simpa using ((hasDerivAt_id x).const_mul c).add_const d
  simpa only [Function.comp_def, mul_assoc, mul_left_comm, mul_comm] using
    (hy.comp x hAffine).const_mul A

/-- On a smooth cell, the pulled-back equation has eigenvalue c^2*lambda.
The global C1 gluing and piecewise spectral identification are separate tasks. -/
theorem mw_affine_ode {y dy ddy rho : ℝ → ℝ} {A c d lam : ℝ}
    (hFirst : ∀ x, HasDerivAt y (dy x) x)
    (hSecond : ∀ x, HasDerivAt dy (ddy x) x)
    (hOde : ∀ x, -(ddy x) = lam * rho x * y x) (x : ℝ) :
    -(deriv (deriv (fun z => A * y (c * z + d))) x) =
      (c ^ 2 * lam) * rho (c * x + d) * (A * y (c * x + d)) := by
  have hFirstEq : deriv (fun z => A * y (c * z + d)) =
      fun z => A * c * dy (c * z + d) := by
    funext z
    exact (mw_affine_has_deriv (hFirst (c * z + d))).deriv
  rw [hFirstEq, (mw_affine_has_deriv (A := A * c) (hSecond (c * x + d))).deriv]
  linear_combination (A * c ^ 2) * hOde (c * x + d)

theorem mw_scaled_ratio (c lamOne lamTwo : ℝ) (hc : c ≠ 0) :
    (c ^ 2 * lamTwo) / (c ^ 2 * lamOne) = lamTwo / lamOne := by
  exact mul_div_mul_left lamTwo lamOne (pow_ne_zero 2 hc)

noncomputable def second_sine_mode (x : ℝ) : ℝ :=
  Real.sin (2 * Real.pi * (x + 1 / 2))

theorem second_sine_mode_has_deriv (x : ℝ) :
    HasDerivAt second_sine_mode
      (2 * Real.pi * Real.cos (2 * Real.pi * (x + 1 / 2))) x := by
  unfold second_sine_mode
  simpa only [id_eq, mul_one, mul_comm] using
    (((hasDerivAt_id x).add_const (1 / 2)).const_mul (2 * Real.pi)).sin

theorem second_sine_mode_endpoint_slopes :
    deriv second_sine_mode (-1 / 2) = 2 * Real.pi ∧
      deriv second_sine_mode (1 / 2) = 2 * Real.pi := by
  constructor
  · convert (second_sine_mode_has_deriv (-1 / 2)).deriv using 1 <;> norm_num
  · convert (second_sine_mode_has_deriv (1 / 2)).deriv using 1 <;>
      norm_num [Real.cos_two_pi]

/-- The second constant-density mode transmits with b=1; the old -Right/Left
convention gives -1 and therefore cannot be assumed positive. -/
theorem second_sine_mode_transmission :
    signed_transmission (deriv second_sine_mode (-1 / 2))
      (deriv second_sine_mode (1 / 2)) = 1 ∧
    -(deriv second_sine_mode (1 / 2)) / deriv second_sine_mode (-1 / 2) = -1 := by
  rcases second_sine_mode_endpoint_slopes with ⟨hLeft, hRight⟩
  rw [hLeft, hRight]
  unfold signed_transmission
  have h : (2 : ℝ) * Real.pi ≠ 0 := by positivity
  simp [h]

theorem attained_le_sup {S : Set ℝ} {C : ℝ} (hBound : BddAbove S)
    (hAttained : C ∈ S) : C ≤ sSup S := le_csSup hBound hAttained

/-- Attainment plus a universal upper bound is precisely the missing bridge. -/
theorem attained_sup_eq_iff_upper_bound {S : Set ℝ} {C : ℝ}
    (hBound : BddAbove S) (hAttained : C ∈ S) :
    sSup S = C ↔ ∀ x ∈ S, x ≤ C := by
  constructor
  · intro h x hx
    rw [← h]
    exact le_csSup hBound hx
  · intro h
    exact le_antisymm (csSup_le ⟨C, hAttained⟩ h) (le_csSup hBound hAttained)

/-- Same formula as the existing balanced-phase theta, defined independently. -/
noncomputable def candidate_theta (s : ℝ) : ℝ := Real.arccos (s / (s + 1))

/-- A candidate value, not a definition of a supremum. -/
noncomputable def balanced_candidate (s : ℝ) : ℝ :=
  ((Real.pi - candidate_theta s) / candidate_theta s) ^ 2

theorem balanced_candidate_le_sup {s : ℝ} (hs : 0 < s) {S : Set ℝ}
    (hBound : BddAbove S)
    (hAttained :
      (((2 * s + 1) * (Real.pi - candidate_theta s) / s) ^ 2) /
        (((2 * s + 1) * candidate_theta s / s) ^ 2) ∈ S) :
    balanced_candidate s ≤ sSup S := by
  have hTheta : 0 < candidate_theta s := by
    unfold candidate_theta
    rw [Real.arccos_pos]
    rw [div_lt_one (by positivity : 0 < s + 1)]
    linarith
  have hRatio :
      (((2 * s + 1) * (Real.pi - candidate_theta s) / s) ^ 2) /
        (((2 * s + 1) * candidate_theta s / s) ^ 2) = balanced_candidate s := by
    unfold balanced_candidate
    field_simp [ne_of_gt hTheta, ne_of_gt hs,
      ne_of_gt (by positivity : 0 < 2 * s + 1)]
  rw [hRatio] at hAttained
  exact attained_le_sup hBound hAttained

/-- Doubling can pass an already available bound to adjacent ratios. -/
theorem adjacent_ratio_le_of_doubled {lam : ℕ → ℝ} {n : ℕ} {nu : ℝ}
    (hMono : Monotone lam) (hn : 1 ≤ n) (hPositive : 0 < lam n)
    (hDoubled : lam (2 * n) / lam n ≤ nu) :
    lam (n + 1) / lam n ≤ nu := by
  apply le_trans _ hDoubled
  exact div_le_div_of_nonneg_right (hMono (by omega)) (le_of_lt hPositive)

/-- For ANY proposed upper bound U, a two-element bounded real set attains C
and satisfies every abstract doubling identity, while its sup exceeds U.
This is an order-theoretic countermodel, not a Sturm-Liouville density. -/
theorem attainment_doubling_countermodel (C U : ℝ) :
    ∃ (S : Set ℝ) (D : ℕ → Set ℝ), BddAbove S ∧ C ∈ S ∧
      (∀ n, D n = S) ∧ (∀ n, sSup (D n) = sSup S) ∧ U < sSup S := by
  let Top : ℝ := max C U + 1
  let S : Set ℝ := {x | x = C ∨ x = Top}
  have hCTop : C ≤ Top := by dsimp [Top]; linarith [le_max_left C U]
  have hUTop : U < Top := by dsimp [Top]; linarith [le_max_right C U]
  have hBound : BddAbove S := by
    refine ⟨Top, ?_⟩
    intro x hx
    rcases hx with rfl | rfl
    · exact hCTop
    · exact le_rfl
  refine ⟨S, fun _ => S, hBound, Or.inl rfl, fun _ => rfl, fun _ => rfl, ?_⟩
  exact lt_of_lt_of_le hUTop (le_csSup hBound (Or.inr rfl))

theorem no_candidate_upper_bound_from_doubling (C : ℝ) :
    ¬ (∀ (S : Set ℝ) (D : ℕ → Set ℝ), BddAbove S → C ∈ S →
      (∀ n, sSup (D n) = sSup S) → sSup S ≤ C) := by
  intro h
  obtain ⟨S, D, hBound, hAttained, _, hDouble, hStrict⟩ :=
    attainment_doubling_countermodel C C
  exact (not_le_of_gt hStrict) (h S D hBound hAttained hDouble)

end SL.AuditRound2
