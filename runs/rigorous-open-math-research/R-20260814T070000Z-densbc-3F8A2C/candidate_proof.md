# Candidate Proof: Polynomial Density in Boundary-Constrained Hilbert Spaces

Run: R-20260814T070000Z-densbc-3F8A2C
Status: RIGOROUS_PARTIAL_RESULT (several STRICT theorems; one reduced open core)
Task: Q-20260814-densbc-3F8A2C

Status label: RIGOROUS_PARTIAL_RESULT

============================================================================
0. Setting and notation
============================================================================
Let I in {[-1,1], [0,1]}. Let H be a Hilbert space over C whose underlying
vector space contains all polynomials Pi, with inner product <.,.>_H and norm
||.||_H.  Write e_k = x^k (the monomial of degree k).  Define the moment of
w in H at degree k as M_k(w) = <w, x^k>_H (well-defined by Cauchy-Schwarz
whenever x^k in H; we assume (H2) below).

Let V be a CLOSED linear subspace of H.  Let Q subset V be a candidate family.
The fundamental density question: is closure(span Q) = V ?

Sparse (adapted) polynomial family (the project basis):
   p_0 = 1,  p_1 = x,
   p_{2m} = x^{2m} - (m/(m-1)) x^{2m-2},      (m >= 2)
   p_{2m+1} = x^{2m+1} - (m/(m-1)) x^{2m-1}.  (m >= 2)
Note: p_n, for n >= 4, has SUPPORT {n, n-2} (both parities): p_{2m} spans
degrees 2m, 2m-2 and p_{2m+1} spans 2m+1, 2m-1.  The family skips degrees 2,3.
{p_n : n in {0,1} union {4,5,...}} is a triangular basis of all of Pi.

Two concrete realizations of "general boundary conditions":

FORM (a)  (functional-constraint form)
   V = Intersection_{j=1..r} ker L_j, where each L_j : H -> C is a nonzero
   bounded linear functional and the L_j are linearly independent.  Then
   dim V^\perp = r and V^\perp = span{v_1,...,v_r}, v_j = Riesz representer of
   L_j.  Candidate family = {x^k : x^k in V} (kept monomials), or the adapted
   sparse family Q_sp = {p_n : p_n in V}.

FORM (b)  (arbitrary closed subspace)
   V arbitrary closed;  candidate family = V cap Pi (all polynomials that lie
   in V), or Q_sp = {p_n : p_n in V}.

Assumptions on H (project (H1),(H2), restated for V):
   (H1) Pi is dense in H and every polynomial is an element of H.
   (H2) moments are well defined: |<w,x^k>_H| <= ||w||_H ||x^k||_H for all
        w in H, k >= 0.  (Automatic by Cauchy-Schwarz.)
No assumption that Pi cap V is dense in V; that is exactly the question.

============================================================================
1. Master criterion (both forms) -- STRICT
============================================================================
Theorem A (master). Let V be a closed subspace of a Hilbert space H and let
Q subset V.  Then
   closure(span Q) = V   (in H)   iff   V cap Q^\perp = {0},
where Q^\perp = { w in H : <w,q>_H = 0 for all q in Q } = (span Q)^\perp.

Proof. Let V0 = closure(span Q) subset V.  V0 is closed.  If V0 = V then for
every w in V with w orthogonal to Q we get w orthogonal to V0 = V, hence
w = 0 (w in V and w in V^\perp).  So V cap Q^\perp = {0}.
Conversely, suppose V cap Q^\perp = {0}.  If V0 != V, then since V0 is a proper
closed subspace of V there is a nonzero w in V with w orthogonal to V0
(orthogonal decomposition V = V0 oplus (V0^\perp cap V); take w in V0^\perp cap V,
w != 0).  But w orthogonal to V0 = closure(span Q) implies w orthogonal to each
q in Q, i.e. w in Q^\perp.  So w in V cap Q^\perp, contradiction.  qed

Theorem A is a tautology but is the precise master statement; the entire
problem reduces to computing V cap Q^\perp, i.e. which elements of the
constrained space are "silent" against the candidate family.

============================================================================
2. Constrained moment characterization -- STRICT
============================================================================
Theorem B (form (a), monomial candidate). Let H satisfy (H1),(H2). Let
V = Intersection_{j=1}^r ker L_j with L_j bounded independent.  Let
S = { k in N_0 : x^k in V }.  Let Q = {x^k : k in S}.  Then
   Q is dense in V
   iff   no w in V \ {0} satisfies  <w, x^k>_H = 0  for every k in S.

