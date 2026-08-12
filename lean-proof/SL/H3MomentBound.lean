import Mathlib
import SL.Completeness

/-!
# H1-moment polynomial bound on [-1,1]

Formalization of Section 5 of `docs/SL_h3_completeness_proof.tex` (Lemma 6,
the polynomial growth bound for the H1-moments), in integral form.

For w in H^1 with derivative wd (on [-1,1]) and c > 0 the H1-moments
M_k = (w, x^k)_1 expand as

    M_{2m}   = 2m·∫ wd·x^{2m-1} + c·∫ w·x^{2m}                 (Δ(x^{2m}) = 0)
    M_{2m+1} = (2m+1)·∫ wd·x^{2m} + c·∫ w·x^{2m+1} - S,

where S = ∫ wd represents the boundary term (1/2)·Δw·Δ(x^{2m+1}) with
Δw = w(1) - w(-1) = ∫ wd (FTC).  The boundary-difference functional
`delta p = p(1) - p(-1)` packages the same term for a general polynomial p:

    M(p) = ∫ wd·p' + c·∫ w·p - (1/2)·Δp·S            (h1MomentFunctional)

Cauchy-Schwarz (reusing `SL.MomentBound.cs_moment` / `moment_bound`) gives
the polynomial bounds

    |M_{2m}|   ≤ (2m)·‖wd‖₂·√(2/(4m-1)) + c·‖w‖₂·√(2/(4m+1))   ≤ C·√m
    |M_{2m+1}| ≤ (2m+1)·‖wd‖₂·√(2/(4m+1)) + c·‖w‖₂·√(2/(4m+3)) + |S| ≤ C·√m

with |S| ≤ √2·‖wd‖₂ (Cauchy-Schwarz with the constant function 1) and the
elementary estimates

    (2m)·√(2/(4m-1)) ≤ 2·√m,   (2m+1)·√(2/(4m+1)) ≤ 3·√m   (m ≥ 1).

The identification of this functional with the H1 inner product of the
source (FTC for Δw and the inner-product expansion (7)) is the analytic
glue that remains together with the isometry step.
-/

namespace SL

namespace H3MomentBound

open Polynomial

open scoped Real Interval
open MeasureTheory

/-- The boundary difference functional Δp = p(1) - p(-1). -/
noncomputable def delta : Polynomial ℝ →ₗ[ℝ] ℝ where
  toFun p := p.eval 1 - p.eval (-1)
  map_add' := by
    intro p q
    simp [Polynomial.eval_add]
    abel
  map_smul' := by
    intro a p
    simp [Polynomial.eval_smul]
    ring

/-- Δ(X^{2m}) = 0 for even powers. -/
lemma delta_X_pow_even (m : ℕ) : delta (X ^ (2 * m)) = 0 := by
  unfold delta
  have hEven : Even (2 * m) := ⟨m, by ring⟩
  simp [Polynomial.eval_pow, Even.neg_one_pow hEven]

/-- Δ(X^{2m+1}) = 2 for odd powers. -/
lemma delta_X_pow_odd (m : ℕ) : delta (X ^ (2 * m + 1)) = 2 := by
  unfold delta
  have hOdd : Odd (2 * m + 1) := ⟨m, by ring⟩
  simp [Polynomial.eval_pow, Odd.neg_one_pow hOdd]
  norm_num

/-- The H1-moment functional of w with derivative wd on [-1,1]:
M(p) = ∫ wd·p' + c·∫ w·p - (1/2)·(p(1)-p(-1))·∫ wd.
For p = X^k this gives the H1-moments of the source document (the boundary
term is (1/2)·Δw·Δp with Δw = ∫ wd by FTC). -/
noncomputable def h1MomentFunctional (w wd : ℝ → ℝ)
    (hw : ContinuousOn w (Set.Icc (-1) 1)) (hwd : ContinuousOn wd (Set.Icc (-1) 1))
    (c : ℝ) : Polynomial ℝ →ₗ[ℝ] ℝ :=
  (Completeness.momentFunctional wd hwd).comp Polynomial.derivative
    + c • Completeness.momentFunctional w hw
    + (-(1 / 2) * MomentBound.moments wd 0) • delta

