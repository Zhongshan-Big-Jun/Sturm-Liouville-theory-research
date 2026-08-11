import Mathlib

open scoped BigOperators

/-!
# Quantitative growth lemma for general second-order jump recurrences

Formalization of Theorem 2.1 (增长引理, 定量形式) from
`docs/SL_stability_moment_jump.tex`: for c0 > 0 and coefficient sequences
A, B : Nat -> K satisfying B m >= 0 and A m - B m >= c0 for every m >= 2,
the solution u of

  u 0 = 0,  u 1 = 1,
  c0 * u m = A m * u (m - 1) - B m * u (m - 2)     (m >= 2)

is strictly positive, nondecreasing, and satisfies the product lower bound

  u m >= ∏_{k=2}^{m} (A k - B k) / c0  =  ∏_{k=2}^{m} (1 + eps k),
  eps k := (A k - B k - c0) / c0 >= 0.

This generalizes the Krein-coefficient growth lemma (SL/MomentGrowth.lean) to
arbitrary admissible coefficient perturbations, which is the stability core of
the moment-jump completeness criterion.
-/

namespace SL

namespace StabilityGrowth

variable {K : Type} [Field K] [LinearOrder K] [IsStrictOrderedRing K]
variable {c0 : K} {A B : Nat -> K}

noncomputable def u (c0 : K) (A B : Nat -> K) : Nat -> K
  | 0 => 0
  | 1 => 1
  | Nat.succ (Nat.succ n) =>
      (A (n + 2) * u c0 A B (n + 1) - B (n + 2) * u c0 A B n) / c0

omit [LinearOrder K] [IsStrictOrderedRing K] in
lemma u_recurrence (hc0 : c0 ≠ 0) {j : Nat} :
    c0 * u c0 A B (j + 2) = A (j + 2) * u c0 A B (j + 1) - B (j + 2) * u c0 A B j := by
  simp [u]
  field_simp [hc0]

omit [LinearOrder K] [IsStrictOrderedRing K] in
lemma u_recurrence' (hc0 : c0 ≠ 0) {j : Nat} (hj : 2 ≤ j) :
    c0 * u c0 A B j = A j * u c0 A B (j - 1) - B j * u c0 A B (j - 2) := by
  have h := u_recurrence (c0 := c0) (A := A) (B := B) hc0 (j := j - 2)
  have h1 : j - 2 + 2 = j := by omega
  have h2 : j - 2 + 1 = j - 1 := by omega
  simpa [h1, h2] using h

omit [LinearOrder K] [IsStrictOrderedRing K] in
lemma u_one : u c0 A B 1 = 1 := by
  simp [u]

omit [LinearOrder K] [IsStrictOrderedRing K] in
lemma u_zero : u c0 A B 0 = 0 := by
  simp [u]

