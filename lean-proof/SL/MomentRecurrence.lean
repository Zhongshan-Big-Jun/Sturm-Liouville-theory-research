import Mathlib
import SL.KcPolynomial
import SL.StabilityGrowth

/-!
# Moment recurrence for a linear functional and the scaling lemma

Formalization of the moment-jump step from docs/SL_h2_completeness_proof.tex
(Section 3.2) and tools/left-definite-moment-recurrence.md:

Let M : Polynomial ℚ →ₗ[ℚ] ℚ be a linear functional with moments
mu k := M (X^k).  If M vanishes on the jump family, i.e.
M (K_c p_even n) = 0 for every n >= 2, then the even moments satisfy the
second-order jump recurrence

  c * mu (2*n) = A_n * mu (2*n - 2) - B_n * mu (2*n - 4)      (n >= 2),

with A_n = 2n(2n-1) + c*n/(n-1) and B_n = 2n(2n-3); the odd moments satisfy
the analogous recurrence with (A'_n, B'_n).  Together with mu 0 = 0 (resp.
mu 1 = 0) this determines the whole even (resp. odd) subsequence from the
single free parameter mu 2 (resp. mu 3):

  mu (2*m)     = mu 2 * u_m,      mu (2*m + 1) = mu 3 * u'_m,

where u is the fundamental solution of the general jump recurrence
(cf. SL/StabilityGrowth.lean).  All statements are over ℚ to match the
exact rational coefficient identities in SL/KcPolynomial.lean; the identical
algebra holds over Real by change of base.

This is the algebraic core of the moment-jump completeness argument: the
growth of u (StabilityGrowth.product_growth) combined with a polynomial bound
on the moments forces mu 2 = mu 3 = 0.
-/

namespace SL

namespace MomentRecurrence

open Polynomial

variable {c : ℚ}

noncomputable def moments (M : Polynomial ℚ →ₗ[ℚ] ℚ) (k : Nat) : ℚ :=
  M (X ^ k)

@[simp] lemma apply_C_mul_X_pow (M : Polynomial ℚ →ₗ[ℚ] ℚ) (a : ℚ) (m : Nat) :
    M (C a * X ^ m) = a * M (X ^ m) := by
  rw [← Polynomial.smul_eq_C_mul]
  exact map_smul M a (X ^ m)

lemma even_recurrence (M : Polynomial ℚ →ₗ[ℚ] ℚ) {n : Nat} (hn : 2 ≤ n)
    (horth : M (KcPolynomial.Kc c (KcPolynomial.pEven n)) = 0) :
    c * moments M (2 * n) =
      KcPolynomial.A c n * moments M (2 * n - 2) - KcPolynomial.B n * moments M (2 * n - 4) := by
  have hK := KcPolynomial.Kc_pEven c hn
  have hM : M (KcPolynomial.Kc c (KcPolynomial.pEven n)) =
      c * moments M (2 * n) - KcPolynomial.A c n * moments M (2 * n - 2) +
        KcPolynomial.B n * moments M (2 * n - 4) := by
    rw [hK]
    simp [moments]
  rw [horth] at hM
  linarith

lemma odd_recurrence (M : Polynomial ℚ →ₗ[ℚ] ℚ) {n : Nat} (hn : 2 ≤ n)
    (horth : M (KcPolynomial.Kc c (KcPolynomial.pOdd n)) = 0) :
    c * moments M (2 * n + 1) =
      KcPolynomial.A' c n * moments M (2 * n - 1) - KcPolynomial.B' n * moments M (2 * n - 3) := by
  have hK := KcPolynomial.Kc_pOdd c hn
  have hM : M (KcPolynomial.Kc c (KcPolynomial.pOdd n)) =
      c * moments M (2 * n + 1) - KcPolynomial.A' c n * moments M (2 * n - 1) +
        KcPolynomial.B' n * moments M (2 * n - 3) := by
    rw [hK]
    simp [moments]
  rw [horth] at hM
  linarith