/-- The even H1-moment at index 2m in integral form:
M_{2m} = 2m·∫ wd·x^{2m-1} + c·∫ w·x^{2m} (Δ(x^{2m}) = 0). -/
noncomputable def momentsEven (w wd : ℝ → ℝ) (c : ℝ) (m : ℕ) : ℝ :=
  (2 * m : ℝ) * MomentBound.moments wd (2 * m - 1) + c * MomentBound.moments w (2 * m)

/-- The odd H1-moment at index 2m+1 in integral form:
M_{2m+1} = (2m+1)·∫ wd·x^{2m} + c·∫ w·x^{2m+1} - S with S = ∫ wd
(Δ(x^{2m+1}) = 2 and (1/2)·Δw·2 = Δw = S by FTC). -/
noncomputable def momentsOdd (w wd : ℝ → ℝ) (c : ℝ) (m : ℕ) : ℝ :=
  (2 * m + 1 : ℝ) * MomentBound.moments wd (2 * m) + c * MomentBound.moments w (2 * m + 1)
    - MomentBound.moments wd 0

/-- (momentFunctional wd hwd) (derivative (X^k)) = k·(moments wd (k-1)). -/
lemma derivative_moment (wd : ℝ → ℝ) (hwd : ContinuousOn wd (Set.Icc (-1) 1)) (k : ℕ) :
    (Completeness.momentFunctional wd hwd) (Polynomial.derivative (X ^ k)) =
      (k : ℝ) * MomentBound.moments wd (k - 1) := by
  rw [Polynomial.derivative_X_pow]
  simpa using Completeness.apply_C_mul_X_pow wd hwd (k : ℕ) (k - 1)

/-- M(X^{2m}) = momentsEven: the boundary difference vanishes for even powers. -/
lemma apply_X_pow_even (w wd : ℝ → ℝ) (hw : ContinuousOn w (Set.Icc (-1) 1))
    (hwd : ContinuousOn wd (Set.Icc (-1) 1)) (c : ℝ) (m : ℕ) :
    h1MomentFunctional w wd hw hwd c (X ^ (2 * m)) = momentsEven w wd c m := by
  unfold h1MomentFunctional
  simp only [LinearMap.add_apply, LinearMap.comp_apply, LinearMap.smul_apply]
  rw [derivative_moment wd hwd (2 * m)]
  rw [show (Completeness.momentFunctional w hw) (X ^ (2 * m)) = MomentBound.moments w (2 * m) by
    simpa using Completeness.apply_C_mul_X_pow w hw (1 : ℝ) (2 * m)]
  rw [delta_X_pow_even m, smul_eq_mul]
  have hcoef : ((2 * m : ℕ) : ℝ) = (2 * m : ℝ) := by push_cast; ring
  rw [hcoef]
  rw [momentsEven]
  ring

/-- M(X^{2m+1}) = momentsOdd: the boundary difference contributes -S. -/
lemma apply_X_pow_odd (w wd : ℝ → ℝ) (hw : ContinuousOn w (Set.Icc (-1) 1))
    (hwd : ContinuousOn wd (Set.Icc (-1) 1)) (c : ℝ) (m : ℕ) :
    h1MomentFunctional w wd hw hwd c (X ^ (2 * m + 1)) = momentsOdd w wd c m := by
  unfold h1MomentFunctional
  simp only [LinearMap.add_apply, LinearMap.comp_apply, LinearMap.smul_apply]
  rw [derivative_moment wd hwd (2 * m + 1)]
  have hidx : 2 * m + 1 - 1 = 2 * m := by omega
  rw [hidx]
  rw [show (Completeness.momentFunctional w hw) (X ^ (2 * m + 1)) = MomentBound.moments w (2 * m + 1) by
    simpa using Completeness.apply_C_mul_X_pow w hw (1 : ℝ) (2 * m + 1)]
  rw [delta_X_pow_odd m]
  simp only [smul_eq_mul]
  have hcoef : ((2 * m + 1 : ℕ) : ℝ) = (2 * m + 1 : ℝ) := by push_cast; ring
  rw [hcoef]
  have hγ : -(1 / 2) * MomentBound.moments wd 0 * 2 = -MomentBound.moments wd 0 := by ring
  rw [hγ]
  rw [momentsOdd]
  ring

/-! ## Elementary sqrt estimates (m ≥ 1) -/