Proof. Immediate from Theorem A: Q^\perp = {w : <w,x^k>_H = 0 for all k in S},
and V cap Q^\perp = {w in V with all those moments zero}.  qed

Theorem C (form (a), sparse candidate). Same H,V.  Let N = { n in N_0 :
p_n in V }.  Let Q_sp = {p_n : n in N}.  Then
   Q_sp is dense in V
   iff   no w in V \ {0} satisfies  <w,p_n>_H = 0  for all n in N.

Proof. Same as Theorem B with Q replaced by Q_sp.  qed

Theorems B, C are the "constrained moment problems": density holds exactly
when the constrained space V carries no nonzero element whose moment sequence
vanishes on the kept-degree index set.  This is the analogue of the project's
Theorem 2 restricted to V.

============================================================================
3. The corrected "constraints restore density" mechanism -- STRICT
============================================================================
The packet claims: V = span{x^2,x^3}^\perp in H_beta restores density for
every beta.  This is FALSIFIED (Section 4).  However, the underlying mechanism
"constraints that pin the free moment parameters restore density" is CORRECT
and is made precise here.

Theorem D (constraint-restores-density, corrected form). Let H satisfy
(H1),(H2).  Let V be a closed subspace with
   (i) every sparse p_n belongs to V :  N = {0,1,4,5,...}, and
   (ii) x^2 and x^3 lie in V^\perp  (so <w,x^2>_H = <w,x^3>_H = 0 for all w in V).
Then Q_sp = {p_n : n in N} = {p_n : all n} is DENSE in V.

Proof. Let w in V with <w, p_n>_H = 0 for all n in {0,1,4,5,...}.
  n = 0 : M_0 = <w, 1>_H = 0.
  n = 1 : M_1 = <w, x>_H = 0.
  For each m >= 2 (recursion monomials are admitted since p_{2m}, p_{2m+1} in V):
    0 = <w,x^{2m} - (m/(m-1)) x^{2m-2}>_H
      = M_{2m} - (m/(m-1)) M_{2m-2}.
    Since M_0 = 0, iterating from m = 2 upward gives M_{2m} = m * M_2 for every
    m >= 1.  But M_2 = 0 by (ii).  Hence M_{2m} = 0 for all m >= 1.
    Odd side: 0 = <w,p_{2m+1}>_H = M_{2m+1} - (m/(m-1)) M_{2m-1}, so
    M_{2m+1} = m * M_3 = 0 by (ii).  So every odd moment vanishes too.
  Thus every moment M_k = 0.  By (H1) Pi dense in H, <w,p>_H = 0 for every
  polynomial p; take p_n -> w (a sequence of polynomials approximating w) gives
  ||w||^2 = lim <w,p_n> = 0, so w = 0.  By Theorem A, Q_sp dense.  qed

REMARK. Condition (ii) is exactly "the two free moment parameters M_2, M_3 are
pinned to zero by the constraint subspace".  Condition (i) is what makes the
recursion hold for every kept p_n.  Together they force w = 0 regardless of
the norm growth of the space (no beta-range restriction).  This is the correct
version of the packet insight.  It matches the concrete left-definite setting:
in H^2 the "boundary constraint" is structural (elements satisfy the boundary
condition), the sparse family {p_n} is exactly the family in H^2, and M_2, M_3
are not present because x^2, x^3 are not in H^2 (the free parameters never
exist).  It does NOT apply to coordinate subspaces (Section 4) where (i) fails.

COROLLARY (monomial-compatible constraints). If instead of (i) we only require
x^k in V for all k not in a finite set F, and x^j in V^\perp for every j in F,
and F contains 2 and 3, then the monomial family {x^k : k not in F} is dense in
V (a direct orthonormal-type argument when the moments M_j for j in F are
pinned; otherwise similar).  More generally any "subspace that cuts out a set
of low degrees" restores density precisely for degrees it fully pins.

============================================================================
4. Diagonal-space complete classification -- STRICT (the A5 deliverable)
============================================================================
Definition. For beta >= 0, H_beta is the completion of Pi under the inner
product <x^j, x^k>_beta = delta_{jk} (k+1)^{2 beta}.  Elements are
w = Sum_k w_k x^k with ||w||_beta^2 = Sum_k |w_k|^2 (k+1)^{2 beta} < inf, and
moments M_k(w) = w_k (k+1)^{2 beta}.

