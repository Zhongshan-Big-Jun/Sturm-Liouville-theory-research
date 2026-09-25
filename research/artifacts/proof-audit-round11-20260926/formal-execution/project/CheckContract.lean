import AuditRound11
example : open scoped Matrix in ((∀ (n : ℕ),
  AuditRound11.parity_inverse n * AuditRound11.parity_basis n = 1 ∧
    AuditRound11.parity_basis n * AuditRound11.parity_inverse n = 1 ∧
    AuditRound11.reversal n * AuditRound11.parity_basis n = AuditRound11.parity_basis n * AuditRound11.parity_sign n ∧
    AuditRound11.parity_inverse n * AuditRound11.reversal n = AuditRound11.parity_sign n * AuditRound11.parity_inverse n) ∧
(∀ {n : ℕ} (J : AuditRound11.PairedMatrix n) (a : ℝ)
    (h : J * AuditRound11.reversal n = a • (AuditRound11.reversal n * J)),
  AuditRound11.parity_matrix J * AuditRound11.parity_sign n = a • (AuditRound11.parity_sign n * AuditRound11.parity_matrix J)) ∧
(∀ {n : ℕ} (J : AuditRound11.PairedMatrix n)
    (h : J * AuditRound11.reversal n = -(AuditRound11.reversal n * J)),
  (AuditRound11.parity_matrix J).toBlocks₁₁ = 0 ∧ (AuditRound11.parity_matrix J).toBlocks₂₂ = 0) ∧
(∀ {n : ℕ} (J : AuditRound11.PairedMatrix n)
    (h : J * AuditRound11.reversal n = AuditRound11.reversal n * J),
  (AuditRound11.parity_matrix J).toBlocks₁₂ = 0 ∧ (AuditRound11.parity_matrix J).toBlocks₂₁ = 0) ∧
(∀ {n : ℕ} (J : AuditRound11.PairedMatrix n),
  (AuditRound11.parity_matrix J).det = J.det) ∧
(∀ {n : ℕ} (C D : AuditRound11.Square n),
  (Matrix.fromBlocks (0 : AuditRound11.Square n) C D (0 : AuditRound11.Square n)).det =
      (-1 : ℝ) ^ n * C.det * D.det) ∧
(∀ {n : ℕ} (J : AuditRound11.PairedMatrix n)
    (h : J * AuditRound11.reversal n = -(AuditRound11.reversal n * J)),
  J.det = (-1 : ℝ) ^ n * (AuditRound11.parity_matrix J).toBlocks₁₂.det *
      (AuditRound11.parity_matrix J).toBlocks₂₁.det) ∧
(∀ {n : ℕ} (x v : AuditRound11.PairIndex n → ℝ),
  AuditRound11.physical_reflection (x + v) - AuditRound11.physical_reflection x = -(AuditRound11.reversal n *ᵥ v)) ∧
(∀ {n : ℕ} (x v : AuditRound11.PairIndex n → ℝ),
  (AuditRound11.physical_reflection (x + v) - AuditRound11.physical_reflection x = v ↔
      AuditRound11.reversal n *ᵥ v = -v) ∧
    (AuditRound11.physical_reflection (x + v) - AuditRound11.physical_reflection x = -v ↔
      AuditRound11.reversal n *ᵥ v = v)) ∧
(∀ (L : ℝ),
  (AuditRound11.boundary_even L).det = 2 * L * (L + 2) * (2 * L - 1) ∧
    (AuditRound11.boundary_odd L).det = 2 * L * (L + 2) * (2 * L + 1)) ∧
(∀ (L : ℝ) (h : 4 ≤ L),
  0 < (AuditRound11.boundary_even L).det ∧ 0 < (AuditRound11.boundary_odd L).det) ∧
(∀ {n : ℕ} (v : AuditRound11.PairIndex n → ℝ) (i : Fin n),
  (AuditRound11.reversal n *ᵥ v) (Sum.inl i) = v (Sum.inr i) ∧
    (AuditRound11.reversal n *ᵥ v) (Sum.inr i) = v (Sum.inl i) ∧
    (AuditRound11.parity_basis n *ᵥ v) (Sum.inl i) = v (Sum.inl i) + v (Sum.inr i) ∧
    (AuditRound11.parity_basis n *ᵥ v) (Sum.inr i) = v (Sum.inl i) - v (Sum.inr i)) ∧
(∀ (L : ℕ) (h : 4 ≤ L),
  0 < (AuditRound11.boundary_full (L : ℝ)).det ∧
    (∀ b : AuditRound11.PairIndex 2 → ℝ, ∃! a : AuditRound11.PairIndex 2 → ℝ,
      AuditRound11.boundary_full (L : ℝ) *ᵥ a = b))) := AuditRound11.root
