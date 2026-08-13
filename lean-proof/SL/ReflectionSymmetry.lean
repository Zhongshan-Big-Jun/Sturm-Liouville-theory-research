import Mathlib

/-!
# Reflection symmetry of the fixed-index alternating configuration

Formalization of the strictly proved J-conjugacy argument from
`docs/SL_fixed_n_supremum.tex` Theorem "reflection symmetry": for the cell and
end transfer matrices of the alternating configuration `[1,R,1,R,...,1]`, the
matrix

    M_n(y) = T_end(y) * T_cell(y)^n

satisfies `M_n(pi - y) = -J * M_n(y) * J`, and therefore its `(0,1)` entry
(the secular function `F_n`) satisfies `F_n(pi - y) = F_n(y)`.

The present file treats the frequency `ω` as a fixed parameter, exactly as the
source proof does when it conjugates the matrices.  The source's phase
normalization `y = ω * sqrt(R) * t` and the spectral identification of the
matrix condition with Dirichlet eigenvalues are not formalized here.
-/

namespace SL

namespace ReflectionSymmetry

open Matrix

noncomputable section

/-- `J = diag(1,-1)`, the reflection conjugation matrix. -/
def J : Matrix (Fin 2) (Fin 2) ℝ :=
  !![(1 : ℝ), 0; 0, -1]

/-- Transfer matrix for one `[1,R]` cell of the alternating configuration. -/
def Tcell (s ω y : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![(Real.cos y) ^ 2 - (Real.sin y) ^ 2 / s,
     (1 + s) * Real.sin y * Real.cos y / (ω * s);
     -ω * (1 + s) * Real.sin y * Real.cos y,
     (Real.cos y) ^ 2 - s * (Real.sin y) ^ 2]

/-- Transfer matrix for the final `[1]` block. -/
def Tend (ω y : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![Real.cos y, Real.sin y / ω;
     -ω * Real.sin y, Real.cos y]

/-- The product `T_end(y) * T_cell(y)^n`. -/
def M (s ω y : ℝ) (n : ℕ) : Matrix (Fin 2) (Fin 2) ℝ :=
  Tend ω y * (Tcell s ω y) ^ n

/-- The secular function `F_n(y) = (M_n(y))_{0,1}`. -/
def F (s ω y : ℝ) (n : ℕ) : ℝ :=
  (M s ω y n) 0 1

lemma J_mul_J : J * J = 1 := by
  ext i j; fin_cases i <;> fin_cases j <;> simp [J, Matrix.mul_apply, Fin.sum_univ_two]

lemma J_Tcell {s ω y : ℝ} (hs : s ≠ 0) (hω : ω ≠ 0) :
    J * Tcell s ω y * J = Tcell s ω (Real.pi - y) := by
  ext i j; fin_cases i <;> fin_cases j <;> simp [J, Tcell, Matrix.mul_apply, Fin.sum_univ_two]
  all_goals field_simp [hs, hω]

lemma J_Tend {ω y : ℝ} :
    J * Tend ω y * J = -Tend ω (Real.pi - y) := by
  ext i j; fin_cases i <;> fin_cases j <;>
    simp [J, Tend, Matrix.mul_apply, Fin.sum_univ_two, Real.cos_pi_sub, Real.sin_pi_sub]

/-- Conjugation commutes with nonnegative matrix powers when `J * J = 1`. -/
lemma J_conj_pow {A : Matrix (Fin 2) (Fin 2) ℝ} {n : ℕ} (hJ : J * J = 1) :
    J * A ^ n * J = (J * A * J) ^ n := by
  induction n with
  | zero =>
      simp [hJ]
  | succ n ih =>
      rw [pow_succ, pow_succ]
      rw [← ih]
      have hjj : J * (J * (A * J)) = A * J := by
        rw [← Matrix.mul_assoc, hJ, one_mul]
      simp [Matrix.mul_assoc, hjj]

lemma Tend_pi_sub_of {ω y : ℝ} :
    Tend ω (Real.pi - y) = -(J * Tend ω y * J) := by
  have h := J_Tend (ω := ω) (y := y)
  rw [h]
  simp

lemma Tcell_pow_pi_sub (hs : s ≠ 0) (hω : ω ≠ 0) {y : ℝ} {n : ℕ} :
    (Tcell s ω (Real.pi - y)) ^ n = J * (Tcell s ω y) ^ n * J := by
  have h := J_Tcell (s := s) (ω := ω) (y := y) hs hω
  rw [← h]
  exact (J_conj_pow (A := Tcell s ω y) J_mul_J).symm

/-- The matrix `M_n` reflects under `y ↦ pi - y` as `-J * M_n * J`. -/
lemma M_reflection {s ω y : ℝ} {n : ℕ} (hs : s ≠ 0) (hω : ω ≠ 0) :
    M s ω (Real.pi - y) n = -(J * M s ω y n * J) := by
  unfold M
  rw [Tcell_pow_pi_sub hs hω]
  rw [Tend_pi_sub_of]
  have hJmid : J * (J * (Tcell s ω y ^ n * J)) = Tcell s ω y ^ n * J := by
    rw [← Matrix.mul_assoc, J_mul_J, one_mul]
  simp [Matrix.mul_assoc, hJmid]

lemma J_conj_entry {A : Matrix (Fin 2) (Fin 2) ℝ} :
    (J * A * J) 0 1 = -(A 0 1) := by
  rw [Matrix.mul_assoc]
  simp [J, Matrix.mul_apply, Fin.sum_univ_two]

/-- Reflection symmetry of the secular function `F_n`. -/
theorem F_reflection {s ω y : ℝ} {n : ℕ} (hs : s ≠ 0) (hω : ω ≠ 0) :
    F s ω (Real.pi - y) n = F s ω y n := by
  unfold F
  rw [M_reflection hs hω]
  rw [Matrix.neg_apply]
  rw [J_conj_entry]
  ring

end

end ReflectionSymmetry

end SL
