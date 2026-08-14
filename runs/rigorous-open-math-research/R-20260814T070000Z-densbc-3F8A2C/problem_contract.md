# Problem Contract: Polynomial Density in Boundary-Constrained Hilbert Spaces

Task: Q-20260814-densbc-3F8A2C
Run root: runs/rigorous-open-math-research/R-20260814T070000Z-densbc-3F8A2C/

## 1. Normalized problem statement

Let H be a Hilbert space of functions on [-1,1] (or [0,1]) whose underlying
vector space contains all polynomials Pi, and let V be a closed linear subspace
of H. Let a candidate family Q subset V be given. We seek an as-exact-as-possible
characterization of when Q is dense in V, i.e. closure(span Q) = V in H.

Two concrete formalizations of "general boundary conditions" (each yields a
distinct criterion; every theorem below states which form it covers):

(a) FUNCTIONAL-CONSTRAINT FORM. V = Intersection_{j=1..r} ker L_j, where each
    L_j : H -> C is a nonzero continuous (bounded) linear functional, and the L_j
    are linearly independent (so codim V = r, dim V^perp = r).
    Candidate family Q = { x^k : L_j(x^k) = 0 for all j } (kept monomials), or
    the adapted sparse family { p_n : p_n in V }.

(b) ARBITRARY-CLOSED-SUBSPACE FORM. V arbitrary closed, candidate family =
    V cap Pi (all polynomials that lie in V), or the adapted sparse family
    { p_n : p_n in V } where the sparse basis p_0=1, p_1=x,
    p_{2m} = x^{2m} - (m/(m-1)) x^{2m-2}, p_{2m+1} = x^{2m+1} - (m/(m-1)) x^{2m-1}
    (m >= 2) is the project's adapted family.

## 2. Core sparse family (project adapted basis)

p_0 = 1, p_1 = x,
p_{2m} = x^{2m} - (m/(m-1)) x^{2m-2},  p_{2m+1} = x^{2m+1} - (m/(m-1)) x^{2m-1}
for m >= 2.  index set n in {0,1} union {4,5,...} (missing degrees 2 and 3).
{p_n} is a triangular basis of Pi: span{p_n} = Pi.

## 3. Framework assumptions on H (adapted from project Theorem 2 hypotheses)

Adapted to V, the hypotheses needed are:
  (A-1) Pi is dense in H (project (H1)); for the constrained case we also need
        to know the monomials (or the sparse family) restricted to V to be in V.
  (A-2) moments well-defined: for w in H, M_k = (w, x^k)_H is well-defined with
        |M_k| <= ||w||_H ||x^k||_H  (automatic by Cauchy-Schwarz in H).

For the boundary-constrained problem, note that when V = (span L_j)^perp we do
NOT in general have Pi dense in V "for free": monomials x^k fail the constraint
L_j(x^k) = 0 for all j in general, so the mere hypothesis Pi dense in H does not
imply the candidate family dense in V.  The characterization must therefore be
restated as density in the closed span V0 = closure(span Q), and we ask whether
V0 = V.

## 4. Master criterion (density in a closed subspace, general form)

For any closed subspace V of H and candidate family Q subset V:
  closure(span Q) = V  (in H)   iff   no nonzero w in V with (w,q)_H = 0 for all q in Q.
This is just the Hahn-Banach / Riesz-Fischer orthogonal-complement criterion,
restricted to V.  If V0 = closure(span Q), then V0 = V iff V0^perp = V^perp
(as subsets of H), and V0^perp = V cap Q^perp.  Hence
  V0 = V  iff  V cap Q^perp = V cap V^\\perp = {0}.

In form (a): Q^perp = { w : (w, x^k) = 0 whenever L_j(x^k) = 0 for all j }.
In form (b) with Q = V cap Pi: Q^perp = { w in Pi^\\perp ... }.

## 5. Completion criteria / deliverables

1. General necessary-and-sufficient criterion (even abstract): establish the
   constrained moment characterization exactly, including the Hahn-Banach and
   Weierstrass pieces, in both forms (a) and (b).
2. Concrete sufficient criteria: first-moment criterion (beta < 1) on V;
   jump-moment criterion on V; and criterion via the constraint functionals L_j
   being "well-behaved" with respect to the monomial basis.
3. Exact classifications where attainable: diagonal-space H_beta with
   V = span{e_{j1},...,e_{jm}}^\\perp (coordinate constraints); decide the
   conjecture: dense iff (beta <= 3/2) OR (constraints force the free-moment
   parameters M_2 = M_3 = 0).
4. If a complete answer is impossible: return strict partial theorems + the exact
   reduced open core, honestly labeled.

Status: OPEN (project summary 5.5 item 4). Baseline audited theorems to build on
without authority to copy: docs/SL_denseness_criteria.tex Theorems 2, 3, 5, 8, 11.

## 6. Cross-cutting honesty conditions

- STRICT means derivation-only. Numerical tables are EVIDENCE only.
- A falsified conjecture or a precise reduced core is a valid deliverable.
- Every citation carries a stable link + exact locator; paywalled items labeled.
