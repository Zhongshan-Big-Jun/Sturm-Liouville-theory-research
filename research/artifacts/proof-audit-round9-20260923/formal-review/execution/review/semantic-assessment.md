# Independent semantic assessment of packet 0480ca86b1aa481aaf4477e9864fbe3520f4470556eced893d9006da14800f6b

This assessment uses the listed frozen inputs, the supplied readback as a translation to check, and the reviewer's newly compiled object. It does not use the supplied readback verdict as evidence of a proof. Execution conclusions are recorded separately in the replay evidence.

## Declaration and binder coverage

The reviewer read the complete candidate and all 59 compact types freshly exported by `ReviewerExport.lean`, including every implicit parameter, instance, explicit premise, and definition body. `declaration-comparison.json` compares every field of every frozen declaration against the fresh export. All 59 match exactly, including fully explicit types, universe lists, and all supplied definition values. The 25 source theorems and 13 definitions/abbreviations account for 38 entries; 21 generated auxiliaries account for the remainder. The supplied blind translation covers precisely the same 59 names.

For the projection declarations the dimension is an implicit natural in individual declarations and an explicit natural in root clauses. The vectors are `Fin n -> Real`, with the standard finite dot product and standard real operations. For the correction declarations, V and W are Type 0 carriers with separately quantified additive commutative group and real-module instances. They are not quantified over arbitrary universe levels. L and K are actual real linear maps. The normalization premise is L(u)=1; the independent equation-preservation premise is K(u)=0. The latter theorem does not require L(u)=1.

All matrix entries are real, both indices are `Fin 2`, and all relevant exponents are natural numbers, including zero. Matrix multiplication uses the actual Mathlib matrix instance, and the selected scalar entry is row 0, column 1. The two constant numeric helper proofs introduce no variables. The generated equation declarations repeat the full parameter and instance lists of their definitions.

The eight polymorphic simplifier helpers were checked separately: three require Zero, the specified OfNat instance for 2, 3, or 4, and NeZero of that numeral; the product helper requires Mul, Zero, NoZeroDivisors and both factors nonzero; the natural-power helper requires MonoidWithZero, IsReduced and a nonzero base; the integer-power helper requires GroupWithZero and a nonzero base; the successor-cast helper requires AddMonoidWithOne and CharZero; the squared-dot helper requires a finite index type, Ring, LinearOrder and IsStrictOrderedRing. Their conclusions are equalities between propositions, not extra unconditional axioms. Natural and integer exponent domains are different and retained. No commutativity assumption was added to the ordered-ring helper. The two parameter-free proof helpers are Nat.AtLeastTwo(1+1) and NeZero(1+1).

`root-clause-binders.json` records the actual AST of each of the 15 root conjuncts. The root has no outer binders. Root clause 11 places both product transport and the entry formula under omega != 0, while the standalone entry theorem is unconditional. Clause 13 has the explicit pointwise premise G(p-y)=G(y). Clauses 10 and 14 do not assume their reflection conclusions: clause 10 is derived from the matrices and actual sine/cosine identities, and clause 14 uses it to discharge clause 13's premise.

## Finite integral-normal coefficient interface

Source comparison: `inputs/analytic-repair.md`, V2, especially lines 60-74; `inputs/HUMAN-CONTRACT.md`, F01; candidate lines 9-39 and root clauses 1-4.

For nonzero A in a finite real coordinate space, sum A_i^2 cannot vanish, so the explicit denominator is nonzero. Substitution gives dot(P_A(b),A)=dot(b,A)-dot(b,A)=0. For A=0 the definition returns b without division. An already tangent b is fixed, and applying that fact to the projected vector proves idempotence. For n=0 every function is the zero vector: the zero branch applies, the sum is empty, and the nonzero-A premise is unsatisfiable. No dimension or nonzero-normal assumption has been dropped from a theorem requiring it.

The analytic normal is A_i=integral over I_i of f, not the block average A_i/length(I_i). The candidate's arbitrary A can represent those integral coefficients. The identification of integrals, block endpoints, program data and quadrature remains external. Neither the optional width-weighted metric nor a separate minimum-distance characterization is selected or proved. This is a finite algebraic interface; it proves no infinite-dimensional Hessian sign or feasibility at a saturated density constraint.

## Linear normalization and kernel correction

Source comparison: `inputs/analytic-repair.md`, V1 lines 25-55; human contract F03; candidate lines 41-55 and root clauses 5-6.

