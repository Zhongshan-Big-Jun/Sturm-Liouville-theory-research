import Mathlib
import SL.ThirdOrderClosedForms

/-!
# Third-order recurrence: product-solution classification (Theorem 1, converse)

Formalization of the converse direction of Theorem 1 of
`docs/SL_third_order_recurrence_theory.tex`: if the ratio sequence
`e_j = 1 + beta/(2j)` is an exact trajectory of the ratio map for all j >= 3,
then `beta in {1,-1}` (even family) / `beta in {3,1}` (odd family).

Algebraic core: clearing denominators turns the trajectory identity into a
polynomial of degree 2 in `j` whose coefficients carry the factor
`(beta-1)(beta+1)` (even) resp. `(beta-3)(beta-1)` (odd).  Three consecutive
vanishing points then force the factor to vanish, hence `beta` is forced.
The clearing is verified by `field_simp` + `ring_nf`; the factored numerators
`TEven`/`TOdd` were obtained by symbolic computation and are recorded here as
the official cleared forms.
-/

namespace SL

namespace ThirdOrderClosedForms

/-- Simplified numerator of the cleared trajectory identity (even family),
a polynomial of degree 2 in `j`. -/
noncomputable def TEven (c β : ℚ) (j : ℕ) : ℚ :=
  (4 * (β - 1) * (β + 1)) * (j : ℚ) ^ 2 +
    (2 * (β - 6) * (β - 1) * (β + 1)) * (j : ℚ) -
      (β - 1) * (β + 1) * (2 * β + c - 8)

/-- Simplified numerator of the cleared trajectory identity (odd family),
a polynomial of degree 2 in `j`. -/
noncomputable def TOdd (c β : ℚ) (j : ℕ) : ℚ :=
  (4 * (β - 3) * (β - 1)) * (j : ℚ) ^ 2 +
    (2 * (β - 6) * (β - 3) * (β - 1)) * (j : ℚ) -
      (β - 3) * (β - 1) * (2 * β + c - 8)

/-- `eSeq beta j = (beta + 2j) / (2j)`. -/
lemma eSeq_eq (β : ℚ) (j : ℕ) (hj : (j : ℚ) ≠ 0) :
    eSeq β j = (β + 2 * (j : ℚ)) / (2 * (j : ℚ)) := by
  unfold eSeq
  field_simp [hj]
  ring

/-- Nonzero criterion for `eSeq beta j` (j nonzero). -/
lemma eSeq_ne_zero_iff (β : ℚ) (j : ℕ) (hj : (j : ℚ) ≠ 0) :
    eSeq β j ≠ 0 ↔ β + 2 * (j : ℚ) ≠ 0 := by
  rw [eSeq_eq β j hj]
  constructor
  · intro h hb
    rw [hb] at h
    simp at h
  · intro hb h
    apply hb
    rcases div_eq_zero_iff.mp h with hz | hd
    · exact hz
    · exfalso
      apply hj
      exact (mul_eq_zero.mp hd).resolve_left (by norm_num)

