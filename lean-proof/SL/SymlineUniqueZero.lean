import Mathlib
import SL.SymlineKeyLemma
import SL.SymlineTensionRatio

/-!
# Symmetry-line KEY LEMMA: unique-zero assembly (n=1 gap line)

Formalization of the assembly step of the KEY LEMMA in
`docs/SL_gap_n1_symline_proof.tex` (section 4.4, thm:keylemma): the
unique zero `c* = c*(q̃)` of `F̃_e` in `(0, 1/2)` together with the sign
conclusions (eq:FeSign).

Content:
* `existsUnique_zero_signs_of_nonneg_mono`: the generic analytic core of
  the KEY LEMMA.  If `f` is continuous on `(a,b]`, differentiable on
  `(a,b)`, has positive right limit `L > 0` at `a`, satisfies `f b < 0`,
  and the monotonicity implication (eq:mono) `f x ≥ 0 → deriv f x < 0`
  on `(a,b)`, then `f` has a unique zero in `(a,b)`, is positive before
  it and negative after it.
* `positive_of_no_zero_and_pos` / `negative_of_no_zero_and_neg`: sign
  constancy on a zero-free interval (the sign-conclusion step).
* `Mf_pos`: positivity of `Mf(α₂(c);c)`, the `M2 > 0` hypothesis of the
  monotonicity step.
* `FeHalf_neg`: the algebraic sign core of lem:endpoints (ii),
  `π sin²α₁ (2α₁−π)/(q̃+Φ(α₁)/2) < 0` for `0 < α₁ < π/2`.
* `FeZero_limit_pos`: positivity of the limit value `π²/(4q̃)` of
  lem:endpoints (i).
* `Fe_deriv_neg_of_nonneg`: the monotonicity implication for the
  concrete `Fe(c) = Mf(α₁(c);c) − Mf(α₂(c);c)` with the derivative
  identity (eq:Fep) as an explicit hypothesis; the algebraic core is
  `Fep_lt_zero_of_nonneg` (SymlineKeyLemma).
* `keylemma_concrete`: the KEY LEMMA for the concrete `Fe`, with all
  analytic facts (regularity, endpoint signs, derivative identity,
  branch reduction) isolated as hypotheses.

Honesty notes (hooks not formalized in this file):
* The derivative identity `d/dc Mf(αk(c);c) = G(αk(c);c)` (eq:Fep,
  eq:G) is a phase-theory hook; `Fe_deriv_neg_of_nonneg` and
  `keylemma_concrete` take it as a hypothesis.
* The endpoint signs of lem:endpoints are phase-theory hooks:
  (i) `lim_{c→0+} F̃_e(c) = π²/(4q̃)` uses `α₁→π/2`, `α₂→π`;
  (ii) `F̃_e(1/2) < 0` uses `α₂(1/2) = π − α₁(1/2)` to identify the
  closed form.  Only the algebraic cores `FeHalf_neg` and
  `FeZero_limit_pos` are formalized here.
* The branch reduction `γ = π − α₂(c) ≤ γ₀(q̃) ≤ Gamma0` (needed for
  P2) is a hypothesis; `gamma0_mono` (SymlineKeyLemma) covers only the
  second half.
* The negativity of `F̃_e` for `c > 1/2` (lem:easy) is not part of this
  file.
* Numerical evidence is never used as a theorem.
-/

namespace SL
namespace SymlineUniqueZero

open Real
open Filter
open scoped Topology
open SymlineKeyLemma

noncomputable section

/-- `Mf(x;c) = x² sin²x / (q + c·Φ_q(x))` of the symmetry-line branch
(alias of `SymlineTensionRatio.Mf`). -/
def Mf (x c q : ℝ) : ℝ := SymlineTensionRatio.Mf x c q

