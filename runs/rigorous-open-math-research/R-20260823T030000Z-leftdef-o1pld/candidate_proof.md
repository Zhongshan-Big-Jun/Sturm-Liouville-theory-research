# Candidate Proof — O1'LD attack: L^2 descent of the left-definite density problem

Run: R-20260823T030000Z-leftdef-o1pld
Repair status: RIGOROUS_PARTIAL_RESULT (repaired after independent audit;
see Repair log at the end)

This run does NOT close the general O1'LD.  It produces new STRICT theorems
for the most transparent descent (s = 2, i.e. the descended space
L^2(-1,1)), a STRICT concrete non-density class, and an honest narrowing for
s = 3 (H^1 descent).  The general O1'LD remains open.  One formerly claimed
STRICT statement (cofinite-N density) is now explicitly NOT-YET-STRICT because
the required tail rigidity is not fully proved in this repair.

## 0. Setting inherited from the prior runs

- H^s = D(K_c^{s/2}) on L^2(-1,1), K_c f = -f'' + c f (c>0) with Krein BC.
- The sparse family p_n and the induced family q_n = K_c p_n:
  q_0 = c, q_1 = c x,
  q_{2m} = c x^{2m} - A_m x^{2m-2} + B_m x^{2m-4},
  q_{2m+1} = c x^{2m+1} - A'_m x^{2m-1} + B'_m x^{2m-3}   (m >= 2),
  with A_m = 2m(2m-1) + c m/(m-1), B_m = 2m(2m-3), and
  A'_m = 2m(2m+1)+c m/(m-1), B'_m = 2m(2m-1).
- The sparse index set is D = {0,1} ∪ {4,5,6,...}.
- For s = 2, K_c : H^2 -> L^2 is an isometric isomorphism (prior L3).  A closed
  subspace V ⊆ H^2 corresponds to W = K_c V ⊆ L^2, and q_n ∈ W iff p_n ∈ V.
  Density in V is equivalent to density of {q_n : n ∈ N} in W, N = {n : q_n ∈ W}.

## 1. STRICT — finite-support moment rigidity in L^2

### Lemma 1 (finite deletion of monomials is total in L^2(-1,1))
Let F ⊆ N_0 be finite.  Then
  span{x^k : k ∉ F}
is dense in L^2(-1,1).

Proof.
The Müntz–Szász theorem in its L^p form states the following.  If Λ = {λ_n} is
an increasing subset of [0,∞) whose positive elements satisfy Σ_n 1/λ_n = ∞,
then {x^{λ_n}} is dense in L^p(0,1) for every 1 ≤ p < ∞.  This is the
Lebesgue-measure statement on (0,1); it is not used in a general
finite-Borel-measure form, and no such form is being relied on here.

Split f ∈ L^2(-1,1) into its even and odd parts interleaved.

*Even part.*  Write f_e(x) = f(x)+f(-x) (or equivalently f_e(x) = g(x^2)).
Put
  h(y) = y^{-1/4} f_e(√y),  y ∈ (0,1).
Then
  ∫_{-1}^1 |f_e(x)|^2 dx = ∫_0^1 |h(y)|^2 dy,
so h ∈ L^2(0,1) with Lebesgue measure.  Moreover, for every m ≥ 0,
  ∫_{-1}^1 f_e(x) x^{2m} dx
  = ∫_0^1 f_e(√y) y^{m-1/2} dy
  = ∫_0^1 h(y) y^{m-1/4} dy.
If the set of deleted even moments is finite, the remaining exponents
  Λ_e = { m - 1/4 : 2m ∉ F, m ≥ 1 }
have divergent reciprocal sum (deleting finitely many terms does not affect
divergence; the exponents are all positive for m ≥ 1).  Applying the L^2
Müntz–Szász theorem on (0,1) to {y^{λ} : λ ∈ Λ_e}, the monomials y^{m-1/4}
for the kept even indices m ≥ 1 span a dense subspace of L^2(0,1).  The m = 0
case, if it is kept, gives the extra condition ∫ f_e dx = 0; this extra
condition is consistent with the same conclusion f_e = 0.  Therefore f_e = 0.