/-- Trajectory identity (even family) at the concrete indices j = 3, 4, 5
forces the cleared numerator to vanish. -/
lemma TEven_of_trajectory_at (c β : ℚ) (hc : c ≠ 0) (j : ℕ)
    (hj : j = 3 ∨ j = 4 ∨ j = 5)
    (h2 : eSeq β (j - 1) ≠ 0) (h1 : eSeq β (j - 2) ≠ 0)
    (h : eSeq β j =
      ThirdOrder.ratioMap (a1Even c) (a2Even c) (a3Even c) j
        (eSeq β (j - 1)) (eSeq β (j - 2))) :
    TEven c β j = 0 := by
  rcases hj with rfl | rfl | rfl
  · -- j = 3
    have h2b : β + 4 ≠ 0 := by
      have h' := (eSeq_ne_zero_iff β 2 (by norm_num)).mp h2
      norm_num at h'
      exact h'
    have h1b : β + 2 ≠ 0 := by
      have h' := (eSeq_ne_zero_iff β 1 (by norm_num)).mp h1
      norm_num at h'
      exact h'
    have h2e : 1 + β / 4 ≠ 0 := by
      have h' : 1 + β / (2 * 2) ≠ 0 := by simpa [eSeq] using h2
      norm_num at h'
      exact h'
    have h1e : 1 + β / 2 ≠ 0 := by
      have h' : 1 + β / (2 * 1) ≠ 0 := by simpa [eSeq] using h1
      norm_num at h'
      exact h'
    unfold ThirdOrder.ratioMap a1Even a2Even a3Even PEven QEven REven lambda eSeq at h
    unfold TEven at ⊢
    have h2c : 4 + β ≠ 0 := by simpa [add_comm] using h2b
    have h1c : 2 + β ≠ 0 := by simpa [add_comm] using h1b
    have h12c : 8 + β * 6 + β ^ 2 ≠ 0 := by
      have hprod : (2 + β) * (4 + β) = 8 + β * 6 + β ^ 2 := by ring
      rw [← hprod]
      exact mul_ne_zero h1c h2c
    field_simp [hc, h2b, h1b, h2e, h1e, h2c, h1c, h12c] at h
    ring_nf at h
    field_simp [h2c, h1c, h12c] at h
    ring_nf at h ⊢
    have hsub :
        3072 + β * 2816 + β ^ 2 * 768 + β ^ 3 * 64 - (3200 + β * 2880 + β ^ 2 * 640 + β ^ 2 * c * 16 - c * 16) = 0 := by
      exact sub_eq_zero.mpr h
    have hfac :
        3072 + β * 2816 + β ^ 2 * 768 + β ^ 3 * 64 - (3200 + β * 2880 + β ^ 2 * 640 + β ^ 2 * c * 16 - c * 16) =
          (16 : ℚ) * (-8 - β * 4 + β ^ 2 * 8 - β ^ 2 * c + β ^ 3 * 4 + c) := by
      ring_nf
    rw [hfac] at hsub
    exact (mul_eq_zero.mp hsub).resolve_left (by norm_num)


  · -- j = 4
    have h2b : β + 6 ≠ 0 := by
      have h' := (eSeq_ne_zero_iff β 3 (by norm_num)).mp h2
      norm_num at h'
      exact h'
    have h1b : β + 4 ≠ 0 := by
      have h' := (eSeq_ne_zero_iff β 2 (by norm_num)).mp h1
      norm_num at h'
      exact h'
    have h2e : 1 + β / 6 ≠ 0 := by
      have h' : 1 + β / (2 * 3) ≠ 0 := by simpa [eSeq] using h2
      norm_num at h'
      exact h'
    have h1e : 1 + β / 4 ≠ 0 := by
      have h' : 1 + β / (2 * 2) ≠ 0 := by simpa [eSeq] using h1
      norm_num at h'
      exact h'
    unfold ThirdOrder.ratioMap a1Even a2Even a3Even PEven QEven REven lambda eSeq at h
    unfold TEven at ⊢
    have h2c : 6 + β ≠ 0 := by simpa [add_comm] using h2b
    have h1c : 4 + β ≠ 0 := by simpa [add_comm] using h1b
    have h12c : 24 + β * 10 + β ^ 2 ≠ 0 := by
      have hprod : (4 + β) * (6 + β) = 24 + β * 10 + β ^ 2 := by ring
      rw [← hprod]
      exact mul_ne_zero h1c h2c
    field_simp [hc, h2b, h1b, h2e, h1e, h2c, h1c, h12c] at h
    ring_nf at h
    field_simp [h2c, h1c, h12c] at h
    ring_nf at h ⊢
    have hsub :
        331776 + β * 235008 + β ^ 2 * 61056 + β ^ 3 * 6912 + β ^ 4 * 288 - (338688 + β * 237888 - β * c * 48 + β ^ 2 * 54432 + β ^ 2 * c * 288 + β ^ 3 * 4032 + β ^ 3 * c * 48 - c * 288) = 0 := by
      exact sub_eq_zero.mpr h
    have hfac :
        331776 + β * 235008 + β ^ 2 * 61056 + β ^ 3 * 6912 + β ^ 4 * 288 - (338688 + β * 237888 - β * c * 48 + β ^ 2 * 54432 + β ^ 2 * c * 288 + β ^ 3 * 4032 + β ^ 3 * c * 48 - c * 288) =
          (48 : ℚ) * (6 + β) * (-24 - β * 6 + β ^ 2 * 24 - β ^ 2 * c + β ^ 3 * 6 + c) := by
      ring_nf
    rw [hfac] at hsub
    exact (mul_eq_zero.mp hsub).resolve_left (mul_ne_zero (by norm_num) h2c)

  · -- j = 5
    have h2b : β + 8 ≠ 0 := by
      have h' := (eSeq_ne_zero_iff β 4 (by norm_num)).mp h2
      norm_num at h'
      exact h'
    have h1b : β + 6 ≠ 0 := by
      have h' := (eSeq_ne_zero_iff β 3 (by norm_num)).mp h1
      norm_num at h'
      exact h'
    have h2e : 1 + β / 8 ≠ 0 := by
      have h' : 1 + β / (2 * 4) ≠ 0 := by simpa [eSeq] using h2
      norm_num at h'
      exact h'
    have h1e : 1 + β / 6 ≠ 0 := by
      have h' : 1 + β / (2 * 3) ≠ 0 := by simpa [eSeq] using h1
      norm_num at h'
      exact h'
    unfold ThirdOrder.ratioMap a1Even a2Even a3Even PEven QEven REven lambda eSeq at h
    unfold TEven at ⊢
    have h2c : 8 + β ≠ 0 := by simpa [add_comm] using h2b
    have h1c : 6 + β ≠ 0 := by simpa [add_comm] using h1b
    have h12c : 48 + β * 14 + β ^ 2 ≠ 0 := by
      have hprod : (6 + β) * (8 + β) = 48 + β * 14 + β ^ 2 := by ring
      rw [← hprod]
      exact mul_ne_zero h1c h2c
    field_simp [hc, h2b, h1b, h2e, h1e, h2c, h1c, h12c] at h
    ring_nf at h
    field_simp [h2c, h1c, h12c] at h
    ring_nf at h ⊢
    have hsub :
        2949120 + β * 1523712 + β ^ 2 * 291840 + β ^ 3 * 24576 + β ^ 4 * 768 - (2985984 + β * 1534464 - β * c * 96 + β ^ 2 * 255744 + β ^ 2 * c * 768 + β ^ 3 * 13824 + β ^ 3 * c * 96 - c * 768) = 0 := by
      exact sub_eq_zero.mpr h
    have hfac :
        2949120 + β * 1523712 + β ^ 2 * 291840 + β ^ 3 * 24576 + β ^ 4 * 768 - (2985984 + β * 1534464 - β * c * 96 + β ^ 2 * 255744 + β ^ 2 * c * 768 + β ^ 3 * 13824 + β ^ 3 * c * 96 - c * 768) =
          (96 : ℚ) * (8 + β) * (-48 - β * 8 + β ^ 2 * 48 - β ^ 2 * c + β ^ 3 * 8 + c) := by
      ring_nf
    rw [hfac] at hsub
    exact (mul_eq_zero.mp hsub).resolve_left (mul_ne_zero (by norm_num) h2c)

