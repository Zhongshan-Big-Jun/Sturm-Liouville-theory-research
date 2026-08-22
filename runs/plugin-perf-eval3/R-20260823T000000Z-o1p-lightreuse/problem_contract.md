# Problem Contract: DensBC O1' general non-diagonal H (Round 3 light-reuse)

## Statement (normalized from PROBLEM-O1P-GENERAL.md)

Let H be a Hilbert space in which the monomials Pi = span{x^k : k >= 0} are
dense and the moment functionals M_k(w) = <w, x^k>_H are well defined.  For
finite r, let v_1, ..., v_r in H and set

    V = { w in H : <w, v_j>_H = 0 for all j = 1..r }.

The sparse family is

    p_0 = 1,  p_1 = x,
    p_{2m} = x^{2m} - (m/(m-1)) x^{2m-2},   m >= 2,
    p_{2m+1} = x^{2m+1} - (m/(m-1)) x^{2m-1}, m >= 2.

Let N = { n : p_n in V } and Q_sp = { p_n : n in N }.

Reduced core O1': decide, from the run structure determined by N and the
membership data, whether closure(span Q_sp) = V.

## Positions and outside scope

- Generic H and arbitrary v_j are in scope for the general problem.
- This run does NOT claim to close general O1'.  It closes the new
  structured subclass H_{beta,lambda} with finite polynomial representers.
- Numerical evidence is never used as proof in this run.

## Completion criteria (for this run)

1. Produce a STRICT exact O1' criterion for a new family of non-diagonal H
   beyond the already closed H_beta and H_lambda subclasses.
2. Show that the new criterion regresses correctly to both prior subclasses.
3. Keep the honest global status: general O1' remains open.

## Forbidden moves

- Do not cite numerical checks as proof of a general theorem.
- Do not silently change the sparse family, the definition of V, or the
  reduced core.
- Do not claim closure of general O1' or of the general moment-problem core.
