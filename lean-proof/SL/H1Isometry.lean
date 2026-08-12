import Mathlib
import SL.H3Completeness

/-!
# H^3 isometry glue: FTC and the H1 inner product

Formalization of the analytic glue of `docs/SL_h3_completeness_proof.tex`
(Section 2, Lemma 2 "isometry"; Section 4, Lemma 4 "H-moment recurrence";
Section 6, main theorem): the identification of the H1-moment functional with
the actual H1 inner product of the source, and the positive-definiteness core
of the H1 norm.

Concretely:

1. FTC glue (`ftc_delta`): for w differentiable on [-1,1] with derivative wd
   (`deriv w = wd`, wd continuous), `∫_{-1}^1 wd = w(1) - w(-1) = Δw`.
2. `h1Inner`: the H1 inner-product functional of the source
   `(w, p)_1 = ∫ wd·p' + c·∫ w·p - (1/2)·Δw·Δp` with the explicit boundary
   term `Δw = w(1) - w(-1)`.  `h1Inner_eq_h1MomentFunctional` shows that,
   given the FTC, this equals the functional `h1MomentFunctional` used in the
   moment machinery (SL/H3MomentBound.lean).
3. `h1Inner_moments_zero_of_orthogonal`: orthogonality of w against
   `{K_c p_n}` in the true H1 inner product forces all H1-moments to vanish
   (the isometry-transport step of the main theorem, source Lemma 2 + Lemma 4).
4. `h1Inner_eq_zero_of_orthogonal`: the assembled H1-side closure
   `(w, p)_1 = 0` for every polynomial p.
5. Positive-definiteness core: `(Δw)^2 ≤ 2·∫ wd^2` (Cauchy-Schwarz) and
   vanishing of the H1 norm-square expression
   `N_1(w) = ∫ wd^2 + c·∫ w^2 - (1/2)·(Δw)^2` forces `w = 0` almost
   everywhere (the "p -> w" step of the source main theorem, without the
   density argument).

Honesty note: the operator-level isometry (K_c: H^3 -> H^1 is a bijection,
`0 ∉ σ(K_c)`, Lemma 1 of the source) requires spectral theory and is NOT
formalized here; what is formalized is the concrete functional identification
and the positive-definiteness core used in the main theorem.  The density of
polynomials in H^1 (the step `p -> w` of the source) is also not formalized;
the moment-level closure `M(p) = 0` for all polynomials is provided
(`eq_zero_of_moments_zero`), and `h1NormSq_eq_zero_imp_ae_zero` closes the
definiteness step.  The H^s transfer (source Section 7) is out of scope here.
-/

namespace SL

namespace H1Isometry

open Polynomial

open scoped Real Interval
open MeasureTheory

/-! ## FTC glue -/

/-- FTC glue: `∫_{-1}^1 wd = w(1) - w(-1)` when wd is the derivative of w
(`deriv w = wd`), w is differentiable on the closed interval and wd is
continuous there.  This is the identity `Δw = ∫ w' dx` of the source. -/
lemma ftc_delta (w wd : ℝ → ℝ) (hderiv : deriv w = wd)
    (hdiff : ∀ x ∈ Set.uIcc (-1) 1, DifferentiableAt ℝ w x)
    (hcont : ContinuousOn wd (Set.Icc (-1) 1)) :
    MomentBound.moments wd 0 = w 1 - w (-1) := by
  unfold MomentBound.moments
  have hcont' : ContinuousOn wd (Set.uIcc (-1) 1) := by
    have hmin : min (-1 : ℝ) 1 = -1 := by norm_num
    have hmax : max (-1 : ℝ) 1 = 1 := by norm_num
    simpa [Set.uIcc, hmin, hmax] using hcont
  simpa using (intervalIntegral.integral_deriv_eq_sub' w hderiv hdiff hcont')

/-! ## H1 inner product identification -/

