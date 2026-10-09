import SL.Krein.PolynomialBridge
import Mathlib.MeasureTheory.Integral.IntervalIntegral.IntegrationByParts

   
                                                     

                                                                              
                                                                             
                                                                                
                                                                   
  

namespace SL.Krein

open MeasureTheory Set Filter Polynomial

noncomputable section

def first_linear_inner (F G : L2) : ℂ := inner ℂ G F

theorem first_linear_inner_to_L2 (F G : ℝ → ℂ)
    (HF : MemLp F 2 intervalMeasure) (HG : MemLp G 2 intervalMeasure) :
    first_linear_inner (SL.Analysis.to_L2 F HF) (SL.Analysis.to_L2 G HG) =
    ∫ X, F X * star (G X) ∂intervalMeasure := by
  unfold first_linear_inner
  rw [MeasureTheory.L2.inner_def]
  apply integral_congr_ae
  filter_upwards [MemLp.coeFn_toLp HF, MemLp.coeFn_toLp HG] with X HFX HGX
  simp only [SL.Analysis.to_L2] at *
  rw [HFX, HGX]
  simp

theorem polynomial_inner_integral (P Q : Polynomial ℝ) :
    first_linear_inner (polynomial_L2 P) (polynomial_L2 Q) =
    ((∫ X in (-1 : ℝ)..1, P.eval X * Q.eval X : ℝ) : ℂ) := by
  unfold polynomial_L2 IntegralRepresentative.to_L2
  rw [first_linear_inner_to_L2]
  simp only [polynomial_rep, Complex.star_def, Complex.conj_ofReal, ← Complex.ofReal_mul]
  rw [integral_complex_ofReal]
  congr 1
  rw [intervalIntegral.integral_of_le (by norm_num : (-1 : ℝ) ≤ 1)]
  simp [intervalMeasure, SL.Analysis.interval_measure, restrict_Ioo_eq_restrict_Ioc]

theorem polynomial_green_identity (P : Polynomial ℝ) (HP : AuditRound5.residues P = 0) (C : ℝ) :
    (∫ X in (-1 : ℝ)..1, (-P.derivative.derivative.eval X + C * P.eval X) * P.eval X) =
    (∫ X in (-1 : ℝ)..1, (P.derivative.eval X) ^ 2) +
      C * (∫ X in (-1 : ℝ)..1, (P.eval X) ^ 2) - (P.eval 1 - P.eval (-1)) ^ 2 / 2 := by
  have HBoundary : P.derivative.eval 1 = (P.eval 1 - P.eval (-1)) / 2 ∧
      P.derivative.eval (-1) = (P.eval 1 - P.eval (-1)) / 2 := by
    simpa [AuditRound5.residues_apply, Prod.mk_eq_zero, sub_eq_zero] using HP
  have HD := intervalIntegral.integral_deriv_mul_eq_sub
    (u := fun X => P.derivative.eval X) (v := fun X => P.eval X)
    (fun X _ => P.derivative.hasDerivAt X) (fun X _ => P.hasDerivAt X)
    (P.derivative.derivative.differentiable.continuous.intervalIntegrable (-1) 1)
    (P.derivative.differentiable.continuous.intervalIntegrable (-1) 1)
  have HSecond : IntervalIntegrable (fun X => P.derivative.derivative.eval X * P.eval X)
      volume (-1) 1 :=
    (P.derivative.derivative.differentiable.continuous.mul P.differentiable.continuous).intervalIntegrable _ _
  have HFirst : IntervalIntegrable (fun X => (P.derivative.eval X) ^ 2) volume (-1) 1 :=
    (P.derivative.differentiable.continuous.pow 2).intervalIntegrable _ _
  have HValue : IntervalIntegrable (fun X => (P.eval X) ^ 2) volume (-1) 1 :=
    (P.differentiable.continuous.pow 2).intervalIntegrable _ _
  have HParts : (∫ X in (-1 : ℝ)..1, P.derivative.derivative.eval X * P.eval X) +
      (∫ X in (-1 : ℝ)..1, (P.derivative.eval X) ^ 2) =
      (P.eval 1 - P.eval (-1)) ^ 2 / 2 := by
    rw [intervalIntegral.integral_add HSecond (by simpa [pow_two] using HFirst)] at HD
    rw [HBoundary.1, HBoundary.2] at HD
    have HB : (P.eval 1 - P.eval (-1)) / 2 * P.eval 1 -
        (P.eval 1 - P.eval (-1)) / 2 * P.eval (-1) =
        (P.eval 1 - P.eval (-1)) ^ 2 / 2 := by ring
    rw [HB] at HD
    simpa only [pow_two] using HD
  calc
    _ = -(∫ X in (-1 : ℝ)..1, P.derivative.derivative.eval X * P.eval X) +
        C * (∫ X in (-1 : ℝ)..1, (P.eval X) ^ 2) := by
      calc
        _ = ∫ X in (-1 : ℝ)..1,
            -(P.derivative.derivative.eval X * P.eval X) + C * (P.eval X) ^ 2 := by
          apply intervalIntegral.integral_congr
          intro X HX
          ring
        _ = _ := by
          simpa only [Pi.neg_apply, intervalIntegral.integral_neg,
            intervalIntegral.integral_const_mul] using!
            intervalIntegral.integral_add HSecond.neg (HValue.const_mul C)
    _ = _ := by linarith [HParts]

theorem operator_polynomial_energy (P : Polynomial ℝ) (HP : AuditRound5.residues P = 0) (C : ℝ) :
    first_linear_inner (operator C (polynomial_domain P HP)) (polynomial_L2 P) =
    (((∫ X in (-1 : ℝ)..1, (P.derivative.eval X) ^ 2) +
      C * (∫ X in (-1 : ℝ)..1, (P.eval X) ^ 2) - (P.eval 1 - P.eval (-1)) ^ 2 / 2 : ℝ) : ℂ) := by
  rw [operator_on_polynomial, polynomial_inner_integral]
  have HE := polynomial_green_identity P HP C
  simpa [Polynomial.eval_add, Polynomial.eval_neg, Polynomial.eval_mul, Polynomial.eval_C] using
    congrArg (fun X : ℝ => (X : ℂ)) HE

end

end SL.Krein
