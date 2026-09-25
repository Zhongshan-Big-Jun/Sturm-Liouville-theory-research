import Mathlib.Data.Fin.Rev
import Mathlib.LinearAlgebra.Pi
import Mathlib.LinearAlgebra.Matrix.DotProduct
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Topology.Order.IntermediateValue
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum

namespace AuditRound10

abbrev Vec (n : ℕ) := Fin (2 * n) → ℝ

def J (n : ℕ) : Vec n →ₗ[ℝ] Vec n where
  toFun v i := v i.rev
  map_add' _ _ := rfl
  map_smul' _ _ := rfl

noncomputable def P_preserve (n : ℕ) : Vec n →ₗ[ℝ] Vec n :=
  (1 / 2 : ℝ) • (LinearMap.id - J n)

noncomputable def P_break (n : ℕ) : Vec n →ₗ[ℝ] Vec n :=
  (1 / 2 : ℝ) • (LinearMap.id + J n)

def reflect {n : ℕ} (x : Vec n) : Vec n := fun i => 1 - x i.rev

theorem linear_interfaces {n : ℕ} (u v : Vec n) (a : ℝ) :
    (J n (u + v) = J n u + J n v) ∧ (J n (a • v) = a • J n v) ∧
    (P_preserve n (u + v) = P_preserve n u + P_preserve n v) ∧
    (P_preserve n (a • v) = a • P_preserve n v) ∧
    (P_break n (u + v) = P_break n u + P_break n v) ∧
    (P_break n (a • v) = a • P_break n v) := by
  exact ⟨map_add _ _ _, map_smul _ _ _, map_add _ _ _, map_smul _ _ _,
    map_add _ _ _, map_smul _ _ _⟩

theorem reversal_coordinate {n : ℕ} (v : Vec n) (i : Fin (2 * n)) :
    J n v i = v ⟨2 * n - 1 - i.val, by omega⟩ := by
  change v i.rev = _
  congr 1
  apply Fin.ext
  simp only [Fin.val_rev]
  omega

theorem reversal_involution {n : ℕ} (v : Vec n) : J n (J n v) = v := by
  funext i
  simp [J]

theorem projection_coordinates {n : ℕ} (v : Vec n) (i : Fin (2 * n)) :
    P_preserve n v i = (v i - v i.rev) / 2 ∧
    P_break n v i = (v i + v i.rev) / 2 := by
  constructor
  · simp [P_preserve, J, div_eq_mul_inv, mul_comm]
  · simp [P_break, J, div_eq_mul_inv, mul_comm]
    ring

theorem preserve_eigen {n : ℕ} (v : Vec n) :
    J n (P_preserve n v) = -P_preserve n v := by
  funext i
  simp [P_preserve, J]
  ring

theorem break_eigen {n : ℕ} (v : Vec n) :
    J n (P_break n v) = P_break n v := by
  funext i
  simp [P_break, J, add_comm]

theorem projection_decomposition {n : ℕ} (v : Vec n) :
    P_preserve n v + P_break n v = v := by
  funext i
  simp [P_preserve, P_break, J]
  ring

theorem projection_idempotence {n : ℕ} (v : Vec n) :
    P_preserve n (P_preserve n v) = P_preserve n v ∧
    P_break n (P_break n v) = P_break n v := by
  constructor <;> funext i <;> simp [P_preserve, P_break, J] <;> ring

theorem projection_annihilation {n : ℕ} (v : Vec n) :
    P_preserve n (P_break n v) = 0 ∧
    P_break n (P_preserve n v) = 0 := by
  constructor <;> funext i <;> simp [P_preserve, P_break, J] <;> ring

theorem projection_fixed_iff {n : ℕ} (v : Vec n) :
    (P_preserve n v = v ↔ J n v = -v) ∧
    (P_break n v = v ↔ J n v = v) := by
  constructor
  · constructor
    · intro h
      simpa only [h] using preserve_eigen v
    · intro h
      funext i
      have hi := congrFun h i
      simp only [J, LinearMap.coe_mk, AddHom.coe_mk, Pi.neg_apply] at hi
      simp [P_preserve, J, hi]
      ring
  · constructor
    · intro h
      simpa only [h] using break_eigen v
    · intro h
      funext i
      have hi := congrFun h i
      simp only [J, LinearMap.coe_mk, AddHom.coe_mk] at hi
      simp [P_break, J, hi]
      ring