lemma constant_orth_moment_zero (M : Polynomial ℚ →ₗ[ℚ] ℚ) (hc : c ≠ 0)
    (horth : M (KcPolynomial.Kc c 1) = 0) : moments M 0 = 0 := by
  have hK : KcPolynomial.Kc c 1 = C c := by
    simp [KcPolynomial.Kc]
  have hM : M (KcPolynomial.Kc c 1) = c * moments M 0 := by
    rw [hK]
    simpa [moments] using (apply_C_mul_X_pow M c 0)
  rw [horth] at hM
  have hmul : c * moments M 0 = 0 := by linarith
  exact (mul_eq_zero.mp hmul).resolve_left hc

lemma linear_orth_moment_zero (M : Polynomial ℚ →ₗ[ℚ] ℚ) (hc : c ≠ 0)
    (horth : M (KcPolynomial.Kc c X) = 0) : moments M 1 = 0 := by
  have hK : KcPolynomial.Kc c X = C c * X := by
    simp [KcPolynomial.Kc]
  have hM : M (KcPolynomial.Kc c X) = c * moments M 1 := by
    rw [hK]
    simpa [moments] using (apply_C_mul_X_pow M c 1)
  rw [horth] at hM
  have hmul : c * moments M 1 = 0 := by linarith
  exact (mul_eq_zero.mp hmul).resolve_left hc

theorem scaling (c0 : ℚ) (A B : Nat → ℚ) (hc0 : c0 ≠ 0) (v : Nat → ℚ)
    (h0 : v 0 = 0)
    (hrec : ∀ n : Nat, 2 ≤ n → c0 * v n = A n * v (n - 1) - B n * v (n - 2)) :
    ∀ m : Nat, v m = v 1 * StabilityGrowth.u (K := ℚ) c0 A B m := by
  intro m
  refine Nat.strong_induction_on m ?_
  intro m ih
  by_cases hm0 : m = 0
  . subst m
    simp [StabilityGrowth.u, h0]
  by_cases hm1 : m = 1
  . subst m
    simp [StabilityGrowth.u]
  . have hm2 : 2 ≤ m := by omega
    have hrec_m : c0 * v m = A m * v (m - 1) - B m * v (m - 2) := hrec m hm2
    have hprev1 : v (m - 1) = v 1 * StabilityGrowth.u (K := ℚ) c0 A B (m - 1) := ih (m - 1) (by omega)
    have hprev2 : v (m - 2) = v 1 * StabilityGrowth.u (K := ℚ) c0 A B (m - 2) := ih (m - 2) (by omega)
    have hu : c0 * StabilityGrowth.u (K := ℚ) c0 A B m =
        A m * StabilityGrowth.u (K := ℚ) c0 A B (m - 1) - B m * StabilityGrowth.u (K := ℚ) c0 A B (m - 2) := by
      have h := StabilityGrowth.u_recurrence (K := ℚ) (c0 := c0) (A := A) (B := B) hc0 (j := m - 2)
      have hsub1 : m - 2 + 2 = m := by omega
      have hsub2 : m - 2 + 1 = m - 1 := by omega
      simpa [hsub1, hsub2] using h
    have hgoal : c0 * v m = c0 * (v 1 * StabilityGrowth.u (K := ℚ) c0 A B m) := by
      calc
        c0 * v m = A m * v (m - 1) - B m * v (m - 2) := hrec_m
        _ = A m * (v 1 * StabilityGrowth.u (K := ℚ) c0 A B (m - 1)) -
            B m * (v 1 * StabilityGrowth.u (K := ℚ) c0 A B (m - 2)) := by rw [hprev1, hprev2]
        _ = v 1 * (A m * StabilityGrowth.u (K := ℚ) c0 A B (m - 1) -
            B m * StabilityGrowth.u (K := ℚ) c0 A B (m - 2)) := by ring
        _ = v 1 * (c0 * StabilityGrowth.u (K := ℚ) c0 A B m) := by rw [hu]
        _ = c0 * (v 1 * StabilityGrowth.u (K := ℚ) c0 A B m) := by ring
    exact mul_left_cancel₀ hc0 hgoal