/-- (2m)·√(2/(4m-1)) ≤ 2·√m for m ≥ 1. -/
lemma sqrt_ineq_even (m : ℕ) (hm : 1 ≤ m) :
    (2 * m : ℝ) * Real.sqrt (2 / (4 * (m : ℝ) - 1)) ≤ 2 * Real.sqrt (m : ℝ) := by
  have hmR : (1 : ℝ) ≤ m := by exact_mod_cast hm
  have h4 : 0 < 4 * (m : ℝ) - 1 := by nlinarith
  have hmain : (2 * m : ℝ) ^ 2 * (2 / (4 * (m : ℝ) - 1)) ≤ 4 * (m : ℝ) := by
    have hrew : (2 * m : ℝ) ^ 2 * (2 / (4 * (m : ℝ) - 1)) = (8 * (m : ℝ) ^ 2) / (4 * (m : ℝ) - 1) := by ring
    rw [hrew]
    rw [div_le_iff₀ h4]
    nlinarith
  have hsqrt4 : Real.sqrt (4 : ℝ) = 2 := by
    rw [show (4 : ℝ) = 2 ^ 2 by norm_num]
    rw [Real.sqrt_sq_eq_abs]
    norm_num
  calc
    (2 * m : ℝ) * Real.sqrt (2 / (4 * (m : ℝ) - 1))
        = Real.sqrt ((2 * m : ℝ) ^ 2) * Real.sqrt (2 / (4 * (m : ℝ) - 1)) := by
          rw [Real.sqrt_sq_eq_abs, abs_of_nonneg (by positivity : 0 ≤ (2 * m : ℝ))]
    _ = Real.sqrt ((2 * m : ℝ) ^ 2 * (2 / (4 * (m : ℝ) - 1))) := by
          rw [← Real.sqrt_mul (sq_nonneg (2 * m : ℝ))]
    _ ≤ Real.sqrt (4 * (m : ℝ)) := Real.sqrt_le_sqrt hmain
    _ = 2 * Real.sqrt (m : ℝ) := by
          rw [Real.sqrt_mul (by norm_num : (0 : ℝ) ≤ 4)]
          rw [hsqrt4]

/-- (2m+1)·√(2/(4m+1)) ≤ 3·√m for m ≥ 1. -/
lemma sqrt_ineq_odd (m : ℕ) (hm : 1 ≤ m) :
    (2 * m + 1 : ℝ) * Real.sqrt (2 / (4 * (m : ℝ) + 1)) ≤ 3 * Real.sqrt (m : ℝ) := by
  have hmR : (1 : ℝ) ≤ m := by exact_mod_cast hm
  have h4 : 0 < 4 * (m : ℝ) + 1 := by nlinarith
  have hmain : (2 * m + 1 : ℝ) ^ 2 * (2 / (4 * (m : ℝ) + 1)) ≤ 9 * (m : ℝ) := by
    have hrew : (2 * m + 1 : ℝ) ^ 2 * (2 / (4 * (m : ℝ) + 1)) = (2 * (2 * m + 1 : ℝ) ^ 2) / (4 * (m : ℝ) + 1) := by ring
    rw [hrew]
    rw [div_le_iff₀ h4]
    nlinarith
  have hsqrt9 : Real.sqrt (9 : ℝ) = 3 := by
    rw [show (9 : ℝ) = 3 ^ 2 by norm_num]
    rw [Real.sqrt_sq_eq_abs]
    norm_num
  calc
    (2 * m + 1 : ℝ) * Real.sqrt (2 / (4 * (m : ℝ) + 1))
        = Real.sqrt ((2 * m + 1 : ℝ) ^ 2) * Real.sqrt (2 / (4 * (m : ℝ) + 1)) := by
          rw [Real.sqrt_sq_eq_abs, abs_of_nonneg (by positivity : 0 ≤ (2 * m + 1 : ℝ))]
    _ = Real.sqrt ((2 * m + 1 : ℝ) ^ 2 * (2 / (4 * (m : ℝ) + 1))) := by
          rw [← Real.sqrt_mul (sq_nonneg (2 * m + 1 : ℝ))]
    _ ≤ Real.sqrt (9 * (m : ℝ)) := Real.sqrt_le_sqrt hmain
    _ = 3 * Real.sqrt (m : ℝ) := by
          rw [Real.sqrt_mul (by norm_num : (0 : ℝ) ≤ 9)]
          rw [hsqrt9]

