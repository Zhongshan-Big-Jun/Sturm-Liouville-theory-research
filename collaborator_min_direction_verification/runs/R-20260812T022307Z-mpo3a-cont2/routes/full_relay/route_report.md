RIGOROUS_PARTIAL_RESULT

# Route C2-D report: full asymmetric relay reduction

## Outcome

The complete, potentially asymmetric multiphase O3a self-consistency problem
admits an exact dimension-independent relay representation.  For fixed
`n>=2`, finite `R>1`, and max/min sign, every self-consistent point maps to
three scalar labels

```text
mu=sqrt(lambda_{n+1}/lambda_n),
q=u_{n+1}'(0)/u_n'(0),
L=sqrt(lambda_n),
```

and conversely exactly those finite-switch relay trajectories satisfying two
indexed endpoint phases and one norm equality reconstruct the full point.
No reflection symmetry is used.  The energy and Wronskian argument proves
`q>1` and exactly `2n` simple relay events a posteriori.

Eliminating the common terminal zero time reduces the full problem to two
scalar equations `(A_n,B_n)=0` in `(mu,q)`, quantified over all
premise-complete transverse relay chambers.  This is a stronger reduction
than the prior symmetric half-interval relay: it covers asymmetric points and
therefore could, in principle, prove or refute full O3a directly.

## Exact auxiliary structure

The relay is a continuous piecewise Hamiltonian system for
`omega=dU wedge dP-dV wedge dQ`.  Its exact saltation matrices are symplectic
and have determinant one.  At a transverse root, the original large switch
Jacobian can be Schur-reduced to the `2x2` derivative of `(A_n,B_n)` with
respect to `(mu,q)`.  This makes the remaining local obstruction a hybrid
twist/conjugate-point question.

## What remains open

No fixed sign or injectivity theorem for the two-scalar residual has been
proved.  Symplecticity alone does not exclude conjugate points.  A complete
route must prove exactly one premise-complete zero across all relay chambers,
or certify two distinct zeros.  Therefore neither the max/min subclaims nor
the universal O3a target are closed by this route.

## Artifacts

- `derivation.md`: exact bijection and two-scalar reduction.
- `audit.md`: independent definition/logic/boundary/adversarial audit.
- `hamiltonian_structure.md`: Hamiltonian and saltation structure.
- `local_jacobian.md`: exact `2x2` local determinant obligation.
- `reproducibility_manifest.md`: snapshot and lineage.
- `research_ledger.md`: decisions and calibrated state.

No computation was used in the proof.  Novelty status: unknown.
