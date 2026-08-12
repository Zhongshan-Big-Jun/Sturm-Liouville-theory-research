import Mathlib
import SL.TransferOperator

/-!
# H^s explicit orthogonal systems: transport machinery

Formalization of the polynomial-level transport of
`docs/SL_hs_orthogonal_systems_proof.tex` (Section 3, "主定理的证明"; Section 4,
"闭式系数"): the construction `Q_n^{(s)} = K_c^{-r} P_n` (even case s = 2r) and
`Q_n^{(2r+1)} = K_c^{-r} K_n` (odd case), and the identities
`(Q_m, Q_n)_{2r} = (P_m, P_n)_{L^2}` / `(Q_m, Q_n)_{2r+1} = (K_m, K_n)_1`
that reduce the orthogonality of the transported system to the classical
systems.

Concretely:

1. `legendreCoeff` / `legendreClosed`: the explicit Legendre coefficient
   formula (source (11)) and `natDegree_legendreClosed` (deg P_n = n).
2. `qnEven` / `qnOdd`: `Q_n^{(s)} := K_c^{-r} P_n / K_c^{-r} K_n` via
   `Transfer.KcR_inv` iterates; `hsPairingEven` / `hsPairingOdd`: the
   transported pairings `(p, q)_{2r} = ∫ (K_c^r p)(K_c^r q)` and
   `(p, q)_{2r+1} = (K_c^r p, K_c^r q)_1` (with `h1PairingPoly`, the H1 pairing
   on polynomials with the explicit boundary-difference term).
3. `KcR_iter_inv_iter` (K_c^r K_c^{-r} = id on polynomials), the degree
   transport `natDegree_iter_KcR_inv`, and the reduction theorems
   `hs_even_pairing` / `hs_odd_pairing` (orthogonality of {Q_n} reduces to that
   of {P_n} / {K_n}) together with `hs_even_deg` / `hs_odd_deg`.
4. `aSeq`: the Krein-Sobolev coefficient sequence (source (9)) with the base
   values a_0 = a_1 = a_2 = a_3 = 1, used in the odd-case norm formula
   `2c/(2n+1) · a_n · a_{n+2}`.

Honesty note: the classical facts are NOT formalized here and enter as
hypotheses of `LegendreFacts` / `KreinSobolevFacts`: Legendre L^2 orthogonality
`∫ P_m P_n = 2/(2n+1) δ_{mn}`, the normalization `P_n(1) = 1` (source (11),
classical), and the Krein-Sobolev H^1 orthogonality with the norm formula
`2c/(2n+1) a_n a_{n+2}` (source, Jones-Littlejohn-Quintero Roba, Theorem 3,
literature).  The operator-level statements (K_c^r : H^s -> L^2 / H^1 is an
isometric isomorphism, completeness/density of {P_n} in L^2 and {K_n} in H^1)
need spectral theory and are out of scope; what is formalized is the
polynomial transport that the source proof uses after the isometry step.
-/

namespace SL
namespace HsOrthogonalSystems

open Polynomial
open scoped BigOperators
open scoped Real Interval
open MeasureTheory

noncomputable section

/-! ## Krein-Sobolev coefficient sequence (source (9)) -/

/-- The coefficient sequence a_n of the Krein-Sobolev polynomials (source (9)):
a_0 = a_1 = a_2 = a_3 = 1 and, for n ≥ 2,
a_{n+2} = a_n (1 + (4n^2 - 1)/c) + (2n+1)/(2n-3) (a_n - a_{n-2});
here the pattern `k + 4` stands for the index n + 2 with n = k + 2. -/
noncomputable def aSeq (c : ℝ) : ℕ → ℝ
  | 0 => 1
  | 1 => 1
  | 2 => 1
  | 3 => 1
  | k + 4 =>
      aSeq c (k + 2) * (1 + ((4 * (k + 2) ^ 2 - 1 : ℕ) : ℝ) / c) +
        (((2 * (k + 2) + 1 : ℕ) : ℝ) / ((2 * (k + 2) - 3 : ℕ) : ℝ)) *
          (aSeq c (k + 2) - aSeq c k)

