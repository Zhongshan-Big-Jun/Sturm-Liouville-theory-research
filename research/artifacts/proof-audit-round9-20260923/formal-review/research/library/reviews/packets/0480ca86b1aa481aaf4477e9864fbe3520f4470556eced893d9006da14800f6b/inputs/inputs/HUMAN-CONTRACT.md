# Round 9 local Lean author contract

This contract describes the submitted candidate, not an independent acceptance. The precise machine type is `positive-contract.json`; its declaration is `AuditRound9.local_root` in `project/AuditRound9.lean`. Its type is a conjunction of 15 universally quantified interfaces, with no top-level assumed mathematical conclusions.

## F01: finite real Euclidean projection

For every natural n, b and A in R^n (represented by `Fin n → ℝ`), define dot(b,A) = sum_i b_i A_i. Define P_A(b) by an explicit branch: b when A=0, otherwise b - [dot(b,A)/dot(A,A)] A.

Clauses 1-4 assert dot(P_A(b),A)=0 for all inputs; P_0(b)=b; A≠0 implies dot(A,A)≠0 and the stated nonzero-branch formula; tangent inputs are fixed and P_A is idempotent. Real positivity of squares discharges the denominator fact. The empty coordinate set n=0 is included and uses the zero branch. No nonzero-normal assumption is hidden in the universal tangency assertion.

Application boundary: A must be the vector of block integrals A_i=integral_{I_i} f; proving that these integrals equal the finite coefficients used in a program is external to this file. No integration, quadrature accuracy, stationarity, Hessian definiteness or infinite-dimensional Hilbert projection is claimed. The optional width-weighted projection is not selected. This file proves the stated Euclidean coefficient formula, tangency and idempotence; it does not add a separate distance-minimization theorem.

## F03: linear normalization correction

For any real module V with additive commutative group structure (V : Type), any real linear functional L:V→R, real a and u,v0 in V, define v=v0-(a/2+L(v0))u. Clause 5 asserts L(u)=1 implies L(v)=-a/2.

Clause 6 adds any real module W and real linear map K:V→W: if K(u)=0, then K(v)=K(v0). The latter needs no assumption L(u)=1. Both are algebraic interfaces; real function spaces fit the carrier universe but no analytic hypotheses or spectral theorems are encoded. The premise L(u)=1 is explicit and satisfiable, e.g. V=R with L the identity and u=1.

Application boundary: identifying L(w)=integral rho*u*w, constructing v0 with a reduced inverse, identifying the kernel of the differential operator, existence/differentiability of eigenfunctions, spectral series convergence and the second-variation formula remain unformalized. The candidate does not prove any infinite-dimensional eigenfunction expansion.

## F04: actual 2x2 normalized matrices and physical scaling

All matrices are `Matrix (Fin 2) (Fin 2) ℝ`, with Mathlib matrix multiplication and natural powers. J=diag(1,-1). The definitions use the actual entries

N_cell(s,C,S) = [[C^2-S^2/s, (s+1)SC/s], [-(s+1)SC, C^2-sS^2]],
N_end(C,S) = [[C,S],[-S,C]],
N_n(s,C,S)=N_end(C,S) N_cell(s,C,S)^n.

Clauses 7-9 prove N_cell(s,-C,S)=J N_cell(s,C,S) J, N_end(-C,S)=-J N_end(C,S) J, (J M J)^n=J M^n J, N_n(s,-C,S)=-J N_n(s,C,S) J, and equality of the (0,1) entries for every n. These algebraic equalities hold for arbitrary real C,S; the Lean field convention at s=0 is not a physical-density claim.

With C=cos y, S=sin y, define G_n(s,y)=(N_n)_{01}. Clause 10 uses the actual Mathlib trigonometric functions to prove G_n(s,pi-y)=G_n(s,y). This is derived from the matrices, not assumed.

Let P_w=diag(1,w) and Q_w=diag(1,w^(-1)). Define T_w(M)=P_w M Q_w. Clause 11 proves, when w≠0,
T_w(E) T_w(M)^n = T_w(E M^n),
and (T_w(M))_{01}=M_{01}/w. The entry formula itself needs no nonzero premise, but the product bridge does. This is the conjugation appropriate to the physical state (u,u'). It gives end-matrix entries [[C,S/w],[-wS,C]] and the original cell entries [[C^2-S^2/s,(s+1)SC/(sw)],[-w(s+1)SC,C^2-sS^2]] for nonzero s,w.

Define w(s,t,y)=y/(st). Define F_n(s,t,y) as the (0,1) entry of the actual product T_w(N_end) T_w(N_cell)^n, with w re-evaluated at each y. Clause 12 proves F_n=G_n/w under s≠0,t≠0,y≠0. Thus G_n=w F_n on this domain.

Clause 13 is a separately exposed conversion lemma: for an arbitrary real function G with the explicit premise G(p-y)=G(y), and s≠0,t≠0,y≠0,p-y≠0, G(p-y)/w(s,t,p-y)=[y/(p-y)]G(y)/w(s,t,y). This conditional lemma does not supply symmetry on its own. Clause 14 applies the already proved matrix/trigonometric symmetry, with p=pi, to obtain
F_n(s,t,pi-y)=[y/(pi-y)] F_n(s,t,y)
under s≠0,t≠0,y≠0,pi-y≠0. No reflection premise remains in this actual physical theorem.

Clause 15 specializes to s>0,t>0,0<y<pi, proving the factor is positive, the physical reflection identity, and equivalence of the reflected zero tests. Natural n=0 is included; the application n≥1 is a specialization. The phase width t is a free positive parameter: substituting t_n=1/((n+1)s+n) requires that elementary positive-width fact, not a different transfer proof.

Application boundary: the ODE fundamental-solution derivation, eigenvalue identification, root count 2n, root multiplicity preservation, Chebyshev/Jacobi formulas, the c_n limit, and global extremality are not formalized here. In particular, zero-set reflection is proved but simple-root transport is not claimed as a formal theorem.

## Evidence and review boundaries

The author uses the unmodified installed lean-verify 2.0.1 `verify_lean_project.py` against existing Lean 4.31.0 and pinned Mathlib fabf563a7c95a166b8d7b6efca11c8b4dc9d911f, without a full build or cache fetch. It freshly compiles local imports in its output directory, compares the complete expected type, extracts transitive dependencies and axioms, and binds loaded artifacts. This is the Lean compiler trust boundary, not a second kernel or a semantic acceptance.

Negative controls request (i) the same root with the normalization sign flipped in the expected type, (ii) a nonexistent root name, and (iii) a real compiled declaration with an explicit, undischarged arbitrary premise H. The third is checked against the unconditional conjunction. No sorry or user-added axiom is used in these sources. The plugin's internal expected-type comparison declaration is a synthetic probe, excluded by its documented closure policy; it is not part of the candidate.

Independent blind readback and comparison with this human contract are pending with the coordinator. `formal-only/` must be supplied without this document, author prose, original reports or intended-theorem descriptions. It contains only formal declarations/definitions and environment facts extracted from actual compilation.
