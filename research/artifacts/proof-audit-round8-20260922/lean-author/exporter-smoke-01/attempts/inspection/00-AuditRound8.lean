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

/-- Original critical curve w_c(R)=1/(2(1+R^(-1/2))). -/
def wCritical (R : ℝ) : ℝ := 1 / (2 * (1 + 1 / Real.sqrt R))

theorem critical_rewrite (R : ℝ) (hR : 0 < R) :
    wCritical R = Real.sqrt R / (2 * (Real.sqrt R + 1)) := by
  have hs : 0 < Real.sqrt R := Real.sqrt_pos.mpr hR
  unfold wCritical
  field_simp

/-- A point in the first R-cell and real B region, above the checked rectangle's top. -/
theorem B_curved_counterexample :
    (1500 : ℝ) < 3015 / 2 ∧ (3015 / 2 : ℝ) < 1515 ∧
    (19 / 100 : ℝ) < 48743 / 100000 ∧ (48743 / 100000 : ℝ) < 1 / 2 ∧
    wCritical 1500 < 48743 / 100000 ∧
    (48743 / 100000 : ℝ) < wCritical (3015 / 2) := by
  have hs0 : 0 < Real.sqrt (1500 : ℝ) := Real.sqrt_pos.mpr (by norm_num)
  have hs1 : 0 < Real.sqrt (3015 / 2 : ℝ) := Real.sqrt_pos.mpr (by norm_num)
  have hupper : Real.sqrt (1500 : ℝ) < 48743 / 1257 := by
    apply (Real.sqrt_lt' (by norm_num)).mpr
    norm_num
  have hlower : (48743 / 1257 : ℝ) < Real.sqrt (3015 / 2 : ℝ) := by
    have hh := Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 3015 / 2)
    nlinarith
  refine ⟨by norm_num, by norm_num, by norm_num, by norm_num, ?_, ?_⟩
  · rw [critical_rewrite 1500 (by norm_num)]
    apply (div_lt_iff₀ (by positivity)).mpr
    nlinarith only [hupper]
  · rw [critical_rewrite (3015 / 2) (by norm_num)]
    apply (lt_div_iff₀ (by positivity)).mpr
    nlinarith only [hlower]

/-- The true mathematical-pi cap curve, not a floating approximation. -/
def wCap (R : ℝ) : ℝ := (1 / 2) / Real.sqrt (1 + 25 / (Real.pi ^ 2 * R))

def capGap (R w : ℝ) : ℝ := Real.pi ^ 2 * R * (1 / (4 * w ^ 2) - 1)

theorem cap_square (R : ℝ) (hR : 0 < R) :
    0 < wCap R ∧ wCap R ^ 2 = Real.pi ^ 2 * R / (4 * (Real.pi ^ 2 * R + 25)) := by
  have hpR : 0 < Real.pi ^ 2 * R := by positivity
  have hx : 0 < 1 + 25 / (Real.pi ^ 2 * R) := by positivity
  constructor
  · unfold wCap
    positivity
  · unfold wCap
    rw [div_pow, Real.sq_sqrt hx.le]
    field_simp
    ring

theorem cap_lt_of_gap_lt (R w : ℝ) (hR : 0 < R) (hw : 0 < w)
    (hgap : capGap R w < 25) : wCap R < w := by
  have hd : 0 < 4 * w ^ 2 := by positivity
  have hc : 0 < 4 * (Real.pi ^ 2 * R + 25) := by positivity
  have hconvert : capGap R w = Real.pi ^ 2 * R / (4 * w ^ 2) - Real.pi ^ 2 * R := by
    unfold capGap
    ring
  rw [hconvert] at hgap
  have hm : Real.pi ^ 2 * R < (25 + Real.pi ^ 2 * R) * (4 * w ^ 2) := by
    apply (div_lt_iff₀ hd).mp
    linarith
  have hs : wCap R ^ 2 < w ^ 2 := by
    rw [(cap_square R hR).2]
    apply (div_lt_iff₀ hc).mpr
    nlinarith only [hm]
  nlinarith [(cap_square R hR).1]

theorem lt_cap_of_lt_gap (R w : ℝ) (hR : 0 < R) (hw : 0 < w)
    (hgap : 25 < capGap R w) : w < wCap R := by
  have hd : 0 < 4 * w ^ 2 := by positivity
  have hc : 0 < 4 * (Real.pi ^ 2 * R + 25) := by positivity
  have hconvert : capGap R w = Real.pi ^ 2 * R / (4 * w ^ 2) - Real.pi ^ 2 * R := by
    unfold capGap
    ring
  rw [hconvert] at hgap
  have hm : (25 + Real.pi ^ 2 * R) * (4 * w ^ 2) < Real.pi ^ 2 * R := by
    apply (lt_div_iff₀ hd).mp
    linarith
  have hs : w ^ 2 < wCap R ^ 2 := by
    rw [(cap_square R hR).2]
    apply (lt_div_iff₀ hc).mpr
    nlinarith only [hm]
  nlinarith [(cap_square R hR).1]