lemma aSeq_zero (c : ℝ) : aSeq c 0 = 1 := rfl

lemma aSeq_one (c : ℝ) : aSeq c 1 = 1 := rfl

lemma aSeq_two (c : ℝ) : aSeq c 2 = 1 := rfl

lemma aSeq_three (c : ℝ) : aSeq c 3 = 1 := rfl

/-- a_4 = 1 + 15/c (first nontrivial value of the recurrence). -/
lemma aSeq_four (c : ℝ) : aSeq c 4 = 1 + 15 / c := by
  norm_num [aSeq, aSeq_zero, aSeq_two]

/-! ## Legendre closed form (source (11)) -/

/-- The coefficient of x^(n-2k) in the Legendre polynomial P_n (source (11)):
`(-1)^k (2n-2k)! / (k! (n-k)! (n-2k)!)`. -/
noncomputable def legendreCoeff (n k : ℕ) : ℝ :=
  (-1 : ℝ) ^ k *
    ((Nat.factorial (2 * n - 2 * k) : ℝ) /
      (Nat.factorial k * Nat.factorial (n - k) * Nat.factorial (n - 2 * k) : ℝ))

/-- The Legendre polynomial P_n via the closed form (11):
`P_n = 2^{-n} Σ_{k=0}^{⌊n/2⌋} legendreCoeff n k · x^{n-2k}`. -/
noncomputable def legendreClosed (n : ℕ) : Polynomial ℝ :=
  C ((2 : ℝ)⁻¹ ^ n) *
    ∑ k ∈ Finset.range (n / 2 + 1), C (legendreCoeff n k) * X ^ (n - 2 * k)

/-- The closed-form coefficients are nonzero (all factors are). -/
lemma legendreCoeff_ne_zero (n k : ℕ) : legendreCoeff n k ≠ 0 := by
  unfold legendreCoeff
  refine mul_ne_zero (pow_ne_zero k (by norm_num : (-1 : ℝ) ≠ 0)) ?_
  exact div_ne_zero (by exact_mod_cast (Nat.factorial_ne_zero (2 * n - 2 * k))) (by
    exact mul_ne_zero (mul_ne_zero (by exact_mod_cast (Nat.factorial_ne_zero k))
      (by exact_mod_cast (Nat.factorial_ne_zero (n - k))))
      (by exact_mod_cast (Nat.factorial_ne_zero (n - 2 * k))))

/-- k ∈ range(n/2+1) implies 2k ≤ n. -/
lemma mem_range_div_two {n j : ℕ} (hj : j ∈ Finset.range (n / 2 + 1)) : 2 * j ≤ n := by
  have hj' : j < n / 2 + 1 := Finset.mem_range.mp hj
  have hj'' : j ≤ n / 2 := Nat.lt_succ_iff.mp hj'
  have hj2 : j * 2 ≤ n := (Nat.le_div_iff_mul_le (by norm_num : 0 < 2)).mp hj''
  omega