theorem even_scaling (c0 : ℚ) (A B : Nat → ℚ) (hc0 : c0 ≠ 0) (mu : Nat → ℚ)
    (h0 : mu 0 = 0)
    (hrec : ∀ n : Nat, 2 ≤ n → c0 * mu (2 * n) = A n * mu (2 * n - 2) - B n * mu (2 * n - 4)) :
    ∀ m : Nat, mu (2 * m) = mu 2 * StabilityGrowth.u (K := ℚ) c0 A B m := by
  let v : Nat → ℚ := fun n => mu (2 * n)
  have hv0 : v 0 = 0 := by simp [v, h0]
  have hv_rec : ∀ n : Nat, 2 ≤ n → c0 * v n = A n * v (n - 1) - B n * v (n - 2) := by
    intro n hn
    have h := hrec n hn
    have h1 : 2 * n - 2 = 2 * (n - 1) := by omega
    have h2 : 2 * n - 4 = 2 * (n - 2) := by omega
    simpa [v, h1, h2] using h
  have hsc := scaling c0 A B hc0 v hv0 hv_rec
  intro m
  have h := hsc m
  simpa [v] using h

theorem odd_scaling (c0 : ℚ) (A' B' : Nat → ℚ) (hc0 : c0 ≠ 0) (mu : Nat → ℚ)
    (h1 : mu 1 = 0)
    (hrec : ∀ n : Nat, 2 ≤ n → c0 * mu (2 * n + 1) = A' n * mu (2 * n - 1) - B' n * mu (2 * n - 3)) :
    ∀ m : Nat, mu (2 * m + 1) = mu 3 * StabilityGrowth.u (K := ℚ) c0 A' B' m := by
  let v : Nat → ℚ := fun n => mu (2 * n + 1)
  have hv0 : v 0 = 0 := by simp [v, h1]
  have hv_rec : ∀ n : Nat, 2 ≤ n → c0 * v n = A' n * v (n - 1) - B' n * v (n - 2) := by
    intro n hn
    have h := hrec n hn
    have h1' : 2 * n - 1 = 2 * (n - 1) + 1 := by omega
    have h2' : 2 * n - 3 = 2 * (n - 2) + 1 := by omega
    simpa [v, h1', h2'] using h
  have hsc := scaling c0 A' B' hc0 v hv0 hv_rec
  intro m
  have h := hsc m
  simpa [v] using h

theorem even_moment_scaling (M : Polynomial ℚ →ₗ[ℚ] ℚ) (hc : c ≠ 0)
    (h0 : moments M 0 = 0)
    (horth : ∀ n : Nat, 2 ≤ n → M (KcPolynomial.Kc c (KcPolynomial.pEven n)) = 0) :
    ∀ m : Nat, moments M (2 * m) =
      moments M 2 * StabilityGrowth.u (K := ℚ) c (KcPolynomial.A c) (KcPolynomial.B) m := by
  apply even_scaling c (KcPolynomial.A c) (KcPolynomial.B) hc (moments M) h0
  intro n hn
  exact even_recurrence M hn (horth n hn)

theorem odd_moment_scaling (M : Polynomial ℚ →ₗ[ℚ] ℚ) (hc : c ≠ 0)
    (h1 : moments M 1 = 0)
    (horth : ∀ n : Nat, 2 ≤ n → M (KcPolynomial.Kc c (KcPolynomial.pOdd n)) = 0) :
    ∀ m : Nat, moments M (2 * m + 1) =
      moments M 3 * StabilityGrowth.u (K := ℚ) c (KcPolynomial.A' c) (KcPolynomial.B') m := by
  apply odd_scaling c (KcPolynomial.A' c) (KcPolynomial.B') hc (moments M) h1
  intro n hn
  exact odd_recurrence M hn (horth n hn)

end MomentRecurrence

end SL