/-- Actual pi bounds from Mathlib suffice to certify both strict gap signs. -/
theorem D_gap_signs :
    capGap (3015 / 2) (4995815 / 10000000) < 25 ∧
    25 < capGap 1515 (4995815 / 10000000) := by
  have hpU : Real.pi ^ 2 < (31416 / 10000 : ℝ) ^ 2 := by
    nlinarith [Real.pi_lt_d4, Real.pi_pos]
  have hpL : (31415 / 10000 : ℝ) ^ 2 < Real.pi ^ 2 := by
    nlinarith [Real.pi_gt_d4, Real.pi_pos]
  constructor
  · norm_num [capGap]
    nlinarith only [hpU]
  · norm_num [capGap]
    nlinarith only [hpL]

/-- A point in true D, below the first checked D rectangle, at the same interior R. -/
theorem D_curved_counterexample :
    (1500 : ℝ) < 3015 / 2 ∧ (3015 / 2 : ℝ) < 1515 ∧
    (0 : ℝ) < 4995815 / 10000000 ∧ (4995815 / 10000000 : ℝ) < 1 / 2 ∧
    wCap (3015 / 2) < 4995815 / 10000000 ∧
    (4995815 / 10000000 : ℝ) < wCap 1515 := by
  exact ⟨by norm_num, by norm_num, by norm_num, by norm_num,
    cap_lt_of_gap_lt _ _ (by norm_num) (by norm_num) D_gap_signs.1,
    lt_cap_of_lt_gap _ _ (by norm_num) (by norm_num) D_gap_signs.2⟩

/-- Materialized local repair conjunction. Every conditional premise is displayed. -/
theorem local_root :
  (∀ (lambda2 : ℝ), 0 ≤ lambda2 → lambda2 ≤ 4 * Real.pi ^ 2 →
    0 ≤ phase lambda2 ∧ phase lambda2 ≤ Real.pi / 20 ∧ Real.pi / 20 < Real.pi / 2) ∧
  (∀ (a b u : ℝ), 0 < a → 0 < u → 0 < b →
    Real.sin a + b * a * Real.cos a = 0 →
    I2 a u = u * (1 + b + b ^ 2 * a ^ 2) / (2 * (1 + b ^ 2 * a ^ 2)) ∧
    0 < I2 a u) ∧
  (∀ (a b u : ℝ), 0 < a → 0 < u → 0 < b →
    Real.sin a + b * a * Real.cos a = 0 →
    S a u = Real.pi ^ 2 / (2 * u ^ 3) -
      2 * a ^ 4 * b ^ 2 / (u ^ 3 * (1 + b + b ^ 2 * a ^ 2))) ∧
  (∀ (a b u : ℝ), 0 < a → 0 < u → u < 1 / 2 → b = ell u / u →
    Real.sin a + b * a * Real.cos a = 0 →
    C a b u = 4 * mubar1 u * ell u / (3 * u) + (ell u / 3) * S a u) ∧
  (∀ (a b u : ℝ), 0 < a → 0 < u → u < 1 / 2 → b = ell u / u →
    Real.sin a + b * a * Real.cos a = 0 → S a u = 0 →
    C a b u = Real.pi ^ 2 * ell u / (3 * u ^ 3) ∧ 0 < C a b u) ∧
  scalarRatio < (8256 / 10000 : ℚ) ∧
  ((1500 : ℝ) < 3015 / 2 ∧ (3015 / 2 : ℝ) < 1515 ∧
    (19 / 100 : ℝ) < 48743 / 100000 ∧ (48743 / 100000 : ℝ) < 1 / 2 ∧
    wCritical 1500 < 48743 / 100000 ∧
    (48743 / 100000 : ℝ) < wCritical (3015 / 2)) ∧
  (capGap (3015 / 2) (4995815 / 10000000) < 25 ∧
    25 < capGap 1515 (4995815 / 10000000)) ∧
  ((1500 : ℝ) < 3015 / 2 ∧ (3015 / 2 : ℝ) < 1515 ∧
    (0 : ℝ) < 4995815 / 10000000 ∧ (4995815 / 10000000 : ℝ) < 1 / 2 ∧
    wCap (3015 / 2) < 4995815 / 10000000 ∧
    (4995815 / 10000000 : ℝ) < wCap 1515) := by
  exact ⟨phase_bound, integral_reduction, S_reduction, coefficient_identity,
    stationary_coefficient, scalar_ratio_bound, B_curved_counterexample,
    D_gap_signs, D_curved_counterexample⟩

end
end AuditRound8
