import Mathlib
import SL.Completeness
import SL.StabilityGrowth
import SL.H3Completeness

open scoped BigOperators
open Filter

/-!
# Stability of the moment-jump completeness criterion

Formalization of the stability theorems from
`docs/SL_stability_moment_jump.tex`:

* Theorem 2.2 (稳定性, `stability_moments_zero`): if a Real-linear moment
  functional M on polynomials satisfies the jump-structure orthogonality
  conditions for the triangular family {q_n}, the divergence condition
  sum_{k=2..m} min(eps k, 1) = omega(log m) for both the even and the odd
  coefficient families, and the polynomial moment bounds
  |M(X^k)| <= C * k^beta, then every moment of M vanishes.

* The S-threshold theorem (S-门槛, `superpolynomial_of_logsum`): the same
  conclusion follows from the (weaker) divergence condition
  sum_{k=2..m} log (1 + eps k) = omega(log m), which is the quantity that
  actually controls log u_m.

* Theorem 2.3 (尖锐性, sharpness core): for eps k = C/k (i.e.
  A k - B k = c0 * (1 + C/k) and B k = 0) the recurrence solution is exactly
  prod_{k=2..m} (1 + C/k) (`sharp_product_eq`), grows at most polynomially
  (`sharp_poly_bound`), satisfies the defining recurrence
  (`sharp_recurrence`), and the sharpness series
  sum_m u_m^2 / (2m+1)^(2 beta) converges whenever beta > C + 1/2
  (`sharp_series_summable`).

Note on constants: the source document uses log(1+eps) >= (log 2) * min(eps,1).
We use the elementary bound log(1+eps) >= min(eps,1) / 2 (any positive
constant works for the omega(log m) implication); this is documented in
`log_one_add_min_half`.

