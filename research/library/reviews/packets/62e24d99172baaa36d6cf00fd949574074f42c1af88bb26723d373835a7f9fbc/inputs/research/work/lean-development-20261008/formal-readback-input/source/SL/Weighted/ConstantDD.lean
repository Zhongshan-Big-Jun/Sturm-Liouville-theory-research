import SL.Weighted.L2Bridge
import Mathlib.Analysis.SpecialFunctions.Integrals.Basic
import Mathlib.Analysis.Complex.RealDeriv
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.LinearCombination
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.FunProp

   
                                                                            
                                                                            
                                                                              
                                                                      
                                                                                
                                                                     
  

noncomputable section

namespace SL.Weighted.ConstantDD

open MeasureTheory Set

def wave_number (Length : ℝ) (Index : ℕ) : ℝ := (Index : ℝ) * Real.pi / Length
def frequency (Length Rho : ℝ) (Index : ℕ) : ℝ := wave_number Length Index / Real.sqrt Rho
def eigenvalue (Length Rho : ℝ) (Index : ℕ) : ℝ := frequency Length Rho Index ^ 2
def amplitude (Length Rho : ℝ) : ℝ := Real.sqrt (2 / (Rho * Length))
def real_mode (Length Rho : ℝ) (Index : ℕ) (x : ℝ) : ℝ :=
  amplitude Length Rho * Real.sin (wave_number Length Index * x)
def mode (Length Rho : ℝ) (Index : ℕ) (x : ℝ) : ℂ :=
  (real_mode Length Rho Index x : ℂ)
def velocity (Length Rho : ℝ) (Index : ℕ) (x : ℝ) : ℂ :=
  (amplitude Length Rho * wave_number Length Index *
    Real.cos (wave_number Length Index * x) : ℝ)

theorem wave_number_pos (Length : ℝ) (Index : ℕ) (LengthPos : 0 < Length)
    (IndexPos : 0 < Index) : 0 < wave_number Length Index := by
  unfold wave_number
  exact div_pos (mul_pos (by exact_mod_cast IndexPos) Real.pi_pos) LengthPos

theorem frequency_pos (Length Rho : ℝ) (Index : ℕ) (LengthPos : 0 < Length)
    (RhoPos : 0 < Rho) (IndexPos : 0 < Index) : 0 < frequency Length Rho Index := by
  exact div_pos (wave_number_pos Length Index LengthPos IndexPos) (Real.sqrt_pos.2 RhoPos)

theorem eigenvalue_mul_density (Length Rho : ℝ) (Index : ℕ) (RhoPos : 0 < Rho) :
    eigenvalue Length Rho Index * Rho = wave_number Length Index ^ 2 := by
  unfold eigenvalue frequency
  rw [div_pow, Real.sq_sqrt RhoPos.le]
  exact div_mul_cancel₀ _ RhoPos.ne'

theorem has_deriv_mode (Length Rho : ℝ) (Index : ℕ) (x : ℝ) :
    HasDerivAt (mode Length Rho Index) (velocity Length Rho Index x) x := by
  have RealDeriv := (((hasDerivAt_id x).const_mul (wave_number Length Index)).sin).const_mul
    (amplitude Length Rho)
  have RealIdentity : HasDerivAt (real_mode Length Rho Index)
      (amplitude Length Rho * wave_number Length Index *
        Real.cos (wave_number Length Index * x)) x := by
    convert RealDeriv using 1 <;> try rfl
    simp only [id_eq, mul_one]
    ring
  exact RealIdentity.ofReal_comp

