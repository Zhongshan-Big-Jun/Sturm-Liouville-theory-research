import SL.Krein.IntegralDomain
import SL.AuditRound5
import Mathlib.Analysis.Calculus.Deriv.Polynomial

   
                                                              

                                                                           
                                                                             
                                                                            
                                                                            
  

namespace SL.Krein

open MeasureTheory Set Filter Polynomial

noncomputable section

def polynomial_rep (P : Polynomial ℝ) : IntegralRepresentative where
  Value X := ((P.eval X : ℝ) : ℂ)
  First X := ((P.derivative.eval X : ℝ) : ℂ)
  Second X := ((P.derivative.derivative.eval X : ℝ) : ℂ)
  ValueContinuous := (Complex.continuous_ofReal.comp P.differentiable.continuous).continuousOn
  FirstContinuous :=
    (Complex.continuous_ofReal.comp P.derivative.differentiable.continuous).continuousOn
  SecondMemLp := SL.Analysis.continuous_mem_l2
    (Complex.continuous_ofReal.comp P.derivative.derivative.differentiable.continuous).continuousOn
  ValueIntegral := by
    intro X HX
    have HI : IntervalIntegrable (fun T => ((P.derivative.eval T : ℝ) : ℂ)) volume (-1) X :=
      (Complex.continuous_ofReal.comp P.derivative.differentiable.continuous).intervalIntegrable _ _
    rw [intervalIntegral.integral_eq_sub_of_hasDerivAt
      (fun T _ => (P.hasDerivAt T).ofReal_comp) HI]
    abel
  FirstIntegral := by
    intro X HX
    have HI : IntervalIntegrable (fun T => ((P.derivative.derivative.eval T : ℝ) : ℂ)) volume (-1) X :=
      (Complex.continuous_ofReal.comp P.derivative.derivative.differentiable.continuous).intervalIntegrable _ _
    rw [intervalIntegral.integral_eq_sub_of_hasDerivAt
      (fun T _ => (P.derivative.hasDerivAt T).ofReal_comp) HI]
    abel

def polynomial_L2 (P : Polynomial ℝ) : L2 := (polynomial_rep P).to_L2

theorem polynomial_boundary_iff (P : Polynomial ℝ) :
    boundary (polynomial_rep P) ↔ AuditRound5.residues P = 0 := by
  rw [AuditRound5.residues_apply, Prod.mk_eq_zero]
  simp only [boundary, polynomial_rep, Complex.ofReal_sub, Complex.ofReal_div,
    Complex.ofReal_ofNat, ← Complex.ofReal_inj, sub_eq_zero]

theorem polynomial_mem_domain (P : Polynomial ℝ) (HP : AuditRound5.residues P = 0) :
    polynomial_L2 P ∈ domain :=
  ⟨polynomial_rep P, rfl, (polynomial_boundary_iff P).2 HP⟩

def polynomial_domain (P : Polynomial ℝ) (HP : AuditRound5.residues P = 0) : domain :=
  ⟨polynomial_L2 P, polynomial_mem_domain P HP⟩

theorem polynomial_rep_action (P : Polynomial ℝ) (C : ℝ) :
    (polynomial_rep P).action C =
    polynomial_L2 (-P.derivative.derivative + Polynomial.C C * P) := by
  unfold polynomial_L2 IntegralRepresentative.to_L2 IntegralRepresentative.action
  apply SL.Analysis.to_L2_congr
  apply ae_of_all
  intro X
  simp [polynomial_rep, Polynomial.eval_neg, Polynomial.eval_add, Polynomial.eval_mul,
    Polynomial.eval_C, Complex.ofReal_add, Complex.ofReal_neg, Complex.ofReal_mul]

theorem operator_on_polynomial (P : Polynomial ℝ) (HP : AuditRound5.residues P = 0) (C : ℝ) :
    operator C (polynomial_domain P HP) =
    polynomial_L2 (-P.derivative.derivative + Polynomial.C C * P) := by
  rw [operator_eq_action C (polynomial_domain P HP) (polynomial_rep P) rfl]
  exact polynomial_rep_action P C

theorem original_family_mem_domain :
    polynomial_L2 AuditRound5.p_zero ∈ domain ∧
    polynomial_L2 AuditRound5.p_one ∈ domain ∧
    (∀ M : ℕ, 2 ≤ M → polynomial_L2 (AuditRound5.p_even M) ∈ domain) ∧
    (∀ M : ℕ, 2 ≤ M → polynomial_L2 (AuditRound5.p_odd M) ∈ domain) := by
  refine ⟨polynomial_mem_domain _ AuditRound5.low_residues.1,
    polynomial_mem_domain _ AuditRound5.low_residues.2, ?_, ?_⟩
  · intro M HM
    exact polynomial_mem_domain _ (AuditRound5.even_residues M HM)
  · intro M HM
    exact polynomial_mem_domain _ (AuditRound5.odd_residues M HM)

end

end SL.Krein
