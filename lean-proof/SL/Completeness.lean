import Mathlib
import SL.StabilityGrowth
import SL.MomentBound

/-!
# H^2 completeness: moment annihilation and the L2 conclusion

Formalization of the final steps of the completeness proof for the sparse
polynomial family {p_n} in the second left-definite space H^2[-1,1]
(`docs/SL_h2_completeness_proof.tex`, Section 3.3 "矩为零"):

1. The L2 moments mu_k = integral_{-1}^1 g(x) x^k dx of a function
   orthogonal to {K_c p_n} satisfy the jump recurrences (over Real),
2. the monotonicity of the fundamental solution (StabilityGrowth) forces
   mu_2 = mu_3 = 0, hence all moments vanish,
3. the Weierstrass theorem (polynomials dense in C[-1,1]) then forces
   integral g^2 = 0, i.e. g = 0 a.e. on (-1,1).

The coefficient identities over Real mirror `SL/KcPolynomial.lean` (which
is stated over Q); the moment machinery is the Real instantiation of the
abstract linear-functional results in `SL/MomentRecurrence.lean`.
-/

namespace SL

namespace Completeness

open Polynomial
open scoped Real Interval
open MeasureTheory Filter

section Coefficients

/-- q_n = n/(n-1) (Real version of `KcPolynomial.q`). -/
noncomputable def qR (n : ℕ) : ℝ := (n : ℝ) / ((n - 1 : ℕ) : ℝ)

/-- The even basis polynomial p_{2n}(x) = x^{2n} - q_n x^{2n-2}. -/
noncomputable def pEvenR (n : ℕ) : Polynomial ℝ :=
  X ^ (2 * n) - C (qR n) * X ^ (2 * n - 2)

/-- The odd basis polynomial p_{2n+1}(x) = x^{2n+1} - q_n x^{2n-1}. -/
noncomputable def pOddR (n : ℕ) : Polynomial ℝ :=
  X ^ (2 * n + 1) - C (qR n) * X ^ (2 * n - 1)

/-- A_n = 2n(2n-1) + c n/(n-1) (Real). -/
noncomputable def AR (c : ℝ) (n : ℕ) : ℝ :=
  ((2 * n : ℕ) : ℝ) * ((2 * n - 1 : ℕ) : ℝ) + c * qR n

/-- A'_n = 2n(2n+1) + c n/(n-1) (Real). -/
noncomputable def A'R (c : ℝ) (n : ℕ) : ℝ :=
  ((2 * n : ℕ) : ℝ) * ((2 * n + 1 : ℕ) : ℝ) + c * qR n

/-- B_n = 2n(2n-3) (Real). -/
noncomputable def BR (n : ℕ) : ℝ :=
  ((2 * n : ℕ) : ℝ) * ((2 * n - 3 : ℕ) : ℝ)

/-- B'_n = 2n(2n-1) (Real). -/
noncomputable def B'R (n : ℕ) : ℝ :=
  ((2 * n : ℕ) : ℝ) * ((2 * n - 1 : ℕ) : ℝ)

/-- The shifted Krein operator on polynomials: K_c p = -p'' + c p (Real). -/
noncomputable def KcR (c : ℝ) (p : Polynomial ℝ) : Polynomial ℝ :=
  -(derivative (derivative p)) + C c * p

lemma qR_nonneg {n : ℕ} (hn : 2 ≤ n) : 0 ≤ qR n := by
  unfold qR
  exact div_nonneg (Nat.cast_nonneg n) (le_of_lt (by
    have : 1 ≤ n - 1 := by omega
    exact_mod_cast this))

lemma qR_ge_one {n : ℕ} (hn : 2 ≤ n) : 1 ≤ qR n := by
  unfold qR
  have hpos : 0 < ((n - 1 : ℕ) : ℝ) := by
    have : 1 ≤ n - 1 := by omega
    exact_mod_cast this
  have hle : ((n - 1 : ℕ) : ℝ) ≤ (n : ℝ) := by
    have : n - 1 ≤ n := by omega
    exact_mod_cast this
  exact (le_div_iff₀ hpos).2 (by simp)

lemma BR_nonneg {n : ℕ} (hn : 2 ≤ n) : 0 ≤ BR n := by
  unfold BR
  exact mul_nonneg (by positivity) (by
    have : 0 ≤ 2 * n - 3 := by omega
    exact_mod_cast this)

lemma B'R_nonneg {n : ℕ} (hn : 2 ≤ n) : 0 ≤ B'R n := by
  unfold B'R
  exact mul_nonneg (by positivity) (by
    have : 0 ≤ 2 * n - 1 := by omega
    exact_mod_cast this)

lemma AR_sub_BR (c : ℝ) {n : ℕ} (hn : 2 ≤ n) : AR c n - BR n = 4 * (n : ℝ) + c * qR n := by
  unfold AR BR qR
  have h1 : ((2 * n - 1 : ℕ) : ℝ) = ((2 * n - 3 : ℕ) : ℝ) + 2 := by
    have h : 2 * n - 1 = (2 * n - 3) + 2 := by omega
    rw [h]
    norm_num
  have h2 : ((2 * n : ℕ) : ℝ) = 2 * (n : ℝ) := by
    rw [Nat.cast_mul]
    ring
  rw [h1, h2]
  ring

lemma A'R_sub_B'R (c : ℝ) {n : ℕ} (hn : 2 ≤ n) : A'R c n - B'R n = 4 * (n : ℝ) + c * qR n := by
  unfold A'R B'R qR
  have h1 : ((2 * n + 1 : ℕ) : ℝ) = ((2 * n - 1 : ℕ) : ℝ) + 2 := by
    have h : 2 * n + 1 = (2 * n - 1) + 2 := by omega
    rw [h]
    norm_num
  have h2 : ((2 * n : ℕ) : ℝ) = 2 * (n : ℝ) := by
    rw [Nat.cast_mul]
    ring
  rw [h1, h2]
  ring

lemma AR_sub_BR_ge_c (c : ℝ) (hc : 0 ≤ c) {n : ℕ} (hn : 2 ≤ n) : c ≤ AR c n - BR n := by
  rw [AR_sub_BR c hn]
  have hcq : c ≤ c * qR n := by
    simpa using (mul_le_mul_of_nonneg_left (qR_ge_one hn) hc)
  exact le_trans hcq (le_add_of_nonneg_left (by positivity : 0 ≤ 4 * (n : ℝ)))

lemma A'R_sub_B'R_ge_c (c : ℝ) (hc : 0 ≤ c) {n : ℕ} (hn : 2 ≤ n) : c ≤ A'R c n - B'R n := by
  rw [A'R_sub_B'R c hn]
  have hcq : c ≤ c * qR n := by
    simpa using (mul_le_mul_of_nonneg_left (qR_ge_one hn) hc)
  exact le_trans hcq (le_add_of_nonneg_left (by positivity : 0 ≤ 4 * (n : ℝ)))

lemma KcR_sub (c : ℝ) (p q : Polynomial ℝ) : KcR c (p - q) = KcR c p - KcR c q := by
  unfold KcR
  rw [derivative_sub, derivative_sub]
  ring