theorem has_deriv_velocity (Length Rho : ℝ) (Index : ℕ) (RhoPos : 0 < Rho) (x : ℝ) :
    HasDerivAt (velocity Length Rho Index)
      (-(eigenvalue Length Rho Index : ℂ) * ((Rho : ℂ) * mode Length Rho Index x)) x := by
  have RealDeriv := (((hasDerivAt_id x).const_mul (wave_number Length Index)).cos).const_mul
    (amplitude Length Rho * wave_number Length Index)
  have Scale := eigenvalue_mul_density Length Rho Index RhoPos
  have RealIdentity : HasDerivAt
      (fun t => amplitude Length Rho * wave_number Length Index *
        Real.cos (wave_number Length Index * t))
      (-(eigenvalue Length Rho Index) * (Rho * real_mode Length Rho Index x)) x := by
    convert RealDeriv using 1 <;> try rfl
    dsimp [real_mode]
    linear_combination -(amplitude Length Rho * Real.sin (wave_number Length Index * x)) * Scale
  convert RealIdentity.ofReal_comp using 1
  · rfl
  · simp only [mode, Complex.ofReal_neg, Complex.ofReal_mul]

theorem continuous_mode (Length Rho : ℝ) (Index : ℕ) : Continuous (mode Length Rho Index) := by
  unfold mode real_mode
  fun_prop

theorem continuous_velocity (Length Rho : ℝ) (Index : ℕ) :
    Continuous (velocity Length Rho Index) := by
  unfold velocity
  fun_prop

def solution (Length Rho : ℝ) (Index : ℕ) (RhoPos : 0 < Rho) :
    Solution Length (fun _ => Rho) (eigenvalue Length Rho Index) where
  value := mode Length Rho Index
  velocity := velocity Length Rho Index
  value_continuous := (continuous_mode Length Rho Index).continuousOn
  velocity_continuous := (continuous_velocity Length Rho Index).continuousOn
  force_integrable := (continuous_const.mul (continuous_mode Length Rho Index)).intervalIntegrable _ _
  first_integral := by
    intro x _
    have Identity := intervalIntegral.integral_eq_sub_of_hasDerivAt
      (fun t _ => has_deriv_mode Length Rho Index t)
      ((continuous_velocity Length Rho Index).intervalIntegrable 0 x)
    rw [Identity]
    abel
  second_integral := by
    intro x _
    have ForceContinuous : Continuous (fun t => -(eigenvalue Length Rho Index : ℂ) *
        ((Rho : ℂ) * mode Length Rho Index t)) :=
      continuous_const.mul (continuous_const.mul (continuous_mode Length Rho Index))
    have Identity := intervalIntegral.integral_eq_sub_of_hasDerivAt
      (fun t _ => has_deriv_velocity Length Rho Index RhoPos t)
      (ForceContinuous.intervalIntegrable 0 x)
    rw [intervalIntegral.integral_const_mul] at Identity
    linear_combination -Identity

theorem dd_boundary (Length Rho : ℝ) (Index : ℕ) (LengthPos : 0 < Length) :
    boundary_condition .DD Length (mode Length Rho Index) (velocity Length Rho Index) := by
  have Endpoint : wave_number Length Index * Length = (Index : ℝ) * Real.pi := by
    exact div_mul_cancel₀ _ LengthPos.ne'
  constructor
  · simp [mode, real_mode]
  · simp [mode, real_mode, Endpoint, Real.sin_nat_mul_pi]

