import SL.Analysis.IntervalL2
import Mathlib.MeasureTheory.Integral.IntervalIntegral.LebesgueDifferentiationThm
import Mathlib.Analysis.Calculus.Deriv.Mul

/-!
# Krein's complex integral Sobolev representatives

`IntegralRepresentative` admits L2 second derivatives, including discontinuous
ones. It is not a C2 subdomain. Its two integral reconstruction identities are
proved to give the genuine first derivative and a.e. second derivative below.
The equivalence with a separately defined distributional H2 space, closedness,
self-adjointness, positivity and power domains are separate remaining targets.
-/

open MeasureTheory Set Filter
open scoped Topology

namespace SL.Analysis

theorem ae_has_deriv_at_integral {A B : ℝ} (HAB : A < B) {F : ℝ → ℂ}
    (HF : IntervalIntegrable F volume A B) :
    ∀ᵐ x ∂interval_measure A B,
      HasDerivAt (fun y => ∫ t in A..y, F t) (F x) x := by
  have HRe : IntervalIntegrable (fun x => (F x).re) volume A B :=
    ⟨Complex.reCLM.integrable_comp HF.1, Complex.reCLM.integrable_comp HF.2⟩
  have HIm : IntervalIntegrable (fun x => (F x).im) volume A B :=
    ⟨Complex.imCLM.integrable_comp HF.1, Complex.imCLM.integrable_comp HF.2⟩
  have HReAE := ae_restrict_of_ae (s := Ioo A B) HRe.ae_hasDerivAt_integral
  have HImAE := ae_restrict_of_ae (s := Ioo A B) HIm.ae_hasDerivAt_integral
  filter_upwards [HReAE, HImAE, ae_restrict_mem measurableSet_Ioo] with x HxRe HxIm Hx
  have HxCC : x ∈ uIcc A B := by rw [uIcc_of_le HAB.le]; exact Ioo_subset_Icc_self Hx
  have HA : A ∈ uIcc A B := by simp [uIcc_of_le HAB.le, HAB.le]
  have HD := ((HxRe HxCC A HA).ofReal_comp).add
    (((HxIm HxCC A HA).ofReal_comp).mul_const Complex.I)
  have HC : HasDerivAt
      (fun y => (↑(∫ t in A..y, (F t).re) : ℂ) +
        ↑(∫ t in A..y, (F t).im) * Complex.I) (F x) x := by
    simpa only [Pi.add_apply, Complex.re_add_im] using! HD
  apply HC.congr_of_eventuallyEq
  filter_upwards [Ioo_mem_nhds Hx.1 Hx.2] with y Hy
  have HI : IntervalIntegrable F volume A y := HF.mono_set <| by
    rw [uIcc_of_le HAB.le, uIcc_of_le Hy.1.le]
    exact Icc_subset_Icc le_rfl Hy.2.le
  have HR : (∫ t in A..y, (F t).re) = (∫ t in A..y, F t).re := by
    simpa only [Complex.reCLM_apply] using! Complex.reCLM.intervalIntegral_comp_comm HI
  have HM : (∫ t in A..y, (F t).im) = (∫ t in A..y, F t).im := by
    simpa only [Complex.imCLM_apply] using! Complex.imCLM.intervalIntegral_comp_comm HI
  rw [HR, HM, Complex.re_add_im]

end SL.Analysis

namespace SL.Krein

noncomputable section

abbrev intervalMeasure := SL.Analysis.interval_measure (-1) 1
abbrev L2 := SL.Analysis.ComplexL2 (-1) 1

structure IntegralRepresentative where
  Value : ℝ → ℂ
  First : ℝ → ℂ
  Second : ℝ → ℂ
  ValueContinuous : ContinuousOn Value (Icc (-1) 1)
  FirstContinuous : ContinuousOn First (Icc (-1) 1)
  SecondMemLp : MemLp Second 2 intervalMeasure
  ValueIntegral : ∀ x ∈ Icc (-1) 1,
    Value x = Value (-1) + ∫ t in (-1 : ℝ)..x, First t
  FirstIntegral : ∀ x ∈ Icc (-1) 1,
    First x = First (-1) + ∫ t in (-1 : ℝ)..x, Second t

def IntegralRepresentative.to_L2 (R : IntegralRepresentative) : L2 :=
  SL.Analysis.to_L2 R.Value (SL.Analysis.continuous_mem_l2 R.ValueContinuous)

theorem IntegralRepresentative.value_has_deriv (R : IntegralRepresentative)
    {x : ℝ} (HX : x ∈ Ioo (-1) 1) : HasDerivAt R.Value (R.First x) x := by
  have HI : IntervalIntegrable R.First volume (-1) x :=
    (R.FirstContinuous.mono <| Icc_subset_Icc le_rfl HX.2.le).intervalIntegrable_of_Icc HX.1.le
  have HOpen := R.FirstContinuous.mono Ioo_subset_Icc_self
  have HD := intervalIntegral.integral_hasDerivAt_right HI
    (HOpen.stronglyMeasurableAtFilter isOpen_Ioo x HX)
    (HOpen.continuousAt <| isOpen_Ioo.mem_nhds HX)
  have HC := HD.const_add (R.Value (-1))
  apply HC.congr_of_eventuallyEq
  filter_upwards [Ioo_mem_nhds HX.1 HX.2] with y HY
  exact R.ValueIntegral y (Ioo_subset_Icc_self HY)

