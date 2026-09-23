import Mathlib.LinearAlgebra.Matrix.DotProduct
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring

namespace AuditRound9

noncomputable def euclidean_project {n : ℕ} (b A : Fin n → ℝ) : Fin n → ℝ := by
  classical
  exact if A = 0 then b else b - (dotProduct b A / dotProduct A A) • A

theorem projection_zero {n : ℕ} (b : Fin n → ℝ) : euclidean_project b 0 = b := by
  simp [euclidean_project]

theorem normal_squared_ne_zero {n : ℕ} (A : Fin n → ℝ) (hA : A ≠ 0) :
    dotProduct A A ≠ 0 := by
  simpa only [ne_eq, dotProduct_self_eq_zero] using hA

theorem projection_formula {n : ℕ} (b A : Fin n → ℝ) (hA : A ≠ 0) :
    euclidean_project b A = b - (dotProduct b A / dotProduct A A) • A := by
  simp [euclidean_project, hA]

theorem projection_tangent {n : ℕ} (b A : Fin n → ℝ) :
    dotProduct (euclidean_project b A) A = 0 := by
  classical
  by_cases hA : A = 0
  · simp [hA]
  · rw [projection_formula b A hA, sub_dotProduct, smul_dotProduct]
    simp only [smul_eq_mul, div_mul_cancel₀ _ (normal_squared_ne_zero A hA), sub_self]

theorem projection_fixes_tangent {n : ℕ} (b A : Fin n → ℝ)
    (h : dotProduct b A = 0) : euclidean_project b A = b := by
  classical
  by_cases hA : A = 0 <;> simp [euclidean_project, hA, h]

theorem projection_idempotent {n : ℕ} (b A : Fin n → ℝ) :
    euclidean_project (euclidean_project b A) A = euclidean_project b A :=
  projection_fixes_tangent _ _ (projection_tangent b A)

noncomputable def normalization_correction {V : Type} [AddCommGroup V] [Module ℝ V]
    (L : V →ₗ[ℝ] ℝ) (a : ℝ) (u v₀ : V) : V :=
  v₀ - (a / 2 + L v₀) • u

theorem normalization_value {V : Type} [AddCommGroup V] [Module ℝ V]
    (L : V →ₗ[ℝ] ℝ) (a : ℝ) (u v₀ : V) (hu : L u = 1) :
    L (normalization_correction L a u v₀) = -a / 2 := by
  simp only [normalization_correction, map_sub, map_smul, hu, smul_eq_mul, mul_one]
  ring

theorem correction_preserves_equation {V W : Type}
    [AddCommGroup V] [Module ℝ V] [AddCommGroup W] [Module ℝ W]
    (L : V →ₗ[ℝ] ℝ) (K : V →ₗ[ℝ] W) (a : ℝ) (u v₀ : V) (hu : K u = 0) :
    K (normalization_correction L a u v₀) = K v₀ := by
  simp [normalization_correction, hu]

abbrev M2 := Matrix (Fin 2) (Fin 2) ℝ

noncomputable def J : M2 := !![1, 0; 0, -1]
noncomputable def normalized_cell (s C S : ℝ) : M2 :=
  !![C ^ 2 - S ^ 2 / s, (s + 1) * S * C / s;
     -(s + 1) * S * C, C ^ 2 - s * S ^ 2]
noncomputable def normalized_end (C S : ℝ) : M2 := !![C, S; -S, C]
noncomputable def normalized_product (n : ℕ) (s C S : ℝ) : M2 :=
  normalized_end C S * normalized_cell s C S ^ n

@[simp] theorem J_square : J * J = (1 : M2) := by
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [J, Matrix.mul_apply, Fin.sum_univ_two]

theorem cell_reflect (s C S : ℝ) :
    normalized_cell s (-C) S = J * normalized_cell s C S * J := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [normalized_cell, J, Matrix.mul_apply, Fin.sum_univ_two]
  all_goals ring

theorem end_reflect (C S : ℝ) :
    normalized_end (-C) S = -(J * normalized_end C S * J) := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [normalized_end, J]