theorem sine_squared_integral (Length : ℝ) (Index : ℕ) (LengthPos : 0 < Length)
    (IndexPos : 0 < Index) :
    (∫ x in 0..Length, Real.sin (wave_number Length Index * x) ^ 2) = Length / 2 := by
  have WavePos := wave_number_pos Length Index LengthPos IndexPos
  have Endpoint : wave_number Length Index * Length = (Index : ℝ) * Real.pi := by
    exact div_mul_cancel₀ _ LengthPos.ne'
  rw [intervalIntegral.integral_comp_mul_left (fun x => Real.sin x ^ 2) WavePos.ne']
  simp only [mul_zero, Endpoint, integral_sin_sq, Real.sin_zero, Real.sin_nat_mul_pi,
    zero_mul, sub_zero, zero_add, smul_eq_mul]
  have Scale : wave_number Length Index * Length = (Index : ℝ) * Real.pi := Endpoint
  field_simp
  nlinarith [Scale]

theorem weighted_mass (Length Rho : ℝ) (Index : ℕ) (LengthPos : 0 < Length)
    (RhoPos : 0 < Rho) (IndexPos : 0 < Index) :
    mass Length (fun _ => Rho) (mode Length Rho Index) = 1 := by
  have AmplitudeSq : amplitude Length Rho ^ 2 = 2 / (Rho * Length) := by
    exact Real.sq_sqrt (by positivity)
  have Integrand : (fun x => Rho * ‖mode Length Rho Index x‖ ^ 2) =
      (fun x => (Rho * amplitude Length Rho ^ 2) *
        Real.sin (wave_number Length Index * x) ^ 2) := by
    funext x
    simp only [mode, real_mode, Complex.norm_real, Real.norm_eq_abs, sq_abs]
    ring
  unfold mass
  rw [Integrand, intervalIntegral.integral_const_mul,
    sine_squared_integral Length Index LengthPos IndexPos, AmplitudeSq]
  field_simp

                                                                                     
                                                                                      
theorem constant_dd_root (Length Rho : ℝ) (Index : ℕ) (LengthPos : 0 < Length)
    (RhoPos : 0 < Rho) (IndexPos : 0 < Index) :
    0 < frequency Length Rho Index ∧
    eigenvalue Length Rho Index = frequency Length Rho Index ^ 2 ∧
    NormalizedEigenfunction .DD Length (fun _ => Rho) (eigenvalue Length Rho Index)
      (solution Length Rho Index RhoPos) := by
  refine ⟨frequency_pos Length Rho Index LengthPos RhoPos IndexPos, rfl, ?_⟩
  refine ⟨sq_pos_of_pos (frequency_pos Length Rho Index LengthPos RhoPos IndexPos), ?_, ?_⟩
  · exact dd_boundary Length Rho Index LengthPos
  · exact weighted_mass Length Rho Index LengthPos RhoPos IndexPos

theorem mode_mem_weighted_l2 (Length Rho : ℝ) (Index : ℕ) (RhoPos : 0 < Rho) :
    MemLp (mode Length Rho Index) 2 (weighted_measure (constant_density Length Rho RhoPos)) := by
  exact continuous_mem_weighted_l2 (constant_density Length Rho RhoPos)
    (continuous_mode Length Rho Index).continuousOn

def eigenvector (Length Rho : ℝ) (Index : ℕ) (RhoPos : 0 < Rho) :
    WeightedL2 (constant_density Length Rho RhoPos) :=
  (mode_mem_weighted_l2 Length Rho Index RhoPos).toLp (mode Length Rho Index)

theorem eigenvector_norm_squared (Length Rho : ℝ) (Index : ℕ) (LengthPos : 0 < Length)
    (RhoPos : 0 < Rho) (IndexPos : 0 < Index) :
    ‖eigenvector Length Rho Index RhoPos‖ ^ 2 = 1 := by
  change ‖weighted_vector (constant_density Length Rho RhoPos) (mode Length Rho Index)
    (continuous_mode Length Rho Index).continuousOn‖ ^ 2 = 1
  rw [weighted_norm_eq_mass Length LengthPos]
  exact weighted_mass Length Rho Index LengthPos RhoPos IndexPos

                                                                                            
theorem constant_dd_l2_root (Length Rho : ℝ) (Index : ℕ) (LengthPos : 0 < Length)
    (RhoPos : 0 < Rho) (IndexPos : 0 < Index) :
    0 < frequency Length Rho Index ∧
    eigenvalue Length Rho Index = frequency Length Rho Index ^ 2 ∧
    NormalizedEigenfunction .DD Length (fun _ => Rho) (eigenvalue Length Rho Index)
      (solution Length Rho Index RhoPos) ∧
    ‖eigenvector Length Rho Index RhoPos‖ ^ 2 = 1 := by
  have Base := constant_dd_root Length Rho Index LengthPos RhoPos IndexPos
  exact ⟨Base.1, Base.2.1, Base.2.2,
    eigenvector_norm_squared Length Rho Index LengthPos RhoPos IndexPos⟩

end SL.Weighted.ConstantDD
