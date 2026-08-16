# Candidate Proof — Left-Definite DensBC O1' specialization (structural constrained density in H^s[-1,1])

Run: R-20260816T120000Z-leftdef-density
Upstream status (verbatim): RIGOROUS_PARTIAL_RESULT (DensBC 3F8A2C and DensBC O1)
This-run status: RIGOROUS_PARTIAL_RESULT (STRICT structural theorems for the
left-definite specialization; the constrained realization core O1'LD remains open).

Status label: RIGOROUS_PARTIAL_RESULT

============================================================================
0. Setting and normalization (see problem_contract.md)
============================================================================
- H^s[-1,1], s integer >= 1, c > 0: H^s = D(K_c^{s/2}), K_c = -d^2/dx^2 + c,
  Krein BC f'(+1)=f'(-1)=(f(1)-f(-1))/2 on D(K_c).  (f,g)_s = (K_c^{s/2}f,K_c^{s/2}g)_L2.
- Sparse family p_0=1, p_1=x, p_{2m}=x^{2m}-(m/(m-1))x^{2m-2},
  p_{2m+1}=x^{2m+1}-(m/(m-1))x^{2m-1} (m>=2), index set D = {0,1} union {n>=4}.
- STRUCTURAL FACT S1 (exact-arithmetic verified + docs): for integer s >= 2,
  H^s ∩ C[x] = span{p_n : n in D}, and the only monomials in H^s are 1 and x
  (x^k notin H^s for all k >= 2).  For s = 1 all monomials lie in H^1.
  Consequence: DensBC O1 hypothesis (H1) (all polynomials in H, dense) FAILS
  for s >= 2; monomial moments M_k(w)=<w,x^k>_s exist only for k=0,1.
- V a closed subspace of H^s (the additional constraint).  Q_sp = {p_n : p_n in V},
  N = {n in D : p_n in V}.  W_s := span{p_n : n in D}.

Audited upstream results used (cited, not copied): DensBC Theorem A (master),
DensBC O1 Theorems 1-5 + reduced core O1', denseness-criteria Lemma 6 (two-step
transfer K_c : H^t -> H^{t-2}), SL_h2/h3 completeness, SL_hs orthogonal systems.

============================================================================
1. STRICT — Whole-space recovery (packet item 3): V = H^s
============================================================================
Theorem L1. For every integer s >= 1 and c > 0, with V = H^s:
  Q_sp = {p_n : n in D} (all sparse polynomials lie in H^s), and
  closure(span Q_sp) = H^s.  In particular no nonzero obstruction:
  H^s ∩ {p_n : n in D}^perp = {0}.

Proof.  (i) p_n in H^s for all n in D: for s=1 all polynomials lie in H^1; for
s>=2, p_n satisfy the Krein BC (SL_h2 Lemma 1, exact-verified here) so p_n in
H^2, and H^s = D(K_c^{s/2}) ⊆ D(K_c) = H^2 with p_n smooth, so p_n in H^s.
  (ii) span{p_n} is dense in H^s for every integer s >= 1.  We prove this
UNIFORMLY and WITHOUT using any undefined H^s-moment of x^k or K_c p_n (the
SL_denseness_criteria Theorem 8 step-(i)/Lemma-7 argument is NOT used here for
s >= 2 because it relies on quantities undefined when x^k notin H^s):
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
    span{p_n} is dense in H^2.  [SL_h2 argument, all moments in L^2]
    s = 3: K_c : H^3 -> H^1 is an isometric isomorphism; density of span{p_n} in
    H^3 is equivalent to density of span{K_c p_n} in H^1.  For w in H^1
    orthogonal to all K_c p_n, the H^1-moments M_k = (w,x^k)_1 (all defined,
    x^k in H^1) satisfy the same 3-term jump recursion; the growth lemma and the
    polynomial bound |M_k| <= C sqrt(k) (SL_h3 Lemma 6) force all M_k = 0, so
    w = 0 and span{p_n} is dense in H^3.  [SL_h3 argument, all moments in H^1]
    s >= 4: use the explicit complete orthogonal polynomial system {Q_n^{(s)}}
    of SL_hs:  for s = 2r, Q_n^{(2r)} = K_c^{-r} P_n (Legendre in L^2); for
    s = 2r+1, Q_n^{(2r+1)} = K_c^{-r} K_n (Krein-Sobolev, complete in H^1).
    {Q_n^{(s)}} is complete in H^s (via the isometries K_c^{-r}: L^2 -> H^{2r}
    and K_c^{-r}: H^1 -> H^{2r+1}, never using H^s-moments of x^k).  Each
    Q_n^{(s)} is a polynomial in H^s, so by S1 (H^s ∩ C[x] = span{p_n}) we have
    Q_n^{(s)} in span{p_n}; hence span{Q_n^{(s)}} ⊆ span{p_n}, and since
    span{Q_n^{(s)}} is dense in H^s, so is span{p_n}.  [UNIFORM, s >= 4]
  Hence Q_sp = {p_n : n in D} and closure(span Q_sp) = H^s.
  (iii) By DensBC Theorem A, H^s ∩ (span Q_sp)^perp = {0}.  qed

