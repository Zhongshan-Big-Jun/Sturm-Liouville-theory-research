# Obligation graph

Root: THEOREM_SUP (S(R) = D_sym^sup(u*) at unique u*) and THEOREM_INF.

O1  Attainment and reduction to 2-parameter families.
    Statement: S(R) = max over barrier family B = {rho=R on (a,b), 1 else,
    0<=a<=b<=1}; I(R) = min over well family W = {rho=1 on (a,b), R else}.
    Method (PROVED, write-up pending): (i) L^1-continuity of lambda_k on
    {1<=rho<=R}; (ii) step-function density; (iii) N-jump maximizer rho^N
    exists (compactness), M_N increases to S(R); (iv) at rho^N each real
    jump point is a zero of f_N (FH derivative wrt jump point), and f_N
    has at most 2 zeros (Wronskian monotonicity, AEH Lemma 2.2 re-derived),
    hence rho^N has at most 2 jumps; (v) sup over <=2-jump [1,R]-valued
    family attained at rho~; (vi) rho~ is a global extremizer of the full
    class, hence bang-bang (values in {1,R}); (vii) with {f>0} a single
    interval, SUP extremizer is a barrier config and INF extremizer a well
    config.  Status: PROVED (draft), obligations O1a-O1f below.
      O1a  lambda_k continuous in L^1 on {1<=rho<=R}.  OPEN (standard; cite).
      O1b  FH derivative wrt moving a jump point is (c_{j+1}-c_j) f(x_j).
           PROVED by L^1 perturbation + continuity of eigenfunctions.
      O1c  f = lambda_1 u_1^2 - lambda_2 u_2^2 has at most 2 zeros and
           {f>0} is one interval.  PROVED (Wronskian; rho-independent).
      O1d  Compactness of N-jump family and existence of rho^N.
           PROVED (closed simplex x [1,R]^{N+1}, continuous map).
      O1e  M_N -> S(R).  PROVED (step functions dense + continuity).
      O1f  Bang-bang at a global extremizer.  PROVED (FH one-sided).
    Status: PROVED (draft in research_ledger, final write-up pending).

O2  Symmetric family analysis (1-parameter).
    For rho^sup_u (symmetric barrier, jump u) define f_sym(u)=f(u;rho_u).
    Claim: f_sym has a unique zero u* in (0,1/2), sign - on (0,u*),
    + on (u*,1/2).  Then D_sym strictly increases then decreases, max at u*.
    Reformulation: g(u) = s_2 sin(s_2 u) - s_1 sin(s_1 u) has unique zero,
    sign + then -; s_k = eigenvalues of the half-problem (even/odd modes).
    Status: OPEN.  Partial: g(0+)=0 with g>0 near 0 (g'(0)>0); g(1/2)<0.
    Sub-obligations:
      O2a  s_1, s_2 (half-problem) are C^1 and increasing in u.
           PROVED: pointwise rho monotonicity + FH formula.
      O2b  h(u) := g(u)/u strictly decreasing on (0,1/2).  OPEN (main
           estimate; sinc + drift competition).
      O2c  Endpoint asymptotics used in O2b.  PROVED.
    Same statements for the well family rho^inf_u (f_sym^inf(u)=f(u;rho_u)
    with the well config; sign pattern reversed in the derivative).

O3  2-parameter extremum (the crux).
    For the barrier family, any sign-consistent interior critical point
    (f(a)=f(b)=0, sign pattern -,+,+) satisfies b = 1 - a.  If this holds,
    O2 gives the global max (boundary of B handled by O3b).
    Status: OPEN.  Routes in approach_registry.md (A-D).
      O3a  Uniqueness (up to reflection) of sign-consistent critical points.
           PARTIAL (Agent B, agentB_O3a_fixed_point.md).  Proved: T1 (fixed points = sign-consistent c.p.),
           T2 (sigma-equivariance; uniqueness implies b = 1 - a), T3 (dR1/db = -dR2/da, FH + Schwarz),
           T4 (reduction to branch lemmas).  Numerics: unique good root for all R in {1.02..1000};
           gap = Lemma A (g1' > g2' on common range) + B (h endpoint signs) + C (coverage).
      O3b  Boundary of B: 2-block configs and constant configs give
           D <= D_sym(u*); same for W.  OPEN (numerics support; needs a
           clean inequality; possibly via O2 asymptotics or ratio bounds).

O4  Synthesis + independent audit.  OPEN.

O5  Novelty audit.  OPEN.

## Dependencies
THEOREM_SUP = O1 + O3(sup variant) + O2 + O4
THEOREM_INF = O1 + O3(inf variant) + O2 + O4
O3 depends on O1c (zeros of f) and O2 (symmetric family critical point).
O2 depends on O1c (for endpoint/derivative identities).

## Status legend
OPEN | PARTIAL | PROVED | FORMALIZED | REFUTED | BLOCKED
