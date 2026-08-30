-- SCAFFOLD: kp-odd-first-zero RIGOROUS_PARTIAL_RESULT open KP-CORANKONE-BRANCH-EQUALITY, KP-KO-SIMULTANEOUS-SINGULARITY, KO-DET
-- Source: v1.9 live recovery run R-20260830T020000Z-g1p-live-recovery.
-- This file states the finite-dimensional algebra isolated by the audited
-- partial result. It is a scaffold and is not formally verified.

import Mathlib

namespace SL.KpOddFirstZeroScaffold

/-- Determinant of the symmetric two-by-two scalar matrix. -/
def det2 (m11 m12 m22 : ℝ) : ℝ :=
  m11 * m22 - m12 ^ 2

/-- The exact scalar equality left by the semiseparable first-zero reduction. -/
def scalarFirstZero (a b gamma1 gamma2 : ℝ) : Prop :=
  gamma2 > b ∧ gamma1 - a = b ^ 2 / (gamma2 - b)

/-- Positive odd off-diagonal entry excludes the zero-matrix alternative. -/
theorem positive_offdiag_excludes_double_zero
  (m11 m12 m22 : ℝ) (hOff : 0 < m12) :
  ¬(m11 = 0 ∧ m12 = 0 ∧ m22 = 0) := by
  intro hZero
  linarith [hOff, hZero.2.1]

/-- Algebraic form of the remaining corank-one equality. -/
theorem scalar_first_zero_of_det
  (a b gamma1 gamma2 : ℝ)
  (h22 : b - gamma2 < 0)
  (hDet : det2 (a - gamma1) b (b - gamma2) = 0) :
  scalarFirstZero a b gamma1 gamma2 := by
  sorry

/-- A nonzero same-sign kernel for the reduced two-by-two matrix. -/
def sameSignKernel
  (a b gamma1 gamma2 y1 y2 : ℝ) : Prop :=
  (y1 ≠ 0 ∨ y2 ≠ 0) ∧
  0 < y1 * y2 ∧
  (a - gamma1) * y1 + b * y2 = 0 ∧
  b * y1 + (b - gamma2) * y2 = 0

/-- Open proof obligation: exclude the branch-realizable same-sign kernel. -/
theorem no_branch_same_sign_kernel
  (a b gamma1 gamma2 y1 y2 : ℝ)
  (hExactSymmetricINFBranch : Prop)
  (hBranchEquations : hExactSymmetricINFBranch) :
  ¬sameSignKernel a b gamma1 gamma2 y1 y2 := by
  sorry

end SL.KpOddFirstZeroScaffold
