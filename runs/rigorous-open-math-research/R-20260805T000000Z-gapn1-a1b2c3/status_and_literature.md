# Status and literature

## Current status of the target problem

KNOWN: none of the papers below settles the box class
1 <= rho <= R (unbounded number of jumps) for lambda_2 - lambda_1.

## Verified relevant results (with sources)

1. Feynman-Hellmann / eigenvalue derivative.  For a one-parameter
   family rho_eps with d/d eps rho in L^1 and 1 <= rho_eps <= R:
     d/d eps lambda_k(rho_eps) = -lambda_k int (d/d eps rho) u_k^2 dx
   where u_k is L^2(rho)-normalized.
   Source: AEH arXiv:2407.02459v2, Lemma 2.1 (with V=0, p=1).  The
   argument is standard Kato perturbation theory; eigenvalues of the
   1D problem are simple.

2. Monotonicity of u_2/u_1 (Wronskian argument).  For any positive
   bounded measurable rho (not just the classes in AEH), with
   u_k = k-th normalized eigenfunction and z_0 the unique zero of u_2:
     W := u_1 u_2' - u_1' u_2 satisfies
     W' = (lambda_1 - lambda_2) rho u_1 u_2,
     W(0) = W(1) = 0,  W < 0 on (0,1),
   hence v := u_2/u_1 is strictly decreasing on (0,1) with v(z_0) = 0.
   Consequence: f := lambda_1 u_1^2 - lambda_2 u_2^2 has at most two
   zeros, and {f > 0} is a single interval containing z_0.
   Source: AEH Lemma 2.2 items (1),(4),(5); the rho-independence of
   the Wronskian computation was re-derived in this run (ledger).

3. Bang-bang structure (variational).  At a global maximizer of D
   over 1 <= rho <= R: rho = R on {f>0}, rho = 1 on {f<0} a.e.
   At a global minimizer: rho = 1 on {f>0}, rho = R on {f<0}.
   This is a direct consequence of (1); it is also Prop 2.1 /
   Cor 2.2 in docs/SL_gap_extremals.tex (project derivation).

4. Ratio analogue (context).  sup over rho of lambda_{n+1}/lambda_n
   for the box class was proved in this project (session 5) using the
   Keller variational conditions and the Mahar-Willner periodic
   extension identity; see docs/SL_ratio_proof.pdf.  The methods
   (Keller Theorem 0 reduction to piecewise constant; MW Lemma 2
   periodic extension; balanced phase) are leads for the gap problem
   but do NOT transfer directly: the gap is not scale invariant.

## Literature landscape (checked 2026-08-05)

- Ashbaugh-Benguria 1989 (PAMS 105 419-424): gap lower bound for
  Schrodinger with symmetric single-well V; different class (V, not
  weight; lower bound, not upper).
- Lavine 1994 (PAMS 121 815-821): convex V minimizes gap (Dirichlet
  and Neumann); different class.
- El Allali-Harrell 2022 (PAMS 150 57-87): direct optimization for
  single-well V, sharp lower bound gamma > 2.04575; V-class.
- AEH 2024 (arXiv:2407.02459): single-barrier weight class with
  monotonicity constraint (Definition 3.2: w non-decreasing then
  non-increasing); minimizes the gap over that class.  Our box class
  is NOT a subclass (box does not force monotone rearrangement), and
  AEH target the minimum, not the maximum.  Lemma 2.2 is class-free.
- Cheng-Kung-Law-Lian 2010 (CAMWA 60): dual eigenvalue problems,
  symmetrization via Wronskian comparison; template for forcing
  symmetric extremizers.
- Keller 1976, Mahar-Willner 1976, Willner-Mahar 1982: ratio
  extremals for box class with bounded jumps; two-jump symmetric
  extremizers.  Structural template; gap analogue open.
- Huang 2007 (Acta Math. Hungar. 117): eigenvalue gap for vibrating
  strings with symmetric densities (assumes symmetry).
- Sun 2022 (JMAA 516, 126513): "On the minimum eigenvalue gap for
  vibrating string"; abstract only; class = bounded number of jumps
  (not the pure box class).  Full text unavailable.
- Horvath 2002, Horvath-Kiss 2006: ratio bounds for Schrodinger
  single-well; not the gap maximum for box class.

## Novelty risk

The reduction (sup/inf over box class = sup/inf over 2-parameter
barrier/well families) is, to the best of our knowledge and search
coverage, not in the literature in this form.  The final 2-parameter
extremal statement (symmetric 3-block) matches the numerical pattern
and the MW/Keller template, but we have not found a published proof
for the pure box class.  Novelty classification: POTENTIALLY_NEW /
UNKNOWN pending the literature audit in Phase 11.
