import SL.Krein.IntegralConstruction
import Mathlib.MeasureTheory.Integral.IntervalIntegral.AbsolutelyContinuousFun
import Mathlib.Analysis.Calculus.ContDiff.Deriv

/-!
# Weak derivative identities for all integral representatives

Every real continuous linear coordinate of the complex representative is
absolutely continuous. Its weak derivatives satisfy the integration-by-parts
identity against arbitrary real C1 tests with zero endpoint values. Applying
the coordinate to real and imaginary parts gives the usual complex weak
derivative identities. The converse characterization of a pre-existing weak
H2 quotient is not asserted here.
-/

namespace SL.Krein

open MeasureTheory Set Filter
open scoped Topology

noncomputable section

theorem ac_of_integral_reconstruction (F Q : ℝ → ℝ)
    (HQ : IntervalIntegrable Q volume (-1) 1)
    (HF : ∀ X ∈ Icc (-1) 1, F X = F (-1) + ∫ T in (-1 : ℝ)..X, Q T) :
    AbsolutelyContinuousOnInterval F (-1) 1 := by
  have HC := HQ.absolutelyContinuousOnInterval_intervalIntegral
    (by simp : (-1 : ℝ) ∈ uIcc (-1) 1)
  rw [absolutelyContinuousOnInterval_iff] at HC ⊢
  intro Eps HEps
  obtain ⟨Delta, HD, HH⟩ := HC Eps HEps
  refine ⟨Delta, HD, ?_⟩
  intro E HE HL
  have HS := HH E HE HL
  convert HS using 1
  apply Finset.sum_congr rfl
  intro I HI
  have HM := HE.1 I HI
  rw [uIcc_of_le (by norm_num : (-1 : ℝ) ≤ 1)] at HM
  rw [HF _ HM.1, HF _ HM.2, dist_add_left]

theorem IntegralRepresentative.value_coord_ac (R : IntegralRepresentative) (Q : ℂ →L[ℝ] ℝ) :
    AbsolutelyContinuousOnInterval (fun X => Q (R.Value X)) (-1) 1 := by
  have HI : IntervalIntegrable R.First volume (-1) 1 :=
    R.FirstContinuous.intervalIntegrable_of_Icc (by norm_num)
  apply ac_of_integral_reconstruction _ _
    ⟨Q.integrable_comp HI.1, Q.integrable_comp HI.2⟩
  intro X HX
  rw [R.ValueIntegral X HX, map_add]
  congr 1
  exact (Q.intervalIntegral_comp_comm (HI.mono_set (by
    rw [uIcc_of_le (by norm_num : (-1 : ℝ) ≤ 1), uIcc_of_le HX.1]
    exact Icc_subset_Icc le_rfl HX.2))).symm

theorem IntegralRepresentative.first_coord_ac (R : IntegralRepresentative) (Q : ℂ →L[ℝ] ℝ) :
    AbsolutelyContinuousOnInterval (fun X => Q (R.First X)) (-1) 1 := by
  have HI := SL.Analysis.mem_l2_interval_integrable (by norm_num) R.SecondMemLp
  apply ac_of_integral_reconstruction _ _
    ⟨Q.integrable_comp HI.1, Q.integrable_comp HI.2⟩
  intro X HX
  rw [R.FirstIntegral X HX, map_add]
  congr 1
  exact (Q.intervalIntegral_comp_comm (HI.mono_set (by
    rw [uIcc_of_le (by norm_num : (-1 : ℝ) ≤ 1), uIcc_of_le HX.1]
    exact Icc_subset_Icc le_rfl HX.2))).symm

theorem IntegralRepresentative.value_coord_deriv_ae (R : IntegralRepresentative)
    (Q : ℂ →L[ℝ] ℝ) :
    deriv (fun X => Q (R.Value X)) =ᵐ[intervalMeasure] (fun X => Q (R.First X)) := by
  filter_upwards [ae_restrict_mem measurableSet_Ioo] with X HX
  exact (Q.hasFDerivAt.comp_hasDerivAt X (R.value_has_deriv HX)).deriv

theorem IntegralRepresentative.first_coord_deriv_ae (R : IntegralRepresentative)
    (Q : ℂ →L[ℝ] ℝ) :
    deriv (fun X => Q (R.First X)) =ᵐ[intervalMeasure] (fun X => Q (R.Second X)) := by
  filter_upwards [R.first_has_deriv_ae] with X HX
  exact (Q.hasFDerivAt.comp_hasDerivAt X HX).deriv

theorem coordinate_weak_identity (F G : ℝ → ℝ)
    (HF : AbsolutelyContinuousOnInterval F (-1) 1)
    (HD : deriv F =ᵐ[intervalMeasure] G)
    (Phi : ℝ → ℝ) (HPhi : ContDiff ℝ 1 Phi)
    (HM : Phi (-1) = 0) (HP : Phi 1 = 0) :
    (∫ X in (-1 : ℝ)..1, F X * deriv Phi X) =
      -(∫ X in (-1 : ℝ)..1, G X * Phi X) := by
  have HC : AbsolutelyContinuousOnInterval Phi (-1) 1 :=
    HPhi.contDiffOn.absolutelyContinuousOnInterval
  have HB := HF.integral_mul_deriv_eq_deriv_mul HC
  rw [HM, HP, mul_zero, mul_zero, sub_self, zero_sub] at HB
  rw [HB]
  congr 1
  simp_rw [intervalIntegral.integral_of_le (by norm_num : (-1 : ℝ) ≤ 1)]
  apply integral_congr_ae
  have HD' : deriv F =ᵐ[volume.restrict (Ioc (-1) 1)] G := by
    simpa [intervalMeasure, SL.Analysis.interval_measure, restrict_Ioo_eq_restrict_Ioc] using HD
  filter_upwards [HD'] with X HX
  rw [HX]

theorem IntegralRepresentative.weak_derivative_pair (R : IntegralRepresentative)
    (Q : ℂ →L[ℝ] ℝ) (Phi : ℝ → ℝ) (HPhi : ContDiff ℝ 1 Phi)
    (HM : Phi (-1) = 0) (HP : Phi 1 = 0) :
    (∫ X in (-1 : ℝ)..1, Q (R.Value X) * deriv Phi X) =
      -(∫ X in (-1 : ℝ)..1, Q (R.First X) * Phi X) ∧
    (∫ X in (-1 : ℝ)..1, Q (R.First X) * deriv Phi X) =
      -(∫ X in (-1 : ℝ)..1, Q (R.Second X) * Phi X) := by
  exact ⟨coordinate_weak_identity _ _ (R.value_coord_ac Q)
      (R.value_coord_deriv_ae Q) Phi HPhi HM HP,
    coordinate_weak_identity _ _ (R.first_coord_ac Q)
      (R.first_coord_deriv_ae Q) Phi HPhi HM HP⟩

end

end SL.Krein