lemma u_two (hc0 : 0 < c0)
    (hB : ∀ m : Nat, 2 ≤ m → 0 ≤ B m)
    (hAB : ∀ m : Nat, 2 ≤ m → c0 ≤ A m - B m) :
    1 ≤ u c0 A B 2 := by
  have hrec : c0 * u c0 A B 2 = A 2 * u c0 A B 1 - B 2 * u c0 A B 0 := by
    have h := u_recurrence' (c0 := c0) (A := A) (B := B) (ne_of_gt hc0) (by omega : 2 ≤ 2)
    simpa using h
  have hA : c0 ≤ A 2 := by
    have hAB2 := hAB 2 (by omega)
    have hB2 := hB 2 (by omega)
    nlinarith
  have hrec' : c0 * u c0 A B 2 = A 2 := by
    rw [hrec]
    simp [u_one, u_zero]
  have hle : c0 ≤ c0 * u c0 A B 2 := by
    rw [hrec']
    exact hA
  nlinarith [hle, hc0]

lemma step_monotone (hc0 : 0 < c0)
    (hB : ∀ m : Nat, 2 ≤ m → 0 ≤ B m)
    (hAB : ∀ m : Nat, 2 ≤ m → c0 ≤ A m - B m)
    {j : Nat} (hj : 1 ≤ j)
    (hprev : 0 < u c0 A B j ∧ u c0 A B j ≤ u c0 A B (j + 1)) :
    0 < u c0 A B (j + 1) ∧ u c0 A B (j + 1) ≤ u c0 A B (j + 2) := by
  constructor
  · exact lt_of_lt_of_le hprev.1 hprev.2
  · have hrec : c0 * u c0 A B (j + 2) =
        A (j + 2) * u c0 A B (j + 1) - B (j + 2) * u c0 A B j :=
      u_recurrence (ne_of_gt hc0)
    have hB' : 0 ≤ B (j + 2) := hB (j + 2) (by omega)
    have hBmul : B (j + 2) * u c0 A B j ≤ B (j + 2) * u c0 A B (j + 1) :=
      mul_le_mul_of_nonneg_left hprev.2 hB'
    have hAB' : c0 ≤ A (j + 2) - B (j + 2) := hAB (j + 2) (by omega)
    have h2 : c0 * u c0 A B (j + 1) ≤ c0 * u c0 A B (j + 2) := by
      rw [hrec]
      calc
        c0 * u c0 A B (j + 1)
            ≤ (A (j + 2) - B (j + 2)) * u c0 A B (j + 1) := by
                exact mul_le_mul_of_nonneg_right hAB'
                  (le_of_lt (lt_of_lt_of_le hprev.1 hprev.2))
        _ = A (j + 2) * u c0 A B (j + 1) - B (j + 2) * u c0 A B (j + 1) := by ring
        _ ≤ A (j + 2) * u c0 A B (j + 1) - B (j + 2) * u c0 A B j := by nlinarith [hBmul]
    nlinarith [h2, hc0]

theorem monotone_pos (hc0 : 0 < c0)
    (hB : ∀ m : Nat, 2 ≤ m → 0 ≤ B m)
    (hAB : ∀ m : Nat, 2 ≤ m → c0 ≤ A m - B m) :
    ∀ j : Nat, 1 ≤ j → 0 < u c0 A B j ∧ u c0 A B j ≤ u c0 A B (j + 1) := by
  intro j hj
  have hbase : 0 < u c0 A B 1 ∧ u c0 A B 1 ≤ u c0 A B 2 := by
    constructor
    · simp [u]
    · rw [u_one]
      exact u_two hc0 hB hAB
  exact Nat.le_induction (m := 1) hbase (fun n hn ih => step_monotone hc0 hB hAB hn ih) j hj

lemma u_nonneg (hc0 : 0 < c0)
    (hB : ∀ m : Nat, 2 ≤ m → 0 ≤ B m)
    (hAB : ∀ m : Nat, 2 ≤ m → c0 ≤ A m - B m)
    {j : Nat} (hj : 1 ≤ j) : 0 ≤ u c0 A B j :=
  (monotone_pos hc0 hB hAB j hj).1.le

lemma key_growth (hc0 : 0 < c0)
    (hB : ∀ m : Nat, 2 ≤ m → 0 ≤ B m)
    (hAB : ∀ m : Nat, 2 ≤ m → c0 ≤ A m - B m)
    {j : Nat} (hj : 2 ≤ j) :
    (A j - B j) / c0 * u c0 A B (j - 1) ≤ u c0 A B j := by
  have hrec : c0 * u c0 A B j = A j * u c0 A B (j - 1) - B j * u c0 A B (j - 2) :=
    u_recurrence' (ne_of_gt hc0) hj
  have hB' : 0 ≤ B j := hB j hj
  have hu_prev : u c0 A B (j - 2) ≤ u c0 A B (j - 1) := by
    by_cases h3 : 3 ≤ j
    · have hmp := (monotone_pos hc0 hB hAB (j - 2) (by omega)).2
      have hm : (j - 2) + 1 = j - 1 := by omega
      simpa [hm] using hmp
    · have hj2 : j = 2 := by omega
      subst j
      simp [u]
  have hBmul : B j * u c0 A B (j - 2) ≤ B j * u c0 A B (j - 1) :=
    mul_le_mul_of_nonneg_left hu_prev hB'
  have hmain : (A j - B j) * u c0 A B (j - 1) ≤
      A j * u c0 A B (j - 1) - B j * u c0 A B (j - 2) := by
    calc
      (A j - B j) * u c0 A B (j - 1)
          = A j * u c0 A B (j - 1) - B j * u c0 A B (j - 1) := by ring
      _ ≤ A j * u c0 A B (j - 1) - B j * u c0 A B (j - 2) := by nlinarith [hBmul]
  have hgoal : (A j - B j) * u c0 A B (j - 1) ≤ c0 * u c0 A B j := by
    rw [hrec]
    exact hmain
  rw [div_mul_eq_mul_div₀]
  exact (div_le_iff₀ hc0).mpr (by simpa [mul_comm] using hgoal)

theorem product_growth (hc0 : 0 < c0)
    (hB : forall m : Nat, 2 ≤ m → 0 ≤ B m)
    (hAB : forall m : Nat, 2 ≤ m → c0 ≤ A m - B m) :
    forall j : Nat, 1 ≤ j → (∏ k ∈ Finset.Icc 2 j, (A k - B k) / c0) ≤ u c0 A B j := by
  intro j hj
  have hbase : (∏ k ∈ Finset.Icc 2 1, (A k - B k) / c0) ≤ u c0 A B 1 := by
    simp [u]
  refine Nat.le_induction (m := 1) hbase ?hstep j hj
  intro n hn ih
  have hkey : (A (n + 1) - B (n + 1)) / c0 * u c0 A B n ≤ u c0 A B (n + 1) := by
    have h := key_growth hc0 hB hAB (by omega : 2 ≤ n + 1)
    simpa [Nat.add_sub_cancel] using h
  have hnonneg : 0 ≤ (A (n + 1) - B (n + 1)) / c0 := by
    exact div_nonneg (by nlinarith [hAB (n + 1) (by omega)]) (le_of_lt hc0)
  have hmul : (∏ k ∈ Finset.Icc 2 n, (A k - B k) / c0) * ((A (n + 1) - B (n + 1)) / c0)
      ≤ u c0 A B n * ((A (n + 1) - B (n + 1)) / c0) := by
    exact mul_le_mul_of_nonneg_right ih hnonneg
  have hkey' : u c0 A B n * ((A (n + 1) - B (n + 1)) / c0) ≤ u c0 A B (n + 1) := by
    simpa [mul_comm] using hkey
  have hprod : (∏ k ∈ Finset.Icc 2 (n + 1), (A k - B k) / c0) =
      (∏ k ∈ Finset.Icc 2 n, (A k - B k) / c0) * ((A (n + 1) - B (n + 1)) / c0) := by
    rw [Finset.prod_Icc_succ_top (by omega : 2 ≤ n + 1)]
  rw [hprod]
  exact le_trans hmul hkey'

noncomputable def eps (c0 : K) (A B : Nat → K) (k : Nat) : K :=
  (A k - B k - c0) / c0

omit [LinearOrder K] [IsStrictOrderedRing K] in
lemma one_add_eps (hc0 : c0 ≠ 0) {k : Nat} : 1 + eps c0 A B k = (A k - B k) / c0 := by
  unfold eps
  field_simp [hc0]
  ring

lemma eps_nonneg (hc0 : 0 < c0) {k : Nat} (hAB : c0 ≤ A k - B k) : 0 ≤ eps c0 A B k := by
  unfold eps
  exact div_nonneg (by nlinarith) (le_of_lt hc0)

theorem product_growth_eps (hc0 : 0 < c0)
    (hB : forall m : Nat, 2 ≤ m → 0 ≤ B m)
    (hAB : forall m : Nat, 2 ≤ m → c0 ≤ A m - B m) :
    forall j : Nat, 1 ≤ j → (∏ k ∈ Finset.Icc 2 j, (1 + eps c0 A B k)) ≤ u c0 A B j := by
  intro j hj
  have h := product_growth hc0 hB hAB j hj
  have hcongr : (∏ k ∈ Finset.Icc 2 j, (1 + eps c0 A B k)) =
      (∏ k ∈ Finset.Icc 2 j, (A k - B k) / c0) := by
    refine Finset.prod_congr rfl ?_
    intro k hk
    exact one_add_eps (ne_of_gt hc0)
  rwa [hcongr]

end StabilityGrowth

end SL
