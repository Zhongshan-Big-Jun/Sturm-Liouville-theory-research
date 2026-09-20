import Mathlib
import SL.ThirdOrder

/-!
# Third-order recurrence: variation of constants and the third solution

Formalization of Theorem 5 (variation constant sum formula) and the
converse direction of Theorem 3 of `docs/SL_third_order_recurrence_theory.tex`.

Notation of the source: with a solution `E` of the third-order recurrence
(2) and the derived second-order recurrence (4)

  s_j = A_j * s_{j-1} + B_j * s_{j-2}   (j >= 3),
  A_j = -(a2_j * E_{j-2} + a3_j * E_{j-3}) / E_j,
  B_j = -a3_j * E_{j-3} / E_j,

the discrete variation weights are w_2 = 1 and
w_j = -B_j * s_{j-2} / s_j * w_{j-1} (j >= 3); the second independent
solution is sInd_j = s_j * (Σ_{k=2..j} w_k), and
zInd_j = E_j * (r_1 + Σ_{k=2..j} sInd_k) solves (2).

Content:
* `IsSolution2`: the second-order recurrence (4), written at index n+3.
* `Acoef`/`Bcoef`: the named coefficients of (4).
* `W`, `sumW`, `sInd`: the weights, their partial sums and `sInd`.
* `variation_constant_solution`: `sInd` solves (4) whenever `s` does.
* `casoratian`, `casoratian_sInd`, `casoratian_prop`: the discrete
  Wronskian of `s` and `sInd` and its propagation `C_j = -B_j * C_{j-1}`.
* `lin_indep_sInd`: `s` and `sInd` are linearly independent when the
  Casoratian at (2, 3) is nonzero.
* `withInitial`, `reduction_converse`: the converse of Theorem 3
  (`z_j = E_j * (r_1 + Σ_{k=2..j} s_k)` solves (2) for any `s` solving (4)).
* `zInd_solution`: Theorem 5, last part - the `z^ind` construction.

Honesty note: the *linear independence of the three solutions*
`{E^+, E^-, z^ind}` (nonzero 3x3 Casoratian) is numerical in the source
(even -0.0117, odd -0.1758, c=3, j=3) and is NOT formalized here.  The
minimal-solution existence and asymptotics (Theorem 6 of the source) and
the constant table K(c) are numerical evidence in the source and are NOT
formalized.  Subtlety of the source's converse of Theorem 3: with the
convention r_0 = r_1 (empty sum), the constructed z solves (2) only when
s_1 = 0; here `withInitial` keeps r_0 = r_1 - s_1, which makes the
converse hold for every solution s of (4).  For `sInd` one has
sInd_0 = sInd_1 = 0, so the two conventions agree in the `z^ind`
construction.
-/

namespace SL

namespace ThirdOrderMinimal

open ThirdOrder
variable {K : Type*} [Field K]

/-- A sequence `s` solves the second-order recurrence
`s_j = A_j * s_{j-1} + B_j * s_{j-2}` for j >= 3, written at index n+3
to avoid truncated subtraction. -/
def IsSolution2 (A B : ℕ → K) (s : ℕ → K) : Prop :=
  ∀ n : ℕ, s (n + 3) = A (n + 3) * s (n + 2) + B (n + 3) * s (n + 1)

/-- The coefficient `A_j = -(a2_j * E_{j-2} + a3_j * E_{j-3}) / E_j`
of the reduced second-order recurrence (4). -/
def Acoef (a2 a3 : ℕ → K) (E : ℕ → K) (j : ℕ) : K :=
  -(a2 j * E (j - 2) + a3 j * E (j - 3)) / E j

/-- The coefficient `B_j = -a3_j * E_{j-3} / E_j`
of the reduced second-order recurrence (4). -/
def Bcoef (a3 : ℕ → K) (E : ℕ → K) (j : ℕ) : K :=
  -(a3 j * E (j - 3)) / E j

/-- The discrete variation weights `w_j`: `w_2 = 1` and
`w_j = -B_j * s_{j-2} / s_j * w_{j-1}` for j >= 3
(written at index n+3; w_0 = w_1 = 0). -/
def W (B s : ℕ → K) : ℕ → K
  | 0 => 0
  | 1 => 0
  | 2 => 1
  | n + 3 => -(B (n + 3) * s (n + 1)) / s (n + 3) * W B s (n + 2)

/-- The partial sums `Σ_{k=0..j} w_k`; since `w_0 = w_1 = 0` this is
the source's `Σ_{k=2..j} w_k`. -/
def sumW (B s : ℕ → K) (j : ℕ) : K :=
  ∑ k ∈ Finset.range (j + 1), W B s k