theorem IntegralRepresentative.first_has_deriv_ae (R : IntegralRepresentative) :
    ∀ᵐ x ∂intervalMeasure, HasDerivAt R.First (R.Second x) x := by
  have HI := SL.Analysis.mem_l2_interval_integrable (by norm_num : (-1 : ℝ) ≤ 1) R.SecondMemLp
  have HD := SL.Analysis.ae_has_deriv_at_integral (by norm_num : (-1 : ℝ) < 1) HI
  filter_upwards [HD, ae_restrict_mem measurableSet_Ioo] with x Hx HX
  apply (Hx.const_add (R.First (-1))).congr_of_eventuallyEq
  filter_upwards [Ioo_mem_nhds HX.1 HX.2] with y HY
  exact R.FirstIntegral y (Ioo_subset_Icc_self HY)

theorem IntegralRepresentative.value_eq_on (R S : IntegralRepresentative)
    (HRS : R.to_L2 = S.to_L2) : EqOn R.Value S.Value (Icc (-1) 1) :=
  SL.Analysis.continuous_eq_on_of_L2_eq (by norm_num) R.ValueContinuous S.ValueContinuous HRS

theorem IntegralRepresentative.first_eq_on (R S : IntegralRepresentative)
    (HRS : R.to_L2 = S.to_L2) : EqOn R.First S.First (Icc (-1) 1) := by
  have HV := R.value_eq_on S HRS
  have HOpen : EqOn R.First S.First (Ioo (-1) 1) := by
    intro x HX
    have HE : R.Value =ᶠ[𝓝 x] S.Value := by
      filter_upwards [Ioo_mem_nhds HX.1 HX.2] with y HY
      exact HV (Ioo_subset_Icc_self HY)
    exact (R.value_has_deriv HX).unique <|
      (S.value_has_deriv HX).congr_of_eventuallyEq HE
  exact HOpen.of_subset_closure R.FirstContinuous S.FirstContinuous Ioo_subset_Icc_self
    (by rw [closure_Ioo (by norm_num : (-1 : ℝ) ≠ 1)])

theorem IntegralRepresentative.second_eq_ae (R S : IntegralRepresentative)
    (HRS : R.to_L2 = S.to_L2) : R.Second =ᵐ[intervalMeasure] S.Second := by
  have HF := R.first_eq_on S HRS
  filter_upwards [R.first_has_deriv_ae, S.first_has_deriv_ae,
    ae_restrict_mem measurableSet_Ioo] with x HR HS HX
  have HE : R.First =ᶠ[𝓝 x] S.First := by
    filter_upwards [Ioo_mem_nhds HX.1 HX.2] with y HY
    exact HF (Ioo_subset_Icc_self HY)
  exact HR.unique (HS.congr_of_eventuallyEq HE)

def boundary (R : IntegralRepresentative) : Prop :=
  R.First 1 = (R.Value 1 - R.Value (-1)) / 2 ∧
  R.First (-1) = (R.Value 1 - R.Value (-1)) / 2

theorem boundary_invariant (R S : IntegralRepresentative) (HRS : R.to_L2 = S.to_L2) :
    boundary R ↔ boundary S := by
  have HV := R.value_eq_on S HRS
  have HF := R.first_eq_on S HRS
  have HM : (-1 : ℝ) ∈ Icc (-1) 1 := by norm_num
  have HP : (1 : ℝ) ∈ Icc (-1) 1 := by norm_num
  simp only [boundary, HV HM, HV HP, HF HM, HF HP]

def domain : Set L2 := {F | ∃ R : IntegralRepresentative, R.to_L2 = F ∧ boundary R}

def IntegralRepresentative.action (R : IntegralRepresentative) (C : ℝ) : L2 :=
  SL.Analysis.to_L2 (fun x => -R.Second x + (C : ℂ) * R.Value x)
    (R.SecondMemLp.neg.add <|
      (SL.Analysis.continuous_mem_l2 R.ValueContinuous).const_mul (C : ℂ))

theorem IntegralRepresentative.action_invariant (R S : IntegralRepresentative)
    (HRS : R.to_L2 = S.to_L2) (C : ℝ) : R.action C = S.action C := by
  apply SL.Analysis.to_L2_congr
  have HV := SL.Analysis.to_L2_eq_iff_ae _ _ |>.1 HRS
  filter_upwards [R.second_eq_ae S HRS, HV] with x HS HF
  simp only [HS, HF]

def operator (C : ℝ) (F : domain) : L2 :=
  F.property.choose.action C

theorem operator_eq_action (C : ℝ) (F : domain) (R : IntegralRepresentative)
    (HR : R.to_L2 = F.val) : operator C F = R.action C := by
  apply IntegralRepresentative.action_invariant
  exact F.property.choose_spec.1.trans HR.symm

end

end SL.Krein
