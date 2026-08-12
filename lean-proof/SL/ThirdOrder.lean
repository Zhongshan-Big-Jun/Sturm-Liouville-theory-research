import Mathlib
import SL.Basic

/-!
# Third-order moment recurrence theory

Formalization of the algebraic core of `docs/SL_third_order_recurrence_theory.tex`
(Sections 2-4): the general third-order recurrence framework, the
fixed-point/product equivalence (Lemma 1), and the exact reduction to a
second-order recurrence (Theorem 3, forward direction).

The concrete even/odd closed-form verification (Theorem 2) lives in
`SL/ThirdOrderClosedForms.lean`.

Honesty note: the classification theorem of the source (Theorem 1, beta in
{1,-1} / {3,1}) relies on symbolic computation in the source document and is
NOT formalized here; the sufficiency direction (the closed forms solve the
recurrence) is a direct algebraic verification.
-/

namespace SL

namespace ThirdOrder

variable {K : Type*} [Field K]

/-- A sequence `z` solves the third-order recurrence
`z_j = a1_j * z_{j-1} + a2_j * z_{j-2} + a3_j * z_{j-3}` for j >= 3,
written at index n+3 to avoid truncated subtraction. -/
def IsSolution (a1 a2 a3 : ℕ → K) (z : ℕ → K) : Prop :=
  ∀ n : ℕ, z (n + 3) = a1 (n + 3) * z (n + 2) + a2 (n + 3) * z (n + 1) + a3 (n + 3) * z n

/-- The ratio map F_j(x,y) = a1_j + a2_j/x + a3_j/(x*y). -/
def ratioMap (a1 a2 a3 : ℕ → K) (j : ℕ) (x y : K) : K :=
  a1 j + a2 j / x + a3 j / (x * y)

/-- Lemma 1 of the source: a sequence E with nonzero terms solves the
recurrence iff its successive ratios e_j = E_j/E_{j-1} satisfy the
fixed-point equation e_j = F_j(e_{j-1}, e_{j-2}) for j >= 3. -/
theorem fixed_point_iff {a1 a2 a3 : ℕ → K} {E : ℕ → K}
    (hEnz : ∀ j : ℕ, E j ≠ 0) :
    IsSolution a1 a2 a3 E ↔
      ∀ n : ℕ, E (n + 3) / E (n + 2) =
        ratioMap a1 a2 a3 (n + 3) (E (n + 2) / E (n + 1)) (E (n + 1) / E n) := by
  constructor
  · intro hE n
    have h1 : E (n + 3) ≠ 0 := hEnz (n + 3)
    have h2 : E (n + 2) ≠ 0 := hEnz (n + 2)
    have h3 : E (n + 1) ≠ 0 := hEnz (n + 1)
    have h4 : E n ≠ 0 := hEnz n
    calc
      E (n + 3) / E (n + 2)
          = (a1 (n + 3) * E (n + 2) + a2 (n + 3) * E (n + 1) + a3 (n + 3) * E n) / E (n + 2) := by
              rw [hE n]
      _ = a1 (n + 3) + a2 (n + 3) * E (n + 1) / E (n + 2) + a3 (n + 3) * E n / E (n + 2) := by
              field_simp [h1, h2]
      _ = ratioMap a1 a2 a3 (n + 3) (E (n + 2) / E (n + 1)) (E (n + 1) / E n) := by
              unfold ratioMap
              field_simp [h1, h2, h3, h4]
  · intro hfp n
    have h1 : E (n + 3) ≠ 0 := hEnz (n + 3)
    have h2 : E (n + 2) ≠ 0 := hEnz (n + 2)
    have h3 : E (n + 1) ≠ 0 := hEnz (n + 1)
    have h4 : E n ≠ 0 := hEnz n
    have h := hfp n
    calc
      E (n + 3)
          = (E (n + 3) / E (n + 2)) * E (n + 2) := by
              field_simp [h2]
      _ = ratioMap a1 a2 a3 (n + 3) (E (n + 2) / E (n + 1)) (E (n + 1) / E n) * E (n + 2) := by
              rw [h]
      _ = a1 (n + 3) * E (n + 2) + a2 (n + 3) * E (n + 1) + a3 (n + 3) * E n := by
              unfold ratioMap
              field_simp [h1, h2, h3, h4]

/-- Theorem 3 (forward direction) of the source: with r_j = z_j/E_j and
s_j = r_j - r_{j-1}, the difference sequence s solves the second-order
recurrence s_j = A_j s_{j-1} + B_j s_{j-2} with
A_j = -(a2_j E_{j-2} + a3_j E_{j-3})/E_j and B_j = -a3_j E_{j-3}/E_j. -/
theorem reduction {a1 a2 a3 : ℕ → K} {E z : ℕ → K}
    (hE : IsSolution a1 a2 a3 E) (hEnz : ∀ j : ℕ, E j ≠ 0)
    (hz : IsSolution a1 a2 a3 z) :
    ∀ n : ℕ,
      let r : ℕ → K := fun j => z j / E j
      let s : ℕ → K := fun j => r j - r (j - 1)
      s (n + 3) =
        -(a2 (n + 3) * E (n + 1) + a3 (n + 3) * E n) / E (n + 3) * s (n + 2)
          + -(a3 (n + 3) * E n) / E (n + 3) * s (n + 1) := by
  intro n
  have h1 : E (n + 3) ≠ 0 := hEnz (n + 3)
  have h2 : E (n + 2) ≠ 0 := hEnz (n + 2)
  have h3 : E (n + 1) ≠ 0 := hEnz (n + 1)
  have h4 : E n ≠ 0 := hEnz n
  dsimp
  rw [hz n]
  field_simp [h1, h2, h3, h4]
  rw [hE n]
  ring

end ThirdOrder

end SL
