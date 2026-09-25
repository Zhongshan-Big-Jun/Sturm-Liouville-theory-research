# Round10 intended local mathematical contract

This document records author intent for the coordinator's later comparison. It must not be given to the first blind readback agent. It is not an independent semantic review.

## Carriers and definitions

`n : ℕ`, `Vec n = Fin (2*n) → ℝ`. `Fin` uses zero-based coordinates. Thus `J n v i = v(2*n-1-i)`. `J n`, `P_preserve n`, and `P_break n` have type `Vec n →ₗ[ℝ] Vec n`; real linearity is certified by their Lean constructions, not supplied as an assumption. The projections are exactly `(I-J)/2` and `(I+J)/2`.

`reflect x i = 1 - x(i.rev)` is the affine geometric reflection. `dotProduct u v = Σ_i u_i v_i` is the real Euclidean inner product on these coordinate vectors. The file does not put the function space's inherited norm in correspondence with its Euclidean norm, nor does it need that identification for the finite sum orthogonality claim.

`Phi : ℝ → ℝ` represents a function on `[0,∞)` by restriction. Hypotheses are only `ContinuousOn Phi (Set.Ici 0)` and `StrictMonoOn Phi (Set.Ici 0)`; no property is asserted or used on negative inputs. `phase_root Phi k x` means exactly `0 ≤ x ∧ Phi x = (k:ℝ)*Real.pi`, where `k : ℕ`. It does not mean that a Sturm differential equation or its k-th eigenvalue has already been formalized.

## Per-target intent

| Fully qualified target under AuditRound10 | Hypotheses and conclusion |
| --- | --- |
| `linear_interfaces` | J and both projections preserve vector addition and real scalar multiplication, for all n,u,v,a. |
| `reversal_coordinate` | For all n, vectors and actual Fin coordinates, evaluate J at the reversed zero-based coordinate. |
| `reversal_involution` | For every n and vector v, J(Jv)=v. |
| `projection_coordinates` | At every coordinate, the two linear maps evaluate to (v_i-v_rev(i))/2 and (v_i+v_rev(i))/2. |
| `preserve_eigen` | J(P_preserve v)=-P_preserve v, with no assumed eigenspace condition on v. |
| `break_eigen` | J(P_break v)=P_break v, with no assumed eigenspace condition on v. |
| `projection_decomposition` | P_preserve v+P_break v=v for every v. |
| `projection_idempotence` | Both maps satisfy P(Pv)=Pv for every v. |
| `projection_annihilation` | Each projection kills the range of the other, in both orders. |
| `projection_fixed_iff` | P_preserve v=v iff Jv=-v; P_break v=v iff Jv=v. These identify the entire ranges, not just inclusions. |
| `reversal_dot` | Simultaneous coordinate reversal preserves the real Euclidean dot product of any two vectors. |
| `projection_orthogonal` | For any u,v of the same dimension, dot(P_preserve u,P_break v)=0. |
| `reflection_involution` | For every x, reflect(reflect x)=x. |
| `reflection_perturbation` | For arbitrary x,v and real t, reflect(x+t v)=reflect(x)-t Jv. No symmetry or small-step hypothesis is needed for this algebraic identity. |
| `reflection_at_fixed` | If reflect x=x, then reflect(x+t(P_preserve u+P_break v))=x+t(P_preserve u-P_break v). |
| `preserved_perturbation_iff` | At a fixed point x, reflect(x+v)=x+v iff Jv=-v. |
| `phase_root_unique` | Strict monotonicity on the nonnegative half-line and two roots at the same natural level imply equal roots. Continuity is not needed for uniqueness. |
| `bracket_unique_root` | Given continuity, strict monotonicity, 0≤a≤b and Phi(a)≤kπ≤Phi(b), IVT supplies exactly one x in [a,b] with phase_root Phi k x. Global same-level uniqueness follows from phase_root_unique. |
| `phase_index_order` | Under strict monotonicity, given roots x,y at levels jπ,kπ, x<y iff j<k. Positivity of π is a library theorem, not an assumption. |
| `indexed_roots_strict_mono` | A strictly increasing natural-valued index sequence and roots at exactly those phase levels yield a strictly increasing real root sequence. |
| `enumeration_from_brackets` | With one valid closed bracket for each entry of a strictly increasing index sequence, there exists a root sequence in those brackets, at those exact levels, and that sequence is strictly increasing. This is a classical existence result, not executable numerical enumeration. |
| `root` | A materialized conjunction of the explicit local statements, including coordinate linearity and the phase interface. The exact formal type is saved separately in root-contract.json and the declaration outputs. |

## Meaningful boundary cases and excluded claims

- `n=0` is included and gives the zero-dimensional vector space. The universal claims also cover every positive n; negative controls use n=1, so nontrivial dimensional behavior is exercised.
- Closed brackets allow a=b and roots at either endpoint. k=0 is allowed but its existence still requires a valid bracket. A positive spectral numbering convention, such as indices m+1, must be supplied by the caller.
- Strict increase of indices need not mean consecutive indices. The ordering theorem alone does not prove there are no omitted natural levels. Full coverage requires choosing the desired consecutive index sequence and supplying a valid bracket for each entry.
- Continuity and strict increase alone do not imply unboundedness or a root at every kπ. The enumeration theorem retains the explicit per-index brackets.
- No Sturm-Liouville operator, Prüfer ODE, phase lift, differentiability, eigenvalue multiplicity, eigenvalue/phase identification, comparison bounds, floating-point errors, interval inclusions, solver termination or Python implementation is certified here.
- Algebraic reflection does not certify preservation of ordered physical interfaces after clipping, feasible step sizes, nonzero normalized projected samples, Hessian sector properties or any global symmetry/extremizer statement.

## Negative controls

The legacy all-index assignment acts as F=-J. On v=(1,1) in dimension two, F(Fv)=v while Fv=-v. A second dimension-two control sets x=0,v=(1,1): reflect(x+v)=0 whereas reflect x+Jv=(2,2). A phase control takes Phi(x)=x; 2π is not the root at level 1π. The latter is an index-interface counterexample, not a replay of the original floating-point root-loss experiment.

Three files attempt to prove these false statements and must return real compiler failures with unresolved mathematical goals. Counterexamples.lean proves their exact negations, which rules out interpreting mere tactic failure as a proof of falsity.

The positive control declarations are `AuditRound10Controls.flip_not_projection`, `AuditRound10Controls.reflection_plus_sign_false`, and `AuditRound10Controls.phase_off_by_one_false`; each has the literal negation of the corresponding Negative file's proposition, under the same dimensions, constants and phase function.

## Review handoff

Only the frozen formal-only packet goes to a fresh blind reader. A different fresh reviewer then compares the actual readback with this contract, the source, exact types, imported environment and compiler/axiom evidence. This author does not issue either review or claim an independent PASS.