/-- √(2/(4m+1)) ≤ √2·√m for m ≥ 1. -/
lemma sqrt_two_div_four_m_plus_one_le (m : ℕ) (hm : 1 ≤ m) :
    Real.sqrt (2 / (4 * (m : ℝ) + 1)) ≤ Real.sqrt 2 * Real.sqrt (m : ℝ) := by
  have hmR : (1 : ℝ) ≤ m := by exact_mod_cast hm
  have hmain : 2 / (4 * (m : ℝ) + 1) ≤ 2 * (m : ℝ) := by
    rw [div_le_iff₀ (by nlinarith : 0 < 4 * (m : ℝ) + 1)]
    nlinarith
  have hs := Real.sqrt_le_sqrt hmain
  rwa [Real.sqrt_mul (by norm_num : (0 : ℝ) ≤ 2) (m : ℝ)] at hs

/-- √(2/(4m+3)) ≤ √2·√m for m ≥ 1. -/
lemma sqrt_two_div_four_m_plus_three_le (m : ℕ) (hm : 1 ≤ m) :
    Real.sqrt (2 / (4 * (m : ℝ) + 3)) ≤ Real.sqrt 2 * Real.sqrt (m : ℝ) := by
  have hmR : (1 : ℝ) ≤ m := by exact_mod_cast hm
  have hmain : 2 / (4 * (m : ℝ) + 3) ≤ 2 * (m : ℝ) := by
    rw [div_le_iff₀ (by nlinarith : 0 < 4 * (m : ℝ) + 3)]
    nlinarith
  have hs := Real.sqrt_le_sqrt hmain
  rwa [Real.sqrt_mul (by norm_num : (0 : ℝ) ≤ 2) (m : ℝ)] at hs

/-- √2 ≤ √2·√m for m ≥ 1. -/
lemma sqrt_two_le (m : ℕ) (hm : 1 ≤ m) :
    Real.sqrt 2 ≤ Real.sqrt 2 * Real.sqrt (m : ℝ) := by
  have hmR : (1 : ℝ) ≤ m := by exact_mod_cast hm
  have hsqrtm : (1 : ℝ) ≤ Real.sqrt (m : ℝ) := by
    rw [← Real.sqrt_one]
    exact Real.sqrt_le_sqrt (by nlinarith)
  calc
    Real.sqrt 2 = Real.sqrt 2 * (1 : ℝ) := by ring
    _ ≤ Real.sqrt 2 * Real.sqrt (m : ℝ) := mul_le_mul_of_nonneg_left hsqrtm (Real.sqrt_nonneg 2)

/-! ## Cauchy-Schwarz bounds

Reusing `SL.MomentBound.moment_bound` (the quadratic-trick Cauchy-Schwarz for
the pair (g, x^k) on [-1,1]) for the pairs (wd, x^{2m-1}), (wd, x^{2m}),
(w, x^{2m}), (w, x^{2m+1}) and the constant pair (wd, 1) for |S|.
-/

