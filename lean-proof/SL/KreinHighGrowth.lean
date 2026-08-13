import Mathlib
import SL.HsOrthogonalSystems
import SL.KreinDegenerateLimit

/-!
# The general high-mode growth of the Krein-Sobolev coefficients (Theorem "high")

Formalization of the *general* part of Theorem "high" of
`docs/SL_krein_c0_limit.tex` (session 12), which session 87 left open in
`SL/KreinDegenerateLimit.lean`: for `n >= 4` the coefficients of the
recurrence `a_{n+2} = a_n (1 + (4n^2-1)/c) + (2n+1)/(2n-3) (a_n - a_{n-2})`
satisfy the two-sided growth bounds
`a_n(c) = Theta(c^{-(n-2)/2})` (even `n`) and `a_n(c) = Theta(c^{-(n-3)/2})`
(odd `n`) as `c -> 0`, and consequently the Krein-Sobolev norms
`||K_n^{(c)}||^2 = 2c a_n a_{n+2}/(2n+1)` diverge to `+infinity` for every
`n >= 4`.

The Θ bounds are proved with explicit constants as the pair of inequalities
`lowerProd m / c^(m-1) <= a_{2m} <= upperProd m / c^(m-1)` (and the odd
analogue), both valid for `0 < c <= 1`.  The divergence is derived from the
lower half of the bounds together with the norm formula (literature fact,
assumed via `KreinSobolevFacts`, exactly as in `SL/KreinDegenerateLimit.lean`).

Honesty notes:
* The quotient-space theorems of the source (Theorem "quotient", Theorem
  "complete" (b)-(d), Theorem "unit") still require functional analysis and
  are NOT formalized anywhere in this project; they are recorded as open in
  `SL/KreinDegenerateLimit.lean` and in `lean-proof/STATUS.md`.
* The lower growth bounds hold for all `c > 0`; the upper bounds need
  `c <= 1`, which is the natural range for a `c -> 0+` asymptotic claim.
-/

namespace SL

namespace KreinHighGrowth

open HsOrthogonalSystems KreinDegenerateLimit
open Polynomial
open Filter
open scoped BigOperators
open scoped Real Interval
open scoped Topology
open MeasureTheory

noncomputable section

/-! ## The recurrence, positivity, and parity-wise monotonicity -/

/-- `1 <= n` implies `1 <= n^2` (natural numbers). -/
private lemma one_le_sq {n : ℕ} (hn : 1 ≤ n) : 1 ≤ n ^ 2 := by
  have hmul : 1 * 1 ≤ n * n := Nat.mul_le_mul hn hn
  simpa [pow_two] using hmul

/-- The recurrence of the Krein-Sobolev coefficients (source (19)) written in
index form: for `n >= 2`,
`a_{n+2} = a_n (1 + (4n^2-1)/c) + (2n+1)/(2n-3) (a_n - a_{n-2})`. -/
lemma aSeq_rec {c : ℝ} {n : ℕ} (hn : 2 ≤ n) :
    aSeq c (n + 2) = aSeq c n * (1 + ((4 * n ^ 2 - 1 : ℕ) : ℝ) / c)
      + (((2 * n + 1 : ℕ) : ℝ) / ((2 * n - 3 : ℕ) : ℝ)) * (aSeq c n - aSeq c (n - 2)) := by
  obtain ⟨k, rfl⟩ := Nat.exists_eq_add_of_le hn
  have h1 : 2 + k + 2 = k + 4 := by omega
  have h2 : 2 + k = k + 2 := by omega
  have h3 : 2 + k - 2 = k := by omega
  rw [h1, h3, h2]
  simp only [aSeq]

