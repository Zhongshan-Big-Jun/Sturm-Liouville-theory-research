# Candidate Proof: O1' for the weighted shift family H_{beta,lambda}

Run: R-20260823T000000Z-o1p-lightreuse
Status: RIGOROUS_PARTIAL_RESULT
  (A new STRICT exact criterion is proved for the non-diagonal two-parameter
   family H_{beta,lambda}, which contains both the closed H_beta subclass
   (lambda = 0) and the closed H_lambda subclass (beta = 0).  General O1'
   remains open.)

All mathematical statements in Sections 1-5 are STRICT.  Numerical
verification is labelled EVIDENCE only and is not used as proof.

============================================================================
0. Setting and standing hypotheses
============================================================================

Let beta >= 0 and lambda in (-1,1).  Let H = H_{beta,lambda} be the real
Hilbert space l^2(N_0) with orthonormal basis (e_k)_{k>=0}.  Define
monomials

    x^k = (k+1)^beta e_k + lambda e_{k+1},    k >= 0.

Then Pi = span{x^k : k >= 0} is dense in H.  Proof: for each k, telescoping
gives

    e_k = sum_{j=0}^{N} (-lambda)^j C_j x^{k+j}
          + (-lambda)^{N+1} C_N e_{k+N+1},

where, for j >= 0,

    C_j = prod_{i=0}^{j} (k+1+i)^{-beta}.

The remainder has norm |lambda|^{N+1} C_N
<= |lambda|^{N+1} (k+1)^{-beta (N+1)} -> 0.  Hence Pi is dense.
For lambda = 0 this is the diagonal H_beta (in the x^k = (k+1)^beta e_k
normalization); for beta = 0 this is exactly H_lambda.

For w = sum_{k>=0} w_k e_k in H, the moments are

    M_k(w) = <w, x^k>_H = (k+1)^beta w_k + lambda w_{k+1}.

The Gram matrix of monomials is

    G_{i,k} = <x^i, x^k>_H

with bandwidth 1.  For finite polynomial constraints we assume

    v_j = sum_{i=0}^{d_j} c_i^{(j)} x^i,    j = 1..r,

with r < infinity and d_j < infinity.  Define

    V = { w in H : <w, v_j>_H = 0 for all j }.

As in the upstream runs, N = { n : p_n in V }, Q_sp = { p_n : n in N }, and
the sparse family is

    p_0 = 1,  p_1 = x,
    p_{2m} = x^{2m} - (m/(m-1)) x^{2m-2},      m >= 2,
    p_{2m+1} = x^{2m+1} - (m/(m-1)) x^{2m-1},  m >= 2.

============================================================================
1. STRICT -- Cofinite kept set and free-run decomposition
============================================================================

Theorem 1.  Let D = max_j d_j (with D = -1 if r = 0).  Then every n > D + 3
lies in N.  Consequently the run graph has finitely many components, the
free-base set B is finite, and on each parity there is at most one infinite
run.

Proof.  For n >= 4, the support of p_n is {n, n-2}.  Since G has bandwidth 1,

    <v_j, p_n>_H = sum_{i=0}^{d_j} c_i^{(j)}
                   (G_{i,n} - (m/(m-1)) G_{i,n-2}).

If n > d_j + 3, then |i - n| > 1 and |i - (n-2)| > 1 for every i <= d_j.
Both G entries are zero for every j.  Thus p_n in V for every n > D+3.
Only finitely many n <= D+3 can fail to be kept.  Above D+3 all edges of
each parity are present, so each parity has one infinite tail run and only
finitely many additional components.  qed

Run graph and free bases.  Use exactly the upstream definitions:

* vertices 0,1,2,...;
* even edge (2m-2,2m) present iff 2m in N (m >= 2);
* odd edge (2m-1,2m+1) present iff 2m+1 in N (m >= 2).

