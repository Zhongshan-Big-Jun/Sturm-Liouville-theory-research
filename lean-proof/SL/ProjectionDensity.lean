import Mathlib

/-!
# Projection density (DensBC O1, Theorem 1)

Formalization of the abstract core of Theorem 1 from
`runs/rigorous-open-math-research/R-20260816T000000Z-densbc-o1/candidate_proof.md`:

If `V` is a closed subspace of a Hilbert space `H` and `s` is dense in `H`,
then the image of `s` under the orthogonal projection onto `V` is dense in `V`.

The application to the polynomial family is obtained by taking
`s = {p : H | p is the image of a polynomial}`; the Hilbert-space part below
is exactly the topological argument used there.
-/

namespace SL

namespace ProjectionDensity

open Set

/-- The image of a dense set under a continuous surjective map is dense. -/
theorem dense_image_of_surjective_continuous {X Y : Type*} [TopologicalSpace X]
    [TopologicalSpace Y] {f : X → Y} (hf : Continuous f) (hsurj : Function.Surjective f)
    {s : Set X} (hs : Dense s) : Dense (f '' s) :=
  (hsurj.denseRange.dense_image hf hs)

/-- Orthogonal projection onto a complete subspace is surjective onto that subspace. -/
theorem surjective_orthogonalProjectionOnto {𝕜 E : Type*} [RCLike 𝕜]
    [NormedAddCommGroup E] [InnerProductSpace 𝕜 E] [CompleteSpace E]
    (K : Submodule 𝕜 E) [K.HasOrthogonalProjection] :
    Function.Surjective (K.orthogonalProjectionOnto : E → K) := by
  intro v
  refine ⟨(v : E), ?_⟩
  exact K.orthogonalProjectionOnto_mem_subspace_eq_self v

/-- The image of a dense set under the orthogonal projection onto a complete
subspace is dense in that subspace. -/
theorem projection_dense_image {𝕜 E : Type*} [RCLike 𝕜] [NormedAddCommGroup E]
    [InnerProductSpace 𝕜 E] [CompleteSpace E] (K : Submodule 𝕜 E) [K.HasOrthogonalProjection]
    {s : Set E} (hs : Dense s) : Dense (K.orthogonalProjectionOnto '' s) :=
  dense_image_of_surjective_continuous K.orthogonalProjectionOnto.continuous
    (surjective_orthogonalProjectionOnto K) hs

/-- If the polynomials are dense in `H`, then their orthogonal projections onto
`V` are dense in `V`.  The set `polySet` is a placeholder for the image of the
polynomials in `H`; the topological content is the previous theorem. -/
theorem projection_polynomial_dense {𝕜 E : Type*} [RCLike 𝕜] [NormedAddCommGroup E]
    [InnerProductSpace 𝕜 E] [CompleteSpace E] (K : Submodule 𝕜 E) [K.HasOrthogonalProjection]
    (polySet : Set E) (hpoly : Dense polySet) : Dense (K.orthogonalProjectionOnto '' polySet) :=
  projection_dense_image K hpoly

end ProjectionDensity

end SL
