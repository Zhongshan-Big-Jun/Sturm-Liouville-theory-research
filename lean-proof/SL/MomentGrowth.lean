import Mathlib

/-!
# Moment-jump growth lemma

Formalization of the "growth lemma" (增长引理) from
`docs/SL_h2_completeness_proof.tex` (completeness of the polynomial family in
the second left-definite space H^2[-1,1] via the moment-jump method).

Statement: for c > 0, let u : Nat -> Real be defined by
  u 0 = 0,  u 1 = 1,
  c * u j = A_j * u (j-1) - B_j * u (j-2)   (j >= 2),
with A_j = 2j(2j-1) + c*j/(j-1) and B_j = 2j(2j-3).
Then for every j >= 1:
  u j > 0,  u j <= u (j+1),  and  u j >= (4/c)^(j-1) * j!.
-/

namespace SL

namespace MomentGrowth

variable {c : Real}

noncomputable def A (c : Real) (j : Nat) : Real :=
  2 * (j : Real) * (2 * (j : Real) - 1) + c * (j : Real) / ((j : Real) - 1)

noncomputable def B (j : Nat) : Real :=
  2 * (j : Real) * (2 * (j : Real) - 3)

noncomputable def u (c : Real) : Nat -> Real
  | 0 => 0
  | 1 => 1
  | Nat.succ (Nat.succ n) =>
      (A c (n + 2) * u c (n + 1) - B (n + 2) * u c n) / c

lemma denom_pos {j : Nat} (hj : 2 <= j) : 0 < (j : Real) - 1 := by
  have h2 : (2 : Real) <= (j : Real) := by exact_mod_cast hj
  nlinarith

lemma A_sub_B (j : Nat) :
    A c j - B j = 4 * (j : Real) + c * (j : Real) / ((j : Real) - 1) := by
  unfold A B
  ring_nf

lemma B_nonneg {j : Nat} (hj : 2 <= j) : 0 <= B j := by
  unfold B
  have h2 : (2 : Real) <= (j : Real) := by exact_mod_cast hj
  have h : 0 <= 2 * (j : Real) - 3 := by nlinarith
  exact mul_nonneg (by positivity) h

lemma A_sub_B_ge_four {j : Nat} (hj : 2 <= j) (hc : 0 <= c) :
    4 * (j : Real) <= A c j - B j := by
  rw [A_sub_B]
  have hterm : 0 <= c * (j : Real) / ((j : Real) - 1) := by
    exact div_nonneg (mul_nonneg hc (Nat.cast_nonneg j)) (le_of_lt (denom_pos hj))
  exact le_add_of_nonneg_right hterm

