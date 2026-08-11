import Mathlib

/-!
# L² moment bound on [-1,1]

Formalization of the polynomial moment bound from
`docs/SL_h2_completeness_proof.tex` (Section 3.3) and
`tools/left-definite-moment-recurrence.md`.

For g continuous on [-1,1] the k-th moment
    mu_k = ∫_{-1}^1 g(x) · x^k dx
satisfies
    |mu_k| ≤ ‖g‖_2 · sqrt (2 / (2k+1)),
where ‖g‖_2 = sqrt (∫_{-1}^1 g^2) and
‖x^k‖_2^2 = ∫_{-1}^1 x^(2k) = 2/(2k+1).

The proof is Cauchy-Schwarz specialized to the pair (g, x^k) via the
quadratic trick: since ∫ (g - c·x^k)^2 ≥ 0 for c = B/C with
B = ∫ g·x^k and C = ∫ x^(2k) > 0, we get B^2 ≤ A·C with
A = ∫ g^2.  This avoids the degenerate case C = 0 (here C is always
positive), which is why the lemma is specialized to the pair (g, x^k)
rather than stated for two arbitrary functions.

The L²-moments here are the integrals of g·x^k over [-1,1]; they are
the base-change to Real of the rational moments in SL/MomentRecurrence.lean.
-/

namespace SL

namespace MomentBound

open scoped Real Interval
open MeasureTheory

/-- The k-th L² moment of g on [-1,1]: mu_k = ∫_{-1}^1 g(x) · x^k dx. -/
noncomputable def moments (g : ℝ → ℝ) (k : ℕ) : ℝ :=
  ∫ x in (-1 : ℝ)..1, g x * x ^ k

/-- ∫_{-1}^1 x^(2k) dx = 2 / (2k+1). -/
lemma integral_x_pow_even (k : ℕ) :
    (∫ x in (-1 : ℝ)..1, x ^ (2 * k)) = 2 / ((2 * k + 1 : ℕ) : ℝ) := by
  rw [integral_pow]
  have heven : (-1 : ℝ) ^ (2 * k) = 1 := by
    rw [pow_mul, neg_one_sq]
    simp
  have hodd : (-1 : ℝ) ^ (2 * k + 1) = -1 := by
    rw [pow_succ, heven]
    ring
  have h1 : (1 : ℝ) ^ (2 * k + 1) = 1 := by simp
  rw [h1, hodd]
  norm_num

/-- ‖x^k‖_2^2 on [-1,1] equals 2 / (2k+1). -/
lemma norm_sq_x_pow (k : ℕ) :
    (∫ x in (-1 : ℝ)..1, (x ^ k) ^ 2) = 2 / ((2 * k + 1 : ℕ) : ℝ) := by
  have hsq : (fun x : ℝ => (x ^ k) ^ 2) = fun x : ℝ => x ^ (2 * k) := by
    funext x
    rw [← pow_mul]
    rw [show k * 2 = 2 * k by omega]
  rw [hsq]
  exact integral_x_pow_even k

/-- Cauchy-Schwarz for the pair (g, x^k) on [-1,1]:
    (∫ g·x^k)^2 ≤ (∫ g^2) · (∫ x^(2k)). -/