/-- Trajectory identity (odd family) at the concrete indices j = 3, 4, 5
forces the cleared numerator to vanish. -/
lemma TOdd_of_trajectory_at (c β : ℚ) (hc : c ≠ 0) (j : ℕ)
    (hj : j = 3 ∨ j = 4 ∨ j = 5)
    (h2 : eSeq β (j - 1) ≠ 0) (h1 : eSeq β (j - 2) ≠ 0)
    (h : eSeq β j =
      ThirdOrder.ratioMap (a1Odd c) (a2Odd c) (a3Odd c) j
        (eSeq β (j - 1)) (eSeq β (j - 2))) :
    TOdd c β j = 0 := by
  rcases hj with rfl | rfl | rfl
  · -- j = 3
    have h2b : β + 4 ≠ 0 := by
      have h' := (eSeq_ne_zero_iff β 2 (by norm_num)).mp h2
      norm_num at h'
      exact h'
    have h1b : β + 2 ≠ 0 := by
      have h' := (eSeq_ne_zero_iff β 1 (by norm_num)).mp h1
      norm_num at h'
      exact h'
    have h2e : 1 + β / 4 ≠ 0 := by
      have h' : 1 + β / (2 * 2) ≠ 0 := by simpa [eSeq] using h2
      norm_num at h'
      exact h'
    have h1e : 1 + β / 2 ≠ 0 := by
      have h' : 1 + β / (2 * 1) ≠ 0 := by simpa [eSeq] using h1
      norm_num at h'
      exact h'
    unfold ThirdOrder.ratioMap a1Odd a2Odd a3Odd POdd QOdd ROdd lambda eSeq at h
    unfold TOdd at ⊢
    have h2c : 4 + β ≠ 0 := by simpa [add_comm] using h2b
    have h1c : 2 + β ≠ 0 := by simpa [add_comm] using h1b
    have h12c : 8 + β * 6 + β ^ 2 ≠ 0 := by
      have hprod : (2 + β) * (4 + β) = 8 + β * 6 + β ^ 2 := by ring
      rw [← hprod]
      exact mul_ne_zero h1c h2c
    field_simp [hc, h2b, h1b, h2e, h1e, h2c, h1c, h12c] at h
    ring_nf at h
    field_simp [h2c, h1c, h12c] at h
    ring_nf at h ⊢
    have hsub :
        3072 + β * 2816 + β ^ 2 * 768 + β ^ 3 * 64 - (2688 + β * 3136 - β * c * 64 + β ^ 2 * 896 + β ^ 2 * c * 16 + c * 48) = 0 := by
      exact sub_eq_zero.mpr h
    have hfac :
        3072 + β * 2816 + β ^ 2 * 768 + β ^ 3 * 64 - (2688 + β * 3136 - β * c * 64 + β ^ 2 * 896 + β ^ 2 * c * 16 + c * 48) =
          (16 : ℚ) * (24 - β * 20 + β * c * 4 - β ^ 2 * 8 - β ^ 2 * c + β ^ 3 * 4 - c * 3) := by
      ring_nf
    rw [hfac] at hsub
    exact (mul_eq_zero.mp hsub).resolve_left (by norm_num)


  · -- j = 4
    have h2b : β + 6 ≠ 0 := by
      have h' := (eSeq_ne_zero_iff β 3 (by norm_num)).mp h2
      norm_num at h'
      exact h'
    have h1b : β + 4 ≠ 0 := by
      have h' := (eSeq_ne_zero_iff β 2 (by norm_num)).mp h1
      norm_num at h'
      exact h'
    have h2e : 1 + β / 6 ≠ 0 := by
      have h' : 1 + β / (2 * 3) ≠ 0 := by simpa [eSeq] using h2
      norm_num at h'
      exact h'
    have h1e : 1 + β / 4 ≠ 0 := by
      have h' : 1 + β / (2 * 2) ≠ 0 := by simpa [eSeq] using h1
      norm_num at h'
      exact h'
    unfold ThirdOrder.ratioMap a1Odd a2Odd a3Odd POdd QOdd ROdd lambda eSeq at h
    unfold TOdd at ⊢
    have h2c : 6 + β ≠ 0 := by simpa [add_comm] using h2b
    have h1c : 4 + β ≠ 0 := by simpa [add_comm] using h1b
    have h12c : 24 + β * 10 + β ^ 2 ≠ 0 := by
      have hprod : (4 + β) * (6 + β) = 24 + β * 10 + β ^ 2 := by ring
      rw [← hprod]
      exact mul_ne_zero h1c h2c
    field_simp [hc, h2b, h1b, h2e, h1e, h2c, h1c, h12c] at h
    ring_nf at h
    field_simp [h2c, h1c, h12c] at h
    ring_nf at h ⊢
    have hsub :
        331776 + β * 235008 + β ^ 2 * 61056 + β ^ 3 * 6912 + β ^ 4 * 288 - (311040 + β * 254016 - β * c * 1008 + β ^ 2 * 64800 + β ^ 2 * c * 96 + β ^ 3 * 5184 + β ^ 3 * c * 48 + c * 864) = 0 := by
      exact sub_eq_zero.mpr h
    have hfac :
        331776 + β * 235008 + β ^ 2 * 61056 + β ^ 3 * 6912 + β ^ 4 * 288 - (311040 + β * 254016 - β * c * 1008 + β ^ 2 * 64800 + β ^ 2 * c * 96 + β ^ 3 * 5184 + β ^ 3 * c * 48 + c * 864) =
          (48 : ℚ) * (6 + β) * (72 - β * 78 + β * c * 4 - β ^ 2 * c + β ^ 3 * 6 - c * 3) := by
      ring_nf
    rw [hfac] at hsub
    exact (mul_eq_zero.mp hsub).resolve_left (mul_ne_zero (by norm_num) h2c)

  · -- j = 5
    have h2b : β + 8 ≠ 0 := by
      have h' := (eSeq_ne_zero_iff β 4 (by norm_num)).mp h2
      norm_num at h'
      exact h'
    have h1b : β + 6 ≠ 0 := by
      have h' := (eSeq_ne_zero_iff β 3 (by norm_num)).mp h1
      norm_num at h'
      exact h'
    have h2e : 1 + β / 8 ≠ 0 := by
      have h' : 1 + β / (2 * 4) ≠ 0 := by simpa [eSeq] using h2
      norm_num at h'
      exact h'
    have h1e : 1 + β / 6 ≠ 0 := by
      have h' : 1 + β / (2 * 3) ≠ 0 := by simpa [eSeq] using h1
      norm_num at h'
      exact h'
    unfold ThirdOrder.ratioMap a1Odd a2Odd a3Odd POdd QOdd ROdd lambda eSeq at h
    unfold TOdd at ⊢
    have h2c : 8 + β ≠ 0 := by simpa [add_comm] using h2b
    have h1c : 6 + β ≠ 0 := by simpa [add_comm] using h1b
    have h12c : 48 + β * 14 + β ^ 2 ≠ 0 := by
      have hprod : (6 + β) * (8 + β) = 48 + β * 14 + β ^ 2 := by ring
      rw [← hprod]
      exact mul_ne_zero h1c h2c
    field_simp [hc, h2b, h1b, h2e, h1e, h2c, h1c, h12c] at h
    ring_nf at h
    field_simp [h2c, h1c, h12c] at h
    ring_nf at h ⊢
    have hsub :
        2949120 + β * 1523712 + β ^ 2 * 291840 + β ^ 3 * 24576 + β ^ 4 * 768 - (2838528 + β * 1638912 - β * c * 2784 + β ^ 2 * 295680 + β ^ 2 * c * 384 + β ^ 3 * 16896 + β ^ 3 * c * 96 + c * 2304) = 0 := by
      exact sub_eq_zero.mpr h
    have hfac :
        2949120 + β * 1523712 + β ^ 2 * 291840 + β ^ 3 * 24576 + β ^ 4 * 768 - (2838528 + β * 1638912 - β * c * 2784 + β ^ 2 * 295680 + β ^ 2 * c * 384 + β ^ 3 * 16896 + β ^ 3 * c * 96 + c * 2304) =
          (96 : ℚ) * (8 + β) * (144 - β * 168 + β * c * 4 + β ^ 2 * 16 - β ^ 2 * c + β ^ 3 * 8 - c * 3) := by
      ring_nf
    rw [hfac] at hsub
    exact (mul_eq_zero.mp hsub).resolve_left (mul_ne_zero (by norm_num) h2c)