/-- The degree of the closed-form Legendre polynomial is exactly n. -/
lemma natDegree_legendreClosed (n : ℕ) : (legendreClosed n).natDegree = n := by
  have hle : (legendreClosed n).natDegree ≤ n := by
    rw [Polynomial.natDegree_le_iff_coeff_eq_zero]
    intro k hk
    unfold legendreClosed
    rw [Polynomial.coeff_C_mul]
    simp_rw [← Polynomial.lcoeff_apply, map_sum, Polynomial.lcoeff_apply]
    rw [Finset.mul_sum]
    apply Finset.sum_eq_zero
    intro j hj
    rw [Polynomial.coeff_C_mul_X_pow]
    have hjk : k ≠ n - 2 * j := by
      have hj2 : 2 * j ≤ n := mem_range_div_two hj
      omega
    simp [hjk]
  have hcoeff : (legendreClosed n).coeff n ≠ 0 := by
    unfold legendreClosed
    rw [Polynomial.coeff_C_mul]
    simp_rw [← Polynomial.lcoeff_apply, map_sum, Polynomial.lcoeff_apply]
    have hs : (∑ x ∈ Finset.range (n / 2 + 1),
        (C (legendreCoeff n x) * X ^ (n - 2 * x)).coeff n) = legendreCoeff n 0 := by
      have hs1 : (∑ x ∈ Finset.range (n / 2 + 1),
          (C (legendreCoeff n x) * X ^ (n - 2 * x)).coeff n)
          = (C (legendreCoeff n 0) * X ^ (n - 2 * 0)).coeff n := by
        refine Finset.sum_eq_single 0 ?_ ?_
        · intro b hb hb0
          rw [Polynomial.coeff_C_mul_X_pow]
          have hb2 : 2 * b ≤ n := mem_range_div_two hb
          have hne : n ≠ n - 2 * b := by
            intro h
            have : 2 * b = 0 := by omega
            have : b = 0 := by omega
            exact hb0 this
          simp [hne]
        · intro h0
          exact False.elim (h0 (Finset.mem_range.mpr (by omega)))
      have hs2 : (C (legendreCoeff n 0) * X ^ (n - 2 * 0)).coeff n = legendreCoeff n 0 := by
        simp
      exact hs1.trans hs2
    rw [hs]
    exact mul_ne_zero (pow_ne_zero n (inv_ne_zero (by norm_num : (2 : ℝ) ≠ 0)))
      (legendreCoeff_ne_zero n 0)
  exact Polynomial.natDegree_eq_of_le_of_coeff_ne_zero hle hcoeff

/-! ## Transport machinery (source Section 3) -/

/-- K_c^r K_c^{-r} = id on polynomials (iterate version). -/
lemma KcR_iter_inv_iter (c : ℝ) (hc : c ≠ 0) (r : ℕ) (p : Polynomial ℝ) :
    (Completeness.KcR c)^[r] ((Transfer.KcR_inv c)^[r] p) = p := by
  have hL : Function.LeftInverse (Completeness.KcR c) (Transfer.KcR_inv c) := by
    intro p'
    exact Transfer.KcR_inv_left_public c hc p'
  exact (hL.iterate r) p

/-- K_c maps 0 to 0. -/
lemma KcR_zero (c : ℝ) : Completeness.KcR c 0 = 0 := by
  simp [Completeness.KcR]

/-- K_c^r 0 = 0. -/
lemma KcR_iter_zero (c : ℝ) (r : ℕ) : (Completeness.KcR c)^[r] 0 = 0 := by
  induction r with
  | zero => simp
  | succ r ih =>
      rw [Function.iterate_succ_apply, KcR_zero, ih]

/-- K_c^{-1} 0 = 0 (c ≠ 0). -/
lemma KcR_inv_zero (c : ℝ) (hc : c ≠ 0) : Transfer.KcR_inv c 0 = 0 := by
  apply Transfer.KcR_inj_public c hc
  rw [Transfer.KcR_inv_left_public c hc, KcR_zero]

/-- K_c^{-r} 0 = 0 (c ≠ 0). -/
lemma KcR_inv_iter_zero (c : ℝ) (hc : c ≠ 0) (r : ℕ) : (Transfer.KcR_inv c)^[r] 0 = 0 := by
  induction r with
  | zero => simp
  | succ r ih =>
      rw [Function.iterate_succ_apply, KcR_inv_zero c hc, ih]