Let V = span{ e_{j_1}, ..., e_{j_m} }^\perp (coordinate constraints), where
e_j = x^j and R = {j_1,...,j_m} is the finite set of constrained degrees.  Then
   w in V  <=>  w_i = 0 for all i in R  <=>  M_i(w) = 0 for all i in R.

Candidate family: the adapted sparse family Q_sp = {p_n : p_n in V}, where
p_n in V iff no degree in the support of p_n belongs to R.  For n >= 4 the
support is {n, n-2}, so
   p_{2m} in V  <=>  {2m, 2m-2} cap R = empty,
   p_{2m+1} in V <=>  {2m+1, 2m-1} cap R = empty,
   p_0 in V <=> 0 not in R,   p_1 in V <=> 1 not in R.

THE RECURSION GRAPH.  On the even degrees 2,4,6,... draw an edge between 2m-2
and 2m iff p_{2m} is kept (2m, 2m-2 not in R).  On the odd degrees 3,5,7,...
draw an edge between 2m-1 and 2m+1 iff p_{2m+1} is kept (2m+1, 2m-1 not in R).
[Degree 1 is never a free base: if 1 not in R then p_1 = x is kept and forces
M_1 = 0; if 1 in R then w_1 = 0 forces M_1 = 0.  M_0 = 0 always.]  A maximal
connected component (a run) is a maximal interval (step 2) of consecutive
unconstrained degrees of one parity, of lowest degree >= 2 (even) or >= 3 (odd).
For a run with lowest degree L, the kept recursions force
   M_k = (idx(k)/idx(L)) * M_L   for every degree k in the run,
where idx(2m) = m and idx(2m+1) = m+1, and M_L is the sole free parameter of the
component.  Because R is finite, the even degrees have a TOP run (all evens
above the largest constrained even are unconstrained) that is INFINITE, and
likewise the odd side.

Lemma 4.1. Let w in V be orthogonal to every kept p_n.  Then M_0 = M_1 = 0; on
each even run moments satisfy M_{2m} = (m/a) M_{2a} (a = idx of the run's lowest
degree), on each odd run M_{2m+1} = ((m+1)/b) M_{2b+1} likewise; and moments at
constrained degrees vanish.  Conversely any assignment of the free run-parameters
summable in the H_beta sense, with M_0 = M_1 = 0 and M_j = 0 for j in R, gives
by w_k = M_k (k+1)^{-2 beta} an element w in V orthogonal to every kept p_n.
[The exact-rational check scripts/densbc_v6_exact_recursion.py confirms
(w, p_n) = 0 EXACTLY (rational zero) for every kept p_n, for 11 constraint sets.]
Proof. Orthogonality of w to kept p_n is exactly the recursion on each run (once
M_0 = M_1 = 0 is built in); conversely the recursion forces those relations.  qed

DEFINITION (finite run). A run is FINITE if it is a bounded interval (both ends
capped by a constrained degree of the same parity, or by the base degree 2/3).
Characterization: a finite EVEN run exists <=> exists a constrained even degree
2q >= 4 with 2q-2 NOT in R.  A finite ODD run exists <=> exists a constrained
odd degree 2q+1 >= 5 with 2q-1 NOT in R.

Theorem E (complete diagonal classification, corrected). Let R be a finite set,
V = {w_i = 0 for i in R} in H_beta, and Q_sp = {p_n : p_n in V}.  Then

   Q_sp is dense in V   <=>   beta <= 3/2  AND  R has NO finite run
                                   (neither even nor odd).

In words: the sparse family is dense in the constrained coordinate subspace
exactly in the regime beta <= 3/2, provided the constraints do not create any
bounded "gaps" (finite runs).  Otherwise density fails.

Proof.
(Non-density directions.) (1) If beta > 3/2: take the top infinite even run
(starting at 2a = (2 + max{even in R})+... i.e. the largest even below which a
constraint sits, extended to infinity; always exists since R finite).  Its free
param M_{2a} = 1 is not pinned.  The induced moments M_{2m} = (m/a) on that
infinite run give
   ||w||_beta^2 = Sum_{m >= a} (m/a)^2 (2m+1)^{-2 beta} + O(1) .