/-- The quadratic factor `4j^2 + 2(beta-6)j - (2*beta + c - 8)` appearing in
the cleared numerators. -/
noncomputable def QFactor (c β : ℚ) (j : ℚ) : ℚ :=
  4 * j ^ 2 + 2 * (β - 6) * j - (2 * β + c - 8)

/-- `TEven c beta j = (beta^2 - 1) * QFactor c beta j`. -/
lemma TEven_eq_factor (c β : ℚ) (j : ℕ) :
    TEven c β j = (β ^ 2 - 1) * QFactor c β (j : ℚ) := by
  unfold TEven QFactor
  ring

/-- `TOdd c beta j = (beta - 3) * (beta - 1) * QFactor c beta j`. -/
lemma TOdd_eq_factor (c β : ℚ) (j : ℕ) :
    TOdd c β j = (β - 3) * (β - 1) * QFactor c β (j : ℚ) := by
  unfold TOdd QFactor
  ring

/-- Three consecutive vanishing points of `TEven` force `beta = 1` or `-1`. -/
lemma beta_two_of_TEven (c β : ℚ) (_hc : c ≠ 0)
    (h3 : TEven c β 3 = 0) (h4 : TEven c β 4 = 0) (h5 : TEven c β 5 = 0) :
    β = 1 ∨ β = -1 := by
  have hb2 : β ^ 2 - 1 = 0 := by
    by_contra hb
    have hQ3 : QFactor c β 3 = 0 := by
      have hz : (β ^ 2 - 1) * QFactor c β 3 = 0 := by
        calc
          (β ^ 2 - 1) * QFactor c β 3 = TEven c β 3 := by
            simp [TEven_eq_factor c β 3]
          _ = 0 := h3
      exact (mul_eq_zero.mp hz).resolve_left hb
    have hQ4 : QFactor c β 4 = 0 := by
      have hz : (β ^ 2 - 1) * QFactor c β 4 = 0 := by
        calc
          (β ^ 2 - 1) * QFactor c β 4 = TEven c β 4 := by
            simp [TEven_eq_factor c β 4]
          _ = 0 := h4
      exact (mul_eq_zero.mp hz).resolve_left hb
    have hQ5 : QFactor c β 5 = 0 := by
      have hz : (β ^ 2 - 1) * QFactor c β 5 = 0 := by
        calc
          (β ^ 2 - 1) * QFactor c β 5 = TEven c β 5 := by
            simp [TEven_eq_factor c β 5]
          _ = 0 := h5
      exact (mul_eq_zero.mp hz).resolve_left hb
    have hd1 : QFactor c β 4 - QFactor c β 3 = 16 + 2 * β := by
      unfold QFactor
      ring
    have hd2 : QFactor c β 5 - QFactor c β 4 = 24 + 2 * β := by
      unfold QFactor
      ring
    nlinarith
  have hb : (β - 1) * (β + 1) = 0 := by nlinarith [hb2]
  rcases mul_eq_zero.mp hb with h | h
  · exact Or.inl (sub_eq_zero.mp h)
  · exact Or.inr (eq_neg_of_add_eq_zero_left h)

