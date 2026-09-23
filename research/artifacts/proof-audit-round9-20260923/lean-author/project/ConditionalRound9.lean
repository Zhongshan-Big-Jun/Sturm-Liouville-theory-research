import AuditRound9

namespace AuditRound9

theorem conditional_root (H : Prop) (_pending : H) :
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
    (AuditRound9.physical_secular n s t (Real.pi - y) = 0 ↔ AuditRound9.physical_secular n s t y = 0)) := local_root

end AuditRound9
