# Problem contract: n=1 adjacent gap extremals (box class)

## Normalized statement

Let R > 1. Dirichlet vibrating string on [0,1]:

    -y''(x) = lambda rho(x) y(x),  y(0) = y(1) = 0,
    rho measurable, 1 <= rho(x) <= R a.e.

Let 0 < lambda_1(rho) < lambda_2(rho) be the first two eigenvalues
(simple; k-th eigenfunction has exactly k-1 interior zeros).

Define  D(rho) := lambda_2(rho) - lambda_1(rho).

Problem SUP:  compute  S(R) := sup { D(rho) : 1 <= rho <= R }  and
              characterize all maximizers.
Problem INF:  compute  I(R) := inf { D(rho) : 1 <= rho <= R }  and
              characterize all minimizers.

## Conjecture (from numerics; target of this run)

SUP: S(R) is attained by the symmetric single-barrier 3-block density
     rho^sup_u = 1 on [0,u] cup [1-u,1],  R on (u, 1-u),
     at the unique u* = u*_sup(R) in (0,1/2) satisfying the
     self-consistency equation  f(u) = 0, where
     f := lambda_1 u_1^2 - lambda_2 u_2^2  (u_k = L^2(rho)-normalized).
     Equivalently d/du D(rho^sup_u) = -2(R-1) f(u) has a unique
     sign change - to + in (0,1/2), so u* is the unique maximizer of
     the symmetric family.

INF: I(R) is attained by the symmetric single-well 3-block density
     rho^inf_u = R on [0,u] cup [1-u,1],  1 on (u,1-u),
     at the unique u* = u*_inf(R) solving the same f(u) = 0 equation
     (different config), with d/du D(rho^inf_u) = +2(R-1) f(u).

## Numerics to be matched (R=4, high precision)

SUP: u* = 0.45148546584, lambda_1 = 6.109280, lambda_2 = 38.723263,
     D* = 32.6139836177  (3 pi^2 = 29.608813)
INF: u* = 0.3825982568, lambda_1 = 3.628360, lambda_2 = 10.412842,
     D* = 6.7844823391  (3 pi^2 / R = 7.402203)

## Completion criteria

A complete solution must:

1. Prove the reduction: for every admissible rho,
     D(rho) <= max over barrier family  and  D(rho) >= min over well family,
   where
     barrier family = { rho = R on (a,b), 1 elsewhere, 0<=a<=b<=1 },
     well family    = { rho = 1 on (a,b), R elsewhere, 0<=a<=b<=1 }.
   (Equality of sup/inf with sup/inf over the respective 2-parameter
   families suffices.)
2. Prove that within each family the extremum is attained at the
   symmetric configuration b = 1 - a (or explicitly handle the
   boundary of the family).
3. Prove that in the symmetric 1-parameter family the self-consistent
   point u* exists, is unique, and is the unique global extremum of the
   restricted functional (single sign change of f).
4. Optionally: closed-form or sharp comparison of the extremal values
   with 3 pi^2 and 3 pi^2 / R.

## Results that do NOT count as completion

- Numerical evidence for any of the above (recorded separately).
- A proof for a different constraint class (e.g. bounded number of
  jumps, L^p balls, fixed mass) unless a rigorous transfer is given.
- A proof assuming symmetry of the maximizer a priori.
- Partial results on lambda_2/lambda_1 ratio instead of the gap.

## Boundary and degenerate cases

- R -> 1+ : both families degenerate to rho = 1; D -> 3 pi^2.
- R -> infinity : SUP u* -> 1/2, D -> 4 pi^2; INF u* -> ~0.3299,
  D* R -> 24.943866 (numerical).
- Degenerate 2-block members (a=0 or b=1) and constant members
  (a=b, or a=0,b=1) are inside the closed families and must be
  covered by the analysis.
- The function f may vanish identically at no point except possibly
  the two jump points; measure-zero changes of rho do not change
  eigenvalues.

## Permitted outcomes

- affirmative proof (complete, with all obligations closed and an
  independent audit);
- counterexample (off-center or asymmetric maximizer, or inf not
  attained, with certificate);
- rigorous partial result (e.g. the reduction alone, or reduction +
  symmetric 1-parameter analysis) with exact remaining gap stated.

## Tool, citation, and search constraints

- Theorems cited must be rechecked against primary sources:
  Keller 1976 (SIAM J. Appl. Math. 31), Mahar-Willner 1976 (CPAM 29),
  Ahrami-El Allali-Harrell 2024 (arXiv:2407.02459), Cheng-Kung-Law-
  Lian 2010 (CAMWA 60), Ashbaugh-Benguria 1989 (PAMS 105).
- Computation is evidence only; every computational claim needs a
  proof bridge or a certificate.
- No use of protected/private chain-of-thought; all claims must be
  externally checkable.

## Contract audit

Conducted by the coordinator against the task packet
Q-20260805-gapn1-proof-9F31D0 and docs/SL_gap_extremals.tex.
The statement above matches the packet source wording (open problem 3).
No quantifier or constraint class was changed.
