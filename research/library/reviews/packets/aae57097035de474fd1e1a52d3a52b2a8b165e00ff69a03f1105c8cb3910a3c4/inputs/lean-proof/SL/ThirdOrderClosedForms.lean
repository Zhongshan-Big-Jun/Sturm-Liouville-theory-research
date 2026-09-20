import Mathlib
import SL.ThirdOrder

/-!
# Third-order recurrence: closed-form verification

Formalization of Theorem 2 (closed forms) of
`docs/SL_third_order_recurrence_theory.tex`, plus the fixed-point
trajectory identities of Theorem 1 (sufficiency direction, beta in
{1,-1} for the even family and {3,1} for the odd family) and the ratio
identities `mu⁻/mu⁺`.

The mu-scale recurrence (equation (1) of the source) is

  c^2 * mu_j = P_j * mu_{j-1} - Q_j * mu_{j-2} + R_j * mu_{j-3}   (j >= 3),

with (even family)

  P_j = 8*c*j^2 - 4*c*j + c^2*j/(j-1),
  Q_j = 4*j*(j-1)*(2*j-1)*(2*j-3) + 4*c*j*(2*j-3),
  R_j = 4*j*(j-2)*(2*j-3)*(2*j-5),

and (odd family) the +4*c*j variant with (2*j+1), (2*j-1) in place of
(2*j-3), (2*j-5) respectively.  The closed forms are

  even:  mu_j^+ = (2*j+1)!/c^j,   mu_j^- = (2*j)!/c^j,
  odd:   mu_j^+ = (2*j+3)!/(6*(j+1)*c^j),   mu_j^- = (2*j+1)!/c^j,

all for c != 0.  All statements are over `ℚ` to match the exact rational
coefficient identities; the same algebra holds over Real by change of base.

Honesty note: the *classification* direction of Theorem 1 of the source
(only beta in {1,-1} / {3,1} works) relies on symbolic computation in the
source document and is NOT formalized here; only the sufficiency direction
(the closed forms and the fixed-point trajectories are exact) is
formalized, as a direct algebraic verification.
-/

namespace SL

namespace ThirdOrderClosedForms

/-- `prodFactors n m = ∏ i in 1..m, (2*n+i)` as a natural number. -/
def prodFactors (n : ℕ) : ℕ → ℕ
  | 0 => 1
  | m + 1 => (2 * n + m + 1) * prodFactors n m

@[simp] theorem prodFactors_succ (n m : ℕ) :
    prodFactors n (m + 1) = (2 * n + m + 1) * prodFactors n m := by
  rfl

/-- Shifted factorial cast: `(2*n+m)! = (∏ i in 1..m, (2*n+i)) * (2*n)!`. -/
lemma cast_factorial_shift (n m : ℕ) :
    ((Nat.factorial (2 * n + m) : ℕ) : ℚ) =
      (prodFactors n m : ℚ) * ((Nat.factorial (2 * n) : ℕ) : ℚ) := by
  induction m with
  | zero =>
      simp [prodFactors]
  | succ m ih =>
      rw [show 2 * n + (m + 1) = (2 * n + m) + 1 by ring]
      rw [Nat.factorial_succ]
      rw [prodFactors_succ]
      norm_cast
      norm_cast at ih
      rw [ih]
      ring_nf

-- even family coefficients

noncomputable def PEven (c : ℚ) (j : ℕ) : ℚ :=
  8 * c * (j : ℚ) ^ 2 - 4 * c * (j : ℚ) + c ^ 2 * (j : ℚ) / ((j : ℚ) - 1)

noncomputable def QEven (c : ℚ) (j : ℕ) : ℚ :=
  4 * (j : ℚ) * ((j : ℚ) - 1) * (2 * (j : ℚ) - 1) * (2 * (j : ℚ) - 3) +
    4 * c * (j : ℚ) * (2 * (j : ℚ) - 3)

noncomputable def REven (_c : ℚ) (j : ℕ) : ℚ :=
  4 * (j : ℚ) * ((j : ℚ) - 2) * (2 * (j : ℚ) - 3) * (2 * (j : ℚ) - 5)

