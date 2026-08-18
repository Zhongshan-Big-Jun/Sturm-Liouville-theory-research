# Candidate Proof: O1' on the shift-perturbed banded Hilbert space H_lambda

Run: R-20260816T220000Z-densbc-o1p2
Upstream status (verbatim): RIGOROUS_PARTIAL_RESULT
This-run status: RIGOROUS_PARTIAL_RESULT
  (The exact subclass "H_lambda with finite polynomial representers", including
   the single representer v_1 = x^4 for all lambda in (-1,1), is CLOSED in this
   run.  General O1' remains open.)

All statements below are STRICT.  No numerical evidence is used.

============================================================================
0. Notation and the space H_lambda
============================================================================
Let lambda in (-1,1).  Let H_lambda be the real Hilbert space l^2(N_0) with
orthonormal basis (e_k)_{k>=0}, and define monomials

    x^k = e_k + lambda e_{k+1},   k >= 0.

Then Pi = span{x^k : k >= 0} is dense in H_lambda: iterating e_j = x^j -
lambda e_{j+1} gives

    e_k = sum_{j=0}^{N} (-lambda)^j x^{k+j} + (-lambda)^{N+1} e_{k+N+1},

and the remainder has norm |lambda|^{N+1} -> 0.  Hence H_lambda satisfies (H1).

The Gram matrix is banded with bandwidth 1:

    G_{i,k} = <x^i, x^k>_H
            = delta_{i,k}(1 + lambda^2) + delta_{|i-k|,1} lambda.

For lambda != 0 this is a genuinely non-diagonal, non-coordinate Hilbert-space
structure; for lambda = 0 it reduces to the diagonal H_0 = l^2 with x^k = e_k.

For w = (w_k) in H_lambda the moments are

    M_k(w) = <w, x^k>_H = w_k + lambda w_{k+1}.

The moment map J: w -> (M_k(w))_{k>=0} is an isomorphism l^2(N_0) -> l^2(N_0).
Indeed J = I + lambda B, where B is the backward shift (Bw)_k = w_{k+1}; since
|lambda| < 1, I + lambda B is invertible with

    w_k = sum_{j>=0} (-lambda)^j M_{k+j}(w).

Both J and J^{-1} are bounded.  This explicit invertibility is the key new
tool: realizability of a moment sequence in H_lambda is exactly square
summability of that sequence.

Sparse family:

    p_0 = 1,  p_1 = x,
    p_{2m} = x^{2m} - (m/(m-1)) x^{2m-2},   m >= 2,
    p_{2m+1} = x^{2m+1} - (m/(m-1)) x^{2m-1}, m >= 2.

For finite polynomial constraints (standing assumption: r < infinity and
each d_j < infinity)

    v_j = sum_{i=0}^{d_j} c_i^{(j)} x^i,   j = 1..r,   c_i^{(j)} in R,

define V = { w : <w,v_j>_H = 0 for all j }, N = { n : p_n in V }, and
Q_sp = { p_n : n in N }.  The coefficients are real because H_lambda is a
real Hilbert space.

============================================================================
1. STRICT -- Kept set is cofinite and the run system is finite
============================================================================
Theorem 1.  Let v_j be finite polynomials as above and let D = max_j d_j + 1.
Then every n > D + 2 lies in N.  Consequently the run graph has finitely many
components, the free-base set B is finite, and on each parity there is exactly
one infinite run.

Proof.  For n >= 4 the support of p_n is {n, n-2}.  Since G is banded of
bandwidth 1,

    <v_j, p_n>_H = sum_{i=0}^{d_j} c_i^{(j)}
                   ( G_{i,n} - (m/(m-1)) G_{i,n-2} ).

If n > d_j + 3 then both n and n-2 are > d_j + 1, so G_{i,n} = G_{i,n-2} = 0
for every i <= d_j.  With D = max_j d_j + 1, every n > D + 2 = max_j d_j + 3
is kept.  The finitely many remaining indices (e.g. {0,1}) are checked
individually; only finitely many can fail to be kept.
Because all kept edges above D+2 are present on each parity, the tail of each
parity is one infinite run.  qed

Remark.  The threshold D = max_j d_j + 1 is one more than the round-1
threshold for diagonal H_beta; the +1 accounts for the bandwidth of G.

============================================================================
2. STRICT -- Exact O1' criterion on H_lambda
============================================================================
Define the run decomposition exactly as in R-20260816T210000Z-densbc-o1p:
vertices are degrees; on the even side an edge (2m-2, 2m) is present iff
2m in N (m >= 2); on the odd side an edge (2m-1, 2m+1) is present iff
2m+1 in N (m >= 2).  A run R is a connected component.  A free base b in B is
the least element of its run, except that b = 0 or b = 1 is free only when
that degree is not in N.  Let B_fin be the set of free bases whose run is
finite.

For a run R_b with least element b, define rho_b : R_b -> R by rho_b(b) = 1,
rho_b(k) = floor(k/2)/floor(b/2) for b >= 2, and rho_b(k) = 1 for b in {0,1}.
As in the round-1 proof, the kept recursions force, for every w in
V cap Q_sp^perp,

    M_k(w) = sum_{b in B} t_b rho_b(k) 1_{k in R_b},   t_b = M_b(w).

Theorem 2 (H_lambda finite-rank criterion).  With the above notation,

    closure(span Q_sp) = V
        <=>
    ker( T|_{B_fin} ) = {0},

where T is the r x B matrix

    T_{j,b} = sum_{i=0}^{d_j} c_i^{(j)} rho_b(i) 1_{i in R_b}

and T|_{B_fin} is the restriction to the finite-run columns.

Proof.  By upstream Theorem A, density holds iff V cap Q_sp^perp = {0}.  We
identify this obstruction space.

Let w in V cap Q_sp^perp.  The run lemma gives M(w) = sum_{b in B} t_b m_b,
where m_b is the pure run moment sequence.  Since w in H_lambda, M(w) is in
l^2 (J is an isomorphism onto l^2).  For an infinite run R_b, m_b is supported
on one parity and has m_b(k) ~ c k as k -> inf along that parity; hence
m_b is not in l^2.  By Theorem 1 each parity has at most one infinite run, so
if t_b != 0 for some infinite b then M(w) is not l^2, contradiction.  Thus
t_b = 0 for every infinite b.

Membership w in V is

    0 = <w, v_j>_H = sum_{i=0}^{d_j} c_i^{(j)} M_i(w)
      = sum_{b in B_fin} t_b sum_{i=0}^{d_j} c_i^{(j)} rho_b(i) 1_{i in R_b}
      = (T|_{B_fin} t)_j.

Thus every obstruction gives a nonzero (or zero) vector t in ker(T|_{B_fin}).

Conversely, let t in ker(T|_{B_fin}).  The finite-support sequence
M = sum_{b in B_fin} t_b m_b is in l^2, so w = J^{-1}M is in H_lambda and has
moments M.  By Theorem 1 each finite run lies strictly below the infinite tail
of its own parity, so M has finite support below both tails.  The run
recursions hold on all kept edges contained in finite runs; kept edges in the
infinite tails have M_n = M_{n-2} = 0 because both indices are above that
finite support.  Hence w in Q_sp^perp.  The identity above and
T t = 0 give w in V.  If 0 in N (resp. 1 in N), then M_0 = 0 (resp. M_1 = 0)
is consistent because no element of B_fin has a run containing 0 (resp. 1);
and conversely t_b = M_b(w) recovers t for every b in B_fin, so the two maps
are inverse by the density of Pi.  Thus V cap Q_sp^perp is isomorphic to
ker(T|_{B_fin}).  qed

This is a finite linear algebra criterion on H_lambda.  It generalizes the
round-1 kernel criterion: the diagonal H_beta summability condition is replaced
by the explicit H_lambda realizability rule "M in l^2", which is exactly why
infinite runs are inadmissible in H_lambda.

Corollary 3 (r = 0).  For H_lambda with no constraints, Q_sp is dense in
H_lambda.  Indeed N = all n, so B_fin = empty, and Theorem 2 gives density.

Proof.  Immediate.  qed

Remark.  The r = 0 case is a non-diagonal counterpart of the H_beta result
beta <= 3/2: in H_lambda the missing low monomials x^2 and x^3 are in the
closure of the sparse family, because the corresponding infinite run moment
vectors are not realizable (they grow linearly, hence are not in l^2) and
therefore cannot obstruct.

============================================================================
3. STRICT -- Complete decision for v_1 = x^4
============================================================================
Let lambda in (-1,1), H = H_lambda, r = 1, and

    v_1 = x^4.

Equivalently V = ker M_4.  Let A = 1 + lambda^2.  The representer moments are
a_k = <v_1, x^k> = G_{4,k}, so a_3 = lambda, a_4 = A, a_5 = lambda, and
a_k = 0 for all other k.

Theorem 4.  For every lambda in (-1,1),

    closure(span Q_sp) != V.

Proof.  First compute N.

For n = 0,1: a_0 = a_1 = 0, so 0,1 in N.

For n = 4: <v_1, p_4> = A - 2 G_{4,2} = A != 0, so 4 not in N.

For n = 5: <v_1, p_5> = G_{4,5} - 2 G_{4,3} = lambda - 2 lambda = -lambda.
Thus 5 in N if lambda = 0, and 5 not in N if lambda != 0.

For n = 6: <v_1, p_6> = G_{4,6} - (3/2) G_{4,4} = -(3/2) A != 0, so
6 not in N.

For n = 7: <v_1, p_7> = G_{4,7} - (3/2) G_{4,5} = -(3/2) lambda.
Thus 7 in N if lambda = 0, and 7 not in N if lambda != 0.

For n >= 8: G_{4,n} = G_{4,n-2} = 0, so n in N.

Hence:
- If lambda != 0: N = {0,1} union {8,9,10,...}.
- If lambda = 0: N = {0,1,5,7} union {8,9,10,...}.

Now compute the finite runs.

Case lambda != 0.  Even side: p_4 and p_6 are not kept, p_8 and all later
even p_n are kept.  The even runs are {0} (pinned, 0 in N), {2}, {4}, and
{6,8,10,...}.  Odd side: p_5 and p_7 are not kept, p_9 and all later odd p_n
are kept.  The odd runs are {1} (pinned), {3}, {5}, and {7,9,11,...}.
Thus

    B_fin = {2,3,4,5},   B_inf = {6,7}.

The single membership equation is M_4 = 0.  Its T row on B_fin is
(0,0,1,0), because the only finite run containing degree 4 is R_4 = {4}.
Hence e_2 = (1,0,0,0) lies in ker(T|_{B_fin}), so by Theorem 2 density fails.

Case lambda = 0.  Even side: p_8 and later even p_n are kept, so even runs
are {0} (pinned), {2}, {4}, and {6,8,10,...}.  Odd side: p_5, p_7, p_9, ...
are kept, so odd runs are {1} (pinned) and {3,5,7,9,...}.  Thus

    B_fin = {2,4},   B_inf = {3,6}.

The T row on B_fin is (0,1), and e_2 is in the kernel.  By Theorem 2 density
fails.

For a direct certificate, take t_2 = 1 and all other t_b = 0.  Then M = delta_2
(M_2 = 1, M_k = 0 for k != 2).  Since delta_2 in l^2, define

    w = J^{-1} delta_2 = lambda^2 e_0 - lambda e_1 + e_2.

Explicitly,

    M_0 = w_0 + lambda w_1 = lambda^2 - lambda^2 = 0,
    M_1 = w_1 + lambda w_2 = -lambda + lambda = 0,
    M_2 = 1,
    M_k = 0  for all k >= 3.

Thus w != 0, w in V (M_4 = 0), and w is orthogonal to every kept p_n: p_0 and
p_1 by M_0 = M_1 = 0; for n >= 8, M_n = M_{n-2} = 0.  In the lambda = 0 case
the additional kept p_5 and p_7 are also orthogonal because M_5 = M_7 =
M_3 = M_5 = 0.  Hence w in V cap Q_sp^perp, so Q_sp is not dense in V.  qed

The explicit obstruction is nonzero for every lambda in (-1,1); for lambda = 0
it is simply w = e_2.

============================================================================
4. STRICT -- Regression and comparison with round 1
============================================================================
- At lambda = 0, H_0 is the diagonal H_beta with beta = 0.  The constraint
  v_1 = x^4 is the coordinate constraint M_4 = 0.  The round-1/upstream
  coordinate criterion also gives non-density: the finite run {2} contains no
  constrained degree, so it is an obstruction.  CONSISTENT.
- For lambda != 0, the same obstruction persists, but the Hilbert space and
  the membership equation are non-diagonal: M_4(w) = w_4 + lambda w_5.
  The diagonal kernel criterion applied to H_0 would not see the lambda
  perturbation; the H_lambda criterion above is the correct replacement.
  CONSISTENT with the run/moment machinery being pure linearity of moments.
- Theorem 2 with r = 0 gives density in H_lambda.  This is the non-diagonal
  analogue of the H_beta statement "r = 0 dense iff beta <= 3/2"; here the
  infinite runs are always inadmissible because their moment sequences are
  not l^2.  CONSISTENT with Corollary 3.

============================================================================
5. What remains open
============================================================================
The theorem closes O1' on the exact subclass "H_lambda with finite polynomial
representers" and gives the complete decision for v_1 = x^4.  It does not
close O1' for:

- general banded Hilbert spaces with banded Gram but without the explicit
  l^2 isomorphism used here;
- non-finite polynomial representers, or representers whose membership
  equations are not finite linear combinations of moments;
- arbitrary non-diagonal H (e.g. weighted L^2), where infinite-run
  realizability is a genuine infinite-dimensional moment problem;
- the full O1' moment-problem core.

Thus the general O1' remains RIGOROUS_PARTIAL_RESULT.
