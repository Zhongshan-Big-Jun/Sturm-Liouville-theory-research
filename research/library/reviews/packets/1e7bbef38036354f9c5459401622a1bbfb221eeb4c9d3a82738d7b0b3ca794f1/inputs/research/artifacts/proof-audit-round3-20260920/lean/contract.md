# Third-round local formal target contract

The informal contract is deliberately local. Scalars are real numbers and recurrence indices are natural numbers. The source is `lean-proof/SL/AuditRound3.lean`; 10 definitions and 24 theorem declarations are selected. The actual elaborated binders, not names or comments, determine the formal scope.

1. A solution includes u(0)=0, u(1)=1 and c*u(n+2)=A(n+2)*u(n+1)-B(n+2)*u(n) for all n. Existence by the defined recursion and uniqueness require c!=0.
2. The second-order decomposition retains B/c*(v-w). A lower bound needs c>0, B>=0 and v>=w. Local equality is equivalent to B=0 or v=w when c!=0 and the recurrence equation holds.
3. All-index assumptions c>0, B(k)>=0 and A(k)-B(k)>=c (k>=2) imply nonnegativity, monotonicity and the finite product lower bound for n>=1. B(k)=0 (k>=2), with c!=0, gives equality. No product equality at n=0 is claimed.
4. With c=1,A=3,B=2, the full actual sequence is 2^n-1. Its coefficient excess is zero and product bound is one. The strict gap holds at n+2, refuting a general product equality.
5. Perturbed A and B are explicit rational coefficient functions. Their exact difference includes delta*(c-(2m-2)*(2m-3)) for real m!=1. At c=3,m=4,delta=1, A=63,B=70 and gap=-7, whereas the old expression is 23.
6. The P2 targets prove rational identities for explicitly defined functions, cancellation under the displayed denominator assumptions, the complement factorization and exact values delta(2)=-36/7, delta(3)=1. They do not identify those functions with integrals or automatically discharge the denominator assumptions for all integer indices.

Excluded: polynomial differentiation to coefficient bridge, operator-domain membership, P2 norm/parity/integrals, boundedness and asymptotics, L2 incompleteness, Gamma identities, diagonal-series criterion, general completeness, the all-index 1/(8m) sufficient perturbation condition, and R3-F3 spectral/quotient arguments. Those remain analytic proofs where stated. No old SL module or Mathlib dependency is rebuilt here. Allowed foundational axioms: propext, Classical.choice, Quot.sound; no sorryAx, added axioms or unsafe constants in the inspected dependency closure.

Machine evidence includes the final author compiler/export logs and a separate coordinator replay. Blind readback receives only exported declarations/definitions and environment pins; a different semantic reviewer then compares that readback with this contract. Each approval is restricted to its explicit scope.