/-- Three consecutive vanishing points of `TOdd` force `beta = 3` or `1`. -/
lemma beta_two_of_TOdd (c β : ℚ) (_hc : c ≠ 0)
    (h3 : TOdd c β 3 = 0) (h4 : TOdd c β 4 = 0) (h5 : TOdd c β 5 = 0) :
    β = 3 ∨ β = 1 := by
  have hb2 : (β - 3) * (β - 1) = 0 := by
    by_contra hb
    have hQ3 : QFactor c β 3 = 0 := by
      have hz : (β - 3) * (β - 1) * QFactor c β 3 = 0 := by
        calc
          (β - 3) * (β - 1) * QFactor c β 3 = TOdd c β 3 := by
            simp [TOdd_eq_factor c β 3]
          _ = 0 := h3
      exact (mul_eq_zero.mp hz).elim (fun h => (False.elim (hb h))) id
    have hQ4 : QFactor c β 4 = 0 := by
      have hz : (β - 3) * (β - 1) * QFactor c β 4 = 0 := by
        calc
          (β - 3) * (β - 1) * QFactor c β 4 = TOdd c β 4 := by
            simp [TOdd_eq_factor c β 4]
          _ = 0 := h4
      exact (mul_eq_zero.mp hz).elim (fun h => (False.elim (hb h))) id
    have hQ5 : QFactor c β 5 = 0 := by
      have hz : (β - 3) * (β - 1) * QFactor c β 5 = 0 := by
        calc
          (β - 3) * (β - 1) * QFactor c β 5 = TOdd c β 5 := by
            simp [TOdd_eq_factor c β 5]
          _ = 0 := h5
      exact (mul_eq_zero.mp hz).elim (fun h => (False.elim (hb h))) id
    have hd1 : QFactor c β 4 - QFactor c β 3 = 16 + 2 * β := by
      unfold QFactor
      ring
    have hd2 : QFactor c β 5 - QFactor c β 4 = 24 + 2 * β := by
      unfold QFactor
      ring
    nlinarith
  rcases mul_eq_zero.mp hb2 with h | h
  · exact Or.inl (sub_eq_zero.mp h)
  · exact Or.inr (sub_eq_zero.mp h)