-- odd family coefficients

noncomputable def POdd (c : ℚ) (j : ℕ) : ℚ :=
  8 * c * (j : ℚ) ^ 2 + 4 * c * (j : ℚ) + c ^ 2 * (j : ℚ) / ((j : ℚ) - 1)

noncomputable def QOdd (c : ℚ) (j : ℕ) : ℚ :=
  4 * (j : ℚ) * ((j : ℚ) - 1) * (2 * (j : ℚ) - 1) * (2 * (j : ℚ) + 1) +
    4 * c * (j : ℚ) * (2 * (j : ℚ) - 1)

noncomputable def ROdd (_c : ℚ) (j : ℕ) : ℚ :=
  4 * (j : ℚ) * ((j : ℚ) - 2) * (2 * (j : ℚ) - 1) * (2 * (j : ℚ) - 3)

-- closed-form moment sequences

noncomputable def muEvenPlus (c : ℚ) (j : ℕ) : ℚ :=
  ((Nat.factorial (2 * j + 1) : ℕ) : ℚ) / c ^ j

noncomputable def muEvenMinus (c : ℚ) (j : ℕ) : ℚ :=
  ((Nat.factorial (2 * j) : ℕ) : ℚ) / c ^ j

noncomputable def muOddPlus (c : ℚ) (j : ℕ) : ℚ :=
  ((Nat.factorial (2 * j + 3) : ℕ) : ℚ) / (6 * ((j + 1 : ℕ) : ℚ) * c ^ j)

noncomputable def muOddMinus (c : ℚ) (j : ℕ) : ℚ :=
  ((Nat.factorial (2 * j + 1) : ℕ) : ℚ) / c ^ j

/-- Shifted factorial split for the even ratio identity. -/
lemma factorial_shift_7 (n : ℕ) :
    Nat.factorial (2 * n + 7) = (2 * n + 7) * Nat.factorial (2 * n + 6) := by
  rw [show 2 * n + 7 = (2 * n + 6) + 1 by ring, Nat.factorial_succ]

/-- Shifted factorial split for the odd ratio identity. -/
lemma factorial_shift_9 (n : ℕ) :
    Nat.factorial (2 * n + 9) = (2 * n + 9) * (2 * n + 8) * Nat.factorial (2 * n + 7) := by
  rw [show 2 * n + 9 = (2 * n + 8) + 1 by ring, Nat.factorial_succ]
  rw [show 2 * n + 8 = (2 * n + 7) + 1 by ring, Nat.factorial_succ]
  ring

-- z-scale coefficients (lambda = 4/c)

noncomputable def lambda (c : ℚ) : ℚ := 4 / c

noncomputable def a1Even (c : ℚ) (j : ℕ) : ℚ :=
  PEven c j / (c ^ 2 * (j : ℚ) ^ 2 * lambda c)

noncomputable def a2Even (c : ℚ) (j : ℕ) : ℚ :=
  -QEven c j / (c ^ 2 * (j : ℚ) ^ 2 * ((j : ℚ) - 1) ^ 2 * lambda c ^ 2)

noncomputable def a3Even (c : ℚ) (j : ℕ) : ℚ :=
  REven c j / (c ^ 2 * (j : ℚ) ^ 2 * ((j : ℚ) - 1) ^ 2 * ((j : ℚ) - 2) ^ 2 * lambda c ^ 3)

noncomputable def a1Odd (c : ℚ) (j : ℕ) : ℚ :=
  POdd c j / (c ^ 2 * (j : ℚ) ^ 2 * lambda c)

noncomputable def a2Odd (c : ℚ) (j : ℕ) : ℚ :=
  -QOdd c j / (c ^ 2 * (j : ℚ) ^ 2 * ((j : ℚ) - 1) ^ 2 * lambda c ^ 2)

noncomputable def a3Odd (c : ℚ) (j : ℕ) : ℚ :=
  ROdd c j / (c ^ 2 * (j : ℚ) ^ 2 * ((j : ℚ) - 1) ^ 2 * ((j : ℚ) - 2) ^ 2 * lambda c ^ 3)

