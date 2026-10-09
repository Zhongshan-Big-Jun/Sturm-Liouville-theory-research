import SL.Weighted.Model
import SL.Analysis.IntervalL2
import Mathlib.MeasureTheory.Integral.Bochner.ContinuousLinearMap

noncomputable section

namespace SL.Weighted

open MeasureTheory Set

theorem norm_squared_toLp {Mu : Measure ℝ} {Value : ℝ → ℂ} (Valid : MemLp Value 2 Mu) :
    ‖Valid.toLp Value‖ ^ 2 = ∫ x, ‖Value x‖ ^ 2 ∂Mu := by
  rw [@norm_sq_eq_re_inner ℂ, L2.inner_def, ← integral_re (L2.integrable_inner _ _)]
  apply integral_congr_ae
  filter_upwards [Valid.coeFn_toLp] with x Same
  simp only [Same, inner_self_eq_norm_sq_to_K, RCLike.re_ofReal_pow]

theorem weighted_measure_le {Length : ℝ} (Rho : Density Length) :
    weighted_measure Rho ≤ ENNReal.ofReal Rho.upper • interval_measure Length := by
  calc
    weighted_measure Rho ≤ (interval_measure Length).withDensity (fun _ => ENNReal.ofReal Rho.upper) := by
      apply withDensity_mono
      filter_upwards [Rho.bounds] with x Bound
      exact ENNReal.ofReal_le_ofReal Bound.2
    _ = _ := withDensity_const _

theorem continuous_mem_weighted_l2 {Length : ℝ} (Rho : Density Length)
    {Value : ℝ → ℂ} (Regular : ContinuousOn Value (Icc 0 Length)) :
    MemLp Value 2 (weighted_measure Rho) := by
  exact (SL.Analysis.continuous_mem_l2 Regular).of_measure_le_smul
    ENNReal.ofReal_ne_top (weighted_measure_le Rho)

def weighted_vector {Length : ℝ} (Rho : Density Length) (Value : ℝ → ℂ)
    (Regular : ContinuousOn Value (Icc 0 Length)) : WeightedL2 Rho :=
  (continuous_mem_weighted_l2 Rho Regular).toLp Value

theorem weighted_norm_eq_mass (Length : ℝ) (LengthPos : 0 < Length)
    (Rho : Density Length) (Value : ℝ → ℂ) (Regular : ContinuousOn Value (Icc 0 Length)) :
    ‖weighted_vector Rho Value Regular‖ ^ 2 = mass Length Rho.value Value := by
  unfold weighted_vector
  rw [norm_squared_toLp]
  have DensityIntegral : (∫ x, ‖Value x‖ ^ 2 ∂weighted_measure Rho) =
      ∫ x, Rho.value x * ‖Value x‖ ^ 2 ∂interval_measure Length := by
    unfold weighted_measure
    change (∫ x, ‖Value x‖ ^ 2 ∂(interval_measure Length).withDensity
      (fun x => (Real.toNNReal (Rho.value x) : ENNReal))) = _
    rw [integral_withDensity_eq_integral_smul Rho.measurable.real_toNNReal]
    apply integral_congr_ae
    filter_upwards [Rho.bounds] with x Bound
    simp only [NNReal.smul_def, smul_eq_mul,
      Real.coe_toNNReal _ (le_trans Rho.lower_pos.le Bound.1)]
  rw [DensityIntegral]
  unfold mass
  rw [intervalIntegral.integral_of_le LengthPos.le]
  simp only [interval_measure, restrict_Ioo_eq_restrict_Ioc]

end SL.Weighted