/-- Theorem 1 (converse, even family): a trajectory of the exact form
`e_j = 1 + beta/(2j)` for all j >= 3 forces `beta = 1` or `beta = -1`. -/
theorem even_beta_classification (c : ℚ) (hc : c ≠ 0) {β : ℚ}
    (hEnz : ∀ j : ℕ, 1 ≤ j → eSeq β j ≠ 0)
    (hfp : ∀ n : ℕ,
      eSeq β (n + 3) =
        ThirdOrder.ratioMap (a1Even c) (a2Even c) (a3Even c) (n + 3)
          (eSeq β (n + 2)) (eSeq β (n + 1))) :
    β = 1 ∨ β = -1 := by
  have h3 : TEven c β 3 = 0 :=
    TEven_of_trajectory_at c β hc 3 (Or.inl rfl) (hEnz 2 (by omega)) (hEnz 1 (by omega)) (hfp 0)
  have h4 : TEven c β 4 = 0 :=
    TEven_of_trajectory_at c β hc 4 (Or.inr (Or.inl rfl)) (hEnz 3 (by omega)) (hEnz 2 (by omega)) (hfp 1)
  have h5 : TEven c β 5 = 0 :=
    TEven_of_trajectory_at c β hc 5 (Or.inr (Or.inr rfl)) (hEnz 4 (by omega)) (hEnz 3 (by omega)) (hfp 2)
  exact beta_two_of_TEven c β hc h3 h4 h5