/-- The second independent solution `sInd_j = s_j * (Σ_{k=2..j} w_k)`
of Theorem 5. -/
def sInd (B s : ℕ → K) (j : ℕ) : K :=
  s j * sumW B s j

/-- The discrete Wronskian (Casoratian) of two sequences at index j. -/
def casoratian (u v : ℕ → K) (j : ℕ) : K :=
  u j * v (j - 1) - u (j - 1) * v j

/-- `withInitial r1 s j = r_1 + Σ_{k=2..j} s_k`, written via the full
prefix sum so that the telescoping identity `r_{j+1} = r_j + s_{j+1}`
holds at every index (this keeps r_0 = r_1 - s_1). -/
def withInitial (r1 : K) (s : ℕ → K) (j : ℕ) : K :=
  r1 + (∑ k ∈ Finset.range (j + 1), s k) - s 0 - s 1

lemma W_zero (B s : ℕ → K) : W B s 0 = 0 := by
  rfl

lemma W_one (B s : ℕ → K) : W B s 1 = 0 := by
  rfl

lemma W_two (B s : ℕ → K) : W B s 2 = 1 := by
  rfl

lemma sumW_succ (B s : ℕ → K) (j : ℕ) :
    sumW B s (j + 1) = sumW B s j + W B s (j + 1) := by
  unfold sumW
  rw [Finset.sum_range_succ]

lemma sumW_zero (B s : ℕ → K) : sumW B s 0 = 0 := by
  unfold sumW
  rw [Finset.sum_range_succ]
  simp [W]

lemma sumW_two (B s : ℕ → K) : sumW B s 2 = 1 := by
  unfold sumW
  rw [Finset.sum_range_succ, Finset.sum_range_succ, Finset.sum_range_succ]
  simp [W]

/-- The weight identity `s_j * w_j = -B_j * s_{j-2} * w_{j-1}` for j >= 3
(the product form of the defining recursion, valid when `s_j != 0`). -/
lemma W_mul {B s : ℕ → K} {n : ℕ} (h : s (n + 3) ≠ 0) :
    s (n + 3) * W B s (n + 3) = -(B (n + 3) * s (n + 1)) * W B s (n + 2) := by
  simp [W]
  field_simp [h]

lemma sumW_one (B s : ℕ → K) : sumW B s 1 = 0 := by
  unfold sumW
  rw [Finset.sum_range_succ, Finset.sum_range_succ]
  simp [W]

lemma sumW_three (B s : ℕ → K) : sumW B s 3 = 1 + W B s 3 := by
  unfold sumW
  rw [Finset.sum_range_succ, Finset.sum_range_succ, Finset.sum_range_succ,
    Finset.sum_range_succ]
  simp [W]
