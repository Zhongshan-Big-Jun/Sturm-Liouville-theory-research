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
* `p`, `Q0`, `rho0`: `pi^2/4`, the right-hand bound of Lemma P2, and the
  chain bound `t/(y+t) * Q0(gamma)`.
* `GammaStar` and its location lemmas: the source threshold `gamma_0*`,
  the root of `tan gamma = 2 * (pi - gamma) / 3` in `(pi/4, 9*pi/20)`.
* `strictConcaveOn_f`, `f_pi_div_four_gt`, `ys2_of_ge_gamma_star`:
  Lemma ys2 in its strict form, `p < (pi - gamma)^2 * sin gamma^2` for
  `gamma in [GammaStar, pi/2)`.
* `P2`: `s1^2 * s2^2 * T / Delta * (1-q^2) <= Q0(gamma)` via the three-term
  nonnegative decomposition `E0/y^2 = cos^2(gamma)*(p-A^2)
  + cos^2(A)*(y^2*s2^2-p) + cos^2(A)*A^2*cos^2(gamma)`.
* `tension_ratio_chain`: `rho <= rho0(gamma)` from P1 and P2.

Honesty note: the algebraic core is formalized here (P1, the
`FeEquiv`/`rho` equivalence, P2's three-term decomposition, and the
tension-ratio chain), together with Lemma ys2.  `GammaStar` is the source
threshold `gamma_0*` (root of `tan gamma = 2 * (pi - gamma) / 3`); its
existence is shown by IVT in `(pi/4, 9*pi/20)` with certificate-free
endpoint checks, and `ys2_of_ge_gamma_star` proves the strict bound
`p < (pi - gamma)^2 * sin gamma^2` for `gamma in [GammaStar, pi/2)` by
strict concavity of `f(gamma) = (pi - gamma) * sin gamma` on `[pi/4, pi/2]`
(`f(pi/4) = 3*pi*sqrt2/8 > pi/2`, `f(pi/2) = pi/2`).  This replaces the
rational certificates of the source (`gamma_0* in (0.961, 0.97)` with
alternating-series tan bounds); the location `gamma_0* > pi/4` is all the
chain needs.  Numerical evidence is never used as a theorem.
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

/-- `p = pi^2/4`, the squared half-period bound of the source. -/
def p : ℝ := Real.pi ^ 2 / 4

/-- `Q0(gamma) = s2^2 * (y^2 - p) / (y^2 * s2^2 - p)` of Lemma P2. -/
def Q0 (γ : ℝ) : ℝ :=
  sin γ ^ 2 * ((Real.pi - γ) ^ 2 - p) / ((Real.pi - γ) ^ 2 * sin γ ^ 2 - p)

/-- `rho0(gamma) = t/(y+t) * Q0(gamma)` of the tension-ratio chain. -/
def rho0 (γ : ℝ) : ℝ :=
  Real.tan γ / (Real.pi - γ + Real.tan γ) * Q0 γ

/-- `1 - q^2 >= 0` for `0 < q < 1`. -/
lemma one_sub_sq_nonneg {q : ℝ} (hq0 : 0 < q) (hq1 : q < 1) :
    0 ≤ 1 - q ^ 2 := by
  nlinarith [hq0, hq1, sq_nonneg q]

/-- `p = (pi/2)^2`. -/
lemma p_eq_sq_half : p = (Real.pi / 2) ^ 2 := by
  unfold p
  ring

/-- `p - A^2 >= 0` for `0 < A < pi/2`. -/
lemma p_sub_sq_nonneg {A : ℝ} (hA0 : 0 < A) (hAp : A < Real.pi / 2) :
    0 ≤ p - A ^ 2 := by
  rw [p_eq_sq_half]
  nlinarith [Real.pi_div_two_pos, hA0, hAp]

/-- `T A gamma > 0` for `0 < A < pi/2` and `gamma < pi/2`
(`y = pi - gamma > pi/2 > A`). -/
lemma T_pos {γ A : ℝ} (hγp : γ < Real.pi / 2) (hA0 : 0 < A)
    (hAp : A < Real.pi / 2) : 0 < T A γ := by
  unfold T
  have hπy : Real.pi / 2 < Real.pi - γ := by linarith [hγp]
  nlinarith [Real.pi_div_two_pos, hA0, hAp]