A run R is a connected component.  A free base b in B is the least element of
its run, except that b = 0 or b = 1 is free only when that degree is not in
N.  For b in B define rho_b : R_b -> R by

    rho_b(b) = 1,
    rho_b(k) = floor(k/2) / floor(b/2)   for k in R_b with b >= 2,
    rho_b(k) = 1                         for b in {0,1}.

This is the corrected F-densbc-01 ratio.  Let B_fin be the set of free bases
whose run is finite, and B_inf the set whose run is infinite.

============================================================================
2. STRICT -- Moment parameterization
============================================================================

Theorem 2.  A vector w in H lies in V cap Q_sp^\perp if and only if there is a
vector t = (t_b)_{b in B} such that

    M_k(w) = sum_{b in B} t_b rho_b(k) 1_{k in R_b}            (M)

and

    T t = 0,

where T is the r x |B| matrix

    T_{j,b} = sum_{i=0}^{d_j} c_i^{(j)} rho_b(i) 1_{i in R_b}.

Moreover the parameter vector t is uniquely determined by w (t_b = M_b(w)).

Proof.  This is the same pure moment-algebra as the upstream H_beta proof.
For every kept p_n, <w,p_n>_H = 0.  If 0 in N then M_0 = 0; if 1 in N then
M_1 = 0.  For m >= 2 and 2m in N (resp. 2m+1 in N), the kept sparse element
gives the recursion M_{2m} = (m/(m-1))M_{2m-2} (resp. the odd analogue).
Within a maximal run these recursions force exactly (M).  Conversely, (M)
satisfies every kept recursion.  Membership w in V is

    <w, v_j>_H = sum_{i=0}^{d_j} c_i^{(j)} M_i(w) = 0

for all j, i.e. T t = 0.  Uniqueness follows because the runs R_b are
disjoint and M_b(w) = t_b.  qed

============================================================================
3. STRICT -- Realizability of run moment vectors in H_{beta,lambda}
============================================================================

This is the new input beyond the H_beta and H_lambda subclasses.

Lemma 3.  Let m be the moment vector of a single run R_b with base b in B_inf.
Then there exists w in H_{beta,lambda} with M_k(w) = m_k for all k if and
only if beta > 3/2.

More generally, if t_even and t_odd are the (possibly nonzero) coefficients of
the even and odd infinite-run moment vectors, then the combined moment
sequence M = t_even m_even + t_odd m_odd is realizable by some w in H if and
only if beta > 3/2, unless both coefficients vanish.

Proof.  Set
    D_j(k) = prod_{i=0}^{j} (k+1+i)^beta   (j >= 0),  D_{-1}(k)=1,
and let
    w_k = sum_{j>=0} (-lambda)^j m_{k+j} / D_j(k).            (S)
We first record the exact properties of (S) that will be used.

For any infinite-run moment vector m, there is a constant C_m such that
|m_q| <= C_m(1+q) for all q.  Since beta >= 0, D_j(k) >= 1, and |lambda| < 1,
the series in (S) converges absolutely for every fixed k:
|(-lambda)^j m_{k+j}| / D_j(k) <= C_m(1+k+j) |lambda|^j.

Iterating the recurrence
    (k+1)^beta w_k + lambda w_{k+1} = m_k                   (E)
N times gives
    w_k = sum_{j=0}^{N} (-lambda)^j m_{k+j} / D_j(k)
          + (-lambda)^{N+1} w_{k+N+1} / D_N(k).             (T_N)
If w in H is an l^2 solution of (E), then the remainder in (T_N) tends to 0:
for beta > 0 it is bounded by |lambda|^{N+1} ||w||_2 (k+1)^{-beta(N+1)};
for beta = 0 it is |lambda|^{N+1} |w_{k+N+1}|, and w_{k+N+1} -> 0 because an
l^2 sequence has terms tending to 0.  Hence every l^2 solution of (E) is
equal to the sequence defined by (S).  Conversely, substituting (S) into (E)
and using
    D_l(k) = (k+1)^beta D_{l-1}(k+1)      (l >= 1)