/-- Theorem 5 (variation of constants): if `s` solves (4) then
`sInd_j = s_j * (Σ_{k=2..j} w_k)` solves (4) as well. -/
theorem variation_constant_solution {A B : ℕ → K} {s : ℕ → K}
    (hs : IsSolution2 A B s) (hsnz : ∀ j : ℕ, s j ≠ 0) :
    IsSolution2 A B (sInd B s) := by
  intro n
  unfold sInd
  have h1 : s (n + 3) ≠ 0 := hsnz (n + 3)
  have hsum : sumW B s (n + 3) = sumW B s (n + 2) + W B s (n + 3) := by
    simpa using sumW_succ B s (n + 2)
  have hsum' : sumW B s (n + 2) = sumW B s (n + 1) + W B s (n + 2) := by
    simpa using sumW_succ B s (n + 1)
  have hsub : sumW B s (n + 2) - W B s (n + 2) = sumW B s (n + 1) := by
    rw [hsum']
    ring
  have hw : s (n + 3) * W B s (n + 3) = -(B (n + 3) * s (n + 1)) * W B s (n + 2) := by
    exact W_mul h1
  have hs3 := hs n
  calc
    s (n + 3) * sumW B s (n + 3)
        = s (n + 3) * (sumW B s (n + 2) + W B s (n + 3)) := by rw [hsum]
    _ = s (n + 3) * sumW B s (n + 2) + s (n + 3) * W B s (n + 3) := by ring
    _ = s (n + 3) * sumW B s (n + 2) + (-(B (n + 3) * s (n + 1))) * W B s (n + 2) := by
        rw [hw]
    _ = (A (n + 3) * s (n + 2) + B (n + 3) * s (n + 1)) * sumW B s (n + 2)
        + (-(B (n + 3) * s (n + 1))) * W B s (n + 2) := by rw [hs3]
    _ = A (n + 3) * (s (n + 2) * sumW B s (n + 2))
        + B (n + 3) * (s (n + 1) * (sumW B s (n + 2) - W B s (n + 2))) := by ring
    _ = A (n + 3) * (s (n + 2) * sumW B s (n + 2))
        + B (n + 3) * (s (n + 1) * sumW B s (n + 1)) := by rw [hsub]

/-- Closed form of the Casoratian of `s` and `sInd` at index n+1:
`C_{n+1} = -s_{n+1} * s_n * w_{n+1}`. -/
lemma casoratian_sInd {B s : ℕ → K} (n : ℕ) :
    casoratian s (sInd B s) (n + 1) = -(s (n + 1) * s n * W B s (n + 1)) := by
  unfold casoratian sInd
  have hsub : (n + 1) - 1 = n := by omega
  rw [hsub]
  rw [sumW_succ B s n]
  ring

/-- Propagation of the Casoratian: `C_j = -B_j * C_{j-1}` (j >= 3). -/
lemma casoratian_prop {B s : ℕ → K} {n : ℕ} (hs : s (n + 3) ≠ 0) :
    casoratian s (sInd B s) (n + 3) = -B (n + 3) * casoratian s (sInd B s) (n + 2) := by
  calc
    casoratian s (sInd B s) (n + 3)
        = -(s (n + 3) * s (n + 2) * W B s (n + 3)) := by
            simpa using casoratian_sInd (B := B) (s := s) (n + 2)
    _ = -((s (n + 3) * W B s (n + 3)) * s (n + 2)) := by ring
    _ = -((-(B (n + 3) * s (n + 1)) * W B s (n + 2)) * s (n + 2)) := by rw [W_mul hs]
    _ = -B (n + 3) * (-(s (n + 2) * s (n + 1) * W B s (n + 2))) := by ring
    _ = -B (n + 3) * casoratian s (sInd B s) (n + 2) := by
        rw [← casoratian_sInd (B := B) (s := s) (n + 1)]

/-- `s` and `sInd` are linearly independent when the Casoratian at
(2, 3) is nonzero, i.e. `s_2 * s_3 * w_3 != 0`. -/
theorem lin_indep_sInd {B s : ℕ → K}
    (h23 : s 2 * s 3 * W B s 3 ≠ 0) :
    ∀ a b : K, (∀ j : ℕ, a * s j + b * sInd B s j = 0) → a = 0 ∧ b = 0 := by
  intro a b h
  have h2 := h 2
  have h3 := h 3
  have hs23 : s 2 * s 3 ≠ 0 := (mul_ne_zero_iff.mp h23).1
  have hW3 : W B s 3 ≠ 0 := (mul_ne_zero_iff.mp h23).2
  have hs2 : s 2 ≠ 0 := (mul_ne_zero_iff.mp hs23).1
  have hs3 : s 3 ≠ 0 := (mul_ne_zero_iff.mp hs23).2
  have hsInd2 : sInd B s 2 = s 2 := by
    unfold sInd
    rw [sumW_two]
    ring
  have hsInd3 : sInd B s 3 = s 3 * (1 + W B s 3) := by
    unfold sInd
    rw [sumW_three]
  rw [hsInd2] at h2
  rw [hsInd3] at h3
  have hab : a + b = 0 := by
    have h2' : (a + b) * s 2 = 0 := by
      calc
        (a + b) * s 2 = a * s 2 + b * s 2 := by ring
        _ = 0 := h2
    exact Or.resolve_right (mul_eq_zero.mp h2') hs2
  have hab3 : a + b * (1 + W B s 3) = 0 := by
    have h3' : (a + b * (1 + W B s 3)) * s 3 = 0 := by
      calc
        (a + b * (1 + W B s 3)) * s 3 = a * s 3 + b * (s 3 * (1 + W B s 3)) := by ring
        _ = 0 := h3
    exact Or.resolve_right (mul_eq_zero.mp h3') hs3
  have hb3 : W B s 3 * b = 0 := by
    have hdiff : (a + b * (1 + W B s 3)) - (a + b) = 0 := by
      rw [hab3, hab]
      ring
    calc
      W B s 3 * b = (a + b * (1 + W B s 3)) - (a + b) := by ring
      _ = 0 := hdiff
  have hb : b = 0 := by
    rw [mul_comm] at hb3
    rcases mul_eq_zero.mp hb3 with hb | hw0
    · exact hb
    · exact False.elim (hW3 hw0)
  have ha : a = 0 := by
    rw [hb] at hab
    simpa using hab
  exact ⟨ha, hb⟩

lemma withInitial_succ (r1 : K) (s : ℕ → K) (j : ℕ) :
    withInitial r1 s (j + 1) = withInitial r1 s j + s (j + 1) := by
  unfold withInitial
  rw [Finset.sum_range_succ]
  ring

/-- For sequences with `s_0 = s_1 = 0` (in particular `sInd`), the
`withInitial` sum agrees with the source's `r_1 + Σ_{k=2..j} s_k`. -/
lemma withInitial_eq_source {r1 : K} {s : ℕ → K} (h0 : s 0 = 0) (h1 : s 1 = 0) (j : ℕ) :
    withInitial r1 s j = r1 + ∑ k ∈ Finset.range (j + 1), s k := by
  unfold withInitial
  rw [h0, h1]
  ring

lemma sInd_zero (B s : ℕ → K) : sInd B s 0 = 0 := by
  unfold sInd
  rw [sumW_zero]
  ring

lemma sInd_one (B s : ℕ → K) : sInd B s 1 = 0 := by
  unfold sInd
  rw [sumW_one]
  ring

/-- Theorem 3 (forward direction) with the named coefficients: the
difference sequence `s_j = z_j/E_j - z_{j-1}/E_{j-1}` of any solution
`z` of (2) solves the second-order recurrence (4). -/
theorem reduction_named {a1 a2 a3 : ℕ → K} {E z : ℕ → K}
    (hE : IsSolution a1 a2 a3 E) (hEnz : ∀ j : ℕ, E j ≠ 0)
    (hz : IsSolution a1 a2 a3 z) :
    IsSolution2 (Acoef a2 a3 E) (Bcoef a3 E)
      (fun j : ℕ => z j / E j - z (j - 1) / E (j - 1)) := by
  intro n
  have h := ThirdOrder.reduction hE hEnz hz n
  dsimp at h
  change z (n + 3) / E (n + 3) - z (n + 2) / E (n + 2) =
      Acoef a2 a3 E (n + 3) * (z (n + 2) / E (n + 2) - z (n + 1) / E (n + 1))
        + Bcoef a3 E (n + 3) * (z (n + 1) / E (n + 1) - z n / E n)
  rw [show Acoef a2 a3 E (n + 3) =
        -(a2 (n + 3) * E (n + 1) + a3 (n + 3) * E n) / E (n + 3) by rfl,
    show Bcoef a3 E (n + 3) = -(a3 (n + 3) * E n) / E (n + 3) by rfl]
  exact h

/-- Theorem 3 (converse direction): any solution `s` of (4) gives a
solution `z_j = E_j * (r_1 + Σ_{k=2..j} s_k)` of (2). -/
theorem reduction_converse {a1 a2 a3 : ℕ → K} {E : ℕ → K}
    (hE : IsSolution a1 a2 a3 E) (hEnz : ∀ j : ℕ, E j ≠ 0)
    {s : ℕ → K} (hs : IsSolution2 (Acoef a2 a3 E) (Bcoef a3 E) s)
    (r1 : K) :
    IsSolution a1 a2 a3 (fun j : ℕ => E j * withInitial r1 s j) := by
  intro n
  have hA : E (n + 3) * Acoef a2 a3 E (n + 3) =
      -(a2 (n + 3) * E (n + 1) + a3 (n + 3) * E n) := by
    unfold Acoef
    have h2 : (n + 3) - 2 = n + 1 := by omega
    have h3 : (n + 3) - 3 = n := by omega
    rw [h2, h3]
    field_simp [hEnz (n + 3)]
  have hB : E (n + 3) * Bcoef a3 E (n + 3) = -(a3 (n + 3) * E n) := by
    unfold Bcoef
    have h3 : (n + 3) - 3 = n := by omega
    rw [h3]
    field_simp [hEnz (n + 3)]
  have hEAs2 : E (n + 3) * (Acoef a2 a3 E (n + 3) * s (n + 2)) =
      (-(a2 (n + 3) * E (n + 1) + a3 (n + 3) * E n)) * s (n + 2) := by
    calc
      E (n + 3) * (Acoef a2 a3 E (n + 3) * s (n + 2))
          = (E (n + 3) * Acoef a2 a3 E (n + 3)) * s (n + 2) := by ring
      _ = (-(a2 (n + 3) * E (n + 1) + a3 (n + 3) * E n)) * s (n + 2) := by rw [hA]
  have hEBs1 : E (n + 3) * (Bcoef a3 E (n + 3) * s (n + 1)) =
      (-(a3 (n + 3) * E n)) * s (n + 1) := by
    calc
      E (n + 3) * (Bcoef a3 E (n + 3) * s (n + 1))
          = (E (n + 3) * Bcoef a3 E (n + 3)) * s (n + 1) := by ring
      _ = (-(a3 (n + 3) * E n)) * s (n + 1) := by rw [hB]
  have hsucc3 : withInitial r1 s (n + 3) = withInitial r1 s (n + 2) + s (n + 3) := by
    simpa using withInitial_succ r1 s (n + 2)
  have hsucc2 : withInitial r1 s (n + 2) = withInitial r1 s (n + 1) + s (n + 2) := by
    simpa using withInitial_succ r1 s (n + 1)
  have hsucc1 : withInitial r1 s (n + 1) = withInitial r1 s n + s (n + 1) := by
    simpa using withInitial_succ r1 s n
  have hsub2 : withInitial r1 s (n + 2) - s (n + 2) = withInitial r1 s (n + 1) := by
    rw [hsucc2]
    ring
  have hsub1 : withInitial r1 s (n + 2) - s (n + 2) - s (n + 1) = withInitial r1 s n := by
    rw [hsucc2, hsucc1]
    ring
  calc
    E (n + 3) * withInitial r1 s (n + 3)
        = E (n + 3) * (withInitial r1 s (n + 2) + s (n + 3)) := by rw [hsucc3]
    _ = E (n + 3) * withInitial r1 s (n + 2) + E (n + 3) * s (n + 3) := by ring
    _ = (a1 (n + 3) * E (n + 2) + a2 (n + 3) * E (n + 1) + a3 (n + 3) * E n)
          * withInitial r1 s (n + 2) + E (n + 3) * s (n + 3) := by rw [hE n]
    _ = (a1 (n + 3) * E (n + 2) + a2 (n + 3) * E (n + 1) + a3 (n + 3) * E n)
          * withInitial r1 s (n + 2)
        + E (n + 3) * (Acoef a2 a3 E (n + 3) * s (n + 2) + Bcoef a3 E (n + 3) * s (n + 1)) := by
            rw [hs n]
    _ = a1 (n + 3) * (E (n + 2) * withInitial r1 s (n + 2))
        + a2 (n + 3) * (E (n + 1) * withInitial r1 s (n + 2))
        + a3 (n + 3) * (E n * withInitial r1 s (n + 2))
        + E (n + 3) * (Acoef a2 a3 E (n + 3) * s (n + 2))
        + E (n + 3) * (Bcoef a3 E (n + 3) * s (n + 1)) := by ring
    _ = a1 (n + 3) * (E (n + 2) * withInitial r1 s (n + 2))
        + a2 (n + 3) * (E (n + 1) * withInitial r1 s (n + 2))
        + a3 (n + 3) * (E n * withInitial r1 s (n + 2))
        + (-(a2 (n + 3) * E (n + 1) + a3 (n + 3) * E n)) * s (n + 2)
        + (-(a3 (n + 3) * E n)) * s (n + 1) := by rw [hEAs2, hEBs1]
    _ = a1 (n + 3) * (E (n + 2) * withInitial r1 s (n + 2))
        + a2 (n + 3) * (E (n + 1) * (withInitial r1 s (n + 2) - s (n + 2)))
        + a3 (n + 3) * (E n * (withInitial r1 s (n + 2) - s (n + 2) - s (n + 1))) := by ring
    _ = a1 (n + 3) * (E (n + 2) * withInitial r1 s (n + 2))
        + a2 (n + 3) * (E (n + 1) * withInitial r1 s (n + 1))
        + a3 (n + 3) * (E n * withInitial r1 s n) := by
            rw [hsub1, hsub2]

/-- Theorem 5 (last part): with `sInd` from the variation of constants,
`zInd_j = E_j * (r_1 + Σ_{k=2..j} sInd_k)` solves the third-order
recurrence (2).  This is the source's `z^ind` construction (`sInd` has
sInd_0 = sInd_1 = 0, so `withInitial` matches the source convention). -/
theorem zInd_solution {a1 a2 a3 : ℕ → K} {E : ℕ → K}
    (hE : IsSolution a1 a2 a3 E) (hEnz : ∀ j : ℕ, E j ≠ 0)
    {s : ℕ → K} (hs : IsSolution2 (Acoef a2 a3 E) (Bcoef a3 E) s)
    (hsnz : ∀ j : ℕ, s j ≠ 0) (r1 : K) :
    IsSolution a1 a2 a3 (fun j : ℕ => E j * withInitial r1 (sInd (Bcoef a3 E) s) j) := by
  exact reduction_converse hE hEnz (variation_constant_solution hs hsnz) r1

end ThirdOrderMinimal

end SL
