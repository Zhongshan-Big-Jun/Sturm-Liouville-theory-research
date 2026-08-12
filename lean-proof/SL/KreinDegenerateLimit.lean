import Mathlib
import SL.H1Isometry
import SL.HsOrthogonalSystems

/-!
# The degenerate limit c -> 0 of the shifted Krein Laplacian (polynomial version)

Formalization of the polynomial-level statements of `docs/SL_krein_c0_limit.tex`
(session 12): the radical of the limiting pairing `(f, g)_1,0` on polynomials,
the exact degeneration of the low Krein-Sobolev modes, the divergence of the
high norms (n = 4 closed form), and the exact span decomposition of the
quotient (Theorem "complete", part (a), polynomial version).

Honesty notes:
* The quotient-space theorems of the source (isometric isomorphism
  `H^1/W -> L^2_0`, Theorem "quotient"; completeness in the quotient,
  Theorem "complete" (b)-(d); convergence of the unit-normalized system,
  Theorem "unit") require functional analysis / density arguments and are
  NOT formalized here.  Only the exact polynomial-level statements are
  formalized: the radical on polynomials (Theorem "radical"), the
  decomposition `Pi = span{1,x} + span{S_2, ..., S_N}` (Theorem "complete"
  (a)), the norm identities of the low modes (Theorem "low"), and the
  divergence of `||K_4||^2` (first part of Theorem "high").
* The norm formula `||K_n||^2 = 2c a_n a_{n+2}/(2n+1)` (source (21)) is a
  literature fact (Theorem 3 of the Axioms paper); it is assumed here via
  `KreinSobolevFacts` (see SL/HsOrthogonalSystems.lean), exactly as in the
  other files of this project.
* The general growth `a_n(c) = Theta(c^{-...})` of Theorem "high" and the
  resulting divergence of `||K_n||^2` for every n >= 4 are only partially
  formalized: the n = 4 closed form and its divergence are proved below;
  the general even-index growth would need an extra induction on the
  recurrence and is recorded as open in this file.
-/

namespace SL

namespace KreinDegenerateLimit

open HsOrthogonalSystems

open Polynomial
open Filter
open scoped BigOperators
open scoped Real Interval
open scoped Topology
open MeasureTheory

noncomputable section

/-! ## The c = 0 pairing and its radical -/

/-- The boundary jump of a polynomial: `Delta p = p(1) - p(-1)`. -/
def delta (p : Polynomial ℝ) : ℝ :=
  p.eval 1 - p.eval (-1)

/-- Polynomial FTC: `∫_{-1}^1 p' = p(1) - p(-1) = Delta p`. -/
theorem poly_ftc (p : Polynomial ℝ) :
    (∫ x in (-1 : ℝ)..1, p.derivative.eval x) = delta p := by
  induction p using Polynomial.induction_on' with
  | add p q hp hq =>
      calc
        (∫ x in (-1 : ℝ)..1, (p + q).derivative.eval x)
            = (∫ x in (-1 : ℝ)..1, (p.derivative + q.derivative).eval x) := by
                simp [Polynomial.derivative_add]
        _ = (∫ x in (-1 : ℝ)..1, p.derivative.eval x + q.derivative.eval x) := by
                simp [Polynomial.eval_add]
        _ = (∫ x in (-1 : ℝ)..1, p.derivative.eval x)
              + (∫ x in (-1 : ℝ)..1, q.derivative.eval x) := by
                rw [intervalIntegral.integral_add]
                · exact Continuous.intervalIntegrable (μ := volume)
                    (by fun_prop : Continuous fun x : ℝ => p.derivative.eval x) (-1) 1
                · exact Continuous.intervalIntegrable (μ := volume)
                    (by fun_prop : Continuous fun x : ℝ => q.derivative.eval x) (-1) 1
        _ = delta p + delta q := by rw [hp, hq]
        _ = delta (p + q) := by
                simp [delta, Polynomial.eval_add]
                ring
  | monomial n a =>
      rw [← Polynomial.C_mul_X_pow_eq_monomial]
      by_cases hn : n = 0
      · subst n
        simp [delta, Polynomial.derivative_C]
      · have hn0 : 0 < n := Nat.pos_of_ne_zero hn
        have hnc : (n : ℝ) ≠ 0 := by exact_mod_cast (ne_of_gt hn0)
        have hsub : n - 1 + 1 = n := Nat.sub_add_cancel (Nat.succ_le_of_lt hn0)
        have hder : (C a * X ^ n).derivative = C (a * (n : ℝ)) * X ^ (n - 1) := by
          rw [Polynomial.derivative_C_mul_X_pow]
        calc
          (∫ x in (-1 : ℝ)..1, (C a * X ^ n).derivative.eval x)
              = (∫ x in (-1 : ℝ)..1, (C (a * (n : ℝ)) * X ^ (n - 1)).eval x) := by
                  rw [hder]
          _ = (∫ x in (-1 : ℝ)..1, (a * (n : ℝ)) * x ^ (n - 1)) := by
                  simp [Polynomial.eval_mul, Polynomial.eval_pow, Polynomial.eval_C,
                    Polynomial.eval_X]
          _ = (a * (n : ℝ)) * (∫ x in (-1 : ℝ)..1, x ^ (n - 1)) := by
                  rw [intervalIntegral.integral_const_mul]
          _ = (a * (n : ℝ)) * ((1 ^ ((n - 1) + 1) - (-1) ^ ((n - 1) + 1))
                / ((↑(n - 1) : ℝ) + 1)) := by
                  rw [integral_pow]
          _ = (a * (n : ℝ)) * ((1 ^ n - (-1) ^ n) / (n : ℝ)) := by
                  rw [hsub]
                  have hden : (↑(n - 1) : ℝ) + 1 = (n : ℝ) := by
                    exact_mod_cast hsub
                  rw [hden]
          _ = a * 1 ^ n - a * (-1) ^ n := by
                  field_simp [hnc]
          _ = (C a * X ^ n).eval 1 - (C a * X ^ n).eval (-1) := by
                  simp [Polynomial.eval_mul, Polynomial.eval_pow, Polynomial.eval_C,
                    Polynomial.eval_X]

