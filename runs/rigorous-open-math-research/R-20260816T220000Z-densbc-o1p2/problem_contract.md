# Problem Contract: DensBC O1' — banded non-diagonal extension via H_lambda

Run ID: R-20260816T220000Z-densbc-o1p2
Task ID: Q-20260816-densbc-o1p2-F1A2B3C4
Upstream status verbatim: RIGOROUS_PARTIAL_RESULT
This-run status: RIGOROUS_PARTIAL_RESULT

## 1. Parent problem (O1')

Let H be a Hilbert space whose monomials Pi = span{x^k : k >= 0} are dense and
whose moment functionals M_k(w) = <w, x^k>_H are well defined.  For r >= 0
finite, let v_1, ..., v_r in H define

    V = { w in H : <w, v_j>_H = 0 for all j = 1..r }.

The sparse family is

    p_0 = 1,  p_1 = x,
    p_{2m} = x^{2m} - (m/(m-1)) x^{2m-2},   m >= 2,
    p_{2m+1} = x^{2m+1} - (m/(m-1)) x^{2m-1}, m >= 2.

Let N = { n : p_n in V } and Q_sp = { p_n : n in N }.  The reduced core O1' asks:

    Decide, from the run structure determined by N and the membership data,
    whether closure(span Q_sp) = V.

This is RIGOROUS_PARTIAL_RESULT: the diagonal H_beta + finite polynomial
constraint subclass was closed in R-20260816T210000Z-densbc-o1p, but general O1'
remains open.

## 2. Target of this run (chosen route: concrete banded non-diagonal example plus exact finite criterion for the example class)

We introduce a one-parameter Hilbert space H_lambda with a non-diagonal,
banded Gram matrix (bandwidth 1), and prove an exact finite linear algebra
criterion for O1' on H_lambda for finite polynomial representers.  We then
apply it to the single representer v_1 = x^4 and give a complete strict
decision for every lambda in (-1,1).

Definitions for H_lambda:

- Underlying space: l^2(N_0) with real orthonormal basis (e_k)_{k>=0}.
- Parameter: lambda in (-1,1).
- Monomials: x^k = e_k + lambda e_{k+1}.
- Gram matrix: G_{i,k} = <x^i, x^k> = delta_{i,k}(1+lambda^2) +
  delta_{|i-k|,1} lambda.  This is banded with bandwidth m = 1 and is
  non-diagonal for lambda != 0.
- Pi = span{x^k} is dense in H_lambda.
- Moment map: M_k(w) = <w, x^k> = w_k + lambda w_{k+1}, where w = (w_k).

The exact theorem to prove:

Theorem A (H_lambda finite-rank criterion).  Let v_j = sum_{i=0}^{d_j}
c_i^{(j)} x^i be real finite polynomials, j = 1..r.  Define V, N, runs, free
bases B and finite free bases B_fin as in the round-1 machinery.  Then

    closure(span Q_sp) = V
        <=>
    ker( T|_{B_fin} ) = {0},

where T is the r x B matrix

    T_{j,b} = sum_{i=0}^{d_j} c_i^{(j)} rho_b(i) 1_{i in R_b}

and rho_b is the run ratio (rho_b(b) = 1, rho_b(k) = floor(k/2)/floor(b/2)
for b >= 2, rho_b = 1 for b in {0,1}).

Theorem B (complete decision for v_1 = x^4).  For every lambda in (-1,1),
with H = H_lambda and V = ker <., x^4>, one has

    closure(span Q_sp) != V.

The proof is STRICT.  No numerical evidence is used.

## 3. Honesty and status

- All statements below are either labeled STRICT (proved in this run) or
  explicitly EVIDENCE/HEURISTIC.
- The exact H_lambda subclass (finite polynomial constraints, in particular
  v_1 = x^4) is fully decided.
- General O1', general banded H, and general non-diagonal H remain open.
- This run's status: RIGOROUS_PARTIAL_RESULT.