cancels all l >= 1 terms, so (S) does solve (E) pointwise.  In particular,
m is realizable iff the sequence (S) is square summable.

Now fix the even run b = 2a (a >= 1), with m^e_{2n} = n/a for n >= a and
m^e_{2n+1} = 0.  In (S) only even j contribute on even degrees, so

    w^e_{2n} = (1/a) sum_{r>=0} lambda^{2r} (n+r) / D_{2r}(2n).

All terms are nonnegative, and D_{2r}(2n) >= (2n+1)^{beta(2r+1)}.  Writing
q = lambda^2,
A_lambda = sum_{r>=0} q^r = 1/(1-q),
B_lambda = sum_{r>=0} r q^r = q/(1-q)^2,
we obtain the two-sided estimate, for every n >= a,

    (1/(a 3^beta)) n^{1-beta}
      <= n / [a (2n+1)^beta]
      <= w^e_{2n}
      <= (1/a) (n A_lambda + B_lambda) (2n+1)^{-beta}
      <= C_e n^{1-beta},
    C_e = (A_lambda + B_lambda)/a.

On odd degrees the first nonzero contribution has j = 1, and

    |w^e_{2n+1}|
      <= (|lambda|/a) [(2n+2)(2n+3)]^{-beta}
         sum_{r>=0} (n+r+1) |lambda|^{2r} (2n+2)^{-2 beta r}
      <= C_o n^{1-2 beta},    C_o = 2 |lambda| (A_lambda + B_lambda)
                                  / (a 2^{2 beta})

for all n >= a.  (For beta = 0 this reads |w^e_{2n+1}| <= C_o n, which is
all we need.)

The odd run b = 2a+1 gives the same estimates with even and odd interchanged:
on its own parity w^o_{2n+1} >= c n^{1-beta} and |w^o_{2n}| <= C n^{1-2 beta}.

Consequence for a single run.  If beta <= 3/2, the own-parity lower bound
given above yields |w_{2n}| >= c n^{1-beta} (or the odd analogue) for large n.
Then
    sum_n |w_{2n}|^2 >= c^2 sum_n n^{2-2 beta}
diverges, because 2 - 2 beta >= -1 with equality at beta = 3/2.  Thus (S) is
not l^2, and by the uniqueness observation no l^2 solution exists.  If
beta > 3/2, the upper bounds give (S) in l^2:
    sum_n n^{2-2 beta} < inf,   sum_n n^{2-4 beta} < inf.
So an infinite-run moment vector is realizable exactly when beta > 3/2.

Combinations of even and odd runs.  Let M = t_e m^e + t_o m^o, with t_e,t_o not
both zero, and let W = t_e w^e + t_o w^o be the corresponding (S)-solution.
If one of the two infinite runs is absent from the run system, the corresponding
coefficient is zero and the single-run case above already covers it.

For beta > 0, suppose t_e != 0.  On even indices, w^e_{2n} >= c n^{1-beta}
and |w^o_{2n}| <= C n^{1-2 beta}.  Hence
    |W_{2n}| >= |t_e| c n^{1-beta} - |t_o| C n^{1-2 beta}
             >= (|t_e| c/2) n^{1-beta}
for all sufficiently large n, because n^{-beta} -> 0.
If beta <= 3/2, the square sum over even n diverges, so W is not l^2.  If
t_e = 0, then t_o != 0 and the same argument on odd indices applies.  Thus a
nonzero even/odd combination is not realizable for 0 < beta <= 3/2.

For beta = 0, (S) can be evaluated in closed form.  Let a_e and a_o be the
bases of the even and odd runs, and put alpha_e = 1/a_e, alpha_o = 1/a_o,
q = lambda^2, A = 1/(1-q), B = q/(1-q)^2.  Then, for large n,
    W_{2n} = (alpha_e t_e - lambda alpha_o t_o)(nA + B),
    W_{2n+1} = (-lambda alpha_e t_e + alpha_o t_o) A n
               + (-lambda alpha_e t_e (A+B) + alpha_o t_o B).
