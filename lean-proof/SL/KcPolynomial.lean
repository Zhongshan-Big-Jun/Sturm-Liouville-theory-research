import Mathlib

/-!
# K_c action on the H^2 polynomial basis: coefficient identities

Formalization of the explicit polynomial identities from
`docs/SL_h2_completeness_proof.tex` (Lemma 4.1): for n >= 2,

  K_c p_{2n}   = c x^{2n}   - A_n x^{2n-2}   + B_n x^{2n-4},
  K_c p_{2n+1} = c x^{2n+1} - A'_n x^{2n-1}  + B'_n x^{2n-3},

where p_{2n}(x) = x^{2n} - n/(n-1) x^{2n-2} (and the odd analogue),
K_c f = -f'' + c f, and

  A_n  = 2n(2n-1) + c n/(n-1),   B_n  = 2n(2n-3),
  A'_n = 2n(2n+1) + c n/(n-1),   B'_n = 2n(2n-1).

These identities are the algebraic core of the moment-jump recurrence
c mu_{2j} = A_j mu_{2j-2} - B_j mu_{2j-4} for the moments of a function
orthogonal to {K_c p_n} in L^2(-1,1).
-/

namespace SL

namespace KcPolynomial

open Polynomial

noncomputable def q (n : ℕ) : ℚ := (n : ℚ) / ((n - 1 : ℕ) : ℚ)

noncomputable def pEven (n : ℕ) : Polynomial ℚ :=
  X ^ (2 * n) - C (q n) * X ^ (2 * n - 2)

noncomputable def pOdd (n : ℕ) : Polynomial ℚ :=
  X ^ (2 * n + 1) - C (q n) * X ^ (2 * n - 1)

noncomputable def A (c : ℚ) (n : ℕ) : ℚ :=
  ((2 * n : ℕ) : ℚ) * ((2 * n - 1 : ℕ) : ℚ) + c * q n

noncomputable def A' (c : ℚ) (n : ℕ) : ℚ :=
  ((2 * n : ℕ) : ℚ) * ((2 * n + 1 : ℕ) : ℚ) + c * q n

noncomputable def B (n : ℕ) : ℚ :=
  ((2 * n : ℕ) : ℚ) * ((2 * n - 3 : ℕ) : ℚ)

noncomputable def B' (n : ℕ) : ℚ :=
  ((2 * n : ℕ) : ℚ) * ((2 * n - 1 : ℕ) : ℚ)

noncomputable def Kc (c : ℚ) (p : Polynomial ℚ) : Polynomial ℚ :=
  -(derivative (derivative p)) + C c * p

lemma derivative_two_X_pow (k : ℕ) :
    derivative (derivative (X ^ k)) = C (k : ℚ) * C ((k - 1 : ℕ) : ℚ) * X ^ (k - 2) := by
  rw [derivative_X_pow, derivative_C_mul, derivative_X_pow, Nat.sub_sub]
  ring

lemma Kc_sub (c : ℚ) (p q : Polynomial ℚ) : Kc c (p - q) = Kc c p - Kc c q := by
  unfold Kc
  rw [derivative_sub, derivative_sub]
  ring

lemma Kc_monomial (c : ℚ) (a : ℚ) (m : ℕ) :
    Kc c (C a * X ^ m) =
      C c * C a * X ^ m - C a * C (m : ℚ) * C ((m - 1 : ℕ) : ℚ) * X ^ (m - 2) := by
  unfold Kc
  rw [derivative_C_mul, derivative_X_pow, derivative_C_mul, derivative_C_mul, derivative_X_pow,
    Nat.sub_sub]
  ring

lemma Kc_X_pow (c : ℚ) (m : ℕ) :
    Kc c (X ^ m) = C c * X ^ m - C (m : ℚ) * C ((m - 1 : ℕ) : ℚ) * X ^ (m - 2) := by
  simpa using Kc_monomial c 1 m

lemma A_prod (c : ℚ) (n : ℕ) :
    C (A c n) = C ((2 * n : ℕ) : ℚ) * C ((2 * n - 1 : ℕ) : ℚ) + C c * C (q n) := by
  rw [← Polynomial.C_mul, ← Polynomial.C_mul, ← Polynomial.C_add]
  rfl