lemma A_sub_B_ge_c {j : Nat} (hj : 2 <= j) (hc : 0 < c) :
    c <= A c j - B j := by
  rw [A_sub_B]
  have hden : 0 < (j : Real) - 1 := denom_pos hj
  have h1 : c <= c * (j : Real) / ((j : Real) - 1) := by
    have hden' := ne_of_gt hden
    field_simp [hden']
    nlinarith [hc]
  have hfour : 0 <= 4 * (j : Real) := by positivity
  exact le_trans h1 (le_add_of_nonneg_left hfour)

lemma u_recurrence (hc : 0 < c) {j : Nat} :
    c * u c (j + 2) = A c (j + 2) * u c (j + 1) - B (j + 2) * u c j := by
  simp [u]
  field_simp [ne_of_gt hc]

lemma u_recurrence' (hc : 0 < c) {j : Nat} (hj : 2 <= j) :
    c * u c j = A c j * u c (j - 1) - B j * u c (j - 2) := by
  have h := u_recurrence (j := j - 2) hc
  have h1 : j - 2 + 2 = j := by omega
  have h2 : j - 2 + 1 = j - 1 := by omega
  simpa [h1, h2] using h

lemma u_two : u c 2 = (12 + 2 * c) / c := by
  simp [u, A, B]
  ring_nf

lemma step_monotone (hc : 0 < c) {j : Nat} (hj : 1 <= j)
    (hprev : 0 < u c j /\ u c j <= u c (j + 1)) :
    0 < u c (j + 1) /\ u c (j + 1) <= u c (j + 2) := by
  constructor
  · exact lt_of_lt_of_le hprev.1 hprev.2
  · have hrec : c * u c (j + 2) = A c (j + 2) * u c (j + 1) - B (j + 2) * u c j :=
      u_recurrence hc
    have hB := B_nonneg (j := j + 2) (by omega : 2 <= j + 2)
    have hBmul : B (j + 2) * u c j <= B (j + 2) * u c (j + 1) :=
      mul_le_mul_of_nonneg_left hprev.2 hB
    have hA : c <= A c (j + 2) - B (j + 2) :=
      A_sub_B_ge_c (by omega : 2 <= j + 2) hc
    have h2 : c * u c (j + 1) <= c * u c (j + 2) := by
      rw [hrec]
      calc
        c * u c (j + 1)
            <= (A c (j + 2) - B (j + 2)) * u c (j + 1) := by
                exact mul_le_mul_of_nonneg_right hA
                  (le_of_lt (lt_of_lt_of_le hprev.1 hprev.2))
        _ = A c (j + 2) * u c (j + 1) - B (j + 2) * u c (j + 1) := by ring
        _ <= A c (j + 2) * u c (j + 1) - B (j + 2) * u c j := by
                nlinarith [hBmul]
    nlinarith [h2, hc]

lemma monotone_pos (hc : 0 < c) :
    forall j : Nat, 1 <= j -> 0 < u c j /\ u c j <= u c (j + 1) := by
  intro j hj
  have hbase : 0 < u c 1 /\ u c 1 <= u c 2 := by
    constructor
    · simp [u]
    · rw [u_two]
      simp [u]
      field_simp [ne_of_gt hc]
      nlinarith [hc]
  exact Nat.le_induction (m := 1) hbase (fun n hn ih => step_monotone hc hn ih) j hj

lemma key_growth (hc : 0 < c) {j : Nat} (hj : 2 <= j) :
    4 * (j : Real) / c * u c (j - 1) <= u c j := by
  have hrec : c * u c j = A c j * u c (j - 1) - B j * u c (j - 2) :=
    u_recurrence' hc hj
  have hB : 0 <= B j := B_nonneg (j := j) hj
  have hA : 4 * (j : Real) <= A c j - B j :=
    A_sub_B_ge_four (j := j) hj (le_of_lt hc)
  have hu_prev : u c (j - 2) <= u c (j - 1) := by
    by_cases h3 : 3 <= j
    · have hmp := (monotone_pos hc (j - 2) (by omega)).2
      have hm : (j - 2) + 1 = j - 1 := by omega
      simpa [hm] using hmp
    · have hj2 : j = 2 := by omega
      subst j
      simp [u]
  have hBmul : B j * u c (j - 2) <= B j * u c (j - 1) :=
    mul_le_mul_of_nonneg_left hu_prev hB
  have hmain : 4 * (j : Real) * u c (j - 1) <= A c j * u c (j - 1) - B j * u c (j - 2) := by
    calc
      4 * (j : Real) * u c (j - 1)
          <= (A c j - B j) * u c (j - 1) := by
              exact mul_le_mul_of_nonneg_right hA
                (le_of_lt (monotone_pos hc (j - 1) (by omega)).1)
      _ <= A c j * u c (j - 1) - B j * u c (j - 2) := by
              nlinarith [hBmul]
  have hgoal : 4 * (j : Real) * u c (j - 1) <= c * u c j := by
    rw [hrec]
    exact hmain
  field_simp [ne_of_gt hc]
  simpa [mul_comm] using hgoal

theorem growth (hc : 0 < c) :
    forall j : Nat, 1 <= j ->
      (4 / c) ^ (j - 1) * (Nat.factorial j : Real) <= u c j := by
  intro j hj
  have hbase : (4 / c) ^ (1 - 1) * (Nat.factorial 1 : Real) <= u c 1 := by
    simp [u]
  refine Nat.le_induction (m := 1) hbase ?hstep j hj
  intro n hn ih
  have hkey : 4 * ((n + 1 : Nat) : Real) / c * u c n <= u c (n + 1) := by
    have h := key_growth hc (by omega : 2 <= n + 1)
    simpa [Nat.add_sub_cancel] using h
  have hnonneg : 0 <= 4 * ((n + 1 : Nat) : Real) / c := by positivity
  have hmul : 4 * ((n + 1 : Nat) : Real) / c * ((4 / c) ^ (n - 1) * (Nat.factorial n : Real))
      <= 4 * ((n + 1 : Nat) : Real) / c * u c n := by
    exact mul_le_mul_of_nonneg_left ih hnonneg
  have hfac : (Nat.factorial (n + 1) : Real) =
      ((n + 1 : Nat) : Real) * (Nat.factorial n : Real) := by
    rw [Nat.factorial_succ, Nat.cast_mul]
  have hpow : (4 / c) ^ n = (4 / c) * (4 / c) ^ (n - 1) := by
    have hn' : n = (n - 1) + 1 := (Nat.sub_add_cancel hn).symm
    nth_rewrite 1 [hn']
    rw [pow_succ]
    ring
  calc
    (4 / c) ^ n * (Nat.factorial (n + 1) : Real)
        = (4 / c) ^ n * (((n + 1 : Nat) : Real) * (Nat.factorial n : Real)) := by rw [hfac]
    _ = (4 / c) ^ n * ((n + 1 : Nat) : Real) * (Nat.factorial n : Real) := by ring
    _ = (4 / c) * (4 / c) ^ (n - 1) * ((n + 1 : Nat) : Real) * (Nat.factorial n : Real) := by rw [hpow]
    _ = 4 * ((n + 1 : Nat) : Real) / c * ((4 / c) ^ (n - 1) * (Nat.factorial n : Real)) := by ring
    _ <= u c (n + 1) := by
        exact le_trans hmul hkey

end MomentGrowth

end SL