/-- The H1 inner-product functional of the source:
`(w, p)_1 = ∫ wd·p' + c·∫ w·p - (1/2)·Δw·Δp` with the explicit boundary term
`Δw = w(1) - w(-1)`. -/
noncomputable def h1Inner (w wd : ℝ → ℝ)
    (hw : ContinuousOn w (Set.Icc (-1) 1)) (hwd : ContinuousOn wd (Set.Icc (-1) 1))
    (c : ℝ) : Polynomial ℝ →ₗ[ℝ] ℝ :=
  (Completeness.momentFunctional wd hwd).comp Polynomial.derivative
    + c • Completeness.momentFunctional w hw
    + (-(1 / 2) * (w 1 - w (-1))) • H3MomentBound.delta

/-- Given the FTC (`∫ wd = Δw`), the H1 inner-product functional coincides
with the H1-moment functional used in the moment machinery. -/
lemma h1Inner_eq_h1MomentFunctional {w wd : ℝ → ℝ}
    (hw : ContinuousOn w (Set.Icc (-1) 1)) (hwd : ContinuousOn wd (Set.Icc (-1) 1))
    (c : ℝ) (hftc : MomentBound.moments wd 0 = w 1 - w (-1)) :
    h1Inner w wd hw hwd c = H3MomentBound.h1MomentFunctional w wd hw hwd c := by
  ext p
  unfold h1Inner H3MomentBound.h1MomentFunctional
  simp only [LinearMap.add_apply, LinearMap.comp_apply, LinearMap.smul_apply]
  have hcoef : -(1 / 2 : ℝ) * (w 1 - w (-1)) = -(1 / 2) * MomentBound.moments wd 0 := by
    rw [hftc]
  rw [hcoef]

/-- Orthogonality of w against `{K_c p_n}` in the true H1 inner product (with
the FTC-supplied boundary term) forces all H1-moments to vanish.  This is the
isometry-transport step of the source's main theorem. -/
theorem h1Inner_moments_zero_of_orthogonal {w wd : ℝ → ℝ}
    (hw : ContinuousOn w (Set.Icc (-1) 1)) (hwd : ContinuousOn wd (Set.Icc (-1) 1))
    (hderiv : deriv w = wd)
    (hdiff : ∀ x ∈ Set.uIcc (-1) 1, DifferentiableAt ℝ w x)
    {c : ℝ} (hc : 0 < c)
    (h0 : H3Completeness.moments (h1Inner w wd hw hwd c) 0 = 0)
    (h1 : H3Completeness.moments (h1Inner w wd hw hwd c) 1 = 0)
    (horthE : ∀ n : ℕ, 2 ≤ n →
      h1Inner w wd hw hwd c (Completeness.KcR c (Completeness.pEvenR n)) = 0)
    (horthO : ∀ n : ℕ, 2 ≤ n →
      h1Inner w wd hw hwd c (Completeness.KcR c (Completeness.pOddR n)) = 0) :
    ∀ k : ℕ, H3Completeness.moments (h1Inner w wd hw hwd c) k = 0 := by
  have hftc : MomentBound.moments wd 0 = w 1 - w (-1) := ftc_delta w wd hderiv hdiff hwd
  have hid : h1Inner w wd hw hwd c = H3MomentBound.h1MomentFunctional w wd hw hwd c :=
    h1Inner_eq_h1MomentFunctional hw hwd c hftc
  rw [hid] at h0 h1 horthE horthO ⊢
  exact H3Completeness.h1_moments_zero_of_orthogonal hw hwd hc h0 h1 horthE horthO

/-! ## Moment-level closure on polynomials -/

/-- If all moments of a functional vanish then the functional vanishes on
every polynomial. -/
lemma eq_zero_of_moments_zero {M : Polynomial ℝ →ₗ[ℝ] ℝ}
    (hzero : ∀ k : ℕ, M (X ^ k) = 0) (p : Polynomial ℝ) : M p = 0 := by
  refine Polynomial.induction_on' p ?_ ?_
  · intro p q hp hq
    rw [map_add, hp, hq, add_zero]
  · intro n a
    rw [← Polynomial.C_mul_X_pow_eq_monomial]
    have h := H3Completeness.apply_C_mul_X_pow M a n
    simp [H3Completeness.moments, hzero]