/-- The ratio sequence `e_j = 1 + beta/(2*j)`. -/
noncomputable def eSeq (β : ℚ) (j : ℕ) : ℚ := 1 + β / (2 * (j : ℚ))

lemma eSeq_ne_zero {β : ℚ} (hβ : β = 1 ∨ β = -1 ∨ β = 3) (j : ℕ) : eSeq β j ≠ 0 := by
  rcases hβ with rfl | rfl | rfl
  · unfold eSeq
    rcases j with _ | _ | j
    · simp
    · norm_num
    · have hb : 0 < 2 * ((j + 2 : ℕ) : ℚ) := by
        exact_mod_cast (show 0 < 2 * (j + 2) by omega)
      have hpos : 0 < 1 + 1 / (2 * ((j + 2 : ℕ) : ℚ)) := by
        positivity
      exact ne_of_gt hpos
  · unfold eSeq
    rcases j with _ | _ | j
    · simp
    · norm_num
    · have hb : 0 < 2 * ((j + 2 : ℕ) : ℚ) := by
        exact_mod_cast (show 0 < 2 * (j + 2) by omega)
      have hlt : 1 / (2 * ((j + 2 : ℕ) : ℚ)) < 1 := (div_lt_one hb).mpr (by
        nlinarith [show (1 : ℚ) ≤ ((j + 2 : ℕ) : ℚ) by
          exact_mod_cast (show 1 ≤ j + 2 by omega)])
      have hpos : 0 < 1 - 1 / (2 * ((j + 2 : ℕ) : ℚ)) := by
        exact sub_pos.mpr hlt
      rw [show 1 + -1 / (2 * ((j + 2 : ℕ) : ℚ)) = 1 - 1 / (2 * ((j + 2 : ℕ) : ℚ)) by ring]
      exact ne_of_gt hpos
  · unfold eSeq
    rcases j with _ | _ | j
    · simp
    · norm_num
    · have hb : 0 < 2 * ((j + 2 : ℕ) : ℚ) := by
        exact_mod_cast (show 0 < 2 * (j + 2) by omega)
      have hpos : 0 < 1 + 3 / (2 * ((j + 2 : ℕ) : ℚ)) := by
        positivity
      exact ne_of_gt hpos

-- Theorem 2: closed forms solve the mu-scale recurrence (j >= 3).