*Odd part.*  Write f_o(x) = x h_o(x^2) (which is the general odd element of
L^2).  Put
  t(y) = y^{1/4} h_o(y).
Then
  ∫_{-1}^1 |f_o(x)|^2 dx = (1/2) ∫_0^1 |h_o(y)|^2 y^{1/2} dy
  = (1/2) ∫_0^1 |t(y)|^2 dy,
so t ∈ L^2(0,1).  Moreover,
  ∫_{-1}^1 f_o(x) x^{2m+1} dx
  = ∫_0^1 h_o(y) y^{m+1/2} dy
  = ∫_0^1 t(y) y^{m+1/4} dy.
If the deleted odd moments are finite, the remaining exponents
  Λ_o = { m + 1/4 : 2m+1 ∉ F, m ≥ 0 }
have divergent reciprocal sum.  The same L^2 Müntz–Szász argument gives
f_o = 0.  Hence f = 0.  qed

### Corollary 2 (finite-support L^2 moment sequences are trivial)
If f ∈ L^2(-1,1) and the set
  {k ∈ N_0 : (f,x^k)_{L^2} ≠ 0}
is finite, then f = 0.

Proof.  Let F be the finite support.  Then f is orthogonal to x^k for every
k ∉ F.  By Lemma 1 those monomials span a dense subset of L^2.  Hence f = 0.
qed

This is the main new tool for the L^2 descent.  It is a sharp difference from
the diagonal H_beta or banded H_lambda spaces used in the previous O1' subclasses:
in those spaces the finite run vector (e.g. M_2 = 1) was realizable by a basis
element; in L^2 no nonzero finite-support moment vector is realizable.

## 2. L^2 moment bounds and the actual q_n recurrences

### Lemma 3 (Cauchy–Schwarz moment bound; linear growth is not realizable)
Let f ∈ L^2(-1,1) and M_k = (f,x^k)_{L^2}.  Then
  |M_k| <= ||f||_2 * ||x^k||_2 = ||f||_2 sqrt(2/(2k+1)).
Consequently, a moment sequence of the form M_k = t * floor(k/2) for all k in
an infinite arithmetic progression of one parity and t ≠ 0 cannot be the moment
sequence of any f ∈ L^2.

Proof.  This is Cauchy-Schwarz plus ||x^k||_2^2 = 2/(2k+1).  The linear growth
of floor(k/2) eventually exceeds C k^{-1/2}.  qed

REMARK (repaired).  Lemma 3 is a true general L^2 fact, but it does NOT by
itself identify the obstruction in the s = 2 descent.  The equations obeyed by
the moments of an f orthogonal to the kept q_n are the three-term q_n
recurrences
  c M_{2m}   = A_m M_{2m-2} - B_m M_{2m-4},
  c M_{2m+1} = A'_m M_{2m-1} - B'_m M_{2m-3},
NOT the two-term run recursion M_k = (floor(k/2)/floor(b/2)) M_b used in the
DensBC O1 run algebra.  All uses of the DensBC O1 run decomposition in the
L^2/H^1 descent have therefore been removed.

### Claim 4 (tail L^2 rigidity, NOT-YET-STRICT)
Let f ∈ L^2(-1,1), and suppose that for some m0 ≥ 2 the even recurrences
  c M_{2m} = A_m M_{2m-2} - B_m M_{2m-4}     (m ≥ m0)
and the odd recurrences
  c M_{2m+1} = A'_m M_{2m-1} - B'_m M_{2m-3}  (m ≥ m0)
hold for all m ≥ m0.  Then all moments M_k vanish.