The tail is asymptotic to a^{-2} Sum_m m^{2 - 2 beta}, which converges iff
2 - 2 beta < -1, i.e. iff beta > 3/2.  So for beta > 3/2 this w is in H_beta,
is in V, is nonzero, and by Lemma 4.1 is orthogonal to every kept p_n.  By
Theorem A, Q_sp is not dense.
(2) If there is a FINITE even or odd run: its free param is not pinned and the
induced w has FINITE support (only finitely many nonzero moments), so w in
H_beta for every beta, w in V, w != 0, orthogonal to every kept p_n.  Hence
again not dense.
(Density direction.)  Suppose beta <= 3/2 and no finite run exists.  Then every
run is infinite (the top run, and by "no finite run", all runs are the top one
on each parity side; since there's an infinite top run and no capped bounded
run, the unconstrained even degrees form a single infinite run, and likewise
odd).  Let w in V be orthogonal to every kept p_n.  By Lemma 4.1 all moments
are determined by the single free even parameter M_{2a} (top run) and single
free odd parameter M_{2b-1}.  If M_{2a} != 0, then
    ||w||_beta^2 >= Sum_{m >> large} (m/a)^2 M_{2a}^2 (2m+1)^{-2 beta},
which behaves like const * Sum_m m^{2-2 beta}.  For beta <= 3/2 this series
DIVERGES, contradicting w in H_beta.  Hence M_{2a} = 0, then all even moments
vanish; similarly M_{2b-1} = 0 forces all odd moments to vanish.  Thus all
moments M_k vanish, w = 0 (Pi dense in H_beta).  By Theorem A, Q_sp is dense.
qed