REMARK (audit repair).  This replaces the earlier citation of SL_denseness_criteria
Theorem 8 step-(i)/Lemma-7 for s >= 2, which used undefined quantities (H^s-moments
(w,x^k)_s and (w,K_c p_{2m})_s with x^k, K_c p_{2m} notin H^s).  All moments in the
repair are taken in L^2 or H^1 (or none at all, via the orthogonal-system route),
where they are well-defined.

REMARK (packet Q2, first obstruction in the structural whole space).
- s = 1: monomial moments M_2, M_3 exist (x^2, x^3 in H^1).  The DensBC first-order
  recursion M_{2m} = (m/(m-1))M_{2m-2} gives M_{2m} = mM_2, M_{2m+1} = mM_3;
  the first-moment criterion (denseness-criteria Theorem 3, ||x^k||_1 <= C k^{1/2},
  beta = 1/2 < 1) forces M_2 = M_3 = 0.  So the would-be free bases degrees 2,3 are
  KILLED by growth; no first obstruction survives; D* does not exist.
- s >= 2: x^2, x^3 notin H^s (S1), so the moments M_2, M_3 are not even defined as
  H^s-inner-products in H^s itself; density still holds by the uniform proof above
  (there is simply no surviving free base in the structural whole space).

============================================================================
2. STRICT — Structural projection density + characterization of proper V
============================================================================
Theorem L2 (structural projection density).  For any closed V ⊆ H^s,
  P_V(W_s) is dense in V, where W_s = span{p_n}.  Hence span{P_V(p_n) : n in D}
  is dense in V.

Proof.  P_V : H^s -> V is bounded linear surjective; W_s is dense in H^s
(by L1(ii): span{p_n} dense in H^s).  A continuous map sends dense subsets to
dense subsets of the image; hence P_V(W_s) is dense in P_V(H^s) = V.  Since
P_V(span{p_n}) = span{P_V(p_n)}, the result follows.  qed

This is the DensBC O1 Theorem 1 corrected for the left-definite class: the dense
polynomial subspace is W_s = span{p_n} (NOT all of Pi, which is not a subspace of
H^s for s>=2).

COROLLARY L2.1.  closure(span Q_sp) = V iff each excluded projection P_V(p_n)
(p_n notin V) lies in closure(span Q_sp) = closure(span{P_V(p_m): p_m in V}).
Equivalently (DensBC Theorem A) V ∩ Q_sp^perp = {0}.

Theorem L4 (all kept => whole space).  If V ⊆ H^s is closed and {p_n : n in D} ⊆ V,
then V = H^s.  Hence every proper closed V excludes at least one p_n.

Proof.  span{p_n : n in D} ⊆ V, and this span is dense in H^s (L1(ii)); so
H^s = closure(span{p_n}) ⊆ closure(V) = V, and V ⊆ H^s, so V = H^s.  qed

============================================================================
3. STRICT — Transfer descent (the correct moment base for s >= 2)
============================================================================
Theorem L3 (transfer descent).  For integer s >= 2, let K_c : H^s -> H^{s-2} be
the isometric isomorphism (denseness-criteria Lemma 6).  For any closed V ⊆ H^s,
  closure(span{p_n : p_n in V}) = V   (in H^s)
  iff
  closure(span{K_c p_n : K_c p_n in K_c V}) = K_c V   (in H^{s-2}).
