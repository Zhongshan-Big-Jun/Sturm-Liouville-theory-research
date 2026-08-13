import Mathlib
import SL.BalancedPhase

/-!
# Transfer-matrix and secular-equation core for the ratio proof

Formalization of the elementary matrix algebra in `docs/SL_ratio_proof.tex`
Sections 1-3: the constant-density transfer matrices, the matrix product for the
balanced three-block configurations `[1,R,1]` and `[R,1,R]`, and the resulting
Dirichlet secular equations.  The file also records the generic monotonicity
step `λ_{n+1} <= λ_{2n}` used as the first step of the main theorem.

This file proves only the algebraic/trigonometric identities.  It does not
formalize the spectral theory that connects the matrix condition to eigenvalues;
that link remains a documented gap.
-/

namespace SL

namespace TransferMatrix

open Matrix

noncomputable section

/-- Transfer matrix for an outer `[1,R,1]` block in balanced phase `p`.
`s = sqrt R`, `t = 1/(2s+1)`, and `sqrt lambda = p/(s*t)`. -/
def supM1 (s t p : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![Real.cos p, Real.sin p * (s * t) / p;
     -(p / (s * t)) * Real.sin p, Real.cos p]

/-- Transfer matrix for the middle `R` block of `[1,R,1]` in balanced phase `p`. -/
def supM2 (t p : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![Real.cos p, Real.sin p * t / p;
     -(p / t) * Real.sin p, Real.cos p]

/-- Product `M_outer * M_mid * M_outer` for the balanced supremum configuration. -/
def supM3 (s t p : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  supM1 s t p * supM2 t p * supM1 s t p

/-- The `(0,1)` entry of the supremum-configuration product. -/
lemma supM3_top_right {s t p : ℝ} (ht : t ≠ 0) (hp : p ≠ 0) :
    (supM3 s t p) 0 1 =
      (Real.sin p * t / p) *
        ((2 * s + 1) * (Real.cos p) ^ 2 - s ^ 2 * (Real.sin p) ^ 2) := by
  unfold supM3 supM1 supM2
  simp [Matrix.mul_apply, Fin.sum_univ_two]
  field_simp [ht, hp]
  ring

/-- The Dirichlet condition is equivalent to the balanced-phase secular equation. -/
lemma supM3_top_right_eq_zero_iff {s t p : ℝ} (ht : t ≠ 0) (hp : p ≠ 0) :
    (supM3 s t p) 0 1 = 0 ↔
      Real.sin p * ((2 * s + 1) * (Real.cos p) ^ 2 - s ^ 2 * (Real.sin p) ^ 2) = 0 := by
  rw [supM3_top_right ht hp]
  have hfac : Real.sin p * t / p = (t / p) * Real.sin p := by ring
  rw [hfac]
  have hne : t / p ≠ 0 := div_ne_zero ht hp
  have hA : (t / p) * (Real.sin p * ((2 * s + 1) * (Real.cos p) ^ 2 - s ^ 2 * (Real.sin p) ^ 2)) = 0 ↔
      Real.sin p * ((2 * s + 1) * (Real.cos p) ^ 2 - s ^ 2 * (Real.sin p) ^ 2) = 0 := by
    constructor
    · intro h
      rcases mul_eq_zero.mp h with h0 | hb
      · exact (hne h0).elim
      · exact hb
    · intro h
      exact mul_eq_zero.mpr (Or.inr h)
  rw [show (t / p) * Real.sin p * ((2 * s + 1) * (Real.cos p) ^ 2 - s ^ 2 * (Real.sin p) ^ 2) =
      (t / p) * (Real.sin p * ((2 * s + 1) * (Real.cos p) ^ 2 - s ^ 2 * (Real.sin p) ^ 2)) by ring]
  exact hA

/-- The balanced-phase bracket also vanishes at `pi - theta`. -/
lemma sup_bracket_pi_sub (hs : 0 < s) :
    (2 * s + 1) * (Real.cos (Real.pi - BalancedPhase.theta s)) ^ 2 -
      s ^ 2 * (Real.sin (Real.pi - BalancedPhase.theta s)) ^ 2 = 0 := by
  rw [Real.cos_pi_sub, Real.sin_pi_sub]
  nlinarith [BalancedPhase.sup_secular_bracket hs]

/-- The first balanced phase `theta` satisfies the Dirichlet matrix condition. -/
lemma supM3_top_right_theta (hs : 0 < s) :
    (supM3 s (BalancedPhase.t s) (BalancedPhase.theta s)) 0 1 = 0 := by
  have ht : BalancedPhase.t s ≠ 0 := by
    unfold BalancedPhase.t
    positivity
  have hp : BalancedPhase.theta s ≠ 0 := ne_of_gt (BalancedPhase.theta_pos hs)
  rw [supM3_top_right ht hp]
  rw [BalancedPhase.sup_secular_bracket hs]
  ring

/-- The second balanced phase `pi - theta` satisfies the Dirichlet matrix condition. -/
lemma supM3_top_right_pi_sub_theta (hs : 0 < s) :
    (supM3 s (BalancedPhase.t s) (Real.pi - BalancedPhase.theta s)) 0 1 = 0 := by
  have ht : BalancedPhase.t s ≠ 0 := by
    unfold BalancedPhase.t
    positivity
  have hp : Real.pi - BalancedPhase.theta s ≠ 0 := by
    have hθ : 0 < BalancedPhase.theta s := BalancedPhase.theta_pos hs
    have hθlt : BalancedPhase.theta s < Real.pi / 2 := BalancedPhase.theta_lt_pi_div_two hs
    nlinarith [Real.pi_pos]
  rw [supM3_top_right ht hp]
  rw [sup_bracket_pi_sub hs]
  ring

/-- Transfer matrix for an outer `R` block of `[R,1,R]` in balanced phase `p`. -/
def infM1 (c p : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![Real.cos p, Real.sin p * c / p;
     -(p / c) * Real.sin p, Real.cos p]

/-- Transfer matrix for the middle `1` block of `[R,1,R]` in balanced phase `p`. -/
def infM2 (s c p : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![Real.cos p, Real.sin p * (s * c) / p;
     -(p / (s * c)) * Real.sin p, Real.cos p]

/-- Product for the balanced infimum configuration `[R,1,R]`. -/
def infM3 (s c p : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  infM1 c p * infM2 s c p * infM1 c p

/-- The `(0,1)` entry of the infimum-configuration product. -/
lemma infM3_top_right {s c p : ℝ} (hs : s ≠ 0) (hc : c ≠ 0) (hp : p ≠ 0) :
    (infM3 s c p) 0 1 =
      (Real.sin p * c / (p * s)) *
        (s * (s + 2) * (Real.cos p) ^ 2 - (Real.sin p) ^ 2) := by
  unfold infM3 infM1 infM2
  simp [Matrix.mul_apply, Fin.sum_univ_two]
  field_simp [hs, hc, hp, mul_ne_zero hs hc]
  ring

/-- The Dirichlet condition is equivalent to the Keller balanced-phase equation. -/
lemma infM3_top_right_eq_zero_iff {s c p : ℝ} (hs : s ≠ 0) (hc : c ≠ 0) (hp : p ≠ 0) :
    (infM3 s c p) 0 1 = 0 ↔
      Real.sin p * (s * (s + 2) * (Real.cos p) ^ 2 - (Real.sin p) ^ 2) = 0 := by
  rw [infM3_top_right hs hc hp]
  have hfac : Real.sin p * c / (p * s) = (c / (p * s)) * Real.sin p := by ring
  rw [hfac]
  have hne : c / (p * s) ≠ 0 := div_ne_zero hc (mul_ne_zero hp hs)
  have hA : (c / (p * s)) * (Real.sin p * (s * (s + 2) * (Real.cos p) ^ 2 - (Real.sin p) ^ 2)) = 0 ↔
      Real.sin p * (s * (s + 2) * (Real.cos p) ^ 2 - (Real.sin p) ^ 2) = 0 := by
    constructor
    · intro h
      rcases mul_eq_zero.mp h with h0 | hb
      · exact (hne h0).elim
      · exact hb
    · intro h
      exact mul_eq_zero.mpr (Or.inr h)
  rw [show (c / (p * s)) * Real.sin p * (s * (s + 2) * (Real.cos p) ^ 2 - (Real.sin p) ^ 2) =
      (c / (p * s)) * (Real.sin p * (s * (s + 2) * (Real.cos p) ^ 2 - (Real.sin p) ^ 2)) by ring]
  exact hA

/-- The Keller balanced-phase bracket vanishes at `phi`. -/
lemma inf_bracket_phi (hs : 0 < s) :
    s * (s + 2) * (Real.cos (BalancedPhase.phi s)) ^ 2 -
      (Real.sin (BalancedPhase.phi s)) ^ 2 = 0 := by
  have hcos := BalancedPhase.phi_cos hs
  rw [Real.sin_sq, hcos]
  have hden : (s + 1 : ℝ) ≠ 0 := by positivity
  field_simp [hden]
  ring

/-- The first Keller phase `phi` satisfies the Dirichlet matrix condition. -/
lemma infM3_top_right_phi (hs : 0 < s) :
    (infM3 s (1 / (s + 2)) (BalancedPhase.phi s)) 0 1 = 0 := by
  have hs0 : s ≠ 0 := ne_of_gt hs
  have hc : (1 / (s + 2) : ℝ) ≠ 0 := by positivity
  have hp : BalancedPhase.phi s ≠ 0 := ne_of_gt (BalancedPhase.phi_pos hs)
  rw [infM3_top_right hs0 hc hp]
  rw [inf_bracket_phi hs]
  ring

/-- First step of the ratio theorem: for a strictly increasing eigenvalue sequence,
`λ_{n+1} <= λ_{2n}` for `n >= 1`. -/
lemma le_of_strictMono_double {lam : ℕ → ℝ} (hmono : StrictMono lam) {n : ℕ} (hn : 1 ≤ n) :
    lam (n + 1) ≤ lam (2 * n) := by
  exact hmono.monotone (by omega)

/-- The resulting positive-denominator ratio inequality. -/
lemma ratio_le_of_strictMono_double {lam : ℕ → ℝ} (hmono : StrictMono lam)
    (hpos : ∀ k, 0 < lam k) {n : ℕ} (hn : 1 ≤ n) :
    lam (n + 1) / lam n ≤ lam (2 * n) / lam n := by
  exact div_le_div_of_nonneg_right (le_of_strictMono_double hmono hn) (le_of_lt (hpos n))

end

end TransferMatrix

end SL
