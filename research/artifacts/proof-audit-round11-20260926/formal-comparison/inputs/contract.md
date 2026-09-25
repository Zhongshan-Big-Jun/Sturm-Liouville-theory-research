# Round 11 local Lean author contract

Status: author specification and self-check only. Independent blind readback, semantic comparison and final acceptance are pending. The two supplied reports are unverified inputs; this packet only addresses the algebra described below.

## Objects and coordinates

All matrices and vectors in this file are over the Lean type `Real`, written `ℝ`. `n : Nat` is arbitrary, including zero. `Square n` is `Matrix (Fin n) (Fin n) ℝ`. `PairIndex n = Fin n ⊕ Fin n`, so a paired matrix has size `2n`.

The first copy indexes one representative from each mirrored pair; the second copy indexes its partner in the SAME pair order. To interpret these as physically increasing interface positions, `inl i` corresponds to zero-based position `i`, and `inr i` to position `2n-1-i`. The last correspondence is a human indexing convention, not a formal theorem about a concrete `Fin (2*n)` permutation or a NumPy array. There is no fixed central coordinate. Odd total dimensions are not covered by this balanced representation.

`P = reversal n = [[0,I],[I,0]]` swaps the two copies. `T = parity_basis n = [[I,I],[I,-I]]`; `S = parity_inverse n = (1/2)T`; `Q = parity_sign n = [[I,0],[0,-I]]`. Physical coordinates equal `T` times parity coordinates; parity coordinates equal `S` times physical coordinates. These are an invertible sum/difference basis, not normalized orthonormal columns. `parity_matrix J = S J T`. Its block 12 maps coordinate-odd input to coordinate-even output; block 21 maps coordinate-even input to coordinate-odd output.

## Exact interfaces

Each name below is prefixed by `AuditRound11.`. The actual elaborated declarations, binder kinds, universes, definition bodies and transitive axioms are exported from Lean into `declarations-full.json`, with a separate raw `#print` and `#print axioms` log. `contract.json` gives a literal universally quantified conjunction, not a proposition that merely says a check flag is true.

| Declaration | Quantifiers, hypotheses and conclusion |
| --- | --- |
| `parity_basis_identities` | For every natural `n`, `ST=TS=I`, `PT=TQ` and `SP=QS`. No nonsingularity hypothesis is assumed. |
| `parity_relation` | For every `n`, real matrix `J` and real scalar `a`, the hypothesis `JP=a(PJ)` implies `(SJT)Q=a Q(SJT)`. The equivariance of a differential model is not a conclusion. |
| `anticommuting_blocks` | For every `n,J` with `JP=−PJ`, blocks 11 and 22 of `SJT` are zero matrices. Other blocks need not be invertible or nonzero. |
| `commuting_blocks` | For every `n,J` with `JP=PJ`, blocks 12 and 21 of `SJT` are zero. This applies to any real matrix satisfying this equation; no Hessian identification is assumed or proved. |
| `parity_determinant` | For every `n,J`, `det(SJT)=det J`. |
| `off_diagonal_determinant` | For all `C,D : Square n`, `det [[0,C],[D,0]] = (−1)^n det C det D`. No invertibility assumption; empty blocks at `n=0` are allowed. |
| `anticommuting_determinant` | Under `JP=−PJ`, `det J = (−1)^n det(block12(SJT)) det(block21(SJT))`. This also needs no nonsingularity assumption. |
| `reflection_increment` | For all paired real vectors `x,v`, define `R(x)=1−Px` componentwise. Then `R(x+v)−R(x)=−Pv`. This is an exact affine increment identity, without derivatives, feasibility or stationarity assumptions. |
| `reflection_parity` | For all `x,v`, `R(x+v)−R(x)=v` iff `Pv=−v`, and `R(x+v)−R(x)=−v` iff `Pv=v`. Thus the preserving linear directions are coordinate-odd and the sign-reversing directions are coordinate-even. For the zero vector both equations hold; no assertion of actual symmetry breaking for zero, or about a nonsymmetric basepoint, is made. |
| `boundary_determinants` | For every real `L`, the explicit matrices `Me` and `Mo` below have determinants `2L(L+2)(2L−1)` and `2L(L+2)(2L+1)`, respectively. |
| `boundary_positive` | For all real `L≥4`, both determinants are strictly positive, hence nonzero. |
| `paired_coordinate_actions` | For every `n,v,i : Fin n`, `(Pv)_left=v_right`, `(Pv)_right=v_left`, `(Tv)_left=v_left+v_right`, `(Tv)_right=v_left−v_right`. This fixes the actual coordinate meaning. |
| `boundary_correction` | For every natural `L≥4`, `B=diag(Me,Mo)` has strictly positive determinant. Every real residual vector `b : Fin 2 ⊕ Fin 2 → ℝ` has exactly one real coefficient vector `a` with `Ba=b`. To cancel a residual use `b=−residual`. |
| `root` | Literal conjunction of all 13 universally quantified interfaces above, with the same implicit/explicit binders. It introduces no extra premise. |

The boundary matrices are the following explicit real arrays:

`Me(L) = [[L, L+2], [L(L−1)(L−2), L(L+1)(L+2)]]`.

`Mo(L) = [[L, L+2], [L(L+1)(L−2), L(L+2)(L+3)]]`.

`boundary_full L` is the 4 by 4 block diagonal matrix `diag(Me(L),Mo(L))`, ordered by parity sectors. The determinant identities hold for all real `L`; positivity is proved for real `L≥4`; the correction theorem quantifies over every natural `L≥4` and in particular covers all even natural indices in the supplied core argument. Evenness is not needed for these algebraic statements. Values `L=0` can make the matrices singular, so no unrestricted invertibility is claimed.

## Relationship to the supplied materials

The Jacobian part supports section 2 of `proof_audit_round11_20260925.md`, conditional on the differential identity `JP=−PJ` at the relevant point and on using exactly this paired coordinate convention. It proves the sign in the determinant formula for all natural sizes. It does not prove that any concrete program computes `J`, applies this change of basis, measures the intended residual or returns correct derivatives.

The boundary part supports the algebra of section 4, equation (4), of `cofinite_all_orders_proof.md`. The four polynomial directions, their actual boundary traces, and the invertible residual-coordinate change leading to `diag(Me,Mo)` are not formalized here. The displayed matrices are inputs defined by their entries, not results obtained by formal differentiation. The correction theorem supplies real finite-dimensional solvability for those matrices. Complex residual splitting, right-inverse continuity and convergence of correction coefficients remain outside this Lean packet.

Not formalized: the full ODE, differentiability of spectral residuals, Python finite differences/clipping/normalization, interval or floating-point numerical correctness, the supplied analytic SL example, Sobolev spaces, operator/fractional domains, polynomial-core density, Fourier logarithmic sequences, critical traces, cofinite closures, Schauder/Riesz non-basis conclusions, or canonical research integration. No previous Lean success or external-report conclusion is accepted as a proof premise.

## Evidence policy

Only foundational axioms from the subset `{propext, Classical.choice, Quot.sound}` may appear in the actual root dependency closure. Author compilation is distinct from exact type comparison and from semantic review. All development failures and deliberate negative controls are preserved under immutable command labels. The installed verifier is used unchanged in direct mode with existing package artifacts, and no full Lake build or dependency download is authorized. Environment/module manifests point to the existing dependencies and record hashes instead of copying Mathlib.