This is the tail version of the SL_h2 growth lemma.  The intended proof is:
assume a nonzero solution of one parity tail recurrence.  The recurrence has
a dominant solution with factorial growth, which contradicts
|M_k| <= C k^{-1/2}.  If the initial pair is not the exceptional minimal
(harmonic) solution, factorial growth is immediate.  The remaining case is a
bounded or polynomially decaying minimal solution; that case is not killed by
the simple Cauchy-Schwarz bound and requires an additional argument using the
orthogonal-polynomial (Legendre/Jacobi) coefficient representation of the
would-be L^2 function.  In the present repair this extra step is not fully
proved.  Consequently Claim 4 is stated as a plausible structural claim, but
it is NOT registered as STRICT.

REMARK.  The stronger naive assertion "any nonzero initial pair leads to
moments that grow too fast" is false as a pure sequence statement: the
recurrence also has a minimal solution with polynomial decay.  The correct
open target is the L^2-realizable version above, i.e. such a minimal solution
must not be the moment sequence of an L^2 function.  That exclusion is not
established in this repair.

## 3. Cofinite-N density theorem (NOT-YET-STRICT)

### Theorem 5 (cofinite-N theorem, L^2 descent, NOT-YET-STRICT)
Let N ⊆ D.  If D \ N is finite, then
  span{ q_n : n ∈ N }
is dense in L^2(-1,1).

Proof attempt.
1. Let f ∈ L^2 be orthogonal to all q_n for n ∈ N.  Define M_k = (f,x^k)_{L^2}.
   The equations (f,q_n)=0 become:
   - if 0 ∈ N, c M_0 = 0;
   - if 1 ∈ N, c M_1 = 0;
   - if 2m ∈ N (m >= 2):
       c M_{2m} - A_m M_{2m-2} + B_m M_{2m-4} = 0;
   - if 2m+1 ∈ N (m >= 2):
       c M_{2m+1} - A'_m M_{2m-1} + B'_m M_{2m-3} = 0.
2. Since D \ N is finite, there is an R such that every n >= R in D lies in N.
   On each parity, all equations from some m0 onward hold.  By Claim 4 (tail
   L^2 rigidity), if that claim were established, both parity solutions would
   vanish.  In particular the initial tail pairs would have to be zero, and by
   backward propagation all moments vanish.
3. Once all moments vanish, Corollary 2 gives f = 0 (or Weierstrass gives the
   same conclusion).
4. Hence the orthogonal complement of span{ q_n : n ∈ N } would be {0}, giving
   density.

Status.  The proof is conditional on Claim 4.  Because Claim 4 is not yet
strict, Theorem 5 is NOT-YET-STRICT.  It is no longer based on the DensBC O1
run algebra.  The statement is likely true, but it is not registered as a
proved theorem in this run.

### Corollary 6 (proper V in H^2 has non-cofinite kept set, NOT-YET-STRICT)
Let V ⊆ H^2 be a closed subspace and N = {n ∈ D : p_n ∈ V}.  If D \ N is finite,
then V = H^2.  Equivalently, every proper closed V ⊆ H^2 excludes infinitely many
sparse polynomials p_n.

Proof.  Conditional on Theorem 5.  By the isometry K_c : H^2 -> L^2, if D \ N
is finite then Theorem 5 says { K_c p_n : n ∈ N } is dense in L^2.  Therefore
span{ p_n : n ∈ N } is dense in H^2.  Since V is closed and contains all those
p_n, V = H^2.  qed (conditional)

This corollary retains the same NOT-YET-STRICT status as Theorem 5.

## 4. STRICT — parity decomposition of the L^2 descent

### Theorem 7 (parity split)
Let W be a closed subspace of L^2(-1,1), let E and O be the even and odd
subspaces, and set
  N_e = { n ∈ D : n even, q_n ∈ W },
  N_o = { n ∈ D : n odd, q_n ∈ W }.
Then
  closure(span{ q_n : n ∈ N })
  = closure(span{ q_n : n ∈ N_e }) ⊕ closure(span{ q_n : n ∈ N_o }).