/-- K_c preserves the degree of a nonzero polynomial (c ≠ 0). -/
lemma natDegree_KcR {c : ℝ} (hc : c ≠ 0) (p : Polynomial ℝ) :
    (Completeness.KcR c p).natDegree = p.natDegree := by
  unfold Completeness.KcR
  by_cases hcst : p.natDegree = 0
  · have hpC : p = C (p.coeff 0) := Polynomial.eq_C_of_natDegree_eq_zero hcst
    rw [hpC]
    simp
    rw [← Polynomial.C_mul]
    rw [Polynomial.natDegree_C]
  · have hdegC : (C c * p).natDegree = p.natDegree := Polynomial.natDegree_C_mul hc
    have hd2 : (-p.derivative.derivative).natDegree < (C c * p).natDegree := by
      rw [Polynomial.natDegree_neg, hdegC]
      by_cases h1 : p.derivative.natDegree = 0
      · have hpp : p.derivative.derivative = 0 := by
          rw [Polynomial.eq_C_of_natDegree_eq_zero h1]
          simp
        rw [hpp, Polynomial.natDegree_zero]
        exact Nat.pos_of_ne_zero hcst
      · have hd1 : p.derivative.natDegree < p.natDegree :=
          Polynomial.natDegree_derivative_lt hcst
        by_cases h2 : p.derivative.derivative.natDegree = 0
        · rw [h2]
          exact Nat.pos_of_ne_zero hcst
        · have hd2' : p.derivative.derivative.natDegree < p.derivative.natDegree :=
            Polynomial.natDegree_derivative_lt h1
          exact lt_trans hd2' hd1
    have hmain : (-p.derivative.derivative + C c * p).natDegree = (C c * p).natDegree :=
      Polynomial.natDegree_add_eq_right_of_natDegree_lt hd2
    rw [hmain, hdegC]

/-- K_c^{-1} preserves the degree of a nonzero polynomial (c ≠ 0). -/
lemma natDegree_KcR_inv (c : ℝ) (hc : c ≠ 0) {p : Polynomial ℝ} (hp : p ≠ 0) :
    (Transfer.KcR_inv c p).natDegree = p.natDegree := by
  have hne : Transfer.KcR_inv c p ≠ 0 := by
    intro h
    have h' := congrArg (fun q : Polynomial ℝ => Completeness.KcR c q) h
    rw [Transfer.KcR_inv_left_public c hc] at h'
    rw [KcR_zero] at h'
    exact hp h'
  have hdeg := natDegree_KcR hc (Transfer.KcR_inv c p)
  rw [Transfer.KcR_inv_left_public c hc] at hdeg
  exact hdeg.symm