/-- The limiting (c = 0) pairing on polynomials:
`(f, g)_0 = ∫ f'' g' - (1/2) Delta f Delta g`. -/
noncomputable def pair0 (f g : Polynomial ℝ) : ℝ :=
  (∫ x in (-1 : ℝ)..1, f.derivative.eval x * g.derivative.eval x)
    - (1 / 2) * delta f * delta g

/-- `(1, p)_0 = 0` for every polynomial p: the constant direction is in the
radical. -/
theorem pair0_one (p : Polynomial ℝ) : pair0 1 p = 0 := by
  unfold pair0
  have hd : delta (1 : Polynomial ℝ) = 0 := by
    norm_num [delta]
  simp [hd]

/-- `(x, p)_0 = 0` for every polynomial p: the affine direction is in the
radical. -/
theorem pair0_X (p : Polynomial ℝ) : pair0 X p = 0 := by
  unfold pair0
  have hdX : delta X = 2 := by
    norm_num [delta]
  simp [hdX, poly_ftc]

/-- Integral of a squared difference against a constant:
`∫ (p - α)^2 = ∫ p^2 - 2α ∫ p + 2α^2` on [-1,1]. -/
lemma integral_sq_sub_const (p : Polynomial ℝ) (α : ℝ) :
    (∫ x in (-1 : ℝ)..1, (p.eval x - α) ^ 2)
      = (∫ x in (-1 : ℝ)..1, (p.eval x) ^ 2)
          - 2 * α * (∫ x in (-1 : ℝ)..1, p.eval x) + 2 * α ^ 2 := by
  have hsplit : (fun x : ℝ => (p.eval x - α) ^ 2)
      = fun x : ℝ => (p.eval x) ^ 2 - 2 * α * p.eval x + α ^ 2 := by
        funext x
        ring
  rw [hsplit]
  calc
    (∫ x in (-1 : ℝ)..1, (p.eval x) ^ 2 - 2 * α * p.eval x + α ^ 2)
        = (∫ x in (-1 : ℝ)..1, (p.eval x) ^ 2 - 2 * α * p.eval x)
            + (∫ x in (-1 : ℝ)..1, α ^ 2) := by
            rw [intervalIntegral.integral_add]
            · exact Continuous.intervalIntegrable (μ := volume)
                (by fun_prop : Continuous fun x : ℝ =>
                  (p.eval x) ^ 2 - 2 * α * p.eval x) (-1) 1
            · exact Continuous.intervalIntegrable (μ := volume)
                (by fun_prop : Continuous fun x : ℝ => α ^ 2) (-1) 1
    _ = (∫ x in (-1 : ℝ)..1, (p.eval x) ^ 2)
          - 2 * α * (∫ x in (-1 : ℝ)..1, p.eval x) + 2 * α ^ 2 := by
            rw [intervalIntegral.integral_sub]
            · rw [intervalIntegral.integral_const_mul]
              have hc : (∫ x in (-1 : ℝ)..1, α ^ 2) = 2 * α ^ 2 := by
                rw [intervalIntegral.integral_const]
                norm_num
              rw [hc]
            · exact Continuous.intervalIntegrable (μ := volume)
                (by fun_prop : Continuous fun x : ℝ => (p.eval x) ^ 2) (-1) 1
            · exact Continuous.intervalIntegrable (μ := volume)
                (by fun_prop : Continuous fun x : ℝ => 2 * α * p.eval x) (-1) 1