Proof.  Every q_n is either even or odd; E ⊥ O.  Hence the two subspaces
A = span{ q_n : n ∈ N_e } and B = span{ q_n : n ∈ N_o } are orthogonal, and
their algebraic span is span{ q_n : n ∈ N }.  In a Hilbert space, the closure of
the sum of two orthogonal subspaces is the direct sum of their closures, so
closure(A + B) = closure(A) ⊕ closure(B).  qed

### Corollary 8 (density for parity-invariant W)
If W is parity-invariant, i.e. W = (W ∩ E) ⊕ (W ∩ O), then
  closure(span Q_sp) = W
iff
  closure(span{ q_n : n ∈ N_e }) = W ∩ E
  and
  closure(span{ q_n : n ∈ N_o }) = W ∩ O.

This decomposition isolates the parity structure of the remaining O1'LD.  The
general non-parity-invariant case still has the extra coupling encoded in W.

## 5. STRICT — concrete non-density: W = ker μ_4 in L^2 (s = 2)

### Theorem 9 (mu_4 example)
Let c > 0.  In H^2 define the bounded functional
  L(f) = ∫_{-1}^1 (K_c f)(x) x^4 dx,
and let V = ker L, a closed codimension-one subspace of H^2.  Then:

  (i) N = {1} ∪ {2m+1 : m >= 2} (the odd sparse indices; p_0 is excluded).
  (ii) closure(span Q_sp) = the odd subspace of H^2, which is strictly smaller
       than V.
  (iii) Hence closure(span Q_sp) ≠ V; density fails.

Proof.
1. Work in W = K_c V = ker μ_4 ⊂ L^2, μ_4(y) = ∫ y x^4.
2. For every odd n, q_n is an odd polynomial, so μ_4(q_n) = 0 by parity.  Thus
   every odd q_n ∈ W.
3. q_0 = c, hence μ_4(q_0) = 2c/5 ≠ 0, so p_0 ∉ V.
4. For n = 2m (m >= 2), q_{2m} is even and
     μ_4(q_{2m}) = 2c/(2m+5) - 2A_m/(2m+3) + 2B_m/(2m+1)
                 = -2(8cm^2 + 10cm + 3c + 32m^3 + 48m^2 - 80m)
                   / ((m-1)(2m+1)(2m+3)(2m+5)).
   The numerator bracket is positive for m >= 2 (it equals
   32m^3+48m^2-80m = 16m(2m+5)(m-1) >= 0 plus strictly positive c-terms), so
   μ_4(q_{2m}) < 0.  Hence no even sparse polynomial lies in V.
   This exact formula is implemented in reproducibility/o1pld_l2_mu4.py.
5. The odd family {q_1} ∪ {q_{2m+1} : m >= 2} is dense in the odd subspace of
   L^2.  Let f ∈ L^2_odd be orthogonal to all of them.  Then q_1 gives
   c M_1 = 0.  The odd recurrences for m >= 2 give
     M_{2m+1} = M_3 u_m     (m >= 1),
   where u_1 = 1, u_0 = 0 and u_m satisfies the SL_h2 odd growth lemma
     u_m >= (4/c)^{m-1} m!     (m >= 1).
   If M_3 ≠ 0, then |M_{2m+1}| grows factorially, contradicting
   |M_{2m+1}| <= ||f||_2 sqrt(2/(4m+3)).  Hence M_3 = 0, all odd moments vanish,
   and f = 0 (Weierstrass).  Thus the odd sparse subfamily is dense in the odd
   subspace.  Its preimage is dense in the odd subspace of H^2.
6. V contains the odd subspace of H^2, and also contains every even f ∈ H^2 with
   μ_4(K_c f) = 0.  The even fibre is an infinite-dimensional hyperplane in the
   even subspace, and it is not contained in the odd subspace.  Since
   closure(span Q_sp) is contained in the odd subspace, it is a proper subset
   of V.  qed

