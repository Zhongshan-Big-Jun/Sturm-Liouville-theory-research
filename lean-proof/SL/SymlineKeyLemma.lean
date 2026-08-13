import Mathlib

/-!
# Symmetry-line key lemma: P1/P2 bounds and the W0 bound (n=1 gap line)

Formalization of the algebraic core of Lemma P1/P2 and the W0 lemma in
`docs/SL_gap_n1_symline_proof.tex` (sections 4.2-4.3): the log-derivative
bounds that drive the KEY LEMMA (unique zero of `Fe` on `(0,1/2)`).

Content:
* `q0 = sqrt(2/3)` and `Gamma0 = arccos(q0/(1+q0))`: the source's
  `q_0` and `Gamma = gamma_0(q_0)`; certificate-free location lemmas
  (`q0 in (4/5, 5/6)`, `Gamma0 < pi/2 - 4/9`, `cot Gamma0 > 1/2`).
* `W0 γ = 3 - 2*(pi-γ)*cot γ` with the bound `W0 γ < 4*q0/3` for
  `0 < γ <= Gamma0`.
* `G q c x`: the log-derivative expression of the source (eq. G).
* `P1_bound`: `G q c x <= -(6*sqrt 6 - 6)/5 < -4/3` for `x in (0, pi/2)`,
  `q in [q0, 1]`, `c in (0, 1/2)`.
* `P2_bound`: `-(4/3) < G q c (pi - γ)` for `γ in (0, Gamma0]`,
  `q in [q0, 1]`, `c in (0, 1/2)`.
* `P1_neg`, `P1_lt_P2`: the sign consequences used by the KEY LEMMA.
* `Fep_lt_zero_of_nonneg`: the KEY-LEMMA monotonicity step
  `Fe >= 0 => Fe' < 0` in its algebraic form.
* `gamma0_mono`: `gamma_0(q) <= Gamma0` for `q0 <= q` (arccos antitone).

Honesty notes:
* The source's P2 requires `γ = pi - alpha2(c) <= gamma_0(q) <= Gamma0`
  from the phase-branch analysis (alpha2 decreasing in c, arccos
  antitone).  The branch reduction is not formalized here; `P2_bound`
  takes `γ <= Gamma0` as a hypothesis, and `gamma0_mono` formalizes only
  the second half (`gamma_0(q) <= Gamma0` for `q0 <= q`).
* The source proves `W0(Gamma0) < 4q0/3` with exact rational certificates
  (alternating-series bounds for cos/cot at 10/9, pi > 22/7).  The
  formal proof uses a certificate-free route: `Gamma0 < pi/2 - 4/9`
  (from `sin(4/9) < 4/9 < q0/(1+q0) = cos Gamma0` and antitone cos),
  `cot Gamma0 > 1/2` (from `q0 < 5/6`), and cot antitone on `(0, pi)`;
  the constants are rational.  Numerical evidence is never used.
* The derivative identity `d/dc log Mf(alpha_k(c);c) = G(alpha_k(c);c)`
  and the endpoint signs of `Fe` are phase-theory hooks, not formalized
  here.
-/

namespace SL
namespace SymlineKeyLemma

open Real

noncomputable section

/-- `q0 = sqrt(2/3)`: the lower endpoint of the small-R range
(`1 < R <= 3/2` iff `q = R^{-1/2} in [q0, 1)`). -/
def q0 : ℝ := Real.sqrt (2 / 3)

/-- `Gamma0 = arccos(q0/(1+q0)) = gamma_0(q_0)` of the source. -/
def Gamma0 : ℝ := Real.arccos (q0 / (1 + q0))

/-- `gamma_0(q) = arccos(q/(1+q))` of the source. -/
def gamma0 (q : ℝ) : ℝ := Real.arccos (q / (1 + q))

/-- `W0(γ) = 3 - 2*(pi-γ)*cot γ` of the source (Lemma W0). -/
def W0 (γ : ℝ) : ℝ :=
  3 - 2 * (Real.pi - γ) * Real.cot γ