lemma cs_moment {g : ℝ → ℝ} (hg : ContinuousOn g (Set.Icc (-1) 1)) (k : ℕ) :
    (∫ x in (-1 : ℝ)..1, g x * x ^ k) ^ 2 ≤
      (∫ x in (-1 : ℝ)..1, g x ^ 2) * (∫ x in (-1 : ℝ)..1, x ^ (2 * k)) := by
  let A : ℝ := ∫ x in (-1 : ℝ)..1, g x ^ 2
  let B : ℝ := ∫ x in (-1 : ℝ)..1, g x * x ^ k
  let C : ℝ := ∫ x in (-1 : ℝ)..1, x ^ (2 * k)
  have hC_pos : 0 < C := by
    dsimp [C]
    rw [integral_x_pow_even]
    positivity
  have hC_ne : C ≠ 0 := ne_of_gt hC_pos
  let c : ℝ := B / C
  have hnonneg : 0 ≤ ∫ x in (-1 : ℝ)..1, (g x - c * x ^ k) ^ 2 := by
    exact intervalIntegral.integral_nonneg (by norm_num : (-1 : ℝ) ≤ 1)
      (by intro x hx; exact sq_nonneg _)
  have hsqpow : ∀ x : ℝ, (c * x ^ k) ^ 2 = c ^ 2 * x ^ (2 * k) := by
    intro x
    rw [mul_pow, ← pow_mul]
    rw [show k * 2 = 2 * k by omega]
  have hxpow : ContinuousOn (fun x : ℝ => x ^ k) (Set.Icc (-1) 1) :=
    (continuous_pow k).continuousOn
  have hg2i : IntervalIntegrable (fun x => g x ^ 2) volume (-1) 1 := by
    exact (hg.pow 2).intervalIntegrable_of_Icc (by norm_num : (-1 : ℝ) ≤ 1)
  have hvi : IntervalIntegrable (fun x => 2 * c * g x * x ^ k) volume (-1) 1 := by
    exact ((hg.const_mul (2 * c)).mul hxpow).intervalIntegrable_of_Icc (by norm_num : (-1 : ℝ) ≤ 1)
  have hwi : IntervalIntegrable (fun x => c ^ 2 * x ^ (2 * k)) volume (-1) 1 := by
    exact (continuous_const.continuousOn.mul (continuous_pow (2 * k)).continuousOn).intervalIntegrable_of_Icc (by norm_num : (-1 : ℝ) ≤ 1)
  have hleft : IntervalIntegrable (fun x => g x ^ 2 - 2 * c * g x * x ^ k) volume (-1) 1 :=
    hg2i.sub hvi
  have hexp : (∫ x in (-1 : ℝ)..1, (g x - c * x ^ k) ^ 2) = A - 2 * c * B + c ^ 2 * C := by
    dsimp [A, B, C]
    calc
      (∫ x in (-1 : ℝ)..1, (g x - c * x ^ k) ^ 2)
          = ∫ x in (-1 : ℝ)..1, (g x ^ 2 - 2 * c * g x * x ^ k + c ^ 2 * x ^ (2 * k)) := by
              apply intervalIntegral.integral_congr
              intro x hx
              calc
                (g x - c * x ^ k) ^ 2 = g x ^ 2 - 2 * g x * (c * x ^ k) + (c * x ^ k) ^ 2 := by ring
                _ = g x ^ 2 - 2 * c * g x * x ^ k + c ^ 2 * x ^ (2 * k) := by
                      rw [hsqpow]
                      ring
      _ = (∫ x in (-1 : ℝ)..1, g x ^ 2) - (∫ x in (-1 : ℝ)..1, 2 * c * g x * x ^ k) +
            (∫ x in (-1 : ℝ)..1, c ^ 2 * x ^ (2 * k)) := by
            rw [intervalIntegral.integral_add hleft hwi,
                 intervalIntegral.integral_sub hg2i hvi]
      _ = (∫ x in (-1 : ℝ)..1, g x ^ 2) - 2 * c * (∫ x in (-1 : ℝ)..1, g x * x ^ k) +
            c ^ 2 * (∫ x in (-1 : ℝ)..1, x ^ (2 * k)) := by
            have hv : (∫ x in (-1 : ℝ)..1, 2 * c * g x * x ^ k) =
                2 * c * (∫ x in (-1 : ℝ)..1, g x * x ^ k) := by
              calc
                (∫ x in (-1 : ℝ)..1, 2 * c * g x * x ^ k)
                    = ∫ x in (-1 : ℝ)..1, (2 * c) * (g x * x ^ k) := by
                        apply intervalIntegral.integral_congr
                        intro x hx
                        ring
                _ = (2 * c) * (∫ x in (-1 : ℝ)..1, g x * x ^ k) := by simp
            rw [hv]
            simp
  have hmain : 0 ≤ A - 2 * c * B + c ^ 2 * C := by
    rw [← hexp]
    exact hnonneg
  have hstep : 0 ≤ A - B ^ 2 / C := by
    calc
      0 ≤ A - 2 * c * B + c ^ 2 * C := hmain
      _ = A - B ^ 2 / C := by
        dsimp [c]
        field_simp [hC_ne]
        ring
  have hfin : B ^ 2 ≤ A * C := by
    have hmul : 0 ≤ (A - B ^ 2 / C) * C := mul_nonneg hstep (le_of_lt hC_pos)
    have hmul' : (A - B ^ 2 / C) * C = A * C - B ^ 2 := by
      field_simp [hC_ne]
    rw [hmul'] at hmul
    exact sub_nonneg.mp hmul
  simpa [A, B, C] using hfin

/-- L² moment bound: |mu_k| ≤ ‖g‖_2 · ‖x^k‖_2 with
    ‖g‖_2 = sqrt (∫ g^2) and ‖x^k‖_2 = sqrt (2 / (2k+1)). -/
theorem moment_bound {g : ℝ → ℝ} (hg : ContinuousOn g (Set.Icc (-1) 1)) (k : ℕ) :
    |moments g k| ≤ Real.sqrt (∫ x in (-1 : ℝ)..1, g x ^ 2) *
      Real.sqrt (2 / ((2 * k + 1 : ℕ) : ℝ)) := by
  let A : ℝ := ∫ x in (-1 : ℝ)..1, g x ^ 2
  let B : ℝ := ∫ x in (-1 : ℝ)..1, g x * x ^ k
  let C : ℝ := ∫ x in (-1 : ℝ)..1, x ^ (2 * k)
  have hA_nonneg : 0 ≤ A := by
    dsimp [A]
    exact intervalIntegral.integral_nonneg (by norm_num : (-1 : ℝ) ≤ 1)
      (by intro x hx; exact sq_nonneg _)
  have hC_eq : C = 2 / ((2 * k + 1 : ℕ) : ℝ) := by
    dsimp [C]
    exact integral_x_pow_even k
  have hC_nonneg : 0 ≤ C := by
    rw [hC_eq]
    positivity
  have hCS : B ^ 2 ≤ A * C := by
    dsimp [A, B, C]
    exact cs_moment hg k
  have hsq : B ^ 2 ≤ (Real.sqrt A * Real.sqrt C) ^ 2 := by
    rw [mul_pow, Real.sq_sqrt hA_nonneg, Real.sq_sqrt hC_nonneg]
    exact hCS
  have hprod_nonneg : 0 ≤ Real.sqrt A * Real.sqrt C :=
    mul_nonneg (Real.sqrt_nonneg A) (Real.sqrt_nonneg C)
  have hB_abs : |B| ≤ Real.sqrt A * Real.sqrt C := by
    calc
      |B| ≤ |Real.sqrt A * Real.sqrt C| := (sq_le_sq).1 hsq
      _ = Real.sqrt A * Real.sqrt C := by rw [abs_of_nonneg hprod_nonneg]
  have hB_abs' : |B| ≤ Real.sqrt A * Real.sqrt (2 / ((2 * k + 1 : ℕ) : ℝ)) := by
    have hC_sqrt : Real.sqrt C = Real.sqrt (2 / ((2 * k + 1 : ℕ) : ℝ)) := by
      rw [hC_eq]
    simpa [hC_sqrt] using hB_abs
  simpa [moments, A, B] using hB_abs'

end MomentBound

end SL