/-- `t/(y+t) <= 1` for `t, y > 0` (part of Lemma P1). -/
lemma t_div_add_le_one {t y : ℝ} (ht : 0 < t) (hy : 0 < y) :
    t / (y + t) ≤ 1 := by
  rw [div_le_iff₀ (by linarith)]
  nlinarith

/-- `gamma_0*` of the source: a root of `tan gamma = 2 * (pi - gamma) / 3`
in `(pi/4, 9*pi/20)`.  Existence by IVT with certificate-free endpoint
checks (`phi(pi/4) = 1 - pi/2 < 0`; `phi(9*pi/20) > 0` from `tan x > x`
and a linear comparison).  Uniqueness is not needed. -/
lemma exists_gamma_star :
    ∃ γ : ℝ, Real.pi / 4 < γ ∧ γ < 9 * Real.pi / 20 ∧
      Real.tan γ = 2 * (Real.pi - γ) / 3 := by
  let φ : ℝ → ℝ := fun γ => Real.tan γ - 2 * (Real.pi - γ) / 3
  have hφcont : ContinuousOn φ (Set.Icc (Real.pi / 4) (9 * Real.pi / 20)) := by
    have htan : ContinuousOn (fun γ : ℝ => Real.tan γ)
        (Set.Icc (Real.pi / 4) (9 * Real.pi / 20)) := by
      exact Real.continuousOn_tan.mono (by
        intro x hx
        exact ne_of_gt (Real.cos_pos_of_mem_Ioo (by
          constructor
          · linarith [hx.1, Real.pi_pos]
          · nlinarith [hx.2, Real.pi_pos])))
    have hlin : ContinuousOn (fun γ : ℝ => 2 * (Real.pi - γ) / 3)
        (Set.Icc (Real.pi / 4) (9 * Real.pi / 20)) := by
      fun_prop
    simpa [φ] using htan.sub hlin
  have hφ4 : φ (Real.pi / 4) < 0 := by
    dsimp [φ]
    rw [Real.tan_pi_div_four]
    nlinarith [Real.pi_gt_three]
  have hφ9 : 0 < φ (9 * Real.pi / 20) := by
    dsimp [φ]
    have htan : 9 * Real.pi / 20 < Real.tan (9 * Real.pi / 20) := by
      exact Real.lt_tan (by nlinarith [Real.pi_pos]) (by nlinarith [Real.pi_pos])
    have hlin : 2 * (Real.pi - 9 * Real.pi / 20) / 3 < 9 * Real.pi / 20 := by
      nlinarith [Real.pi_pos]
    have hlt : 2 * (Real.pi - 9 * Real.pi / 20) / 3 < Real.tan (9 * Real.pi / 20) :=
      lt_of_lt_of_le hlin htan.le
    linarith
  have hmid : 0 ∈ Set.Icc (φ (Real.pi / 4)) (φ (9 * Real.pi / 20)) :=
    ⟨le_of_lt hφ4, le_of_lt hφ9⟩
  have hroot : 0 ∈ (fun γ => φ γ) '' Set.Icc (Real.pi / 4) (9 * Real.pi / 20) :=
    intermediate_value_Icc (a := Real.pi / 4) (b := 9 * Real.pi / 20)
      (by nlinarith [Real.pi_pos]) hφcont hmid
  rcases hroot with ⟨γ, hγ, hφγ⟩
  refine ⟨γ, ?_, ?_, ?_⟩
  · have hne : γ ≠ Real.pi / 4 := by
      intro h
      subst γ
      dsimp [φ] at hφ4 hφγ
      nlinarith [hφ4, hφγ]
    exact lt_of_le_of_ne hγ.1 hne.symm
  · have hne : γ ≠ 9 * Real.pi / 20 := by
      intro h
      subst γ
      dsimp [φ] at hφ9 hφγ
      nlinarith [hφ9, hφγ]
    exact lt_of_le_of_ne hγ.2 hne
  · dsimp [φ] at hφγ
    linarith

/-- The source threshold `gamma_0*`: the root of
`tan gamma = 2 * (pi - gamma) / 3` in `(pi/4, 9*pi/20)`. -/
noncomputable def GammaStar : ℝ := Classical.choose exists_gamma_star