/-- Assembled H1-side closure: orthogonality of `(w, ·)_1` against `{K_c p_n}`
(equivalently, by the isometry `(K_c f, K_c g)_1 = (f, g)_3`, the H3-
orthogonality hypotheses of the main theorem) forces `(w, p)_1 = 0` for every
polynomial p. -/
theorem h1Inner_eq_zero_of_orthogonal {w wd : ℝ → ℝ}
    (hw : ContinuousOn w (Set.Icc (-1) 1)) (hwd : ContinuousOn wd (Set.Icc (-1) 1))
    (hderiv : deriv w = wd)
    (hdiff : ∀ x ∈ Set.uIcc (-1) 1, DifferentiableAt ℝ w x)
    {c : ℝ} (hc : 0 < c)
    (h0 : H3Completeness.moments (h1Inner w wd hw hwd c) 0 = 0)
    (h1 : H3Completeness.moments (h1Inner w wd hw hwd c) 1 = 0)
    (horthE : ∀ n : ℕ, 2 ≤ n →
      h1Inner w wd hw hwd c (Completeness.KcR c (Completeness.pEvenR n)) = 0)
    (horthO : ∀ n : ℕ, 2 ≤ n →
      h1Inner w wd hw hwd c (Completeness.KcR c (Completeness.pOddR n)) = 0) :
    ∀ p : Polynomial ℝ, h1Inner w wd hw hwd c p = 0 := by
  have hz := h1Inner_moments_zero_of_orthogonal hw hwd hderiv hdiff hc h0 h1 horthE horthO
  intro p
  exact eq_zero_of_moments_zero (fun k => by simpa [H3Completeness.moments] using hz k) p

/-! ## Positive definiteness of the H1 norm -/

/-- Cauchy-Schwarz core: `(∫_{-1}^1 wd)^2 ≤ 2·∫ wd^2` (constant function 1). -/
lemma moments_zero_sq_le (wd : ℝ → ℝ) (hwd : ContinuousOn wd (Set.Icc (-1) 1)) :
    (MomentBound.moments wd 0) ^ 2 ≤ 2 * (∫ x in (-1 : ℝ)..1, wd x ^ 2) := by
  have h := MomentBound.cs_moment hwd 0
  have hm : (∫ x in (-1 : ℝ)..1, wd x * x ^ 0) = MomentBound.moments wd 0 := by
    unfold MomentBound.moments
    apply intervalIntegral.integral_congr
    intro x hx
    simp
  have hx : (∫ x in (-1 : ℝ)..1, x ^ (2 * 0)) = 2 := by
    rw [MomentBound.integral_x_pow_even 0]
    norm_num
  rw [hm, hx] at h
  nlinarith

/-- `(Δw)^2 ≤ 2·∫ wd^2` by Cauchy-Schwarz and the FTC. -/
lemma delta_sq_le_two_int_sq {w wd : ℝ → ℝ} (hwd : ContinuousOn wd (Set.Icc (-1) 1))
    (hftc : MomentBound.moments wd 0 = w 1 - w (-1)) :
    (w 1 - w (-1)) ^ 2 ≤ 2 * (∫ x in (-1 : ℝ)..1, wd x ^ 2) := by
  rw [← hftc]
  exact moments_zero_sq_le wd hwd

/-- The H1 norm-square expression of the source:
`N_1(w) = ∫ wd^2 + c·∫ w^2 - (1/2)·(Δw)^2` with `Δw = w(1) - w(-1)`. -/
noncomputable def h1NormSq (w wd : ℝ → ℝ) (c : ℝ) : ℝ :=
  (∫ x in (-1 : ℝ)..1, wd x ^ 2) + c * (∫ x in (-1 : ℝ)..1, w x ^ 2)
    - (1 / 2) * (w 1 - w (-1)) ^ 2