theorem even_plus (c : ℚ) (hc : c ≠ 0) :
    ∀ n : ℕ,
      c ^ 2 * muEvenPlus c (n + 3) =
        PEven c (n + 3) * muEvenPlus c (n + 2) -
          QEven c (n + 3) * muEvenPlus c (n + 1) + REven c (n + 3) * muEvenPlus c n := by
  intro n
  unfold muEvenPlus PEven QEven REven
  rw [show 2 * (n + 3) + 1 = 2 * n + 7 by ring,
      show 2 * (n + 2) + 1 = 2 * n + 5 by ring,
      show 2 * (n + 1) + 1 = 2 * n + 3 by ring,
      cast_factorial_shift n 7, cast_factorial_shift n 5, cast_factorial_shift n 3,
      cast_factorial_shift n 1]
  have hc' : ∀ k : ℕ, c ^ k ≠ 0 := fun k => pow_ne_zero k hc
  have hjm1 : (↑(n + 3 : ℕ) : ℚ) - 1 ≠ 0 := by
    have hgt : 1 < (↑(n + 3 : ℕ) : ℚ) := by
      exact_mod_cast (show 1 < n + 3 by omega)
    exact ne_of_gt (sub_pos.mpr hgt)
  field_simp [hc, hc', hjm1]
  norm_num [prodFactors]
  ring_nf

theorem even_minus (c : ℚ) (hc : c ≠ 0) :
    ∀ n : ℕ,
      c ^ 2 * muEvenMinus c (n + 3) =
        PEven c (n + 3) * muEvenMinus c (n + 2) -
          QEven c (n + 3) * muEvenMinus c (n + 1) + REven c (n + 3) * muEvenMinus c n := by
  intro n
  unfold muEvenMinus PEven QEven REven
  rw [show 2 * (n + 3) = 2 * n + 6 by ring,
      show 2 * (n + 2) = 2 * n + 4 by ring,
      show 2 * (n + 1) = 2 * n + 2 by ring,
      cast_factorial_shift n 6, cast_factorial_shift n 4, cast_factorial_shift n 2]
  have hc' : ∀ k : ℕ, c ^ k ≠ 0 := fun k => pow_ne_zero k hc
  have hjm1 : (↑(n + 3 : ℕ) : ℚ) - 1 ≠ 0 := by
    have hgt : 1 < (↑(n + 3 : ℕ) : ℚ) := by
      exact_mod_cast (show 1 < n + 3 by omega)
    exact ne_of_gt (sub_pos.mpr hgt)
  field_simp [hc, hc', hjm1]
  norm_num [prodFactors]
  ring_nf

theorem odd_plus (c : ℚ) (hc : c ≠ 0) :
    ∀ n : ℕ,
      c ^ 2 * muOddPlus c (n + 3) =
        POdd c (n + 3) * muOddPlus c (n + 2) -
          QOdd c (n + 3) * muOddPlus c (n + 1) + ROdd c (n + 3) * muOddPlus c n := by
  intro n
  unfold muOddPlus POdd QOdd ROdd
  rw [show 2 * (n + 3) + 3 = 2 * n + 9 by ring,
      show 2 * (n + 2) + 3 = 2 * n + 7 by ring,
      show 2 * (n + 1) + 3 = 2 * n + 5 by ring,
      cast_factorial_shift n 9, cast_factorial_shift n 7, cast_factorial_shift n 5,
      cast_factorial_shift n 3]
  rw [show ((n + 3 + 1 : ℕ) : ℚ) = ((n + 4 : ℕ) : ℚ) by
        exact_mod_cast (show n + 3 + 1 = n + 4 by omega),
      show ((n + 2 + 1 : ℕ) : ℚ) = ((n + 3 : ℕ) : ℚ) by
        exact_mod_cast (show n + 2 + 1 = n + 3 by omega),
      show ((n + 1 + 1 : ℕ) : ℚ) = ((n + 2 : ℕ) : ℚ) by
        exact_mod_cast (show n + 1 + 1 = n + 2 by omega)]
  have hc' : ∀ k : ℕ, c ^ k ≠ 0 := fun k => pow_ne_zero k hc
  have hjm1 : (↑(n + 3 : ℕ) : ℚ) - 1 ≠ 0 := by
    have hgt : 1 < (↑(n + 3 : ℕ) : ℚ) := by
      exact_mod_cast (show 1 < n + 3 by omega)
    exact ne_of_gt (sub_pos.mpr hgt)
  have hodd1 : 6 * ((n + 4 : ℕ) : ℚ) ≠ 0 := by
    exact ne_of_gt (by exact_mod_cast (show 0 < 6 * (n + 4) by omega))
  have hodd2 : 6 * ((n + 3 : ℕ) : ℚ) ≠ 0 := by
    exact ne_of_gt (by exact_mod_cast (show 0 < 6 * (n + 3) by omega))
  have hodd3 : 6 * ((n + 2 : ℕ) : ℚ) ≠ 0 := by
    exact ne_of_gt (by exact_mod_cast (show 0 < 6 * (n + 2) by omega))
  field_simp [hc, hc', hjm1, hodd1, hodd2, hodd3]
  norm_num [prodFactors]
  ring_nf

theorem odd_minus (c : ℚ) (hc : c ≠ 0) :
    ∀ n : ℕ,
      c ^ 2 * muOddMinus c (n + 3) =
        POdd c (n + 3) * muOddMinus c (n + 2) -
          QOdd c (n + 3) * muOddMinus c (n + 1) + ROdd c (n + 3) * muOddMinus c n := by
  intro n
  unfold muOddMinus POdd QOdd ROdd
  rw [show 2 * (n + 3) + 1 = 2 * n + 7 by ring,
      show 2 * (n + 2) + 1 = 2 * n + 5 by ring,
      show 2 * (n + 1) + 1 = 2 * n + 3 by ring,
      cast_factorial_shift n 7, cast_factorial_shift n 5, cast_factorial_shift n 3,
      cast_factorial_shift n 1]
  have hc' : ∀ k : ℕ, c ^ k ≠ 0 := fun k => pow_ne_zero k hc
  have hjm1 : (↑(n + 3 : ℕ) : ℚ) - 1 ≠ 0 := by
    have hgt : 1 < (↑(n + 3 : ℕ) : ℚ) := by
      exact_mod_cast (show 1 < n + 3 by omega)
    exact ne_of_gt (sub_pos.mpr hgt)
  field_simp [hc, hc', hjm1]
  norm_num [prodFactors]
  ring_nf

-- Ratio identities mu^-/mu^+.

theorem ratio_even (c : ℚ) (hc : c ≠ 0) (n : ℕ) :
    muEvenMinus c (n + 3) / muEvenPlus c (n + 3) = 1 / (2 * (n : ℚ) + 7) := by
  have hc' : ∀ k : ℕ, c ^ k ≠ 0 := fun k => pow_ne_zero k hc
  have h7 : 2 * (n : ℚ) + 7 ≠ 0 := by
    nlinarith [show (0 : ℚ) ≤ (n : ℚ) by positivity]
  have hmul : (2 * (n : ℚ) + 7) * muEvenMinus c (n + 3) = muEvenPlus c (n + 3) := by
    unfold muEvenMinus muEvenPlus
    rw [show 2 * (n + 3) + 1 = 2 * n + 7 by ring,
        show 2 * (n + 3) = 2 * n + 6 by ring]
    rw [factorial_shift_7 n]
    push_cast
    field_simp [hc']
  have hmnz : muEvenMinus c (n + 3) ≠ 0 := by
    unfold muEvenMinus
    exact div_ne_zero
      (ne_of_gt (by exact_mod_cast (Nat.factorial_pos (2 * (n + 3)))))
      (pow_ne_zero (n + 3) hc)
  have hDx : (2 * (n : ℚ) + 7) * muEvenMinus c (n + 3) ≠ 0 := mul_ne_zero h7 hmnz
  calc
    muEvenMinus c (n + 3) / muEvenPlus c (n + 3)
        = muEvenMinus c (n + 3) / ((2 * (n : ℚ) + 7) * muEvenMinus c (n + 3)) := by
            rw [hmul]
    _ = 1 / (2 * (n : ℚ) + 7) := by
            field_simp [hmnz, h7, hDx]

theorem ratio_odd (c : ℚ) (hc : c ≠ 0) (n : ℕ) :
    muOddMinus c (n + 3) / muOddPlus c (n + 3) = 3 / (2 * (n : ℚ) + 9) := by
  have hc' : ∀ k : ℕ, c ^ k ≠ 0 := fun k => pow_ne_zero k hc
  have h3 : (3 : ℚ) ≠ 0 := by norm_num
  have h9 : 2 * (n : ℚ) + 9 ≠ 0 := by
    nlinarith [show (0 : ℚ) ≤ (n : ℚ) by positivity]
  have hn4 : 6 * ((n : ℚ) + 4) ≠ 0 := by
    nlinarith [show (0 : ℚ) ≤ (n : ℚ) by positivity]
  have hden : 6 * ((n : ℚ) + 4) * c ^ (n + 3) ≠ 0 := mul_ne_zero hn4 (hc' (n + 3))
  have hmul : (2 * (n : ℚ) + 9) * muOddMinus c (n + 3) = 3 * muOddPlus c (n + 3) := by
    unfold muOddMinus muOddPlus
    rw [show 2 * (n + 3) + 1 = 2 * n + 7 by ring,
        show 2 * (n + 3) + 3 = 2 * n + 9 by ring]
    rw [show ((n + 3 + 1 : ℕ) : ℚ) = ((n + 4 : ℕ) : ℚ) by
        exact_mod_cast (show n + 3 + 1 = n + 4 by omega)]
    rw [factorial_shift_9 n]
    push_cast
    field_simp [hc', hn4, hden]; ring
  have hmnz : muOddMinus c (n + 3) ≠ 0 := by
    unfold muOddMinus
    exact div_ne_zero
      (ne_of_gt (by exact_mod_cast (Nat.factorial_pos (2 * (n + 3) + 1))))
      (pow_ne_zero (n + 3) hc)
  have hDx : (2 * (n : ℚ) + 9) * muOddMinus c (n + 3) ≠ 0 := mul_ne_zero h9 hmnz
  have hDx3 : (2 * (n : ℚ) + 9) * muOddMinus c (n + 3) / 3 ≠ 0 := div_ne_zero hDx h3
  have hmuPlus : muOddPlus c (n + 3) = (2 * (n : ℚ) + 9) * muOddMinus c (n + 3) / 3 := by
    calc
      muOddPlus c (n + 3) = (3 * muOddPlus c (n + 3)) / 3 := by
        field_simp [h3]
      _ = (2 * (n : ℚ) + 9) * muOddMinus c (n + 3) / 3 := by
        rw [← hmul]
  calc
    muOddMinus c (n + 3) / muOddPlus c (n + 3)
        = muOddMinus c (n + 3) / ((2 * (n : ℚ) + 9) * muOddMinus c (n + 3) / 3) := by
            rw [hmuPlus]
    _ = 3 / (2 * (n : ℚ) + 9) := by
            field_simp [hmnz, h9, h3, hDx, hDx3]

-- Fixed-point trajectories (Theorem 1, sufficiency direction).

theorem fixed_point_even_mul (c : ℚ) (hc : c ≠ 0) :
    ∀ β : ℚ, β = 1 ∨ β = -1 →
    ∀ n : ℕ,
      eSeq β (n + 3) * eSeq β (n + 2) * eSeq β (n + 1) =
        a1Even c (n + 3) * eSeq β (n + 2) * eSeq β (n + 1) +
          a2Even c (n + 3) * eSeq β (n + 1) + a3Even c (n + 3) := by
  intro β hβ n
  have hc' : ∀ k : ℕ, c ^ k ≠ 0 := fun k => pow_ne_zero k hc
  have hjn1 : (↑(n + 3 : ℕ) : ℚ) ≠ 0 := by
    exact ne_of_gt (by exact_mod_cast (show 0 < n + 3 by omega))
  have hjn2 : (↑(n + 2 : ℕ) : ℚ) ≠ 0 := by
    exact ne_of_gt (by exact_mod_cast (show 0 < n + 2 by omega))
  have hjn3 : (↑(n + 1 : ℕ) : ℚ) ≠ 0 := by
    exact ne_of_gt (by exact_mod_cast (show 0 < n + 1 by omega))
  have hjm1 : (↑(n + 3 : ℕ) : ℚ) - 1 ≠ 0 := by
    have hgt : 1 < (↑(n + 3 : ℕ) : ℚ) := by
      exact_mod_cast (show 1 < n + 3 by omega)
    exact ne_of_gt (sub_pos.mpr hgt)
  have hjm2 : (↑(n + 3 : ℕ) : ℚ) - 2 ≠ 0 := by
    have hgt : 2 < (↑(n + 3 : ℕ) : ℚ) := by
      exact_mod_cast (show 2 < n + 3 by omega)
    exact ne_of_gt (sub_pos.mpr hgt)
  have h2j1 : 2 * (↑(n + 3 : ℕ) : ℚ) ≠ 0 := by
    exact mul_ne_zero (by norm_num) hjn1
  have h2j2 : 2 * (↑(n + 2 : ℕ) : ℚ) ≠ 0 := by
    exact mul_ne_zero (by norm_num) hjn2
  have h2j3 : 2 * (↑(n + 1 : ℕ) : ℚ) ≠ 0 := by
    exact mul_ne_zero (by norm_num) hjn3
  have hj1sq : (↑(n + 3 : ℕ) : ℚ) ^ 2 ≠ 0 := pow_ne_zero 2 hjn1
  have hjm1sq : ((↑(n + 3 : ℕ) : ℚ) - 1) ^ 2 ≠ 0 := pow_ne_zero 2 hjm1
  have hjm2sq : ((↑(n + 3 : ℕ) : ℚ) - 2) ^ 2 ≠ 0 := pow_ne_zero 2 hjm2
  rcases hβ with rfl | rfl
  · unfold eSeq a1Even a2Even a3Even lambda PEven QEven REven
    field_simp [hc, hc', hjn1, hjn2, hjn3, hjm1, hjm2, h2j1, h2j2, h2j3, hj1sq, hjm1sq, hjm2sq]
    norm_num
    ring_nf
  · unfold eSeq a1Even a2Even a3Even lambda PEven QEven REven
    field_simp [hc, hc', hjn1, hjn2, hjn3, hjm1, hjm2, h2j1, h2j2, h2j3, hj1sq, hjm1sq, hjm2sq]
    norm_num
    ring_nf

theorem fixed_point_odd_mul (c : ℚ) (hc : c ≠ 0) :
    ∀ β : ℚ, β = 3 ∨ β = 1 →
    ∀ n : ℕ,
      eSeq β (n + 3) * eSeq β (n + 2) * eSeq β (n + 1) =
        a1Odd c (n + 3) * eSeq β (n + 2) * eSeq β (n + 1) +
          a2Odd c (n + 3) * eSeq β (n + 1) + a3Odd c (n + 3) := by
  intro β hβ n
  have hc' : ∀ k : ℕ, c ^ k ≠ 0 := fun k => pow_ne_zero k hc
  have hjn1 : (↑(n + 3 : ℕ) : ℚ) ≠ 0 := by
    exact ne_of_gt (by exact_mod_cast (show 0 < n + 3 by omega))
  have hjn2 : (↑(n + 2 : ℕ) : ℚ) ≠ 0 := by
    exact ne_of_gt (by exact_mod_cast (show 0 < n + 2 by omega))
  have hjn3 : (↑(n + 1 : ℕ) : ℚ) ≠ 0 := by
    exact ne_of_gt (by exact_mod_cast (show 0 < n + 1 by omega))
  have hjm1 : (↑(n + 3 : ℕ) : ℚ) - 1 ≠ 0 := by
    have hgt : 1 < (↑(n + 3 : ℕ) : ℚ) := by
      exact_mod_cast (show 1 < n + 3 by omega)
    exact ne_of_gt (sub_pos.mpr hgt)
  have hjm2 : (↑(n + 3 : ℕ) : ℚ) - 2 ≠ 0 := by
    have hgt : 2 < (↑(n + 3 : ℕ) : ℚ) := by
      exact_mod_cast (show 2 < n + 3 by omega)
    exact ne_of_gt (sub_pos.mpr hgt)
  have h2j1 : 2 * (↑(n + 3 : ℕ) : ℚ) ≠ 0 := by
    exact mul_ne_zero (by norm_num) hjn1
  have h2j2 : 2 * (↑(n + 2 : ℕ) : ℚ) ≠ 0 := by
    exact mul_ne_zero (by norm_num) hjn2
  have h2j3 : 2 * (↑(n + 1 : ℕ) : ℚ) ≠ 0 := by
    exact mul_ne_zero (by norm_num) hjn3
  have hj1sq : (↑(n + 3 : ℕ) : ℚ) ^ 2 ≠ 0 := pow_ne_zero 2 hjn1
  have hjm1sq : ((↑(n + 3 : ℕ) : ℚ) - 1) ^ 2 ≠ 0 := pow_ne_zero 2 hjm1
  have hjm2sq : ((↑(n + 3 : ℕ) : ℚ) - 2) ^ 2 ≠ 0 := pow_ne_zero 2 hjm2
  rcases hβ with rfl | rfl
  · unfold eSeq a1Odd a2Odd a3Odd lambda POdd QOdd ROdd
    field_simp [hc, hc', hjn1, hjn2, hjn3, hjm1, hjm2, h2j1, h2j2, h2j3, hj1sq, hjm1sq, hjm2sq]
    norm_num
    ring_nf
  · unfold eSeq a1Odd a2Odd a3Odd lambda POdd QOdd ROdd
    field_simp [hc, hc', hjn1, hjn2, hjn3, hjm1, hjm2, h2j1, h2j2, h2j3, hj1sq, hjm1sq, hjm2sq]
    norm_num
    ring_nf

/-- Ratio-map form of the even fixed-point trajectory: with
`e_j = 1 + beta/(2*j)` and beta in {1,-1}, `e_j = F_j(e_{j-1}, e_{j-2})`
for the z-scale ratio map, for all j >= 3. -/
theorem fixed_point_even (c : ℚ) (hc : c ≠ 0) {β : ℚ} (hβ : β = 1 ∨ β = -1) :
    ∀ n : ℕ,
      eSeq β (n + 3) = ThirdOrder.ratioMap (a1Even c) (a2Even c) (a3Even c) (n + 3)
        (eSeq β (n + 2)) (eSeq β (n + 1)) := by
  intro n
  have he1 : eSeq β (n + 1) ≠ 0 := eSeq_ne_zero (by rcases hβ with rfl | rfl <;> simp) (n + 1)
  have he2 : eSeq β (n + 2) ≠ 0 := eSeq_ne_zero (by rcases hβ with rfl | rfl <;> simp) (n + 2)
  calc
    eSeq β (n + 3)
        = (eSeq β (n + 3) * eSeq β (n + 2) * eSeq β (n + 1)) /
            (eSeq β (n + 2) * eSeq β (n + 1)) := by
            field_simp [he1, he2]
    _ = (a1Even c (n + 3) * eSeq β (n + 2) * eSeq β (n + 1) +
          a2Even c (n + 3) * eSeq β (n + 1) + a3Even c (n + 3)) /
            (eSeq β (n + 2) * eSeq β (n + 1)) := by
            rw [fixed_point_even_mul c hc β hβ n]
    _ = ThirdOrder.ratioMap (a1Even c) (a2Even c) (a3Even c) (n + 3)
          (eSeq β (n + 2)) (eSeq β (n + 1)) := by
            unfold ThirdOrder.ratioMap
            field_simp [he1, he2]

/-- Ratio-map form of the odd fixed-point trajectory: with
`e_j = 1 + beta/(2*j)` and beta in {3,1}, `e_j = F_j(e_{j-1}, e_{j-2})`
for the z-scale ratio map, for all j >= 3. -/
theorem fixed_point_odd (c : ℚ) (hc : c ≠ 0) {β : ℚ} (hβ : β = 3 ∨ β = 1) :
    ∀ n : ℕ,
      eSeq β (n + 3) = ThirdOrder.ratioMap (a1Odd c) (a2Odd c) (a3Odd c) (n + 3)
        (eSeq β (n + 2)) (eSeq β (n + 1)) := by
  intro n
  have hb' : β = 1 ∨ β = -1 ∨ β = 3 := by
    rcases hβ with rfl | rfl <;> simp
  have he1 : eSeq β (n + 1) ≠ 0 := eSeq_ne_zero hb' (n + 1)
  have he2 : eSeq β (n + 2) ≠ 0 := eSeq_ne_zero hb' (n + 2)
  calc
    eSeq β (n + 3)
        = (eSeq β (n + 3) * eSeq β (n + 2) * eSeq β (n + 1)) /
            (eSeq β (n + 2) * eSeq β (n + 1)) := by
            field_simp [he1, he2]
    _ = (a1Odd c (n + 3) * eSeq β (n + 2) * eSeq β (n + 1) +
          a2Odd c (n + 3) * eSeq β (n + 1) + a3Odd c (n + 3)) /
            (eSeq β (n + 2) * eSeq β (n + 1)) := by
            rw [fixed_point_odd_mul c hc β hβ n]
    _ = ThirdOrder.ratioMap (a1Odd c) (a2Odd c) (a3Odd c) (n + 3)
          (eSeq β (n + 2)) (eSeq β (n + 1)) := by
            unfold ThirdOrder.ratioMap
            field_simp [he1, he2]

end ThirdOrderClosedForms

end SL