/-- Theorem 1 (converse, odd family): a trajectory of the exact form
`e_j = 1 + beta/(2j)` for all j >= 3 forces `beta = 3` or `beta = 1`. -/
theorem odd_beta_classification (c : ℚ) (hc : c ≠ 0) {β : ℚ}
    (hEnz : ∀ j : ℕ, 1 ≤ j → eSeq β j ≠ 0)
    (hfp : ∀ n : ℕ,
      eSeq β (n + 3) =
        ThirdOrder.ratioMap (a1Odd c) (a2Odd c) (a3Odd c) (n + 3)
          (eSeq β (n + 2)) (eSeq β (n + 1))) :
    β = 3 ∨ β = 1 := by
  have h3 : TOdd c β 3 = 0 :=
    TOdd_of_trajectory_at c β hc 3 (Or.inl rfl) (hEnz 2 (by omega)) (hEnz 1 (by omega)) (hfp 0)
  have h4 : TOdd c β 4 = 0 :=
    TOdd_of_trajectory_at c β hc 4 (Or.inr (Or.inl rfl)) (hEnz 3 (by omega)) (hEnz 2 (by omega)) (hfp 1)
  have h5 : TOdd c β 5 = 0 :=
    TOdd_of_trajectory_at c β hc 5 (Or.inr (Or.inr rfl)) (hEnz 4 (by omega)) (hEnz 3 (by omega)) (hfp 2)
  exact beta_two_of_TOdd c β hc h3 h4 h5

end ThirdOrderClosedForms

end SL