/-- Even H1-moment bound: |M_{2m}| ≤ (2m)·‖wd‖₂·√(2/(4m-1)) + c·‖w‖₂·√(2/(4m+1)). -/
theorem even_moment_bound {w wd : ℝ → ℝ} (hw : ContinuousOn w (Set.Icc (-1) 1))
    (hwd : ContinuousOn wd (Set.Icc (-1) 1)) {c : ℝ} (hc : 0 ≤ c) {m : ℕ} (hm : 1 ≤ m) :
    |momentsEven w wd c m| ≤
      (2 * m : ℝ) * Real.sqrt (∫ x in (-1 : ℝ)..1, wd x ^ 2) *
          Real.sqrt (2 / (4 * (m : ℝ) - 1)) +
        c * Real.sqrt (∫ x in (-1 : ℝ)..1, w x ^ 2) *
          Real.sqrt (2 / (4 * (m : ℝ) + 1)) := by
  unfold momentsEven
  have hA1 : |MomentBound.moments wd (2 * m - 1)| ≤
      Real.sqrt (∫ x in (-1 : ℝ)..1, wd x ^ 2) *
        Real.sqrt (2 / (4 * (m : ℝ) - 1)) := by
    have h := MomentBound.moment_bound hwd (2 * m - 1)
    have hk : ((2 * (2 * m - 1) + 1 : ℕ) : ℝ) = 4 * (m : ℝ) - 1 := by
      have hk' : (2 * (2 * m - 1) + 1 : ℕ) = 4 * m - 1 := by omega
      have hcast : ((4 * m - 1 : ℕ) : ℝ) = 4 * (m : ℝ) - 1 := by
        have hle : (1 : ℕ) ≤ 4 * m := by omega
        rw [Nat.cast_sub hle]
        norm_num
      rw [hk', hcast]
    simpa [hk] using h
  have hA2 : |MomentBound.moments w (2 * m)| ≤
      Real.sqrt (∫ x in (-1 : ℝ)..1, w x ^ 2) *
        Real.sqrt (2 / (4 * (m : ℝ) + 1)) := by
    have h := MomentBound.moment_bound hw (2 * m)
    have hk : ((2 * (2 * m) + 1 : ℕ) : ℝ) = 4 * (m : ℝ) + 1 := by
      push_cast
      ring
    simpa [hk] using h
  let A1 : ℝ := MomentBound.moments wd (2 * m - 1)
  let A2 : ℝ := MomentBound.moments w (2 * m)
  have hsplit : |(2 * m : ℝ) * A1 + c * A2| ≤ (2 * m : ℝ) * |A1| + c * |A2| := by
    calc
      |(2 * m : ℝ) * A1 + c * A2| ≤ |(2 * m : ℝ) * A1| + |c * A2| := abs_add_le _ _
      _ = (2 * m : ℝ) * |A1| + c * |A2| := by
        have h1' : |(2 * m : ℝ) * A1| = (2 * m : ℝ) * |A1| := by
          rw [abs_mul]
          rw [abs_of_nonneg (by positivity : 0 ≤ (2 * m : ℝ))]
        have h2' : |c * A2| = c * |A2| := by
          rw [abs_mul]
          rw [abs_of_nonneg hc]
        rw [h1', h2']
  calc
    |momentsEven w wd c m| = |(2 * m : ℝ) * A1 + c * A2| := by simp [momentsEven, A1, A2]
    _ ≤ (2 * m : ℝ) * |A1| + c * |A2| := hsplit
    _ ≤ (2 * m : ℝ) * Real.sqrt (∫ x in (-1 : ℝ)..1, wd x ^ 2) *
          Real.sqrt (2 / (4 * (m : ℝ) - 1)) +
        c * Real.sqrt (∫ x in (-1 : ℝ)..1, w x ^ 2) *
          Real.sqrt (2 / (4 * (m : ℝ) + 1)) := by
      have h1 : (2 * m : ℝ) * |A1| ≤ (2 * m : ℝ) * Real.sqrt (∫ x in (-1 : ℝ)..1, wd x ^ 2) *
          Real.sqrt (2 / (4 * (m : ℝ) - 1)) := by
        calc
          (2 * m : ℝ) * |A1| ≤ (2 * m : ℝ) * (Real.sqrt (∫ x in (-1 : ℝ)..1, wd x ^ 2) *
              Real.sqrt (2 / (4 * (m : ℝ) - 1))) :=
            mul_le_mul_of_nonneg_left hA1 (by positivity : 0 ≤ (2 * m : ℝ))
          _ = (2 * m : ℝ) * Real.sqrt (∫ x in (-1 : ℝ)..1, wd x ^ 2) *
              Real.sqrt (2 / (4 * (m : ℝ) - 1)) := by ring
      have h2 : c * |A2| ≤ c * Real.sqrt (∫ x in (-1 : ℝ)..1, w x ^ 2) *
          Real.sqrt (2 / (4 * (m : ℝ) + 1)) := by
        calc
          c * |A2| ≤ c * (Real.sqrt (∫ x in (-1 : ℝ)..1, w x ^ 2) *
              Real.sqrt (2 / (4 * (m : ℝ) + 1))) := mul_le_mul_of_nonneg_left hA2 hc
          _ = c * Real.sqrt (∫ x in (-1 : ℝ)..1, w x ^ 2) *
              Real.sqrt (2 / (4 * (m : ℝ) + 1)) := by ring
      exact add_le_add h1 h2

/-- Odd H1-moment bound:
|M_{2m+1}| ≤ (2m+1)·‖wd‖₂·√(2/(4m+1)) + c·‖w‖₂·√(2/(4m+3)) + ‖wd‖₂·√2. -/
theorem odd_moment_bound {w wd : ℝ → ℝ} (hw : ContinuousOn w (Set.Icc (-1) 1))
    (hwd : ContinuousOn wd (Set.Icc (-1) 1)) {c : ℝ} (hc : 0 ≤ c) {m : ℕ} (hm : 1 ≤ m) :
    |momentsOdd w wd c m| ≤
      (2 * m + 1 : ℝ) * Real.sqrt (∫ x in (-1 : ℝ)..1, wd x ^ 2) *
          Real.sqrt (2 / (4 * (m : ℝ) + 1)) +
        c * Real.sqrt (∫ x in (-1 : ℝ)..1, w x ^ 2) *
          Real.sqrt (2 / (4 * (m : ℝ) + 3)) +
        Real.sqrt (∫ x in (-1 : ℝ)..1, wd x ^ 2) * Real.sqrt 2 := by
  unfold momentsOdd
  have hB1 : |MomentBound.moments wd (2 * m)| ≤
      Real.sqrt (∫ x in (-1 : ℝ)..1, wd x ^ 2) *
        Real.sqrt (2 / (4 * (m : ℝ) + 1)) := by
    have h := MomentBound.moment_bound hwd (2 * m)
    have hk : ((2 * (2 * m) + 1 : ℕ) : ℝ) = 4 * (m : ℝ) + 1 := by
      push_cast
      ring
    simpa [hk] using h
  have hB2 : |MomentBound.moments w (2 * m + 1)| ≤
      Real.sqrt (∫ x in (-1 : ℝ)..1, w x ^ 2) *
        Real.sqrt (2 / (4 * (m : ℝ) + 3)) := by
    have h := MomentBound.moment_bound hw (2 * m + 1)
    have hk : ((2 * (2 * m + 1) + 1 : ℕ) : ℝ) = 4 * (m : ℝ) + 3 := by
      push_cast
      ring
    simpa [hk] using h
  have hS : |MomentBound.moments wd 0| ≤
      Real.sqrt (∫ x in (-1 : ℝ)..1, wd x ^ 2) * Real.sqrt 2 := by
    have h := MomentBound.moment_bound hwd 0
    norm_num at h ⊢
    simpa using h
  let B1 : ℝ := MomentBound.moments wd (2 * m)
  let B2 : ℝ := MomentBound.moments w (2 * m + 1)
  have hsplit : |(2 * m + 1 : ℝ) * B1 + c * B2 - MomentBound.moments wd 0| ≤
      (2 * m + 1 : ℝ) * |B1| + c * |B2| + |MomentBound.moments wd 0| := by
    calc
      |(2 * m + 1 : ℝ) * B1 + c * B2 - MomentBound.moments wd 0|
          ≤ |(2 * m + 1 : ℝ) * B1 + c * B2| + |MomentBound.moments wd 0| := by
            rw [sub_eq_add_neg, ← abs_neg (MomentBound.moments wd 0)]
            exact abs_add_le _ _
      _ ≤ |(2 * m + 1 : ℝ) * B1| + |c * B2| + |MomentBound.moments wd 0| := by
            have hAB : |(2 * m + 1 : ℝ) * B1 + c * B2| ≤ |(2 * m + 1 : ℝ) * B1| + |c * B2| :=
              abs_add_le _ _
            exact add_le_add hAB le_rfl
      _ = (2 * m + 1 : ℝ) * |B1| + c * |B2| + |MomentBound.moments wd 0| := by
            rw [abs_mul, abs_mul]
            rw [abs_of_nonneg (by positivity : 0 ≤ (2 * m + 1 : ℝ)), abs_of_nonneg hc]
  calc
    |momentsOdd w wd c m| =
        |(2 * m + 1 : ℝ) * B1 + c * B2 - MomentBound.moments wd 0| := by
          simp [momentsOdd, B1, B2]
    _ ≤ (2 * m + 1 : ℝ) * |B1| + c * |B2| + |MomentBound.moments wd 0| := hsplit
    _ ≤ (2 * m + 1 : ℝ) * Real.sqrt (∫ x in (-1 : ℝ)..1, wd x ^ 2) *
          Real.sqrt (2 / (4 * (m : ℝ) + 1)) +
        c * Real.sqrt (∫ x in (-1 : ℝ)..1, w x ^ 2) *
          Real.sqrt (2 / (4 * (m : ℝ) + 3)) +
        Real.sqrt (∫ x in (-1 : ℝ)..1, wd x ^ 2) * Real.sqrt 2 := by
      have h1 : (2 * m + 1 : ℝ) * |B1| ≤ (2 * m + 1 : ℝ) * Real.sqrt (∫ x in (-1 : ℝ)..1, wd x ^ 2) *
          Real.sqrt (2 / (4 * (m : ℝ) + 1)) := by
        calc
          (2 * m + 1 : ℝ) * |B1| ≤ (2 * m + 1 : ℝ) * (Real.sqrt (∫ x in (-1 : ℝ)..1, wd x ^ 2) *
              Real.sqrt (2 / (4 * (m : ℝ) + 1))) :=
            mul_le_mul_of_nonneg_left hB1 (by positivity : 0 ≤ (2 * m + 1 : ℝ))
          _ = (2 * m + 1 : ℝ) * Real.sqrt (∫ x in (-1 : ℝ)..1, wd x ^ 2) *
              Real.sqrt (2 / (4 * (m : ℝ) + 1)) := by ring
      have h2 : c * |B2| ≤ c * Real.sqrt (∫ x in (-1 : ℝ)..1, w x ^ 2) *
          Real.sqrt (2 / (4 * (m : ℝ) + 3)) := by
        calc
          c * |B2| ≤ c * (Real.sqrt (∫ x in (-1 : ℝ)..1, w x ^ 2) *
              Real.sqrt (2 / (4 * (m : ℝ) + 3))) := mul_le_mul_of_nonneg_left hB2 hc
          _ = c * Real.sqrt (∫ x in (-1 : ℝ)..1, w x ^ 2) *
              Real.sqrt (2 / (4 * (m : ℝ) + 3)) := by ring
      exact add_le_add (add_le_add h1 h2) hS

/-- Even H1-moment bound in sqrt form:
|M_{2m}| ≤ (2·‖wd‖₂ + c·√2·‖w‖₂)·√m. -/
theorem even_moment_bound_sqrt {w wd : ℝ → ℝ} (hw : ContinuousOn w (Set.Icc (-1) 1))
    (hwd : ContinuousOn wd (Set.Icc (-1) 1)) {c : ℝ} (hc : 0 ≤ c) {m : ℕ} (hm : 1 ≤ m) :
    |momentsEven w wd c m| ≤
      (2 * Real.sqrt (∫ x in (-1 : ℝ)..1, wd x ^ 2) +
          c * Real.sqrt 2 * Real.sqrt (∫ x in (-1 : ℝ)..1, w x ^ 2)) *
        Real.sqrt (m : ℝ) := by
  let nwd : ℝ := Real.sqrt (∫ x in (-1 : ℝ)..1, wd x ^ 2)
  let nw : ℝ := Real.sqrt (∫ x in (-1 : ℝ)..1, w x ^ 2)
  have hnwd : 0 ≤ nwd := by dsimp [nwd]; exact Real.sqrt_nonneg _
  have hnw : 0 ≤ nw := by dsimp [nw]; exact Real.sqrt_nonneg _
  have hraw := even_moment_bound hw hwd hc hm
  have h1 : (2 * m : ℝ) * nwd * Real.sqrt (2 / (4 * (m : ℝ) - 1)) ≤
      2 * nwd * Real.sqrt (m : ℝ) := by
    have h := sqrt_ineq_even m hm
    calc
      (2 * m : ℝ) * nwd * Real.sqrt (2 / (4 * (m : ℝ) - 1))
          = nwd * ((2 * m : ℝ) * Real.sqrt (2 / (4 * (m : ℝ) - 1))) := by ring
      _ ≤ nwd * (2 * Real.sqrt (m : ℝ)) := mul_le_mul_of_nonneg_left h hnwd
      _ = 2 * nwd * Real.sqrt (m : ℝ) := by ring
  have h2 : c * nw * Real.sqrt (2 / (4 * (m : ℝ) + 1)) ≤
      c * Real.sqrt 2 * nw * Real.sqrt (m : ℝ) := by
    have h := sqrt_two_div_four_m_plus_one_le m hm
    calc
      c * nw * Real.sqrt (2 / (4 * (m : ℝ) + 1)) =
          (c * nw) * Real.sqrt (2 / (4 * (m : ℝ) + 1)) := by ring
      _ ≤ (c * nw) * (Real.sqrt 2 * Real.sqrt (m : ℝ)) :=
        mul_le_mul_of_nonneg_left h (mul_nonneg hc hnw)
      _ = c * Real.sqrt 2 * nw * Real.sqrt (m : ℝ) := by ring
  have hfin : |momentsEven w wd c m| ≤
      (2 * m : ℝ) * nwd * Real.sqrt (2 / (4 * (m : ℝ) - 1)) +
        c * nw * Real.sqrt (2 / (4 * (m : ℝ) + 1)) := by
    simpa [nwd, nw] using hraw
  linarith

/-- Odd H1-moment bound in sqrt form:
|M_{2m+1}| ≤ (3·‖wd‖₂ + c·√2·‖w‖₂ + √2·‖wd‖₂)·√m. -/
theorem odd_moment_bound_sqrt {w wd : ℝ → ℝ} (hw : ContinuousOn w (Set.Icc (-1) 1))
    (hwd : ContinuousOn wd (Set.Icc (-1) 1)) {c : ℝ} (hc : 0 ≤ c) {m : ℕ} (hm : 1 ≤ m) :
    |momentsOdd w wd c m| ≤
      (3 * Real.sqrt (∫ x in (-1 : ℝ)..1, wd x ^ 2) +
          c * Real.sqrt 2 * Real.sqrt (∫ x in (-1 : ℝ)..1, w x ^ 2) +
        Real.sqrt 2 * Real.sqrt (∫ x in (-1 : ℝ)..1, wd x ^ 2)) *
        Real.sqrt (m : ℝ) := by
  let nwd : ℝ := Real.sqrt (∫ x in (-1 : ℝ)..1, wd x ^ 2)
  let nw : ℝ := Real.sqrt (∫ x in (-1 : ℝ)..1, w x ^ 2)
  have hnwd : 0 ≤ nwd := by dsimp [nwd]; exact Real.sqrt_nonneg _
  have hnw : 0 ≤ nw := by dsimp [nw]; exact Real.sqrt_nonneg _
  have hraw := odd_moment_bound hw hwd hc hm
  have h1 : (2 * m + 1 : ℝ) * nwd * Real.sqrt (2 / (4 * (m : ℝ) + 1)) ≤
      3 * nwd * Real.sqrt (m : ℝ) := by
    have h := sqrt_ineq_odd m hm
    calc
      (2 * m + 1 : ℝ) * nwd * Real.sqrt (2 / (4 * (m : ℝ) + 1))
          = nwd * ((2 * m + 1 : ℝ) * Real.sqrt (2 / (4 * (m : ℝ) + 1))) := by ring
      _ ≤ nwd * (3 * Real.sqrt (m : ℝ)) := mul_le_mul_of_nonneg_left h hnwd
      _ = 3 * nwd * Real.sqrt (m : ℝ) := by ring
  have h2 : c * nw * Real.sqrt (2 / (4 * (m : ℝ) + 3)) ≤
      c * Real.sqrt 2 * nw * Real.sqrt (m : ℝ) := by
    have h := sqrt_two_div_four_m_plus_three_le m hm
    calc
      c * nw * Real.sqrt (2 / (4 * (m : ℝ) + 3)) =
          (c * nw) * Real.sqrt (2 / (4 * (m : ℝ) + 3)) := by ring
      _ ≤ (c * nw) * (Real.sqrt 2 * Real.sqrt (m : ℝ)) :=
        mul_le_mul_of_nonneg_left h (mul_nonneg hc hnw)
      _ = c * Real.sqrt 2 * nw * Real.sqrt (m : ℝ) := by ring
  have h3 : nwd * Real.sqrt 2 ≤ nwd * Real.sqrt 2 * Real.sqrt (m : ℝ) := by
    have h := sqrt_two_le m hm
    calc
      nwd * Real.sqrt 2 ≤ nwd * (Real.sqrt 2 * Real.sqrt (m : ℝ)) :=
        mul_le_mul_of_nonneg_left h hnwd
      _ = nwd * Real.sqrt 2 * Real.sqrt (m : ℝ) := by ring
  have hfin : |momentsOdd w wd c m| ≤
      (2 * m + 1 : ℝ) * nwd * Real.sqrt (2 / (4 * (m : ℝ) + 1)) +
        c * nw * Real.sqrt (2 / (4 * (m : ℝ) + 3)) + nwd * Real.sqrt 2 := by
    simpa [nwd, nw] using hraw
  linarith

end H3MomentBound

end SL
