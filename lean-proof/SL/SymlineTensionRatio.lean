import Mathlib

/-!
# Symmetry-line tension ratio: algebraic core of the n=1 gap line

Formalization of the STRICT (proved) algebraic core of
`docs/SL_gap_n1_symline_allR_proof.tex`: the comparison `P1`
(`c/(q+c) <= t/(y+t)` from `u <= tan u`), the algebraic form of the
left-hand functional `FeEquiv` on the symmetry line (Lemma 1 of the
source), and the equivalence `FeEquiv < 0 <-> rho < 1` between the
sign of the functional and the tension ratio below 1.

Content:
* `Phi`, `Mf`, `FeEquiv`, `Delta`, `T`, `rho`: the named quantities.
* `Phi_nonneg`, `Phi_eq`: positivity and the closed form of `Phi`.
* `P1`: `c/(q+c) <= t/(y+t)` from `c = arctan(q*t)/y`.
* `P1_tan`: the same comparison with `t = tan gamma`.
* `FeEquiv_eq`: common-denominator form of `FeEquiv` on the symmetry line.
* `FeEquiv_iff_rho_lt_one`: `FeEquiv < 0 <-> rho < 1` for `Delta > 0`.

Honesty note: only the algebraic core is formalized here.  The
transcendental facts of the source (existence and location of the
solution `gamma_0*`, the inequality `(y * sin gamma)^2 >= pi^2/4`, the
three-term nonnegative decomposition of Lemma P2, and the full tension
ratio chain of Theorem 1) are not yet formalized and remain pending
audit.  Numerical evidence is never used as a theorem.
-/

namespace SL
namespace SymlineTensionRatio

open Real

noncomputable section

def Phi (q x : ℝ) : ℝ :=
  cos x ^ 2 + q ^ 2 * sin x ^ 2

def Mf (x c q : ℝ) : ℝ :=
  x ^ 2 * sin x ^ 2 / (q + c * Phi q x)

def FeEquiv (A γ c q : ℝ) : ℝ :=
  Mf A c q - Mf (Real.pi - γ) c q

def Delta (A γ : ℝ) : ℝ :=
  (Real.pi - γ) ^ 2 * sin γ ^ 2 - A ^ 2 * sin A ^ 2

def T (A γ : ℝ) : ℝ :=
  (Real.pi - γ) ^ 2 - A ^ 2

def rho (A γ c q : ℝ) : ℝ :=
  c * (1 - q ^ 2) * sin A ^ 2 * sin γ ^ 2 * T A γ / ((q + c) * Delta A γ)

lemma Phi_nonneg (q x : ℝ) : 0 ≤ Phi q x := by
  unfold Phi
  nlinarith [sq_nonneg (cos x), sq_nonneg (sin x), sq_nonneg q]

lemma Phi_eq (q x : ℝ) :
    Phi q x = 1 - (1 - q ^ 2) * sin x ^ 2 := by
  unfold Phi
  nlinarith [Real.cos_sq_add_sin_sq x]