theorem reversal_dot {n : ℕ} (u v : Vec n) :
    dotProduct (J n u) (J n v) = dotProduct u v := by
  exact Equiv.sum_comp (Fin.revPerm : Equiv.Perm (Fin (2 * n))) (fun i => u i * v i)

theorem projection_orthogonal {n : ℕ} (u v : Vec n) :
    dotProduct (P_preserve n u) (P_break n v) = 0 := by
  have h := reversal_dot (P_preserve n u) (P_break n v)
  rw [preserve_eigen, break_eigen, neg_dotProduct] at h
  linarith

theorem reflection_involution {n : ℕ} (x : Vec n) :
    reflect (reflect x) = x := by
  funext i
  simp [reflect]

theorem reflection_perturbation {n : ℕ} (x v : Vec n) (t : ℝ) :
    reflect (x + t • v) = reflect x - t • J n v := by
  funext i
  simp [reflect, J]
  ring

theorem reflection_at_fixed {n : ℕ} (x u v : Vec n) (t : ℝ)
    (hx : reflect x = x) :
    reflect (x + t • (P_preserve n u + P_break n v)) =
      x + t • (P_preserve n u - P_break n v) := by
  rw [reflection_perturbation, hx, map_add, preserve_eigen, break_eigen]
  funext i
  simp
  ring

theorem preserved_perturbation_iff {n : ℕ} (x v : Vec n)
    (hx : reflect x = x) :
    reflect (x + v) = x + v ↔ J n v = -v := by
  have hp := reflection_perturbation x v 1
  simp only [one_smul, hx] at hp
  rw [hp]
  constructor
  · intro h
    funext i
    have hi := congrFun h i
    simp only [Pi.sub_apply, Pi.add_apply] at hi
    simp only [Pi.neg_apply]
    linarith
  · intro h
    rw [h, sub_neg_eq_add]

def phase_root (Phi : ℝ → ℝ) (k : ℕ) (x : ℝ) : Prop :=
  0 ≤ x ∧ Phi x = (k : ℝ) * Real.pi

theorem phase_root_unique {Phi : ℝ → ℝ}
    (hm : StrictMonoOn Phi (Set.Ici 0)) {k : ℕ} {x y : ℝ}
    (hx : phase_root Phi k x) (hy : phase_root Phi k y) : x = y :=
  hm.injOn hx.1 hy.1 (hx.2.trans hy.2.symm)

theorem bracket_unique_root {Phi : ℝ → ℝ}
    (hc : ContinuousOn Phi (Set.Ici 0))
    (hm : StrictMonoOn Phi (Set.Ici 0))
    (k : ℕ) (a b : ℝ) (ha : 0 ≤ a) (hab : a ≤ b)
    (hl : Phi a ≤ (k : ℝ) * Real.pi) (hr : (k : ℝ) * Real.pi ≤ Phi b) :
    ∃! x : ℝ, x ∈ Set.Icc a b ∧ phase_root Phi k x := by
  have hsub : Set.Icc a b ⊆ Set.Ici 0 := fun x hx => ha.trans hx.1
  obtain ⟨x, hx, he⟩ := intermediate_value_Icc hab (hc.mono hsub) ⟨hl, hr⟩
  refine ⟨x, ⟨hx, ha.trans hx.1, he⟩, ?_⟩
  intro y hy
  exact phase_root_unique hm hy.2 ⟨ha.trans hx.1, he⟩

