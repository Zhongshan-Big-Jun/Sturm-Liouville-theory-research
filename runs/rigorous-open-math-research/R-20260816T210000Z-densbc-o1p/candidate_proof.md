# Candidate Proof: O1' decided on H_beta with finite polynomial constraint data

Run: R-20260816T210000Z-densbc-o1p
Upstream status (verbatim): RIGOROUS_PARTIAL_RESULT
This-run status: RIGOROUS_PARTIAL_RESULT
  (The reduced core O1' is CLOSED on the structured subclass "H_beta +
   finite-degree polynomial representers".  It remains open for general H.)

Scope.  We work in the diagonal Hilbert space H_beta (beta >= 0) with
constraints L_j(w) = Sum_{k=0}^{d_j} c^{(j)}_k M_k(w), d_j finite.  All
statements below are STRICT.  No numerical evidence is used.

============================================================================
0. Notation and standing hypotheses
============================================================================
Let beta >= 0 and let H_beta be the Hilbert space of sequences
w = (w_k)_{k>=0} with
    <w,v>_beta = Sum_{k>=0} w_k \overline{v_k} (k+1)^{2 beta},
    ||w||_beta^2 = Sum_{k>=0} |w_k|^2 (k+1)^{2 beta} < inf.
Write e_k = x^k.  Then M_k(w) = <w,x^k>_beta = w_k (k+1)^{2 beta}.
The polynomials Pi = span{x^k} are dense in H_beta (finite sequences are dense
in weighted l^2).

Sparse family:
    p_0 = 1, p_1 = x,
    p_{2m} = x^{2m} - (m/(m-1)) x^{2m-2},   m >= 2,
    p_{2m+1} = x^{2m+1} - (m/(m-1)) x^{2m-1}, m >= 2.

Constraint data: for j=1..r,
    L_j(w) = Sum_{k=0}^{d_j} c^{(j)}_k M_k(w),   c^{(j)}_k in C,
with r >= 0 finite and d_j finite.  The coefficient rows are assumed linearly
independent; V = Intersection_{j=1..r} ker L_j.  For r=0 set V = H_beta and
D = -1.  For r >= 1 set D = max_j d_j.  Put A = (c^{(j)}_k) for j=1..r and
0 <= k <= D (entries with k > d_j are zero).

The Riesz representer of L_j is v_j = Sum_{k=0}^{d_j} \overline{c^{(j)}_k} x^k,
so <w,v_j>_beta = Sum_k c^{(j)}_k M_k(w) = L_j(w).  Its representer moments are
    a^{(j)}_k = <v_j,x^k>_beta = \overline{c^{(j)}_k} (k+1)^{2 beta}  for k <= d_j,
    a^{(j)}_k = 0 for k > d_j.
The kept set is N = { n : p_n in V } = { n : <v_j,p_n>_beta = 0 for all j }.
Note that L_j(p_n) = 0 is equivalent to the conjugate sum vanishing, so the
kept-set conditions may be read either through c^{(j)} or through a^{(j)}.
The index set of the sparse family is {0,1} union {4,5,...}; the absent indices
2,3 are not elements of N and are always treated as free bases.

============================================================================
1. STRICT — Cofinite kept set and finite run system
============================================================================
Theorem 1.  With D as above, every n > D+2 lies in N.  Consequently the
run graph defined below has only finitely many components, and the set B of
free bases is finite.

Proof.  For n >= 4 the support of p_n is {n,n-2}.  If n > D+2, then both
n and n-2 are > D, so a^{(j)}_n = a^{(j)}_{n-2} = 0 for every j.  Hence
<v_j,p_n>_beta = 0 for all j, so p_n in V.  For n = 0,1 the same is immediate
when 0,1 > D (i.e. D < 0); otherwise they are among the finitely many low
cases.  Thus all but finitely many indices are kept.

Run graph.  Vertices are the nonnegative integers.  Edges:
    (2m-2, 2m) is an edge iff 2m in N (m >= 2);
    (2m-1, 2m+1) is an edge iff 2m+1 in N (m >= 2).
A component is called a run.  Because N is cofinite, on each parity the
vertices above D+2 form one infinite run; below D+2 there are only finitely
many vertices.  Hence the number of components is finite.  qed

Definition (free bases).  A free base is a vertex b such that the moment M_b
is not forced by a kept sparse element:
    b = 0 is free iff 0 notin N;
    b = 1 is free iff 1 notin N;
    for b even >= 2, b is free iff b is the least vertex of its even run
      (equivalently b = 2, or b >= 4 and b notin N);
    for b odd >= 3, b is free iff b is the least vertex of its odd run
      (equivalently b = 3, or b >= 5 and b notin N).
Let B be the finite set of free bases.

For b in B let R_b be the run (component) containing b.  Define ratios
rho_b : R_b -> R by rho_b(b) = 1 and by the kept recursions:
    for an even run with least vertex b = 2a, rho_b(2m) = m/a;
    for an odd run with least vertex b = 2a+1, rho_b(2m+1) = m/a
      (with a = floor(b/2); for b=3 this gives rho_3(5)=2, rho_3(7)=3, ...);
    for b = 0 or b = 1, R_b = {b} and rho_b(b) = 1.
The formula rho_b(k) = floor(k/2)/floor(b/2) holds for all k in R_b with
b >= 2; this is the corrected ratio from F-densbc-01.

============================================================================
2. STRICT — Moment parameterization of V cap Q_sp^\perp
============================================================================
Theorem 2.  Let w in H_beta.  Then w lies in V cap Q_sp^\perp if and only if
there exists a vector t = (t_b)_{b in B} such that:

  (i) M_k(w) = Sum_{b in B : k in R_b} t_b rho_b(k) for every k >= 0;

  (ii) T t = 0, where T is the r x |B| matrix whose (j,b)-entry is
       T_{j,b} = Sum_{k=0}^{D} c^{(j)}_k rho_b(k) 1_{k in R_b};

  (iii) Sum_{b in B} |t_b|^2 C_b(beta) < inf, where
       C_b(beta) = Sum_{k in R_b} rho_b(k)^2 (k+1)^{-2 beta} in (0, inf],
       with the convention that |t_b|^2 C_b(beta) = inf if t_b != 0 and
       C_b(beta) = inf.

Moreover the correspondence w <-> t is injective: if w satisfies (i)-(iii),
then w is the unique element of H_beta with coefficients
    w_k = ( Sum_{b : k in R_b} t_b rho_b(k) ) (k+1)^{-2 beta}.

Proof.  Let w in H_beta.
First suppose w in V cap Q_sp^\perp.  For every kept p_n, <w,p_n>_beta = 0.
If 0 in N then M_0 = <w,p_0> = 0; if 1 in N then M_1 = <w,p_1> = 0.
For m >= 2, if 2m in N then
    M_{2m} - (m/(m-1)) M_{2m-2} = <w,p_{2m}>_beta = 0;
if 2m+1 in N then
    M_{2m+1} - (m/(m-1)) M_{2m-1} = <w,p_{2m+1}>_beta = 0.
Thus within each run the moments satisfy the ratio recursions; setting
t_b = M_b for b in B gives (i).  Membership w in V gives
    Sum_{k=0}^{D} c^{(j)}_k M_k(w) = 0  for all j,
which is (ii) after inserting (i) and using that R_b are disjoint.  Finally
||w||_beta^2 = Sum_k |M_k(w)|^2 (k+1)^{-2 beta}
             = Sum_{b in B} |t_b|^2 C_b(beta),
the second equality because the R_b are disjoint.  This gives (iii).

Conversely, given t satisfying (ii)-(iii), define w by the displayed formula.
The norm identity above shows w in H_beta.  Membership w in V is exactly (ii).
For orthogonality to Q_sp: if n in N and n >= 4, then p_n corresponds to a
kept edge, so its two endpoints lie in one run R_b and the ratio rho_b
satisfies the edge recursion; hence <w,p_n>_beta = 0.  If 0 in N then t_0 is
not a free variable and M_0 = 0, so <w,p_0> = 0; if 1 in N similarly M_1 = 0.
Thus w in V cap Q_sp^\perp.  Injectivity: if two parameter vectors give the
same w, their difference has all moments M_k = 0; since Pi is dense in
H_beta, the difference is orthogonal to Pi and hence is 0.  In particular
t_b = M_b(w) for each free base b, so the parameter vector is determined by w.
qed

Remark.  Condition (iii) is the exact realizability step of O1' in this
subclass.  Because the runs are disjoint, there is no cancellation between
inadmissible run parameters: a nonzero t_b with C_b(beta) = inf makes
||w||_beta^2 = inf.

============================================================================
3. STRICT — Summability classification
============================================================================
Lemma 3.  For b in B:
  (a) if R_b is finite, then C_b(beta) < inf for every beta >= 0;
  (b) if b in {0,1}, then R_b = {b} and C_b(beta) < inf;
  (c) if R_b is infinite, then b >= 2 and
      C_b(beta) < inf  <=>  beta > 3/2.

Proof.  (a) and (b) are finite sums.  For (c), suppose first b = 2a even.
Then R_b = {2a, 2a+2, 2a+4, ...} and rho_b(2m) = m/a, so
    C_b(beta) = a^{-2} Sum_{m=a}^inf m^2 (2m+1)^{-2 beta}.
The summand is asymptotic to (1/4^beta) m^{2-2 beta}.  The series converges
iff 2 - 2 beta < -1, i.e. beta > 3/2.  For odd b = 2a+1, R_b =
{2a+1, 2a+3, ...} and rho_b(2m+1) = m/a for m >= a (with a >= 1), so
    C_b(beta) = a^{-2} Sum_{m=a}^inf m^2 (2m+2)^{-2 beta},
again convergent iff beta > 3/2.  qed

============================================================================
4. STRICT — Exact O1' decision criterion on the subclass
============================================================================
Theorem 4 (main theorem).  Let B_adm = { b in B : C_b(beta) < inf }.  Then

    closure(span Q_sp) = V
        <=>
    ker( T|_{B_adm} ) = {0}
        <=>
    the columns { A m_b : b in B_adm } are linearly independent,

where m_b = (rho_b(0), ..., rho_b(D)) is the truncated moment vector of the
normalized single-run sequence, and T|_{B_adm} is the matrix with columns
A m_b for b in B_adm.  Equivalently, density fails iff there exists a nonzero
t = (t_b)_{b in B_adm} with T t = 0; such t produces a nonzero w in
V cap Q_sp^\perp by Theorem 2.  For r = 0, A has zero rows, T is the zero map
from C^B to {0}, and the kernel condition simply means B_adm = empty.

Proof.  By upstream Theorem A (master criterion), density holds iff
V cap Q_sp^\perp = {0}.  By Theorem 2, V cap Q_sp^\perp is isomorphic, via
t |-> w, to the space
    { t in C^B : T t = 0  and  t_b = 0 for all b with C_b(beta) = inf }.
Indeed (iii) is equivalent to t_b = 0 whenever C_b(beta) = inf, because the
terms |t_b|^2 C_b(beta) are nonnegative and the R_b are disjoint.  This space
is nonzero iff ker(T|_{B_adm}) != {0}.  The equivalence with linear
independence of the listed columns is the definition of the kernel of the
matrix T|_{B_adm}.  qed

Corollary 5 (single-base sufficient condition).  If there exists b in B_adm
with A m_b = 0 (i.e. the single-run moment vector itself satisfies all
membership equations), then density fails.  In general density can also fail
by a linear combination of admissible single-run vectors even when no single
column is zero; the full criterion is the kernel condition of Theorem 4.

Proof.  Immediate from Theorem 4.  qed

Algorithmic content.  On this subclass O1' is decidable by finite linear
algebra:
  1. Compute N for the finitely many n <= D+2; all n > D+2 are kept.
  2. Build the finite run graph and the finite free-base list B.
  3. For each b, form A m_b (a vector of length r).
  4. Mark b admissible iff R_b is finite, or b in {0,1}, or beta > 3/2
     (Lemma 3).
  5. Density holds iff the marked columns are linearly independent.

============================================================================
5. STRICT — Regression to the coordinate/diagonal Theorem E
============================================================================
Theorem 6.  Let R subset N_0 be finite and V = { w in H_beta : M_i(w) = 0
for all i in R }.  This is the coordinate case of the subclass (rows of A are
the unit vectors e_i).  Then Theorem 4 reduces exactly to upstream Theorem E:

    closure(span Q_sp) = V  <=>  beta <= 3/2  AND  R has no finite run.

Proof.  In the coordinate case, A has one row e_i for each i in R.  The
membership equations are M_i = 0.  A free base b is killed by the row i iff
i in R_b, because then the i-th coordinate of A m_b is rho_b(i) != 0.  Thus
a nonzero t supported on B_adm lies in the kernel iff there is an admissible
free run that contains no constrained degree.

If beta > 3/2, the top infinite run on each parity is admissible and contains
no constrained degree (it starts above the largest constrained degree of that
parity).  Its single-base column A m_b is zero, so density fails.  This is the
beta > 3/2 direction of Theorem E.

Now assume beta <= 3/2.  Then the only admissible runs are finite runs
(Lemma 3).  A finite run contains no constrained degree exactly when it is a
"finite run" in the sense of Theorem E; such a run gives a zero column, so
density fails.  Conversely, if R has no finite run, then every finite component that contains
a free base contains at least one constrained degree, so the corresponding row
forces its t_b to vanish; the pinned singleton components {0}, {1} carry no
free parameter and do not affect the kernel.  The infinite runs are
inadmissible.  Hence ker(T|_{B_adm}) = {0} and density holds.  qed

This also covers r=0 by R = empty: Theorem 6 says dense iff beta <= 3/2, the
audited whole-space criterion.

============================================================================
6. STRICT — Explicit non-coordinate example
============================================================================
Example 7.  Fix any beta >= 0 and any real alpha != 0.  Let H = H_beta,
r = 1, and
    v_1 = x^4 + alpha x^6.
Equivalently V = { M_4(w) + alpha M_6(w) = 0 }.  This is a non-coordinate
polynomial representer of degree D = 6.

Claim: for every beta >= 0, closure(span Q_sp) != V.

Proof.  The element w = x^2 (coefficient sequence w_2 = 1, all other w_k = 0)
is nonzero and in H_beta.  It lies in V because M_4(w) = M_6(w) = 0.  The
kept set contains 0 and 1, but p_4 is not kept: indeed
    <v_1, p_4>_beta = a_4 - 2 a_2 = (5)^{2 beta} != 0,
so 4 notin N.  Therefore degree 2 is a free base (the edge (2,4) is absent)
and R_2 = {2} is finite.  Its truncated vector m_2 has only M_2 = 1, and
A m_2 = 0 because the constraint involves only M_4 and M_6.  Thus b = 2 is
admissible and has zero column; Theorem 4/Corollary 5 gives non-density.

Directly: for every kept p_n,
    <w,p_n>_beta = 0.
Indeed n = 0,1 give M_0 = M_1 = 0; for n >= 4, the support of p_n is
{n,n-2}, which contains degree 2 only when n = 4, and p_4 is not kept.  So
w in V cap Q_sp^\perp, w != 0.  By Theorem A, Q_sp is not dense.  qed

The example shows a genuinely non-coordinate finite free-base obstruction that
cannot be detected by the coordinate rule "finite run in R": there is no R;
the obstruction is created by a moment equation that leaves the low degree 2
free.

============================================================================
7. STRICT — What remains open
============================================================================
The theorem closes O1' on the subclass "H_beta with finite-degree polynomial
representers".  It does not close O1' for:

- general non-diagonal H with infinite representer-moment data;
- banded non-diagonal moment matrices not of the diagonal H_beta form;
- representers that are not polynomials or have d_j = inf;
- the general moment-problem core of Theorem 5 in R-20260816T000000Z.

The remaining general O1' is unchanged: decide free-base realizability
(moment representability + membership in V) for arbitrary H.

============================================================================
8. Regression check (STRICT statements only)
============================================================================
- r = 0 (R = empty) in Theorem 6: dense iff beta <= 3/2.  CONSISTENT with
  Theorem E/Theorem 11.
- Coordinate R finite: Theorem 6 reproduces Theorem E exactly.  CONSISTENT.
- Example 7: the produced w is finite-support and hence in H_beta for every
  beta; no summability threshold appears.  CONSISTENT with Lemma 3(a).
- The ratio rho_b(k) = floor(k/2)/floor(b/2) uses the audited F-densbc-01
  correction.  CONSISTENT with R-20260816T000000Z Theorem 3.