lemma P1 {q t y c : ℝ} (hq : 0 < q) (ht : 0 < t) (hy : 0 < y)
    (hc : c = Real.arctan (q * t) / y) :
    c / (q + c) ≤ t / (y + t) := by
  rw [hc]
  let u : ℝ := Real.arctan (q * t)
  have hu : 0 < u := by
    dsimp [u]
    exact Real.arctan_pos.mpr (mul_pos hq ht)
  have htan : Real.tan u = q * t := by
    dsimp [u]
    exact Real.tan_arctan (q * t)
  have hu_lt : u < Real.pi / 2 := by
    dsimp [u]
    exact Real.arctan_lt_pi_div_two (q * t)
  have hu_le_tan : u ≤ Real.tan u := by
    exact (Real.lt_tan hu hu_lt).le
  have hu_le_qt : u ≤ q * t := by
    simpa [htan] using hu_le_tan
  have hden1 : 0 < y * q + u := by positivity
  have hden2 : 0 < y + t := by positivity
  have hkey : u / (y * q + u) ≤ t / (y + t) := by
    have hmul := mul_le_mul_of_nonneg_right hu_le_qt hy.le
    field_simp [hy.ne', hden1.ne', hden2.ne']
    nlinarith
  have hnorm : u / y / (q + u / y) = u / (y * q + u) := by
    field_simp [hy.ne']
  rw [hnorm]
  exact hkey

lemma P1_tan {q γ y c : ℝ} (hq : 0 < q) (hγ : 0 < γ)
    (hγp : γ < Real.pi / 2) (hy : 0 < y)
    (hc : c = Real.arctan (q * Real.tan γ) / y) :
    c / (q + c) ≤ Real.tan γ / (y + Real.tan γ) := by
  exact P1 hq (Real.tan_pos_of_pos_of_lt_pi_div_two hγ hγp) hy hc

lemma FeEquiv_eq {A γ c q : ℝ} (hq : 0 < q) (hc : 0 < c) :
    FeEquiv A γ c q =
      (c * (1 - q ^ 2) * sin A ^ 2 * sin γ ^ 2 * T A γ - (q + c) * Delta A γ) /
        ((q + c * Phi q A) * (q + c * Phi q (Real.pi - γ))) := by
  have hdA : q + c * Phi q A ≠ 0 := by
    have hΦA : 0 ≤ Phi q A := Phi_nonneg q A
    have hcΦ : 0 ≤ c * Phi q A := mul_nonneg hc.le hΦA
    have : 0 < q + c * Phi q A := by linarith
    exact this.ne'
  have hdY : q + c * Phi q (Real.pi - γ) ≠ 0 := by
    have hΦY : 0 ≤ Phi q (Real.pi - γ) := Phi_nonneg q (Real.pi - γ)
    have hcΦ : 0 ≤ c * Phi q (Real.pi - γ) := mul_nonneg hc.le hΦY
    have : 0 < q + c * Phi q (Real.pi - γ) := by linarith
    exact this.ne'
  have hmain : (A ^ 2 * sin A ^ 2) * (q + c * Phi q (Real.pi - γ)) -
      ((Real.pi - γ) ^ 2 * sin γ ^ 2) * (q + c * Phi q A) =
      c * (1 - q ^ 2) * sin A ^ 2 * sin γ ^ 2 * ((Real.pi - γ) ^ 2 - A ^ 2) -
        (q + c) * ((Real.pi - γ) ^ 2 * sin γ ^ 2 - A ^ 2 * sin A ^ 2) := by
    rw [Phi_eq q A, Phi_eq q (Real.pi - γ), Real.sin_pi_sub]
    ring
  calc
    FeEquiv A γ c q
        = A ^ 2 * sin A ^ 2 / (q + c * Phi q A) -
            (Real.pi - γ) ^ 2 * sin γ ^ 2 / (q + c * Phi q (Real.pi - γ)) := by
      unfold FeEquiv Mf
      rw [Real.sin_pi_sub]
    _ = (A ^ 2 * sin A ^ 2 * (q + c * Phi q (Real.pi - γ)) -
            (Real.pi - γ) ^ 2 * sin γ ^ 2 * (q + c * Phi q A)) /
          ((q + c * Phi q A) * (q + c * Phi q (Real.pi - γ))) := by
      field_simp [hdA, hdY]
    _ = (c * (1 - q ^ 2) * sin A ^ 2 * sin γ ^ 2 * T A γ - (q + c) * Delta A γ) /
          ((q + c * Phi q A) * (q + c * Phi q (Real.pi - γ))) := by
      unfold T Delta
      rw [hmain]

lemma FeEquiv_iff_rho_lt_one {A γ c q : ℝ} (hq : 0 < q) (hc : 0 < c)
    (hΔ : 0 < Delta A γ) :
    FeEquiv A γ c q < 0 ↔ rho A γ c q < 1 := by
  have hFe := FeEquiv_eq (A := A) (γ := γ) (c := c) (q := q) hq hc
  rw [hFe]
  have hDpos : 0 < (q + c * Phi q A) * (q + c * Phi q (Real.pi - γ)) := by
    have hΦA : 0 ≤ Phi q A := Phi_nonneg q A
    have hΦY : 0 ≤ Phi q (Real.pi - γ) := Phi_nonneg q (Real.pi - γ)
    have h1 : 0 < q + c * Phi q A := by
      have hcΦ : 0 ≤ c * Phi q A := mul_nonneg hc.le hΦA
      linarith
    have h2 : 0 < q + c * Phi q (Real.pi - γ) := by
      have hcΦ : 0 ≤ c * Phi q (Real.pi - γ) := mul_nonneg hc.le hΦY
      linarith
    exact mul_pos h1 h2
  have hN : (c * (1 - q ^ 2) * sin A ^ 2 * sin γ ^ 2 * T A γ - (q + c) * Delta A γ) /
      ((q + c * Phi q A) * (q + c * Phi q (Real.pi - γ))) < 0 ↔
      c * (1 - q ^ 2) * sin A ^ 2 * sin γ ^ 2 * T A γ - (q + c) * Delta A γ < 0 := by
    constructor
    · intro h
      have hmul := (div_lt_iff₀ hDpos).mp h
      simpa using hmul
    · intro h
      exact (div_lt_iff₀ hDpos).mpr (by simpa using h)
  have hR : c * (1 - q ^ 2) * sin A ^ 2 * sin γ ^ 2 * T A γ - (q + c) * Delta A γ < 0 ↔
      rho A γ c q < 1 := by
    unfold rho
    have hqcpos : 0 < q + c := by linarith
    have hDq : 0 < (q + c) * Delta A γ := mul_pos hqcpos hΔ
    constructor
    · intro h
      apply (div_lt_iff₀ hDq).mpr
      unfold T Delta at h ⊢
      nlinarith
    · intro h
      have hlt := (div_lt_iff₀ hDq).mp h
      unfold T Delta at hlt ⊢
      nlinarith
  exact hN.trans hR

end
end SymlineTensionRatio
end SL