theorem conjugate_power (M : M2) (n : ℕ) :
    (J * M * J) ^ n = J * M ^ n * J := by
  induction n with
  | zero => simp
  | succ n ih =>
    rw [pow_succ, ih, pow_succ]
    simp only [Matrix.mul_assoc, ← Matrix.mul_assoc J J, J_square, Matrix.one_mul]

theorem product_reflect (n : ℕ) (s C S : ℝ) :
    normalized_product n s (-C) S = -(J * normalized_product n s C S * J) := by
  simp only [normalized_product, cell_reflect, end_reflect, conjugate_power,
    Matrix.neg_mul]
  congr 1
  simp only [Matrix.mul_assoc, ← Matrix.mul_assoc J J, J_square, Matrix.one_mul]

theorem conjugate_entry (M : M2) : (-(J * M * J)) 0 1 = M 0 1 := by
  simp [J, Matrix.mul_apply, Matrix.vecMul, dotProduct, Fin.sum_univ_two]

theorem product_entry_reflect (n : ℕ) (s C S : ℝ) :
    normalized_product n s (-C) S 0 1 = normalized_product n s C S 0 1 := by
  rw [product_reflect, conjugate_entry]

noncomputable def normalized_secular (n : ℕ) (s y : ℝ) : ℝ :=
  normalized_product n s (Real.cos y) (Real.sin y) 0 1

theorem normalized_secular_reflect (n : ℕ) (s y : ℝ) :
    normalized_secular n s (Real.pi - y) = normalized_secular n s y := by
  simp only [normalized_secular, Real.cos_pi_sub, Real.sin_pi_sub, product_entry_reflect]

noncomputable def state_scale (ω : ℝ) : M2 := !![1, 0; 0, ω]
noncomputable def state_unscale (ω : ℝ) : M2 := !![1, 0; 0, ω⁻¹]
noncomputable def physical_matrix (ω : ℝ) (M : M2) : M2 :=
  state_scale ω * M * state_unscale ω

@[simp] theorem scale_inverse (ω : ℝ) (hω : ω ≠ 0) :
    state_unscale ω * state_scale ω = (1 : M2) := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [state_unscale, state_scale, Matrix.mul_apply, Fin.sum_univ_two, hω]

theorem physical_matrix_entry (ω : ℝ) (M : M2) :
    physical_matrix ω M 0 1 = M 0 1 / ω := by
  simp [physical_matrix, state_scale, state_unscale, Matrix.mul_apply, Fin.sum_univ_two,
    Matrix.vecMul, dotProduct, div_eq_mul_inv]

theorem physical_matrix_mul (ω : ℝ) (A B : M2) (hω : ω ≠ 0) :
    physical_matrix ω A * physical_matrix ω B = physical_matrix ω (A * B) := by
  unfold physical_matrix
  calc
    _ = state_scale ω * (A * ((state_unscale ω * state_scale ω) *
          (B * state_unscale ω))) := by simp only [Matrix.mul_assoc]
    _ = _ := by rw [scale_inverse ω hω]; simp only [Matrix.one_mul, Matrix.mul_assoc]

theorem physical_product (ω : ℝ) (E M : M2) (n : ℕ) (hω : ω ≠ 0) :
    physical_matrix ω E * physical_matrix ω M ^ n = physical_matrix ω (E * M ^ n) := by
  induction n with
  | zero => simp
  | succ n ih =>
    calc
      _ = (physical_matrix ω E * physical_matrix ω M ^ n) * physical_matrix ω M := by
        rw [pow_succ, Matrix.mul_assoc]
      _ = physical_matrix ω (E * M ^ n) * physical_matrix ω M := by rw [ih]
      _ = physical_matrix ω ((E * M ^ n) * M) := physical_matrix_mul ω _ _ hω
      _ = _ := by rw [pow_succ, Matrix.mul_assoc]