lemma gamma_star_gt_pi_div_four : Real.pi / 4 < GammaStar :=
  (Classical.choose_spec exists_gamma_star).1

lemma gamma_star_lt_nine_pi_div_twenty : GammaStar < 9 * Real.pi / 20 :=
  (Classical.choose_spec exists_gamma_star).2.1

lemma gamma_star_tan : Real.tan GammaStar = 2 * (Real.pi - GammaStar) / 3 :=
  (Classical.choose_spec exists_gamma_star).2.2

lemma gamma_star_pos : 0 < GammaStar := by
  linarith [gamma_star_gt_pi_div_four, Real.pi_pos]

lemma gamma_star_lt_pi_div_two : GammaStar < Real.pi / 2 := by
  linarith [gamma_star_lt_nine_pi_div_twenty, Real.pi_pos]

/-- `f(gamma) = (pi - gamma) * sin gamma` is strictly concave on
`[pi/4, pi/2]` (`f'' = -2 * cos gamma - (pi - gamma) * sin gamma < 0`). -/
lemma strictConcaveOn_f :
    StrictConcaveOn ℝ (Set.Icc (Real.pi / 4) (Real.pi / 2))
      (fun γ : ℝ => (Real.pi - γ) * Real.sin γ) := by
  refine strictConcaveOn_of_deriv2_neg ?_ ?_ ?_
  · exact convex_Icc (Real.pi / 4) (Real.pi / 2)
  · exact (by fun_prop : Continuous fun γ : ℝ => (Real.pi - γ) * Real.sin γ).continuousOn
  · intro x hx
    rw [interior_Icc] at hx
    have hxlo : Real.pi / 4 < x := hx.1
    have hxhi : x < Real.pi / 2 := hx.2
    have hxpos : 0 < x := by linarith [hxlo, Real.pi_pos]
    have hd1 : deriv (fun γ : ℝ => (Real.pi - γ) * Real.sin γ) =
        fun γ : ℝ => (Real.pi - γ) * Real.cos γ - Real.sin γ := by
      funext γ
      have hg : HasDerivAt (fun γ : ℝ => Real.pi - γ) (-1) γ := by
        simpa using (hasDerivAt_id γ).const_sub (Real.pi)
      have hs : HasDerivAt Real.sin (Real.cos γ) γ := Real.hasDerivAt_sin γ
      have hmul : HasDerivAt (fun γ : ℝ => (Real.pi - γ) * Real.sin γ)
          ((-1) * Real.sin γ + (Real.pi - γ) * Real.cos γ) γ := hg.mul hs
      convert hmul.deriv using 1; ring
    have hd2 : deriv (fun γ : ℝ => (Real.pi - γ) * Real.cos γ - Real.sin γ) =
        fun γ : ℝ => -2 * Real.cos γ - (Real.pi - γ) * Real.sin γ := by
      funext γ
      have hg : HasDerivAt (fun γ : ℝ => Real.pi - γ) (-1) γ := by
        simpa using (hasDerivAt_id γ).const_sub (Real.pi)
      have hc : HasDerivAt Real.cos (-Real.sin γ) γ := Real.hasDerivAt_cos γ
      have hmul : HasDerivAt (fun γ : ℝ => (Real.pi - γ) * Real.cos γ)
          ((-1) * Real.cos γ + (Real.pi - γ) * (-Real.sin γ)) γ := hg.mul hc
      have hs : HasDerivAt Real.sin (Real.cos γ) γ := Real.hasDerivAt_sin γ
      have hsub : HasDerivAt (fun γ : ℝ => (Real.pi - γ) * Real.cos γ - Real.sin γ)
          ((-1) * Real.cos γ + (Real.pi - γ) * (-Real.sin γ) - Real.cos γ) γ := hmul.sub hs
      convert hsub.deriv using 1; ring
    have hd2x : deriv^[2] (fun γ : ℝ => (Real.pi - γ) * Real.sin γ) x =
        -2 * Real.cos x - (Real.pi - x) * Real.sin x := by
      change deriv (deriv (fun γ : ℝ => (Real.pi - γ) * Real.sin γ)) x =
        -2 * Real.cos x - (Real.pi - x) * Real.sin x
      rw [hd1]
      rw [hd2]
    rw [hd2x]
    have hcospos : 0 < Real.cos x :=
      Real.cos_pos_of_mem_Ioo ⟨by linarith [hxpos, Real.pi_pos], hxhi⟩
    have hsinpos : 0 < Real.sin x :=
      Real.sin_pos_of_pos_of_lt_pi hxpos (by linarith [hxhi, Real.pi_pos])
    have hπx : 0 < Real.pi - x := by linarith [hxhi]
    nlinarith