/-- The H1 norm-square is nonnegative (positive-definiteness core):
`(1/2)(Δw)^2 ≤ ∫ wd^2` by Cauchy-Schwarz, and the remaining terms are
nonnegative for c ≥ 0. -/
theorem h1NormSq_nonneg {w wd : ℝ → ℝ} (_hw : ContinuousOn w (Set.Icc (-1) 1))
    (hwd : ContinuousOn wd (Set.Icc (-1) 1)) {c : ℝ} (hc : 0 ≤ c)
    (hftc : MomentBound.moments wd 0 = w 1 - w (-1)) :
    0 ≤ h1NormSq w wd c := by
  have hcs := delta_sq_le_two_int_sq hwd hftc
  have hw2 : 0 ≤ (∫ x in (-1 : ℝ)..1, w x ^ 2) := by
    exact intervalIntegral.integral_nonneg (by norm_num : (-1 : ℝ) ≤ 1)
      (by intro x hx; exact sq_nonneg _)
  have hwd2 : 0 ≤ (∫ x in (-1 : ℝ)..1, wd x ^ 2) := by
    exact intervalIntegral.integral_nonneg (by norm_num : (-1 : ℝ) ≤ 1)
      (by intro x hx; exact sq_nonneg _)
  unfold h1NormSq
  nlinarith

/-- If the H1 norm-square vanishes then `∫ w^2 = 0` (hence `w = 0` a.e. by
continuity): the "w = 0" definiteness step of the source's main theorem. -/
theorem h1NormSq_eq_zero_imp_sq_int_zero {w wd : ℝ → ℝ}
    (_hw : ContinuousOn w (Set.Icc (-1) 1)) (hwd : ContinuousOn wd (Set.Icc (-1) 1))
    {c : ℝ} (hc : 0 < c)
    (hftc : MomentBound.moments wd 0 = w 1 - w (-1))
    (h : h1NormSq w wd c = 0) :
    (∫ x in (-1 : ℝ)..1, w x ^ 2) = 0 := by
  have hcs := delta_sq_le_two_int_sq hwd hftc
  have hB : 0 ≤ (∫ x in (-1 : ℝ)..1, w x ^ 2) := by
    exact intervalIntegral.integral_nonneg (by norm_num : (-1 : ℝ) ≤ 1)
      (by intro x hx; exact sq_nonneg _)
  have hcB0 : c * (∫ x in (-1 : ℝ)..1, w x ^ 2) = 0 := by
    have hle0 : c * (∫ x in (-1 : ℝ)..1, w x ^ 2) ≤ 0 := by
      unfold h1NormSq at h
      nlinarith
    have hge0 : 0 ≤ c * (∫ x in (-1 : ℝ)..1, w x ^ 2) := mul_nonneg (le_of_lt hc) hB
    linarith
  exact (mul_eq_zero.mp hcB0).resolve_left (ne_of_gt hc)

/-- The H1-side "w = 0" conclusion: a continuous w with vanishing H1
norm-square is zero almost everywhere on (-1,1). -/
theorem h1NormSq_eq_zero_imp_ae_zero {w wd : ℝ → ℝ}
    (hw : ContinuousOn w (Set.Icc (-1) 1)) (hwd : ContinuousOn wd (Set.Icc (-1) 1))
    {c : ℝ} (hc : 0 < c)
    (hftc : MomentBound.moments wd 0 = w 1 - w (-1))
    (h : h1NormSq w wd c = 0) :
    w =ᵐ[volume.restrict (Set.Ioc (-1) 1)] 0 := by
  have hI : (∫ x in (-1 : ℝ)..1, w x ^ 2) = 0 :=
    h1NormSq_eq_zero_imp_sq_int_zero hw hwd hc hftc h
  have hIoc : (∫ x in Set.Ioc (-1) 1, w x ^ 2) = 0 := by
    rw [intervalIntegral.integral_of_le (by norm_num : (-1 : ℝ) ≤ 1)] at hI
    exact hI
  have hfi : Integrable (fun x : ℝ => w x ^ 2) (volume.restrict (Set.Ioc (-1) 1)) := by
    exact (ContinuousOn.integrableOn_Icc (hw.pow 2)).mono_set Set.Ioc_subset_Icc_self
  have hae : (fun x : ℝ => w x ^ 2) =ᵐ[volume.restrict (Set.Ioc (-1) 1)] 0 :=
    (integral_eq_zero_iff_of_nonneg (by intro x; exact sq_nonneg _) hfi).mp hIoc
  filter_upwards [hae] with x hx
  exact sq_eq_zero_iff.mp hx

end H1Isometry

end SL
