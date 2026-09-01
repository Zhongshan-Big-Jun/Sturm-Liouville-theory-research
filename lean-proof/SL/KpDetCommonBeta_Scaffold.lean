-- SCAFFOLD: kp-det common-beta algebraic core.
-- Source: R-20260831T020156Z-g1p-kpdet, audited packages P8-P15.
-- This file formalizes only the algebraic sign chain, not the trigonometric
-- common-beta reconstruction or the complete Sturm-Liouville contract.
-- Lean 4 rejects tab characters, so this file uses spaces.

import Mathlib

namespace SL.KpDetCommonBetaScaffold

/-- Positive mass weights exclude a nonnegative middle coefficient once the
exact phase identities force the two other coefficients to be positive. -/
theorem mass_balance_forces_b_negative
    (alpha beta theta Acoef Bcoef Hcoef : ℝ)
    (hAlpha : 0 < alpha)
    (hBeta : 0 < beta)
    (hTheta : 0 < theta)
    (hMass : alpha * Acoef + beta * Bcoef + theta * Hcoef = 0)
    (hAOfB : 0 ≤ Bcoef → 0 < Acoef)
    (hHOfB : 0 ≤ Bcoef → 0 < Hcoef) :
    Bcoef < 0 := by
  by_contra hNotNegative
  have hBNonnegative : 0 ≤ Bcoef := not_lt.mp hNotNegative
  have hAlphaA : 0 < alpha * Acoef :=
    mul_pos hAlpha (hAOfB hBNonnegative)
  have hBetaB : 0 ≤ beta * Bcoef :=
    mul_nonneg (le_of_lt hBeta) hBNonnegative
  have hThetaH : 0 < theta * Hcoef :=
    mul_pos hTheta (hHOfB hBNonnegative)
  have hFirstTwo : 0 < alpha * Acoef + beta * Bcoef :=
    add_pos_of_pos_of_nonneg hAlphaA hBetaB
  have hPositiveMass :
      0 < alpha * Acoef + beta * Bcoef + theta * Hcoef :=
    add_pos hFirstTwo hThetaH
  exact (ne_of_gt hPositiveMass) hMass

/-- The accepted factorization turns `q < E` into strict positivity of `G`. -/
theorem g_positive_of_factorization
    (X prefactor q E G : ℝ)
    (hX : X < 0)
    (hPrefactor : 0 < prefactor)
    (hQE : q < E)
    (hFactorization : G = X * prefactor * (q - E)) :
    0 < G := by
  have hXPrefactor : X * prefactor < 0 :=
    mul_neg_of_neg_of_pos hX hPrefactor
  have hDifference : q - E < 0 := sub_neg.mpr hQE
  rw [hFactorization]
  exact mul_pos_of_neg_of_neg hXPrefactor hDifference

/-- The accepted split `Xi = X^2 G - r K Dtheta` is positive when `G > 0`
and the correction has the audited signs. -/
theorem xi_positive_of_split
    (X G r K Dtheta Xi : ℝ)
    (hG : 0 < G)
    (hR : 0 < r)
    (hK : K < 0)
    (hDtheta : 0 < Dtheta)
    (hSplit : Xi = X ^ 2 * G - r * K * Dtheta) :
    0 < Xi := by
  have hSquareTerm : 0 ≤ X ^ 2 * G :=
    mul_nonneg (sq_nonneg X) (le_of_lt hG)
  have hRK : r * K < 0 := mul_neg_of_pos_of_neg hR hK
  have hRKDtheta : r * K * Dtheta < 0 :=
    mul_neg_of_neg_of_pos hRK hDtheta
  rw [hSplit, sub_eq_add_neg]
  exact add_pos_of_nonneg_of_pos hSquareTerm (neg_pos.mpr hRKDtheta)

/-- Machine-checked algebraic core of the audited closed chamber. The analytic
work needed to derive `q < 0 < E` from common-beta geometry is not encoded. -/
theorem closed_chamber_sign_chain
    (X prefactor q E G r K Dtheta Xi : ℝ)
    (hX : X < 0)
    (hPrefactor : 0 < prefactor)
    (hQ : q < 0)
    (hE : 0 < E)
    (hFactorization : G = X * prefactor * (q - E))
    (hR : 0 < r)
    (hK : K < 0)
    (hDtheta : 0 < Dtheta)
    (hSplit : Xi = X ^ 2 * G - r * K * Dtheta) :
    0 < G ∧ 0 < Xi := by
  have hQE : q < E := lt_trans hQ hE
  have hG : 0 < G :=
    g_positive_of_factorization X prefactor q E G hX hPrefactor hQE
      hFactorization
  exact ⟨hG, xi_positive_of_split X G r K Dtheta Xi hG hR hK hDtheta hSplit⟩

end SL.KpDetCommonBetaScaffold
