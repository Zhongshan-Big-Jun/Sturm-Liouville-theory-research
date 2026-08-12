import Mathlib
import SL.Completeness

/-!
# Transfer operator: closed form of K_c^{-r} on monomials

Formalization of the explicit action of the inverse powers of the shifted Krein
operator K_c p = -p'' + c p on the polynomial space (the "transmission operator"
section of `docs/SL_hs_orthogonal_systems_proof.tex`, Section 3):

For r ∈ ℕ and k ∈ ℕ,
    K_c^{-r} x^k = ∑_{j=0}^{⌊k/2⌋} binom(r+j-1, j) * c^{-(r+j)} * k!/(k-2j)! * x^{k-2j}.

Concretely we define `transferCoeff` (the coefficient closed form) and
`transferPoly c r k` (the polynomial on the right-hand side), then prove:

1. `KcR_transferPoly`: K_c (transferPoly c (r+1) k) = transferPoly c r k (the
   recursion that identifies `transferPoly` with K_c^{-1} applied r times),
2. `transferPoly_zero`: transferPoly c 0 k = X^k,
3. `KcR_inj` / `KcR_inv_left` / `KcR_inv_right`: K_c is a bijection of the
   polynomial space with inverse `KcR_inv` (for c ≠ 0),
4. `KcR_inv_iter_X_pow`: (KcR_inv)^[r] (X^k) = transferPoly c r k, i.e. the
   closed form of K_c^{-r} x^k,
5. `coeff_transferPoly` / `natDegree_transferPoly` / `transferCoeff_zero`:
   coefficient and degree properties used in the orthogonal-system construction.

The key algebraic steps are the Pascal rule for binomial coefficients and the
hockey-stick-style reindexing of the finite sum over j ≤ ⌊k/2⌋.
-/

namespace SL
namespace Transfer

open Polynomial
open scoped BigOperators

noncomputable section

/-- The shifted Krein operator on polynomials (alias of `Completeness.KcR`). -/
private abbrev KcR (c : ℝ) (p : Polynomial ℝ) : Polynomial ℝ := Completeness.KcR c p

/-- Factorials are non-zero in ℝ. -/
lemma factorial_cast_ne_zero (k : ℕ) : (Nat.factorial k : ℝ) ≠ 0 := by
  exact_mod_cast Nat.factorial_ne_zero k

/-- Coefficient of x^(k-2j) in K_c^{-r} x^k:
    binom(r+j-1, j) * k!/(k-2j)! / c^(r+j). -/
noncomputable def transferCoeff (c : ℝ) (r j k : ℕ) : ℝ :=
  (Nat.choose (r + j - 1) j : ℝ) * (Nat.factorial k : ℝ) /
    (Nat.factorial (k - 2 * j) : ℝ) / c ^ (r + j)

/-- The transfer polynomial T_{r,k} = K_c^{-r} x^k (right-hand side of the closed form). -/
noncomputable def transferPoly (c : ℝ) (r k : ℕ) : Polynomial ℝ :=
  ∑ j ∈ Finset.range (k / 2 + 1), C (transferCoeff c r j k) * X ^ (k - 2 * j)

/-- The inverse of K_c on polynomials: K_c^{-1} p = ∑ a_k T_{1,k}. -/
noncomputable def KcR_inv (c : ℝ) (p : Polynomial ℝ) : Polynomial ℝ :=
  p.sum fun k a => C a * transferPoly c 1 k

lemma KcR_add (c : ℝ) (p q : Polynomial ℝ) : KcR c (p + q) = KcR c p + KcR c q := by
  unfold KcR
  unfold Completeness.KcR
  rw [Polynomial.derivative_add, Polynomial.derivative_add]
  ring

lemma KcR_sum (c : ℝ) (s : Finset ℕ) (f : ℕ → Polynomial ℝ) :
    KcR c (∑ j ∈ s, f j) = ∑ j ∈ s, KcR c (f j) := by
  refine Finset.induction_on s ?_ ?_
  · simp [KcR, Completeness.KcR]
  · intro j t hjt hrec
    rw [Finset.sum_insert hjt, KcR_add, hrec, Finset.sum_insert hjt]