lemma A'_prod (c : ℚ) (n : ℕ) :
    C (A' c n) = C ((2 * n : ℕ) : ℚ) * C ((2 * n + 1 : ℕ) : ℚ) + C c * C (q n) := by
  rw [← Polynomial.C_mul, ← Polynomial.C_mul, ← Polynomial.C_add]
  rfl

lemma B_coeff (n : ℕ) (hn : 2 ≤ n) :
    q n * ((2 * n - 2 : ℕ) : ℚ) * ((2 * n - 3 : ℕ) : ℚ) =
      ((2 * n : ℕ) : ℚ) * ((2 * n - 3 : ℕ) : ℚ) := by
  unfold q
  have hden : ((n - 1 : ℕ) : ℚ) ≠ 0 := by
    exact_mod_cast (by omega : (n - 1 : ℕ) ≠ 0)
  field_simp [hden]
  have hA : ((2 * n - 2 : ℕ) : ℚ) = (2 : ℚ) * ((n - 1 : ℕ) : ℚ) := by
    have h : 2 * n - 2 = 2 * (n - 1) := by omega
    rw [h]
    norm_num
  have hB : ((2 * n - 3 : ℕ) : ℚ) = (2 : ℚ) * ((n - 1 : ℕ) : ℚ) - 1 := by
    have h : 2 * n - 3 = 2 * (n - 1) - 1 := by omega
    rw [h]
    rw [Nat.cast_sub (by omega : 1 ≤ 2 * (n - 1))]
    norm_num
  have hC : ((2 * n : ℕ) : ℚ) = (2 : ℚ) * ((n - 1 : ℕ) : ℚ) + 2 := by
    have h : 2 * n = 2 * (n - 1) + 2 := by omega
    rw [h]
    norm_num
  have hn' : (n : ℚ) = ((n - 1 : ℕ) : ℚ) + 1 := by
    have hsub : n = (n - 1) + 1 := (Nat.sub_add_cancel (by omega : 1 ≤ n)).symm
    rw [hsub]
    norm_num
  rw [hA, hB, hC, hn']
  ring

lemma B'_coeff (n : ℕ) (hn : 2 ≤ n) :
    q n * ((2 * n - 2 : ℕ) : ℚ) * ((2 * n - 1 : ℕ) : ℚ) =
      ((2 * n : ℕ) : ℚ) * ((2 * n - 1 : ℕ) : ℚ) := by
  unfold q
  have hden : ((n - 1 : ℕ) : ℚ) ≠ 0 := by
    exact_mod_cast (by omega : (n - 1 : ℕ) ≠ 0)
  field_simp [hden]
  have hA : ((2 * n - 2 : ℕ) : ℚ) = (2 : ℚ) * ((n - 1 : ℕ) : ℚ) := by
    have h : 2 * n - 2 = 2 * (n - 1) := by omega
    rw [h]
    norm_num
  have hC : ((2 * n : ℕ) : ℚ) = (2 : ℚ) * ((n - 1 : ℕ) : ℚ) + 2 := by
    have h : 2 * n = 2 * (n - 1) + 2 := by omega
    rw [h]
    norm_num
  have hn' : (n : ℚ) = ((n - 1 : ℕ) : ℚ) + 1 := by
    have hsub : n = (n - 1) + 1 := (Nat.sub_add_cancel (by omega : 1 ≤ n)).symm
    rw [hsub]
    norm_num
  rw [hA, hC, hn']
  ring

lemma B_prod (n : ℕ) (hn : 2 ≤ n) :
    C (B n) = C (q n) * C ((2 * n - 2 : ℕ) : ℚ) * C ((2 * n - 3 : ℕ) : ℚ) := by
  rw [← Polynomial.C_mul, ← Polynomial.C_mul]
  congr 1
  unfold B
  exact (B_coeff n hn).symm

lemma B'_prod (n : ℕ) (hn : 2 ≤ n) :
    C (B' n) = C (q n) * C ((2 * n - 2 : ℕ) : ℚ) * C ((2 * n - 1 : ℕ) : ℚ) := by
  rw [← Polynomial.C_mul, ← Polynomial.C_mul]
  congr 1
  unfold B'
  exact (B'_coeff n hn).symm

lemma Kc_pEven (c : ℚ) {n : ℕ} (hn : 2 ≤ n) :
    Kc c (pEven n) =
      C c * X ^ (2 * n) - C (A c n) * X ^ (2 * n - 2) + C (B n) * X ^ (2 * n - 4) := by
  unfold pEven
  rw [Kc_sub, Kc_X_pow, Kc_monomial]
  rw [show (2 * n - 2 - 1 : ℕ) = 2 * n - 3 by omega]
  rw [show (2 * n - 2 - 2 : ℕ) = 2 * n - 4 by omega]
  rw [A_prod c n, B_prod n hn]
  ring

lemma Kc_pOdd (c : ℚ) {n : ℕ} (hn : 2 ≤ n) :
    Kc c (pOdd n) =
      C c * X ^ (2 * n + 1) - C (A' c n) * X ^ (2 * n - 1) + C (B' n) * X ^ (2 * n - 3) := by
  unfold pOdd
  rw [Kc_sub, Kc_X_pow, Kc_monomial]
  rw [show (2 * n + 1 - 1 : ℕ) = 2 * n by omega]
  rw [show (2 * n + 1 - 2 : ℕ) = 2 * n - 1 by omega]
  rw [show (2 * n - 1 - 1 : ℕ) = 2 * n - 2 by omega]
  rw [show (2 * n - 1 - 2 : ℕ) = 2 * n - 3 by omega]
  rw [A'_prod c n, B'_prod n hn]
  ring

lemma A_sub_B (c : ℚ) {n : ℕ} (hn : 2 ≤ n) : A c n - B n = 4 * (n : ℚ) + c * q n := by
  unfold A B q
  have h1 : ((2 * n - 1 : ℕ) : ℚ) = ((2 * n - 3 : ℕ) : ℚ) + 2 := by
    have h : 2 * n - 1 = (2 * n - 3) + 2 := by omega
    rw [h]
    norm_num
  have h2 : ((2 * n : ℕ) : ℚ) = 2 * (n : ℚ) := by
    rw [Nat.cast_mul]
    ring
  rw [h1, h2]
  ring

lemma A'_sub_B' (c : ℚ) {n : ℕ} (hn : 2 ≤ n) : A' c n - B' n = 4 * (n : ℚ) + c * q n := by
  unfold A' B' q
  have h1 : ((2 * n + 1 : ℕ) : ℚ) = ((2 * n - 1 : ℕ) : ℚ) + 2 := by
    have h : 2 * n + 1 = (2 * n - 1) + 2 := by omega
    rw [h]
    norm_num
  have h2 : ((2 * n : ℕ) : ℚ) = 2 * (n : ℚ) := by
    rw [Nat.cast_mul]
    ring
  rw [h1, h2]
  ring

end KcPolynomial

end SL
