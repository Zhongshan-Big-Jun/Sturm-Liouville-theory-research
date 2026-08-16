# Candidate Proof: DensBC O1 — exact low-moment-survival criterion, general non-diagonal H

Run: R-20260816T000000Z-densbc-o1
Upstream status (verbatim): RIGOROUS_PARTIAL_RESULT
This-run status: RIGOROUS_PARTIAL_RESULT (new STRICT structure theorems for O1;
the realizability/membership step is a precisely-stated reduced core O1').

============================================================================
0. Setting (see problem_contract.md)
============================================================================
H Hilbert (H1): Pi dense, (H2) moments well defined.  FORM (a):
V = Intersection_{j=1..r} ker L_j, W := V^\perp = span{v_1,...,v_r}, dim W = r.
Sparse family p_0=1, p_1=x, p_{2m}=x^{2m}-(m/(m-1))x^{2m-2}, p_{2m+1} likewise
(m>=2).  N = { n : p_n in V } = { n : <v_j,p_n>_H = 0 for all j }.
Q_sp = {p_n : n in N}.  Representer moments a^{(j)}_k = <v_j,x^k>_H.
P_V = orthogonal projection onto V.

The packet treats only FORM (a); we keep that.  Upstream Theorems A-H are
audited (esp. Theorem E diagonal classification) and are used as established
results, not re-derived.

============================================================================
1. STRICT — Projection (polynomial) density theorem (new)
============================================================================
Theorem 1 (projection density). Let H satisfy (H1). Let V be any closed subspace
of H and P_V the orthogonal projection onto V.  Then P_V(Pi) is dense in V.
In particular span{ P_V(p_n) : all n } is dense in V.

Proof. P_V : H -> H is bounded linear, surjective onto its image V (P_V is
idempotent, image = V).  Pi is dense in H by (H1).  A continuous map sends dense
subsets to dense subsets of the image; hence P_V(Pi) is dense in P_V(H) = V.
Since span{p_n} = Pi (triangular basis), P_V(span{p_n}) = span{P_V(p_n)} is dense
in V.  qed

REMARK.  This is the single most important new fact for O1: for EVERY closed
subspace (any boundary-constrained V), the projected polynomial family is ALWAYS
dense in V.  So polynomial density "in V" is never the issue; the issue is
exactly the SELECTION Q_sp = {p_n in V} (kept elements equal to their own
projection) versus the full projected family {P_V(p_n)}.

COROLLARY 1.1.  closure(span Q_sp) = V  <=>  each excluded projection
P_V(p_n) for p_n notin V lies in closure(span{ P_V(p_m) : p_m in V }) = closure(span Q_sp).
Equivalently (upstream Theorem A),  V cap Q_sp^\perp = {0}.

============================================================================
2. STRICT — Obstruction space as a structured linear system in M_k
============================================================================
Theorem 2 (obstruction system).  V cap Q_sp^\perp =
  { w in H : <w,v_j>_H = 0 for all j, and <w,p_n>_H = 0 for all n in N },
where, expanding p_n in monomials,
  n = 0:  <w,p_0> = M_0(w);
  n = 1:  <w,p_1> = M_1(w);
  n = 2m >= 4:  <w,p_{2m}> = M_{2m}(w) - (m/(m-1)) M_{2m-2}(w);
  n = 2m+1 >= 5: <w,p_{2m+1}> = M_{2m+1}(w) - (m/(m-1)) M_{2m-1}(w).
So the obstructions are exactly the moment sequences that (a) satisfy the kept
recursions (R below) with the kept M_0/M_1, and (b) are realized by an element
w in V = W^\perp (the membership condition <w,v_j> = 0).

Proof.  Q_sp^\perp = {w : <w,p_n>=0 for all n in N} by definition; intersect with
V = W^\perp gives <w,v_j>=0.  The expansions are linearity of the moment
functional.  qed

The kept recursion system (R): for w in V cap Q_sp^\perp,
  (R0) 0 in N  => M_0 = 0;
  (R1) 1 in N  => M_1 = 0;
  (R2) 2m in N (m>=2) => M_{2m} = (m/(m-1)) M_{2m-2};
  (R3) 2m+1 in N (m>=2) => M_{2m+1} = (m/(m-1)) M_{2m-1}.

============================================================================
3. STRICT — Run decomposition and the first obstruction
============================================================================
The system (R) is IDENTICAL in form to the diagonal case, because it is pure
linearity of moments — it does not depend on the diagonal/non-diagonal nature of
H.  Only the kept set N differs (N is now defined by representer moments a^{(j)}_k,
not by "degree in R").

Even side: vertices 0,2,4,...; kept p_{2m} (m>=2) imposes the recursion edge
(2m-2, 2m).  Vertex 2 is a base (no p_2 in the sparse family).  Odd side:
vertices 1,3,5,...; kept p_{2m+1} gives edge (2m-1,2m+1); vertex 3 is a base.
A RUN is a maximal step-2 interval of degrees connected by kept edges.

Theorem 3 (run lemma + first obstruction).  Let w in V cap Q_sp^\perp.
(i) On a run with lowest degree L (L >= 2 even, or L >= 3 odd, or L in {0,1} if
    pinned by (R0)/(R1)), within the run  M_k = (floor(k/2)/floor(L/2)) * M_L
    (the corrected ratio; for L=0 use M_0, for L=1 use M_1).  M_L is the unique
    free parameter of the run unless L in {0,1} with the run pinned to zero.
(ii) The moments at degrees not touched by any kept recursion (isolated base
     vertices whose runs contain no other degree) are free parameters, each
     generating a finite-support moment sequence.
(iii) If V cap Q_sp^\perp contains a nonzero w, let d_min(w) = min{ k : M_k(w) != 0 }.
     The minimal possible d_min over nonzero obstructions is the FIRST
     OBSTRUCTION degree D*.  By (i)-(ii) D* is a free run-base degree (2, 3, or a
     run base, or 0/1 if not pinned) whose free parameter can be set nonzero with
     all lower bases zero and still be realized by an element of V.
(iv) Consequently: closure(span Q_sp) = V  <=>  no such free base admits a nonzero
     realization in V; and if density holds it holds "up from the first base".

Proof. (i) is the same recursion algebra as upstream Lemma 4.1 (corrected:
within a run M_k = (floor(k/2)/floor(L/2)) M_L), proven by iterating the kept
recursion along the run; it holds in any H because it is pure linearity of
moments.  (ii) isolated vertices have no kept recursion touching them, so their
M is unconstrained by (R) (only by membership in V).  (iii)-(iv) by the moment
filtration: kept recursions only propagate a moment upward in degree from lower
moments, so the lowest nonzero moment of an obstruction is not produced by any
kept recursion; it must be a free base; minimality gives D*.  qed

REMARK (packet item 3: first obstruction).  D* is the "which low moment survives":
the smallest degree whose free base can be realized by w in V orthogonal to all
kept p_n.  In the diagonal coordinate case this matches exactly the lowest
free-base of any finite/infinite run of Theorem E.

============================================================================
4. STRICT — Diagonal reduction (packet item 2)
============================================================================
Theorem 4 (reduction to Theorem E).  Suppose L_j are coordinate projections on a
diagonal space H_beta (i.e. V = { W_i = 0 for i in R }, R finite).  Then the
criterion of Theorems 2-3 reduces exactly to upstream Theorem E:
  closure(span Q_sp) = V  <=>  beta <= 3/2 AND R has no finite run.

Proof.  In the diagonal case the constraint functional L_j(w) = w_{i_j} has Riesz
representer v_j = x^{i_j}/(i_j+1)^{2 beta} (since <w,x^{i_j}>_beta = w_{i_j}
(i_j+1)^{2 beta}), so its representer moments normalize to
a^{(j)}_k = <v_j, x^k>_beta = delta_{k, i_j}.  (Audit correction: the naive
(a^{(j)}_k = (k+1)^{2 beta} delta_{k,i_j}) is off by the Riesz normalization; the
delta form is correct.  Either way the kept set is unchanged.)  Hence p_n in V
<=>  no degree in the support of p_n lies in R, which is exactly the kept set of
Theorem E.  The kept
recursion system (R) is therefore identical; the run decomposition of Theorem 3
is exactly the run graph of Lemma 4.1/Theorem E (with the corrected ratio).  The
membership step w in V becomes "w_i = 0 for i in R", i.e. certain free-base
moments are pinned to zero and the realization step is the H_beta summability of
the moment sequence, precisely the convergence analysis in Theorem E.  The
resulting iff is Theorem E.  qed

So the general criterion (Theorems 2-3) specialises to Theorem E when the
representers are coordinate; this satisfies packet item 2.

============================================================================
5. STRICT — What the answer is / is not (finite-rank question, packet risk)
============================================================================
Theorem 5 (structure of the criterion).  For a general FORM (a) V, the exact
criterion is:
   closure(span Q_sp) = V
   <=>  there is NO assignment of the free run-base parameters (Theorems 2-3)
        that (a) yields a moment sequence representable by some w in H
        (moment representability), and (b) satisfies <w,v_j>_H = 0 for all j
        (membership in V), with w != 0.
This is NOT a purely finite-rank condition in general: both (a) and (b) depend
on the infinite moment data a^{(j)}_k = <v_j, x^k>_H and on the realization
(moment problem) structure of H.  It IS finite/structured when:
  - every representer v_j is a polynomial (then a^{(j)}_k has finite support and
    N, hence the run/free-base structure, is finite to determine), AND
  - the moment-representability + membership step is finite-rank in H
    (e.g. the diagonal/coordinate case, where it is H_beta summability).

Proof.  (a) The obstruction space is characterized by Theorems 2-3.  The "free
base parameter realized" step is exactly: find nonzero w in H with <w,x^k> = m_k
and <w,v_j>=0.  This is a moment problem / linear feasibility in H; in a general
H it is not determined by finitely many moments or finitely many representer
moments.  (b) If all v_j are polynomials of max degree d, then N = {n : p_n
orthogonal to a finite-dimensional polynomial space}, a finitely-presented set,
and the run/free-base data is finite; the realizability step is the only
remaining (possibly infinite) part.  qed

This RESOLVES the packet's ambiguity: the answer is a structured linear system in
M_k with a genuine moment-problem core O1'; it is not a universally finite-rank
closed form.

============================================================================
6. STRICT — Negative/structure observation (generic constraints)
============================================================================
Proposition 6 (generic empty kept set).  For a generic single non-coordinate
constraint (v_1 not a scalar multiple of any monomial, and the equations
a^{(1)}_n = (m/(m-1)) a^{(1)}_{n-2} holding only exceptionally), N is empty or
sparse; for N empty, Q_sp = empty and closure(span Q_sp) = {0}, so density fails
whenever V != {0}.

Proof.  For N to be nonempty at index n we need <v_1,p_n> = a_1(n) - (m/(m-1)) a_1(n-2)
= 0 for n >= 4 (and 0,1 similarly).  For a generic infinite sequence a_1(k) these
finitely-parameter constraints are satisfied only exceptionally; generically no n
qualifies.  If N is empty, Q_sp has no elements, so its closed span is {0}.  qed

REMARK.  The EVIDENCE scripts (o1_projection_density.py with v_1 = e^x, and
o1_poly_rep_example.py with v_1 = x - 1/2 x^2) both confirm N = empty: the kept
set is empty and the runs collapse to isolated bases.  These are EVIDENCE, not
the proof of Proposition 6.

============================================================================
7. Reduced open core (honest, NOT claimed)
============================================================================
O1' (the precise remaining core).  Given the structured system of Theorems 2-3
(N, runs, free bases), decide whether some free run-base admits a nonzero w in H
with <w,x^k> = (the moments specified by the free assignment and the kept
recursions) and <w,v_j> = 0 for all j.  This is a moment-representability +
membership problem in H.  It is finite-rank exactly under Theorem 5's conditions;
in general it requires infinite moment-problem data.  This is the honest reduced
core of O1 — strictly smaller than O1 because N, the runs, the free bases and the
first-obstruction degree D* are now determined exactly from the representer
moments.

O2' (inherited, still open): full characterization of which L_j "kill the free
parameters everywhere" for all beta in non-coordinate H (upstream O2).
O3 (inherited open): fractional left-definite window 3/2 <= s < 2.

============================================================================
8. Regression check (STRICT statements only)
============================================================================
- Theorem 1 with V = H (r=0): P_H(Pi) = Pi dense in H — reduces to (H1).  CONSISTENT.
- Theorem 4 with R = {}: reduces to upstream Theorem E/Theorem 11: sparse family
  dense in unconstrained H_beta iff beta <= 3/2.  CONSISTENT.
- Theorem 2 with r=0: V cap Q_sp^\perp = {w : <w,p_n>=0 for all n} — the upstream
  whole-space moment characterization (project Theorem 2/Theorem B).  CONSISTENT.
- No contradiction with audited Theorems A-H; Theorem 3 uses the F-densbc-01
  corrected ratio M_k = (floor(k/2)/floor(L/2)) M_L.