theorem phase_index_order {Phi : ℝ → ℝ}
    (hm : StrictMonoOn Phi (Set.Ici 0)) {j k : ℕ} {x y : ℝ}
    (hx : phase_root Phi j x) (hy : phase_root Phi k y) :
    (x < y ↔ j < k) := by
  constructor
  · intro hxy
    have hh := hm hx.1 hy.1 hxy
    rw [hx.2, hy.2] at hh
    have hk : (j : ℝ) < (k : ℝ) := by
      nlinarith [Real.pi_pos]
    exact_mod_cast hk
  · intro hjk
    have hcast : (j : ℝ) < (k : ℝ) := by exact_mod_cast hjk
    have hh : Phi x < Phi y := by
      rw [hx.2, hy.2]
      exact mul_lt_mul_of_pos_right hcast Real.pi_pos
    by_contra hxy
    have hyx : y ≤ x := le_of_not_gt hxy
    have hmle := hm.monotoneOn hy.1 hx.1 hyx
    exact (not_lt_of_ge hmle) hh

theorem indexed_roots_strict_mono {Phi : ℝ → ℝ}
    (hm : StrictMonoOn Phi (Set.Ici 0)) (index : ℕ → ℕ) (roots : ℕ → ℝ)
    (hi : StrictMono index) (hr : ∀ m, phase_root Phi (index m) (roots m)) :
    StrictMono roots := by
  intro a b hab
  exact (phase_index_order hm (hr a) (hr b)).2 (hi hab)

theorem enumeration_from_brackets {Phi : ℝ → ℝ}
    (hc : ContinuousOn Phi (Set.Ici 0))
    (hm : StrictMonoOn Phi (Set.Ici 0))
    (index : ℕ → ℕ) (hi : StrictMono index) (left right : ℕ → ℝ)
    (hleft : ∀ m, 0 ≤ left m) (horder : ∀ m, left m ≤ right m)
    (hl : ∀ m, Phi (left m) ≤ (index m : ℝ) * Real.pi)
    (hr : ∀ m, (index m : ℝ) * Real.pi ≤ Phi (right m)) :
    ∃ roots : ℕ → ℝ,
      (∀ m, roots m ∈ Set.Icc (left m) (right m) ∧ phase_root Phi (index m) (roots m)) ∧
      StrictMono roots := by
  have hex (m : ℕ) :=
    (bracket_unique_root hc hm (index m) (left m) (right m)
      (hleft m) (horder m) (hl m) (hr m)).exists
  choose roots hroots using hex
  exact ⟨roots, hroots, indexed_roots_strict_mono hm index roots hi (fun m => (hroots m).2)⟩

-- BEGIN GENERATED ROOT

set_option linter.unusedVariables false in
theorem root :
(∀ {n : ℕ} (u v : Vec n) (a : ℝ),
(J n (u + v) = J n u + J n v) ∧ (J n (a • v) = a • J n v) ∧
    (P_preserve n (u + v) = P_preserve n u + P_preserve n v) ∧
    (P_preserve n (a • v) = a • P_preserve n v) ∧
    (P_break n (u + v) = P_break n u + P_break n v) ∧
    (P_break n (a • v) = a • P_break n v)) ∧
(∀ {n : ℕ} (v : Vec n) (i : Fin (2 * n)),
J n v i = v ⟨2 * n - 1 - i.val, by omega⟩) ∧
(∀ {n : ℕ} (v : Vec n),
J n (J n v) = v) ∧
(∀ {n : ℕ} (v : Vec n) (i : Fin (2 * n)),
P_preserve n v i = (v i - v i.rev) / 2 ∧
    P_break n v i = (v i + v i.rev) / 2) ∧
(∀ {n : ℕ} (v : Vec n),
J n (P_preserve n v) = -P_preserve n v) ∧
(∀ {n : ℕ} (v : Vec n),
J n (P_break n v) = P_break n v) ∧
(∀ {n : ℕ} (v : Vec n),
P_preserve n v + P_break n v = v) ∧
(∀ {n : ℕ} (v : Vec n),
P_preserve n (P_preserve n v) = P_preserve n v ∧
    P_break n (P_break n v) = P_break n v) ∧
