import Mathlib

/-!
# Balanced-phase method: closed-form constants for eigenvalue ratios

Formalization of the algebraic/trigonometric core of the "balanced phase" method
from `docs/SL_ratio_proof.tex` and `tools/balanced-phase.md`.

Setup: s > 0 plays the role of sqrt R (R >= 1), and
  theta s = arccos (s / (s + 1)),   phi s = arccos (1 / (s + 1)).

Results:
- theta satisfies the sup-configuration secular equation:
      sin theta * ((2s+1) * cos^2 theta - s^2 * sin^2 theta) = 0
  (in fact the bracket vanishes identically);
- arccos (-(s/(s+1))) = pi - theta, giving the closed form
      nu(R) = ((pi - theta)/theta)^2 = (arccos (-(s/(s+1))) / arccos (s/(s+1)))^2;
- any p in (0, pi) satisfying the secular equation is theta or pi - theta;
- tan^2 phi = s * (s + 2) (Keller inf-configuration secular condition).
-/

namespace SL

namespace BalancedPhase

noncomputable def theta (s : ℝ) : ℝ := Real.arccos (s / (s + 1))

noncomputable def phi (s : ℝ) : ℝ := Real.arccos (1 / (s + 1))

noncomputable def t (s : ℝ) : ℝ := 1 / (2 * s + 1)

lemma theta_cos (hs : 0 < s) : Real.cos (theta s) = s / (s + 1) := by
  unfold theta
  exact Real.cos_arccos (by
    have h : 0 ≤ s / (s + 1) := div_nonneg (le_of_lt hs) (by positivity)
    nlinarith) (by
    rw [div_le_one (by positivity : 0 < (s + 1 : ℝ))]
    nlinarith)

lemma phi_cos (hs : 0 < s) : Real.cos (phi s) = 1 / (s + 1) := by
  unfold phi
  exact Real.cos_arccos (by
    have h : 0 ≤ 1 / (s + 1) := div_nonneg zero_le_one (by positivity)
    nlinarith) (by
    rw [div_le_one (by positivity : 0 < (s + 1 : ℝ))]
    nlinarith)

lemma theta_pos (hs : 0 < s) : 0 < theta s := by
  unfold theta
  rw [Real.arccos_pos]
  rw [div_lt_one (by positivity : 0 < (s + 1 : ℝ))]
  nlinarith

lemma theta_lt_pi_div_two (hs : 0 < s) : theta s < Real.pi / 2 := by
  unfold theta
  rw [Real.arccos_lt_pi_div_two]
  exact div_pos hs (by positivity)

lemma phi_pos (hs : 0 < s) : 0 < phi s := by
  unfold phi
  rw [Real.arccos_pos]
  rw [div_lt_one (by positivity : 0 < (s + 1 : ℝ))]
  nlinarith

lemma phi_lt_pi_div_two (hs : 0 < s) : phi s < Real.pi / 2 := by
  unfold phi
  rw [Real.arccos_lt_pi_div_two]
  positivity

lemma sup_secular_bracket (hs : 0 < s) :
    (2 * s + 1) * Real.cos (theta s) ^ 2 - s ^ 2 * Real.sin (theta s) ^ 2 = 0 := by
  have hc := theta_cos hs
  rw [Real.sin_sq, hc]
  have hden : (s + 1 : ℝ) ≠ 0 := ne_of_gt (by positivity)
  field_simp [hden]
  ring

lemma sup_secular (hs : 0 < s) :
    Real.sin (theta s) *
      ((2 * s + 1) * Real.cos (theta s) ^ 2 - s ^ 2 * Real.sin (theta s) ^ 2) = 0 := by
  rw [sup_secular_bracket hs]
  ring

lemma arccos_neg_theta (_hs : 0 < s) :
    Real.arccos (-(s / (s + 1))) = Real.pi - theta s := by
  unfold theta
  rw [Real.arccos_neg]

theorem nu_closed_form (_hs : 0 < s) :
    ((Real.pi - theta s) / theta s) ^ 2 =
      (Real.arccos (-(s / (s + 1))) / Real.arccos (s / (s + 1))) ^ 2 := by
  rw [show theta s = Real.arccos (s / (s + 1)) from rfl]
  rw [Real.arccos_neg]