noncomputable def omega (s t y : ℝ) : ℝ := y / (s * t)
noncomputable def physical_secular (n : ℕ) (s t y : ℝ) : ℝ :=
  (physical_matrix (omega s t y) (normalized_end (Real.cos y) (Real.sin y)) *
    physical_matrix (omega s t y) (normalized_cell s (Real.cos y) (Real.sin y)) ^ n) 0 1

theorem physical_normalized (n : ℕ) (s t y : ℝ)
    (hs : s ≠ 0) (ht : t ≠ 0) (hy : y ≠ 0) :
    physical_secular n s t y = normalized_secular n s y / omega s t y := by
  have hw : omega s t y ≠ 0 := div_ne_zero hy (mul_ne_zero hs ht)
  rw [physical_secular, physical_product _ _ _ _ hw, physical_matrix_entry]
  rfl

theorem frequency_scaling (G : ℝ → ℝ) (s t p y : ℝ)
    (hs : s ≠ 0) (ht : t ≠ 0) (hy : y ≠ 0) (hpy : p - y ≠ 0)
    (hG : G (p - y) = G y) :
    G (p - y) / omega s t (p - y) = (y / (p - y)) * (G y / omega s t y) := by
  rw [hG]
  unfold omega
  field_simp

theorem physical_reflect (n : ℕ) (s t y : ℝ)
    (hs : s ≠ 0) (ht : t ≠ 0) (hy : y ≠ 0) (hpy : Real.pi - y ≠ 0) :
    physical_secular n s t (Real.pi - y) =
      (y / (Real.pi - y)) * physical_secular n s t y := by
  rw [physical_normalized n s t (Real.pi - y) hs ht hpy,
    physical_normalized n s t y hs ht hy]
  exact frequency_scaling (normalized_secular n s) s t Real.pi y hs ht hy hpy
    (normalized_secular_reflect n s y)

theorem internal_reflection (n : ℕ) (s t y : ℝ)
    (hs : 0 < s) (ht : 0 < t) (hy : 0 < y) (hyp : y < Real.pi) :
    0 < y / (Real.pi - y) ∧
    physical_secular n s t (Real.pi - y) =
      (y / (Real.pi - y)) * physical_secular n s t y ∧
    (physical_secular n s t (Real.pi - y) = 0 ↔ physical_secular n s t y = 0) := by
  have hpos : 0 < y / (Real.pi - y) := div_pos hy (sub_pos.mpr hyp)
  have heq := physical_reflect n s t y (ne_of_gt hs) (ne_of_gt ht)
    (ne_of_gt hy) (ne_of_gt (sub_pos.mpr hyp))
  refine ⟨hpos, heq, ?_⟩
  rw [heq, mul_eq_zero]
  simp [ne_of_gt hpos]