Iterating, the constrained-density problem in H^s descends to H^{s'} with
s' in {0,1}.

Proof.  K_c is an isometric linear isomorphism H^s -> H^{s-2} (audited
denseness-criteria Lemma 6).  K_c V is a closed subspace of H^{s-2}.  Since K_c
is injective, p_n in V iff K_c p_n in K_c V.  Isometries preserve linear span,
closures, and subspace equality: closure_Hs(span{p_n in V}) = V  iff
closure_{H^{s-2}}(K_c(span{p_n in V})) = K_c V  iff
closure_{H^{s-2}}(span{K_c p_n : K_c p_n in K_c V}) = K_c V.  Iterating 2r times
reduces H^s to H^0 = L^2 (even s) or H^1 (odd s).  qed

REMARK (moment base; AUDIT-CORRECTED).  The equivalent moment problem is only
clean at a SINGLE descent r = 1 of {K_c p_n}:
- s = 2 (descent to H^0 = L^2): the descended family is {K_c p_n} in L^2; the
  moments of an obstruction g are the L^2-moments mu_k = (g,x^k)_L2 (all defined)
  and satisfy the 3-term jump recursion c mu_{2m} = A_m mu_{2m-2} - B_m mu_{2m-4}
  (free params mu_2, mu_3).  This is exactly the SL_h2 proof.
- s = 3 (descent to H^1): the descended family is {K_c p_n} in H^1; moments are
  the H^1-moments M_k = (w,x^k)_1 (all defined) with the same 3-term jump
  recursion (free params M_2, M_3).  This is exactly the SL_h3 proof.
For s >= 4 the transfer must be iterated; the descended family is K_c^r p_n with
r >= 2, whose monomial expansion has >= 4 terms (e.g. K_c^2 p_{2m} has 4 terms;
upstream SL_denseness_criteria Remark 2.1), so the clean scalar 3-term jump of
Lemma 7 does NOT hold for the iterate in general.  The isometric equivalence
(core L3) remains correct; the residual moment recursion in H^{s'} (s' in {0,1})
is then higher-order in general, which is part of the honest O1'LD core.
The DensBC O1 first-order monomial-moment recursion is NOT directly available in
H^s for s >= 2 (x^2,x^3 absent); the first-order recursion is only directly
legitimate in H^1 (all monomials present).

============================================================================
4. STRICT — Concrete non-density instance in H^2 (first left-definite O1'LD witness)
============================================================================
Theorem L5.  Let H = H^2[-1,1] and V = ker(Delta), Delta f = f(1)-f(-1) (a
bounded linear functional on H^2).  Then Q_sp = {p_0} ∪ {p_{2n} : n >= 2} (the
even sparse polynomials), and closure(span Q_sp) != V.  Explicitly,
  q := p_5 - 2 p_7 = -2x^7 + 4x^5 - 2x^3  satisfies  q in V ∩ Q_sp^perp, q != 0.

Proof.
1. Delta is bounded on H^2: H^2 ⊂ H^1[-1,1] ⊂ C[-1,1] (Sobolev embedding, 1D),
   so |Delta f| <= 2 ||f||_infty <= C ||f||_{H^2}.  Hence V = ker(Delta) is a
   closed subspace (kernel of a bounded functional), codim 1 (Delta(p_1) = 2 != 0).
2. Q_sp = even sparse family:
   - Even p_n (p_0, p_{2n}, n>=2): even functions => p_n(1)=p_n(-1) => Delta p_n = 0
     => p_n in V.
   - Odd p_n (p_1, p_{2n+1}): Delta = 2 p_n(1).  p_1(1) = 1 (Delta = 2).
     For n>=2, p_{2n+1}(1) = 1 - (n/(n-1)) = -1/(n-1) != 0 (documented BC
     computation), so Delta p_{2n+1} = -2/(n-1) != 0 => p_{2n+1} notin V.
   Hence Q_sp = {p_0} ∪ {p_{2n} : n >= 2}.
3. q in V: q = p_5 - 2p_7 in H^2 (finite combination of H^2 polynomials), q odd,
   Delta q = 2 q(1) = 2(p_5(1) - 2 p_7(1)) = 2( (-1) - 2(-1/2) ) = 0.  So q in V.
   q != 0 (explicitly -2x^7+4x^5-2x^3, exact-verified).
4. q in Q_sp^perp: q is odd; every element of Q_sp is even.  The H^2 inner product
   is parity-orthogonal: for f even, g odd, (f,g)_2 = 0 because the crossed
   integrands f''g'', f'g', fg are all odd (integrate to 0) and Delta f = 0
   (even) kills the boundary term.  Hence q ⊥ p_n for every even p_n in Q_sp.
5. By DensBC Theorem A, a nonzero q in V ∩ Q_sp^perp implies closure(span Q_sp)
   != V.  qed

REMARK.  This is the first concrete left-definite witness that a natural bounded
structural/functional constraint can DESTROY density: the constraint excludes
all odd p_n from the candidate, which are then orthogonally silent (parity) and
can never be recaptured, while V also contains odd functions with Delta = 0
(such as q) that are not in the even span.  The obstruction is detected by
finite data (parity + boundary value), so this instance is finite-data decidable.

============================================================================
5. STRICT — Honest status of O1' in the left-definite class (packet Q1)
============================================================================
Theorem L6 (status of O1' in the class).
(1) For V = H^s (whole structural space), O1' is DECIDED: there is no surviving
    free base and density holds (Theorem L1); the decision is "dense", finite and
    proved for all integer s >= 1 and all c > 0.
(2) For a general proper closed V ⊆ H^s, Theorem L3 descends the problem to
    H^{s'} (s' in {0,1}), where all monomials and inner products are well-defined.
    For a SINGLE descent (s = 2 to L^2, or s = 3 to H^1) the descended family
    {K_c p_n} satisfies the 3-term jump recursion with free parameters
    (mu_2, mu_3 in L^2; M_2, M_3 in H^1); for s >= 4 the transferred family
    K_c^r p_n has >= 4 monomial terms and the recursion is higher-order (see L3
    Remark), which is part of the honest O1'LD core.
(3) Finite-data decidability in H^{s'}: by DensBC O1 Theorem 5 (audited), the
    core is finite/structured exactly when the membership equations are finite
    moment equations AND the relevant moment data are banded/diagonal.  In the
    class, the H^1 moment matrix <x^i,x^k>_1 is NON-diagonal (exact-verified;
    e.g. <x^1,x^3>_1 = 2c/5 != 0, and (p_4,p_6)_1 = 128/105 + 181c/693 != 0),
    so the DensBC O1 Theorem 5 sufficient condition is NOT automatic; the general
    decision remains a genuine moment problem.  (NOTE: in H^s for s >= 2 the only
    monomials present are 1 and x with (1,x)_s = 0, so the monomial moment block
    "inside H^s" is vacuous/trivial and carries no obstruction data; the
    non-trivial non-diagonality that blocks finiteness lives in H^1.)
(4) Hence O1'LD := "given proper closed V ⊆ H^s, decide whether some free
    run-base / jump-free parameter admits a nonzero realization in V" remains
    OPEN for general proper V; it is decided for V = H^s and for concrete
    instances such as Theorem L5 (and all density/non-density witnesses thereof).

Proof.  (1) from Theorem L1.  (2) from Theorem L3 + DensBC O1 Theorems 2-5.
(3) DensBC O1 Theorem 5 (audited) + exact-verified non-diagonality of the H^1
moment matrix (F1 in reproducibility; <x^1,x^3>_1 = 2c/5 != 0).  For s >= 2 the
monomial block inside H^s is vacuous (only 1,x present), which does NOT provide
banded/diagonal structure for the transferred L^2/H^1 moment problem.
(4) is a summary of (1)-(3); no closed form is claimed for general V.  qed

============================================================================
6. Regression checks (STRICT statements only)
============================================================================
- L1 with V = H^s and s = 2 recovers the H^2 completeness theorem (SL_h2):
  span{p_n} dense in H^2.  CONSISTENT.
- L1 with s = 1 recovers H^1 completeness (denseness-criteria Cor 3, beta<1).
  CONSISTENT.
- L2 with V = H^s reduces to "W_s dense in H^s" (L1(ii)).  CONSISTENT.
- L4 with the DensBC O1 setting (H contains all Pi) reduces to the trivial fact
  that if every p_n in V and Pi dense then V = H.  CONSISTENT.
- L3 with s = 2 (descent to L^2 with {K_c p_n}) matches the H^2 proof structure
  (transfer to L^2).  CONSISTENT.
- L5 does not contradict the project's whole-space completeness: it concerns a
  PROPER constrained V = ker(Delta), not V = H^2.  CONSISTENT.
- No claim of a closed-form criterion for general proper V is made; O1'LD open.

============================================================================
7. Reduced open core (honest)
============================================================================
O1'LD (this run's reduced core): for a general proper closed V ⊆ H^s[-1,1]
(constraint given by bounded structure/functionals), decide whether
closure(span{p_n in V}) = V, i.e. whether the descended obstruction space
(in H^{s'}, s' in {0,1}) contains a nonzero element with the prescribed
moments while lying in the descended constraint K_c^r V.  This is a genuine
moment/membership problem in general (non-diagonal H^1 moment matrix); it is
decided for V = H^s and for concrete finite-data instances such as Theorem L5.
O2' (inherited, open): full characterization of which constraints guarantee
density for all c in non-coordinate left-definite H.
O3 (inherited, open): fractional window 3/2 <= s < 2.