lemma KcR_monomial (c : ℝ) (a : ℝ) (m : ℕ) :
    KcR c (C a * X ^ m) =
      C c * C a * X ^ m - C a * C (m : ℝ) * C ((m - 1 : ℕ) : ℝ) * X ^ (m - 2) := by
  unfold KcR
  rw [derivative_C_mul, derivative_X_pow, derivative_C_mul, derivative_C_mul, derivative_X_pow,
    Nat.sub_sub]
  ring

lemma KcR_X_pow (c : ℝ) (m : ℕ) :
    KcR c (X ^ m) = C c * X ^ m - C (m : ℝ) * C ((m - 1 : ℕ) : ℝ) * X ^ (m - 2) := by
  simpa using KcR_monomial c 1 m

lemma AR_prod (c : ℝ) (n : ℕ) :
    C (AR c n) = C ((2 * n : ℕ) : ℝ) * C ((2 * n - 1 : ℕ) : ℝ) + C c * C (qR n) := by
  rw [← Polynomial.C_mul, ← Polynomial.C_mul, ← Polynomial.C_add]
  rfl

lemma A'R_prod (c : ℝ) (n : ℕ) :
    C (A'R c n) = C ((2 * n : ℕ) : ℝ) * C ((2 * n + 1 : ℕ) : ℝ) + C c * C (qR n) := by
  rw [← Polynomial.C_mul, ← Polynomial.C_mul, ← Polynomial.C_add]
  rfl

lemma BR_coeff (n : ℕ) (hn : 2 ≤ n) :
    qR n * ((2 * n - 2 : ℕ) : ℝ) * ((2 * n - 3 : ℕ) : ℝ) =
      ((2 * n : ℕ) : ℝ) * ((2 * n - 3 : ℕ) : ℝ) := by
  unfold qR
  have hden : ((n - 1 : ℕ) : ℝ) ≠ 0 := by
    have : 1 ≤ n - 1 := by omega
    exact_mod_cast (ne_of_gt this)
  field_simp [hden]
  have hA : ((2 * n - 2 : ℕ) : ℝ) = (2 : ℝ) * ((n - 1 : ℕ) : ℝ) := by
    have h : 2 * n - 2 = 2 * (n - 1) := by omega
    rw [h]
    norm_num
  have hB : ((2 * n - 3 : ℕ) : ℝ) = (2 : ℝ) * ((n - 1 : ℕ) : ℝ) - 1 := by
    have h : 2 * n - 3 = 2 * (n - 1) - 1 := by omega
    rw [h]
    rw [Nat.cast_sub (by omega : 1 ≤ 2 * (n - 1))]
    norm_num
  have hC : ((2 * n : ℕ) : ℝ) = (2 : ℝ) * ((n - 1 : ℕ) : ℝ) + 2 := by
    have h : 2 * n = 2 * (n - 1) + 2 := by omega
    rw [h]
    norm_num
  have hn' : (n : ℝ) = ((n - 1 : ℕ) : ℝ) + 1 := by
    have hsub : n = (n - 1) + 1 := (Nat.sub_add_cancel (by omega : 1 ≤ n)).symm
    rw [hsub]
    norm_num
  rw [hA, hB, hC, hn']
  ring

lemma B'R_coeff (n : ℕ) (hn : 2 ≤ n) :
    qR n * ((2 * n - 2 : ℕ) : ℝ) * ((2 * n - 1 : ℕ) : ℝ) =
      ((2 * n : ℕ) : ℝ) * ((2 * n - 1 : ℕ) : ℝ) := by
  unfold qR
  have hden : ((n - 1 : ℕ) : ℝ) ≠ 0 := by
    have : 1 ≤ n - 1 := by omega
    exact_mod_cast (ne_of_gt this)
  field_simp [hden]
  have hA : ((2 * n - 2 : ℕ) : ℝ) = (2 : ℝ) * ((n - 1 : ℕ) : ℝ) := by
    have h : 2 * n - 2 = 2 * (n - 1) := by omega
    rw [h]
    norm_num
  have hC : ((2 * n : ℕ) : ℝ) = (2 : ℝ) * ((n - 1 : ℕ) : ℝ) + 2 := by
    have h : 2 * n = 2 * (n - 1) + 2 := by omega
    rw [h]
    norm_num
  have hn' : (n : ℝ) = ((n - 1 : ℕ) : ℝ) + 1 := by
    have hsub : n = (n - 1) + 1 := (Nat.sub_add_cancel (by omega : 1 ≤ n)).symm
    rw [hsub]
    norm_num
  rw [hA, hC, hn']
  ring

lemma BR_prod (n : ℕ) (hn : 2 ≤ n) :
    C (BR n) = C (qR n) * C ((2 * n - 2 : ℕ) : ℝ) * C ((2 * n - 3 : ℕ) : ℝ) := by
  rw [← Polynomial.C_mul, ← Polynomial.C_mul]
  congr 1
  unfold BR
  exact (BR_coeff n hn).symm

lemma B'R_prod (n : ℕ) (hn : 2 ≤ n) :
    C (B'R n) = C (qR n) * C ((2 * n - 2 : ℕ) : ℝ) * C ((2 * n - 1 : ℕ) : ℝ) := by
  rw [← Polynomial.C_mul, ← Polynomial.C_mul]
  congr 1
  unfold B'R
  exact (B'R_coeff n hn).symm

/-- K_c p_{2n} = c x^{2n} - A_n x^{2n-2} + B_n x^{2n-4} (Real version of
`KcPolynomial.Kc_pEven`). -/
lemma KcR_pEven (c : ℝ) {n : ℕ} (hn : 2 ≤ n) :
    KcR c (pEvenR n) =
      C c * X ^ (2 * n) - C (AR c n) * X ^ (2 * n - 2) + C (BR n) * X ^ (2 * n - 4) := by
  unfold pEvenR
  rw [KcR_sub, KcR_X_pow, KcR_monomial]
  rw [show (2 * n - 2 - 1 : ℕ) = 2 * n - 3 by omega]
  rw [show (2 * n - 2 - 2 : ℕ) = 2 * n - 4 by omega]
  rw [AR_prod c n, BR_prod n hn]
  ring

/-- K_c p_{2n+1} = c x^{2n+1} - A'_n x^{2n-1} + B'_n x^{2n-3} (Real version of
`KcPolynomial.Kc_pOdd`). -/
lemma KcR_pOdd (c : ℝ) {n : ℕ} (hn : 2 ≤ n) :
    KcR c (pOddR n) =
      C c * X ^ (2 * n + 1) - C (A'R c n) * X ^ (2 * n - 1) + C (B'R n) * X ^ (2 * n - 3) := by
  unfold pOddR
  rw [KcR_sub, KcR_X_pow, KcR_monomial]
  rw [show (2 * n + 1 - 1 : ℕ) = 2 * n by omega]
  rw [show (2 * n + 1 - 2 : ℕ) = 2 * n - 1 by omega]
  rw [show (2 * n - 1 - 1 : ℕ) = 2 * n - 2 by omega]
  rw [show (2 * n - 1 - 2 : ℕ) = 2 * n - 3 by omega]
  rw [A'R_prod c n, B'R_prod n hn]
  ring

end Coefficients

section MomentFunctional

/-- The L2 moment functional M(p) = integral_{-1}^1 g(x) p(x) dx for a
continuous g: a Real-linear map on polynomials. -/
noncomputable def momentFunctional (g : ℝ → ℝ) (hg : ContinuousOn g (Set.Icc (-1) 1)) :
    (Polynomial ℝ) →ₗ[ℝ] ℝ where
  toFun p := ∫ x in (-1 : ℝ)..1, g x * p.eval x
  map_add' := by
    intro p q
    change (∫ x in (-1 : ℝ)..1, g x * (p + q).eval x) =
      (∫ x in (-1 : ℝ)..1, g x * p.eval x) + (∫ x in (-1 : ℝ)..1, g x * q.eval x)
    have hIp : IntervalIntegrable (fun x : ℝ => g x * p.eval x) volume (-1) 1 := by
      exact (hg.mul (Polynomial.continuousOn p)).intervalIntegrable_of_Icc (by norm_num : (-1 : ℝ) ≤ 1)
    have hIq : IntervalIntegrable (fun x : ℝ => g x * q.eval x) volume (-1) 1 := by
      exact (hg.mul (Polynomial.continuousOn q)).intervalIntegrable_of_Icc (by norm_num : (-1 : ℝ) ≤ 1)
    have h1 : (∫ x in (-1 : ℝ)..1, g x * (p + q).eval x) =
        (∫ x in (-1 : ℝ)..1, g x * p.eval x + g x * q.eval x) := by
      apply intervalIntegral.integral_congr
      intro x hx
      simp [Polynomial.eval_add, mul_add]
    rw [h1]
    exact intervalIntegral.integral_add hIp hIq
  map_smul' := by
    intro a p
    change (∫ x in (-1 : ℝ)..1, g x * (a • p).eval x) =
      a • (∫ x in (-1 : ℝ)..1, g x * p.eval x)
    have hIp : IntervalIntegrable (fun x : ℝ => g x * p.eval x) volume (-1) 1 := by
      exact (hg.mul (Polynomial.continuousOn p)).intervalIntegrable_of_Icc (by norm_num : (-1 : ℝ) ≤ 1)
    have h1 : (∫ x in (-1 : ℝ)..1, g x * (a • p).eval x) =
        (∫ x in (-1 : ℝ)..1, a * (g x * p.eval x)) := by
      apply intervalIntegral.integral_congr
      intro x hx
      rw [Polynomial.smul_eq_C_mul]
      simp
      ring
    rw [h1]
    rw [intervalIntegral.integral_const_mul]
    simp

/-- M(C a * X^m) = a * mu_m for the monomials. -/
lemma apply_C_mul_X_pow (g : ℝ → ℝ) (hg : ContinuousOn g (Set.Icc (-1) 1)) (a : ℝ) (m : ℕ) :
    momentFunctional g hg (C a * X ^ m) = a * MomentBound.moments g m := by
  rw [← Polynomial.smul_eq_C_mul]
  have hX : momentFunctional g hg (X ^ m) = MomentBound.moments g m := by
    change (∫ x in (-1 : ℝ)..1, g x * (X ^ m).eval x) = (∫ x in (-1 : ℝ)..1, g x * x ^ m)
    apply intervalIntegral.integral_congr
    intro x hx
    simp [Polynomial.eval_pow, Polynomial.eval_X]
  rw [map_smul, hX]
  simp

/-- The jump recurrence for the even moments (Real):
    c mu_{2n} = A_n mu_{2n-2} - B_n mu_{2n-4}. -/
lemma even_recurrence (g : ℝ → ℝ) (hg : ContinuousOn g (Set.Icc (-1) 1)) {c : ℝ} (_hc : c ≠ 0)
    {n : ℕ} (hn : 2 ≤ n) (horth : momentFunctional g hg (KcR c (pEvenR n)) = 0) :
    c * MomentBound.moments g (2 * n) =
      AR c n * MomentBound.moments g (2 * n - 2) - BR n * MomentBound.moments g (2 * n - 4) := by
  have hK := KcR_pEven c hn
  have hM : momentFunctional g hg (KcR c (pEvenR n)) =
      c * MomentBound.moments g (2 * n) - AR c n * MomentBound.moments g (2 * n - 2) +
        BR n * MomentBound.moments g (2 * n - 4) := by
    rw [hK]
    rw [map_add, map_sub]
    rw [apply_C_mul_X_pow g hg c (2 * n), apply_C_mul_X_pow g hg (AR c n) (2 * n - 2),
      apply_C_mul_X_pow g hg (BR n) (2 * n - 4)]
  rw [horth] at hM
  linarith

/-- The jump recurrence for the odd moments (Real):
    c mu_{2n+1} = A'_n mu_{2n-1} - B'_n mu_{2n-3}. -/
lemma odd_recurrence (g : ℝ → ℝ) (hg : ContinuousOn g (Set.Icc (-1) 1)) {c : ℝ} (_hc : c ≠ 0)
    {n : ℕ} (hn : 2 ≤ n) (horth : momentFunctional g hg (KcR c (pOddR n)) = 0) :
    c * MomentBound.moments g (2 * n + 1) =
      A'R c n * MomentBound.moments g (2 * n - 1) - B'R n * MomentBound.moments g (2 * n - 3) := by
  have hK := KcR_pOdd c hn
  have hM : momentFunctional g hg (KcR c (pOddR n)) =
      c * MomentBound.moments g (2 * n + 1) - A'R c n * MomentBound.moments g (2 * n - 1) +
        B'R n * MomentBound.moments g (2 * n - 3) := by
    rw [hK]
    rw [map_add, map_sub]
    rw [apply_C_mul_X_pow g hg c (2 * n + 1), apply_C_mul_X_pow g hg (A'R c n) (2 * n - 1),
      apply_C_mul_X_pow g hg (B'R n) (2 * n - 3)]
  rw [horth] at hM
  linarith

/-- K_c p_0 = c forces mu_0 = 0 when c != 0. -/
lemma constant_orth_moment_zero (g : ℝ → ℝ) (hg : ContinuousOn g (Set.Icc (-1) 1)) {c : ℝ}
    (hc : c ≠ 0) (horth : momentFunctional g hg (KcR c 1) = 0) :
    MomentBound.moments g 0 = 0 := by
  have hK : KcR c 1 = C c := by simp [KcR]
  have hM : momentFunctional g hg (KcR c 1) = c * MomentBound.moments g 0 := by
    rw [hK]
    simpa using apply_C_mul_X_pow g hg c 0
  rw [horth] at hM
  have hmul : c * MomentBound.moments g 0 = 0 := by linarith
  exact (mul_eq_zero.mp hmul).resolve_left hc

/-- K_c p_1 = c x forces mu_1 = 0 when c != 0. -/
lemma linear_orth_moment_zero (g : ℝ → ℝ) (hg : ContinuousOn g (Set.Icc (-1) 1)) {c : ℝ}
    (hc : c ≠ 0) (horth : momentFunctional g hg (KcR c X) = 0) :
    MomentBound.moments g 1 = 0 := by
  have hK : KcR c X = C c * X := by simp [KcR]
  have hM : momentFunctional g hg (KcR c X) = c * MomentBound.moments g 1 := by
    rw [hK]
    simpa using apply_C_mul_X_pow g hg c 1
  rw [horth] at hM
  have hmul : c * MomentBound.moments g 1 = 0 := by linarith
  exact (mul_eq_zero.mp hmul).resolve_left hc

end MomentFunctional

section Scaling

/-- Real version of `MomentRecurrence.scaling`: any solution of the jump
recurrence with v_0 = 0 is v_m = v_1 u_m. -/
theorem scaling (c0 : ℝ) (A B : ℕ → ℝ) (hc0 : c0 ≠ 0) (v : ℕ → ℝ) (h0 : v 0 = 0)
    (hrec : ∀ n : ℕ, 2 ≤ n → c0 * v n = A n * v (n - 1) - B n * v (n - 2)) :
    ∀ m : ℕ, v m = v 1 * StabilityGrowth.u (K := ℝ) c0 A B m := by
  intro m
  refine Nat.strong_induction_on m ?_
  intro m ih
  by_cases hm0 : m = 0
  · subst m
    simp [StabilityGrowth.u, h0]
  by_cases hm1 : m = 1
  · subst m
    simp [StabilityGrowth.u]
  · have hm2 : 2 ≤ m := by omega
    have hrec_m : c0 * v m = A m * v (m - 1) - B m * v (m - 2) := hrec m hm2
    have hprev1 : v (m - 1) = v 1 * StabilityGrowth.u (K := ℝ) c0 A B (m - 1) := ih (m - 1) (by omega)
    have hprev2 : v (m - 2) = v 1 * StabilityGrowth.u (K := ℝ) c0 A B (m - 2) := ih (m - 2) (by omega)
    have hu : c0 * StabilityGrowth.u (K := ℝ) c0 A B m =
        A m * StabilityGrowth.u (K := ℝ) c0 A B (m - 1) - B m * StabilityGrowth.u (K := ℝ) c0 A B (m - 2) := by
      exact StabilityGrowth.u_recurrence' (K := ℝ) (c0 := c0) (A := A) (B := B) hc0 (j := m) hm2
    have hgoal : c0 * v m = c0 * (v 1 * StabilityGrowth.u (K := ℝ) c0 A B m) := by
      calc
        c0 * v m = A m * v (m - 1) - B m * v (m - 2) := hrec_m
        _ = A m * (v 1 * StabilityGrowth.u (K := ℝ) c0 A B (m - 1)) -
            B m * (v 1 * StabilityGrowth.u (K := ℝ) c0 A B (m - 2)) := by rw [hprev1, hprev2]
        _ = v 1 * (A m * StabilityGrowth.u (K := ℝ) c0 A B (m - 1) -
            B m * StabilityGrowth.u (K := ℝ) c0 A B (m - 2)) := by ring
        _ = v 1 * (c0 * StabilityGrowth.u (K := ℝ) c0 A B m) := by rw [hu]
        _ = c0 * (v 1 * StabilityGrowth.u (K := ℝ) c0 A B m) := by ring
    exact mul_left_cancel₀ hc0 hgoal

theorem even_scaling (c0 : ℝ) (A B : ℕ → ℝ) (hc0 : c0 ≠ 0) (mu : ℕ → ℝ) (h0 : mu 0 = 0)
    (hrec : ∀ n : ℕ, 2 ≤ n → c0 * mu (2 * n) = A n * mu (2 * n - 2) - B n * mu (2 * n - 4)) :
    ∀ m : ℕ, mu (2 * m) = mu 2 * StabilityGrowth.u (K := ℝ) c0 A B m := by
  let v : ℕ → ℝ := fun n => mu (2 * n)
  have hv0 : v 0 = 0 := by simp [v, h0]
  have hv_rec : ∀ n : ℕ, 2 ≤ n → c0 * v n = A n * v (n - 1) - B n * v (n - 2) := by
    intro n hn
    have h := hrec n hn
    have h1 : 2 * n - 2 = 2 * (n - 1) := by omega
    have h2 : 2 * n - 4 = 2 * (n - 2) := by omega
    simpa [v, h1, h2] using h
  have hsc := scaling c0 A B hc0 v hv0 hv_rec
  intro m
  have h := hsc m
  simpa [v] using h

theorem odd_scaling (c0 : ℝ) (A' B' : ℕ → ℝ) (hc0 : c0 ≠ 0) (mu : ℕ → ℝ) (h1 : mu 1 = 0)
    (hrec : ∀ n : ℕ, 2 ≤ n → c0 * mu (2 * n + 1) = A' n * mu (2 * n - 1) - B' n * mu (2 * n - 3)) :
    ∀ m : ℕ, mu (2 * m + 1) = mu 3 * StabilityGrowth.u (K := ℝ) c0 A' B' m := by
  let v : ℕ → ℝ := fun n => mu (2 * n + 1)
  have hv0 : v 0 = 0 := by simp [v, h1]
  have hv_rec : ∀ n : ℕ, 2 ≤ n → c0 * v n = A' n * v (n - 1) - B' n * v (n - 2) := by
    intro n hn
    have h := hrec n hn
    have h1' : 2 * n - 1 = 2 * (n - 1) + 1 := by omega
    have h2' : 2 * n - 3 = 2 * (n - 2) + 1 := by omega
    simpa [v, h1', h2'] using h
  have hsc := scaling c0 A' B' hc0 v hv0 hv_rec
  intro m
  have h := hsc m
  simpa [v] using h

/-- Orthogonality + mu_0 = 0 imply the even scaling mu_{2m} = mu_2 u_m. -/
theorem even_moment_scaling (g : ℝ → ℝ) (hg : ContinuousOn g (Set.Icc (-1) 1)) {c : ℝ}
    (hc : c ≠ 0) (h0 : MomentBound.moments g 0 = 0)
    (horth : ∀ n : ℕ, 2 ≤ n → momentFunctional g hg (KcR c (pEvenR n)) = 0) :
    ∀ m : ℕ, MomentBound.moments g (2 * m) =
      MomentBound.moments g 2 * StabilityGrowth.u (K := ℝ) c (AR c) BR m := by
  apply even_scaling c (AR c) BR hc (MomentBound.moments g) h0
  intro n hn
  exact even_recurrence g hg hc hn (horth n hn)

/-- Orthogonality + mu_1 = 0 imply the odd scaling mu_{2m+1} = mu_3 u'_m. -/
theorem odd_moment_scaling (g : ℝ → ℝ) (hg : ContinuousOn g (Set.Icc (-1) 1)) {c : ℝ}
    (hc : c ≠ 0) (h1 : MomentBound.moments g 1 = 0)
    (horth : ∀ n : ℕ, 2 ≤ n → momentFunctional g hg (KcR c (pOddR n)) = 0) :
    ∀ m : ℕ, MomentBound.moments g (2 * m + 1) =
      MomentBound.moments g 3 * StabilityGrowth.u (K := ℝ) c (A'R c) B'R m := by
  apply odd_scaling c (A'R c) B'R hc (MomentBound.moments g) h1
  intro n hn
  exact odd_recurrence g hg hc hn (horth n hn)

/-- The fundamental solution is >= 1 for the even Krein coefficients. -/
lemma u_ge_one_even (c : ℝ) (hc : 0 < c) :
    ∀ m : ℕ, 1 ≤ m → 1 ≤ StabilityGrowth.u (K := ℝ) c (AR c) BR m := by
  intro m hm
  have hB : ∀ m : ℕ, 2 ≤ m → 0 ≤ BR m := fun m hm' => BR_nonneg hm'
  have hAB : ∀ m : ℕ, 2 ≤ m → c ≤ AR c m - BR m := fun m hm' => AR_sub_BR_ge_c c (le_of_lt hc) hm'
  have hmono := StabilityGrowth.monotone_pos (K := ℝ) (c0 := c) (A := AR c) (B := BR) hc hB hAB
  refine Nat.le_induction (m := 1) ?base ?step m hm
  · simp [StabilityGrowth.u]
  · intro n hn ih
    exact le_trans ih (hmono n (by omega)).2

/-- The fundamental solution is >= 1 for the odd Krein coefficients. -/
lemma u_ge_one_odd (c : ℝ) (hc : 0 < c) :
    ∀ m : ℕ, 1 ≤ m → 1 ≤ StabilityGrowth.u (K := ℝ) c (A'R c) B'R m := by
  intro m hm
  have hB : ∀ m : ℕ, 2 ≤ m → 0 ≤ B'R m := fun m hm' => B'R_nonneg hm'
  have hAB : ∀ m : ℕ, 2 ≤ m → c ≤ A'R c m - B'R m := fun m hm' => A'R_sub_B'R_ge_c c (le_of_lt hc) hm'
  have hmono := StabilityGrowth.monotone_pos (K := ℝ) (c0 := c) (A := A'R c) (B := B'R) hc hB hAB
  refine Nat.le_induction (m := 1) ?base ?step m hm
  · simp [StabilityGrowth.u]
  · intro n hn ih
    exact le_trans ih (hmono n (by omega)).2

/-- If |a| is bounded by B * t m for all m >= 1 with t m -> 0 (in the eps
sense), then a = 0. -/
lemma bound_tendsto_annihilate {a B : ℝ} (hB : 0 ≤ B) {t : ℕ → ℝ}
    (hsmall : ∀ ε : ℝ, 0 < ε → ∃ m : ℕ, 1 ≤ m ∧ t m < ε)
    (hbd : ∀ m : ℕ, 1 ≤ m → |a| ≤ B * t m) : a = 0 := by
  by_contra ha
  have hδ : 0 < |a| := abs_pos.mpr ha
  by_cases hB0 : B = 0
  · have : |a| ≤ 0 := by
      have h := hbd 1 (by norm_num)
      simpa [hB0] using h
    nlinarith
  · have hBpos : 0 < B := lt_of_le_of_ne' hB hB0
    let D : ℝ := B + 1
    have hD : 0 < D := by dsimp [D]; positivity
    rcases hsmall (|a| / (2 * D)) (by positivity) with ⟨m, hm1, hm⟩
    have h1 : |a| < B * (|a| / (2 * D)) :=
      lt_of_le_of_lt (hbd m hm1) (mul_lt_mul_of_pos_left hm hBpos)
    have h2 : B * (|a| / (2 * D)) ≤ |a| / 2 := by
      have hBD : B ≤ D := by dsimp [D]; linarith
      have h2D : 2 * D ≠ 0 := by positivity
      have hDne : D ≠ 0 := by positivity
      have heq : B * (|a| / (2 * D)) = (B / D) * (|a| / 2) := by
        field_simp [hDne, h2D]
      rw [heq]
      simpa using mul_le_mul_of_nonneg_right ((div_le_one hD).2 hBD) (by positivity : 0 ≤ |a| / 2)
    nlinarith [h1, h2, hδ]

/-- sqrt (2/(4m+1)) -> 0. -/
lemma sqrt_bound_small (ε : ℝ) (hε : 0 < ε) :
    ∃ m : ℕ, 1 ≤ m ∧ Real.sqrt (2 / ((4 * m + 1 : ℕ) : ℝ)) < ε := by
  rcases exists_nat_gt (max 1 (2 / ε ^ 2)) with ⟨m, hm⟩
  have hm1 : 1 ≤ m := by
    have hlt : (1 : ℝ) < (m : ℝ) := lt_of_le_of_lt (le_max_left 1 (2 / ε ^ 2)) hm
    have : 1 < m := by exact_mod_cast hlt
    omega
  have hmε : (2 / ε ^ 2) < (m : ℝ) := lt_of_le_of_lt (le_max_right 1 (2 / ε ^ 2)) hm
  have hε2 : 0 < ε ^ 2 := sq_pos_of_pos hε
  have h2 : 2 < (m : ℝ) * ε ^ 2 := by
    have h1 : (2 / ε ^ 2) * ε ^ 2 < (m : ℝ) * ε ^ 2 :=
      mul_lt_mul_of_pos_right hmε hε2
    have hc : (2 / ε ^ 2) * ε ^ 2 = 2 := by
      field_simp [ne_of_gt hε2]
    simpa [hc] using h1
  have hpos : 0 < 4 * (m : ℝ) + 1 := by positivity
  have hgoal : 2 / (4 * (m : ℝ) + 1) < ε ^ 2 := by
    have hmain : 2 < (4 * (m : ℝ) + 1) * ε ^ 2 := by
      nlinarith [h2, sq_nonneg ε]
    have hc : (2 / (4 * (m : ℝ) + 1)) * (4 * (m : ℝ) + 1) = 2 := by
      field_simp [ne_of_gt hpos]
    have h1 : (2 / (4 * (m : ℝ) + 1)) * (4 * (m : ℝ) + 1) < ε ^ 2 * (4 * (m : ℝ) + 1) := by
      rw [hc]
      simpa [mul_comm] using hmain
    exact lt_of_mul_lt_mul_right h1 (le_of_lt hpos)
  have hden : ((4 * m + 1 : ℕ) : ℝ) = 4 * (m : ℝ) + 1 := by simp
  have hgoalC : 2 / ((4 * m + 1 : ℕ) : ℝ) < ε ^ 2 := by
    rw [hden]
    exact hgoal
  refine ⟨m, hm1, ?_⟩
  exact (Real.sqrt_lt (by rw [hden]; positivity : 0 ≤ 2 / ((4 * m + 1 : ℕ) : ℝ)) (le_of_lt hε)).2 hgoalC

/-- sqrt (2/(4m+3)) -> 0. -/
lemma sqrt_bound_small' (ε : ℝ) (hε : 0 < ε) :
    ∃ m : ℕ, 1 ≤ m ∧ Real.sqrt (2 / ((4 * m + 3 : ℕ) : ℝ)) < ε := by
  rcases exists_nat_gt (max 1 (2 / ε ^ 2)) with ⟨m, hm⟩
  have hm1 : 1 ≤ m := by
    have hlt : (1 : ℝ) < (m : ℝ) := lt_of_le_of_lt (le_max_left 1 (2 / ε ^ 2)) hm
    have : 1 < m := by exact_mod_cast hlt
    omega
  have hmε : (2 / ε ^ 2) < (m : ℝ) := lt_of_le_of_lt (le_max_right 1 (2 / ε ^ 2)) hm
  have hε2 : 0 < ε ^ 2 := sq_pos_of_pos hε
  have h2 : 2 < (m : ℝ) * ε ^ 2 := by
    have h1 : (2 / ε ^ 2) * ε ^ 2 < (m : ℝ) * ε ^ 2 :=
      mul_lt_mul_of_pos_right hmε hε2
    have hc : (2 / ε ^ 2) * ε ^ 2 = 2 := by
      field_simp [ne_of_gt hε2]
    simpa [hc] using h1
  have hpos : 0 < 4 * (m : ℝ) + 3 := by positivity
  have hgoal : 2 / (4 * (m : ℝ) + 3) < ε ^ 2 := by
    have hmain : 2 < (4 * (m : ℝ) + 3) * ε ^ 2 := by
      nlinarith [h2, sq_nonneg ε]
    have hc : (2 / (4 * (m : ℝ) + 3)) * (4 * (m : ℝ) + 3) = 2 := by
      field_simp [ne_of_gt hpos]
    have h1 : (2 / (4 * (m : ℝ) + 3)) * (4 * (m : ℝ) + 3) < ε ^ 2 * (4 * (m : ℝ) + 3) := by
      rw [hc]
      simpa [mul_comm] using hmain
    exact lt_of_mul_lt_mul_right h1 (le_of_lt hpos)
  have hden : ((4 * m + 3 : ℕ) : ℝ) = 4 * (m : ℝ) + 3 := by simp
  have hgoalC : 2 / ((4 * m + 3 : ℕ) : ℝ) < ε ^ 2 := by
    rw [hden]
    exact hgoal
  refine ⟨m, hm1, ?_⟩
  exact (Real.sqrt_lt (by rw [hden]; positivity : 0 ≤ 2 / ((4 * m + 3 : ℕ) : ℝ)) (le_of_lt hε)).2 hgoalC

/-- mu_2 = 0 from the scaling and the L2 moment bound (the bound
sqrt (2/(4m+1)) -> 0 beats the growth u_m >= 1). -/
theorem even_annihilation (g : ℝ → ℝ) (hg : ContinuousOn g (Set.Icc (-1) 1)) {c : ℝ} (hc : 0 < c)
    (hscal : ∀ m : ℕ, MomentBound.moments g (2 * m) =
      MomentBound.moments g 2 * StabilityGrowth.u (K := ℝ) c (AR c) BR m) :
    MomentBound.moments g 2 = 0 := by
  let B : ℝ := Real.sqrt (∫ x in (-1 : ℝ)..1, g x ^ 2)
  have hB0 : 0 ≤ B := by dsimp [B]; exact Real.sqrt_nonneg _
  have hbd : ∀ m : ℕ, 1 ≤ m → |MomentBound.moments g 2| ≤
      B * Real.sqrt (2 / ((4 * m + 1 : ℕ) : ℝ)) := by
    intro m hm
    have hmb := MomentBound.moment_bound hg (2 * m)
    have hmb' : |MomentBound.moments g (2 * m)| ≤
        B * Real.sqrt (2 / ((4 * m + 1 : ℕ) : ℝ)) := by
      dsimp [B]
      simpa [show 2 * (2 * m) + 1 = 4 * m + 1 by omega] using hmb
    have hge : |MomentBound.moments g 2| ≤ |MomentBound.moments g (2 * m)| := by
      rw [hscal m]
      have hu1 : 1 ≤ StabilityGrowth.u (K := ℝ) c (AR c) BR m := u_ge_one_even c hc m hm
      have hu0 : 0 ≤ StabilityGrowth.u (K := ℝ) c (AR c) BR m := le_trans zero_le_one hu1
      rw [abs_mul, abs_of_nonneg hu0]
      calc
        |MomentBound.moments g 2| = |MomentBound.moments g 2| * 1 := by rw [mul_one]
        _ ≤ |MomentBound.moments g 2| * StabilityGrowth.u (K := ℝ) c (AR c) BR m := by
              exact mul_le_mul_of_nonneg_left hu1 (abs_nonneg _)
    exact le_trans hge hmb'
  exact bound_tendsto_annihilate (t := fun m => Real.sqrt (2 / ((4 * m + 1 : ℕ) : ℝ)))
    hB0 sqrt_bound_small hbd

/-- mu_3 = 0 from the scaling and the L2 moment bound (odd analogue). -/
theorem odd_annihilation (g : ℝ → ℝ) (hg : ContinuousOn g (Set.Icc (-1) 1)) {c : ℝ} (hc : 0 < c)
    (hscal : ∀ m : ℕ, MomentBound.moments g (2 * m + 1) =
      MomentBound.moments g 3 * StabilityGrowth.u (K := ℝ) c (A'R c) B'R m) :
    MomentBound.moments g 3 = 0 := by
  let B : ℝ := Real.sqrt (∫ x in (-1 : ℝ)..1, g x ^ 2)
  have hB0 : 0 ≤ B := by dsimp [B]; exact Real.sqrt_nonneg _
  have hbd : ∀ m : ℕ, 1 ≤ m → |MomentBound.moments g 3| ≤
      B * Real.sqrt (2 / ((4 * m + 3 : ℕ) : ℝ)) := by
    intro m hm
    have hmb := MomentBound.moment_bound hg (2 * m + 1)
    have hmb' : |MomentBound.moments g (2 * m + 1)| ≤
        B * Real.sqrt (2 / ((4 * m + 3 : ℕ) : ℝ)) := by
      dsimp [B]
      simpa [show 2 * (2 * m + 1) + 1 = 4 * m + 3 by omega] using hmb
    have hge : |MomentBound.moments g 3| ≤ |MomentBound.moments g (2 * m + 1)| := by
      rw [hscal m]
      have hu1 : 1 ≤ StabilityGrowth.u (K := ℝ) c (A'R c) B'R m := u_ge_one_odd c hc m hm
      have hu0 : 0 ≤ StabilityGrowth.u (K := ℝ) c (A'R c) B'R m := le_trans zero_le_one hu1
      rw [abs_mul, abs_of_nonneg hu0]
      calc
        |MomentBound.moments g 3| = |MomentBound.moments g 3| * 1 := by rw [mul_one]
        _ ≤ |MomentBound.moments g 3| * StabilityGrowth.u (K := ℝ) c (A'R c) B'R m := by
              exact mul_le_mul_of_nonneg_left hu1 (abs_nonneg _)
    exact le_trans hge hmb'
  exact bound_tendsto_annihilate (t := fun m => Real.sqrt (2 / ((4 * m + 3 : ℕ) : ℝ)))
    hB0 sqrt_bound_small' hbd

/-- Orthogonality against {K_c p_n} forces all moments of g to vanish. -/
theorem all_moments_zero (g : ℝ → ℝ) (hg : ContinuousOn g (Set.Icc (-1) 1)) {c : ℝ} (hc : 0 < c)
    (h0 : MomentBound.moments g 0 = 0) (h1 : MomentBound.moments g 1 = 0)
    (horthE : ∀ n : ℕ, 2 ≤ n → momentFunctional g hg (KcR c (pEvenR n)) = 0)
    (horthO : ∀ n : ℕ, 2 ≤ n → momentFunctional g hg (KcR c (pOddR n)) = 0) :
    ∀ k : ℕ, MomentBound.moments g k = 0 := by
  have hcne : c ≠ 0 := ne_of_gt hc
  have hscalE := even_moment_scaling g hg hcne h0 horthE
  have hscalO := odd_moment_scaling g hg hcne h1 horthO
  have hμ2 : MomentBound.moments g 2 = 0 := even_annihilation g hg hc hscalE
  have hμ3 : MomentBound.moments g 3 = 0 := odd_annihilation g hg hc hscalO
  intro k
  rcases Nat.even_or_odd k with ⟨m, rfl⟩ | ⟨m, rfl⟩
  · simp [← two_mul, hscalE m, hμ2]
  · simp [hscalO m, hμ3]

end Scaling

section Weierstrass

/-- Polynomials approximate any continuous function on [-1,1] in the sup norm
(Weierstrass, via `polynomialFunctions.topologicalClosure`). -/
lemma exists_polynomial_sup_approx {ε : ℝ} (hε : 0 < ε) (f : C(Set.Icc (-1) 1, ℝ)) :
    ∃ p : ℝ[X], ‖f - Polynomial.toContinuousMapOn p (Set.Icc (-1) 1)‖ < ε := by
  have hcl : f ∈ (polynomialFunctions (Set.Icc (-1) 1)).topologicalClosure :=
    continuousMap_mem_polynomialFunctions_closure (-1) 1 f
  have hfreq : ∃ᶠ h : C(Set.Icc (-1) 1, ℝ) in nhds f,
      h ∈ polynomialFunctions (Set.Icc (-1) 1) := mem_closure_iff_frequently.mp hcl
  have hball : Metric.ball f ε ∈ nhds f := Metric.ball_mem_nhds f hε
  have hboth : ∃ᶠ h : C(Set.Icc (-1) 1, ℝ) in nhds f,
      h ∈ polynomialFunctions (Set.Icc (-1) 1) ∧ h ∈ Metric.ball f ε :=
    hfreq.and_eventually (Filter.eventually_of_mem hball (fun x hx => hx))
  rcases hboth.exists with ⟨h, hmem, hnear⟩
  have hmem' : h ∈ (⊤ : Subalgebra ℝ ℝ[X]).map
      (Polynomial.toContinuousMapOnAlgHom (Set.Icc (-1) 1)) := by
    simpa [polynomialFunctions] using hmem
  rcases (Subalgebra.mem_map.mp hmem') with ⟨p, hp_top, hp_eq⟩
  have hdist : dist h f < ε := Metric.mem_ball.mp hnear
  have hnorm : ‖h - f‖ < ε := by simpa [dist_eq_norm] using hdist
  have hnorm' : ‖f - h‖ < ε := by simpa [norm_sub_rev] using hnorm
  refine ⟨p, ?_⟩
  rw [← toContinuousMapOnAlgHom_apply]
  simpa [hp_eq] using hnorm'

/-- If all moments of a continuous g vanish then the functional vanishes on
every polynomial. -/
theorem momentFunctional_eq_zero_of_moments_zero (g : ℝ → ℝ)
    (hg : ContinuousOn g (Set.Icc (-1) 1))
    (hzero : ∀ k : ℕ, MomentBound.moments g k = 0) :
    ∀ p : ℝ[X], momentFunctional g hg p = 0 := by
  intro p
  refine Polynomial.induction_on' p ?_ ?_
  · intro p q hp hq
    rw [map_add, hp, hq, add_zero]
  · intro n a
    rw [← Polynomial.C_mul_X_pow_eq_monomial]
    rw [apply_C_mul_X_pow g hg a n, hzero n, mul_zero]

/-- A continuous g with all moments zero satisfies integral g^2 = 0
(the Weierstrass step: polynomials are dense in C[-1,1] and hence in L2). -/
theorem integral_sq_eq_zero_of_all_moments_zero (g : ℝ → ℝ)
    (hg : ContinuousOn g (Set.Icc (-1) 1))
    (hzero : ∀ k : ℕ, MomentBound.moments g k = 0) :
    (∫ x in (-1 : ℝ)..1, g x ^ 2) = 0 := by
  let gf : C(Set.Icc (-1 : ℝ) 1, ℝ) :=
    ⟨fun x : Set.Icc (-1 : ℝ) 1 => g x.1, by
      exact continuousOn_iff_continuous_restrict.mp hg⟩
  have hM0 : 0 ≤ ‖gf‖ := norm_nonneg _
  have hgb : ∀ x : ℝ, x ∈ Set.Icc (-1) 1 → |g x| ≤ ‖gf‖ := by
    intro x hx
    have h := ((ContinuousMap.norm_le gf hM0).mp le_rfl) ⟨x, hx⟩
    simpa [gf] using h
  have hzero_fun : ∀ p : ℝ[X], momentFunctional g hg p = 0 :=
    momentFunctional_eq_zero_of_moments_zero g hg hzero
  refine le_antisymm ?_ ?_
  · apply le_of_forall_pos_le_add
    intro ε hε
    let ε₁ : ℝ := ε / (2 * (‖gf‖ + 1))
    have hε₁ : 0 < ε₁ := by positivity
    rcases exists_polynomial_sup_approx hε₁ gf with ⟨p, hp⟩
    have hgp : (∫ x in (-1 : ℝ)..1, g x * p.eval x) = 0 := hzero_fun p
    have hsplit : (∫ x in (-1 : ℝ)..1, g x ^ 2) =
        (∫ x in (-1 : ℝ)..1, g x * (g x - p.eval x)) + (∫ x in (-1 : ℝ)..1, g x * p.eval x) := by
      have h1 : (fun x : ℝ => g x ^ 2) = fun x : ℝ => g x * (g x - p.eval x) + g x * p.eval x := by
        funext x
        ring
      rw [h1]
      have hI1 : IntervalIntegrable (fun x : ℝ => g x * (g x - p.eval x)) volume (-1) 1 := by
        exact (hg.mul (hg.sub (Polynomial.continuousOn p))).intervalIntegrable_of_Icc (by norm_num : (-1 : ℝ) ≤ 1)
      have hI2 : IntervalIntegrable (fun x : ℝ => g x * p.eval x) volume (-1) 1 := by
        exact (hg.mul (Polynomial.continuousOn p)).intervalIntegrable_of_Icc (by norm_num : (-1 : ℝ) ≤ 1)
      exact intervalIntegral.integral_add hI1 hI2
    have hb : |(∫ x in (-1 : ℝ)..1, g x * (g x - p.eval x))| ≤ ‖gf‖ * ε₁ * 2 := by
      have hnorm : ‖(∫ x in (-1 : ℝ)..1, g x * (g x - p.eval x))‖ ≤
          ‖gf‖ * ε₁ * |(1 : ℝ) - (-1)| := by
        refine intervalIntegral.norm_integral_le_of_norm_le_const ?_
        intro x hx
        have hxIcc : x ∈ Set.Icc (-1 : ℝ) 1 := by
          have hxU : x ∈ [[(-1 : ℝ), 1]] := Set.uIoc_subset_uIcc hx
          simpa [Set.uIcc_of_le (by norm_num : (-1 : ℝ) ≤ 1)] using hxU
        have hgx : |g x| ≤ ‖gf‖ := hgb x hxIcc
        have hpnt : |g x - p.eval x| ≤ ε₁ := by
          have hnormp : ‖gf - Polynomial.toContinuousMapOn p (Set.Icc (-1) 1)‖ ≤ ε₁ := le_of_lt hp
          have hpt := ((ContinuousMap.norm_le (gf - Polynomial.toContinuousMapOn p (Set.Icc (-1) 1)) (le_of_lt hε₁)).mp hnormp) ⟨x, hxIcc⟩
          simpa [gf] using hpt
        have hcalc : |g x * (g x - p.eval x)| ≤ ‖gf‖ * ε₁ := by
          calc
            |g x * (g x - p.eval x)| = |g x| * |g x - p.eval x| := abs_mul _ _
            _ ≤ ‖gf‖ * ε₁ := mul_le_mul hgx hpnt (abs_nonneg _) hM0
        simpa [Real.norm_eq_abs] using hcalc
      have hnorm' : |(∫ x in (-1 : ℝ)..1, g x * (g x - p.eval x))| ≤
          ‖gf‖ * ε₁ * |(1 : ℝ) - (-1)| := by
        simpa [Real.norm_eq_abs] using hnorm
      have h2 : |(1 : ℝ) - (-1)| = 2 := by norm_num
      rwa [h2] at hnorm'
    have hsum : (∫ x in (-1 : ℝ)..1, g x ^ 2) ≤ ‖gf‖ * ε₁ * 2 := by
      rw [hsplit]
      rw [hgp, add_zero]
      exact le_trans (le_abs_self _) hb
    have hlt : ‖gf‖ * ε₁ * 2 < ε := by
      dsimp [ε₁]
      have hmain : ‖gf‖ * (ε / (2 * (‖gf‖ + 1))) * 2 = ‖gf‖ * ε / (‖gf‖ + 1) := by
        field_simp [show 2 * (‖gf‖ + 1) ≠ 0 by positivity, show (‖gf‖ + 1) ≠ 0 by positivity]
      rw [hmain]
      have hden : 0 < ‖gf‖ + 1 := by positivity
      have hq : ‖gf‖ / (‖gf‖ + 1) < 1 := by
        rw [div_lt_one hden]
        linarith
      have hrewrite : ‖gf‖ * ε / (‖gf‖ + 1) = (‖gf‖ / (‖gf‖ + 1)) * ε := by ring
      rw [hrewrite]
      simpa using mul_lt_mul_of_pos_right hq hε
    simpa using le_of_lt (lt_of_le_of_lt hsum hlt)
  · exact intervalIntegral.integral_nonneg (by norm_num : (-1 : ℝ) ≤ 1) (by intro x hx; exact sq_nonneg _)

/-- The full contradiction step of the H^2 completeness proof: a continuous g
orthogonal to {K_c p_n} in L2 has integral g^2 = 0. -/
theorem completeness_contradiction (g : ℝ → ℝ) (hg : ContinuousOn g (Set.Icc (-1) 1)) {c : ℝ}
    (hc : 0 < c)
    (horth0 : momentFunctional g hg (KcR c 1) = 0)
    (horth1 : momentFunctional g hg (KcR c X) = 0)
    (horthE : ∀ n : ℕ, 2 ≤ n → momentFunctional g hg (KcR c (pEvenR n)) = 0)
    (horthO : ∀ n : ℕ, 2 ≤ n → momentFunctional g hg (KcR c (pOddR n)) = 0) :
    (∫ x in (-1 : ℝ)..1, g x ^ 2) = 0 := by
  have hcne : c ≠ 0 := ne_of_gt hc
  have h0 : MomentBound.moments g 0 = 0 := constant_orth_moment_zero g hg hcne horth0
  have h1 : MomentBound.moments g 1 = 0 := linear_orth_moment_zero g hg hcne horth1
  have hz : ∀ k : ℕ, MomentBound.moments g k = 0 := all_moments_zero g hg hc h0 h1 horthE horthO
  exact integral_sq_eq_zero_of_all_moments_zero g hg hz

/-- The completeness conclusion: a continuous g orthogonal to {K_c p_n} in L2
is zero almost everywhere on (-1,1). -/
theorem completeness_ae_zero (g : ℝ → ℝ) (hg : ContinuousOn g (Set.Icc (-1) 1)) {c : ℝ}
    (hc : 0 < c)
    (horth0 : momentFunctional g hg (KcR c 1) = 0)
    (horth1 : momentFunctional g hg (KcR c X) = 0)
    (horthE : ∀ n : ℕ, 2 ≤ n → momentFunctional g hg (KcR c (pEvenR n)) = 0)
    (horthO : ∀ n : ℕ, 2 ≤ n → momentFunctional g hg (KcR c (pOddR n)) = 0) :
    g =ᵐ[volume.restrict (Set.Ioc (-1) 1)] 0 := by
  have hI : (∫ x in (-1 : ℝ)..1, g x ^ 2) = 0 :=
    completeness_contradiction g hg hc horth0 horth1 horthE horthO
  have hIoc : (∫ x in Set.Ioc (-1) 1, g x ^ 2) = 0 := by
    rw [intervalIntegral.integral_of_le (by norm_num : (-1 : ℝ) ≤ 1)] at hI
    exact hI
  have hfi : Integrable (fun x : ℝ => g x ^ 2) (volume.restrict (Set.Ioc (-1) 1)) := by
    exact (ContinuousOn.integrableOn_Icc (hg.pow 2)).mono_set Set.Ioc_subset_Icc_self
  have hae : (fun x : ℝ => g x ^ 2) =ᵐ[volume.restrict (Set.Ioc (-1) 1)] 0 :=
    (integral_eq_zero_iff_of_nonneg (by intro x; exact sq_nonneg _) hfi).mp hIoc
  filter_upwards [hae] with x hx
  exact sq_eq_zero_iff.mp hx

end Weierstrass

end Completeness

end SL