theorem local_root :
  (∀ (n : ℕ) (b A : Fin n → ℝ),
    dotProduct (AuditRound9.euclidean_project b A) A = 0) ∧
  (∀ (n : ℕ) (b : Fin n → ℝ), AuditRound9.euclidean_project b 0 = b) ∧
  (∀ (n : ℕ) (b A : Fin n → ℝ), A ≠ 0 →
    dotProduct A A ≠ 0 ∧
    AuditRound9.euclidean_project b A = b - (dotProduct b A / dotProduct A A) • A) ∧
  (∀ (n : ℕ) (b A : Fin n → ℝ),
    (dotProduct b A = 0 → AuditRound9.euclidean_project b A = b) ∧
    AuditRound9.euclidean_project (AuditRound9.euclidean_project b A) A =
      AuditRound9.euclidean_project b A) ∧
  (∀ (V : Type) [AddCommGroup V] [Module ℝ V]
    (L : V →ₗ[ℝ] ℝ) (a : ℝ) (u v₀ : V), L u = 1 →
    L (AuditRound9.normalization_correction L a u v₀) = -a / 2) ∧
  (∀ (V W : Type) [AddCommGroup V] [Module ℝ V] [AddCommGroup W] [Module ℝ W]
    (L : V →ₗ[ℝ] ℝ) (K : V →ₗ[ℝ] W) (a : ℝ) (u v₀ : V), K u = 0 →
    K (AuditRound9.normalization_correction L a u v₀) = K v₀) ∧
  (∀ (s C S : ℝ),
    AuditRound9.normalized_cell s (-C) S = AuditRound9.J * AuditRound9.normalized_cell s C S * AuditRound9.J ∧
    AuditRound9.normalized_end (-C) S = -(AuditRound9.J * AuditRound9.normalized_end C S * AuditRound9.J)) ∧
  (∀ (M : AuditRound9.M2) (n : ℕ),
    (AuditRound9.J * M * AuditRound9.J) ^ n = AuditRound9.J * M ^ n * AuditRound9.J) ∧
  (∀ (n : ℕ) (s C S : ℝ),
    AuditRound9.normalized_product n s (-C) S =
      -(AuditRound9.J * AuditRound9.normalized_product n s C S * AuditRound9.J) ∧
    AuditRound9.normalized_product n s (-C) S 0 1 = AuditRound9.normalized_product n s C S 0 1) ∧
  (∀ (n : ℕ) (s y : ℝ),
    AuditRound9.normalized_secular n s (Real.pi - y) = AuditRound9.normalized_secular n s y) ∧
  (∀ (ω : ℝ) (E M : AuditRound9.M2) (n : ℕ), ω ≠ 0 →
    AuditRound9.physical_matrix ω E * AuditRound9.physical_matrix ω M ^ n =
      AuditRound9.physical_matrix ω (E * M ^ n) ∧
    AuditRound9.physical_matrix ω M 0 1 = M 0 1 / ω) ∧
  (∀ (n : ℕ) (s t y : ℝ), s ≠ 0 → t ≠ 0 → y ≠ 0 →
    AuditRound9.physical_secular n s t y = AuditRound9.normalized_secular n s y / AuditRound9.omega s t y) ∧
  (∀ (G : ℝ → ℝ) (s t p y : ℝ), s ≠ 0 → t ≠ 0 → y ≠ 0 → p - y ≠ 0 →
    G (p - y) = G y →
    G (p - y) / AuditRound9.omega s t (p - y) =
      (y / (p - y)) * (G y / AuditRound9.omega s t y)) ∧
  (∀ (n : ℕ) (s t y : ℝ), s ≠ 0 → t ≠ 0 → y ≠ 0 → Real.pi - y ≠ 0 →
    AuditRound9.physical_secular n s t (Real.pi - y) =
      (y / (Real.pi - y)) * AuditRound9.physical_secular n s t y) ∧
  (∀ (n : ℕ) (s t y : ℝ), 0 < s → 0 < t → 0 < y → y < Real.pi →
    0 < y / (Real.pi - y) ∧
    AuditRound9.physical_secular n s t (Real.pi - y) =
      (y / (Real.pi - y)) * AuditRound9.physical_secular n s t y ∧
    (AuditRound9.physical_secular n s t (Real.pi - y) = 0 ↔ AuditRound9.physical_secular n s t y = 0)) := by
  exact ⟨fun n b A => projection_tangent b A,
    fun n b => projection_zero b,
    fun n b A hA => ⟨normal_squared_ne_zero A hA, projection_formula b A hA⟩,
    fun n b A => ⟨projection_fixes_tangent b A, projection_idempotent b A⟩,
    fun V _ _ L a u v₀ hu => normalization_value L a u v₀ hu,
    fun V W _ _ _ _ L K a u v₀ hu => correction_preserves_equation L K a u v₀ hu,
    fun s C S => ⟨cell_reflect s C S, end_reflect C S⟩,
    conjugate_power,
    fun n s C S => ⟨product_reflect n s C S, product_entry_reflect n s C S⟩,
    normalized_secular_reflect,
    fun ω E M n hω => ⟨physical_product ω E M n hω, physical_matrix_entry ω M⟩,
    physical_normalized,
    frequency_scaling,
    physical_reflect,
    internal_reflection⟩

end AuditRound9