lemma eq_theta_of_cos {p : ℝ} (_hs : 0 < s) (hp0 : 0 ≤ p) (hpi : p ≤ Real.pi)
    (hcos : Real.cos p = s / (s + 1)) : p = theta s := by
  unfold theta
  rw [← hcos]
  exact (Real.arccos_cos hp0 hpi).symm

lemma eq_pi_sub_theta_of_cos {p : ℝ} (_hs : 0 < s) (hp0 : 0 ≤ p) (hpi : p ≤ Real.pi)
    (hcos : Real.cos p = -(s / (s + 1))) : p = Real.pi - theta s := by
  have h1 : p = Real.arccos (Real.cos p) := (Real.arccos_cos hp0 hpi).symm
  rw [hcos] at h1
  exact h1.trans (arccos_neg_theta _hs)

theorem roots_of_secular {p : ℝ} (hs : 0 < s) (hp0 : 0 < p) (hpi : p < Real.pi)
    (hsec : Real.sin p * ((2 * s + 1) * Real.cos p ^ 2 - s ^ 2 * Real.sin p ^ 2) = 0) :
    p = theta s ∨ p = Real.pi - theta s := by
  have hsin_ne : Real.sin p ≠ 0 := ne_of_gt (Real.sin_pos_of_pos_of_lt_pi hp0 hpi)
  have hb0 : (2 * s + 1) * Real.cos p ^ 2 - s ^ 2 * Real.sin p ^ 2 = 0 :=
    (mul_eq_zero.mp hsec).resolve_left hsin_ne
  have hsin2 : Real.sin p ^ 2 = 1 - Real.cos p ^ 2 := Real.sin_sq p
  have hprod : ((s + 1) * Real.cos p - s) * ((s + 1) * Real.cos p + s) = 0 := by
    rw [hsin2] at hb0
    ring_nf at hb0 ⊢
    exact hb0
  rcases mul_eq_zero.mp hprod with h1 | h2
  · left
    apply eq_theta_of_cos (_hs := hs) (hp0 := le_of_lt hp0) (hpi := le_of_lt hpi)
    apply (eq_div_iff (by positivity : (s + 1 : ℝ) ≠ 0)).2
    nlinarith
  · right
    apply eq_pi_sub_theta_of_cos (_hs := hs) (hp0 := le_of_lt hp0) (hpi := le_of_lt hpi)
    rw [← neg_div]
    apply (eq_div_iff (by positivity : (s + 1 : ℝ) ≠ 0)).2
    nlinarith

lemma phi_tan_sq (hs : 0 < s) : Real.tan (phi s) ^ 2 = s * (s + 2) := by
  have hc := phi_cos hs
  rw [Real.tan_eq_sin_div_cos, div_pow, Real.sin_sq, hc]
  have hden : (1 / (s + 1)) ^ 2 ≠ 0 := by positivity
  have hs1 : (s + 1 : ℝ) ≠ 0 := by positivity
  field_simp [hden, hs1]
  ring

lemma arccos_neg_phi (_hs : 0 < s) :
    Real.arccos (-(1 / (s + 1))) = Real.pi - phi s := by
  unfold phi
  rw [Real.arccos_neg]

theorem mu_closed_form (_hs : 0 < s) :
    ((Real.pi - phi s) / phi s) ^ 2 =
      (Real.arccos (-(1 / (s + 1))) / Real.arccos (1 / (s + 1))) ^ 2 := by
  rw [show phi s = Real.arccos (1 / (s + 1)) from rfl]
  rw [Real.arccos_neg]

lemma lambda1_phase (hs : 0 < s) :
    ((2 * s + 1) * theta s / s) * s * t s = theta s := by
  unfold t
  field_simp [ne_of_gt hs, ne_of_gt (by positivity : 0 < 2 * s + 1)]

lemma lambda2_phase (hs : 0 < s) :
    ((2 * s + 1) * (Real.pi - theta s) / s) * s * t s = Real.pi - theta s := by
  unfold t
  field_simp [ne_of_gt hs, ne_of_gt (by positivity : 0 < 2 * s + 1)]

lemma ratio_of_lambdas (hs : 0 < s) :
    (((2 * s + 1) * (Real.pi - theta s) / s) ^ 2) /
        (((2 * s + 1) * theta s / s) ^ 2) = ((Real.pi - theta s) / theta s) ^ 2 := by
  field_simp [ne_of_gt (theta_pos hs), ne_of_gt hs,
    ne_of_gt (by positivity : 0 < 2 * s + 1)]

end BalancedPhase

end SL