This is a new explicit non-density example for s = 2, with a finite-moment
(not just boundary-value) constraint.  It complements the boundary constraint
V = ker Δ from the prior run.

## 6. H^1 descent (s = 3): downgraded claim

In the s = 3 descent, the base space is H^1 and the moments are M_k = (w,x^k)_1.
The prior H3 proof gives the polynomial moment bound
  |M_k| <= C(c, ||w||_{H^1}) sqrt(k).           [prior result, STRICT]

However, the earlier candidate proof asserted that an "infinite run" (whose
H^1 moments grow linearly) is never realizable in H^1.  That conclusion was
based on the DensBC O1 linear run model, which is not the actual H^1 q_n
moment recurrence.  No precise tail-recurrence inadmissibility result for
H^1 has been proved in this run.  Therefore the H^1 infinite-run inadmissibility
claim is downgraded:

  EVIDENCE / PLAUSIBLE (not strict): the H^1 moment bound alone supports the
  plausibility that unbounded tail solutions of the H^1 recurrences are not
  realizable, but a proof is not supplied.

The finite-support rigidity of Corollary 2 does NOT automatically transfer to
H^1.  EVIDENCE (not proof): finite-dimensional numerical projections in H^1 for
the deleted degree 2 show a residual of order 0.06 that did not visibly decrease
in the tested range N = 20..80.  Because the L^2 analogue only decreases very
slowly (logarithmically), this is not conclusive.  We therefore do NOT assert
a cofinite-N density theorem for s = 3, and we leave the finite-run
realizability question open.

## 7. Honest remaining core

For s = 2, the remaining O1'LD is now precisely:

  For an arbitrary closed W ⊆ L^2 (equivalently V ⊆ H^2), and the parity-split
  kept sets N_e, N_o, decide whether the closure of
  closure(span{ q_n : n ∈ N_e }) ⊕ closure(span{ q_n : n ∈ N_o })
  equals W.

The new STRICT facts narrow this:
  (a') the finite-support moment rigidity (Corollary 2) is STRICT;
  (b') the parity decomposition (Theorem 7) is STRICT;
  (c') the μ_4 example (Theorem 9) is STRICT;
  (d') the cofinite-N density theorem would follow from the tail rigidity
       Claim 4, but Claim 4 is NOT-YET-STRICT, so the cofinite-N theorem is
       not registered strict.  If that claim is later proved, then proper V in
       H^2 cannot have cofinite kept set.

The general criterion remains OPEN.  For s = 3, the parity decomposition
carries over, but the infinite-run inadmissibility and finite-run realizability
questions are open (the former is EVIDENCE/plausible only).

## Repair log

- Lemma 1: rewritten with explicit even/odd substitutions to Lebesgue L^2
  (h(y)=y^{-1/4} f_e(√y), t(y)=y^{1/4} h_o(y)) before applying the L^p
  Müntz-Szász theorem.  Removed the invalid citation of a general
  finite-Borel-measure Müntz-Szász statement.
- Section 2: removed every use of the DensBC O1 two-term run decomposition in
  the L^2/H^1 descent.  The actual three-term q_n moment recurrences are now
  stated explicitly.
- Claim 4: tail version of the SL_h2 growth lemma stated.  It is marked
  NOT-YET-STRICT because the exceptional minimal solution is not fully
  excluded in this repair.
- Theorem 5 (cofinite-N density): rewritten to use the tail recurrence/Claim 4
  and the finite-support rigidity; status downgraded from STRICT to
  NOT-YET-STRICT.
- Corollary 6: downgraded to NOT-YET-STRICT.
- Theorem 9: odd-density step replaced by the SL_h2 odd growth lemma with
  M_1=0 from q_1; changed the index set to m >= 2.  The theorem remains STRICT.
- Section 6 (H^1): the infinite-run inadmissibility claim is downgraded from
  STRICT to EVIDENCE/plausible; no precise tail-recurrence proof is claimed.
- Obligation graph and final report updated to reflect the repaired statuses.
