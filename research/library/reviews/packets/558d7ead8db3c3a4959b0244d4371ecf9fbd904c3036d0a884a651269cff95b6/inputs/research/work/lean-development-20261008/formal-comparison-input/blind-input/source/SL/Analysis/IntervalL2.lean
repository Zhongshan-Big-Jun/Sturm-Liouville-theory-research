import Mathlib.MeasureTheory.Function.L2Space
import Mathlib.MeasureTheory.Measure.OpenPos
import Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus
import Mathlib.Analysis.Complex.RealDeriv

   
                                                                        

                                                                              
                                                                           
                                                          
  

namespace SL.Analysis

open MeasureTheory Set Filter
open scoped Topology

noncomputable section

def interval_measure (A B : ℝ) : Measure ℝ := volume.restrict (Ioo A B)

abbrev ComplexL2 (A B : ℝ) := Lp ℂ 2 (interval_measure A B)

instance interval_measure_finite (A B : ℝ) : IsFiniteMeasure (interval_measure A B) := by
  dsimp [interval_measure]
  infer_instance

theorem continuous_mem_l2 {A B : ℝ} {F : ℝ → ℂ}
  (HF : ContinuousOn F (Icc A B)) : MemLp F 2 (interval_measure A B) := by
  apply (memLp_two_iff_integrable_sq_norm
    ((HF.mono Ioo_subset_Icc_self).aestronglyMeasurable measurableSet_Ioo)).2
  exact ((HF.norm.pow 2).integrableOn_Icc).mono_set Ioo_subset_Icc_self

def to_L2 {A B : ℝ} (F : ℝ → ℂ) (HF : MemLp F 2 (interval_measure A B)) :
  ComplexL2 A B := HF.toLp F

theorem to_L2_eq_iff_ae {A B : ℝ} {F G : ℝ → ℂ}
  (HF : MemLp F 2 (interval_measure A B))
  (HG : MemLp G 2 (interval_measure A B)) :
  to_L2 F HF = to_L2 G HG ↔ F =ᵐ[interval_measure A B] G :=
  MemLp.toLp_eq_toLp_iff HF HG

theorem to_L2_congr {A B : ℝ} {F G : ℝ → ℂ}
  (HF : MemLp F 2 (interval_measure A B))
  (HG : MemLp G 2 (interval_measure A B))
  (HFG : F =ᵐ[interval_measure A B] G) : to_L2 F HF = to_L2 G HG :=
  (to_L2_eq_iff_ae HF HG).2 HFG

theorem continuous_eq_on_of_ae_eq {A B : ℝ} (HAB : A < B) {F G : ℝ → ℂ}
  (HF : ContinuousOn F (Icc A B)) (HG : ContinuousOn G (Icc A B))
  (HFG : F =ᵐ[interval_measure A B] G) : EqOn F G (Icc A B) := by
  have HOpen : EqOn F G (Ioo A B) :=
    Measure.eqOn_open_of_ae_eq HFG isOpen_Ioo
      (HF.mono Ioo_subset_Icc_self) (HG.mono Ioo_subset_Icc_self)
  exact HOpen.of_subset_closure HF HG Ioo_subset_Icc_self
    (by rw [closure_Ioo HAB.ne])

theorem continuous_eq_on_of_L2_eq {A B : ℝ} (HAB : A < B) {F G : ℝ → ℂ}
  (HF : ContinuousOn F (Icc A B)) (HG : ContinuousOn G (Icc A B))
  (HFG : to_L2 F (continuous_mem_l2 HF) = to_L2 G (continuous_mem_l2 HG)) :
  EqOn F G (Icc A B) :=
  continuous_eq_on_of_ae_eq HAB HF HG (to_L2_eq_iff_ae _ _ |>.1 HFG)

theorem mem_l2_interval_integrable {A B : ℝ} (HAB : A ≤ B) {F : ℝ → ℂ}
  (HF : MemLp F 2 (interval_measure A B)) : IntervalIntegrable F volume A B := by
  have HI : Integrable F (interval_measure A B) := HF.integrable (by norm_num)
  apply intervalIntegrable_iff_integrableOn_Ioc_of_le HAB |>.2
  simpa [interval_measure, IntegrableOn, restrict_Ioo_eq_restrict_Ioc] using HI

end

end SL.Analysis