/-- For `g = f' - α` with `α = Δf/2`, the integral of `g^2` equals the
limiting pairing `(f, f)_0`. -/
lemma integral_g_sq_eq_pair0 {f : Polynomial ℝ} (α : ℝ)
    (hα : α = delta f / 2) :
    (∫ x in (-1 : ℝ)..1, ((f.derivative - C α).eval x) ^ 2) = pair0 f f := by
  calc
    (∫ x in (-1 : ℝ)..1, ((f.derivative - C α).eval x) ^ 2)
        = (∫ x in (-1 : ℝ)..1, (f.derivative.eval x - α) ^ 2) := by
            simp [Polynomial.eval_sub, Polynomial.eval_C]
    _ = (∫ x in (-1 : ℝ)..1, (f.derivative.eval x) ^ 2)
          - 2 * α * (∫ x in (-1 : ℝ)..1, f.derivative.eval x) + 2 * α ^ 2 := by
            exact integral_sq_sub_const f.derivative α
    _ = (∫ x in (-1 : ℝ)..1, (f.derivative.eval x) ^ 2) - 2 * α * delta f + 2 * α ^ 2 := by
            rw [poly_ftc]
    _ = pair0 f f := by
            unfold pair0
            rw [hα]
            ring_nf

/-- The limiting pairing vanishes on affine polynomials:
`pair0 (C a + C b X) (C c + C d X) = 0`. -/
theorem pair0_affine (a b c d : ℝ) :
    pair0 (C a + C b * X) (C c + C d * X) = 0 := by
  unfold pair0
  have hder1 : (C a + C b * X).derivative = C b := by simp
  have hder2 : (C c + C d * X).derivative = C d := by simp
  have hd1 : delta (C a + C b * X) = 2 * b := by
    simp [delta]
    ring
  have hd2 : delta (C c + C d * X) = 2 * d := by
    simp [delta]
    ring
  rw [hder1, hder2, hd1, hd2]
  simp [intervalIntegral.integral_const]
  ring