lemma KcR_polynomial_sum (c : ℝ) (p : Polynomial ℝ) (f : ℕ → ℝ → Polynomial ℝ) :
    KcR c (p.sum f) = p.sum fun k a => KcR c (f k a) := by
  classical
  rw [Polynomial.sum_def, Polynomial.sum_def]
  exact KcR_sum c p.support (fun k => f k (p.coeff k))

lemma KcR_C_mul (c : ℝ) (a : ℝ) (q : Polynomial ℝ) : KcR c (C a * q) = C a * KcR c q := by
  unfold KcR
  unfold Completeness.KcR
  rw [Polynomial.derivative_C_mul, Polynomial.derivative_C_mul]
  ring

lemma KcR_C_mul_X_pow (c : ℝ) (a : ℝ) (m : ℕ) :
    KcR c (C a * X ^ m) =
      C (c * a) * X ^ m - C (a * (m : ℝ) * ((m - 1 : ℕ) : ℝ)) * X ^ (m - 2) := by
  unfold KcR
  rw [Completeness.KcR_monomial]
  simp only [← Polynomial.C_mul]

lemma half_gap_product_zero (k : ℕ) : (k - 2 * (k / 2)) * (k - 2 * (k / 2) - 1) = 0 := by
  have hdiv : k = 2 * (k / 2) + k % 2 := (Nat.div_add_mod k 2).symm
  have hcases : k % 2 = 0 ∨ k % 2 = 1 := by omega
  rcases hcases with h0 | h1
  · have hk : k - 2 * (k / 2) = 0 := by omega
    rw [hk]
  · have hk : k - 2 * (k / 2) = 1 := by omega
    rw [hk]

lemma transferCoeff_zero (c : ℝ) (_hc : c ≠ 0) (r k : ℕ) :
    transferCoeff c r 0 k = 1 / c ^ r := by
  unfold transferCoeff
  have hf : (Nat.factorial k : ℝ) ≠ 0 := factorial_cast_ne_zero k
  simp [Nat.choose_zero_right, hf]

lemma transferCoeff_zero_rec (c : ℝ) (hc : c ≠ 0) (r k : ℕ) :
    c * transferCoeff c (r + 1) 0 k = transferCoeff c r 0 k := by
  rw [transferCoeff_zero c hc (r + 1) k, transferCoeff_zero c hc r k]
  field_simp [hc]
  rw [pow_succ]
  ring

lemma transferCoeff_rec (c : ℝ) (hc : c ≠ 0) (r k i : ℕ) (hi : 1 ≤ i) (hk : 2 * i ≤ k) :
    transferCoeff c r i k =
      c * transferCoeff c (r + 1) i k -
        transferCoeff c (r + 1) (i - 1) k *
          ((k - 2 * (i - 1) : ℕ) : ℝ) * ((k - 2 * (i - 1) - 1 : ℕ) : ℝ) := by
  have hmm2 : r + 1 + i - 1 = r + i := by omega
  have hmm3 : r + 1 + (i - 1) - 1 = r + i - 1 := by omega
  have hexp : r + 1 + (i - 1) = r + i := by omega
  have hsub : k - 2 * (i - 1) = (k - 2 * i) + 2 := by omega
  have hsub1 : k - 2 * (i - 1) - 1 = (k - 2 * i) + 1 := by omega
  have hPascal : Nat.choose (r + i) i =
      Nat.choose (r + i - 1) (i - 1) + Nat.choose (r + i - 1) i := by
    have h1 : (r + i - 1) + 1 = r + i := by omega
    have h2 : (i - 1) + 1 = i := by omega
    simpa [h1, h2] using Nat.choose_succ_succ (r + i - 1) (i - 1)
  have hPascalR : ((Nat.choose (r + i) i : ℕ) : ℝ) =
      ((Nat.choose (r + i - 1) (i - 1) : ℕ) : ℝ) + ((Nat.choose (r + i - 1) i : ℕ) : ℝ) := by
    exact_mod_cast hPascal
  have hp1 : c ^ (r + 1 + i) = c * c ^ (r + i) := by
    rw [show r + 1 + i = (r + i) + 1 by omega, pow_succ]
    ring
  have hfact (m : ℕ) : (Nat.factorial (m + 2) : ℝ) =
      (Nat.factorial m : ℝ) * ((m + 2 : ℕ) : ℝ) * ((m + 1 : ℕ) : ℝ) := by
    rw [Nat.factorial_succ, Nat.factorial_succ]
    simp [Nat.cast_add, Nat.cast_one]
    ring
  unfold transferCoeff
  rw [hmm2, hmm3, hexp, hsub1, hsub, hp1]
  rw [hPascalR, hfact (k - 2 * i)]
  have hden1 : (Nat.factorial (k - 2 * i) : ℝ) ≠ 0 := factorial_cast_ne_zero (k - 2 * i)
  have hpw : c ^ (r + i) ≠ 0 := pow_ne_zero (r + i) hc
  have hcmul : c * c ^ (r + i) ≠ 0 := mul_ne_zero hc hpw
  field_simp [hc, hpw, hcmul, hden1]
  ring

