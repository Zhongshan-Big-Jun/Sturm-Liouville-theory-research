import Mathlib.Analysis.Real.Pi.Bounds
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Positivity

/-! Round8 local AUTHOR proofs. No spectral minmax, analytic IFT expansion,
T1/deep-sliver certification or global convergence is asserted here. -/
namespace AuditRound8

noncomputable section

/-- The phase for the explicit parameter counterexample, conditional on the spectral bound. -/
def phase (lambda2 : ℝ) : ℝ := (1 / 1600) * Real.sqrt (1600 * lambda2)

theorem phase_bound (lambda2 : ℝ) (_h0 : 0 ≤ lambda2)
    (hmax : lambda2 ≤ 4 * Real.pi ^ 2) :
    0 ≤ phase lambda2 ∧ phase lambda2 ≤ Real.pi / 20 ∧ Real.pi / 20 < Real.pi / 2 := by
  have hs : Real.sqrt (1600 * lambda2) ≤ 80 * Real.pi := by
    apply Real.sqrt_le_iff.mpr
    constructor
    · positivity
    · nlinarith
  refine ⟨by unfold phase; positivity, ?_, ?_⟩
  · unfold phase
    linarith
  · linarith [Real.pi_pos]

/-- Light half-length. -/
def ell (u : ℝ) : ℝ := 1 / 2 - u

def mubar1 (u : ℝ) : ℝ := Real.pi ^ 2 / (4 * u ^ 2)

def mubar2 (a u : ℝ) : ℝ := a ^ 2 / u ^ 2

/-- The trigonometric expression in the analytic supplement, not a free variable. -/
def I2 (a u : ℝ) : ℝ := u / 2 - u * Real.sin (2 * a) / (4 * a)

def S (a u : ℝ) : ℝ :=
  2 * mubar1 u / u - mubar2 a u * Real.sin a ^ 2 / I2 a u

/-- Candidate coefficient obtained in the informal expansion; algebraically explicit here. -/
def C (a b u : ℝ) : ℝ :=
  Real.pi ^ 2 * b / (2 * u ^ 2) -
  2 * a ^ 4 * b ^ 3 / (3 * u ^ 2 * (1 + b + b ^ 2 * a ^ 2))

/-- Consequences of the pole-free limiting odd-root equation. -/
theorem root_trig_reduction (a b : ℝ)
    (hroot : Real.sin a + b * a * Real.cos a = 0) :
    Real.sin a ^ 2 = b ^ 2 * a ^ 2 / (1 + b ^ 2 * a ^ 2) ∧
    Real.sin (2 * a) = -(2 * b * a) / (1 + b ^ 2 * a ^ 2) := by
  have hd : 1 + b ^ 2 * a ^ 2 ≠ 0 := by positivity
  have hs : Real.sin a = -(b * a * Real.cos a) := by linarith
  have hid := Real.sin_sq_add_cos_sq a
  rw [hs] at hid
  have hc : (1 + b ^ 2 * a ^ 2) * Real.cos a ^ 2 = 1 := by nlinarith only [hid]
  constructor
  · rw [hs]
    field_simp
    nlinarith only [congrArg (fun x : ℝ => b ^ 2 * a ^ 2 * x) hc]
  · rw [Real.sin_two_mul, hs]
    field_simp
    nlinarith only [congrArg (fun x : ℝ => b * a * x) hc]

theorem integral_reduction (a b u : ℝ) (ha : 0 < a) (hu : 0 < u) (hb : 0 < b)
    (hroot : Real.sin a + b * a * Real.cos a = 0) :
    I2 a u = u * (1 + b + b ^ 2 * a ^ 2) / (2 * (1 + b ^ 2 * a ^ 2)) ∧
    0 < I2 a u := by
  have hd : 1 + b ^ 2 * a ^ 2 ≠ 0 := by positivity
  have heq : I2 a u = u * (1 + b + b ^ 2 * a ^ 2) / (2 * (1 + b ^ 2 * a ^ 2)) := by
    unfold I2
    rw [(root_trig_reduction a b hroot).2]
    field_simp
    ring
  refine ⟨heq, ?_⟩
  rw [heq]
  positivity

/-- The trigonometric-to-algebraic bridge for S is proved, not assumed. -/
theorem S_reduction (a b u : ℝ) (ha : 0 < a) (hu : 0 < u) (hb : 0 < b)
    (hroot : Real.sin a + b * a * Real.cos a = 0) :
    S a u = Real.pi ^ 2 / (2 * u ^ 3) -
      2 * a ^ 4 * b ^ 2 / (u ^ 3 * (1 + b + b ^ 2 * a ^ 2)) := by
  have hd : 1 + b ^ 2 * a ^ 2 ≠ 0 := by positivity
  have he : 1 + b + b ^ 2 * a ^ 2 ≠ 0 := by positivity
  unfold S mubar1 mubar2
  rw [(root_trig_reduction a b hroot).1, (integral_reduction a b u ha hu hb hroot).1]
  field_simp
  ring

/-- No coefficient identity is assumed: b=ell/u and the odd-root equation suffice. -/
theorem coefficient_identity (a b u : ℝ) (ha : 0 < a) (hu : 0 < u)
    (hu_half : u < 1 / 2) (hb : b = ell u / u)
    (hroot : Real.sin a + b * a * Real.cos a = 0) :
    C a b u = 4 * mubar1 u * ell u / (3 * u) + (ell u / 3) * S a u := by
  have hell : 0 < ell u := by unfold ell; linarith
  have hbpos : 0 < b := by rw [hb]; exact div_pos hell hu
  have hd : 1 + b ^ 2 * a ^ 2 ≠ 0 := by positivity
  have he : 1 + b + b ^ 2 * a ^ 2 ≠ 0 := by positivity
  have hbu : b * u = ell u := ((div_eq_iff (ne_of_gt hu)).mp hb.symm).symm
  unfold C S mubar1 mubar2
  rw [(root_trig_reduction a b hroot).1, (integral_reduction a b u ha hu hbpos hroot).1]
  rw [← hbu]
  field_simp
  ring

/-- Stationarity only cancels the now-proved residual S; the remaining coefficient is positive. -/
theorem stationary_coefficient (a b u : ℝ) (ha : 0 < a) (hu : 0 < u)
    (hu_half : u < 1 / 2) (hb : b = ell u / u)
    (hroot : Real.sin a + b * a * Real.cos a = 0) (hstat : S a u = 0) :
    C a b u = Real.pi ^ 2 * ell u / (3 * u ^ 3) ∧ 0 < C a b u := by
  have hid := coefficient_identity a b u ha hu hu_half hb hroot
  rw [hstat] at hid
  have heq : C a b u = Real.pi ^ 2 * ell u / (3 * u ^ 3) := by
    rw [hid]
    unfold mubar1
    field_simp
    ring
  refine ⟨heq, ?_⟩
  rw [heq]
  have hell : 0 < ell u := by unfold ell; linarith
  positivity

/-- Exact constants from analytic_repairs.md section 2. This is a rational scalar statement. -/
def scalarRatio : ℚ :=
  (4 * (337 / 1000) * 9 * (100046 / 100000)) /
  (3 * (333 / 106) * (156 / 100) * (99996 / 100000))

theorem scalar_ratio_bound : scalarRatio < (8256 / 10000 : ℚ) := by
  norm_num [scalarRatio]

end
end AuditRound8