/-- `Phi_q(x) = cos^2 x + q^2 sin^2 x` (the source's `Phi_{q̃}`). -/
def Phi (q x : ℝ) : ℝ :=
  cos x ^ 2 + q ^ 2 * sin x ^ 2

/-- The log-derivative expression `G(x;c)` of the source (eq. G). -/
def G (q c x : ℝ) : ℝ :=
  -Phi q x * (3 + 2 * x * Real.cot x) / (q + c * Phi q x) +
    2 * c * x * Phi q x * (q ^ 2 - 1) * sin x * cos x / (q + c * Phi q x) ^ 2

lemma q0_sq : q0 ^ 2 = 2 / 3 := by
  unfold q0
  exact Real.sq_sqrt (by norm_num)

lemma q0_pos : 0 < q0 := by
  unfold q0
  exact Real.sqrt_pos.2 (by norm_num)

lemma q0_gt_four_fifths : 4 / 5 < q0 := by
  have hsq : ((4 : ℝ) / 5) ^ 2 < q0 ^ 2 := by
    rw [q0_sq]
    norm_num
  exact (sq_lt_sq₀ (by norm_num : 0 ≤ (4 : ℝ) / 5) (Real.sqrt_nonneg _)).1 hsq

lemma q0_lt_five_sixths : q0 < 5 / 6 := by
  have hsq : q0 ^ 2 < (5 / 6) ^ 2 := by
    rw [q0_sq]
    norm_num
  exact (sq_lt_sq₀ (Real.sqrt_nonneg _) (by norm_num : 0 ≤ (5 : ℝ) / 6)).1 hsq

lemma q0_le_one : q0 ≤ 1 := by
  linarith [q0_lt_five_sixths]

lemma q0_div_one_add_q0_gt_four_ninths : 4 / 9 < q0 / (1 + q0) := by
  have hden : 0 < 1 + q0 := by linarith [q0_pos]
  rw [lt_div_iff₀ hden]
  nlinarith [q0_gt_four_fifths]

lemma q0_div_one_add_q0_lt_one : q0 / (1 + q0) < 1 := by
  have hden : 0 < 1 + q0 := by linarith [q0_pos]
  rw [div_lt_iff₀ hden]
  nlinarith [q0_pos]

lemma Gamma0_nonneg : 0 ≤ Gamma0 := by
  unfold Gamma0
  exact Real.arccos_nonneg _

lemma Gamma0_le_pi : Gamma0 ≤ Real.pi := by
  unfold Gamma0
  exact Real.arccos_le_pi _

lemma Gamma0_pos : 0 < Gamma0 := by
  unfold Gamma0
  exact Real.arccos_pos.mpr q0_div_one_add_q0_lt_one

lemma cos_Gamma0 : cos Gamma0 = q0 / (1 + q0) := by
  unfold Gamma0
  have hden : 0 < 1 + q0 := by linarith [q0_pos]
  have hpos : 0 < q0 / (1 + q0) := div_pos q0_pos hden
  exact Real.cos_arccos (by nlinarith [hpos]) q0_div_one_add_q0_lt_one.le

/-- `Gamma0 < pi/2 - 4/9`: rational-free location of the source's
`Gamma`.  From `sin(4/9) < 4/9 < q0/(1+q0) = cos Gamma0` and cos
antitone on `[0, pi]`. -/
lemma Gamma0_lt_pi_div_two_sub_four_ninths : Gamma0 < Real.pi / 2 - 4 / 9 := by
  have hsinlt : sin (4 / 9) < 4 / 9 := Real.sin_lt (by norm_num)
  have hcoslt : cos (Real.pi / 2 - 4 / 9) < cos Gamma0 := by
    rw [Real.cos_pi_div_two_sub, cos_Gamma0]
    exact lt_trans hsinlt q0_div_one_add_q0_gt_four_ninths
  have hx : Real.pi / 2 - 4 / 9 ∈ Set.Icc (0 : ℝ) Real.pi := by
    constructor <;> nlinarith [Real.pi_pos, Real.pi_gt_three]
  have hy : Gamma0 ∈ Set.Icc (0 : ℝ) Real.pi := ⟨Gamma0_nonneg, Gamma0_le_pi⟩
  by_contra hnot
  have hxΓ : Real.pi / 2 - 4 / 9 ≤ Gamma0 := le_of_not_gt hnot
  have hcosle : cos Gamma0 ≤ cos (Real.pi / 2 - 4 / 9) :=
    Real.cos_le_cos_of_nonneg_of_le_pi (by nlinarith [Real.pi_gt_three]) hy.2 hxΓ
  exact lt_irrefl _ (lt_of_lt_of_le hcoslt hcosle)

lemma Gamma0_lt_pi_div_two : Gamma0 < Real.pi / 2 := by
  linarith [Gamma0_lt_pi_div_two_sub_four_ninths, Real.pi_pos]

/-- `cot Gamma0 > 1/2`: from `cos Gamma0 = q0/(1+q0)`,
`sin^2 = 1 - cos^2` and `q0 < 5/6`. -/
lemma cot_Gamma0_gt_half : 1 / 2 < Real.cot Gamma0 := by
  rw [Real.cot_eq_cos_div_sin]
  have hsinpos : 0 < sin Gamma0 :=
    Real.sin_pos_of_pos_of_lt_pi Gamma0_pos (by linarith [Gamma0_lt_pi_div_two, Real.pi_pos])
  have hcosn : 0 ≤ cos Gamma0 :=
    (Real.cos_pos_of_mem_Ioo ⟨by linarith [Gamma0_pos, Real.pi_pos], Gamma0_lt_pi_div_two⟩).le
  have hsq : (2 * cos Gamma0) ^ 2 > 1 - cos Gamma0 ^ 2 := by
    have hc : cos Gamma0 = q0 / (1 + q0) := cos_Gamma0
    rw [hc]
    have hden : 0 < 1 + q0 := by linarith [q0_pos]
    have h5 : 5 * (q0 / (1 + q0)) ^ 2 > 1 := by
      rw [div_pow]
      have hnum : (1 + q0) ^ 2 < 5 * q0 ^ 2 := by
        nlinarith [q0_sq, q0_lt_five_sixths]
      rw [← mul_div_assoc]
      exact (one_lt_div (sq_pos_of_pos hden)).2 hnum
    nlinarith [h5]
  have hsq' : sin Gamma0 ^ 2 < (2 * cos Gamma0) ^ 2 := by
    have hsc : sin Gamma0 ^ 2 = 1 - cos Gamma0 ^ 2 := by
      nlinarith [Real.sin_sq_add_cos_sq Gamma0]
    nlinarith [hsq, hsc]
  have hlt : sin Gamma0 < 2 * cos Gamma0 :=
    (sq_lt_sq₀ (Real.sin_nonneg_of_nonneg_of_le_pi Gamma0_nonneg (by linarith [Gamma0_lt_pi_div_two, Real.pi_pos]))
      (by nlinarith [hcosn])).1 hsq'
  rw [lt_div_iff₀ hsinpos]
  nlinarith [hlt]

/-- cot is antitone on `(0, pi)`, stated for `γ <= Gamma0 < pi/2`. -/
lemma cot_ge_cot_Gamma0 {γ : ℝ} (hγ0 : 0 < γ) (hγΓ : γ ≤ Gamma0) :
    Real.cot Gamma0 ≤ Real.cot γ := by
  have hγp : γ < Real.pi / 2 := by linarith [hγΓ, Gamma0_lt_pi_div_two]
  have hγπ : γ < Real.pi := by linarith [hγp, Real.pi_pos]
  have hsinγ : 0 < sin γ := Real.sin_pos_of_pos_of_lt_pi hγ0 hγπ
  have hcosγ : 0 < cos γ := Real.cos_pos_of_mem_Ioo ⟨by linarith [hγ0, Real.pi_pos], hγp⟩
  have hsinΓ : 0 < sin Gamma0 :=
    Real.sin_pos_of_pos_of_lt_pi Gamma0_pos (by linarith [Gamma0_lt_pi_div_two, Real.pi_pos])
  have hcosΓ : 0 < cos Gamma0 :=
    Real.cos_pos_of_mem_Ioo ⟨by linarith [Gamma0_pos, Real.pi_pos], Gamma0_lt_pi_div_two⟩
  rw [Real.cot_eq_cos_div_sin, Real.cot_eq_cos_div_sin]
  rw [div_le_div_iff₀ hsinΓ hsinγ]
  have hcosle : cos Gamma0 ≤ cos γ :=
    Real.cos_le_cos_of_nonneg_of_le_pi hγ0.le (by linarith [Gamma0_le_pi]) hγΓ
  have hsinle : sin γ ≤ sin Gamma0 :=
    Real.sin_le_sin_of_le_of_le_pi_div_two (by linarith [hγ0, Real.pi_pos])
      (by linarith [Gamma0_lt_pi_div_two]) hγΓ
  have h1 : cos Gamma0 * sin γ ≤ cos Gamma0 * sin Gamma0 :=
    mul_le_mul_of_nonneg_left hsinle hcosΓ.le
  have h2 : cos Gamma0 * sin Gamma0 ≤ cos γ * sin Gamma0 :=
    mul_le_mul_of_nonneg_right hcosle hsinΓ.le
  exact le_trans h1 h2

/-- `W0(γ) < 4*q0/3` for `0 < γ <= Gamma0` (certificate-free; used by P2). -/
lemma W0_lt_four_thirds_q0 {γ : ℝ} (hγ0 : 0 < γ) (hγΓ : γ ≤ Gamma0) :
    W0 γ < 4 / 3 * q0 := by
  have hγp : γ < Real.pi / 2 := by linarith [hγΓ, Gamma0_lt_pi_div_two]
  have hcotγ : 1 / 2 < Real.cot γ := lt_of_lt_of_le cot_Gamma0_gt_half (cot_ge_cot_Gamma0 hγ0 hγΓ)
  have hcotγ' : 0 < Real.cot γ := by linarith [hcotγ]
  have hπΓ : 0 < Real.pi - Gamma0 := by linarith [Gamma0_lt_pi_div_two, Real.pi_pos]
  have hπγ : Real.pi - Gamma0 ≤ Real.pi - γ := by linarith [hγΓ]
  have hprod : Real.pi / 2 + 4 / 9 < 2 * (Real.pi - γ) * Real.cot γ := by
    have hA : Real.pi / 2 + 4 / 9 < Real.pi - Gamma0 := by
      have hΓ : Gamma0 < Real.pi / 2 - 4 / 9 := Gamma0_lt_pi_div_two_sub_four_ninths
      linarith
    have hB : Real.pi - Gamma0 < 2 * (Real.pi - Gamma0) * Real.cot γ := by
      have h1 : 1 < 2 * Real.cot γ := by nlinarith [hcotγ]
      simpa using (mul_lt_mul_of_pos_left h1 hπΓ).trans_eq (by ring)
    have hC : 2 * (Real.pi - Gamma0) * Real.cot γ ≤ 2 * (Real.pi - γ) * Real.cot γ := by
      have h' : (Real.pi - Gamma0) * Real.cot γ ≤ (Real.pi - γ) * Real.cot γ :=
        mul_le_mul_of_nonneg_right hπγ hcotγ'.le
      nlinarith [h']
    exact lt_of_lt_of_le (lt_trans hA hB) hC
  unfold W0
  have hW : 3 - 2 * (Real.pi - γ) * Real.cot γ < 3 - (Real.pi / 2 + 4 / 9) := by
    linarith [hprod]
  have h19 : 3 - (Real.pi / 2 + 4 / 9) ≤ 19 / 18 := by
    have hπ : Real.pi / 2 + 4 / 9 > 3 / 2 + 4 / 9 := by nlinarith [Real.pi_gt_three]
    nlinarith
  have hc : (19 : ℝ) / 18 < 4 / 3 * q0 := by
    have h16 : (19 : ℝ) / 18 < (16 : ℝ) / 15 := by norm_num
    have hq : 16 / 15 < 4 / 3 * q0 := by nlinarith [q0_gt_four_fifths]
    exact lt_trans h16 hq
  exact lt_trans (lt_of_lt_of_le hW h19) hc

lemma Phi_nonneg (q x : ℝ) : 0 ≤ Phi q x := by
  unfold Phi
  nlinarith [sq_nonneg (cos x), sq_nonneg (sin x), sq_nonneg q]

lemma Phi_le_one {q x : ℝ} (hq0 : 0 ≤ q) (hq1 : q ≤ 1) : Phi q x ≤ 1 := by
  unfold Phi
  have hq2 : q ^ 2 ≤ 1 := by nlinarith [mul_self_le_mul_self hq0 hq1]
  have hc : q ^ 2 * sin x ^ 2 ≤ sin x ^ 2 := mul_le_of_le_one_left (sq_nonneg (sin x)) hq2
  have hsum : cos x ^ 2 + q ^ 2 * sin x ^ 2 ≤ cos x ^ 2 + sin x ^ 2 := by nlinarith [hc]
  nlinarith [Real.cos_sq_add_sin_sq x]

lemma Phi_ge_sq {q x : ℝ} (hq0 : 0 ≤ q) (hq1 : q ≤ 1) : q ^ 2 ≤ Phi q x := by
  unfold Phi
  have hq2 : q ^ 2 ≤ 1 := by nlinarith [mul_self_le_mul_self hq0 hq1]
  have hc : q ^ 2 * cos x ^ 2 ≤ cos x ^ 2 := mul_le_of_le_one_left (sq_nonneg (cos x)) hq2
  calc
    q ^ 2 = q ^ 2 * (cos x ^ 2 + sin x ^ 2) := by rw [Real.cos_sq_add_sin_sq]; ring
    _ = q ^ 2 * cos x ^ 2 + q ^ 2 * sin x ^ 2 := by ring
    _ ≤ cos x ^ 2 + q ^ 2 * sin x ^ 2 := by nlinarith [hc]

/-- `(6*sqrt 6 - 6)/5 > 4/3` (P1's strict constant; from `486 > 361`). -/
lemma six_sqrt_six_sub_six_div_five_gt_four_thirds : 4 / 3 < (6 * Real.sqrt 6 - 6) / 5 := by
  have hsq : (19 / 9 : ℝ) ^ 2 < (Real.sqrt 6) ^ 2 := by
    rw [Real.sq_sqrt (by norm_num)]
    norm_num
  have hlt : 19 / 9 < Real.sqrt 6 :=
    (sq_lt_sq₀ (by norm_num : 0 ≤ (19 : ℝ) / 9) (Real.sqrt_nonneg 6)).1 hsq
  nlinarith [hlt]

/-- Lemma P1: `G(q,c,x) <= -(6*sqrt 6 - 6)/5` for `x in (0, pi/2)`,
`q in [q0, 1]`, `c in (0, 1/2)`. -/
lemma P1_bound {q c x : ℝ} (hq0 : 0 < q) (hq1 : q ≤ 1) (hqq : q0 ≤ q)
    (hc0 : 0 < c) (hc : c < 1 / 2) (hx0 : 0 < x) (hxp : x < Real.pi / 2) :
    G q c x ≤ -(6 * Real.sqrt 6 - 6) / 5 := by
  have hD : 0 < q + c * Phi q x := by
    have hcΦ : 0 ≤ c * Phi q x := mul_nonneg hc0.le (Phi_nonneg q x)
    linarith
  have hΦ : q ^ 2 ≤ Phi q x := Phi_ge_sq hq0.le hq1
  have hΦpos : 0 < Phi q x := lt_of_lt_of_le (sq_pos_of_pos hq0) hΦ
  have hcot : 0 < Real.cot x := by
    rw [Real.cot_eq_cos_div_sin]
    exact div_pos (Real.cos_pos_of_mem_Ioo ⟨by linarith [hx0, Real.pi_pos], hxp⟩)
      (Real.sin_pos_of_pos_of_lt_pi hx0 (by linarith [hxp, Real.pi_pos]))
  have hxcot : 0 ≤ x * Real.cot x := mul_nonneg hx0.le hcot.le
  have hW : 3 ≤ 3 + 2 * x * Real.cot x := by nlinarith [hxcot]
  have hT2 : 2 * c * x * Phi q x * (q ^ 2 - 1) * sin x * cos x /
      (q + c * Phi q x) ^ 2 ≤ 0 := by
    have hq1' : q ^ 2 - 1 ≤ 0 := by nlinarith [hq1]
    have hsin : 0 ≤ sin x := (Real.sin_pos_of_pos_of_lt_pi hx0 (by linarith [hxp, Real.pi_pos])).le
    have hcos : 0 ≤ cos x := (Real.cos_pos_of_mem_Ioo ⟨by linarith [hx0, Real.pi_pos], hxp⟩).le
    have hbase : 0 ≤ 2 * c * x * Phi q x :=
      mul_nonneg (by positivity : 0 ≤ 2 * c * x) (Phi_nonneg q x)
    have h1 : 2 * c * x * Phi q x * (q ^ 2 - 1) ≤ 0 :=
      mul_nonpos_of_nonneg_of_nonpos hbase hq1'
    have h2 : 2 * c * x * Phi q x * (q ^ 2 - 1) * sin x ≤ 0 :=
      mul_nonpos_of_nonpos_of_nonneg h1 hsin
    have hnum : 2 * c * x * Phi q x * (q ^ 2 - 1) * sin x * cos x ≤ 0 :=
      mul_nonpos_of_nonpos_of_nonneg h2 hcos
    exact div_nonpos_of_nonpos_of_nonneg hnum (sq_pos_of_pos hD).le
  have hΦDpos : 0 < Phi q x / (q + c * Phi q x) := div_pos hΦpos hD
  have hWle : -Phi q x * (3 + 2 * x * Real.cot x) / (q + c * Phi q x) ≤
      -3 * Phi q x / (q + c * Phi q x) := by
    have h3le : 3 * (Phi q x / (q + c * Phi q x)) ≤
        (3 + 2 * x * Real.cot x) * (Phi q x / (q + c * Phi q x)) :=
      mul_le_mul_of_nonneg_right hW (le_of_lt hΦDpos)
    have h1 : -Phi q x * (3 + 2 * x * Real.cot x) / (q + c * Phi q x) =
        -((3 + 2 * x * Real.cot x) * (Phi q x / (q + c * Phi q x))) := by
      field_simp [hD.ne']
    have h2 : -3 * Phi q x / (q + c * Phi q x) =
        -3 * (Phi q x / (q + c * Phi q x)) := by
      field_simp [hD.ne']
    rw [h1, h2]
    nlinarith [h3le, hxcot, hΦDpos.le]
  have hmain : -3 * Phi q x / (q + c * Phi q x) ≤ -(6 * Real.sqrt 6 - 6) / 5 := by
    have hΦD_id : Phi q x / (q + c * Phi q x) = 1 / (q / Phi q x + c) := by
      field_simp [hΦpos.ne', hD.ne']
    have hqΦ : q / Phi q x ≤ 1 / q := by
      exact (div_le_div_iff₀ hΦpos hq0).2 (by simpa [pow_two] using hΦ)
    have hq1inv : 1 / q ≤ 1 / q0 := by
      exact (div_le_div_iff₀ hq0 q0_pos).2 (by nlinarith [hqq])
    have hsum : q / Phi q x + c ≤ 1 / q0 + 1 / 2 := by nlinarith [hqΦ, hq1inv, hc]
    have hqΦpos : 0 < q / Phi q x := div_pos hq0 hΦpos
    have hsumpos : 0 < q / Phi q x + c := by nlinarith [hqΦpos, hc0]
    have hdenle : 1 / (1 / q0 + 1 / 2) ≤ 1 / (q / Phi q x + c) := by
      have h := inv_anti₀ hsumpos hsum
      simpa [one_div] using h
    have hconst : 3 / (1 / q0 + 1 / 2) = (6 * Real.sqrt 6 - 6) / 5 := by
      have hq0' : q0 = Real.sqrt 6 / 3 := by
        refine (sq_eq_sq₀ (le_of_lt q0_pos) (by positivity)).1 ?_
        rw [q0_sq, div_pow, Real.sq_sqrt (by norm_num : 0 ≤ (6 : ℝ))]
        norm_num
      have h1q0 : 1 / q0 = Real.sqrt 6 / 2 := by
        rw [one_div, hq0']
        have hsq6 : (Real.sqrt 6) ^ 2 = 6 := Real.sq_sqrt (by norm_num)
        field_simp [hsq6]; nlinarith [hsq6]
      rw [h1q0]
      have hsq6 : (Real.sqrt 6) ^ 2 = 6 := Real.sq_sqrt (by norm_num)
      field_simp [hsq6]; nlinarith [hsq6]
    have h3Φ : 3 * (Phi q x / (q + c * Phi q x)) ≥ 3 / (1 / q0 + 1 / 2) := by
      rw [hΦD_id]
      exact mul_le_mul_of_nonneg_left (by simpa [one_div] using hdenle) (by norm_num)
    have h3Φ' : -3 * (Phi q x / (q + c * Phi q x)) ≤ -3 / (1 / q0 + 1 / 2) := by
      rw [neg_mul, neg_div]
      exact neg_le_neg h3Φ
    have h2 : -3 * Phi q x / (q + c * Phi q x) =
        -3 * (Phi q x / (q + c * Phi q x)) := by
      field_simp [hD.ne']
    have hneg : -3 / (1 / q0 + 1 / 2) = -(6 * Real.sqrt 6 - 6) / 5 := by
      rw [neg_div, hconst]
      rw [← neg_div]
    rw [h2]
    exact le_trans h3Φ' hneg.le
  calc
    G q c x = -Phi q x * (3 + 2 * x * Real.cot x) / (q + c * Phi q x) +
        2 * c * x * Phi q x * (q ^ 2 - 1) * sin x * cos x / (q + c * Phi q x) ^ 2 := by
      rfl
    _ ≤ -Phi q x * (3 + 2 * x * Real.cot x) / (q + c * Phi q x) := by nlinarith [hT2]
    _ ≤ -3 * Phi q x / (q + c * Phi q x) := hWle
    _ ≤ -(6 * Real.sqrt 6 - 6) / 5 := hmain

/-- `G(q,c,x) < 0` under the P1 hypotheses. -/
lemma P1_neg {q c x : ℝ} (hq0 : 0 < q) (hq1 : q ≤ 1) (hqq : q0 ≤ q)
    (hc0 : 0 < c) (hc : c < 1 / 2) (hx0 : 0 < x) (hxp : x < Real.pi / 2) :
    G q c x < 0 := by
  have h := P1_bound hq0 hq1 hqq hc0 hc hx0 hxp
  have hcst : -(6 * Real.sqrt 6 - 6) / 5 < 0 := by
    have h6 : 1 < Real.sqrt 6 := by
      have hsq : (1 : ℝ) ^ 2 < (Real.sqrt 6) ^ 2 := by
        rw [Real.sq_sqrt (by norm_num)]
        norm_num
      exact (sq_lt_sq₀ (by norm_num : 0 ≤ (1 : ℝ)) (Real.sqrt_nonneg 6)).1 hsq
    nlinarith
  exact lt_of_le_of_lt h hcst

/-- Lemma P2: `G(q,c,pi-γ) > -4/3` for `γ in (0, Gamma0]`,
`q in [q0, 1]`, `c in (0, 1/2)` (the branch reduction `γ <= Gamma0`
is a hypothesis, see the file header). -/
lemma P2_bound {q c γ : ℝ} (hq0 : 0 < q) (hq1 : q ≤ 1) (hqq : q0 ≤ q)
    (hc0 : 0 < c) (hc : c < 1 / 2) (hγ0 : 0 < γ) (hγΓ : γ ≤ Gamma0) :
    -(4 / 3) < G q c (Real.pi - γ) := by
  have hγp : γ < Real.pi / 2 := by linarith [hγΓ, Gamma0_lt_pi_div_two]
  have hγπ : γ < Real.pi := by linarith [hγp, Real.pi_pos]
  have hsinγ : 0 < sin γ := Real.sin_pos_of_pos_of_lt_pi hγ0 hγπ
  have hcosγ : 0 < cos γ := Real.cos_pos_of_mem_Ioo ⟨by linarith [hγ0, Real.pi_pos], hγp⟩
  have hπγ : 0 < Real.pi - γ := by linarith [hγπ]
  have hcot : Real.cot (Real.pi - γ) = -Real.cot γ := by
    rw [Real.cot_eq_cos_div_sin, Real.cot_eq_cos_div_sin]
    rw [Real.cos_pi_sub, Real.sin_pi_sub]
    ring
  have hΦπ : Phi q (Real.pi - γ) = Phi q γ := by
    unfold Phi
    rw [Real.cos_pi_sub, Real.sin_pi_sub]
    ring
  have hD : 0 < q + c * Phi q γ := by
    have hcΦ : 0 ≤ c * Phi q γ := mul_nonneg hc0.le (Phi_nonneg q γ)
    linarith
  let D : ℝ := q + c * Phi q γ
  have hG : G q c (Real.pi - γ) =
      -Phi q γ * W0 γ / D +
        2 * c * (Real.pi - γ) * Phi q γ * (1 - q ^ 2) * sin γ * cos γ / D ^ 2 := by
    unfold G W0
    rw [hΦπ, hcot]
    have hsc : 2 * c * (Real.pi - γ) * Phi q γ * (q ^ 2 - 1) * sin (Real.pi - γ) *
          cos (Real.pi - γ) =
        2 * c * (Real.pi - γ) * Phi q γ * (1 - q ^ 2) * sin γ * cos γ := by
      rw [Real.sin_pi_sub, Real.cos_pi_sub]
      ring
    rw [hsc]
    ring
  have hP : 0 ≤ 2 * c * (Real.pi - γ) * Phi q γ * (1 - q ^ 2) * sin γ * cos γ / D ^ 2 := by
    have h1q : 0 ≤ 1 - q ^ 2 := by nlinarith [hq1]
    have hbase : 0 ≤ 2 * c * (Real.pi - γ) * Phi q γ :=
      mul_nonneg (by positivity : 0 ≤ 2 * c * (Real.pi - γ)) (Phi_nonneg q γ)
    have h1 : 0 ≤ 2 * c * (Real.pi - γ) * Phi q γ * (1 - q ^ 2) := mul_nonneg hbase h1q
    have h2 : 0 ≤ 2 * c * (Real.pi - γ) * Phi q γ * (1 - q ^ 2) * sin γ :=
      mul_nonneg h1 hsinγ.le
    have h3 : 0 ≤ 2 * c * (Real.pi - γ) * Phi q γ * (1 - q ^ 2) * sin γ * cos γ :=
      mul_nonneg h2 hcosγ.le
    exact div_nonneg h3 (sq_pos_of_pos hD).le
  have hW0 : W0 γ < 4 / 3 * q0 := W0_lt_four_thirds_q0 hγ0 hγΓ
  by_cases hW : W0 γ ≤ 0
  · have hneg : 0 ≤ -Phi q γ * W0 γ / D := by
      have hnum : 0 ≤ -Phi q γ * W0 γ := by
        rw [neg_mul]
        exact neg_nonneg.mpr (mul_nonpos_of_nonneg_of_nonpos (Phi_nonneg q γ) hW)
      exact div_nonneg hnum hD.le
    rw [hG]
    nlinarith [hP, hneg]
  · have hW' : 0 < W0 γ := lt_of_not_ge hW
    have hΦle : Phi q γ ≤ 1 := Phi_le_one hq0.le hq1
    have hqΦ : q * Phi q γ ≤ D := by
      dsimp [D]
      have h1 : q * (Phi q γ - 1) ≤ 0 :=
        mul_nonpos_of_nonneg_of_nonpos hq0.le (sub_nonpos.mpr hΦle)
      have h2 : 0 ≤ c * Phi q γ := mul_nonneg hc0.le (Phi_nonneg q γ)
      nlinarith [h1, h2]
    have hΦD : Phi q γ / D ≤ 1 / q := by
      exact (div_le_div_iff₀ hD hq0).2 (by simpa [mul_comm, one_mul] using hqΦ)
    have h1q : 1 / q ≤ 1 / q0 := by
      exact (div_le_div_iff₀ hq0 q0_pos).2 (by nlinarith [hqq])
    have hmain : Phi q γ * W0 γ / D < 4 / 3 := by
      have h1 : W0 γ * (Phi q γ / D) ≤ W0 γ * (1 / q) :=
        mul_le_mul_of_nonneg_left hΦD (le_of_lt hW')
      have h2 : W0 γ * (1 / q) ≤ W0 γ * (1 / q0) :=
        mul_le_mul_of_nonneg_left h1q (le_of_lt hW')
      have h3 : W0 γ * (1 / q0) < 4 / 3 := by
        rw [mul_one_div]
        exact (div_lt_iff₀ q0_pos).mpr hW0
      have h01 : W0 γ * (Phi q γ / D) < 4 / 3 := lt_of_le_of_lt (le_trans h1 h2) h3
      have hEq : Phi q γ * W0 γ / D = W0 γ * (Phi q γ / D) := by
        field_simp [D, hD.ne']
      rw [hEq]
      exact h01
    have hgt : -(4 / 3) < -Phi q γ * W0 γ / D := by
      rw [neg_mul, neg_div]
      exact neg_lt_neg hmain
    rw [hG]
    nlinarith [hP, hgt]

/-- KEY-LEMMA monotonicity step (algebraic form): if `Fe = M1 - M2 >= 0`
then `Fe' = (M1-M2)*G1 + M2*(G1-G2) < 0`, given `G1 < 0` (P1) and
`G1 < G2` (P1+P2). -/
lemma Fep_lt_zero_of_nonneg {M1 M2 G1 G2 : ℝ} (hM2 : 0 < M2)
    (hG1 : G1 < 0) (hG12 : G1 < G2) (hM : M2 ≤ M1) :
    (M1 - M2) * G1 + M2 * (G1 - G2) < 0 := by
  have h1 : (M1 - M2) * G1 ≤ 0 :=
    mul_nonpos_of_nonneg_of_nonpos (sub_nonneg.mpr hM) (le_of_lt hG1)
  have h2 : M2 * (G1 - G2) < 0 :=
    mul_neg_of_pos_of_neg hM2 (sub_neg.mpr hG12)
  nlinarith [h1, h2]

/-- `G1 < G2` under the P1/P2 hypotheses (both evaluated at the
branch points `x = alpha1`, `pi-γ = alpha2`). -/
lemma P1_lt_P2 {q c x γ : ℝ} (hq0 : 0 < q) (hq1 : q ≤ 1) (hqq : q0 ≤ q)
    (hc0 : 0 < c) (hc : c < 1 / 2) (hx0 : 0 < x) (hxp : x < Real.pi / 2)
    (hγ0 : 0 < γ) (hγΓ : γ ≤ Gamma0) :
    G q c x < G q c (Real.pi - γ) := by
  have h1 := P1_bound hq0 hq1 hqq hc0 hc hx0 hxp
  have h2 := P2_bound hq0 hq1 hqq hc0 hc hγ0 hγΓ
  have hcst : 4 / 3 < (6 * Real.sqrt 6 - 6) / 5 := six_sqrt_six_sub_six_div_five_gt_four_thirds
  have h1' : G q c x < -(4 / 3) := lt_of_le_of_lt h1 (by nlinarith [hcst])
  exact lt_trans h1' h2

/-- `gamma_0(q) <= Gamma0` for `q0 <= q` (arccos antitone; the second
half of the branch reduction `γ <= gamma_0(q) <= Gamma0`). -/
lemma gamma0_mono {q : ℝ} (hqq : q0 ≤ q) : gamma0 q ≤ Gamma0 := by
  have hden : 0 < 1 + q := by nlinarith [hqq, q0_pos]
  have hq0den : 0 < 1 + q0 := by linarith [q0_pos]
  have hle : q0 / (1 + q0) ≤ q / (1 + q) := by
    rw [div_le_div_iff₀ hq0den hden]
    nlinarith [hqq]
  unfold gamma0 Gamma0
  exact Real.arccos_le_arccos hle

end
end SymlineKeyLemma
end SL
