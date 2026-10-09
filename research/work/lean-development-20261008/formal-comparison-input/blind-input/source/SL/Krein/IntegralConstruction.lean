import SL.Krein.IntegralDomain

   
                                                                           

                                                                        
                                                                     
                                                                              
                     
  

namespace SL.Krein

open MeasureTheory Set Filter

noncomputable section

def first_primitive (F : ℝ → ℂ) (A : ℂ) (X : ℝ) : ℂ := A + ∫ T in (-1 : ℝ)..X, F T

theorem first_primitive_continuous (F : ℝ → ℂ) (HF : MemLp F 2 intervalMeasure) (A : ℂ) :
    ContinuousOn (first_primitive F A) (Icc (-1) 1) := by
  have HI := SL.Analysis.mem_l2_interval_integrable (by norm_num) HF
  have HC := intervalIntegral.continuousOn_primitive_interval' HI
    (by simp : (-1 : ℝ) ∈ uIcc (-1) 1)
  have HE : uIcc (-1 : ℝ) 1 = Icc (-1) 1 := uIcc_of_le (by norm_num)
  unfold first_primitive
  simpa only [HE] using! HC.const_add A

def from_l2_second (F : ℝ → ℂ) (HF : MemLp F 2 intervalMeasure) (A B : ℂ) :
    IntegralRepresentative where
  Value X := B + ∫ T in (-1 : ℝ)..X, first_primitive F A T
  First := first_primitive F A
  Second := F
  ValueContinuous := by
    have HC := first_primitive_continuous F HF A
    have HI : IntervalIntegrable (first_primitive F A) volume (-1) 1 :=
      HC.intervalIntegrable_of_Icc (by norm_num : (-1 : ℝ) ≤ 1)
    have HV := intervalIntegral.continuousOn_primitive_interval' HI
      (by simp : (-1 : ℝ) ∈ uIcc (-1) 1)
    have HE : uIcc (-1 : ℝ) 1 = Icc (-1) 1 := uIcc_of_le (by norm_num)
    simpa only [HE] using! HV.const_add B
  FirstContinuous := first_primitive_continuous F HF A
  SecondMemLp := HF
  ValueIntegral := by
    intro X HX
    simp
  FirstIntegral := by
    intro X HX
    simp [first_primitive]

theorem from_l2_second_initial (F : ℝ → ℂ) (HF : MemLp F 2 intervalMeasure) (A B : ℂ) :
    (from_l2_second F HF A B).Value (-1) = B ∧
    (from_l2_second F HF A B).First (-1) = A ∧
    (from_l2_second F HF A B).Second = F := by
  simp [from_l2_second, first_primitive]

theorem representative_parameterization (R : IntegralRepresentative) :
    EqOn (from_l2_second R.Second R.SecondMemLp (R.First (-1)) (R.Value (-1))).Value
      R.Value (Icc (-1) 1) ∧
    EqOn (from_l2_second R.Second R.SecondMemLp (R.First (-1)) (R.Value (-1))).First
      R.First (Icc (-1) 1) := by
  have HF : EqOn (first_primitive R.Second (R.First (-1))) R.First (Icc (-1) 1) := by
    intro X HX
    exact (R.FirstIntegral X HX).symm
  refine ⟨?_, HF⟩
  intro X HX
  change R.Value (-1) + (∫ T in (-1 : ℝ)..X, first_primitive R.Second (R.First (-1)) T) = R.Value X
  rw [R.ValueIntegral X HX]
  congr 1
  apply intervalIntegral.integral_congr
  intro T HT
  apply HF
  rw [uIcc_of_le HX.1] at HT
  exact ⟨HT.1, HT.2.trans HX.2⟩

end

end SL.Krein