The determinant of the matrix
    [ alpha_e    -lambda alpha_o ]
    [ -lambda alpha_e   alpha_o  ]
is alpha_e alpha_o (1 - lambda^2) != 0.  Therefore the two leading coefficients
can both vanish only when t_e = t_o = 0.  For a nonzero pair at least one
parity has |W_{2n}| >= c n for large n; the square sum over that parity
diverges, so W is not l^2.

Combining the two cases: for beta <= 3/2 no nonzero combination of infinite
runs is realizable, whereas for beta > 3/2 the pure-run upper bounds show that
both w^e and w^o are in l^2, and hence the linear combination M is realizable.
This proves the "more generally" part and completes the lemma.  qed

Corollary 4.  A moment sequence whose support is finite is always realizable
in H_{beta,lambda}.  Indeed choose K > max support, set w_k = 0 for k > K,
and solve (E) downward from k = K to k = 0; the resulting w has finite
support and is therefore in l^2.

============================================================================
4. STRICT -- Exact O1' criterion on H_{beta,lambda}
============================================================================

Define

    B_adm = B_fin  union  { b in B_inf : beta > 3/2 }.

Theorem 5 (main theorem).  For the family H_{beta,lambda} with finite
polynomial constraints,

    closure(span Q_sp) = V
        <=>
    ker( T|_{B_adm} ) = {0}.

Equivalently, density holds iff the columns { A m_b : b in B_adm } are
linearly independent, where m_b = (rho_b(0),...,rho_b(D)) is the truncated
low-degree moment vector of the single-run sequence and A is the coefficient
matrix (c_i^{(j)}).

Proof.  By the upstream master criterion, density holds iff
V cap Q_sp^\perp = {0}.  By Theorem 2, every element of V cap Q_sp^\perp
corresponds to a parameter t with T t = 0 and M(t) = sum_b t_b m_b.  The
correspondence is injective because the m_b have disjoint supports.

Write
    F = sum_{b in B_fin} t_b m_b,
    I = sum_{b in B_inf} t_b m_b.
Both sums are finite: B is finite by Theorem 1, and on each parity there is at
most one infinite run, so B_inf has at most two elements.  By Corollary 4
every finite-support sequence is realizable; each m_b with b in B_fin has
finite support, and a finite sum of realizable moment sequences is realizable
because the realizing l^2 vectors can be added.  Hence F is realizable.
Moreover, if F + I were realizable, subtracting a realizing vector of F would
give an l^2 vector realizing I; conversely, if F and I are realizable, their
sum is realizable.  Therefore M(t) is realizable in H_{beta,lambda} iff I is
realizable.

Now apply Lemma 3 to I.  When beta <= 3/2, I is realizable iff t_b = 0 for
every b in B_inf; in particular a nonzero infinite-tail coefficient cannot be
cancelled by any finite-run vector, because the finite-support part F is itself
realizable and subtracting it would leave the same nonzero I.  When
beta > 3/2, Lemma 3 shows every such I is realizable for arbitrary coefficients.

Thus, in the obstruction space V cap Q_sp^\perp, a parameter vector t is allowed
exactly when
    T t = 0   and   t_b = 0 for all b notin B_adm.
Indeed for beta <= 3/2, B_adm = B_fin, so the second condition is exactly the
condition that I = 0; for beta > 3/2, B_adm = B, so there is no additional
restriction.  Therefore the obstruction space is isomorphic to
ker(T|_{B_adm}), and it is nonzero exactly when ker(T|_{B_adm}) != {0}.  The
equivalence with linear independence of the columns {A m_b : b in B_adm} is
the definition of the kernel.  qed