Linearity gives L(v0-(a/2+L(v0))u)=L(v0)-(a/2+L(v0))*L(u)=-a/2 when L(u)=1. Independently, K(u)=0 gives K(v)=K(v0). These premises are explicit; L(u)=1 implies the normalization direction is nonzero, and is satisfiable in V=Real with identity L and u=1. There is no assumption of the desired corrected value. In the application, L(w)=integral rho*u_k*w and K is the differential operator on an appropriate domain; proving those identifications, producing v0 or establishing an analytic eigenfunction derivative is outside this file. No claim of uniqueness or convergence is extracted from the module interface.

## Normalized matrices, transport and physical reflection

Source comparison: `inputs/analytic-repair.md`, B1 lines 140-163; `inputs/SL_fixed_n_supremum.tex`, lines 76-129; human contract F04; candidate lines 57-189 and root clauses 7-15.

The fresh bodies have J=diag(1,-1), cell entries [C^2-S^2/s, (s+1)SC/s; -(s+1)SC, C^2-sS^2], end entries [C,S; -S,C], and ordered product end*cell^n. These coincide with the supplied analytic normalized entries; no scalar surrogate replaces the matrix product. Replacing C by -C changes exactly the required entries. J^2=I makes conjugation commute with every natural power, including the identity at n=0. The negative sign from the end matrix occurs once, independently of n. The 01 entry of -J*M*J is M01.

The actual functions Real.cos and Real.sin satisfy cos(pi-y)=-cos(y) and sin(pi-y)=sin(y). Thus the normalized scalar G reflects exactly. Arbitrary real s,C,S in the polynomial identities impose neither a unit-circle condition nor s != 0; Lean's total division at zero makes these broader algebraic statements meaningful without supplying a physical zero-density model.

For omega != 0, Q_omega*P_omega=I with P=diag(1,omega), Q=diag(1,omega^-1). Multiplication therefore transports end*cell^n to the physical product. Its entries are [a,b/omega; omega*c,d], which yields the analytic cell's top-right (s+1)SC/(s*omega) and lower-left -omega*(s+1)SC. The order of end and cell factors agrees with the source's column-state propagation. In particular the definition is T=P*N*Q, consistent with N=P^-1*T*P. It does not assert that the zero-frequency transformation is invertible.

The frequency is re-evaluated as y/(s*t) at each phase. With s,t,y nonzero, F=G/omega. At the reflected phase the additional premise pi-y != 0 is explicit, and division gives F(pi-y)=[y/(pi-y)]F(y). The general frequency_scaling lemma is conditional on a pointwise equality for arbitrary G; the physical theorem supplies that equality from the already proved trigonometric matrix theorem. For s,t>0 and 0<y<pi, the multiplier is positive and nonzero, so the two scalar zero tests are equivalent. At y=pi/2 the factor is 1. The endpoints 0 and pi are excluded; no analytic extension of the totalized definitions at zero frequency is asserted. The parameter n=0 remains included in the algebraic statements, with no claim of a positive root count there.

The physical application s=sqrt(R)>1 and t=1/((n+1)s+n)>0 specializes the contract's free positive s,t; positivity of that width is an elementary external substitution. ODE solution construction, identifying zeros with Dirichlet eigenvalues, preserving root multiplicity, counting 2n roots, Jacobi/Chebyshev formulas, candidate monotonicity and limits, and global extrema are not Lean conclusions of this source.

## Controls and trust scope

The wrong-sign expected clause demands +a/2 in place of -a/2. For example L=id, u=1, v0=0, a=2 makes the corrected value -1, not +1; the expected proposition is genuinely different. The missing-name control must fail specifically because AuditRound9.missing_root is absent. The conditional_root declaration has two extra binders H:Prop and pending:H, followed by the same conjunction. Its body is local_root: it does not prove an arbitrary H. The whole type differs from the unconditional root, despite the conjunction being available separately. Only completed fresh controls with these causes establish the requested control behavior.

The independently traversed exported root graph has 16,629 nodes and 378,242 recorded dependency edges, all resolved. Its only axiom nodes are propext, Classical.choice and Quot.sound. The synthetic expected-statement axiom is absent from both the root graph and the closure of the expected type's constants. Every one of the 59 freshly exported declarations reports only allowed axioms and is safe. These are fresh compiler/probe observations in the pinned artifact environment, not a second implementation of the kernel or a rebuild of all imported dependencies.

The blind dispatch/receipt/completion/report hashes are consistent, and the supplied spawn record says fork_context=false. That historical independence is coordinator-attested; this review did not seek conversations to strengthen the attestation. The supplied readback's lack of a compiler replay is not upgraded to one: the new replay and new export are distinct reviewer evidence.
