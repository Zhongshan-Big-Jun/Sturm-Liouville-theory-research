import Mathlib

/-!
# DensBC O1: empty kept set forces density failure (Lemma 6.1)

Formalization of the algebraic/topological core of Lemma 6.1 from
`runs/rigorous-open-math-research/R-20260816T000000Z-densbc-o1/candidate_proof.md`:

If the kept sparse family `Q_sp` is empty, then its closed span is `{0}`,
so it can be dense in `V` only in the degenerate case `V = {0}`.
-/

namespace SL

namespace DensBCEmpty

open Set

/-- The closure of the span of the empty set is the zero subspace (in a T1 space). -/
theorem closure_span_empty_eq_bot {M : Type*} [AddCommGroup M] [Module ℝ M]
    [TopologicalSpace M] [T1Space M] :
    closure (Submodule.span ℝ (∅ : Set M) : Set M) = ({0} : Set M) := by
  simp

/-- If a set `Q` is empty, then the closure of its span is the zero set. -/
theorem closure_span_empty {M : Type*} [AddCommGroup M] [Module ℝ M]
    [TopologicalSpace M] [T1Space M] {Q : Set M} (hQ : Q = ∅) :
    closure (Submodule.span ℝ Q : Set M) = ({0} : Set M) := by
  rw [hQ]
  exact closure_span_empty_eq_bot

/-- If an empty candidate family were dense in a subspace `V`, then `V` is the
zero subspace.  This is the contrapositive content of Lemma 6.1. -/
theorem eq_bot_of_dense_of_empty {M : Type*} [AddCommGroup M] [Module ℝ M]
    [TopologicalSpace M] [T1Space M] {V : Submodule ℝ M} {Q : Set V}
    (hQ : Q = ∅) (hd : Dense (Submodule.span ℝ Q : Set V)) : V = ⊥ := by
  have hspan : closure (Submodule.span ℝ Q : Set V) = ({0} : Set V) := by
    rw [hQ]
    simp
  have huniv : closure (Submodule.span ℝ Q : Set V) = Set.univ := hd.closure_eq
  have hzero : ∀ x : V, x = 0 := by
    intro x
    have hx : x ∈ closure (Submodule.span ℝ Q : Set V) := by simp [huniv]
    rw [hspan] at hx
    simpa using hx
  apply (Submodule.eq_bot_iff V).mpr
  intro x hx
  exact Subtype.ext_iff.mp (hzero ⟨x, hx⟩)

end DensBCEmpty

end SL