/-- `f(pi/4) = 3 * pi * sqrt 2 / 8 > pi/2`: the left endpoint of the
chord bound used for Lemma ys2. -/
lemma f_pi_div_four_gt :
    Real.pi / 2 < (Real.pi - Real.pi / 4) * Real.sin (Real.pi / 4) := by
  rw [Real.sin_pi_div_four]
  have hsqrt2 : 4 < 3 * Real.sqrt 2 := by
    have hsq : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
    by_contra h
    have hle : 3 * Real.sqrt 2 ≤ 4 := le_of_not_gt h
    have hsqle : (3 * Real.sqrt 2) ^ 2 ≤ 16 := by
      nlinarith [hle, Real.sqrt_nonneg 2]
    nlinarith [hsq, hsqle]
  have hident : (Real.pi - Real.pi / 4) * (Real.sqrt 2 / 2) =
      Real.pi * (3 * Real.sqrt 2) / 8 := by
    ring
  rw [hident]
  nlinarith [hsqrt2, Real.pi_pos]

/-- Lemma ys2 (certificate-free): for `gamma >= GammaStar` with
`gamma < pi/2`, `p < (pi - gamma)^2 * sin gamma^2`.

Proof: `f(gamma) = (pi - gamma) * sin gamma` is strictly concave on
`[pi/4, pi/2]`, hence lies above the chord between `pi/4` and `pi/2`;
`f(pi/4) = 3*pi*sqrt2/8 > pi/2` and `f(pi/2) = pi/2` force
`f(gamma) > pi/2` for `gamma < pi/2`.  The threshold enters only through
`GammaStar > pi/4`. -/
lemma ys2_of_ge_gamma_star {γ : ℝ} (hγs : GammaStar ≤ γ) (hγp : γ < Real.pi / 2) :
    p < (Real.pi - γ) ^ 2 * sin γ ^ 2 := by
  let f : ℝ → ℝ := fun x => (Real.pi - x) * Real.sin x
  have hγ4 : Real.pi / 4 ≤ γ := by linarith [hγs, gamma_star_gt_pi_div_four]
  let t : ℝ := (Real.pi / 2 - γ) / (Real.pi / 2 - Real.pi / 4)
  have hden : 0 < Real.pi / 2 - Real.pi / 4 := by nlinarith [Real.pi_pos]
  have ht0 : 0 ≤ t := div_nonneg (by linarith) hden.le
  have ht1 : t ≤ 1 := by
    rw [div_le_iff₀ hden]
    nlinarith [hγ4]
  have htpos : 0 < t := div_pos (by linarith [hγp]) hden
  have hγ_eq : γ = t * (Real.pi / 4) + (1 - t) * (Real.pi / 2) := by
    dsimp [t]
    field_simp [hden.ne']
    ring
  have hconc : ConcaveOn ℝ (Set.Icc (Real.pi / 4) (Real.pi / 2)) f :=
    strictConcaveOn_f.concaveOn
  have h4mem : Real.pi / 4 ∈ Set.Icc (Real.pi / 4) (Real.pi / 2) :=
    ⟨le_rfl, by nlinarith [Real.pi_pos]⟩
  have h2mem : Real.pi / 2 ∈ Set.Icc (Real.pi / 4) (Real.pi / 2) :=
    ⟨by nlinarith [Real.pi_pos], le_rfl⟩
  have hchord : t * f (Real.pi / 4) + (1 - t) * f (Real.pi / 2) ≤
      f (t * (Real.pi / 4) + (1 - t) * (Real.pi / 2)) :=
    hconc.2 h4mem h2mem ht0 (by linarith [ht1]) (by ring)
  have hf4 : Real.pi / 2 < f (Real.pi / 4) := by
    simpa [f] using f_pi_div_four_gt
  have hf2 : f (Real.pi / 2) = Real.pi / 2 := by
    dsimp [f]
    rw [Real.sin_pi_div_two]
    ring
  have hlow : Real.pi / 2 < t * f (Real.pi / 4) + (1 - t) * f (Real.pi / 2) := by
    rw [hf2]
    nlinarith [hf4, htpos]
  have hfγ : Real.pi / 2 < f γ := by
    have hchord' : t * f (Real.pi / 4) + (1 - t) * f (Real.pi / 2) ≤ f γ := by
      rw [hγ_eq]
      exact hchord
    exact lt_of_lt_of_le hlow hchord'
  have hγpos : 0 < γ := by linarith [hγ4, Real.pi_pos]
  have hsinpos : 0 < Real.sin γ :=
    Real.sin_pos_of_pos_of_lt_pi hγpos (by linarith [hγp, Real.pi_pos])
  have hfsq : (Real.pi / 2) ^ 2 < (f γ) ^ 2 :=
    (sq_lt_sq₀ (le_of_lt Real.pi_div_two_pos)
      (le_of_lt (lt_trans Real.pi_div_two_pos hfγ))).mpr hfγ
  rw [p_eq_sq_half]
  simpa [f, mul_pow] using hfsq

/-- `Delta A gamma > 0` on the symmetry line under Lemma ys2
(`A < pi/2`, `gamma < pi/2`, `gamma >= gamma_0*`). -/
lemma Delta_pos {γ A : ℝ} (hγp : γ < Real.pi / 2) (hA0 : 0 < A)
    (hAp : A < Real.pi / 2) (hγs : GammaStar ≤ γ) : 0 < Delta A γ := by
  have hys2 : p < (Real.pi - γ) ^ 2 * sin γ ^ 2 := ys2_of_ge_gamma_star hγs hγp
  unfold Delta
  have hA2p : A ^ 2 < p := by
    rw [p_eq_sq_half]
    nlinarith [Real.pi_div_two_pos, hA0, hAp]
  have hyy2 : 0 < (Real.pi - γ) ^ 2 * sin γ ^ 2 - A ^ 2 := by
    nlinarith [hys2, hA2p]
  have hs1le : sin A ^ 2 ≤ 1 := by
    nlinarith [Real.sin_sq_add_cos_sq A, sq_nonneg (cos A)]
  have hA2s1 : A ^ 2 * sin A ^ 2 ≤ A ^ 2 := by
    nlinarith [hs1le, sq_nonneg A]
  nlinarith [hyy2, hA2s1]

/-- `Q0(gamma) >= 0` under Lemma ys2 (part of Lemma P2). -/
lemma Q0_nonneg {γ : ℝ} (hγp : γ < Real.pi / 2) (hγs : GammaStar ≤ γ) : 0 ≤ Q0 γ := by
  have hys2 : p < (Real.pi - γ) ^ 2 * sin γ ^ 2 := ys2_of_ge_gamma_star hγs hγp
  unfold Q0
  have hπy : Real.pi / 2 < Real.pi - γ := by linarith [hγp]
  have hy2p : 0 ≤ (Real.pi - γ) ^ 2 - p := by
    rw [p_eq_sq_half]
    nlinarith [Real.pi_div_two_pos]
  have hden : 0 < (Real.pi - γ) ^ 2 * sin γ ^ 2 - p := by linarith
  exact div_nonneg (mul_nonneg (sq_nonneg (sin γ)) hy2p) hden.le

/-- Lemma P2 of the source (in the stronger form valid for every real `q`):
for `0 < A < pi/2`, `gamma < pi/2` and `gamma >= gamma_0*` (which implies
the strict Lemma ys2 bound `p < y^2 * sin gamma^2`),

  `s1^2 * s2^2 * T / Delta * (1 - q^2) <= Q0(gamma)`.

Proof: cross-multiply to `E >= 0`, use `W <= W0` (from `1 - q^2 <= 1`)
and the three-term nonnegative decomposition of `E0`. -/
lemma P2 (q : ℝ) {γ A : ℝ}
    (hγp : γ < Real.pi / 2) (hA0 : 0 < A) (hAp : A < Real.pi / 2)
    (hγs : GammaStar ≤ γ) :
    sin A ^ 2 * sin γ ^ 2 * T A γ / Delta A γ * (1 - q ^ 2) ≤ Q0 γ := by
  have hys2 : p < (Real.pi - γ) ^ 2 * sin γ ^ 2 := ys2_of_ge_gamma_star hγs hγp
  have hyy : 0 < (Real.pi - γ) ^ 2 * sin γ ^ 2 - p := by linarith
  have hT : 0 < T A γ := T_pos hγp hA0 hAp
  have hΔ : 0 < Delta A γ := Delta_pos hγp hA0 hAp hγs
  have hpA : 0 ≤ p - A ^ 2 := p_sub_sq_nonneg hA0 hAp
  let C0 : ℝ := (Real.pi - γ) ^ 2 * ((Real.pi - γ) ^ 2 - p) * sin γ ^ 2
  let W : ℝ := ((Real.pi - γ) ^ 2 - p) * A ^ 2 +
      (1 - q ^ 2) * T A γ * ((Real.pi - γ) ^ 2 * sin γ ^ 2 - p)
  let W0 : ℝ := ((Real.pi - γ) ^ 2 - p) * A ^ 2 +
      T A γ * ((Real.pi - γ) ^ 2 * sin γ ^ 2 - p)
  have hdec : C0 - sin A ^ 2 * W0 =
      (Real.pi - γ) ^ 2 * (cos γ ^ 2 * (p - A ^ 2) +
        cos A ^ 2 * ((Real.pi - γ) ^ 2 * sin γ ^ 2 - p) +
        cos A ^ 2 * A ^ 2 * cos γ ^ 2) := by
    dsimp [C0, W0]
    unfold T
    rw [show sin A ^ 2 = 1 - cos A ^ 2 by nlinarith [Real.sin_sq_add_cos_sq A]]
    rw [show sin γ ^ 2 = 1 - cos γ ^ 2 by nlinarith [Real.sin_sq_add_cos_sq γ]]
    ring
  have hE0 : 0 ≤ C0 - sin A ^ 2 * W0 := by
    rw [hdec]
    have ht1 : 0 ≤ cos γ ^ 2 * (p - A ^ 2) :=
      mul_nonneg (sq_nonneg (cos γ)) hpA
    have ht2 : 0 ≤ cos A ^ 2 * ((Real.pi - γ) ^ 2 * sin γ ^ 2 - p) :=
      mul_nonneg (sq_nonneg (cos A)) hyy.le
    have ht3 : 0 ≤ cos A ^ 2 * A ^ 2 * cos γ ^ 2 :=
      mul_nonneg (mul_nonneg (sq_nonneg (cos A)) (sq_nonneg A)) (sq_nonneg (cos γ))
    have hsum : 0 ≤ cos γ ^ 2 * (p - A ^ 2) + cos A ^ 2 * ((Real.pi - γ) ^ 2 * sin γ ^ 2 - p)
        + cos A ^ 2 * A ^ 2 * cos γ ^ 2 := by
      nlinarith
    exact mul_nonneg (sq_nonneg (Real.pi - γ)) hsum
  have hWle : W ≤ W0 := by
    dsimp [W, W0]
    have h1mle : 1 - q ^ 2 ≤ 1 := by nlinarith [sq_nonneg q]
    have hprod : 0 ≤ T A γ * ((Real.pi - γ) ^ 2 * sin γ ^ 2 - p) :=
      mul_nonneg hT.le hyy.le
    nlinarith
  have hE : 0 ≤ ((Real.pi - γ) ^ 2 - p) * Delta A γ -
      sin A ^ 2 * (1 - q ^ 2) * T A γ * ((Real.pi - γ) ^ 2 * sin γ ^ 2 - p) := by
    have hEid : ((Real.pi - γ) ^ 2 - p) * Delta A γ -
          sin A ^ 2 * (1 - q ^ 2) * T A γ * ((Real.pi - γ) ^ 2 * sin γ ^ 2 - p) =
        C0 - sin A ^ 2 * W := by
      dsimp [C0, W]
      unfold Delta
      ring
    rw [hEid]
    have hEge : C0 - sin A ^ 2 * W0 ≤ C0 - sin A ^ 2 * W := by
      have hWs : sin A ^ 2 * W ≤ sin A ^ 2 * W0 :=
        mul_le_mul_of_nonneg_left hWle (sq_nonneg (sin A))
      nlinarith
    exact le_trans hE0 hEge
  have hmain : sin A ^ 2 * sin γ ^ 2 * (1 - q ^ 2) * T A γ * ((Real.pi - γ) ^ 2 * sin γ ^ 2 - p) ≤
      sin γ ^ 2 * ((Real.pi - γ) ^ 2 - p) * Delta A γ := by
    have htmp : sin A ^ 2 * (1 - q ^ 2) * T A γ * ((Real.pi - γ) ^ 2 * sin γ ^ 2 - p) ≤
        ((Real.pi - γ) ^ 2 - p) * Delta A γ := by nlinarith [hE]
    simpa [mul_assoc, mul_comm, mul_left_comm] using
      mul_le_mul_of_nonneg_right htmp (sq_nonneg (sin γ))
  unfold Q0
  rw [le_div_iff₀ hyy]
  field_simp [hΔ.ne']
  simpa [mul_assoc, mul_comm, mul_left_comm] using hmain

/-- Theorem 张力比链: on the symmetry line with
`c = arctan(q * tan gamma) / (pi - gamma)` and `gamma >= gamma_0*`,

  `rho A gamma c q <= rho0 gamma = t/(y+t) * Q0(gamma)`.

This is the product of Lemma P1 (`c/(q+c) <= t/(y+t)`) and Lemma P2
(the bracket `s1^2*s2^2*T/Delta*(1-q^2) <= Q0(gamma)`); Lemma ys2 enters
through P2. -/
theorem tension_ratio_chain {q γ A : ℝ} (hq0 : 0 < q) (hq1 : q < 1)
    (hγ0 : 0 < γ) (hγp : γ < Real.pi / 2) (hA0 : 0 < A) (hAp : A < Real.pi / 2)
    (hγs : GammaStar ≤ γ) :
    rho A γ (Real.arctan (q * Real.tan γ) / (Real.pi - γ)) q ≤ rho0 γ := by
  let c : ℝ := Real.arctan (q * Real.tan γ) / (Real.pi - γ)
  let t : ℝ := Real.tan γ
  let y : ℝ := Real.pi - γ
  have hy : 0 < y := by dsimp [y]; linarith [Real.pi_pos]
  have ht : 0 < t := by
    dsimp [t]
    exact Real.tan_pos_of_pos_of_lt_pi_div_two hγ0 hγp
  have hqc : 0 < q + c := by
    have hc0 : 0 < c := by
      dsimp [c]
      exact div_pos (Real.arctan_pos.mpr (mul_pos hq0 ht)) hy
    linarith
  have hΔ : 0 < Delta A γ := Delta_pos hγp hA0 hAp hγs
  have h1 : c / (q + c) ≤ t / (y + t) := by
    exact P1 hq0 ht hy (by rfl)
  have h2 := P2 q hγp hA0 hAp hγs
  have hb_nonneg : 0 ≤ sin A ^ 2 * sin γ ^ 2 * T A γ / Delta A γ * (1 - q ^ 2) := by
    have hT : 0 ≤ T A γ := (T_pos hγp hA0 hAp).le
    have h1m : 0 ≤ 1 - q ^ 2 := one_sub_sq_nonneg hq0 hq1
    exact mul_nonneg
      (div_nonneg (mul_nonneg (mul_nonneg (sq_nonneg (sin A)) (sq_nonneg (sin γ))) hT) hΔ.le) h1m
  have hb2 : 0 ≤ t / (y + t) := div_nonneg ht.le (by linarith)
  have hfac : rho A γ c q =
      (c / (q + c)) * (sin A ^ 2 * sin γ ^ 2 * T A γ / Delta A γ * (1 - q ^ 2)) := by
    unfold rho
    field_simp [hqc.ne', hΔ.ne']
    try ring
  rw [hfac]
  exact mul_le_mul h1 h2 hb_nonneg hb2


end
end SymlineTensionRatio
end SL