(∀ {n : ℕ} (v : Vec n),
P_preserve n (P_break n v) = 0 ∧
    P_break n (P_preserve n v) = 0) ∧
(∀ {n : ℕ} (v : Vec n),
(P_preserve n v = v ↔ J n v = -v) ∧
    (P_break n v = v ↔ J n v = v)) ∧
(∀ {n : ℕ} (u v : Vec n),
dotProduct (J n u) (J n v) = dotProduct u v) ∧
(∀ {n : ℕ} (u v : Vec n),
dotProduct (P_preserve n u) (P_break n v) = 0) ∧
(∀ {n : ℕ} (x : Vec n),
reflect (reflect x) = x) ∧
(∀ {n : ℕ} (x v : Vec n) (t : ℝ),
reflect (x + t • v) = reflect x - t • J n v) ∧
(∀ {n : ℕ} (x u v : Vec n) (t : ℝ)
    (hx : reflect x = x),
reflect (x + t • (P_preserve n u + P_break n v)) =
      x + t • (P_preserve n u - P_break n v)) ∧
(∀ {n : ℕ} (x v : Vec n)
    (hx : reflect x = x),
reflect (x + v) = x + v ↔ J n v = -v) ∧
(∀ {Phi : ℝ → ℝ}
    (hm : StrictMonoOn Phi (Set.Ici 0)) {k : ℕ} {x y : ℝ}
    (hx : phase_root Phi k x) (hy : phase_root Phi k y),
x = y) ∧
(∀ {Phi : ℝ → ℝ}
    (hc : ContinuousOn Phi (Set.Ici 0))
    (hm : StrictMonoOn Phi (Set.Ici 0))
    (k : ℕ) (a b : ℝ) (ha : 0 ≤ a) (hab : a ≤ b)
    (hl : Phi a ≤ (k : ℝ) * Real.pi) (hr : (k : ℝ) * Real.pi ≤ Phi b),
∃! x : ℝ, x ∈ Set.Icc a b ∧ phase_root Phi k x) ∧
(∀ {Phi : ℝ → ℝ}
    (hm : StrictMonoOn Phi (Set.Ici 0)) {j k : ℕ} {x y : ℝ}
    (hx : phase_root Phi j x) (hy : phase_root Phi k y),
(x < y ↔ j < k)) ∧
(∀ {Phi : ℝ → ℝ}
    (hm : StrictMonoOn Phi (Set.Ici 0)) (index : ℕ → ℕ) (roots : ℕ → ℝ)
    (hi : StrictMono index) (hr : ∀ m, phase_root Phi (index m) (roots m)),
StrictMono roots) ∧
(∀ {Phi : ℝ → ℝ}
    (hc : ContinuousOn Phi (Set.Ici 0))
    (hm : StrictMonoOn Phi (Set.Ici 0))
    (index : ℕ → ℕ) (hi : StrictMono index) (left right : ℕ → ℝ)
    (hleft : ∀ m, 0 ≤ left m) (horder : ∀ m, left m ≤ right m)
    (hl : ∀ m, Phi (left m) ≤ (index m : ℝ) * Real.pi)
    (hr : ∀ m, (index m : ℝ) * Real.pi ≤ Phi (right m)),
∃ roots : ℕ → ℝ,
      (∀ m, roots m ∈ Set.Icc (left m) (right m) ∧ phase_root Phi (index m) (roots m)) ∧
      StrictMono roots) := by
  exact ⟨@linear_interfaces,
    @reversal_coordinate,
    @reversal_involution,
    @projection_coordinates,
    @preserve_eigen,
    @break_eigen,
    @projection_decomposition,
    @projection_idempotence,
    @projection_annihilation,
    @projection_fixed_iff,
    @reversal_dot,
    @projection_orthogonal,
    @reflection_involution,
    @reflection_perturbation,
    @reflection_at_fixed,
    @preserved_perturbation_iff,
    @phase_root_unique,
    @bracket_unique_root,
    @phase_index_order,
    @indexed_roots_strict_mono,
    @enumeration_from_brackets⟩

end AuditRound10