Corollary 6 (regression).  For lambda = 0, H_{beta,lambda} is the diagonal
H_beta and Theorem 5 reduces to the H_beta criterion of run
R-20260816T210000Z.  For beta = 0, H_{beta,lambda} is H_lambda and
Theorem 5 reduces to the H_lambda criterion of run
R-20260816T220000Z.  In particular:

   * beta = 0, any lambda in (-1,1): B_adm = B_fin, exactly H_lambda;
   * lambda = 0, any beta >= 0: B_adm = finite runs plus infinite runs when
     beta > 3/2, exactly H_beta.

============================================================================
5. STRICT -- Concrete bandwidth-1 non-diagonal example: H_{beta,lambda},
   v_1 = x^4
============================================================================

As an explicit check of the general criterion, take r = 1, v_1 = x^4, and
any lambda in (-1,1), beta >= 0.  Since

    <v_1, p_4>_H = G_{4,4} - 2 G_{4,2}
                 = (5^{2 beta} + lambda^2) - 0 != 0,

p_4 is not in N.  Hence the degree-2 run is a finite singleton free base.
Its truncated moment vector has M_2 = 1 and M_k = 0 for k != 2; the
constraint is M_4 = 0, so the T row on B_fin contains a zero at b = 2.
More directly, the finite-support moment sequence delta_2 is realizable by
solving the moment equations downward; for beta = 0 it is

    w = lambda^2 e_0 - lambda e_1 + e_2,

and for beta > 0 it is the finitely supported w with

    w_2 = 3^{-beta},  w_1 = -lambda 2^{-beta} 3^{-beta},
    w_0 = lambda^2 2^{-beta} 3^{-beta},  w_k = 0 (k >= 3).

One checks M_0 = 0, M_1 = 0, M_2 = 1, and M_k = 0 for k >= 3.  Hence
non-density for every beta >= 0 and lambda in (-1,1).  This is a
non-diagonal, weighted analogue of the v_1 = x^4 example and, for
beta = 0, agrees with the H_lambda theorem.

============================================================================
6. Relation to the parallel baseline H_shift(m,lambda)
============================================================================

The parallel baseline run (R-20260823T000000Z-o1p-baseline) proves a strict
finite-rank criterion for the stable banded-shift family H_shift(m,lambda)
with x^k = e_k + sum_{s=1}^m lambda_s e_{k+s}.  That family is Toeplitz and
has no diagonal weighting.  The family proved here, H_{beta,lambda}, has
x^k = (k+1)^beta e_k + lambda e_{k+1}; for beta > 0 it is not Toeplitz and
is not covered by the baseline theorem.  The two families overlap at
beta = 0, m = 1 (H_lambda).  Thus the baseline and this run are complementary:
the baseline widens the shift bandwidth, while this run adds a diagonal
weighting and reproduces the H_beta threshold beta > 3/2 inside a
non-diagonal space.

============================================================================
7. STRICT -- What remains open
============================================================================

The theorem closes O1' on the structured subclass:

   H_{beta,lambda} with finite-degree polynomial representers.

It does not close O1' for:

- general banded H whose moment map is not of the weighted-shift form
  D_beta + lambda B, or whose run-moment realizability is not governed by
  a single beta > 3/2 threshold;
- fully general non-diagonal H with infinite representer-moment data;
- representers that are not finite polynomials;
- the general abstract moment-problem core.

Thus, as stated in the problem statement, general O1' remains RIGOROUS_PARTIAL_RESULT.

============================================================================
8. Regression checks
============================================================================

- beta = 0: H_{0,lambda} = H_lambda.  Theorem 5 gives ker(T|_{B_fin}) = {0},
  matching R-20260816T220000Z Theorem 2.
- lambda = 0: H_{beta,0} is diagonal H_beta.  Theorem 5 gives the H_beta
  finite/infinite admissibility criterion, matching R-20260816T210000Z
  Theorem 4.