lemma transferPoly_zero (c : ℝ) (k : ℕ) : transferPoly c 0 k = X ^ k := by
  classical
  unfold transferPoly
  rw [Finset.sum_eq_single 0]
  · have hc0 : transferCoeff c 0 0 k = 1 := by
      unfold transferCoeff
      have hf : (Nat.factorial k : ℝ) ≠ 0 := factorial_cast_ne_zero k
      simp [hf]
    simp [hc0]
  · intro j hj hne
    have hjlt : j < k / 2 + 1 := by simpa [Finset.mem_range] using hj
    have hj1 : 1 ≤ j := Nat.succ_le_of_lt (Nat.pos_of_ne_zero hne)
    have hc0 : transferCoeff c 0 j k = 0 := by
      unfold transferCoeff
      have hchoose : Nat.choose (j - 1) j = 0 := by
        exact Nat.choose_eq_zero_of_lt (by omega)
      simp [hchoose]
    simp [hc0]
  · intro hnot
    exact False.elim (hnot (by simp [Finset.mem_range]))

lemma transferPoly_eq_split (c : ℝ) (r k : ℕ) :
    transferPoly c r k =
      C (transferCoeff c r 0 k) * X ^ k +
        ∑ i ∈ Finset.range (k / 2), C (transferCoeff c r (i + 1) k) * X ^ (k - 2 * (i + 1)) := by
  unfold transferPoly
  rw [Finset.sum_range_succ']
  ac_rfl

lemma KcR_transferPoly_step (c : ℝ) (r k j : ℕ) :
    KcR c (C (transferCoeff c (r + 1) j k) * X ^ (k - 2 * j)) =
      C (c * transferCoeff c (r + 1) j k) * X ^ (k - 2 * j) -
        C (transferCoeff c (r + 1) j k * ((k - 2 * j : ℕ) : ℝ) * ((k - 2 * j - 1 : ℕ) : ℝ)) *
          X ^ (k - 2 * (j + 1)) := by
  rw [KcR_C_mul_X_pow]
  have hsub : (k - 2 * j) - 2 = k - 2 * (j + 1) := by omega
  simp [hsub, mul_assoc]

lemma KcR_transferPoly (c : ℝ) (hc : c ≠ 0) (r k : ℕ) :
    KcR c (transferPoly c (r + 1) k) = transferPoly c r k := by
  classical
  let M := k / 2
  let B : ℕ → ℝ := fun j => transferCoeff c (r + 1) j k
  let A : ℕ → ℝ := fun j => transferCoeff c r j k
  have hLHS :
      KcR c (transferPoly c (r + 1) k) =
        C (c * B 0) * X ^ k +
          ∑ j ∈ Finset.range M,
            (C (c * B (j + 1)) - C (B j * ((k - 2 * j : ℕ) : ℝ) * ((k - 2 * j - 1 : ℕ) : ℝ))) *
              X ^ (k - 2 * (j + 1)) -
          C (B M * ((k - 2 * M : ℕ) : ℝ) * ((k - 2 * M - 1 : ℕ) : ℝ)) * X ^ (k - 2 * (M + 1)) := by
    unfold transferPoly
    rw [KcR_sum]
    simp_rw [KcR_transferPoly_step]
    rw [Finset.sum_sub_distrib]
    nth_rw 1 [Finset.sum_range_succ']
    rw [Finset.sum_range_succ]
    rw [sub_add_eq_sub_sub]
    nth_rw 1 [add_comm]
    nth_rw 1 [add_sub_assoc]
    rw [← Finset.sum_sub_distrib]
    simp_rw [← sub_mul]
    simp [B, M]
  have hmid (j : ℕ) (hj : j < M) :
      C (c * B (j + 1)) - C (B j * ((k - 2 * j : ℕ) : ℝ) * ((k - 2 * j - 1 : ℕ) : ℝ)) =
        C (A (j + 1)) := by
    have h2 : 2 * (j + 1) ≤ k := by
      have hM2 : 2 * M ≤ k := by omega
      omega
    have hrec := transferCoeff_rec c hc r k (j + 1) (by omega) h2
    have hrec' : A (j + 1) = c * B (j + 1) -
        B j * ((k - 2 * j : ℕ) : ℝ) * ((k - 2 * j - 1 : ℕ) : ℝ) := by
      simpa [A, B] using hrec
    rw [← map_sub]
    rw [← hrec']
  have hzero : C (c * B 0) = C (A 0) := by
    unfold B A
    rw [transferCoeff_zero_rec c hc r k]
  have htail :
      C (B M * ((k - 2 * M : ℕ) : ℝ) * ((k - 2 * M - 1 : ℕ) : ℝ)) * X ^ (k - 2 * (M + 1)) = 0 := by
    have hz : (k - 2 * M) * (k - 2 * M - 1) = 0 := by
      simpa [M] using half_gap_product_zero k
    have hz' : ((k - 2 * M : ℕ) : ℝ) * ((k - 2 * M - 1 : ℕ) : ℝ) = 0 := by
      exact_mod_cast hz
    rw [mul_assoc]
    rw [hz']
    simp
  have hmain :
      KcR c (transferPoly c (r + 1) k) =
        C (A 0) * X ^ k + ∑ j ∈ Finset.range M, C (A (j + 1)) * X ^ (k - 2 * (j + 1)) := by
    rw [hLHS, htail]
    rw [sub_zero]
    rw [hzero]
    refine congrArg₂ (fun a b => a + b) rfl ?_
    refine Finset.sum_congr rfl ?_
    intro j hj
    rw [hmid j (by simpa [Finset.mem_range] using hj)]
  rw [hmain]
  rw [transferPoly_eq_split]

lemma coeff_transferPoly (c : ℝ) (r j k : ℕ) (hj : 2 * j ≤ k) :
    (transferPoly c r k).coeff (k - 2 * j) = transferCoeff c r j k := by
  classical
  unfold transferPoly
  rw [finsetSum_coeff]
  rw [Finset.sum_eq_single j]
  · simp
  · intro j' hj' hne
    have h2j' : 2 * j' ≤ k := by
      have hj'le : j' ≤ k / 2 := by
        have hj'lt : j' < k / 2 + 1 := by simpa [Finset.mem_range] using hj'
        omega
      have : j' * 2 ≤ k := (Nat.le_div_iff_mul_le (by norm_num : 0 < 2)).mp hj'le
      simpa [mul_comm] using this
    have hne2 : k - 2 * j ≠ k - 2 * j' := by
      intro h
      have : 2 * j' = 2 * j := by omega
      exact hne (by omega)
    simp [hne2]
  · intro hnot
    have hjle : j ≤ k / 2 := (Nat.le_div_iff_mul_le (by norm_num : 0 < 2)).mpr (by
      simpa [mul_comm] using hj)
    exact False.elim (hnot (by
      simpa [Finset.mem_range] using Nat.lt_succ_of_le hjle))

lemma natDegree_transferPoly (c : ℝ) (hc : c ≠ 0) (r k : ℕ) :
    (transferPoly c r k).natDegree = k := by
  classical
  apply le_antisymm
  · unfold transferPoly
    refine natDegree_sum_le_of_forall_le (Finset.range (k / 2 + 1))
      (fun j => C (transferCoeff c r j k) * X ^ (k - 2 * j)) ?_
    intro j hj
    exact le_trans (natDegree_C_mul_X_pow_le (transferCoeff c r j k) (k - 2 * j)) (by omega)
  · by_contra hnot
    have hlt : (transferPoly c r k).natDegree < k := by omega
    have hcoeff0 : (transferPoly c r k).coeff k = 0 := Polynomial.coeff_eq_zero_of_natDegree_lt hlt
    have hc0 : (transferPoly c r k).coeff k = transferCoeff c r 0 k := by
      simpa using coeff_transferPoly c r 0 k (by omega)
    rw [hc0] at hcoeff0
    rw [transferCoeff_zero c hc r k] at hcoeff0
    exact (one_div_ne_zero (pow_ne_zero r hc)) hcoeff0

lemma KcR_inj (c : ℝ) (hc : c ≠ 0) {p q : Polynomial ℝ} (h : KcR c p = KcR c q) : p = q := by
  let r := p - q
  have hsub : KcR c r = 0 := by
    dsimp [r]
    unfold KcR
    rw [Completeness.KcR_sub]
    change KcR c p - KcR c q = 0
    rw [h]
    simp
  by_contra hrne
  have hr0 : r ≠ 0 := by
    intro hr0
    exact hrne (by simpa [r, sub_eq_zero] using hr0)
  have hcoeff : (KcR c r).coeff r.natDegree ≠ 0 := by
    unfold KcR
    unfold Completeness.KcR
    rw [Polynomial.coeff_add, Polynomial.coeff_neg, Polynomial.coeff_C_mul]
    have hd1 : (derivative (derivative r)).coeff r.natDegree = 0 := by
      rw [Polynomial.coeff_derivative, Polynomial.coeff_derivative]
      have hc2 : r.coeff (r.natDegree + 2) = 0 := by
        exact Polynomial.coeff_eq_zero_of_natDegree_lt (by omega)
      simp [hc2]
    have hlc : r.coeff r.natDegree ≠ 0 := (Polynomial.leadingCoeff_ne_zero).2 hr0
    have hlc0 : c * r.coeff r.natDegree ≠ 0 := mul_ne_zero hc hlc
    rw [hd1]
    rw [neg_zero, zero_add]
    exact hlc0
  exact hcoeff (by rw [hsub]; simp)

lemma KcR_inv_left (c : ℝ) (hc : c ≠ 0) (p : Polynomial ℝ) : KcR c (KcR_inv c p) = p := by
  rw [KcR_inv, KcR_polynomial_sum]
  simp_rw [KcR_C_mul]
  have hstep (k : ℕ) : KcR c (transferPoly c 1 k) = transferPoly c 0 k := by
    simpa using KcR_transferPoly c hc 0 k
  simp_rw [hstep, transferPoly_zero]
  rw [Polynomial.sum_C_mul_X_pow_eq]

lemma KcR_inv_right (c : ℝ) (hc : c ≠ 0) (p : Polynomial ℝ) : KcR_inv c (KcR c p) = p := by
  exact KcR_inj c hc (KcR_inv_left c hc (KcR c p))

/-- The closed form of K_c^{-r} x^k for every r: (KcR_inv)^[r] (X^k) = T_{r,k}. -/
theorem KcR_inv_iter_X_pow (c : ℝ) (hc : c ≠ 0) (r k : ℕ) :
    (KcR_inv c)^[r] (X ^ k) = transferPoly c r k := by
  induction r with
  | zero => simp [transferPoly_zero]
  | succ r ih =>
      rw [Function.iterate_succ_apply', ih]
      apply KcR_inj c hc
      rw [KcR_inv_left c hc]
      exact (KcR_transferPoly c hc r k).symm

end

/-! ## Public wrappers (usable from other files) -/

/-- Public version of `KcR_inv_left`: the private alias `KcR` is not
accessible from other files, so restate the cancellation with
`Completeness.KcR`. -/
lemma KcR_inv_left_public (c : ℝ) (hc : c ≠ 0) (p : Polynomial ℝ) :
    Completeness.KcR c (KcR_inv c p) = p := by
  exact KcR_inv_left c hc p

/-- Public version of `KcR_inv_right`. -/
lemma KcR_inv_right_public (c : ℝ) (hc : c ≠ 0) (p : Polynomial ℝ) :
    KcR_inv c (Completeness.KcR c p) = p := by
  exact KcR_inv_right c hc p

/-- Public version of `KcR_inj`. -/
lemma KcR_inj_public (c : ℝ) (hc : c ≠ 0) {p q : Polynomial ℝ}
    (h : Completeness.KcR c p = Completeness.KcR c q) : p = q := by
  exact KcR_inj c hc h

end Transfer
end SL