/-- `F̃_e(c) = M1(c) − M2(c) = Mf(α₁(c);c) − Mf(α₂(c);c)` on the branch
(the source's `F̃_e`; `α₁`, `α₂` are the branch functions). -/
def Fe (q : ℝ) (c α1 α2 : ℝ) : ℝ :=
  Mf α1 c q - Mf α2 c q

/-- `Mf(x;c) > 0` for `x ∈ (0, π)`, `c > 0`, `q > 0`. -/
lemma Mf_pos {x c q : ℝ} (hx0 : 0 < x) (hxp : x < Real.pi)
    (hc0 : 0 < c) (hq0 : 0 < q) : 0 < Mf x c q := by
  unfold Mf SymlineTensionRatio.Mf
  have hx2 : 0 < x ^ 2 := sq_pos_of_pos hx0
  have hsin : 0 < sin x := Real.sin_pos_of_pos_of_lt_pi hx0 hxp
  have hs2 : 0 < sin x ^ 2 := sq_pos_of_pos hsin
  have hnum : 0 < x ^ 2 * sin x ^ 2 := mul_pos hx2 hs2
  have hden : 0 < q + c * SymlineTensionRatio.Phi q x := by
    have hcΦ : 0 ≤ c * SymlineTensionRatio.Phi q x :=
      mul_nonneg hc0.le (SymlineTensionRatio.Phi_nonneg q x)
    linarith
  exact div_pos hnum hden

/-- Algebraic sign core of lem:endpoints (ii):
`π sin²α (2α−π)/(q̃+Φ(α)/2) < 0` for `0 < α < π/2`.  The identity
`F̃_e(1/2) = ...` additionally needs `α₂(1/2) = π − α₁(1/2)` (phase
hook). -/
lemma FeHalf_neg {q α : ℝ} (hq0 : 0 < q) (hα0 : 0 < α) (hαp : α < Real.pi / 2) :
    Real.pi * sin α ^ 2 * (2 * α - Real.pi) / (q + Phi q α / 2) < 0 := by
  have hsin : 0 < sin α := Real.sin_pos_of_pos_of_lt_pi hα0 (by linarith [Real.pi_pos])
  have hnum : Real.pi * sin α ^ 2 * (2 * α - Real.pi) < 0 := by
    have h1 : 0 < Real.pi * sin α ^ 2 := mul_pos Real.pi_pos (sq_pos_of_pos hsin)
    have h2 : 2 * α - Real.pi < 0 := by linarith [hαp]
    exact mul_neg_of_pos_of_neg h1 h2
  have hden : 0 < q + Phi q α / 2 := by
    have hΦ : 0 ≤ Phi q α / 2 := div_nonneg (Phi_nonneg q α) (by norm_num)
    linarith
  exact div_neg_of_neg_of_pos hnum hden

/-- The positive limit value of lem:endpoints (i): `π²/(4q̃) > 0`. -/
lemma FeZero_limit_pos {q : ℝ} (hq0 : 0 < q) :
    0 < Real.pi ^ 2 / (4 * q) := by
  exact div_pos (sq_pos_of_pos Real.pi_pos) (mul_pos (by norm_num : (0 : ℝ) < 4) hq0)

/-- Sign constancy: a function continuous on `(x,y]` with no zeros on
`(x,y)` that is positive at some point of `(x,y]` is positive on all of
`(x,y)`. -/
lemma positive_of_no_zero_and_pos {f : ℝ → ℝ} {x y : ℝ}
    (hcont : ContinuousOn f (Set.Ioc x y))
    (hnozero : ∀ z ∈ Set.Ioo x y, f z ≠ 0)
    (hpos : ∃ z ∈ Set.Ioc x y, 0 < f z) :
    ∀ z ∈ Set.Ioo x y, 0 < f z := by
  intro z hz
  by_contra h
  have hzle : f z ≤ 0 := le_of_not_gt h
  have hzne : f z ≠ 0 := hnozero z hz
  have hzlt : f z < 0 := lt_of_le_of_ne hzle hzne
  rcases hpos with ⟨z0, hz0, hz0pos⟩
  have hzz0 : z ≠ z0 := by
    intro hze
    subst z0
    linarith
  by_cases hlt : z < z0
  · have hsub : Set.Icc z z0 ⊆ Set.Ioc x y := by
      intro w hw
      exact ⟨lt_of_lt_of_le hz.1 hw.1, le_trans hw.2 hz0.2⟩
    have hivt : (0 : ℝ) ∈ Set.Icc (f z) (f z0) := ⟨le_of_lt hzlt, le_of_lt hz0pos⟩
    rcases (intermediate_value_Icc (le_of_lt hlt) (hcont.mono hsub)) hivt with ⟨w, hw, hfw⟩
    have hwz0ne : w ≠ z0 := by
      intro hwz0
      subst w
      linarith
    have hwz : w ∈ Set.Ioo x y :=
      ⟨lt_of_lt_of_le hz.1 hw.1, lt_of_lt_of_le (lt_of_le_of_ne hw.2 hwz0ne) hz0.2⟩
    exact hnozero w hwz hfw
  · have hgt : z0 < z := lt_of_le_of_ne (le_of_not_gt hlt) hzz0.symm
    have hsub : Set.Icc z0 z ⊆ Set.Ioc x y := by
      intro w hw
      exact ⟨lt_of_lt_of_le hz0.1 hw.1, le_of_lt (lt_of_le_of_lt hw.2 hz.2)⟩
    have hivt : (0 : ℝ) ∈ Set.Icc (f z) (f z0) := ⟨le_of_lt hzlt, le_of_lt hz0pos⟩
    rcases (intermediate_value_Icc' (le_of_lt hgt) (hcont.mono hsub)) hivt with ⟨w, hw, hfw⟩
    have hwz : w ∈ Set.Ioo x y := ⟨lt_of_lt_of_le hz0.1 hw.1, lt_of_le_of_lt hw.2 hz.2⟩
    exact hnozero w hwz hfw

/-- Sign constancy (negative version), derived from the positive one
applied to `-f`. -/
lemma negative_of_no_zero_and_neg {f : ℝ → ℝ} {x y : ℝ}
    (hcont : ContinuousOn f (Set.Ioc x y))
    (hnozero : ∀ z ∈ Set.Ioo x y, f z ≠ 0)
    (hneg : ∃ z ∈ Set.Ioc x y, f z < 0) :
    ∀ z ∈ Set.Ioo x y, f z < 0 := by
  intro z hz
  have hg : 0 < -f z :=
    positive_of_no_zero_and_pos (f := fun w => -f w) hcont.neg
      (by
        intro w hw hfw
        exact hnozero w hw (neg_eq_zero.mp hfw))
      (by
        rcases hneg with ⟨z0, hz0, hz0neg⟩
        exact ⟨z0, hz0, neg_pos.mpr hz0neg⟩)
      z hz
  linarith

/-- KEY LEMMA assembly (generic analytic form, thm:keylemma): if `f`
has positive right limit `L > 0` at `a`, is negative at `b`, is
continuous on `(a,b]`, differentiable on `(a,b)`, and satisfies the
monotonicity implication (eq:mono) `f x ≥ 0 → deriv f x < 0` on
`(a,b)`, then `f` has a unique zero in `(a,b)`, is positive before it
and negative after it (eq:FeSign on `(0, 1/2)` when `a = 0`, `b = 1/2`). -/
theorem existsUnique_zero_signs_of_nonneg_mono
    {f : ℝ → ℝ} {a b L : ℝ} (hab : a < b)
    (hcont : ContinuousOn f (Set.Ioc a b))
    (hlim : Tendsto f (𝓝[>] a) (𝓝 L)) (hL : 0 < L)
    (hdiff : ∀ x ∈ Set.Ioo a b, DifferentiableAt ℝ f x)
    (hmono : ∀ x ∈ Set.Ioo a b, 0 ≤ f x → deriv f x < 0)
    (hfb : f b < 0) :
    ∃ c, c ∈ Set.Ioo a b ∧ f c = 0 ∧
      (∀ x ∈ Set.Ioo a c, 0 < f x) ∧
      (∀ x ∈ Set.Ioo c b, f x < 0) ∧
      (∀ c', c' ∈ Set.Ioo a b → f c' = 0 → c' = c) := by
  -- a positive point inside (a, b) exists by the right limit:
  have hpos_ev : ∀ᶠ x in 𝓝[>] a, 0 < f x := hlim.eventually (isOpen_Ioi.mem_nhds hL)
  have hIoo_ev : Set.Ioo a b ∈ 𝓝[>] a := by
    rw [show Set.Ioo a b = Set.Iio b ∩ Set.Ioi a by
      ext x
      constructor <;> intro hx <;> exact ⟨hx.2, hx.1⟩]
    exact Filter.inter_mem (nhdsWithin_le_nhds (isOpen_Iio.mem_nhds hab)) self_mem_nhdsWithin
  haveI : NeBot (𝓝[>] a) := nhdsGT_neBot_of_exists_gt ⟨b, hab⟩
  rcases (hpos_ev.and hIoo_ev).exists with ⟨x0, hx0pos, hx0⟩
  -- existence of a zero by IVT on [x0, b]:
  have hcont_xb : ContinuousOn f (Set.Icc x0 b) :=
    hcont.mono (by intro y hy; exact ⟨lt_of_lt_of_le hx0.1 hy.1, hy.2⟩)
  have hivt0 : (0 : ℝ) ∈ Set.Icc (f b) (f x0) := ⟨le_of_lt hfb, le_of_lt hx0pos⟩
  rcases (intermediate_value_Icc' (le_of_lt hx0.2) hcont_xb) hivt0 with ⟨c, hc, hfc⟩
  have hc_b : c ≠ b := by
    intro hce
    subst c
    linarith [hfb, hfc]
  have hc' : c ∈ Set.Ioo a b := ⟨lt_of_lt_of_le hx0.1 hc.1, lt_of_le_of_ne hc.2 hc_b⟩
  -- uniqueness: no two zeros
  have hno_two : ∀ u v, u ∈ Set.Ioo a b → v ∈ Set.Ioo a b → u < v →
      f u = 0 → f v = 0 → False := by
    intro u v hu hv huv hfu hfv
    have hslope : ∀ z ∈ Set.Ioo a b,
        Tendsto (fun y : ℝ => (f y - f z) / (y - z)) (𝓝[≠] z) (𝓝 (deriv f z)) := by
      intro z hz
      simpa [slope_fun_def_field] using (hasDerivAt_iff_tendsto_slope.mp ((hdiff z hz).hasDerivAt))
    have hright : ∀ z ∈ Set.Ioo a b, f z = 0 → ∃ η > 0,
        ∀ y ∈ Set.Ioo z (z + η), f y < 0 := by
      intro z hz hfz
      have hd : deriv f z < 0 := hmono z hz (by simp [hfz])
      have hsl : Tendsto (fun y : ℝ => (f y - f z) / (y - z)) (𝓝[>] z) (𝓝 (deriv f z)) :=
        (hslope z hz).mono_left (nhdsGT_le_nhdsNE z)
      have hev : ∀ᶠ y in 𝓝[>] z, (f y - f z) / (y - z) < 0 :=
        hsl.eventually (isOpen_Iio.mem_nhds hd)
      rcases (Metric.eventually_nhds_iff.mp (eventually_nhdsWithin_iff.mp hev)) with
        ⟨ε, hε, hεp⟩
      refine ⟨ε, hε, ?_⟩
      intro y hy
      have hdist : dist y z < ε := by
        rw [Real.dist_eq]
        rw [abs_of_pos (sub_pos.mpr hy.1)]
        linarith [hy.2]
      have hsl' : (f y - f z) / (y - z) < 0 := hεp hdist hy.1
      have hden : 0 < y - z := sub_pos.mpr hy.1
      have hnum : f y - f z < 0 := by
        simpa using ((div_lt_iff₀ hden).mp hsl')
      rw [hfz] at hnum
      simpa using hnum
    have hleft : ∀ z ∈ Set.Ioo a b, f z = 0 → ∃ η > 0,
        ∀ y ∈ Set.Ioo (z - η) z, f y > 0 := by
      intro z hz hfz
      have hd : deriv f z < 0 := hmono z hz (by simp [hfz])
      have hsl : Tendsto (fun y : ℝ => (f y - f z) / (y - z)) (𝓝[<] z) (𝓝 (deriv f z)) :=
        (hslope z hz).mono_left (nhdsLT_le_nhdsNE z)
      have hev : ∀ᶠ y in 𝓝[<] z, (f y - f z) / (y - z) < 0 :=
        hsl.eventually (isOpen_Iio.mem_nhds hd)
      rcases (Metric.eventually_nhds_iff.mp (eventually_nhdsWithin_iff.mp hev)) with
        ⟨ε, hε, hεp⟩
      refine ⟨ε, hε, ?_⟩
      intro y hy
      have hdist : dist y z < ε := by
        rw [Real.dist_eq]
        rw [abs_of_neg (sub_neg.mpr hy.2)]
        linarith [hy.1]
      have hsl' : (f y - f z) / (y - z) < 0 := hεp hdist hy.2
      have hden : y - z < 0 := sub_neg.mpr hy.2
      have hnum : 0 < f y - f z := by
        simpa using ((div_lt_iff_of_neg hden).mp hsl')
      rw [hfz] at hnum
      simpa using hnum
    -- right-isolation at u; v cannot lie in (u, u+η):
    rcases hright u hu hfu with ⟨η, hη, hηp⟩
    have hvu : u + η ≤ v := by
      by_contra h
      have hvlt : v < u + η := lt_of_not_ge h
      have : f v < 0 := hηp v ⟨huv, hvlt⟩
      linarith [hfv]
    have huv_le : u ≤ v := le_of_lt (lt_of_lt_of_le (by linarith [hη]) hvu)
    have hne : (Set.Icc u v).Nonempty := ⟨u, le_rfl, huv_le⟩
    have hcont_uv : ContinuousOn f (Set.Icc u v) :=
      hcont.mono (by intro y hy; exact ⟨lt_of_lt_of_le hu.1 hy.1, le_of_lt (lt_of_le_of_lt hy.2 hv.2)⟩)
    rcases isCompact_Icc.exists_isMaxOn hne hcont_uv with ⟨m, hm, hmle⟩
    by_cases hmpos : 0 < f m
    · have hmu : u < m := lt_of_le_of_ne hm.1 (by
        intro hme
        subst m
        linarith [hfu, hmpos])
      have hmv : m < v := lt_of_le_of_ne hm.2 (by
        intro hme
        subst m
        linarith [hfv, hmpos])
      have hmab : m ∈ Set.Ioo a b := ⟨lt_trans hu.1 hmu, lt_trans hmv hv.2⟩
      have hd : deriv f m < 0 := hmono m hmab (le_of_lt hmpos)
      have hsl : Tendsto (fun y : ℝ => (f y - f m) / (y - m)) (𝓝[<] m) (𝓝 (deriv f m)) :=
        (hslope m hmab).mono_left (nhdsLT_le_nhdsNE m)
      have hIoo_m : Set.Ioo u m ∈ 𝓝[<] m := by
        rw [show Set.Ioo u m = Set.Iio m ∩ Set.Ioi u by
          ext x
          constructor <;> intro hx <;> exact ⟨hx.2, hx.1⟩]
        exact Filter.inter_mem self_mem_nhdsWithin (nhdsWithin_le_nhds (isOpen_Ioi.mem_nhds hmu))
      have hev : ∀ᶠ y in 𝓝[<] m, 0 ≤ (f y - f m) / (y - m) := by
        filter_upwards [hIoo_m] with y hy
        have hymem : y ∈ Set.Icc u v := ⟨le_of_lt hy.1, le_trans (le_of_lt hy.2) hm.2⟩
        have hnum : f y - f m ≤ 0 := sub_nonpos.mpr (hmle hymem)
        have hden : y - m < 0 := sub_neg.mpr hy.2
        exact div_nonneg_of_nonpos hnum (le_of_lt hden)
      haveI : NeBot (𝓝[<] m) := nhdsLT_neBot_of_exists_lt ⟨a, hmab.1⟩
      have hdge : 0 ≤ deriv f m := ge_of_tendsto hsl hev
      linarith
    · have h0le : 0 ≤ f m := by
        simpa [hfu] using (hmle ⟨le_rfl, huv_le⟩)
      have hfm : f m = 0 := le_antisymm (not_lt.mp hmpos) h0le
      rcases hleft v hv hfv with ⟨ε, hε, hεp⟩
      let w0 : ℝ := max u (v - ε / 2)
      have hw0_lt : w0 < v :=
        max_lt (by linarith) (by linarith)
      have hw0_ge_u : u ≤ w0 := le_max_left u (v - ε / 2)
      have hvε_le : v - ε ≤ w0 := by
        have h1 : v - ε < v - ε / 2 := by linarith [hε]
        have h2 : v - ε / 2 ≤ w0 := le_max_right u (v - ε / 2)
        linarith
      let w : ℝ := (w0 + v) / 2
      have hmid : w0 < (w0 + v) / 2 := by
        rw [lt_div_iff₀ (by norm_num : (0 : ℝ) < 2)]
        nlinarith [hw0_lt]
      have hwu : u < w := by
        dsimp [w]
        exact lt_of_le_of_lt hw0_ge_u hmid
      have hwv : w < v := by
        dsimp [w]
        rw [div_lt_iff₀ (by norm_num : (0 : ℝ) < 2)]
        nlinarith [hw0_lt]
      have hwε : v - ε < w := by
        dsimp [w]
        exact lt_of_le_of_lt hvε_le hmid
      have hwpos : 0 < f w := hεp w ⟨hwε, hwv⟩
      have hwmem : w ∈ Set.Icc u v := ⟨le_of_lt hwu, le_of_lt hwv⟩
      have hwle : f w ≤ 0 := by
        have h := hmle hwmem
        rwa [hfm] at h
      linarith
  have huniq : ∀ c', c' ∈ Set.Ioo a b → f c' = 0 → c' = c := by
    intro c' hci hfc'
    by_contra hne
    rcases lt_or_gt_of_ne hne with hc'c | hcc'
    · exact hno_two c' c hci hc' hc'c hfc' hfc
    · exact hno_two c c' hc' hci hcc' hfc hfc'
  -- sign conclusions:
  have hnozero_ac : ∀ z ∈ Set.Ioo a c, f z ≠ 0 := by
    intro z hz hfz
    have hzab : z ∈ Set.Ioo a b := ⟨hz.1, lt_trans hz.2 hc'.2⟩
    exact (ne_of_lt hz.2) (huniq z hzab hfz)
  have hpos_ac : ∃ z ∈ Set.Ioc a c, 0 < f z := by
    have hIoo : Set.Ioo a c ∈ 𝓝[>] a := by
      rw [show Set.Ioo a c = Set.Iio c ∩ Set.Ioi a by
        ext x
        constructor <;> intro hx <;> exact ⟨hx.2, hx.1⟩]
      exact Filter.inter_mem (nhdsWithin_le_nhds (isOpen_Iio.mem_nhds hc'.1)) self_mem_nhdsWithin
    rcases (hpos_ev.and hIoo).exists with ⟨z, hzpos, hz⟩
    exact ⟨z, ⟨hz.1, le_of_lt hz.2⟩, hzpos⟩
  have hpos_c : ∀ x ∈ Set.Ioo a c, 0 < f x :=
    positive_of_no_zero_and_pos
      (hcont.mono (by intro z hz; exact ⟨hz.1, le_of_lt (lt_of_le_of_lt hz.2 hc'.2)⟩))
      hnozero_ac hpos_ac
  have hnozero_cb : ∀ z ∈ Set.Ioo c b, f z ≠ 0 := by
    intro z hz hfz
    have hzab : z ∈ Set.Ioo a b := ⟨lt_trans hc'.1 hz.1, hz.2⟩
    exact (ne_of_lt hz.1) ((huniq z hzab hfz).symm)
  have hneg_cb : ∃ z ∈ Set.Ioc c b, f z < 0 := ⟨b, ⟨hc'.2, le_rfl⟩, hfb⟩
  have hneg_c : ∀ x ∈ Set.Ioo c b, f x < 0 :=
    negative_of_no_zero_and_neg
      (hcont.mono (by intro z hz; exact ⟨lt_trans hc'.1 hz.1, hz.2⟩))
      hnozero_cb hneg_cb
  exact ⟨c, hc', hfc, hpos_c, hneg_c, huniq⟩

/-- KEY-LEMMA monotonicity implication for the concrete `Fe` at a fixed
`c` with the branch functions `α₁`, `α₂`: if `Fe ≥ 0` and the derivative
identity (eq:Fep) holds, then `deriv Fe < 0`.  The hypotheses on
`γ = π − α₂(c)` are exactly the branch reduction needed for P2. -/
theorem Fe_deriv_neg_of_nonneg
    {q c : ℝ} {α1 α2 : ℝ → ℝ} {γ : ℝ}
    (hq0 : 0 < q) (hq1 : q ≤ 1) (hqq : q0 ≤ q)
    (hc0 : 0 < c) (hc12 : c < 1 / 2)
    (hα1 : 0 < α1 c) (hα1p : α1 c < Real.pi / 2)
    (hγ0 : 0 < γ) (hγΓ : γ ≤ Gamma0) (hγdef : γ = Real.pi - α2 c)
    (hFe : 0 ≤ Fe q c (α1 c) (α2 c))
    (hderiv : deriv (fun x : ℝ => Fe q x (α1 x) (α2 x)) c =
      (Mf (α1 c) c q - Mf (α2 c) c q) * G q c (α1 c) +
        Mf (α2 c) c q * (G q c (α1 c) - G q c (α2 c))) :
    deriv (fun x : ℝ => Fe q x (α1 x) (α2 x)) c < 0 := by
  have hM2 : 0 < Mf (α2 c) c q := by
    have hα2p : α2 c < Real.pi := by linarith [hγdef, hγ0]
    have hα2 : 0 < α2 c := by
      have hγp : γ < Real.pi / 2 := by linarith [hγΓ, Gamma0_lt_pi_div_two]
      linarith [hγdef, hγp]
    exact Mf_pos hα2 hα2p hc0 hq0
  have hG1 : G q c (α1 c) < 0 := P1_neg hq0 hq1 hqq hc0 hc12 hα1 hα1p
  have hG12 : G q c (α1 c) < G q c (α2 c) := by
    have h1 : G q c (α1 c) < G q c (Real.pi - γ) :=
      P1_lt_P2 hq0 hq1 hqq hc0 hc12 hα1 hα1p hγ0 hγΓ
    have hπγ : Real.pi - γ = α2 c := by linarith [hγdef]
    simpa [hπγ] using h1
  have hM : Mf (α2 c) c q ≤ Mf (α1 c) c q := by
    unfold Fe at hFe
    linarith
  rw [hderiv]
  exact SymlineKeyLemma.Fep_lt_zero_of_nonneg hM2 hG1 hG12 hM

/-- KEY LEMMA for the concrete `Fe` (thm:keylemma) with the analytic
hooks isolated as hypotheses: regularity (`hcont`, `hdiff`), the right
limit at `0+` (`hlim`), the value at `1/2` (`hFe12`), the derivative
identity (`hderiv`, eq:Fep) and the branch reduction (`hbranch`).  The
conclusion is the unique zero in `(0, 1/2)` with the sign conclusions of
(eq:FeSign); the `c > 1/2` part is lem:easy (not here). -/
theorem keylemma_concrete
    {q : ℝ} {α1 α2 : ℝ → ℝ} (hq0 : 0 < q) (hqq : q0 ≤ q) (hq1 : q ≤ 1)
    (hcont : ContinuousOn (fun c : ℝ => Fe q c (α1 c) (α2 c)) (Set.Ioc 0 (1 / 2)))
    (hdiff : ∀ c ∈ Set.Ioo 0 (1 / 2),
      DifferentiableAt ℝ (fun c : ℝ => Fe q c (α1 c) (α2 c)) c)
    (hlim : Tendsto (fun c : ℝ => Fe q c (α1 c) (α2 c)) (𝓝[>] 0)
      (𝓝 (Real.pi ^ 2 / (4 * q))))
    (hFe12 : Fe q (1 / 2) (α1 (1 / 2)) (α2 (1 / 2)) < 0)
    (hderiv : ∀ c ∈ Set.Ioo 0 (1 / 2),
      deriv (fun c : ℝ => Fe q c (α1 c) (α2 c)) c =
        (Mf (α1 c) c q - Mf (α2 c) c q) * G q c (α1 c) +
          Mf (α2 c) c q * (G q c (α1 c) - G q c (α2 c)))
    (hbranch : ∀ c ∈ Set.Ioo 0 (1 / 2),
      0 < α1 c ∧ α1 c < Real.pi / 2 ∧
        0 < Real.pi - α2 c ∧ Real.pi - α2 c ≤ Gamma0) :
    ∃ c, c ∈ Set.Ioo 0 (1 / 2) ∧ Fe q c (α1 c) (α2 c) = 0 ∧
      (∀ x ∈ Set.Ioo 0 c, 0 < Fe q x (α1 x) (α2 x)) ∧
      (∀ x ∈ Set.Ioo c (1 / 2), Fe q x (α1 x) (α2 x) < 0) ∧
      (∀ c', c' ∈ Set.Ioo 0 (1 / 2) → Fe q c' (α1 c') (α2 c') = 0 → c' = c) := by
  let F : ℝ → ℝ := fun c => Fe q c (α1 c) (α2 c)
  have hab : (0 : ℝ) < 1 / 2 := by norm_num
  have hL : 0 < Real.pi ^ 2 / (4 * q) := FeZero_limit_pos hq0
  have hmono : ∀ x ∈ Set.Ioo 0 (1 / 2), 0 ≤ F x → deriv F x < 0 := by
    intro c hc hF
    rcases hbranch c hc with ⟨hα1, hα1p, hγ0, hγΓ⟩
    have hstep := Fe_deriv_neg_of_nonneg (q := q) (α1 := α1) (α2 := α2)
      (γ := Real.pi - α2 c) hq0 hq1 hqq hc.1 hc.2 hα1 hα1p hγ0 hγΓ rfl
      (by simpa [F] using hF) (hderiv c hc)
    simpa [F] using hstep
  simpa [F] using
    (existsUnique_zero_signs_of_nonneg_mono (f := F) hab
      (by simpa [F] using hcont) (by simpa [F] using hlim) hL
      (by simpa [F] using hdiff) hmono (by simpa [F] using hFe12))

end
end SymlineUniqueZero
end SL
