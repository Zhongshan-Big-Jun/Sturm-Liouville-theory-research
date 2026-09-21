import SL.AuditRound5
open Polynomial SL.AuditRound5
example : p_even 2 = (X ^ 4 - C 2 * X ^ 2 : Polynomial ℝ) := by
  norm_num [p_even]
example : p_odd 2 = (X ^ 5 - C 2 * X ^ 3 : Polynomial ℝ) := by
  norm_num [p_odd]
example : correction_alpha 2 (3, 1) = 1 / 2 ∧ correction_beta 2 (3, 1) = 1 := by
  norm_num [correction_alpha, correction_beta]
example : endpoint_matrix 2 * correction_matrix 2 = 1 :=
  (endpoint_matrix_inverse 2 (by norm_num)).1
example (m₀ : ℕ) : (1 + X : Polynomial ℝ) ∈ oblique ⊓ krein_polynomials ∧
    (1 + X : Polynomial ℝ) ∉ high_span m₀ :=
  ⟨oblique_with_krein_witness.1, one_add_X_not_mem_high_span m₀⟩
example (m₀ : ℕ) : high_span m₀ ≠ oblique ⊓ krein_polynomials :=
  (high_span_lt_krein_oblique m₀).ne
example (m : ℕ) (hm : 2 ≤ m) : (p_even m).eval 0 = 0 ∧
    (p_odd m).derivative.eval 0 = 0 := by
  have he := congrArg Prod.fst (even_traces m hm)
  have ho := congrArg Prod.snd (odd_traces m hm)
  exact ⟨he, ho⟩