/-- If `(f, f)_0 = 0` then `f` is affine, i.e. `f` lies in
`span {1, x}`.  Together with `pair0_one` and `pair0_X` this identifies the
radical of the limiting pairing exactly (Theorem "radical" of the source,
polynomial version). -/
theorem pair0_self_eq_zero_imp_affine (f : Polynomial ℝ) (h : pair0 f f = 0) :
    f ∈ Submodule.span ℝ ({1, X} : Set (Polynomial ℝ)) := by
  let α : ℝ := delta f / 2
  let g : Polynomial ℝ := f.derivative - C α
  have hα : α = delta f / 2 := rfl
  have hint0 : (∫ x in (-1 : ℝ)..1, (g.eval x) ^ 2) = 0 := by
    rw [integral_g_sq_eq_pair0 (f := f) (α := α) hα]
    exact h
  have hnn : 0 ≤ᵐ[volume.restrict (Set.Ioc (-1 : ℝ) 1)]
      (fun x : ℝ => (g.eval x) ^ 2) := by
    filter_upwards with x
    exact sq_nonneg (g.eval x)
  have hfi : IntervalIntegrable (fun x : ℝ => (g.eval x) ^ 2) volume (-1) 1 := by
    exact Continuous.intervalIntegrable (μ := volume)
      (by fun_prop : Continuous fun x : ℝ => (g.eval x) ^ 2) (-1) 1
  have hzero_ae : (fun x : ℝ => (g.eval x) ^ 2)
      =ᵐ[volume.restrict (Set.Ioc (-1 : ℝ) 1)] 0 := by
    exact (intervalIntegral.integral_eq_zero_iff_of_le_of_nonneg_ae (by norm_num) hnn hfi).1 hint0
  have hzero_ae_oo : (fun x : ℝ => (g.eval x) ^ 2)
      =ᵐ[volume.restrict (Set.Ioo (-1 : ℝ) 1)] 0 := by
    exact ae_restrict_of_ae_restrict_of_subset Set.Ioo_subset_Ioc_self hzero_ae
  have heqon : Set.EqOn (fun x : ℝ => (g.eval x) ^ 2) 0 (Set.Ioo (-1 : ℝ) 1) := by
    exact MeasureTheory.Measure.eqOn_open_of_ae_eq hzero_ae_oo isOpen_Ioo
      (by fun_prop : ContinuousOn (fun x : ℝ => (g.eval x) ^ 2) (Set.Ioo (-1 : ℝ) 1))
      (by fun_prop : ContinuousOn (0 : ℝ → ℝ) (Set.Ioo (-1 : ℝ) 1))
  have hpoint : ∀ x ∈ Set.Ioo (-1 : ℝ) 1, g.eval x = 0 := by
    intro x hx
    exact sq_eq_zero_iff.mp (heqon hx)
  have hinf_oo : (Set.Ioo (-1 : ℝ) 1).Infinite := by
    let u : ℕ → ℝ := fun n => 1 - 1 / (n + 2 : ℝ)
    have hu_mem : ∀ n : ℕ, u n ∈ Set.Ioo (-1 : ℝ) 1 := by
      intro n
      have hpos : 0 < 1 / (n + 2 : ℝ) := by positivity
      have hle : 1 / (n + 2 : ℝ) ≤ 1 / 2 := by
        apply one_div_le_one_div_of_le (by norm_num)
        exact_mod_cast (Nat.le_add_left 2 n)
      constructor <;> dsimp [u] <;> linarith
    have hu_inj : Function.Injective u := by
      intro m n hmn
      dsimp [u] at hmn
      have h1 : 1 / (m + 2 : ℝ) = 1 / (n + 2 : ℝ) := by linarith
      have h1' : (m + 2 : ℝ)⁻¹ = (n + 2 : ℝ)⁻¹ := by
        simpa [one_div] using h1
      have h2 : (m + 2 : ℝ) = (n + 2 : ℝ) := by
        calc
          (m + 2 : ℝ) = ((m + 2 : ℝ)⁻¹)⁻¹ := (inv_inv (a := (m + 2 : ℝ))).symm
          _ = ((n + 2 : ℝ)⁻¹)⁻¹ := by rw [h1']
          _ = (n + 2 : ℝ) := inv_inv (a := (n + 2 : ℝ))
      have h3 : (m : ℝ) = (n : ℝ) := by linarith
      exact_mod_cast h3
    exact Set.infinite_of_injective_forall_mem hu_inj hu_mem
  have hroots : Set.Infinite {x : ℝ | g.eval x = 0} := by
    apply Set.Infinite.mono (s := Set.Ioo (-1 : ℝ) 1)
    · intro x hx
      exact hpoint x hx
    · exact hinf_oo
  have hg0 : g = 0 := by
    exact Polynomial.eq_zero_of_infinite_isRoot g (by simpa [Polynomial.IsRoot] using hroots)
  have hder : f.derivative = C α := sub_eq_zero.mp hg0
  have hanti : (C α * X + C (f.coeff 0)).derivative = C α := by
    simp
  have hdif : (f - (C α * X + C (f.coeff 0))).derivative = 0 := by
    rw [Polynomial.derivative_sub, hder, hanti]
    simp
  have hdifC : f - (C α * X + C (f.coeff 0)) = C ((f - (C α * X + C (f.coeff 0))).coeff 0) :=
    Polynomial.eq_C_of_derivative_eq_zero hdif
  have hcoeff0 : ((f - (C α * X + C (f.coeff 0))).coeff 0) = 0 := by
    simp
  have hfeq : f = C α * X + C (f.coeff 0) := by
    have hzero : f - (C α * X + C (f.coeff 0)) = 0 := by
      rw [hdifC, hcoeff0]
      simp
    exact sub_eq_zero.mp hzero
  rw [hfeq]
  refine Submodule.mem_span_pair.mpr ?_
  refine ⟨f.coeff 0, α, ?_⟩
  rw [Polynomial.smul_eq_C_mul, Polynomial.smul_eq_C_mul]
  ring

/-- Theorem "radical" (polynomial version): the radical of the limiting
pairing `(·, ·)_0` is exactly `span {1, x}`. -/
theorem radical_pair0 (f : Polynomial ℝ) :
    pair0 f f = 0 ↔ f ∈ Submodule.span ℝ ({1, X} : Set (Polynomial ℝ)) := by
  constructor
  · exact pair0_self_eq_zero_imp_affine f
  · intro hf
    rcases (Submodule.mem_span_pair.mp hf) with ⟨a, b, hfab⟩
    rw [← hfab]
    rw [Polynomial.smul_eq_C_mul, Polynomial.smul_eq_C_mul]
    simpa [mul_one] using pair0_affine a b a b
/-! ## Krein-Sobolev polynomials: definition and exact low modes -/

/-- `S_n = P_n - P_{n-2}` (source Section 4). -/
noncomputable def sN (n : ℕ) : Polynomial ℝ :=
  legendreClosed n - legendreClosed (n - 2)

/-- The Krein-Sobolev polynomial `K_n^{(c)} = a_n S_n + K_{n-2}^{(c)}` with
`K_0 = 1`, `K_1 = x` (source (19)). -/
noncomputable def kS (c : ℝ) : ℕ → Polynomial ℝ
  | 0 => 1
  | 1 => X
  | n + 2 => C (aSeq c (n + 2)) * sN (n + 2) + kS c n

lemma legendreClosed_zero : legendreClosed 0 = 1 := by
  simp [legendreClosed, legendreCoeff]

lemma legendreClosed_one : legendreClosed 1 = X := by
  simp [legendreClosed, legendreCoeff]
  rw [← mul_assoc, ← Polynomial.C_mul]
  norm_num

theorem kS_zero (c : ℝ) : kS c 0 = 1 := rfl

theorem kS_one (c : ℝ) : kS c 1 = X := rfl

/-- `K_2 = P_2` is c-independent (source Theorem "low"). -/
theorem kS_two (c : ℝ) : kS c 2 = legendreClosed 2 := by
  unfold kS
  simp [sN, aSeq_two, legendreClosed_zero, kS_zero]

/-- `K_3 = P_3` is c-independent (source Theorem "low"). -/
theorem kS_three (c : ℝ) : kS c 3 = legendreClosed 3 := by
  unfold kS
  simp [sN, aSeq_three, legendreClosed_one, kS_one]

/-- `a_5 = 1 + 35/c` (source Theorem "low"). -/
theorem aSeq_five (c : ℝ) : aSeq c 5 = 1 + 35 / c := by
  norm_num [aSeq, aSeq_one, aSeq_three]

/-- `a_6 = 1 + 105/c + 945/c^2` (source Theorem "high"). -/
theorem aSeq_six (c : ℝ) : aSeq c 6 = 1 + 105 / c + 945 / c ^ 2 := by
  norm_num [aSeq, aSeq_four, aSeq_two]
  ring_nf

/-! ## Low-mode norm identities (Theorem "low") -/

/-- `||K_0||^2 = 2c`. -/
theorem kS_norm_zero {c : ℝ} (hK : KreinSobolevFacts c (kS c)) :
    h1PairingPoly c (kS c 0) (kS c 0) = 2 * c := by
  have h := hK.1 0 0
  simp [aSeq_zero, aSeq_two] at h
  simpa [kS_zero] using h

/-- `||K_1||^2 = 2c/3`. -/
theorem kS_norm_one {c : ℝ} (hK : KreinSobolevFacts c (kS c)) :
    h1PairingPoly c (kS c 1) (kS c 1) = 2 * c / 3 := by
  have h := hK.1 1 1
  simp [aSeq_one, aSeq_three, kS_one] at h
  have hcalc : 2 * c / (2 + 1) = 2 * c / 3 := by norm_num
  rw [hcalc] at h
  exact h

/-- `||K_2||^2 = 6 + 2c/5` (converges to 6 as c -> 0). -/
theorem kS_norm_two {c : ℝ} (hc : c ≠ 0) (hK : KreinSobolevFacts c (kS c)) :
    h1PairingPoly c (kS c 2) (kS c 2) = 6 + 2 * c / 5 := by
  have h := hK.1 2 2
  simp [aSeq_two, aSeq_four] at h
  have hcalc : 2 * c / (2 * 2 + 1) * (1 + 15 / c) = 6 + 2 * c / 5 := by
    field_simp [hc]
    ring
  rw [hcalc] at h
  exact h

/-- `||K_3||^2 = 10 + 2c/7` (converges to 10 as c -> 0). -/
theorem kS_norm_three {c : ℝ} (hc : c ≠ 0) (hK : KreinSobolevFacts c (kS c)) :
    h1PairingPoly c (kS c 3) (kS c 3) = 10 + 2 * c / 7 := by
  have h := hK.1 3 3
  simp [aSeq_three, aSeq_five] at h
  have hcalc : 2 * c / (2 * 3 + 1) * (1 + 35 / c) = 10 + 2 * c / 7 := by
    field_simp [hc]
    ring
  rw [hcalc] at h
  exact h

/-- `||K_4||^2 = (2c + 240 + 5040/c + 28350/c^2)/9` (closed form of Theorem
"high" for n = 4). -/
theorem kS_norm_four {c : ℝ} (hc : c ≠ 0) (hK : KreinSobolevFacts c (kS c)) :
    h1PairingPoly c (kS c 4) (kS c 4) = (2 * c + 240 + 5040 / c + 28350 / c ^ 2) / 9 := by
  have h := hK.1 4 4
  simp [aSeq_four, aSeq_six] at h
  have hcalc : 2 * c / (2 * 4 + 1) * (1 + 15 / c) * (1 + 105 / c + 945 / c ^ 2)
      = (2 * c + 240 + 5040 / c + 28350 / c ^ 2) / 9 := by
    field_simp [hc]
    ring
  rw [hcalc] at h
  exact h

/-! ## Divergence of the high norms (Theorem "high", n = 4) -/

/-- `1/x -> +infinity` as `x -> 0+`. -/
lemma tendsto_inv_nhdsWithin_0_pos_atTop :
    Tendsto (fun x : ℝ => 1 / x) (𝓝[>] (0 : ℝ)) atTop := by
  rw [tendsto_atTop]
  intro M
  by_cases hM : M ≤ 0
  · change ({x : ℝ | M ≤ 1 / x} ∈ 𝓝[>] (0 : ℝ))
    rw [Metric.mem_nhdsWithin_iff]
    refine ⟨1, by norm_num, ?_⟩
    intro x hx
    rcases hx with ⟨hxball, hxpos⟩
    have hxinv : 0 < 1 / x := div_pos zero_lt_one hxpos
    exact le_of_lt (lt_of_le_of_lt hM hxinv)
  · have hM' : 0 < M := lt_of_not_ge hM
    change ({x : ℝ | M ≤ 1 / x} ∈ 𝓝[>] (0 : ℝ))
    rw [Metric.mem_nhdsWithin_iff]
    refine ⟨1 / M, div_pos zero_lt_one hM', ?_⟩
    intro x hx
    rcases hx with ⟨hxball, hxpos⟩
    have hxabs : |x| < 1 / M := by
      simpa [Real.dist_eq] using (Metric.mem_ball.mp hxball)
    have hxlt : x < 1 / M := by
      rwa [abs_of_nonneg (le_of_lt hxpos)] at hxabs
    have hMx : M * x < 1 := by
      have h1 : M * x < M * (1 / M) := mul_lt_mul_of_pos_left hxlt hM'
      have h2 : M * (1 / M) = 1 := by
        simp [mul_inv_cancel₀ (ne_of_gt hM')]
      rwa [h2] at h1
    have hMlt : M < 1 / x := by
      rw [lt_div_iff₀ hxpos]
      exact hMx
    exact le_of_lt hMlt

/-- `1/x^2 -> +infinity` as `x -> 0+` (dominates `1/x` for `0 < x <= 1`). -/
lemma tendsto_one_div_sq_nhdsWithin_0_pos_atTop :
    Tendsto (fun x : ℝ => 1 / x ^ 2) (𝓝[>] (0 : ℝ)) atTop := by
  refine tendsto_atTop_mono' (𝓝[>] (0 : ℝ)) ?hle tendsto_inv_nhdsWithin_0_pos_atTop
  change ({x : ℝ | 1 / x ≤ 1 / x ^ 2} ∈ 𝓝[>] (0 : ℝ))
  rw [Metric.mem_nhdsWithin_iff]
  refine ⟨1, by norm_num, ?_⟩
  intro x hx
  rcases hx with ⟨hxball, hxpos⟩
  have hxabs : |x| < 1 := by
    simpa [Real.dist_eq] using (Metric.mem_ball.mp hxball)
  have hxlt : x < 1 := by
    rwa [abs_of_nonneg (le_of_lt hxpos)] at hxabs
  have hx2le : x ^ 2 ≤ x := by
    have h1 : x * x ≤ x * 1 := mul_le_mul_of_nonneg_left (le_of_lt hxlt) (le_of_lt hxpos)
    simpa [pow_two] using h1
  exact one_div_le_one_div_of_le (sq_pos_of_pos hxpos) hx2le

/-- Sum of two `atTop` limits is `atTop` (on a common filter). -/
lemma tendsto_add_atTop {l : Filter ℝ} {f g : ℝ → ℝ}
    (hf : Tendsto f l atTop) (hg : Tendsto g l atTop) :
    Tendsto (fun x => f x + g x) l atTop := by
  rw [tendsto_atTop]
  intro b
  filter_upwards [tendsto_atTop.1 hf (b / 2), tendsto_atTop.1 hg (b / 2)] with x hfx hgx
  linarith

/-- `||K_4||^2 -> +infinity` as `c -> 0+` (Theorem "high", n = 4). -/
theorem tendsto_norm_four_atTop (hK : ∀ c : ℝ, KreinSobolevFacts c (kS c)) :
    Tendsto (fun c : ℝ => h1PairingPoly c (kS c 4) (kS c 4)) (𝓝[>] 0) atTop := by
  have hsplit : ∀ c : ℝ,
      (2 * c + 240 + 5040 / c + 28350 / c ^ 2) / 9
        = 3150 / c ^ 2 + (2 * c + 240 + 5040 / c) / 9 := by
    intro c
    ring_nf
  have hcongr : (fun c : ℝ => h1PairingPoly c (kS c 4) (kS c 4))
      =ᶠ[𝓝[>] (0 : ℝ)] (fun c : ℝ => 3150 / c ^ 2 + (2 * c + 240 + 5040 / c) / 9) := by
    filter_upwards [self_mem_nhdsWithin] with c hc
    have hne : c ≠ 0 := ne_of_gt hc
    rw [kS_norm_four hne (hK c), hsplit c]
  have h1 : Tendsto (fun c : ℝ => 3150 / c ^ 2) (𝓝[>] 0) atTop := by
    have h := tendsto_one_div_sq_nhdsWithin_0_pos_atTop.const_mul_atTop
      (by norm_num : (0 : ℝ) < 3150)
    simpa [div_eq_mul_inv] using h
  have h2 : Tendsto (fun c : ℝ => (2 * c + 240 + 5040 / c) / 9) (𝓝[>] 0) atTop := by
    have hbg : Tendsto (fun c : ℝ => 560 / c) (𝓝[>] 0) atTop := by
      have h := tendsto_inv_nhdsWithin_0_pos_atTop.const_mul_atTop
        (by norm_num : (0 : ℝ) < 560)
      simpa [div_eq_mul_inv] using h
    refine tendsto_atTop_mono' (𝓝[>] 0) ?hle hbg
    change ({c : ℝ | 560 / c ≤ (2 * c + 240 + 5040 / c) / 9} ∈ 𝓝[>] (0 : ℝ))
    rw [Metric.mem_nhdsWithin_iff]
    refine ⟨1, by norm_num, ?_⟩
    intro c hc
    rcases hc with ⟨_, hcpos⟩
    have hcpos' : 0 < c := by simpa using hcpos
    have hcalc : (2 * c + 240 + 5040 / c) / 9 = (240 + 2 * c) / 9 + 560 / c := by
      field_simp [ne_of_gt hcpos']
      ring
    change 560 / c ≤ (2 * c + 240 + 5040 / c) / 9
    rw [hcalc]
    have hnonneg : 0 ≤ (240 + 2 * c) / 9 := div_nonneg (by nlinarith) (by norm_num)
    exact le_add_of_nonneg_left hnonneg
  have hmain : Tendsto (fun c : ℝ => 3150 / c ^ 2 + (2 * c + 240 + 5040 / c) / 9)
      (𝓝[>] 0) atTop := tendsto_add_atTop h1 h2
  exact (Filter.tendsto_congr' hcongr).2 hmain
/-! ## The span decomposition of the quotient (Theorem "complete" (a)) -/

/-- `deg S_n = n` for `n >= 2`. -/
theorem sN_natDegree {n : ℕ} (hn : 2 ≤ n) : (sN n).natDegree = n := by
  unfold sN
  apply Polynomial.natDegree_eq_of_le_of_coeff_ne_zero
  · have hle1 : (legendreClosed n).natDegree ≤ n :=
      le_of_eq (natDegree_legendreClosed n)
    have hle2 : (legendreClosed (n - 2)).natDegree ≤ n := by
      exact le_trans (le_of_eq (natDegree_legendreClosed (n - 2)))
        (by exact_mod_cast (Nat.sub_le n 2))
    exact le_trans (Polynomial.natDegree_sub_le _ _) (max_le_iff.mpr ⟨hle1, hle2⟩)
  · rw [Polynomial.coeff_sub]
    have h2 : (legendreClosed (n - 2)).coeff n = 0 := by
      exact Polynomial.coeff_eq_zero_of_natDegree_lt
        (lt_of_le_of_lt (le_of_eq (natDegree_legendreClosed (n - 2))) (by omega))
    rw [h2, sub_zero]
    have hdeg : (legendreClosed n).natDegree = n := natDegree_legendreClosed n
    have hne0 : legendreClosed n ≠ 0 := by
      intro hz
      rw [hz, Polynomial.natDegree_zero] at hdeg
      omega
    have hlc : (legendreClosed n).leadingCoeff ≠ 0 := by
      intro hlc0
      exact hne0 (Polynomial.leadingCoeff_eq_zero.mp hlc0)
    simpa [hdeg] using ne_of_eq_of_ne (Polynomial.coeff_natDegree (p := legendreClosed n)) hlc

/-- Every polynomial `p` lies in the span of `{1, x}` together with
`{S_n : 2 <= n <= deg p}`.  This is the exact polynomial version of the
decomposition `Pi_N = span{1,x} + span{S_2, ..., S_N}` of the source
(Theorem "complete" (a)). -/
theorem poly_mem_span_quotient (p : Polynomial ℝ) :
    p ∈ Submodule.span ℝ (({1, X} : Set (Polynomial ℝ)) ∪ {sN n | n ∈ Set.Icc 2 p.natDegree}) := by
  let S : Set (Polynomial ℝ) := {1, X}
  have hmain : ∀ N : ℕ,
      (∀ k < N, ∀ q : Polynomial ℝ, q.natDegree ≤ k →
        q ∈ Submodule.span ℝ (S ∪ {sN n | n ∈ Set.Icc 2 k})) →
      ∀ q : Polynomial ℝ, q.natDegree ≤ N →
        q ∈ Submodule.span ℝ (S ∪ {sN n | n ∈ Set.Icc 2 N}) := by
    intro N ih q hqdeg
    by_cases hN : q.natDegree ≤ 1
    · -- q is affine: q = c0 + c1 x in span{1, x}
      have hspan : q ∈ Submodule.span ℝ S := by
        refine Submodule.mem_span_pair.mpr ?_
        refine ⟨q.coeff 0, q.coeff 1, ?_⟩
        rw [Polynomial.smul_eq_C_mul, Polynomial.smul_eq_C_mul]
        ext k
        by_cases hk : k = 0
        · subst k
          simp
        · by_cases hk1 : k = 1
          · subst k
            simp
          · rw [Polynomial.coeff_add, Polynomial.coeff_C_mul, Polynomial.coeff_C_mul]
            rw [Polynomial.coeff_one, Polynomial.coeff_X]
            simp [hk, hk1, eq_comm]
            rw [eq_comm]
            apply Polynomial.coeff_eq_zero_of_natDegree_lt
            omega
      exact Submodule.span_mono
        (Set.subset_union_left (s := S) (t := {sN n | n ∈ Set.Icc 2 N})) hspan
    · -- q.natDegree >= 2: leading-term elimination
      let m : ℕ := q.natDegree
      have hm : 2 ≤ m := by dsimp [m]; omega
      have hmN : m ≤ N := by dsimp [m]; exact hqdeg
      have hlc : (sN m).coeff m ≠ 0 := by
        have hdeg : (sN m).natDegree = m := sN_natDegree hm
        have hne0 : sN m ≠ 0 := by
          intro hz
          rw [hz, Polynomial.natDegree_zero] at hdeg
          omega
        have hlc0 : (sN m).leadingCoeff ≠ 0 := by
          intro h
          exact hne0 (Polynomial.leadingCoeff_eq_zero.mp h)
        simpa [hdeg] using ne_of_eq_of_ne (Polynomial.coeff_natDegree (p := sN m)) hlc0
      let c : ℝ := q.coeff m / (sN m).coeff m
      let q' : Polynomial ℝ := q - c • sN m
      have hdeg' : q'.natDegree < m := by
        have hle' : q'.natDegree ≤ m - 1 := by
          rw [Polynomial.natDegree_le_iff_coeff_eq_zero]
          intro k hk
          have hmk : m ≤ k := by omega
          rw [Polynomial.coeff_sub, Polynomial.coeff_smul]
          by_cases hkm : k = m
          · subst k
            dsimp [q', c]
            field_simp [hlc]
            ring
          · have hkm' : m < k := by omega
            have hqk : q.coeff k = 0 :=
              Polynomial.coeff_eq_zero_of_natDegree_lt hkm'
            have hsk : (sN m).coeff k = 0 :=
              Polynomial.coeff_eq_zero_of_natDegree_lt
                (lt_of_le_of_lt (le_of_eq (sN_natDegree hm)) hkm')
            rw [hqk, hsk]
            ring
        exact lt_of_le_of_lt hle' (by omega)
      have hq' : q' ∈ Submodule.span ℝ (S ∪ {sN n | n ∈ Set.Icc 2 q'.natDegree}) :=
        ih q'.natDegree (lt_of_lt_of_le hdeg' hmN) q' (le_rfl)
      have hmono : Submodule.span ℝ (S ∪ {sN n | n ∈ Set.Icc 2 q'.natDegree})
          ≤ Submodule.span ℝ (S ∪ {sN n | n ∈ Set.Icc 2 N}) := by
        apply Submodule.span_mono
        intro x hx
        rcases hx with hxS | hxS
        · exact Set.mem_union_left {sN n | n ∈ Set.Icc 2 N} hxS
        · rcases hxS with ⟨n, hmem, hfn⟩
          refine Set.mem_union_right S ⟨n, ?_, hfn⟩
          exact ⟨hmem.1, le_trans hmem.2 (le_trans (le_of_lt hdeg') hmN)⟩
      have hsN : sN m ∈ Submodule.span ℝ (S ∪ {sN n | n ∈ Set.Icc 2 N}) := by
        exact Submodule.subset_span
          (Set.mem_union_right S ⟨m, ⟨hm, hmN⟩, rfl⟩)
      have hcS : c • sN m ∈ Submodule.span ℝ (S ∪ {sN n | n ∈ Set.Icc 2 N}) :=
        Submodule.smul_mem _ c hsN
      have hq'in : q' ∈ Submodule.span ℝ (S ∪ {sN n | n ∈ Set.Icc 2 N}) :=
        hmono hq'
      have hqeq : q = q' + c • sN m := by
        dsimp [q']
        ring
      rw [hqeq]
      exact Submodule.add_mem _ hq'in hcS
  have hres := Nat.strong_induction_on (p := fun N => ∀ q : Polynomial ℝ,
      q.natDegree ≤ N → q ∈ Submodule.span ℝ (S ∪ {sN n | n ∈ Set.Icc 2 N}))
      p.natDegree hmain
  exact hres p le_rfl

end
end KreinDegenerateLimit

end SL
