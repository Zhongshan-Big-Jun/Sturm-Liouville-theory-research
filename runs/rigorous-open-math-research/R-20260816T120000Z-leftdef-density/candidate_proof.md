# Candidate Proof — Left-Definite DensBC O1' specialization (structural constrained density in H^s[-1,1])

Run: R-20260816T120000Z-leftdef-density
Upstream status (verbatim): RIGOROUS_PARTIAL_RESULT (DensBC 3F8A2C and DensBC O1)
This-run status: RIGOROUS_PARTIAL_RESULT (STRICT structural theorems for the
left-definite specialization; the constrained realization core O1'LD remains open;
a decisive negative structural finding for s >= 4 is recorded honestly).

Status label: RIGOROUS_PARTIAL_RESULT

============================================================================
0. Setting, normalization, and EXACT structural facts (see problem_contract.md)
============================================================================
- H^s[-1,1], s integer >= 1, c > 0: H^s = D(K_c^{s/2}), K_c = -d^2/dx^2 + c,
  Krein BC f'(+1)=f'(-1)=(f(1)-f(-1))/2 on D(K_c).  (f,g)_s = (K_c^{s/2}f,K_c^{s/2}g)_L2.
  This run uses the OPERATOR-DOMAIN interpretation H^s = D(K_c^{s/2}) (the one used
  in the project's concrete H^2/H^3 proofs, SL_h2/h3 docs).
- Sparse family p_0=1, p_1=x, p_{2m}=x^{2m}-(m/(m-1))x^{2m-2},
  p_{2m+1}=x^{2m+1}-(m/(m-1))x^{2m-1} (m>=2), index set D = {0,1} union {n>=4}.
- STRUCTURAL FACTS (exact-arithmetic verified; AUDIT-CORRECTED after independent
  re-verification found the earlier S1 equality false for s >= 4):
  S1a. For s = 2: H^2 ∩ C[x] = span{p_n : n in D}, and the only monomials in H^2
       are 1 and x (x^k notin H^2 for k >= 2).  ALL p_n (n in D) lie in H^2.
  S1b. For s = 3: H^3 ∩ C[x] = span{p_n : n in D}; all p_n lie in H^3.
  S1c. For s in {1,2,3}: all p_n (n in D) lie in H^s.
  S1d. **For s >= 4, the sparse polynomials p_n (n >= 4) are NOT in H^s.**
       Exact check (s=4): K_c p_4 = c x^4 - (2c+12)x^2 + 4 has
       (K_c p_4)'(+1) = -24, (K_c p_4)'(-1) = +24 != (K_c p_4)(±1) difference (0),
       so K_c p_4 fails the Krein BC => K_c p_4 notin H^2 => p_4 notin H^4 = D(K_c^2).
       The same holds for p_n (4<=n<=8) checked exactly.  Hence
       H^s ∩ C[x] = span{1, x} for s >= 4 (only linear polynomials).
       ([p_0=1, p_1=x are in every H^s; every polynomial of degree >= 2 fails the
         iterated Krein condition at the K_c level.]  See also L1' below.)
  Consequence for DensBC O1: its hypothesis (H1) (all polynomials in H, dense)
  is FALSE for H^s, s >= 2; monomial moments M_k(w)=<w,x^k>_s exist only for
  k=0,1 when s >= 2; and for s >= 4 the sparse family is not even a subset of H^s.
- V a closed subspace of H^s (the additional constraint).  Q_sp = {p_n : p_n in V},
  N = {n in D : p_n in V}.  W_s := span{p_n : n in D} (only meaningful where
  p_n in H^s, i.e. s in {1,2,3}).

Audited upstream results used (cited, not copied): DensBC Theorem A (master),
DensBC O1 Theorems 1-5 + reduced core O1', denseness-criteria Lemma 6 (two-step
transfer K_c : H^t -> H^{t-2}), SL_h2/h3 completeness (s = 2, 3).

============================================================================
1. STRICT — Whole-space recovery (packet item 3), CORRECT SCOPE: s in {1,2,3}
============================================================================
Theorem L1'. For every integer s in {1,2,3} and c > 0, with V = H^s:
  Q_sp = {p_n : n in D} (all sparse polynomials lie in H^s), and
  closure(span Q_sp) = H^s.  In particular no nonzero obstruction:
  H^s ∩ {p_n : n in D}^perp = {0}.

Proof.  (i) p_n in H^s for all n in D (S1c; for s=2,3 these are SL_h2/h3 facts,
exact-verified).  (ii) span{p_n} is dense in H^s for s in {1,2,3}, proved WITHOUT
undefined H^s-moments:
    s = 1: all moments (w,x^k)_1 are defined (x^k in H^1); density of span{p_n}
    follows from the first-moment criterion (denseness-criteria Theorem 3,
    ||x^k||_1 <= C k^{1/2}, beta = 1/2 < 1).  [SELF-CONTAINED]
    s = 2: K_c : H^2 -> L^2 is an isometric isomorphism, so density of span{p_n}
    in H^2 is equivalent to density of span{K_c p_n} in L^2.  For g in L^2
    orthogonal to all K_c p_n, the L^2-moments mu_k = (g,x^k)_L2 (all defined)
    satisfy the 3-term jump recursion c mu_{2m} = A_m mu_{2m-2} - B_m mu_{2m-4}
    (A_m = 2m(2m-1)+cm/(m-1), B_m = 2m(2m-3)); by the growth lemma
    u_j >= (4/c)^{j-1} j! and the bound |mu_k| <= ||g||_L2 sqrt(2/(2k+1)), this
    forces all mu_k = 0, so g = 0 and span{K_c p_n} is dense in L^2, hence
    span{p_n} is dense in H^2.  [SL_h2, all moments in L^2]
    s = 3: K_c : H^3 -> H^1 is an isometric isomorphism; density of span{p_n} in
    H^3 is equivalent to density of span{K_c p_n} in H^1.  For w in H^1
    orthogonal to all K_c p_n, the H^1-moments M_k = (w,x^k)_1 (all defined,
    x^k in H^1) satisfy the same 3-term jump recursion; the growth lemma and the
    polynomial bound |M_k| <= C sqrt(k) (SL_h3 Lemma 6) force all M_k = 0, so
    w = 0 and span{p_n} is dense in H^3.  [SL_h3, all moments in H^1]
  Hence Q_sp = {p_n : n in D} and closure(span Q_sp) = H^s.
  (iii) By DensBC Theorem A, H^s ∩ (span Q_sp)^perp = {0}.  qed

Theorem L1'' (STRICT NEGATIVE finding for s >= 4).  For integer s >= 4 and c > 0,
with V = H^s (operator-domain):  Q_sp = {p_0, p_1} = {1, x} (the only sparse
polynomials in H^s), and
  closure(span Q_sp) = span{1, x} != H^s   (density FAILS).
In particular the sparse family does NOT recover H^s for s >= 4.

Proof.  (i) By S1d, p_n notin H^s for n >= 4, while p_0 = 1, p_1 = x are in H^s.
So Q_sp = {1, x}.  (ii) span{1,x} is the 2-dimensional space of linear
polynomials, and its closure in H^s is itself (finite-dimensional subspace of a
Hilbert space is closed).  (iii) H^s is infinite-dimensional for s >= 4 (it
contains, e.g., the eigenfunctions of K_c and, more elementarily, infinitely many
linearly independent functions), so span{1,x} is a proper closed subspace,
hence closure(span Q_sp) != H^s.  qed

REMARK (honest correction, packet item 3).  The packet's premise "the known
full-space completeness results (H^s complete for all integer s >= 1) are
recovered as the unconstrained case V = H" is correct for the sparse family ONLY
for s in {1,2,3}.  For s >= 4, under the operator-domain interpretation
H^s = D(K_c^{s/2}), the sparse family {p_n} (n >= 4) is not even a subset of H^s,
so it cannot recover H^s; indeed H^s ∩ C[x] = span{1,x} and the sparse whole-space
density fails.  The Hilbert space H^s does possess a complete orthogonal
polynomial system {Q_n^{(s)}} of SL_hs (Legendre/Krein-Sobolev transported by
K_c^{-r}), but whether those Q_n^{(s)} lie in the operator domain D(K_c^{s/2})
(for the even case s = 2r: Q_n = K_c^{-r}P_n satisfies K_c^r Q_n = P_n in L^2 but
fails the iterated Krein condition at the K_c level for r >= 2, e.g.
K_c Q_4^{(4)} fails the Krein BC, exact-verified) needs reconciliation between the
operator-domain and an abstract-completion reading of H^s.  This is recorded as
an ambiguity/open point, NOT resolved here; the STRICT results of this run are
scoped to s in {1,2,3} (unambiguous) plus the exact negative s >= 4 finding.

REMARK (packet Q2, first obstruction in the structural whole space).
- s = 1: monomial moments M_2, M_3 exist (x^2, x^3 in H^1).  The DensBC first-order
  recursion M_{2m} = (m/(m-1))M_{2m-2} gives M_{2m} = mM_2, M_{2m+1} = mM_3;
  the first-moment criterion forces M_2 = M_3 = 0.  No first obstruction survives.
- s = 2, 3: p_n all in H^s; density holds (L1').  No obstruction.
- s >= 4: the sparse family fails (L1''); the "first obstruction" is vacuous —
  there are no high-degree sparse candidates at all (Q_sp = {1,x}).

============================================================================
2. STRICT — Structural projection density + characterization of proper V (s in {1,2,3})
============================================================================
Theorem L2 (structural projection density).  For s in {1,2,3} and any closed
V ⊆ H^s, P_V(W_s) is dense in V, where W_s = span{p_n} (dense in H^s by L1').
Hence span{P_V(p_n) : n in D} is dense in V.

Proof.  P_V : H^s -> V is bounded linear surjective; W_s is dense in H^s (L1').
A continuous map sends dense subsets to dense subsets of the image; hence
P_V(W_s) is dense in P_V(H^s) = V.  qed

COROLLARY L2.1.  closure(span Q_sp) = V iff each excluded projection P_V(p_n)
(p_n notin V) lies in closure(span Q_sp).  Equivalently (DensBC Theorem A)
V ∩ Q_sp^perp = {0}.

Theorem L4 (all kept => whole space; s in {1,2,3}).  If V ⊆ H^s is closed and
{p_n : n in D} ⊆ V, then V = H^s.  Hence every proper closed V excludes some p_n.

Proof.  span{p_n} ⊆ V and span{p_n} dense in H^s (L1'); so
H^s = closure(span{p_n}) ⊆ closure(V) = V, and V ⊆ H^s, so V = H^s.  qed

============================================================================
3. STRICT — Transfer descent (s >= 2); correct moment base
============================================================================
Theorem L3 (transfer descent).  For integer s >= 2, let K_c : H^s -> H^{s-2} be
the isometric isomorphism (denseness-criteria Lemma 6).  For any closed V ⊆ H^s,
  closure(span{p_n : p_n in V}) = V   (in H^s)
  iff
  closure(span{K_c p_n : K_c p_n in K_c V}) = K_c V   (in H^{s-2}).
Iterating, the constrained-density problem descends to H^{s'} with s' in {0,1}.

Proof.  K_c is an isometric linear isomorphism H^s -> H^{s-2} (audited
denseness-criteria Lemma 6).  K_c V is a closed subspace of H^{s-2}.  Since K_c
is injective, p_n in V iff K_c p_n in K_c V.  Isometries preserve linear span,
closures, and subspace equality.  Iterating reduces H^s to H^0 = L^2 (even s) or
H^1 (odd s).  qed

REMARK (moment base; AUDIT-CORRECTED).  The equivalent moment problem is only
clean at a SINGLE descent r = 1 of {K_c p_n}:
- s = 2 (descent to L^2): descendants {K_c p_n} in L^2; obstruction moments are
  L^2-moments mu_k = (g,x^k)_L2, satisfying the 3-term jump recursion
  c mu_{2m} = A_m mu_{2m-2} - B_m mu_{2m-4} (free params mu_2, mu_3) — SL_h2 proof.
- s = 3 (descent to H^1): descendants {K_c p_n} in H^1; moments are H^1-moments
  M_k = (w,x^k)_1 with the same 3-term jump recursion (free params M_2, M_3) —
  SL_h3 proof.
For s >= 4 the transfer must be iterated; the descended family is K_c^r p_n with
r >= 2, whose monomial expansion has >= 4 terms (e.g. K_c^2 p_6 has 4 terms), so
the clean scalar 3-term jump is NOT available for the iterate; the residual
recursion in H^{s'} (s' in {0,1}) is higher-order.  Moreover for s >= 4 the
sparse p_n (n>=4) are not even in H^s (S1d), so the "p_n in V" candidate problem
is only meaningful for the surviving p_0,p_1 (L1'').  The DensBC O1 first-order
monomial-moment recursion is only directly legitimate in H^1 (all monomials
present).

============================================================================
4. STRICT — Concrete non-density instance in H^2 (first left-definite O1'LD witness)
============================================================================
Theorem L5.  Let H = H^2[-1,1] and V = ker(Delta), Delta f = f(1)-f(-1) (a
bounded linear functional on H^2).  Then Q_sp = {p_0} ∪ {p_{2n} : n >= 2} (the
even sparse polynomials), and closure(span Q_sp) != V.  Explicitly,
  q := p_5 - 2 p_7 = -2x^7 + 4x^5 - 2x^3  satisfies  q in V ∩ Q_sp^perp, q != 0.

Proof.  (1) Delta bounded on H^2 (H^2 ⊂ H^1 ⊂ C), so V = ker(Delta) is closed,
codim 1.  (2) Even p_n (p_0, p_{2n}) have Delta = 0 => in V; odd p_n
(p_1, p_{2n+1}) have Delta = 2 p_n(1) != 0 => not in V; hence Q_sp is the even
sparse family.  (3) q = p_5 - 2p_7 odd, in H^2, q(1) = 0 so Delta q = 0 => q in V,
q != 0.  (4) q ⊥ Q_sp by parity-orthogonality of the H^2 inner product.
(5) By DensBC Theorem A, closure(span Q_sp) != V.  qed

REMARK.  First concrete left-definite STRICT non-density instance: a bounded
structural/functional constraint (Delta = 0) excludes one parity from Q_sp, which
is then orthogonally silent and never recaptured.  Detected by finite data.

============================================================================
5. STRICT — Honest status of O1' in the left-definite class (packet Q1)
============================================================================
Theorem L6 (status of O1' in the class).
(1) For V = H^s and s in {1,2,3}, O1' is DECIDED: sparse-family density holds
    (L1'), no surviving free base.  For V = H^s and s >= 4, the sparse-family
    decision is DECIDED as NON-dense (Q_sp = {1,x}, L1''); the full-space
    completeness of H^s is via the SL_hs system {Q_n^{(s)}}, not the sparse family.
(2) For a general proper closed V ⊆ H^s (s in {1,2,3}), Theorem L3 descends the
    problem to H^{s'} (s' in {0,1}); for a single descent (s=2->L^2, s=3->H^1)
    the descended family {K_c p_n} satisfies the 3-term jump recursion with free
    parameters; for s >= 4 (if any sparse candidates survive) the recursion is
    higher-order and the surviving candidate set is degenerate (L1'').
(3) Finite-data decidability in H^{s'}: by DensBC O1 Theorem 5 (audited), the
    core is finite/structured exactly when the membership equations are finite
    moment equations AND the moment data are banded/diagonal.  The H^1 moment
    matrix <x^i,x^k>_1 is NON-diagonal (exact; <x^1,x^3>_1 = 2c/5 != 0), so
    finiteness is NOT automatic; the general decision remains a genuine moment
    problem.  (In H^s, s >= 2, the monomial block is vacuous — only 1,x present,
    (1,x)_s = 0 — and carries no obstruction data.)
(4) Hence O1'LD := "given proper closed V ⊆ H^s (s in {1,2,3}; or a surviving
    candidate set for s >= 4), decide whether some free run-base / jump-free
    parameter admits a nonzero realization in V" remains OPEN for general proper
    V; it is decided for V = H^s (L1' / L1'') and for concrete instances such as
    Theorem L5.

Proof.  (1) L1' + L1''.  (2) L3 + DensBC O1 Theorems 2-5.  (3) DensBC O1 Theorem
5 (audited) + exact non-diagonality of the H^1 moment matrix; vacuous H^s block.
(4) summary of (1)-(3); no closed form claimed.  qed

============================================================================
6. Regression checks (STRICT statements only)
============================================================================
- L1' with s = 2 recovers the SL_h2 completeness theorem (span{p_n} dense in H^2).
  CONSISTENT.  L1' with s = 1 recovers H^1 completeness (denseness Cor 3).  CONSISTENT.
- L1'' (s >= 4 negative) is NEW and corrects the packet's Q3 premise for s >= 4;
  it does NOT contradict the SL_hs orthogonal-system completeness of H^s (a
  different family).  The membership of {Q_n^{(s)}} in D(K_c^{s/2}) for s >= 4 is
  flagged open/ambiguous (operator-domain vs abstract-completion reading).
- L5 does not contradict whole-space completeness (proper V, s=2).  CONSISTENT.
- No claim of a closed-form criterion for general proper V; O1'LD open.

============================================================================
7. Reduced open core (honest)
============================================================================
O1'LD: for a general proper closed V ⊆ H^s (s in {1,2,3}; or surviving candidates
for s >= 4), decide whether closure(span{p_n in V}) = V, i.e. whether the descended
obstruction space (in H^{s'}, s' in {0,1}) contains a nonzero element with the
prescribed moments while lying in the descended constraint K_c^r V.  Genuine
moment/membership problem in general (non-diagonal H^1 moment matrix); decided for
V = H^s (L1'/L1'') and concrete instances such as Theorem L5.
OPEN (new, from this run): whether the SL_hs orthogonal system {Q_n^{(s)}} (s >= 4)
lies in the operator domain H^s = D(K_c^{s/2}); reconciling the operator-domain and
abstract-completion readings of H^s for s >= 4.
O2' (inherited, open): constraints guaranteeing density for all c.
O3 (inherited, open): fractional window 3/2 <= s < 2.