- r = 0: B_adm is empty when beta <= 3/2; when beta > 3/2 the top infinite
  runs are admissible but T has zero rows, so any nonzero t is in the
  kernel; hence for beta > 3/2 the span of the sparse family is not dense
  in H.  This matches the whole-space H_beta threshold and the H_lambda
  r = 0 density result (beta = 0 <= 3/2).  In the intermediate non-diagonal
  case beta <= 3/2, lambda != 0, r = 0, the criterion says density holds in
  H_{beta,lambda}; this is the non-diagonal analogue of the H_beta result.
- Theorem 1's threshold D+3 reduces to H_lambda's D+2?  H_lambda used
  D = max d_j + 1 and n > D+2; in our notation D=max d_j and n>D+3, same
  as D+3 = max d_j + 3.  CONSISTENT.


============================================================================
Repair log
============================================================================

- Changed sections:
  1. Lemma 3 (Section 3) -- proof rewritten from asymptotic sketch to a
     rigorous two-sided estimate proof.
  2. Theorem 5 (Section 4) -- proof expanded with an explicit finite/infinite
     decomposition argument.

- Exact repair decisions:
  * Lemma 3 statement is unchanged.  No revision of the condition
    "beta > 3/2" was needed; the audit's mathematical conclusion was correct.
  * The formal series (S) is now proved to be absolutely convergent for every
    infinite-run moment vector by the elementary bound
    |m_q| <= C_m(1+q), D_j(k) >= 1, |lambda| < 1.
  * A truncation identity (T_N) is written out; it shows that any l^2 solution
    of (E) must agree with the formal series (S).  This is the missing logical
    step that closes the "no other l^2 solution via cancellation" loophole.
  * Explicit constants are given: q = lambda^2,
    A_lambda = 1/(1-q), B_lambda = q/(1-q)^2,
    C_e = (A_lambda+B_lambda)/a,
    C_o = 2|lambda|(A_lambda+B_lambda)/(a 2^{2 beta}).
    These give the uniform bounds
        c n^{1-beta} <= w^e_{2n} <= C_e n^{1-beta},
        |w^e_{2n+1}| <= C_o n^{1-2 beta}.
  * For mixed even/odd combinations, beta > 0 is handled by parity separation:
    the own-parity term has order n^{1-beta} and the opposite-parity term has
    order n^{1-2 beta}, so a nonzero coefficient cannot be cancelled.  The
    beta = 0 case is handled by an explicit 2x2 leading-coefficient matrix
    with determinant alpha_e alpha_o(1-lambda^2) != 0.
  * Theorem 5 now separates M(t) = F + I, where F is the finite-run part and I
    is the at-most-two-term infinite-run part.  Since F is realizable by
    Corollary 4 and the realizable moment sequences form a linear subspace,
    M(t) is realizable iff I is realizable.  This is the explicit proof that
    finite-run vectors cannot repair a nonzero infinite tail.

- New rigorous proof outline:
  * Lemma 3: (i) define (S); (ii) prove absolute convergence; (iii) prove every
    l^2 solution equals (S) via (T_N); (iv) prove two-sided parity-separated
    bounds for pure infinite runs; (v) use lower bounds to show non-l^2 for
    beta <= 3/2 and upper bounds to show l^2 for beta > 3/2; (vi) handle
    even/odd mixtures with the dominant-parity argument for beta > 0 and the
    2x2 determinant for beta = 0.
  * Theorem 5: (i) invoke the run parameterization; (ii) split into finite and
    infinite parts; (iii) use realizability linearity and Corollary 4 to reduce
    to Lemma 3; (iv) conclude the obstruction space is ker(T|_{B_adm}).

- Remaining doubts:
  * None about the repaired steps.  The proof now uses only elementary
    estimates, explicit constants, and the uniqueness of l^2 solutions of the
    finite-order recurrence.  The statements are unchanged and the conclusion
    remains RIGOROUS_PARTIAL_RESULT for the structured H_{beta,lambda} family.