/-- For `c > 0` the coefficients are nonnegative and nondecreasing along each
parity class: `0 <= a_n` and `a_n <= a_{n+2}` for every `n`. -/
lemma aSeq_nonneg_step_ge {c : ℝ} (hc : 0 < c) (n : ℕ) :
    0 ≤ aSeq c n ∧ aSeq c n ≤ aSeq c (n + 2) := by
  have hmain : ∀ n : ℕ, (∀ m : ℕ, m < n → 0 ≤ aSeq c m ∧ aSeq c m ≤ aSeq c (m + 2)) →
      0 ≤ aSeq c n ∧ aSeq c n ≤ aSeq c (n + 2) := by
    intro n ih
    by_cases hn : n ≤ 3
    · have hn0 : n = 0 ∨ n = 1 ∨ n = 2 ∨ n = 3 := by omega
      rcases hn0 with rfl | rfl | rfl | rfl
      · simp [aSeq]
      · simp [aSeq]
      · constructor
        · norm_num [aSeq]
        · rw [aSeq_two, aSeq_four]
          have h15 : (0 : ℝ) ≤ 15 / c := div_nonneg (by norm_num) (le_of_lt hc)
          linarith
      · constructor
        · norm_num [aSeq]
        · rw [aSeq_three, aSeq_five]
          have h35 : (0 : ℝ) ≤ 35 / c := div_nonneg (by norm_num) (le_of_lt hc)
          linarith
    · have hn4 : 4 ≤ n := by omega
      obtain ⟨k, rfl⟩ := Nat.exists_eq_add_of_le hn4
      have hik : 0 ≤ aSeq c k ∧ aSeq c k ≤ aSeq c (k + 2) := ih k (by omega)
      have hik2 : 0 ≤ aSeq c (k + 2) ∧ aSeq c (k + 2) ≤ aSeq c (k + 2 + 2) :=
        ih (k + 2) (by omega)
      have hik2' : aSeq c (k + 2) ≤ aSeq c (4 + k) := by
        have hind : k + 2 + 2 = 4 + k := by omega
        simpa [hind] using hik2.2
      have h04 : 0 ≤ aSeq c (4 + k) := by
        rw [show aSeq c (4 + k) = aSeq c (k + 2 + 2) by congr 1; omega]
        rw [aSeq_rec (c := c) (n := k + 2) (by omega : 2 ≤ k + 2)]
        rw [show k + 2 - 2 = k by omega]
        have hA : (0 : ℝ) ≤ ((4 * (k + 2) ^ 2 - 1 : ℕ) : ℝ) := by
          have hle : 1 ≤ 4 * (k + 2) ^ 2 := by
            have hsq : 1 ≤ (k + 2) ^ 2 := one_le_sq (by omega : 1 ≤ k + 2)
            omega
          exact_mod_cast (by omega : 0 ≤ 4 * (k + 2) ^ 2 - 1)
        have hAc : (0 : ℝ) ≤ ((4 * (k + 2) ^ 2 - 1 : ℕ) : ℝ) / c :=
          div_nonneg hA (le_of_lt hc)
        have hcoef : (0 : ℝ) ≤
            (((2 * (k + 2) + 1 : ℕ) : ℝ) / ((2 * (k + 2) - 3 : ℕ) : ℝ)) := by
          exact div_nonneg (by exact_mod_cast Nat.zero_le (2 * (k + 2) + 1))
            (by exact_mod_cast (by omega : 0 ≤ 2 * (k + 2) - 3))
        have hdiff : 0 ≤ aSeq c (k + 2) - aSeq c k := by
          linarith [hik.2]
        have hX : 0 ≤ aSeq c (k + 2) * (1 + ((4 * (k + 2) ^ 2 - 1 : ℕ) : ℝ) / c) := by
          exact mul_nonneg hik2.1
            (by nlinarith [hAc] : 0 ≤ 1 + ((4 * (k + 2) ^ 2 - 1 : ℕ) : ℝ) / c)
        have hY : 0 ≤ (((2 * (k + 2) + 1 : ℕ) : ℝ) / ((2 * (k + 2) - 3 : ℕ) : ℝ)) *
            (aSeq c (k + 2) - aSeq c k) := mul_nonneg hcoef hdiff
        nlinarith
      constructor
      · exact h04
      · rw [aSeq_rec (c := c) (n := 4 + k) (by omega : 2 ≤ 4 + k)]
        rw [show 4 + k - 2 = k + 2 by omega]
        have hA' : (0 : ℝ) ≤ ((4 * (4 + k) ^ 2 - 1 : ℕ) : ℝ) := by
          have hle : 1 ≤ 4 * (4 + k) ^ 2 := by
            have hsq : 1 ≤ (4 + k) ^ 2 := one_le_sq (by omega : 1 ≤ 4 + k)
            omega
          exact_mod_cast (by omega : 0 ≤ 4 * (4 + k) ^ 2 - 1)
        have hAc' : (0 : ℝ) ≤ ((4 * (4 + k) ^ 2 - 1 : ℕ) : ℝ) / c :=
          div_nonneg hA' (le_of_lt hc)
        have hcoef' : (0 : ℝ) ≤
            (((2 * (4 + k) + 1 : ℕ) : ℝ) / ((2 * (4 + k) - 3 : ℕ) : ℝ)) := by
          exact div_nonneg (by exact_mod_cast Nat.zero_le (2 * (4 + k) + 1))
            (by exact_mod_cast (by omega : 0 ≤ 2 * (4 + k) - 3))
        have hdiff' : 0 ≤ aSeq c (4 + k) - aSeq c (k + 2) := by
          linarith [hik2']
        have hfirst : aSeq c (4 + k) ≤
            aSeq c (4 + k) * (1 + ((4 * (4 + k) ^ 2 - 1 : ℕ) : ℝ) / c) := by
          have h1 : (1 : ℝ) ≤ 1 + ((4 * (4 + k) ^ 2 - 1 : ℕ) : ℝ) / c := by
            nlinarith [hAc']
          nlinarith [mul_le_mul_of_nonneg_left h1 h04]
        have hsecond : 0 ≤ (((2 * (4 + k) + 1 : ℕ) : ℝ) / ((2 * (4 + k) - 3 : ℕ) : ℝ)) *
            (aSeq c (4 + k) - aSeq c (k + 2)) := mul_nonneg hcoef' hdiff'
        nlinarith
  exact Nat.strong_induction_on n hmain

/-- `0 <= a_n` for `c > 0`. -/
lemma aSeq_nonneg {c : ℝ} (hc : 0 < c) (n : ℕ) : 0 ≤ aSeq c n :=
  (aSeq_nonneg_step_ge hc n).1

/-- `a_n <= a_{n+2}` for `c > 0` (monotone along each parity class). -/
lemma aSeq_step_ge {c : ℝ} (hc : 0 < c) (n : ℕ) : aSeq c n ≤ aSeq c (n + 2) :=
  (aSeq_nonneg_step_ge hc n).2

/-- The first half of the recurrence dominates: for `n >= 2` and `c > 0`,
`(4n^2-1)/c * a_n <= a_{n+2}`. -/
lemma aSeq_lower_step {c : ℝ} (hc : 0 < c) {n : ℕ} (hn : 2 ≤ n) :
    ((4 * n ^ 2 - 1 : ℕ) : ℝ) / c * aSeq c n ≤ aSeq c (n + 2) := by
  rw [aSeq_rec hn]
  have hA : (0 : ℝ) ≤ ((4 * n ^ 2 - 1 : ℕ) : ℝ) := by
    have hle : 1 ≤ 4 * n ^ 2 := by
      have hsq : 1 ≤ n ^ 2 := one_le_sq (by omega : 1 ≤ n)
      omega
    exact_mod_cast (by omega : 0 ≤ 4 * n ^ 2 - 1)
  have hAc : (0 : ℝ) ≤ ((4 * n ^ 2 - 1 : ℕ) : ℝ) / c := div_nonneg hA (le_of_lt hc)
  have hcoef : (0 : ℝ) ≤ (((2 * n + 1 : ℕ) : ℝ) / ((2 * n - 3 : ℕ) : ℝ)) := by
    exact div_nonneg (by exact_mod_cast Nat.zero_le (2 * n + 1))
      (by exact_mod_cast (by omega : 0 ≤ 2 * n - 3))
  have hdiff : 0 ≤ aSeq c n - aSeq c (n - 2) := by
    have h := aSeq_nonneg_step_ge hc (n - 2)
    rw [Nat.sub_add_cancel hn] at h
    linarith [h.2]
  have hnn : 0 ≤ aSeq c n := aSeq_nonneg hc n
  have hfirst : ((4 * n ^ 2 - 1 : ℕ) : ℝ) / c * aSeq c n ≤
      aSeq c n * (1 + ((4 * n ^ 2 - 1 : ℕ) : ℝ) / c) := by
    rw [mul_add, mul_one]
    rw [mul_comm (aSeq c n) (((4 * n ^ 2 - 1 : ℕ) : ℝ) / c)]
    exact le_add_of_nonneg_left hnn
  have hsecond : 0 ≤ (((2 * n + 1 : ℕ) : ℝ) / ((2 * n - 3 : ℕ) : ℝ)) *
      (aSeq c n - aSeq c (n - 2)) := mul_nonneg hcoef hdiff
  nlinarith

/-- The second half is bounded above: for `0 < c <= 1` and `n >= 2`,
`a_{n+2} <= 6n^2/c * a_n`. -/
lemma aSeq_upper_step {c : ℝ} (hc : 0 < c) (hcle : c ≤ 1) {n : ℕ} (hn : 2 ≤ n) :
    aSeq c (n + 2) ≤ 6 * (n : ℝ) ^ 2 / c * aSeq c n := by
  have hnn : 0 ≤ aSeq c n := aSeq_nonneg hc n
  have hmono : aSeq c (n - 2) ≤ aSeq c n := by
    have h := aSeq_nonneg_step_ge hc (n - 2)
    rw [Nat.sub_add_cancel hn] at h
    exact h.2
  have hdiff : aSeq c n - aSeq c (n - 2) ≤ aSeq c n := by
    linarith [aSeq_nonneg hc (n - 2)]
  have hcoefpos : (0 : ℝ) ≤ (((2 * n + 1 : ℕ) : ℝ) / ((2 * n - 3 : ℕ) : ℝ)) := by
    exact div_nonneg (by exact_mod_cast Nat.zero_le (2 * n + 1))
      (by exact_mod_cast (by omega : 0 ≤ 2 * n - 3))
  have hcoef_le : (((2 * n + 1 : ℕ) : ℝ) / ((2 * n - 3 : ℕ) : ℝ)) ≤
      (((2 * n + 1 : ℕ) : ℝ)) / c := by
    have hnum : (0 : ℝ) ≤ ((2 * n + 1 : ℕ) : ℝ) := by
      exact_mod_cast Nat.zero_le (2 * n + 1)
    have hle : (1 : ℝ) / ((2 * n - 3 : ℕ) : ℝ) ≤ 1 / c := by
      have h1 : (1 : ℝ) ≤ ((2 * n - 3 : ℕ) : ℝ) := by
        exact_mod_cast (by omega : 1 ≤ 2 * n - 3)
      exact one_div_le_one_div_of_le hc (le_trans hcle h1)
    rw [div_eq_mul_inv, div_eq_mul_inv] at hle ⊢
    simpa [one_mul] using mul_le_mul_of_nonneg_left hle hnum
  have hfirst : aSeq c n * (1 + ((4 * n ^ 2 - 1 : ℕ) : ℝ) / c) ≤
      aSeq c n * (1 / c + ((4 * n ^ 2 - 1 : ℕ) : ℝ) / c) := by
    refine mul_le_mul_of_nonneg_left ?_ hnn
    have h1c : (1 : ℝ) ≤ 1 / c := one_le_one_div hc hcle
    linarith
  have hsecond : (((2 * n + 1 : ℕ) : ℝ) / ((2 * n - 3 : ℕ) : ℝ)) * (aSeq c n - aSeq c (n - 2))
      ≤ (((2 * n + 1 : ℕ) : ℝ)) / c * aSeq c n := by
    have h1 : (((2 * n + 1 : ℕ) : ℝ) / ((2 * n - 3 : ℕ) : ℝ)) * (aSeq c n - aSeq c (n - 2))
        ≤ (((2 * n + 1 : ℕ) : ℝ) / ((2 * n - 3 : ℕ) : ℝ)) * aSeq c n :=
      mul_le_mul_of_nonneg_left hdiff hcoefpos
    have h2 : (((2 * n + 1 : ℕ) : ℝ) / ((2 * n - 3 : ℕ) : ℝ)) * aSeq c n
        ≤ (((2 * n + 1 : ℕ) : ℝ)) / c * aSeq c n :=
      mul_le_mul_of_nonneg_right hcoef_le hnn
    exact le_trans h1 h2
  have hmain : aSeq c n * (1 + ((4 * n ^ 2 - 1 : ℕ) : ℝ) / c) +
        (((2 * n + 1 : ℕ) : ℝ) / ((2 * n - 3 : ℕ) : ℝ)) * (aSeq c n - aSeq c (n - 2))
      ≤ aSeq c n * (1 / c + ((4 * n ^ 2 - 1 : ℕ) : ℝ) / c) +
        (((2 * n + 1 : ℕ) : ℝ)) / c * aSeq c n := add_le_add hfirst hsecond
  have hcomb : aSeq c n * (1 / c + ((4 * n ^ 2 - 1 : ℕ) : ℝ) / c) +
        (((2 * n + 1 : ℕ) : ℝ)) / c * aSeq c n
      = ((1 + ((4 * n ^ 2 - 1 : ℕ) : ℝ) + ((2 * n + 1 : ℕ) : ℝ)) / c) * aSeq c n := by
    ring_nf
  have hnum : (1 : ℝ) + ((4 * n ^ 2 - 1 : ℕ) : ℝ) + ((2 * n + 1 : ℕ) : ℝ) ≤
      6 * (n : ℝ) ^ 2 := by
    have hA : ((4 * n ^ 2 - 1 : ℕ) : ℝ) = 4 * (n : ℝ) ^ 2 - 1 := by
      have hle : 1 ≤ 4 * n ^ 2 := by
        have hsq : 1 ≤ n ^ 2 := one_le_sq (by omega : 1 ≤ n)
        omega
      rw [Nat.cast_sub hle, Nat.cast_mul, Nat.cast_pow, Nat.cast_ofNat, Nat.cast_one]
    have hB : ((2 * n + 1 : ℕ) : ℝ) = 2 * (n : ℝ) + 1 := by
      rw [Nat.cast_add, Nat.cast_mul, Nat.cast_ofNat, Nat.cast_one]
    rw [hA, hB]
    have hnR : (2 : ℝ) ≤ n := by exact_mod_cast hn
    nlinarith
  have hle2 : ((1 + ((4 * n ^ 2 - 1 : ℕ) : ℝ) + ((2 * n + 1 : ℕ) : ℝ)) / c) * aSeq c n
      ≤ 6 * (n : ℝ) ^ 2 / c * aSeq c n := by
    refine mul_le_mul_of_nonneg_right ?_ hnn
    exact div_le_div_of_nonneg_right hnum (le_of_lt hc)
  calc
    aSeq c (n + 2)
        = aSeq c n * (1 + ((4 * n ^ 2 - 1 : ℕ) : ℝ) / c) +
            (((2 * n + 1 : ℕ) : ℝ) / ((2 * n - 3 : ℕ) : ℝ)) * (aSeq c n - aSeq c (n - 2)) := by
            rw [aSeq_rec hn]
    _ ≤ aSeq c n * (1 / c + ((4 * n ^ 2 - 1 : ℕ) : ℝ) / c) +
            (((2 * n + 1 : ℕ) : ℝ)) / c * aSeq c n := hmain
    _ = ((1 + ((4 * n ^ 2 - 1 : ℕ) : ℝ) + ((2 * n + 1 : ℕ) : ℝ)) / c) * aSeq c n := hcomb
    _ ≤ 6 * (n : ℝ) ^ 2 / c * aSeq c n := hle2

/-! ## Explicit product constants for the Θ bounds -/

/-- Even-index lower product: `prod_{j=0}^{m-2} (4(2(j+1))^2 - 1)`; iterating the
lower step from `a_2 = 1` gives `a_{2m} >= lowerEvenProd m / c^(m-1)`. -/
def lowerEvenProd (m : ℕ) : ℝ :=
  ∏ j ∈ Finset.range (m - 1), (((4 * (2 * (j + 1)) ^ 2 - 1 : ℕ) : ℝ))

/-- Odd-index lower product: `prod_{j=0}^{m-2} (4(2(j+1)+1)^2 - 1)`. -/
def lowerOddProd (m : ℕ) : ℝ :=
  ∏ j ∈ Finset.range (m - 1), (((4 * (2 * (j + 1) + 1) ^ 2 - 1 : ℕ) : ℝ))

/-- Even-index upper product: `prod_{j=0}^{m-2} 6(2(j+1))^2` (from
`aSeq_upper_step` with `n = 2(j+1)`). -/
def upperEvenProd (m : ℕ) : ℝ :=
  ∏ j ∈ Finset.range (m - 1), ((6 * (2 * (j + 1)) ^ 2 : ℕ) : ℝ)

/-- Odd-index upper product: `prod_{j=0}^{m-2} 6(2(j+1)+1)^2`. -/
def upperOddProd (m : ℕ) : ℝ :=
  ∏ j ∈ Finset.range (m - 1), ((6 * (2 * (j + 1) + 1) ^ 2 : ℕ) : ℝ)

/-- The lower products are positive (all factors are at least 15). -/
lemma lowerEvenProd_pos (m : ℕ) : 0 < lowerEvenProd m := by
  unfold lowerEvenProd
  refine Finset.prod_pos ?_
  intro j hj
  have hle : 1 ≤ 4 * (2 * (j + 1)) ^ 2 := by
    have hsq : 1 ≤ (2 * (j + 1)) ^ 2 := one_le_sq (by omega : 1 ≤ 2 * (j + 1))
    omega
  exact_mod_cast (by omega : 0 < 4 * (2 * (j + 1)) ^ 2 - 1)

lemma lowerOddProd_pos (m : ℕ) : 0 < lowerOddProd m := by
  unfold lowerOddProd
  refine Finset.prod_pos ?_
  intro j hj
  have hle : 1 ≤ 4 * (2 * (j + 1) + 1) ^ 2 := by
    have hsq : 1 ≤ (2 * (j + 1) + 1) ^ 2 := one_le_sq (by omega : 1 ≤ 2 * (j + 1) + 1)
    omega
  exact_mod_cast (by omega : 0 < 4 * (2 * (j + 1) + 1) ^ 2 - 1)

/-! ## Lower growth bounds (valid for all `c > 0`) -/

/-- Even indices: `a_{2m} >= lowerEvenProd m / c^(m-1)` for `m >= 2`, `c > 0`. -/
lemma aSeq_lower_even {m : ℕ} (hm : 2 ≤ m) {c : ℝ} (hc : 0 < c) :
    lowerEvenProd m / c ^ (m - 1) ≤ aSeq c (2 * m) := by
  obtain ⟨k, rfl⟩ := Nat.exists_eq_add_of_le hm
  induction k with
  | zero =>
      have hP : lowerEvenProd 2 = 15 := by
        unfold lowerEvenProd
        norm_num
      have hpow : c ^ (2 - 1) = c := by norm_num
      rw [hP, hpow, aSeq_four]
      rw [div_eq_mul_inv]
      nlinarith
  | succ k ih =>
      have ih' := ih (by omega : 2 ≤ 2 + k)
      have hstep := aSeq_lower_step hc (n := 2 * (2 + k)) (by omega : 2 ≤ 2 * (2 + k))
      have hApos : (0 : ℝ) ≤ ((4 * (2 * (2 + k)) ^ 2 - 1 : ℕ) : ℝ) / c := by
        exact div_nonneg
          (by
            have hle : 1 ≤ 4 * (2 * (2 + k)) ^ 2 := by
              have hsq : 1 ≤ (2 * (2 + k)) ^ 2 := one_le_sq (by omega : 1 ≤ 2 * (2 + k))
              omega
            exact_mod_cast (by omega : 0 ≤ 4 * (2 * (2 + k)) ^ 2 - 1))
          (le_of_lt hc)
      have hmul : ((4 * (2 * (2 + k)) ^ 2 - 1 : ℕ) : ℝ) / c *
            (lowerEvenProd (2 + k) / c ^ (2 + k - 1))
          ≤ ((4 * (2 * (2 + k)) ^ 2 - 1 : ℕ) : ℝ) / c * aSeq c (2 * (2 + k)) :=
        mul_le_mul_of_nonneg_left ih' hApos
      have htrans : ((4 * (2 * (2 + k)) ^ 2 - 1 : ℕ) : ℝ) / c *
            (lowerEvenProd (2 + k) / c ^ (2 + k - 1))
          ≤ aSeq c (2 * (2 + k) + 2) := le_trans hmul hstep
      have hprod : lowerEvenProd (2 + (k + 1)) =
          ((4 * (2 * (2 + k)) ^ 2 - 1 : ℕ) : ℝ) * lowerEvenProd (2 + k) := by
        unfold lowerEvenProd
        have hrange1 : 2 + (k + 1) - 1 = k + 1 + 1 := by omega
        have hrange2 : 2 + k - 1 = k + 1 := by omega
        rw [hrange1, hrange2, Finset.prod_range_succ]
        rw [mul_comm]
        congr 1
        have harg : 2 * ((k + 1) + 1) = 2 * (2 + k) := by omega
        rw [harg]
      have hpow2 : c ^ (2 + (k + 1) - 1) = c ^ (2 + k - 1) * c := by
        have hpow1 : 2 + (k + 1) - 1 = 2 + k - 1 + 1 := by omega
        rw [hpow1, pow_succ', mul_comm]
      calc
        lowerEvenProd (2 + (k + 1)) / c ^ (2 + (k + 1) - 1)
            = ((4 * (2 * (2 + k)) ^ 2 - 1 : ℕ) : ℝ) * lowerEvenProd (2 + k) /
                (c ^ (2 + k - 1) * c) := by
                rw [hprod, hpow2]
        _ = ((4 * (2 * (2 + k)) ^ 2 - 1 : ℕ) : ℝ) / c *
              (lowerEvenProd (2 + k) / c ^ (2 + k - 1)) := by
                field_simp [ne_of_gt hc]
        _ ≤ aSeq c (2 * (2 + k) + 2) := htrans
        _ = aSeq c (2 * (2 + (k + 1))) := by
                congr 1

/-- Odd indices: `a_{2m+1} >= lowerOddProd m / c^(m-1)` for `m >= 2`, `c > 0`. -/
lemma aSeq_lower_odd {m : ℕ} (hm : 2 ≤ m) {c : ℝ} (hc : 0 < c) :
    lowerOddProd m / c ^ (m - 1) ≤ aSeq c (2 * m + 1) := by
  obtain ⟨k, rfl⟩ := Nat.exists_eq_add_of_le hm
  induction k with
  | zero =>
      have hP : lowerOddProd 2 = 35 := by
        unfold lowerOddProd
        norm_num
      have hpow : c ^ (2 - 1) = c := by norm_num
      rw [hP, hpow, aSeq_five]
      rw [div_eq_mul_inv]
      nlinarith
  | succ k ih =>
      have ih' := ih (by omega : 2 ≤ 2 + k)
      have hstep := aSeq_lower_step hc (n := 2 * (2 + k) + 1) (by omega : 2 ≤ 2 * (2 + k) + 1)
      have hApos : (0 : ℝ) ≤ ((4 * (2 * (2 + k) + 1) ^ 2 - 1 : ℕ) : ℝ) / c := by
        exact div_nonneg
          (by
            have hle : 1 ≤ 4 * (2 * (2 + k) + 1) ^ 2 := by
              have hsq : 1 ≤ (2 * (2 + k) + 1) ^ 2 := one_le_sq (by omega : 1 ≤ 2 * (2 + k) + 1)
              omega
            exact_mod_cast (by omega : 0 ≤ 4 * (2 * (2 + k) + 1) ^ 2 - 1))
          (le_of_lt hc)
      have hmul : ((4 * (2 * (2 + k) + 1) ^ 2 - 1 : ℕ) : ℝ) / c *
            (lowerOddProd (2 + k) / c ^ (2 + k - 1))
          ≤ ((4 * (2 * (2 + k) + 1) ^ 2 - 1 : ℕ) : ℝ) / c * aSeq c (2 * (2 + k) + 1) :=
        mul_le_mul_of_nonneg_left ih' hApos
      have htrans : ((4 * (2 * (2 + k) + 1) ^ 2 - 1 : ℕ) : ℝ) / c *
            (lowerOddProd (2 + k) / c ^ (2 + k - 1))
          ≤ aSeq c (2 * (2 + k) + 1 + 2) := le_trans hmul hstep
      have hprod : lowerOddProd (2 + (k + 1)) =
          ((4 * (2 * (2 + k) + 1) ^ 2 - 1 : ℕ) : ℝ) * lowerOddProd (2 + k) := by
        unfold lowerOddProd
        have hrange1 : 2 + (k + 1) - 1 = k + 1 + 1 := by omega
        have hrange2 : 2 + k - 1 = k + 1 := by omega
        rw [hrange1, hrange2, Finset.prod_range_succ]
        rw [mul_comm]
        congr 1
        have harg : 2 * ((k + 1) + 1) + 1 = 2 * (2 + k) + 1 := by omega
        rw [harg]
      have hpow2 : c ^ (2 + (k + 1) - 1) = c ^ (2 + k - 1) * c := by
        have hpow1 : 2 + (k + 1) - 1 = 2 + k - 1 + 1 := by omega
        rw [hpow1, pow_succ', mul_comm]
      calc
        lowerOddProd (2 + (k + 1)) / c ^ (2 + (k + 1) - 1)
            = ((4 * (2 * (2 + k) + 1) ^ 2 - 1 : ℕ) : ℝ) * lowerOddProd (2 + k) /
                (c ^ (2 + k - 1) * c) := by
                rw [hprod, hpow2]
        _ = ((4 * (2 * (2 + k) + 1) ^ 2 - 1 : ℕ) : ℝ) / c *
              (lowerOddProd (2 + k) / c ^ (2 + k - 1)) := by
                field_simp [ne_of_gt hc]
        _ ≤ aSeq c (2 * (2 + k) + 1 + 2) := htrans
        _ = aSeq c (2 * (2 + (k + 1)) + 1) := by
                congr 1

/-! ## Upper growth bounds (valid for `0 < c <= 1`) -/

/-- Even indices: `a_{2m} <= upperEvenProd m / c^(m-1)` for `m >= 2`, `0 < c <= 1`. -/
lemma aSeq_upper_even {m : ℕ} (hm : 2 ≤ m) {c : ℝ} (hc : 0 < c) (hcle : c ≤ 1) :
    aSeq c (2 * m) ≤ upperEvenProd m / c ^ (m - 1) := by
  obtain ⟨k, rfl⟩ := Nat.exists_eq_add_of_le hm
  induction k with
  | zero =>
      have hP : upperEvenProd 2 = 24 := by norm_num [upperEvenProd]
      have hpow : c ^ (2 - 1) = c := by norm_num
      rw [hP, hpow, aSeq_four]
      rw [div_eq_mul_inv]
      have h1c : (1 : ℝ) ≤ c⁻¹ := by simpa using one_le_one_div hc hcle
      have h9 : (9 : ℝ) ≤ 9 * c⁻¹ := by
        have h := mul_le_mul_of_nonneg_left h1c (by norm_num : (0 : ℝ) ≤ 9)
        simpa only [mul_one] using h
      have hgoal : (1 : ℝ) ≤ 9 * c⁻¹ := le_trans (by norm_num : (1 : ℝ) ≤ 9) h9
      calc
        1 + 15 * c⁻¹ ≤ 9 * c⁻¹ + 15 * c⁻¹ := add_le_add hgoal le_rfl
        _ = 24 * c⁻¹ := by ring
  | succ k ih =>
      have ih' := ih (by omega : 2 ≤ 2 + k)
      have hstep := aSeq_upper_step hc hcle (n := 2 * (2 + k)) (by omega : 2 ≤ 2 * (2 + k))
      have hcast2 : ↑(2 * (2 + k)) = 2 * (2 + ↑k) := by norm_cast
      have hstep' : aSeq c (2 * (2 + k) + 2) ≤ 6 * (2 * (2 + ↑k)) ^ 2 / c * aSeq c (2 * (2 + k)) := by
        simpa [hcast2] using hstep
      have hcoefnn : 0 ≤ 6 * (2 * (2 + ↑k)) ^ 2 / c :=
        div_nonneg (by nlinarith) (le_of_lt hc)
      have hmul : 6 * (2 * (2 + ↑k)) ^ 2 / c * aSeq c (2 * (2 + k))
          ≤ 6 * (2 * (2 + ↑k)) ^ 2 / c * (upperEvenProd (2 + k) / c ^ (2 + k - 1)) :=
        mul_le_mul_of_nonneg_left ih' hcoefnn
      have hprod : upperEvenProd (2 + (k + 1)) =
          ((6 * (2 * (2 + k)) ^ 2 : ℕ) : ℝ) * upperEvenProd (2 + k) := by
        unfold upperEvenProd
        have hrange1 : 2 + (k + 1) - 1 = k + 1 + 1 := by omega
        have hrange2 : 2 + k - 1 = k + 1 := by omega
        rw [hrange1, hrange2, Finset.prod_range_succ]
        rw [mul_comm]
        congr 1
        have harg : 2 * ((k + 1) + 1) = 2 * (2 + k) := by omega
        rw [harg]
      have hcast : ((6 * (2 * (2 + k)) ^ 2 : ℕ) : ℝ) = 6 * (2 * (2 + ↑k)) ^ 2 := by norm_cast
      have hpow2 : c ^ (2 + (k + 1) - 1) = c ^ (2 + k - 1) * c := by
        have hpow1 : 2 + (k + 1) - 1 = 2 + k - 1 + 1 := by omega
        rw [hpow1, pow_succ', mul_comm]
      calc
        aSeq c (2 * (2 + (k + 1)))
            = aSeq c (2 * (2 + k) + 2) := by congr 1
        _ ≤ 6 * (2 * (2 + ↑k)) ^ 2 / c * aSeq c (2 * (2 + k)) := hstep'
        _ ≤ 6 * (2 * (2 + ↑k)) ^ 2 / c * (upperEvenProd (2 + k) / c ^ (2 + k - 1)) := hmul
        _ = ((6 * (2 * (2 + k)) ^ 2 : ℕ) : ℝ) / c * (upperEvenProd (2 + k) / c ^ (2 + k - 1)) := by
                rw [← hcast]
        _ = ((6 * (2 * (2 + k)) ^ 2 : ℕ) : ℝ) * upperEvenProd (2 + k) / (c ^ (2 + k - 1) * c) := by
                field_simp [ne_of_gt hc]
        _ = upperEvenProd (2 + (k + 1)) / c ^ (2 + (k + 1) - 1) := by rw [← hprod, ← hpow2]

/-- Odd indices: `a_{2m+1} <= upperOddProd m / c^(m-1)` for `m >= 2`, `0 < c <= 1`. -/
lemma aSeq_upper_odd {m : ℕ} (hm : 2 ≤ m) {c : ℝ} (hc : 0 < c) (hcle : c ≤ 1) :
    aSeq c (2 * m + 1) ≤ upperOddProd m / c ^ (m - 1) := by
  obtain ⟨k, rfl⟩ := Nat.exists_eq_add_of_le hm
  induction k with
  | zero =>
      have hP : upperOddProd 2 = 54 := by norm_num [upperOddProd]
      have hpow : c ^ (2 - 1) = c := by norm_num
      rw [hP, hpow, aSeq_five]
      rw [div_eq_mul_inv]
      have h1c : (1 : ℝ) ≤ c⁻¹ := by simpa using one_le_one_div hc hcle
      have h19 : (19 : ℝ) ≤ 19 * c⁻¹ := by
        have h := mul_le_mul_of_nonneg_left h1c (by norm_num : (0 : ℝ) ≤ 19)
        simpa only [mul_one] using h
      have hgoal : (1 : ℝ) ≤ 19 * c⁻¹ := le_trans (by norm_num : (1 : ℝ) ≤ 19) h19
      calc
        1 + 35 * c⁻¹ ≤ 19 * c⁻¹ + 35 * c⁻¹ := add_le_add hgoal le_rfl
        _ = 54 * c⁻¹ := by ring
  | succ k ih =>
      have ih' := ih (by omega : 2 ≤ 2 + k)
      have hstep := aSeq_upper_step hc hcle (n := 2 * (2 + k) + 1) (by omega : 2 ≤ 2 * (2 + k) + 1)
      have hcast2 : ↑(2 * (2 + k) + 1) = 2 * (2 + ↑k) + 1 := by norm_cast
      have hstep' : aSeq c (2 * (2 + k) + 1 + 2) ≤ 6 * (2 * (2 + ↑k) + 1) ^ 2 / c * aSeq c (2 * (2 + k) + 1) := by
        simpa [hcast2] using hstep
      have hcoefnn : 0 ≤ 6 * (2 * (2 + ↑k) + 1) ^ 2 / c :=
        div_nonneg (by nlinarith) (le_of_lt hc)
      have hmul : 6 * (2 * (2 + ↑k) + 1) ^ 2 / c * aSeq c (2 * (2 + k) + 1)
          ≤ 6 * (2 * (2 + ↑k) + 1) ^ 2 / c * (upperOddProd (2 + k) / c ^ (2 + k - 1)) :=
        mul_le_mul_of_nonneg_left ih' hcoefnn
      have hprod : upperOddProd (2 + (k + 1)) =
          ((6 * (2 * (2 + k) + 1) ^ 2 : ℕ) : ℝ) * upperOddProd (2 + k) := by
        unfold upperOddProd
        have hrange1 : 2 + (k + 1) - 1 = k + 1 + 1 := by omega
        have hrange2 : 2 + k - 1 = k + 1 := by omega
        rw [hrange1, hrange2, Finset.prod_range_succ]
        rw [mul_comm]
        congr 1
        have harg : 2 * ((k + 1) + 1) + 1 = 2 * (2 + k) + 1 := by omega
        rw [harg]
      have hcast : ((6 * (2 * (2 + k) + 1) ^ 2 : ℕ) : ℝ) = 6 * (2 * (2 + ↑k) + 1) ^ 2 := by norm_cast
      have hpow2 : c ^ (2 + (k + 1) - 1) = c ^ (2 + k - 1) * c := by
        have hpow1 : 2 + (k + 1) - 1 = 2 + k - 1 + 1 := by omega
        rw [hpow1, pow_succ', mul_comm]
      calc
        aSeq c (2 * (2 + (k + 1)) + 1)
            = aSeq c (2 * (2 + k) + 1 + 2) := by congr 1
        _ ≤ 6 * (2 * (2 + ↑k) + 1) ^ 2 / c * aSeq c (2 * (2 + k) + 1) := hstep'
        _ ≤ 6 * (2 * (2 + ↑k) + 1) ^ 2 / c * (upperOddProd (2 + k) / c ^ (2 + k - 1)) := hmul
        _ = ((6 * (2 * (2 + k) + 1) ^ 2 : ℕ) : ℝ) / c * (upperOddProd (2 + k) / c ^ (2 + k - 1)) := by
                rw [← hcast]
        _ = ((6 * (2 * (2 + k) + 1) ^ 2 : ℕ) : ℝ) * upperOddProd (2 + k) / (c ^ (2 + k - 1) * c) := by
                field_simp [ne_of_gt hc]
        _ = upperOddProd (2 + (k + 1)) / c ^ (2 + (k + 1) - 1) := by rw [← hprod, ← hpow2]

/-! ## The two-sided Θ growth bounds (Theorem "high", first sentence) -/

/-- Even case of Theorem "high": for `0 < c <= 1` the coefficient `a_{2m}` is
exactly of order `c^-(m-1)` (equivalently `c^(-(n-2)/2)` with `n = 2m`), with
the explicit positive constants `lowerEvenProd m` and `upperEvenProd m`. -/
theorem aSeq_growth_even {m : ℕ} (hm : 2 ≤ m) {c : ℝ} (hc : 0 < c) (hcle : c ≤ 1) :
    lowerEvenProd m / c ^ (m - 1) ≤ aSeq c (2 * m) ∧
      aSeq c (2 * m) ≤ upperEvenProd m / c ^ (m - 1) :=
  ⟨aSeq_lower_even hm hc, aSeq_upper_even hm hc hcle⟩

/-- Odd case of Theorem "high": for `0 < c <= 1` the coefficient `a_{2m+1}` is
exactly of order `c^-(m-1)` (equivalently `c^(-(n-3)/2)` with `n = 2m+1`), with
the explicit positive constants `lowerOddProd m` and `upperOddProd m`. -/
theorem aSeq_growth_odd {m : ℕ} (hm : 2 ≤ m) {c : ℝ} (hc : 0 < c) (hcle : c ≤ 1) :
    lowerOddProd m / c ^ (m - 1) ≤ aSeq c (2 * m + 1) ∧
      aSeq c (2 * m + 1) ≤ upperOddProd m / c ^ (m - 1) :=
  ⟨aSeq_lower_odd hm hc, aSeq_upper_odd hm hc hcle⟩

/-! ## Divergence of all high norms (Theorem "high", consequence) -/

/-- `C / c^r -> +infinity` as `c -> 0+` for any `r >= 1` and `C > 0`. -/
lemma tendsto_const_div_pow_nhdsWithin_0_pos_atTop (C : ℝ) (hC : 0 < C) (r : ℕ) (hr : 1 ≤ r) :
    Tendsto (fun c : ℝ => C / c ^ r) (𝓝[>] (0 : ℝ)) atTop := by
  have hbg : Tendsto (fun c : ℝ => C / c) (𝓝[>] 0) atTop := by
    have h := tendsto_inv_nhdsWithin_0_pos_atTop.const_mul_atTop hC
    simpa [div_eq_mul_inv] using h
  refine tendsto_atTop_mono' (𝓝[>] (0 : ℝ)) (f₁ := fun c : ℝ => C / c)
    (f₂ := fun c : ℝ => C / c ^ r) ?hle hbg
  change ({c : ℝ | C / c ≤ C / c ^ r} ∈ 𝓝[>] (0 : ℝ))
  rw [Metric.mem_nhdsWithin_iff]
  refine ⟨1, by norm_num, ?_⟩
  intro c hc
  rcases hc with ⟨hcball, hcpos⟩
  have hcpos' : 0 < c := by simpa using hcpos
  have hcabs : |c| < 1 := by
    simpa [Real.dist_eq] using (Metric.mem_ball.mp hcball)
  have hclt1 : c < 1 := by
    rwa [abs_of_nonneg (le_of_lt hcpos')] at hcabs
  have hpowle : c ^ r ≤ c := by
    obtain ⟨s, rfl⟩ := Nat.exists_eq_add_of_le hr
    rw [pow_add, pow_one]
    have hcs : c ^ s ≤ 1 := pow_le_one₀ (le_of_lt hcpos') (le_of_lt hclt1)
    simpa [mul_one] using mul_le_mul_of_nonneg_left hcs (le_of_lt hcpos')
  have hleinv : 1 / c ≤ 1 / c ^ r :=
    one_div_le_one_div_of_le (pow_pos hcpos' r) hpowle
  simpa [div_eq_mul_inv] using mul_le_mul_of_nonneg_left hleinv (le_of_lt hC)

/-- Lower bound for `||K_{2m}||^2` from the norm formula and the even lower
growth bound: `||K_{2m}||^2 >= C / c^(2m-2)` with an explicit positive `C`. -/
lemma norm_even_ge {c : ℝ} (hc : 0 < c) {m : ℕ} (hm : 2 ≤ m)
    (hK : KreinSobolevFacts c (kS c)) :
    (2 / (2 * (2 * (m : ℝ)) + 1)) * lowerEvenProd m * lowerEvenProd (m + 1) / c ^ (2 * m - 2)
      ≤ h1PairingPoly c (kS c (2 * m)) (kS c (2 * m)) := by
  have hnorm : h1PairingPoly c (kS c (2 * m)) (kS c (2 * m))
      = 2 * c / (2 * (2 * (m : ℝ)) + 1) * aSeq c (2 * m) * aSeq c (2 * m + 2) := by
    have h := hK.1 (2 * m) (2 * m)
    simpa using h
  have ha1 : lowerEvenProd m / c ^ (m - 1) ≤ aSeq c (2 * m) := aSeq_lower_even hm hc
  have ha2 : lowerEvenProd (m + 1) / c ^ m ≤ aSeq c (2 * m + 2) := by
    have h := aSeq_lower_even (m := m + 1) (by omega : 2 ≤ m + 1) hc
    have hsub : m + 1 - 1 = m := by omega
    have hind : 2 * (m + 1) = 2 * m + 2 := by omega
    simpa [hsub, hind] using h
  have hpos1 : 0 ≤ lowerEvenProd m / c ^ (m - 1) :=
    div_nonneg (le_of_lt (lowerEvenProd_pos m)) (pow_nonneg (le_of_lt hc) (m - 1))
  have hpos2 : 0 ≤ lowerEvenProd (m + 1) / c ^ m :=
    div_nonneg (le_of_lt (lowerEvenProd_pos (m + 1))) (pow_nonneg (le_of_lt hc) m)
  have hpos3 : 0 ≤ aSeq c (2 * m) := aSeq_nonneg hc (2 * m)
  have hprod : lowerEvenProd m / c ^ (m - 1) * (lowerEvenProd (m + 1) / c ^ m)
      ≤ aSeq c (2 * m) * aSeq c (2 * m + 2) := by
    exact mul_le_mul ha1 ha2 hpos2 hpos3
  have hcoef : 0 ≤ 2 * c / (2 * (2 * (m : ℝ)) + 1) :=
    div_nonneg (mul_nonneg (by norm_num) (le_of_lt hc))
      (by
        have hm0 : (0 : ℝ) ≤ (m : ℝ) := Nat.cast_nonneg m
        nlinarith)
  have hmul := mul_le_mul_of_nonneg_left hprod hcoef
  rw [hnorm]
  have hc' : c ≠ 0 := ne_of_gt hc
  have hpow1' : c ^ (m - 1) * c ^ m = c ^ (2 * m - 1) := by
    have hsum : m - 1 + m = 2 * m - 1 := by omega
    rw [← pow_add, hsum]
  have hpow2 : c * c ^ (2 * m - 2) = c ^ (2 * m - 1) := by
    have hsucc : 2 * m - 2 + 1 = 2 * m - 1 := by omega
    rw [← hsucc, pow_succ']
  have halg : 2 * c / (2 * (2 * (m : ℝ)) + 1) *
        (lowerEvenProd m / c ^ (m - 1) * (lowerEvenProd (m + 1) / c ^ m))
      = (2 / (2 * (2 * (m : ℝ)) + 1)) * lowerEvenProd m * lowerEvenProd (m + 1) / c ^ (2 * m - 2) := by
    have h1 : 2 * c / (2 * (2 * (m : ℝ)) + 1) *
          (lowerEvenProd m / c ^ (m - 1) * (lowerEvenProd (m + 1) / c ^ m))
        = 2 * c * lowerEvenProd m * lowerEvenProd (m + 1) /
            ((2 * (2 * (m : ℝ)) + 1) * (c ^ (m - 1) * c ^ m)) := by
      field_simp [hc']
    rw [h1, hpow1']
    rw [← hpow2]
    field_simp [hc']
  have hmain : (2 / (2 * (2 * (m : ℝ)) + 1)) * lowerEvenProd m * lowerEvenProd (m + 1) / c ^ (2 * m - 2)
      ≤ 2 * c / (2 * (2 * (m : ℝ)) + 1) * aSeq c (2 * m) * aSeq c (2 * m + 2) := by
    rw [← halg]
    simpa [mul_assoc] using hmul
  exact hmain

/-- Lower bound for `||K_{2m+1}||^2` from the norm formula and the odd lower
growth bound: `||K_{2m+1}||^2 >= C / c^(2m-2)` with an explicit positive `C`. -/
lemma norm_odd_ge {c : ℝ} (hc : 0 < c) {m : ℕ} (hm : 2 ≤ m)
    (hK : KreinSobolevFacts c (kS c)) :
    (2 / (2 * (2 * (m : ℝ) + 1) + 1)) * lowerOddProd m * lowerOddProd (m + 1) / c ^ (2 * m - 2)
      ≤ h1PairingPoly c (kS c (2 * m + 1)) (kS c (2 * m + 1)) := by
  have hnorm : h1PairingPoly c (kS c (2 * m + 1)) (kS c (2 * m + 1))
      = 2 * c / (2 * (2 * (m : ℝ) + 1) + 1) * aSeq c (2 * m + 1) * aSeq c (2 * m + 3) := by
    have h := hK.1 (2 * m + 1) (2 * m + 1)
    simpa [show 2 * m + 1 + 2 = 2 * m + 3 by omega] using h
  have ha1 : lowerOddProd m / c ^ (m - 1) ≤ aSeq c (2 * m + 1) := aSeq_lower_odd hm hc
  have ha2 : lowerOddProd (m + 1) / c ^ m ≤ aSeq c (2 * m + 3) := by
    have h := aSeq_lower_odd (m := m + 1) (by omega : 2 ≤ m + 1) hc
    have hsub : m + 1 - 1 = m := by omega
    have hind : 2 * (m + 1) + 1 = 2 * m + 3 := by omega
    simpa [hsub, hind] using h
  have hpos1 : 0 ≤ lowerOddProd m / c ^ (m - 1) :=
    div_nonneg (le_of_lt (lowerOddProd_pos m)) (pow_nonneg (le_of_lt hc) (m - 1))
  have hpos2 : 0 ≤ lowerOddProd (m + 1) / c ^ m :=
    div_nonneg (le_of_lt (lowerOddProd_pos (m + 1))) (pow_nonneg (le_of_lt hc) m)
  have hpos3 : 0 ≤ aSeq c (2 * m + 1) := aSeq_nonneg hc (2 * m + 1)
  have hprod : lowerOddProd m / c ^ (m - 1) * (lowerOddProd (m + 1) / c ^ m)
      ≤ aSeq c (2 * m + 1) * aSeq c (2 * m + 3) := by
    exact mul_le_mul ha1 ha2 hpos2 hpos3
  have hcoef : 0 ≤ 2 * c / (2 * (2 * (m : ℝ) + 1) + 1) :=
    div_nonneg (mul_nonneg (by norm_num) (le_of_lt hc))
      (by
        have hm0 : (0 : ℝ) ≤ (m : ℝ) := Nat.cast_nonneg m
        nlinarith)
  have hmul := mul_le_mul_of_nonneg_left hprod hcoef
  rw [hnorm]
  have hc' : c ≠ 0 := ne_of_gt hc
  have hpow1' : c ^ (m - 1) * c ^ m = c ^ (2 * m - 1) := by
    have hsum : m - 1 + m = 2 * m - 1 := by omega
    rw [← pow_add, hsum]
  have hpow2 : c * c ^ (2 * m - 2) = c ^ (2 * m - 1) := by
    have hsucc : 2 * m - 2 + 1 = 2 * m - 1 := by omega
    rw [← hsucc, pow_succ']
  have halg : 2 * c / (2 * (2 * (m : ℝ) + 1) + 1) *
        (lowerOddProd m / c ^ (m - 1) * (lowerOddProd (m + 1) / c ^ m))
      = (2 / (2 * (2 * (m : ℝ) + 1) + 1)) * lowerOddProd m * lowerOddProd (m + 1) / c ^ (2 * m - 2) := by
    have h1 : 2 * c / (2 * (2 * (m : ℝ) + 1) + 1) *
          (lowerOddProd m / c ^ (m - 1) * (lowerOddProd (m + 1) / c ^ m))
        = 2 * c * lowerOddProd m * lowerOddProd (m + 1) /
            ((2 * (2 * (m : ℝ) + 1) + 1) * (c ^ (m - 1) * c ^ m)) := by
      field_simp [hc']
    rw [h1, hpow1']
    rw [← hpow2]
    field_simp [hc']
  have hmain : (2 / (2 * (2 * (m : ℝ) + 1) + 1)) * lowerOddProd m * lowerOddProd (m + 1) / c ^ (2 * m - 2)
      ≤ 2 * c / (2 * (2 * (m : ℝ) + 1) + 1) * aSeq c (2 * m + 1) * aSeq c (2 * m + 3) := by
    rw [← halg]
    simpa [mul_assoc] using hmul
  exact hmain

/-- `||K_{2m}||^2 -> +infinity` as `c -> 0+` for `m >= 2`. -/
theorem tendsto_norm_even_atTop (hK : ∀ c : ℝ, KreinSobolevFacts c (kS c)) {m : ℕ} (hm : 2 ≤ m) :
    Tendsto (fun c : ℝ => h1PairingPoly c (kS c (2 * m)) (kS c (2 * m))) (𝓝[>] 0) atTop := by
  have hCpos : 0 < (2 / (2 * (2 * (m : ℝ)) + 1)) * lowerEvenProd m * lowerEvenProd (m + 1) := by
    have hD : 0 < (2 * (2 * (m : ℝ)) + 1) := by
      have hm0 : (0 : ℝ) ≤ (m : ℝ) := Nat.cast_nonneg m
      nlinarith
    have hdiv : 0 < 2 / (2 * (2 * (m : ℝ)) + 1) := div_pos (by norm_num) hD
    exact mul_pos (mul_pos hdiv (lowerEvenProd_pos m)) (lowerEvenProd_pos (m + 1))
  have hbg : Tendsto (fun c : ℝ =>
      (2 / (2 * (2 * (m : ℝ)) + 1)) * lowerEvenProd m * lowerEvenProd (m + 1) / c ^ (2 * m - 2))
      (𝓝[>] 0) atTop :=
    tendsto_const_div_pow_nhdsWithin_0_pos_atTop
      ((2 / (2 * (2 * (m : ℝ)) + 1)) * lowerEvenProd m * lowerEvenProd (m + 1)) hCpos (2 * m - 2)
      (by omega)
  refine tendsto_atTop_mono' (𝓝[>] (0 : ℝ))
    (f₁ := fun c : ℝ => (2 / (2 * (2 * (m : ℝ)) + 1)) * lowerEvenProd m * lowerEvenProd (m + 1) / c ^ (2 * m - 2))
    (f₂ := fun c : ℝ => h1PairingPoly c (kS c (2 * m)) (kS c (2 * m))) ?hle hbg
  change ({c : ℝ | (2 / (2 * (2 * (m : ℝ)) + 1)) * lowerEvenProd m * lowerEvenProd (m + 1) / c ^ (2 * m - 2)
      ≤ h1PairingPoly c (kS c (2 * m)) (kS c (2 * m))} ∈ 𝓝[>] (0 : ℝ))
  filter_upwards [self_mem_nhdsWithin] with c hc
  have hcpos : 0 < c := by simpa using hc
  exact norm_even_ge hcpos hm (hK c)

/-- `||K_{2m+1}||^2 -> +infinity` as `c -> 0+` for `m >= 2`. -/
theorem tendsto_norm_odd_atTop (hK : ∀ c : ℝ, KreinSobolevFacts c (kS c)) {m : ℕ} (hm : 2 ≤ m) :
    Tendsto (fun c : ℝ => h1PairingPoly c (kS c (2 * m + 1)) (kS c (2 * m + 1))) (𝓝[>] 0) atTop := by
  have hCpos : 0 < (2 / (2 * (2 * (m : ℝ) + 1) + 1)) * lowerOddProd m * lowerOddProd (m + 1) := by
    have hD : 0 < (2 * (2 * (m : ℝ) + 1) + 1) := by
      have hm0 : (0 : ℝ) ≤ (m : ℝ) := Nat.cast_nonneg m
      nlinarith
    have hdiv : 0 < 2 / (2 * (2 * (m : ℝ) + 1) + 1) := div_pos (by norm_num) hD
    exact mul_pos (mul_pos hdiv (lowerOddProd_pos m)) (lowerOddProd_pos (m + 1))
  have hbg : Tendsto (fun c : ℝ =>
      (2 / (2 * (2 * (m : ℝ) + 1) + 1)) * lowerOddProd m * lowerOddProd (m + 1) / c ^ (2 * m - 2))
      (𝓝[>] 0) atTop :=
    tendsto_const_div_pow_nhdsWithin_0_pos_atTop
      ((2 / (2 * (2 * (m : ℝ) + 1) + 1)) * lowerOddProd m * lowerOddProd (m + 1)) hCpos (2 * m - 2)
      (by omega)
  refine tendsto_atTop_mono' (𝓝[>] (0 : ℝ))
    (f₁ := fun c : ℝ => (2 / (2 * (2 * (m : ℝ) + 1) + 1)) * lowerOddProd m * lowerOddProd (m + 1) / c ^ (2 * m - 2))
    (f₂ := fun c : ℝ => h1PairingPoly c (kS c (2 * m + 1)) (kS c (2 * m + 1))) ?hle hbg
  change ({c : ℝ | (2 / (2 * (2 * (m : ℝ) + 1) + 1)) * lowerOddProd m * lowerOddProd (m + 1) / c ^ (2 * m - 2)
      ≤ h1PairingPoly c (kS c (2 * m + 1)) (kS c (2 * m + 1))} ∈ 𝓝[>] (0 : ℝ))
  filter_upwards [self_mem_nhdsWithin] with c hc
  have hcpos : 0 < c := by simpa using hc
  exact norm_odd_ge hcpos hm (hK c)

/- Theorem "high", general part: `||K_n^{(c)}||^2 -> +infinity` as `c -> 0+`
for every `n >= 4`. -/
set_option maxHeartbeats 800000 in
theorem tendsto_norm_atTop (hK : ∀ c : ℝ, KreinSobolevFacts c (kS c)) {n : ℕ} (hn : 4 ≤ n) :
    Tendsto (fun c : ℝ => h1PairingPoly c (kS c n) (kS c n)) (𝓝[>] 0) atTop := by
  rcases Nat.even_or_odd' n with ⟨m, rfl | rfl⟩
  · exact tendsto_norm_even_atTop hK (by omega : 2 ≤ m)
  · exact tendsto_norm_odd_atTop hK (by omega : 2 ≤ m)

end

end KreinHighGrowth

end SL