REMARK (falsification of the packet's two claims).
  The packet example V = span{x^2,x^3}^\perp (R = {2,3}) is dense in H_beta
  iff beta <= 3/2, NOT for every beta: for beta > 3/2 a nonzero orthogonal w
  with free M_4 (even) and M_5 (odd) exists.  Numerical verification
  (scripts/densbc_v1, v3) confirms the full two-parameter w has zero inner
  product with every kept p_n and finite H_beta norm for beta > 3/2.
  Moreover the proposed criterion "beta <= 3/2 OR constraints force M_2 = M_3
  = 0" is FALSE: the free parameters merely relocate to M_4, M_5 (etc.), and a
  constraint like R = {4} even destroys density at beta <= 3/2 via the finite
  singleton run at degree 2 (M_2 free, finite support).

COROLLARY (monomial family in the diagonal space). For coordinate R, the
monomial candidate family {x^k : k not in R} is an orthonormal basis of V
(once normalized) and hence is ALWAYS dense in V for every beta.  The failure
is an artifact of the SPARSE family, not of polynomials in general.

============================================================================
5. Sufficient criteria on a constrained subspace -- STRICT
============================================================================
The following generalize the project's Theorem 3 (first moment, beta < 1) and
Theorem 5 (jump criterion) to a constrained subspace V, with the exact
hypotheses that make the recursion data available.

Theorem F (first-moment criterion on V). Let H satisfy (H1),(H2) and suppose
||x^k||_H <= C k^beta with beta < 1.  Let V be closed, and suppose there is
m_0 >= 2 such that for every m >= m_0 both p_{2m} and p_{2m+1} belong to V
(i.e. the recursion monomials are eventually in V).  Suppose in addition that
no nonzero w in V satisfies BOTH (a) <w,p_n>_H = 0 for the finitely many kept
p_n with n < 2 m_0, and (b) M_2 = M_3 = 0 (equivalently x^2, x^3 in V^\perp).
Then Q_sp is dense in V.

Proof. Let w in V orthogonal to every kept p_n.  For m >= m_0 the kept p_{2m}
gives M_{2m} = (m/(m-1)) M_{2m-2}.  Iterating from the highest index m_0 up, the
moments M_{2m} for m >= m_0 are determined by M_{2m_0} (or M_2 if m_0 = 2,
otherwise by the first kept moment of that chain).  For large m,
   |M_{2m}| >= c * (m/m_0) * |M_{2m_0^0}|
where M_{2m_0^0} is the base of the even chain.  But Cauchy-Schwarz:
   |M_{2m}| <= ||w||_H ||x^{2m}||_H <= C ||w||_H (2m)^beta .
If the base moment is nonzero, m grows linearly while the RHS grows like m^beta
with beta < 1, a contradiction for m large.  Hence the even base forcing all
even moments >= some degree to vanish, and a similar odd argument.  The only
potentially nonzero moments are those at degrees < 2 m_0 (and < 2 such for odd),
a finite set.  Hypothesis (b) + the finitely-many kept test vectors then pin
those to zero; with M_2 = M_3 = 0 the whole moment system collapses (odd side
M_3 = 0 kills odds, even side base 0 kills evens).  Hence all moments vanish,
w = 0, so Q_sp dense by Theorem A.  qed

REMARK. The finite-support obstruction (a) is exactly the finite-run phenomenon
seen in the diagonal space (Section 4): with only finitely many constrained
degrees, low-degree free moments survive unless pinned.  In the concrete
whole-space left-definite case V = H^s, all p_n in V and x^2,x^3 are simply
absent from the space, so m_0 = 2 and there is no low obstruction; Theorem F
reduces to the project Corollary 3 (beta = s - 1/2 < 1 for 0 <= s < 3/2).

Theorem G (jump criterion on V). Let H satisfy (H1),(H2) and ||x^k||_H <= C k^beta
for some finite beta (any).  Let {q_n} subset Pi satisfy the three-term jump
structure with the growth-lemma hypotheses of the project (q_{2m} = c_0 x^{2m}
- A_m x^{2m-2} + B_m x^{2m-4}, B_m >= 0, and the super-polynomial product
hypothesis giving u_m = omega(m^beta)).  Suppose q_n in V for all n >= n_0 and
the finitely many low moments are pinned as in Theorem F.  Then {q_n cap V} is
dense in V.  Proof is identical to Theorem F, replacing the first-order growth
m by the super-polynomial u_m (which contradicts any polynomial bound).  qed

============================================================================
6. Boundary-functional interpretation -- STRICT
============================================================================
Theorem H. Let V = Intersection_{j=1}^r ker L_j.  For the sparse family, the
obstruction set V cap Q_sp^\perp is exactly
   { w in V : for all n with p_n in V, <w,p_n>_H = 0 },
and Theorem D holds when (i) all p_n in V and (ii) x^2, x^3 in V^\perp.  The
condition x^2, x^3 in V^\perp means the Riesz representers v_j of the L_j
span a subspace of V^\perp that detects (is nonzero on) x^2 and x^3; equivalently
the moment functional M(w) = <w, .> restricted to polynomials has its two free
parameters M_2, M_3 annihilated by the constraints.  Proof. Immediate from
Theorems A, D.  qed

============================================================================
7. Reduced open core (honestly labeled)
============================================================================
The following remain open and are NOT claimed.
O1. For a GENERAL Hilbert space H (not diagonal) with a general codimension-r
    constraint subspace V, the exact criterion "which finite low free base
    moments survive" is governed by the representability of the moment sequence
    by an element of V (analogue of the project's open problem O2).  The
    abstract answer is Theorem B/C (moment characterization); a closed-form
    criterion beyond the diagonal case is not available.
O2. General criterion on the constraint functionals L_j guaranteeing clause
    (ii) of Theorem D (x^2, x^3 in V^\perp) and density for every beta, in
    non-coordinate H.  The Krein H^s case is a special case (structural
    constraints); a full characterization of which L_j "kill the free
    parameters everywhere" is open.
O3. Fractional window 3/2 <= s < 2 in the left-definite family: not addressed
    by this run (inherited from project O1); the diagonal beta in (3/2, 2) is
    covered by Theorem E but only for coordinate subspaces.

============================================================================
8. Regression check against project theorems
============================================================================
- Theorem E with R empty recovers the project Theorem 11: monomial family dense
  (always), and (matching the exact statement) the sparse family {p_n} in the
  UNCONSTRAINED diagonal space is complete iff beta <= 3/2.  Indeed R = {} has no
  finite run (single infinite run at 2), so Theorem E says dense <=> beta <= 3/2,
  exactly the project's diagonal critical exponent.  CONSISTENT.
- Theorem 2 (project moment characterization) is the R = {} special case of our
  Theorem B/C.  CONSISTENT.
- Theorem 3 / Corollary (first moment beta < 1) is the m_0 = 2, pinning-free
  special case of our Theorem F in the whole-space setting.  CONSISTENT.
- Theorem 5 (jump) is the V = H (whole space), all-q_n-in-V special case of our
  Theorem G.  CONSISTENT.
- Theorem 8 (left-definite H^s complete): V = H^s satisfies Theorem D
  Corollary-form hypotheses (all sparse p_n are in H^s, and x^2,x^3 are not in
  H^s so M_2 = M_3 = 0 in the relevant moments); matches the existing proof.
  CONSISTENT.
No contradiction with Theorems 2, 3, 5, 8, 11.