The Hilbert-space wrapper (polynomial density (H1) and continuity of the
moment functional (H2) turning "all moments vanish" into "the orthogonal
vector is zero") is the analytic companion of this file, exactly as in
`SL/H3Completeness.lean` where the H1-moment bound is an assumption.
-/

namespace SL

namespace Stability

open Polynomial

/-! ## The key analytic inequality -/

/-- For 0 <= eps, log(1 + eps) >= eps / (1 + eps).  Proved from
`Real.log_lt_sub_one_of_pos` applied to (1 + eps)^(-1). -/
lemma log_one_add_ge_self_div_one_add {eps : ℝ} (heps : 0 ≤ eps) :
    eps / (1 + eps) ≤ Real.log (1 + eps) := by
  by_cases heps0 : eps = 0
  · subst eps
    simp
  · have hpos : 0 < 1 + eps := by linarith
    have hxpos : 0 < (1 + eps)⁻¹ := inv_pos.mpr hpos
    have hxne : (1 + eps)⁻¹ ≠ 1 := by
      intro h
      have hmul := congrArg (fun t : ℝ => (1 + eps) * t) h
      rw [mul_inv_cancel₀ (ne_of_gt hpos)] at hmul
      have : (1 + eps) * 1 = 1 + eps := by ring
      rw [this] at hmul
      have heq : eps = 0 := by linarith
      exact heps0 heq
    have hlt := Real.log_lt_sub_one_of_pos hxpos hxne
    rw [Real.log_inv] at hlt
    have hrew : (1 + eps)⁻¹ - 1 = -(eps / (1 + eps)) := by
      field_simp [ne_of_gt hpos]
      ring
    rw [hrew] at hlt
    have hlt' : eps / (1 + eps) < Real.log (1 + eps) := by linarith
    exact le_of_lt hlt'

/-- The elementary key bound used for the omega(log m) implication:
    min(eps, 1) / 2 <= log(1 + eps) for every eps >= 0.  (The source uses the
    constant log 2; any positive constant suffices.) -/
lemma log_one_add_min_half {eps : ℝ} (heps : 0 ≤ eps) :
    (1 / 2 : ℝ) * min eps 1 ≤ Real.log (1 + eps) := by
  by_cases h1 : 1 ≤ eps
  · have hmin : min eps 1 = 1 := min_eq_right h1
    rw [hmin]
    have hlog2 : (1 / 2 : ℝ) < Real.log 2 := by
      have h := Real.log_two_gt_d9
      norm_num at h ⊢
      linarith
    have hle : Real.log 2 ≤ Real.log (1 + eps) := Real.log_le_log (by norm_num) (by linarith)
    linarith
  · have heps1 : eps ≤ 1 := le_of_not_ge h1
    have hmin : min eps 1 = eps := min_eq_left heps1
    rw [hmin]
    have hpos : 0 < 1 + eps := by linarith
    have hdiv : (1 / 2 : ℝ) * eps ≤ eps / (1 + eps) := by
      calc
        (1 / 2 : ℝ) * eps = eps / 2 := by ring
        _ ≤ eps / (1 + eps) := div_le_div_of_nonneg_left heps hpos (by linarith)
    exact le_trans hdiv (log_one_add_ge_self_div_one_add heps)

/-- Sum form: (1/2) * sum min(eps k, 1) <= log (prod (1 + eps k)). -/
lemma sum_min_half_le_log_prod {s : Finset ℕ} {eps : ℕ → ℝ}
    (heps : ∀ k ∈ s, 0 ≤ eps k) :
    (1 / 2 : ℝ) * (∑ k ∈ s, min (eps k) 1) ≤ Real.log (∏ k ∈ s, (1 + eps k)) := by
  calc
    (1 / 2 : ℝ) * (∑ k ∈ s, min (eps k) 1) = ∑ k ∈ s, (1 / 2 : ℝ) * min (eps k) 1 := by
      rw [Finset.mul_sum]
    _ ≤ ∑ k ∈ s, Real.log (1 + eps k) :=
      Finset.sum_le_sum (fun k hk => log_one_add_min_half (heps k hk))
    _ = Real.log (∏ k ∈ s, (1 + eps k)) := by
      rw [Real.log_prod (s := s) (f := fun k => (1 + eps k))]
      intro k hk
      have : 0 ≤ eps k := heps k hk
      nlinarith

/-- Sum form: sum log (1 + eps k) <= log (prod (1 + eps k)). -/
lemma sum_log_le_log_prod {s : Finset ℕ} {eps : ℕ → ℝ}
    (heps : ∀ k ∈ s, 0 ≤ eps k) :
    (∑ k ∈ s, Real.log (1 + eps k)) ≤ Real.log (∏ k ∈ s, (1 + eps k)) := by
  rw [Real.log_prod (s := s) (f := fun k => (1 + eps k))]
  intro k hk
  have : 0 ≤ eps k := heps k hk
  nlinarith

/-! ## Super-polynomiality from a divergent logarithmic sum -/

/-- log(m) tends to infinity along the naturals. -/
lemma tendsto_log_nat_atTop : Tendsto (fun m : ℕ => Real.log (m : ℝ)) atTop atTop :=
  Real.tendsto_log_atTop.comp tendsto_natCast_atTop_atTop

/-- If S(m)/log m -> infinity, then (1/2) * S(m) - beta * log m -> infinity
for every real beta. -/
lemma tendsto_half_S_sub_beta_log {S : ℕ → ℝ} {β : ℝ}
    (hdiv : Tendsto (fun m : ℕ => S m / Real.log (m : ℝ)) atTop atTop) :
    Tendsto (fun m : ℕ => (1 / 2 : ℝ) * S m - β * Real.log (m : ℝ)) atTop atTop := by
  have hB : Tendsto (fun m : ℕ => (1 / 2 : ℝ) * (S m / Real.log (m : ℝ)) - β) atTop atTop := by
    have h1 : Tendsto (fun m : ℕ => (1 / 2 : ℝ) * (S m / Real.log (m : ℝ))) atTop atTop :=
      Filter.Tendsto.const_mul_atTop' (by norm_num : (0 : ℝ) < 1 / 2) hdiv
    have h2 : Tendsto (fun m : ℕ => -β + (1 / 2 : ℝ) * (S m / Real.log (m : ℝ))) atTop atTop :=
      Filter.tendsto_atTop_add_const_left atTop (-β) h1
    simpa [sub_eq_add_neg, add_comm, add_left_comm, add_assoc] using h2
  have hL := tendsto_log_nat_atTop
  have hP : Tendsto (fun m : ℕ => ((1 / 2 : ℝ) * (S m / Real.log (m : ℝ)) - β) * Real.log (m : ℝ))
      atTop atTop := by
    rw [tendsto_atTop]
    intro X
    have hB1 : ∀ᶠ m in atTop, max 1 (X + 1) ≤ (1 / 2 : ℝ) * (S m / Real.log (m : ℝ)) - β :=
      tendsto_atTop.1 hB (max 1 (X + 1))
    have hL1 : ∀ᶠ m : ℕ in atTop, (1 : ℝ) ≤ Real.log (m : ℝ) := tendsto_atTop.1 hL 1
    refine (hB1.and hL1).mono ?_
    intro m hm
    have hbm : max 1 (X + 1) ≤ (1 / 2 : ℝ) * (S m / Real.log (m : ℝ)) - β := hm.1
    have hlm : (1 : ℝ) ≤ Real.log (m : ℝ) := hm.2
    have hmax0 : (0 : ℝ) ≤ max 1 (X + 1) := le_trans (by norm_num : (0 : ℝ) ≤ 1) (le_max_left 1 (X + 1))
    have hb0 : 0 ≤ (1 / 2 : ℝ) * (S m / Real.log (m : ℝ)) - β := by linarith [hbm, hmax0]
    have hl0 : 0 ≤ Real.log (m : ℝ) := by linarith
    have hmul : max 1 (X + 1) * 1 ≤
        ((1 / 2 : ℝ) * (S m / Real.log (m : ℝ)) - β) * Real.log (m : ℝ) :=
      mul_le_mul hbm hlm (by norm_num : (0 : ℝ) ≤ 1) hb0
    calc
      X ≤ X + 1 := by linarith
      _ ≤ max 1 (X + 1) := le_max_right 1 (X + 1)
      _ = max 1 (X + 1) * 1 := by ring
      _ ≤ ((1 / 2 : ℝ) * (S m / Real.log (m : ℝ)) - β) * Real.log (m : ℝ) := hmul
  refine hP.congr' ?_
  filter_upwards [eventually_ge_atTop 2] with m hm
  have hlog : Real.log (m : ℝ) ≠ 0 := by
    have hm1 : 1 < (m : ℝ) := by exact_mod_cast (by omega : 1 < m)
    exact ne_of_gt (Real.log_pos hm1)
  calc
    ((1 / 2 : ℝ) * (S m / Real.log (m : ℝ)) - β) * Real.log (m : ℝ)
        = (1 / 2 : ℝ) * (S m / Real.log (m : ℝ)) * Real.log (m : ℝ) - β * Real.log (m : ℝ) := by ring
    _ = (1 / 2 : ℝ) * S m - β * Real.log (m : ℝ) := by
          field_simp [hlog]

/-- From a logarithmic lower bound on u (eventually (1/2) * S m <= log (u m))
and S(m)/log m -> infinity, the ratio u m / m^beta tends to infinity. -/
lemma superpolynomial_of_logdiv {u S : ℕ → ℝ} {β : ℝ}
    (hS : ∀ᶠ m in atTop, 2 ≤ m ∧ (1 / 2 : ℝ) * S m ≤ Real.log (u m))
    (hu0 : ∀ᶠ m in atTop, 0 < u m)
    (hdiv : Tendsto (fun m : ℕ => S m / Real.log (m : ℝ)) atTop atTop) :
    Tendsto (fun m : ℕ => u m / (m : ℝ) ^ β) atTop atTop := by
  have hT : Tendsto (fun m : ℕ => (1 / 2 : ℝ) * S m - β * Real.log (m : ℝ)) atTop atTop :=
    tendsto_half_S_sub_beta_log (S := S) (β := β) hdiv
  have hLogT : Tendsto (fun m : ℕ => Real.log (u m) - β * Real.log (m : ℝ)) atTop atTop := by
    rw [tendsto_atTop]
    intro X
    have hTX : ∀ᶠ m in atTop, X ≤ (1 / 2 : ℝ) * S m - β * Real.log (m : ℝ) := tendsto_atTop.1 hT X
    refine (hS.and hTX).mono ?_
    intro m hm
    have hleS : (1 / 2 : ℝ) * S m ≤ Real.log (u m) := hm.1.2
    have hX : X ≤ (1 / 2 : ℝ) * S m - β * Real.log (m : ℝ) := hm.2
    linarith
  rw [tendsto_atTop]
  intro X
  by_cases hXle : X ≤ 0
  · refine (hu0.and (eventually_ge_atTop 2)).mono ?_
    intro m hm
    have hpow : 0 < (m : ℝ) ^ β := Real.rpow_pos_of_pos (by exact_mod_cast (by omega : 0 < m)) β
    have hpos : 0 < u m / (m : ℝ) ^ β := div_pos hm.1 hpow
    linarith
  · have hXpos : 0 < X := lt_of_not_ge hXle
    have hLX : ∀ᶠ m in atTop, Real.log X ≤ Real.log (u m) - β * Real.log (m : ℝ) :=
      tendsto_atTop.1 hLogT (Real.log X)
    refine ((hLX.and hu0).and (eventually_ge_atTop 2)).mono ?_
    intro m hm
    have hle : Real.log X ≤ Real.log (u m) - β * Real.log (m : ℝ) := hm.1.1
    have hu : 0 < u m := hm.1.2
    have hm2 : 2 ≤ m := hm.2
    have hpow : 0 < (m : ℝ) ^ β := Real.rpow_pos_of_pos (by exact_mod_cast (by omega : 0 < m)) β
    have hlogeq : Real.log (u m / (m : ℝ) ^ β) = Real.log (u m) - β * Real.log (m : ℝ) := by
      rw [Real.log_div (ne_of_gt hu) (ne_of_gt hpow)]
      rw [Real.log_rpow (by exact_mod_cast (by omega : 0 < m)) β]
    have hle2 : Real.log X ≤ Real.log (u m / (m : ℝ) ^ β) := by
      rwa [← hlogeq] at hle
    have hXe : Real.exp (Real.log X) = X := Real.exp_log hXpos
    have hue : Real.exp (Real.log (u m / (m : ℝ) ^ β)) = u m / (m : ℝ) ^ β :=
      Real.exp_log (div_pos hu hpow)
    have h1 := Real.exp_le_exp.mpr hle2
    rwa [hXe, hue] at h1

/-- Theorem 2.2, growth part (min-sum version): if eps k >= 0,
u m >= prod (1 + eps k), and
(sum_{k=2..m} min (eps k) 1) / log m -> infinity, then u m / m^beta -> infinity
for every real beta. -/
theorem superpolynomial_of_divergent_sum {u eps : ℕ → ℝ} {β : ℝ}
    (heps : ∀ m : ℕ, 2 ≤ m → 0 ≤ eps m)
    (hu : ∀ m : ℕ, 2 ≤ m → (∏ k ∈ Finset.Icc 2 m, (1 + eps k)) ≤ u m)
    (hdiv : Tendsto (fun m : ℕ => (∑ k ∈ Finset.Icc 2 m, min (eps k) 1 : ℝ) / Real.log (m : ℝ))
      atTop atTop) :
    Tendsto (fun m : ℕ => u m / (m : ℝ) ^ β) atTop atTop := by
  apply superpolynomial_of_logdiv (S := fun m => ∑ k ∈ Finset.Icc 2 m, min (eps k) 1) (β := β)
  · refine (eventually_ge_atTop 2).mono ?_
    intro m hm
    constructor
    · exact hm
    · have h1 := sum_min_half_le_log_prod (s := Finset.Icc 2 m) (eps := eps)
        (fun k hk => heps k (Finset.mem_Icc.mp hk).1)
      have hprodpos : 0 < ∏ k ∈ Finset.Icc 2 m, (1 + eps k) := by
        apply Finset.prod_pos
        intro k hk
        have : 0 ≤ eps k := heps k (Finset.mem_Icc.mp hk).1
        nlinarith
      have hlog : Real.log (∏ k ∈ Finset.Icc 2 m, (1 + eps k)) ≤ Real.log (u m) :=
        Real.log_le_log hprodpos (hu m hm)
      exact le_trans h1 hlog
  · refine (eventually_ge_atTop 2).mono ?_
    intro m hm
    have hprodge : (1 : ℝ) ≤ ∏ k ∈ Finset.Icc 2 m, (1 + eps k) :=
      Finset.one_le_prod (fun k hk => by
        have : 0 ≤ eps k := heps k (Finset.mem_Icc.mp hk).1
        nlinarith)
    have hu1 : (1 : ℝ) ≤ u m := le_trans hprodge (hu m hm)
    linarith
  · exact hdiv

/-- The S-threshold theorem (S-门槛): the same conclusion follows from the
divergence of S(m) = sum_{k=2..m} log (1 + eps k), the quantity that actually
controls log u_m. -/
theorem superpolynomial_of_logsum {u eps : ℕ → ℝ} {β : ℝ}
    (heps : ∀ m : ℕ, 2 ≤ m → 0 ≤ eps m)
    (hu : ∀ m : ℕ, 2 ≤ m → (∏ k ∈ Finset.Icc 2 m, (1 + eps k)) ≤ u m)
    (hdiv : Tendsto (fun m : ℕ =>
      (∑ k ∈ Finset.Icc 2 m, Real.log (1 + eps k) : ℝ) / Real.log (m : ℝ)) atTop atTop) :
    Tendsto (fun m : ℕ => u m / (m : ℝ) ^ β) atTop atTop := by
  apply superpolynomial_of_logdiv (S := fun m => ∑ k ∈ Finset.Icc 2 m, Real.log (1 + eps k)) (β := β)
  · refine (eventually_ge_atTop 2).mono ?_
    intro m hm
    constructor
    · exact hm
    · have hS0 : 0 ≤ ∑ k ∈ Finset.Icc 2 m, Real.log (1 + eps k) := by
        exact Finset.sum_nonneg (fun k hk => by
          have hx : 0 < 1 + eps k := by
            have : 0 ≤ eps k := heps k (Finset.mem_Icc.mp hk).1
            nlinarith
          exact (Real.log_nonneg_iff hx).2 (by
            have : 0 ≤ eps k := heps k (Finset.mem_Icc.mp hk).1
            nlinarith))
      have h1 := sum_log_le_log_prod (s := Finset.Icc 2 m) (eps := eps)
        (fun k hk => heps k (Finset.mem_Icc.mp hk).1)
      have hprodpos : 0 < ∏ k ∈ Finset.Icc 2 m, (1 + eps k) := by
        exact Finset.prod_pos (fun k hk => by
          have : 0 ≤ eps k := heps k (Finset.mem_Icc.mp hk).1
          nlinarith)
      have h2 : Real.log (∏ k ∈ Finset.Icc 2 m, (1 + eps k)) ≤ Real.log (u m) :=
        Real.log_le_log hprodpos (hu m hm)
      have hhalf : (1 / 2 : ℝ) * (∑ k ∈ Finset.Icc 2 m, Real.log (1 + eps k))
          ≤ ∑ k ∈ Finset.Icc 2 m, Real.log (1 + eps k) := by nlinarith [hS0]
      exact le_trans hhalf (le_trans h1 h2)
  · refine (eventually_ge_atTop 2).mono ?_
    intro m hm
    have hprodge : (1 : ℝ) ≤ ∏ k ∈ Finset.Icc 2 m, (1 + eps k) :=
      Finset.one_le_prod (fun k hk => by
        have : 0 ≤ eps k := heps k (Finset.mem_Icc.mp hk).1
        nlinarith)
    have hu1 : (1 : ℝ) ≤ u m := le_trans hprodge (hu m hm)
    linarith
  · exact hdiv

/-! ## Annihilation against a polynomial bound -/

/-- If u m / m^beta -> infinity and |a| * u m <= C * m^beta for all m >= 1,
then a = 0. -/
theorem annihilate_of_superpolynomial {a C β : ℝ} {u : ℕ → ℝ} (ha : a ≠ 0)
    (hgrowth : Tendsto (fun m : ℕ => u m / (m : ℝ) ^ β) atTop atTop)
    (hbd : ∀ m : ℕ, 1 ≤ m → |a| * u m ≤ C * (m : ℝ) ^ β) : False := by
  have hapos : 0 < |a| := abs_pos.mpr ha
  have hE : ∀ᶠ m in atTop, C / |a| + 1 ≤ u m / (m : ℝ) ^ β :=
    tendsto_atTop.1 hgrowth (C / |a| + 1)
  rcases (hE.and (eventually_ge_atTop 1)).exists with ⟨m, hm⟩
  have hb : C / |a| + 1 ≤ u m / (m : ℝ) ^ β := hm.1
  have hm1 : (1 : ℕ) ≤ m := hm.2
  have hmpos : 0 < (m : ℝ) := by exact_mod_cast (by omega : 0 < m)
  have hpow : 0 < (m : ℝ) ^ β := Real.rpow_pos_of_pos hmpos β
  have hbdm : |a| * u m ≤ C * (m : ℝ) ^ β := hbd m hm1
  have hb' : (C / |a| + 1) * (m : ℝ) ^ β ≤ u m / (m : ℝ) ^ β * (m : ℝ) ^ β := by
    exact mul_le_mul_of_nonneg_right hb (le_of_lt hpow)
  have hrew0 : |a| * (C / |a| + 1) = C + |a| := by
    field_simp [ne_of_gt hapos]
  have hrew2 : u m / (m : ℝ) ^ β * (m : ℝ) ^ β = u m := by
    field_simp [ne_of_gt hpow]
  rw [hrew2] at hb'
  have hmain : (C + |a|) * (m : ℝ) ^ β ≤ |a| * u m := by
    have hmul := mul_le_mul_of_nonneg_left hb' (le_of_lt hapos)
    rwa [← mul_assoc, hrew0] at hmul
  have hle : (C + |a|) * (m : ℝ) ^ β ≤ C * (m : ℝ) ^ β := le_trans hmain hbdm
  have hpos : 0 < |a| * (m : ℝ) ^ β := mul_pos hapos hpow
  nlinarith

/-- Combined annihilation: the min-sum divergence condition (Thm 2.2) plus a
polynomial bound force a = 0. -/
theorem annihilate_of_divergent_sum {a C β : ℝ} {u eps : ℕ → ℝ} (ha : a ≠ 0)
    (heps : ∀ m : ℕ, 2 ≤ m → 0 ≤ eps m)
    (hu : ∀ m : ℕ, 2 ≤ m → (∏ k ∈ Finset.Icc 2 m, (1 + eps k)) ≤ u m)
    (hdiv : Tendsto (fun m : ℕ => (∑ k ∈ Finset.Icc 2 m, min (eps k) 1 : ℝ) / Real.log (m : ℝ))
      atTop atTop)
    (hbd : ∀ m : ℕ, 1 ≤ m → |a| * u m ≤ C * (m : ℝ) ^ β) : False := by
  exact annihilate_of_superpolynomial ha
    (superpolynomial_of_divergent_sum (u := u) (eps := eps) (β := β) heps hu hdiv) hbd

/-! ## The stability theorem: moments of an orthogonal functional vanish -/

/-- q_0 = c0. -/
noncomputable def qZero (c0 : ℝ) : Polynomial ℝ :=
  Polynomial.C c0

/-- q_1 = c0 * x. -/
noncomputable def qOne (c0 : ℝ) : Polynomial ℝ :=
  Polynomial.C c0 * Polynomial.X

/-- q_{2m} = c0 x^{2m} - A_m x^{2m-2} + B_m x^{2m-4}. -/
noncomputable def qEven (c0 : ℝ) (A B : ℕ → ℝ) (m : ℕ) : Polynomial ℝ :=
  Polynomial.C c0 * Polynomial.X ^ (2 * m) - Polynomial.C (A m) * Polynomial.X ^ (2 * m - 2) +
    Polynomial.C (B m) * Polynomial.X ^ (2 * m - 4)

/-- q_{2m+1} = c0 x^{2m+1} - A'_m x^{2m-1} + B'_m x^{2m-3}. -/
noncomputable def qOdd (c0 : ℝ) (A' B' : ℕ → ℝ) (m : ℕ) : Polynomial ℝ :=
  Polynomial.C c0 * Polynomial.X ^ (2 * m + 1) - Polynomial.C (A' m) * Polynomial.X ^ (2 * m - 1) +
    Polynomial.C (B' m) * Polynomial.X ^ (2 * m - 3)

/-- M (q_0) = 0 forces mu_0 = 0 when c0 != 0. -/
lemma constant_orth_moment_zero (M : Polynomial ℝ →ₗ[ℝ] ℝ) {c0 : ℝ} (hc0 : c0 ≠ 0)
    (horth : M (qZero c0) = 0) : H3Completeness.moments M 0 = 0 := by
  have hM : M (qZero c0) = c0 * H3Completeness.moments M 0 := by
    unfold qZero
    simpa [H3Completeness.moments] using (H3Completeness.apply_C_mul_X_pow M c0 0)
  rw [horth] at hM
  exact (mul_eq_zero.mp hM.symm).resolve_left hc0

/-- M (q_1) = 0 forces mu_1 = 0 when c0 != 0. -/
lemma linear_orth_moment_zero (M : Polynomial ℝ →ₗ[ℝ] ℝ) {c0 : ℝ} (hc0 : c0 ≠ 0)
    (horth : M (qOne c0) = 0) : H3Completeness.moments M 1 = 0 := by
  have hM : M (qOne c0) = c0 * H3Completeness.moments M 1 := by
    unfold qOne
    simpa [H3Completeness.moments] using (H3Completeness.apply_C_mul_X_pow M c0 1)
  rw [horth] at hM
  exact (mul_eq_zero.mp hM.symm).resolve_left hc0

/-- The even jump recurrence from orthogonality against q_{2m}. -/
lemma even_recurrence (M : Polynomial ℝ →ₗ[ℝ] ℝ) {c0 : ℝ} {A B : ℕ → ℝ} {m : ℕ} (_hm : 2 ≤ m)
    (horth : M (qEven c0 A B m) = 0) :
    c0 * H3Completeness.moments M (2 * m) =
      A m * H3Completeness.moments M (2 * m - 2) - B m * H3Completeness.moments M (2 * m - 4) := by
  have hM : M (qEven c0 A B m) =
      c0 * H3Completeness.moments M (2 * m) - A m * H3Completeness.moments M (2 * m - 2) +
        B m * H3Completeness.moments M (2 * m - 4) := by
    unfold qEven
    rw [map_add, map_sub]
    rw [H3Completeness.apply_C_mul_X_pow M c0 (2 * m),
      H3Completeness.apply_C_mul_X_pow M (A m) (2 * m - 2),
      H3Completeness.apply_C_mul_X_pow M (B m) (2 * m - 4)]
  rw [horth] at hM
  linarith

/-- The odd jump recurrence from orthogonality against q_{2m+1}. -/
lemma odd_recurrence (M : Polynomial ℝ →ₗ[ℝ] ℝ) {c0 : ℝ} {A' B' : ℕ → ℝ} {m : ℕ} (_hm : 2 ≤ m)
    (horth : M (qOdd c0 A' B' m) = 0) :
    c0 * H3Completeness.moments M (2 * m + 1) =
      A' m * H3Completeness.moments M (2 * m - 1) - B' m * H3Completeness.moments M (2 * m - 3) := by
  have hM : M (qOdd c0 A' B' m) =
      c0 * H3Completeness.moments M (2 * m + 1) - A' m * H3Completeness.moments M (2 * m - 1) +
        B' m * H3Completeness.moments M (2 * m - 3) := by
    unfold qOdd
    rw [map_add, map_sub]
    rw [H3Completeness.apply_C_mul_X_pow M c0 (2 * m + 1),
      H3Completeness.apply_C_mul_X_pow M (A' m) (2 * m - 1),
      H3Completeness.apply_C_mul_X_pow M (B' m) (2 * m - 3)]
  rw [horth] at hM
  linarith

/-- Theorem 2.2 (functional core): orthogonality against the jump family
{q_n} together with the omega(log m) divergence conditions and the polynomial
moment bounds forces every moment of M to vanish.  This is the algebraic core
of the stability theorem; the Hilbert-space wrapper (polynomial density and
continuity) turns "all moments vanish" into "the orthogonal vector is zero". -/
theorem stability_moments_zero {M : Polynomial ℝ →ₗ[ℝ] ℝ} {c0 : ℝ} {A B A' B' : ℕ → ℝ}
    (hc0 : 0 < c0)
    (hB : ∀ m : ℕ, 2 ≤ m → 0 ≤ B m) (hB' : ∀ m : ℕ, 2 ≤ m → 0 ≤ B' m)
    (hAB : ∀ m : ℕ, 2 ≤ m → c0 ≤ A m - B m) (hAB' : ∀ m : ℕ, 2 ≤ m → c0 ≤ A' m - B' m)
    (horth0 : M (qZero c0) = 0) (horth1 : M (qOne c0) = 0)
    (horthE : ∀ m : ℕ, 2 ≤ m → M (qEven c0 A B m) = 0)
    (horthO : ∀ m : ℕ, 2 ≤ m → M (qOdd c0 A' B' m) = 0)
    (hdivE : Tendsto (fun m : ℕ =>
      (∑ k ∈ Finset.Icc 2 m, min (StabilityGrowth.eps c0 A B k) 1 : ℝ) / Real.log (m : ℝ))
      atTop atTop)
    (hdivO : Tendsto (fun m : ℕ =>
      (∑ k ∈ Finset.Icc 2 m, min (StabilityGrowth.eps c0 A' B' k) 1 : ℝ) / Real.log (m : ℝ))
      atTop atTop)
    (hC : ℝ) (hC0 : 0 ≤ hC) (hβ : ℝ) (hβ0 : 0 ≤ hβ)
    (hbdE : ∀ m : ℕ, 1 ≤ m → |H3Completeness.moments M (2 * m)| ≤ hC * (2 * (m : ℝ)) ^ hβ)
    (hbdO : ∀ m : ℕ, 1 ≤ m →
      |H3Completeness.moments M (2 * m + 1)| ≤ hC * (2 * (m : ℝ) + 1) ^ hβ) :
    ∀ k : ℕ, H3Completeness.moments M k = 0 := by
  have hc0ne : c0 ≠ 0 := ne_of_gt hc0
  have hμ0 : H3Completeness.moments M 0 = 0 := constant_orth_moment_zero M hc0ne horth0
  have hμ1 : H3Completeness.moments M 1 = 0 := linear_orth_moment_zero M hc0ne horth1
  have hrecE : ∀ n : ℕ, 2 ≤ n → c0 * H3Completeness.moments M (2 * n) =
      A n * H3Completeness.moments M (2 * n - 2) - B n * H3Completeness.moments M (2 * n - 4) := by
    intro n hn
    exact even_recurrence M hn (horthE n hn)
  have hrecO : ∀ n : ℕ, 2 ≤ n → c0 * H3Completeness.moments M (2 * n + 1) =
      A' n * H3Completeness.moments M (2 * n - 1) - B' n * H3Completeness.moments M (2 * n - 3) := by
    intro n hn
    exact odd_recurrence M hn (horthO n hn)
  have hscalE : ∀ m : ℕ, H3Completeness.moments M (2 * m) =
      H3Completeness.moments M 2 * StabilityGrowth.u (K := ℝ) c0 A B m :=
    Completeness.even_scaling c0 A B hc0ne (H3Completeness.moments M) hμ0 hrecE
  have hscalO : ∀ m : ℕ, H3Completeness.moments M (2 * m + 1) =
      H3Completeness.moments M 3 * StabilityGrowth.u (K := ℝ) c0 A' B' m :=
    Completeness.odd_scaling c0 A' B' hc0ne (H3Completeness.moments M) hμ1 hrecO
  have hepsE : ∀ m : ℕ, 2 ≤ m → 0 ≤ StabilityGrowth.eps c0 A B m :=
    fun m hm => StabilityGrowth.eps_nonneg hc0 (hAB m hm)
  have hepsO : ∀ m : ℕ, 2 ≤ m → 0 ≤ StabilityGrowth.eps c0 A' B' m :=
    fun m hm => StabilityGrowth.eps_nonneg hc0 (hAB' m hm)
  have hgrowE : ∀ m : ℕ, 2 ≤ m → (∏ k ∈ Finset.Icc 2 m, (1 + StabilityGrowth.eps c0 A B k)) ≤
      StabilityGrowth.u (K := ℝ) c0 A B m := by
    intro m hm
    exact StabilityGrowth.product_growth_eps hc0 hB hAB m (by omega : 1 ≤ m)
  have hgrowO : ∀ m : ℕ, 2 ≤ m → (∏ k ∈ Finset.Icc 2 m, (1 + StabilityGrowth.eps c0 A' B' k)) ≤
      StabilityGrowth.u (K := ℝ) c0 A' B' m := by
    intro m hm
    exact StabilityGrowth.product_growth_eps hc0 hB' hAB' m (by omega : 1 ≤ m)
  have hbdE2 : ∀ m : ℕ, 1 ≤ m → |H3Completeness.moments M 2| * StabilityGrowth.u (K := ℝ) c0 A B m
      ≤ (hC * (2 : ℝ) ^ hβ) * (m : ℝ) ^ hβ := by
    intro m hm
    have hsc := hscalE m
    have hbdm := hbdE m hm
    rw [hsc] at hbdm
    have hu0 : 0 ≤ StabilityGrowth.u (K := ℝ) c0 A B m :=
      StabilityGrowth.u_nonneg hc0 hB hAB hm
    rw [abs_mul, abs_of_nonneg hu0] at hbdm
    have hpow : (2 * (m : ℝ)) ^ hβ = (2 : ℝ) ^ hβ * (m : ℝ) ^ hβ := by
      rw [Real.mul_rpow (by norm_num) (by positivity : 0 ≤ (m : ℝ))]
    rw [hpow] at hbdm
    simpa [mul_assoc] using hbdm
  have hμ2 : H3Completeness.moments M 2 = 0 := by
    by_contra hne
    exact annihilate_of_divergent_sum hne hepsE hgrowE hdivE hbdE2
  have hbdO3 : ∀ m : ℕ, 1 ≤ m → |H3Completeness.moments M 3| * StabilityGrowth.u (K := ℝ) c0 A' B' m
      ≤ (hC * (3 : ℝ) ^ hβ) * (m : ℝ) ^ hβ := by
    intro m hm
    have hsc := hscalO m
    have hbdm := hbdO m hm
    rw [hsc] at hbdm
    have hu0 : 0 ≤ StabilityGrowth.u (K := ℝ) c0 A' B' m :=
      StabilityGrowth.u_nonneg hc0 hB' hAB' hm
    rw [abs_mul, abs_of_nonneg hu0] at hbdm
    have hle : (2 * (m : ℝ) + 1) ^ hβ ≤ (3 * (m : ℝ)) ^ hβ := by
      have hmr : (1 : ℝ) ≤ (m : ℝ) := by exact_mod_cast hm
      exact Real.rpow_le_rpow (by positivity : 0 ≤ 2 * (m : ℝ) + 1)
        (by nlinarith : 2 * (m : ℝ) + 1 ≤ 3 * (m : ℝ)) hβ0
    have hbdm' : |H3Completeness.moments M 3| * StabilityGrowth.u (K := ℝ) c0 A' B' m
        ≤ hC * (3 * (m : ℝ)) ^ hβ :=
      le_trans hbdm (mul_le_mul_of_nonneg_left hle hC0)
    have hpow : (3 * (m : ℝ)) ^ hβ = (3 : ℝ) ^ hβ * (m : ℝ) ^ hβ := by
      rw [Real.mul_rpow (by norm_num) (by positivity : 0 ≤ (m : ℝ))]
    rw [hpow] at hbdm'
    simpa [mul_assoc] using hbdm'
  have hμ3 : H3Completeness.moments M 3 = 0 := by
    by_contra hne
    exact annihilate_of_divergent_sum hne hepsO hgrowO hdivO hbdO3
  intro k
  rcases Nat.even_or_odd k with ⟨m, rfl⟩ | ⟨m, rfl⟩
  · rw [← two_mul m, hscalE m, hμ2]
    simp
  · rw [hscalO m, hμ3]
    simp

/-! ## Sharpness: the C/k family (Theorem 2.3) -/

/-- The sharpness coefficient family: A k = c0 * (1 + C/k), B k = 0, so that
eps k = C/k. -/
noncomputable def sharpA (c0 C : ℝ) (k : ℕ) : ℝ :=
  c0 * (1 + C / (k : ℝ))

/-- The zero second coefficient family. -/
noncomputable def sharpB (_ : ℕ) : ℝ := 0

/-- The recurrence solution for the sharpness family. -/
noncomputable def sharpU (c0 C : ℝ) : ℕ → ℝ :=
  StabilityGrowth.u (K := ℝ) c0 (sharpA c0 C) sharpB

/-- eps for the sharpness family is exactly C/k. -/
lemma sharp_eps {c0 C : ℝ} (hc0 : c0 ≠ 0) (k : ℕ) :
    StabilityGrowth.eps c0 (sharpA c0 C) sharpB k = C / (k : ℝ) := by
  unfold StabilityGrowth.eps sharpA sharpB
  field_simp [hc0]
  ring

/-- The sharpness family satisfies A k - B k >= c0 for k >= 2. -/
lemma sharp_AB {c0 C : ℝ} (hc0 : 0 < c0) (hC : 0 ≤ C) (k : ℕ) (hk : 2 ≤ k) :
    c0 ≤ sharpA c0 C k - sharpB k := by
  unfold sharpA sharpB
  have hck : 0 ≤ C / (k : ℝ) := div_nonneg hC (by positivity)
  have : 0 ≤ c0 * (C / (k : ℝ)) := mul_nonneg (le_of_lt hc0) hck
  nlinarith

/-- B k = 0 is nonnegative. -/
lemma sharp_B_nonneg (k : ℕ) : 0 ≤ sharpB k := by
  simp [sharpB]

/-- Exact product formula: u_m = prod_{k=2..m} (1 + C/k) for m >= 1. -/
theorem sharp_product_eq {c0 C : ℝ} (hc0 : c0 ≠ 0) :
    ∀ m : ℕ, 1 ≤ m → sharpU c0 C m = ∏ k ∈ Finset.Icc 2 m, (1 + C / (k : ℝ)) := by
  intro m hm
  refine Nat.le_induction (m := 1) ?base ?step m hm
  · simp [sharpU, StabilityGrowth.u_one]
  · intro n hn ih
    have hrec := StabilityGrowth.u_recurrence' (K := ℝ) (c0 := c0) (A := sharpA c0 C)
      (B := sharpB) hc0 (by omega : 2 ≤ n + 1)
    have hstep : sharpU c0 C (n + 1) = (1 + C / (n + 1 : ℝ)) * sharpU c0 C n := by
      unfold sharpU
      have hA : sharpA c0 C (n + 1) = c0 * (1 + C / (n + 1 : ℝ)) := by
        simp [sharpA, Nat.cast_add]
      have hrec' : c0 * StabilityGrowth.u (K := ℝ) c0 (sharpA c0 C) sharpB (n + 1)
          = c0 * ((1 + C / (n + 1 : ℝ)) * StabilityGrowth.u (K := ℝ) c0 (sharpA c0 C) sharpB n) := by
        rw [hrec, hA]
        simp [sharpB]
        ring
      exact mul_left_cancel₀ hc0 hrec'
    have hprod : (∏ k ∈ Finset.Icc 2 (n + 1), (1 + C / (k : ℝ))) =
        (∏ k ∈ Finset.Icc 2 n, (1 + C / (k : ℝ))) * (1 + C / (n + 1 : ℝ)) := by
      rw [Finset.prod_Icc_succ_top (by omega : 2 ≤ n + 1)]
      simp [Nat.cast_add]
    calc
      sharpU c0 C (n + 1) = (1 + C / (n + 1 : ℝ)) * sharpU c0 C n := hstep
      _ = (1 + C / (n + 1 : ℝ)) * (∏ k ∈ Finset.Icc 2 n, (1 + C / (k : ℝ))) := by rw [ih]
      _ = (∏ k ∈ Finset.Icc 2 n, (1 + C / (k : ℝ))) * (1 + C / (n + 1 : ℝ)) := by ring
      _ = ∏ k ∈ Finset.Icc 2 (n + 1), (1 + C / (k : ℝ)) := hprod.symm

/-- sum_{k=2..m} 1/k <= log m (elementary, via log((k+1)/k) >= 1/(k+1)). -/
lemma sum_inv_Icc_two_le_log (m : ℕ) :
    (∑ k ∈ Finset.Icc 2 m, ((k : ℝ))⁻¹) ≤ Real.log (m : ℝ) := by
  by_cases hm : 2 ≤ m
  · have hbase : (∑ k ∈ Finset.Icc (2 : ℕ) 2, ((k : ℝ))⁻¹) ≤ Real.log (2 : ℝ) := by
      simp
      have h := Real.log_two_gt_d9
      norm_num at h ⊢
      linarith
    refine Nat.le_induction (m := 2) hbase ?step m hm
    intro n hn ih
    have hsum : (∑ k ∈ Finset.Icc 2 (n + 1), ((k : ℝ))⁻¹) =
        (∑ k ∈ Finset.Icc 2 n, ((k : ℝ))⁻¹) + ((n + 1 : ℕ) : ℝ)⁻¹ := by
      rw [Finset.sum_Icc_succ_top (by omega : 2 ≤ n + 1)]
    rw [hsum]
    have hlog : ((n + 1 : ℕ) : ℝ)⁻¹ ≤
        Real.log ((n + 1 : ℕ) : ℝ) - Real.log (n : ℝ) := by
      have hn1 : 1 ≤ n := by omega
      have hnpos : 0 < (n : ℝ) := by exact_mod_cast (by omega : 0 < n)
      have hn1pos : 0 < ((n + 1 : ℕ) : ℝ) := by positivity
      have hnn : (n : ℝ) ≠ 0 := ne_of_gt hnpos
      have hdiv : Real.log (((n + 1 : ℕ) : ℝ) / (n : ℝ)) =
          Real.log ((n + 1 : ℕ) : ℝ) - Real.log (n : ℝ) :=
        Real.log_div (ne_of_gt hn1pos) hnn
      have hxpos : 0 < (n : ℝ) / ((n + 1 : ℕ) : ℝ) := div_pos hnpos (by positivity)
      have hxne : (n : ℝ) / ((n + 1 : ℕ) : ℝ) ≠ 1 := by
        intro h
        have hmul := congrArg (fun t : ℝ => t * ((n + 1 : ℕ) : ℝ)) h
        have hnn1 : ((n + 1 : ℕ) : ℝ) ≠ 0 := by positivity
        field_simp [hnn1] at hmul
        have hncast : (n : ℝ) < ((n + 1 : ℕ) : ℝ) := by
          exact_mod_cast (by omega : n < n + 1)
        linarith
      have hlt := Real.log_lt_sub_one_of_pos hxpos hxne
      have hrew : (n : ℝ) / ((n + 1 : ℕ) : ℝ) - 1 = -(((n + 1 : ℕ) : ℝ)⁻¹) := by
        field_simp [hnpos, (by positivity : ((n + 1 : ℕ) : ℝ) ≠ 0)]
        simp [Nat.cast_add]
      have hlinv : Real.log ((n : ℝ) / ((n + 1 : ℕ) : ℝ)) =
          -(Real.log (((n + 1 : ℕ) : ℝ) / (n : ℝ))) := by
        rw [Real.log_div (ne_of_gt hnpos) (by positivity : ((n + 1 : ℕ) : ℝ) ≠ 0)]
        rw [Real.log_div (by positivity : ((n + 1 : ℕ) : ℝ) ≠ 0) hnn]
        ring
      rw [hlinv, hrew] at hlt
      have hlt' : ((n + 1 : ℕ) : ℝ)⁻¹ < Real.log (((n + 1 : ℕ) : ℝ) / (n : ℝ)) := by linarith
      rw [hdiv] at hlt'
      exact le_of_lt hlt'
    calc
      (∑ k ∈ Finset.Icc 2 n, ((k : ℝ))⁻¹) + ((n + 1 : ℕ) : ℝ)⁻¹
          ≤ Real.log (n : ℝ) + ((n + 1 : ℕ) : ℝ)⁻¹ := by linarith
      _ ≤ Real.log (n : ℝ) + (Real.log ((n + 1 : ℕ) : ℝ) - Real.log (n : ℝ)) := by linarith
      _ = Real.log ((n + 1 : ℕ) : ℝ) := by ring
  · have hm01 : m = 0 ∨ m = 1 := by omega
    rcases hm01 with rfl | rfl
    · simp
    · simp [Real.log_one]

/-- Polynomial growth of the sharpness product:
prod_{k=2..m} (1 + C/k) <= exp C * m^C for C >= 0 and m >= 1. -/
theorem sharp_poly_bound {C : ℝ} (hC : 0 ≤ C) (m : ℕ) (hm : 1 ≤ m) :
    (∏ k ∈ Finset.Icc 2 m, (1 + C / (k : ℝ))) ≤ Real.exp C * (m : ℝ) ^ C := by
  have hprodpos : 0 < ∏ k ∈ Finset.Icc 2 m, (1 + C / (k : ℝ)) := by
    apply Finset.prod_pos
    intro k hk
    have hck : 0 ≤ C / (k : ℝ) := div_nonneg hC (by positivity)
    nlinarith
  have hlog : Real.log (∏ k ∈ Finset.Icc 2 m, (1 + C / (k : ℝ))) ≤ C + C * Real.log (m : ℝ) := by
    calc
      Real.log (∏ k ∈ Finset.Icc 2 m, (1 + C / (k : ℝ)))
          = ∑ k ∈ Finset.Icc 2 m, Real.log (1 + C / (k : ℝ)) := by
              rw [Real.log_prod (s := Finset.Icc 2 m) (f := fun k => (1 + C / (k : ℝ)))]
              intro k hk
              have hck : 0 ≤ C / (k : ℝ) := div_nonneg hC (by positivity)
              nlinarith
      _ ≤ ∑ k ∈ Finset.Icc 2 m, (C / (k : ℝ)) := Finset.sum_le_sum (fun k hk => by
            have hck : 0 ≤ C / (k : ℝ) := div_nonneg hC (by positivity)
            have hpos : 0 < 1 + C / (k : ℝ) := by nlinarith
            have hle := Real.log_le_sub_one_of_pos hpos
            rwa [show (1 + C / (k : ℝ)) - 1 = C / (k : ℝ) by ring] at hle)
      _ = C * (∑ k ∈ Finset.Icc 2 m, ((k : ℝ))⁻¹) := by
            rw [Finset.mul_sum]
            rfl
      _ ≤ C * Real.log (m : ℝ) := by
            exact mul_le_mul_of_nonneg_left (sum_inv_Icc_two_le_log m) hC
      _ ≤ C + C * Real.log (m : ℝ) := by nlinarith [hC]
  have hle := (Real.log_le_iff_le_exp hprodpos).1 hlog
  have hmm : 0 < (m : ℝ) := by exact_mod_cast (by omega : 0 < m)
  have hexp : Real.exp (C + C * Real.log (m : ℝ)) = Real.exp C * (m : ℝ) ^ C := by
    rw [Real.exp_add]
    have hlogpow : Real.exp (C * Real.log (m : ℝ)) = (m : ℝ) ^ C := by
      rw [← Real.exp_log (Real.rpow_pos_of_pos hmm C)]
      congr 1
      rw [Real.log_rpow hmm C]
    rw [hlogpow]
  rwa [hexp] at hle

/-- The sharpness moments satisfy the defining recurrence (the algebraic
orthogonality content of Thm 2.3): c0 u_m - A_m u_{m-1} + B_m u_{m-2} = 0. -/
theorem sharp_recurrence {c0 C : ℝ} (hc0 : c0 ≠ 0) {m : ℕ} (hm : 2 ≤ m) :
    c0 * sharpU c0 C m - sharpA c0 C m * sharpU c0 C (m - 1) + sharpB m * sharpU c0 C (m - 2) = 0 := by
  have hrec := StabilityGrowth.u_recurrence' (K := ℝ) (c0 := c0) (A := sharpA c0 C)
    (B := sharpB) hc0 hm
  unfold sharpU
  linarith

/-- Term bound for the sharpness series: for m >= 1,
u_m^2 / (2m+1)^(2 beta) <= exp(2C) * 2^(-2 beta) * m^(2C - 2 beta). -/
lemma sharp_term_bound {C β : ℝ} (hC : 0 ≤ C) (hβ : 0 < β) {m : ℕ} (hm : 1 ≤ m) :
    ((∏ k ∈ Finset.Icc 2 m, (1 + C / (k : ℝ))) ^ 2) / (2 * (m : ℝ) + 1) ^ (2 * β)
      ≤ Real.exp (2 * C) * (2 : ℝ) ^ (-(2 * β)) * (m : ℝ) ^ (2 * C - 2 * β) := by
  have hmm : 0 < (m : ℝ) := by exact_mod_cast (by omega : 0 < m)
  have hm0 : 0 ≤ (m : ℝ) := le_of_lt hmm
  have hpb := sharp_poly_bound hC m hm
  have hsq : (∏ k ∈ Finset.Icc 2 m, (1 + C / (k : ℝ))) ^ 2 ≤ Real.exp (2 * C) * (m : ℝ) ^ (2 * C) := by
    have hnonneg : 0 ≤ (∏ k ∈ Finset.Icc 2 m, (1 + C / (k : ℝ))) := by
      apply Finset.prod_nonneg
      intro k hk
      have : 0 ≤ C / (k : ℝ) := div_nonneg hC (by positivity)
      nlinarith
    have hsqle := pow_le_pow_left₀ hnonneg hpb 2
    have hrew : (Real.exp C * (m : ℝ) ^ C) ^ 2 = Real.exp (2 * C) * (m : ℝ) ^ (2 * C) := by
      rw [pow_two]
      calc
        Real.exp C * (m : ℝ) ^ C * (Real.exp C * (m : ℝ) ^ C)
            = (Real.exp C * Real.exp C) * ((m : ℝ) ^ C * (m : ℝ) ^ C) := by ring
        _ = Real.exp (2 * C) * (m : ℝ) ^ (2 * C) := by
              rw [← Real.exp_add, ← Real.rpow_add hmm]
              congr 1 <;> congr 1 <;> ring
    rwa [hrew] at hsqle
  have hden : (2 : ℝ) ^ (2 * β) * (m : ℝ) ^ (2 * β) ≤ (2 * (m : ℝ) + 1) ^ (2 * β) := by
    have hpow2 : (2 * (m : ℝ)) ^ (2 * β) = (2 : ℝ) ^ (2 * β) * (m : ℝ) ^ (2 * β) := by
      rw [Real.mul_rpow (by norm_num) hm0]
    rw [← hpow2]
    exact Real.rpow_le_rpow (by positivity : 0 ≤ 2 * (m : ℝ)) (by linarith) (by nlinarith : 0 ≤ 2 * β)
  have hdenpos : 0 < (2 : ℝ) ^ (2 * β) * (m : ℝ) ^ (2 * β) := by positivity
  have hdenpos' : 0 < (2 * (m : ℝ) + 1) ^ (2 * β) := by positivity
  have hdivle : (∏ k ∈ Finset.Icc 2 m, (1 + C / (k : ℝ))) ^ 2 / (2 * (m : ℝ) + 1) ^ (2 * β)
      ≤ (Real.exp (2 * C) * (m : ℝ) ^ (2 * C)) /
          ((2 : ℝ) ^ (2 * β) * (m : ℝ) ^ (2 * β)) := by
    have hnumle : (∏ k ∈ Finset.Icc 2 m, (1 + C / (k : ℝ))) ^ 2 / (2 * (m : ℝ) + 1) ^ (2 * β)
        ≤ Real.exp (2 * C) * (m : ℝ) ^ (2 * C) / (2 * (m : ℝ) + 1) ^ (2 * β) := by
      exact div_le_div_of_nonneg_right hsq (le_of_lt hdenpos')
    have hdiv2 : Real.exp (2 * C) * (m : ℝ) ^ (2 * C) / (2 * (m : ℝ) + 1) ^ (2 * β)
        ≤ Real.exp (2 * C) * (m : ℝ) ^ (2 * C) /
            ((2 : ℝ) ^ (2 * β) * (m : ℝ) ^ (2 * β)) := by
      exact div_le_div_of_nonneg_left
        (by positivity : 0 ≤ Real.exp (2 * C) * (m : ℝ) ^ (2 * C)) hdenpos hden
    exact le_trans hnumle hdiv2
  have hrew : (Real.exp (2 * C) * (m : ℝ) ^ (2 * C)) /
        ((2 : ℝ) ^ (2 * β) * (m : ℝ) ^ (2 * β))
      = Real.exp (2 * C) * (2 : ℝ) ^ (-(2 * β)) * (m : ℝ) ^ (2 * C - 2 * β) := by
    have h2 : (2 : ℝ) ^ (-(2 * β)) = ((2 : ℝ) ^ (2 * β))⁻¹ := by
      rw [Real.rpow_neg (by norm_num : 0 ≤ (2 : ℝ))]
    have hm2 : (m : ℝ) ^ (-(2 * β)) = ((m : ℝ) ^ (2 * β))⁻¹ := by
      rw [Real.rpow_neg hm0]
    have hmmul : (m : ℝ) ^ (2 * C) * (m : ℝ) ^ (-(2 * β)) = (m : ℝ) ^ (2 * C - 2 * β) := by
      rw [← Real.rpow_add hmm]
      congr 1
    have hmmul2 : (m : ℝ) ^ (2 * C) / (m : ℝ) ^ (2 * β) = (m : ℝ) ^ (2 * C - 2 * β) := by
      rw [div_eq_mul_inv, ← hm2, hmmul]
    have h2nz : (2 : ℝ) ^ (2 * β) ≠ 0 := by positivity
    have hmnz : (m : ℝ) ^ (2 * β) ≠ 0 := by positivity
    calc
      Real.exp (2 * C) * (m : ℝ) ^ (2 * C) / ((2 : ℝ) ^ (2 * β) * (m : ℝ) ^ (2 * β))
          = Real.exp (2 * C) * ((m : ℝ) ^ (2 * C) / (m : ℝ) ^ (2 * β)) / (2 : ℝ) ^ (2 * β) := by
            field_simp [h2nz, hmnz]
      _ = Real.exp (2 * C) * ((m : ℝ) ^ (2 * C - 2 * β)) / (2 : ℝ) ^ (2 * β) := by
            rw [hmmul2]
      _ = Real.exp (2 * C) * (2 : ℝ) ^ (-(2 * β)) * (m : ℝ) ^ (2 * C - 2 * β) := by
            rw [div_eq_mul_inv, ← h2]
            ring
  rwa [hrew] at hdivle

/-- Theorem 2.3, analytic core: the sharpness series
sum_{m >= 1} u_m^2 / (2m+1)^(2 beta) converges whenever beta > C + 1/2,
so the candidate vector w = sum u_m / (2m+1)^(2 beta) * x^{2m} has finite
H_beta-norm (it is nonzero since its even moments u_m do not vanish, and it
is orthogonal to the family by `sharp_recurrence`; the diagonal-space wrapper
is the analytic companion). -/
theorem sharp_series_summable {c0 C β : ℝ} (hc0 : 0 < c0) (hC : 0 < C) (hβ : C + 1 / 2 < β) :
    Summable (fun m : ℕ => (sharpU c0 C (m + 1) ^ 2) / (2 * (m + 1 : ℝ) + 1) ^ (2 * β)) := by
  have hprod : ∀ m : ℕ, sharpU c0 C (m + 1) =
      ∏ k ∈ Finset.Icc 2 (m + 1), (1 + C / (k : ℝ)) :=
    fun m => sharp_product_eq (ne_of_gt hc0) (m + 1) (by omega)
  let f : ℕ → ℝ := fun m => (Real.exp (2 * C) * (2 : ℝ) ^ (-(2 * β))) * (m + 1 : ℝ) ^ (2 * C - 2 * β)
  have hp : 2 * C - 2 * β < -1 := by nlinarith [hβ]
  have hsum0 : Summable (fun n : ℕ => (n : ℝ) ^ (2 * C - 2 * β)) :=
    (Real.summable_nat_rpow).2 hp
  have hsum1 : Summable (fun m : ℕ => (m + 1 : ℝ) ^ (2 * C - 2 * β)) :=
    by
    simpa [Nat.cast_add, Nat.cast_one] using (summable_nat_add_iff 1).2 hsum0
  have hsum : Summable f := by
    unfold f
    exact Summable.mul_left (Real.exp (2 * C) * (2 : ℝ) ^ (-(2 * β))) hsum1
  refine Summable.of_nonneg_of_le ?hnonneg ?hle hsum
  · intro m
    have hu : 0 ≤ sharpU c0 C (m + 1) := by
      rw [hprod m]
      have : (1 : ℝ) ≤ ∏ k ∈ Finset.Icc 2 (m + 1), (1 + C / (k : ℝ)) := by
        exact Finset.one_le_prod (fun k hk => by
          have hck : 0 ≤ C / (k : ℝ) := div_nonneg (le_of_lt hC) (by positivity)
          nlinarith)
      linarith
    have hsq : 0 ≤ sharpU c0 C (m + 1) ^ 2 := sq_nonneg _
    have hd : 0 < (2 * (m + 1 : ℝ) + 1) ^ (2 * β) := by positivity
    exact div_nonneg hsq (le_of_lt hd)
  · intro m
    have hm1 : 1 ≤ m + 1 := by omega
    have htb := sharp_term_bound (le_of_lt hC) (by nlinarith [hβ] : 0 < β) hm1
    have hrew : ((∏ k ∈ Finset.Icc 2 (m + 1), (1 + C / (k : ℝ))) ^ 2) /
          (2 * ((m + 1 : ℕ) : ℝ) + 1) ^ (2 * β)
        = (sharpU c0 C (m + 1) ^ 2) / (2 * ((m + 1 : ℕ) : ℝ) + 1) ^ (2 * β) := by
      rw [hprod m]
    have hle : (sharpU c0 C (m + 1) ^ 2) / (2 * ((m + 1 : ℕ) : ℝ) + 1) ^ (2 * β)
        ≤ Real.exp (2 * C) * (2 : ℝ) ^ (-(2 * β)) * ((m + 1 : ℕ) : ℝ) ^ (2 * C - 2 * β) := by
      rwa [hrew] at htb
    simpa [f, Nat.cast_add, Nat.cast_one] using hle

end Stability

end SL