/-- K_c^{-r} preserves the degree of a nonzero polynomial (c ≠ 0). -/
lemma natDegree_iter_KcR_inv (c : ℝ) (hc : c ≠ 0) {p : Polynomial ℝ} (hp : p ≠ 0)
    (r : ℕ) : ((Transfer.KcR_inv c)^[r] p).natDegree = p.natDegree := by
  induction r with
  | zero => simp
  | succ r ih =>
      rw [Function.iterate_succ_apply']
      have hne' : (Transfer.KcR_inv c)^[r] p ≠ 0 := by
        intro h
        have h' := congrArg (fun q : Polynomial ℝ => (Completeness.KcR c)^[r] q) h
        rw [KcR_iter_inv_iter c hc r] at h'
        rw [KcR_iter_zero c r] at h'
        exact hp h'
      rw [natDegree_KcR_inv c hc hne']
      exact ih

/-! ## The transported pairings and Q_n (source Section 3) -/

/-- The transported H^{2r} pairing on polynomials:
`(p, q)_{2r} := ∫_{-1}^1 (K_c^r p)(x) (K_c^r q)(x) dx`. -/
noncomputable def hsPairingEven (c : ℝ) (r : ℕ) (p q : Polynomial ℝ) : ℝ :=
  ∫ x in (-1 : ℝ)..1, ((Completeness.KcR c)^[r] p).eval x * ((Completeness.KcR c)^[r] q).eval x

/-- The H1 pairing on polynomials (source boundary-difference form):
`(p, q)_1 = ∫ p'q' + c∫ pq - (1/2)(Δp)(Δq)` with `Δp = p(1) - p(-1)`. -/
noncomputable def h1PairingPoly (c : ℝ) (p q : Polynomial ℝ) : ℝ :=
  (∫ x in (-1 : ℝ)..1, p.derivative.eval x * q.derivative.eval x)
    + c * (∫ x in (-1 : ℝ)..1, p.eval x * q.eval x)
    - (1 / 2) * (p.eval 1 - p.eval (-1)) * (q.eval 1 - q.eval (-1))

/-- The transported H^{2r+1} pairing on polynomials:
`(p, q)_{2r+1} := (K_c^r p, K_c^r q)_1`. -/
noncomputable def hsPairingOdd (c : ℝ) (r : ℕ) (p q : Polynomial ℝ) : ℝ :=
  h1PairingPoly c ((Completeness.KcR c)^[r] p) ((Completeness.KcR c)^[r] q)

/-- Q_n^{(2r)} := K_c^{-r} P_n. -/
noncomputable def qnEven (P : ℕ → Polynomial ℝ) (c : ℝ) (r n : ℕ) : Polynomial ℝ :=
  (Transfer.KcR_inv c)^[r] (P n)

/-- Q_n^{(2r+1)} := K_c^{-r} K_n. -/
noncomputable def qnOdd (K : ℕ → Polynomial ℝ) (c : ℝ) (r n : ℕ) : Polynomial ℝ :=
  (Transfer.KcR_inv c)^[r] (K n)

/-- Orthogonality transport, even case: the pairing of Q_m, Q_n in H^{2r}
reduces to the L2 pairing of P_m, P_n. -/
theorem hs_even_pairing {c : ℝ} (hc : c ≠ 0) (r : ℕ) (P : ℕ → Polynomial ℝ)
    (hPorth : ∀ m n : ℕ, (∫ x in (-1 : ℝ)..1, (P m).eval x * (P n).eval x) =
      if m = n then 2 / (2 * (n : ℝ) + 1) else 0) :
    ∀ m n : ℕ, hsPairingEven c r (qnEven P c r m) (qnEven P c r n) =
      if m = n then 2 / (2 * (n : ℝ) + 1) else 0 := by
  intro m n
  unfold hsPairingEven qnEven
  rw [KcR_iter_inv_iter c hc r (P m), KcR_iter_inv_iter c hc r (P n)]
  exact hPorth m n

/-- Orthogonality transport, odd case: the pairing of Q_m, Q_n in H^{2r+1}
reduces to the H1 pairing of K_m, K_n. -/
theorem hs_odd_pairing {c : ℝ} (hc : c ≠ 0) (r : ℕ) (K : ℕ → Polynomial ℝ)
    (hKorth : ∀ m n : ℕ, h1PairingPoly c (K m) (K n) =
      if m = n then 2 * c / (2 * (n : ℝ) + 1) * aSeq c n * aSeq c (n + 2) else 0) :
    ∀ m n : ℕ, hsPairingOdd c r (qnOdd K c r m) (qnOdd K c r n) =
      if m = n then 2 * c / (2 * (n : ℝ) + 1) * aSeq c n * aSeq c (n + 2) else 0 := by
  intro m n
  unfold hsPairingOdd qnOdd
  rw [KcR_iter_inv_iter c hc r (K m), KcR_iter_inv_iter c hc r (K n)]
  exact hKorth m n

/-- Degree transport, even case: deg Q_n^{(2r)} = n whenever deg P_n = n. -/
theorem hs_even_deg {c : ℝ} (hc : c ≠ 0) (r n : ℕ) (P : ℕ → Polynomial ℝ)
    (hdegP : ∀ n : ℕ, (P n).natDegree = n) : (qnEven P c r n).natDegree = n := by
  unfold qnEven
  by_cases hz : P n = 0
  · have hn0 : n = 0 := by
      specialize hdegP n
      rw [hz] at hdegP
      simpa using hdegP.symm
    subst n
    rw [hz, KcR_inv_iter_zero c hc r]
    simp
  · rw [natDegree_iter_KcR_inv c hc hz r]
    exact hdegP n

/-- Degree transport, odd case: deg Q_n^{(2r+1)} = n whenever deg K_n = n. -/
theorem hs_odd_deg {c : ℝ} (hc : c ≠ 0) (r n : ℕ) (K : ℕ → Polynomial ℝ)
    (hdegK : ∀ n : ℕ, (K n).natDegree = n) : (qnOdd K c r n).natDegree = n := by
  unfold qnOdd
  by_cases hz : K n = 0
  · have hn0 : n = 0 := by
      specialize hdegK n
      rw [hz] at hdegK
      simpa using hdegK.symm
    subst n
    rw [hz, KcR_inv_iter_zero c hc r]
    simp
  · rw [natDegree_iter_KcR_inv c hc hz r]
    exact hdegK n

/-- The classical Legendre facts (source (11), classical, NOT formalized
here): L2 orthogonality with norm 2/(2n+1), degree n, and P_n(1) = 1. -/
def LegendreFacts (P : ℕ → Polynomial ℝ) : Prop :=
  (∀ m n : ℕ, (∫ x in (-1 : ℝ)..1, (P m).eval x * (P n).eval x) =
      if m = n then 2 / (2 * (n : ℝ) + 1) else 0) ∧
    (∀ n : ℕ, (P n).natDegree = n) ∧
    (∀ n : ℕ, (P n).eval 1 = 1)

/-- The classical Krein-Sobolev facts (source (9)+(10), literature,
NOT formalized here): H1 orthogonality with norm 2c/(2n+1) a_n a_{n+2} and
degree n. -/
def KreinSobolevFacts (c : ℝ) (K : ℕ → Polynomial ℝ) : Prop :=
  (∀ m n : ℕ, h1PairingPoly c (K m) (K n) =
      if m = n then 2 * c / (2 * (n : ℝ) + 1) * aSeq c n * aSeq c (n + 2) else 0) ∧
    (∀ n : ℕ, (K n).natDegree = n)

/-- Assembled even-case theorem: given the classical Legendre facts, the
transported system {Q_n^{(2r)}} is orthogonal with norm 2/(2n+1) in the
transported pairing and has deg Q_n = n. -/
theorem hs_even_main {c : ℝ} (hc : c ≠ 0) (r : ℕ) (P : ℕ → Polynomial ℝ)
    (hP : LegendreFacts P) :
    (∀ m n : ℕ, hsPairingEven c r (qnEven P c r m) (qnEven P c r n) =
      if m = n then 2 / (2 * (n : ℝ) + 1) else 0) ∧
      (∀ n : ℕ, (qnEven P c r n).natDegree = n) := by
  constructor
  · exact hs_even_pairing hc r P hP.1
  · intro n
    exact hs_even_deg hc r n P hP.2.1

/-- Assembled odd-case theorem: given the classical Krein-Sobolev facts, the
transported system {Q_n^{(2r+1)}} is orthogonal with norm
2c/(2n+1) a_n a_{n+2} in the transported pairing and has deg Q_n = n. -/
theorem hs_odd_main {c : ℝ} (hc : c ≠ 0) (r : ℕ) (K : ℕ → Polynomial ℝ)
    (hK : KreinSobolevFacts c K) :
    (∀ m n : ℕ, hsPairingOdd c r (qnOdd K c r m) (qnOdd K c r n) =
      if m = n then 2 * c / (2 * (n : ℝ) + 1) * aSeq c n * aSeq c (n + 2) else 0) ∧
      (∀ n : ℕ, (qnOdd K c r n).natDegree = n) := by
  constructor
  · exact hs_odd_pairing hc r K hK.1
  · intro n
    exact hs_odd_deg hc r n K hK.2

/-! ## Sanity: the r = 0 reduction (source remark after the main theorem) -/

lemma qnEven_r0 (P : ℕ → Polynomial ℝ) (c : ℝ) (n : ℕ) : qnEven P c 0 n = P n := by
  simp [qnEven]

lemma qnOdd_r0 (K : ℕ → Polynomial ℝ) (c : ℝ) (n : ℕ) : qnOdd K c 0 n = K n := by
  simp [qnOdd]

lemma hs_pairing_even_r0 (c : ℝ) (p q : Polynomial ℝ) :
    hsPairingEven c 0 p q = ∫ x in (-1 : ℝ)..1, p.eval x * q.eval x := by
  simp [hsPairingEven]

lemma hs_pairing_odd_r0 (c : ℝ) (p q : Polynomial ℝ) :
    hsPairingOdd c 0 p q = h1PairingPoly c p q := by
  simp [hsPairingOdd]

end
end HsOrthogonalSystems
end SL
